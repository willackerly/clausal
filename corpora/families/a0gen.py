#!/usr/bin/env python3
"""Class (a0): one type under many names.  Kernel-check that every member is the first member, by `rfl`.
usage: a0gen.py gen | collect"""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.join(HERE, '..', '..'); G = os.path.join(REPO, 'out/families/gen')
tri = json.load(open(os.path.join(REPO, 'out/families/triage_2026-11-11.json')))
ids = [r['id'] for r in tri['rows'] if r['cls'] == 'a0']
recs = {}
for l in open(os.path.join(REPO, 'out/families/ns/clusters.jsonl')):
    r = json.loads(l)
    if r['id'] in ids: recs[r['id']] = r
if sys.argv[1] == 'gen':
    mods = set(); body = []
    for f in ids:
        r = recs[f]; ms = r['members']
        for m in r['memberInfo']: mods.add(m['module'])
        for m in ms[1:]:
            body.append(f'run_cmd IO.println "BLOCK {f} {m}"\nexample : @{m} = @{ms[0]} := rfl')
    open(f'{HERE}/lean/A0.lean', 'w').write('\n'.join('import ' + m for m in sorted(mods)) + '\n\n' + '\n'.join(body) + '\n')
    print(len(ids), 'families', len(body), 'checks', len(mods), 'modules')
else:
    cur = None; res = {}
    for l in open(f'{HERE}/build/A0.log'):
        m = re.match(r'BLOCK (\S+) (\S+)', l)
        if m: cur = (m.group(1), m.group(2)); res[cur] = True; continue
        if cur and re.match(r'[^:]+\.lean:\d+:\d+: error', l): res[cur] = False
    out = {}
    for f in ids:
        r = recs[f]
        ok = sum(1 for (ff, m), v in res.items() if ff == f and v); n = sum(1 for (ff, m) in res if ff == f)
        out[f] = dict(members=r['m'], checked=n, rfl=ok, users=r['users'], skeleton=r['skeleton'][:80], modules=r['modules'])
    json.dump(out, open(f'{G}/a0.json', 'w'), indent=1, ensure_ascii=False)
    print(sum(v['members'] for v in out.values()), 'members;', sum(v['rfl'] for v in out.values()), 'of', sum(v['checked'] for v in out.values()), 'equal to the first member by rfl')
    for f, v in out.items():
        if v['rfl'] != v['checked']: print('  ', f, v)
