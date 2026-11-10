#!/usr/bin/env python3
"""Aggregate shape.jsonl (from Lean) into classes, with proof-size shares from decls.jsonl."""
import json, sys, collections
R = sys.argv[1]
decl = {}
for l in open(R + '/out/corpus/ns/decls.jsonl'):
    d = json.loads(l); decl[d['name']] = d
tot = sum(d['proofSize'] for d in decl.values() if d['kind'] == 'theorem')
fam = {f['name'] for f in json.load(open(R + '/out/corpus/lesssim/family.json'))}
depth = json.load(open(R + '/out/corpus/lesssim/producers.json'))['depth']
OK = {'O', 'O1', 'Oprod'}
def cls(s):
    a = s['atoms']
    if s['realEx'] == 0: return 'no real ∃ found by the walker'
    if not a: return 'constant not used in any atom reached'
    if s['otherEx'] > 0: return 'also binds a non-numeric ∃ (function, set, structure)'
    if s['realEx'] > 1:
        return 'several real constants, each an upper-bound factor' if all(x in OK for x in a) else 'several real constants, other uses'
    if s['hypMentions'] > 0: return 'constant also appears in a hypothesis inside the conclusion'
    if all(x in OK for x in a):
        k = 'one bound' if len(a) == 1 else 'conjunction of bounds'
        return f'FITS: {k}' + (', with ∃ exponent' if s['natEx'] else '')
    if any(x in ('lower', 'both-sides') for x in a): return 'constant on the left of an inequality (lower bound or both sides)'
    if any(x == 'upper-other' for x in a): return 'upper bound, constant not a plain factor (sum, power, exponent, max)'
    if any(x == 'nonreal' for x in a): return 'inequality not in ℝ'
    return 'constant passed to a predicate or equation'
rows = [json.loads(l) for l in open(R + '/out/corpus/lesssim/shape.jsonl')]
C = collections.defaultdict(lambda: [0, 0, 0, 0])
out = []
for s in rows:
    c = cls(s); d = decl[s['name']]
    C[c][0] += 1; C[c][1] += d['proofSize']; C[c][2] += s['name'] in fam; C[c][3] += depth[s['name']] > 1
    out.append({'name': s['name'], 'class': c, 'proofSize': d['proofSize'], 'depth': depth[s['name']], **{k: s[k] for k in ('realEx', 'natEx', 'otherEx', 'atoms', 'hypMentions')}})
json.dump(out, open(R + '/out/corpus/lesssim/shape_classes.json', 'w'), indent=0)
n = len(rows); pm = sum(d['proofSize'] for d in map(lambda s: decl[s['name']], rows))
print('| class | theorems | % of the 946 | proof size | % of ∃C proof size | of which in the family | of which use another ∃C lemma |')
print('|---|---|---|---|---|---|---|')
for c, v in sorted(C.items(), key=lambda kv: (not kv[0].startswith('FITS'), -kv[1][0])):
    print(f'| {c} | {v[0]} | {100*v[0]/n:.1f} | {v[1]} | {100*v[1]/pm:.1f} | {v[2]} | {v[3]} |')
fits = [v for c, v in C.items() if c.startswith('FITS')]
print('FITS total', sum(v[0] for v in fits), f'{100*sum(v[0] for v in fits)/n:.1f}%', 'proof', sum(v[1] for v in fits), f'{100*sum(v[1] for v in fits)/pm:.1f}% of ∃C proof size', f'{100*sum(v[1] for v in fits)/tot:.2f}% of all theorem proof size', 'all ∃C share', f'{100*pm/tot:.2f}%')
print('family classes', [(o['name'].split('.')[-1], o['class']) for o in out if o['name'] in fam])
