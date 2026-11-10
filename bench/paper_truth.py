#!/usr/bin/env python3
"""Score a ranked list or an outline of declarations against the paper ground truth.

Ground truth: out/corpus/papers/truth.json (built by out/corpus/papers/src/build_truth.py).  Each
numbered item of the Navier-Stokes and Euler papers is mapped to zero or more exported Lean
declarations, each mapping with a confidence (certain / probable / guess).

    python3 bench/paper_truth.py --test                      # self-test on a hand-made graph
    python3 bench/paper_truth.py --baselines                 # the three baselines; writes
                                                             #   out/corpus/papers/baselines.json, BASELINES.md
    python3 bench/paper_truth.py --ranking FILE --paper ns   # FILE: JSON list of names, or one name per line
    python3 bench/paper_truth.py --outline out/corpus/outline/outline.json --key ns_r3

Definitions
  item       one numbered paper result or key definition (truth.json "items").
  target     a declaration an item is mapped to.  --min-confidence drops weaker mappings; an item
             with no remaining mapping leaves the denominator.
  graph      edge A -> B when A's statement or proof uses B (typeDeps | valueDeps of the export).
  exact hit  at depth k: one of the item's targets is among the first k listed declarations.
  near hit   at depth k: exact, or a listed declaration is one dependency step from a target
             (it uses the target or the target uses it).  Near hits are easy to get by listing
             hubs, so every report carries a random-order reference at the same depth.
  depth      a prefix length of a ranked list; for an outline, the cumulative levels as well.
The scorer reports; it does not pass or fail anything.
"""
import argparse
import json
import os
import random
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRUTH = os.path.join(REPO, 'out', 'corpus', 'papers', 'truth.json')
DECLS = os.path.join(REPO, 'out', 'corpus', 'ns', 'decls.jsonl')
OUTLINE = os.path.join(REPO, 'out', 'corpus', 'outline', 'outline.json')
OUT = os.path.join(REPO, 'out', 'corpus', 'papers')
DEPTHS = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
ORDER = {'guess': 1, 'probable': 2, 'certain': 3}
ROOT = {'ns': 'NavierStokes', 'euler': 'Euler'}
SEED = 20261110
DRAWS = 200


# --------------------------------------------------------------------------- loading

def load_truth(path=TRUTH):
    with open(path) as f:
        return json.load(f)


def load_decls(path=DECLS):
    """name -> record (only the fields used here)."""
    D = {}
    with open(path) as f:
        for line in f:
            d = json.loads(line)
            D[d['name']] = dict(name=d['name'], module=d['module'], kind=d['kind'], doc=d['hasDocstring'],
                                mass=d['proofSize'] + d['auxProofSize'],
                                deps=sorted(set(d['typeDeps']) | set(d['valueDeps'])))
    return D


def neighbours(D):
    """name -> set of declarations one dependency step away, in either direction."""
    nb = {n: set(d['deps']) for n, d in D.items()}
    for n, d in D.items():
        for t in d['deps']:
            nb[t].add(n)
    return nb


def targets(truth, paper, min_conf='guess'):
    """item id -> set of target declarations, for one paper ('ns' / 'euler')."""
    out = {}
    for it in truth['items']:
        if it['paper'] != paper:
            continue
        t = {m['decl'] for m in it['mappings'] if ORDER[m['confidence']] >= ORDER[min_conf]}
        if t:
            out[it['id']] = t
    return out


# --------------------------------------------------------------------------- scoring

def first_ranks(ranked, tg, nb):
    """item id -> (first exact rank, first near rank), 1-based; None if never hit."""
    rank = {}
    for i, n in enumerate(ranked):
        rank.setdefault(n, i + 1)
    res = {}
    for item, ts in tg.items():
        ex = [rank[t] for t in ts if t in rank]
        near = list(ex)
        for t in ts:
            near.extend(rank[x] for x in nb.get(t, ()) if x in rank)
        res[item] = (min(ex) if ex else None, min(near) if near else None)
    return res


def score(ranked, tg, nb, depths=DEPTHS):
    """Hits at each depth.  Returns dict(listed, items, rows=[{depth, exact, near}], firstRanks)."""
    fr = first_ranks(ranked, tg, nb)
    rows = []
    for k in list(depths) + [len(ranked)]:
        if k > len(ranked) and rows and rows[-1]['depth'] == len(ranked):
            continue
        kk = min(k, len(ranked))
        if rows and rows[-1]['depth'] == kk:
            continue
        rows.append(dict(depth=kk,
                         exact=sum(1 for e, _ in fr.values() if e is not None and e <= kk),
                         near=sum(1 for _, n in fr.values() if n is not None and n <= kk)))
    return dict(listed=len(ranked), items=len(tg), rows=rows,
                firstRanks={i: dict(exact=e, near=n) for i, (e, n) in sorted(fr.items())})


