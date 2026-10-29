# 킬러들의 수학몰 (킬러 ShrekMath)

수능 20·21·29·30번형 창작문항을 "먼저 풀기 → 채점 → 조건 분석 → 핵심 개념 → 풀이 단계 → 함정 → 변형 → 한 줄" 순으로 분석하는 학습 페이지.
(국어 '킬러 분석학' 사이트의 구조를 수학용으로 옮기고, 조건 하이라이트·KaTeX·변형 문항·기록 내보내기를 더했습니다.)

## 배포 (Vercel)

저장소 루트의 `vercel.json`이 `site/`를 정적 사이트로 서비스하도록 되어 있다.
Vercel → Add New → Project → 이 저장소 Import → 설정 그대로 Deploy. 이후 `main`에 푸시할 때마다 자동 배포.
(Vercel은 Python을 돌리지 않으므로 `python build.py`는 로컬에서 실행하고 `site/`를 함께 커밋한다.)

`src/essay/season18.txt`(책 전체 추출본)는 용량 때문에 저장소에 넣지 않았다. 논술 문항은 `src/essay/items_18.json`에 이미 정리되어 있어 빌드에는 필요 없다.

## 수리 논술 탭

`src/essay/` 에 수리논술 나침반(hwpx)에서 뽑은 문제가 들어 있다.

1. `python src/essay/extract_hwpx.py "…/수리논술나침반 시즌 18 한글(2026).hwpx" > src/essay/season18.txt`
2. `python parse_essay.py src/essay/season18.txt` → `src/essay/items_18.json` (대학 세트 → 문제 → 소문항·예시답안·채점기준)
3. `python build.py`

다른 시즌도 같은 방법으로 `season17.txt` → `items_17.json`을 만들면 자동으로 합쳐진다. (책마다 형식이 조금씩 달라 파서가 놓치는 문제가 있을 수 있다. 그림은 `[그림]`으로만 표시된다.)

## 접근 코드로 잠그기 (문항 유출 방지)

```
pip install cryptography        # 처음 한 번
python build.py --key 늪2026
```

문항·해설·논술 데이터 전체가 AES-GCM으로 암호화되어 들어가고, 페이지를 열면 코드 입력창이 먼저 뜬다.
코드를 모르면 소스 보기·파일 다운로드로도 문항을 꺼낼 수 없다. 코드를 바꾸려면 다시 빌드하면 된다.
(코드를 아는 학생이 화면을 캡처하거나 코드를 퍼뜨리는 것까지는 막지 못한다. 그건 어떤 방식도 못 막는다.)

## 폴더

```
killer-math/
├─ build.py            빌드 스크립트  (python3 build.py)
├─ hwptex.py           한글(HWP) 수식 → LaTeX 변환기
├─ template.html       앱 템플릿 (화면·동작 전부 여기)
├─ src/bank/           문항 은행 원본 (.claude/tools/bank 의 q*_final.json 복사본)
├─ src/katex.*         KaTeX (폰트 인라인 CSS, JS 로컬 사본)
├─ anatomy/            ★ 완전 분석 파일 (문항 id별 JSON, LaTeX 문법)
├─ parse_essay.py      수리논술 텍스트 → 문제 JSON
├─ src/essay/          논술 원문 추출본(seasonNN.txt)·문제 JSON(items_NN.json)·추출 스크립트
├─ site/               정적 호스팅용 결과물 (index.html + list.json + data/NNN.json)
└─ killer-math.html    단일 파일 결과물 (데이터 포함, 그냥 열면 됨 · 아티팩트용)

`site/`에는 `elist.json`, `edata/NNN.json`(논술)도 생긴다. `--key`로 빌드하면 대신 `enc.json` 하나만 생긴다.
```

## 한글 파일에서 문항 가져오기 (`src/bank_src/`)

`수능창작문항/*.hwpx` 처럼 "NN. [과목] 난이도 ★★★★☆ … 정답 및 해설 … NN번 정답 X" 형식의 한글 파일은 자동으로 읽는다.

