#!/usr/bin/env python3
"""Generate the four replay files of a family and (after compiling) collect the results.
usage: family.py gen FID IMPORT      -> lean/FID_{api,down}_{spec,sub}.lean   (substitution map: subst/FID.json)
       family.py collect FID         -> out/families/gen/FID_replay.json
The API list is out/families/gen/api.json (frozen); the downstream sample is 10 theorems whose statement
mentions a member, not in the API list, drawn with random.Random(20261111) from the sorted names; theorems
that depend on a private declaration cannot be re-elaborated outside their module and are skipped (counted)."""
import json, os, random, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.join(HERE, '..', '..')
mode, fid = sys.argv[1:3]
api = json.load(open(os.path.join(REPO, 'out/families/gen/api.json')))[fid]
G = os.path.join(REPO, 'out/families/gen')
if mode == 'gen':
    imp = sys.argv[3]
    members = set(api['members']); apinames = [t['name'] for t in api['thms']]
    decl = {}
    cand = []
    for l in open(os.path.join(REPO, 'out/corpus/ns/decls.jsonl')):
        d = json.loads(l)
        if d['kind'] != 'theorem': continue
        decl[d['name']] = d
        if members & set(d['typeDeps']) and d['name'] not in apinames and not d['isPrivate']:
            cand.append(d['name'])
    cand.sort()
    order = cand[:]; random.Random(20261111).shuffle(order)
    def private(n): return any(x.startswith('_private') for x in decl[n]['valueDeps'] + decl[n]['typeDeps'])
    sample, skipped = [], []
    for n in order:
        if len(sample) == 10: break
        (skipped if private(n) else sample).append(n)
    apiok = [n for n in apinames if not private(n) and not decl[n]['isPrivate']]
    json.dump(dict(candidates=len(cand), sample=sample, skippedPrivate=skipped, api=apinames, apiReplayable=apiok,
                   apiPrivate=[n for n in apinames if n not in apiok]), open(f'{G}/{fid}_sample.json', 'w'), indent=1)
    sub = os.path.join(HERE, 'subst', fid + '.json')
    for tag, names in (('api', apiok), ('down', sample)):
        subprocess.check_call([sys.executable, os.path.join(HERE, 'replay.py'), f'{HERE}/lean/{fid}_{tag}_spec.lean', '_S', '', '-'] + names)
        subprocess.check_call([sys.executable, os.path.join(HERE, 'replay.py'), f'{HERE}/lean/{fid}_{tag}_sub.lean', '_R', imp, sub] + names)
    print(f'{fid}: {len(cand)} candidates downstream; sample {len(sample)}, skipped private {len(skipped)}; api replayable {len(apiok)}/{len(apinames)}')
else:
    res = {}
    for tag in ('api', 'down'):
        for v in ('spec', 'sub'):
            if not os.path.exists(f'{HERE}/build/{fid}_{tag}_{v}.log'): res[f'{tag}_{v}'] = []; continue
            out = subprocess.check_output([sys.executable, os.path.join(HERE, 'replay_log.py'), f'{HERE}/build/{fid}_{tag}_{v}.log']).decode()
            res[f'{tag}_{v}'] = [json.loads(x) for x in out.strip().split('\n') if x]
    json.dump(res, open(f'{G}/{fid}_replay.json', 'w'), indent=1, ensure_ascii=False)
    for k, v in res.items():
        print(fid, k, 'ok', sum(x['ok'] for x in v), 'of', len(v), 'heartbeats(ok)', sum(x['heartbeats'] or 0 for x in v if x['ok']))
    for tag in ('api', 'down'):
        sp = {x['name']: x for x in res[f'{tag}_spec']}
        for x in res[f'{tag}_sub']:
            if not x['ok']: print('  FAIL', tag, x['name'], '|', (x['error'] or '')[:230], '| spec ok:', sp.get(x['name'], {}).get('ok'))
