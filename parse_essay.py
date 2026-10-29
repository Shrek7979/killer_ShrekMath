"""수리논술나침반 추출 텍스트(src/essay/seasonNN.txt) → 논술 문항 JSON (src/essay/items_NN.json)

구조: 대학 세트(제목 → 시험정보 표 → 문제들 → '예시답안' → 답안·채점기준) 를 문제 단위로 쪼갠다.
수식은 한글 수식 문법 그대로 두고, build.py에서 LaTeX로 바꾼다.
"""
import re, json, sys, os

UNIV = re.compile(r'^(\S+대학교.*?(수시|모의))\s*$')
MAIN = re.compile(r'^\[\s*(?:문제|문항)\s*(\d+)\s*\]')
SUB = re.compile(r'^\[\s*(?:문제|문항)?\s*(\d+)\s*[-.–]\s*([0-9ⅰⅱⅲⅳⅴⅵ]+)\s*\]')
RUBRIC = re.compile(r'^(○\s*)?채점\s*기준')
ANSHEAD = re.compile(r'^예시\s*답안$')
PTS = re.compile(r'\((?:총\s*)?(\d+)\s*점\)|\[(\d+)\s*점\]')
ROMAN = {'ⅰ': '1', 'ⅱ': '2', 'ⅲ': '3', 'ⅳ': '4', 'ⅴ': '5', 'ⅵ': '6'}
REF = re.compile(r'^\]\s*(에서|의|로부터|에|과|와|을|를|은|는|으로|처럼|에 의해|에서는|을 이용|를 이용)')


def is_header(t, rx):
    """'[1-1] …' 가 문항 머리인지, '[1-1]에서 구한' 같은 참조인지"""
    m = rx.match(t)
    if not m:
        return None
    rest = t[m.end() - 1:]
    if REF.match(rest):
        return None
    return m


def norm_title(t):
    return re.sub(r'[․·‧・\s]', '', t)


def parse(path):
    raw = re.sub(r'[\ue000-\uf8ff]', '', open(path, encoding='utf-8').read()).split('\n')
    lines = [(len(l) - len(l.lstrip(' ')), l.strip()) for l in raw]
    # 목차(앞부분) 건너뛰기: 첫 번째 '시험 시간' 표가 나오기 전의 제목은 무시
    sets, cur = [], None
    i = 0
    while i < len(lines):
        d, t = lines[i]
        m = UNIV.match(t)
        if m and not t[0].isdigit():
            key = norm_title(m.group(1))
            # 같은 제목이 연속 등장(머리글 반복)하면 같은 세트
            if cur and cur['key'] == key:
                i += 1; continue
            # 새 세트는 뒤에 시험정보 표(TBL)가 따라와야 한다
            look = ' '.join(x[1] for x in lines[i + 1:i + 14])
            if '시험 시간' in look or '출제 분야' in look or '시험시간' in look:
                cur = {'key': key, 'title': m.group(1), 'lines': [], 'start': i}
                sets.append(cur)
                i += 1; continue
        if cur is not None:
            cur['lines'].append((d, t))
        i += 1
    return sets


def split_set(st):
    L = st['lines']
    # 1) 시험 정보 표
    info = {}
    j = 0
    t0 = next((x for x in range(min(6, len(L))) if L[x][1] == 'TBL'), None)
    if t0 is not None:
        k = t0 + 1
        cells = []
        while k < len(L) and L[k][1] != '/TBL':
            cells.append(L[k][1]); k += 1
        j = k + 1
        heads = ['핵심개념 및 용어', '수능 최저기준', '출제 분야', '시험 시간']
        vals = [c for c in cells if c not in heads]
        if len(vals) >= 4:
            info = {'concepts': vals[0], 'min': vals[1], 'field': ' '.join(vals[2:-1]), 'time': vals[-1]}
        elif vals:
            info = {'concepts': vals[0], 'time': vals[-1]}
    body = L[j:]
    # 2) 문제부 / 답안부
    ai = next((x for x, (d, t) in enumerate(body) if ANSHEAD.match(t)), len(body))
    prob_lines = [t for d, t in body[:ai] if t not in ('TBL', '/TBL') and not UNIV.match(t)]
    ans_lines = [t for d, t in body[ai + 1:] if t not in ('TBL', '/TBL') and not UNIV.match(t)]
    return info, prob_lines, ans_lines


