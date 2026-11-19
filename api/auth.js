// 회원가입·로그인 (Vercel 서버리스 함수 + Neon Postgres)
//  POST /api/auth  { action: 'signup' | 'login' | 'google' | 'config' | 'me' | 'logout' | 'delete'
//                   | 'password' | 'admin_list' | 'admin_reset' | 'admin_delete', ... }
//  · 관리자: Vercel 환경변수 ADMIN_EMAILS(쉼표로 구분)에 든 이메일의 '구글 로그인' 계정만 관리자다.
//    아이디 가입 때 적는 이메일은 확인되지 않은 값이라 관리자 판정에 쓰지 않는다.
//  · 구글 로그인: Vercel 환경변수 GOOGLE_CLIENT_ID 가 있을 때만 켜진다. 구글이 서명한 ID 토큰을 구글 서버에 확인받아 쓴다.
//  · 비밀번호는 scrypt(솔트 포함)로 해시해 저장하고, 원문은 어디에도 남기지 않는다.
//  · 로그인 토큰은 임의의 32바이트. DB에는 SHA-256 해시만 저장한다.
//  · 수집 항목: 아이디, 비밀번호(해시), 닉네임, 학년 구분 (필수) / 이메일, 학교, 선택과목 (선택)
const { neon } = require('@neondatabase/serverless');
const crypto = require('crypto');

const GRADES = ['고1', '고2', '고3', 'N수', '교사', '기타'];
const ELECTIVES = ['', '미적분', '확률과 통계', '기하'];
const SESSION_DAYS = 180;
let ready = false;

