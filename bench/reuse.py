#!/usr/bin/env python3
"""H2 analysis: do closed sub-statements recur across different theorems?

Reads the JSON lines written by `ROSETTE_REUSE=1 lake env lean Rosette/Reuse.lean`
(out/reuse/{candidates,statements,lgg}.jsonl, run.json) and writes
out/reuse/REUSE.md (verdict + tables), out/reuse/clusters.json and out/reuse/summary.json.

    python3 bench/reuse.py [out/reuse]

The whole pipeline is `bench/run_reuse.sh`: Lean pass 1, this script (which writes
probe_keys.json: the statements no filter explains), Lean probe pass (one-call tactics on those
statements, written to probe.jsonl), this script again.

All numbers come from the Lean dump; nothing here is hand-entered.

Definitions (see Rosette/Reuse.lean for the three statement keys E / L1 / L2):
  position          a candidate (Prop-typed proof subterm, proof DAG size >= 20) that is not
                    the root of its theorem. The Lean traversal walks the proof as a tree, so
                    a shared subterm is met at many positions.
  occurrence        positions of one theorem with the same closed statement and the same
                    closed proof (same hashes) count as ONE occurrence, because sizes are DAG
                    sizes and a shared subterm is stored once.
  cluster           all occurrences with the same key
  recurring         a cluster with occurrences in >= 2 different theorems
  maximal occurrence an occurrence none of whose enclosing candidates is itself in a
                    recurring cluster of the population under study (if the enclosing lemma is
                    factored out, the nested one is no longer a separate saving)
  saving (exact)    over the maximal occurrences of a cluster, if there are >= 2:
                      gross = sum(proofSize) - max(proofSize) - statementSize
                      net   = gross - sum(1 + numDeps)            (one call per occurrence)
                    The kept proof is the LARGEST one. Keeping the smallest would be wrong:
                    a small occurrence is often `S` derived from another theorem of the
                    cluster whose own proof contains the large proof of `S`, so using it as
                    the lemma body would be circular.
  saving (L1/L2)    same, but the statement is the anti-unifier (size lggSize) and every call
                    passes `holes` extra arguments. This assumes the generalised statement is
                    provable at the cost of the largest member proof, which is not checked:
                    it is an optimistic estimate.
  sizes             DAG sizes (distinct subterms) of kernel terms.
"""
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out/reuse")

# ---------------------------------------------------------------- load

decls = {}
cands = []  # occurrences: non-root candidates, deduplicated per (theorem, statement, proof)
by_decl = defaultdict(dict)
n_all = 0
n_positions = 0
n_restate = 0
_groups = {}
_root_hash = None
for line in open(OUT / "candidates.jsonl"):
    r = json.loads(line)
    if r["record"] == "decl":
        decls[r["decl"]] = r
        _root_hash = None
    else:
        n_all += 1
        by_decl[r["decl"]][r["id"]] = r
        if r["role"] == "root":
            _root_hash = r["stmtHash"]
        elif r["stmtHash"] == _root_hash:
            # e.g. the body of the outer `fun`, closed again over all hypotheses: it restates
            # the theorem itself and is not a factoring candidate
            n_restate += 1
            r["role"] = "root"
        else:
            n_positions += 1
            k = (r["decl"], r["stmtHash"], r["proofHash"])
            rep_ = _groups.get(k)
            if rep_ is None:
                r["positions"] = [r["id"]]
                _groups[k] = r
                cands.append(r)
            else:
                rep_["positions"].append(r["id"])
del _groups
stmts = {}
for line in open(OUT / "statements.jsonl"):
    r = json.loads(line)
    stmts[r["stmtHash"]] = r
lggs = {}
for line in open(OUT / "lgg.jsonl"):
    r = json.loads(line)
    lggs[(r["level"], r["key"])] = r
run = json.load(open(OUT / "run.json"))
# second Lean pass (optional): first one-call tactic that closes a statement, or null
probe = {}
if (OUT / "probe.jsonl").exists():
    for line in open(OUT / "probe.jsonl"):
        r = json.loads(line)
        probe[r["stmtHash"]] = r["tactic"]
BUDGET_K = run.get("probeBudgetK", 20000)

LEVELS = [("E", "stmtHash"), ("L1", "h1"), ("L2", "h2")]

# ---------------------------------------------------------------- triviality classes

GLUE_HEADS = {
    "congrArg", "congr", "congrFun", "Eq.trans", "Eq.symm", "Eq.mpr", "Eq.mp", "Eq.refl",
    "of_eq_true", "eq_true", "eq_false", "eq_self", "id", "propext", "implies_congr",
    "forall_congr", "of_eq_false", "eq_true_intro", "eq_false_intro", "Eq.mpr_prop",
    "Eq.mpr_not", "of_decide_eq_true", "Eq.ndrec", "Eq.rec", "HEq.refl", "eq_of_heq",
    "iff_of_eq", "Iff.of_eq", "forall_prop_congr_dom", "ite_congr", "dite_congr", "funext",
    "Mathlib.Tactic.Ring.of_eq", "eq_comm", "ne_eq", "letFun", "cast",
}
GLUE_PREFIX = ("Mathlib.Tactic.", "Mathlib.Meta.", "Nat.Linarith.", "Int.Linarith.",
               "Lean.Omega.", "Linarith.", "Lean.Grind.", "Nat.ToInt.", "Int.OfNat.",
               "Lean.Meta.", "Simp.", "Bool.", "Classical.not_")

SIDE_RE = re.compile(
    r"(^|[,→] )\s*(0 < [^,→]*|0 ≤ [^,→]*|[^,→]* ≠ 0|[^,→]* ≠ ⊤|[^,→]* ≠ ⊥|[^,→]* < ⊤|"
    r"[^,→]* ≠ ∞|[^,→]* < ∞)$")
