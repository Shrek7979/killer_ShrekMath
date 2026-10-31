"""수능창작문항 폴더(hwpx) → 문항 은행 자동 반영

사용: python sync_bank.py <hwpx 파일이 있는 폴더 또는 hwpx 파일들...>

- 각 hwpx 의 sha1 을 src/bank_src/manifest.json 과 비교해 새 파일·바뀐 파일만 처리한다.
- 처리: extract_hwpx → src/bank_src/<slug>.txt → parse_hwpx_bank.parse → 항목 중 본문이 이미 은행에 있는 것은 버린다(중복 금지)
  → src/bank/x_<slug>.json. 파일이 바뀌었으면 그 파일의 json 을 통째로 다시 만든다(같은 파일 안의 문항은 그 파일이 책임진다).
- 은행 id 접두어는 파일명에서 뽑는다: "수능형 창작문항_2차(2022개정 교육과정).hwpx" → "2차".  (한글 그대로 둔다)
- 2015 교육과정 파일(이름에 "1차")은 manifest 에 ignore 로 적어 두고 건너뛴다. 다른 파일을 건너뛰려면 manifest 의 ignore 목록에 파일명을 적는다.
- 끝에 추가/변경 요약을 한 줄씩 출력하고, 변화가 있으면 종료 코드 0 + "CHANGED" 를, 없으면 "NOCHANGE" 를 찍는다.
"""
import sys, os, re, json, glob, hashlib, subprocess, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT, 'src/bank_src'); BANK = os.path.join(ROOT, 'src/bank')
MANI = os.path.join(SRC_DIR, 'manifest.json')
os.makedirs(SRC_DIR, exist_ok=True)


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


pb = load_mod('parse_hwpx_bank', os.path.join(ROOT, 'parse_hwpx_bank.py'))


def norm(blocks):
    """본문 블록 → 비교용 지문 (공백·기호 제거, 앞 120자)"""
    flat = []
    for b in blocks or []:
        if b[0] in ('p', 'eq'): flat.append(str(b[1]))
        elif b[0] in ('box', 'table'): flat.append(' '.join(' '.join(r) if isinstance(r, list) else str(r) for r in b[1]))
    s = re.sub(r'[^0-9A-Za-z가-힣]', '', ''.join(flat))
    return s


def bank_fingerprints(exclude_file=None):
    fp = {}
    for f in sorted(glob.glob(os.path.join(BANK, '*.json'))):
        if exclude_file and os.path.abspath(f) == os.path.abspath(exclude_file): continue
        try:
            for it in json.load(open(f, encoding='utf-8')):
                fp[norm(it.get('body'))] = it['id']
        except Exception:
            pass
    return fp


def slug_of(fname):
    stem = os.path.splitext(os.path.basename(fname))[0]
    s = re.sub(r'^수능형\s*창작문항[_\s-]*', '', stem).strip()
    s = re.sub(r'[()]', ' ', s).strip()             # 괄호는 공백으로 (과목 구분이 괄호 안에 있으므로 남긴다)
    s = re.sub(r'[\s_]+', '_', s)
    return s or hashlib.sha1(stem.encode()).hexdigest()[:8]


def extract(hwpx, txt):
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'src/essay/extract_hwpx.py'), hwpx], capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(r.stderr[-500:])
    open(txt, 'w', encoding='utf-8').write(r.stdout)


def main(args):
    files = []
    for a in args:
        if os.path.isdir(a): files += sorted(glob.glob(os.path.join(a, '*.hwpx')))
        elif a.lower().endswith('.hwpx'): files.append(a)
    mani = json.load(open(MANI, encoding='utf-8')) if os.path.exists(MANI) else {'files': {}, 'ignore': []}
    changed, report = False, []
    for f in files:
        name = os.path.basename(f)
        if any(ig in name for ig in mani['ignore']):
            report.append(f'건너뜀(ignore): {name}'); continue
        sha = hashlib.sha1(open(f, 'rb').read()).hexdigest()
        prev = mani['files'].get(name)
        if prev and prev.get('sha1') == sha:
            continue
        slug = slug_of(name)
        txt = os.path.join(SRC_DIR, slug + '.txt'); outj = os.path.join(BANK, 'x_' + slug + '.json')
        extract(f, txt)
        items = pb.parse(txt, name=slug)
        fp = bank_fingerprints(exclude_file=outj)
        kept, dup = [], []
        for it in items:
            k = norm(it['body'])
            if k in fp: dup.append(f"{it['id']}≈{fp[k]}")
            else: kept.append(it); fp[k] = it['id']
        if kept:
            json.dump(kept, open(outj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        elif os.path.exists(outj):
            os.remove(outj)
        mani['files'][name] = {'sha1': sha, 'slug': slug, 'items': len(kept), 'dups': len(dup), 'status': 'updated' if prev else 'new'}
        changed = True
        report.append(f"{'갱신' if prev else '추가'}: {name} → {len(kept)}문항 (중복 제외 {len(dup)})" + (f"  [{', '.join(dup[:6])}{'…' if len(dup) > 6 else ''}]" if dup else ''))
        report += [f"   + {it['id']} {it['subject']} {it['type']} ★{it['stars']} {it['topic']} (답 {it['answer']})" for it in kept]
    json.dump(mani, open(MANI, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n'.join(report) if report else '처리할 파일 없음')
    print('CHANGED' if changed else 'NOCHANGE')


if __name__ == '__main__':
    main(sys.argv[1:])
