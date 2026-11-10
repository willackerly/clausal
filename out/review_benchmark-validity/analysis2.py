import json, math, pickle
import numpy as np
from collections import Counter
rows=pickle.load(open('out/review_benchmark-validity/rows.pkl','rb'))
def rank(score,mask,tgt):
    s=score[mask]; best=math.inf
    for v in set(score[tgt&mask].tolist()):
        best=min(best,1+(s>v).sum()+((s==v).sum()-1)/2)
    return best,int(mask.sum())
def summ(rs,ns=None):
    rs=np.array(rs,dtype=float)
    return dict(n=len(rs),top1=round(100*(rs<=1).mean(),1),top3=round(100*(rs<=3).mean(),1),top5=round(100*(rs<=5).mean(),1),mrr=round(float((1/rs).mean()),3))
hr=lambda r:r['P']/r['S']
# 1 pool composition
fu=[(r['U']&r['m']&~r['T']).sum()/r['m'].sum() for r in rows]
fa=[(r['A']&r['m']).sum() for r in rows]
fe=[(~r['U']&~r['A']&~r['T']&r['m']).sum()/r['m'].sum() for r in rows]
print('share of noRoot pool INSIDE target: median %.2f mean %.2f; elsewhere median %.2f; #enclosing non-root median %d'%(np.median(fu),np.mean(fu),np.median(fe),np.median(fa)))
# structural floor: normalized rank if target beat all descendants and lost to everything else
nrfloor=[1-(r['U']&r['m']&~r['T']).sum()/max(r['m'].sum()-1,1) - 0 for r in rows]
# best-case/worst-case under proofSize given nesting: target must beat descendants, lose to ancestors
lo=[(r['A']&r['m']).sum()/max(r['m'].sum()-1,1) for r in rows]
hi=[1-(r['U']&r['m']&~r['T']).sum()/max(r['m'].sum()-1,1) for r in rows]
print('proofSize norm-rank forced interval by nesting alone: median lower %.3f, median upper %.3f'%(np.median(lo),np.median(hi)))
# 2 ties at top
ties=0;strict=0
for r in rows:
    s=np.where(r['m'],hr(r),-np.inf); mx=s.max()
    if (s[r['T']]==mx).any():
        if (s==mx).sum()>1: ties+=1
        else: strict+=1
print('hr top is GT strict',strict,'tied',ties)
# 3 statement-level matching: winner has same stmt hash as GT?
same=0; near=0; cnt=Counter()
rk_stmt=[]
for r in rows:
    s=np.where(r['m'],hr(r),-np.inf); j=int(np.argmax(s))
    th=set(r['H'][r['T']].tolist())
    if not r['T'][j] and r['H'][j] in th: same+=1; cnt['above' if r['A'][j] else 'under' if r['U'][j] else 'else']+=1
    # rank among distinct statements (best score per hash)
    best={}
    for k in np.where(r['m'])[0]:
        h=r['H'][k]; best[h]=max(best.get(h,-np.inf),s[k])
    tv=max(best[h] for h in th if h in best)
    vals=np.array(list(best.values()))
    rk_stmt.append(1+(vals>tv).sum()+((vals==tv).sum()-1)/2)
print('hr winner is non-GT but has GT statement hash:',same,cnt)
print('rank by distinct statement (hash-level match):',summ(rk_stmt))
# lenient: count winner as hit if it is GT or encloses/inside GT with proof size within 10% and S within 10%
for tol in (0.05,0.1,0.25):
    hit=0
    for r in rows:
        s=np.where(r['m'],hr(r),-np.inf); j=int(np.argmax(s))
        i=int(np.argmax(np.where(r['T'],s,-np.inf)))
        if r['T'][j] or ((r['A'][j] or r['U'][j]) and abs(r['P'][j]-r['P'][i])<=tol*r['P'][i]): hit+=1
    print('tolerance',tol,'top-1 (GT or nested near-copy with proof size within tol):',round(100*hit/len(rows),1))
    hit=0
    for r in rows:
        s=np.where(r['m'],r['P'],-np.inf); j=int(np.argmax(s))
        i=int(np.argmax(np.where(r['T'],r['P'],-np.inf)))
        if r['T'][j] or ((r['A'][j] or r['U'][j]) and abs(r['P'][j]-r['P'][i])<=tol*r['P'][i]): hit+=1
    print('   same for proofSize:',round(100*hit/len(rows),1))
# growth of enclosing winner
g=[]
for r in rows:
    s=np.where(r['m'],hr(r),-np.inf); j=int(np.argmax(s))
    if r['A'][j] and not r['T'][j]:
        i=int(np.argmax(np.where(r['T'],s,-np.inf))); g.append(r['P'][j]/r['P'][i])
