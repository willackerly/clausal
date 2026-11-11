#!/usr/bin/env python3
"""Collect every measurement into out/families/gen/summary.json.  usage: measure.py"""
import json, os, re, collections, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.join(HERE, '..', '..'); G = os.path.join(REPO, 'out/families/gen')
FAMS = [('F00015', 'F15'), ('F00019', 'F19'), ('F00042', 'F42'), ('F00046', 'F46'), ('F00079', 'F79'), ('F00073', 'F73'), ('F02076', 'F2076')]
decl = {}
for l in open(os.path.join(REPO, 'out/corpus/ns/decls.jsonl')):
    d = json.loads(l); decl[d['name']] = d
def measures(path):
    return [json.loads(l[8:]) for l in open(path) if l.startswith('MEASURE ')] if os.path.exists(path) else []
def jl(path):
    return [json.loads(l) for l in open(path) if l.strip()] if os.path.exists(path) else []
def cut_statement(src):
    depth = 0; i = 0
    while i < len(src):
        c = src[i]
        if c in '([{⟨': depth += 1
        elif c in ')]}⟩': depth -= 1
        elif src.startswith(':=', i) and depth == 0: return src[:i]
        i += 1
    return src
def srclines(n):
    d = decl[n]
    L = open(os.path.join(REPO, 'corpora/ns', d['module'].replace('.', '/') + '.lean')).read().split('\n')[d['line'] - 1:d['endLine']]
    L = [x for x in L if x.strip() and not x.strip().startswith('/--') and not x.strip().endswith('-/') and not x.strip().startswith('--')]
    txt = '\n'.join(L)
    st = cut_statement(txt)
    return len(L), st.count('\n') + 1
def libsource(fam):
    """source lines of the new declarations in the family file (comments, blank lines, imports, the Re section and the measuring block excluded)"""
    out = 0; inre = False; incomment = False; inrun = False
    for l in open(f'{HERE}/lean/{fam}.lean'):
        s = l.strip()
        if incomment:
            if '-/' in s: incomment = False
            continue
        if s.startswith('/-') :
            if '-/' not in s: incomment = True
            continue
        if s.startswith('namespace Re') or s.startswith('namespace Fam.F2076.Re'): inre = True
        if s.startswith('end Re') or s.startswith('end Fam.F2076.Re'): inre = False; continue
        if s.startswith('run_cmd') or s.startswith('open Fam.F2076 in'): inrun = True
        if inre or inrun or not s or s.startswith('--') or s.startswith('import') or s.startswith('open ') or s.startswith('variable') \
           or s.startswith('section') or s.startswith('end') or s.startswith('namespace') or s.startswith('set_option') or s.startswith('noncomputable section') or s.startswith('#count') or s.startswith('omit'): continue
        out += 1
    return out
S = {}
# post-review inputs (checkgen.py): circular re-derivations and the elaboration cost of the new library
CIRC = json.load(open(f'{G}/circular.json')) if os.path.exists(f'{G}/circular.json') else {'circular': []}
LIBHB = json.load(open(f'{G}/libhb.json')) if os.path.exists(f'{G}/libhb.json') else {}
def pair_rows(re_rows, hb_new, hb_old):
    pairs = []; o = None
    for r in re_rows:
        if r['group'] == 'orig': o = r; continue
        n = o['name']; tot, stl = srclines(n)
        ho = hb_old.get(n) or {}; hn = hb_new.get(n) or {}
        pairs.append(dict(name=n, same=r['same'] or r.get('sameDefeq', False), sameSyntactic=r['same'], origNodes=o['valueDag'], newNodes=r['valueDag'], origInstSlots=o['instSlots'], newInstSlots=r['instSlots'],
                          origInstNodes=o['instNodes'], newInstNodes=r['instNodes'], origApps=o['apps'], newApps=r['apps'],
                          statementNodes=o['statementDag'], hyps=o['hyps'], instBinders=o['instBinders'], binders=o['binders'],
                          origLines=tot, newLines=stl + 1, origProofLines=tot - stl, newProofLines=1,
                          # a heartbeat figure counts only if that elaboration succeeded (the corpus replay can fail in a scratch file)
                          origHeartbeats=ho.get('heartbeats') if ho.get('ok') else None, newHeartbeats=hn.get('heartbeats') if hn.get('ok') else None,
                          origReplayError=None if ho.get('ok') else (ho.get('error') or 'not replayed')[:120],
                          circular=n in CIRC['circular'], axioms=r.get('axioms')))
    return pairs
