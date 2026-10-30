/**
 * 킬러들의 수학몰 — 교사용 기록 수집 (Google Apps Script)
 *
 * 1. Google 스프레드시트 새로 만들기 → 확장 프로그램 → Apps Script
 * 2. 이 코드를 붙여넣고 저장
 * 3. 배포 → 새 배포 → 유형 "웹 앱" → 실행: 나, 액세스: "모든 사용자" → 배포 → 웹 앱 URL 복사
 * 4. template.html 의 SITE.sheetUrl 에 그 URL 을 넣고 python build.py → 푸시
 *
 * 학생이 채점할 때마다 한 줄씩 쌓인다. (이름은 학생이 사이트에서 한 번 입력)
 */
function doPost(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName('기록') || ss.insertSheet('기록');
  if (sh.getLastRow() === 0) {
    sh.appendRow(['받은 시각', '이름', '구분', '번호', '문항ID', '제목', '결과', '내 답', '정답', '점수', '만점', '시간(초)', '제한(초)', '초과', '세트', '기기']);
  }
  var rows = JSON.parse(e.postData.contents);
  if (!Array.isArray(rows)) rows = [rows];
  rows.forEach(function (r) {
    sh.appendRow([new Date(), r.name || '', r.kind || '', r.num || '', r.id || '', r.title || '', r.result || '',
      r.ans == null ? '' : r.ans, r.answer == null ? '' : r.answer, r.score == null ? '' : r.score, r.total == null ? '' : r.total,
      r.secs == null ? '' : r.secs, r.limit == null ? '' : r.limit, r.over ? 'Y' : '', r.set || '', r.ua || '']);
  });
  return ContentService.createTextOutput(JSON.stringify({ ok: true, n: rows.length })).setMimeType(ContentService.MimeType.JSON);
}
function doGet() { return ContentService.createTextOutput('킬러들의 수학몰 수집기 작동 중'); }
