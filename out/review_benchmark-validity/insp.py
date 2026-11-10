import json,numpy as np
from collections import Counter
D='out/review_benchmark-validity/'
I=[json.loads(l) for l in open(D+'inspect.jsonl')]
print('items',len(I),'errors',[ (x['idx'],x['error'][:100]) for x in I if 'error' in x])
I=[x for x in I if 'error' not in x]
print('independent inlining agrees up to beta:',sum(x['sameFlatUpToBeta'] for x in I),'/',len(I), [x['idx'] for x in I if not x['sameFlatUpToBeta']][:20])
print('flatDag identical w/o beta:',sum(x['flatDag']==x['flat2Dag'] for x in I))
T=[(x['idx'],t) for x in I for t in x['targets']]
print('exact targets checked',len(T),'of',sum(x['nExact'] for x in I),'total tgts',sum(x['nTargets'] for x in I))
for k in ['headIsL','tyDefEq','tySynEq','tySynEqBeta','hashEq']:
    print(k,Counter(t[k] for _,t in T))
print('kernel',Counter(t['kernel'] for _,t in T))
# per item first target
first={}
for i,t in T: first.setdefault(i,t)
F=list(first.values())
sd=np.array([t['S_declAtArgs'] for t in F]);si=np.array([t['S_inferred'] for t in F]);sr=np.array([t['S_inferredRaw'] for t in F])
print('per item (first site) n=',len(F),': inferred S != decl-at-args S in',(sd!=si).sum(),'; inferred larger',(si>sd).sum(),'smaller',(si<sd).sum(),'; median ratio among differing',np.median((si/sd)[sd!=si]).round(2), 'ratio>1.2:',(si/sd>1.2).sum(),'ratio<0.8',(si/sd<0.8).sum())
print('deps_F != deps_T',sum(t['deps_F']!=t['deps_T'] for t in F),'(body uses fewer fvars than call)', sum(t['deps_F']<t['deps_T'] for t in F))
print('dup bug: target numDeps inflated in',sum(t['deps_Fraw']>t['deps_F'] for t in F),'median inflation',np.median([t['deps_Fraw']-t['deps_F'] for t in F if t['deps_Fraw']>t['deps_F']]),'max',max(t['deps_Fraw']-t['deps_F'] for t in F),'; S inflation median',np.median(sr-si),'max',(sr-si).max())
pc=np.array([t['P_closed'] for t in F]);pi=np.array([t['P_inlined'] for t in F])
print('P in-context / P closed lemma: median',np.median(pi/pc).round(2))
rb=[x['rootBody'] for x in I if x['rootBody']]
print('root bodies',len(rb),'raw hash is thm',sum(r['rawHashIsThm'] for r in rb),'dedup hash is thm',sum(r['dedupHashIsThm'] for r in rb),'deps inflated',sum(r['depsRaw']>r['depsDedup'] for r in rb))
for i,t in T:
    if 'stmtDecl' in t:
        print('\n=== item',i,'path',t['path'],'P_site',t['P_site'],'P_inl',t['P_inlined'],'S decl/inf/raw',t['S_declAtArgs'],t['S_inferred'],t['S_inferredRaw'],'deps T/F/raw',t['deps_T'],t['deps_F'],t['deps_Fraw'],'synEq',t['tySynEq'],'kernel',t['kernel'])
        print(' DECL@ARGS:',' '.join(t['stmtDecl'].split())[:420]); 
        if not t['hashEq']: print(' INFERRED :',' '.join(t['stmtInferred'].split())[:420])