def totals(pairs):
    """node, line and instance totals over the non-circular pairs; heartbeat totals over the non-circular pairs whose two elaborations both succeeded"""
    P = [p for p in pairs if not p['circular']]; H = [p for p in P if p['origHeartbeats'] is not None and p['newHeartbeats'] is not None]
    t = {k: sum(p[k] for p in P) for k in ('origNodes', 'newNodes', 'origInstSlots', 'newInstSlots', 'origApps', 'newApps', 'origLines', 'newLines', 'statementNodes', 'hyps')}
    t.update(pairs=len(P), hbPairs=len(H), origHeartbeats=sum(p['origHeartbeats'] for p in H), newHeartbeats=sum(p['newHeartbeats'] for p in H))
    return t
api = json.load(open(f'{G}/api.json'))
for fid, fam in FAMS:
    rows = measures(f'{HERE}/build/{fam}.log')
    new = [r for r in rows if r['name'].startswith('Fam.') and '.Re.' not in r['name'] and r['group'] in ('prim', 'lib', 'inst')]
    counter = [r for r in rows if r['group'] == 'counter']
    lib = dict(decls=len(new), names=[r['name'] for r in new], nodes=sum(r.get('valueDag', 0) for r in new),
               statementNodes=sum(r['statementDag'] for r in new), instSlots=sum(r.get('instSlots', 0) for r in new), sourceLines=libsource(fam),
               byGroup={g: dict(n=sum(1 for r in new if r['group'] == g), nodes=sum(r.get('valueDag', 0) for r in new if r['group'] == g)) for g in ('prim', 'lib', 'inst')},
               counterexamples=[r['name'] for r in counter], axioms=sorted({a for r in rows if r['name'].startswith('Fam.') for a in r.get('axioms', [])}))
    re_rows = measures(f'{HERE}/build/{fid}_re.log')
    hb_new = {r['name']: r for r in jl(f'{G}/{fid}_re_hb.jsonl')}; hb_old = {r['name']: r for r in jl(f'{G}/{fid}_re_spec_hb.jsonl')}
    pairs = pair_rows(re_rows, hb_new, hb_old)
    # elaboration cost of the new library: "charged" = the declarations charged in nodes (prim, lib, inst); "used" = those a re-derived proof depends on
    lh = LIBHB.get(fid, {'decls': []})
    def charged(short): return any(n == 'Fam.' + fam + '.' + short or n.endswith('.' + short) for n in lib['names'])
    lib['heartbeatsCharged'] = sum(d['heartbeats'] or 0 for d in lh['decls'] if charged(d['name']))
    lib['heartbeatsUsed'] = sum(d['heartbeats'] or 0 for d in lh['decls'] if d['usedByRederivations'])
    lib['heartbeatDecls'] = sum(1 for d in lh['decls'] if charged(d['name']))
    alt = None
    if fid == 'F00042' and os.path.exists(f'{HERE}/build/F00042_mathlib.log'):
        ap = pair_rows(measures(f'{HERE}/build/F00042_mathlib.log'), {r['name']: r for r in jl(f'{G}/F00042_mathlib_hb.jsonl')}, hb_old)
        alt = dict(pairs=ap, same=sum(1 for p in ap if p['same']), sameSyntactic=sum(1 for p in ap if p['sameSyntactic']), totals=totals(ap))
    prox = json.load(open(f'{HERE}/subst/{fid}.re.json')) if os.path.exists(f'{HERE}/subst/{fid}.re.json') else {}
    absr = json.load(open(f'{G}/{fid}_abs.json')) if os.path.exists(f'{G}/{fid}_abs.json') else []
    meta = json.load(open(f'{G}/{fid}_abs_meta.json')) if os.path.exists(f'{G}/{fid}_abs_meta.json') else {}
    sm = json.load(open(f'{G}/{fid}_sample.json')) if os.path.exists(f'{G}/{fid}_sample.json') else {}
    users = [r for r in absr if r['name'] in set(meta.get('usersAnalysed', []))]
    def cnt(rs): return dict(collections.Counter(r['result'] for r in rs))
    ab = dict(usersTotal=meta.get('theorems'), analysed=len(users), results=cnt(users), inStatement=cnt([r for r in users if r.get('inStatement')]),
              down10=cnt([r for r in absr if r['name'] in sm.get('sample', [])]), down10detail={r['name']: r['result'] for r in absr if r['name'] in sm.get('sample', [])},
              api=cnt([r for r in absr if r['name'] in sm.get('apiReplayable', [])]), private=meta.get('private'))
    # interface: body-opening theorems cited by generic ones
    opening = {r['name'] for r in users if r['result'] in ('opens', 'unfolds')}
    cited = collections.Counter(x for r in users if r['result'] == 'generic' for x in r.get('cited', []))
    ab['distinctCitedByGeneric'] = len(cited)
    trr = json.load(open(f'{G}/{fid}_tr.json')) if os.path.exists(f'{G}/{fid}_tr.json') else []
    tr = {}
    for s in ('api', 'down'):
        rs = [r for r in trr if r['set'] == s]
        tr[s] = dict(results=cnt(rs), statementBefore=sum(r['statementDag'] for r in rs if 'newStatementDag' in r), statementAfter=sum(r['newStatementDag'] for r in rs if 'newStatementDag' in r))
    rep = json.load(open(f'{G}/{fid}_replay.json')) if os.path.exists(f'{G}/{fid}_replay.json') else {}
    spec = {k: dict(ok=sum(x['ok'] for x in v), n=len(v), heartbeats=sum(x['heartbeats'] or 0 for x in v if x['ok'])) for k, v in rep.items() if k.endswith('spec')}
    S[fid] = dict(file=fam, members=api[fid]['members'], apiFull=api[fid]['full'], apiSampled=api[fid]['sampled'], lib=lib, pairs=pairs,
                  attempted=len(prox), compiled=sum(1 for p in pairs if p['same']), rederived=sum(1 for p in pairs if p['same'] and not p['circular']),
                  circular=[p['name'] for p in pairs if p['circular']], baselineFailed=[p['name'] for p in pairs if p['origHeartbeats'] is None],
                  totals=totals(pairs), mathlibOnly=alt,
                  abs=ab, transport=tr, specReplay=spec, sample=sm.get('sample'), candidatesDownstream=sm.get('candidates'))
