#!/usr/bin/env python3
"""Freeze the family by rule (see DECISIONS.md / LESSSIM.md section 1).
Rule: producers = census set (concl.exRealPos > 0); depth = longest producer->producer chain through valueDeps.
Head = the deepest producer, ties broken by lexicographically smallest full name.
Family = one longest path from the head: at each step the direct producer dependency of depth d-1,
ties broken by lexicographically smallest full name."""
import json, sys
REPO = sys.argv[1]
decl = {}
for l in open(REPO + '/out/corpus/ns/decls.jsonl'):
    d = json.loads(l); decl[d['name']] = d
P = json.load(open(REPO + '/out/corpus/lesssim/producers.json'))
prod, depth = set(P['prod']), P['depth']
m = max(depth.values())
cur = min(p for p in prod if depth[p] == m)
fam = [cur]
while depth[cur] > 1:
    cur = min(x for x in decl[cur]['valueDeps'] if x in prod and x != cur and depth[x] == depth[cur] - 1)
    fam.append(cur)
out = [{'name': n, 'depth': depth[n], 'module': decl[n]['module'], 'line': decl[n]['line'], 'endLine': decl[n]['endLine'],
        'proofSize': decl[n]['proofSize'], 'statementSize': decl[n]['statementSize'],
        'producerDeps': sorted(x for x in decl[n]['valueDeps'] if x in prod and x != n)} for n in fam]
json.dump(out, open(REPO + '/out/corpus/lesssim/family.json', 'w'), indent=1)
for o in out: print(o['depth'], o['name'], o['module'], o['line'], o['endLine'], o['proofSize'], o['statementSize'], o['producerDeps'])
