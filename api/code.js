// POST {code} — 웹용 이용 코드 (환경 변수 ACCESS_CODES: "코드:YYYY-MM-DD,코드2:YYYY-MM-DD")
const { setEntitlement, json, readBody } = require('./_lib');
const tries = new Map();
module.exports = async (req, res) => {
  if (req.method !== 'POST') return json(res, 405, { error: 'POST only' });
  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0];
  const t = tries.get(ip) || { n: 0, at: Date.now() };
  if (Date.now() - t.at > 600000) { t.n = 0; t.at = Date.now(); }
  if (++t.n > 10) return json(res, 429, { error: '잠시 후 다시 시도하세요' });
  tries.set(ip, t);
  let body; try { body = await readBody(req); } catch { return json(res, 400, { error: 'bad json' }); }
  const code = String(body.code || '').trim();
  for (const ent of String(process.env.ACCESS_CODES || '').split(',')) {
    const [c, until] = ent.trim().split(':');
    if (c && code === c) {
      const exp = Date.parse(until + 'T23:59:59+09:00');
      if (!(exp > Date.now())) return json(res, 402, { active: false, error: '기간이 끝난 코드입니다' });
      setEntitlement(res, { exp, src: 'code' });
      return json(res, 200, { active: true, exp });
    }
  }
  return json(res, 402, { active: false, error: '코드가 맞지 않습니다' });
};