PROPEQ_RE = re.compile(r"= (True|False)\)?$|\) = \(|= \(¬|≍")
CAST_HEADS = ("Nat.cast", "Int.cast", "Rat.cast", "NNReal", "ENNReal", "Real.toNNReal",
              "ENNReal.ofReal", "ENNReal.toReal")


def conclusion(s: str) -> str:
    """Text after the last top-level arrow / binder comma (good enough for classification)."""
    depth, cut = 0, 0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in "([{⦃":
            depth += 1
        elif ch in ")]}⦄":
            depth -= 1
        elif depth == 0 and (s.startswith(" → ", i) or s.startswith(", ", i)):
            cut = i + (3 if s.startswith(" → ", i) else 2)
        i += 1
    return s[cut:]


def is_glue_head(h):
    return h is not None and (h in GLUE_HEADS or h.startswith(GLUE_PREFIX))


def classify(members):
    """Class of an exact-statement cluster. First matching rule wins."""
    c0 = members[0]
    st = stmts.get(c0["stmtHash"], {})
    text = st.get("statement", "")
    concl = conclusion(text)
    if any(m["stmtIsClass"] for m in members):
        return "instance"            # typeclass instance proof (instance synthesis)
    if st.get("inLib"):
        return "in-mathlib"          # a theorem with exactly this statement exists
    if st.get("exact") == "closed":
        return "exact?"              # closed by rfl, or exact? closes it from the library
    if all(m["numThms"] == 0 for m in members):
        return "no-lemma"            # no proof mentions any theorem: pure term plumbing
    if all(m["numThms"] <= 1 for m in members):
        return "one-lemma"           # every proof is one library lemma + terms/instances
    if PROPEQ_RE.search(concl) or all(is_glue_head(m["headConst"]) for m in members):
        return "automation-glue"     # simp/rw/norm_num plumbing: Prop equalities, congr chains
    if all(m.get("numAuto", 0) > 0 for m in members):
        return "tactic-certificate"  # ring / linarith / norm_num / omega output
    if SIDE_RE.search(concl) and len(concl) < 60:
        return "side-goal"           # positivity / nonvanishing / finiteness side condition
    if st.get("inLibL1"):
        return "in-mathlib-L1"       # exists up to instance path / literals / universes
    if probe.get(c0["stmtHash"]):
        return "one-tactic"          # one call of simp / norm_num / ring / fun_prop / ... closes it
    return "substantive"


TRIVIAL = {"instance", "in-mathlib", "exact?", "no-lemma", "one-lemma", "automation-glue",
           "tactic-certificate", "side-goal", "in-mathlib-L1", "one-tactic"}
CLASS_ORDER = ["instance", "in-mathlib", "exact?", "no-lemma", "one-lemma", "automation-glue",
               "tactic-certificate", "side-goal", "in-mathlib-L1", "one-tactic", "substantive"]
CLASS_DOC = {
    "instance": "statement is a typeclass (`DenselyOrdered ℝ`): emitted by instance synthesis",
    "in-mathlib": "a theorem with exactly this statement (same hash) already exists",
    "exact?": "`rfl` closes the statement, or `exact?` closes it from the library within the heartbeat budget",
    "no-lemma": "no occurrence's proof mentions any theorem constant (constructors, projections, recursors only)",
    "one-lemma": "every occurrence's proof mentions at most one theorem constant, and some mention one",
    "automation-glue": "conclusion is an equation between propositions (`… = True`, `(a ∧ b) = (c ∧ d)`) "
                       "or a heterogeneous equality (`≍`, congruence lemmas generated on the fly), "
                       "or every occurrence is headed by congruence / `Eq.mpr` / tactic-framework glue",
    "tactic-certificate": "every occurrence's proof mentions tactic-framework constants "
                          "(`Mathlib.Tactic.Ring.*`, `Linarith.*`, `Mathlib.Meta.NormNum.*`, `Lean.Omega.*`, …): "
                          "the output of one `ring` / `linarith` / `norm_num` / `omega` call",
    "side-goal": "short positivity / nonvanishing / finiteness conclusion (`0 < x`, `x ≠ 0`, `x ≠ ⊤`)",
    "in-mathlib-L1": "a library theorem has the same statement up to instance terms, literals, universes",
    "one-tactic": "none of the above, but one call of `simp`, `norm_num`, `ring`, `fun_prop`, `positivity`, `omega`, "
                  "`linarith`, `simp_all`, `measurability` or `aesop` closes the statement (probe pass; only run on "
                  "statements that reach this point)",
    "substantive": "none of the above",
}

# ---------------------------------------------------------------- clustering


def clusters_at(field):
    m = defaultdict(list)
    for c in cands:
        m[c[field]].append(c)
    return m


def ndecl(ms):
    return len({m["decl"] for m in ms})


def maximal_filter(rec_keys, field):
    """Occurrences with no enclosing candidate in a recurring cluster of `rec_keys`."""
    keep = defaultdict(list)
    for c in cands:
        if c[field] not in rec_keys:
            continue
        tbl = by_decl[c["decl"]]
        # the occurrence is maximal if at least one of its positions is not dominated
        for pos in c["positions"]:
            p = tbl[pos]["parent"]
            dominated = False
            while p is not None:
                pc = tbl[p]
                if pc["role"] != "root" and pc[field] in rec_keys:
                    dominated = True
                    break
                p = pc["parent"]
            if not dominated:
                keep[c[field]].append(c)
                break
    return keep


