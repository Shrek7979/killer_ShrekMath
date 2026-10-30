"""킬러 분석학 · 수학 — 사이트 빌드 스크립트

입력
  src/bank/q*_final.json   수능형 창작문항 은행 (한글 수식 문법)
  anatomy/<문항id>.json    교사가 쓰는 완전 분석 파일 (LaTeX 문법, 선택)
  template.html            앱 템플릿

출력
  site/index.html, site/list.json, site/data/NNN.json   → 정적 호스팅(Cloudflare Pages/Workers 등)용
  killer-math.html                                        → 데이터를 한 파일에 넣은 단일 파일(공유·아티팩트용)

실행:  python3 build.py
"""
import json, re, glob, os, html
from hwptex import convert_text, hwp2tex

ROOT = os.path.dirname(os.path.abspath(__file__))
BANK = sorted(glob.glob(os.path.join(ROOT, 'src/bank/q*_final.json'))) + sorted(glob.glob(os.path.join(ROOT, 'src/bank/x_*.json')))
ANAT = os.path.join(ROOT, 'anatomy')
SITE = os.path.join(ROOT, 'site')

MIN_STARS = 3   # 이 난도 이상만 사이트에 올린다 (완전 분석 파일이 있는 문항은 항상 포함)
TYPE_OF = {'20': '20번형', '21': '21번형', '29': '29번형', '30': '30번형'}
TYPE_DESC = {
    '20': '공통 4점 · 대수 고난도', '21': '공통 4점 · 미적분Ⅰ 최고난도',
    '29': '선택 단답형 · 미적분Ⅱ', '30': '선택 단답형 · 미적분Ⅱ 최고난도',
}

# 문장 분리: "…다. ", "…자. ", "…시오. " 뒤에서 자른다. 수식 안의 소수점은 공백이 따라오지 않아 안전하다.
SENT = re.compile(r'(?<=[다자오])\.\s+(?=\S)')


def split_sentences(p):
    parts = SENT.split(p)
    # 잘린 자리에 마침표 복원
    parts = [s if (i == len(parts) - 1 or s.endswith(('.', '?', ']', ')'))) else s + '.' for i, s in enumerate(parts)]
    # "[4점]" 같은 배점 표시는 앞 문장에 붙인다
    out = []
    for s in parts:
        if re.fullmatch(r'\[\d점\]', s) and out:
            out[-1] += ' ' + s
        else:
            out.append(s)
    return out


def conv_block(b):
    """은행 블록 → 사이트 블록 (수식 LaTeX로 변환)"""
    kind = b[0]
    if kind == 'p':
        return {'t': 'p', 'sents': split_sentences(convert_text(b[1]))}
    if kind == 'eq':
        return {'t': 'eq', 'tex': hwp2tex(b[1])}
    if kind == 'box':
        return {'t': 'box', 'items': [convert_text(x) for x in b[1]]}
    if kind == 'table':
        return {'t': 'table', 'rows': [[convert_text(c) for c in r] for r in b[1]]}
    return {'t': 'p', 'sents': [convert_text(str(b[1]))]}


def build_conds(blocks):
    """본문의 문장 하나하나를 조건 C1, C2…로 번호 붙인다 (풀이 단계·함정 카드와 연결용)"""
    conds = []
    for bi, b in enumerate(blocks):
        if b['t'] == 'p':
            for si, s in enumerate(b['sents']):
                conds.append({'id': f'C{len(conds)+1}', 'at': [bi, si], 'text': s})
        elif b['t'] == 'box':
            for si, s in enumerate(b['items']):
                conds.append({'id': f'C{len(conds)+1}', 'at': [bi, si], 'text': s})
        elif b['t'] == 'eq':
            conds.append({'id': f'C{len(conds)+1}', 'at': [bi, 0], 'text': '$' + b['tex'] + '$'})
    return conds


def load_overlay(qid):
    p = os.path.join(ANAT, qid + '.json')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    return {}


