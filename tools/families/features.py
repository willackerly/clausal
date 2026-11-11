#!/usr/bin/env python3
"""M9 families, step 1: features per project definition.   features.py <project> [--planted]

Reads out/families/<p>/raw/export.jsonl (typed trees from Lean), the dead-code tool's result
(out/deadcode/<p>/) and writes out/families/<p>/features.pkl plus funnel.json.
With --planted: raw/planted.jsonl (the synthetic controls) is mixed into the project; writes planted.pkl.
"""
import sys, json, os, pickle, collections
sys.setrecursionlimit(100000)
from tree import parse, size, renumber_params, consts, Renderer, h64, role

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '..', '..')

META_PREFIX = ('Lean.', 'Qq.', 'Mathlib.Tactic.', 'Mathlib.Meta.', 'Aesop.', 'Batteries.Tactic', 'Std.Tactic',
               'Lean', 'ReaderT', 'StateT', 'IO', 'EStateM')


def is_meta(rec, cs):
    if rec.get('rtag', '').startswith(META_PREFIX) or rec['name'].startswith(('Mathlib.Tactic', 'Mathlib.Meta', 'Lean.')):
        return True
    if '_aux_' in rec['name'] or 'macroRules' in rec['name'] or '«term' in rec['name']:
        return True
    return any(c.startswith(('Lean.', 'Qq.', 'Mathlib.Tactic.', 'Mathlib.Meta.')) for c in cs)


