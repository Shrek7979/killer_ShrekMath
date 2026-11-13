// GET — 지금 이 브라우저(앱)에 이용권이 있는지
const { entitled, json } = require('./_lib');
module.exports = (req, res) => { const p = entitled(req); json(res, 200, p ? { active: true, exp: p.exp } : { active: false }); };
