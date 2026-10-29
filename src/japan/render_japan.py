"""★4 이상 문제·해설 페이지를 WebP로 렌더링. 여러 번 실행해도 이미 만든 것은 건너뜀."""
import json, os, subprocess, sys, time
from PIL import Image, ImageChops
Q = sys.argv[1]; S = sys.argv[2]; MIN = int(sys.argv[3]) if len(sys.argv) > 3 else 4
BUDGET = float(sys.argv[4]) if len(sys.argv) > 4 else 150
os.makedirs('img', exist_ok=True)
d = json.load(open('index.json', encoding='utf-8'))
jobs = []
for x in d:
    if x['stars'] < MIN: continue
    for k, p in enumerate(x['pages']): jobs.append((Q, p, f"img/{x['id']}-q{k}.webp"))
    for k, p in enumerate(x['spages']): jobs.append((S, p, f"img/{x['id']}-s{k}.webp"))
t0 = time.time(); done = 0
for pdf, page, out in jobs:
    if os.path.exists(out): continue
    if time.time() - t0 > BUDGET: break
    subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-r', '110', '-jpeg', '-singlefile', pdf, '/tmp/_pg'], check=True)
    im = Image.open('/tmp/_pg.jpg').convert('L')
    bg = Image.new('L', im.size, 255)
    diff = ImageChops.difference(im, bg).point(lambda v: 255 if v > 40 else 0)
    bbox = diff.crop((0, 0, im.width, im.height - 70)).getbbox()   # 아래 70px(쪽 번호)는 무시
    if bbox:
        x0, y0, x1, y1 = bbox; pad = 18
        im = im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))
    if im.width > 900: im = im.resize((900, int(im.height * 900 / im.width)), Image.LANCZOS)
    im.save(out, 'WEBP', quality=72, method=4); done += 1
left = sum(1 for _, _, o in jobs if not os.path.exists(o))
print(f'{done} 장 생성, 남은 {left} / 전체 {len(jobs)}')
