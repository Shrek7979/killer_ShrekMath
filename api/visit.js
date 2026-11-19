// 방문자 수 (Vercel 서버 함수 + Neon Postgres)
// GET /api/visit        → { total, today, day }
// GET /api/visit?hit=1  → 하나 올린 뒤 { total, today, day }  (같은 기기 하루 1번은 브라우저 쪽에서 막는다)
// 환경 변수: Vercel 대시보드에서 Neon 을 연결하면 DATABASE_URL(또는 POSTGRES_URL) 이 자동으로 들어온다.
// 의존성: 저장소 루트 package.json 의 @neondatabase/serverless (Vercel 이 배포할 때 설치)
const { neon } = require('@neondatabase/serverless');

let ready = false;   // 표는 함수 인스턴스마다 처음 한 번만 만든다

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'GET') { res.status(405).json({ error: 'GET only' }); return; }
  const dbUrl = process.env.DATABASE_URL || process.env.POSTGRES_URL;
  if (!dbUrl) { res.status(503).json({ error: 'counter store not connected' }); return; }
  const sql = neon(dbUrl);
  const day = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);   // 한국 시간 기준 날짜
  const dk = `day:${day}`;
  const hit = req.query && req.query.hit === '1';
  try {
    if (!ready) {
      await sql`CREATE TABLE IF NOT EXISTS km_visit (k TEXT PRIMARY KEY, n BIGINT NOT NULL DEFAULT 0)`;
      ready = true;
    }
    const rows = hit
      ? await sql`INSERT INTO km_visit (k, n) VALUES ('total', 1), (${dk}, 1)
                  ON CONFLICT (k) DO UPDATE SET n = km_visit.n + 1
                  RETURNING k, n`
      : await sql`SELECT k, n FROM km_visit WHERE k IN ('total', ${dk})`;
    // 날짜별 행은 계속 쌓이므로 가끔(약 2%) 90일 지난 것을 지운다
    if (hit && Math.random() < 0.02) {
      const old = 'day:' + new Date(Date.now() + 9 * 3600e3 - 90 * 864e5).toISOString().slice(0, 10);
      await sql`DELETE FROM km_visit WHERE k LIKE 'day:%' AND k < ${old}`;
    }
    const v = key => Number((rows.find(r => r.k === key) || {}).n || 0);   // BIGINT 는 문자열로 오므로 Number 로
    res.status(200).json({ total: v('total'), today: v(dk), day });
  } catch (e) {
    console.error('visit counter:', e && e.message);
    res.status(502).json({ error: 'counter store error' });
  }
};
