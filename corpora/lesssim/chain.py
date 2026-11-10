#!/usr/bin/env python3
"""Recompute the census's producer set (conclusion has a real ∃ with a sign conjunct: concl.exRealPos > 0)
and the producer->producer chain depth, from the Lean exports.  Prints the deepest producers and their cones."""
import json, sys, collections
REPO = sys.argv[1]
decl = {}
for l in open(REPO + '/out/corpus/ns/decls.jsonl'):
    d = json.loads(l)
    decl[d['name']] = d
prod = set()
for l in open(REPO + '/out/corpus/friction/ns/hyps.jsonl'):
    d = json.loads(l)
    if d['concl'].get('exRealPos', 0) > 0:
        prod.add(d['name'])
sys.setrecursionlimit(100000)
depth = {}
def dep(n):
    if n in depth: return depth[n]
    depth[n] = 1
    best = 0
    for x in decl[n]['valueDeps']:
        if x in prod and x != n:
            best = max(best, dep(x))
    depth[n] = 1 + best
    return depth[n]
for p in prod: dep(p)
json.dump({'prod': sorted(prod), 'depth': depth}, open(REPO + '/out/corpus/lesssim/producers.json', 'w'))
print(len(prod), collections.Counter(depth.values()))
top = sorted([p for p in prod if depth[p] == max(depth.values())])
def cone(n, seen):
    if n in seen: return
    seen.add(n)
    for x in decl[n]['valueDeps']:
        if x in prod and x != n: cone(x, seen)
for t in top:
    s = set(); cone(t, s)
    print(t, decl[t]['module'], 'cone', len(s), 'proofSize', decl[t]['proofSize'])
    for x in sorted(s, key=lambda x: (-depth[x], x)):
        print('   ', depth[x], x, decl[x]['module'], decl[x]['line'], decl[x]['endLine'], decl[x]['proofSize'], decl[x]['statementSize'])
