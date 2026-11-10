#!/usr/bin/env python3
"""Definition-centred outline of the machine Navier-Stokes / Euler proofs (plan node M2).

Chapters are CONCEPTS (structures and predicates), not lemmas.  Inputs:
  out/corpus/ns/decls.jsonl                declaration graph exported from Lean
  out/corpus/outline2/lean/heads.jsonl     per declaration: head of each hypothesis, what the
                                           conclusion produces (corpora/outline2/run.sh heads)
and, written by this script and printed back by Lean (corpora/outline2/run.sh print):
  out/corpus/outline2/lean/spec_*.json  ->  printed_*.jsonl
Outputs in out/corpus/outline2/: OUTLINE2.md, outline2.json, metrics.json, rating_items.json.

    python3 bench/outline2.py            # everything; four Lean cold starts of 15-25 s each
    python3 bench/outline2.py --no-lean  # reuse the printed_*.jsonl already on disk
    python3 bench/outline2.py --test     # unit test of the selection rule on a toy graph

Definitions
  graph      edge A -> B when A's statement or proof uses B (typeDeps | valueDeps).
  mass       proofSize + auxProofSize (as bench/outline.py).
  dom(d)     declarations all of whose dependency paths from the headline pass through d.
  spine      chain from the headline through dominator children carrying >= 90% of the parent.
  candidate  a structure, an inductive type, or a Prop-valued definition (a predicate) below the
             headline.  Type-valued definitions (`Plane := EuclideanSpace R (Fin 2)`) are NOTATION:
             printed once in a glossary, never a chapter.
  producer   of concept c: a declaration whose conclusion has head c, looking through
             Nonempty / exists / and / sigma / subtype (from Lean, heads.jsonl).
  object     a producer that is a definition taking no project concept as input: a chosen object.
  consumer   of c: a declaration with a hypothesis whose head is c, or that uses an object of c.
  region(c)  union of dom(p) over producers p off the spine, plus the consumers themselves.
  selection  greedy, K_CHAPTERS rounds.  The proof below the headline is kept as a partition into
             cells (one per chosen concept, plus "unattributed").  The gain of a candidate is the
             unattributed mass its region covers plus, for each existing cell, the smaller of the
             two sides its region cuts that cell into.  A chosen concept takes the unattributed
             part and, from each cell, its side when that side is the smaller one.
No LLM and no source regex is involved.  Labels are the corpus's own docstrings, read from the
Lean environment; where there is none the outline says "undocumented".
"""
import collections
import hashlib
import json
import os
import random
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import outline as O1          # dominator algorithm of the lemma-based outline
import paper_truth as PT      # scorer

REPO = os.path.dirname(HERE)
DECLS = os.path.join(REPO, 'out', 'corpus', 'ns', 'decls.jsonl')
OUT = os.path.join(REPO, 'out', 'corpus', 'outline2')
LEAN = os.path.join(OUT, 'lean')
RUN = os.path.join(REPO, 'corpora', 'outline2', 'run.sh')
OLD = os.path.join(REPO, 'out', 'corpus', 'outline', 'outline.json')

ROOTS = collections.OrderedDict([
    ('ns_r3', dict(root='NavierStokes.Comparator.navier_stokes_breakdown_R3', paper='ns',
                   title='Navier-Stokes', what='Navier-Stokes Theorem 1.1, Clay alternative (C): breakdown on R^3')),
    ('euler_compact', dict(root='Euler.exists_compact_smooth_euler_singularity', paper='euler',
                           title='Euler', what='Euler Theorem 1.1, alternate version (compact support, C^1 norm and vorticity integral blow up)')),
])

# ---- parameters (fixed before any score against the paper ground truth was computed) ----------
K_CHAPTERS = 14          # concept chapters; the goal and the closing chapter are extra
PER_CHAPTER = 4          # statements per concept chapter: construction (1-2) then consumers
SUPPORT = 3              # supporting definitions unfolded per chapter (goal chapter: GOAL_SUPPORT)
GOAL_SUPPORT = 6
SPINE_SHARE = 0.9
FIELD_CAP = 300          # characters of one field type shown in OUTLINE2.md
BODY_CAP = 700           # characters of a definition body shown
STMT_CAP = 900           # characters of a statement (added binders + conclusion) shown
NOTATION_ROUNDS = 3
RATING_SEED = 20261110
RATING_PER_CELL = 15     # entries per outline per paper


# --------------------------------------------------------------------------- loading

def load_decls():
    D = {}
    with open(DECLS) as f:
        for line in f:
            d = json.loads(line)
            D[d['name']] = d
    return D


def load_heads():
    H = {}
    with open(os.path.join(LEAN, 'heads.jsonl')) as f:
        for line in f:
            h = json.loads(line)
            H[h['name']] = h
    return H


def parent_of(D, n):
    """Exported declaration a constant belongs to (projections, constructors -> the structure)."""
    while n and n not in D:
        if '.' not in n:
            return None
        n = n.rsplit('.', 1)[0]
    return n or None


def mass_of(d):
    return d['proofSize'] + d['auxProofSize']


# --------------------------------------------------------------------------- graph

class G:
    """Dominator tree and concept relations below one headline theorem."""

    def __init__(self, D, H, succ, root):
        self.D, self.H, self.succ, self.root = D, H, succ, root
        idom = O1.immediate_dominators(succ, root)
        self.idom = idom
        self.R = set(idom)
        kids = collections.defaultdict(list)
        for n, p in idom.items():
            if n != root:
                kids[p].append(n)
        for k in kids.values():
            k.sort()
        self.kids = kids
        order, st = [], [root]
        while st:                                  # preorder; each subtree is a contiguous slice
            n = st.pop()
            order.append(n)
            st.extend(kids[n])
        self.order = order
        self.idx = {n: i for i, n in enumerate(order)}
        self.massarr = np.array([mass_of(D[n]) for n in order], dtype=np.int64)
        self.total = int(self.massarr.sum())
        size = {n: 1 for n in order}
        dm = {n: mass_of(D[n]) for n in order}
        for n in reversed(order):
            if n != root:
                size[idom[n]] += size[n]
                dm[idom[n]] += dm[n]
        self.size, self.dm = size, dm
        height = {}
        for n in reversed(O1.reverse_postorder(succ, root)):
            height[n] = 1 + max((height[s] for s in succ[n]), default=0)
        self.height = height
        spine, n = [], root
        while True:
            ch = kids[n]
            if not ch:
                break
            best = max(ch, key=lambda c: (dm[c], c))
            if dm[best] < SPINE_SHARE * dm[n]:
                break
            spine.append(best)
            n = best
        self.spine = spine
        self.onspine = set(spine) | {root}
        users = collections.defaultdict(set)
        for n in self.R:
            for s in succ[n]:
                users[s].add(n)
        self.users = users
        self._relations()

    def is_candidate(self, n):
        d = self.D[n]
        return d['kind'] in ('structure', 'inductive') or (d['kind'] == 'def' and self.H[n]['propValued'])

    def is_notation(self, n):
        d = self.D[n]
        return d['kind'] == 'def' and self.H[n]['sortValued'] and not self.H[n]['propValued']

    def _relations(self):
        D, H = self.D, self.H
        prod = collections.defaultdict(set)
        cons = collections.defaultdict(set)
        for n in self.R:
            h = H[n]
            if h['sortValued']:
                continue                              # a definition of a type or predicate proves nothing
            for p in set(h['produces']):
                p = parent_of(D, p)
                if p and p != n and D[p]['kind'] != 'theorem':
                    prod[p].add(n)
            for b in h['binders']:
                if b['head']:
                    p = parent_of(D, b['head'])
                    if p and p != n and D[p]['kind'] != 'theorem':
                        cons[p].add(n)
        self.cands = sorted(n for n in self.R if self.is_candidate(n))
        cset = set(self.cands)
        objs = collections.defaultdict(set)
        for c in self.cands:
            for p in prod[c]:
                if D[p]['kind'] not in ('def', 'instance'):
                    continue
                if parent_of(D, H[p]['conclHead'] or '') != c:
                    continue
                if any(b['head'] and parent_of(D, b['head']) in cset for b in H[p]['binders']):
                    continue
                objs[c].add(p)
        via = collections.defaultdict(set)
        for c in self.cands:
            for p in objs[c]:
                via[c] |= self.users[p]
            via[c] -= prod[c]
            via[c].discard(c)
        self.prod, self.cons, self.objs, self.via = prod, cons, objs, via

    def sub(self, n):
        i = self.idx[n]
        return slice(i, i + self.size[n])

    def built_mask(self, c):
        m = np.zeros(len(self.order), dtype=bool)
        for p in self.prod[c]:
            if p not in self.onspine:
                m[self.sub(p)] = True
        return m

    def region_mask(self, c):
        m = self.built_mask(c)
        for t in self.cons[c] | self.via[c]:
            if t not in self.onspine:
                m[self.idx[t]] = True
        return m

    def pct(self, mask):
        return 100.0 * float(self.massarr[mask].sum()) / self.total


