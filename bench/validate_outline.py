#!/usr/bin/env python3
"""H3 validation: do graph-structure scores predict which declarations humans put in the blueprint?

Reads   out/corpus/<corpus>/{decls.jsonl,blueprint.json,axioms.json}   (data exported from Lean)
Writes  out/corpus/validation/{results.json,tables.md,scores_<corpus>.csv,examples_<corpus>.json}

Usage:  python3 bench/validate_outline.py [--boot 1000] [--corpora pfr carleson]

No Lean is invoked. Everything is deterministic given --seed.
"""
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import argparse, csv, json, math, os, sys, collections
import numpy as np
import networkx as nx
from scipy.stats import rankdata
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedGroupKFold

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "out", "corpus", "validation")
STAGING = (".Mathlib.", ".ForMathlib.", ".ToMathlib.", ".Tactic.", ".Examples.")
ROOT = "__ROOT__"


def is_mainline(module):
    m = "." + module + "."
    return not any(s in m for s in STAGING)


# ----------------------------------------------------------------------------- graph features
def load(corpus):
    d = os.path.join(REPO, "out", "corpus", corpus)
    decls = [json.loads(l) for l in open(os.path.join(d, "decls.jsonl"))]
    bp = json.load(open(os.path.join(d, "blueprint.json")))
    roots = list(json.load(open(os.path.join(d, "axioms.json"))).keys())
    return decls, bp, roots


def build(decls, roots):
    names = [d["name"] for d in decls]
    idx = {n: i for i, n in enumerate(names)}
    G = nx.DiGraph()
    G.add_nodes_from(names)
    for d in decls:
        for b in set(d["typeDeps"]) | set(d["valueDeps"]):
            if b in idx and b != d["name"]:
                G.add_edge(d["name"], b)
    # `mutual` blocks give genuine 2-cycles (Carleson has two); everything below tolerates cycles
    roots = [r for r in roots if r in idx]
    return G, idx, roots


def features(decls, G, idx, roots):
    n = len(decls)
    names = [d["name"] for d in decls]
    mass = {d["name"]: d["proofSize"] + d.get("auxProofSize", 0) for d in decls}
    # dominator tree from a virtual root that uses every headline theorem
    H = G.copy()
    H.add_node(ROOT)
    for r in roots:
        H.add_edge(ROOT, r)
    idom = nx.immediate_dominators(H, ROOT)
    reach = set(idom) - {ROOT}
    children = collections.defaultdict(list)
    for v, p in idom.items():
        if v != p:
            children[p].append(v)
    depth = {ROOT: 0}
    order = [ROOT]
    for v in order:
        for c in children[v]:
            depth[c] = depth[v] + 1
            order.append(c)
    dom_mass = {}
    dom_cnt = {}
    for v in reversed(order):
        dom_mass[v] = mass.get(v, 0) + sum(dom_mass[c] for c in children[v])
        dom_cnt[v] = 1 + sum(dom_cnt[c] for c in children[v])
    # transitive mass / descendant count through bitsets in reverse topological order
    C = nx.condensation(G)
    cbits = {}
    for c in reversed(list(nx.topological_sort(C))):
        b = 0
        for v in C.nodes[c]["members"]:
            b |= 1 << idx[v]
        for w in C.successors(c):
            b |= cbits[w]
        cbits[c] = b
    bits = {v: cbits[C.graph["mapping"][v]] for v in names}
    mass_arr = np.array([mass[x] for x in names], dtype=np.int64)
    trans_mass = {}
    trans_cnt = {}
    for v in names:
        b = bits[v]
        ids = [i for i in range(n) if (b >> i) & 1]
        trans_cnt[v] = len(ids)
        trans_mass[v] = int(mass_arr[ids].sum())
    pr_used = nx.pagerank(G, alpha=0.85)            # rank flows from user to used: "library" rank
    pr_user = nx.pagerank(G.reverse(), alpha=0.85)  # rank flows from used to user: "top-level" rank
    F = []
    maxdepth = max(depth.values())
    for d in decls:
        v = d["name"]
        r = v in reach
        dm = dom_mass[v] if r else 0
        un = d["userName"]
        F.append(dict(
            name=v, userName=un, module=d["module"], kind=d["kind"], line=d["line"],
            reachable=int(r),
            dom_mass=dm,
            dom_mass_excl=(dm - mass[v]) if r else 0,
            dom_count=(dom_cnt[v] - 1) if r else 0,
            nontrivial_dom=int(r and dom_cnt[v] > 1),
            dom_depth=depth[v] if r else maxdepth + 1,
            trans_mass=trans_mass[v],
            trans_count=trans_cnt[v] - 1,
            proof_size=mass[v],
            in_degree=G.in_degree(v),
            out_degree=G.out_degree(v),
            pagerank_used=pr_used[v],
            pagerank_user=pr_user[v],
            statement_size=d["statementSize"],
            statement_dag_size=d["statementDagSize"],
            dom_mass_per_stmt=dm / max(1, d["statementSize"]),
            dom_mass_per_stmt_dag=dm / max(1, d["statementDagSize"]),
            has_docstring=int(d["hasDocstring"]),
            non_private=int(not d["isPrivate"]),
            name_len=len(un),
            name_parts=un.count(".") + 1,
            src_lines=(d["endLine"] - d["line"] + 1) if d.get("line") and d.get("endLine") else 1,
            stmt_chars=len(d["statement"]),
            mainline=int(is_mainline(d["module"])),
            is_root=int(v in roots),
        ))
    return F, idom, bits


