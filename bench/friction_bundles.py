#!/usr/bin/env python3
"""Hypothesis-bundle mining for the friction census ("packet" test).

Input : out/corpus/friction/<corpus>/bundles/b.{thm,pkg}.jsonl  (corpora/friction/Bundles.lean, Expr level)
Output: out/corpus/friction/<corpus>/bundles/{mine.json, MINING.md}

  python3 -I bench/friction_bundles.py mine <ns|carleson> [minsup]

Definitions
  atom        a Prop-valued binder type split through top-level `and` (hypotheses), or a conjunct of
              the conclusion under `and` / `exists` (conclusions).
  subject     the telescope variables of kind term (or exists-bound) that occur in the atom's key, i.e.
              in explicit argument positions.
  V-bundle    (per variable, exact) a set of >= 2 atom keys about one variable v: keys are rewritten
              with v -> `$`, other term variables -> `_`, type variables -> `T`.  Mined exhaustively
              (Eclat) over the transactions {atoms about v} for every (theorem, v).
  G-bundle    (variable group, heuristic) a set of >= 2 atoms identified up to the binder NAMES of the
              variables involved (names are read from the environment); one transaction per theorem;
              grown greedily from every frequent atom by total saving.  Not exhaustive.
  saving      per instance: sum(atom tree size + 1) - (2 + 2*|parameters|), where parameters are all
              telescope variables occurring in the atoms (types and instances included): the atoms'
              binders are replaced by ONE binder whose type is `P x1 .. xn`.
              Same tree-size measure as statementSize.
  strict      every atom of the bundle is in a side-condition class; loose: at least one is.
"""
import json, re, sys, collections, os, itertools

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAM = json.load(open(os.path.join(REPO, 'bench/friction_families.json')))
HEADS = {h: t['class'] for t in FAM['type_heads'] for h in t['heads']}
SIDE = set(FAM['side_condition_classes'])
VAR = re.compile(r'§(\d+|x)')


def cls_of(a):
    if a['fin']:
        return 'finiteness'
    if a['pos']:
        return 'positivity'
    if a['so']:
        return 'mem'
    c = HEADS.get(a['hd'])
    if c:
        return c
    return 'tc' if a['tc'] else 'other'


def key_vars(k):
    return [int(x) for x in VAR.findall(k) if x != 'x']


def rekey(k, v, kinds):
    def f(m):
        if m.group(1) == 'x':
            return '?'
        j = int(m.group(1))
        if j == v:
            return '$'
        kd = kinds[j]
        return {'type': 'T', 'inst': 'I', 'hyp': 'H'}.get(kd, '_')
    return VAR.sub(f, k)


def namekey(k, names):
    return VAR.sub(lambda m: '?' if m.group(1) == 'x' else '‹' + names[int(m.group(1))] + '›', k)


def anon(k):
    return VAR.sub('_', k)


def load(corpus):
    d = os.path.join(REPO, 'out/corpus/friction', corpus, 'bundles')
    thms = [json.loads(l) for l in open(os.path.join(d, 'b.thm.jsonl'))]
    pkgs = [json.loads(l) for l in open(os.path.join(d, 'b.pkg.jsonl'))]
    return d, thms, pkgs


def var_items(rec, concl=False):
    """{v: {item: (size, mentions, cls, src)}} for hypotheses (concl=False) or conclusion atoms."""
    kinds = [b['k'] for b in rec['b']]
    out = collections.defaultdict(dict)
    for ai, a in enumerate(rec['a']):
        if (a['s'] < 0) != concl:
            continue
        if a['k'].startswith('BIG:'):
            continue
        c = cls_of(a)
        for v in set(key_vars(a['k'])):
            if kinds[v] in ('term', 'ex'):
                it = rekey(a['k'], v, kinds)
                out[v].setdefault(it, (a['sz'], a['m'], c, a['s'], ai))
    return out


def group_items(rec, concl=False):
    names = [b['n'] + ':' + b['th'] for b in rec['b']]
    out = {}
    for ai, a in enumerate(rec['a']):
        if (a['s'] < 0) != concl or a['k'].startswith('BIG:'):
            continue
        out.setdefault(namekey(a['k'], names), (a['sz'], a['m'], cls_of(a), a['s'], ai))
    return out


def saving(entries):
    params = set()
    for e in entries:
        params.update(e[1])
    return sum(e[0] + 1 for e in entries) - (2 + 2 * len(params))


