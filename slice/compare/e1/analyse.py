#!/usr/bin/env python3
"""Plan node E1: the generated harness set beside K2's arms, on the same mutants.

    python3 compare/e1/analyse.py        -> compare/e1/results/summary.json, compare/e1/results/tables.md

Joins compare/e1/results/raw/<mutant>.json (compare/e1/run.py) with compare/results/results.json (K2, per mutant, arm and
rule). The unit is K2's: a (mutant, rule) pair, for the 23 rules of the K2 comparison; a mutant counts for an arm if the
arm shows at least one of those rules false of it. "Shown false" for a generated harness: the property test fails or does
not finish (K2 counted a hang the same way), or a Kani harness fails at some rung of the ladder.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPARE = HERE.parent
RAW = HERE / "results" / "raw"
K2 = json.loads((COMPARE / "results" / "results.json").read_text())
RULES = json.loads((COMPARE / "rules.json").read_text())["rules"]
RULE = {r["id"]: r for r in RULES}
KINDS = ["safety", "exact", "rejection", "progress", "bound"]
KIND_NAME = {"safety": "safety / never-changes", "exact": "exact-result", "rejection": "rejection-and-unchanged",
             "progress": "progress (1 rule)", "bound": "bound (1 rule)"}
CAND = {"Rule.ledger_rules.k2_whole_agrees_with_batch": "candidate 1: whole batch agrees with the batch applied transfer by transfer",
        "Rule.ledger_rules.k2_batch_agrees_with_transfers": "candidate 2: batch agrees with its transfers applied one at a time"}
K2_ARMS = ["a", "b_plain", "b_edge", "c", "d"]


def rid(rule):
    return f"Spec.{RULE[rule]['crate']}.{rule}"


def lab(g):
    """One wording for a rung, whatever the label stored with the run says."""
    a, b = g.get("accounts"), g.get("transfers")
    if a is None and b is None:
        return "no size bound"
    return " and ".join(([f"up to {a} accounts"] if a is not None else []) + ([f"up to {b} transfer{'s' if b != 1 else ''}"] if b is not None else []))


def gen_of(ev, reading):
    """(property shows it false, Kani shows it false, detail) for one reading of one run."""
    r = (ev.get("readings") or {}).get(reading)
    if r is None:
        return None
    p = r["property"]
    rungs = r["bounded"]["rungs"]
    return {"prop": p.get("status") in ("fail", "hang"), "prop_status": p.get("status"), "prop_at": p.get("calls_to_first_failure"),
            "prop_ms": p.get("elapsed_ms"), "prop_witness": p.get("witness"),
            # a Kani failure whose concrete input does NOT fail when replayed on the compiled Rust is not counted (it was
            # seen once: a stale Kani build after a mutant whose loop does not terminate; see E1_TRADES.md)
            "kani": any(g["status"] == "failed" for g in rungs) and r["bounded"].get("replay") not in ("holds", "out-of-scope", "mismatch"),
            "kani_unreproduced": any(g["status"] == "failed" for g in rungs) and r["bounded"].get("replay") in ("holds", "out-of-scope", "mismatch"),
            "kani_rung": next((lab(g) for g in rungs if g["status"] == "failed"), None),
            "kani_checks": next((g["failed_checks"] for g in rungs if g["status"] == "failed"), []),
            "kani_timeouts": [lab(g) for g in rungs if g["status"] == "timeout"], "kani_verified": [lab(g) for g in rungs if g["status"] == "verified"],
            "kani_secs": round(sum(g["secs"] or 0 for g in rungs), 1), "kani_witness": r["bounded"].get("witness"), "kani_replay": r["bounded"].get("replay"),
            "mismatch": p.get("status") == "mismatch"}


def md_table(head, rows):
    return ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows] + [""]


def main():
    raw = {p.stem: json.loads(p.read_text()) for p in sorted(RAW.glob("*.json"))}
    k2 = {m["id"]: m for m in K2["mutants"]}
    missing = [i for i in k2 if i not in raw]
    recs = []
    for mid, km in k2.items():
        m = raw.get(mid)
        if m is None or "evidence" not in m:
            continue
        ev = m["evidence"]
        rec = {"id": mid, "set": km["set"], "author": km.get("author"), "crate": km["crate"], "description": km["description"], "pairs": {}, "cand": {},
               "secs": ev.get("cost", {}), "total_secs": m.get("total_secs"), "error": ev.get("error")}
        for r in RULES:
            if r["crate"] != km["crate"]:
                continue
            g = gen_of(ev, rid(r["id"]))
            det = {a: r["id"] in km["detected_by"].get(a, []) for a in K2_ARMS}
            rec["pairs"][r["id"]] = {"k2": det, "k2_any": any(det.values()), "k2_hand": det["b_plain"] or det["b_edge"] or det["c"], "gen": g}
        for c in CAND:
            if km["crate"] == "ledger":
                rec["cand"][c] = gen_of(ev, c)
        rec["mismatches"] = [i for i, r in (ev.get("readings") or {}).items() if r["property"].get("status") == "mismatch"]
        recs.append(rec)
    base = raw.get("baseline", {}).get("evidence")

    def sets():
        yield "cargo-mutants, wallet", [r for r in recs if r["set"] == "cargo-mutants" and r["crate"] == "wallet"]
        yield "cargo-mutants, ledger", [r for r in recs if r["set"] == "cargo-mutants" and r["crate"] == "ledger"]
        yield "cargo-mutants, both", [r for r in recs if r["set"] == "cargo-mutants"]
        yield "hand-written, wallet", [r for r in recs if r["set"] == "hand-written" and r["crate"] == "wallet"]
        yield "hand-written, ledger (builder)", [r for r in recs if r["set"] == "hand-written" and r["crate"] == "ledger" and r["author"] == "builder"]
        yield "hand-written, ledger (reviewer)", [r for r in recs if r["set"] == "hand-written" and r["crate"] == "ledger" and r["author"] == "reviewer"]
        yield "hand-written, all", [r for r in recs if r["set"] == "hand-written"]

    def caught(rec, f):
        return any(f(p) for p in rec["pairs"].values())
    gp = lambda p: bool(p["gen"] and p["gen"]["prop"])        # noqa: E731
    gk = lambda p: bool(p["gen"] and p["gen"]["kani"])        # noqa: E731
    ge = lambda p: gp(p) or gk(p)                              # noqa: E731
    o = [f"Generated from {len(recs)} of {len(k2)} mutant runs" + (f" (NOT YET RUN: {', '.join(missing)})" if missing else "") + ".", ""]
    summary = {"runs": len(recs), "missing": missing, "sets": {}, "kinds": {}}

    # ---- 1. mutants
    o += ["### Detection, mutant by mutant (through at least one of the 23 rules)", ""]
    rows = []
    for name, rs in sets():
        row = [name, len(rs)] + [sum(caught(r, lambda p, a=a: p["k2"][a]) for r in rs) for a in K2_ARMS] + [
            sum(caught(r, gp) for r in rs), sum(caught(r, gk) for r in rs), sum(caught(r, ge) for r in rs),
            sum(not caught(r, lambda p: p["k2_any"]) for r in rs), sum(not caught(r, ge) for r in rs),
            sum(not caught(r, ge) and not any(c and (c["prop"] or c["kani"]) for c in r["cand"].values()) for r in rs)]
        rows.append(row)
        summary["sets"][name] = dict(zip(["mutants", "k2_rows", "k2_plain", "k2_edge", "k2_kani", "k2_lean", "gen_prop", "gen_kani", "gen_either",
                                          "k2_no_arm", "gen_none", "gen_none_with_candidates"], row[1:]))
    o += md_table(["Mutant set", "Mutants", "K2 a. rows", "K2 b. plain", "K2 b. edge", "K2 c. Kani", "K2 d. Lean (incl. confirmed)",
                   "GENERATED property test", "GENERATED Kani ladder", "GENERATED either", "K2: no arm at all", "GENERATED: neither",
                   "GENERATED: neither, with the two candidate rules added"], rows)

    # ---- 2. pairs by kind
    for label, sel in (("Tool set (cargo-mutants)", "cargo-mutants"), ("Hand-written set", "hand-written")):
        rs = [r for r in recs if r["set"] == sel]
        o += [f"### Detection by kind of rule: {label}", "",
              "Unit: a (mutant, rule) pair in which some K2 arm shows the rule false of the mutant.", ""]
        rows = []
        tot = Counter()
        for k in KINDS + ["all"]:
            pairs = [(r["id"], rule, p) for r in rs for rule, p in r["pairs"].items() if k == "all" or RULE[rule]["kind"] == k]
            anyp = [x for x in pairs if x[2]["k2_any"]]
            row = [KIND_NAME.get(k, "all 23 rules"), len(anyp), sum(x[2]["k2"]["b_edge"] for x in anyp), sum(x[2]["k2"]["c"] for x in anyp),
                   sum(gp(x[2]) for x in anyp), sum(gk(x[2]) for x in anyp), sum(ge(x[2]) for x in anyp),
                   sum(ge(x[2]) for x in pairs if not x[2]["k2_any"]),
                   sum(1 for x in pairs if x[2]["gen"] and x[2]["gen"]["kani_timeouts"] and not gk(x[2]))]
            rows.append(row)
            summary["kinds"][f"{sel}:{k}"] = dict(zip(["k2_any", "k2_edge", "k2_kani", "gen_prop", "gen_kani", "gen_either", "gen_only", "kani_some_rung_no_answer"], row[1:]))
        o += md_table(["Kind of rule", "Pairs where some K2 arm shows the rule false", "K2 b. edge (hand-written)", "K2 c. Kani (hand-written)",
                       "GENERATED property test", "GENERATED Kani ladder", "GENERATED either", "GENERATED shows false, no K2 arm did",
                       "Kani: not failed, and no answer at some rung"], rows)

    # ---- 3. what the generated set misses, and what only it finds
    miss_hand = [(r["id"], rule, p) for r in recs for rule, p in r["pairs"].items() if p["k2_hand"] and not ge(p)]
    miss_any = [(r["id"], rule, p) for r in recs for rule, p in r["pairs"].items() if p["k2_any"] and not ge(p)]
    only_gen = [(r["id"], rule, p) for r in recs for rule, p in r["pairs"].items() if ge(p) and not p["k2_any"]]
    summary["missed_vs_hand_arms"] = [(a, b) for a, b, _ in miss_hand]
    summary["missed_vs_any_arm"] = [(a, b) for a, b, _ in miss_any]
    summary["only_generated"] = [(a, b) for a, b, _ in only_gen]
    o += ["### Pairs a hand-written property test or Kani harness of K2 found and the generated set did not", ""]
    if miss_hand:
        o += md_table(["Mutant", "Rule", "K2 arms that found it", "Generated property test", "Generated Kani"],
                      [[a, b, ", ".join(x for x in K2_ARMS if p["k2"][x]), p["gen"]["prop_status"] if p["gen"] else "-",
                        ("no answer at: " + "; ".join(p["gen"]["kani_timeouts"]) if p["gen"] and p["gen"]["kani_timeouts"] else "verified at every rung") if p["gen"] else "-"]
                       for a, b, p in miss_hand])
    else:
        o += ["None.", ""]
    extra = [x for x in miss_any if x not in miss_hand]
    o += ["### Pairs only K2's example rows or Lean arm found and the generated set did not", ""]
    o += (md_table(["Mutant", "Rule", "K2 arms that found it"], [[a, b, ", ".join(x for x in K2_ARMS if p["k2"][x])] for a, b, p in extra]) if extra else ["None.", ""])
    o += ["### Pairs the generated set shows false and no K2 arm did", ""]
    if only_gen:
        o += md_table(["Mutant", "Rule", "By", "Input", "Replayed on the compiled Rust"],
                      [[a, b, " + ".join((["property test"] if gp(p) else []) + ([f"Kani ({p['gen']['kani_rung']})"] if gk(p) else [])),
                        "`" + json.dumps(p["gen"]["prop_witness"] or p["gen"]["kani_witness"], ensure_ascii=False) + "`",
                        (p["gen"]["kani_replay"] or "-") if gk(p) and not gp(p) else "found there"] for a, b, p in only_gen])
    else:
        o += ["None.", ""]

    # ---- 4. which generated harness finds what
    o += ["### Property test against Kani ladder, within the generated set", ""]
    rows = []
    for label, sel in (("tool", "cargo-mutants"), ("hand-written", "hand-written")):
        pairs = [p for r in recs if r["set"] == sel for p in r["pairs"].values()]
        rows.append([label, sum(ge(p) for p in pairs), sum(gp(p) and gk(p) for p in pairs), sum(gp(p) and not gk(p) for p in pairs),
                     sum(gk(p) and not gp(p) for p in pairs),
                     sum(1 for p in pairs if p["gen"] and p["gen"]["prop_status"] == "hang")])
    o += md_table(["Set", "Pairs shown false by either", "by both", "by the property test only", "by Kani only", "property test did not finish (counted as shown false)"], rows)
    rung = Counter(p["gen"]["kani_rung"] for r in recs for p in r["pairs"].values() if gk(p))
    o += ["Rung of the ladder at which Kani first fails a pair: " + "; ".join(f"{k}: {v}" for k, v in rung.most_common()) + ".", ""]
    summary["first_failing_rung"] = dict(rung)
    late = sorted((p["gen"]["prop_at"] or 0, r["id"], rule) for r in recs for rule, p in r["pairs"].items() if gp(p) and p["gen"]["prop_status"] == "fail")
    if late:
        ats = [x[0] for x in late]
        o += [f"Generated input at which the property test first fails: median {statistics.median(ats):.0f}, largest {max(ats)} "
              f"({late[-1][1]}, {late[-1][2]}); {sum(a > 1000 for a in ats)} of {len(ats)} pairs after the 1,000th.", ""]
        summary["prop_first_failure"] = {"median": statistics.median(ats), "max": max(ats), "after_1000": sum(a > 1000 for a in ats), "pairs": len(ats)}

    # ---- 5. the survivors and the candidate rules
    o += ["### The mutants no K2 arm caught, and the two candidate rules", ""]
    surv = [r for r in recs if not caught(r, lambda p: p["k2_any"])]
    rows = []
    for r in surv:
        row = [r["id"], r["description"][:90], "yes" if caught(r, ge) else "no"]
        for c in CAND:
            g = r["cand"].get(c)
            row.append("-" if g is None else ("FALSE: " + " + ".join((["property test"] if g["prop"] else []) + ([f"Kani ({g['kani_rung']})"] if g["kani"] else []))
                                             + f" at `{json.dumps(g['prop_witness'] or g['kani_witness'], ensure_ascii=False)}`") if g["prop"] or g["kani"] else "not shown false")
        rows.append(row)
    o += md_table(["Mutant", "Change", "Shown false through one of the 23 rules by a generated harness"] + list(CAND.values()), rows)
    summary["survivors"] = {r["id"]: {c: bool(g and (g["prop"] or g["kani"])) for c, g in r["cand"].items()} for r in surv}
    lm = [r for r in recs if r["crate"] == "ledger"]
    for c, name in CAND.items():
        n = sum(1 for r in lm if r["cand"].get(c) and (r["cand"][c]["prop"] or r["cand"][c]["kani"]))
        o.append(f"- {name}: shown false of {n} of {len(lm)} ledger mutants (tool {sum(1 for r in lm if r['set'] == 'cargo-mutants' and r['cand'].get(c) and (r['cand'][c]['prop'] or r['cand'][c]['kani']))} of "
                 f"{sum(r['set'] == 'cargo-mutants' for r in lm)}, hand-written {sum(1 for r in lm if r['set'] == 'hand-written' and r['cand'].get(c) and (r['cand'][c]['prop'] or r['cand'][c]['kani']))} of "
                 f"{sum(r['set'] == 'hand-written' for r in lm)}).")
        summary.setdefault("candidates", {})[c] = n
    o.append("")

    # ---- 6. the unmutated code
    if base:
        o += ["### The unmutated code", ""]
        rows = []
        for r in RULES:
            g = gen_of(base, rid(r["id"]))
            if g is None:
                continue
            rows.append([r["id"], r["kind"], f"{g['prop_status']} ({g['prop_ms']} ms)", "; ".join(g["kani_verified"]) or "-",
                         "; ".join(g["kani_timeouts"]) or "-", "FAILED at " + g["kani_rung"] if g["kani"] else "-", g["kani_secs"]])
        for c in CAND:
            g = gen_of(base, c)
            if g:
                rows.append([c.split(".")[-1], "candidate", f"{g['prop_status']} ({g['prop_ms']} ms)", "; ".join(g["kani_verified"]) or "-",
                             "; ".join(g["kani_timeouts"]) or "-", "FAILED at " + g["kani_rung"] if g["kani"] else "-", g["kani_secs"]])
        o += md_table(["Rule", "Kind", "Generated property test", "Kani: verified with", f"Kani: no answer in {base.get('kani_timeout')} s with", "Kani: failed", "Solver seconds (answered rungs)"], rows)
        summary["baseline_cost"] = base.get("cost")
        o += [f"Baseline cost: {json.dumps(base.get('cost'))}", ""]

    # ---- 7. cost
    o += ["### Cost of the generated harnesses on the mutants (seconds, wall-clock)", ""]
    rows = []
    for crate in ("wallet", "ledger"):
        rs = [r for r in recs if r["crate"] == crate and not r["error"]]
        if not rs:
            continue
        for key, name in (("property_secs", "property tests, every reading of the crate"), ("bounded_secs", "Kani ladder, the K2 rules of the crate (and the 2 candidates)"),
                          ("bounded_witness_secs", "Kani: concrete input of each failing rule, and its replay")):
            xs = [r["secs"].get(key) or 0 for r in rs]
            rows.append([f"{crate} ({len(rs)})", name, f"{statistics.median(xs):.1f}", f"{max(xs):.1f}", f"{sum(xs):.0f}"])
        xs = [r["total_secs"] or 0 for r in rs]
        rows.append([f"{crate} ({len(rs)})", "whole run (build included)", f"{statistics.median(xs):.1f}", f"{max(xs):.1f}", f"{sum(xs):.0f}"])
    o += md_table(["Crate (mutants)", "What", "Median per mutant", "Largest", "All mutants"], rows)
    summary["mismatch_runs"] = {r["id"]: r["mismatches"] for r in recs if r["mismatches"]}
    o += [f"READING MISMATCH (generated predicate against the tree evaluator) in any mutant run: "
          f"{sum(len(r['mismatches']) for r in recs)} readings in {sum(bool(r['mismatches']) for r in recs)} runs"
          + ("" if not summary["mismatch_runs"] else ": " + json.dumps(summary["mismatch_runs"])) + ".", ""]
    unrep = [(r["id"], rule) for r in recs for rule, p in r["pairs"].items() if p["gen"] and p["gen"]["kani_unreproduced"]]
    summary["kani_failed_not_reproduced"] = unrep
    o += [f"Kani failures whose concrete input did not fail when replayed on the compiled Rust (not counted as shown false): {len(unrep)}"
          + ("" if not unrep else ": " + ", ".join(f"{a} / {b}" for a, b in unrep)) + ".", ""]
    noinput = sum(1 for r in recs for p in r["pairs"].values() if p["gen"] and p["gen"]["kani"] and p["gen"]["kani_replay"] == "Kani gave no concrete input")
    summary["kani_failed_no_input"] = noinput
    o += [f"Kani failures with no concrete input to replay (the failed check is an unwinding assertion: the loop does not terminate within the bound): {noinput} pairs, counted as shown false as K2 did.", ""]
    errs = [r["id"] for r in recs if r["error"]]
    if errs:
        o += [f"Runs in which the generated property tests did not build: {', '.join(errs)}.", ""]
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n")
    (HERE / "results" / "pairs.json").write_text(json.dumps(recs, indent=1, ensure_ascii=False) + "\n")
    (HERE / "results" / "tables.md").write_text("\n".join(o) + "\n")
    print("\n".join(o))
    return 0


if __name__ == "__main__":
    sys.exit(main())
