"""pick3.json(또는 4번째 인자로 준 목록)에 적힌 ★3 문항의 문제·해설 페이지를 WebP로 (render_japan.py 와 같은 방식). 이미 만든 것은 건너뜀."""
import json, os, sys, subprocess, time
from PIL import Image, ImageChops
Q, S = sys.argv[1], sys.argv[2]; BUDGET = float(sys.argv[3]) if len(sys.argv) > 3 else 150
PICK = sys.argv[4] if len(sys.argv) > 4 else 'pick3.json'
ids = set(json.load(open(PICK, encoding='utf-8'))['ids'])
d = [x for x in json.load(open('index.json', encoding='utf-8')) if x['id'] in ids]
jobs = [(Q, p, f"img/{x['id']}-q{k}.webp") for x in d for k, p in enumerate(x['pages'])] + \
       [(S, p, f"img/{x['id']}-s{k}.webp") for x in d for k, p in enumerate(x['spages'])]
t0 = time.time(); done = 0
for pdf, page, out in jobs:
    if os.path.exists(out): continue
    if time.time() - t0 > BUDGET: break
    tmp = '/tmp/_pg3'
    subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-r', '110', '-jpeg', '-singlefile', pdf, tmp], check=True)
    im = Image.open(tmp + '.jpg').convert('L')
    diff = ImageChops.difference(im, Image.new('L', im.size, 255)).point(lambda v: 255 if v > 40 else 0)
    bbox = diff.crop((0, 0, im.width, im.height - 70)).getbbox()
    if bbox:
        x0, y0, x1, y1 = bbox; pad = 18
        im = im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))
    if im.width > 900: im = im.resize((900, int(im.height * 900 / im.width)), Image.LANCZOS)
    im.save(out, 'WEBP', quality=72, method=4); done += 1
print(f'{done} 장 생성, 남은 {sum(1 for _, _, o in jobs if not os.path.exists(o))} / 전체 {len(jobs)}')
