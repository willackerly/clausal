import json, math, sys
import numpy as np
from collections import Counter
res=[json.loads(l) for l in open('out/bench/results.jsonl')]
raw=[json.loads(l) for l in open('out/bench/raw.jsonl')]
corpus=json.load(open('bench/corpus.json'))
print('results',len(res),'raw',len(raw),'corpus',len(corpus),'uniq idx',len({r['idx'] for r in res}), 'ok',sum(r['ok'] for r in res))
print('name match', all(corpus[r['idx']]['theorem']==r['theorem'] and corpus[r['idx']]['helper']==r['helper'] for r in raw))
# headline from results.jsonl
def metrics(rule,pool='noRoot',sub=None):
    rs=[];ns=[]
    for r in res:
        if sub is not None and not sub(r): continue
        x=r['rank'][pool][rule]; x=math.inf if x is None else x
        rs.append(x); ns.append(r['poolSize'][pool])
    rs=np.array(rs);ns=np.array(ns)
    nr=np.where(np.isinf(rs),1.0,(rs-1)/np.maximum(ns-1,1))
    return len(rs),100*(rs<=1).mean(),100*(rs<=3).mean(),100*(rs<=5).mean(),(1/rs).mean(),np.median(nr)
for rule in ['hidingRatio','hidingRatioTree','proofSize','invStatementSize','fewestDeps','logP-lam*logS','logP-lam*S','mdlSaving']:
    print(rule, ['%.3f'%v for v in metrics(rule)])
# independent recompute from raw
F={n:i for i,n in enumerate(raw[0]['groupFields'])}
def arr(d,name,t=float): return np.array([g[F[name]] for g in d['groups']],dtype=t)
def rank(score,mask,tgt):
    s=score[mask]; best=math.inf
    for v in set(score[tgt&mask].tolist()):
        best=min(best,1+(s>v).sum()+((s==v).sum()-1)/2)
    return best,int(mask.sum())
out={}
rows=[]
for d in raw:
    P=arr(d,'proofSizeDag');S=arr(d,'statementSize');D=arr(d,'numDeps');rep=arr(d,'rep',int)
    T=arr(d,'isTarget',bool);U=arr(d,'underTarget',bool);A=arr(d,'aboveTarget',bool);dep=arr(d,'minDepth')
    H=np.array([g[F['stmtHash']] for g in d['groups']])
    role=np.array([g[F['role']] for g in d['groups']]);kind=np.array([g[F['kind']] for g in d['groups']])
    m=rep!=0
    rows.append(dict(d=d,P=P,S=S,D=D,T=T,U=U,A=A,dep=dep,H=H,m=m,role=role,kind=kind,rep=rep))
def agg(fn,sub=None,mask=None):
    rs=[];ns=[]
    for r in rows:
        if sub and not sub(r): continue
        mm=r['m'] if mask is None else mask(r)
        x,n=rank(fn(r),mm,r['T']); rs.append(x);ns.append(n)
    rs=np.array(rs,dtype=float);ns=np.array(ns)
    nr=np.where(np.isinf(rs),1.0,(rs-1)/np.maximum(ns-1,1))
    return rs,dict(n=len(rs),top1=round(100*(rs<=1).mean(),1),top3=round(100*(rs<=3).mean(),1),top5=round(100*(rs<=5).mean(),1),mrr=round(float((1/rs).mean()),3),medNR=round(float(np.median(nr)),3))
print('--- independent recompute from raw (noRoot)')
R={}
for name,fn in [('hidingRatio',lambda r:r['P']/r['S']),('proofSize',lambda r:r['P']),('invS',lambda r:-r['S']),('deps',lambda r:-r['D']),
                ('shallowest(minDepth)',lambda r:-r['dep']),('P-S',lambda r:r['P']-r['S']),('P*ratio',lambda r:r['P']*r['P']/r['S'])]:
    R[name],a=agg(fn); print(name,a)
# bootstrap check
rng=np.random.default_rng(1)
def boot(v,B=5000):
    idx=rng.integers(0,len(v),size=(B,len(v))); m=v[idx].mean(axis=1); return np.percentile(m,[2.5,97.5])
h=R['hidingRatio'];p=R['proofSize']
print('top1 CI',boot((h<=1).astype(float))*100,'top5 CI',boot((h<=5).astype(float))*100)
print('paired MRR diff',(1/h-1/p).mean(),boot(1/h-1/p),'top5 diff',100*((h<=5).astype(float)-(p<=5)).mean(),100*boot((h<=5).astype(float)-(p<=5)))
print('paired top1 diff',100*((h<=1).astype(float)-(p<=1)).mean(),100*boot((h<=1).astype(float)-(p<=1)))
# Wilson for top1
k=(h<=1).sum();n=len(h);z=1.96;ph=k/n
lo=(ph+z*z/2/n-z*math.sqrt(ph*(1-ph)/n+z*z/4/n/n))/(1+z*z/n);hi=(ph+z*z/2/n+z*math.sqrt(ph*(1-ph)/n+z*z/4/n/n))/(1+z*z/n)
print('wilson top1',k,n,lo*100,hi*100)
# sign test on ranks
print('hr rank better',(h<p).sum(),'worse',(h>p).sum(),'equal',(h==p).sum())
import pickle; pickle.dump(rows,open('out/review_benchmark-validity/rows.pkl','wb'))