def main():
    proj = sys.argv[1]
    planted = '--planted' in sys.argv
    O = os.path.join(REPO, 'out', 'families', proj)
    recs = [json.loads(l) for l in open(os.path.join(O, 'raw', 'export.jsonl'))]
    pl_names = set()
    if planted:   # the synthetic controls are mixed into the project, and count as reachable
        pl = [json.loads(l) for l in open(os.path.join(O, 'raw', 'planted.jsonl'))]
        pl_names = {r['name'] for r in pl}
        recs += pl
    names = {r['name'] for r in recs}
    parents = set(names)

    _pc = {}

    def isproj(n):
        v = _pc.get(n)
        if v is None:
            v = False
            p = n
            while True:
                if p in parents:
                    v = True
                    break
                i = p.rfind('.')
                if i < 0:
                    break
                p = p[:i]
            _pc[n] = v
        return v

    # reachability from the headline theorems (dead-code tool)
    funnel = collections.OrderedDict()
    users = collections.defaultdict(set)
    D = os.path.join(REPO, 'out', 'deadcode', proj)
    dd = [json.loads(l) for l in open(os.path.join(D, 'export', 'decls.jsonl'))]
    unreach = {json.loads(l)['name'] for l in open(os.path.join(D, 'unreachable.jsonl'))}
    indead = {d['name'] for d in dd} | pl_names
    reachable = indead - unreach
    for d in dd:
        if d['name'] in reachable:
            for x in set(d.get('typeDeps', [])) | set(d.get('valueDeps', [])):
                users[x].add(d['name'])
    funnel['records exported (definitions, structures, theorems, inductives)'] = len(recs)

    defs = {}
    thms = {}
    cnt = collections.Counter()
    for r in recs:
        if r['rec'] == 'thm':
            if r.get('big'):
                cnt['theorem statements over the node limit (not profiled)'] += 1
                continue
            thms[r['name']] = r
            continue
        if r['rec'] != 'def':
            cnt['rec:' + r['rec']] += 1
            continue
        cnt['definitions and structures exported'] += 1
        if r.get('big'):
            cnt['dropped: body over 4000 nodes'] += 1
            continue
        body = parse(r['body'])
        cs = consts(body)
        ptrees = [parse(p['t']) for p in r['params']]
        for pt in ptrees:
            consts(pt, cs)
        if is_meta(r, cs):
            cnt['dropped: syntax / metaprogramming'] += 1
            continue
        if r['name'].startswith('_private.') and ('match_' in r['name'] or '_proof_' in r['name']):
            cnt['dropped: auxiliary'] += 1
            continue
        r['_body'] = body
        r['_ptrees'] = ptrees
        r['_consts'] = cs
        defs[r['name']] = r
    funnel.update(cnt)
    funnel['definitions and structures kept (all)'] = len(defs)
    funnel['… not in the dead-code export (auxiliary definitions Lean generated)'] = sum(1 for n in defs if n not in indead)
    funnel['… reachable from the headline theorems'] = sum(1 for n in defs if n in reachable)
    funnel['theorems with a statement tree'] = len(thms)
    funnel['… reachable'] = sum(1 for n in thms if n in reachable)

    R = [Renderer(l, isproj) for l in range(4)]
    feats = {}
    for n, r in defs.items():
        body, order = renumber_params(r['_body'])
        pn = [r['params'][o]['n'] for o in order]
        rty = parse(r['rty']) if 'rty' in r else ('BIG',)
        sig = ('SIG',) + tuple(('P', p['k'], t) for p, t in zip(r['params'], r['_ptrees'])) + (rty,)
        f = {
            'name': n, 'module': r['module'], 'kind': r['kind'], 'isProp': r['isProp'], 'rtag': r['rtag'],
            'reach': n in reachable, 'body': body, 'pnames': pn, 'nodes': size(body), 'sig': sig,
            'pp': r['pp'], 'ppBody': r.get('ppBody', ''), 'unf': r.get('unf', []),
            'nparams': len(r['params']), 'pk': ''.join(p['k'] for p in r['params']),
            'projconsts': sorted(c for c in r['_consts'] if isproj(c)),
            'bk': [h64(R[l].r(body)) for l in range(4)],
            'sk': [h64(R[l].r(sig)) for l in range(4)],
            'users': sorted(users.get(n, ())),
        }
        # specialisation: the body is one project definition applied to arguments
        b = body
        f['wraps'] = b[2] if (not isinstance(b, str) and b[0] == 'A' and isinstance(b[2], str) and b[2] in defs) else None
        # after unfolding an abbrev, the wrapped head is gone; record what was unfolded at the root instead
        feats[n] = f

    # API profile: statement shapes of the theorems that mention the definition, the definition a hole
    prof = {n: collections.defaultdict(list) for n in feats}
    prof_all = {n: collections.defaultdict(list) for n in feats}
    profL = {n: collections.defaultdict(list) for n in feats}
    profL_all = {n: collections.defaultdict(list) for n in feats}
    roles = {n: collections.defaultdict(list) for n in feats}
    roles_all = {n: collections.defaultdict(list) for n in feats}
    mention = collections.defaultdict(set)
    cooc = collections.Counter()
    nprof = 0
    for tn, r in thms.items():
        st = parse(r['st'])
        cs = consts(st)
        ds = set()
        for c in cs:
            p = c
            while True:
                if p in feats:
                    ds.add(p)
                    break
                i = p.rfind('.')
                if i < 0:
                    break
                p = p[:i]
        reach = tn in reachable
        ds = sorted(ds)
        if reach:
            for i in range(len(ds)):
                for j in range(i + 1, len(ds)):
                    cooc[(ds[i], ds[j])] += 1
        for d in ds:
            ren = {}
            pre = d + '.'

            def cmap(c, d=d, pre=pre, ren=ren):
                if c == d:
                    return '◊'
                if c.startswith(pre):
                    return '◊.'
                if isproj(c):
                    if c not in ren:
                        ren[c] = f'P{len(ren)}'
                    return ren[c]
                return c
            key = h64(Renderer(1, isproj, cmap).r(st))
            ren.clear()
            keyL = h64(Renderer(2, isproj, cmap).r(st))
            rl = role(st, d, isproj)
            prof_all[d][key].append(tn)
            profL_all[d][keyL].append(tn)
            roles_all[d][rl].append(tn)
            if reach:
                prof[d][key].append(tn)
                profL[d][keyL].append(tn)
                roles[d][rl].append(tn)
                mention[d].add(tn)
            nprof += 1
    for n, f in feats.items():
        f['api'] = dict(prof[n])
        f['api_all'] = dict(prof_all[n])
        f['apiL'] = dict(profL[n])
        f['apiL_all'] = dict(profL_all[n])
        f['roles'] = dict(roles[n])
        f['roles_all'] = dict(roles_all[n])
        f['nstmt'] = len(mention[n])
    funnel['(theorem, definition) profile entries'] = nprof
    funnel['definitions with ≥ 1 reachable theorem stated about them'] = sum(1 for f in feats.values() if f['nstmt'])
    funnel['reachable definitions by kind'] = dict(collections.Counter(
        ('predicate/relation' if f['isProp'] and f['kind'] not in ('structure', 'class') else
         'structure' if f['kind'] in ('structure', 'class') else
         'type family' if f['rtag'] == 'U' else 'function/operation' if f['nparams'] else 'constant')
        for f in feats.values() if f['reach']))
    pickle.dump({'feats': feats, 'cooc': dict(cooc), 'reachable_thms': sorted(n for n in thms if n in reachable),
                 'projnames': sorted(parents)}, open(os.path.join(O, 'planted.pkl' if planted else 'features.pkl'), 'wb'))
    json.dump(funnel, open(os.path.join(O, 'planted_funnel.json' if planted else 'funnel.json'), 'w'), indent=1, ensure_ascii=False)
    for k, v in funnel.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()
