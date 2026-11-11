#!/usr/bin/env python3
"""M9 families, step 2: clusters at each looseness level, generalisations, triage score.

  cluster.py <project> [--all] [--planted]

  --all      cluster every exported definition (not only those reachable from the headline theorems);
             used for the cloned-module control.  Output goes to clusters_all.jsonl / summary_all.json.
  --planted  the synthetic controls (raw/planted.jsonl, features from `features.py <p> --planted`).

Channels
  L0..L3   equal body key at looseness 0..3 (see tree.Renderer); `+sig` also equal signature key
  AU@t     anti-unification: greedy agglomeration; a cluster is kept together while every member keeps
           at least a share t of its nodes outside COMPOUND holes (holes filled only by leaves or heads
           are free, so AU@1.0 contains L3)
  API@k    parallel lemma families: every member has the same >= k statement shapes proved about it
           (the definition replaced by a hole, other project constants by numbered holes, numerals abstracted)
  APIL@k   the same with constants standing as arguments also abstracted to typed holes
  ROLE@t   (types excluded) parallel lemma ROLES (tree.role: how many hypotheses mention the definition, the head of the
           conclusion, the library operations around the definition): at least 3 roles common to all
           members and  weight(roles common to all) / weight(roles of any member) >= t, weights = idf
  AUxAPI   both: AU@0.7 link and >= 2 common statement shapes
  WRAP     a definition and the definitions whose body is that definition applied to arguments
"""
import sys, os, json, pickle, collections, math, time
import numpy as np
import scipy.sparse as sp
sys.setrecursionlimit(100000)
from tree import (size, lgg, skel_size, lost_mass, is_leaf_filler, free_bvars, filler_kind, pretty, Renderer, short)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '..', '..')
AU_LEVELS = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]
API_LEVELS = [8, 5, 3, 2]
ROLE_LEVELS = [0.5, 0.35, 0.25, 0.15]
DFCAP = 300
TOPK = 60
MAXC = 250          # a cluster of more distinct bodies than this is not grown further by AU
TRIVIAL = 4         # a shared skeleton below this many nodes is flagged "trivial"


def tclass(f):
    return 'Prop' if f['rtag'] == 'Prop' else 'U' if f['rtag'] == 'U' else 'val'


# ------------------------------------------------------------------ candidate neighbours for AU

def labels(t, isproj, out):
    """bag of node labels and parent/child edges, project heads abstracted"""
    if isinstance(t, str):
        return '*'
    k = t[0]
    if k == 'A':
        h = t[2]
        if isinstance(h, str):
            hl = 'v' if h[0] in '$#' else ('?P' if isproj(h) else h)
        else:
            hl = labels(h, isproj, out)
        lab = 'A:' + hl
        kids = [labels(a, isproj, out) for a in t[3:]]
    elif k == 'Q':
        lab = 'Q'
        kids = [labels(t[2], isproj, out), labels(t[3], isproj, out)]
    elif k in ('L', 'I', 'K'):
        lab = k
        kids = [labels(a, isproj, out) for a in t[1:]]
    elif k in ('C', 'N', 'V', 'B'):
        lab = k
        kids = []
    else:
        lab = k
        kids = []
    out[lab] += 1
    for i, c in enumerate(kids):
        if c != '*':
            out[lab + '>' + str(min(i, 6)) + '>' + c] += 1
    return lab


