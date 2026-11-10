#!/usr/bin/env python3
"""Score the boundary-recovery benchmark (hypothesis H1).

Input : out/bench/raw.jsonl  (one line per corpus item, written by Rosette/Bench.lean)
Output: out/bench/results.jsonl (per-item ranks under every scoring rule and pool)
        out/bench/RESULTS.md    (tables, worked examples, verdict)

Every number in RESULTS.md is computed here from raw.jsonl; nothing is hand-entered.
Only the Python standard library and numpy are used.
"""
import argparse
import json
import math
import os
import random
from collections import Counter

import numpy as np

SEED = 20261109
N_BOOT = 2000

# ---------------------------------------------------------------- loading

def load(raw_path, corpus_path):
    corpus = json.load(open(corpus_path))
    items = []
    for line in open(raw_path):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        for k, v in corpus[d["idx"]].items():      # crash records only carry idx
            d.setdefault(k, v)
        items.append(d)
    items.sort(key=lambda d: d["idx"])
    return items


class Item:
    """Numeric view of one successfully processed item."""

    def __init__(self, d):
        self.d = d
        f = {name: i for i, name in enumerate(d["groupFields"])}
        g = d["groups"]
        col = lambda name: [row[f[name]] for row in g]
        self.rep = np.array(col("rep"))
        self.count = np.array(col("count"))
        self.P = np.array(col("proofSizeDag"), dtype=float)
        self.Pt = np.array(col("proofSizeTree"), dtype=float)
        self.S = np.array(col("statementSize"), dtype=float)
        self.St = np.array(col("statementSizeTree"), dtype=float)
        self.D = np.array(col("numDeps"), dtype=float)
        self.isClass = np.array(col("stmtIsClass"), dtype=bool)
        self.isTarget = np.array(col("isTarget"), dtype=bool)
        self.under = np.array(col("underTarget"), dtype=bool)
        self.above = np.array(col("aboveTarget"), dtype=bool)
        self.minDepth = np.array(col("minDepth"), dtype=float)
        self.role = col("role")
        self.hash = col("stmtHash")
        self.isRoot = self.rep == 0
        root_hash = [h for h, r in zip(self.hash, self.isRoot) if r]
        self.restates = np.array([bool(root_hash) and h == root_hash[0] for h in self.hash])
        self.flat = float(d["flatDag"])
        self.found = bool(self.isTarget.any())
        # size of the helper's own proof relative to the theorem's own proof (before inlining)
        self.sizeRatio = float(d["helperProofDag"]) / max(1.0, float(d["thmProofDag"]))
        self.helperProof = float(d["helperProofDag"])

    def pool(self, name):
        if name == "all":
            return np.ones(len(self.P), dtype=bool)
        if name == "noRoot":
            return ~self.isRoot
        if name == "noRestate":
            return (~self.isRoot) & (~self.restates)
        if name == "oracleNoEnclosing":   # diagnostic only: uses the ground truth
            return (~self.isRoot) & (~self.above)
        if name == "liftFilter":   # the default filter of Rosette.Lift
            return (~self.isRoot) & (~self.restates) & (~self.isClass) & (self.P <= 0.8 * self.flat)
        raise ValueError(name)


POOLS = ["noRoot", "all", "noRestate", "liftFilter", "oracleNoEnclosing"]
PRIMARY_POOL = "noRoot"
EXPLORATORY_POOLS = {"noRestate", "liftFilter", "oracleNoEnclosing"}   # added after the first results were seen
POOL_DESC = {
    "noRoot": "PRIMARY. Every distinct candidate except the root (the whole proof, whose statement is the theorem itself)",
    "all": "every distinct candidate, root included",
    "noRestate": "EXPLORATORY (added after seeing the first results). No root and no candidate whose closed statement is the theorem's own statement (for example the body of the "
                 "outermost `fun`, which re-proves the theorem from its own hypotheses). Ground truths that restate the theorem are "
                 "excluded too and count as misses",
    "oracleNoEnclosing": "EXPLORATORY, DIAGNOSTIC ONLY, uses the ground truth: `noRoot` minus every candidate that encloses the ground truth. "
                         "It answers: if enclosing chunks were somehow ruled out, would the rule find the boundary",
    "liftFilter": "EXPLORATORY (added after seeing the first results). The filter `Rosette.Lift` applies before selecting: no root, no restatement of the theorem, "
                  "no typeclass-instance statement, proof at most 80% of the whole proof",
}

# ---------------------------------------------------------------- scoring rules (higher = better)

RULES = {
    "hidingRatio": lambda it: it.P / it.S,
    "hidingRatioTree": lambda it: it.Pt / it.St,
    "proofSize": lambda it: it.P,
    "invStatementSize": lambda it: -it.S,
    "fewestDeps": lambda it: -it.D,
    "shallowest": lambda it: -it.minDepth,
}
RULE_DESC = {
    "hidingRatio": "(a) proofSize / statementSize, both DAG sizes",
    "hidingRatioTree": "(a') same ratio with tree sizes. EXPLORATORY: added after the first results were seen, no held-out protection",
    "proofSize": "(b) proofSize only",
    "invStatementSize": "(c) 1 / statementSize only",
    "fewestDeps": "(d) fewest dependencies only",
    "shallowest": "(g) shallowest tree position first: uses no size at all, only how close to the root the candidate sits. "
                  "Added on review as the control for 'the helper ranks high because of where it sits in the tree'",
    "random": "(e) uniform random order (exact expectation)",
    "logP-lam*S": "(f1) log proofSize - lambda * statementSize, lambda fitted on the other half",
    "logP-lam*logS": "(f2) log proofSize - lambda * log statementSize, lambda fitted on the other half",
    "mdlSaving": "(f3) MDL saving proofSize - lambda * statementSize - mu * numDeps, fitted on the other half",
}

LAM_S = [0.0] + [round(10 ** x, 5) for x in np.linspace(-4, 0, 25)]
LAM_LOG = [round(x, 3) for x in np.linspace(0, 3, 31)]
MDL_LAM = [0, 0.5, 1, 2, 3, 5, 8, 12, 20, 35, 60]
MDL_MU = [0, 1, 3, 10, 30, 100, 300]
FAMILIES = {
    "logP-lam*S": ([(l,) for l in LAM_S], lambda it, p: np.log(it.P) - p[0] * it.S),
    "logP-lam*logS": ([(l,) for l in LAM_LOG], lambda it, p: np.log(it.P) - p[0] * np.log(it.S)),
    "mdlSaving": ([(l, m) for l in MDL_LAM for m in MDL_MU], lambda it, p: it.P - p[0] * it.S - p[1] * it.D),
}


def rank_of_target(it, score, mask):
    """(rank, n): mid-rank (ties broken at random, in expectation) of the best ground-truth
    candidate among the pool; rank = inf if no ground-truth candidate is in the pool."""
    n = int(mask.sum())
    t = it.isTarget & mask
    if not t.any():
        return math.inf, n
    s = score[mask]
    best = math.inf
    for v in set(score[t].tolist()):
        r = 1 + float((s > v).sum()) + (float((s == v).sum()) - 1) / 2.0
        best = min(best, r)
    return best, n


def random_expectation(n, m):
    """Exact expectations for a uniformly random order with m ground-truth candidates among n:
    P(hit@1), P(hit@3), P(hit@5), E[1/rank], E[normalised rank] of the best one."""
    if m == 0 or n == 0:
        return 0.0, 0.0, 0.0, 0.0, 1.0
    # P(min rank >= r) = C(n-r+1, m) / C(n, m)
    def surv(r):
        return math.comb(n - r + 1, m) / math.comb(n, m) if n - r + 1 >= m else 0.0
    pm = [surv(r) - surv(r + 1) for r in range(1, n - m + 2)]
    hit = lambda k: 1 - surv(k + 1)
    mrr = sum(p / r for r, p in enumerate(pm, start=1))
    er = sum(p * r for r, p in enumerate(pm, start=1))
    return hit(1), hit(3), hit(5), mrr, ((er - 1) / (n - 1) if n > 1 else 0.0)