def make_item(num, q, type_code):
    ov = load_overlay(q['id'])
    qtype = q.get('type') or TYPE_OF.get(type_code, (type_code or '') + '번형')
    tdesc = TYPE_DESC[type_code] if type_code in TYPE_DESC else f"{q['subject']} · 수능 {qtype} 자리의 고난도"
    blocks = [conv_block(b) for b in q['body']]
    conds = build_conds(blocks)
    for c in conds:                       # 교사 분석 파일의 조건 설명 합치기
        o = ov.get('conds', {}).get(c['id'], {})
        c['label'] = o.get('label', '')
        c['why'] = o.get('why', '')
        c['uses'] = o.get('uses', [])

    if ov.get('steps'):
        steps = [{'n': i + 1, 'text': s['text'], 'uses': s.get('uses', []), 'title': s.get('title', '')}
                 for i, s in enumerate(ov['steps'])]
    else:
        steps = []
        for i, b in enumerate(q['solution']):
            cb = conv_block(b)
            text = ' '.join(cb['sents']) if cb['t'] == 'p' else ('$$' + cb['tex'] + '$$' if cb['t'] == 'eq' else ' / '.join(cb['items']))
            steps.append({'n': i + 1, 'text': text, 'uses': [], 'title': ''})

    full = bool(ov.get('traps')) and bool(ov.get('conds'))
    return {
        'num': num, 'id': q['id'], 'subject': q['subject'], 'topic': q['topic'],
        'type': qtype, 'typeDesc': tdesc, 'stars': q.get('stars', 3),
        'standards': q.get('standards', []),
        'source': ov.get('source', q.get('source', f'ShrekMath 창작 · 수능 {qtype}')),
        'rate': ov.get('rate', ''), 'wrong': ov.get('wrong', ''),
        'answer': q['answer'], 'full': full,
        'body': blocks, 'conds': conds,
        'intro': ov.get('intro', q.get('intro', [])),
        'concepts': ov.get('concepts', []),
        'steps': steps,
        'traps': ov.get('traps', []),
        'variants': ov.get('variants', []),
        'line': ov.get('line', ''),
        'note': ov.get('note', ''),
    }


def joinlines(ls):
    """채점 기준: 줄이 중간에 끊긴 문장은 이어 붙인다"""
    out = []
    for t in ls:
        if out and not re.match(r'^[-·•(\d○※]', t) and not re.search(r'[.다함음임됨\)]\s*$', out[-1]):
            out[-1] += ' ' + t
        else:
            out.append(t)
    return out


def essay_items():
    """src/essay/items_*.json (parse_essay.py 결과) → 사이트용 논술 문항"""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/essay/items_*.json'))):
        with open(f, encoding='utf-8') as fp:
            for it in json.load(fp):
                ct = convert_text
                subs = []
                for sub in it['subs']:
                    subs.append({'k': sub['k'], 'label': sub['label'], 'points': sub['points'],
                                 'text': [ct(t) for t in sub['text']],
                                 'answer': [ct(t) for t in sub['answer']], 'rubric': [ct(t) for t in joinlines(sub['rubric'])]})
                head = re.sub(r'^\[[^\]]*\]\s*', '', it['head'] or '')
                passage = [t for t in it['passage'] if t.strip() != head.strip()]
                topic = (it['info'] or {}).get('concepts', '')
                out.append({
                    'num': len(out) + 1, 'id': it['id'], 'univ': it['univ'], 'n': it['n'],
                    'title': f"문제 {it['n']}" + (f" · {it['points']}점" if it['points'] else ''),
                    'head': ct(head), 'points': it['points'], 'minutes': it['minutes'], 'info': it['info'],
                    'pre': [ct(t) for t in it['pre']], 'passage': [ct(t) for t in passage],
                    'subs': subs, 'answer': [ct(t) for t in it['answer']], 'rubric': [ct(t) for t in joinlines(it['rubric'])],
                    'field': (topic.split(',')[0].strip() if topic else ''),
                })
    return out


def japan_items():
    """src/japan/index.json + img/ → 일본 대학 문제 목록 (★4 이상, 이미지 기반)"""
    p = os.path.join(ROOT, 'src/japan/index.json')
    if not os.path.exists(p):
        return []
    out = []
    for x in json.load(open(p, encoding='utf-8')):
        if x['stars'] < 4:
            continue
        q = [f"jp/{x['id']}-q{k}.webp" for k in range(len(x['pages']))]
        s = [f"jp/{x['id']}-s{k}.webp" for k in range(len(x['spages']))]
        if not all(os.path.exists(os.path.join(ROOT, 'src/japan/img', os.path.basename(f))) for f in q + s):
            continue
        univ, _, track = x['univ'].partition('·')
        text = re.sub(r'[\u200b\ue000-\uf8ff]', '', x['text']).strip()
        out.append({'num': len(out) + 1, 'id': x['id'], 'year': x['year'], 'num0': x['num'], 'stars': x['stars'],
                    'univ': univ.strip(), 'track': track.strip() or '이과', 'subj': x['subj'] or '', 'text': text[:90],
                    'qimg': q, 'simg': s})
    return out


ART_EXT = ('.webp', '.png', '.jpg', '.jpeg')


def art_path(key):
    """src/art/<key>.<ext> 가 있으면 사이트 경로(art/<key>.<ext>) 반환"""
    for ext in ART_EXT:
        p = os.path.join(ROOT, 'src/art', key + ext)
        if os.path.exists(p):
            return 'art/' + key + ext
    return ''