def saving(level, key, ms):
    """(gross, net) saving of factoring the occurrences `ms` of one cluster."""
    if len(ms) < 2:
        return 0, 0
    ps = [m["proofSizeDag"] for m in ms]
    calls = sum(1 + m["numDeps"] for m in ms)
    g = lggs.get((level, key))
    if level == "E" or g is None:
        # one statement (or a generalised cluster with a single distinct statement)
        stmt = min(m["statementSize"] for m in ms)
    else:
        stmt = g["lggSize"]
        calls += g["holes"] * len(ms)
    gross = sum(ps) - max(ps) - stmt
    return gross, gross - calls


def bucket(n):
    if n <= 4:
        return str(n)
    if n <= 9:
        return "5-9"
    if n <= 19:
        return "10-19"
    if n <= 49:
        return "20-49"
    return "50+"


BUCKETS = ["2", "3", "4", "5-9", "10-19", "20-49", "50+"]

total_thm_proof = sum(d["proofSizeDag"] for d in decls.values())
n_thm = len(decls)
level_stats = {}
level_clusters = {}
for level, field in LEVELS:
    cl = clusters_at(field)
    rec = {k: v for k, v in cl.items() if ndecl(v) >= 2}
    mx = maximal_filter(set(rec), field)
    rows = []
    for k, ms in rec.items():
        mms = mx.get(k, [])
        gross, net = saving(level, k, mms)
        gross_all, net_all = saving(level, k, ms)
        rows.append({
            "level": level, "key": k, "occurrences": len(ms), "theorems": ndecl(ms),
            "slices": sorted({decls[m["decl"]]["slice"] for m in ms}),
            "modules": len({decls[m["decl"]]["module"] for m in ms}),
            "distinctStatements": len({m["stmtHash"] for m in ms}),
            "distinctProofs": len({m["proofHash"] for m in ms}),
            "maximalOccurrences": len(mms),
            "medianProof": statistics.median(m["proofSizeDag"] for m in ms),
            "maxProof": max(m["proofSizeDag"] for m in ms),
            "statementSize": min(m["statementSize"] for m in ms),
            "gross": gross, "net": net, "grossAll": gross_all, "netAll": net_all,
            "members": ms,
        })
    level_clusters[level] = rows
    thms_with = {m["decl"] for r in rows for m in r["members"]}
    level_stats[level] = {
        "clusters": len(cl),
        "recurring": len(rows),
        "occurrencesInRecurring": sum(r["occurrences"] for r in rows),
        "shareOfOccurrences": sum(r["occurrences"] for r in rows) / max(1, len(cands)),
        "theoremsWithRecurring": len(thms_with),
        "crossModule": sum(1 for r in rows if r["modules"] >= 2),
        "crossSlice": sum(1 for r in rows if len(r["slices"]) >= 2),
        "hist": dict(Counter(bucket(r["theorems"]) for r in rows)),
        "maxTheorems": max((r["theorems"] for r in rows), default=0),
        "netPositive": sum(1 for r in rows if r["net"] > 0),
        "netSaving": sum(max(0, r["net"]) for r in rows),
        "grossSaving": sum(max(0, r["gross"]) for r in rows),
        "netSavingShare": sum(max(0, r["net"]) for r in rows) / total_thm_proof,
    }

# ---------------------------------------------------------------- exact level: classes

E = level_clusters["E"]
for r in E:
    r["class"] = classify(r["members"])
    st = stmts.get(r["key"], {})
    r["statement"] = st.get("statement", "?")
    r["inLib"] = st.get("inLib", [])
    r["inLibL1"] = st.get("inLibL1", [])
    r["exact"] = st.get("exact", "notrun")
    r["exactLemma"] = st.get("exactLemma")
    r["exactNote"] = st.get("exactNote", "")
    r["probe"] = probe.get(r["key"], "notrun" if r["key"] not in probe else None)
    r["sameProof"] = r["distinctProofs"] == 1

# statements that reach the end of the filter chain: input of the Lean probe pass
_pk = [r for r in E if r["class"] in ("one-tactic", "substantive")]
json.dump({"keys": sorted(r["key"] for r in _pk),
           "decls": sorted({m["decl"] for r in _pk for m in r["members"]})},
          open(OUT / "probe_keys.json", "w"), ensure_ascii=False)
probe_ran = bool(probe)
probe_missing = [r for r in _pk if r["key"] not in probe]

class_tbl = {}
for cls in CLASS_ORDER:
    rs = [r for r in E if r["class"] == cls]
    class_tbl[cls] = {
        "clusters": len(rs),
        "occurrences": sum(r["occurrences"] for r in rs),
        "medianProof": statistics.median([r["medianProof"] for r in rs]) if rs else 0,
        "netSaving": sum(max(0, r["net"]) for r in rs),
    }

# savings restricted to substantive clusters (maximality recomputed inside that population)
sub_keys = {r["key"] for r in E if r["class"] == "substantive"}
sub_max = maximal_filter(sub_keys, "stmtHash")
for r in E:
    if r["class"] == "substantive":
        mms = sub_max.get(r["key"], [])
        r["subGross"], r["subNet"] = saving("E", r["key"], mms)
        r["subMaximal"] = len(mms)
        # distinct theorems among the maximal occurrences
        r["subTheorems"] = ndecl(mms) if mms else 0
sub = [r for r in E if r["class"] == "substantive"]
sub_net = sum(max(0, r["subNet"]) for r in sub)
sub_pos = [r for r in sub if r["subNet"] > 0]
sub_cross_mod = [r for r in sub_pos if r["modules"] >= 2]
sub_same_proof = [r for r in sub_pos if r["sameProof"]]
exact_tried = [r for r in E if r["exact"] != "notrun"]
exact_counts = Counter(r["exact"] for r in exact_tried)