tim = collections.defaultdict(lambda: collections.defaultdict(list))
if os.path.exists(f'{HERE}/build/timing.txt'):
    for l in open(f'{HERE}/build/timing.txt'):
        p = l.split()
        if len(p) >= 4: tim[p[0]][{'re_t': 're'}.get(p[1], p[1])].append(float(p[3]))
for fid in S: S[fid]['timing'] = {k: dict(min=min(v), runs=v) for k, v in tim.get(fid, {}).items()}
json.dump(S, open(f'{G}/summary.json', 'w'), indent=1, ensure_ascii=False)
for fid, s in S.items():
    t = s['totals']
    print(f"{fid}: lib {s['lib']['decls']} decls {s['lib']['nodes']} nodes {s['lib']['sourceLines']} lines | re {s['rederived']}/{s['attempted']} nodes {t['origNodes']}->{t['newNodes']} inst {t['origInstSlots']}->{t['newInstSlots']} lines {t['origLines']}->{t['newLines']} hb({t['hbPairs']}) {t['origHeartbeats']}->{t['newHeartbeats']} lib hb {s['lib']['heartbeatsCharged']}/{s['lib']['heartbeatsUsed']} circ {len(s['circular'])} | abs {s['abs']['results']} of {s['abs']['usersTotal']} | down10 {s['abs']['down10']} | tr {s['transport']} | timing {s['timing']}")
