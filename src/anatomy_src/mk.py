"""압축 형식 → anatomy/<id>.json (8단계 분석 오버레이)
I(id, wrong, intro=[..], C={'C1':(label, why), ...}, K=[(h,[p..])], S=[(title,[conds])..] (기존 풀이 단계 순서대로) 또는 S=[(title,text,[conds])],
  T=[(h,cond,[p..])], V=[(h,[body..],answer,hint)], L=line)"""
import json,os,re
ROOT='/home/claude/killer_shrekmath'
L={x['id']:x['num'] for x in json.load(open(ROOT+'/site/list.json'))}
def I(qid,wrong,intro,C,K,S,T,V,line):
    d=json.load(open(f"{ROOT}/site/data/{L[qid]:03d}.json"))
    cids=[c['id'] for c in d['conds']]
    st=[]
    if all(len(s)==2 for s in S):
        assert len(S)==len(d['steps']),(qid,len(S),len(d['steps']))
        for s,(t,u) in zip(d['steps'],S): st.append({'title':t,'text':re.sub(r'문항 ?\d+[과와] 같(은 방법으로|이) ?','',s['text']),'uses':u})
    else:
        for s in S:
            if len(s)==2: raise SystemExit('mixed')
            st.append({'title':s[0],'text':s[1],'uses':s[2]})
    uses={}
    for i,s in enumerate(st):
        for c in s['uses']:
            assert c in cids,(qid,c); uses.setdefault(c,[]).append(i+1)
    conds={}
    for c,(lab,why) in C.items():
        assert c in cids,(qid,c); conds[c]={'label':lab,'why':why,'uses':uses.get(c,[])}
    for t in T: assert t[1] in cids,(qid,t[1])
    o={'wrong':wrong,'intro':intro,'conds':conds,
       'concepts':[{'h':h,'p':p} for h,p in K],'steps':st,
       'traps':[{'h':h,'cond':c,'text':p} for h,c,p in T],
       'variants':[{'h':v[0],'body':v[1],'answer':v[2],'hint':v[3]} for v in V],'line':line}
    for k in ('rate','source'):
        pass
    json.dump(o,open(f"{ROOT}/anatomy/{qid}.json",'w'),ensure_ascii=False,indent=1)
    return qid
