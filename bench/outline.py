#!/usr/bin/env python3
"""Dominator-tree outline of a Lean project's declaration graph.

Input : out/corpus/<corpus>/decls.jsonl (exported from the Lean environment) and main_theorems.json.
Output: out/corpus/outline/{dominators_<key>.jsonl, shape.json, relaxations.json, outline.json, OUTLINE.md}

    python3 bench/outline.py            # everything, about 1-2 minutes
    python3 bench/outline.py --test     # unit tests of the dominator algorithm only

Definitions used throughout
  graph     node = exported declaration; edge A -> B when A's statement or proof uses B
            (typeDeps | valueDeps).
  mass      proofSize + auxProofSize of a declaration (distinct subterms of its value, plus those of
            the auxiliaries folded into it).  For a definition this is the size of its body.
  dom(d)    the set of nodes all of whose dependency paths from the root pass through d (d included).
  spine     the chain root -> c1 -> c2 ... where each ci is the heaviest dominator-tree child of the
            previous one and carries at least 90% of its mass.  The last spine node is the "hub".
  chapter   a dominator-tree child of the hub that dominates at least MIN_CHAPTER declarations.
No LLM and no source regex is involved; ratings in OUTLINE.md come from ratings.json (hand-written).
"""
import collections
import heapq
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(REPO, 'out', 'corpus', 'ns')
OUT = os.path.join(REPO, 'out', 'corpus', 'outline')
KEYS = {
    'NavierStokes.Comparator.navier_stokes_breakdown_R3': 'ns_r3',
    'NavierStokes.Comparator.navier_stokes_breakdown_periodic': 'ns_periodic',
    'Euler.euler_breakdown_R3': 'euler_r3',
    'Euler.exists_compact_smooth_euler_singularity': 'euler_compact',
}
PRIMARY = ['ns_r3', 'euler_r3']          # printed in full; the other two share almost everything
MIN_CHAPTER = 20                         # declarations dominated, for a node to count as a chapter
SPINE_SHARE = 0.9
BUDGET = 40                              # statements per outline
MAX_LEVEL = 3
TRIM = 420                               # characters of a statement shown in OUTLINE.md


# --------------------------------------------------------------------------- dominators

def reverse_postorder(succ, root):
    """Reverse postorder of the nodes reachable from root (iterative DFS)."""
    seen = {root}
    post = []
    stack = [(root, iter(succ.get(root, ())))]
    while stack:
        node, it = stack[-1]
        for nxt in it:
            if nxt not in seen:
                seen.add(nxt)
                stack.append((nxt, iter(succ.get(nxt, ()))))
                break
        else:
            post.append(node)
            stack.pop()
    post.reverse()
    return post


def immediate_dominators(succ, root):
    """Cooper-Harvey-Kennedy iterative algorithm.  succ: node -> iterable of successors.
    Returns {node: idom} for every node reachable from root, with idom[root] == root."""
    rpo = reverse_postorder(succ, root)
    num = {n: i for i, n in enumerate(rpo)}
    preds = [[] for _ in rpo]
    for n in rpo:
        i = num[n]
        for s in succ.get(n, ()):
            preds[num[s]].append(i)
    idom = [-1] * len(rpo)
    idom[0] = 0
    changed = True
    while changed:
        changed = False
        for i in range(1, len(rpo)):
            new = -1
            for p in preds[i]:
                if idom[p] == -1:
                    continue
                if new == -1:
                    new = p
                    continue
                a, b = p, new
                while a != b:
                    while a > b:
                        a = idom[a]
                    while b > a:
                        b = idom[b]
                new = a
            if new != idom[i]:
                idom[i] = new
                changed = True
    return {rpo[i]: rpo[idom[i]] for i in range(len(rpo))}


def dominated_by_definition(succ, root):
    """Brute force for tests: d dominates n iff n is unreachable from root once d is removed."""
    reach = reverse_postorder(succ, root)
    dom = {n: {n, root} for n in reach}
    for d in reach:
        if d == root:
            continue
        cut = {k: [s for s in v if s != d] for k, v in succ.items() if k != d}
        still = set(reverse_postorder(cut, root))
        for n in reach:
            if n not in still:
                dom[n].add(d)
    return dom


def run_tests():
    # Hand-made example.  r uses a and b; a and b both use c (so c hangs off r, not a or b);
    # a alone uses d; d uses e and f; e and f use g (so g hangs off d); b uses h; h uses c.
    succ = {'r': ['a', 'b'], 'a': ['c', 'd'], 'b': ['c', 'h'], 'd': ['e', 'f'],
            'e': ['g'], 'f': ['g'], 'h': ['c'], 'c': [], 'g': [], 'unreached': ['a']}
    want = {'r': 'r', 'a': 'r', 'b': 'r', 'c': 'r', 'd': 'a', 'e': 'd', 'f': 'd', 'g': 'd', 'h': 'b'}
    got = immediate_dominators(succ, 'r')
    assert got == want, got
    # A chain and a diamond below it: every node of the chain dominates the diamond.
    succ2 = {0: [1], 1: [2], 2: [3, 4], 3: [5], 4: [5], 5: [6], 6: []}
    assert immediate_dominators(succ2, 0) == {0: 0, 1: 0, 2: 1, 3: 2, 4: 2, 5: 2, 6: 5}
    # Random DAGs against the definition (and against networkx when it is installed).
    import random
    rng = random.Random(7)
    try:
        import networkx as nx
    except ImportError:
        nx = None
    for trial in range(300):
        n = rng.randint(2, 40)
        succ3 = {i: [j for j in range(i + 1, n) if rng.random() < rng.choice([0.05, 0.15, 0.4])]
                 for i in range(n)}
        idom = immediate_dominators(succ3, 0)
        dom = dominated_by_definition(succ3, 0)
        for node, parent in idom.items():
            chain, x = {node}, node
            while x != 0:
                x = idom[x]
                chain.add(x)
            assert chain == dom[node], (trial, node, chain, dom[node])
        if nx is not None:
            g = nx.DiGraph()
            g.add_node(0)
            g.add_edges_from((a, b) for a, bs in succ3.items() for b in bs)
            ref = dict(nx.immediate_dominators(g, 0))
            ref[0] = 0          # networkx >= 3.6 omits the root, older versions map it to itself
            assert ref == idom, trial
    print('dominator tests passed: 2 hand-made graphs, 300 random DAGs checked against the definition'
          + (' and networkx' if nx is not None else ''))