def score_levels(levels, tg, nb):
    """levels: list of (label, [names]).  Cumulative hits after each level."""
    ranked, rows = [], []
    for label, names in levels:
        ranked.extend(n for n in names if n not in ranked)
        fr = first_ranks(ranked, tg, nb)
        rows.append(dict(level=label, depth=len(ranked),
                         exact=sum(1 for e, _ in fr.values() if e is not None),
                         near=sum(1 for _, n in fr.values() if n is not None)))
    return dict(listed=len(ranked), items=len(tg), rows=rows, ranked=ranked)


def random_reference(universe, tg, nb, depths, draws=DRAWS, seed=SEED):
    """Mean hits at each depth over seeded random orders of `universe` (the calibration row)."""
    rng = random.Random(seed)
    depths = [min(k, len(universe)) for k in depths]
    acc = [[0.0, 0.0] for _ in depths]
    pool = list(universe)
    for _ in range(draws):
        rng.shuffle(pool)
        fr = first_ranks(pool[:max(depths)], tg, nb)
        for j, k in enumerate(depths):
            acc[j][0] += sum(1 for e, _ in fr.values() if e is not None and e <= k)
            acc[j][1] += sum(1 for _, n in fr.values() if n is not None and n <= k)
    return dict(listed=len(pool), items=len(tg), draws=draws, seed=seed,
                rows=[dict(depth=k, exact=round(a / draws, 2), near=round(b / draws, 2))
                      for k, (a, b) in zip(depths, acc)])


# --------------------------------------------------------------------------- rankings

