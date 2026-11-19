"""ShrekMath 서울대·KAIST 모의 면접 한글 파일(추출 텍스트) → 논술관 문항 JSON (src/essay/items_zmock.json)
src/essay/mock_src/*.txt : extract_hwpx.py 로 뽑은 텍스트. 파일 이름과 대학 표기는 아래 SRC 에 적는다."""
import re, json, sys, os
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = [  # (txt, 대학 표기(회차는 {r}), 문항당 시간(분))
    ('f1.txt', '서울대학교 면접 대비 제{r}회 (ShrekMath)', 15),
    ('f2.txt', '서울대학교 모의 면접 최고난도 (ShrekMath)', 15),
    ('f3.txt', '서울대학교 모의 면접 (ShrekMath)', 15),
    ('f4.txt', 'KAIST 면접 대비 제{r}회 (ShrekMath)', 10),
    ('f5.txt', 'KAIST 모의 면접 (ShrekMath)', 10),
]
ROUND = re.compile(r'^제\s*(\d+)\s*회$')
AROUND = re.compile(r'^제\s*(\d+)\s*회\s*예시\s*답안$')
PROB = re.compile(r'^(?:문제\s*(\d+)\.|\[문항\s*(\d+)\])\s*(.*)$')
SUB_S = re.compile(r'^(\d+)-(\d+)\.\s*(.*)$')
SUB_K = re.compile(r'^\((\d+)\)\s*(.*)$')
PTS = re.compile(r'\[(\d+)\s*점\]')

def clean(path):
    out = []
    for l in open(path, encoding='utf-8'):
        t = l.strip()
        if t in ('TBL', '/TBL') or not t: continue
        out.append(t)
    return out

def sub_match(t, pn):
    m = SUB_S.match(t)
    if m and int(m.group(1)) == pn: return m.group(2), m.group(3)
    m = SUB_K.match(t)
    if m: return m.group(1), m.group(2)
    return None

def split_probs(lines):
    probs, cur, pre = [], None, []
    for t in lines:
        m = PROB.match(t)
        if m:
            cur = {'n': int(m.group(1) or m.group(2)), 'lines': [m.group(3)] if m.group(3) else []}; probs.append(cur); continue
        (cur['lines'] if cur else pre).append(t)
    return pre, probs

def by_round(lines, rx):
    rounds, cur = {}, None
    for t in lines:
        m = rx.match(t)
        if m: cur = int(m.group(1)); rounds[cur] = []; continue
        if cur is not None: rounds[cur].append(t)
    return rounds

def subs_of(p):
    body, subs = [], []
    for t in p['lines']:
        sm = sub_match(t, p['n'])
        if sm and sm[0] == str(len(subs) + 1):   # 소문항 번호는 1, 2, 3… 차례로만 (본문의 '(1)의 …' 같은 참조는 무시)
            subs.append({'k': sm[0], 'text': [sm[1]]}); continue
        (subs[-1]['text'] if subs else body).append(t)
    return body, subs

def build():
    items = []
    for fn, uni, mins in SRC:
        L = clean(os.path.join(ROOT, 'src/essay/mock_src', fn))
        qend = next(i for i, t in enumerate(L) if t == '문항 구성')
        a0 = next(i for i, t in enumerate(L) if re.match(r'^(제\s*\d+\s*회\s*)?예시\s*답안$', t))
        Q, A = L[:qend], L[a0:]
        if any(ROUND.match(t) for t in Q):
            qr = by_round(Q, ROUND); ar = by_round(A, AROUND)
        else:
            qr = {0: Q}; ar = {0: A[1:]}
        for r in sorted(qr):
            pre, probs = split_probs(qr[r]); _, aprobs = split_probs(ar.get(r, []))
            amap = {p['n']: p for p in aprobs}
            title = uni.format(r=r)
            for p in probs:
                body, subs = subs_of(p)
                apre, asubs = subs_of(amap[p['n']]) if p['n'] in amap else ([], [])
                ad = {s['k']: s['text'] for s in asubs}
                out_subs = []
                for j, s in enumerate(subs):
                    ans = ad.get(s['k'], [])
                    if j == 0 and apre: ans = apre + ans
                    pts = PTS.search(' '.join(s['text']))
                    lab = f"[{p['n']}-{s['k']}]" if SUB_S.match(f"{p['n']}-{s['k']}. x") and '서울대' in uni else f"({s['k']})"
                    out_subs.append({'k': s['k'], 'label': lab, 'text': s['text'], 'points': int(pts.group(1)) if pts else None, 'answer': ans, 'rubric': []})
                if not out_subs:
                    out_subs = [{'k': '1', 'label': '[답안]', 'text': [], 'points': None, 'answer': apre, 'rubric': []}]
                tot = sum(s['points'] or 0 for s in out_subs) or None
                head = f"[문제 {p['n']}]"
                items.append({'id': f"MK-{re.sub(r'[^0-9A-Za-z가-힣]', '', title)}-{p['n']}", 'univ': title, 'n': p['n'], 'head': head,
                              'points': tot, 'minutes': mins, 'info': {'concepts': '', 'time': f'{mins}분'},
                              'pre': pre if p is probs[0] else [], 'passage': body, 'subs': out_subs,
                              'answer': [], 'rubric': [], 'season': 18})
    return items

if __name__ == '__main__':
    it = build()
    json.dump(it, open(os.path.join(ROOT, 'src/essay/items_zmock.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(it), '문항')
