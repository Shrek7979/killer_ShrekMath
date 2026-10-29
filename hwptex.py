"""한글(HWP) 수식 문법 → KaTeX(LaTeX) 변환기.

문항은행·수리논술 자료는 한글 수식 편집기 문법({a} over {b}, LEFT ( … RIGHT ), rm AB it, le, ge, inf,
root {3} of {x}, rarrow, ` 공백 …)으로 작성되어 있다. 웹에서 KaTeX로 렌더링하려면 LaTeX로 바꿔야 한다.

사용:  from hwptex import hwp2tex, convert_text
  hwp2tex('{pi} over {3}')            -> '\\frac{\\pi}{3}'
  convert_text('각 $theta = pi$ 에서') -> '각 $\\theta = \\pi$ 에서'
"""
import re

WORDS = {
    'pi': r'\pi', 'alpha': r'\alpha', 'beta': r'\beta', 'gamma': r'\gamma', 'theta': r'\theta',
    'lambda': r'\lambda', 'mu': r'\mu', 'omega': r'\omega', 'phi': r'\phi', 'delta': r'\delta',
    'epsilon': r'\varepsilon', 'sigma': r'\sigma', 'rho': r'\rho', 'tau': r'\tau', 'xi': r'\xi',
    'le': r'\le', 'ge': r'\ge', 'ne': r'\ne', 'leq': r'\le', 'geq': r'\ge', 'neq': r'\ne',
    'inf': r'\infty', 'infty': r'\infty', 'infinity': r'\infty',
    'times': r'\times', 'cdot': r'\cdot', 'cdots': r'\cdots',
    'ldots': r'\ldots', 'dots': r'\cdots', 'vdots': r'\vdots', 'ddots': r'\ddots',
    'pm': r'\pm', 'mp': r'\mp', 'div': r'\div',
    'sin': r'\sin', 'cos': r'\cos', 'tan': r'\tan', 'sec': r'\sec', 'csc': r'\csc', 'cot': r'\cot',
    'log': r'\log', 'ln': r'\ln', 'exp': r'\exp',
    'lim': r'\lim', 'sum': r'\sum', 'int': r'\int', 'prod': r'\prod', 'max': r'\max', 'min': r'\min',
    'sqrt': r'\sqrt', 'bar': r'\overline', 'vec': r'\vec', 'hat': r'\hat', 'dot': r'\dot', 'tilde': r'\tilde',
    'bold': r'\mathbf',
    'angle': r'\angle', 'triangle': r'\triangle', 'parallel': r'\parallel', 'perp': r'\perp',
    'approx': r'\approx', 'equiv': r'\equiv', 'sim': r'\sim', 'in': r'\in', 'notin': r'\notin',
    'subset': r'\subset', 'supset': r'\supset', 'cup': r'\cup', 'cap': r'\cap', 'emptyset': r'\varnothing',
    'forall': r'\forall', 'exists': r'\exists', 'partial': r'\partial', 'nabla': r'\nabla',
    'therefore': r'\therefore', 'because': r'\because', 'deg': r'^\circ', 'prime': r"'",
    'rarrow': r'\rightarrow', 'larrow': r'\leftarrow', 'rightarrow': r'\rightarrow', 'leftarrow': r'\leftarrow',
    'lrarrow': r'\leftrightarrow', 'uparrow': r'\uparrow', 'downarrow': r'\downarrow',
    'circ': r'\circ', 'ast': r'\ast', 'star': r'\star', 'oplus': r'\oplus', 'otimes': r'\otimes',
    'binom': r'\binom', 'choose': r'\binom',
}
# 글자가 붙어 있는 토큰(rmA, piover2, rootn …)을 쪼갤 때 쓰는 키워드 (긴 것부터)
KEYS = sorted(set(list(WORDS) + ['over', 'root', 'of', 'rm', 'it', 'cases', 'left', 'right']), key=len, reverse=True)
NOSPLIT = {'dx', 'dy', 'dt', 'ds', 'du', 'dv', 'dr'}

TOK = re.compile(r"""
    \\left\\lbrace|\\right\\rbrace|\\left[(\[|.]|\\right[)\]|.]|\\to|\\\\|
    [A-Za-z]+|[0-9]+(?:\.[0-9]+)?|\s+|.
""", re.X | re.S)