def abbrev_only(entries):
    """saving if every atom were merely given its own name (no bundling): the part of `saving` that is
    abbreviation of large hypotheses rather than merging of hypotheses"""
    return sum(max(0, e[0] - (1 + 2 * len(e[1]))) for e in entries)


def eclat(tidsets, minsup, maxlen=12, cap=400000):
    """all itemsets of size >= 2 with support >= minsup; returns {frozenset: tidset}"""
    items = sorted((i for i, t in tidsets.items() if len(t) >= minsup), key=lambda i: len(tidsets[i]))
    res = {}
    def rec(prefix, ptids, cands):
        for n, (i, t) in enumerate(cands):
            if len(res) >= cap:
                return
            np_ = prefix + (i,)
            if len(np_) >= 2:
                res[frozenset(np_)] = t
            if len(np_) < maxlen:
                nxt = []
                for j, tj in cands[n + 1:]:
                    x = t & tj
                    if len(x) >= minsup:
                        nxt.append((j, x))
                if nxt:
                    rec(np_, t, nxt)
    rec((), None, [(i, tidsets[i]) for i in items])
    return res


def closed_only(res):
    """drop itemsets that have a strict superset with the same support"""
    by_sup = collections.defaultdict(list)
    for s, t in res.items():
        by_sup[len(t)].append(s)
    out = {}
    for sup, sets in by_sup.items():
        sets.sort(key=len, reverse=True)
        kept = []
        for s in sets:
            if not any(s < k and res[k] == res[s] for k in kept):
                kept.append(s)
        for s in kept:
            out[s] = res[s]
    return out


def greedy_grow(tidsets, trans, minsup, seeds):
    """grow each seed itemset by the item that most increases total saving; returns {frozenset: tids}"""
    out = {}
    def total(S, tids):
        return sum(saving([trans[t][i] for i in S]) for t in tids)
    for seed in seeds:
        S = frozenset(seed)
        tids = set.intersection(*[tidsets[i] for i in S])
        best = total(S, tids) if len(S) >= 2 else -1
        while True:
            cnt = collections.Counter()
            for t in tids:
                for i in trans[t]:
                    if i not in S:
                        cnt[i] += 1
            cand = None
            for i, c in cnt.most_common(40):
                if c < minsup:
                    break
                nt = tids & tidsets[i]
                sc = total(S | {i}, nt)
                if sc > best:
                    best, cand = sc, (i, nt)
            if cand is None:
                break
            S = S | {cand[0]}
            tids = cand[1]
        if len(S) >= 2:
            out[S] = tids
    return out


def describe(S, tids, trans, thm_of):
    S = sorted(S)
    ents = [[trans[t][i] for i in S] for t in tids]
    sav = [saving(e) for e in ents]
    abb = sum(abbrev_only(e) for e in ents)
    cl = [trans[next(iter(tids))][i][2] for i in S]
    hyp_red = sum(len({x[3] for x in e}) - 1 for e in ents)
    return {'items': S, 'classes': cl, 'instances': len(tids), 'theorems': len({thm_of(t) for t in tids}),
            'saved': sum(sav), 'abbrevOnly': abb, 'mergeOnly': sum(sav) - abb, 'savedMean': round(sum(sav) / len(sav), 1), 'hypsSaved': hyp_red,
            'strict': all(c in SIDE for c in cl), 'loose': any(c in SIDE for c in cl)}


