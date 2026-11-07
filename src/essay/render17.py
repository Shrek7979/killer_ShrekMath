"""seg17.json 의 문제·답안 영역을 WebP 로 잘라 src/essay/img/ 에, 문항 목록을 items_17.json 으로"""
import json, re, sys, os, subprocess, tempfile
from PIL import Image
PDF, SEG, LINES, OUT, JS = sys.argv[1:6]
os.makedirs(OUT, exist_ok=True)
sets = json.load(open(SEG, encoding='utf-8')); L = json.load(open(LINES, encoding='utf-8'))['lines']
DPI = 150; S = DPI / 72; X0, X1, TOP, BOT = 52, 548, 78, 778
A = ('서울대', '연세대', '고려대', '성균관대', '한양대', '서강대', '중앙대', '경희대', '이화여자대', '서울시립대')
MED = ('의예', '의·약', '의․약', '의약', '약학', '의학')
cache = {}
def page(p):
    if p not in cache:
        cache.clear(); tmp = os.path.join(tempfile.gettempdir(), '_s17')
        subprocess.run(['pdftoppm', '-r', str(DPI), '-f', str(p), '-l', str(p), '-png', '-singlefile', PDF, tmp], check=True)
        cache[p] = Image.open(tmp + '.png').convert('L')
    return cache[p]
def trim(im):
    g = im.point(lambda v: 0 if v > 235 else 255); bb = g.getbbox()
    if not bb: return None
    x0, y0, x1, y1 = bb
    return im.crop((0, max(0, y0 - 12), im.width, min(im.height, y1 + 16)))
def crop(reg, base):
    (p0, y0), (p1, y1) = reg['from'], reg['to']; files = []
    for p in range(p0, p1 + 1):
        a = y0 if p == p0 else TOP; b = y1 if p == p1 else BOT
        a = max(a, TOP); b = min(b, BOT)
        if b - a < 25: continue
        im = trim(page(p).crop((int(X0 * S), int(a * S), int(X1 * S), int(b * S))))
        if im is None or im.height < 40: continue
        if im.width > 900: im = im.resize((900, int(im.height * 900 / im.width)), Image.LANCZOS)
        f = f'{base}-{len(files)}.webp'; im.save(os.path.join(OUT, f), 'WEBP', quality=74, method=4); files.append('ess/' + f)
    return files
items = []
for si, s in enumerate(sets):
    u = s['univ']
    if not (u.startswith(A) or any(m in u for m in MED)): continue
    ok = sorted(set(s['q']) & set(s['a']), key=int)
    if not ok: continue
    per = round(s['time'] / len(s['q'])) if s['time'] else 30
    whole = None
    if any(r['head'].startswith('[논제') for r in s['q'].values()):
        # 경희대형: 제시문 [가]~[사]가 논제 앞뒤에 흩어져 있어 논제별로 자르면 제시문이 엇갈린다 → 문제지 전체를 보여 준다
        f0 = min((tuple(r['from']) for r in s['q'].values()))
        ga = [(p, y0 - 6) for p, x0, y0, x1, y1, t in L if p >= s['page'] and (p, y0) < f0 and t.startswith('[가]') and x0 < 90]
        whole = {'from': list(ga[0] if ga else f0), 'to': max((tuple(r['to']) for r in s['q'].values()))}
    for n in ok:
        q, a = s['q'][n], s['a'][n]
        if whole: q = dict(q, **{'from': whole['from'], 'to': list(whole['to'])})
        base = f's17-{si:02d}-{int(n)}'
        qi, ai = crop(q, base + 'q'), crop(a, base + 'a')
        if not qi or not ai: print('skip', u, n); continue
        head = re.sub(r'[-]', '', q['head']).strip()
        pts = re.search(r'\((?:총\s*)?(\d+)\s*점\)', head)
        items.append({'id': f"S17-{re.sub(r'[·․\s]', '', u)}-{n}", 'univ': u, 'n': int(n), 'season': 17, 'head': head,
                      'points': int(pts.group(1)) if pts else None, 'minutes': per,
                      'info': {'time': f"{s['time']}분" if s['time'] else ''}, 'pre': [], 'passage': [],
                      'subs': [{'k': '1', 'label': '[답안]', 'text': [], 'points': int(pts.group(1)) if pts else None, 'answer': [], 'rubric': []}],
                      'answer': [], 'rubric': [], 'qimg': qi, 'aimg': ai})
json.dump(items, open(JS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(items), '문항,', sum(len(x['qimg']) + len(x['aimg']) for x in items), '장')
