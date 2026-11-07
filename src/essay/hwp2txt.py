"""hwp(5.x) → extract_hwpx.py 와 같은 문단 텍스트 (수식 $한글수식$, 표 TBL … /TBL, 그림 [그림]).
사용: python hwp2txt.py 파일.hwp > seasonNN.txt   (pyhwp 필요: pip install pyhwp)
pyhwp 의 xml 출력에는 수식 내용이 빠져 있어서, HWPTAG_CTRL_EQEDIT 레코드에서 수식 스크립트를 꺼내 문서 순서대로 채운다."""
import sys, re, json, subprocess, tempfile, os
import xml.etree.ElementTree as ET
hwp = sys.argv[1]
secs = [l.strip() for l in subprocess.run(['hwp5proc', 'ls', hwp], capture_output=True, text=True).stdout.split('\n') if l.startswith('BodyText/')]
EQ = []
for sec in sorted(secs, key=lambda x: int(x.split('Section')[1])):
    js = subprocess.run(['hwp5proc', 'models', hwp, sec.replace('BodyText/Section', 'bodytext/')], capture_output=True, text=True).stdout
    for r in json.loads(js):
        if r.get('tagname') == 'HWPTAG_CTRL_EQEDIT':
            b = bytes.fromhex(' '.join(r['payload'])); n = int.from_bytes(b[4:6], 'little')
            EQ.append(b[6:6 + 2 * n].decode('utf-16-le'))
xml = subprocess.run(['hwp5proc', 'xml', hwp], capture_output=True, text=True).stdout
root = ET.fromstring(xml)
assert sum(1 for _ in root.iter('EqEdit')) == len(EQ), '수식 개수 불일치'
k = [0]
SKIP = ('HeaderParagraphList', 'FooterParagraphList', 'Header', 'Footer', 'FootNote', 'EndNote')
def eq():
    s = EQ[k[0]]; k[0] += 1
    return ' $' + re.sub(r'\s+', ' ', s).strip() + '$ '
def skip(el):
    k[0] += sum(1 for _ in el.iter('EqEdit'))
def walk(el, depth=0):
    for ch in el:
        if ch.tag in SKIP:
            skip(ch); continue
        if ch.tag == 'Paragraph':
            segs = []
            for ls in ch:
                if ls.tag != 'LineSeg':
                    if ls.tag in SKIP: skip(ls)
                    else: yield from walk(ls, depth)
                    continue
                for nd in ls:
                    if nd.tag == 'Text':
                        segs.append(nd.text or '')
                    elif nd.tag == 'ControlChar':
                        if nd.get('name') in ('TAB',): segs.append(' ')
                    elif nd.tag == 'Control' and nd.find('EqEdit') is not None:
                        segs.append(eq())
                    elif nd.tag == 'TableControl':
                        yield ('TBL', depth); yield from walk(nd, depth + 1); yield ('/TBL', depth)
                    elif nd.tag == 'GShapeObjectControl':
                        if any(True for _ in nd.iter('ShapePicture')) and not any(True for _ in nd.iter('TextboxParagraphList')):
                            segs.append(' [그림] ')
                        else:
                            yield from walk(nd, depth + 1)
                    elif nd.tag in SKIP or any(nd.iter(t) for t in ()):
                        skip(nd)
                    else:
                        # 머리말/꼬리말 등 그 밖의 컨트롤: 안쪽 문단은 버리되 수식 순서는 맞춘다
                        if any(True for _ in nd.iter('HeaderParagraphList')) or any(True for _ in nd.iter('FooterParagraphList')):
                            skip(nd)
                        else:
                            yield from walk(nd, depth + 1)
            t = re.sub(r'\s+', ' ', ''.join(segs)).strip()
            if t: yield (t, depth)
        else:
            yield from walk(ch, depth)
for t, d in walk(root):
    print(('  ' * d) + t)
assert k[0] == len(EQ), (k[0], len(EQ))