def copy_art():
    """src/art/ (문항별) 와 src/art/cat/ (주제별) 를 site/art/ 로"""
    import shutil
    dst = os.path.join(SITE, 'art'); shutil.rmtree(dst, ignore_errors=True)
    cats = {}
    for sub in ('', 'cat'):
        src = os.path.join(ROOT, 'src/art', sub)
        if not os.path.isdir(src):
            continue
        os.makedirs(os.path.join(dst, sub), exist_ok=True)
        for f in os.listdir(src):
            if f.lower().endswith(ART_EXT):
                shutil.copy(os.path.join(src, f), os.path.join(dst, sub, f))
                if sub == 'cat':
                    cats[os.path.splitext(f)[0]] = 'art/cat/' + f
    return cats


def snip_blocks(body):
    """카드 썸네일용 문항 발췌: 첫 수식·박스 조건과 그 앞뒤 문장 (없으면 앞 두 문장)"""
    flat = []
    for b in body:
        if b['t'] == 'p':
            flat += [{'t': 'p', 's': s} for s in b['sents']]
        elif b['t'] == 'eq':
            flat.append({'t': 'eq', 'tex': b['tex']})
        elif b['t'] == 'box':
            flat.append({'t': 'box', 'items': b['items'][:3]})
    k = next((i for i, x in enumerate(flat) if x['t'] != 'p'), None)
    return flat[max(0, k - 1):k + 2] if k is not None else flat[:2]


def essay_snip(e):
    lines = [s for s in e['passage'] if s.strip() and '[그림]' not in s]
    return [{'t': 'p', 's': s} for s in lines[:4]]


def encrypt_payload(obj, password):
    """AES-GCM + PBKDF2. 페이지의 unlockData()와 짝."""
    import base64, secrets, hashlib
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    salt = secrets.token_bytes(16); iv = secrets.token_bytes(12); iters = 200000
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iters, 32)
    data = AESGCM(key).encrypt(iv, json.dumps(obj, ensure_ascii=False).encode('utf-8'), None)
    b64 = lambda b: base64.b64encode(b).decode()
    return {'salt': b64(salt), 'iv': b64(iv), 'iter': iters, 'data': b64(data)}


