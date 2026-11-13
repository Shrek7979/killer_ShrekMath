// GET /p/<경로> → 구독자에게만 paid/<경로> 파일을 보낸다 (vercel.json rewrite)
const fs = require('fs'), path = require('path');
const { entitled, json } = require('./_lib');
const ROOT = path.join(process.cwd(), 'paid');
const TYPES = { '.json': 'application/json; charset=utf-8', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg' };
module.exports = (req, res) => {
  const f = String((req.query && req.query.f) || new URL(req.url, 'http://x').searchParams.get('f') || '');
  if (!/^(data|edata|jx|jp|past|ess)\/[\w.\-]+$/.test(f)) return json(res, 404, { error: 'not found' });
  if (!entitled(req)) return json(res, 402, { error: 'subscription required' });
  const p = path.join(ROOT, f);
  if (!p.startsWith(ROOT + path.sep) || !fs.existsSync(p)) return json(res, 404, { error: 'not found' });
  res.statusCode = 200;
  res.setHeader('Content-Type', TYPES[path.extname(p)] || 'application/octet-stream');
  res.setHeader('Cache-Control', 'private, max-age=86400');
  res.end(fs.readFileSync(p));
};