def _pre(s):
    s = s.replace('`', ' ')                       # 한글 수식의 작은 공백
    s = s.replace('×', ' times ').replace('÷', ' div ').replace('·', ' cdot ').replace('≤', ' le ').replace('≥', ' ge ').replace('≠', ' ne ').replace('∞', ' inf ').replace('π', ' pi ').replace('°', ' deg ').replace('√', ' sqrt ')
    s = re.sub(r'[_^]\{\s*\}', ' ', s)                       # ^{} _{} 빈 첨자
    s = re.sub(r'[_^]\{\s*(?:[_^]\{\s*)*[_^]*\s*(?:\}\s*)*\}', ' ', s)   # _{_{_}} 같은 공백 꼼수
    s = re.sub(r'(?:[_^]\s*)+(?=[\s#&$)\\]|$)', ' ', s)     # 뒤에 피연산자가 없는 _ ^ (공백 꼼수)
    s = re.sub(r'(?i)LEFT\s*\(', r'\\left(', s)
    s = re.sub(r'(?i)RIGHT\s*\)', r'\\right)', s)
    s = re.sub(r'(?i)LEFT\s*\{', r'\\left\\lbrace ', s)
    s = re.sub(r'(?i)RIGHT\s*\}', r'\\right\\rbrace ', s)
    s = re.sub(r'(?i)LEFT\s*\[', r'\\left[', s)
    s = re.sub(r'(?i)RIGHT\s*\]', r'\\right]', s)
    s = re.sub(r'(?i)LEFT\s*\|', r'\\left|', s)
    s = re.sub(r'(?i)RIGHT\s*\|', r'\\right|', s)
    s = re.sub(r'(?i)LEFT\s*\.', r'\\left.', s)
    s = re.sub(r'(?i)RIGHT\s*\.', r'\\right.', s)
    s = s.replace('->', r'\to')
    s = s.replace('<=', ' le ').replace('>=', ' ge ').replace('!=', ' ne ')
    s = s.replace('+-', ' pm ').replace('-+', ' mp ')
    return s


def _split_word(w):
    """piover2 → [pi, over]; rmA → [rm, A]; ita → [it, a]; rootn → [root, n]"""
    if w.lower() in WORDS or w in ('over', 'root', 'of', 'rm', 'it', 'cases', 'left', 'right'):
        return [w]
    if len(w) == 1 or w in NOSPLIT:
        return [w]
    out, i = [], 0
    while i < len(w):
        for k in KEYS:
            if w[i:i + len(k)].lower() == k and (len(k) > 1):
                out.append(k); i += len(k); break
        else:
            out.append(w[i]); i += 1
    return out


def _tokens(s):
    """(토큰, 앞에 공백 있었나) 목록. 공백 여부는 over의 결합 범위를 정할 때 쓴다."""
    toks, sp = [], True
    for t in TOK.findall(s):
        if t.isspace():
            sp = True; continue
        if re.fullmatch(r'[A-Za-z]+', t):
            parts = _split_word(t)
            for k, p in enumerate(parts):
                toks.append((p, sp if k == 0 else False))
        else:
            toks.append((t, sp))
        sp = False
    return toks


def _parse(tokens, i=0, close=None):
    out = []
    while i < len(tokens):
        t, sp = tokens[i]
        if t == '{':
            node, i = _parse(tokens, i + 1, '}')
            out.append(('g', node, sp))
            continue
        if t == '}':
            if close == '}':
                return out, i + 1
            i += 1
            continue
        out.append(('t', t, sp))
        i += 1
    return out, i


def _kw(n, *names):
    return n[0] == 't' and n[1].lower() in names


def _rm_it(nodes):
    """rm A B it  ->  \\mathrm{AB}"""
    out, i = [], 0
    while i < len(nodes):
        n = nodes[i]
        if _kw(n, 'rm'):
            j, buf = i + 1, []
            if j < len(nodes) and _kw(nodes[j], 'bar'):      # rm bar AB → bar{rm AB}
                out.append(('t', 'bar', True)); j += 1
            if j < len(nodes) and nodes[j][0] == 'g':         # rm {AB}
                out.append(('rm', _rm_it(nodes[j][1]), True)); i = j + 1
                continue
            while j < len(nodes) and not _kw(nodes[j], 'it', 'rm'):
                nj = nodes[j]
                if nj[0] == 't' and re.fullmatch(r"[A-Za-z0-9']+", nj[1]) and nj[1].lower() not in WORDS:
                    buf.append(nj); j += 1; continue
                break
            if buf:
                out.append(('rm', buf, True))
            i = j + (1 if j < len(nodes) and _kw(nodes[j], 'it') else 0)
            continue
        if _kw(n, 'it'):
            i += 1
            continue
        if n[0] == 'g':
            out.append(('g', _rm_it(n[1]), n[2]))
        else:
            out.append(n)
        i += 1
    return out