def greedy(masses, regions, k):
    """Balanced-split greedy.  masses: int array; regions: {name: bool array}.
    Returns (chosen names in pick order, cell array (-1 unattributed, else index), gains)."""
    n = len(masses)
    cell = np.full(n, -1, dtype=np.int64)
    chosen, gains = [], []
    names = sorted(regions)
    for _ in range(k):
        ncell = len(chosen) + 1
        tot = np.bincount(cell + 1, weights=masses, minlength=ncell)
        best, bestg = None, 0.0
        for c in names:
            if c in chosen:
                continue
            m = regions[c]
            ins = np.bincount(cell[m] + 1, weights=masses[m], minlength=ncell)
            g = ins[0] + np.minimum(ins[1:], tot[1:] - ins[1:]).sum()
            if g > bestg:
                best, bestg = c, g
        if best is None:
            break
        m = regions[best]
        ins = np.bincount(cell[m] + 1, weights=masses[m], minlength=ncell)
        take = m & (cell == -1)
        for j in range(1, ncell):
            if 0 < ins[j] <= tot[j] - ins[j]:
                take |= m & (cell == j - 1)
        cell[take] = len(chosen)
        chosen.append(best)
        gains.append(float(bestg))
    return chosen, cell, gains


def selftest():
    # six unit-mass nodes; region A = {0,1,2,3}, B = {2,3} (nested in A), C = {0,1,2,3} (duplicate of A), E = {4}
    masses = np.ones(6, dtype=np.int64)
    def mk(ix):
        m = np.zeros(6, dtype=bool); m[list(ix)] = True; return m
    regions = {'A': mk([0, 1, 2, 3]), 'B': mk([2, 3]), 'C': mk([0, 1, 2, 3]), 'E': mk([4])}
    chosen, cell, gains = greedy(masses, regions, 4)
    assert chosen[0] == 'A' and gains[0] == 4, (chosen, gains)
    assert chosen[1] == 'B' and gains[1] == 2, (chosen, gains)        # splits A in half
    assert chosen[2] == 'E' and gains[2] == 1, (chosen, gains)        # new mass beats the duplicate
    assert 'C' not in chosen, chosen                                   # a duplicate region gains nothing
    assert list(cell) == [0, 0, 1, 1, 2, -1], list(cell)
    assert rel_name('NavierStokes.A.foo', 'NavierStokes.A') == 'foo'
    assert rel_name('NavierStokes.B.foo', 'NavierStokes.A') == 'B.foo'
    assert rel_name('Other.foo', 'NavierStokes.A') == 'Other.foo'
    assert first_sentence('The profile. More text.') == 'The profile.'
    assert cap('abcdef', 3)[0] == 'abc' and cap('abc', 3) == ('abc', 0)
    print('outline2 self-test passed')


# --------------------------------------------------------------------------- selection

def choose(g):
    regions = {}
    for c in g.cands:
        m = g.region_mask(c)
        if m.any():
            regions[c] = m
    chosen, cell, gains = greedy(g.massarr, regions, K_CHAPTERS)
    chapters = []
    for i, c in enumerate(chosen):
        chapters.append(dict(concept=c, pick=i + 1, gainPct=round(100.0 * gains[i] / g.total, 2),
                             regionPct=round(g.pct(regions[c]), 2), builtPct=round(g.pct(g.built_mask(c)), 2),
                             cellPct=round(g.pct(cell == i), 2),
                             producers=len(g.prod[c]), objects=len(g.objs[c]),
                             consumers=len(g.cons[c]), consumersViaObject=len(g.via[c])))
    return chapters, round(g.pct(cell >= 0), 2)


def eligible(g, n):
    return n not in g.onspine and g.D[n]['kind'] in ('theorem', 'def', 'instance') and not g.H[n]['sortValued']


def pick_statements(g, chapters):
    D = g.D
    concepts = {ch['concept'] for ch in chapters}
    key = lambda n: (-g.dm[n], n)
    # construction statements first (a statement constructs at most one chapter's concept: the heaviest region)
    taken = set()
    for ch in sorted(chapters, key=lambda ch: ch['pick']):
        c = ch['concept']
        ps = sorted((p for p in g.prod[c] if eligible(g, p) and p not in taken and p not in concepts), key=key)
        cons = []
        if ps:
            cons.append(ps[0])
            if D[ps[0]]['kind'] != 'theorem':
                th = [p for p in ps[1:] if D[p]['kind'] == 'theorem' and g.dm[p] >= 0.5 * g.dm[ps[0]]]
                if th:
                    cons.append(th[0])
        taken |= set(cons)
        ch['construction'] = cons
        ch['producedOnSpine'] = sorted(p for p in g.prod[c] if p in g.onspine)
        ch['first'] = None
    # order: height of the construction statement, else of the lowest consumer
    for ch in chapters:
        c = ch['concept']
        pool = sorted((t for t in (g.cons[c] | g.via[c]) if eligible(g, t) and t not in g.prod[c] and t not in concepts), key=key)
        ch['_pool'] = pool
    # consumers: later chapters (by provisional order) choose first, so a statement that uses two
    # concepts is shown under the later one
    def prov(ch):
        if ch['construction']:
            return g.height[ch['construction'][0]]
        return min((g.height[t] for t in ch['_pool'][:PER_CHAPTER]), default=0)
    for ch in sorted(chapters, key=lambda ch: (-prov(ch), ch['concept'])):
        want = PER_CHAPTER - len(ch['construction'])
        got = []
        for t in ch['_pool']:
            if len(got) >= want:
                break
            if t in taken:
                continue
            got.append(t)
        taken |= set(got)
        ch['consumersShown'] = got
        del ch['_pool']
    for ch in chapters:
        first = ch['construction'][0] if ch['construction'] else None
        if first is None and ch['consumersShown']:
            first = min(ch['consumersShown'], key=lambda t: (g.height[t], t))
        ch['orderKey'] = g.height[first] if first else 0
        ch['orderBy'] = 'construction' if ch['construction'] else 'first consumer'
    chapters.sort(key=lambda ch: (ch['orderKey'], ch['concept']))
    for i, ch in enumerate(chapters):
        ch['number'] = i + 1
    return chapters