# ----------------------------------------------------------------------------- metrics
def p_at_k(y, s, k, tie):
    o = np.lexsort((tie, -s))[:k]
    hits = y[o].sum()
    return hits / k, hits / max(1, y.sum())


def metrics(y, s, k, tie):
    p, r = p_at_k(y, s, k, tie)
    return np.array([roc_auc_score(y, s), average_precision_score(y, s), p, r])


def boot_metrics(y, S, k, B, rng, groups):
    """S: dict name -> score array. Same resamples for every score (paired). Returns point + CI.
    Module-cluster bootstrap: whole modules are resampled with replacement, because blueprint
    theorems cluster by file. The intervals cover test-set sampling only; fitted models are held fixed."""
    n = len(y)
    tie = rng.permutation(n)
    point = {m: metrics(y, s, k, tie) for m, s in S.items()}
    samples = {m: np.empty((B, 4)) for m in S}
    ug, inv = np.unique(groups, return_inverse=True)
    members = [np.where(inv == g)[0] for g in range(len(ug))]
    for b in range(B):
        while True:
            ii = np.concatenate([members[g] for g in rng.integers(0, len(ug), len(ug))])
            yy = y[ii]
            if 0 < yy.sum() < len(ii):
                break
        for m, s in S.items():
            samples[m][b] = metrics(yy, s[ii], k, tie[ii])
    res = {}
    for m in S:
        lo, hi = np.percentile(samples[m], [2.5, 97.5], axis=0)
        res[m] = dict(auc=point[m][0], ap=point[m][1], p_at_k=point[m][2], r_at_k=point[m][3],
                      auc_ci=[lo[0], hi[0]], ap_ci=[lo[1], hi[1]],
                      p_ci=[lo[2], hi[2]], r_ci=[lo[3], hi[3]])
    return res, samples


SCORES = [  # (label, key, sign, group)
    ("(a) dominated proof mass (incl. own)", "dom_mass", 1),
    ("(a') dominated proof mass (excl. own)", "dom_mass_excl", 1),
    ("(b) is nontrivial dominator", "nontrivial_dom", 1),
    ("(b) dominator-tree depth (deeper = higher)", "dom_depth", 1),
    ("(b) dominator-tree depth (shallower = higher)", "dom_depth", -1),
    ("(c) transitive proof mass beneath", "trans_mass", 1),
    ("(d) own proof size", "proof_size", 1),
    ("(e) in-degree (users)", "in_degree", 1),
    ("(e) PageRank, rank flows to used decls", "pagerank_used", 1),
    ("(e) PageRank, rank flows to users", "pagerank_user", 1),
    ("(f) statement size, negated", "statement_size", -1),
    ("(f') statement size", "statement_size", 1),
    ("(g) dominated mass / statement size", "dom_mass_per_stmt", 1),
    ("(g') dominated mass / statement DAG size", "dom_mass_per_stmt_dag", 1),
    ("(h) has docstring", "has_docstring", 1),
    ("(h) non-private", "non_private", 1),
    ("(h) short name (neg. length)", "name_len", -1),
    ("(h') long name", "name_len", 1),
    ("(s) source lines of the declaration", "src_lines", 1),
    ("(x) reachable from headline theorems", "reachable", 1),
    ("(x) out-degree", "out_degree", 1),
    ("(i) random", "random", 1),
]

