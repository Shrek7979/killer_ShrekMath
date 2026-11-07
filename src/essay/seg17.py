"""수리논술 나침반 PDF(수식이 글꼴 그림이라 글자로 안 뽑히는 판) → 대학 세트별 문제·예시답안 영역(페이지·y 범위)"""
import json, re, sys
d = json.load(open(sys.argv[1], encoding='utf-8')); L = d['lines']
ROM = {'Ⅰ': 1, 'Ⅱ': 2, 'Ⅲ': 3, 'Ⅳ': 4, 'Ⅴ': 5}
SET = re.compile(r'^(\S*대학교.*?(?:수시|모의))\s*\d*\)?$')
NUM = r'(\d+|[ⅠⅡⅢⅣⅤ])?'
HEAD = re.compile(r'^\[\s*(?:문항|문제|논제)\s*' + NUM + r'\s*(?:,[^\]]*)?\]\s*(.*)$')     # [문항 1] [문제 2, 서술형] [논제 Ⅰ] [문항]
SUBA = re.compile(r'^\[\s*(?:문제\s*)?(\d+)\s*[-.]\s*\d+\s*\]\s*대학\s*발표')                   # [1-1] 대학발표 예시답안
SNU = re.compile(r'^문제\s+(\d+)\s*\.$')                                                     # 서울대 '문제 1.'
ANS = re.compile(r'^대학\s*발표\s*예시\s*답안')
ev = []
for p, x0, y0, x1, y1, t in L:
    if y0 < 80 or y0 > 775: continue
    m = SET.match(t)
    if m and 100 < y0 < 160 and x0 > 120: ev.append([p, y0, 'set', m.group(1), t]); continue
    if x0 < 80:
        m = SUBA.match(t)
        if m: ev.append([p, y0, 'a', int(m.group(1)), t]); continue
        m = HEAD.match(t)
        if m:
            n = m.group(1); n = (ROM[n] if n in ROM else int(n)) if n else None
            ev.append([p, y0, 'a' if ANS.match(m.group(2)) else 'q', n, t]); continue
    m = SNU.match(t)
    if m and x0 < 260: ev.append([p, y0, 'snu', int(m.group(1)), t]); continue
    if (t.startswith('풀어보기') and x0 < 120) or t.replace(' ', '') == '예시답안':
        ev.append([p, y0, 'x', 0, t])
ev.sort(key=lambda e: (e[0], e[1]))
sets, cur = [], None
for e in ev:
    if e[2] == 'set':
        cur = {'univ': e[3], 'page': e[0], 'ev': []}; sets.append(cur)
    elif cur is not None:
        cur['ev'].append(e)
for s in sets:
    E = s['ev']
    fa = next((i for i, e in enumerate(E) if e[2] == 'a'), None)
    if fa is not None:   # 예시답안 구간에서 문제를 다시 적어 둔 머리('[문제 2, 단답형]' 등)는 문제로 보지 않는다
        E = s['ev'] = [e for i, e in enumerate(E) if not (i > fa and e[2] == 'q')]
    qn = an = 0; seen_snu = set()
    for e in E:                       # 번호 없는 [문항]/[문제] 는 차례로 번호를 매기고, 서울대 '문제 n.' 은 두 번째 등장이 답안
        if e[2] == 'q':
            qn = e[3] or qn + 1; e[3] = qn
        elif e[2] == 'a':
            an = e[3] or an + 1; e[3] = an
        elif e[2] == 'snu':
            e[2] = 'a' if e[3] in seen_snu else 'q'; seen_snu.add(e[3])
    s['q'], s['a'] = {}, {}
    nxt_set = sets[sets.index(s) + 1]['page'] if sets.index(s) + 1 < len(sets) else 10**6
    for i, e in enumerate(E):
        if e[2] not in ('q', 'a'): continue
        j = i + 1
        while j < len(E) and E[j][2] == e[2] and E[j][3] == e[3]: j += 1   # 같은 번호의 소문항 답안은 한 덩어리
        end = (E[j][0], E[j][1] - 6) if j < len(E) else (min(nxt_set - 1, max(l[0] for l in L)), 780)
        tgt = s[e[2]]
        if e[3] not in tgt: tgt[e[3]] = {'from': [e[0], e[1] - 6], 'to': list(end), 'head': e[4]}
    txt = ' '.join(t for p, x0, y0, x1, y1, t in L if p == s['page'] and 180 < y0 < 330)
    tm = re.search(r'(\d{2,3})\s*분', txt); s['time'] = int(tm.group(1)) if tm else None
    del s['ev']
json.dump(sets, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tot = 0
for s in sets:
    ok = sorted(set(s['q']) & set(s['a'])); tot += len(ok)
    print(s['page'], s['univ'], 'Q', sorted(s['q']), 'A', sorted(s['a']), s['time'])
print('짝 맞는 문제', tot)
