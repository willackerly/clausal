#!/usr/bin/env python3
"""Opacity analysis driver.  usage: absgen.py gen FID [extra member ...] | collect FID
gen: writes lean/FID_abs.lean and build/FID_abs.txt (all non-private theorems whose statement or proof uses a member)."""
import json, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.join(HERE, '..', '..'); G = os.path.join(REPO, 'out/families/gen')
mode, fid = sys.argv[1:3]
api = json.load(open(f'{G}/api.json'))[fid]
members = api['members'] + sys.argv[3:]
if mode == 'gen':
    ms = set(members); ts = []; mods = set(); priv = 0
    for l in open(os.path.join(REPO, 'out/corpus/ns/decls.jsonl')):
        d = json.loads(l)
        if d['kind'] != 'theorem': continue
        if ms & (set(d['typeDeps']) | set(d['valueDeps'])):
            if d['isPrivate'] or '«' in d['name']: priv += 1; continue
            ts.append(d['name']); mods.add(d['module'])
    ts.sort(); total = len(ts)
    if len(ts) > 200:
        import random
        ts = sorted(random.Random(20261111).sample(ts, 200))
    users_list = list(ts)
    sm = json.load(open(f'{G}/{fid}_sample.json')) if os.path.exists(f'{G}/{fid}_sample.json') else dict(sample=[], apiReplayable=[])
    extra = [n for n in sm['sample'] + sm['apiReplayable'] if n not in ts]
    ts = ts + extra
    for l in open(os.path.join(REPO, 'out/corpus/ns/decls.jsonl')):
        d = json.loads(l)
        if d['name'] in extra: mods.add(d['module'])
    open(f'{HERE}/build/{fid}_abs.txt', 'w').write('\n'.join(ts) + '\n')
    json.dump(dict(theorems=total, analysed=len(ts), usersAnalysed=users_list, private=priv, members=members), open(f'{G}/{fid}_abs_meta.json', 'w'))
    L = ['import Abs'] + ['import ' + m for m in sorted(mods)] + ['open Lean Elab Command', 'set_option maxHeartbeats 0', 'set_option Elab.async false',
         'run_cmd do',
         f'  let ts := (← IO.FS.lines "{HERE}/build/{fid}_abs.txt").toList.filter (· != "") |>.map String.toName',
         f'  Fam.Abs.go "{fid}" [{", ".join("`" + m for m in (json.load(open(HERE + "/subst/" + fid + ".abs.json"))["ms"] if os.path.exists(HERE + "/subst/" + fid + ".abs.json") else members))}] ts']
    open(f'{HERE}/lean/{fid}_abs.lean', 'w').write('\n'.join(L) + '\n')
    print(fid, len(ts), 'theorems', priv, 'private skipped', len(mods), 'modules')
else:
    rows = [json.loads(l[4:]) for l in open(f'{HERE}/build/{fid}_abs.out') if l.startswith('ABS ')]
    json.dump(rows, open(f'{G}/{fid}_abs.json', 'w'), ensure_ascii=False)
    sm = json.load(open(f'{G}/{fid}_sample.json'))
    meta = json.load(open(f'{G}/{fid}_abs_meta.json'))
    users = [r for r in rows if r['name'] in set(meta['usersAnalysed'])]
    c = collections.Counter(r['result'] for r in users)
    print(fid, 'users analysed', len(users), 'of', meta['theorems'], dict(c))
    for tag, names in (('down10', sm['sample']), ('api', sm['apiReplayable'])):
        print('  ', tag, dict(collections.Counter(r['result'] for r in rows if r['name'] in names)))
    cs = collections.Counter(r['result'] for r in rows if r.get('inStatement'))
    print('  member in statement:', dict(cs))
    cited = collections.Counter(x for r in rows if r['result'] == 'generic' for x in r['cited'])
    print('  distinct cited lemmas by generic proofs:', len(cited), cited.most_common(8))
    for r in rows:
        if r['result'] == 'error': print('  ERR', r['name'], r.get('why', '')[:200])