def reach_mass(D, names):
    """Proof mass of everything reachable from each declaration (itself included), exact.

    Reachable sets are kept as packed bit rows; `names` must be closed under dependencies.
    """
    import numpy as np
    names = list(names)
    ix = {n: i for i, n in enumerate(names)}
    N = len(names)
    bits = np.zeros((N, (N + 7) // 8), dtype=np.uint8)
    done = bytearray(N)
    for start in range(N):                      # iterative post-order over dependencies
        if done[start]:
            continue
        stack = [(start, 0)]
        while stack:
            i, j = stack.pop()
            deps = D[names[i]]['deps']
            while j < len(deps) and done[ix[deps[j]]]:
                j += 1
            if j < len(deps):
                stack.append((i, j + 1))
                stack.append((ix[deps[j]], 0))
                continue
            if not done[i]:
                if deps:
                    bits[i] = np.bitwise_or.reduce(bits[[ix[t] for t in deps]], axis=0)
                bits[i, i >> 3] |= 0x80 >> (i & 7)
                done[i] = 1
    mass = np.array([D[n]['mass'] for n in names], dtype=np.float64)
    out = np.zeros(N)
    for a in range(0, N, 64):                   # 64 rows at a time bounds the unpacked block
        out[a:a + 64] = np.unpackbits(bits[a:a + 64], axis=1, count=N).astype(np.float64) @ mass
    return {n: float(out[i]) for i, n in enumerate(names)}


def rank_by(values, names):
    return sorted(names, key=lambda n: (-values[n], n))


def outline_levels(outline):
    """Order an outline of bench/outline.py: root and spine, then chapters, sections, toolkit."""
    nodes = outline['nodes']
    def m(n):
        return -(n.get('sizes') or {}).get('dominatedMass', 0)
    lv = [('root + spine', [n['name'] for n in nodes if n['role'] in ('root', 'spine')]),
          ('level 1 (chapters)', [n['name'] for n in sorted((n for n in nodes if n['role'] == 'chapter'), key=m)])]
    for L in (2, 3):
        lv.append((f'level {L}', [n['name'] for n in sorted((n for n in nodes if n['role'] == 'section' and n.get('level') == L), key=m)]))
    lv.append(('toolkit', [n['name'] for n in nodes if n['role'] == 'toolkit']))
    return lv


def read_ranking(path):
    with open(path) as f:
        txt = f.read()
    try:
        x = json.loads(txt)
        return [e if isinstance(e, str) else e['name'] for e in x]
    except ValueError:
        return [l.strip() for l in txt.splitlines() if l.strip() and not l.startswith('#')]


# --------------------------------------------------------------------------- reports

def fmt_rows(rep, key='depth'):
    return ' | '.join(f"{r[key]}: {r['exact']}/{r['near']}" for r in rep['rows'])


def baselines():
    truth = load_truth()
    D = load_decls()
    nb = neighbours(D)
    with open(OUTLINE) as f:
        outlines = json.load(f)['outlines']
    result = dict(truth='out/corpus/papers/truth.json', depths=DEPTHS,
                  legend='each cell is exact/near hits among the items of that paper that have a mapping at the stated confidence or better',
                  papers={})
    md = ['# Paper ground truth: baseline scores', '',
          'Written by `python3 bench/paper_truth.py --baselines`. Each cell is **exact / near**: the number of paper items with a mapped declaration in the first k listed declarations, and the number with a mapped declaration in the first k or one dependency step from one of them. Random rows are means over %d seeded random orders (seed %d).' % (DRAWS, SEED), '']
    for paper, okeys in (('ns', ['ns_r3', 'ns_periodic']), ('euler', ['euler_compact', 'euler_r3'])):
        names = sorted(n for n, d in D.items() if d['module'].split('.')[0] == ROOT[paper])
        rm = reach_mass(D, names)
        own = {n: D[n]['mass'] for n in names}
        docs = [n for n in names if D[n]['doc']]
        rankings = {
            'largest proof beneath it (proof mass reachable through dependencies)': rank_by(rm, names),
            'own proof size': rank_by(own, names),
            'has a docstring, ordered by proof mass beneath': rank_by(rm, docs),
        }
        pres = dict(declarations=len(names), withDocstring=len(docs), variants={})
        all_items = [it for it in truth['items'] if it['paper'] == paper]
        md += [f'## {paper}: {len(all_items)} paper items, {len(names):,} declarations, {len(docs):,} with a docstring', '']
        for label, mc in (('all mapped items (any confidence)', 'guess'), ('items mapped at probable or certain', 'probable'), ('items mapped at certain', 'certain')):
            tg = targets(truth, paper, mc)
            v = dict(items=len(tg), outlines={}, rankings={}, sets={}, random={})
            md += [f'### {label}: {len(tg)} items', '', '| list | size | ' + ' | '.join(f'k={k}' for k in DEPTHS) + ' | all |', '|---|---|' + '---|' * (len(DEPTHS) + 1)]
            def row(name, rep):
                cells = {r['depth']: f"{r['exact']} / {r['near']}" for r in rep['rows']}
                last = rep['rows'][-1]
                md.append(f"| {name} | {rep['listed']:,} | " + ' | '.join(cells.get(k, '') for k in DEPTHS) + f" | {last['exact']} / {last['near']} |")
            for ok in okeys:
                lv = outline_levels(outlines[ok])
                rep = score_levels(lv, tg, nb)
                flat = score(rep['ranked'], tg, nb)
                v['outlines'][ok] = dict(levels=rep['rows'], prefix=flat['rows'], firstRanks=flat['firstRanks'])
                row(f'dominator outline `{ok}`', flat)
            for name, rk in rankings.items():
                rep = score(rk, tg, nb)
                v['rankings'][name] = dict(rows=rep['rows'], top20=rk[:20])
                row(name, rep)
            rr = random_reference(docs, tg, nb, DEPTHS)
            v['random']['has a docstring, random order'] = rr
            md.append('| has a docstring, random order (mean) | %s | ' % f'{len(docs):,}' + ' | '.join(f"{r['exact']} / {r['near']}" for r in rr['rows']) + ' | |')
            rr = random_reference(names, tg, nb, DEPTHS)
            v['random']['any declaration, random order'] = rr
            md.append('| any declaration, random order (mean) | %s | ' % f'{len(names):,}' + ' | '.join(f"{r['exact']} / {r['near']}" for r in rr['rows']) + ' | |')
            md.append('')
            md.append('Dominator outline by level (cumulative exact / near): ' + '; '.join(
                f"`{ok}`: " + ', '.join(f"{r['level']} ({r['depth']}) {r['exact']}/{r['near']}" for r in v['outlines'][ok]['levels']) for ok in okeys))
            md.append('')
            pres['variants'][mc] = v
        result['papers'][paper] = pres
    with open(os.path.join(OUT, 'baselines.json'), 'w') as f:
        json.dump(result, f, indent=1)
    with open(os.path.join(OUT, 'BASELINES.md'), 'w') as f:
        f.write('\n'.join(md) + '\n')
    print('\n'.join(md))


def selftest():
    D = {n: dict(name=n, module='NavierStokes.T', kind='theorem', doc=False, mass=m, deps=deps)
         for n, m, deps in [('top', 1, ['mid', 'side']), ('mid', 5, ['leaf', 'defn']), ('side', 2, ['defn']),
                            ('leaf', 7, []), ('defn', 3, []), ('lonely', 100, [])]}
    nb = neighbours(D)
    assert nb['defn'] == {'mid', 'side'} and nb['lonely'] == set()
    truth = dict(items=[
        dict(id='ns:A', paper='ns', mappings=[dict(decl='leaf', confidence='certain')]),
        dict(id='ns:B', paper='ns', mappings=[dict(decl='defn', confidence='guess')]),
        dict(id='ns:C', paper='ns', mappings=[dict(decl='lonely', confidence='probable')]),
        dict(id='ns:D', paper='ns', mappings=[]),
        dict(id='euler:A', paper='euler', mappings=[dict(decl='top', confidence='certain')])])
    tg = targets(truth, 'ns')
    assert set(tg) == {'ns:A', 'ns:B', 'ns:C'}
    assert set(targets(truth, 'ns', 'probable')) == {'ns:A', 'ns:C'}
    rep = score(['top', 'mid', 'leaf'], tg, nb, depths=[1, 2, 3])
    got = [(r['depth'], r['exact'], r['near']) for r in rep['rows']]
    # depth 1: nothing.  depth 2: mid is adjacent to leaf and defn -> 2 near.  depth 3: leaf exact.
    assert got == [(1, 0, 0), (2, 0, 2), (3, 1, 2)], got
    assert rep['firstRanks']['ns:C'] == dict(exact=None, near=None)
    lv = score_levels([('a', ['top']), ('b', ['side', 'lonely'])], tg, nb)
    assert [(r['depth'], r['exact'], r['near']) for r in lv['rows']] == [(1, 0, 0), (3, 1, 2)], lv['rows']
    rm = reach_mass(D, sorted(D))
    assert rm == dict(top=18.0, mid=15.0, side=5.0, leaf=7.0, defn=3.0, lonely=100.0), rm
    assert rank_by(rm, sorted(D))[:3] == ['lonely', 'top', 'mid']
    rr = random_reference(sorted(D), tg, nb, [6], draws=5)
    assert rr['rows'][0]['exact'] == 3 and rr['rows'][0]['near'] == 3
    print('paper_truth self-test: ok')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--test', action='store_true')
    ap.add_argument('--baselines', action='store_true')
    ap.add_argument('--ranking')
    ap.add_argument('--outline')
    ap.add_argument('--key', help='outline key in outline.json, e.g. ns_r3')
    ap.add_argument('--paper', choices=['ns', 'euler'])
    ap.add_argument('--min-confidence', default='guess', choices=['guess', 'probable', 'certain'])
    ap.add_argument('--json', action='store_true', help='print the full report as JSON')
    a = ap.parse_args()
    if a.test:
        return selftest()
    if a.baselines:
        return baselines()
    if not (a.ranking or a.outline):
        ap.error('one of --test, --baselines, --ranking, --outline')
    truth = load_truth()
    D = load_decls()
    nb = neighbours(D)
    if a.outline:
        with open(a.outline) as f:
            o = json.load(f)
        o = o['outlines'][a.key] if 'outlines' in o else o
        lv = outline_levels(o)
        paper = a.paper or ('euler' if any(n.startswith('Euler') for n in lv[0][1]) else 'ns')
        tg = targets(truth, paper, a.min_confidence)
        rep = score_levels(lv, tg, nb)
        flat = score(rep['ranked'], tg, nb)
        rep = dict(paper=paper, items=len(tg), levels=rep['rows'], prefix=flat['rows'], firstRanks=flat['firstRanks'])
    else:
        ranked = read_ranking(a.ranking)
        unknown = [n for n in ranked if n not in D]
        paper = a.paper or ('euler' if ranked and D.get(ranked[0], {}).get('module', '').startswith('Euler') else 'ns')
        tg = targets(truth, paper, a.min_confidence)
        rep = score(ranked, tg, nb)
        rep.update(paper=paper, unknownNames=len(unknown))
    if a.json:
        print(json.dumps(rep, indent=1))
    else:
        print(f"paper {rep['paper']}: {rep['items']} items with a mapping at {a.min_confidence} or better")
        for r in rep.get('levels', []):
            print(f"  after {r['level']:<20} {r['depth']:>6} listed: exact {r['exact']:>3}  near {r['near']:>3}")
        for r in rep.get('prefix', rep.get('rows', [])):
            print(f"  depth {r['depth']:>6}: exact {r['exact']:>3}  near {r['near']:>3}")
        if rep.get('unknownNames'):
            print(f"  {rep['unknownNames']} listed names are not in the export")


if __name__ == '__main__':
    main()
