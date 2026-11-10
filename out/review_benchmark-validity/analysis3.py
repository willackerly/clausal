import json, math, pickle, sys
import numpy as np
sys.path.insert(0,'bench')
from score import random_expectation
rows=pickle.load(open('out/review_benchmark-validity/rows.pkl','rb'))
def rank(score,mask,tgt):
    s=score[mask]; best=math.inf
    for v in set(score[tgt&mask].tolist()):
        best=min(best,1+(s>v).sum()+((s==v).sum()-1)/2)
    return best
rng=np.random.default_rng(7)
def ci(v,B=4000):
    v=np.asarray(v,float); idx=rng.integers(0,len(v),size=(B,len(v))); m=v[idx].mean(axis=1); return v.mean(),np.percentile(m,2.5),np.percentile(m,97.5)
h=np.array([rank(r['P']/r['S'],r['m'],r['T']) for r in rows]);p=np.array([rank(r['P'],r['m'],r['T']) for r in rows]);dp=np.array([rank(-r['dep'],r['m'],r['T']) for r in rows])
rnd=np.array([random_expectation(int(r['m'].sum()),int((r['T']&r['m']).sum())) for r in rows])
d=[r['d'] for r in rows]
hp=np.array([x['helperProofDag'] for x in d]);tp=np.array([x['thmProofDag'] for x in d])
print('hr - shallowest: MRR diff %.3f [%.3f,%.3f]'%ci(1/h-1/dp),' top5 diff %.3f [%.3f,%.3f]'%ci((h<=5)*1.0-(dp<=5)),' top1 diff %.3f [%.3f,%.3f]'%ci((h<=1)*1.0-(dp<=1)))
print('proofSize - shallowest: MRR diff %.3f [%.3f,%.3f]'%ci(1/p-1/dp))
ratio=hp/tp
for nm,m in [('helper<0.5x thm',ratio<0.5),('0.5-1x',(ratio>=.5)&(ratio<1)),('1-3x',(ratio>=1)&(ratio<3)),('>=3x',ratio>=3),('thm own proof<150',tp<150),('thm own proof<300',tp<300)]:
    print('%-18s n=%3d | hr top1 %.1f top5 %.1f mrr %.3f | size top5 %.1f mrr %.3f | depth top5 %.1f mrr %.3f | random top1 %.1f top5 %.1f mrr %.3f'%(nm,m.sum(),100*(h[m]<=1).mean(),100*(h[m]<=5).mean(),(1/h[m]).mean(),100*(p[m]<=5).mean(),(1/p[m]).mean(),100*(dp[m]<=5).mean(),(1/dp[m]).mean(),100*rnd[m,0].mean(),100*rnd[m,2].mean(),rnd[m,3].mean()))
m=ratio<0.5
print('helper<0.5x thm: hr MRR - random MRR: %.3f [%.3f,%.3f]'%ci(1/h[m]-rnd[m,3]),'top5: %.3f [%.3f,%.3f]'%ci((h[m]<=5)*1.0-rnd[m,2]))
m=ratio<1
print('helper<1x thm (n=%d): hr MRR - random MRR: %.3f [%.3f,%.3f]'%((m.sum(),)+ci(1/h[m]-rnd[m,3])),'top5: %.3f [%.3f,%.3f]'%ci((h[m]<=5)*1.0-rnd[m,2]), 'hr-size mrr %.3f [%.3f,%.3f]'%ci(1/h[m]-1/p[m]))
# chain analysis
cr=[];cn=[]
for r in rows:
    ch=(r['A']|r['T'])&r['m']; cr.append(rank(r['P']/r['S'],ch,r['T'])); cn.append(ch.sum())
cr=np.array(cr);cn=np.array(cn)
mm=cn>1
print('chain (len>1, n=%d): hr picks GT on chain %.3f [%.3f,%.3f]'%((mm.sum(),)+ci((cr[mm]<=1)*1.0)),'random-on-chain %.3f'%np.mean(1/cn[mm]),'diff %.3f [%.3f,%.3f]'%ci((cr[mm]<=1)*1.0-1/cn[mm]))
# normalised position on chain
print('median normalised chain rank of GT under hr (0 best):',np.median((cr[mm]-1)/(cn[mm]-1)))
# corpus thresholds
print('helper proof quantiles',np.percentile(hp,[0,10,25,50,75,90]),'thm own proof quantiles',np.percentile(tp,[0,10,25,50,75,90]))
frac=np.array([ (r['P'][r['T']].max())/r['d']['flatDag'] for r in rows])
print('GT fraction of flat proof quantiles',np.percentile(frac,[10,25,50,75,90]).round(2))