BASE = ["proof_size", "trans_mass", "trans_count", "in_degree", "out_degree", "pagerank_used",
        "pagerank_user", "statement_size", "statement_dag_size", "reachable"]
DOM = ["dom_mass", "dom_mass_excl", "dom_count", "nontrivial_dom", "dom_depth",
       "dom_mass_per_stmt", "dom_mass_per_stmt_dag"]
SURF = ["has_docstring", "non_private", "name_len", "name_parts"]
SURF_NODOC = ["non_private", "name_len", "name_parts"]
LENGTH = ["src_lines", "stmt_chars"]
SIZE = ["src_lines", "proof_size", "statement_size"]
LOGF = {"proof_size", "trans_mass", "trans_count", "in_degree", "out_degree", "pagerank_used",
        "pagerank_user", "statement_size", "statement_dag_size", "dom_mass", "dom_mass_excl",
        "dom_count", "dom_mass_per_stmt", "dom_mass_per_stmt_dag", "name_len", "src_lines", "stmt_chars"}
MODELS = [
    ("graph baselines (c,d,e,f)", BASE),
    ("dominator features only (a,b,g)", DOM),
    ("graph baselines + dominator", BASE + DOM),
    ("surface cues only (h)", SURF),
    ("surface + graph baselines", SURF + BASE),
    ("surface + graph baselines + dominator", SURF + BASE + DOM),
    ("size only (source lines, own proof size, statement size)", SIZE),
    ("surface cues without docstring", SURF_NODOC),
    ("surface + length (source lines, statement chars)", SURF + LENGTH),
    ("surface + length + graph baselines", SURF + LENGTH + BASE),
]


def matrix(F, keys):
    X = np.array([[f[k] for k in keys] for f in F], dtype=float)
    for j, k in enumerate(keys):
        if k in LOGF:
            x = X[:, j]
            X[:, j] = np.log1p(x) if k not in ("pagerank_used", "pagerank_user") else np.log(x)
    return X


def lr():
    return make_pipeline(StandardScaler(),
                         LogisticRegressionCV(Cs=[0.01, 0.03, 0.1, 0.3, 1.0], cv=3,
                                              scoring="roc_auc", max_iter=2000, class_weight="balanced"))


def oof(X, y, groups, make, seeds):
    """Out-of-fold scores, folds grouped by module (a file never straddles train and test)."""
    acc = np.zeros(len(y))
    for s in seeds:
        cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=s)
        for tr, te in cv.split(X, y, groups):
            m = make()
            m.fit(X[tr], y[tr])
            p = m.predict_proba(X[te])[:, 1]
            acc[te] += p
    return acc / len(seeds)


