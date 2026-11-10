#!/usr/bin/env python3
"""Markdown tables for LESSSIM.md from measure.jsonl, measure_sample.jsonl, source_measure.json, family.json."""
import json, sys, collections
R = sys.argv[1]; O = R + '/out/corpus/lesssim/'
M = [json.loads(l) for l in open(O + 'measure.jsonl')]
MS = [json.loads(l) for l in open(O + 'measure_sample.jsonl')]
SRC = json.load(open(O + 'source_measure.json'))
fam = sorted(json.load(open(O + 'family.json')), key=lambda f: f['depth'])
by = collections.defaultdict(dict)
for r in M: by[r['group']][r['name']] = r
short = lambda n: n.split('.', 2)[2]
src = {r['name']: r for r in SRC['family']}
OUTCOME = {7: 'escape hatch (statement kept)', 8: 'escape hatch (inside the proof)'}
var = {r['name'].split('Lesssim.Variant.')[1]: r for r in MS if r['group'] == 'variant'}
val = lambda r: r['valueDag'] + r['auxDag']
print('### Family: statements\n')
print('| # | theorem | statement nodes: original → native | conclusion nodes | ∀ and ∃ binders in the conclusion | hypotheses | statement source lines |')
print('|---|---|---|---|---|---|---|')
T = collections.Counter()
for f in fam:
    o = by['orig'][f['name']]; n = by['native']['Lesssim.Native.' + short(f['name'])]; s = src[f['name']]
    v = var.get(short(f['name']))
    sn = f"{o['statementTree']} → {n['statementTree']}" + (f" ({v['statementTree']} with projections)" if v else '')
    print(f"| {f['depth']} | `{short(f['name'])}` | {sn} | {o['conclTree']} → {n['conclTree']} | {o['conclForall']}+{o['conclExists']} → {n['conclForall']}+{n['conclExists']} | {o['hyps']} → {n['hyps']} | {s['orig']['stmtLines']} → {s['native']['stmtLines']} |")
    for k in ('statementTree', 'conclTree', 'hyps', 'conclForall', 'conclExists', 'statementDag'):
        T['o' + k] += o[k]; T['n' + k] += n[k]
    T['nv'] += (v or n)['statementTree']
    T['osl'] += s['orig']['stmtLines']; T['nsl'] += s['native']['stmtLines']
    T['ost'] += s['orig']['stmtTokens']; T['nst'] += s['native']['stmtTokens']
print(f"| | **total** | {T['ostatementTree']} → {T['nstatementTree']} ({T['nv']} with projections) | {T['oconclTree']} → {T['nconclTree']} | {T['oconclForall']}+{T['oconclExists']} → {T['nconclForall']}+{T['nconclExists']} | {T['ohyps']} → {T['nhyps']} | {T['osl']} → {T['nsl']} |")
print(f"\nStatement source tokens: {T['ost']} → {T['nst']}.  Distinct subterms of the statements: {T['ostatementDag']} → {T['nstatementDag']}.\n")
print('### Family: proofs\n')
print('| # | theorem | proof nodes: original → native | change | proof source lines | proof source tokens | outcome | laws used (Mathlib `Asymptotics.*`; library) |')
print('|---|---|---|---|---|---|---|---|')
P = collections.Counter()
for f in fam:
    o = by['orig'][f['name']]; n = by['native']['Lesssim.Native.' + short(f['name'])]; s = src[f['name']]
    laws = sorted(c.replace('Asymptotics.', '') for c in n['asymptoticsConsts'] if c not in ('Asymptotics.IsBigO', 'Asymptotics.IsBigOWith'))
    libs = sorted(c.replace('Lesssim.', '') for c in n['libConsts'])
    d = val(n) - val(o)
    print(f"| {f['depth']} | `{short(f['name'])}` | {val(o)} → {val(n)} | {d:+d} ({100*d/val(o):+.0f}%) | {s['orig']['proofLines']} → {s['native']['proofLines']} | {s['orig']['proofTokens']} → {s['native']['proofTokens']} | {OUTCOME.get(f['depth'], 'native')} | {', '.join(laws) or '–'}; {', '.join(libs) or '–'} |")
    P['o'] += val(o); P['n'] += val(n); P['ol'] += s['orig']['proofLines']; P['nl'] += s['native']['proofLines']
    P['ot'] += s['orig']['proofTokens']; P['nt'] += s['native']['proofTokens']
    P['oc'] += s['orig']['proofChars']; P['nc'] += s['native']['proofChars']
    P['ob'] += o['bodyDag']; P['nb'] += n['bodyDag']