# generalised levels: clusters that are NOT already exact-recurring (>= 2 distinct statements)
gen = {}
for level in ("L1", "L2"):
    rows = [r for r in level_clusters[level] if r["distinctStatements"] >= 2]
    for r in rows:
        g = lggs.get((level, r["key"]), {})
        r["lgg"] = g.get("lgg", "?")
        r["holes"] = g.get("holes")
        r["lggSize"] = g.get("lggSize")
        if r["lgg"].startswith("failed to pretty print"):
            r["lgg"] = "(anti-unifier not printable)"
        ms = r["members"]
        half = len(ms) / 2
        r["anyClass"] = any(m["stmtIsClass"] for m in ms)
        r["oneLemma"] = sum(1 for m in ms if m["numThms"] <= 1) >= half
        # automation: at least half of the occurrences are glue-headed or carry tactic
        # certificates, or a member / the anti-unifier is a Prop-equation
        r["glue"] = bool(PROPEQ_RE.search(conclusion(r["lgg"]))) or \
            sum(1 for m in ms if is_glue_head(m["headConst"]) or m.get("numAuto", 0) > 0) >= half or \
            any(PROPEQ_RE.search(conclusion(stmts.get(h, {}).get("statement", "")))
                for h in {m["stmtHash"] for m in ms})
        # ground facts: no hypotheses, variables or quantifiers at all (`0 < 4`, `4 * 0 = 0`)
        def _ground(m):
            t = stmts.get(m["stmtHash"], {}).get("statement", "∀")
            return m["numDeps"] == 0 and "∀" not in t and "∃" not in t
        r["ground"] = sum(1 for m in ms if _ground(m)) >= half
        med_stmt = statistics.median(m["statementSize"] for m in ms)
        # tight: the anti-unifier keeps most of the statement and needs few extra arguments
        r["tight"] = (r["holes"] is not None and r["holes"] <= 3
                      and r["lggSize"] >= 0.6 * med_stmt)
        # sibling theorems: at least half of the occurrences are (nearly) the whole proof of their
        # own theorem, i.e. the cluster pairs theorems Mathlib already states and names separately
        r["wholeBody"] = sum(1 for m in ms
                             if m["proofSizeDag"] >= 0.8 * decls[m["decl"]]["proofSizeDag"]) >= half
        r["trivial"] = r["anyClass"] or r["oneLemma"] or r["glue"] or r["ground"] or r["wholeBody"]
        r["examples"] = []
        seen = set()
        for m in sorted(r["members"], key=lambda m: -m["proofSizeDag"]):
            if m["stmtHash"] not in seen:
                seen.add(m["stmtHash"])
                r["examples"].append((m["decl"], m["proofSizeDag"],
                                      stmts.get(m["stmtHash"], {}).get("statement", "?")))
    gen[level] = rows

# ---------------------------------------------------------------- report


def esc(s):
    return s.replace("|", "\\|").replace("\n", " ")


def code(s, n=260):
    s = s if len(s) <= n else s[:n] + " …"
    return "`" + s.replace("`", "'") + "`"


def pct(x):
    return f"{100 * x:.1f}%"


L = []
w = L.append
w("# H2 — do closed sub-statements recur across proofs?")
w("")
w("Generated by `bench/reuse.py` from the Lean dump of `Rosette/Reuse.lean`. Every number below "
  "is computed from `out/reuse/*.jsonl`; sizes are DAG sizes of kernel terms.")
w("")
w("## Data")
w("")
w(f"- Lean `{run['leanVersion']}`; theorems with proof DAG size ≥ {run['minTheoremProof']} that are "
  "human-written by name (not auto-generated, not a `to_additive` image, not an instance).")
w("")
w("| slice | module prefixes | eligible | used |")
w("|---|---|---:|---:|")
for s in run["slices"]:
    w(f"| {s['slice']} | {', '.join('`' + p + '`' for p in s['prefixes'])} | {s['eligible']} | {s['used']} |")
w("")
trunc = [d for d in decls.values() if d["truncated"]]
failed = [d for d in decls.values() if not d["ok"]]
errs = sum(d["errors"] for d in decls.values())
w(f"- {n_thm} theorems enumerated: {n_thm - len(failed)} ok, {len(failed)} failed, "
  f"{len(trunc)} truncated by a budget, {errs} subterms skipped on a type-inference error.")
for d in trunc + failed:
    w(f"  - `{d['decl']}`: {'failed' if not d['ok'] else 'truncated'} — {esc(d['note'])} "
      f"({d['numCandidates']} candidates kept)")
w(f"- {n_all} candidate positions (Prop-typed proof subterms, proof DAG ≥ {run['minCandidateProof']}; "
  f"the traversal walks the term as a tree), {n_positions} excluding theorem roots and {n_restate} "
  f"inner restatements of the theorem itself. Positions of one "
  f"theorem with the same closed statement and closed proof are one *occurrence*: {len(cands)} occurrences, "
  f"{run['distinctStatements']} distinct closed statements.")
w(f"- Total proof size of the theorems: {total_thm_proof} nodes "
  f"(median {int(statistics.median(d['proofSizeDag'] for d in decls.values()))} per theorem).")
w(f"- Library lookup table: statement hashes of all {run['libraryTheoremsHashed']} theorems in the environment.")
w("")
w("## Recurrence by level")
w("")
w("E = exact statement (up to binder names, universe names); L1 = literals, universes and "
  "instance arguments abstracted; L2 = depth-2 shape (heads of each hypothesis / conclusion and "
  "of their arguments; deeper terms and bound variables are holes). A cluster is *recurring* if "
  "it occurs in ≥ 2 different theorems.")
