import pickle, json, random, re, math, collections
P=pickle.load(open('ns/features.pkl','rb')); F=P['feats']
D=[f for f in F.values() if f['reach'] is True and f['kind'] in ('def','structure','abbrev') and not (f['kind']=='abbrev' and f['rtag']=='U')]
D.sort(key=lambda f:f['name'])
mem=collections.defaultdict(set)
for l in open('ns/clusters.jsonl'):
    r=json.loads(l)
    for m in r['members']: mem[m].add(r['id'])
def toks(f):
    short=f['name'].split('.')[-1]
    t=re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+', short)
    t=['n:'+x.lower() for x in t]
    pp=re.findall(r'[A-Za-z][A-Za-z0-9_.]*', f['pp'])
    t+=['t:'+x.split('.')[-1] for x in pp]
    return t
docs=[collections.Counter(toks(f)) for f in D]
df=collections.Counter(w for d in docs for w in d)
N=len(D)
def vec(d):
    v={w:(1+math.log(c))*math.log(N/df[w]) for w,c in d.items()}
    n=math.sqrt(sum(x*x for x in v.values())) or 1
    return {w:x/n for w,x in v.items()}
V=[vec(d) for d in docs]
inv=collections.defaultdict(list)
for i,v in enumerate(V):
    for w,x in v.items(): inv[w].append((i,x))
rng=random.Random(31337)
pick=rng.sample(range(N),30)
print('universe',N)
for i in pick:
    f=D[i]
    sc=collections.Counter()
    for w,x in V[i].items():
        if df[w]>800: continue
        for j,y in inv[w]: sc[j]+=x*y
    sc.pop(i,None)
    print('=====',f['name'],'[',f['kind'],']','clusters:',sorted(mem.get(f['name'],[]))[:6])
    print('   pp:',str(f['pp'])[:160].replace('\n',' '))
    print('   body:',str(f['ppBody'])[:220].replace('\n',' '))
    for j,s in sc.most_common(5):
        g=D[j]; shared=mem.get(f['name'],set())&mem.get(g['name'],set())
        print(f'   {s:.2f} {"SAME" if shared else "-"} {g["name"]} :: {str(g["ppBody"])[:160]}'.replace('\n',' '))