# --------------------------------------------------------------------------- Lean round trip

def user_name(D, n):
    return D[n]['userName']


def ns_of(D, n):
    u = user_name(D, n)
    return u.rsplit('.', 1)[0] if '.' in u else ''


def rel_name(name, ns):
    """Name as Lean resolves it inside namespace `ns` (longest enclosing prefix removed)."""
    parts = ns.split('.') if ns else []
    for i in range(len(parts), 0, -1):
        pre = '.'.join(parts[:i]) + '.'
        if name.startswith(pre):
            return name[len(pre):]
    return name


def lean_print(tag, items, use_lean):
    spec = os.path.join(LEAN, f'spec_{tag}.json')
    out = os.path.join(LEAN, f'printed_{tag}.jsonl')
    if use_lean:
        with open(spec, 'w') as f:
            json.dump(items, f, indent=0)
        subprocess.run([RUN, 'print', spec, out], check=True)
    else:
        with open(spec) as f:
            if json.load(f) != items:
                sys.exit(f'--no-lean: {spec} no longer matches the selection; rerun without --no-lean')
    res = {}
    with open(out) as f:
        for line in f:
            r = json.loads(line)
            if 'error' in r or r.get('missing'):
                sys.exit(f'Lean could not print {r["name"]}: {r}')
            res[(r['name'], r['as'])] = r
    return res


# --------------------------------------------------------------------------- text

def first_sentence(doc):
    if not doc:
        return None
    s = ' '.join(doc.split())
    m = re.search(r'(?<=[.!?])\s', s)
    s = s[:m.start()] if m else s
    return s if len(s) <= 240 else s[:240].rstrip() + ' ...'


def cap(s, n):
    return (s, 0) if len(s) <= n else (s[:n].rstrip(), len(s) - n)


def binder_text(b):
    t = b['type']
    if b['bi'] == 'inst':
        return f'[{t}]'
    o, c = {'default': '()', 'implicit': '{}', 'strict': '⦃⦄'}[b['bi']]
    return f'{o}{b["name"]} : {t}{c}'


def binder_ref(b):
    return f'[{b["type"]}]' if b['bi'] == 'inst' else b['name']


def group_binders(bs):
    """(a b : T) for consecutive binders of the same kind and printed type."""
    out, i = [], 0
    while i < len(bs):
        b = bs[i]
        if b['bi'] == 'inst':
            out.append(binder_text(b)); i += 1; continue
        j = i
        names = []
        while j < len(bs) and bs[j]['bi'] == b['bi'] and bs[j]['type'] == b['type']:
            names.append(bs[j]['name']); j += 1
        o, c = {'default': '()', 'implicit': '{}', 'strict': '⦃⦄'}[b['bi']]
        out.append(f'{o}{" ".join(names)} : {b["type"]}{c}')
        i = j
    return out


def wrap_binders(parts, indent='    ', width=100):
    lines, cur = [], ''
    for p in parts:
        if cur and len(cur) + 1 + len(p) > width:
            lines.append(cur); cur = indent + p
        else:
            cur = (cur + ' ' + p) if cur else p
    if cur:
        lines.append(cur)
    return '\n'.join(lines)


def indent(s, pre):
    return '\n'.join(pre + l if l else l for l in s.split('\n'))


class Vis:
    """Which project definitions a printed piece shows.  A constant of the printed expression
    counts when its last name component occurs as a token of the printed text (implicit
    arguments and instances are in the expression but not on the page)."""

    def __init__(self, D):
        self.D = D
        self.tok = {}

    def of(self, consts, text):
        key = id(text)
        toks = set(re.findall(r"[^\s()\[\]{}⦃⦄,:.↑←→∀∃λ¬∧∨=≤<≥>+*/^|·⁻¹]+", text))
        out = set()
        for k in consts:
            p = parent_of(self.D, k)
            if not p or self.D[p]['kind'] == 'theorem' or self.D[p]['kind'] == 'instance':
                continue
            if self.D[p]['userName'].rsplit('.', 1)[-1] in toks:
                out.add(p)
        return out


def stmt_vis(vis, r):
    v = vis.of(r['conclusionConsts'], r['conclusion'])
    for b in r['binders']:
        v |= vis.of(b['consts'], b['type'])
    return v


def concept_vis(vis, r):
    v = set()
    if r['form'] == 'structure':
        for b in r['params'] + r['fields']:
            v |= vis.of(b['consts'], b['type'])
    elif r['form'] == 'inductive':
        for b in r['signature']['b']:
            v |= vis.of(b['consts'], b['type'])
        for c in r['ctors']:
            for b in c['args']:
                v |= vis.of(b['consts'], b['type'])
    elif r['form'] == 'def':
        for b in r['params']:
            v |= vis.of(b['consts'], b['type'])
        v |= vis.of(r['resultConsts'], r['resultType'])
        v |= vis.of(r['bodyConsts'], r['body'])
    v.discard(r['name'])
    return v


def render_concept(D, r, ns):
    """Markdown lean block for a concept unfolded one level.  Returns (text, truncatedChars)."""
    name = rel_name(user_name(D, r['name']), ns)
    trunc = 0
    L = []
    if r['doc']:
        L.append('/-- ' + ' '.join(r['doc'].split()) + ' -/')
    if r['form'] == 'structure':
        head = ('class ' if r['isClass'] else 'structure ') + name
        ps = group_binders(r['params'])
        head = wrap_binders([head] + ps)
        if r['parents']:
            head += ' extends ' + ', '.join(rel_name(p, ns) for p in r['parents'])
        L.append(head + ' : ' + r['resultSort'] + ' where')
        for f in r['fields']:
            if f['doc']:
                L.append('  /-- ' + ' '.join(f['doc'].split()) + ' -/')
            t, cut = cap(f['type'], FIELD_CAP)
            trunc += cut
            t = indent(t, '    ').lstrip()
            L.append(f'  {f["name"]} : {t}' + (f' … [+{cut:,} characters]' if cut else ''))
    elif r['form'] == 'inductive':
        L.append(wrap_binders(['inductive ' + name] + group_binders(r['signature']['b'])) + ' : ' + r['signature']['r'])
        for c in r['ctors']:
            if c['doc']:
                L.append('  /-- ' + ' '.join(c['doc'].split()) + ' -/')
            t = wrap_binders([f'  | {c["ctor"].rsplit(".", 1)[-1]}'] + group_binders(c['args'])) + ' : ' + c['result']
            t, cut = cap(t, FIELD_CAP)
            trunc += cut
            L.append(t + (f' … [+{cut:,} characters]' if cut else ''))
    else:
        head = wrap_binders(['def ' + name] + group_binders(r['params']))
        body, cut = cap(r['body'], BODY_CAP)
        trunc += cut
        L.append(head + ' : ' + r['resultType'] + ' :=')
        L.append(indent(body, '  ') + (f' … [+{cut:,} characters]' if cut else ''))
    return '\n'.join(L), trunc