w("")
w("| | E | L1 | L2 |")
w("|---|---:|---:|---:|")
rowspec = [
    ("clusters (all)", "clusters", str),
    ("recurring clusters", "recurring", str),
    ("occurrences inside recurring clusters", "occurrencesInRecurring", str),
    ("… as share of all occurrences", "shareOfOccurrences", pct),
    (f"theorems (of {n_thm}) with ≥ 1 recurring occurrence", "theoremsWithRecurring", str),
    ("recurring clusters spanning ≥ 2 modules", "crossModule", str),
    ("recurring clusters spanning ≥ 2 slices", "crossSlice", str),
    ("largest cluster (theorems)", "maxTheorems", str),
    ("clusters with positive net saving", "netPositive", str),
    ("net saving, nodes (maximal occurrences)", "netSaving", str),
    ("… as share of total proof size", "netSavingShare", pct),
]
for label, key, fmt in rowspec:
    w(f"| {label} | " + " | ".join(fmt(level_stats[lv][key]) for lv, _ in LEVELS) + " |")
w("")
w("The L1 / L2 savings are optimistic: they assume the anti-unified statement is a true, provable "
  "lemma costing no more than the largest member proof. The E saving is bookkeeping on existing "
  "proofs: the lemma keeps the largest member proof and every other occurrence becomes a call. "
  "Savings are sums of DAG sizes of the removed subterms; subterms shared between different "
  "clusters inside one theorem are counted more than once, so the shares are upper estimates.")
w("")
w("Distribution of the number of theorems per recurring cluster:")
w("")
w("| theorems | " + " | ".join(BUCKETS) + " |")
w("|---|" + "---:|" * len(BUCKETS))
for lv, _ in LEVELS:
    h = level_stats[lv]["hist"]
    w(f"| {lv} | " + " | ".join(str(h.get(b, 0)) for b in BUCKETS) + " |")
w("")
w("## What the exact recurrences are")
w("")
w("Each exact recurring cluster gets the first class that applies:")
w("")
for cls in CLASS_ORDER:
    w(f"- **{cls}** — {CLASS_DOC[cls]}")
w("")
w("| class | clusters | share | occurrences | median proof size | net saving (nodes) |")
w("|---|---:|---:|---:|---:|---:|")
nE = max(1, len(E))
for cls in CLASS_ORDER:
    t = class_tbl[cls]
    w(f"| {cls} | {t['clusters']} | {pct(t['clusters'] / nE)} | {t['occurrences']} | "
      f"{t['medianProof']:.0f} | {t['netSaving']} |")
triv = sum(class_tbl[c]["clusters"] for c in TRIVIAL)
w(f"| **all trivial classes** | {triv} | {pct(triv / nE)} | "
  f"{sum(class_tbl[c]['occurrences'] for c in TRIVIAL)} | | "
  f"{sum(class_tbl[c]['netSaving'] for c in TRIVIAL)} |")
w("")
rfl_closed = sum(1 for r in exact_tried if r["exact"] == "closed" and r["exactNote"] == "rfl")
w(f"`exact?` was run on {len(exact_tried)} recurring statements without a hash match (largest gross "
  f"saving first; {BUDGET_K:,}k heartbeats each, a tenth of Lean's default budget for one command): "
  + ", ".join(f"{v} {k}" for k, v in sorted(exact_counts.items())) + f". Of the closed ones, {rfl_closed} are closed by `rfl` "
  "alone (no lemma is reported for those). `timeout` means the heartbeat or recursion budget ran out, which is not evidence "
  "either way; `error` is any other exception.")
w("")
if probe_ran:
    pc = Counter(r["probe"] for r in _pk if r["key"] in probe)
    w(f"Probe pass: the {len(_pk)} statements that reach the end of the filter chain were each tried with one call of "
      "`simp`, `norm_num`, `ring` (with `push_cast`), `fun_prop`, `positivity`, `omega`, `linarith`, `simp_all`, "
      f"`measurability`, `aesop` (in that order, {BUDGET_K:,}k heartbeats per call). First tactic that closes the statement: "
      + ", ".join(f"{k or 'none'}: {v}" for k, v in sorted(pc.items(), key=lambda kv: (-kv[1], str(kv[0]))))
      + (f". Not probed (statement not found again): {len(probe_missing)}." if probe_missing else "."))
else:
    w("Probe pass not run: the `one-tactic` class is empty and the substantive count is higher than it would be. "
      "Run `bench/run_reuse.sh`.")
w("")
w("### Substantive exact recurrences")
w("")
w(f"- {len(sub)} substantive recurring statements; {len(sub_pos)} of them have a positive net saving "
  "once nested occurrences are counted only at the outermost substantive level.")
w(f"- Net saving of factoring all of them: **{sub_net} nodes = {pct(sub_net / total_thm_proof)}** "
  f"of the {total_thm_proof} proof nodes.")
w(f"- {len(sub_cross_mod)} of the {len(sub_pos)} span ≥ 2 modules; "
  f"{sum(1 for r in sub_pos if len(r['slices']) >= 2)} span ≥ 2 slices.")
w(f"- {len(sub_same_proof)} of the {len(sub_pos)} have literally the same closed proof term at every "
  "occurrence (same proof hash): duplicated proof text or identical automation output.")
for sl in sorted({d["slice"] for d in decls.values()}):
    rs = [r for r in sub_pos if r["slices"] == [sl]]
    tot = sum(d["proofSizeDag"] for d in decls.values() if d["slice"] == sl)
    w(f"  - slice `{sl}`: {len(rs)} clusters, net {sum(r['subNet'] for r in rs)} nodes "
      f"= {pct(sum(r['subNet'] for r in rs) / tot)} of that slice's {tot} proof nodes")
if sub_pos:
    w(f"- Theorems per cluster among those {len(sub_pos)}: "
      + ", ".join(f"{b}: {c}" for b, c in
                  sorted(Counter(bucket(r['theorems']) for r in sub_pos).items(),
                         key=lambda kv: BUCKETS.index(kv[0]))) + ".")
    w(f"- Median proof size {statistics.median(r['medianProof'] for r in sub_pos):.0f}, "
      f"median statement size {statistics.median(r['statementSize'] for r in sub_pos):.0f}.")
