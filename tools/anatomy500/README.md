# 최고난도 500제 8단계 분석 작성 도구

- `dump.py A B` : site/data/A~B 번 문항의 조건(C1…)과 은행 풀이 단계를 출력 (분석이 아직 없는 문항 기준)
- `mk.py spec.json` : 압축 스펙 → `anatomy/<id>.json` 생성. 조건 id·단계 번호(1..n 빠짐없이)·KaTeX 검사 후 기록.
  단계 텍스트는 은행 풀이를 hwptex 로 다시 변환해 쓰므로, hwptex 를 고치면 스펙을 다시 돌리면 된다.
- 스펙 형식: `{n, wrong, intro[], conds{C1:[label, why, [단계번호]]}, concepts[[h,p]], steps[[제목,[원 단계들],[조건]]], traps[[h,조건,text]], variants[[h,본문,답,힌트]], line}`
- `b0NN.json` = 기하 100제(최고난도500(2)), `c0NN.json` = 미적분Ⅱ 250제(최고난도500(3)). 변형 문항의 답은 작성 시 계산으로 확인함.
- 경로는 /home/claude/ks 기준으로 하드코딩되어 있음 (R 변수).