# --------------------------------------------------------------------------- data

class Corpus:
    def __init__(self, path):
        self.decl = {}
        with open(os.path.join(path, 'decls.jsonl')) as fh:
            for line in fh:
                d = json.loads(line)
                self.decl[d['name']] = d
        self.succ = {n: sorted(set(d['typeDeps']) | set(d['valueDeps'])) for n, d in self.decl.items()}
        with open(os.path.join(path, 'main_theorems.json')) as fh:
            self.roots = json.load(fh)['mainTheorems']

    def own(self, n):
        d = self.decl[n]
        return d['proofSize'] + d['auxProofSize']


class DomTree:
    """Dominator tree from one root, with rolled-up mass and counts."""

    def __init__(self, succ, root, own):
        self.root = root
        self.succ = succ
        self.idom = immediate_dominators(succ, root)
        self.children = collections.defaultdict(list)
        for n, p in self.idom.items():
            if n != p:
                self.children[p].append(n)
        self.depth = {root: 0}
        order = [root]
        for n in order:
            for c in self.children[n]:
                self.depth[c] = self.depth[n] + 1
                order.append(c)
        self.mass, self.count = {}, {}
        for n in reversed(order):
            self.mass[n] = own(n) + sum(self.mass[c] for c in self.children[n])
            self.count[n] = 1 + sum(self.count[c] for c in self.children[n])
        self.order = order
        self.total = self.mass[root]
        self.spine = [root]
        while True:
            kids = self.children[self.spine[-1]]
            if not kids:
                break
            best = max(kids, key=lambda c: self.mass[c])
            if self.mass[best] < SPINE_SHARE * self.mass[self.spine[-1]]:
                break
            self.spine.append(best)
        self.hub = self.spine[-1]

    def chain_end(self, n):
        """Follow n down while one child carries >= 90% of the mass. Returns the list n..end."""
        chain = [n]
        while True:
            kids = self.children[chain[-1]]
            if not kids:
                return chain
            best = max(kids, key=lambda c: self.mass[c])
            if self.mass[best] < SPINE_SHARE * self.mass[chain[-1]] or self.count[best] < MIN_CHAPTER:
                return chain
            chain.append(best)

    def top_ancestor(self):
        """node -> the child of the hub it sits under (None for spine nodes and off-hub leaves)."""
        top = {}
        for c in self.children[self.hub]:
            stack = [c]
            while stack:
                x = stack.pop()
                top[x] = c
                stack.extend(self.children[x])
        return top


def pct(x, total):
    return round(100.0 * x / total, 2) if total else 0.0


# --------------------------------------------------------------------------- shape

