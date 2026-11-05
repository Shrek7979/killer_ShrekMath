"""문제지 묶음 PDF 끝의 '수학 영역 정답표' → {시험: {c1..c22, k23..k30, m23..m30, g23..g30}}
사용: python parse_answers.py <공통.pdf> answers.json <출력.json>"""
import re, sys, json, subprocess
CIR = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
def val(t): return CIR.get(t, int(t) if re.fullmatch(r'[0-9]+', t) else None)
def tables(pdf):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    blocks = txt.split('수학 영역 정답표')[1:]
    out = []
    for b in blocks:
        ans = {}
        for line in b.split('\n'):
            tk = line.split()
            if not tk or not re.fullmatch(r'[0-9]+', tk[0]) or len(tk) % 3: continue
            gr = [tk[i:i + 3] for i in range(0, len(tk), 3)]
            if not all(re.fullmatch(r'[0-9]+', g[0]) and val(g[1]) is not None for g in gr): continue
            n0 = int(gr[0][0])
            if n0 > 11: continue
            ans[f'c{n0}'] = val(gr[0][1])
            if len(gr) > 1: ans[f'c{int(gr[1][0])}'] = val(gr[1][1])
            for key, g in zip('kmg', gr[2:5]): ans[f'{key}{int(g[0])}'] = val(g[1])
        out.append(ans)
    return out
if __name__ == '__main__':
    # 정답표에는 시험 이름이 일정하지 않아, answers.json 의 기존 정답(14·15·20~22·28~30번)과 맞춰 어느 시험인지 정한다
    known = {k: v for k, v in json.load(open(sys.argv[2], encoding='utf-8')).items() if not k.startswith('_')}
    res = {}
    for t in tables(sys.argv[1]):
        m = [ex for ex, d in known.items() if all(t.get(k) == v for k, v in d.items() if v is not None)]
        assert len(m) == 1 and len(t) == 46, (m, len(t))
        res[m[0]] = t
    json.dump(res, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('정답표', len(res), '회 · 없음:', sorted(set(known) - set(res)))
