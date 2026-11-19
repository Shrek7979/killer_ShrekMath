// 회원가입·로그인 (Vercel 서버리스 함수 + Neon Postgres)
//  POST /api/auth  { action: 'signup' | 'login' | 'me' | 'logout' | 'delete', ... }
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
const pub = u => ({ uid: u.uid, nick: u.nick, grade: u.grade, email: u.email || '', school: u.school || '', elective: u.elective || '' });

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
      ready = true;
    }
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

    if (action === 'login') {
      const uid = String(b.uid || '').trim().toLowerCase(), pw = String(b.pw || '');
      if (!uid || !pw) return bad('아이디와 비밀번호를 입력해 주세요.');
      const r = await sql`SELECT *, (locked_until IS NOT NULL AND locked_until > now()) AS locked FROM km_user WHERE uid = ${uid}`;
      const u = r[0];
      if (u && u.locked) return bad('로그인 시도가 너무 많았어요. 5분 뒤에 다시 해 주세요.', 429);
      if (!u || !checkPw(pw.slice(0, 72), u.pw)) {
        if (u) await sql`UPDATE km_user SET fails = fails + 1,
          locked_until = CASE WHEN fails + 1 >= 5 THEN now() + interval '5 minutes' ELSE locked_until END WHERE id = ${u.id}`;
        return bad('아이디 또는 비밀번호가 맞지 않아요.', 401);
      }
      await sql`UPDATE km_user SET fails = 0, locked_until = NULL, last_login = now() WHERE id = ${u.id}`;
      if (Math.random() < 0.05) await sql`DELETE FROM km_session WHERE created_at < now() - make_interval(days => ${SESSION_DAYS})`;
      res.status(200).json({ ok: true, token: await newSession(u.id), user: pub(u) }); return;
    }

    if (action === 'me' || action === 'logout' || action === 'delete') {
      const u = await userOf(b.token);
      if (!u) { res.status(401).json({ error: 'not signed in', msg: '로그인이 만료되었어요. 다시 로그인해 주세요.' }); return; }
      if (action === 'me') { res.status(200).json({ ok: true, user: pub(u) }); return; }
      if (action === 'logout') { await sql`DELETE FROM km_session WHERE tok = ${sha(b.token)}`; res.status(200).json({ ok: true }); return; }
      // 회원 탈퇴: 본인 확인을 위해 비밀번호를 다시 받고, 계정과 모든 로그인 기록을 지운다
      if (!checkPw(String(b.pw || '').slice(0, 72), u.pw)) return bad('비밀번호가 맞지 않아요.', 401);
      await sql`DELETE FROM km_user WHERE id = ${u.id}`;
      res.status(200).json({ ok: true }); return;
    }

    bad('알 수 없는 요청이에요.');
  } catch (e) {
    console.error('auth:', e && e.message);
    res.status(502).json({ error: 'account store error' });
  }
};