def neighbours(items, isproj, topk=TOPK):
    vocab = {}
    rows, cols, vals = [], [], []
    for i, it in enumerate(items):
        bag = collections.Counter()
        labels(it['body'], isproj, bag)
        for w, c in bag.items():
            j = vocab.setdefault(w, len(vocab))
            rows.append(i); cols.append(j); vals.append(1 + math.log(c))
    X = sp.csr_matrix((vals, (rows, cols)), shape=(len(items), len(vocab)), dtype=np.float32)
    df = np.asarray((X > 0).sum(axis=0)).ravel()
    idf = np.log((1 + len(items)) / (1 + df)) + 1
    X = X.multiply(idf).tocsr()
    nrm = np.sqrt(np.asarray(X.multiply(X).sum(axis=1)).ravel())
    nrm[nrm == 0] = 1
    X = sp.diags(1 / nrm) @ X
    XT = X.T.tocsr()
    pairs = set()
    n = len(items)
    for s in range(0, n, 1000):
        S = (X[s:s + 1000] @ XT).toarray()
        for r in range(S.shape[0]):
            i = s + r
            S[r, i] = -1
            k = min(topk, n - 1)
            if k <= 0:
                continue
            idx = np.argpartition(-S[r], k - 1)[:k]
            for j in idx:
                if S[r, j] > 0.2:
                    j = int(j)
                    pairs.add((i, j) if i < j else (j, i))
    return pairs


def cluster_sim(bodies):
    """(similarity, generalisation, holes): similarity = min over members of the share of its nodes
    that is outside compound holes"""
    g, holes = lgg(bodies)
    hl = sorted(holes, key=lambda k: holes[k])
    sim = 1.0
    for j, b in enumerate(bodies):
        n = max(size(b), 1)
        sim = min(sim, 1 - min(lost_mass(hl, j), n) / n)
    return sim, g, hl


class UF:
    def __init__(self, n):
        self.p = list(range(n))
        self.m = [[i] for i in range(n)]

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return a
        if len(self.m[a]) < len(self.m[b]):
            a, b = b, a
        self.p[b] = a
        self.m[a] += self.m[b]
        self.m[b] = None
        return a


def au_clusters(items, scored_pairs, theta):
    """greedy agglomeration over distinct bodies; pairs in descending similarity"""
    uf = UF(len(items))
    for s, i, j in scored_pairs:
        if s < theta:
            break
        a, b = uf.find(i), uf.find(j)
        if a == b:
            continue
        mem = uf.m[a] + uf.m[b]
        if len(mem) > MAXC:
            continue
        if len(mem) > 2:
            sim, _, _ = cluster_sim([items[x]['body'] for x in mem])
            if sim < theta:
                continue
        uf.union(a, b)
    return [m for m in uf.m if m is not None]


def dist(clusters_sizes):
    """definitions in clusters of size >= 2, 3, 5, 10; number of clusters; largest"""
    out = {}
    for k in (2, 3, 5, 10):
        out[f'>={k}'] = sum(s for s in clusters_sizes if s >= k)
    out['clusters'] = sum(1 for s in clusters_sizes if s >= 2)
    out['largest'] = max(clusters_sizes) if clusters_sizes else 0
    return out