# ----------------------------------------------------------------------------- structure
def structure(decls, bp, G, idx, idom, bits):
    names = [d["name"] for d in decls]
    node_decls = {}
    for i, nd in enumerate(bp):
        ds = [r["decl"] for r in nd.get("leanResolved", []) if r.get("status") == "exported" and r.get("decl") in idx]
        if nd.get("label") and ds:
            node_decls[nd["label"]] = ds
    labels = sorted(node_decls)
    L = {l: i for i, l in enumerate(labels)}
    m = len(labels)
    Hd = np.zeros((m, m), bool)
    Hs = np.zeros((m, m), bool)   # statement uses only
    for nd in bp:
        a = nd.get("label")
        if a not in L:
            continue
        for b in nd.get("uses", []):
            if b in L and b != a:
                Hd[L[a], L[b]] = True
                Hs[L[a], L[b]] = True
        for b in nd.get("proofUses", []):
            if b in L and b != a:
                Hd[L[a], L[b]] = True
    # blueprint transitive closure is taken over ALL labelled nodes, then restricted
    BG = nx.DiGraph()
    for nd in bp:
        if nd.get("label"):
            BG.add_node(nd["label"])
            for b in list(nd.get("uses", [])) + list(nd.get("proofUses", [])):
                if b != nd["label"]:
                    BG.add_edge(nd["label"], b)
    Ht = np.zeros((m, m), bool)
    for a in labels:
        for b in nx.descendants(BG, a):
            if b in L:
                Ht[L[a], L[b]] = True
    tagged = {}
    for l, ds in node_decls.items():
        for d in ds:
            tagged.setdefault(d, set()).add(l)
    Ld = np.zeros((m, m), bool)
    Lr = np.zeros((m, m), bool)
    Lc = np.zeros((m, m), bool)
    Lda = np.zeros((m, m), bool)   # B strictly dominated by A (any ancestor)
    Ldp = np.zeros((m, m), bool)   # A holds the nearest tagged strict dominator of B
    for a, ds in node_decls.items():
        own = set(ds)
        for d in ds:
            for w in G.successors(d):
                for b in tagged.get(w, ()):
                    Ld[L[a], L[b]] = True
            bset = bits[d]
            for w, ls in tagged.items():
                if w not in own and (bset >> idx[w]) & 1:
                    for b in ls:
                        Lr[L[a], L[b]] = True
            # contracted reachability: paths whose interior holds no tagged declaration
            seen = {d}
            st = [d]
            while st:
                v = st.pop()
                for w in G.successors(v):
                    if w in seen:
                        continue
                    seen.add(w)
                    if w in tagged and w not in own:
                        for b in tagged[w]:
                            Lc[L[a], L[b]] = True
                    else:
                        st.append(w)
    for b, ds in node_decls.items():
        for d in ds:
            if d not in idom:
                continue
            v = idom[d]
            first = True
            while v != ROOT:
                if v in tagged:
                    for a in tagged[v]:
                        Lda[L[a], L[b]] = True
                        if first:
                            Ldp[L[a], L[b]] = True
                    first = False
                if idom[v] == v:
                    break
                v = idom[v]
    for M in (Hd, Hs, Ht, Ld, Lr, Lc, Lda, Ldp):
        np.fill_diagonal(M, False)

    def pr(Lm, Hm):
        tp = int((Lm & Hm).sum())
        return dict(lean_edges=int(Lm.sum()), human_edges=int(Hm.sum()), both=tp,
                    precision=tp / max(1, int(Lm.sum())), recall=tp / max(1, int(Hm.sum())))
    out = dict(blueprint_nodes_with_decl=m, ordered_pairs=m * (m - 1),
               human_direct_edges=int(Hd.sum()), human_statement_edges=int(Hs.sum()),
               human_closure_edges=int(Ht.sum()),
               density_direct=float(Hd.sum() / (m * (m - 1))), density_closure=float(Ht.sum() / (m * (m - 1))),
               comparisons={})
    for nm, Lm in [("Lean direct dependency", Ld), ("Lean contracted reachability (no tagged decl in between)", Lc),
                   ("Lean reachability (transitive)", Lr), ("dominator tree: nearest tagged ancestor", Ldp),
                   ("dominator tree: any tagged ancestor", Lda)]:
        out["comparisons"][nm] = {"vs human direct \\uses": pr(Lm, Hd), "vs human \\uses closure": pr(Lm, Ht)}
    # reverse direction sanity: human edge A uses B but Lean has A reachable FROM B
    out["human_direct_edges_reversed_in_lean"] = int((Hd & Lr.T & ~Lr).sum())
    out["human_direct_edges_unrelated_in_lean"] = int((Hd & ~Lr.T & ~Lr).sum())
    # dominator parent defined at all?
    out["nodes_with_tagged_dom_ancestor"] = int(Ldp.any(axis=0).sum())
    out["nodes_reachable"] = int(sum(any(d in idom for d in ds) for ds in node_decls.values()))
    return out


def docstring_diag(corpus, decls, tagged):
    """Diagnostic only (the one place source text is read): does the docstring above a theorem cite the
    blueprint or paper numbering ("Lemma 3.2", "blueprint", "Proposition 2.0.1", "(7.2.3)")?"""
    import re
    pat = re.compile(r"blueprint|\\b(Lemma|Theorem|Proposition|Corollary|Definition|Section|Equation|Eq\.?)\s*\(?\d+(\.\d+)*|\(\d+\.\d+(\.\d+)*\)", re.I)
    cache = {}
    out = {k: dict(n=0, with_docstring=0, cites=0) for k in ("tagged", "untagged")}
    for d in decls:
        if d["kind"] != "theorem":
            continue
        k = "tagged" if d["name"] in tagged else "untagged"
        out[k]["n"] += 1
        if not d["hasDocstring"]:
            continue
        out[k]["with_docstring"] += 1
        path = os.path.join(REPO, "corpora", corpus, d["module"].replace(".", "/") + ".lean")
        if path not in cache:
            try:
                cache[path] = open(path, encoding="utf-8").read().split("\n")
            except OSError:
                cache[path] = None
        src = cache[path]
        if src is None:
            continue
        # the declaration range starts at the docstring or at the keyword; scan back to the opening /--
        j = d["line"] - 1
        lo = j
        while lo > 0 and "/--" not in src[lo] and j - lo < 60:
            lo -= 1
        hi = j
        while hi < len(src) - 1 and "-/" not in src[hi] and hi - j < 60:
            hi += 1
        text = "\n".join(src[lo:hi + 1])
        if pat.search(text):
            out[k]["cites"] += 1
    return out


