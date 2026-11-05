"""기출관 추가분(2026-11-05): 공통 12·13(+11번은 2023-11 이후), 확통 28·29, 기하 28·29 → img/, index.json 뒤에 'add':1 로 덧붙임
사용: python src/past/render_past_add.py <공통.pdf> <확통.pdf> <미적.pdf> <기하.pdf> [c|k|g]"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_past, subprocess, tempfile
from PIL import Image
from render_past import exams, crop_items, IMG, ROOT
def _render(pdf, page):   # 연결 폴더 안에서는 임시 파일을 지울 수 없어 시스템 임시 폴더를 쓴다
    k = (pdf, page)
    if k not in render_past._cache:
        tmp = os.path.join(tempfile.gettempdir(), '_pgadd')
        subprocess.run(['pdftoppm', '-r', str(render_past.DPI), '-f', str(page), '-l', str(page), '-png', '-singlefile', pdf, tmp], check=True)
        render_past._cache.clear(); render_past._cache[k] = Image.open(tmp + '.png').convert('RGB')
    return render_past._cache[k]
render_past.render = _render
ADD = {'c': ([11, 12, 13], {11: 3, 12: 3, 13: 4}, '공통'), 'k': ([28, 29], {28: 3, 29: 4}, '확률과 통계'), 'g': ([28, 29], {28: 3, 29: 4}, '기하')}
def main(pdfs, only):
    p = os.path.join(ROOT, 'index.json'); idx = json.load(open(p, encoding='utf-8')); have = {x['id'] for x in idx}
    for key, pdf in zip('ckmg', pdfs):
        if key not in ADD or (only and key not in only): continue
        nums, stars, subj = ADD[key]
        for y, mo, pg in exams(pdf):
            want = list(nums)
            if key == 'c' and int(y) < 2024 and not (y == '2023' and mo == '11월'): want = [n for n in want if n != 11]
            got = crop_items(pdf, pg, pg + (8 if key == 'c' else 4) - 1, set(want))
            for n in want:
                iid = f'{y}-{mo[:-1].zfill(2)}-{key}{n}'
                if n not in got: print('  missing', iid); continue
                got[n].save(os.path.join(IMG, iid + '.webp'), 'WEBP', quality=86, method=6)
                if iid not in have:
                    idx.append({'id': iid, 'year': y, 'month': mo, 'part': subj, 'num': n, 'stars': stars[n],
                                'choice': n <= 15 or (key != 'c' and n <= 28), 'add': 1}); have.add(iid)
    json.dump(idx, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(idx), '문항 (추가', sum(1 for x in idx if x.get('add')), ')')
if __name__ == '__main__':
    main(sys.argv[1:5], sys.argv[5] if len(sys.argv) > 5 else '')
