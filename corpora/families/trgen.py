#!/usr/bin/env python3
"""Statement transport driver.  usage: trgen.py gen FID | collect FID
config subst/FID.tr.json: {"import": "F42", "pairs": [[member, replacement, eqThm|null], ...]} or {"import":..., "eqns": [[member, eqThm], ...]}
Theorems: the family's API list and its downstream sample (out/families/gen/FID_sample.json)."""
import json, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.join(HERE, '..', '..'); G = os.path.join(REPO, 'out/families/gen')
mode, fid = sys.argv[1:3]
if mode == 'gen':
    cfg = json.load(open(f'{HERE}/subst/{fid}.tr.json'))
    sm = json.load(open(f'{G}/{fid}_sample.json'))
    ts = sm['apiReplayable'] + sm['sample']
    decl = {}
    for l in open(os.path.join(REPO, 'out/corpus/ns/decls.jsonl')):
        d = json.loads(l)
        if d['name'] in ts: decl[d['name']] = d['module']
    open(f'{HERE}/build/{fid}_tr.txt', 'w').write('\n'.join(ts) + '\n')
    L = ['import Abs', 'import ' + cfg['import']] + ['import ' + m for m in sorted(set(decl.values()))] + ['open Lean Elab Command', 'set_option maxHeartbeats 0', 'set_option Elab.async false', 'run_cmd do',
         f'  let ts := (← IO.FS.lines "{HERE}/build/{fid}_tr.txt").toList.filter (· != "") |>.map String.toName']
    if 'eqns' in cfg:
        L.append(f'  Fam.Abs.transportEqns "{fid}" [' + ', '.join(f'(`{a}, `{b})' for a, b in cfg['eqns']) + '] ts')
    else:
        L.append(f'  Fam.Abs.transport "{fid}" [' + ', '.join(f'(`{a}, `{b}, {"some `" + c if c else "none"})' for a, b, c in cfg['pairs']) + '] ts')
    open(f'{HERE}/lean/{fid}_tr.lean', 'w').write('\n'.join(L) + '\n')
    print(fid, len(ts), 'theorems')
else:
    sm = json.load(open(f'{G}/{fid}_sample.json'))
    rows = [json.loads(l[3:]) for l in open(f'{HERE}/build/{fid}_tr.out') if l.startswith('TR ')]
    for r in rows: r['set'] = 'down' if r['name'] in sm['sample'] else 'api'
    json.dump(rows, open(f'{G}/{fid}_tr.json', 'w'), ensure_ascii=False)
    for s in ('api', 'down'):
        c = collections.Counter(r['result'] for r in rows if r['set'] == s)
        a = sum(r.get('statementDag', 0) for r in rows if r['set'] == s and 'newStatementDag' in r); b = sum(r.get('newStatementDag', 0) for r in rows if r['set'] == s and 'newStatementDag' in r)
        print(fid, s, dict(c), 'statement dag', a, '->', b)
    for r in rows:
        if r['result'] == 'fail': print('  FAIL', r['name'], r.get('why', '')[:200])