def notation_line(D, r, ns):
    name = rel_name(user_name(D, r['name']), ns)
    head = wrap_binders(['def ' + name] + group_binders(r['params']))
    body, cut = cap(' '.join(r['body'].split()), 300)
    return f'{head} : {r["resultType"]} := {body}' + (f' … [+{cut:,} characters]' if cut else ''), cut


def render_statement(D, r, ns, shared_keys):
    """Statement relative to the chapter: binders already declared for the chapter are named only."""
    name = rel_name(user_name(D, r['name']), ns)
    kind = 'theorem' if D[r['name']]['kind'] == 'theorem' else 'def'
    used = [b for b in r['binders'] if (b['name'], b['bi'], b['type']) in shared_keys]
    added = [b for b in r['binders'] if (b['name'], b['bi'], b['type']) not in shared_keys]
    sig = wrap_binders([f'{kind} {name}'] + group_binders(added))
    body = sig + ' :\n' + indent(r['conclusion'], '    ')
    body, cut = cap(body, STMT_CAP)
    if cut:
        body += f' … [+{cut:,} characters]'
    pre = ''
    if used:
        pre = '-- with ' + ' '.join(binder_ref(b) for b in used) + '\n'
    full = wrap_binders([f'{kind} {name}'] + group_binders(r['binders'])) + ' :\n' + indent(r['conclusion'], '    ')
    return pre + body, cut, len(sig) + 3 + len(r['conclusion']), len(full)


# --------------------------------------------------------------------------- assemble one outline