def split_problems(lines):
    """[문제 N] / [N-M] 마커로 문제·소문항 나누기"""
    probs = {}
    order = []
    cur = None; sub = None
    pre = []  # 첫 마커 전의 공통 제시문
    for t in lines:
        m = is_header(t, MAIN); s = is_header(t, SUB)
        if s:
            n = int(s.group(1)); k = s.group(2); k = ROMAN.get(k, k)
            if n not in probs:
                probs[n] = {'n': n, 'head': '', 'passage': [], 'subs': []}; order.append(n)
            cur = probs[n]
            sub = {'k': k, 'label': t[:t.index(']') + 1], 'text': [t[t.index(']') + 1:].strip()]}
            cur['subs'].append(sub)
            continue
        if m:
            n = int(m.group(1))
            if n not in probs:
                probs[n] = {'n': n, 'head': t, 'passage': [], 'subs': []}; order.append(n)
            else:
                probs[n]['head'] = probs[n]['head'] or t
            cur = probs[n]; sub = None
            rest = t[t.index(']') + 1:].strip()
            if rest:
                cur['passage'].append(rest)
            continue
        if cur is None:
            pre.append(t)
        elif sub is None:
            cur['passage'].append(t)
        else:
            sub['text'].append(t)
    out = [probs[n] for n in order]
    if not out and lines:
        out = [{'n': 1, 'head': '', 'passage': lines, 'subs': []}]
    if pre and out:
        out[0]['pre'] = pre
    return out


def split_answers(lines):
    """답안부를 (문제번호, 소문항) 별 {answer:[], rubric:[]} 로"""
    res = {}
    cur_n = None; cur_k = None; mode = 'answer'
    def slot(n, k):
        return res.setdefault((n, k), {'answer': [], 'rubric': []})
    for t in lines:
        s = is_header(t, SUB); m = is_header(t, MAIN)
        if s:
            cur_n = int(s.group(1)); cur_k = ROMAN.get(s.group(2), s.group(2)); mode = 'answer'
            rest = t[t.index(']') + 1:].strip()
            rest = re.sub(r'^\(\d+점\)\s*', '', rest)
            if rest and '예시답안' not in rest:
                slot(cur_n, cur_k)['answer'].append(rest)
            elif rest and '예시답안' in rest:
                rest2 = rest.split('예시답안', 1)[1].strip()
                if rest2: slot(cur_n, cur_k)['answer'].append(rest2)
            continue
        if m:
            cur_n = int(m.group(1)); cur_k = None; mode = 'answer'
            rest = t[t.index(']') + 1:].strip()
            if '예시답안' in rest:
                rest = rest.split('예시답안', 1)[1].strip()
            rest = re.sub(r'^\(\d+점\)\s*', '', rest)
            if rest:
                slot(cur_n, None)['answer'].append(rest)
            continue
        if RUBRIC.match(t):
            mode = 'rubric'
            rest = RUBRIC.sub('', t).strip()
            if cur_n is not None and rest:
                slot(cur_n, cur_k)['rubric'].append(rest)
            continue
        if cur_n is None:
            continue
        slot(cur_n, cur_k)[mode].append(t)
    return res


def build_items(path):
    sets = parse(path)
    items = []
    for st in sets:
        info, pl, al = split_set(st)
        probs = split_problems(pl)
        ans = split_answers(al)
        tm = re.search(r'(\d+)\s*분', info.get('time', '') or '')
        nq = re.search(r'(\d+)\s*문항', info.get('time', '') or '')
        total_min = int(tm.group(1)) if tm else None
        nprob = int(nq.group(1)) if nq else len(probs)
        per = round(total_min / max(nprob, 1)) if total_min else 25
        for p in probs:
            pts = PTS.search(p['head'] or '')
            points = int(pts.group(1) or pts.group(2)) if pts else None
            subs = []
            for s in p['subs']:
                a = ans.get((p['n'], s['k']), {'answer': [], 'rubric': []})
                sp = PTS.search(' '.join(s['text']))
                subs.append({'k': s['k'], 'label': s['label'], 'text': s['text'],
                             'points': int(sp.group(1) or sp.group(2)) if sp else None,
                             'answer': a['answer'], 'rubric': a['rubric']})
            whole = ans.get((p['n'], None), {'answer': [], 'rubric': []})
            # 소문항이 없고 답안이 통으로 있으면 소문항 하나로
            if not subs:
                subs = [{'k': '1', 'label': '[답안]', 'text': [], 'points': points, 'answer': whole['answer'], 'rubric': whole['rubric']}]
                whole = {'answer': [], 'rubric': []}
            if not any(s['answer'] for s in subs) and not whole['answer']:
                continue   # 답안이 전혀 없는 문제(면접 평가 항목 등)는 뺀다
            items.append({
                'id': f"{norm_title(st['title'])}-{p['n']}",
                'univ': st['title'], 'n': p['n'], 'head': p['head'], 'points': points,
                'minutes': per, 'info': info,
                'pre': p.get('pre', []), 'passage': p['passage'], 'subs': subs,
                'answer': whole['answer'], 'rubric': whole['rubric'],
            })
    return items


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'src/essay/season18.txt'
    items = build_items(src)
    out = src.replace('season', 'items_').replace('.txt', '.json')
    json.dump(items, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(items), '문제 →', out)
    univs = {}
    for it in items:
        univs.setdefault(it['univ'], 0); univs[it['univ']] += 1
    for u, c in univs.items():
        print(f'  {c:2d}  {u}')