g=np.array(g); print('enclosing winner growth quantiles',np.percentile(g,[10,25,50,75,90]).round(2),'<=1.1:',(g<=1.1).sum(),'<=1.25',(g<=1.25).sum(),'of',len(g))
# 4 multi-site
for nm,f in [('sites==1',lambda r:r['d']['sites']==1),('sites>1',lambda r:r['d']['sites']>1),('multi target groups',lambda r:r['T'].sum()>1),('useCount1',lambda r:r['d']['helperUseCount']==1),('useCount2',lambda r:r['d']['helperUseCount']==2)]:
    sub=[r for r in rows if f(r)]
    print(nm,summ([rank(hr(r),r['m'],r['T'])[0] for r in sub]),'proofSize',summ([rank(r['P'],r['m'],r['T'])[0] for r in sub]))
# 5 selection: helper vs theorem size
d=[r['d'] for r in rows]
hp=np.array([x['helperProofDag'] for x in d]);tp=np.array([x['thmProofDag'] for x in d]);fl=np.array([x['flatDag'] for x in d])
print('helper proof >= theorem own proof in',(hp>=tp).sum(),'of',len(d),'; median helper/thm',np.median(hp/tp).round(2), 'median thm',np.median(tp),'median helper',np.median(hp))
frac=np.array([ (r['P'][r['T']].max())/r['d']['flatDag'] for r in rows])
h=np.array([rank(hr(r),r['m'],r['T'])[0] for r in rows]);p=np.array([rank(r['P'],r['m'],r['T'])[0] for r in rows])
qs=np.quantile(hp/tp,[0,.25,.5,.75,1])
for a,b in zip(qs[:-1],qs[1:]):
    m=(hp/tp>=a)&(hp/tp<=b)
    print('helper/thm size in [%.2f,%.2f]: n=%d hr top5 %.1f mrr %.3f | proofSize top5 %.1f mrr %.3f | median frac %.2f'%(a,b,m.sum(),100*(h[m]<=5).mean(),(1/h[m]).mean(),100*(p[m]<=5).mean(),(1/p[m]).mean(),np.median(frac[m])))
# 6 counterfactual: score GT with L's own declared sizes
ts=np.array([r['S'][int(np.argmax(np.where(r['T'],hr(r),-np.inf)))] for r in rows]); hs=np.array([x['helperStmtDag'] for x in d])
tpz=np.array([r['P'][int(np.argmax(np.where(r['T'],hr(r),-np.inf)))] for r in rows])
print('target instantiated S vs declared helper S: median ratio %.2f; inst>decl in %d; inst>1.5x in %d; inst<decl/1.5 in %d'%(np.median(ts/hs),(ts>hs).sum(),(ts>1.5*hs).sum(),(ts<hs/1.5).sum()))
print('target P (fvar-dag) vs helperProofDag median ratio %.2f'%np.median(tpz/hp))
cf=[];cf2=[]
for r in rows:
    x=r['d']; s=hr(r).copy(); t=r['T']
    v=x['helperProofDag']/x['helperStmtDag']
    sm=s[r['m']&~t]
    cf.append(1+(sm>v).sum()+(sm==v).sum()/2)
    # only replace S
    v2=(r['P'][t]/x['helperStmtDag']).max()
    cf2.append(1+(sm>v2).sum()+(sm==v2).sum()/2)
print('counterfactual: GT scored with L declared proof/stmt size:',summ(cf)); print('counterfactual: GT scored with instantiated P, declared S:',summ(cf2))
# 7 local-max on chain
loc=0;chainrank=[]
for r in rows:
    s=hr(r); ch=(r['A']|r['T'])&r['m']
    chainrank.append(rank(s,ch,r['T']))
cr=np.array([c[0] for c in chainrank]);cn=np.array([c[1] for c in chainrank])
print('rank of GT among chain (enclosing non-root + GT): top1 %.1f%%, median chain len %d; random-on-chain expectation %.1f%%'%(100*(cr<=1).mean(),np.median(cn),100*np.mean(1/cn)))
crp=np.array([rank(r['P'],(r['A']|r['T'])&r['m'],r['T'])[0] for r in rows]); print('proofSize on chain top1 (must be 0 unless chain len 1):',100*(crp<=1).mean(), 'chain len 1:',(cn==1).sum())
# 8 depth baseline restricted etc: role of target
print(Counter(r['role'][int(np.argmax(np.where(r['T'],hr(r),-np.inf)))] for r in rows))
print('target minDepth median',np.median([r['dep'][r['T']].min() for r in rows]))
# pool sizes tiny
ns=np.array([r['m'].sum() for r in rows]); print('pool<=5:',(ns<=5).sum(),'pool<=10',(ns<=10).sum(),'pool<=20',(ns<=20).sum())
print('top5 hr excluding pools<=20:',summ(h[ns>20]),'proofSize',summ(p[ns>20]))