def shape_of(C, T):
    D = C.decl
    hub_kids = T.children[T.hub]
    trivial = [c for c in hub_kids if T.count[c] == 1]
    bins = [(1, 1), (2, 4), (5, 19), (20, 99), (100, 10 ** 9)]
    by_bin = []
    for lo, hi in bins:
        sel = [c for c in hub_kids if lo <= T.count[c] <= hi]
        by_bin.append({'dominatedDecls': '%d-%s' % (lo, hi if hi < 10 ** 9 else 'up'), 'heads': len(sel),
                       'decls': sum(T.count[c] for c in sel),
                       'massPct': pct(sum(T.mass[c] for c in sel), T.total)})
    spine_side = sum(T.mass[c] for n in T.spine[:-1] for c in T.children[n] if c not in T.spine)
    nontriv = [n for n in T.order if T.count[n] >= 2 and n not in T.spine]
    chapters = [c for c in hub_kids if T.count[c] >= MIN_CHAPTER]
    depth_hist = collections.Counter(T.depth[n] - T.depth[T.hub] for n in T.order if n not in T.spine)
    mass_by_depth = collections.Counter()
    for n in T.order:
        if n not in T.spine:
            mass_by_depth[T.depth[n] - T.depth[T.hub]] += C.own(n)
    kinds_trivial = collections.Counter(D[c]['kind'] for c in trivial)

    def med(xs):
        xs = sorted(xs)
        return xs[len(xs) // 2] if xs else None

    return {
        'root': T.root,
        'reachable': len(T.idom),
        'totalMass': T.total,
        'spine': [{'name': n, 'massPct': pct(T.mass[n], T.total), 'dominated': T.count[n],
                   'treeChildren': len(T.children[n])} for n in T.spine],
        'hub': T.hub,
        'hubChildren': len(hub_kids),
        'hubChildrenTrivial': len(trivial),
        'hubChildrenTrivialByKind': dict(kinds_trivial),
        'sharedLayer': {
            'comment': 'declarations whose only dominators are the root and the spine',
            'decls': len(hub_kids), 'declsPct': pct(len(hub_kids), len(T.idom)),
            'ownMassPct': pct(sum(C.own(c) for c in hub_kids), T.total),
            'ofWhichTrivialOwnMassPct': pct(sum(C.own(c) for c in trivial), T.total)},
        'spineOwnMassPct': pct(sum(C.own(n) for n in T.spine), T.total),
        'spineSideBranchesMassPct': pct(spine_side, T.total),
        'hubChildrenBySize': by_bin,
        'chapters': len(chapters),
        'chaptersMassPct': pct(sum(T.mass[c] for c in chapters), T.total),
        'chaptersStrictlyHiddenMassPct': pct(sum(T.mass[c] - C.own(c) for c in chapters), T.total),
        'nontrivialDominators': len(nontriv),
        'maxDepthBelowHub': max(depth_hist),
        'declsByDepthBelowHub': {str(k): depth_hist[k] for k in sorted(depth_hist)[:12]},
        'ownMassPctByDepthBelowHub': {str(k): pct(mass_by_depth[k], T.total) for k in sorted(mass_by_depth)[:12]},
        'chapterHeads': {
            'theorems': sum(1 for c in chapters if D[c]['kind'] == 'theorem'),
            'nonTheorems': sum(1 for c in chapters if D[c]['kind'] != 'theorem'),
            'withDocstringPct': pct(sum(1 for c in chapters if D[c]['hasDocstring']), len(chapters)),
            'medianStatementChars': med([D[c]['statementChars'] for c in chapters]),
            'medianStatementDagSize': med([D[c]['statementDagSize'] for c in chapters]),
            'over1000Chars': sum(1 for c in chapters if D[c]['statementChars'] > 1000)},
        'allReachable': {
            'withDocstringPct': pct(sum(1 for n in T.idom if D[n]['hasDocstring']), len(T.idom)),
            'medianTheoremStatementChars': med([D[n]['statementChars'] for n in T.idom
                                                if D[n]['kind'] == 'theorem'])},
    }


def skip_curve(C, T):
    """Mass a reader skips by trusting the K heaviest chapter statements (heads under the hub)."""
    kids = sorted(T.children[T.hub], key=lambda c: -T.mass[c])
    out = []
    for k in (1, 2, 5, 10, 20, 40, 100, 300, 1000):
        sel = kids[:k]
        out.append({'statements': len(sel), 'skippedMassPct': pct(sum(T.mass[c] for c in sel), T.total),
                    'skippedDecls': sum(T.count[c] for c in sel)})
    sel = [c for c in kids if T.count[c] >= 2]
    out.append({'statements': len(sel), 'note': 'every head that dominates at least one other declaration',
                'skippedMassPct': pct(sum(T.mass[c] for c in sel), T.total),
                'skippedDecls': sum(T.count[c] for c in sel)})
    return out


# --------------------------------------------------------------------------- relaxations

def reach_without(succ, root, removed):
    seen = {root}
    stack = [root]
    while stack:
        n = stack.pop()
        for s in succ[n]:
            if s not in seen and s not in removed:
                seen.add(s)
                stack.append(s)
    return seen


def relax_library(C, T):
    """(a) Declare nodes with many users to be 'library', cut them out, recompute dominators."""
    reach = set(T.idom)
    indeg = collections.Counter()
    for n in reach:
        for s in C.succ[n]:
            indeg[s] += 1
    rows = []
    variants = [('users>=%d' % k, {n for n in reach if indeg[n] >= k and n != T.root})
                for k in (200, 100, 50, 20, 10, 5, 3)]
    variants.append(('all non-theorems', {n for n in reach if C.decl[n]['kind'] != 'theorem' and n != T.root}))
    for label, lib in variants:
        succ = {n: [s for s in C.succ[n] if s not in lib] for n in reach if n not in lib}
        T2 = DomTree(succ, T.root, C.own)
        kids = T2.children[T2.hub]
        chap = [c for c in kids if T2.count[c] >= MIN_CHAPTER]
        rows.append({
            'library': label, 'libraryDecls': len(lib),
            'libraryOwnMassPct': pct(sum(C.own(n) for n in lib), T.total),
            'reachedOnlyThroughLibraryDecls': len(reach) - len(lib) - len(T2.idom),
            'remainingDecls': len(T2.idom), 'remainingMassPctOfOriginal': pct(T2.total, T.total),
            'spineLength': len(T2.spine), 'hub': T2.hub, 'hubChildren': len(kids),
            'hubChildrenTrivial': sum(1 for c in kids if T2.count[c] == 1),
            'chapters': len(chap),
            'chaptersMassPctOfRemaining': pct(sum(T2.mass[c] for c in chap), T2.total),
            'chaptersMassPctOfOriginal': pct(sum(T2.mass[c] for c in chap), T.total),
            'top40HeadsMassPctOfOriginal': pct(sum(sorted((T2.mass[c] for c in kids), reverse=True)[:40]), T.total),
        })
    return rows


def relax_cuts(C, T):
    """(b) Vertex cuts of size 2-3 made of chapter statements.
    For every declaration outside the chapters, owners(n) = the chapters (or HUB, meaning the hub,
    the spine and its side branches) that reach n by a path whose interior avoids all chapters.
    Deleting the owner chapters' heads disconnects n from the root when HUB is not an owner, so a
    declaration with 2 or 3 owners and no HUB is cut off by that pair or triple of chapter statements.
    The owner set is a sufficient cut, not always a minimal one (deleting two heads can also cut off a
    third chapter), so the table is slightly pessimistic; `extraDeclsByDeletionCheck` recounts the best
    cuts by actually deleting the heads and recomputing reachability."""
    top = T.top_ancestor()
    chapters = {c for c in T.children[T.hub] if T.count[c] >= MIN_CHAPTER}
    spine = set(T.spine)
    pred = collections.defaultdict(list)
    for n in T.idom:
        for s in C.succ[n]:
            pred[s].append(n)
    BIG = frozenset(['4+'])
    owners = {}
    # users come before the declarations they use in a reverse postorder of the dependency graph
    for n in reverse_postorder(C.succ, T.root):
        if n not in top or top[n] in chapters:
            continue          # spine, side branches above the hub, or inside a chapter
        acc = set()
        for p in pred[n]:
            if p not in top:
                acc.add('HUB')
            elif top[p] in chapters:
                acc.add(top[p])
            else:
                acc |= owners[p]
        if '4+' in acc or len(acc - {'HUB'}) > 3:
            acc = set(BIG) | ({'HUB'} if 'HUB' in acc else set())
        owners[n] = frozenset(acc)
    by = collections.Counter()
    byn = collections.Counter()
    sets = collections.Counter()
    setn = collections.Counter()
    for n, o in owners.items():
        if 'HUB' in o:
            key = 'reached from the hub or spine without passing a chapter'
        elif '4+' in o:
            key = 'cut needs 4 or more chapters'
        else:
            key = 'cut of %d chapters' % len(o)
            sets[o] += C.own(n)
            setn[o] += 1
        by[key] += C.own(n)
        byn[key] += 1
    outside = sum(by.values())
    table = {k: {'decls': byn[k], 'massPctOfAll': pct(by[k], T.total), 'massPctOfOutsideChapters': pct(by[k], outside)}
             for k in sorted(by)}

    def row(o):
        still = reach_without(C.succ, T.root, set(o))
        exact = sum(1 for n in owners if n not in still)
        return {'cut': sorted(o), 'chaptersMassPct': pct(sum(T.mass[h] for h in o), T.total),
                'extraMassPct': pct(sets[o], T.total), 'extraDecls': setn[o],
                'extraDeclsByDeletionCheck': exact}

    pairs = sorted((o for o in sets if len(o) == 2), key=lambda o: -sets[o])
    triples = sorted((o for o in sets if len(o) == 3), key=lambda o: -sets[o])

    def cumulative(lst, k):
        return pct(sum(sets[o] for o in lst[:k]), T.total)

    return {'chapters': len(chapters), 'outsideChaptersDecls': len(owners),
            'outsideChaptersMassPct': pct(outside, T.total),
            'byCutSize': table,
            'distinctPairs': len(pairs), 'distinctTriples': len(triples),
            'extraMassPctFromBest': {'5 pairs': cumulative(pairs, 5), '20 pairs': cumulative(pairs, 20),
                                     'all pairs': cumulative(pairs, len(pairs)),
                                     '5 triples': cumulative(triples, 5), '20 triples': cumulative(triples, 20),
                                     'all triples': cumulative(triples, len(triples))},
            'bestPairs': [row(o) for o in pairs[:10]], 'bestTriples': [row(o) for o in triples[:6]]}


def relax_condense(C, T):
    """(c) Concepts instead of lemmas: definitions as dominators, and the module quotient graph."""
    D = C.decl
    nonthm = [n for n in T.order if D[n]['kind'] != 'theorem' and T.count[n] >= MIN_CHAPTER and n not in T.spine]
    # maximal ones only (not below another non-theorem dominator)
    nonthm_set = set(nonthm)
    maximal = []
    for n in nonthm:
        x = T.idom[n]
        while x != T.root and x not in nonthm_set:
            x = T.idom[x]
        if x == T.root or x in T.spine:
            maximal.append(n)
    defs = {
        'definitionDominators': len(nonthm),
        'maximalDefinitionDominators': len(maximal),
        'massPctUnderMaximal': pct(sum(T.mass[n] for n in maximal), T.total),
        'top': [{'name': n, 'kind': D[n]['kind'], 'massPct': pct(T.mass[n], T.total), 'dominated': T.count[n],
                 'statementChars': D[n]['statementChars']}
                for n in sorted(maximal, key=lambda n: -T.mass[n])[:15]],
    }
    # module quotient
    mod_of = {n: D[n]['module'] for n in T.idom}
    msucc = collections.defaultdict(set)
    mmass = collections.Counter()
    mcount = collections.Counter()
    for n in T.idom:
        mmass[mod_of[n]] += C.own(n)
        mcount[mod_of[n]] += 1
        msucc[mod_of[n]]
        for s in C.succ[n]:
            if mod_of[s] != mod_of[n]:
                msucc[mod_of[n]].add(mod_of[s])
    MT = DomTree({m: sorted(v) for m, v in msucc.items()}, mod_of[T.root], lambda m: mmass[m])
    kids = MT.children[MT.hub]
    nontriv = [c for c in kids if MT.count[c] >= 2]
    big = [c for c in kids if MT.count[c] >= 5]
    modules = {
        'modules': len(MT.idom), 'spine': MT.spine, 'hub': MT.hub, 'hubChildren': len(kids),
        'hubChildrenTrivial': len(kids) - len(nontriv),
        'trivialModulesMassPct': pct(sum(MT.mass[c] for c in kids if MT.count[c] == 1), MT.total),
        'headsWith2PlusModules': len(nontriv),
        'massPctUnderHeadsWith2PlusModules': pct(sum(MT.mass[c] for c in nontriv), MT.total),
        'headsWith5PlusModules': len(big),
        'massPctUnderHeadsWith5PlusModules': pct(sum(MT.mass[c] for c in big), MT.total),
        'top': [{'module': c, 'massPct': pct(MT.mass[c], MT.total), 'modulesDominated': MT.count[c],
                 'declsInModule': mcount[c]} for c in sorted(kids, key=lambda c: -MT.mass[c])[:15]],
    }
    return {'definitions': defs, 'modules': modules}


def relax_cluster(C, T):
    """(d) A different method: Louvain communities of the undirected reachable graph.
    Reported with the size of each community's interface (members used from outside), because a
    cluster, unlike a dominator, has no single statement to trust."""
    try:
        import networkx as nx
    except ImportError:
        return {'skipped': 'networkx not installed'}
    reach = set(T.idom)
    indeg = collections.Counter()
    for n in reach:
        for s in C.succ[n]:
            indeg[s] += 1
    lib = {n for n in reach if indeg[n] >= 50}
    g = nx.Graph()
    for n in reach - lib:
        g.add_node(n)
        for s in C.succ[n]:
            if s not in lib:
                g.add_edge(n, s)
    comms = nx.community.louvain_communities(g, seed=1)
    mod = nx.community.modularity(g, comms)
    comms.sort(key=lambda c: -sum(C.own(n) for n in c))
    top = T.top_ancestor()
    rows = []
    for c in comms[:40]:
        entry = {s for n in reach - c - lib for s in C.succ[n] if s in c}
        mods = collections.Counter(C.decl[n]['module'] for n in c)
        heads = collections.Counter(top.get(n, '(spine)') for n in c)
        h, hc = heads.most_common(1)[0]
        rows.append({'decls': len(c), 'massPct': pct(sum(C.own(n) for n in c), T.total),
                     'entryPoints': len(entry), 'modules': len(mods),
                     'topModule': mods.most_common(1)[0][0],
                     'largestDominatorRegion': h if T.count.get(h, 0) > 1 else '(none: shared layer)',
                     'shareInThatRegionPct': pct(hc, len(c)) if T.count.get(h, 0) > 1 else 0.0})
    ents = sorted(r['entryPoints'] for r in rows)
    return {'method': 'Louvain (networkx, seed 1) on the undirected graph after removing nodes with >= 50 users',
            'libraryRemoved': len(lib), 'communities': len(comms), 'modularity': round(mod, 3),
            'top40MassPct': round(sum(r['massPct'] for r in rows), 2),
            'top40MedianEntryPoints': ents[len(ents) // 2] if ents else None,
            'top40MinEntryPoints': ents[0] if ents else None,
            'top': rows[:15]}


# --------------------------------------------------------------------------- outline

def build_outline(C, T):
    """Best-first growth of a tree of at most BUDGET entries and MAX_LEVEL levels below the hub.
    An entry whose dominated mass sits >= 90% under one child is shown once, with the chain noted."""
    entries = {}      # head -> dict
    heap = []
    floor = 0.001 * T.total

    def push(parent, level):
        src = T.hub if parent is None else entries[parent]['chain'][-1]
        for c in T.children[src]:
            if T.count[c] >= 2 and T.mass[c] >= floor:
                heapq.heappush(heap, (-T.mass[c], c, parent, level))

    push(None, 1)
    while heap and len(entries) < BUDGET:
        negm, c, parent, level = heapq.heappop(heap)
        entries[c] = {'name': c, 'parent': parent, 'level': level, 'chain': T.chain_end(c), 'kids': []}
        if parent is not None:
            entries[parent]['kids'].append(c)
        if level < MAX_LEVEL:
            push(c, level + 1)
    return entries


def vocabulary(C, names):
    """Definitions a reader must know to read the given statements: closure of the statements'
    typeDeps, continued through the bodies of non-theorem declarations."""
    seen = set()
    stack = []
    for n in names:
        stack.extend(C.decl[n]['typeDeps'])
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        d = C.decl[x]
        stack.extend(d['typeDeps'])
        if d['kind'] != 'theorem':
            stack.extend(v for v in d['valueDeps'] if C.decl[v]['kind'] != 'theorem')
    return {n for n in seen if C.decl[n]['kind'] != 'theorem'}


def toolkit(C, T, k=12):
    reach = set(T.idom)
    indeg = collections.Counter()
    for n in reach:
        for s in C.succ[n]:
            indeg[s] += 1
    defs = [n for n, _ in indeg.most_common() if C.decl[n]['kind'] != 'theorem'][:k]
    thms = [n for n, _ in indeg.most_common() if C.decl[n]['kind'] == 'theorem'][:k]
    return [{'name': n, 'kind': C.decl[n]['kind'], 'users': indeg[n],
             'statement': C.decl[n]['statement']} for n in defs + thms], indeg


def trim(s, n=TRIM):
    s = ' '.join(s.split())
    return s if len(s) <= n else s[:n].rstrip() + ' ...'


def short(name):
    if name.startswith('_private.'):
        return name.split('.0.', 1)[1] + ' (private)'
    return name


# --------------------------------------------------------------------------- main

def main():
    os.makedirs(OUT, exist_ok=True)
    C = Corpus(CORPUS)
    D = C.decl
    ratings = {}
    rpath = os.path.join(OUT, 'ratings.json')
    if os.path.exists(rpath):
        ratings = json.load(open(rpath))

    shapes, relax, graphs = {}, {}, {}
    md = []
    trees = {}
    for r in C.roots:
        key = KEYS[r['name']]
        T = DomTree(C.succ, r['name'], C.own)
        trees[key] = T
        # per-node table
        with open(os.path.join(OUT, 'dominators_%s.jsonl' % key), 'w') as fh:
            for n in T.order:
                d = D[n]
                fh.write(json.dumps({
                    'name': n, 'idom': T.idom[n] if n != T.root else None, 'depth': T.depth[n],
                    'dominatedMass': T.mass[n], 'ownMass': C.own(n), 'dominatedDecls': T.count[n],
                    'kind': d['kind'],
                    'statementDagSize': d['statementDagSize'], 'statementSize': d['statementSize'],
                    'statementChars': d['statementChars'], 'hasDocstring': d['hasDocstring'],
                    'onSpine': n in T.spine, 'module': d['module'], 'line': d['line']},
                    ensure_ascii=False) + '\n')
        s = shape_of(C, T)
        s['paper'] = r['paper']
        s['skipCurve'] = skip_curve(C, T)
        shapes[key] = s
        print(key, 'reach', s['reachable'], 'hub', T.hub, 'hub children', s['hubChildren'],
              'chapters', s['chapters'], 'chapter mass %', s['chaptersMassPct'], flush=True)

    for key in PRIMARY:
        T = trees[key]
        relax[key] = {'a_library_removed': relax_library(C, T), 'b_small_cuts': relax_cuts(C, T),
                      'c_condense': relax_condense(C, T), 'd_clustering': relax_cluster(C, T)}
        print(key, 'relaxations done', flush=True)

    # ---- outlines, outline.json
    for r in C.roots:
        key = KEYS[r['name']]
        T = trees[key]
        ents = build_outline(C, T)
        tk, indeg = toolkit(C, T)
        level1 = [e for e in ents.values() if e['level'] == 1]
        leaves = [e for e in ents.values() if not e['kids']]
        shown = [e['name'] for e in ents.values()]
        vocab = vocabulary(C, shown + T.spine)
        top = T.top_ancestor()
        hidden_heads = {e['name'] for e in level1}
        vocab_hidden = [v for v in vocab if top.get(v) in hidden_heads and v not in hidden_heads]
        summary = {
            'statementsInOutline': len(ents), 'level1': len(level1),
            'skippedByTrustingLevel1MassPct': pct(sum(T.mass[e['name']] for e in level1), T.total),
            'skippedByTrustingLevel1Decls': sum(T.count[e['name']] for e in level1),
            'skippedByTrustingLeavesMassPct': pct(sum(T.mass[e['name']] for e in leaves), T.total),
            'notCoveredMassPct': pct(T.total - sum(T.mass[e['name']] for e in level1), T.total),
            'notCoveredDecls': len(T.idom) - sum(T.count[e['name']] for e in level1),
            'vocabularyDirect': len({t for n in shown + T.spine for t in D[n]['typeDeps']}),
            'vocabularyDefinitions': len(vocab),
            'vocabularyDefinitionsInsideHiddenRegions': len(vocab_hidden),
            'outlineStatementChars': {'median': sorted(D[n]['statementChars'] for n in shown)[len(shown) // 2],
                                      'over1000': sum(1 for n in shown if D[n]['statementChars'] > 1000),
                                      'max': max(D[n]['statementChars'] for n in shown)},
            'outlineWithDocstring': sum(1 for n in shown if D[n]['hasDocstring']),
            'outlineTheorems': sum(1 for n in shown if D[n]['kind'] == 'theorem'),
        }
        reach_all = set(T.idom)
        bad = 0
        for e in level1:
            still = reach_without(C.succ, T.root, {e['name']})
            if len(reach_all) - len(still) != T.count[e['name']]:
                bad += 1
        summary['level1DominanceCheckedByDeletion'] = {'checked': len(level1), 'mismatches': bad}
        shapes[key]['outline'] = summary

        nodes, edges = [], []

        def node(n, role, level=None):
            d = D[n]
            nodes.append({'name': n, 'kind': d['kind'], 'role': role, 'level': level,
                          'statement': d['statement'], 'statementTruncated': d['statementTruncated'],
                          'statementHash': d['statementHash'],
                          'sizes': {'statementChars': d['statementChars'], 'statementDagSize': d['statementDagSize'],
                                    'ownMass': C.own(n), 'dominatedMass': T.mass.get(n), 'dominatedDecls': T.count.get(n),
                                    'dominatedMassPct': pct(T.mass.get(n, 0), T.total),
                                    'users': indeg.get(n, 0)},
                          'depthInDominatorTree': T.depth.get(n), 'hasDocstring': d['hasDocstring'],
                          'module': d['module'], 'line': d['line'], 'rating': ratings.get(n)})

        for i, n in enumerate(T.spine):
            node(n, 'root' if i == 0 else 'spine')
            if i:
                edges.append({'from': T.spine[i - 1], 'to': n, 'relation': 'dominates', 'immediate': True})
        for e in ents.values():
            node(e['name'], 'chapter' if e['level'] == 1 else 'section', e['level'])
            parent = T.hub if e['parent'] is None else e['parent']
            edges.append({'from': parent, 'to': e['name'], 'relation': 'dominates',
                          'immediate': T.idom[e['name']] == parent,
                          'via': [x for x in (ents[e['parent']]['chain'][1:] if e['parent'] else [])]})
        have = {n['name'] for n in nodes}
        for t in tk:
            if t['name'] not in have:
                node(t['name'], 'toolkit')
        have = {n['name'] for n in nodes}
        for n in have:
            for s in C.succ[n]:
                if s in have:
                    edges.append({'from': n, 'to': s, 'relation': 'uses',
                                  'in': ('statement' if s in D[n]['typeDeps'] else 'proof')})
        graphs[key] = {'root': T.root, 'paper': r['paper'], 'hub': T.hub, 'totalMass': T.total,
                       'reachable': len(T.idom), 'summary': summary, 'nodes': nodes, 'edges': edges}

        # ---- markdown
        full = key in PRIMARY
        md.append('\n## %s\n' % r['name'])
        md.append('%s. Reaches %s declarations, proof mass %s.\n' % (r['paper'], f"{len(T.idom):,}", f"{T.total:,}"))
        md.append('```lean\n%s\n```\n' % D[T.root]['statement'])
        md.append('**Spine** (each statement is the only way into the one before it and carries at least 90% of its mass):\n')
        for i, n in enumerate(T.spine[1:], 1):
            d = D[n]
            md.append('%d. `%s` (%s, `%s:%d`), %.1f%% of mass, %s declarations beneath, %d tree children' % (
                i, short(n), d['kind'], d['module'], d['line'], pct(T.mass[n], T.total), f"{T.count[n]:,}", len(T.children[n])))
            if full:
                md.append('   ```lean\n   %s\n   ```' % trim(d['statement'], 700))
        if len(T.spine) == 1:
            md.append('(none: the root itself is the hub; no single statement stands between it and the rest)')
        md.append('')
        md.append('**Hub** `%s` has %s dominator-tree children; %s of them dominate nothing but themselves.\n' % (
            short(T.hub), f"{len(T.children[T.hub]):,}", f"{shapes[key]['hubChildrenTrivial']:,}"))
        md.append('**Outline** (%d statements; mass = share of all proof mass below the root that sits under the statement, itself included; hidden = declarations a reader skips by trusting it):\n' % len(ents))

        def emit(name, indent):
            e = ents[name]
            d = D[name]
            pad = '  ' * indent
            tag = ''
            if name in ratings:
                tag = ' **[%s]**' % ratings[name]['rating']
            md.append('%s- `%s` (%s%s) | mass %.2f%% | hidden %s decls | statement %d chars%s' % (
                pad, short(name), d['kind'], ', doc' if d['hasDocstring'] else '', pct(T.mass[name], T.total),
                f"{T.count[name] - 1:,}", d['statementChars'], tag))
            if len(e['chain']) > 1:
                md.append('%s  - _passes through:_ %s' % (pad, ' → '.join('`%s`' % short(x) for x in e['chain'][1:])))
            if full:
                md.append('%s  ```lean\n%s  %s\n%s  ```' % (pad, pad, trim(d['statement']), pad))
                if name in ratings:
                    md.append('%s  _%s_' % (pad, ratings[name]['why']))
            for k in sorted(e['kids'], key=lambda k: -T.mass[k]):
                emit(k, indent + 1)

        for e in sorted(level1, key=lambda e: -T.mass[e['name']]):
            emit(e['name'], 0)
        md.append('')
        md.append('Trusting the %d top-level statements skips **%.1f%%** of the proof mass (%s of %s declarations). '
                  'The other %.1f%% (%s declarations) is the hub\'s own proof plus the shared layer and small regions not listed. '
                  'The %d outline statements and the spine mention %d distinct project declarations directly; unfolding those definitions down to Mathlib takes %d project definitions, %d of which sit inside the regions being skipped.\n' % (
                      len(level1), summary['skippedByTrustingLevel1MassPct'], f"{summary['skippedByTrustingLevel1Decls']:,}",
                      f"{len(T.idom):,}", summary['notCoveredMassPct'], f"{summary['notCoveredDecls']:,}",
                      len(ents), summary['vocabularyDirect'], summary['vocabularyDefinitions'], summary['vocabularyDefinitionsInsideHiddenRegions']))
        md.append('**Shared toolkit** (most-used declarations below this root; users counted below this root only):\n')
        md.append('| users | kind | name | statement |\n|---|---|---|---|')
        for t in tk:
            md.append('| %d | %s | `%s` | `%s` |' % (t['users'], t['kind'], short(t['name']),
                                                    trim(t['statement'], 160).replace('|', '\\|')))
        md.append('')

    json.dump(shapes, open(os.path.join(OUT, 'shape.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(relax, open(os.path.join(OUT, 'relaxations.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump({'schema': 'outline/1', 'corpus': 'openai/NavierStokesAndEuler@f9e8bc5b',
               'method': 'dominator tree of the declaration dependency graph (bench/outline.py)',
               'massDefinition': 'proofSize + auxProofSize (distinct subterms)',
               'roles': {'root': 'headline theorem', 'spine': 'sole entry into the root, >= 90% of mass',
                         'chapter': 'dominator-tree child of the hub shown at level 1',
                         'section': 'dominator shown at level 2 or 3',
                         'toolkit': 'heavily used shared declaration; not dominated by any chapter'},
               'edgeRelations': {'dominates': 'every dependency path from the root to `to` passes through `from` '
                                              '(immediate=false when intermediate single-child dominators were collapsed; they are listed in `via`)',
                                 'uses': 'direct dependency between two nodes of this file, in the statement or in the proof'},
               'outlines': graphs}, open(os.path.join(OUT, 'outline.json'), 'w'), indent=1, ensure_ascii=False)
    head = []
    vpath = os.path.join(OUT, 'verdict.md')
    if os.path.exists(vpath):
        head.append(open(vpath).read().rstrip() + '\n')
    head.append('\n# Generated tables\n')
    head.append('Everything below is written by `bench/outline.py` from `out/corpus/ns/decls.jsonl`. '
                'Mass = proofSize + auxProofSize (distinct subterms). A chapter is a dominator-tree child of the hub that dominates at least %d declarations.\n' % MIN_CHAPTER)
    head.append('## Shape of the dominator tree\n')
    keys = [KEYS[r['name']] for r in C.roots]
    head.append('| | ' + ' | '.join(keys) + ' |\n|---|' + '---|' * len(keys))

    def line(label, fn):
        head.append('| %s | %s |' % (label, ' | '.join(str(fn(shapes[k])) for k in keys)))

    line('declarations below the root', lambda s: f"{s['reachable']:,}")
    line('spine length below the root', lambda s: len(s['spine']) - 1)
    line('children of the hub', lambda s: f"{s['hubChildren']:,}")
    line('... that dominate nothing else', lambda s: f"{s['hubChildrenTrivial']:,}")
    line('share of declarations hanging directly off the hub', lambda s: '%.1f%%' % s['sharedLayer']['declsPct'])
    line('their own mass (the shared layer)', lambda s: '%.1f%%' % s['sharedLayer']['ownMassPct'])
    line('chapters (20+ declarations)', lambda s: s['chapters'])
    line('mass under chapters', lambda s: '%.1f%%' % s['chaptersMassPct'])
    line('mass under heads dominating 100+ declarations', lambda s: '%.1f%% (%d heads)' % (s['hubChildrenBySize'][4]['massPct'], s['hubChildrenBySize'][4]['heads']))
    line('mass under heads dominating 2 to 19', lambda s: '%.1f%% (%d heads)' % (s['hubChildrenBySize'][1]['massPct'] + s['hubChildrenBySize'][2]['massPct'], s['hubChildrenBySize'][1]['heads'] + s['hubChildrenBySize'][2]['heads']))
    line('skipped by trusting the 10 heaviest heads', lambda s: '%.1f%%' % s['skipCurve'][3]['skippedMassPct'])
    line('... the 40 heaviest', lambda s: '%.1f%%' % s['skipCurve'][5]['skippedMassPct'])
    line('... the 100 heaviest', lambda s: '%.1f%%' % s['skipCurve'][6]['skippedMassPct'])
    line('... every head that dominates anything', lambda s: '%.1f%% (%s statements)' % (s['skipCurve'][-1]['skippedMassPct'], f"{s['skipCurve'][-1]['statements']:,}"))
    line('skipped by the outline printed below (level 1 only)', lambda s: '%.1f%% (%d statements)' % (s['outline']['skippedByTrustingLevel1MassPct'], s['outline']['level1']))
    line('chapter heads that are theorems / not', lambda s: '%d / %d' % (s['chapterHeads']['theorems'], s['chapterHeads']['nonTheorems']))
    line('chapter heads with a docstring (all declarations)', lambda s: '%.0f%% (%.0f%%)' % (s['chapterHeads']['withDocstringPct'], s['allReachable']['withDocstringPct']))
    line('median statement length of chapter heads, chars (all theorems)', lambda s: '%d (%d)' % (s['chapterHeads']['medianStatementChars'], s['allReachable']['medianTheoremStatementChars']))
    line('outline statements over 1,000 chars', lambda s: '%d of %d' % (s['outline']['outlineStatementChars']['over1000'], s['outline']['statementsInOutline']))
    line('project declarations mentioned directly by outline statements', lambda s: s['outline']['vocabularyDirect'])
    line('definitions needed to unfold them fully', lambda s: f"{s['outline']['vocabularyDefinitions']:,}")
    head.append('')
    head.append('## Relaxations (two primary roots)\n')
    for k in PRIMARY:
        R = relax[k]
        head.append('### %s\n' % k)
        head.append('(a) Library layer cut out, dominators recomputed. "Lost" = declarations reached only through the library, which no longer belong to any region.\n')
        head.append('| library = | library decls | lost decls | hub children | chapters | chapter mass, % of original | 40 heaviest heads, % of original |\n|---|---|---|---|---|---|---|')
        head.append('| (none, baseline) | 0 | 0 | %s | %d | %.1f | %.1f |' % (f"{shapes[k]['hubChildren']:,}", shapes[k]['chapters'], shapes[k]['chaptersMassPct'], shapes[k]['skipCurve'][5]['skippedMassPct']))
        for r_ in R['a_library_removed']:
            head.append('| %s | %s | %s | %s | %d | %.1f | %.1f |' % (r_['library'], f"{r_['libraryDecls']:,}", f"{r_['reachedOnlyThroughLibraryDecls']:,}", f"{r_['hubChildren']:,}", r_['chapters'], r_['chaptersMassPctOfOriginal'], r_['top40HeadsMassPctOfOriginal']))
        b_ = R['b_small_cuts']
        head.append('\n(b) Cuts made of 2 or 3 chapter statements. %.1f%% of the mass (%s declarations) lies outside the chapters; of it:\n' % (b_['outsideChaptersMassPct'], f"{b_['outsideChaptersDecls']:,}"))
        head.append('| where it sits | declarations | % of all mass |\n|---|---|---|')
        for name, v in b_['byCutSize'].items():
            head.append('| %s | %s | %.1f |' % (name, f"{v['decls']:,}", v['massPctOfAll']))
        e_ = b_['extraMassPctFromBest']
        head.append('\n%d distinct pairs and %d distinct triples occur. The best 5 pairs add %.1f%% of the mass, the best 20 add %.1f%%; the best 5 triples %.1f%%. Best pairs:\n' % (b_['distinctPairs'], b_['distinctTriples'], e_['5 pairs'], e_['20 pairs'], e_['5 triples']))
        for r_ in b_['bestPairs'][:5]:
            head.append('- %s: +%.2f%% (%d declarations)' % (' + '.join('`%s`' % short(x) for x in r_['cut']), r_['extraMassPct'], r_['extraDecls']))
        c_ = R['c_condense']
        d_, m_ = c_['definitions'], c_['modules']
        head.append('\n(c) Definitions as dominators: %d non-theorem declarations dominate 20+ declarations; the %d maximal ones cover %.1f%% of the mass. '
                    'Module quotient graph: %s modules, hub module `%s` has %s children of which %s dominate no other module (%.1f%% of mass); heads dominating 5+ modules: %d, covering %.1f%%.\n' % (
                        d_['definitionDominators'], d_['maximalDefinitionDominators'], d_['massPctUnderMaximal'],
                        f"{m_['modules']:,}", m_['hub'], f"{m_['hubChildren']:,}", f"{m_['hubChildrenTrivial']:,}", m_['trivialModulesMassPct'],
                        m_['headsWith5PlusModules'], m_['massPctUnderHeadsWith5PlusModules']))
        head.append('| definition | mass % | declarations dominated | statement chars |\n|---|---|---|---|')
        for t in d_['top'][:8]:
            head.append('| `%s` (%s) | %.2f | %s | %d |' % (short(t['name']), t['kind'], t['massPct'], f"{t['dominated']:,}", t['statementChars']))
        cl = R['d_clustering']
        if 'skipped' not in cl:
            head.append('\n(d) Different method, not dominators: %s. %d communities, modularity %.2f. '
                        'The median community has %d entry points (members used from outside it), so there is no single statement to trust. Louvain is randomised; counts move by a community or two between runs.\n' % (
                            cl['method'], cl['communities'], cl['modularity'], cl['top40MedianEntryPoints']))
            head.append('| declarations | mass % | entry points | modules | most common module | share inside one dominator chapter |\n|---|---|---|---|---|---|')
            for t in cl['top'][:8]:
                head.append('| %s | %.1f | %d | %d | `%s` | %.0f%% in `%s` |' % (f"{t['decls']:,}", t['massPct'], t['entryPoints'], t['modules'], t['topModule'], t['shareInThatRegionPct'], short(t['largestDominatorRegion']).split('.')[-1]))
        head.append('')
    if ratings:
        head.append('## Ratings of the 15 heaviest chapter statements\n')
        head.append('One reader (the agent that wrote this file), after reading the source around each declaration. '
                    'milestone = a recognisable mathematical milestone; waypoint = a sensible technical waypoint; unreadable = arbitrary or unreadable as a statement.\n')
        head.append('| root | statement | mass % | hidden | chars | rating | why |\n|---|---|---|---|---|---|---|')
        tally = collections.Counter()
        for k in PRIMARY:
            T = trees[k]
            for n in sorted((n for n in ratings if n in T.mass), key=lambda n: -T.mass[n]):
                tally[ratings[n]['rating']] += 1
                head.append('| %s | `%s` | %.2f | %s | %d | **%s** | %s |' % (k, short(n), pct(T.mass[n], T.total), f"{T.count[n] - 1:,}", D[n]['statementChars'], ratings[n]['rating'], ratings[n]['why'].replace('|', '\\|')))
        head.append('\nTally: ' + ', '.join('%d %s' % (v, k) for k, v in tally.most_common()) + '.\n')
    head.append('# Outlines\n')
    head.append('The two primary roots are printed with statements (trimmed to %d characters). The other two share almost all of their graph with them and are printed as names only.\n' % TRIM)
    with open(os.path.join(OUT, 'OUTLINE.md'), 'w') as fh:
        fh.write('\n'.join(head) + '\n' + '\n'.join(md) + '\n')
    old = os.path.join(OUT, 'outline_body.md')
    if os.path.exists(old):
        os.remove(old)
    print('wrote', OUT)


if __name__ == '__main__':
    if '--test' in sys.argv:
        run_tests()
    else:
        main()