def main():
    import argparse, shutil
    ap = argparse.ArgumentParser()
    ap.add_argument('--key', help='접근 코드. 주면 문항 데이터를 암호화해서 넣는다 (학생은 코드를 입력해야 열림)')
    args = ap.parse_args()

    items = []
    for f in BANK:
        mcode = re.search(r'q(\d\d)[AB]_', os.path.basename(f))
        code = mcode.group(1) if mcode else None
        with open(f, encoding='utf-8') as fp:
            for q in json.load(fp):
                if q.get('stars', 3) < MIN_STARS and not os.path.exists(os.path.join(ANAT, q['id'] + '.json')):
                    continue
                items.append(make_item(len(items) + 1, q, code))
    cats = copy_art()
    lst = [{'num': x['num'], 'id': x['id'], 'subject': x['subject'], 'type': x['type'], 'topic': x['topic'],
            'stars': x['stars'], 'rate': x['rate'], 'full': x['full'], 'nconds': len(x['conds']), 'nsteps': len(x['steps']), 'art': art_path(x['id']),
            'snip': snip_blocks(x['body'])}
           for x in items]
    essays = essay_items()
    japan = japan_items()
    elst = [{'num': e['num'], 'id': e['id'], 'univ': e['univ'], 'n': e['n'], 'title': e['title'], 'points': e['points'],
             'minutes': e['minutes'], 'nsubs': len(e['subs']), 'field': e['field'], 'art': art_path('essay-' + str(e['num'])), 'snip': essay_snip(e)} for e in essays]
    for j in japan:
        j['art'] = art_path(j['id'])

    with open(os.path.join(ROOT, 'template.html'), encoding='utf-8') as f:
        tpl = f.read()
    with open(os.path.join(ROOT, 'src/katex.inline.css'), encoding='utf-8') as f:
        tpl = tpl.replace('/*__KATEX_CSS__*/', f.read())

    for d in ('data', 'edata', 'jp'):
        shutil.rmtree(os.path.join(SITE, d), ignore_errors=True)
    for fn in ('list.json', 'elist.json', 'jlist.json', 'enc.json'):
        p = os.path.join(SITE, fn)
        if os.path.exists(p): os.remove(p)
    os.makedirs(SITE, exist_ok=True)
    dump = lambda obj, p: json.dump(obj, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 일본 문제 이미지는 암호화 여부와 상관없이 site/jp/ 에 복사 (단일 파일에는 data URI로 인라인)
    import base64
    os.makedirs(os.path.join(SITE, 'jp'), exist_ok=True)
    jimg_js = {}
    for j in japan:
        for f in j['qimg'] + j['simg']:
            src = os.path.join(ROOT, 'src/japan/img', os.path.basename(f))
            shutil.copy(src, os.path.join(SITE, 'jp', os.path.basename(f)))
            jimg_js[f] = 'data:image/webp;base64,' + base64.b64encode(open(src, 'rb').read()).decode()
    # 카드 그림(art/)도 단일 파일에는 인라인
    art_dir = os.path.join(SITE, 'art')
    if os.path.isdir(art_dir):
        for dp, _, fs in os.walk(art_dir):
            for fn in fs:
                if fn.lower().endswith(ART_EXT):
                    full = os.path.join(dp, fn); rel = os.path.relpath(full, SITE).replace(os.sep, '/')
                    mime = 'image/webp' if fn.lower().endswith('.webp') else 'image/png' if fn.lower().endswith('.png') else 'image/jpeg'
                    jimg_js[rel] = f'data:{mime};base64,' + base64.b64encode(open(full, 'rb').read()).decode()
    jimg_script = 'window.__JIMG__=' + json.dumps(jimg_js) + ';'

    if args.key:
        payload = {'list': lst, 'data': {x['num']: x for x in items}, 'elist': elst, 'edata': {e['num']: e for e in essays}, 'jlist': japan, 'cats': cats}
        enc = encrypt_payload(payload, args.key)
        dump(enc, os.path.join(SITE, 'enc.json'))
        data_js = 'window.__ENC__=' + json.dumps(enc) + ';' + jimg_script
        mode = f'암호화(접근 코드 사용)'
    else:
        os.makedirs(os.path.join(SITE, 'data')); os.makedirs(os.path.join(SITE, 'edata'))
        dump(lst, os.path.join(SITE, 'list.json')); dump(elst, os.path.join(SITE, 'elist.json')); dump(japan, os.path.join(SITE, 'jlist.json')); dump(cats, os.path.join(SITE, 'cats.json'))
        for x in items: dump(x, os.path.join(SITE, 'data', f"{x['num']:03d}.json"))
        for e in essays: dump(e, os.path.join(SITE, 'edata', f"{e['num']:03d}.json"))
        data_js = ('window.__LIST__=' + json.dumps(lst, ensure_ascii=False) + ';\n' +
                   'window.__DATA__=' + json.dumps({x['num']: x for x in items}, ensure_ascii=False) + ';\n' +
                   'window.__ELIST__=' + json.dumps(elst, ensure_ascii=False) + ';\n' +
                   'window.__EDATA__=' + json.dumps({e['num']: e for e in essays}, ensure_ascii=False) + ';\n' +
                   'window.__JLIST__=' + json.dumps(japan, ensure_ascii=False) + ';\n' +
                   'window.__CATS__=' + json.dumps(cats) + ';' + jimg_script)
        mode = '공개'
    data_js = data_js.replace('</', '<\\/')
    # 정적 호스팅(Vercel 등)용: 완전한 HTML 뼈대로 감싼다 (아티팩트용 파일은 뼈대 없이)
    skeleton = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
                '<meta name="description" content="킬러들의 수학몰 · 수능 킬러 문항 분석, 대학별 수리논술, 일본 대학 입시 수학">\n'
                '<meta name="theme-color" content="#141414">\n'
                '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="수학몰">\n'
                '<link rel="manifest" href="manifest.json">\n'
                '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}</style>\n'
                '</head>\n<body>\n__BODY__\n</body>\n</html>\n')
    with open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(skeleton.replace('__BODY__', tpl.replace('/*__INLINE_DATA__*/', '')))
    with open(os.path.join(SITE, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump({'name': '킬러들의 수학몰', 'short_name': '수학몰', 'start_url': './', 'display': 'standalone', 'background_color': '#141414', 'theme_color': '#141414',
                   'icons': [{'src': 'icon.svg', 'sizes': 'any', 'type': 'image/svg+xml'}]}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(SITE, 'icon.svg'), 'w', encoding='utf-8') as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#141414"/><circle cx="50" cy="50" r="28" fill="none" stroke="#e50914" stroke-width="6"/><circle cx="50" cy="50" r="10" fill="none" stroke="#e50914" stroke-width="5"/><path d="M50 8v18M50 74v18M8 50h18M74 50h18" stroke="#e50914" stroke-width="6" stroke-linecap="round"/></svg>')
    with open(os.path.join(SITE, 'vercel.json'), 'w', encoding='utf-8') as f:
        json.dump({'cleanUrls': True, 'headers': [{'source': '/(.*)\\.json', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=300'}]}]}, f, indent=1)
    with open(os.path.join(ROOT, 'killer-math.html'), 'w', encoding='utf-8') as f:
        f.write(tpl.replace('/*__INLINE_DATA__*/', data_js))

    nfull = sum(1 for x in items if x['full'])
    print(f'킬러 {len(items)}개 (완전 분석 {nfull}개) · 논술 {len(essays)}개 · 일본 {len(japan)}개 · {mode} → site/, killer-math.html')


if __name__ == '__main__':
    main()
