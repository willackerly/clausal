#!/usr/bin/env python3
"""names.py <project>: library constants whose theorems the `thms` export keeps: every Prop-valued library
definition/structure (for the API-signature generator) and every library notion of a stage 1 candidate."""
import json, os, sys
from stage1 import GLUE
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
p = sys.argv[1]
names = set()
for l in open(os.path.join(REPO, 'out/reinvent', p, 'raw/defs.jsonl')):
    r = json.loads(l)
    if not r['proj'] and r['isProp'] and r['kind'] != 'char':
        names.add(r['name'])
cand = set()
for d in [p] + (['planted'] if p == 'pfr' else []):
    f = os.path.join(REPO, 'out/reinvent', d, 'candidates.jsonl')
    if os.path.exists(f):
        for l in open(f):
            cand.add(json.loads(l)['L'])
# glue constants are dropped unless a stage 1 candidate names one as its library notion (e.g. `Set.preimage`):
# without its theorems the API-copy signal has nothing to compare against
names = (names - GLUE) | cand
open(os.path.join(REPO, 'out/reinvent', p, 'raw/names.txt'), 'w').write('\n'.join(sorted(names)) + '\n')
print(p, len(names))
