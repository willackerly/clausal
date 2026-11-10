#!/usr/bin/env python3
"""Seeded sample for the soundness check -> data/sound_sample.json

Population: functions that end as compiling Lean with all four patches (p4, as shipped) and did not with the unpatched build.
Sample A: random.Random(20261110).sample(population sorted by (crate, id), 30)                (the sample the task asks for)
Sample B: the same generator, continued: a shuffle of the part of the population that the census join marks as closed
          (the function, every local function it calls, and no axiom: `ok_closure_no_axiom`), minus sample A; the first 30.
          Used only to get more executed comparisons, because few of sample A can be run. Reported separately.
"""
import json, os, random
FORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(FORK, 'data', 'summary.json')))
pop = []
for c, d in S['variants']['shipped']['p4'].items():
    base = set(S['variants']['shipped']['base'][c]['ok_ids'])
    r = json.load(open(os.path.join(FORK, 'runs', 'p4-shipped', 'results', c + '.json')))
    okids = set(d['ok_ids'])
    for f in r['functions']:
        if f['origin'] == 'source' and f['id'] in okids and f['id'] not in base:
            pop.append({'crate': c, 'id': f['id'], 'file': f['file'], 'line_start': f['line_start'], 'line_end': f['line_end'], 'name': f['name'], 'path': f['path'],
                        'loc': f['loc'], 'lean_names': f['lean_names'], 'ok_closure': f['ok_closure'], 'ok_closure_no_axiom': f['ok_closure_no_axiom'],
                        'dep_axioms': f['dep_axioms'][:8]})
pop.sort(key=lambda x: (x['crate'], x['id']))
rng = random.Random(20261110)
A = rng.sample(pop, 30)
inA = {(x['crate'], x['id']) for x in A}
rest = [x for x in pop if x['ok_closure_no_axiom'] and (x['crate'], x['id']) not in inA]
rng.shuffle(rest)
B = rest[:30]
json.dump({'seed': 20261110, 'population': len(pop), 'population_closed_no_axiom': sum(1 for x in pop if x['ok_closure_no_axiom']), 'A': A, 'B': B},
          open(os.path.join(FORK, 'data', 'sound_sample.json'), 'w'), indent=1)
print('population', len(pop), 'closed/no axiom', sum(1 for x in pop if x['ok_closure_no_axiom']))
for tag, L in (('A', A), ('B', B)):
    for i, x in enumerate(L):
        print(tag, i, x['crate'], '%s:%d-%d' % (x['file'], x['line_start'], x['line_end']), x['lean_names'], 'closed' if x['ok_closure_no_axiom'] else ('axioms: ' + ','.join(x['dep_axioms'][:3]) if x['ok_closure'] else 'callee fails'))
