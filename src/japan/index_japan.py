"""일본 대학 수학 문제집/해설집 PDF → 문제별 페이지 범위 색인 (index.json)"""
import re, json, sys, subprocess
PDF_Q = sys.argv[1]; PDF_S = sys.argv[2]
SUBJ = ('대수', '미적분', '확률과 통계', '기하')
hdr = re.compile(r'^\s*(\d{3})\s+(★+)\s+(.+?)\s*$', re.M)
def scan(pdf, kind):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    pages = txt.split('\f')
    year = None; subj = None; items = []; cur = None
    for i, p in enumerate(pages):
        m = re.search(r'^\s*(20\d\d)\s*·\s*' + kind, p, re.M)
        if m:
            year = m.group(1); cur = None; continue
        s = p.strip()
        lines = [l.strip() for l in s.split('\n') if l.strip()]
        if lines and lines[0] in SUBJ and len(lines) <= 3:
            subj = lines[0]; cur = None; continue
        h = hdr.search(p[:400])
        if h and year:
            cur = {'year': year, 'num': h.group(1), 'stars': len(h.group(2)), 'univ': h.group(3).strip(), 'subj': subj,
                   'pages': [i + 1], 'text': re.sub(r'\s+', ' ', p[h.end():])[:160]}
            items.append(cur)
        elif cur and s and not re.match(r'^\d+$', s):
            cur['pages'].append(i + 1)
    return items
Q = scan(PDF_Q, '문제'); S = scan(PDF_S, '해설')
smap = {(x['year'], x['num']): x for x in S}
out = []
for q in Q:
    s = smap.get((q['year'], q['num']))
    out.append({'id': f"{q['year']}-{q['num']}", **{k: q[k] for k in ('year', 'num', 'stars', 'univ', 'subj', 'pages', 'text')},
                'spages': s['pages'] if s else []})
json.dump(out, open('index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(Q), '문제', len(S), '해설', sum(1 for o in out if not o['spages']), '해설 없음')
print(sum(len(o['pages']) for o in out if o['stars'] >= 4), '문제쪽', sum(len(o['spages']) for o in out if o['stars'] >= 4), '해설쪽 (★4+)')
