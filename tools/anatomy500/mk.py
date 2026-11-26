"""spec(json list) → anatomy/<id>.json. 검사: 조건 id, 단계 번호 1..n 순서대로 빠짐없이, 수식 KaTeX"""
import json,sys,subprocess,os,re,glob
R='/home/claude/ks/'
sys.path.insert(0,R); os.chdir(R)
import build as B
BANK={}
for f in glob.glob(R+'src/bank/x_최고난도_500제_*.json'):
    for q in json.load(open(f,encoding='utf-8')): BANK[q['id']]=q
def raw_steps(qid):
    out={}
    for i,b in enumerate(BANK[qid]['solution']):
        cb=B.conv_block(b)
        out[i+1]=' '.join(cb['sents']) if cb['t']=='p' else ('$$'+cb['tex']+'$$' if cb['t']=='eq' else ' / '.join(cb['items']))
    return out
spec=json.load(open(os.path.join('/home/claude/tools',sys.argv[1]),encoding='utf-8'))
out=[]; errs=[]
for it in spec:
    n=it['n']; d=json.load(open(f'{R}site/data/{n}.json',encoding='utf-8'))
    cids=[c['id'] for c in d['conds']]; S=raw_steps(d['id'])
    A={}
    if it.get('wrong'):A['wrong']=it['wrong']
    A['intro']=it['intro']
    conds={}
    for k,v in it['conds'].items():
        if k not in cids: errs.append(f'#{n} 조건 {k} 없음 ({cids})')
        conds[k]={'label':v[0],'why':v[1],'uses':v[2] if len(v)>2 else []}
    miss=[c for c in cids if c not in conds]
    if miss: errs.append(f'#{n} 조건 빠짐 {miss}')
    A['conds']=conds
    A['concepts']=[{'h':h,'p':p if isinstance(p,list) else [p]} for h,p in it['concepts']]
    steps=[];seen=[]
    for t,ns,u in it['steps']:
        if isinstance(ns,int): ns=[ns]
        seen+=ns
        for x in u:
            if x not in cids: errs.append(f'#{n} 단계 uses {x} 없음')
        steps.append({'title':t,'text':' '.join(S[k] for k in ns),'uses':u})
    if seen!=list(range(1,len(S)+1)): errs.append(f'#{n} 단계 번호 {seen} ≠ 1..{len(S)}')
    nst=len(steps)
    for k,v in conds.items():
        for x in v['uses']:
            if not (1<=x<=nst): errs.append(f'#{n} {k} uses {x} 범위밖(1..{nst})')
    A['steps']=steps
    A['traps']=[{'h':h,'cond':c,'text':t if isinstance(t,list) else [t]} for h,c,t in it['traps']]
    for tr in A['traps']:
        if tr['cond'] not in cids: errs.append(f"#{n} 함정 cond {tr['cond']} 없음")
    A['variants']=[{'h':v[0],'body':[v[1]],'answer':v[2],'hint':v[3]} for v in it['variants']]
    A['line']=it['line']
    out.append((d['id'],A))
# KaTeX
blob=json.dumps([a for _,a in out],ensure_ascii=False)
open('/tmp/_k.json','w',encoding='utf-8').write(blob)
r=subprocess.run(['node','/home/claude/tools/kcheck.js'],capture_output=True,text=True); 
if r.stdout.strip(): errs+=r.stdout.strip().split('\n')
if errs: print('\n'.join(errs)); sys.exit(1)
for i,A in out: json.dump(A,open(f'{R}anatomy/{i}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('OK',len(out),'개 작성:',', '.join(i for i,_ in out))