1. `python src/essay/extract_hwpx.py 파일.hwpx > src/bank_src/이름.txt`
2. `python parse_hwpx_bank.py` → `src/bank/x_이름.json`
3. `python build.py`

## 문항 추가·수정

1. `src/bank/`의 JSON을 고치거나 새 파일(`qNN?_final.json` 이름 규칙)을 넣는다. 수식은 한글 수식 문법 그대로.
2. `python3 build.py`
3. `site/`를 Cloudflare Pages / GitHub Pages 등에 올리거나, `killer-math.html` 한 파일을 공유한다.

번호(#001…)는 파일명 순(20A→20B→21A→…)·파일 안 순서로 자동 매겨진다.

## 완전 분석 파일 쓰기 (`anatomy/<문항id>.json`)

분석 파일이 없으면 "부분 분석"(조건 번호 + 은행의 풀이 단계만)로 올라간다.
`conds`와 `traps`가 있으면 "완전 분석" 배지가 붙는다. 수식은 **LaTeX**(`$…$`), 굵게는 `**…**`.

```json
{
 "source": "출처 표시",
 "rate": "정답률 12% (있을 때만)",
 "wrong": "많이 고른 오답 설명",
 "intro": ["진단 카드 문단", "…"],
 "conds": { "C1": {"label": "정의", "why": "이 조건이 말하는 것", "uses": [1,2]} },
 "concepts": [ {"h": "개념 제목", "p": ["문단", "…"]} ],
 "steps": [ {"title": "단계 제목", "text": "풀이", "uses": ["C1","C3"]} ],
 "traps": [ {"h": "함정 제목", "cond": "C2", "text": ["문단", "…"]} ],
 "variants": [ {"h": "변형 1", "lead": "안내", "body": ["문항 본문"], "answer": 97, "hint": "힌트·풀이"} ],
 "line": "오늘의 한 줄"
}
```

- 조건 번호 `C1, C2…`는 빌드가 본문을 **문장 단위**로 자동으로 매긴다. 먼저 `python3 build.py` 후 `site/data/NNN.json`의 `conds`에서 번호를 확인하고 분석 파일을 쓴다.
- `steps`를 쓰지 않으면 은행의 `solution` 문단이 그대로 단계가 된다. 쓰면 그걸로 대체된다.
- `uses`에 적은 조건은 그 카드에서 왼쪽 문항에 자동으로 색칠된다.

## 카드 그림 (ChatGPT·OpenAI 이미지)

카드 삽화는 기본적으로 내장 SVG 선 그림이다. 그림 파일을 넣으면 그걸 우선 쓴다.
- 문항별: `src/art/<문항id>.png|webp` (예 `20A-02.png`, `2021-035.png`, 논술 `essay-12.png`)
- 주제별: `src/art/cat/<그림키>.png` — 키는 `parabola, tangent, area, inflect, sine, exp, log, seq, series, limit, inverse, circle, triangle, ellipse, hyper, vector, space, sphere, dice, normal, count, integer, poly, set, ineq, motion, essay`
- 자동 생성: `pip install openai pillow` → `OPENAI_API_KEY` 설정 → `python gen_images.py --cat` (주제별 27장) / `--killer` / `--all`. 자세한 건 `gen_images.py` 머리말.
- 넣은 뒤 `python build.py`. 그림은 2:3 세로 비율이 가장 잘 맞는다.

## 화면 설정

`template.html` 맨 아래 스크립트의 `SITE={author:'…', blog:'…'}`에서 만든이·블로그 링크를 바꾼다.
등급 기준은 `RANKS`, 단계 이름은 `STAGE`.

## 학생 기록

브라우저 localStorage(`km:v1`)에만 저장된다. 홈의 "기록 내보내기"를 누르면 탭 구분 텍스트가 복사되어 엑셀·구글시트에 바로 붙여넣을 수 있다 (교사 제출용).
