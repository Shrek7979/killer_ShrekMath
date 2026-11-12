/* 킬러들의 수학몰 서비스 워커 — 빌드할 때 20261112134632 이 바뀌어 옛 캐시를 지운다.
   - 페이지·목록(JSON): 네트워크 우선, 안 되면 캐시 (오프라인)
   - 문제 이미지·KaTeX·글꼴: 캐시 우선 (한 번 본 문제는 오프라인에서도 열림) */
const V = '20261112134632';
const SHELL = 'shell-' + V, RUN = 'run-v1';
const PRE = ['/', '/list.json', '/elist.json', '/jlist.json', '/cats.json', '/manifest.json', '/icon-192.png', '/icon-512.png', '/favicon-32.png', '/privacy'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(SHELL).then(c => Promise.all(PRE.map(u => c.add(u).catch(() => {})))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('shell-') && k !== SHELL).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

async function networkFirst(req) {
  const c = await caches.open(SHELL);
  try {
    const r = await fetch(req);
    if (r && r.ok) c.put(req, r.clone());
    return r;
  } catch (e) {
    return (await c.match(req)) || (await c.match('/')) || Response.error();
  }
}
async function cacheFirst(req) {
  const c = await caches.open(RUN);
  const hit = await c.match(req);
  if (hit) return hit;
  const r = await fetch(req);
  if (r && (r.ok || r.type === 'opaque')) {
    c.put(req, r.clone());
    trim(c);
  }
  return r;
}
let trimming = false;
async function trim(c) {           // 이미지 캐시는 최대 600개까지만
  if (trimming) return; trimming = true;
  try { const ks = await c.keys(); for (let i = 0; i < ks.length - 600; i++) await c.delete(ks[i]); } finally { trimming = false; }
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  const same = u.origin === self.location.origin;
  const isCdn = /cdnjs\.cloudflare\.com|fonts\.(googleapis|gstatic)\.com/.test(u.host);
  if (req.mode === 'navigate' || (same && /\.(json|html)$/.test(u.pathname))) { e.respondWith(networkFirst(req)); return; }
  if (isCdn || (same && /\.(webp|png|jpe?g|svg|gif|woff2?|css|js)$/.test(u.pathname))) { e.respondWith(cacheFirst(req)); return; }
});
