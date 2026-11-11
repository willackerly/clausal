#!/usr/bin/env python3
"""M7 stage 1 (candidates by rule).  usage: stage1.py <project> [extra-project-records.jsonl]

Reads out/reinvent/<project>/raw/defs.jsonl (skeletons from Export.lean) and writes
out/reinvent/<project>/candidates.jsonl and stage1.json (the funnel counts).

Rule S (shape).  A library notion L gives one PATTERN per body: its definition body, the conjunction of its
  fields if it is a structure, and the right-hand side of every library theorem `L xs <-> R` / `L xs = R`
  whose value arguments are distinct variables.  The pattern's variables are L's parameters.  A project
  definition D (body after unfolding project-local reducible definitions; second attempt after unfolding
  project-local definitions one further level) is a candidate for L when the pattern matches the body by
  second-order pattern matching (Miller patterns: a parameter applied to distinct bound variables may be
  bound to a lambda; other applied parameters are checked after the fact), up to: bound-variable names;
  erased arguments (types, instances, proofs); order of conjuncts; and two approximate rules, each recorded:
    extra    the project body has conjuncts the pattern lacks (D is at least as strong);
    absorbed a norm or absolute value in the pattern has no counterpart in the project body (gives the
             side condition `0 <= t`; whether that condition can hold is not checked).
  Kept when the pattern has rigid weight >= MINW (constants, literals and binders; variables count 0), the
  pattern's weight is >= MINCOV of the project body's, and the extra conjuncts weigh <= MAXEXTRA of it.
Rule W (thin wrapper).  D is a `def`/`abbrev` whose body (same unfolding) has at most MAXWRAP nodes and
  mentions library constants only.  `alias`: the body is one library constant applied to D's parameters
  (any order, each at most once); otherwise `composite`.
"""
import collections
import json
import os
import signal
import sys
import time

from skel import (parse, rigidify, first_match, sig, sig_variants, term_key, term_key_variants, weight, size,
                  consts, instantiate, to_lean, Unprintable, is_const, lean_name, prune_forall, BUDGET_HITS, show)

MINW = 3
MINCOV = 0.4
MAXEXTRA = 0.34
MAXWRAP = 15
TOPK = 3
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

# heads that are logic / arithmetic glue: never reported as "the library notion" of an alias
GLUE = set('''Eq Ne And Or Not Iff Exists True False HEq id Function.comp LE.le LT.lt GE.ge GT.gt HAdd.hAdd HMul.hMul
HSub.hSub HDiv.hDiv HPow.hPow HSMul.hSMul Neg.neg Inv.inv OfNat.ofNat Membership.mem DFunLike.coe Subtype.val
Prod.fst Prod.snd Prod.mk Nat.cast Int.cast NatCast.natCast IntCast.intCast HMod.hMod Max.max Min.min
Subtype Prod Sum Set Finset Nat Real Int Complex ENNReal NNReal Fin Option List Function.const Singleton.singleton
Exists.choose Classical.choose Classical.choice Nat.find Subtype.mk Insert.insert SDiff.sdiff Union.union Inter.inter HasSubset.Subset ite dite Nat.succ Zero.zero One.one
setOf Set.univ Set.Icc Set.Ioo Set.Ico Set.Ioc Set.Ici Set.Iic Set.Ioi Set.Iio Finset.range Finset.sum Finset.prod
Finset.univ Set.image Set.preimage Sigma PSigma Quotient HAppend.hAppend Bool Unit PUnit Empty'''.split())


class KeyTimeout(Exception):
    pass


def _alarm(*a):
    raise KeyTimeout()


signal.signal(signal.SIGALRM, _alarm)


def load(project, extra):
    recs = []
    for path in [os.path.join(REPO, 'out/reinvent', project, 'raw/defs.jsonl')] + extra:
        with open(path) as f:
            for line in f:
                recs.append(json.loads(line))
    return recs


def proj_names(project):
    names = set()
    p = os.path.join(REPO, 'out/corpus', project, 'decls.jsonl')
    with open(p) as f:
        for line in f:
            i = line.find('"name":"')
            j = line.find('"', i + 8)
            names.add(line[i + 8:j])
    return names