def rank_generic(score, target, mask):
    """Mid-rank of the best target among mask (like rank_of_target, on plain arrays)."""
    n = int(mask.sum())
    t = target & mask
    if not t.any():
        return math.inf, n
    sc = score[mask]
    best = math.inf
    for v in set(score[t].tolist()):
        best = min(best, 1 + float((sc > v).sum()) + (float((sc == v).sum()) - 1) / 2.0)
    return best, n


def statement_level(it, score, mask):
    """Rank among distinct closed statements: every statement hash gets its best score in the pool."""
    best = {}
    tgt = set()
    for j in np.nonzero(mask)[0]:
        h = it.hash[j]
        best[h] = max(best.get(h, -math.inf), float(score[j]))
        if it.isTarget[j]:
            tgt.add(h)
    if not tgt:
        return math.inf, len(best)
    vals = np.array(list(best.values()))
    r = min(1 + float((vals > best[h]).sum()) + (float((vals == best[h]).sum()) - 1) / 2.0 for h in tgt)
    return r, len(best)


def norm_rank(r, n):
    if math.isinf(r):
        return 1.0
    return (r - 1) / (n - 1) if n > 1 else 0.0

# ---------------------------------------------------------------- metrics + bootstrap

def per_item_metrics(r, n):
    return (float(r <= 1), float(r <= 3), float(r <= 5), 0.0 if math.isinf(r) else 1.0 / r, norm_rank(r, n))


def summarise(rows, rng):
    """rows: array (items x 5) of [hit1, hit3, hit5, rr, normRank]. Returns the five point
    estimates (means, except the last = median) with 95% percentile-bootstrap intervals."""
    rows = np.asarray(rows, dtype=float)
    k = len(rows)
    if k == 0:
        return None
    point = list(rows[:, :4].mean(axis=0)) + [float(np.median(rows[:, 4]))]
    idx = rng.integers(0, k, size=(N_BOOT, k))
    bs = rows[idx]
    means = bs[:, :, :4].mean(axis=1)
    med = np.median(bs[:, :, 4], axis=1)
    lo = list(np.percentile(means, 2.5, axis=0)) + [float(np.percentile(med, 2.5))]
    hi = list(np.percentile(means, 97.5, axis=0)) + [float(np.percentile(med, 97.5))]
    return [(point[i], lo[i], hi[i]) for i in range(5)]


def fmt_ci(t, pct=True):
    p, lo, hi = t
    if pct:
        return f"{100*p:.1f} [{100*lo:.1f}, {100*hi:.1f}]"
    return f"{p:.3f} [{lo:.3f}, {hi:.3f}]"


def table(rule_rows, rng, order):
    out = ["| rule | n | top-1 % | top-3 % | top-5 % | MRR | median normalised rank |", "|---|---:|---:|---:|---:|---:|---:|"]
    for rule in order:
        rows = rule_rows.get(rule)
        if rows is None or len(rows) == 0:
            continue
        s = summarise(rows, rng)
        out.append(f"| {rule} | {len(rows)} | {fmt_ci(s[0])} | {fmt_ci(s[1])} | {fmt_ci(s[2])} | {fmt_ci(s[3], False)} | {fmt_ci(s[4], False)} |")
    return "\n".join(out)

# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="out/bench/raw.jsonl")
    ap.add_argument("--corpus", default="bench/corpus.json")
    ap.add_argument("--out", default="out/bench")
    args = ap.parse_args()
    rng = np.random.default_rng(SEED)

    raw = load(args.raw, args.corpus)
    failed = [d for d in raw if not d.get("ok")]
    items = [Item(d) for d in raw if d.get("ok")]
    found = [it for it in items if it.found]
    notfound = [it for it in items if not it.found]

    if len(found) < 4:
        raise SystemExit(f"only {len(found)} usable items in {args.raw} ({len(failed)} failed): nothing to score")

    # deterministic split into two halves for parameter fitting
    order = sorted(found, key=lambda it: it.d["idx"])
    random.Random(SEED).shuffle(order)
    half = {it.d["idx"]: (i % 2) for i, it in enumerate(order)}

    # ranks[pool][rule][idx] = (rank, n)
    ranks = {p: {} for p in POOLS}
    for p in POOLS:
        masks = {it.d["idx"]: it.pool(p) for it in found}
        for rule, fn in RULES.items():
            ranks[p][rule] = {it.d["idx"]: rank_of_target(it, fn(it), masks[it.d["idx"]]) for it in found}
    # fitted families: fit on one half (max MRR, ties -> smaller parameter), score the other
    fitted = {p: {} for p in POOLS}
    for p in POOLS:
        masks = {it.d["idx"]: it.pool(p) for it in found}
        for fam, (grid, fn) in FAMILIES.items():
            allr = {prm: {it.d["idx"]: rank_of_target(it, fn(it, prm), masks[it.d["idx"]]) for it in found} for prm in grid}
            chosen = {}
            for h in (0, 1):
                def mrr(prm):
                    v = [0.0 if math.isinf(r) else 1 / r for i, (r, n) in allr[prm].items() if half[i] == h]
                    return sum(v) / len(v)
                chosen[h] = max(grid, key=lambda prm: (round(mrr(prm), 9), [-x for x in prm]))
            # an item in half h is scored with the parameter fitted on half 1-h
            ranks[p][fam] = {i: allr[chosen[1 - half[i]]][i] for i in half}
            fitted[p][fam] = {"fitOnHalf0": chosen[0], "fitOnHalf1": chosen[1],
                              "inSampleMRR": {str(prm): round(sum((0.0 if math.isinf(r) else 1 / r) for r, n in allr[prm].values()) / len(allr[prm]), 4) for prm in grid}}

    rule_order = ["hidingRatio", "hidingRatioTree", "proofSize", "invStatementSize", "fewestDeps", "shallowest", "random",
                  "logP-lam*S", "logP-lam*logS", "mdlSaving"]

    def rows_for(pool, subset):
        out = {}
        for rule in rule_order:
            if rule == "random":
                rr = []
                for it in subset:
                    m = it.pool(pool)
                    rr.append(random_expectation(int(m.sum()), int((it.isTarget & m).sum())))
                out[rule] = rr
            else:
                out[rule] = [per_item_metrics(*ranks[pool][rule][it.d["idx"]]) for it in subset]
        return out

    # ---------------- strata (defined on the noRoot pool)
    def tinfo(it):
        nr = ~it.isRoot
        tP = it.P[it.isTarget].max()
        largest = bool(tP >= it.P[nr].max())
        i = int(np.argmax(np.where(it.isTarget, it.P, -1)))
        return {"targetP": float(tP), "targetS": float(it.S[i]), "targetDeps": float(it.D[i]),
                "targetRatio": float(it.P[i] / it.S[i]), "fraction": float(tP / it.flat),
                "largestNonRoot": largest, "restatesTheorem": bool(it.restates[it.isTarget].any()),
                "targetIsClass": bool(it.isClass[it.isTarget].any()), "targetRep": int(it.rep[i])}
    info = {it.d["idx"]: tinfo(it) for it in found}

    # ---------------- results.jsonl
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "results.jsonl"), "w") as fh:
        for d in raw:
            rec = {k: d.get(k) for k in ["idx", "theorem", "helper", "module", "area", "signal", "helperUseCount", "ok"]}
            if not d.get("ok"):
                rec["error"] = d.get("error")
                fh.write(json.dumps(rec) + "\n")
                continue
            it = next(x for x in items if x.d["idx"] == d["idx"])
            rec.update({k: d[k] for k in ["ms", "thmProofDag", "helperProofDag", "helperStmtDag", "flatDag", "flatTree",
                                          "sites", "droppedTags", "lostTags", "typecheck", "leakConst", "leakMData",
                                          "redexT", "redexL", "redexFlat", "nCands", "nGroups", "truncated", "note", "targets"]})
            rec["groundTruthFound"] = it.found
            if it.found:
                rec["half"] = half[d["idx"]]
                rec["target"] = info[d["idx"]]
                rec["poolSize"] = {p: int(it.pool(p).sum()) for p in POOLS}
                rec["rank"] = {p: {rule: (None if math.isinf(ranks[p][rule][d["idx"]][0]) else ranks[p][rule][d["idx"]][0])
                                   for rule in ranks[p]} for p in POOLS}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    write_report(args, raw, failed, items, found, notfound, ranks, fitted, half, info, rows_for, rule_order, rng)