w("")


def table_exact(rows, net_key, title):
    w(f"### {title}")
    w("")
    w("| # | net | thms | occ | proof (med) | proof (max) | stmt | class | same proof | exact? | one tactic | statement | where |")
    w("|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        ds = sorted({m["decl"] for m in r["members"]})
        where = ", ".join(f"`{d}`" for d in ds[:3]) + (f" +{len(ds) - 3}" if len(ds) > 3 else "")
        cls = r["class"]
        if cls == "in-mathlib" and r["inLib"]:
            cls += f" (`{r['inLib'][0]}`)"
        elif cls == "exact?":
            cls += " (`rfl`)" if r["exactNote"] == "rfl" else (f" (`{r['exactLemma']}`)" if r["exactLemma"] else "")
        elif cls == "one-tactic":
            cls += f" (`{r['probe']}`)"
        elif cls == "in-mathlib-L1" and r["inLibL1"]:
            cls += f" (`{r['inLibL1'][0]}`)"
        w(f"| {i} | {r[net_key]} | {r['theorems']} | {r['occurrences']} | {r['medianProof']:.0f} | "
          f"{r['maxProof']} | {r['statementSize']} | {esc(cls)} | {'yes' if r['sameProof'] else 'no'} | "
          f"{r['exact']} | {r['probe'] if r['probe'] else ('none' if r['key'] in probe else '')} | "
          f"{esc(code(r['statement']))} | {esc(where)} |")
    w("")


top_all = sorted(E, key=lambda r: (-r["net"], r["key"]))[:25]
table_exact(top_all, "net", "Top 25 exact recurring clusters by net saving (all classes)")
top_sub = sorted(sub, key=lambda r: (-r["subNet"], r["key"]))[:25]
table_exact(top_sub, "subNet", "Top 25 substantive exact clusters by net saving")

w("## Recurrence up to generalisation")
w("")
for level in ("L1", "L2"):
    rows = gen[level]
    pos = [r for r in rows if r["net"] > 0]
    nontriv = [r for r in pos if not r["trivial"]]
    tight = [r for r in nontriv if r["tight"]]
    holes = [r["holes"] for r in rows if r["holes"] is not None]
    w(f"- **{level}**: {len(rows)} recurring clusters contain ≥ 2 distinct exact statements (the rest "
      f"of the {level_stats[level]['recurring']} are exact recurrences again). "
      f"{len(pos)} have a positive optimistic net saving; of those {len(nontriv)} are not "
      "instance / one-lemma / automation / ground-fact / whole-theorem-body clusters (at least half of the occurrences; "
      f"{sum(1 for r in pos if r['wholeBody'])} are whole-theorem-body clusters, meaning the occurrences are at least 80% of "
      "the proof of their own theorem, so the cluster just pairs sibling theorems that Mathlib already names), "
      f"with optimistic net saving {sum(r['net'] for r in nontriv)} nodes; {len(tight)} of them are also "
      "*tight* (≤ 3 holes and the anti-unifier keeps ≥ 60% of the median statement size), "
      f"saving {sum(r['net'] for r in tight)} nodes. "
      + (f"Holes in the anti-unifier: median {statistics.median(holes):.0f}, "
         f"{sum(1 for h in holes if h <= 3)} clusters with ≤ 3 holes." if holes else ""))
w("")
w("Cluster sizes (distinct exact statements per generalised cluster):")
w("")
SB = ["2", "3", "4", "5-9", "10-19", "20-49", "50+"]
w("| distinct statements | " + " | ".join(SB) + " |")
w("|---|" + "---:|" * len(SB))
for level in ("L1", "L2"):
    h = Counter(bucket(r["distinctStatements"]) for r in gen[level])
    w(f"| {level} | " + " | ".join(str(h.get(b, 0)) for b in SB) + " |")
w("")


def table_gen(level, rows, title):
    w(f"### {title}")
    w("")
    for i, r in enumerate(rows, 1):
        tags = [t for t, f in (("instance", r["anyClass"]), ("one-lemma", r["oneLemma"]),
                               ("automation", r["glue"]), ("ground fact", r["ground"]),
                               ("whole theorem bodies", r["wholeBody"]),
                               ("tight", r["tight"])) if f]
        w(f"{i}. net {r['net']} (optimistic) · {r['theorems']} theorems · {r['occurrences']} occurrences · "
          f"{r['distinctStatements']} distinct statements · {r['holes']} holes · max proof {r['maxProof']}"
          + (f" · _{', '.join(tags)}_" if tags else ""))
        w(f"   - anti-unifier: {code(r['lgg'], 320)}")
        for d, p, s in r["examples"][:2]:
            w(f"   - e.g. in `{d}` (proof {p}): {code(s, 240)}")
    w("")


for level in ("L1", "L2"):
    rows = sorted(gen[level], key=lambda r: (-r["net"], r["key"]))
    table_gen(level, rows[:10], f"Top 10 {level} clusters by optimistic net saving (all kinds, tagged)")
    table_gen(level, [r for r in rows if not r["trivial"]][:15],
              f"Top 15 non-trivial {level} clusters by optimistic net saving (tight or not)")
    clean = [r for r in rows if not r["trivial"] and r["tight"]]
    table_gen(level, clean[:25], f"Top 25 {level} clusters by optimistic net saving among the "
              "non-trivial, tight ones")


# machine-readable
strip = lambda r: {k: v for k, v in r.items() if k not in ("members", "examples")}  # noqa: E731
json.dump({"E": [dict(strip(r), decls=sorted({m["decl"] for m in r["members"]})) for r in
                 sorted(E, key=lambda r: -r["net"])],
           "L1": [strip(r) for r in sorted(gen["L1"], key=lambda r: -r["net"])],
           "L2": [strip(r) for r in sorted(gen["L2"], key=lambda r: -r["net"])]},
          open(OUT / "clusters.json", "w"), ensure_ascii=False, indent=1)
summary = {
    "theorems": n_thm, "candidatePositions": n_all, "nonRootPositions": n_positions, "innerRestatements": n_restate,
    "occurrences": len(cands),
    "totalTheoremProofSize": total_thm_proof, "levels": level_stats, "classes": class_tbl,
    "substantive": {"clusters": len(sub), "netPositive": len(sub_pos), "netSaving": sub_net,
                    "netSavingShare": sub_net / total_thm_proof,
                    "crossModule": len(sub_cross_mod), "sameProof": len(sub_same_proof)},
    "exactQ": dict(exact_counts), "exactClosedByRfl": rfl_closed,
    "probe": {"ran": probe_ran, "tried": len([r for r in _pk if r["key"] in probe]),
              "closed": sum(1 for r in _pk if probe.get(r["key"])),
              "byTactic": dict(Counter(probe[r["key"]] or "none" for r in _pk if r["key"] in probe))},
    "generalised": {lv: {"clusters": len(gen[lv]),
                         "netPositive": sum(1 for r in gen[lv] if r["net"] > 0),
                         "netPositiveNontrivial": sum(
                             1 for r in gen[lv] if r["net"] > 0 and not r["trivial"]),
                         "netSavingNontrivial": sum(
                             r["net"] for r in gen[lv] if r["net"] > 0 and not r["trivial"]),
                         "netPositiveNontrivialTight": sum(
                             1 for r in gen[lv] if r["net"] > 0 and not r["trivial"] and r["tight"]),
                         "netSavingNontrivialTight": sum(
                             r["net"] for r in gen[lv]
                             if r["net"] > 0 and not r["trivial"] and r["tight"])}
                    for lv in ("L1", "L2")},
}
json.dump(summary, open(OUT / "summary.json", "w"), indent=1)

# ---------------------------------------------------------------- verdict
# The numbers and the example statements are computed; the judgement sentences were written
# against the rerun of 2026-11-09 (600 theorems, three slices) and must be re-read if the data
# changes.
auto_cls = ("instance", "automation-glue", "tactic-certificate")
lib_cls = ("in-mathlib", "exact?", "no-lemma", "one-lemma", "in-mathlib-L1", "one-tactic")
E_net = level_stats["E"]["netSaving"]
auto_net = sum(class_tbl[c]["netSaving"] for c in auto_cls)
lib_net = sum(class_tbl[c]["netSaving"] for c in lib_cls)
auto_n = sum(class_tbl[c]["clusters"] for c in auto_cls)
lib_n = sum(class_tbl[c]["clusters"] for c in lib_cls)
sub_open = [r for r in sub_pos if r["exact"] == "open"]
sub_to = [r for r in sub_pos if r["exact"] == "timeout"]
sub_err = [r for r in sub_pos if r["exact"] == "error"]
gs = summary["generalised"]
whole = {lv: [r for r in gen[lv] if r["net"] > 0 and r["wholeBody"]] for lv in ("L1", "L2")}
V = []
v = V.append
v("## Verdict on H2")
v("")
v("**Raw recurrence is common; reuse worth mining was not found in human-written Mathlib.**")
v("")
v(f"1. *Recurrence exists.* {level_stats['E']['recurring']} closed statements occur in ≥ 2 of the {n_thm} "
  f"theorems; they cover {pct(level_stats['E']['shareOfOccurrences'])} of all candidate occurrences and touch "
  f"{level_stats['E']['theoremsWithRecurring']} theorems. Replacing every repeat by a call would remove at most "
  f"{E_net} nodes, {pct(level_stats['E']['netSavingShare'])} of the proof terms (upper estimate).")
v(f"2. *Almost none of it is a discovery.* {pct(triv / nE)} of the recurring statements fall in a trivial class. "
  f"{auto_n} ({pct(auto_n / nE)}) are machine output inside the human proof (typeclass instances, "
  f"`simp`/`rw` congruence plumbing, `ring`/`linarith`/`norm_num` certificates) and carry "
  f"{pct(auto_net / max(1, sum(t['netSaving'] for t in class_tbl.values())))} of the per-class saving. "
  f"{lib_n} ({pct(lib_n / nE)}) are a library lemma or trivially closed: same hash as an existing theorem, closed by `rfl` or "
  "`exact?`, a proof that uses at most one library lemma, or closed by one call of a standard tactic.")
v(f"3. *What is left is small, local, and on inspection not new mathematics.* {len(sub)} statements ({pct(len(sub) / nE)}) "
  f"survive every filter{', including the one-tactic probe' if probe_ran else ' (the one-tactic probe was NOT run for this report)'}; {len(sub_pos)} of them would save anything, together {sub_net} nodes = "
  f"**{pct(sub_net / total_thm_proof)}** of the proof terms. For {len(sub_open)} of those `exact?` finished without finding a "
  f"library lemma, for {len(sub_to)} it ran out of budget"
  + (f", for {len(sub_err)} it failed with an error" if sub_err else "") + ". "
  f"{len(sub_pos) - len(sub_cross_mod)} of the {len(sub_pos)} live inside one file, "
  f"{sum(1 for r in sub_pos if len(r['slices']) >= 2)} cross slices, and {len(sub_same_proof)} have the identical "
  "proof term at every occurrence. The largest three by saving are: "
  + "; ".join(code(r["statement"], 140) + f" ({r['subNet']} nodes, {r['theorems']} theorems)"
              for r in sorted(sub_pos, key=lambda r: (-r["subNet"], r["key"]))[:3])
  + ". These are side computations repeated between sibling theorems of one file, or rewriting residue that the filters "
  "do not recognise; the full list is the second top-25 table. An independent review of the first version of this "
  "analysis drew a seeded sample of 10 of its net-positive 'substantive' statements and found that 9 closed with one "
  "tactic or one library lemma and the tenth was a two-lemma rewrite; that is why the one-tactic probe was added. "
  f"None of the {len(sub_pos)} that remain was shown to be a lemma worth naming, and none was examined by a mathematician; "
  "several are one-line consequences of an existing lemma that the probes do not find. "
  "The realistic number of unnamed lemmas found by exact matching is small and may be zero.")
v(f"4. *Generalisation does not rescue it.* Abstracting literals and instances (L1) adds {gs['L1']['clusters']} "
  "clusters, but they are numeral facts (`0 < 4`, `4 * 0 = 0`); after removing instance / one-lemma / automation / "
  f"ground-fact / whole-theorem-body clusters, {gs['L1']['netPositiveNontrivialTight']} tight ones remain, worth "
  f"{gs['L1']['netSavingNontrivialTight']} nodes if their generalisations are provable. The depth-2 shape (L2) "
  f"gives {gs['L2']['netPositiveNontrivial']} non-trivial clusters with an optimistic "
  f"{gs['L2']['netSavingNontrivial']} nodes, but most anti-unifiers are vacuous (`◻ * ◻ = ◻ * ◻`); only "
  f"{gs['L2']['netPositiveNontrivialTight']} are tight ({gs['L2']['netSavingNontrivialTight']} nodes = "
  f"{pct(gs['L2']['netSavingNontrivialTight'] / total_thm_proof)}). "
  f"{len(whole['L2'])} L2 clusters with positive saving ({sum(r['net'] for r in whole['L2'])} nodes) and {len(whole['L1'])} at L1 are "
  "excluded as whole-theorem-body clusters: their members are nearly the entire proofs of sibling theorems that Mathlib "
  "states and names separately. The first version of this report presented one of them "
  "(`∃ p, 0 < p ∧ ◻ =O[atTop] fun x => exp (-p * x)`, four Hurwitz kernels) as a real parametrised lemma. It is not: "
  "the four are the named theorems `isBigO_atTop_evenKernel_sub`, `isBigO_atTop_cosKernel_sub`, `isBigO_atTop_oddKernel` "
  "and `isBigO_atTop_sinKernel`, each a short proof that already calls a shared lemma `HurwitzKernelBounds.isBigO_atTop_F_*`, "
  "and the anti-unified statement (with an arbitrary function in the hole) is false. No generalised statement was checked "
  "for provability.")
v("")
v("**So: H2 is not supported as a source of new lemmas for human-written Mathlib** (three slices, proofs ≥ "
  f"{run['minTheoremProof']} nodes). The library is already factored by its authors and reviewers; what a hash "
  "finds across proofs is the residue of automation. H2 holds only in the weak sense that proof *terms* are "
  f"redundant (up to {pct(level_stats['E']['netSavingShare'])}), which matters for term size and checking time, "
  "not for readability.")
v("")
v("**What this suggests for machine-generated proofs (not measured here).** The recurrence we did measure "
  "sits almost entirely in the parts of these proofs that a machine wrote: instance synthesis, simp sets, "
  "arithmetic certificates. The human-written skeleton around them barely repeats. A proof produced wholesale "
  "by a generator has no author who states a fact once and names it, so the plausible expectation is that it "
  "looks like the automation residue here (heavy, exact, same-proof repetition) rather than like the skeleton. "
  "That is a hypothesis, not a result: the measurement needed is this same pipeline run on a corpus of generated proofs "
  "(same hashes, same classes, and `Rosette.Lift` to kernel-check the factored result).")
v("")
v("Limits of this measurement:")
v("")
v("- The exact hash is sensitive to the order of hypotheses (local-context order) and to which variables a "
  "proof happens to use, so the same fact with permuted or extra hypotheses is not matched at level E. L1 / L2 "
  "do not fix that either. Recurrence is undercounted to that extent.")
v(f"- `exact?` ran out of budget on {exact_counts.get('timeout', 0)} of {len(exact_tried)} statements"
  + (f" and failed with an error on {exact_counts.get('error', 0)}" if exact_counts.get('error') else "")
  + f" ({BUDGET_K:,}k heartbeats, a tenth of Lean's default); those are left in "
  "whatever later class applies, so the substantive count is an upper bound on discoveries. The one-tactic probe uses a fixed "
  "list of ten tactics with default settings; a statement it does not close can still be a one-line consequence of the library.")
v("- No cluster was actually factored into a shared lemma and kernel-checked; savings are bookkeeping on sizes.")
v("- Savings add DAG sizes of removed subterms; sharing between different clusters in one theorem is counted "
  "more than once. Shares of total proof size are upper estimates.")
v(f"- Candidates are Prop-typed subterms with proof DAG size ≥ {run['minCandidateProof']}; theorems are those with "
  f"proof DAG size ≥ {run['minTheoremProof']} in three slices. Nothing is claimed about other areas or short proofs.")
v("- L1 / L2 anti-unifiers are not checked for provability (`0 < ◻` is false for `◻ = 0`).")
v("- The class rules are heuristics read off names and pretty-printed conclusions; the top-25 tables show the "
  "statements so the labels can be audited. They were not validated on a labelled sample.")
v("")

body = "\n".join(L) + "\n"
head, _, rest = body.partition("\n## Data\n")
body = head + "\n" + "\n".join(V) + "\n## Data\n" + rest
(OUT / "REUSE.md").write_text(body)
print(json.dumps(summary, indent=1))