def main():
    proj = sys.argv[1]
    ALL = '--all' in sys.argv
    planted = '--planted' in sys.argv
    O = os.path.join(REPO, 'out', 'families', proj)
    P = pickle.load(open(os.path.join(O, 'planted.pkl' if planted else 'features.pkl'), 'rb'))
    F = P['feats']
    projnames = set(P['projnames'])
    _pc = {}

    def isproj(n):
        v = _pc.get(n)
        if v is None:
            v = False
            p = n
            while True:
                if p in projnames:
                    v = True
                    break
                i = p.rfind('.')
                if i < 0:
                    break
                p = p[:i]
            _pc[n] = v
        return v

    D = [f for f in F.values() if (ALL or f['reach'])]
    D.sort(key=lambda f: f['name'])
    N = len(D)
    sfxk = '_all' if ALL else ''
    apik, apiLk, rolek = 'api' + sfxk, 'apiL' + sfxk, 'roles' + sfxk
    byname = {f['name']: f for f in D}
    for f in D:
        f['_thms'] = {t for v in f[rolek].values() for t in v}
    summary = collections.OrderedDict()
    summary['definitions clustered'] = N

    def clean(a, b, pk):
        """keys of a's profile carried by at least one theorem that does not also mention b
        (a statement that mentions both is co-occurrence, not a parallel lemma)"""
        common = a['_thms'] & b['_thms']
        if not common:
            return set(a[pk])
        return {k for k, v in a[pk].items() if any(t not in common for t in v)}
    t0 = time.time()

    found = []   # (channel, level, [names])

    # ---------------- exact keys
    summary['levels'] = collections.OrderedDict()
    for l in range(4):
        g = collections.defaultdict(list)
        g2 = collections.defaultdict(list)
        for f in D:
            g[(tclass(f), f['bk'][l])].append(f['name'])
            g2[(f['bk'][l], f['sk'][l])].append(f['name'])
        summary['levels'][f'L{l}'] = dist([len(v) for v in g.values()])
        summary['levels'][f'L{l}+sig'] = dist([len(v) for v in g2.values()])
        nt = [len(v) for v in g.values() if byname[v[0]]['nodes'] >= TRIVIAL]
        summary['levels'][f'L{l} (body ≥ {TRIVIAL} nodes)'] = dist(nt)
        for v in g.values():
            if len(v) >= 2:
                found.append(('body', f'L{l}', v))

    # ---------------- anti-unification
    uniq = collections.OrderedDict()
    for f in D:
        uniq.setdefault((tclass(f), f['bk'][0]), []).append(f['name'])
    items = [{'body': byname[v[0]]['body'], 'names': v, 'cls': k[0], 'nodes': byname[v[0]]['nodes']} for k, v in uniq.items()]
    summary['distinct bodies (level 0)'] = len(items)
    pairs = neighbours(items, isproj) if len(items) > 1 else set()
    # all pairs inside one L3 bucket are candidates too (chain them)
    b3 = collections.defaultdict(list)
    for i, it in enumerate(items):
        b3[(it['cls'], byname[it['names'][0]]['bk'][3])].append(i)
    for v in b3.values():
        for a, b in zip(v, v[1:]):
            pairs.add((a, b))
    scored = []
    for i, j in pairs:
        a, b = items[i], items[j]
        if a['cls'] != b['cls']:
            continue
        if min(a['nodes'], b['nodes']) < 0.4 * max(a['nodes'], b['nodes']):
            continue
        sim, g, hl = cluster_sim([a['body'], b['body']])
        if sim >= min(AU_LEVELS):
            scored.append((sim, i, j))
    scored.sort(key=lambda x: (-x[0], x[1], x[2]))
    summary['AU candidate pairs (top-%d neighbours by label/edge cosine)' % TOPK] = len(pairs)
    summary['AU pairs with similarity ≥ %.1f' % min(AU_LEVELS)] = len(scored)
    au_pairs = {}
    for s, i, j in scored:
        if s >= 0.7:
            for x in items[i]['names']:
                for y in items[j]['names']:
                    au_pairs[(x, y) if x < y else (y, x)] = s
    for it in items:   # definitions with the same body are AU-linked too
        nm = it['names']
        if 2 <= len(nm) <= 80:
            for x in range(len(nm)):
                for y in range(x + 1, len(nm)):
                    au_pairs[(nm[x], nm[y]) if nm[x] < nm[y] else (nm[y], nm[x])] = 1.0
    for th in AU_LEVELS:
        cl = au_clusters(items, scored, th)
        groups = [[n for x in m for n in items[x]['names']] for m in cl]
        summary['levels'][f'AU@{th}'] = dist([len(g) for g in groups])
        nt = []
        for m, g in zip(cl, groups):
            if len(g) >= 2:
                _, gg, _ = cluster_sim([items[x]['body'] for x in m]) if len(m) > 1 else (1, items[m[0]]['body'], [])
                if skel_size(gg) >= TRIVIAL:
                    nt.append(len(g))
        summary['levels'][f'AU@{th} (shared skeleton ≥ {TRIVIAL} nodes)'] = dist(nt)
        if th in (1.0, 0.7, 0.5):
            for g in groups:
                if len(g) >= 2:
                    found.append(('body', f'AU@{th}', g))
    print('AU done', round(time.time() - t0), 's', flush=True)

    # ---------------- API profiles (exact statement shapes; leaf-abstracted shapes)
    idx = {f['name']: i for i, f in enumerate(D)}
    summary['api'] = collections.OrderedDict()
    keydf = {}

    def shape_channel(pk, label, levels, tag):
        df = collections.Counter()
        inv = collections.defaultdict(list)
        for f in D:
            for k in f[pk]:
                df[k] += 1
                inv[k].append(f['name'])
        keydf[pk] = df
        summary['api'][f'{label}: distinct shapes'] = len(df)
        summary['api'][f'{label}: shapes held by ≥ 2 definitions'] = sum(1 for v in df.values() if v >= 2)
        summary['api'][f'{label}: definitions with ≥ 1 shape shared with another definition'] = sum(
            1 for f in D if any(df[k] >= 2 for k in f[pk]))
        summary['api'][f'{label}: most widely held shape, definitions'] = max(df.values()) if df else 0
        shared = collections.Counter()
        for k, v in inv.items():
            if 2 <= len(v) <= DFCAP:
                for a in range(len(v)):
                    for b in range(a + 1, len(v)):
                        shared[(v[a], v[b])] += 1
        prs = sorted(((len(clean(byname[a], byname[b], pk) & clean(byname[b], byname[a], pk)), a, b) for (a, b) in shared),
                     key=lambda x: (-x[0], x[1], x[2]))
        summary['api'][f'{label}: pairs sharing ≥ 1 shape held by ≤ {DFCAP} definitions'] = len(prs)
        for kmin in levels:
            uf = UF(N)
            core = {}
            for c, a, b in prs:
                if c < kmin:
                    break
                ra, rb = uf.find(idx[a]), uf.find(idx[b])
                if ra == rb:
                    continue
                cc = (core.get(ra) or set(D[ra][pk])) & (core.get(rb) or set(D[rb][pk]))
                if len(cc) < kmin:
                    continue
                core[uf.union(ra, rb)] = cc
            groups = [[D[x]['name'] for x in m] for m in uf.m if m is not None and len(m) >= 2]
            summary['levels'][f'{tag}@{kmin}'] = dist([len(g) for g in groups])
            for g in groups:
                found.append(('api', f'{tag}@{kmin}', g))
        return prs

    api_pairs = shape_channel(apik, 'exact statement shape', API_LEVELS, 'API')
    shape_channel(apiLk, 'leaf-abstracted statement shape', API_LEVELS, 'APIL')

    # ---------------- lemma roles
    rdf = collections.Counter()
    rinv = collections.defaultdict(list)
    for f in D:
        for k in f[rolek]:
            rdf[k] += 1
            rinv[k].append(f['name'])
    keydf[rolek] = rdf
    nwith = max(1, sum(1 for f in D if f[rolek]))
    idf = {k: math.log(1 + nwith / v) for k, v in rdf.items()}
    summary['api']['roles: distinct'] = len(rdf)
    summary['api']['roles: held by ≥ 2 definitions'] = sum(1 for v in rdf.values() if v >= 2)
    summary['api']['roles: most widely held, definitions'] = max(rdf.values()) if rdf else 0
    shared = collections.Counter()
    for k, v in rinv.items():
        if 2 <= len(v) <= DFCAP:
            for a in range(len(v)):
                for b in range(a + 1, len(v)):
                    shared[(v[a], v[b])] += 1

    def w(ks):
        return sum(idf[k] for k in ks)
    rsim = {}
    for (a, b), c in shared.items():
        if c < 3 or tclass(byname[a]) == 'U' or tclass(byname[b]) == 'U':
            continue   # a type is "mentioned" by every theorem that quantifies over it: roles say nothing
        ka, kb = clean(byname[a], byname[b], rolek), clean(byname[b], byname[a], rolek)
        cm = ka & kb
        if len(cm) < 3:
            continue
        rsim[(a, b) if a < b else (b, a)] = w(cm) / w(ka | kb)
    rprs = sorted(((v, a, b) for (a, b), v in rsim.items()), key=lambda x: (-x[0], x[1], x[2]))
    summary['api']['roles: pairs with ≥ 3 common roles (statements that mention both not counted)'] = len(rprs)
    for th in ROLE_LEVELS:
        uf = UF(N)
        for s_, a, b in rprs:
            if s_ < th:
                break
            ra, rb = uf.find(idx[a]), uf.find(idx[b])
            if ra == rb:
                continue
            ok = True
            for x in uf.m[ra]:
                for y in uf.m[rb]:
                    nx, ny = D[x]['name'], D[y]['name']
                    if rsim.get((nx, ny) if nx < ny else (ny, nx), 0) < 0.6 * th:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                uf.union(ra, rb)
        groups = [[D[x]['name'] for x in m] for m in uf.m if m is not None and len(m) >= 2]
        summary['levels'][f'ROLE@{th}'] = dist([len(g) for g in groups])
        for g in groups:
            found.append(('role', f'ROLE@{th}', g))

    # ---------------- API x body
    both = sorted(((c, a, b) for (c, a, b) in api_pairs if c >= 2 and ((a, b) in au_pairs)),
                  key=lambda x: (-x[0], x[1], x[2]))
    uf = UF(N)
    core = {}
    for c, a, b in both:
        ra, rb = uf.find(idx[a]), uf.find(idx[b])
        if ra == rb:
            continue
        cc = (core.get(ra) or set(D[ra][apik])) & (core.get(rb) or set(D[rb][apik]))
        if len(cc) < 2:
            continue
        mem = uf.m[ra] + uf.m[rb]
        if len(mem) <= 60:
            sim, _, _ = cluster_sim([D[x]['body'] for x in mem])
            if sim < 0.7:
                continue
        core[uf.union(ra, rb)] = cc
    groups = [[D[x]['name'] for x in m] for m in uf.m if m is not None and len(m) >= 2]
    summary['levels']['AU@0.7 x API@2'] = dist([len(g) for g in groups])
    for g in groups:
        found.append(('body+api', 'AU@0.7xAPI@2', g))
    # ---------------- wrappers (specialisations)
    wr = collections.defaultdict(list)
    for f in D:
        if f['wraps'] and f['wraps'] in byname and f['wraps'] != f['name']:
            wr[f['wraps']].append(f['name'])
    groups = [[k] + v for k, v in wr.items() if len(v) >= 2]
    summary['levels']['WRAP (a definition and ≥ 2 specialisations of it)'] = dist([len(g) for g in groups])
    wrapbase = {}
    for g in groups:
        found.append(('wrap', 'WRAP', g))
        wrapbase[tuple(sorted(g))] = g[0]
    print('API done', round(time.time() - t0), 's', flush=True)

    # ---------------- family records: one per distinct member set
    bymem = collections.OrderedDict()
    for ch, lv, g in found:
        key = tuple(sorted(g))
        if lv not in bymem.setdefault(key, []):
            bymem[key].append(lv)
    cooc = P['cooc']
    recs = []
    for key, lvs in bymem.items():
        mem = [byname[n] for n in key]
        m = len(mem)
        base = wrapbase.get(key)
        # generalisation over distinct bodies (cap for very large clusters); for a WRAP family, over the
        # specialisations (the base is the generalisation that already exists)
        ub = collections.OrderedDict()
        for f in mem:
            if f['name'] != base:
                ub.setdefault(f['bk'][0], f)
        reps = list(ub.values())[:80]
        sim, g, hl = cluster_sim([f['body'] for f in reps])
        root_hole = (not isinstance(g, str)) and g[0] == '?'
        holes = []
        for hid, fill in enumerate(hl):
            kinds = collections.Counter(filler_kind(x) for x in fill)
            dep = any((not is_leaf_filler(x)) and free_bvars(x) for x in fill) or any(
                (not isinstance(x, str)) and x[0] == 'B' for x in fill)
            part = collections.defaultdict(list)
            for j, x in enumerate(fill):
                part[x].append(j)
            holes.append({'id': hid + 1, 'kinds': dict(kinds), 'kind': kinds.most_common(1)[0][0] if len(kinds) == 1 else 'mixed',
                          'distinct': len(part), 'dependsOnBound': dep,
                          'compound': not all(is_leaf_filler(x) for x in fill),
                          'partition': tuple(sorted(tuple(v) for v in part.values())),
                          'fill': [pretty(x, f['pnames'], limit=160) for x, f in zip(fill, reps)]})
        parts = {h['partition'] for h in holes}
        eff = len(parts)
        joint = len({tuple(h['fill'][j] for h in holes) for j in range(len(reps))}) if holes else 1
        maxd = max((h['distinct'] for h in holes), default=1)
        for h in holes:
            del h['partition']
        users = set()
        nstmt = 0
        for f in mem:
            users |= set(f['users'])
            nstmt += f['nstmt']
        users -= set(key)
        co = sum(cooc.get((a, b), 0) for i, a in enumerate(key) for b in key[i + 1:]) if m <= 80 else None

        tcount = collections.Counter(t for f in mem for t in f['_thms'])

        def family(pk, cap=None, conservative=False):
            # statements that mention two or more members are left out: they are not parallel lemmas
            kc = collections.defaultdict(dict)
            for f in mem:
                for k, v in f[pk].items():
                    v = [t for t in v if tcount[t] == 1]
                    if v:
                        kc[k][f['name']] = v
            sh = {k: v for k, v in kc.items() if len(v) >= 2 and (cap is None or keydf[pk][k] <= cap)}
            corek = [k for k, v in sh.items() if len(v) == m]
            tot = sum(len(t) for v in sh.values() for t in v.values())
            if conservative:   # one lemma per further member and role
                red = sum((len(v) - 1) * min(len(t) for t in v.values()) for v in sh.values())
            else:
                red = sum(sum(len(t) for t in v.values()) - max(len(t) for t in v.values()) for v in sh.values())
            return sh, corek, tot, red
        sharedk, corek, lem_total, lem_red = family(apik)
        rshared, rcore, rtot, rred = family(rolek, cap=max(40, 3 * m + 20), conservative=True)
        all_lem = sum(len(t) for f in mem for t in f[apik].values())
        tight = min((l for l in ('L0', 'L1', 'L2', 'L3') if l in lvs), default=None)
        if tight is None:
            au = [float(x[3:]) for x in lvs if x.startswith('AU@') and 'x' not in x]
            tight = f'AU@{max(au)}' if au else lvs[0]
        nho = sum(1 for h in holes if h['dependsOnBound'])
        ncomp = sum(1 for h in holes if h['compound'])
        sk = 0 if root_hole else skel_size(g)
        low = (m - 1) + lem_red
        if all(tclass(f) == 'U' for f in mem):
            rred = 0           # roles are not meaningful for a family of types
        high = (m - 1) + max(lem_red, rred)
        if base is not None:
            pen = 2.0          # the general form exists; the specialisations are named instances of it
        elif root_hole or sim < 0.5:
            pen = 5.0          # no common body: an interface (structure / class) would be needed
        else:
            pen = 1 + eff + 0.5 * nho + 0.5 * ncomp
        score = high / pen
        top_keys = sorted(sharedk.items(), key=lambda kv: (-len(kv[1]), keydf[apik][kv[0]], kv[0]))[:12]
        top_roles = sorted(rshared.items(), key=lambda kv: (-len(kv[1]), rdf[kv[0]], kv[0]))[:14]
        recs.append({
            'members': list(key), 'm': m, 'levels': lvs, 'tightest': tight, 'wrapBase': base,
            'kinds': dict(collections.Counter(f['kind'] for f in mem)),
            'resultClass': dict(collections.Counter(tclass(f) for f in mem)),
            'modules': len({f['module'] for f in mem}),
            'instanceParams': [min(f['pk'].count('i') for f in mem), max(f['pk'].count('i') for f in mem)],
            'typeParams': [min(f['pk'].count('t') for f in mem), max(f['pk'].count('t') for f in mem)],
            'skeleton': None if root_hole else pretty(g, None, limit=1500),
            'skeletonNodes': sk, 'similarity': round(sim, 3), 'distinctBodies': len(ub), 'lggOver': len(reps),
            'holes': holes, 'nHoles': len(holes), 'effectiveParams': eff, 'jointDistinct': joint, 'maxDistinct': maxd,
            'independent': (joint > maxd) if len(holes) > 1 else None,
            'higherOrderHoles': nho, 'compoundHoles': ncomp,
            'users': len(users), 'stmtMentions': nstmt, 'cooccurInStatements': co,
            'sharedShapes': len(sharedk), 'coreShapes': len(corek), 'lemmasInSharedShapes': lem_total,
            'lemmaReduction': lem_red, 'lemmasAboutMembers': all_lem,
            'sharedRoles': len(rshared), 'coreRoles': len(rcore), 'lemmasInSharedRoles': rtot, 'roleReduction': rred,
            'conceptReductionLow': low, 'conceptReductionHigh': high, 'penalty': pen, 'score': round(score, 2),
            'trivialSkeleton': sk < TRIVIAL,
            'parallel': [{'shape': k, 'heldByDefinitionsOverall': keydf[apik][k],
                          'thms': {n: t[:3] for n, t in v.items()}} for k, v in top_keys],
            'parallelRoles': [{'role': k, 'heldByDefinitionsOverall': rdf[k],
                               'thms': {n: t[:3] for n, t in v.items()}} for k, v in top_roles],
            'memberInfo': [{'name': f['name'], 'kind': f['kind'], 'module': f['module'], 'nodes': f['nodes'],
                            'nstmt': f['nstmt'], 'users': len(f['users']), 'pp': f['pp'][:300],
                            'body': f['ppBody'][:300] or pretty(f['body'], f['pnames'], limit=300)} for f in mem[:60]],
            'repNames': [f['name'] for f in reps],
        })
    recs.sort(key=lambda r: (-r['score'], r['members'][0]))
    for i, r in enumerate(recs):
        r['id'] = f'F{i + 1:05d}'
    sfx = '_planted' if planted else ('_all' if ALL else '')
    with open(os.path.join(O, f'clusters{sfx}.jsonl'), 'w') as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + '\n')
    summary['family records (distinct member sets over all channels)'] = len(recs)
    # exact duplicates by kind of definition, and theorems with a parallel twin
    g0 = collections.defaultdict(list)
    for f in D:
        g0[(tclass(f), f['bk'][0])].append(f)
    dup = collections.Counter()
    for (c, _), v in g0.items():
        if len(v) >= 2:
            dup[{'U': 'type', 'Prop': 'proposition', 'val': 'value or function'}[c]] += len(v) - 1
    summary['exact duplicates removable (members − 1), by kind'] = dict(dup)
    summary['definitions by result class'] = dict(collections.Counter(
        {'U': 'type', 'Prop': 'proposition', 'val': 'value or function'}[tclass(f)] for f in D))
    twin = set()
    for f in D:
        for k, v in f[apik].items():
            if keydf[apik][k] >= 2:
                twin.update(v)
    summary['theorems with a statement shape (some definition holed) also proved about another definition'] = len(twin)
    summary['reachable theorems profiled'] = len({t for f in D for t in f['_thms']})
    json.dump(summary, open(os.path.join(O, f'summary{sfx}.json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(summary['api'], indent=1, ensure_ascii=False))
    for k, v in summary['levels'].items():
        print(f'{k:48s} {v}')
    print('total', round(time.time() - t0), 's')


if __name__ == '__main__':
    main()