def med(xs):
    xs = list(xs)
    return float(np.median(xs)) if xs else float("nan")


def clip(s, n=420):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n] + " …"


def write_report(args, raw, failed, items, found, notfound, ranks, fitted, half, info, rows_for, rule_order, rng):
    L = []
    w = L.append
    nItems = len(raw)
    hr = ranks["noRoot"]["hidingRatio"]
    R = lambda rule, it, pool="noRoot": ranks[pool][rule][it.d["idx"]][0]

    def relation(it, j):
        if it.isTarget[j]:
            return "GROUND TRUTH"
        if it.above[j]:
            return "encloses the ground truth"
        if it.under[j]:
            return "inside the ground truth"
        return "elsewhere in the proof"

    def top_rel(it, rule_fn, pool="noRoot"):
        m = it.pool(pool)
        s = np.where(m, rule_fn(it), -np.inf)
        return relation(it, int(np.argmax(s)))

    w("# Boundary-recovery benchmark: results for hypothesis H1")
    w("")
    w("Generated by `bench/score.py` from `out/bench/raw.jsonl` (written by `Rosette/Bench.lean`). "
      "All numbers below are computed from that file. Intervals are 95% percentile bootstrap "
      f"intervals over items ({N_BOOT} resamples).")
    w("")
    w("## What was measured")
    w("")
    w("For each ground-truth pair (theorem T, helper L) of `bench/corpus.json`, L's proof is inlined into T's proof "
      "term: every maximal application `L a1 ... an` is replaced by L's proof value with universe parameters "
      "instantiated and the arguments substituted and beta-reduced. The constant L no longer occurs. Every candidate "
      "lemma boundary (Prop-typed subterm with DAG size at least 20) of the flattened term is enumerated, and we ask "
      "where the inlined copy ranks under each scoring rule.")
    w("")
    w("**Ground-truth target.** The target is the subterm that the application `L a1 ... an` turned into, i.e. the "
      "*instantiated* body, identified by its tree position (recorded during inlining with a private marker that is "
      "erased before enumeration). Its closed statement is `forall (the local variables it uses), "
      "(L's conclusion at those arguments)`, which is usually not syntactically L's statement: L is stated for "
      "arbitrary arguments, the inlined copy only for the ones T passes. This is the fair target, because no "
      "subterm of the flattened proof has L's general statement; requiring it would make the task unsolvable by "
      "construction. If L is used several times, the best-ranked copy counts. If L was under-applied directly under "
      "a lambda, its leading lambdas merge with the enclosing telescope and the target is the telescope body "
      "(same closed statement).")
    w("")
    w("**Candidates.** Candidates with the same closed statement (structural hash) and the same proof and statement "
      "sizes are one candidate: they are the same lemma under every rule. The enumeration is DAG-aware "
      "(a subterm already visited with the same free variables is not visited again); see the caveat on "
      "`Rosette.Candidates` at the end.")
    w("")
    w("**Ranks.** Rank 1 is best. Ties get the mid-rank (expected rank under random tie-breaking), so a top-1 hit "
      "requires a strictly best score. Normalised rank is (rank - 1) / (pool size - 1): 0 is best, 0.5 is what a "
      "random order gives for a single target.")
    w("")
    w("## Run summary")
    w("")
    ok = [it.d for it in items]
    w(f"- corpus items: {nItems}; processed without error: {len(items)}; failed (exception, crash or timeout): {len(failed)}")
    for d in failed:
        w(f"  - item {d['idx']} `{d.get('theorem')}`: {clip(d.get('error'), 200)}")
    tc = Counter(d["typecheck"] for d in ok)
    w(f"- kernel re-check of the flattened proof against T's statement: {dict(tc)}")
    w(f"- enumerations truncated by a budget: {sum(d['truncated'] for d in ok)}; subterms skipped on a type-inference error: {sum(d['enumErrors'] for d in ok)}")
    w(f"- ground truth among the candidates: {len(found)} of {len(items)} items; not among them: {len(notfound)}")
    occ = [t for d in ok for t in d["targets"]]
    rc = Counter(t["reason"] or "resolved to a candidate" for t in occ)
    w(f"- inlined copies (tree positions) in total: {len(occ)}: " + ", ".join(f"{k}: {v}" for k, v in rc.most_common()))
    w(f"  - `insideSharedDuplicate` copies sit inside a subterm that is an exact repeat of one visited earlier; the first copy is the one enumerated, so nothing is lost")
    w(f"  - copies located through the merged-telescope rule (`lamBody`): {sum(t['via'] == 'lamBody' for t in occ)}")
    w(f"- items where L is used at more than one site: {sum(d['sites'] > 1 for d in ok)}; ground-truth markers lost to beta-reduction or to a function position: {sum(d['droppedTags'] + len(d['lostTags']) for d in ok)}")
    w(f"- distinct candidates per theorem (root included): median {med(d['nGroups'] for d in ok):.0f}, mean {np.mean([d['nGroups'] for d in ok]):.0f}, "
      f"min {min(d['nGroups'] for d in ok)}, max {max(d['nGroups'] for d in ok)}; before merging identical lemmas: median {med(d['nCands'] for d in ok):.0f}, max {max(d['nCands'] for d in ok)}")
    w(f"- flattened proof DAG size: median {med(d['flatDag'] for d in ok):.0f}; time per item: median {med(d['ms'] for d in ok):.0f} ms, max {max(d['ms'] for d in ok)} ms")
    w("")
    if notfound:
        w("### Items whose ground truth is not a candidate")
        w("")
        for it in notfound:
            w(f"- item {it.d['idx']} `{it.d['theorem']}` / `{it.d['helper']}`: " + "; ".join(sorted({t['reason'] for t in it.d['targets']}) or ["no visitable occurrence (only in binder types)"]))
        w("")
    else:
        w("The ground truth was a candidate for every processed item, so there is no 'not among the candidates' category to explain.")
        w("")

    w("## Leakage and triviality checks")
    w("")
    w("- All rules use only three numbers per candidate (proof size, statement size, number of dependencies). "
      "They cannot see names, universe parameters, metadata or term shape, so artifacts could only matter through sizes.")
    w(f"- `mdata` is erased from both proofs before inlining (present in {sum(d['mdataT'] for d in ok)} theorem proofs and {sum(d['mdataL'] for d in ok)} helper proofs); "
      f"flattened terms still containing `mdata`: {sum(d['leakMData'] for d in ok)}; still mentioning the constant L: {sum(d['leakConst'] for d in ok)}.")
    w(f"- Beta-redexes: the inlined application is beta-reduced, including redexes created when an argument that is a lambda lands in head position. "
      f"Helper proofs that already contained redexes before inlining: {sum(d['redexL'] > 0 for d in ok)}; theorem proofs: {sum(d['redexT'] > 0 for d in ok)} (so a redex is not a marker of the inlined region). "
      f"Items where the flattened term has more distinct redexes than T and L had together (redexes created deeper than head position): {sum(d['redexFlat'] > d['redexT'] + d['redexL'] for d in ok)}.")
    w("- Universe parameters of L are instantiated with the levels T used. Binder names inside the inlined body are L's own; no rule reads them.")
    w("- Sizes are DAG sizes of the instantiated terms, so an argument substituted many times is counted once. Candidate sizes are measured with bound variables replaced by local variables, "
      "which shares more than the de Bruijn form; the `dag` field of `targets` in results.jsonl is the de Bruijn size and is larger.")
    nl = sum(info[it.d['idx']]['largestNonRoot'] for it in found)
    nrs = sum(info[it.d['idx']]['restatesTheorem'] for it in found)
    w(f"- Triviality: in {nl} of {len(found)} items the inlined helper is the largest non-root candidate (nothing but the whole proof is bigger), "
      f"and in {nrs} its closed statement is the theorem's own statement (T is a direct wrapper of L). Results are split on this below. "
      f"Median share of the flattened proof taken by the inlined helper: {100*med(info[it.d['idx']]['fraction'] for it in found):.0f}%.")
    w("")

    w("## Main results")
    w("")
    for p in POOLS:
        w(f"### Pool `{p}`: {POOL_DESC[p]}")
        w("")
        sizes = [int(it.pool(p).sum()) for it in found]
        excl = sum(1 for it in found if not (it.isTarget & it.pool(p)).any())
        w(f"Candidates per theorem in this pool: median {med(sizes):.0f}, mean {np.mean(sizes):.0f}, max {max(sizes)}. "
          f"Items whose ground truth is excluded by the pool (counted as misses): {excl}.")
        w("")
        w(table(rows_for(p, found), rng, rule_order))
        w("")
    w("Rules:")
    w("")
    for r in rule_order:
        w(f"- `{r}`: {RULE_DESC[r]}")
    w("")
    w("### Fitted parameters")
    w("")
    w("Items were split into two halves at random (fixed seed). Each parameter was chosen on one half to maximise MRR and "
      "the rule was then scored on the other half; the rows above pool the two held-out halves. For `mdlSaving` the two numbers are lambda, mu. Parameter grids: "
      f"lambda for `logP-lam*S` in {{0}} and 25 log-spaced values from 1e-4 to 1; lambda for `logP-lam*logS` in 0, 0.1, ..., 3 "
      f"(0 is proofSize only, 1 is hidingRatio); MDL lambda in {MDL_LAM}, mu in {MDL_MU}.")
    w("")
    w("| pool | rule | parameter fitted on half 0 | parameter fitted on half 1 | held-out MRR on half 0 | held-out MRR on half 1 |")
    w("|---|---|---|---|---:|---:|")
    for p in POOLS:
        for fam in FAMILIES:
            f = fitted[p][fam]
            hm = []
            for h in (0, 1):
                v = [(0.0 if math.isinf(r) else 1 / r) for i, (r, n) in ranks[p][fam].items() if half[i] == h]
                hm.append(sum(v) / len(v))
            show = lambda prm: ", ".join(f"{float(x):g}" for x in prm)
            w(f"| {p} | {fam} | {show(f['fitOnHalf0'])} | {show(f['fitOnHalf1'])} | {hm[0]:.3f} | {hm[1]:.3f} |")
    w("")

    w("## Triviality split (pool `noRoot`)")
    w("")
    strata = [
        ("inlined helper IS the largest non-root candidate", [it for it in found if info[it.d['idx']]['largestNonRoot']]),
        ("inlined helper is NOT the largest non-root candidate", [it for it in found if not info[it.d['idx']]['largestNonRoot']]),
        ("helper takes at least half of the flattened proof", [it for it in found if info[it.d['idx']]['fraction'] >= 0.5]),
        ("helper takes less than half of the flattened proof", [it for it in found if info[it.d['idx']]['fraction'] < 0.5]),
        ("helper's closed statement differs from the theorem's", [it for it in found if not info[it.d['idx']]['restatesTheorem']]),
    ]
    for name, sub in strata:
        w(f"### {name} ({len(sub)} items)")
        w("")
        if sub:
            w(table(rows_for("noRoot", sub), rng, rule_order))
        w("")

    # ---------------- failure analysis for hidingRatio
    w("## Where hidingRatio's top pick lands (pool `noRoot`)")
    w("")
    rel = Counter(top_rel(it, RULES["hidingRatio"]) for it in found)
    relP = Counter(top_rel(it, RULES["proofSize"]) for it in found)
    w("| top-1 candidate is ... | hidingRatio | proofSize |")
    w("|---|---:|---:|")
    for k in ["GROUND TRUTH", "encloses the ground truth", "inside the ground truth", "elsewhere in the proof"]:
        w(f"| {k} | {rel.get(k, 0)} | {relP.get(k, 0)} |")
    w("")
    w("(A top-1 candidate counted here as GROUND TRUTH may be tied with another candidate, in which case the main table does not count it as a top-1 hit.)")
    w("")
    hit5 = [it for it in found if R("hidingRatio", it) <= 5]
    miss5 = [it for it in found if R("hidingRatio", it) > 5]
    w("Ground-truth features, split by whether hidingRatio puts the ground truth in its top 5:")
    w("")
    w(f"| median of ... | top-5 hit ({len(hit5)}) | miss ({len(miss5)}) |")
    w("|---|---:|---:|")
    for label, key in [("ground-truth proof size", "targetP"), ("ground-truth statement size", "targetS"),
                       ("ground-truth hiding ratio", "targetRatio"), ("ground-truth dependencies", "targetDeps"),
                       ("share of the flattened proof", "fraction")]:
        w(f"| {label} | {med(info[it.d['idx']][key] for it in hit5):.2f} | {med(info[it.d['idx']][key] for it in miss5):.2f} |")
    w(f"| distinct candidates in the theorem | {med(it.d['nGroups'] for it in hit5):.0f} | {med(it.d['nGroups'] for it in miss5):.0f} |")
    w(f"| helper is largest non-root candidate (share of items) | {np.mean([info[it.d['idx']]['largestNonRoot'] for it in hit5]) if hit5 else float('nan'):.2f} | {np.mean([info[it.d['idx']]['largestNonRoot'] for it in miss5]) if miss5 else float('nan'):.2f} |")
    w("")
    # what beats the ground truth in the misses
    beat_above, beat_under, beat_else, beat_class = [], [], [], []
    for it in miss5:
        m = it.pool("noRoot")
        s = RULES["hidingRatio"](it)
        tbest = s[it.isTarget].max()
        b = m & (s > tbest)
        k = max(int(b.sum()), 1)
        beat_above.append((b & it.above).sum() / k)
        beat_under.append((b & it.under).sum() / k)
        beat_else.append((b & ~it.above & ~it.under).sum() / k)
        beat_class.append((b & it.isClass).sum() / k)
    if miss5:
        w(f"In the {len(miss5)} top-5 misses, the candidates that out-score the ground truth are on average "
          f"{100*np.mean(beat_above):.0f}% enclosing chunks (the ground truth plus more of the surrounding proof), "
          f"{100*np.mean(beat_under):.0f}% pieces inside the inlined helper, and {100*np.mean(beat_else):.0f}% unrelated parts of the proof; "
          f"{100*np.mean(beat_class):.0f}% of them are typeclass-instance statements.")
        w("")

    # ---------------- worked examples
    def example(it, k):
        d = it.d
        inf = info[d["idx"]]
        st = d.get("statements", {})
        m = it.pool("noRoot")
        s = np.where(m, RULES["hidingRatio"](it), -np.inf)
        order = np.argsort(-s, kind="stable")[:3]
        r, n = ranks["noRoot"]["hidingRatio"][d["idx"]]
        w(f"### {k}. `{d['theorem']}` with helper `{d['helper']}` (item {d['idx']}, {d['area']})")
        w("")
        w(f"- hidingRatio rank of the ground truth: **{r:g} of {n}**; proofSize rank {R('proofSize', it):g}, 1/statementSize rank {R('invStatementSize', it):g}, fewest-deps rank {R('fewestDeps', it):g}")
        w(f"- ground truth: proof size {inf['targetP']:.0f}, statement size {inf['targetS']:.0f}, dependencies {inf['targetDeps']:.0f}, hiding ratio {inf['targetRatio']:.2f}, "
          f"{100*inf['fraction']:.0f}% of the flattened proof (DAG size {d['flatDag']}); largest non-root candidate: {'yes' if inf['largestNonRoot'] else 'no'}")
        w(f"- theorem: `{clip(d['theoremStatement'])}`")
        w(f"- helper as written in Mathlib: `{clip(d['helperStatement'])}`")
        w(f"- ground-truth candidate (instantiated, closed over what it uses): `{clip(st.get(str(inf['targetRep']), '(not stored)'))}`")
        w("- top 3 by hidingRatio:")
        for j in order:
            if not m[j]:
                continue
            w(f"  - ratio {it.P[j]/it.S[j]:.2f} (proof {it.P[j]:.0f}, statement {it.S[j]:.0f}, deps {it.D[j]:.0f}) [{relation(it, int(j))}]: `{clip(st.get(str(int(it.rep[j])), '(not stored)'), 300)}`")
        w("")

    w("## Worked examples")
    w("")
    w("Chosen mechanically. Wins: hidingRatio ranks the ground truth strictly first although it is not the largest non-root candidate "
      "(so proofSize alone does not find it); the four with the most candidates. Failures: the ground truth is outside the top 5; "
      "the four with the worst normalised rank among theorems with at least 30 candidates, at most one per Mathlib area.")
    w("")
    wins = [it for it in found if R("hidingRatio", it) == 1 and not info[it.d['idx']]['largestNonRoot']]
    wins.sort(key=lambda it: (-it.d["nGroups"], it.d["idx"]))
    if len(wins) < 4:
        extra = [it for it in found if R("hidingRatio", it) == 1 and it not in wins]
        extra.sort(key=lambda it: (-it.d["nGroups"], it.d["idx"]))
        wins += extra
    w(f"### Where hidingRatio wins ({len([it for it in found if R('hidingRatio', it) == 1])} strict top-1 hits in total, "
      f"{len([it for it in found if R('hidingRatio', it) == 1 and not info[it.d['idx']]['largestNonRoot']])} of them with a helper that is not the largest non-root candidate)")
    w("")
    for k, it in enumerate(wins[:4], 1):
        example(it, k)
    fails = [it for it in found if R("hidingRatio", it) > 5 and it.d["nGroups"] >= 30]
    fails.sort(key=lambda it: (-norm_rank(*ranks["noRoot"]["hidingRatio"][it.d["idx"]]), it.d["idx"]))
    chosen, seen = [], set()
    for it in fails:
        if it.d["area"] in seen:
            continue
        seen.add(it.d["area"])
        chosen.append(it)
        if len(chosen) == 4:
            break
    w(f"### Where hidingRatio fails ({len([it for it in found if R('hidingRatio', it) > 5])} items with the ground truth outside the top 5)")
    w("")
    for k, it in enumerate(chosen, 5):
        example(it, k)

    extra = review_sections(w, found, ranks, info, rows_for, rng, R)
    verdict(w, found, ranks, info, rows_for, rng, rel, relP, miss5, hit5, R, extra)

    w("## Caveats")
    w("")
    w("- The corpus contains only helpers that Mathlib authors marked as such (private or `aux`-named), one per module. It says nothing about unmarked lemma boundaries.")
    w("- The ground truth is one boundary per theorem. A candidate that out-ranks it is not thereby a bad lemma: other good boundaries may exist in the same proof and are counted as errors here. "
      "The benchmark measures agreement with one human choice, not lemma quality.")
    w("- Inlining removes a boundary that the human had already cut out, and the surrounding proof of T was written around that boundary. Whether flattened proofs resemble proofs written without the helper is not tested.")
    w("- Enumeration here is `Rosette.Bench.enumVisit`, a copy of `Rosette.visit` with the same path conventions and the same per-candidate computation that additionally resolves the ground-truth positions. "
      "Both are DAG-aware (a repeated subterm is one candidate).")
    w("- An earlier run of this benchmark used a version of `Rosette.interfaceOf` that could list the same variable twice among a candidate's dependencies (statements such as `forall {R} {R} ...`). "
      "That is fixed and this report is from a rerun. Dependency counts, statement sizes and statement hashes changed for the affected candidates, so the `fewestDeps` row and the `noRestate` / `liftFilter` pools "
      "(which test 'restates the theorem' by hash) differ from the earlier report.")
    w("- Candidate proof size is the DAG size of the subterm in context, with bound variables replaced by local variables. The proof of the lemma one would actually lift is that subterm closed over its interface, "
      "whose DAG size is typically larger (measured by the review on the ground-truth targets: in-context size is a median 0.67 of the closed size). This applies to all candidates alike; whether it changes rankings was not tested.")
    w("- Corpus bias runs in favour of every size-based rule: the corpus keeps private or `aux`-named helpers with proofs of at least 150 nodes, which are larger than typical Mathlib helpers (see section 2 of the controls).")
    w("- The statement of an inlined copy is the type Lean infers for the instantiated proof body, not L's declared statement at those arguments. The two are definitionally equal but can differ syntactically "
      "(for example an inferred statement of the form `a = a`, or a definition unfolded). Statement sizes of ground truths can therefore differ from the size of the human-written statement at those arguments. "
      "The independent review measured this on the earlier run: the two types differ syntactically at 88 of 462 inlined sites, and where the statement size differs the inferred one is usually the larger (44 of 50 items), "
      "which penalises the ground truth under hidingRatio. This rerun did not change the target definition.")
    w("- Candidates below 20 DAG nodes, non-Prop subterms, and applications of a constant or variable to atoms are not candidates (the `Rosette.Candidates` defaults).")
    w("- The headline sentences of the verdict ('not supported', the numbered headings) are fixed text in `bench/score.py`, written for this run's numbers; "
      "the figures and the 'higher / lower / not distinguishable' readings inside them are computed. Re-read the verdict if the corpus or the candidate definition changes.")
    w("- A top-1 'hit' requires a strictly best score; with mid-ranks a two-way tie for first gives rank 1.5 and counts as a top-3 hit only.")
    w("- The fitted rules were selected on MRR over small grids; the two halves have about 160 items each, so differences of a few points between fitted rules are within noise.")
    w("")

    with open(os.path.join(args.out, "RESULTS.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"wrote {os.path.join(args.out, 'results.jsonl')} and {os.path.join(args.out, 'RESULTS.md')}")


def review_sections(w, found, ranks, info, rows_for, rng, R):
    """Controls added after the independent review of the first version of this report. They ask
    whether 'the helper ranks high' says anything about the scoring rule, or only about where the
    helper sits in the tree and how the corpus was selected. Returns numbers for the verdict."""
    ex = {}
    n = len(found)
    rule_names = ["hidingRatio", "proofSize", "shallowest"]
    pct = lambda x: f"{100*x:.1f}"

    def metrics(pairs):
        return np.array([per_item_metrics(r, k) for r, k in pairs])

    def cell(rows):
        return f"{100*rows[:,0].mean():.1f} / {100*rows[:,2].mean():.1f} / {rows[:,3].mean():.3f}"

    def rand_rows(sub, pool="noRoot"):
        return np.array(rows_for(pool, sub)["random"])

    def pts(t):
        return f"{100*t[0]:+.1f} [{100*t[1]:+.1f}, {100*t[2]:+.1f}]"

    w("## Controls added on review")
    w("")
    w("These analyses were added after an independent review of the first version of this report. They are computed from the same raw data. "
      "All use the primary pool `noRoot` unless stated.")
    w("")

    # ---------------------------------------------------------------- 1. tree position
    w("### 1. How much of the rank is tree position, not score")
    w("")
    inside, enclosing = [], []
    for it in found:
        nr = ~it.isRoot
        inside.append(float((it.under & ~it.isTarget & ~it.above & nr).sum()) / max(1, int(nr.sum())))
        enclosing.append(int((it.above & ~it.isTarget & nr).sum()))
    ex["insideShare"] = med(inside)
    ex["enclosing"] = med(enclosing)
    w(f"A candidate nested inside the inlined helper has a smaller proof than the helper, so any rule that grows with proof size ranks the helper above it automatically. "
      f"Such pieces make up a median **{100*med(inside):.0f}%** (mean {100*np.mean(inside):.0f}%) of each theorem's pool; a median of only {med(enclosing):.0f} non-root candidates enclose the helper. "
      "A normalised rank near 0 is therefore largely built in. Two controls: the `shallowest` rule, which uses no sizes at all, and a normalised rank computed after removing the helper's own pieces from the pool.")
    w("")
    w("| rule | median absolute rank | median normalised rank | median normalised rank, helper's own pieces removed | top-1 % / top-5 % / MRR |")
    w("|---|---:|---:|---:|---:|")
    for rule in rule_names:
        absr = med(R(rule, it) for it in found)
        nrm = med(norm_rank(*ranks["noRoot"][rule][it.d["idx"]]) for it in found)
        outside = []
        for it in found:
            mask = (~it.isRoot) & (~it.under | it.isTarget | it.above)
            outside.append(norm_rank(*rank_generic(RULES[rule](it), it.isTarget, mask)))
        rows = metrics([ranks["noRoot"][rule][it.d["idx"]] for it in found])
        ex[rule] = {"abs": absr, "norm": nrm, "normOutside": med(outside)}
        w(f"| {rule} | {absr:g} | {nrm:.3f} | {med(outside):.3f} | {cell(rows)} |")
    rr = rand_rows(found)
    w(f"| random (expectation) | | 0.500 | 0.500 | {cell(rr)} |")
    w("")
    A = metrics([ranks["noRoot"]["hidingRatio"][it.d["idx"]] for it in found])
    B = metrics([ranks["noRoot"]["shallowest"][it.d["idx"]] for it in found])
    ex["vsShallow"] = [paired_diff(A[:, c], B[:, c], rng) for c in (0, 2, 3)]
    d1, d5, dm = ex["vsShallow"]
    w(f"Paired difference hidingRatio minus `shallowest`: top-1 {pts(d1)} points, top-5 {pts(d5)} points, MRR {dm[0]:+.3f} [{dm[1]:+.3f}, {dm[2]:+.3f}].")
    w("")

    # ---------------------------------------------------------------- 2. size-ratio strata
    w("### 2. Split by how big the helper is relative to the theorem that uses it")
    w("")
    ratios = [it.sizeRatio for it in found]
    bigger = sum(r >= 1 for r in ratios)
    ex["helperBigger"] = bigger
    ex["medSizeRatio"] = med(ratios)
    w(f"The corpus keeps helpers whose own proof has at least 150 nodes and theorems of at least 50. As a result the helper's proof is at least as large as the theorem's own proof "
      f"(before inlining) in **{bigger} of {n}** items; the median helper is {med(ratios):.2f} times the size of its consumer. In such items 'the biggest chunk' is the target almost by construction. "
      "The stratum that matches the intended use (a helper that is a small part of a long proof) is the first row.")
    w("")
    w("| helper proof / theorem's own proof | n | hidingRatio top-1 % / top-5 % / MRR | proofSize | shallowest | random | hidingRatio minus random: top-5 (points) | MRR |")
    w("|---|---:|---:|---:|---:|---:|---:|---:|")
    bins = [("below 0.5", 0, 0.5), ("0.5 to 1", 0.5, 1), ("1 to 3", 1, 3), ("3 and above", 3, math.inf)]
    ex["strata"] = {}
    for label, lo, hi in bins:
        sub = [it for it in found if lo <= it.sizeRatio < hi]
        if not sub:
            continue
        rows = {rule: metrics([ranks["noRoot"][rule][it.d["idx"]] for it in sub]) for rule in rule_names}
        rd = rand_rows(sub)
        t5 = paired_diff(rows["hidingRatio"][:, 2], rd[:, 2], rng)
        tm = paired_diff(rows["hidingRatio"][:, 3], rd[:, 3], rng)
        ex["strata"][label] = {"n": len(sub), "hr": rows["hidingRatio"].mean(axis=0), "rand": rd.mean(axis=0), "d5": t5, "dm": tm,
                               "ps": rows["proofSize"].mean(axis=0)}
        w(f"| {label} | {len(sub)} | {cell(rows['hidingRatio'])} | {cell(rows['proofSize'])} | {cell(rows['shallowest'])} | {cell(rd)} | {pts(t5)} | {tm[0]:+.3f} [{tm[1]:+.3f}, {tm[2]:+.3f}] |")
    w("")
    w("By absolute helper proof size (316 nodes is the median helper proof size over all 66,874 rarely-used same-module pairs in Mathlib, 1,196 the median of this corpus; both from `bench/CORPUS.md`):")
    w("")
    w("| helper proof size | n | median absolute rank (hidingRatio) | median normalised rank | hidingRatio top-5 % | random top-5 % |")
    w("|---|---:|---:|---:|---:|---:|")
    ex["bySize"] = {}
    for label, lo, hi in [("below 316", 0, 316), ("316 to 1,195", 316, 1196), ("1,196 and above", 1196, math.inf)]:
        sub = [it for it in found if lo <= it.helperProof < hi]
        if not sub:
            continue
        rows = metrics([ranks["noRoot"]["hidingRatio"][it.d["idx"]] for it in sub])
        rd = rand_rows(sub)
        nrm = med(norm_rank(*ranks["noRoot"]["hidingRatio"][it.d["idx"]]) for it in sub)
        ex["bySize"][label] = {"n": len(sub), "norm": nrm, "top5": rows[:, 2].mean()}
        w(f"| {label} | {len(sub)} | {med(R('hidingRatio', it) for it in sub):g} | {nrm:.3f} | {pct(rows[:,2].mean())} | {pct(rd[:,2].mean())} |")
    w("")

    # ---------------------------------------------------------------- 3. the chain task
    w("### 3. Where to cut along the helper's own nesting chain")
    w("")
    w("The chain of an item is the helper together with every non-root candidate that encloses it. Choosing among these is the decision 'how far out should the lemma extend', "
      "and it is where the first version of this report located the failures. A uniformly random pick on the chain is the baseline. Items whose chain has only the helper are left out.")
    w("")
    chain_items, hits, rnd, nrk, lens = [], {r: [] for r in rule_names}, [], {r: [] for r in rule_names}, []
    for it in found:
        chain = (~it.isRoot) & (it.isTarget | it.above)
        k = int(chain.sum())
        t = int((it.isTarget & chain).sum())
        if k <= t:
            continue
        chain_items.append(it)
        lens.append(k)
        rnd.append(t / k)
        for rule in rule_names:
            r, _ = rank_generic(RULES[rule](it), it.isTarget, chain)
            hits[rule].append(float(r <= 1))
            nrk[rule].append((r - 1) / (k - 1))
    ex["chainN"] = len(chain_items)
    ex["chainLen"] = med(lens)
    ex["chain"] = {}
    w(f"Items with a chain of more than one member: {len(chain_items)} of {n}; median chain length {med(lens):.0f}.")
    w("")
    w("| rule | helper is the strict best on its chain, % | minus random (points) | median normalised rank on the chain (0 = best, 1 = worst) |")
    w("|---|---:|---:|---:|")
    for rule in rule_names:
        dfr = paired_diff(hits[rule], rnd, rng)
        ex["chain"][rule] = {"hit": float(np.mean(hits[rule])), "diff": dfr, "norm": med(nrk[rule])}
        w(f"| {rule} | {pct(np.mean(hits[rule]))} | {pts(dfr)} | {med(nrk[rule]):.2f} |")
    ex["chainRandom"] = float(np.mean(rnd))
    w(f"| random pick on the chain | {pct(np.mean(rnd))} | | 0.50 |")
    w("")
    w("(`proofSize` and `shallowest` prefer the outermost member by construction, so they essentially never pick the helper here; they are shown for completeness.)")
    w("")

    # ---------------------------------------------------------------- 4. looser matching
    w("### 4. Looser notions of a hit")
    w("")
    w("The main tables require the exact extent of the helper. Two relaxations: (a) the rule's top pick counts if it is the helper, or a chunk nested in or enclosing the helper whose proof size is within a tolerance of the helper's; "
      "(b) ranking distinct closed statements instead of positions (each statement gets its best score), which merges near-copies of the helper that have the same statement.")
    w("")
    w("| rule | exact top-1 % | top pick within 5% of the helper's proof size, % | within 10%, % | statement-level top-1 % / top-5 % / MRR |")
    w("|---|---:|---:|---:|---:|")
    ex["loose"] = {}
    for rule in ["hidingRatio", "proofSize"]:
        tol = {0.05: [], 0.10: []}
        sl = []
        for it in found:
            m = ~it.isRoot
            sc = np.where(m, RULES[rule](it), -np.inf)
            j = int(np.argmax(sc))
            tP = it.P[it.isTarget & m].max()
            for t in tol:
                tol[t].append(float(it.isTarget[j] or ((it.above[j] or it.under[j]) and abs(it.P[j] - tP) <= t * tP)))
            sl.append(statement_level(it, RULES[rule](it), m))
        slr = metrics(sl)
        exact = metrics([ranks["noRoot"][rule][it.d["idx"]] for it in found])[:, 0].mean()
        ex["loose"][rule] = {"tol5": float(np.mean(tol[0.05])), "tol10": float(np.mean(tol[0.10])), "stmt": slr.mean(axis=0)}
        w(f"| {rule} | {pct(exact)} | {pct(np.mean(tol[0.05]))} | {pct(np.mean(tol[0.10]))} | {cell(slr)} |")
    w("")
    w("(In the tolerance columns a tie for first place is resolved in favour of the first candidate in traversal order, so the 'exact' part of those columns can exceed the strict top-1 figure.)")
    w("")
    return ex


def paired_diff(xs, ys, rng):
    """Mean of xs - ys with a 95% paired bootstrap interval."""
    d = np.asarray(xs, dtype=float) - np.asarray(ys, dtype=float)
    idx = rng.integers(0, len(d), size=(N_BOOT, len(d)))
    m = d[idx].mean(axis=1)
    return float(d.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def verdict(w, found, ranks, info, rows_for, rng, rel, relP, miss5, hit5, R, ex):
    """Plain-language verdict. Every number is computed; the wording of each comparison is
    selected by whether the paired bootstrap interval excludes zero."""
    def stat(rule, subset, pool="noRoot"):
        return summarise(rows_for(pool, subset)[rule], rng)
    hard = [it for it in found if not info[it.d['idx']]['largestNonRoot']]
    easy = [it for it in found if info[it.d['idx']]['largestNonRoot']]
    w("## Verdict on H1")
    w("")
    w("H1 was: human-chosen lemma boundaries rank high under hidingRatio among all candidate subterms, clearly beating baselines.")
    w("")
    w("| subset (pool `noRoot`) | n | hidingRatio top-1 % / top-5 % / MRR | proofSize top-1 % / top-5 % / MRR | 1/statementSize top-1 % / top-5 % / MRR | random top-1 % / top-5 % / MRR |")
    w("|---|---:|---:|---:|---:|---:|")
    for name, sub in [("all items", found), ("helper is the largest non-root candidate", easy), ("helper is not the largest", hard)]:
        if not sub:
            continue
        cell = lambda s: f"{100*s[0][0]:.1f} / {100*s[2][0]:.1f} / {s[3][0]:.3f}"
        w(f"| {name} | {len(sub)} | " + " | ".join(cell(stat(r, sub)) for r in ["hidingRatio", "proofSize", "invStatementSize", "random"]) + " |")
    w("")

    cache = {}

    def diff(rule_a, rule_b, pool, col):
        key = (rule_a, rule_b, pool, col)
        if key not in cache:
            cache[key] = _diff(rule_a, rule_b, pool, col)
        return cache[key]

    def _diff(rule_a, rule_b, pool, col):
        A = np.array(rows_for(pool, found)[rule_a])[:, col]
        B = np.array(rows_for(pool, found)[rule_b])[:, col]
        return paired_diff(A, B, rng)

    def says(t):
        m, lo, hi = t
        if lo > 0:
            return "higher (interval excludes 0)"
        if hi < 0:
            return "lower (interval excludes 0)"
        return "not distinguishable (interval includes 0)"

    w("Paired differences, hidingRatio minus the other rule, same items (95% paired bootstrap):")
    w("")
    w("| pool | versus | top-1 (points) | top-5 (points) | MRR | reading of the MRR difference |")
    w("|---|---|---:|---:|---:|---|")
    for pool in ["noRoot", "noRestate", "liftFilter", "oracleNoEnclosing"]:
        for other in ["proofSize", "random", "logP-lam*logS", "mdlSaving"]:
            d1, d5, dm = diff("hidingRatio", other, pool, 0), diff("hidingRatio", other, pool, 2), diff("hidingRatio", other, pool, 3)
            pts = lambda t: f"{100*t[0]:+.1f} [{100*t[1]:+.1f}, {100*t[2]:+.1f}]"
            w(f"| {pool} | {other} | {pts(d1)} | {pts(d5)} | {dm[0]:+.3f} [{dm[1]:+.3f}, {dm[2]:+.3f}] | {says(dm)} |")
    w("")

    a = stat("hidingRatio", found)
    b = stat("proofSize", found)
    e = stat("random", found)
    c = stat("invStatementSize", found)
    dd = stat("fewestDeps", found)
    ah = stat("hidingRatio", hard) if hard else None
    bh = stat("proofSize", hard) if hard else None
    dm = diff("hidingRatio", "proofSize", "noRoot", 3)
    d5 = diff("hidingRatio", "proofSize", "noRoot", 2)
    d1 = diff("hidingRatio", "proofSize", "noRoot", 0)
    lf = stat("hidingRatio", found, "liftFilter")
    nr = stat("hidingRatio", found, "noRestate")
    orc = stat("hidingRatio", found, "oracleNoEnclosing")
    orcP = stat("proofSize", found, "oracleNoEnclosing")
    n = len(found)
    enc = rel.get("encloses the ground truth", 0)
    med_hit = med(info[it.d['idx']]['fraction'] for it in hit5)
    med_miss = med(info[it.d['idx']]['fraction'] for it in miss5)
    w("**H1 is not supported.** In plain terms:")
    w("")
    sh = stat("shallowest", found)
    vs1, vs5, vsm = ex["vsShallow"]
    lo = ex["loose"]["hidingRatio"]
    w(f"1. *The human boundary is rarely the first pick, and its good-looking rank is mostly tree position.* Over {n} theorems (median {med(int(it.pool('noRoot').sum()) for it in found):.0f} candidates each), "
      f"hidingRatio makes the human helper its strict first pick in {100*a[0][0]:.1f}% of theorems (about one in {round(1/a[0][0]) if a[0][0] > 0 else 0}; this requires the exact extent, "
      f"and rises to {100*lo['tol10']:.1f}% if a nested or enclosing chunk within 10% of the helper's proof size also counts) and puts it in the top 5 in {100*a[2][0]:.0f}%, against {100*e[2][0]:.0f}% for a random order. "
      f"Its median absolute rank is {ex['hidingRatio']['abs']:g} (proofSize {ex['proofSize']['abs']:g}). The median normalised rank of {a[4][0]:.3f} is not evidence that the score finds the boundary: "
      f"a median {100*ex['insideShare']:.0f}% of each pool are pieces of the helper itself, which rank below it under any size-increasing rule. "
      f"With those pieces removed the median normalised rank is {ex['hidingRatio']['normOutside']:.2f} (0.5 is chance). "
      f"Ranking by depth in the tree alone, with no sizes, already gets top-5 {100*sh[2][0]:.0f}% and MRR {sh[3][0]:.3f}; "
      f"relative to that control hidingRatio's top-5 is {says(vs5)} ({100*vs5[0]:+.1f} points), its MRR {says(vsm)} ({vsm[0]:+.3f}), its top-1 {says(vs1)} ({100*vs1[0]:+.1f} points).")
    w(f"2. *It does not clearly beat the simplest baseline.* Ranking by proof size alone gets top-5 {100*b[2][0]:.0f}% and MRR {b[3][0]:.3f}, versus {100*a[2][0]:.0f}% and {a[3][0]:.3f} for hidingRatio. "
      f"The paired MRR difference is {dm[0]:+.3f} [{dm[1]:+.3f}, {dm[2]:+.3f}], top-5 {100*d5[0]:+.1f} points [{100*d5[1]:+.1f}, {100*d5[2]:+.1f}], top-1 {100*d1[0]:+.1f} points [{100*d1[1]:+.1f}, {100*d1[2]:+.1f}]: "
      f"On MRR hidingRatio is {says(dm)}; on top-5 it is {says(d5)}; on top-1 it is {says(d1)}. "
      "Where the difference is real it is a few points, not a different regime: most of the signal is 'big subterms are lemma-like', and dividing by statement size is a small correction to that.")
    w(f"3. *Statement size alone and dependency count alone carry no signal.* 1/statementSize (top-5 {100*c[2][0]:.0f}%) and fewest dependencies (top-5 {100*dd[2][0]:.0f}%) are at or below random ({100*e[2][0]:.0f}%), "
      f"with median normalised ranks of {c[4][0]:.2f} and {dd[4][0]:.2f} (0.5 is chance). The 'small working-memory state' idea, taken alone as a ranking rule, does not point at human boundaries.")
    f2 = stat("logP-lam*logS", found)
    f3 = stat("mdlSaving", found)
    f1 = stat("logP-lam*S", found)
    w(f"4. *Fitted combinations do not rescue it.* Held-out MRR in pool `noRoot`: log P - lambda * log S {f2[3][0]:.3f} (lambda = 1 is exactly hidingRatio, lambda = 0 is proofSize), "
      f"log P - lambda * S {f1[3][0]:.3f}, MDL-style saving {f3[3][0]:.3f}, against {a[3][0]:.3f} for hidingRatio. "
      f"Relative to log P - lambda * log S, hidingRatio's MRR is {says(diff('hidingRatio', 'logP-lam*logS', 'noRoot', 3))}; relative to the MDL saving it is {says(diff('hidingRatio', 'mdlSaving', 'noRoot', 3))}. "
      "No tested per-candidate formula of these three numbers does better than the plain ratio by more than noise.")
    if easy and hard:
      w(f"5. *The triviality split matters.* In the {len(easy)} theorems where the inlined helper is the largest non-root candidate, proofSize is right by construction and hidingRatio is right {100*stat('hidingRatio', easy)[0][0]:.0f}% of the time. "
        f"In the other {len(hard)}, hidingRatio's strict top-1 rate is {100*ah[0][0]:.1f}% (proofSize: {100*bh[0][0]:.1f}%, necessarily, because something bigger exists), top-5 {100*ah[2][0]:.0f}% versus {100*bh[2][0]:.0f}%.")
    ch = ex["chain"]["hidingRatio"]
    w(f"6. *On the choice that matters, where to stop along the nesting chain, hidingRatio is {'worse than' if ch['diff'][2] < 0 else ('better than' if ch['diff'][1] > 0 else 'not distinguishable from')} a random pick.* "
      f"Among the helper and the chunks that enclose it ({ex['chainN']} theorems, median chain length {ex['chainLen']:.0f}), hidingRatio scores the human cut strictly best in {100*ch['hit']:.1f}% of theorems; "
      f"picking a chain member at random gets {100*ex['chainRandom']:.1f}% (difference {100*ch['diff'][0]:+.1f} points [{100*ch['diff'][1]:+.1f}, {100*ch['diff'][2]:+.1f}]). "
      f"The helper's median position on its own chain under hidingRatio is {ch['norm']:.2f} on a scale where 1 is last: the ratio mostly keeps rising outward, so ranking by it selects against the human cut.")
    st0 = ex["strata"].get("below 0.5")
    if st0 is not None:
        w(f"7. *The headline depends on the corpus containing large helpers.* The helper's proof is at least as large as the theorem's own proof in {ex['helperBigger']} of {n} items. "
          f"In the {st0['n']} items where the helper is less than half the size of the theorem that uses it (the situation the project is about: a small lemma inside a long proof), "
          f"hidingRatio's top-1 is {100*st0['hr'][0]:.1f}%, top-5 {100*st0['hr'][2]:.1f}%, MRR {st0['hr'][3]:.3f}, against {100*st0['rand'][2]:.1f}% and {st0['rand'][3]:.3f} for a random order: "
          f"on top-5 it is {says(st0['d5'])} relative to random, on MRR {says(st0['dm'])}.")
    w("")
    w("**What the failures have in common.**")
    w("")
    # how the enclosing winner compares with the ground truth
    sm, restate, growth = [], [], []
    for it in found:
        m = it.pool("noRoot")
        sc = np.where(m, it.P / it.S, -np.inf)
        j = int(np.argmax(sc))
        if it.above[j] and not it.isTarget[j]:
            i = int(np.argmax(np.where(it.isTarget, it.P / it.S, -np.inf)))
            sm.append(it.S[j] <= it.S[i])
            restate.append(bool(it.restates[j]))
            growth.append(it.P[j] / it.P[i])
    w(f"- *The winner is usually the helper plus some of its surroundings.* In {enc} of {n} theorems hidingRatio's top candidate is a chunk that encloses the human helper "
      f"(proofSize: {relP.get('encloses the ground truth', 0)}). In those {len(sm)} cases the enclosing winner's proof is a median {med(growth):.1f} times the helper's, its statement is no larger than the helper's in {100*np.mean(sm):.0f}% of them, "
      f"and in {100*np.mean(restate):.0f}% its statement is simply the theorem's own statement (the proof body after introducing the theorem's variables). "
      "Moving outward from a good lemma the proof grows while the statement does not grow in proportion, so the ratio keeps rising; a score computed per candidate from sizes alone has no way to say 'stop here'.")
    w(f"- *Small helpers lose.* Helpers found in the top 5 take a median {100*med_hit:.0f}% of the flattened proof; missed ones {100*med_miss:.0f}%. Missed helpers also have larger instantiated statements "
      f"(median {med(info[it.d['idx']]['targetS'] for it in miss5):.0f} nodes versus {med(info[it.d['idx']]['targetS'] for it in hit5):.0f}) and sit in proofs with more candidates "
      f"(median {med(it.d['nGroups'] for it in miss5):.0f} versus {med(it.d['nGroups'] for it in hit5):.0f}).")
    w("- *Instantiated statements are long.* After inlining, the helper is stated at T's specific arguments, with every local variable it touches as a binder. Human helpers with ratio below 1 at their use site exist (examples 5 to 8): "
      "whatever made the human cut there, it is not visible in these sizes. (Possible reasons, none measured here: the statement is short only in its general form, the helper is used twice, or it keeps the caller readable.)")
    w(f"- *If enclosing chunks are removed by oracle*, hidingRatio's top-1 rises to {100*orc[0][0]:.0f}% and top-5 to {100*orc[2][0]:.0f}% (proofSize: {100*orcP[0][0]:.0f}% and {100*orcP[2][0]:.0f}%). "
      f"So the dominant failure is the choice of *extent* along one nested chain, not confusion with unrelated parts of the proof. In that pool hidingRatio's MRR is {says(diff('hidingRatio', 'proofSize', 'oracleNoEnclosing', 3))} relative to proof size alone: "
      "once the enclosing chain is out of the way, dividing by statement size does not help. This pool uses the ground truth and is not an achievable result.")
    w(f"- *Filters help top-1 but cost recall.* Dropping restatements of the theorem gives top-1 {100*nr[0][0]:.1f}%; the full `Rosette.Lift` filter gives top-1 {100*lf[0][0]:.1f}% but excludes the human helper itself in "
      f"{sum(1 for it in found if not (it.isTarget & it.pool('liftFilter')).any())} theorems "
      f"(ground truth restates the theorem: {sum(1 for it in found if it.restates[it.isTarget].all())}; is a typeclass-instance statement: {sum(1 for it in found if it.isClass[it.isTarget].all())}; "
      f"is more than 80% of the flattened proof: {sum(1 for it in found if (it.P[it.isTarget] > 0.8 * it.flat).all())}; a theorem can fall in more than one group).")
    w("")
    w("**What this does and does not show.** As a per-candidate ranking rule, hidingRatio does not recover human lemma boundaries. It beats a random order overall, "
      "but most of that margin is shared with rules that know nothing about statements (proof size, or depth in the tree), it disappears for helpers that are small relative to their theorem, "
      "and along the nesting chain it points away from the human cut. The first version of this report called it 'a usable shortlisting signal'; the controls above do not support that wording. "
      "The benchmark scores agreement with one human-chosen boundary per theorem, on a corpus of explicitly marked, mostly large helpers; it cannot tell whether the enclosing chunk that out-ranks the helper "
      "would have been an equally good lemma. A rule that compares a candidate with its own parent and children along the nesting chain (where does the ratio stop improving?), or a global objective over a set of cuts, "
      "is the obvious next thing to test, and section 3 of the controls (random pick on the chain) is the baseline it has to beat; neither was tested here.")
    w("")


if __name__ == "__main__":
    main()
