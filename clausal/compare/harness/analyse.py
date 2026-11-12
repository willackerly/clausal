#!/usr/bin/env python3
"""Turn results/raw/*.json into results/results.json (everything, per mutant, arm and rule),
results/summary.json (the numbers of the tables) and results/tables.md (the tables of TRADES.md).

    python3 harness/analyse.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import COMPARE, RESULTS, RULE, RULE_IDS, RULES, SNAPSHOT, feature_index  # noqa: E402

RAW = RESULTS / "raw"
KINDS = ["safety", "exact", "rejection", "progress", "bound"]
KIND_NAME = {"safety": "safety / never-changes", "exact": "exact-result", "rejection": "rejection-and-unchanged",
             "progress": "progress (1 rule)", "bound": "bound (1 rule)"}
ARMS = ["a", "b_plain", "b_edge", "c", "d"]
ARM_NAME = {"a": "a. example rows", "b_plain": "b. proptest, plain", "b_edge": "b. proptest, edge", "c": "c. Kani", "d": "d. Lean"}
FALSE = ("REFUTED", "COUNTEREXAMPLE")


def load():
    raw = {p.stem: json.loads(p.read_text()) for p in sorted(RAW.glob("*.json"))}
    confirm = {}
    for p in sorted((RAW / "confirm").glob("*.json")) if (RAW / "confirm").exists() else []:
        confirm[p.stem] = json.loads(p.read_text())
    return raw, confirm


def analyse_mutant(m, base, index, confirm):
    """Per rule and arm, what happened. Returns the record stored in results.json."""
    crate = m["crate"]
    literal_ids = [s[2] for name, spans in index.items() if name != "negative.feature" for s in spans
                   if s[4] == "Scenario" and not any(t.startswith("@expect") for t in s[3])]
    rec = {k: m.get(k) for k in ("id", "set", "author", "crate", "fn", "description", "genre", "viable")}
    if not m.get("viable", True):
        rec["class"] = "unviable"
        rec["build_output"] = m.get("build_output", "")[-400:]
        return rec
    rec["oracle"] = {"differs": m["oracle"]["differs"], "witness": (m["oracle"]["witnesses"] or [{}])[0].get("witness"),
                     "tried": m["oracle"]["tried"], "ok": m["oracle"]["ok"]}
    rules = {}
    feature = crate
    d = m.get("d", {})
    dfail = set((d.get("proofs") or {}).get("failed", []))
    dbuilt = set((d.get("proofs") or {}).get("built", []))
    cf = (confirm.get(m["id"]) or {}).get("rules", {})
    for r in RULE_IDS:
        if RULE[r]["crate"] != crate:
            continue
        out = {}
        # a
        brows = base["a"]["rows"].get(r, {})
        mrows = m["a"]["rows"].get(r, {})
        failing = sorted(l for l, x in brows.items() if x["status"] == "pass" and mrows.get(l, {}).get("status") != "pass")
        if "hang" in mrows:
            failing = ["hang"]
        out["a"] = {"detected": bool(failing), "rows_failing": failing, "rows": len(brows)}
        # b
        for prof in ("plain", "edge"):
            pr = m["b"][prof]["rules"].get(r)
            out[f"b_{prof}"] = ({"detected": pr["status"] in ("fail", "hang"), "status": pr["status"], "row": pr["row"],
                                 "calls_to_first_failure": pr["calls_to_first_failure"], "ms": pr["elapsed_ms"], "message": pr["message"][:200]}
                                if pr else {"detected": False, "status": "not run"})
        # c
        cr = m["c"]["rules"].get(r)
        out["c"] = ({"detected": cr["status"] == "failed", "status": cr["status"], "secs": cr["secs"], "failed_checks": cr["failed_checks"]}
                    if cr else {"detected": False, "status": "not run"})
        # d
        key = f"{feature}.{r}"
        verdict = (d.get("verdicts") or {}).get(key)
        module = f"Wallet.Proofs.{feature}.{r}"
        search = ((d.get("search") or {}).get(key) or {})
        model_rows = [x["line"] for x in search.get("rows", []) if x["check"] not in ("pass", "givenFalse")]
        c = cf.get(r)
        if verdict in FALSE:
            outcome = "shown false (kernel-checked)" if verdict == "REFUTED" else "shown false (search on the model)"
        elif model_rows and verdict is not None and not verdict.startswith("PROVED"):
            # the pipeline evaluated a failing Examples row on the model but its search did not turn it into a verdict
            outcome = "shown false (an Examples row fails on the model)"
        elif verdict and verdict.startswith("PROVED"):
            outcome = "still proved"
        elif verdict is None and d.get("proofs") is None:
            # the pipeline stopped before any proof was checked (the generated model does not build)
            outcome = "no model"
        elif verdict is None and module in dbuilt:
            # the proof was checked; the pipeline stopped later (evaluating the model crashed), so no verdict was printed
            outcome = "still proved"
        elif verdict == "TESTED-ONLY" or (verdict is None and module in dfail):
            outcome = "proof lost, confirmed false" if c and c.get("confirmed") else "proof lost, not shown false"
        else:
            outcome = f"other: {verdict}"
        out["d"] = {"detected": outcome.startswith("shown false") or outcome == "proof lost, confirmed false", "outcome": outcome,
                    "verdict": verdict, "proof_module_failed": module in dfail, "search_bad": search.get("bad"),
                    "model_rows_failing": model_rows, "confirm": c,
                    "pipeline_stopped_before_verdict": verdict is None}
        rules[r] = out
    rec["rules"] = rules
    # literal-value scenarios (not rules): failing on the compiled Rust
    lit = []
    for sid in literal_ids:
        if not any(sid in (s[2] for s in spans) for name, spans in index.items() if name.startswith(crate)):
            continue
        brows = base["a"]["rows"].get(sid, {})
        mrows = m["a"]["rows"].get(sid, {})
        if any(x["status"] == "pass" and mrows.get(l, {}).get("status") != "pass" for l, x in brows.items()) or "hang" in mrows:
            lit.append(sid)
    rec["literal_scenarios_failing"] = lit
    rec["detected_by"] = {a: sorted(r for r, o in rules.items() if o[a]["detected"]) for a in ARMS}
    rec["d_proof_lost_not_shown_false"] = sorted(r for r, o in rules.items() if o["d"]["outcome"] == "proof lost, not shown false")
    # a lost proof where the rule nevertheless holds as far as the other arms can tell: Kani verifies it (within its
    # bounds) and neither proptest profile finds a failing case. This is proof brittleness, not detection.
    rec["d_proof_lost_rule_holds_per_kani"] = sorted(r for r, o in rules.items() if o["d"]["outcome"] == "proof lost, not shown false"
                                                     and o["c"].get("status") == "verified" and not o["b_plain"]["detected"] and not o["b_edge"]["detected"])
    rec["d_still_proved"] = sorted(r for r, o in rules.items() if o["d"]["outcome"] == "still proved")
    rec["d_no_verdict"] = sorted(r for r, o in rules.items() if o["d"]["outcome"] == "no model")
    rec["c_timeouts"] = sorted(r for r, o in rules.items() if o["c"].get("status") == "timeout")
    rec["d_pipeline"] = {"exit": d.get("exit"), "timeout": d.get("timeout"), "translated": d.get("translated"),
                         "steps_reached": d.get("steps_reached"), "lemma_modules_failed": sorted(x for x in dfail if ".Lemmas." in x)}
    rec["secs"] = {"a": m["a"]["secs"], "b_plain": m["b"]["plain"]["secs"], "b_edge": m["b"]["edge"]["secs"], "c": m["c"]["secs"], "d": d.get("secs"),
                   "a_build": m["a"]["build_secs"], "b_build": m["b"]["build_secs"], "c_build": m["c"]["build_secs"]}
    # disagreement: an arm detects through a rule the kernel still accepts as proved of the mutant
    rec["disagreements"] = sorted(f"{a}:{r}" for r, o in rules.items() if o["d"]["outcome"] == "still proved"
                                  for a in ("a", "b_plain", "b_edge", "c") if o[a]["detected"])
    any_arm = any(rec["detected_by"][a] for a in ARMS)
    if any_arm:
        rec["class"] = "detected"
    elif not rec["oracle"]["differs"]:
        rec["class"] = "no arm, no difference found"
    else:
        rec["class"] = "no arm, behaviour differs"
    return rec


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def short(rules, crate_rules=None):
    return ", ".join(rules) if rules else "-"


def main():
    raw, confirm = load()
    base = raw.pop("baseline")
    index = feature_index(SNAPSHOT)
    records = [analyse_mutant(m, base, index, confirm) for m in raw.values() if "harness_error" not in m]
    errors = [m["id"] for m in raw.values() if "harness_error" in m]
    order = {m["id"]: k for k, m in enumerate(json.loads((COMPARE / "mutants/cargo-mutants.json").read_text())["mutants"]
                                              + json.loads((COMPARE / "mutants/hand-written.json").read_text())["mutants"])}
    records.sort(key=lambda r: order[r["id"]])
    T = {}
    summary = {"errors": errors}

    # ---- baseline: every arm discharges every rule on the unmutated code
    brow = []
    for r in RULES:
        rid = r["id"]
        key = f"{r['crate']}.{rid}"
        brow.append([rid, KIND_NAME[r["kind"]].split(" (")[0], len(base["a"]["rows"].get(rid, {})),
                     "pass" if all(x["status"] == "pass" for x in base["a"]["rows"].get(rid, {}).values()) else "FAIL",
                     base["b"]["plain"]["rules"][rid]["status"], base["b"]["edge"]["rules"][rid]["status"],
                     f"{base['c']['rules'][rid]['status']} ({base['c']['rules'][rid]['secs']:.0f} s)", base["d"]["verdicts"].get(key)])
    T["baseline"] = md_table(["Rule", "Kind", "Rows", "a", "b plain", "b edge", "c (wall-clock)", "d"], brow)

    # ---- per set and crate: counts
    def count_rows(recs):
        viable = [r for r in recs if r["class"] != "unviable"]
        n = len(viable)
        det = lambda a: sum(1 for r in viable if r["detected_by"][a])  # noqa: E731
        d_own = sum(1 for r in viable if any(o["d"]["outcome"].startswith("shown false") for o in r["rules"].values()))
        d_conf_only = sum(1 for r in viable if r["detected_by"]["d"] and not any(o["d"]["outcome"].startswith("shown false") for o in r["rules"].values()))
        lost_only = sum(1 for r in viable if not r["detected_by"]["d"] and r["d_proof_lost_not_shown_false"])
        none = sum(1 for r in viable if not any(r["detected_by"][a] for a in ARMS))
        return {"mutants": len(recs), "unviable": len(recs) - n, "viable": n, "a": det("a"), "b_plain": det("b_plain"), "b_edge": det("b_edge"),
                "c": det("c"), "d": det("d"), "d_shown_false_by_pipeline": d_own, "d_confirmed_only": d_conf_only,
                "d_proof_lost_only": lost_only, "no_arm": none, "d_no_model": sum(1 for r in viable if r["d_no_verdict"]),
                "d_confirmed_on_rust_only": sum(1 for r in viable if any((o["d"].get("confirm") or {}).get("confirmed_on", "") and "Rust only" in (o["d"]["confirm"]["confirmed_on"] or "") and o["d"]["outcome"] == "proof lost, confirmed false" for o in r["rules"].values())),
                "literal_only": sum(1 for r in viable if not any(r["detected_by"][a] for a in ARMS) and r["literal_scenarios_failing"]),
                "oracle_no_difference": sum(1 for r in viable if not r["oracle"]["differs"])}
    groups = [("cargo-mutants, wallet", lambda r: r["set"] == "cargo-mutants" and r["crate"] == "wallet"),
              ("cargo-mutants, ledger", lambda r: r["set"] == "cargo-mutants" and r["crate"] == "ledger"),
              ("cargo-mutants, both", lambda r: r["set"] == "cargo-mutants"),
              ("hand-written, wallet", lambda r: r["set"] == "hand-written" and r["crate"] == "wallet"),
              ("hand-written, ledger (builder)", lambda r: r["set"] == "hand-written" and r["crate"] == "ledger" and r.get("author") == "builder"),
              ("hand-written, ledger (reviewer)", lambda r: r["set"] == "hand-written" and r.get("author") == "reviewer"),
              ("hand-written, all", lambda r: r["set"] == "hand-written")]
    summary["counts"] = {name: count_rows([r for r in records if f(r)]) for name, f in groups}
    T["counts"] = md_table(
        ["Mutant set", "Mutants", "Unviable", "Viable", "a. rows", "b. plain", "b. edge", "c. Kani", "d. Lean (shown false by the pipeline + confirmed with another arm's input)",
         "d: proof lost only, nothing shown false", "d: no model (pipeline stops)", "No arm at all", "... of which a literal scenario fails", "Oracle finds no difference"],
        [[name, c["mutants"], c["unviable"], c["viable"], c["a"], c["b_plain"], c["b_edge"], c["c"],
          f"{c['d']} ({c['d_shown_false_by_pipeline']} + {c['d_confirmed_only']})", c["d_proof_lost_only"], c["d_no_model"], c["no_arm"], c["literal_only"], c["oracle_no_difference"]]
         for name, c in summary["counts"].items()])

    # ---- matrix by kind of rule
    def kind_matrix(recs, label):
        viable = [r for r in recs if r["class"] != "unviable"]
        rows, data = [], {}
        for k in KINDS:
            krules = [x["id"] for x in RULES if x["kind"] == k]
            # pairs (mutant, rule of this kind) for which some arm shows the rule false of the mutant
            pairs = [(r, rid) for r in viable for rid in krules if rid in r["rules"] and any(r["rules"][rid][a]["detected"] for a in ARMS)]
            muts = {r["id"] for r, _ in pairs}
            cell = {}
            for a in ARMS:
                pa = sum(1 for r, rid in pairs if r["rules"][rid][a]["detected"])
                ma = len({r["id"] for r, rid in pairs if r["rules"][rid][a]["detected"]})
                cell[a] = {"pairs": pa, "mutants": ma}
            own = sum(1 for r, rid in pairs if r["rules"][rid]["d"]["outcome"].startswith("shown false"))
            ctime = sum(1 for r in viable for rid in krules if rid in r["rules"] and r["rules"][rid]["c"].get("status") == "timeout")
            lost = sum(1 for r in viable for rid in krules if rid in r["rules"] and r["rules"][rid]["d"]["outcome"] == "proof lost, not shown false")
            lost_holds = sum(1 for r in viable for rid in krules if rid in r["d_proof_lost_rule_holds_per_kani"])
            still = sum(1 for r in viable for rid in krules if rid in r["rules"] and r["rules"][rid]["d"]["outcome"] == "still proved")
            considered = sum(1 for r in viable for rid in krules if rid in r["rules"])
            data[k] = {"rules": len(krules), "pairs": len(pairs), "mutants": len(muts), "arms": cell, "d_pairs_shown_false_by_pipeline": own,
                       "c_timeouts": ctime, "d_proof_lost_not_shown_false": lost,
                       "d_proof_lost_rule_verified_by_kani": lost_holds, "d_still_proved": still, "pairs_considered": considered}
            rows.append([KIND_NAME[k], len(krules), f"{len(pairs)} ({len(muts)})"]
                        + [f"{cell[a]['pairs']} ({cell[a]['mutants']})" for a in ("a", "b_plain", "b_edge", "c")]
                        + [f"{cell['d']['pairs']} ({cell['d']['mutants']}); {own} by its own search", ctime, f"{lost} ({lost_holds})", still, considered])
        summary.setdefault("by_kind", {})[label] = data
        return md_table(["Kind of rule", "Rules", "Rule shown false of a mutant by some arm: pairs (mutants)", "a. rows", "b. plain", "b. edge", "c. Kani",
                         "d. Lean", "Kani timeouts (pairs)", "Lean: proof lost, not shown false (of which Kani verifies the rule on the mutant)", "Lean: still proved", "All pairs"], rows)
    T["kind_tool"] = kind_matrix([r for r in records if r["set"] == "cargo-mutants"], "cargo-mutants")
    T["kind_hand"] = kind_matrix([r for r in records if r["set"] == "hand-written"], "hand-written")

    # ---- short form of the kind matrix (pairs only), and the Lean outcomes of every pair
    def kind_short(label):
        d = summary["by_kind"][label]
        return md_table(["Kind of rule", "Pairs where some arm shows the rule false", "a. rows", "b. plain", "b. edge", "c. Kani", "d. Lean (of which by its own search)"],
                        [[KIND_NAME[k].replace(" (1 rule)", "") + f" ({d[k]['rules']} rule{'s' if d[k]['rules'] > 1 else ''})", d[k]["pairs"]]
                         + [d[k]["arms"][a]["pairs"] for a in ("a", "b_plain", "b_edge", "c")]
                         + [f"{d[k]['arms']['d']['pairs']} ({d[k]['d_pairs_shown_false_by_pipeline']})"] for k in KINDS]
                        + [["all 23 rules", sum(d[k]["pairs"] for k in KINDS)] + [sum(d[k]["arms"][a]["pairs"] for k in KINDS) for a in ("a", "b_plain", "b_edge", "c")]
                           + [f"{sum(d[k]['arms']['d']['pairs'] for k in KINDS)} ({sum(d[k]['d_pairs_shown_false_by_pipeline'] for k in KINDS)})"]])
    T["kind_short_tool"] = kind_short("cargo-mutants")
    T["kind_short_hand"] = kind_short("hand-written")

    def lean_outcomes():
        rows = []
        cats = [("still proved", lambda o: o["d"]["outcome"] == "still proved"),
                ("shown false by the pipeline's own search, kernel-checked refutation", lambda o: o["d"]["outcome"] == "shown false (kernel-checked)"),
                ("shown false by the pipeline's own search, on the model only", lambda o: o["d"]["outcome"] in ("shown false (search on the model)", "shown false (an Examples row fails on the model)")),
                ("proof lost, confirmed false: another arm's input fails on the Lean model and the compiled Rust",
                 lambda o: o["d"]["outcome"] == "proof lost, confirmed false" and "Lean model" in (o["d"]["confirm"]["confirmed_on"] or "")),
                ("proof lost, confirmed false on the compiled Rust only (the pipeline crashes evaluating the model)",
                 lambda o: o["d"]["outcome"] == "proof lost, confirmed false" and "Lean model" not in (o["d"]["confirm"]["confirmed_on"] or "")),
                ("proof lost, not shown false", lambda o: o["d"]["outcome"] == "proof lost, not shown false"),
                ("no model (the generated Lean does not build)", lambda o: o["d"]["outcome"] == "no model")]
        tot = {}
        for name, f in cats:
            row = [name]
            for st in ("cargo-mutants", "hand-written"):
                n = sum(1 for r in records if r["set"] == st and r.get("rules") for o in r["rules"].values() if f(o))
                tot[st] = tot.get(st, 0) + n
                row.append(n)
            rows.append(row)
        rows.append(["all pairs (every rule of the mutated crate, every mutant)", tot["cargo-mutants"], tot["hand-written"]])
        return md_table(["Outcome for the rule's proof on the mutant", "Tool set", "Hand-written set"], rows)
    T["lean_outcomes"] = lean_outcomes()

    # ---- per rule: how often each arm detects through it
    def rule_table(recs, label):
        viable = [r for r in recs if r["class"] != "unviable"]
        rows = []
        for x in RULES:
            rid = x["id"]
            rs = [r for r in viable if rid in r["rules"]]
            false_of = [r for r in rs if any(r["rules"][rid][a]["detected"] for a in ARMS)]
            rows.append([rid, KIND_NAME[x["kind"]].split(" (")[0], len(rs), len(false_of)]
                        + [sum(1 for r in false_of if r["rules"][rid][a]["detected"]) for a in ARMS]
                        + [sum(1 for r in rs if r["rules"][rid]["c"].get("status") == "timeout"),
                           sum(1 for r in rs if r["rules"][rid]["d"]["outcome"] == "proof lost, not shown false"),
                           sum(1 for r in rs if r["rules"][rid]["d"]["outcome"] == "still proved")])
        summary.setdefault("by_rule", {})[label] = rows
        return md_table(["Rule", "Kind", "Viable mutants of its crate", "Rule shown false by some arm", "a", "b plain", "b edge", "c", "d",
                         "c timeout", "d proof lost, not shown false", "d still proved"], rows)
    T["rule_tool"] = rule_table([r for r in records if r["set"] == "cargo-mutants"], "cargo-mutants")
    T["rule_hand"] = rule_table([r for r in records if r["set"] == "hand-written"], "hand-written")

    # ---- per mutant
    def mutant_table(recs):
        rows = []
        for r in recs:
            if r["class"] == "unviable":
                rows.append([r["id"], r["fn"], r["description"], "UNVIABLE (does not compile)"] + ["-"] * 9)
                continue
            db = r["detected_by"]
            own = sorted(x for x, o in r["rules"].items() if o["d"]["outcome"].startswith("shown false"))
            conf = sorted(x for x, o in r["rules"].items() if o["d"]["outcome"] == "proof lost, confirmed false")
            s = r["secs"]
            rows.append([r["id"], r["fn"], r["description"].replace("|", "\\|"), "differs" if r["oracle"]["differs"] else "no difference found",
                         short(db["a"]), short(r["literal_scenarios_failing"]), short(db["b_plain"]), short(db["b_edge"]),
                         short(db["c"]) + (f"; TIMEOUT: {short(r['c_timeouts'])}" if r["c_timeouts"] else ""),
                         short(own), short(conf),
                         ("NO MODEL: the generated Lean does not build, so no rule gets a verdict" if r["d_no_verdict"] else
                          short(r["d_proof_lost_not_shown_false"]) + (" [the pipeline crashed evaluating the model; proofs had been checked]" if r["d_pipeline"]["steps_reached"][-1:] != ["8"] else "")),
                         f"{s['a']:.0f} / {s['b_plain']:.1f} / {s['b_edge']:.1f} / {s['c']:.0f} / {s['d'] or 0:.0f}"])
        return md_table(["Mutant", "Function", "Change", "Oracle", "a. rows: rules with a failing row", "literal scenarios failing (not rules)",
                         "b. plain: rules falsified", "b. edge: rules falsified", "c. Kani: rules failed", "d: shown false by the pipeline's search",
                         "d: proof lost, confirmed false", "d: proof lost, NOT shown false", "seconds a / b plain / b edge / c / d"], rows)
    T["mutants_tool"] = mutant_table([r for r in records if r["set"] == "cargo-mutants"])
    T["mutants_hand"] = mutant_table([r for r in records if r["set"] == "hand-written"])

    # ---- unique catches
    def unique(recs, b_arm):
        arms = ["a", b_arm, "c", "d"]
        out = defaultdict(list)
        for r in recs:
            if r["class"] == "unviable":
                continue
            hit = [a for a in arms if r["detected_by"][a]]
            if len(hit) == 1:
                out[hit[0]].append(r["id"])
        return {a: out.get(a, []) for a in arms}
    summary["unique"] = {s: {"with_b_plain": unique([r for r in records if r["set"] == s], "b_plain"),
                             "with_b_edge": unique([r for r in records if r["set"] == s], "b_edge")}
                         for s in ("cargo-mutants", "hand-written")}
    # who FOUND a falsifying input (d counts only when the pipeline's own search found it), per mutant and per (mutant, rule)
    def found(o, arm):
        return o["d"]["outcome"].startswith("shown false") if arm == "d_own" else o[arm]["detected"]

    def finders(recs, b_arm):
        arms = ["a", b_arm, "c", "d_own"]
        mut, pair = defaultdict(list), defaultdict(list)
        for r in recs:
            if r["class"] == "unviable":
                continue
            hit = [a for a in arms if any(found(o, a) for o in r["rules"].values())]
            if len(hit) == 1:
                mut[hit[0]].append(r["id"])
            for rid, o in r["rules"].items():
                h = [a for a in arms if found(o, a)]
                if len(h) == 1:
                    pair[h[0]].append(f"{r['id']}:{rid}")
        return {"mutants": {a: mut.get(a, []) for a in arms}, "pairs": {a: pair.get(a, []) for a in arms}}
    summary["sole_finder"] = {s: {"with_b_plain": finders([r for r in records if r["set"] == s], "b_plain"),
                                  "with_b_edge": finders([r for r in records if r["set"] == s], "b_edge")}
                              for s in ("cargo-mutants", "hand-written")}
    # pairs each arm misses although another arm shows the rule false
    def pair_misses(recs):
        out = {a: [] for a in ("a", "b_plain", "b_edge", "c", "d_own")}
        for r in recs:
            if r["class"] == "unviable":
                continue
            for rid, o in r["rules"].items():
                if any(o[a]["detected"] for a in ARMS):
                    for a in out:
                        if not found(o, a):
                            out[a].append(f"{r['id']}:{rid}")
        return out
    summary["pair_misses"] = {s: pair_misses([r for r in records if r["set"] == s]) for s in ("cargo-mutants", "hand-written")}
    # d by its own search only (without help from another arm's input)
    def missed_by(recs, arm):
        return [r["id"] for r in recs if r["class"] != "unviable" and not r["detected_by"][arm] and any(r["detected_by"][a] for a in ARMS)]
    summary["missed"] = {s: {a: missed_by([r for r in records if r["set"] == s], a) for a in ARMS} for s in ("cargo-mutants", "hand-written")}
    summary["no_arm"] = {s: [{"id": r["id"], "fn": r["fn"], "description": r["description"], "class": r["class"], "oracle_witness": r["oracle"]["witness"],
                              "literal_scenarios_failing": r["literal_scenarios_failing"], "d_proof_lost_not_shown_false": r["d_proof_lost_not_shown_false"],
                              "c_timeouts": r["c_timeouts"], "d_still_proved": len(r["d_still_proved"]), "rules": len(r["rules"])}
                             for r in records if r["set"] == s and r["class"].startswith("no arm")] for s in ("cargo-mutants", "hand-written")}
    summary["disagreements"] = [{"id": r["id"], "what": r["disagreements"]} for r in records if r.get("disagreements")]
    summary["unviable"] = [{"id": r["id"], "description": r["description"]} for r in records if r["class"] == "unviable"]

    # ---- time per arm
    def med(xs):
        xs = sorted(x for x in xs if x is not None)
        return xs[len(xs) // 2] if xs else None
    times = {}
    for crate in ("wallet", "ledger"):
        rs = [r for r in records if r["class"] != "unviable" and r["crate"] == crate]
        times[crate] = {a: {"median": med([r["secs"][a] for r in rs]), "max": max([r["secs"][a] or 0 for r in rs], default=None),
                            "total": round(sum(r["secs"][a] or 0 for r in rs), 1)} for a in ARMS}
        times[crate]["n"] = len(rs)
    summary["times"] = times
    T["times"] = md_table(["Crate (viable mutants)", "Arm", "Median seconds per mutant", "Largest", "All mutants"],
                          [[f"{c} ({times[c]['n']})", ARM_NAME[a], times[c][a]["median"], times[c][a]["max"], times[c][a]["total"]] for c in ("wallet", "ledger") for a in ARMS])
    summary["baseline_secs"] = {"a": base["a"]["secs"], "a_build": base["a"]["build_secs"], "b_plain": base["b"]["plain"]["secs"], "b_edge": base["b"]["edge"]["secs"],
                                "b_build": base["b"]["build_secs"], "c": base["c"]["secs"], "c_build": base["c"]["build_secs"], "d": base["d"]["secs"],
                                "c_rules": {k: v["secs"] for k, v in base["c"]["rules"].items()},
                                "b_plain_ms": {k: v["elapsed_ms"] for k, v in base["b"]["plain"]["rules"].items()},
                                "b_edge_ms": {k: v["elapsed_ms"] for k, v in base["b"]["edge"]["rules"].items()}}

    (RESULTS / "results.json").write_text(json.dumps({"slice_commit": (COMPARE / "SLICE_COMMIT").read_text().strip(),
                                                        "rules": RULES, "mutants": records}, indent=1, ensure_ascii=False) + "\n")
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n")
    (RESULTS / "tables.md").write_text("\n\n".join(f"<!-- table:{k} -->\n{v}" for k, v in T.items()) + "\n")
    print(json.dumps(summary["counts"], indent=1))
    print("errors:", errors, "| disagreements:", len(summary["disagreements"]), "| unviable:", len(summary["unviable"]))


if __name__ == "__main__":
    main()
