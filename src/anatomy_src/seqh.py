"""역추적형 수열 문항(22번형) 공통 도우미 — 변형 답은 앞으로 직접 계산해 확정."""
import json
from mk import I,L,ROOT
BK=("역추적",[r"$a_{n+1}$의 값에서 각 경우의 식을 거꾸로 풀어 $a_n$ 후보를 구함."])
CK=("조건 확인",[r"구한 후보가 그 경우의 조건을 실제로 만족하는지 매 단계 확인 — 범위는 맨 끝에."])
def run(f,starts,k,target):
    out=[]
    for a in starts:
        x=a;h=[a]
        for n in range(1,k):
            x=f(h,n) if getattr(f,'hist',False) else f(x,n); h.append(x)
        if x==target: out.append(a)
    return out
AGG={'sum':lambda r:sum(r),'pq_max':lambda r:len(r)+max(r),'pq_sum':lambda r:len(r)+sum(r),
     'maxmin':lambda r:max(r)-min(r),'count':lambda r:len(r),'max':lambda r:max(r),'min':lambda r:min(r),
     'maxplusmin':lambda r:max(r)+min(r)}
def SQ(qid,wrong,intro,C,R,A,Q,T,vh,vbody,f,starts,k,target,agg,line,orig=None,K=None):
    d=json.load(open(f"{ROOT}/site/data/{L[qid]:03d}.json")); n=len(d['steps'])
    if orig:  # 원 문항도 앞으로 계산해 정답 확인
        of,ok,ot=orig; assert AGG[agg[0]](run(of,starts,ok,ot))==int(d['answer']),(qid,'orig')
    S=[("원리",R),("시작",[Q])]+[("역추적",R)]*(n-4)+[("검산",[A]),("답",[Q])]
    r=run(f,starts,k,target); ans=AGG[agg[-1]](r)
    lst=', '.join(map(str,r))
    I(qid,wrong,intro,C,K or [BK,CK],S,T,[(vh,[vbody],ans,f"$a_1$: ${lst}$.")],line)