# ----------------------------------------------------------------------------- main
def fmt(v, ci):
    return f"{v:.3f} [{ci[0]:.3f}, {ci[1]:.3f}]"


def run(corpus, B, seed, md):
    rng = np.random.default_rng(seed)
    decls, bp, roots = load(corpus)
    G, idx, roots = build(decls, roots)
    F, idom, bits = features(decls, G, idx, roots)
    tagged = set()
    for nd in bp:
        for r in nd.get("leanResolved", []):
            if r.get("status") == "exported" and r.get("decl") in idx:
                tagged.add(r["decl"])
    rnd = rng.random(len(F))
    for f, x in zip(F, rnd):
        f["tagged"] = int(f["name"] in tagged)
        f["random"] = float(x)
    nbp = len(bp)
    R = dict(corpus=corpus, declarations=len(F), edges=G.number_of_edges(), roots=roots,
             reachable=int(sum(f["reachable"] for f in F)), blueprint_nodes=nbp, tagged_decls=len(tagged),
             nontrivial_dominators=int(sum(f["nontrivial_dom"] for f in F)),
             tagged_roots=int(sum(1 for r in roots if r in tagged)), sets={}, models={}, structure={})
    md.append(f"\n# {corpus}\n")
    md.append(f"{len(F)} declarations, {G.number_of_edges()} edges, {len(roots)} headline roots, "
              f"{R['reachable']} reachable, {R['nontrivial_dominators']} nontrivial dominators, "
              f"{len(tagged)} blueprint-tagged declarations, {nbp} blueprint nodes (k = {nbp}).\n")

    thm = np.array([f["kind"] == "theorem" for f in F])
    tag = np.array([f["tagged"] == 1 for f in F])
    main = np.array([f["mainline"] == 1 for f in F])
    reach = np.array([f["reachable"] == 1 for f in F])
    sets = [
        ("T-all: all theorems", thm),
        ("T-main: theorems outside staging folders", thm & main),
        ("T-main-reach: mainline theorems reachable from the headline theorems", thm & main & reach),
        ("SPEC: tagged declarations of any kind + untagged theorems", thm | tag),
    ]
    y_all = tag.astype(int)
    oofs = {}
    for sname, mask in sets:
        ii = np.where(mask)[0]
        Fs = [F[i] for i in ii]
        y = y_all[ii]
        k = min(nbp, len(ii))
        S = {lab: sign * np.array([f[key] for f in Fs], dtype=float) for lab, key, sign in SCORES}
        groups = np.array([f["module"] for f in Fs])
        res, samp1 = boot_metrics(y, S, k, B, rng, groups)
        key = sname.split(":")[0]
        A_ = "(a) dominated proof mass (incl. own)"
        pd_ = {}
        for other in ["(c) transitive proof mass beneath", "(d) own proof size", "(x) out-degree",
                      "(e) PageRank, rank flows to users", "(h) has docstring",
                      "(s) source lines of the declaration", "(i) random"]:
            dd = samp1[A_] - samp1[other]
            lo, hi = np.percentile(dd, [2.5, 97.5], axis=0)
            pd_[other] = dict(d_auc=res[A_]["auc"] - res[other]["auc"], d_auc_ci=[lo[0], hi[0]],
                              d_ap=res[A_]["ap"] - res[other]["ap"], d_ap_ci=[lo[1], hi[1]])
        R["sets"][key] = dict(description=sname, n=len(ii), positives=int(y.sum()), prevalence=float(y.mean()),
                              k=k, scores=res, dom_mass_minus=pd_)
        md.append(f"\n## {corpus} / {sname}\n")
        md.append(f"n = {len(ii)}, positives = {int(y.sum())} ({100*y.mean():.1f}%), k = {k}. "
                  f"95% bootstrap intervals, {B} resamples of whole modules (test-set sampling only).\n")
        md.append("| score | ROC-AUC | average precision | precision@k | recall@k |")
        md.append("|---|---|---|---|---|")
        for lab, _, _ in SCORES:
            r = res[lab]
            md.append(f"| {lab} | {fmt(r['auc'], r['auc_ci'])} | {fmt(r['ap'], r['ap_ci'])} | "
                      f"{fmt(r['p_at_k'], r['p_ci'])} | {fmt(r['r_at_k'], r['r_ci'])} |")
        md.append("\n| (a) dominated mass minus ... (paired) | dAUC | dAP |")
        md.append("|---|---|---|")
        for other, d in pd_.items():
            md.append(f"| {other} | {d['d_auc']:+.3f} [{d['d_auc_ci'][0]:+.3f}, {d['d_auc_ci'][1]:+.3f}] | "
                      f"{d['d_ap']:+.3f} [{d['d_ap_ci'][0]:+.3f}, {d['d_ap_ci'][1]:+.3f}] |")
        # ---- models
        if key == "SPEC":
            continue
        groups = np.array([f["module"] for f in Fs])
        P = {}
        for mname, keys in MODELS:
            P["LR: " + mname] = oof(matrix(Fs, keys), y, groups, lr, seeds=[0, 1, 2])
        for mname, keys in [MODELS[0], MODELS[2]]:
            P["GBT: " + mname] = oof(matrix(Fs, keys), y, groups,
                                     lambda: HistGradientBoostingClassifier(max_depth=3, max_iter=150,
                                                                            learning_rate=0.05, random_state=0),
                                     seeds=[0])
        res, samp = boot_metrics(y, P, k, B, rng, groups)
        deltas = {}
        for a, b in [("LR: graph baselines + dominator", "LR: graph baselines (c,d,e,f)"),
                     ("LR: surface + graph baselines + dominator", "LR: surface + graph baselines"),
                     ("LR: surface + graph baselines", "LR: surface cues only (h)"),
                     ("LR: surface + graph baselines + dominator", "LR: surface cues only (h)"),
                     ("LR: graph baselines (c,d,e,f)", "LR: size only (source lines, own proof size, statement size)"),
                     ("LR: graph baselines (c,d,e,f)", "LR: surface cues without docstring"),
                     ("LR: graph baselines (c,d,e,f)", "LR: surface cues only (h)"),
                     ("LR: surface + length + graph baselines", "LR: surface + length (source lines, statement chars)"),
                     ("GBT: graph baselines + dominator", "GBT: graph baselines (c,d,e,f)")]:
            d = samp[a] - samp[b]
            lo, hi = np.percentile(d, [2.5, 97.5], axis=0)
            deltas[f"{a}  minus  {b}"] = dict(
                d_auc=res[a]["auc"] - res[b]["auc"], d_auc_ci=[lo[0], hi[0]],
                d_ap=res[a]["ap"] - res[b]["ap"], d_ap_ci=[lo[1], hi[1]],
                d_p=res[a]["p_at_k"] - res[b]["p_at_k"], d_p_ci=[lo[2], hi[2]])
        R["models"][key] = dict(scores=res, deltas=deltas)
        oofs[key] = (ii, P)
        md.append(f"\n### {corpus} / {key}: models, out-of-fold (5 folds grouped by module)\n")
        md.append("| model | ROC-AUC | average precision | precision@k | recall@k |")
        md.append("|---|---|---|---|---|")
        for mname in P:
            r = res[mname]
            md.append(f"| {mname} | {fmt(r['auc'], r['auc_ci'])} | {fmt(r['ap'], r['ap_ci'])} | "
                      f"{fmt(r['p_at_k'], r['p_ci'])} | {fmt(r['r_at_k'], r['r_ci'])} |")
        md.append("\n| paired difference | dAUC | dAP | dP@k |")
        md.append("|---|---|---|---|")
        for nm, d in deltas.items():
            md.append(f"| {nm} | {d['d_auc']:+.3f} [{d['d_auc_ci'][0]:+.3f}, {d['d_auc_ci'][1]:+.3f}] | "
                      f"{d['d_ap']:+.3f} [{d['d_ap_ci'][0]:+.3f}, {d['d_ap_ci'][1]:+.3f}] | "
                      f"{d['d_p']:+.3f} [{d['d_p_ci'][0]:+.3f}, {d['d_p_ci'][1]:+.3f}] |")

    # coefficients of the full-sample graph model (for reading, not for evaluation)
    ii = np.where(thm)[0]
    keys = BASE + DOM
    pipe = make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=2000, class_weight="balanced"))
    pipe.fit(matrix([F[i] for i in ii], keys), y_all[ii])
    R["coefficients_T_all_graph"] = dict(zip(keys, [float(c) for c in pipe[-1].coef_[0]]))

    # ---- structure
    R["structure"] = structure(decls, bp, G, idx, idom, bits)
    st = R["structure"]
    md.append(f"\n## {corpus} / structure: Lean graph restricted to blueprint nodes vs blueprint \\uses\n")
    md.append(f"{st['blueprint_nodes_with_decl']} blueprint nodes with an exported declaration; "
              f"{st['human_direct_edges']} direct \\uses edges among them "
              f"({st['human_statement_edges']} from statements), {st['human_closure_edges']} in the transitive closure; "
              f"chance precision = edge density = {st['density_direct']:.4f} (direct), {st['density_closure']:.4f} (closure).\n")
    md.append("| Lean relation (A -> B) | edges | vs direct \\uses: precision | recall | vs \\uses closure: precision | recall |")
    md.append("|---|---|---|---|---|---|")
    for nm, c in st["comparisons"].items():
        a, b = c["vs human direct \\uses"], c["vs human \\uses closure"]
        md.append(f"| {nm} | {a['lean_edges']} | {a['precision']:.3f} | {a['recall']:.3f} | {b['precision']:.3f} | {b['recall']:.3f} |")
    md.append(f"\nOf the {st['human_direct_edges']} human edges, {st['human_direct_edges_reversed_in_lean']} run the other way in Lean "
              f"and {st['human_direct_edges_unrelated_in_lean']} join declarations with no Lean dependency in either direction. "
              f"{st['nodes_with_tagged_dom_ancestor']} of {st['nodes_reachable']} reachable blueprint nodes have any tagged dominator ancestor.\n")

    # ---- single-root sensitivity of the dominated-mass score
    R["single_root"] = {}
    md.append(f"\n## {corpus} / root sensitivity: dominated proof mass computed from ONE headline theorem\n")
    md.append("| root | reachable declarations | AUC, all theorems | AUC, theorems reachable from that root | positives reachable |")
    md.append("|---|---|---|---|---|")
    mass = {d["name"]: d["proofSize"] + d.get("auxProofSize", 0) for d in decls}
    thm_i = np.where(thm)[0]
    for r0 in ["(virtual root over all)"] + roots:
        if r0.startswith("("):
            idm = idom
        else:
            idm = nx.immediate_dominators(G, r0)
        ch = collections.defaultdict(list)
        for v, pp in idm.items():
            if v != pp:
                ch[pp].append(v)
        top = ROOT if r0.startswith("(") else r0
        order = [top]
        for v in order:
            order.extend(ch[v])
        dmm = {}
        for v in reversed(order):
            dmm[v] = mass.get(v, 0) + sum(dmm[c] for c in ch[v])
        sc = np.array([dmm.get(F[i]["name"], 0) for i in thm_i], dtype=float)
        yy = y_all[thm_i]
        inr = np.array([F[i]["name"] in dmm for i in thm_i])
        a_all = roc_auc_score(yy, sc)
        a_in = roc_auc_score(yy[inr], sc[inr]) if 0 < yy[inr].sum() < inr.sum() else float("nan")
        R["single_root"][r0] = dict(reachable=len(order) - (1 if top == ROOT else 0), auc_all=a_all, auc_reachable=a_in,
                                    positives_reachable=int(yy[inr].sum()), theorems_reachable=int(inr.sum()))
        md.append(f"| {r0} | {R['single_root'][r0]['reachable']} | {a_all:.3f} | {a_in:.3f} | {int(yy[inr].sum())} of {int(yy.sum())} |")

    R["docstring_diagnostic"] = docstring_diag(corpus, decls, tagged)
    dd = R["docstring_diagnostic"]
    md.append(f"\n## {corpus} / docstring contamination diagnostic (source text, diagnostic only)\n")
    md.append("| theorems | n | with docstring | docstring cites the blueprint/paper (regex) |")
    md.append("|---|---|---|---|")
    for kk in ("tagged", "untagged"):
        md.append(f"| {kk} | {dd[kk]['n']} | {dd[kk]['with_docstring']} | {dd[kk]['cites']} |")
    # ---- files
    cols = list(F[0].keys())
    ii, P = oofs["T-all"]
    g = dict(zip(ii.tolist(), P["LR: graph baselines + dominator"]))
    s = dict(zip(ii.tolist(), P["LR: surface + graph baselines + dominator"]))
    with open(os.path.join(OUT, f"scores_{corpus}.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols + ["oof_graph", "oof_all"])
        for i, f in enumerate(F):
            w.writerow([f[c] for c in cols] + [g.get(i, ""), s.get(i, "")])
    # examples: theorems, ranked by the out-of-fold graph-only model and by dominated mass
    byname = {d["name"]: d for d in decls}
    def card(i, sc):
        f = F[i]; d = byname[f["name"]]
        return dict(name=f["userName"], module=f["module"], line=f["line"], score=float(sc), tagged=f["tagged"],
                    reachable=f["reachable"], mainline=f["mainline"], has_docstring=f["has_docstring"],
                    proof_size=f["proof_size"], dom_mass=f["dom_mass"], dom_count=f["dom_count"],
                    dom_depth=f["dom_depth"], trans_mass=f["trans_mass"], in_degree=f["in_degree"],
                    out_degree=f["out_degree"], statement_size=f["statement_size"],
                    statement=d["statement"][:600])
    ex = {}
    order = sorted(ii.tolist(), key=lambda i: -g[i])
    rank = {i: r for r, i in enumerate(order)}
    ex["graph_model_top_untagged"] = [card(i, g[i]) for i in order if not F[i]["tagged"]][:25]
    ex["graph_model_bottom_tagged"] = [dict(card(i, g[i]), rank=rank[i] + 1, of=len(order))
                                       for i in reversed(order) if F[i]["tagged"]][:25]
    od = sorted(ii.tolist(), key=lambda i: -F[i]["dom_mass"])
    rankd = {i: r for r, i in enumerate(od)}
    ex["dom_mass_top_untagged"] = [card(i, F[i]["dom_mass"]) for i in od if not F[i]["tagged"]][:25]
    ex["dom_mass_bottom_tagged"] = [dict(card(i, F[i]["dom_mass"]), rank=rankd[i] + 1, of=len(od))
                                    for i in reversed(od) if F[i]["tagged"]][:25]
    json.dump(ex, open(os.path.join(OUT, f"examples_{corpus}.json"), "w"), indent=1, ensure_ascii=False)
    return R, F


def transfer(Fa, Fb, B, rng, k):
    """Train on corpus a (theorems), test on corpus b (theorems)."""
    out = {}
    A = [f for f in Fa if f["kind"] == "theorem"]
    Bt = [f for f in Fb if f["kind"] == "theorem"]
    ya = np.array([f["tagged"] for f in A]); yb = np.array([f["tagged"] for f in Bt])
    P = {}
    for mname, keys in MODELS:
        m = lr(); m.fit(matrix(A, keys), ya)
        P["LR: " + mname] = m.predict_proba(matrix(Bt, keys))[:, 1]
    res, _ = boot_metrics(yb, P, k, B, rng, np.array([f["module"] for f in Bt]))
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20261109)
    ap.add_argument("--corpora", nargs="+", default=["pfr", "carleson"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    md = ["<!-- generated by bench/validate_outline.py; do not edit -->"]
    ALL = {}
    FS = {}
    for c in a.corpora:
        if not os.path.exists(os.path.join(REPO, "out", "corpus", c, "blueprint.json")):
            print("missing corpus", c, file=sys.stderr)
            continue
        ALL[c], FS[c] = run(c, a.boot, a.seed, md)
        print("done", c, file=sys.stderr)
    if len(FS) == 2:
        rng = np.random.default_rng(a.seed + 1)
        c1, c2 = list(FS)
        ALL["transfer"] = {}
        md.append("\n# Cross-project transfer (theorems; model fitted on one project, scored on the other)\n")
        md.append("| train -> test | model | ROC-AUC | average precision | precision@k |")
        md.append("|---|---|---|---|---|")
        for x, yv in [(c1, c2), (c2, c1)]:
            res = transfer(FS[x], FS[yv], a.boot, rng, ALL[yv]["blueprint_nodes"])
            ALL["transfer"][f"{x}->{yv}"] = res
            for mname, r in res.items():
                md.append(f"| {x} -> {yv} | {mname} | {fmt(r['auc'], r['auc_ci'])} | {fmt(r['ap'], r['ap_ci'])} | {fmt(r['p_at_k'], r['p_ci'])} |")
    json.dump(ALL, open(os.path.join(OUT, "results.json"), "w"), indent=1)
    open(os.path.join(OUT, "tables.md"), "w").write("\n".join(md) + "\n")
