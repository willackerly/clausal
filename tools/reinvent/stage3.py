#!/usr/bin/env python3
"""M7 stage 1c (API-copy signal) and stage 3 (cost).  usage: stage3.py <project> [--planted] [--derive N] [--jobs K]

Inputs: out/reinvent/<p>/stage2.jsonl + candidates.jsonl, raw/thms.jsonl (statement skeletons from Export.lean,
mode thms), out/corpus/<p>/decls.jsonl (source lines, proof sizes and direct dependencies, exported from Lean
by an earlier node).

API-copy signal, two forms:
 (a) per candidate pair (D, L): every project theorem whose statement mentions D is rewritten by replacing
     each full application of D with the library term of the candidate; it "maps" if some library theorem
     mentioning L has a conclusion that matches the rewritten conclusion as a pattern (the library theorem's
     binders are the pattern variables; exact rules only, no approximate ones) and each of its Prop
     hypotheses matches some hypothesis of the project theorem under the same assignment.
 (b) with no candidate pair: Prop-level signatures of statements with one predicate replaced by a hole;
     a pair (D, L) is proposed when >= 3 project theorems about D, and >= 25% of them, have the holed
     signature of some library theorem about L, counting only signatures with >= 3 symbols.
Cost, for confirmed pairs: project theorems whose statement mentions D, those that map under (a), their
source lines and proof sizes, project theorems that use D at all (statement or proof, direct), and a seeded
sample of mapped theorems re-derived in Lean from the library theorem through the confirmed equivalence."""
import collections
import json
import os
import random
import re
import sys

import skel
from skel import parse, rigidify, match, finish, State, consts, sig, shift, mk_app, is_const, weight, Budget
from stage2 import run_batches, cmd

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SEED = 20261110
CONFIRMED = ('proved', 'proved under side condition')


def subst_params(t, args, depth=0):
    """Replace rigid parameters '§i' of a candidate's library term by args[i] (given at depth 0)."""
    if isinstance(t, str):
        if t[0] == '§':
            i = int(t[1:])
            return shift(args[i], depth) if i < len(args) else '*'
        return t
    tag = t[0]
    if tag in ('\\', '!'):
        return (tag, subst_params(t[1], args, depth), subst_params(t[2], args, depth + 1))
    if tag in ('p', 'a'):
        h = subst_params(t[1], args, depth)
        rest = tuple(subst_params(x, args, depth) for x in t[2:])
        if isinstance(h, tuple) and isinstance(t[1], str) and t[1][0] == '§':
            return mk_app(tag, h, rest)
        return (tag, h) + rest
    return (tag,) + tuple(subst_params(x, args, depth) for x in t[1:])


def occurs0(t, k=0):
    if isinstance(t, str):
        return t == '#%d' % k
    if t[0] in ('\\', '!'):
        return occurs0(t[1], k) or occurs0(t[2], k + 1)
    return any(occurs0(x, k) for x in t[1:])


def eta(t):
    """Eta-reduce `fun x => h a.. x` bottom-up."""
    if isinstance(t, str):
        return t
    t = (t[0],) + tuple(eta(x) for x in t[1:])
    if t[0] == '\\':
        b = t[2]
        if isinstance(b, tuple) and b[0] in ('p', 'a') and len(b) >= 3 and b[-1] == '#0' and \
                not any(occurs0(x) for x in b[1:-1]):
            r = b[1] if len(b) == 3 else b[:-1]
            return skel.subst_bv0(r, '*')
    return t


class Partial(Exception):
    pass


def rewrite(t, D, rhs, np):
    """Replace applications of D.  Raises Partial when D occurs unapplied or under-applied."""
    if isinstance(t, str):
        if t == D:
            if np == 0:
                return rhs
            raise Partial()
        return t
    if t[0] in ('p', 'a') and t[1] == D:
        args = tuple(rewrite(x, D, rhs, np) for x in t[2:])
        if len(args) < np:
            raise Partial()
        r = subst_params(rhs, args[:np])
        if len(args) > np:
            r = mk_app('a', r, args[np:])
        return r
    return (t[0],) + tuple(rewrite(x, D, rhs, np) for x in t[1:])