print(f"| | **total** | {P['o']} → {P['n']} | {P['n']-P['o']:+d} ({100*(P['n']-P['o'])/P['o']:+.1f}%) | {P['ol']} → {P['nl']} | {P['ot']} → {P['nt']} | | |")
print(f"\nProof source characters (leading whitespace stripped): {P['oc']} → {P['nc']}.  Proof nodes without the leading binders (body only): {P['ob']} → {P['nb']}.\n")
print('### Library\n')
use = collections.Counter()
for f in fam:
    for c in by['native']['Lesssim.Native.' + short(f['name'])]['libConsts']: use[c] += 1
print('| lemma | statement nodes | proof nodes | source lines (statement + proof) | family theorems using it |')
print('|---|---|---|---|---|')
L = collections.Counter()
for name, r in by['lib'].items():
    s = SRC['lib'][name.split('Lesssim.')[1]]
    print(f"| `{name.split('Lesssim.')[1]}` | {r['statementTree']} | {val(r)} | {s['stmtLines']} + {s['proofLines']} | {use[name]} |")
    L['st'] += r['statementTree']; L['v'] += val(r); L['sl'] += s['stmtLines']; L['pl'] += s['proofLines']; L['tok'] += s['stmtTokens'] + s['proofTokens']
print(f"| **total (15)** | {L['st']} | {L['v']} | {L['sl']} + {L['pl']} | |")
print(f"\nLibrary source tokens: {L['tok']}.\n")
E = collections.Counter()
for g in ('back', 'fwd', 'shape'):
    for r in by[g].values(): E[g] += val(r); E[g + 'n'] += 1
print(f"Equivalence proofs (not part of the library a native corpus would keep): {E['backn']} `Back` theorems {E['back']} proof nodes, {E['fwdn']} `Fwd` theorems {E['fwd']}, {E['shapen']} shape lemmas {E['shape']}; source lines {sum(v['stmtLines']+v['proofLines'] for v in SRC['equiv'].values())}.\n")
chk = by['check']
print(f"Checks from Lean: `Back.X` type structurally equal to the original for {sum(r['backSameStatement'] for r in chk.values())} of {len(chk)}; `Fwd.X` type equal to `Native.X` for {sum(bool(r['fwdSameStatement']) for r in chk.values())} of {sum(r['fwdSameStatement'] is not None for r in chk.values())}; native proofs using an original family theorem: {sum(r['nativeUsesOriginalFamily'] for r in chk.values())}; `Back` proofs using one: {sum(r['backUsesOriginalFamily'] for r in chk.values())}.")
ax = set()
for r in M + MS: ax |= set(r.get('axioms', []))
print(f"Axioms over all new declarations: {', '.join(sorted(ax))}.\n")
print('### Sample: measured rows\n')
print('| theorem | statement nodes: original → native | proof nodes: original → native | proof source lines | proof source tokens |')
print('|---|---|---|---|---|')
so = {r['name']: r for r in MS if r['group'] == 'orig'}
sn = {r['name'].split('.')[-1]: r for r in MS if r['group'] in ('native', 'native-universe0')}
ss = {r['name']: r for r in SRC['sample']}
for name, o in so.items():
    k = name.split('.')[-1]
    if k not in sn: continue
    n = sn[k]; s = ss[name]
    print(f"| `{k}`{' (universe 0 only)' if n['group'] != 'native' else ''} | {o['statementTree']} → {n['statementTree']} | {val(o)} → {val(n)} ({100*(val(n)-val(o))/val(o):+.0f}%) | {s['orig']['proofLines']} → {s['native']['proofLines']} | {s['orig']['proofTokens']} → {s['native']['proofTokens']} |")