const sha = s => crypto.createHash('sha256').update(s).digest('hex');
function hashPw(pw, salt) {
  salt = salt || crypto.randomBytes(16).toString('hex');
  return salt + ':' + crypto.scryptSync(pw, salt, 32).toString('hex');
}
function checkPw(pw, stored) {
  const [salt, h] = String(stored).split(':');
  if (!salt || !h) return false;
  const a = Buffer.from(h, 'hex'), b = crypto.scryptSync(pw, salt, 32);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
const clean = (v, max) => String(v == null ? '' : v).replace(/[\u0000-\u001f<>]/g, '').trim().slice(0, max);
const adminEmails = () => String(process.env.ADMIN_EMAILS || '').toLowerCase().split(/[\s,]+/).filter(Boolean);
const isAdmin = u => !!(u && u.google_sub && u.email && adminEmails().includes(String(u.email).toLowerCase()));
const pub = u => ({ uid: u.uid, nick: u.nick, grade: u.grade, email: u.email || '', school: u.school || '', elective: u.elective || '', google: !!u.google_sub, admin: isAdmin(u) });
// 임시 비밀번호: 헷갈리는 글자(0·o·1·l·i)를 뺀 10자
const tempPw = () => { const A = 'abcdefghjkmnpqrstuvwxyz23456789'; let s = ''; for (let i = 0; i < 10; i++) s += A[crypto.randomInt(A.length)]; return s; };
// 구글 ID 토큰 확인: 구글 tokeninfo 가 서명·만료를 검사해 준다. 우리 사이트용으로 발급된 토큰인지(aud)는 여기서 확인한다.
async function verifyGoogle(credential, clientId) {
  if (!credential || typeof credential !== 'string' || credential.length > 4096) return null;
  const r = await fetch('https://oauth2.googleapis.com/tokeninfo?id_token=' + encodeURIComponent(credential));
  if (!r.ok) return null;
  const t = await r.json();
  if (t.aud !== clientId) return null;
  if (t.iss !== 'accounts.google.com' && t.iss !== 'https://accounts.google.com') return null;
  if (!t.sub || Number(t.exp) * 1000 < Date.now()) return null;
  return { sub: String(t.sub), email: String(t.email_verified) === 'true' ? String(t.email || '') : '', name: String(t.given_name || t.name || '') };
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.status(405).json({ error: 'POST only' }); return; }
  const dbUrl = process.env.DATABASE_URL || process.env.POSTGRES_URL;
  if (!dbUrl) { res.status(503).json({ error: 'account store not connected' }); return; }
  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch (e) { b = null; } }
  if (!b || typeof b !== 'object') { res.status(400).json({ error: 'bad request', msg: '요청 형식이 올바르지 않아요.' }); return; }
  const sql = neon(dbUrl);
  const bad = (msg, code) => res.status(code || 400).json({ error: 'invalid', msg });

  try {
    if (!ready) {
      await sql`CREATE TABLE IF NOT EXISTS km_user (
        id BIGSERIAL PRIMARY KEY, uid TEXT NOT NULL UNIQUE, pw TEXT NOT NULL, nick TEXT NOT NULL, grade TEXT NOT NULL,
        email TEXT, school TEXT, elective TEXT, agreed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(), last_login TIMESTAMPTZ, fails INT NOT NULL DEFAULT 0, locked_until TIMESTAMPTZ)`;
      await sql`CREATE TABLE IF NOT EXISTS km_session (
        tok TEXT PRIMARY KEY, user_id BIGINT NOT NULL REFERENCES km_user(id) ON DELETE CASCADE, created_at TIMESTAMPTZ NOT NULL DEFAULT now())`;
      await sql`ALTER TABLE km_user ADD COLUMN IF NOT EXISTS google_sub TEXT UNIQUE`;
      await sql`ALTER TABLE km_user ALTER COLUMN pw DROP NOT NULL`;
      ready = true;
    }
    const gid = process.env.GOOGLE_CLIENT_ID || '';
    const newSession = async userId => {
      const tok = crypto.randomBytes(32).toString('hex');
      await sql`INSERT INTO km_session (tok, user_id) VALUES (${sha(tok)}, ${userId})`;
      return tok;
    };
    const userOf = async tok => {
      if (!tok || typeof tok !== 'string' || tok.length > 200) return null;
      const r = await sql`SELECT u.* FROM km_session s JOIN km_user u ON u.id = s.user_id
        WHERE s.tok = ${sha(tok)} AND s.created_at > now() - make_interval(days => ${SESSION_DAYS})`;
      return r[0] || null;
    };
    const action = b.action;

    if (action === 'signup') {
      const uid = String(b.uid || '').trim().toLowerCase();
      const pw = String(b.pw || '');
      const nick = clean(b.nick, 20), grade = String(b.grade || '');
      const email = clean(b.email, 100), school = clean(b.school, 40), elective = String(b.elective || '');
      if (!/^[a-z0-9_]{4,20}$/.test(uid)) return bad('아이디는 영문 소문자·숫자·밑줄(_) 4~20자로 만들어 주세요.');
      if (pw.length < 8 || pw.length > 72) return bad('비밀번호는 8자 이상으로 만들어 주세요.');
      if (!nick) return bad('닉네임을 입력해 주세요.');
      if (!GRADES.includes(grade)) return bad('학년 구분을 골라 주세요.');
      if (!ELECTIVES.includes(elective)) return bad('선택과목 값이 올바르지 않아요.');
      if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return bad('이메일 형식이 올바르지 않아요.');
      if (b.agree14 !== true || b.agreePrivacy !== true) return bad('만 14세 이상 확인과 개인정보 수집·이용 동의가 필요해요.');
      const rows = await sql`INSERT INTO km_user (uid, pw, nick, grade, email, school, elective, last_login)
        VALUES (${uid}, ${hashPw(pw)}, ${nick}, ${grade}, ${email || null}, ${school || null}, ${elective || null}, now())
        ON CONFLICT (uid) DO NOTHING RETURNING *`;
      if (!rows.length) return bad('이미 쓰고 있는 아이디예요. 다른 아이디를 골라 주세요.', 409);
      res.status(200).json({ ok: true, token: await newSession(rows[0].id), user: pub(rows[0]) }); return;
    }

    if (action === 'config') { res.status(200).json({ ok: true, googleClientId: gid }); return; }

    if (action === 'google') {
      if (!gid) return bad('구글 로그인이 아직 설정되지 않았어요.', 503);
      const g = await (module.exports._verifyGoogle || verifyGoogle)(b.credential, gid);
      if (!g) return bad('구글 계정을 확인하지 못했어요. 다시 시도해 주세요.', 401);
      const ex = await sql`SELECT * FROM km_user WHERE google_sub = ${g.sub}`;
      if (ex[0]) {
        await sql`UPDATE km_user SET last_login = now() WHERE id = ${ex[0].id}`;
        res.status(200).json({ ok: true, token: await newSession(ex[0].id), user: pub(ex[0]) }); return;
      }
      // 처음 온 구글 계정: 닉네임·학년·동의를 받아야 가입된다. 아직 안 받았으면 그 화면을 띄우라고 알려 준다.
      if (b.nick == null && b.grade == null) { res.status(200).json({ need: 'profile', suggest: clean(g.name, 20) }); return; }
      const nick = clean(b.nick, 20), grade = String(b.grade || ''), school = clean(b.school, 40), elective = String(b.elective || '');
      if (!nick) return bad('닉네임을 입력해 주세요.');
      if (!GRADES.includes(grade)) return bad('학년 구분을 골라 주세요.');
      if (!ELECTIVES.includes(elective)) return bad('선택과목 값이 올바르지 않아요.');
      if (b.agree14 !== true || b.agreePrivacy !== true) return bad('만 14세 이상 확인과 개인정보 수집·이용 동의가 필요해요.');
      const uid = 'g_' + sha(g.sub).slice(0, 14);
      const rows = await sql`INSERT INTO km_user (uid, pw, nick, grade, email, school, elective, google_sub, last_login)
        VALUES (${uid}, ${null}, ${nick}, ${grade}, ${g.email || null}, ${school || null}, ${elective || null}, ${g.sub}, now())
        ON CONFLICT DO NOTHING RETURNING *`;
      if (!rows.length) return bad('가입을 처리하지 못했어요. 다시 시도해 주세요.', 409);
      res.status(200).json({ ok: true, token: await newSession(rows[0].id), user: pub(rows[0]) }); return;
    }

    if (action === 'login') {
      const uid = String(b.uid || '').trim().toLowerCase(), pw = String(b.pw || '');
      if (!uid || !pw) return bad('아이디와 비밀번호를 입력해 주세요.');
      const r = await sql`SELECT *, (locked_until IS NOT NULL AND locked_until > now()) AS locked FROM km_user WHERE uid = ${uid}`;
      const u = r[0];
      if (u && u.locked) return bad('로그인 시도가 너무 많았어요. 5분 뒤에 다시 해 주세요.', 429);
      if (!u || !u.pw || !checkPw(pw.slice(0, 72), u.pw)) {
        if (u) await sql`UPDATE km_user SET fails = fails + 1,
          locked_until = CASE WHEN fails + 1 >= 5 THEN now() + interval '5 minutes' ELSE locked_until END WHERE id = ${u.id}`;
        return bad('아이디 또는 비밀번호가 맞지 않아요.', 401);
      }
      await sql`UPDATE km_user SET fails = 0, locked_until = NULL, last_login = now() WHERE id = ${u.id}`;
      if (Math.random() < 0.05) await sql`DELETE FROM km_session WHERE created_at < now() - make_interval(days => ${SESSION_DAYS})`;
      res.status(200).json({ ok: true, token: await newSession(u.id), user: pub(u) }); return;
    }

    if (typeof action === 'string' && action.startsWith('admin_')) {
      const u = await userOf(b.token);
      if (!u) { res.status(401).json({ error: 'not signed in', msg: '로그인이 만료되었어요. 다시 로그인해 주세요.' }); return; }
      if (!isAdmin(u)) return bad('관리자만 쓸 수 있어요.', 403);
      if (action === 'admin_list') {
        const rows = await sql`SELECT id, uid, nick, grade, email, school, elective, created_at, last_login,
          (google_sub IS NOT NULL) AS google, (locked_until IS NOT NULL AND locked_until > now()) AS locked
          FROM km_user ORDER BY created_at DESC LIMIT 5000`;
        const week = Date.now() - 7 * 864e5, grade = {}, elective = {}, via = { '구글': 0, '아이디': 0 };
        GRADES.forEach(g => { grade[g] = 0; });
        ['미적분', '확률과 통계', '기하', '미선택'].forEach(e => { elective[e] = 0; });
        const users = rows.map(r => {
          grade[r.grade] = (grade[r.grade] || 0) + 1;
          const e = r.elective || '미선택'; elective[e] = (elective[e] || 0) + 1;
          via[r.google ? '구글' : '아이디']++;
          return { id: String(r.id), uid: r.uid, nick: r.nick, grade: r.grade, email: r.email || '', school: r.school || '', elective: r.elective || '',
            created_at: r.created_at, last_login: r.last_login, google: !!r.google, locked: !!r.locked, self: String(r.id) === String(u.id) };
        });
        const stats = { total: users.length, week: rows.filter(r => new Date(r.created_at).getTime() > week).length, grade, elective, via };
        res.status(200).json({ ok: true, users, stats }); return;
      }
      const id = String(b.id == null ? '' : b.id);
      if (!/^\d{1,18}$/.test(id)) return bad('대상 회원이 올바르지 않아요.');
      const t = (await sql`SELECT id, uid, google_sub FROM km_user WHERE id = ${id}`)[0];
      if (!t) return bad('이미 없는 회원이에요. 목록을 새로고침해 주세요.', 404);
      if (action === 'admin_reset') {
        if (t.google_sub) return bad('구글로 가입한 계정은 비밀번호가 없어요.');
        const temp = tempPw();
        await sql`UPDATE km_user SET pw = ${hashPw(temp)}, fails = 0, locked_until = NULL WHERE id = ${t.id}`;
        await sql`DELETE FROM km_session WHERE user_id = ${t.id}`;   // 이 계정의 다른 기기 로그인도 풀린다
        res.status(200).json({ ok: true, temp }); return;
      }
      if (action === 'admin_delete') {
        if (String(t.id) === String(u.id)) return bad('관리자 본인 계정은 여기서 지울 수 없어요.');
        await sql`DELETE FROM km_user WHERE id = ${t.id}`;
        res.status(200).json({ ok: true }); return;
      }
      return bad('알 수 없는 요청이에요.');
    }

    if (action === 'me' || action === 'logout' || action === 'delete' || action === 'password') {
      const u = await userOf(b.token);
      if (!u) { res.status(401).json({ error: 'not signed in', msg: '로그인이 만료되었어요. 다시 로그인해 주세요.' }); return; }
      if (action === 'me') { res.status(200).json({ ok: true, user: pub(u) }); return; }
      if (action === 'logout') { await sql`DELETE FROM km_session WHERE tok = ${sha(b.token)}`; res.status(200).json({ ok: true }); return; }
      // 비밀번호 바꾸기: 현재 비밀번호를 확인한다. 다른 기기의 로그인은 풀고, 지금 기기는 그대로 둔다
      if (action === 'password') {
        if (!u.pw) return bad('구글로 가입한 계정은 비밀번호가 없어요.');
        if (!checkPw(String(b.pw || '').slice(0, 72), u.pw)) return bad('현재 비밀번호가 맞지 않아요.', 401);
        const np = String(b.newPw || '');
        if (np.length < 8 || np.length > 72) return bad('새 비밀번호는 8자 이상으로 만들어 주세요.');
        await sql`UPDATE km_user SET pw = ${hashPw(np)}, fails = 0, locked_until = NULL WHERE id = ${u.id}`;
        await sql`DELETE FROM km_session WHERE user_id = ${u.id} AND tok <> ${sha(b.token)}`;
        res.status(200).json({ ok: true }); return;
      }
      // 회원 탈퇴: 본인 확인을 위해 비밀번호를 다시 받고, 계정과 모든 로그인 기록을 지운다
      if (u.pw && !checkPw(String(b.pw || '').slice(0, 72), u.pw)) return bad('비밀번호가 맞지 않아요.', 401);   // 구글 가입 계정은 비밀번호가 없어 로그인 상태만 확인
      await sql`DELETE FROM km_user WHERE id = ${u.id}`;
      res.status(200).json({ ok: true }); return;
    }

    bad('알 수 없는 요청이에요.');
  } catch (e) {
    console.error('auth:', e && e.message);
    res.status(502).json({ error: 'account store error' });
  }
};
