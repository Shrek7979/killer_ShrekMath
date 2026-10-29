"""hwpx → 문단 단위 텍스트 (수식은 $한글수식$ 그대로). 사용: python extract_hwpx.py 파일.hwpx > out.txt"""
import sys, zipfile, re, html
import xml.etree.ElementTree as ET
NS={'hp':'http://www.hancom.co.kr/hwpml/2011/paragraph','hc':'http://www.hancom.co.kr/hwpml/2011/core'}
HP='{%s}'%NS['hp']
def para_text(p):
    out=[]
    for node in p.iter():
        if node.tag==HP+'t':
            if node.text: out.append(node.text)
            for c in node:   # hp:t 안의 lineBreak/tab 등
                if c.tail: out.append(c.tail)
        elif node.tag==HP+'script':
            s=(node.text or '').strip()
            if s: out.append(' $'+re.sub(r'\s+',' ',s)+'$ ')
        elif node.tag==HP+'tab': out.append(' ')
    return re.sub(r'\s+',' ',''.join(out)).strip()
def walk(el,depth=0):
    # 문단을 문서 순서대로. 표(tbl)/그리기 개체 안의 문단은 안쪽에서 처리하므로 바깥 문단 텍스트와 중복되지 않게 직접 자식만 모음
    for child in el:
        if child.tag==HP+'p':
            # 이 문단의 직접 텍스트(중첩 개체 제외)
            segs=[]
            for run in child.findall(HP+'run'):
                for node in run:
                    if node.tag==HP+'t':
                        segs.append(node.text or ''); segs+= [c.tail or '' for c in node]
                    elif node.tag==HP+'equation':
                        sc=node.find(HP+'script'); s=(sc.text if sc is not None and sc.text else '').strip()
                        if s: segs.append(' $'+re.sub(r'\s+',' ',s)+'$ ')
                    elif node.tag==HP+'tbl':
                        yield ('TBL',depth); yield from walk(node,depth+1); yield ('/TBL',depth)
                    elif node.tag in (HP+'pic',):
                        segs.append(' [그림] ')
                    else:
                        # container/rect 등 그리기 개체 안의 문단
                        yield from walk(node,depth+1)
            t=re.sub(r'\s+',' ',''.join(segs)).strip()
            if t: yield (t,depth)
        else:
            yield from walk(child,depth)
z=zipfile.ZipFile(sys.argv[1])
root=ET.fromstring(z.read('Contents/section0.xml'))
for t,d in walk(root):
    print(('  '*d)+t)
