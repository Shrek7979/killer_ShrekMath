// POST {purchaseToken, sku} — Google Play 구독을 확인하고 이용권 쿠키를 준다 (앱 안에서 호출)
const { setEntitlement, json, readBody, googleToken, PACKAGE } = require('./_lib');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return json(res, 405, { error: 'POST only' });
  let body; try { body = await readBody(req); } catch { return json(res, 400, { error: 'bad json' }); }
  const token = String(body.purchaseToken || '');
  if (!/^[\w.\-:]{10,512}$/.test(token)) return json(res, 400, { error: 'bad token' });
  try {
    const g = await googleToken();
    const base = `https://androidpublisher.googleapis.com/androidpublisher/v3/applications/${PACKAGE}/purchases/subscriptions`;
    const r = await fetch(`${base}v2/tokens/${encodeURIComponent(token)}`, { headers: { Authorization: 'Bearer ' + g } });
    const s = await r.json();
    if (!r.ok) return json(res, 402, { active: false, error: s.error && s.error.message });
    const okState = ['SUBSCRIPTION_STATE_ACTIVE', 'SUBSCRIPTION_STATE_IN_GRACE_PERIOD', 'SUBSCRIPTION_STATE_CANCELED'];
    const exp = Math.max(0, ...(s.lineItems || []).map(li => Date.parse(li.expiryTime) || 0));
    if (!okState.includes(s.subscriptionState) || exp <= Date.now()) return json(res, 402, { active: false, state: s.subscriptionState });
    if (s.acknowledgementState === 'ACKNOWLEDGEMENT_STATE_PENDING') {
      const pid = (s.lineItems[0] || {}).productId || body.sku;
      await fetch(`${base}/${encodeURIComponent(pid)}/tokens/${encodeURIComponent(token)}:acknowledge`,
        { method: 'POST', headers: { Authorization: 'Bearer ' + g, 'Content-Type': 'application/json' }, body: '{}' });
    }
    setEntitlement(res, { exp, src: 'play' });
    return json(res, 200, { active: true, exp });
  } catch (e) {
    return json(res, 500, { error: String(e.message || e) });
  }
};
