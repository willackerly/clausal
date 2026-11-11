#!/usr/bin/env python3
"""Checks the synthetic controls against planted/expected.json; writes out/families/ns/planted_result.json."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
O = os.path.join(H, '..', '..', 'out', 'families', 'ns')
R = [json.loads(l) for l in open(os.path.join(O, 'clusters_planted.jsonl'))]
E = json.load(open(os.path.join(H, 'planted', 'expected.json')))
res = {}
for k, e in E.items():
    mem = set(e['members'])
    hits = []
    for rank, r in enumerate(R):
        ms = set(r['members'])
        if ms & mem:
            hits.append({'rank': rank + 1, 'of': len(R), 'levels': r['levels'], 'tightest': r['tightest'], 'm': r['m'],
                         'containsAll': mem <= ms, 'onlyPlanted': ms <= mem,
                         'others': sorted(ms - mem)[:8], 'nHoles': r['nHoles'],
                         'holeKinds': [h['kind'] for h in r['holes']], 'skeleton': r['skeleton'],
                         'sharedShapes': r['sharedShapes'], 'sharedRoles': r['sharedRoles'], 'score': r['score']})
    res[k] = {'expect': e['expect'], 'members': e['members'], 'families': hits}
A = res['A']['families']
res['A']['pass'] = any(h['containsAll'] and h['onlyPlanted'] and h['tightest'] == 'L1' and h['nHoles'] == 1
                       and h['holeKinds'] == ['numeral'] and h['sharedShapes'] >= 4
                       and any('xAPI' in l for l in h['levels']) for h in A)
B = res['B']['families']
res['B']['pass'] = (not any(h['containsAll'] and any(l in ('L0', 'L1', 'L2', 'L3') for l in h['levels']) for h in B)
                    and any(h['containsAll'] and any(l.startswith(('ROLE', 'API')) for l in h['levels']) for h in B))
res['N1']['pass'] = not res['N1']['families']
N2 = res['N2']['families']
res['N2']['pass'] = any(h['containsAll'] and h['tightest'] == 'L1' and h['sharedShapes'] == 0 and h['sharedRoles'] == 0 for h in N2)
json.dump(res, open(os.path.join(O, 'planted_result.json'), 'w'), indent=1, ensure_ascii=False)
for k, v in res.items():
    print(k, 'PASS' if v['pass'] else 'FAIL', '|', v['expect'])
    for h in v['families']:
        print('    rank', h['rank'], h['levels'], 'm', h['m'], 'all', h['containsAll'], 'others', [o.split('.')[-1] for o in h['others']],
              'holes', h['holeKinds'], 'shapes', h['sharedShapes'], 'roles', h['sharedRoles'], '|', (h['skeleton'] or '')[:90])