OPS = set('+-=<>(),:;|[]&#')


def _isop(n):
    return n[0] == 't' and (n[1] in OPS or n[1].startswith('\\left') or n[1].startswith('\\right') or n[1] == '\\to')


def _take_left(out):
    """over 왼쪽 피연산자: 바로 앞 덩어리(공백 없이 붙은 토큰들, 첨자 포함). 연산자에서 멈춤"""
    if not out:
        return ('t', '', False)
    got = []
    # 뒤에 붙은 첨자 ^{..} _{..} 는 먼저 포함
    while len(out) >= 2 and out[-2][0] == 't' and out[-2][1] in ('^', '_'):
        got = out[-2:] + got; del out[-2:]
    if not out:
        return ('g', got, True)
    if out[-1][0] == 'g' or _isop(out[-1]):
        if got:
            return ('g', [out.pop()] + got, True)
        return out.pop()
    # 공백 없이 붙은 토큰들을 거슬러 모음
    got = [out.pop()] + got
    while out and not got[0][2] and not _isop(out[-1]):
        got = [out.pop()] + got
    return got[0] if len(got) == 1 else ('g', got, True)


def _take_right(nodes, i):
    """over 오른쪽 피연산자: 다음 덩어리(공백 없이 붙은 토큰들, 첨자 포함). (노드, 다음 인덱스)"""
    if i >= len(nodes):
        return ('t', '', False), i
    got = [nodes[i]]; j = i + 1
    if nodes[i][0] == 't' and not _isop(nodes[i]):
        while j < len(nodes) and not nodes[j][2] and not _isop(nodes[j]) and not _kw(nodes[j], 'over'):
            got.append(nodes[j]); j += 1
    while j + 1 < len(nodes) and nodes[j][0] == 't' and nodes[j][1] in ('^', '_'):
        got += nodes[j:j + 2]; j += 2
    return (got[0] if len(got) == 1 else ('g', got, True)), j


def _struct(nodes):
    """over / root…of / cases 처리"""
    out, i = [], 0
    while i < len(nodes):
        n = nodes[i]
        if _kw(n, 'over') and out and i + 1 < len(nodes):
            left = _take_left(out); right, i = _take_right(nodes, i + 1)
            out.append(('frac', _sub(left), _sub(right), True))
            continue
        if _kw(n, 'root') and i + 1 < len(nodes):
            a = nodes[i + 1]
            if i + 3 < len(nodes) and _kw(nodes[i + 2], 'of'):
                out.append(('nroot', _sub(a), _sub(nodes[i + 3]), True)); i += 4
            else:
                out.append(('sqrt', _sub(a), True)); i += 2
            continue
        if _kw(n, 'cases') and i + 1 < len(nodes) and nodes[i + 1][0] == 'g':
            out.append(('cases', _struct(nodes[i + 1][1]), True)); i += 2
            continue
        if _kw(n, 'bar', 'vec', 'hat', 'sqrt', 'bold') and i + 1 < len(nodes) and nodes[i + 1][0] != 'g':
            # bar PQ (그룹 없이) → \overline{PQ}: 다음 덩어리를 그룹으로
            right, i2 = _take_right(nodes, i + 1)
            out.append(n); out.append(('g', [right] if right[0] != 'g' else right[1], True)); i = i2
            continue
        out.append(_sub(n)); i += 1
    return out


def _sub(n):
    if n[0] == 'g':
        return ('g', _struct(n[1]), n[2])
    if n[0] == 'rm':
        return ('rm', _struct(n[1]), n[2] if len(n) > 2 else True)
    return n


def _join(parts):
    s = ''
    for p in parts:
        if not p:
            continue
        if s and (s[-1].isalnum() or s[-1] == "'") and (p[0].isalnum() or p[0] == '\\'):
            s += ' '
        elif s and s[-1] == '\\' and p[0].isalnum():
            s += ' '
        s += p
    return s


def _render_list(nodes):
    return _join([_render(n) for n in nodes])


