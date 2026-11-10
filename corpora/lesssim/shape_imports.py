#!/usr/bin/env python3
"""Write producers.txt and generate lean/Shape.lean = imports of every module holding a producer + ShapeBody.lean."""
import json, sys, os
R = sys.argv[1]
H = os.path.dirname(os.path.abspath(__file__))
prod = set(json.load(open(R + '/out/corpus/lesssim/producers.json'))['prod'])
mods = set()
for l in open(R + '/out/corpus/ns/decls.jsonl'):
    d = json.loads(l)
    if d['name'] in prod: mods.add(d['module'])
open(R + '/out/corpus/lesssim/producers.txt', 'w').write('\n'.join(sorted(prod)) + '\n')
open(H + '/lean/Shape.lean', 'w').write(''.join(f'import {m}\n' for m in sorted(mods)) + open(H + '/lean/ShapeBody.lean').read())