def head_key(t):
    if isinstance(t, tuple) and t[0] in ('p', 'a') and isinstance(t[1], str) and is_const(t[1]):
        return t[1]
    return t[0] if isinstance(t, tuple) else 'atom'


def thm_match(pc, phyps, sc, shyps):
    """Is the subject statement an instance of the pattern statement?"""
    skel.STEPS[0] = 0
    try:
        for st in match(pc, sc, 0, State(), (), False):
            def go(i, st1):
                if i == len(phyps):
                    return finish(st1) is not None
                for h in shyps:
                    for st2 in match(phyps[i], h, 0, st1, (), False):
                        if go(i + 1, st2):
                            return True
                return False
            if go(0, st):
                return True
    except Budget:
        return False
    return False


HOLE = '□'


def stmt_sig(concl, hyps):
    hs = sorted(x for x in (sig(h, False) for h in hyps) if x and x != '§')
    return '⊢' + sig(concl, False) + '|' + ';'.join(hs)


def holed(s, name):
    out = re.sub(r"(?<![\w.'₀-₉])" + re.escape(name) + r"\[", HOLE + '[', s)
    return out if out != s else None


def nsym(s):
    return len(re.findall(r"[^\[\],;|>&!\\⊢§?]+", s))


def main():
    project = sys.argv[1]
    planted = '--planted' in sys.argv
    nder = int(sys.argv[sys.argv.index('--derive') + 1]) if '--derive' in sys.argv else 5
    jobs = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 4
    out = os.path.join(REPO, 'out/reinvent', 'planted' if planted else project)
    skels = {}
    for l in open(os.path.join(out, 'candidates.jsonl')):
        c = json.loads(l)
        skels[c['id']] = c.get('rhs_skel')
    cands = [json.loads(l) for l in open(os.path.join(out, 'stage2.jsonl'))]
    for c in cands:
        c['rhs_skel'] = skels.get(c['id'])
    Ds = {c['D'] for c in cands}
    Ls = {c['L'] for c in cands}

    # ---- declarations (lines, sizes, dependencies)
    decl = {}
    users = collections.Counter()
    stmt_users = collections.defaultdict(list)
    if not planted:
        for l in open(os.path.join(REPO, 'out/corpus', project, 'decls.jsonl')):
            r = json.loads(l)
            decl[r['name']] = dict(lines=((r.get('endLine') or 0) - (r.get('line') or 0) + 1) if r.get('line') else 0, psize=r.get('proofSize') or 0,
                                   module=r.get('module'), line=r.get('line'), statement=r.get('statement', ''),
                                   kind=r.get('kind'))
            if r.get('kind') == 'theorem':
                for d in set(r.get('typeDeps', [])) | set(r.get('valueDeps', [])):
                    users[d] += 1
                for d in set(r.get('typeDeps', [])):
                    stmt_users[d].append(r['name'])

    # ---- theorem skeletons
    tf = os.path.join(REPO, 'out/reinvent', project, 'raw', 'planted_thms.jsonl' if planted else 'thms.jsonl')
    proj_thms = collections.defaultdict(list)     # D -> [(name, concl, hyps)]
    lib_thms = collections.defaultdict(lambda: collections.defaultdict(list))   # L -> head -> [(name, concl, hyps, pp)]
    lib_sig = collections.defaultdict(set)        # holed signature -> {L}
    proj_sig = collections.defaultdict(lambda: collections.defaultdict(set))    # D -> sig -> {thm}
    proj_pred = set()
    for l in open(os.path.join(REPO, 'out/reinvent', project, 'raw/defs.jsonl')):
        if '"proj":true' in l and '"isProp":true' in l:
            r = json.loads(l)
            if r['kind'] != 'char':
                proj_pred.add(r['name'])
    if planted:
        for l in open(os.path.join(REPO, 'out/reinvent', project, 'raw/planted_defs.jsonl')):
            r = json.loads(l)
            if r['isProp'] and r['kind'] != 'char':
                proj_pred.add(r['name'])
    wanted = set(open(os.path.join(REPO, 'out/reinvent', project, 'raw/names.txt')).read().split())
    n_proj = n_lib = 0
    for l in open(tf):
        r = json.loads(l)
        try:
            concl = parse(r['concl'])
            hyps = [parse(h[1]) for h in r['hyps']]
        except Exception:
            continue
        cs = consts(concl)
        for h in hyps:
            consts(h, cs)
        if r['proj']:
            if planted and not r['module'].startswith('ReinventPlanted'):
                continue
            n_proj += 1
            hit = cs & Ds
            for D in hit:
                proj_thms[D].append((r['name'], concl, hyps))
            preds = cs & proj_pred
            if preds:
                s = stmt_sig(concl, hyps)
                for D in preds:
                    hs = holed(s, D)
                    if hs and nsym(hs) >= 3:
                        proj_sig[D][hs].add(r['name'])
        else:
            n_lib += 1
            for L in cs & Ls:
                lib_thms[L][head_key(concl)].append((r['name'], concl, hyps, r.get('pp', '')))
            s = None
            for L in cs & wanted:
                if s is None:
                    s = stmt_sig(concl, hyps)
                hs = holed(s, L)
                if hs and nsym(hs) >= 3:
                    lib_sig[hs].add(L)
    print('theorem statements: project %d, library %d' % (n_proj, n_lib), file=sys.stderr)

    # ---- (a) API copies per candidate pair
    for c in cands:
        D, L = c['D'], c['L']
        c['n_stmt'] = len(proj_thms.get(D, []))
        c['mapped'] = []
        if not c['rhs_skel'] or c['verdict'] == 'ill-typed':
            continue
        rhs = parse(c['rhs_skel'])
        lt = lib_thms.get(L, {})
        for (name, concl, hyps) in proj_thms.get(D, []):
            try:
                sc = rigidify(eta(rewrite(concl, D, rhs, c['np'])))
                sh = [rigidify(eta(rewrite(h, D, rhs, c['np']))) for h in hyps]
            except Partial:
                continue
            found = []
            for (ln, pc, ph, pp) in lt.get(head_key(sc), []):
                if weight(pc) < 2 or len(ph) > 6:
                    continue
                if thm_match(pc, ph, sc, sh):
                    found.append(ln)
                    if len(found) >= 12:
                        break
            if found:
                found.sort(key=lambda n: (len(n), n))
                c['mapped'].append((name, found[0], found[1:3]))
        c['n_mapped'] = len(c['mapped'])

    # ---- (b) holed-signature generator
    api_pairs = []
    for D, sigs in proj_sig.items():
        total = set()
        for s, ts in sigs.items():
            total |= ts
        perL = collections.defaultdict(set)
        for s, ts in sigs.items():
            for L in lib_sig.get(s, ()):
                perL[L] |= ts
        for L, ts in perL.items():
            if len(ts) >= 3 and len(ts) >= 0.25 * len(total):
                api_pairs.append(dict(D=D, L=L, matched=len(ts), about_D=len(total)))
    api_pairs.sort(key=lambda x: (-x['matched'], x['D'], x['L']))
    shape_pairs = {(c['D'], c['L']) for c in cands}
    conf_pairs = {(c['D'], c['L']) for c in cands if c['verdict'] in CONFIRMED}
    for a in api_pairs:
        a['also_shape_candidate'] = (a['D'], a['L']) in shape_pairs
        a['confirmed'] = (a['D'], a['L']) in conf_pairs

    # ---- cost for confirmed pairs: one primary library notion per D
    # shown notion: most mapped theorems, then proved outright, then a shape match over an alias, then the
    # fewest approximations, then the heaviest pattern (the most specific library notion), then the smallest
    # library term (fewest arguments the matcher had to invent), then candidate order
    def pkey(c):
        return (c['n_mapped'], c['verdict'] == 'proved', c['rule'] != 'wrapper', -c['extras'] - c['absorbed'], c['wpat'],
                -skel.size(parse(c['rhs_skel'])) if c.get('rhs_skel') else 0)
    primary = {}
    for c in cands:
        if c['verdict'] in CONFIRMED and (c['D'] not in primary or pkey(c) > pkey(primary[c['D']])):
            primary[c['D']] = c
    rnd = random.Random(SEED)
    lines = [[] for _ in range(jobs)]
    k = 0
    for D in sorted(primary):
        c = primary[D]
        about = [t[0] for t in proj_thms.get(D, [])]
        c['cost'] = dict(
            lemmas_about_D=len(about),
            lemmas_about_D_lines=sum(decl.get(t, {}).get('lines', 0) for t in about),
            lemmas_about_D_proof_size=sum(decl.get(t, {}).get('psize', 0) for t in about),
            mapped=len(c['mapped']),
            mapped_lines=sum(decl.get(m[0], {}).get('lines', 0) for m in c['mapped']),
            mapped_proof_size=sum(decl.get(m[0], {}).get('psize', 0) for m in c['mapped']),
            users=users.get(D, 0), statement_users=len(stmt_users.get(D, [])))
        if c['mapped'] and nder:
            sample = rnd.sample(sorted(c['mapped']), min(nder, len(c['mapped'])))
            side = c['verdict'] == 'proved under side condition'
            J = lines[k % jobs]
            k += 1
            J.append(cmd(c, 'iff', c['sides'] if side else []))
            for i, (t, ln, alts) in enumerate(sample):
                for j, ln2 in enumerate([ln] + list(alts)):
                    try:
                        skel.lean_name(t), skel.lean_name(ln2)
                    except skel.Unprintable:
                        continue
                    J.append('reinvent_derive "%s_%d_%d" %s %s Reinvent.eqv.%s' % (c['id'], i, j, t, ln2, c['id'] + ('s' if side else '')))
            c['derive_sample'] = sample
    derived = {}
    if any(lines):
        for r in run_batches(project, 'drv', [l for l in lines if l], ['ReinventPlanted'] if planted else []):
            if r['kind'] == 'derive':
                derived[r['id']] = r
    for c in primary.values():
        ds = []
        for i in range(len(c.get('derive_sample', []))):
            rs = [derived.get('%s_%d_%d' % (c['id'], i, j)) for j in range(3)]
            rs = [r for r in rs if r]
            ds.append(next((r for r in rs if r['status'] == 'derived'), rs[0] if rs else None))
        c['derive'] = [dict(lemma=s[0], lib=(d or {}).get('lib', s[1]), status=(d or {}).get('status', 'no result'),
                            tactic=(d or {}).get('tactic'), stdAxioms=(d or {}).get('stdAxioms'))
                       for s, d in zip(c.get('derive_sample', []), ds)]
        c['primary'] = True
    with open(os.path.join(out, 'stage3.jsonl'), 'w') as f:
        for c in cands:
            c['mapped'] = [list(m) for m in c['mapped']]
            f.write(json.dumps(c, ensure_ascii=False) + '\n')
    with open(os.path.join(out, 'api_pairs.json'), 'w') as f:
        json.dump(dict(n_pairs=len(api_pairs), n_also_shape=sum(a['also_shape_candidate'] for a in api_pairs),
                       n_confirmed=sum(a['confirmed'] for a in api_pairs),
                       project_predicates_with_theorems=len(proj_sig), pairs=api_pairs[:300]), f, indent=1,
                  ensure_ascii=False)
    print('%s: pairs with >=1 mapped lemma: %d; API-signature pairs: %d (also shape: %d); confirmed D: %d; derived %d of %d'
          % (project, sum(1 for c in cands if c.get('n_mapped')), len(api_pairs),
             sum(a['also_shape_candidate'] for a in api_pairs), len(primary),
             sum(1 for c in primary.values() for d in c['derive'] if d['status'] == 'derived'),
             sum(len(c['derive']) for c in primary.values())))


if __name__ == '__main__':
    main()
