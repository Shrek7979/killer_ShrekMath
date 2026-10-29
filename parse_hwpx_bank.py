"""한글(hwpx) 창작문항 추출 텍스트 → 문항 은행 JSON

입력: src/bank_src/*.txt  (extract_hwpx.py 로 뽑은 텍스트)
출력: src/bank/x_<이름>.json  (build.py 가 q*_final.json 과 함께 읽는다)

지원 형식
  A) "01. [공통(대수)] 난이도 ★★★★☆" … "▶ 소재: … → 변형 포인트: …"
     해설: "01번 정답 384 난이도 … [과목]" / "주제: … / 성취기준: …" / 풀이 문단
  B) "20. [대수]" … 해설: "20번 정답 600" / 성취기준 / 출제 의도 / 풀이
"""
import re, json, glob, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
HEAD = re.compile(r'^(\d{1,2})\.\s*\[([^\]]+)\]\s*(?:난이도\s*([★☆]+))?')
SOL = re.compile(r'^(\d{1,2})번\s*정답\s*(\d+)')
SUBJ = {'공통(대수)': '대수', '대수': '대수', '공통(미적분Ⅰ)': '미적분Ⅰ', '미적분Ⅰ': '미적분Ⅰ', '미적분Ⅱ': '미적분Ⅱ',
        '확률과 통계': '확률과 통계', '기하': '기하', '수학Ⅰ': '대수', '수학Ⅱ': '미적분Ⅰ', '미적분': '미적분Ⅱ'}
# 손으로 붙인 주제 (형식 B에는 주제 줄이 없다)
TOPICS = {'2cha-20': '회전하는 두 점과 삼각방정식', '2cha-21': '평균값 정리의 c의 개수', '2cha-29': '등차수열과 각의 급수', '2cha-30': '지수곡선의 접선과 반사'}


def blocks_from(lines):
    """본문 줄 → [["p",…],["eq",…],["box",[…]]]"""
    out, i = [], 0
    while i < len(lines):
        t = lines[i]
        if t == 'TBL':
            j = i + 1; items = []
            while j < len(lines) and lines[j] != '/TBL':
                items.append(lines[j]); j += 1
            # 표준정규분포표처럼 셀이 나열된 표 → table
            if items and items[0].strip() in ('$z$', 'z') and len(items) % 2 == 0:
                rows = [[items[k], items[k + 1]] for k in range(0, len(items), 2)]
                out.append(['table', rows])
            else:
                out.append(['box', items])
            i = j + 1; continue
        if t == '/TBL':
            i += 1; continue
        m = re.fullmatch(r'\$([^$]+)\$', t.strip())
        if m:
            out.append(['eq', m.group(1)])
        elif t.strip():
            out.append(['p', t])
        i += 1
    return out


def parse(path):
    name = os.path.splitext(os.path.basename(path))[0]
    L = [l.rstrip('\n') for l in open(path, encoding='utf-8')]
    L = [re.sub(r'[-]', '', l) for l in L]
    L = [l if l.strip() in ('TBL', '/TBL') else l.strip() for l in L]
    L = [l.strip() if l.strip() in ('TBL', '/TBL') else l for l in L]
    si = next((i for i, l in enumerate(L) if l.startswith('정답 및 해설')), len(L))
    probs, cur = {}, None
    for l in L[:si]:
        m = HEAD.match(l)
        if m:
            n = int(m.group(1)); cur = {'n': n, 'subj': m.group(2), 'stars': (m.group(3) or '').count('★') or 4, 'lines': [], 'note': ''}
            probs[n] = cur; continue
        if cur is None:
            continue
        if l.startswith('▶'):
            cur['note'] = l.lstrip('▶ ').strip(); continue
        cur['lines'].append(l)
    sols, cur = {}, None
    for l in L[si + 1:]:
        m = SOL.match(l)
        if m:
            n = int(m.group(1)); cur = {'answer': int(m.group(2)), 'lines': [], 'topic': '', 'standards': [], 'intent': ''}
            sols[n] = cur; mode = 'sol'; continue
        if cur is None:
            continue
        if l.startswith('주제:'):
            body = l[3:]
            parts = body.split('/ 성취기준:')
            cur['topic'] = parts[0].strip()
            if len(parts) > 1:
                cur['standards'] = [s.strip() for s in re.findall(r'\[[^\]]+\]', parts[1])]
            continue
        if l in ('성취기준', '출제 의도', '풀이'):
            mode = l; continue
        if mode == '성취기준':
            found = re.findall(r'\[[^\]]+\][^,\[]*', l)
            if found and not cur['standards']:
                cur['standards'] = [s.strip() for s in found]
            continue
        if mode == '출제 의도':
            cur['intent'] += (' ' if cur['intent'] else '') + l; continue
        if l.startswith('정답:') or l.startswith('참고:'):
            continue
        cur['lines'].append(l)
    items = []
    for n, p in sorted(probs.items()):
        s = sols.get(n)
        if not s:
            continue
        qid = f'{name}-{n:02d}'
        subj = SUBJ.get(p['subj'].strip(), p['subj'].strip())
        src = p['note']
        mt = re.search(r'(\d+)번', src)
        qtype = (mt.group(1) if mt else str(n)) + '번형'
        topic = s['topic'].split(',')[0].strip() if s['topic'] else TOPICS.get(qid, f'{subj} {n}번')
        items.append({
            'id': qid, 'subject': subj, 'topic': topic, 'stars': p['stars'], 'type': qtype,
            'standards': s['standards'], 'answer': s['answer'],
            'body': blocks_from(p['lines']),
            'solution': blocks_from(s['lines']),
            'source': ('2026 수능 기출 변형 · ' + src.split('→')[0].replace('소재:', '').strip()) if src else 'ShrekMath 창작 · 수능 ' + qtype,
            'intro': [x for x in [s['intent'], (src.split('→', 1)[1].strip() if '→' in src else '')] if x],
        })
    return items


if __name__ == '__main__':
    files = sys.argv[1:] or glob.glob(os.path.join(ROOT, 'src/bank_src/*.txt'))
    for f in files:
        items = parse(f)
        out = os.path.join(ROOT, 'src/bank', 'x_' + os.path.splitext(os.path.basename(f))[0] + '.json')
        json.dump(items, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'{len(items)}문항 → {out}')
        for it in items:
            print(f"   {it['id']} {it['subject']} {it['type']} ★{it['stars']} {it['topic']} 답 {it['answer']} 본문{len(it['body'])} 풀이{len(it['solution'])}")