def main():
    project = sys.argv[1]
    extra = sys.argv[2:]
    out = os.path.join(REPO, 'out/reinvent', project if not extra else 'planted')
    os.makedirs(out, exist_ok=True)
    recs = load(project, extra)
    pnames = proj_names(project) | {r['name'] for r in recs if r['proj']}
    if extra:
        recs = [r for r in recs if not r['proj'] or r['module'].startswith('ReinventPlanted')]

    def is_proj_const(c):
        return c in pnames or c.rsplit('.', 1)[0] in pnames

    # ---------------- library patterns
    t0 = time.time()
    pats = []          # (L, src, tree, record)
    idx = collections.defaultdict(list)
    npat = collections.Counter()
    for r in recs:
        if r['proj'] or r.get('rec'):
            continue
        try:
            lean_name(r['name'])
        except Unprintable:
            continue
        try:
            t = parse(r['body'])
        except Exception:
            continue
        wt = weight(t)
        if wt < MINW:
            continue
        if r['kind'] == 'char' and r['name'] in consts(t):
            continue
        key = ('P:' + sig(t, True)) if r['isProp'] else None
        if key is None:
            k = term_key(t, True)
            if k is None:
                continue
            key = 'a:' + k[0] + '(' + ','.join(k[1]) + ')'
        elif key in ('P:?', 'P:', 'P:§', 'P:app'):
            continue
        i = len(pats)
        pats.append((r['name'], r['kind'] if r['kind'] != 'char' else 'char:' + r['thm'], t, r, wt))
        idx[key].append(i)
        npat['prop' if r['isProp'] else 'term'] += 1
    print('patterns', dict(npat), 'keys', len(idx), '%.0fs' % (time.time() - t0), file=sys.stderr)

    # ---------------- project subjects
    subjects = [r for r in recs if r['proj'] and r['kind'] != 'char']
    n_all = len(subjects)
    # syntax, macros and other metaprogramming definitions are not mathematical notions
    subjects = [r for r in subjects if 'Lean.' not in r.get('pp', '') and 'ParserDescr' not in r.get('pp', '')]
    if os.environ.get('RV_LIMIT'):
        subjects = subjects[:int(os.environ['RV_LIMIT'])]
    funnel = collections.OrderedDict()
    funnel['project definitions and structures in the environment'] = n_all
    funnel['  after removing syntax and metaprogramming definitions (type mentions `Lean.`)'] = len(subjects)
    funnel['  of which Prop-valued'] = sum(1 for r in subjects if r['isProp'])
    cands = []
    n_shape_D = set()
    n_keyhit = set()
    n_match_raw = 0
    n_unprintable = 0
    wrappers = collections.Counter()
    too_big = set()
    t0 = time.time()
    for si, r in enumerate(subjects):
        if si % 1000 == 0:
            print('subject', si, '%.0fs' % (time.time() - t0), file=sys.stderr, flush=True)
        D = r['name']
        try:
            lean_name(D)
        except Unprintable:
            continue
        ts = time.time()
        levels = [(0, r['body'])]
        if 'body1' in r:
            levels.append((1, r['body1']))
        per_L = {}
        for lvl, b in levels:
            try:
                s = rigidify(parse(b))
            except Exception:
                continue
            ws = weight(s)
            if ws < MINW and r['kind'] in ('def', 'abbrev', 'irreducible_def') and lvl == 0:
                pass
            signal.setitimer(signal.ITIMER_REAL, 2.0)
            try:
                keys = ['P:' + k for k in sig_variants(s)] if r['isProp'] else term_key_variants(s)
                signal.setitimer(signal.ITIMER_REAL, 0)
            except KeyTimeout:
                too_big.add(D)
                continue
            seen = set()
            pl = []
            for k in keys:
                for i in idx.get(k, ()):
                    if i not in seen:
                        seen.add(i)
                        pl.append(i)
            if pl:
                n_keyhit.add(D)
            for i in pl[:400]:
                L, src, p, lr, wp = pats[i]
                if ws == 0 or wp / ws < MINCOV:
                    continue
                st = first_match(p, s, True)
                if st is None:
                    continue
                wex = sum(weight(e[1]) for e in st.extras)
                if wex > MAXEXTRA * ws:
                    continue
                n_match_raw += 1
                # arguments of L
                args = []
                ok = True
                order = lr['argmap'] if lr['kind'] == 'char' else list(range(len(lr['pk'])))
                for j in order:
                    if j < 0 or lr['pk'][j] in ('i', 'h'):
                        args.append('*')
                        continue
                    a = instantiate('$%d' % j, st.bind)
                    if a is None:
                        if lr['pk'][j] == 't':
                            args.append('*')
                            continue
                        ok = False
                        break
                    args.append(a)
                if not ok:
                    continue
                rhs = (('p' if r['isProp'] else 'a'), L) + tuple(args)
                sides = []
                for (ctx, wrapped, inner) in st.absorbed:
                    if wrapped[1] in ('Norm.norm', 'abs'):
                        c = ('p', 'LE.le', '*', '*', ('a', 'OfNat.ofNat', '*', '%0', '*'), inner)
                    else:
                        c = ('p', 'Eq', '*', wrapped, inner)
                    sides.append(prune_forall(ctx, c))
                try:
                    rhs_s = to_lean(rhs)
                    sides_s = [to_lean(c) for c in sides]
                except Unprintable:
                    n_unprintable += 1
                    continue
                atomic = all(isinstance(a, str) for a in args)
                cls = 'same shape' if atomic and not st.extras and not st.absorbed else \
                      ('instance' if not st.extras and not st.absorbed else 'approximate')
                score = (len(st.absorbed) + wex, 0 if atomic else 1, lvl, -wp)
                c = dict(D=D, Dkind=r['kind'], isProp=r['isProp'], level=lvl, L=L, Lsrc=src, rule='shape',
                         cls=cls, extras=len(st.extras), absorbed=len(st.absorbed), cov=round(wp / ws, 2),
                         wpat=wp, rhs=rhs_s, rhs_skel=show(rhs), sides=sides_s, np=len(r['pk']),
                         unfold=[D] + (r.get('unf', []) if lvl else []) if r['kind'] not in ('structure', 'class') else
                         (r.get('unf', []) if lvl else []),
                         rw=[src[5:]] if src.startswith('char:') else [L], module=r['module'], pp=r.get('pp', ''))
                c['_score'] = score
                if L not in per_L or score < per_L[L]['_score']:
                    per_L[L] = c
        if time.time() - ts > 3:
            print('slow', D, '%.0fs' % (time.time() - ts), r['nodes'], r.get('nodes1'), len(pl), file=sys.stderr, flush=True)
        best = sorted(per_L.values(), key=lambda c: c['_score'])[:TOPK]
        if best:
            n_shape_D.add(D)
        for c in best:
            del c['_score']
            cands.append(c)
        # ---------------- rule W
        if r['kind'] in ('def', 'abbrev', 'irreducible_def') and not r.get('rec'):
            try:
                s = rigidify(parse(r['body']))
            except Exception:
                continue
            cs = consts(s)
            if size(s) <= MAXWRAP and cs and not any(is_proj_const(c) for c in cs):
                alias = isinstance(s, tuple) and s[0] in ('p', 'a') and isinstance(s[1], str) and is_const(s[1]) \
                    and all(isinstance(a, str) and a[0] in '§*' for a in s[2:]) \
                    and len([a for a in s[2:] if a != '*']) == len({a for a in s[2:] if a != '*'}) \
                    and s[1] not in GLUE
                if not alias and isinstance(s, str) and is_const(s) and s not in GLUE:
                    alias = True
                wrappers['alias' if alias else 'composite'] += 1
                if alias:
                    try:
                        rhs_s = to_lean(s)
                    except Unprintable:
                        n_unprintable += 1
                        continue
                    L = s if isinstance(s, str) else s[1]
                    if not any(c['L'] == L and c['D'] == D for c in best):
                        cands.append(dict(D=D, Dkind=r['kind'], isProp=r['isProp'], level=0, L=L, Lsrc='body',
                                          rule='wrapper', cls='alias', extras=0, absorbed=0, cov=1.0, wpat=1,
                                          rhs=rhs_s, rhs_skel=show(s), sides=[], np=len(r['pk']), unfold=[D], rw=[],
                                          module=r['module'], pp=r.get('pp', '')))
                    else:
                        for c in best:
                            if c['L'] == L:
                                c['rule'] = 'shape+wrapper'
    print('matching %.0fs' % (time.time() - t0), file=sys.stderr)
    funnel_budget = BUDGET_HITS[0]
    for i, c in enumerate(cands):
        c['id'] = 'c%05d' % i
    funnel['rule S: definitions skipped, index keys not enumerated within 2 s (bodies with many conjuncts)'] = len(too_big)
    funnel['rule S: definitions whose index key meets a library pattern key'] = len(n_keyhit)
    funnel['rule S: pattern matches found (before keeping the best per library notion)'] = n_match_raw
    funnel['rule S: definitions with at least one shape candidate'] = len(n_shape_D)
    funnel['rule S: candidate pairs kept (best %d library notions per definition)' % TOPK] = \
        sum(1 for c in cands if c['rule'].startswith('shape'))
    funnel['  same shape / instance / approximate'] = ' / '.join(
        str(sum(1 for c in cands if c['rule'].startswith('shape') and c['cls'] == k))
        for k in ('same shape', 'instance', 'approximate'))
    funnel['rule W: thin wrappers (alias / composite)'] = '%d / %d' % (wrappers['alias'], wrappers['composite'])
    funnel['rule W: alias pairs added (not already a shape pair)'] = sum(1 for c in cands if c['rule'] == 'wrapper')
    funnel['candidate pairs dropped because a name cannot be written back as Lean source'] = n_unprintable
    funnel['pattern matches abandoned at the search budget (20,000 steps)'] = funnel_budget
    funnel['candidate pairs passed to stage 2'] = len(cands)
    funnel['distinct project definitions among them'] = len({c['D'] for c in cands})
    with open(os.path.join(out, 'candidates.jsonl'), 'w') as f:
        for c in cands:
            f.write(json.dumps(c, ensure_ascii=False) + '\n')
    with open(os.path.join(out, 'stage1.json'), 'w') as f:
        json.dump(dict(project=project, funnel=funnel, params=dict(MINW=MINW, MINCOV=MINCOV, MAXEXTRA=MAXEXTRA, MAXWRAP=MAXWRAP,
                                                                   TOPK=TOPK),
                       library_patterns=dict(npat)), f, indent=1, ensure_ascii=False)
    for k, v in funnel.items():
        print('%-90s %s' % (k, v))


if __name__ == '__main__':
    main()
