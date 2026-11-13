// 공용: 구독 확인 토큰(HMAC 서명 쿠키), Google Play API 토큰
const crypto = require('crypto');
const COOKIE = 'km_t';
const SECRET = () => process.env.TOKEN_SECRET || '';
const b64u = b => Buffer.from(b).toString('base64url');

function sign(payload) {
  const body = b64u(JSON.stringify(payload));
  const mac = crypto.createHmac('sha256', SECRET()).update(body).digest('base64url');
  return body + '.' + mac;
}
function verifyToken(tok) {
  if (!tok || !SECRET()) return null;
  const [body, mac] = String(tok).split('.');
  if (!body || !mac) return null;
  const good = crypto.createHmac('sha256', SECRET()).update(body).digest('base64url');
  if (mac.length !== good.length || !crypto.timingSafeEqual(Buffer.from(mac), Buffer.from(good))) return null;
  try { const p = JSON.parse(Buffer.from(body, 'base64url').toString()); return p.exp > Date.now() ? p : null; } catch { return null; }
}
function getCookie(req, name) {
  const m = (req.headers.cookie || '').match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
  return m ? decodeURIComponent(m[1]) : null;
}
const entitled = req => verifyToken(getCookie(req, COOKIE));
function setEntitlement(res, payload) {
  const maxAge = Math.max(0, Math.floor((payload.exp - Date.now()) / 1000));
  res.setHeader('Set-Cookie', `${COOKIE}=${sign(payload)}; Path=/; Max-Age=${maxAge}; HttpOnly; Secure; SameSite=Lax`);
}
function json(res, code, obj) {
  res.statusCode = code;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(obj));
}
async function readBody(req) {
  if (req.body) return typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
  const chunks = []; for await (const c of req) chunks.push(c);
  return chunks.length ? JSON.parse(Buffer.concat(chunks).toString()) : {};
}

// 서비스 계정 JSON(환경 변수 GOOGLE_SERVICE_ACCOUNT)으로 androidpublisher 접근 토큰 받기
let cached = null;
async function googleToken() {
  if (cached && cached.exp > Date.now() + 60000) return cached.tok;
  const sa = JSON.parse(process.env.GOOGLE_SERVICE_ACCOUNT || '{}');
  if (!sa.client_email) throw new Error('GOOGLE_SERVICE_ACCOUNT 환경 변수가 없습니다');
  const now = Math.floor(Date.now() / 1000);
  const head = b64u(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
  const claim = b64u(JSON.stringify({ iss: sa.client_email, scope: 'https://www.googleapis.com/auth/androidpublisher',
    aud: 'https://oauth2.googleapis.com/token', iat: now, exp: now + 3600 }));
  const sig = crypto.createSign('RSA-SHA256').update(head + '.' + claim).sign(sa.private_key, 'base64url');
  const r = await fetch('https://oauth2.googleapis.com/token', { method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=' + head + '.' + claim + '.' + sig });
  const j = await r.json();
  if (!j.access_token) throw new Error('Google 토큰 실패: ' + JSON.stringify(j));
  cached = { tok: j.access_token, exp: Date.now() + (j.expires_in || 3600) * 1000 };
  return cached.tok;
}

const PACKAGE = 'com.shrekmath.killermath';
module.exports = { entitled, setEntitlement, json, readBody, googleToken, PACKAGE };
