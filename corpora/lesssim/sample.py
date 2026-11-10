#!/usr/bin/env python3
"""The seeded sample of 10 producers outside the family: random.Random(20261110).sample(sorted(pool), 10)."""
import json, random, sys, os
R = sys.argv[1]
P = json.load(open(R + '/out/corpus/lesssim/producers.json'))
fam = {f['name'] for f in json.load(open(R + '/out/corpus/lesssim/family.json'))}
pool = sorted(n for n in P['prod'] if n not in fam)
S = random.Random(20261110).sample(pool, 10)
decl = {}
for l in open(R + '/out/corpus/ns/decls.jsonl'):
    d = json.loads(l)
    if d['name'] in S: decl[d['name']] = d
cp = R + '/out/corpus/lesssim/shape_classes.json'
cl = {o['name']: o for o in json.load(open(cp))} if os.path.exists(cp) else {}
out = []
for n in S:
    d = decl[n]
    out.append({'name': n, 'module': d['module'], 'line': d['line'], 'endLine': d['endLine'], 'proofSize': d['proofSize'],
                'statementSize': d['statementSize'], 'depth': P['depth'][n], 'class': cl.get(n, {}).get('class'),
                'atoms': cl.get(n, {}).get('atoms'),
                'producerDeps': sorted(x for x in d['valueDeps'] if x in P['prod'] and x != n)})
    print(n, d['module'], d['line'], d['endLine'], d['proofSize'], P['depth'][n], out[-1]['class'], out[-1]['atoms'], len(out[-1]['producerDeps']))
json.dump({'seed': 20261110, 'pool': len(pool), 'sample': out}, open(R + '/out/corpus/lesssim/sample.json', 'w'), indent=1)