def residual_top(cands, trans, thm_of, sizes, n=10, pred=lambda d: True):
    """greedy packing: repeatedly take the bundle with the largest saving over atoms not yet consumed
    (an atom of a theorem can be absorbed by one bundle only, whichever variable it was reached from)."""
    used = collections.defaultdict(set)   # theorem -> consumed atom indices
    pool = [(S, sorted(t)) for S, t in cands if pred(S)]
    chosen = []
    per_thm = collections.Counter()
    hyp_thm = collections.Counter()
    def live(S, tids):
        out = []
        seen = set()
        for t in tids:
            e = [trans[t][i] for i in S]
            ids = {x[4] for x in e}
            th = thm_of(t)
            if (used[th] & ids) or any((th, x) in seen for x in ids):
                continue
            for x in ids:
                seen.add((th, x))
            out.append((t, e, ids))
        return out
    for _ in range(n):
        best = None
        for S, tids in pool:
            lv = live(S, tids)
            tot = sum(saving(e) for _, e, _ in lv)
            if best is None or tot > best[0]:
                best = (tot, S, lv)
        if best is None or best[0] <= 0:
            break
        tot, S, lv = best
        hy = 0; ab = 0
        for t, e, ids in lv:
            used[thm_of(t)] |= ids
            per_thm[thm_of(t)] += saving(e)
            h = len({x[3] for x in e}) - 1
            hyp_thm[thm_of(t)] += h; hy += h; ab += abbrev_only(e)
        chosen.append({'items': sorted(S), 'residualSaved': tot, 'residualInstances': len(lv), 'residualHypsSaved': hy,
                       'residualAbbrevOnly': ab, 'theorems': len({thm_of(t) for t, _, _ in lv})})
    rel = sorted(per_thm[t] / sizes[t] for t in per_thm)
    summ = {'bundles': len(chosen), 'saved': sum(per_thm.values()), 'hypsSaved': sum(hyp_thm.values()),
            'abbrevOnly': sum(c['residualAbbrevOnly'] for c in chosen),
            'theoremsTouched': len(per_thm),
            'medianRelSavingTouched': round(rel[len(rel) // 2], 4) if rel else 0,
            'byCap': {str(cap): {'saved': sum(v for t, v in per_thm.items() if sizes[t] <= cap),
                                 'statementNodes': sum(x for x in sizes if x <= cap),
                                 'theorems': sum(1 for x in sizes if x <= cap)} for cap in (4000, 100000, 10 ** 15)}}
    return {'chosen': chosen, 'summary': summ}


def mine(corpus, minsup):
    d, thms, pkgs = load(corpus)
    total_size = sum(t['size'] for t in thms)
    n_hyp_binders = sum(1 for t in thms for b in t['b'][:t['nb']] if b['p'])
    n_hyp_atoms = sum(1 for t in thms for a in t['a'] if a['s'] >= 0)
    side_atoms = sum(1 for t in thms for a in t['a'] if a['s'] >= 0 and cls_of(a) in SIDE)
    side_nodes = sum(a['sz'] + 1 for t in thms for a in t['a'] if a['s'] >= 0 and cls_of(a) in SIDE)
    hyp_nodes = sum(a['sz'] + 1 for t in thms for a in t['a'] if a['s'] >= 0)

    # ---------- V-bundles
    trans = {}
    for ti, t in enumerate(thms):
        for v, items in var_items(t).items():
            if len(items) >= 2:
                trans[(ti, v)] = items
    tidsets = collections.defaultdict(set)
    for tid, items in trans.items():
        for i in items:
            tidsets[i].add(tid)
    res = eclat(tidsets, minsup)
    capped = len(res) >= 400000
    res = closed_only(res)
    thm_of = lambda tid: tid[0]
    vb = [describe(S, t, trans, thm_of) for S, t in res.items()]
    vb = [b for b in vb if b['loose'] and b['saved'] > 0]
    vb.sort(key=lambda b: -b['saved'])

    # conclusions: does the bundle travel through conclusions?
    ctrans = {}
    single = collections.Counter()
    for ti, t in enumerate(thms):
        ci = var_items(t, concl=True)
        nconc = sum(1 for a in t['a'] if a['s'] < 0)
        for v, items in ci.items():
            ctrans[(ti, v)] = set(items)
            if nconc == 1:
                for i in items:
                    single[i] += 1
    cidx = collections.defaultdict(set)
    for tid, items in ctrans.items():
        for i in items:
            cidx[i].add(tid)
    def produced(S):
        tids = set.intersection(*[cidx.get(i, set()) for i in S])
        return {'whole': len({t[0] for t in tids}),
                'anyItem': len({t[0] for i in S for t in cidx.get(i, ())}),
                'perItemSoleConclusion': [single.get(i, 0) for i in sorted(S)]}

    # packaging: structures / classes / conjunctive Prop defs whose atoms about one variable contain the bundle
    pidx = collections.defaultdict(set)
    pitems = []
    for pi, p in enumerate(pkgs):
        vi = var_items(p)
        if p['kind'] == 'def':
            for v, items in var_items(p, concl=True).items():
                vi.setdefault(v, {}).update(items)
        for v, items in vi.items():
            pid = len(pitems)
            pitems.append((pi, v, set(items)))
            for i in items:
                pidx[i].add(pid)
    def packaged(S):
        S = list(S)
        full = set.intersection(*[pidx.get(i, set()) for i in S])
        cnt = collections.Counter()
        for i in S:
            for pid in pidx.get(i, ()):
                cnt[pid] += 1
        part = [(c, pid) for pid, c in cnt.items() if c >= 2 and pid not in full]
        part.sort(reverse=True)
        nm = lambda pid: {'name': pkgs[pitems[pid][0]]['name'], 'kind': pkgs[pitems[pid][0]]['kind'],
                          'project': pkgs[pitems[pid][0]]['proj'], 'nAtoms': len(pitems[pid][2])}
        return {'full': [nm(p) for p in sorted(full)][:8], 'nFull': len(full),
                'partial': [dict(nm(p), matched=c) for c, p in part[:5]]}

    for b in vb[:60]:
        b['produced'] = produced(b['items'])
        b['packaged'] = packaged(b['items'])

    cands = [(frozenset(b['items']), res[frozenset(b['items'])]) for b in vb[:3000]]
    strict_set = {frozenset(b['items']) for b in vb if b['strict']}
    sizes = [t['size'] for t in thms]
    top_loose = residual_top(cands, trans, thm_of, sizes, 10)
    top_strict = residual_top(cands, trans, thm_of, sizes, 10, pred=lambda S: S in strict_set)
    top100 = residual_top(cands, trans, thm_of, sizes, 100)['summary']

    # ---------- G-bundles (name-keyed, per theorem)
    gtrans = {}
    for ti, t in enumerate(thms):
        gi = group_items(t)
        if len(gi) >= 2:
            gtrans[ti] = gi
    gtid = collections.defaultdict(set)
    for tid, items in gtrans.items():
        for i in items:
            gtid[i].add(tid)
    seeds = [(i,) for i, t in gtid.items() if len(t) >= minsup]
    gres = greedy_grow(gtid, gtrans, minsup, seeds)
    gthm = lambda tid: tid
    gb = [describe(S, t, gtrans, gthm) for S, t in gres.items()]
    gb = [b for b in gb if b['loose'] and b['saved'] > 0]
    gb.sort(key=lambda b: -b['saved'])
    gcon = {}
    for ti, t in enumerate(thms):
        gcon[ti] = set(group_items(t, concl=True))
    gcidx = collections.defaultdict(set)
    for tid, items in gcon.items():
        for i in items:
            gcidx[i].add(tid)
    # anonymous packaging match for G-bundles
    panon = []
    for p in pkgs:
        c = collections.Counter(anon(a['k']) for a in p['a'])
        panon.append(c)
    aidx = collections.defaultdict(set)
    for pi, c in enumerate(panon):
        for k in c:
            aidx[k].add(pi)
    def gpack(S):
        need = collections.Counter(anon(re.sub(r'‹[^›]*›', '§0', i)) for i in S)
        full = set.intersection(*[aidx.get(k, set()) for k in need])
        full = [pi for pi in full if all(panon[pi][k] >= n for k, n in need.items())]
        return {'nFull': len(full), 'full': [{'name': pkgs[pi]['name'], 'kind': pkgs[pi]['kind'], 'project': pkgs[pi]['proj'],
                                              'nAtoms': sum(panon[pi].values())} for pi in full[:8]]}
    for b in gb[:60]:
        S = b['items']
        b['produced'] = {'whole': len(set.intersection(*[gcidx.get(i, set()) for i in S])),
                         'anyItem': len(set().union(*[gcidx.get(i, set()) for i in S]))}
        b['packaged'] = gpack(S)
    gcands = [(frozenset(b['items']), gres[frozenset(b['items'])]) for b in gb[:3000]]
    gstrict = {frozenset(b['items']) for b in gb if b['strict']}
    gtop_loose = residual_top(gcands, gtrans, gthm, sizes, 10)
    gtop_strict = residual_top(gcands, gtrans, gthm, sizes, 10, pred=lambda S: S in gstrict)
    gtop100 = residual_top(gcands, gtrans, gthm, sizes, 100)['summary']
    # absolute ceiling: ALL side-condition hypothesis atoms of a theorem become one hypothesis
    ceil = {'hypsSaved': 0, 'byCap': {}}
    per = []
    for t in thms:
        side = [a for a in t['a'] if a['s'] >= 0 and cls_of(a) in SIDE]
        if len(side) >= 2:
            ceil['hypsSaved'] += len({a['s'] for a in side}) - 1
            per.append((t['size'], max(0, saving([(a['sz'], a['m']) for a in side]))))
    for cap in (4000, 100000, 10 ** 15):
        ceil['byCap'][str(cap)] = {'saved': sum(v for s_, v in per if s_ <= cap), 'statementNodes': sum(x for x in sizes if x <= cap)}
    ceil['theorems'] = len(per)

    # ---------- context: how much does the corpus already bundle?
    proj_structs = [p for p in pkgs if p['proj'] and p['kind'] in ('structure', 'class')]
    proj_structs_prop = [p for p in proj_structs if sum(1 for a in p['a']) >= 2]
    proj_defs = [p for p in pkgs if p['proj'] and p['kind'] == 'def']
    struct_heads = {p['name'] for p in pkgs if p['kind'] in ('structure', 'class', 'def') and p['proj']}
    hyp_struct = sum(1 for t in thms for a in t['a'] if a['s'] >= 0 and a['hd'] in struct_heads)
    term_struct = sum(1 for t in thms for b in t['b'][:t['nb']] if b['k'] == 'term' and b['th'] in struct_heads)
    n_term = sum(1 for t in thms for b in t['b'][:t['nb']] if b['k'] == 'term')

    out = {
        'corpus': corpus, 'minsup': minsup, 'theorems': len(thms), 'statementNodes': total_size,
        'hypBinders': n_hyp_binders, 'hypAtoms': n_hyp_atoms, 'sideAtoms': side_atoms,
        'hypNodes': hyp_nodes, 'sideNodes': side_nodes,
        'vTransactions': len(trans), 'vItemsetsClosed': len(res), 'vEclatCapped': capped, 'vBundlesLoose': len(vb),
        'vBundlesStrict': sum(1 for b in vb if b['strict']),
        'vTop': vb[:60], 'vTop10Loose': top_loose, 'vTop10Strict': top_strict, 'vTop100': top100, 'gTop100': gtop100, 'allSideCeiling': ceil,
        'gBundles': len(gb), 'gTop': gb[:60], 'gTop10Loose': gtop_loose, 'gTop10Strict': gtop_strict,
        'projectStructures': len(proj_structs), 'projectStructuresWith2PropAtoms': len(proj_structs_prop),
        'projectConjunctiveDefs': len(proj_defs),
        'hypAtomsHeadedByProjectBundle': hyp_struct, 'termBindersOfProjectStructureType': term_struct, 'termBinders': n_term,
    }
    json.dump(out, open(os.path.join(d, 'mine.json'), 'w'), indent=1, ensure_ascii=False)
    return out


def check_classes(corpus):
    """agreement of the Python class rule with the exporter's classes (whole Prop binders)"""
    d, thms, _ = load(corpus)
    hy = {}
    for l in open(os.path.join(REPO, 'out/corpus/friction', corpus, 'hyps.jsonl')):
        r = json.loads(l)
        hy[r['name']] = r
    agree = dis = 0; ex = []; size_dis = 0
    for t in thms:
        r = hy[t['name']]
        if r['statementSize'] != t['size']:
            size_dis += 1
        per = collections.defaultdict(list)
        for a in t['a']:
            per[a['s']].append(a)
        for b in r['binders']:
            if b['isProp'] and len(per[b['i']]) == 1:
                c = cls_of(per[b['i']][0])
                if c == b['cls']:
                    agree += 1
                else:
                    dis += 1
                    if len(ex) < 5:
                        ex.append((t['name'], b['i'], c, b['cls']))
    return {'agree': agree, 'disagree': dis, 'examples': ex, 'statementSizeDiffers': size_dis}


# ---------------------------------------------------------------- cluster selection for the experiment
FRAME_ITEMS = ('0 <= T', '0 < c', 'coercive', 'deriv')


def frame_atoms(t):
    """the four atoms of the frame bundle in theorem record t, or None.  Identified by Expr shape:
    hT : 0 <= T;  hc : 0 < c;  hQ : forall t x, c * |x|^2 <= |Q t x|^2;
    hd : forall t, HasDerivWithinAt (extendPath T hT Q) (Q1 t) (Icc 0 T) t   (same T, c, Q throughout)."""
    kinds = [b['k'] for b in t['b']]
    hyps = [a for a in t['a'] if a['s'] >= 0]
    for d in hyps:
        if d['hd'] != 'HasDerivWithinAt' or 'EulerVolterraConvolution.extendPath' not in d['k'] or d['pe'] != 'A':
            continue
        vs = key_vars(d['k'])
        terms = [v for v in dict.fromkeys(vs) if kinds[v] == 'term']
        hyp_refs = [v for v in dict.fromkeys(vs) if kinds[v] == 'hyp']
        if len(hyp_refs) != 1:
            continue
        hT = hyp_refs[0]
        aT = [a for a in hyps if a['s'] == hT and a['pos'] == 'le']
        if not aT:
            continue
        T = key_vars(aT[0]['k'])[0]
        for q in hyps:
            if q['pe'] != 'AA' or q['hd'] != 'LE.le' or 'Norm.norm' not in q['k']:
                continue
            qv = [v for v in dict.fromkeys(key_vars(q['k'])) if kinds[v] == 'term']
            # c, T, Q occur; Q must also occur in the derivative hypothesis
            cs = [v for v in qv if t['b'][v]['th'] == 'Real' and v != T]
            Qs = [v for v in qv if t['b'][v]['th'] == 'ContinuousMap' and v in terms]
            if len(cs) != 1 or len(Qs) != 1:
                continue
            c = cs[0]
            aC = [a for a in hyps if a['pos'] == 'lt' and key_vars(a['k']) == [c]]
            if not aC:
                continue
            return {'T': T, 'c': c, 'Q': Qs[0], 'hT': aT[0]['s'], 'hc': aC[0]['s'], 'hQ': q['s'], 'hd': d['s'],
                    'Q1': [v for v in terms if t['b'][v]['th'] == 'ContinuousMap' and v != Qs[0]]}
    return None


def cluster():
    """Rule (stated before looking at any proof): among the theorems carrying the whole frame bundle,
    take the dependency graph (an edge when one's proof uses the other, decls.jsonl valueDeps); rank
    modules by number of bundle-carrying theorems (ties: module name); in the first module whose
    bundle-carrying theorems contain a weakly connected component of >= 8 theorems, take that component."""
    d, thms, _ = load('ns')
    D = {}
    for l in open(os.path.join(REPO, 'out/corpus/ns/decls.jsonl')):
        r = json.loads(l)
        D[r['name']] = r
    car = {t['name']: (t, frame_atoms(t)) for t in thms}
    car = {n: v for n, v in car.items() if v[1]}
    bymod = collections.defaultdict(list)
    for n, (t, _) in car.items():
        bymod[t['module']].append(n)
    order = sorted(bymod, key=lambda m: (-len(bymod[m]), m))
    report = {'carriers': len(car), 'modules': [(m, len(bymod[m])) for m in order]}
    chosen = None
    for m in order:
        ns_ = set(bymod[m])
        adj = collections.defaultdict(set)
        for n in ns_:
            for x in D[n]['valueDeps']:
                if x in ns_ and x != n:
                    adj[n].add(x); adj[x].add(n)
        seen = set(); comps = []
        for n in sorted(ns_):
            if n in seen:
                continue
            comp = []; st = [n]; seen.add(n)
            while st:
                y = st.pop(); comp.append(y)
                for z in adj[y]:
                    if z not in seen:
                        seen.add(z); st.append(z)
            comps.append(sorted(comp))
        comps.sort(key=lambda c: (-len(c), c))
        report.setdefault('components', {})[m] = [len(c) for c in comps]
        if chosen is None and comps and len(comps[0]) >= 8:
            chosen = (m, comps[0])
    with open(os.path.join(REPO, 'out/corpus/friction/ns/bundles/frame_targets.txt'), 'w') as f:
        for n, (t, fr) in sorted(car.items()):
            f.write('%s %d,%d,%d,%d\n' % (n, fr['hT'], fr['hc'], fr['hQ'], fr['hd']))
    report['chosenModule'] = chosen[0] if chosen else None
    report['cluster'] = [{'name': n, 'line': D[n]['line'], 'endLine': D[n]['endLine'], 'statementSize': car[n][0]['size'],
                          'proofSize': D[n]['proofSize'], 'binders': car[n][0]['nb'],
                          'hyps': sum(1 for b in car[n][0]['b'][:car[n][0]['nb']] if b['k'] == 'hyp'),
                          'frame': car[n][1],
                          'depsInCluster': [x for x in D[n]['valueDeps'] if x in set(chosen[1])]}
                         for n in (chosen[1] if chosen else [])]
    json.dump(report, open(os.path.join(REPO, 'out/corpus/friction/ns/bundles/cluster.json'), 'w'), indent=1, ensure_ascii=False)
    return report


def partial_use():
    """How often the two large atoms of the frame bundle occur WITHOUT the rest (any variables)."""
    d, thms, _ = load('ns')
    ref = [t for t in thms if t['name'] == 'EulerFixedEndpointStrong.coordinateSlope_range'][0]
    fr = frame_atoms(ref)
    kQ = anon([a for a in ref['a'] if a['s'] == fr['hQ']][0]['k'])
    kD = anon([a for a in ref['a'] if a['s'] == fr['hd']][0]['k'])
    car = {t['name'] for t in thms if frame_atoms(t)}
    pat = collections.Counter()
    car_size = 0
    car_pred = 0
    for t in thms:
        ks = [anon(a['k']) for a in t['a'] if a['s'] >= 0]
        D = sum(k == kD for k in ks); Q = sum(k == kQ for k in ks)
        if D or Q:
            pat['deriv=%d coercive=%d carrier=%s' % (min(D, 2), min(Q, 2), t['name'] in car)] += 1
        if t['name'] in car:
            car_size += t['size']
            f = frame_atoms(t)
            ents = [(a['sz'], a['m']) for a in t['a'] if a['s'] in (f['hT'], f['hc'], f['hQ'], f['hd'])]
            car_pred += saving(ents)
    out = {'patterns': dict(sorted(pat.items())), 'carriers': len(car), 'carrierStatementNodes': car_size,
           'carrierPredictedSaving': car_pred,
           'bigHypAtomsExcludedFromMining': sum(1 for t in thms for a in t['a'] if a['s'] >= 0 and a['k'].startswith('BIG:'))}
    json.dump(out, open(os.path.join(d, 'frame_partial.json'), 'w'), indent=1)
    return out


def callsites():
    d = os.path.join(REPO, 'out/corpus/friction/ns/bundles')
    S = [json.loads(l) for l in open(os.path.join(d, 'frame_callsites.jsonl'))]
    car = {l.split()[0] for l in open(os.path.join(d, 'frame_targets.txt'))}
    pat = collections.Counter(' '.join(a['kind'] for a in s['args']) for s in S)
    heads = collections.Counter()
    for s in S:
        for nm, a in zip(['hT', 'hc', 'hQ', 'hd'], s['args']):
            if a['kind'] == 'built':
                heads[nm + ' <- ' + a['head']] += 1
    out = {'sites': len(S), 'callers': len({s['caller'] for s in S}), 'targetsCalled': len({s['target'] for s in S}),
           'targets': len(car), 'callerIsCarrier': sum(1 for s in S if s['caller'] in car),
           'patterns(hT hc hQ hd)': dict(pat.most_common()), 'builtFrom': dict(heads.most_common())}
    json.dump(out, open(os.path.join(d, 'frame_callsites_summary.json'), 'w'), indent=1)
    return out


def short(k, n=110):
    return k if len(k) <= n else k[:n] + ' …'


def tables(corpus):
    d = os.path.join(REPO, 'out/corpus/friction', corpus, 'bundles')
    m = json.load(open(os.path.join(d, 'mine.json')))
    L = ['# Bundle mining: %s' % corpus, '',
         'Generated by `bench/friction_bundles.py tables %s` from `mine.json` (minimum support %d). Definitions: docstring of the script and `../../BUNDLES.md`.' % (corpus, m['minsup']), '']
    def block(title, key):
        L.append('## ' + title); L.append('')
        for n, b in enumerate(m[key][:25], 1):
            pk = b['packaged']
            L.append('**%d.** %d instances in %d theorems; saving %d nodes (%.0f per instance; %d of it from merely naming each atom, %d from merging); %d hypotheses removed; %s.' % (
                n, b['instances'], b['theorems'], b['saved'], b['savedMean'], b['abbrevOnly'], b['mergeOnly'], b['hypsSaved'],
                'all atoms side-condition' if b['strict'] else 'mixed classes'))
            L.append('Produced: whole bundle in the conclusion of %d theorems; some atom of it in %d. Already packaged by %d structures/definitions%s.' % (
                b['produced']['whole'], b['produced']['anyItem'], pk['nFull'],
                (': ' + ', '.join('`%s`' % x['name'] for x in pk['full'][:4])) if pk['full'] else ''))
            L.append('')
            for it, c in zip(b['items'], b['classes']):
                L.append('- %s: `%s`' % (c, short(it)))
            L.append('')
    block('Per-variable bundles (exact, closed itemsets), by total saving', 'vTop')
    block('Variable-group bundles (heuristic, name-keyed), by total saving', 'gTop')
    open(os.path.join(d, 'MINING.md'), 'w').write('\n'.join(L) + '\n')


def packet():
    """tabulate out/corpus/friction/ns/bundles/packet_measure.jsonl (written by corpora/friction/packet/PacketMeasure.lean)"""
    d = os.path.join(REPO, 'out/corpus/friction/ns/bundles')
    R = [json.loads(l) for l in open(os.path.join(d, 'packet_measure.jsonl'))]
    by = collections.defaultdict(dict)
    for r in R:
        by[r['name'].split('.')[-1]][r['group']] = r
    order = [r['name'] for r in R if r['group'] == 'backcheck']
    rows = []
    tot = collections.Counter()
    for n in order:
        g = by[n]
        row = {'name': n}
        for grp in ('orig', 'wrap', 'api'):
            for k in ('statementTree', 'statementDag', 'hyps', 'binders', 'explicit'):
                row['%s.%s' % (grp, k)] = g[grp][k]
        for grp in ('orig', 'direct', 'wrap', 'back', 'api'):
            row['%s.valueDag' % grp] = g[grp]['valueDag']
            row['%s.bodyDag' % grp] = g[grp]['bodyDag']
        row['sameStatementBack'] = g['backcheck']['sameStatement']
        row['directUsesOriginalCluster'] = g['direct']['usesOriginalCluster']
        rows.append(row)
        for k, v in row.items():
            if isinstance(v, int) and not isinstance(v, bool):
                tot[k] += v
    glue = [r for r in R if r['group'] == 'glue']
    struct = [r for r in R if r['group'] == 'struct']
    axioms = sorted({a for r in R for a in r.get('axioms', [])})
    out = {'rows': rows, 'totals': dict(tot), 'axioms': axioms,
           'glueDefs': len(glue), 'glueStatementTree': sum(r['statementTree'] for r in glue),
           'glueValueDag': sum(r.get('valueDag', 0) for r in glue),
           'structDeclsStatementTree': sum(r['statementTree'] for r in struct),
           'allBackStatementsIdentical': all(r['sameStatementBack'] for r in rows)}
    json.dump(out, open(os.path.join(d, 'packet_summary.json'), 'w'), indent=1)
    L = ['| theorem | statement nodes: original / packet / packet + API | hypotheses | explicit arguments | proof value: original / direct | proof body: original / direct |', '|---|---|---|---|---|---|']
    for r in rows:
        L.append('| `%s` | %d / %d / %d | %d → %d | %d → %d | %d / %d | %d / %d |' % (
            r['name'], r['orig.statementTree'], r['wrap.statementTree'], r['api.statementTree'], r['orig.hyps'], r['wrap.hyps'],
            r['orig.explicit'], r['wrap.explicit'], r['orig.valueDag'], r['direct.valueDag'], r['orig.bodyDag'], r['direct.bodyDag']))
    t = tot
    L.append('| **total** | %d / %d / %d | %d → %d | %d → %d | %d / %d | %d / %d |' % (
        t['orig.statementTree'], t['wrap.statementTree'], t['api.statementTree'], t['orig.hyps'], t['wrap.hyps'],
        t['orig.explicit'], t['wrap.explicit'], t['orig.valueDag'], t['direct.valueDag'], t['orig.bodyDag'], t['direct.bodyDag']))
    open(os.path.join(d, 'packet_table.md'), 'w').write('\n'.join(L) + '\n')
    return out


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'mine':
        corpus = sys.argv[2]
        minsup = int(sys.argv[3]) if len(sys.argv) > 3 else (20 if corpus == 'ns' else 5)
        o = mine(corpus, minsup)
        print(json.dumps({k: v for k, v in o.items() if not isinstance(v, (list, dict))}, indent=1))
    elif cmd == 'check':
        print(json.dumps(check_classes(sys.argv[2]), indent=1))
    elif cmd == 'cluster':
        r = cluster()
        print(json.dumps({k: v for k, v in r.items() if k != 'cluster'}))
        for c in r['cluster']:
            print(c['name'], c['line'], c['endLine'], c['statementSize'], c['proofSize'], c['binders'], c['hyps'], c['depsInCluster'])
    elif cmd == 'partial':
        print(json.dumps(partial_use(), indent=1))
    elif cmd == 'callsites':
        print(json.dumps(callsites(), indent=1))
    elif cmd == 'tables':
        tables(sys.argv[2])
    elif cmd == 'packet':
        o = packet()
        print(json.dumps({k: v for k, v in o.items() if k != 'rows'}, indent=1))
