// 방문자 수 (Vercel 서버 함수 + Upstash Redis REST)
// GET /api/visit        → { total, today }
// GET /api/visit?hit=1  → 하나 올린 뒤 { total, today }  (같은 기기 하루 1번은 브라우저 쪽에서 막는다)
// 환경 변수: Vercel 대시보드에서 Upstash Redis 를 연결하면 자동으로 들어온다.
//   KV_REST_API_URL / KV_REST_API_TOKEN  또는  UPSTASH_REDIS_REST_URL / UPSTASH_REDIS_REST_TOKEN
module.exports = async (req, res) => {
  const url = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
  res.setHeader('Cache-Control', 'no-store');
  if (!url || !token) { res.status(503).json({ error: 'counter store not connected' }); return; }
  const day = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);   // 한국 시간 기준 날짜
  const dk = `km:visit:day:${day}`, tk = 'km:visit:total';
  const hit = req.query && (req.query.hit === '1');
  const cmds = hit ? [['INCR', tk], ['INCR', dk], ['EXPIRE', dk, '259200']] : [['GET', tk], ['GET', dk]];
  try {
    const r = await fetch(url.replace(/\/$/, '') + '/pipeline', {
      method: 'POST', headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }, body: JSON.stringify(cmds)
    });
    const j = await r.json();
    const v = k => Number((j[k] && j[k].result) || 0);
    res.status(200).json({ total: v(0), today: v(1), day });
  } catch (e) {
    res.status(502).json({ error: 'counter store error' });
  }
};