def build(key, cfg, D, H, succ, use_lean):
    g = G(D, H, succ, cfg['root'])
    chapters, covered = choose(g)
    chapters = pick_statements(g, chapters)
    root_ns = ns_of(D, cfg['root'])
    goal = dict(number=0, role='goal', concept=None, statements=[cfg['root']], ns=root_ns)
    closing = dict(number=len(chapters) + 1, role='closing', concept=None, statements=list(reversed(g.spine)), ns=root_ns)
    for ch in chapters:
        ch['role'] = 'concept'
        ch['ns'] = ns_of(D, ch['concept'])
        ch['statements'] = ch['construction'] + ch['consumersShown']
    allch = [goal] + chapters + ([closing] if g.spine else [])
    concepts = [ch['concept'] for ch in chapters]

    # ---- pass A: concepts and statements, printed by Lean in the chapter's namespace
    items = []
    for ch in allch:
        if ch['concept']:
            items.append(dict(name=ch['concept'], **{'as': 'concept'}, ns=ch['ns']))
        for s in ch['statements']:
            items.append(dict(name=s, **{'as': 'statement'}, ns=ch['ns']))
    PA = lean_print(key + '_a', items, use_lean)
    vis = Vis(D)
    for ch in allch:
        ch['_st'] = [PA[(s, 'statement')] for s in ch['statements']]
        ch['_vis'] = {s: stmt_vis(vis, PA[(s, 'statement')]) for s in ch['statements']}
        if ch['concept']:
            ch['_c'] = PA[(ch['concept'], 'concept')]
            ch['_cvis'] = concept_vis(vis, ch['_c'])

    # ---- supporting definitions (by rule) and notation, printed in pass B (+ notation rounds)
    known = set(concepts)
    support_of = {}
    for ch in allch:
        cnt = collections.Counter()
        for s in ch['statements']:
            for d in ch['_vis'][s]:
                if d not in known and not g.is_notation(d):
                    cnt[d] += 1
        glob = collections.Counter(d for c2 in allch for s in c2['statements'] for d in c2['_vis'][s])
        lim = GOAL_SUPPORT if ch['role'] == 'goal' else SUPPORT
        sup = [d for d, _ in sorted(cnt.items(), key=lambda kv: (-kv[1], -glob[kv[0]], kv[0]))][:lim]
        ch['support'] = sup
        for d in sup:
            support_of.setdefault(d, ch)
            known.add(d)
    for ch in allch:
        ch['support'] = [d for d in ch['support'] if support_of[d] is ch]
    printed_defs = {}                       # name -> (record, ns)
    for ch in allch:
        if ch['concept']:
            printed_defs[ch['concept']] = (ch['_c'], ch['ns'])
    itemsB = [dict(name=d, **{'as': 'concept'}, ns=ch['ns']) for ch in allch for d in ch['support']]
    notation, frontier = [], set()
    for ch in allch:
        for s in ch['statements']:
            frontier |= {d for d in ch['_vis'][s] if g.is_notation(d)}
        if ch['concept']:
            frontier |= {d for d in ch['_cvis'] if g.is_notation(d)}
    rounds = 0
    pending = itemsB
    seen_not = set()
    while True:
        new = sorted(frontier - seen_not)
        seen_not |= set(new)
        pending = pending + [dict(name=d, **{'as': 'concept'}, ns=root_ns.split('.')[0]) for d in new]
        if not pending or rounds >= NOTATION_ROUNDS:
            break
        PB = lean_print(f'{key}_b{rounds}', pending, use_lean)
        frontier = set()
        for it in pending:
            r = PB[(it['name'], 'concept')]
            printed_defs[it['name']] = (r, it['ns'])
            if g.is_notation(it['name']):
                notation.append(it['name'])
            frontier |= {d for d in concept_vis(vis, r) if g.is_notation(d)}
        pending = []
        rounds += 1
    notation_left = sorted(frontier - seen_not) + [it['name'] for it in pending]
    # a definition counts as printed only when the page shows all of it
    cut_defs = set()
    for d, (r, dns) in printed_defs.items():
        if (notation_line(D, r, dns)[1] if g.is_notation(d) else render_concept(D, r, dns)[1]):
            cut_defs.add(d)
    known = set(printed_defs) - cut_defs

    # ---- strategy edges: which chapter's construction the next one is built on
    cons_of = {ch['number']: ch['construction'][0] for ch in chapters if ch['construction']}
    if g.spine:
        cons_of[closing['number']] = g.spine[-1]
    def reach_from(n):
        seen, st = {n}, [n]
        while st:
            x = st.pop()
            for y in succ[x]:
                if y not in seen:
                    seen.add(y); st.append(y)
        return seen
    rs = {k: reach_from(v) for k, v in cons_of.items()}
    uses = {k: {j for j, v in cons_of.items() if j != k and v in rs[k]} for k in cons_of}
    direct = {k: sorted(j for j in uses[k] if not any(j in uses[m] for m in uses[k] if m != j)) for k in uses}
    for ch in allch:
        ch['buildsOn'] = direct.get(ch['number'], [])
        ch['usedBy'] = sorted(k for k, v in direct.items() if ch['number'] in v)

    # ---- visibility of every printed definition, closure inside the outline
    dvis = {d: concept_vis(vis, r) for d, (r, _) in printed_defs.items()}
    closed = set(known)
    changed = True
    while changed:
        changed = False
        for d in sorted(closed):
            if not dvis[d] <= closed:
                closed.discard(d); changed = True

    # ---- render
    md = []
    stmts_json = []
    stats = dict(lengthsRelative=[], lengthsFull=[], truncatedStatements=0)
    selfc1 = np.zeros(len(g.order), dtype=bool)
    selfc2 = np.zeros(len(g.order), dtype=bool)
    beneath = np.zeros(len(g.order), dtype=bool)
    beneath_cons = np.zeros(len(g.order), dtype=bool)
    n_l1 = n_l2 = n_counted = 0
    kn_concepts = set(concepts) - cut_defs
    kn_notation = kn_concepts | (set(notation) - cut_defs)
    stepmask = {k: np.zeros(len(g.order), dtype=bool) for k in ('none', 'concepts', 'concepts+notation')}
    stepn = collections.Counter()
    rating_pool = []
    nodes = []

    def docline(n, r):
        fs = first_sentence(r.get('doc'))
        return fs if fs else 'undocumented'

    md.append(f'# {cfg["title"]}: `{cfg["root"]}`\n')
    md.append(f'{cfg["what"]}. {len(g.R):,} declarations and proof mass {g.total:,} below it. '
              f'{len(chapters)} concept chapters, chosen by the rule in `METHOD.md`; their regions hold {covered}% of the proof mass.\n')
    md.append('| # | concept | label (corpus docstring) | constructed by | builds on | region | built beneath it | consumers |')
    md.append('|---|---|---|---|---|---|---|---|')
    for ch in chapters:
        cb = f'`{rel_name(user_name(D, ch["construction"][0]), root_ns.split(".")[0])}`' if ch['construction'] else 'no producing statement found'
        bo = ', '.join(str(x) for x in ch['buildsOn']) or '-'
        md.append(f'| {ch["number"]} | `{user_name(D, ch["concept"])}` | {docline(ch["concept"], ch["_c"])} | {cb} | {bo} | {ch["regionPct"]}% | {ch["builtPct"]}% | {ch["consumers"] + ch["consumersViaObject"]:,} |')
    if g.spine:
        md.append(f'| {closing["number"]} | closing chain | | `{rel_name(user_name(D, g.spine[-1]), root_ns.split(".")[0])}` | {", ".join(str(x) for x in closing["buildsOn"]) or "-"} | | | |')
    md.append('')
    md.append('"Builds on" lists the chapters whose constructing statement the proof of this chapter\'s constructing statement depends on, directly (dependencies already implied through another listed chapter are left out). It is read from the declaration graph.')
    md.append('')
    md.append('Chapters are in the order the headline proof uses them: by the dependency height of the statement that constructs the concept (lowest first), so a chapter never constructs something an earlier chapter\'s construction depends on. Names are printed by Lean relative to the namespace named in each chapter heading.\n')

    for ch in allch:
        ns = ch['ns']
        if ch['role'] == 'goal':
            md.append(f'## {key} · 0. The goal\n')
            md.append(f'Namespace `{ns}`. The headline theorem and the definitions its statement names.\n')
        elif ch['role'] == 'closing':
            md.append(f'## {key} · {ch["number"]}. Closing: from the last concepts to the headline\n')
            md.append(f'Namespace `{ns}`. The chain of statements each of which is the only way into the one after it and carries at least {int(SPINE_SHARE*100)}% of its proof (lowest first).\n')
        else:
            c = ch['concept']
            md.append(f'## {key} · {ch["number"]}. `{rel_name(user_name(D, c), ns.rsplit(".", 1)[0] if "." in ns else "")}`: {docline(c, ch["_c"])}\n')
            md.append(f'Namespace `{ns}` (`{D[c]["module"]}:{D[c]["line"]}`). Region {ch["regionPct"]}% of the proof mass: {ch["builtPct"]}% is built beneath statements that produce it '
                      f'({ch["producers"]} producers, {ch["objects"]} chosen objects) and it is a hypothesis of {ch["consumers"]:,} declarations'
                      + (f', used through its chosen object by {ch["consumersViaObject"]:,}' if ch['consumersViaObject'] else '') + '.\n')
            if ch['buildsOn'] or ch['usedBy']:
                md.append('Construction builds on: ' + (', '.join(f'chapter {x}' for x in ch['buildsOn']) or 'no other chapter')
                          + '. Used by the construction of: ' + (', '.join(('the closing chain' if x == closing['number'] and g.spine else f'chapter {x}') for x in ch['usedBy']) or 'no other chapter') + '.\n')
            text, cut = render_concept(D, ch['_c'], ns)
            ch['conceptText'] = text
            ch['conceptTruncated'] = cut
            md.append('**The concept, unfolded one level**\n')
            md.append('```lean\n' + text + '\n```\n')
        # supporting definitions
        ch['supportText'] = []
        if ch['support']:
            md.append('**Also unfolded here** (named by this chapter\'s statements, picked by rule)\n' if ch['role'] == 'concept' else '**Definitions named by these statements, unfolded one level**\n')
            for d in ch['support']:
                r, dns = printed_defs[d]
                text, cut = render_concept(D, r, ns)
                ch['supportText'].append(dict(name=d, text=text, truncatedChars=cut, label=docline(d, r)))
                md.append('```lean\n' + text + '\n```\n')
        # shared binders
        cnt = collections.Counter()
        first = {}
        for r in ch['_st']:
            for b in r['binders']:
                k = (b['name'], b['bi'], b['type'])
                cnt[k] += 1
                first.setdefault(k, b)
        shared = [first[k] for k in first if cnt[k] >= 2]
        shared_keys = {(b['name'], b['bi'], b['type']) for b in shared}
        ch['sharedText'] = ''
        if shared:
            ch['sharedText'] = wrap_binders(['variable'] + group_binders(shared), indent='  ')
            md.append('**Throughout this chapter**\n')
            md.append('```lean\n' + ch['sharedText'] + '\n```\n')
        # statements
        for i, s in enumerate(ch['statements']):
            r = PA[(s, 'statement')]
            text, cut, rel_len, full_len = render_statement(D, r, ns, shared_keys)
            if ch['role'] == 'concept':
                role = 'constructs' if s in ch['construction'] else 'consumes'
            else:
                role = 'headline' if s == cfg['root'] else 'closing'
            v = ch['_vis'][s]
            unknown = sorted(v - known)
            l1 = not unknown and not cut
            l2 = l1 and v <= closed
            label = docline(s, r)
            md.append(f'{ch["number"]}.{i + 1} **{role}** · {label} · `{D[s]["module"]}:{D[s]["line"]}` · {100.0 * g.dm[s] / g.total:.2f}% of the proof beneath it\n')
            md.append('```lean\n' + text + '\n```\n')
            if unknown:
                md.append('Not unfolded in this outline: ' + ', '.join(f'`{rel_name(user_name(D, u), ns)}`' for u in unknown[:12])
                          + (f' and {len(unknown) - 12} more' if len(unknown) > 12 else '') + '.\n')
            stats['lengthsRelative'].append(rel_len)
            stats['lengthsFull'].append(full_len)
            stats['truncatedStatements'] += 1 if cut else 0
            if s not in g.onspine:
                n_counted += 1
                beneath[g.sub(s)] = True
                if role == 'constructs':
                    beneath_cons[g.sub(s)] = True
                if l1:
                    n_l1 += 1; selfc1[g.sub(s)] = True
                if l2:
                    n_l2 += 1; selfc2[g.sub(s)] = True
                if v <= set(printed_defs):
                    stepn['uncut'] += 1; stepmask.setdefault('uncut', np.zeros(len(g.order), dtype=bool))[g.sub(s)] = True
                if not cut:
                    for lab, kn in (('none', set()), ('concepts', kn_concepts), ('concepts+notation', kn_notation)):
                        if v <= kn:
                            stepn[lab] += 1; stepmask[lab][g.sub(s)] = True
                # what a reader sees for this entry: chapter context + the statement
                ctx = []
                if ch.get('conceptText'):
                    ctx.append(ch['conceptText'])
                ctx += [t['text'] for t in ch['supportText']]
                if ch['sharedText']:
                    ctx.append(ch['sharedText'])
                rating_pool.append(dict(name=s, chapter=ch['number'], role=role,
                                        text='\n\n'.join(ctx + [text]), statementOnly=text))
            stmts_json.append(dict(name=s, chapter=ch['number'], role=role, label=label, kind=D[s]['kind'],
                                   module=D[s]['module'], line=D[s]['line'], text=text,
                                   binders=r['binders'], conclusion=r['conclusion'],
                                   relativeChars=rel_len, fullChars=full_len, exportChars=D[s]['statementChars'],
                                   truncatedChars=cut, dominatedMass=g.dm[s],
                                   dominatedMassPct=round(100.0 * g.dm[s] / g.total, 3),
                                   definitionsShown=sorted(v), notUnfolded=unknown,
                                   selfContainedOneLevel=l1, selfContainedClosed=l2))
            nodes.append(dict(name=s, role={'headline': 'root', 'closing': 'spine'}.get(role, 'section'),
                              level=None if role in ('headline', 'closing') else (2 if role == 'constructs' else 3),
                              sizes=dict(dominatedMass=g.dm[s])))
        if ch['concept']:
            nodes.append(dict(name=ch['concept'], role='chapter', level=1, sizes=dict(dominatedMass=int(g.massarr[g.region_mask(ch['concept'])].sum()))))
        for d in ch['support']:
            nodes.append(dict(name=d, role='toolkit', level=None, sizes=dict(dominatedMass=0)))

    # notation glossary
    md.append(f'## {key} · Notation\n')
    md.append(f'Type-valued definitions named above, each with its defining clause as Lean prints it ({len(notation)} entries; closure followed for {rounds} rounds).\n')
    nlines = []
    for d in sorted(notation, key=lambda d: user_name(D, d)):
        r, dns = printed_defs[d]
        line, _ = notation_line(D, r, dns)
        nlines.append(line)
        nodes.append(dict(name=d, role='toolkit', level=None, sizes=dict(dominatedMass=0)))
    md.append('```lean\n' + '\n'.join(nlines) + '\n```\n')
    if notation_left:
        md.append(f'{len(notation_left)} further type-valued definitions are named inside these clauses and not printed.\n')

    # ---- metrics
    top_stmts = [cfg['root']] + [ch['construction'][0] for ch in chapters if ch['construction']]
    top_defs_shown = set(concepts) | set(goal['support'])
    top_mentions = set()
    for ch in allch:
        if ch['concept']:
            top_mentions |= ch['_cvis']
        for s in ch['statements']:
            if s in top_stmts:
                top_mentions |= ch['_vis'][s]
    for d in goal['support']:
        top_mentions |= dvis[d]
    top_mentions -= top_defs_shown
    def vocabulary(names):
        seen, stack = set(), []
        for n in names:
            stack.extend(D[n]['typeDeps'])
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            d = D[x]
            stack.extend(d['typeDeps'])
            if d['kind'] != 'theorem':
                stack.extend(v for v in d['valueDeps'] if D[v]['kind'] != 'theorem')
        return {x for x in seen if D[x]['kind'] != 'theorem'}
    all_stmt = [s['name'] for s in stmts_json]
    rel = sorted(stats['lengthsRelative']); full = sorted(stats['lengthsFull'])
    med = lambda xs: xs[len(xs) // 2] if xs else 0
    metrics = dict(
        root=cfg['root'], reachable=len(g.R), totalMass=g.total, spine=g.spine,
        chapters=len(chapters), statements=len(stmts_json), conceptsUnfolded=len(concepts),
        supportingUnfolded=sum(len(ch['support']) for ch in allch), notationPrinted=len(notation),
        definitionsPrinted=len(printed_defs), definitionsPrintedInFull=len(known), notationNotPrinted=len(notation_left),
        regionsCoverMassPct=covered,
        massBeneath=dict(
            comment='union of dominated regions of the outline statements off the spine, as a share of all proof mass below the headline',
            statementsCounted=n_counted,
            allStatementsPct=round(g.pct(beneath), 2),
            constructionStatementsPct=round(g.pct(beneath_cons), 2),
            selfContainedOneLevel=dict(statements=n_l1, massPct=round(g.pct(selfc1), 2)),
            selfContainedByWhatIsPrinted=collections.OrderedDict(
                [(lab, dict(statements=stepn[lab], massPct=round(g.pct(stepmask[lab]), 2))) for lab in ('none', 'concepts', 'concepts+notation')]
                + [('concepts+notation+supporting', dict(statements=n_l1, massPct=round(g.pct(selfc1), 2)))]),
            selfContainedIfNothingWereCutForDisplay=dict(statements=stepn['uncut'], massPct=round(g.pct(stepmask['uncut']), 2) if 'uncut' in stepmask else 0.0),
            selfContainedClosed=dict(statements=n_l2, massPct=round(g.pct(selfc2), 2))),
        statementChars=dict(relativeMedian=med(rel), relativeMax=rel[-1], relativeOver1000=sum(1 for x in rel if x > 1000),
                            fullMedian=med(full), fullMax=full[-1], fullOver1000=sum(1 for x in full if x > 1000),
                            exportMedianSameStatements=med(sorted(x['exportChars'] for x in stmts_json)),
                            sharedBinderSavingPct=round(100.0 * (1 - sum(rel) / max(1, sum(full))), 1),
                            truncatedInDisplay=stats['truncatedStatements']),
        conceptChars=dict(median=med(sorted(len(ch['conceptText']) for ch in chapters)),
                          max=max(len(ch['conceptText']) for ch in chapters),
                          truncated=sum(1 for ch in chapters if ch['conceptTruncated'])),
        topLevel=dict(
            comment='top level = the headline statement, each chapter concept unfolded one level, and each chapter\'s first construction statement',
            statements=len(top_stmts),
            definitionsUnfolded=len(top_defs_shown),
            furtherDefinitionsNamed=len(top_mentions),
            furtherOfWhichPrintedElsewhereInOutline=len(top_mentions & known),
            furtherNotPrinted=len(top_mentions - known),
            mustReadToFollowTopLevel=len(top_defs_shown) + len(top_mentions),
            fullUnfoldingClosure=len(vocabulary(top_stmts) | set().union(*[vocabulary([c]) | {c} for c in concepts]))),
        wholeOutline=dict(definitionsNamedByStatements=len(set().union(*[set(s['definitionsShown']) for s in stmts_json])),
                          ofWhichPrinted=len(set().union(*[set(s['definitionsShown']) for s in stmts_json]) & known),
                          fullUnfoldingClosure=len(vocabulary(all_stmt))),
        definitionsClosedInsideOutline=len(closed),
    )
    out = dict(root=cfg['root'], paper=cfg['what'], totalMass=g.total, reachable=len(g.R), spine=g.spine,
               summary=metrics, nodes=nodes,
               chapters=[dict(number=ch['number'], role=ch['role'], concept=ch['concept'], namespace=ch['ns'],
                              label=(docline(ch['concept'], ch['_c']) if ch['concept'] else None),
                              conceptText=ch.get('conceptText'), conceptRecord=ch.get('_c'),
                              supporting=ch['supportText'], shared=ch['sharedText'],
                              statements=ch['statements'],
                              **{k: ch[k] for k in ('pick', 'gainPct', 'regionPct', 'builtPct', 'cellPct', 'producers', 'objects',
                                                    'consumers', 'consumersViaObject', 'construction', 'consumersShown', 'buildsOn', 'usedBy',
                                                    'producedOnSpine', 'orderKey', 'orderBy') if k in ch})
                         for ch in allch],
               statements=stmts_json,
               notation=[dict(name=d, text=notation_line(D, *printed_defs[d])[0]) for d in sorted(notation)])
    ranking = []
    for ch in allch:
        if ch['concept']:
            ranking.append(ch['concept'])
        ranking += ch['support'] + ch['statements']
    ranking += sorted(notation)
    seen = set()
    ranking = [n for n in ranking if not (n in seen or seen.add(n))]
    return dict(md='\n'.join(md), json=out, metrics=metrics, ranking=ranking, rating_pool=rating_pool, g=g,
                contributions=contributions(g, chapters, stmts_json))


def contributions(g, chapters, stmts):
    """What each design step contributed, in numbers."""
    return dict(
        step1_concepts=dict(candidates=len(g.cands), chosen=len(chapters),
                            documented=sum(1 for ch in chapters if ch['_c'].get('doc')),
                            kinds=dict(collections.Counter(ch['_c']['form'] for ch in chapters)),
                            fieldsShown=sum(len(ch['_c'].get('fields', [])) for ch in chapters),
                            fieldsWithDocstring=sum(1 for ch in chapters for f in ch['_c'].get('fields', []) if f.get('doc'))),
        step2_statements=dict(construction=sum(1 for s in stmts if s['role'] == 'constructs'),
                              consumers=sum(1 for s in stmts if s['role'] == 'consumes'),
                              chaptersWithoutConstruction=sum(1 for ch in chapters if not ch['construction']),
                              chaptersWithSharedBinders=sum(1 for ch in chapters if ch['sharedText']),
                              statementsDocumented=sum(1 for s in stmts if s['label'] != 'undocumented')),
        step3_order=dict(byConstruction=sum(1 for ch in chapters if ch['orderBy'] == 'construction'),
                         byFirstConsumer=sum(1 for ch in chapters if ch['orderBy'] != 'construction')))


# --------------------------------------------------------------------------- old outline, same yardsticks

def old_outline_metrics(D, H, succ, key, old):
    o = old['outlines'][key]
    g = G(D, H, succ, o['root'])
    res = {}
    for label, pick in (('level1', lambda n: n['role'] == 'chapter'), ('allEntries', lambda n: n['role'] in ('chapter', 'section'))):
        ns_ = [n for n in o['nodes'] if pick(n)]
        b = np.zeros(len(g.order), dtype=bool); s = np.zeros(len(g.order), dtype=bool); k = 0
        for n in ns_:
            d = D[n['name']]
            b[g.sub(n['name'])] = True
            toks = set(re.findall(r"[^\s()\[\]{}⦃⦄,:↑←→∀∃λ¬∧∨=≤<≥>+*/^|·⁻¹]+", d['statement']))
            shown = [t for t in d['typeDeps'] if D[t]['kind'] not in ('theorem', 'instance') and D[t]['userName'] in toks]
            if not shown and not d['statementTruncated']:
                k += 1; s[g.sub(n['name'])] = True
        res[label] = dict(statements=len(ns_), massBeneathPct=round(g.pct(b), 2),
                          namingNoProjectDefinition=dict(statements=k, massPct=round(g.pct(s), 2)))
    chars = sorted(D[n['name']]['statementChars'] for n in o['nodes'] if n['role'] in ('chapter', 'section'))
    res['statementChars'] = dict(median=chars[len(chars) // 2], max=chars[-1], over1000=sum(1 for c in chars if c > 1000))
    res['handRated'] = o['summary'].get('level1SkipByReadabilityMassPct')
    res['level1VocabularyDefinitions'] = o['summary'].get('level1VocabularyDefinitions')
    res['vocabularyDirect'] = o['summary'].get('vocabularyDirect')
    res['vocabularyDefinitions'] = o['summary'].get('vocabularyDefinitions')
    return res


# --------------------------------------------------------------------------- paper ground truth

def paper_scores(built, old):
    truth = PT.load_truth()
    PD = PT.load_decls()
    nb = PT.neighbours(PD)
    res = {}
    for key, cfg in ROOTS.items():
        paper = cfg['paper']
        names = sorted(n for n, d in PD.items() if d['module'].split('.')[0] == PT.ROOT[paper])
        b = built[key]
        g = b['g']
        res[key] = {}
        for mc in ('guess', 'probable', 'certain'):
            tg = PT.targets(truth, paper, mc)
            below = sum(1 for ts in tg.values() if ts & g.R)
            new = PT.score(b['ranking'], tg, nb, depths=[20, 50, 100])
            parts = collections.OrderedDict()
            j = b['json']
            concept_names = [c['concept'] for c in j['chapters'] if c['concept']]
            cons_names = [s['name'] for s in j['statements'] if s['role'] == 'constructs']
            other = [s['name'] for s in j['statements'] if s['role'] not in ('constructs',)]
            sup = [t['name'] for c in j['chapters'] for t in c['supporting']]
            nota = [n['name'] for n in j['notation']]
            lv = PT.score_levels([('concepts', concept_names), ('+ construction statements', cons_names),
                                  ('+ headline, closing and consumer statements', other),
                                  ('+ supporting definitions', sup), ('+ notation', nota)], tg, nb)
            oldlv = PT.outline_levels(old['outlines'][key])
            oldrep = PT.score_levels(oldlv, tg, nb)
            oldflat = PT.score(oldrep['ranked'], tg, nb, depths=[20, 50, 100])
            rr = PT.random_reference(names, tg, nb, [len(b['ranking'])])
            hits = sorted(i for i, fr in new['firstRanks'].items() if fr['exact'] is not None)
            oldhits = sorted(i for i, fr in oldflat['firstRanks'].items() if fr['exact'] is not None)
            res[key][mc] = dict(items=len(tg), itemsWithTargetBelowHeadline=below,
                                outline2=dict(listed=new['listed'], rows=new['rows'], levels=lv['rows'], exactItems=hits),
                                dominatorOutline=dict(listed=oldflat['listed'], rows=oldflat['rows'], levels=oldrep['rows'], exactItems=oldhits),
                                exactOnlyOutline2=sorted(set(hits) - set(oldhits)), exactOnlyDominator=sorted(set(oldhits) - set(hits)),
                                randomSameLength=rr['rows'][0])
    return res


# --------------------------------------------------------------------------- rating items

def rating_items(built, old, D):
    rng = random.Random(RATING_SEED)
    items = []
    rule = ('For each of the two outlines and each of the two papers, %d entries drawn without replacement by '
            'random.Random(%d) from all eligible entries, in the order: outline2 ns_r3, outline2 euler_compact, '
            'dominator ns_r3, dominator euler_compact; then all 60 shuffled by the same generator. Eligible, '
            'outline2: every statement off the spine (not the headline or closing chain). Eligible, dominator outline: '
            'every node with role chapter or section in out/corpus/outline/outline.json. Text, outline2: the chapter '
            'context a reader has on the page (concept unfolded one level, supporting definitions, shared variables) '
            'followed by the statement, exactly as in OUTLINE2.md. Text, dominator outline: the full name, kind and the '
            'statement trimmed as OUTLINE.md prints it (whitespace collapsed, %d characters); mass figures and the '
            'hand ratings are left out because they would reveal the source and prime the rating.'
            % (RATING_PER_CELL, RATING_SEED, O1.TRIM))
    for key in ROOTS:
        pool = sorted(built[key]['rating_pool'], key=lambda e: e['name'])
        for e in rng.sample(pool, RATING_PER_CELL):
            items.append(dict(text='```lean\n' + e['text'] + '\n```', statementOnly=e['statementOnly'],
                              hidden=dict(source='outline2', key=key, name=e['name'], chapter=e['chapter'], role=e['role'])))
    for key in ROOTS:
        pool = sorted((n for n in old['outlines'][key]['nodes'] if n['role'] in ('chapter', 'section')), key=lambda n: n['name'])
        for n in rng.sample(pool, RATING_PER_CELL):
            text = f'`{O1.short(n["name"])}` ({n["kind"]})\n```lean\n{O1.trim(n["statement"])}\n```'
            items.append(dict(text=text, statementOnly=O1.trim(n['statement']),
                              hidden=dict(source='dominator', key=key, name=n['name'], role=n['role'], level=n['level'])))
    rng.shuffle(items)
    for i, it in enumerate(items):
        it['id'] = 'R%02d' % (i + 1)
    return dict(schema='rating-items/1', seed=RATING_SEED, rule=rule,
                note='`hidden` must be removed before the items are shown to a rater; `text` is what the rater sees. '
                     '`textStatementOnly` is the same entry without its chapter context, for a second arm that isolates the effect of the context. '
                     'The two formats differ visibly (context block, relative names), so a rater can guess the source; '
                     'the rating is blind to the label, not to the format.',
                counts=dict(collections.Counter((it['hidden']['source'], it['hidden']['key']) and f"{it['hidden']['source']}:{it['hidden']['key']}" for it in items)),
                items=[dict(id=it['id'], text=it['text'], textStatementOnly=it['statementOnly'], hidden=it['hidden']) for it in items])


# --------------------------------------------------------------------------- main

def main():
    if '--test' in sys.argv:
        selftest()
        return
    use_lean = '--no-lean' not in sys.argv
    os.makedirs(LEAN, exist_ok=True)
    D = load_decls()
    H = load_heads()
    succ = {n: sorted(set(d['typeDeps']) | set(d['valueDeps'])) for n, d in D.items()}
    with open(OLD) as f:
        old = json.load(f)
    built = collections.OrderedDict()
    for key, cfg in ROOTS.items():
        built[key] = build(key, cfg, D, H, succ, use_lean)
        print(key, json.dumps(built[key]['metrics'], indent=1, ensure_ascii=False))
    scores = paper_scores(built, old) if '--no-score' not in sys.argv else None
    oldm = {key: old_outline_metrics(D, H, succ, key, old) for key in ROOTS}
    params = dict(K_CHAPTERS=K_CHAPTERS, PER_CHAPTER=PER_CHAPTER, SUPPORT=SUPPORT, GOAL_SUPPORT=GOAL_SUPPORT,
                  SPINE_SHARE=SPINE_SHARE, FIELD_CAP=FIELD_CAP, BODY_CAP=BODY_CAP, STMT_CAP=STMT_CAP,
                  NOTATION_ROUNDS=NOTATION_ROUNDS, RATING_SEED=RATING_SEED, RATING_PER_CELL=RATING_PER_CELL)
    with open(os.path.abspath(__file__), 'rb') as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    metrics = dict(script='bench/outline2.py', scriptSha256=digest, parameters=params,
                   outlines={k: b['metrics'] for k, b in built.items()},
                   contributions={k: b['contributions'] for k, b in built.items()},
                   dominatorOutlineSameYardsticks=oldm, paperTruth=scores)
    with open(os.path.join(OUT, 'metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, 'outline2.json'), 'w') as f:
        json.dump(dict(schema='outline2/1', corpus='openai/NavierStokesAndEuler@f9e8bc5b',
                       method='definition-centred outline; see out/corpus/outline2/METHOD.md',
                       massDefinition='proofSize + auxProofSize', parameters=params,
                       roles=dict(root='headline theorem', spine='closing chain', chapter='concept (structure or predicate)',
                                  section='statement: level 2 constructs the concept, level 3 consumes it',
                                  toolkit='supporting definition or notation unfolded in the outline'),
                       outlines={k: b['json'] for k, b in built.items()}), f, indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, 'rating_items.json'), 'w') as f:
        json.dump(rating_items(built, old, D), f, indent=1, ensure_ascii=False)
    head = ['# Definition-centred outline of the machine Navier-Stokes and Euler proofs', '',
            'Generated by `python3 bench/outline2.py` from the Lean export and from text printed by Lean (`corpora/outline2/Outline2.lean`). '
            'Every `lean` block below is Lean\'s own pretty-printer output, re-assembled; labels are the corpus\'s docstrings, and "undocumented" means there is none. '
            'Apart from the one-line caption naming each headline theorem (`ROOTS` in `bench/outline2.py`), no sentence of mathematical narrative was written by the builder. Method, measurements and limits: `METHOD.md`; numbers: `metrics.json`.', '',
            'How to read a chapter: the concept is shown with its fields or defining clause unfolded one level; "Throughout this chapter" declares the variables and hypotheses that two or more of the chapter\'s statements share; '
            'each statement then shows only what it adds (`-- with F W` names the shared ones it uses). "constructs" marks the statement that produces the concept, "consumes" a statement that takes it as a hypothesis or uses its chosen object. '
            '`… [+n characters]` marks text cut for display; the full text is in `outline2.json`.', '']
    with open(os.path.join(OUT, 'OUTLINE2.md'), 'w') as f:
        f.write('\n'.join(head) + '\n' + '\n\n'.join(b['md'] for b in built.values()) + '\n')
    print(json.dumps(dict(contributions=metrics['contributions'], old=oldm), indent=1, ensure_ascii=False))
    if scores:
        for key in scores:
            for mc in scores[key]:
                s = scores[key][mc]
                print(key, mc, 'items', s['items'], 'outline2', s['outline2']['rows'][-1], 'dominator', s['dominatorOutline']['rows'][-1], 'random', s['randomSameLength'])


if __name__ == '__main__':
    main()