def _brace(s):
    return s if (s.startswith('{') and s.endswith('}')) else '{' + s + '}'


def _render(n):
    k = n[0]
    if k == 't':
        t = n[1]
        tl = t.lower()
        if tl in WORDS and (len(t) > 1 or t == tl):
            return WORDS[tl]
        if t == '~':
            return r'\,'
        if t == '#':
            return r'\\'
        if t == '\\to':
            return r'\to'
        if tl in ('left', 'right', 'of', 'over', 'root', 'cases', 'rm', 'it'):
            return ''
        return t
    if k == 'g':
        return '{' + _render_list(n[1]) + '}'
    if k == 'rm':
        inner = _render_list(n[1])
        if '\\' in inner:
            return '{' + inner + '}'
        return r'\mathrm{' + inner.replace(' ', '').replace('{', '').replace('}', '') + '}'
    if k == 'frac':
        return r'\frac' + _brace(_render(n[1])) + _brace(_render(n[2]))
    if k == 'sqrt':
        return r'\sqrt' + _brace(_render(n[1]))
    if k == 'nroot':
        return r'\sqrt[' + _render(n[1]).strip('{}') + ']' + _brace(_render(n[2]))
    if k == 'cases':
        return r'\begin{cases}' + _render_list(n[1]) + r'\end{cases}'
    return ''


def hwp2tex(s):
    s = _pre(s)
    nodes, _ = _parse(_tokens(s))
    nodes = _rm_it(nodes)
    nodes = _struct(nodes)
    # 최상위에 줄바꿈(#)이 있으면 aligned 환경
    top_break = any(_kw(n, '#') or _kw(n, '&') for n in nodes)
    out = _render_list(nodes)
    out = re.sub(r'\s+', ' ', out).strip()
    out = out.replace(' _', '_').replace(' ^', '^').replace('_ ', '_').replace('^ ', '^')
    out = re.sub(r'\\left\\lbrace\s*', r'\\left\\{', out).replace(r'\right\rbrace', r'\right\}')
    out = re.sub(r'[_^]\{\}', '', out).replace('{}', '')  # 한글 수식의 빈 그룹
    if top_break:
        out = r'\begin{aligned}' + out + r'\end{aligned}'
    return out


def convert_text(text):
    """문단 안의 $…$ 수식만 변환. aligned가 생기면 display($$)로."""
    def rep(m):
        t = hwp2tex(m.group(1))
        return ('$$' + t + '$$') if t.startswith(r'\begin{aligned}') else ('$' + t + '$')
    return re.sub(r'\$([^$]+)\$', rep, text)


if __name__ == '__main__':
    tests = [
        '{pi} over {3}', 'sin {a pi} over {6} + 1', '3 LEFT ( -1- {1} over {2} RIGHT ) =-3',
        'bar {rm OP it} ^{2} =403', 'angle rm BAC it = {2} over {3} pi', 'rm P it _{n}',
        'lim _{x -> inf} x ^{2} e ^{-x} =0', 'sum _{n=1} ^{inf} LEFT ( {m} over {k} RIGHT ) ^{n}',
        'f(x)= cases{ x ^{2} & ~~~(x<a) # 2x+3 & ~~~(x ge a)}', 'k=1,~2,~cdots ,~19',
        '{LEFT | a RIGHT |} over {3}', 'log _{a} n=k', 'a over b + c', '{2} over {1+ {1} over {9}}',
        'lim _{n`->`inf} {} {a _{n}`^{2}} over {root {3} of {n ^{2}}} `',
        'lim _{n` rarrow ` INF } {} root {3} of {n} TIMES LEFT ( a _{n+1}`^{2} -a _{n}`^{2} RIGHT ) `',
        'rmP(ita,```0,```b)', 'LEQ 1over6 LEFT | `x`RIGHT |', 'sin`alpha = root2 over4 `', 't= 2pi over 3',
        'f`\'(0)= lim _{t` rarrow `0+} {} {f(t)-f(0)} over {t}', '\\P left( 0`,`` - root{5} over 2 right)',
        'A & = b # & = c', 'rm bar PQ = it 2x over{x^2 +2}', 'ANGLE rm POQ `= theta', 'rmbar{AB}:bar{AD _{1} }=itm:1',
        'int_0^x t f(x-t) dt', 'e^x = e^2 over 2 + 1 over 2e', 'bold{k}',
    ]
    for t in tests:
        print(t, '\n   ->', hwp2tex(t))
