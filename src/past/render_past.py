"""평가원 문제지 PDF(공통/확통/미적/기하 묶음) → 킬러 번호 문항 잘라내기

사용: python src/past/render_past.py <공통.pdf> <확통.pdf> <미적.pdf> <기하.pdf>
출력: src/past/img/<id>.webp, src/past/index.json (정답은 answers.json 에서 합친다)

문제지 레이아웃: 2단. 문항 번호 "NN." 단어의 위치(pdftotext -bbox-layout)로 각 문항의 세로 구간을 정한다.
"""
import re, os, sys, json, subprocess, io
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, 'img'); os.makedirs(IMG, exist_ok=True)
DPI = 160
# 과목별 (PDF 인덱스, 잘라낼 번호, 난이도)
PLAN = {
    'c': ([14, 15, 20, 21, 22], {14: 3, 15: 4, 20: 3, 21: 4, 22: 5}, '공통'),
    'k': ([30], {30: 3}, '확률과 통계'),
    'm': ([28, 29, 30], {28: 4, 29: 4, 30: 5}, '미적분'),
    'g': ([30], {30: 3}, '기하'),
}
EXAM_RE = re.compile(r'(\d{4})학년도\s*대학수학능력시험\s*(6월|9월)?[^\n]*?문제지')


def pages_text(pdf):
    return subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')


def exams(pdf):
    """[(year, month, first_page)]"""
    out = []
    for i, p in enumerate(pages_text(pdf), 1):
        head = re.sub(r'\s+', ' ', p[:400])
        m = re.search(r'(\d{4})학년도 대학수학능력시험 (6월|9월)? ?(?:통계\)|\(미적분\)|\(기하\))? ?(?:모의평가 )?문제지', head)
        if not m:
            m2 = re.search(r'(\d{4})학년도 대학수학능력시험', head)
            if m2 and ('문제지' in head) and (' 1 ' in head[:160] or '13 ' in head):
                mon = '6월' if '6월' in head else '9월' if '9월' in head else None
                out.append((m2.group(1), mon or '11월', i)); continue
            continue
        out.append((m.group(1), (m.group(2) or '11월'), i))
    # 같은 시험이 두 번 잡히면(헤더 반복) 첫 페이지만
    seen, res = set(), []
    for y, mo, pg in out:
        if (y, mo) in seen: continue
        seen.add((y, mo)); res.append((y, mo, pg))
    return res


def words(pdf, page):
    h = subprocess.run(['pdftotext', '-bbox-layout', '-f', str(page), '-l', str(page), pdf, '-'], capture_output=True, text=True).stdout
    pw, ph = map(float, re.search(r'<page width="([\d.]+)" height="([\d.]+)"', h).groups())
    ws = [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in
          re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', h)]
    return pw, ph, ws


_cache = {}


def render(pdf, page):
    k = (pdf, page)
    if k not in _cache:
        tmp = os.path.join(IMG, '_pg')
        subprocess.run(['pdftoppm', '-r', str(DPI), '-f', str(page), '-l', str(page), '-png', '-singlefile', pdf, tmp], check=True)
        _cache.clear(); _cache[k] = Image.open(tmp + '.png').convert('RGB'); os.remove(tmp + '.png')
    return _cache[k]


def trim(im):
    """아래쪽 흰 여백 자르기 (그림은 픽셀로 남으므로 안전)"""
    g = im.convert('L'); w, h = g.size; px = g.load()
    last = h - 1
    while last > 60:
        if any(px[x, last] < 200 for x in range(0, w, 2)): break
        last -= 1
    return im.crop((0, 0, w, min(h, last + 30)))


def crop_items(pdf, first, last, wanted):
    """first..last 페이지에서 wanted 번호 문항을 찾아 {num: Image}"""
    found = {}
    for pg in range(first, last + 1):
        pw, ph, ws = words(pdf, pg)
        mid = pw / 2
        nums = [(w, int(w[4][:-1])) for w in ws if re.fullmatch(r'\d{1,2}\.', w[4]) and w[0] < pw * 0.62 and (w[0] < 130 or abs(w[0] - mid - 16) < 40 or 400 < w[0] < 470)]
        # 번호 단어는 단 시작 x 에 있다: 왼쪽 단(x<130) / 오른쪽 단(x≈pw/2+15)
        left = [n for n in nums if n[0][0] < 130]
        right = [n for n in nums if n[0][0] >= 130]
        body_bottom = max([w[3] for w in ws if w[3] < ph - 110] or [ph - 120])
        for col, lst, x0, x1 in (('L', left, 50, mid - 8), ('R', right, mid + 8, pw - 45)):
            lst.sort(key=lambda n: n[0][1])
            for i, (w, n) in enumerate(lst):
                if n not in wanted or n in found: continue
                y0 = w[1] - 10
                y1 = (lst[i + 1][0][1] - 12) if i + 1 < len(lst) else body_bottom + 14
                # 같은 단에서 y0..y1 사이 실제 글자의 최대 yMax 로 바닥을 조인다
                chk = [t[1] for t in ws if x0 <= t[0] < x1 and y0 <= t[1] < y1 and t[4] in ('확인', '※')]
                for t in ws:
                    if x0 <= t[0] < x1 and y0 <= t[1] < y1 and t[4] == '사항':
                        chk.append(t[1] - 26)
                if chk: y1 = min(y1, min(chk) - 6)
                ys = [t[3] for t in ws if x0 <= t[0] < x1 and y0 <= t[1] < y1]
                if ys: y1 = min(y1, max(ys) + 14)
                xs = [t[2] for t in ws if x0 <= t[0] < x1 and y0 <= t[1] < y1]
                x1c = min(x1, (max(xs) + 14) if xs else x1)
                img = render(pdf, pg); s = DPI / 72
                box = (int(x0 * s), int(y0 * s), int(max(x1c, x0 + 300) * s), int(y1 * s))
                found[n] = trim(img.crop(box))
    return found


def main(pdfs):
    out = []
    for key, pdf in zip('ckmg', pdfs):
        nums, stars, subj = PLAN[key]
        ex = exams(pdf)
        span = 8 if key == 'c' else 4
        print(key, pdf, ex)
        for y, mo, pg in ex:
            got = crop_items(pdf, pg, pg + span - 1, set(nums))
            for n in nums:
                if n not in got:
                    print('  missing', y, mo, key, n); continue
                iid = f'{y}-{mo[:-1].zfill(2)}-{key}{n}'
                got[n].save(os.path.join(IMG, iid + '.webp'), 'WEBP', quality=86, method=6)
                out.append({'id': iid, 'year': y, 'month': mo, 'part': subj, 'num': n, 'stars': stars[n],
                            'choice': n <= 15 or (key != 'c' and n <= 28)})
    out.sort(key=lambda x: (x['year'], x['month'], 'ckmg'.index(x['id'].split('-')[2][0]), x['num']), reverse=False)
    json.dump(out, open(os.path.join(ROOT, 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(out), '문항')


if __name__ == '__main__':
    main(sys.argv[1:5])
