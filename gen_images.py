"""카드 삽화 생성 (OpenAI 이미지 API) — 선택 사항

두 가지 방식 모두 build.py 가 자동으로 집어 쓴다.
  1) 문항별 그림:  src/art/<문항id>.png            (예: src/art/20A-02.png, src/art/2021-035.png, 논술은 src/art/essay-<num>.png)
  2) 주제별 그림:  src/art/cat/<그림키>.png         (예: src/art/cat/parabola.png, log.png, dice.png …  template.html 의 PIC 키와 같음)
문항별 그림이 있으면 그것을, 없으면 주제별 그림을, 그것도 없으면 내장 SVG 삽화를 쓴다.
ChatGPT 화면에서 직접 만든 이미지를 위 이름으로 저장해 넣어도 된다.

이 스크립트는 OpenAI API 로 자동 생성한다.
  pip install openai pillow
  set OPENAI_API_KEY=sk-...          (Windows)   /  export OPENAI_API_KEY=sk-...  (mac/linux)
  python gen_images.py --cat          # 주제별 27장 (권장, 약 $0.5~1)
  python gen_images.py --killer       # 킬러관 72문항 각각 (약 $1~3)
  python gen_images.py --all          # 전부 (357장, 약 $5~10)
생성 크기는 1024x1536(2:3 포스터), 저장은 WebP 로 줄여서(약 40KB) 저장한다.
"""
import os, sys, json, glob, re, io, base64, argparse
ROOT = os.path.dirname(os.path.abspath(__file__))
STYLE = ("minimalist flat vector illustration for a math poster, dark charcoal background, one bold white line drawing "
         "with a single gold accent, no text, no letters, no numbers, no formulas, centered composition, high contrast, clean edges")
CATS = {
 'parabola': '포물선 위의 점과 접선', 'tangent': '곡선과 접선, 극값 점', 'area': '곡선 아래 넓이(정적분)', 'inflect': 'S자 곡선의 변곡점',
 'sine': '사인 파형', 'exp': '지수함수 곡선과 점근선', 'log': '로그함수 곡선', 'seq': '커지는 막대 수열', 'series': '줄어드는 막대 급수',
 'limit': '점근선에 가까워지는 곡선(극한)', 'inverse': 'y=x 대칭인 두 곡선(역함수)', 'circle': '원과 현, 반지름', 'triangle': '삼각형과 높이',
 'ellipse': '타원과 두 초점', 'hyper': '쌍곡선과 점근선', 'vector': '두 벡터 화살표와 내적', 'space': '공간의 상자와 평면', 'sphere': '구와 적도선',
 'dice': '주사위 두 개(확률)', 'normal': '정규분포 종 모양 곡선', 'count': '색칠된 공 배열(경우의 수)', 'integer': '수직선 위 정수 점',
 'poly': '삼차함수 곡선과 근', 'set': '벤 다이어그램', 'ineq': '부등식 영역 색칠', 'motion': '궤적 위를 움직이는 점', 'essay': '답안지와 펜',
}
def client():
    from openai import OpenAI
    return OpenAI()
def gen(c, prompt, out):
    if os.path.exists(out): return
    r = c.images.generate(model='gpt-image-1', prompt=f'{prompt}. {STYLE}', size='1024x1536', quality='low', n=1)
    b = base64.b64decode(r.data[0].b64_json)
    from PIL import Image
    im = Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((600, 900))
    os.makedirs(os.path.dirname(out), exist_ok=True); im.save(out, 'WEBP', quality=72); print('saved', out)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--cat', action='store_true'); ap.add_argument('--killer', action='store_true'); ap.add_argument('--all', action='store_true')
    a = ap.parse_args(); c = client()
    if a.cat or a.all:
        for k, desc in CATS.items(): gen(c, f'{desc} 를 상징하는 그림', os.path.join(ROOT, 'src/art/cat', k + '.webp'))
    if a.killer or a.all:
        for f in glob.glob(os.path.join(ROOT, 'src/bank/*.json')):
            for q in json.load(open(f, encoding='utf-8')): gen(c, f"고등학교 수학 '{q['topic']}' 를 상징하는 그림", os.path.join(ROOT, 'src/art', q['id'] + '.webp'))
    if a.all:
        for x in json.load(open(os.path.join(ROOT, 'src/japan/index.json'), encoding='utf-8')):
            if x['stars'] >= 4: gen(c, f"수학 문제 '{x['text'][:60]}' 를 상징하는 그림", os.path.join(ROOT, 'src/art', x['id'] + '.webp'))
if __name__ == '__main__': main()
