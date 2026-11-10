#!/usr/bin/env python3
"""Tables for p2/RESULTS.md from p2/score/results/*.json (no numbers are typed by hand).

    python3 p2/score/summarize.py            prints Markdown tables; writes results/summary.json
"""
import json
from pathlib import Path

RES = Path(__file__).resolve().parent / "results"
ARMS = ["arm-fable", "arm-opus"]
SHORT = {"arm-fable": "fable", "arm-opus": "opus"}
ORDER = ["stock_of", "find_bin", "restock", "take", "fill_orders", "product_count", "dominant_product"]
KIND = {"stock_of": "accumulation, early return on overflow", "find_bin": "search, early exit",
        "restock": "in-place update of every match", "take": "in-place update, two-part condition, early stop",
        "fill_orders": "loop calling two looping functions", "product_count": "nested loop",
        "dominant_product": "non-obvious invariant (two passes)"}
SCEN_FN = {"stock_is_sum": "stock_of", "stock_too_big": "stock_of", "find_first_bin": "find_bin",
           "find_no_bin": "find_bin", "restock_adds": "restock", "restock_counts": "restock",
           "take_amount": "take", "take_stock_down": "take", "take_earliest_first": "take",
           "fill_count": "fill_orders", "fill_state": "fill_orders", "fill_at_most": "fill_orders",
           "count_products": "product_count", "count_at_most_bins": "product_count",
           "dominant_found": "dominant_product", "dominant_none": "dominant_product"}
CALLERS = {"stock_of": {"fill_orders"}, "take": {"fill_orders"}, "can_fill": {"fill_orders"}}


def load(name):
    p = RES / name
    return json.loads(p.read_text()) if p.exists() else None


def md(rows, hdr):
    out = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def main():
    S = {}
    audit = {a: load(f"audit-{SHORT[a]}.json") for a in ARMS}
    lines = {a: load(f"lines-{SHORT[a]}.json") for a in ARMS}
    att = {a: load(f"attempts-{SHORT[a]}.json") for a in ARMS}
    # 1. verdicts per scenario and per function (independent audit)
    rows = []
    for fn in ORDER:
        sids = [s for s in SCEN_FN if SCEN_FN[s] == fn]
        row = [fn]
        for a in ARMS:
            sc = audit[a]["scenarios"]
            ok = [s for s in sids if sc.get(s, {}).get("proved")]
            row.append(f"{len(ok)}/{len(sids)}" + (" done" if len(ok) == len(sids) else ""))
        rows.append(row)
    print("## Per function (independent audit)\n")
    print(md(rows, ["function", "fable", "opus"]))
    for a in ARMS:
        sc = audit[a]["scenarios"]
        S[a] = {"scenarios_proved": sum(1 for v in sc.values() if v["proved"]),
                "functions_done": sum(1 for fn in ORDER if all(sc[s]["proved"] for s in SCEN_FN if SCEN_FN[s] == fn)),
                "kernel_replay_ok": sum(1 for v in audit[a]["kernel_replay"].values() if v["exit"] == 0 and not v["tail"]),
                "kernel_replay_modules": len(audit[a]["kernel_replay"]),
                "axioms": sorted({x for v in sc.values() for x in v["axioms"]})}
    print("\n", json.dumps(S, indent=1))
    print("\n## Per scenario\n")
    srows = []
    for sid, fn in SCEN_FN.items():
        r = [sid, fn]
        for a in ARMS:
            sc = audit[a]["scenarios"][sid]
            decl_names = {d["name"] for d in lines[a]["declarations"]}
            reached = [n for n in sc["hand"] if n in decl_names]
            reached_lines = sum(d["code_lines"] for d in lines[a]["declarations"] if d["name"] in reached)
            r += ["PROVED-FOR-ALL" if sc["proved"] else "not proved", lines[a]["proof_lines"][sid],
                  f"{len(reached)} / {reached_lines}"]
        srows.append(r)
    print(md(srows, ["scenario", "function", "fable verdict", "fable proof lines", "fable lemmas reached (decls / lines)",
                     "opus verdict", "opus proof lines", "opus lemmas reached (decls / lines)"]))
    # 2. cost
    print("\n## Cost\n")
    rows = []
    for k in ["attempts_proof", "failed_proof", "failed_real", "failed_mixed", "failed_probe", "post_hoc_probe_attempts",
              "minutes_first_to_last_proof_attempt", "minutes_copy_to_last_proof_attempt", "minutes_copy_to_final_report",
              "build_seconds_proof"]:
        rows.append([k] + [att[a]["summary"].get(k) for a in ARMS])
    for k in ["hand_written_lean", "lemma_code_lines", "lemma_boilerplate_lines", "scenario_proof_lines",
              "lean_per_rust_code_line", "lean_per_rust_code_line_with_glossary", "declarations", "theorems",
              "definitions", "loop_lemmas"]:
        rows.append([k] + [lines[a]["summary"].get(k) for a in ARMS])
    for cat in ["loop lemma", "function spec", "pure helper", "Aeneas/scalar helper", "definition"]:
        rows.append([f"{cat}: decls / statement / proof lines"] + [
            "{decls} / {statement_lines} / {proof_lines}".format(**lines[a]["summary"]["by_category"].get(
                cat, {"decls": 0, "statement_lines": 0, "proof_lines": 0})) for a in ARMS])
    print(md(rows, ["measure", "fable", "opus"]))
    # 3. per function, per arm
    print("\n## Per function and kind of loop\n")
    rows = []
    for fn in ORDER:
        for a in ARMS:
            f = lines[a]["per_function"][fn]
            t = att[a]["per_function"][fn]
            rows.append([fn if a == ARMS[0] else "", KIND[fn] if a == ARMS[0] else "", SHORT[a], f["rust_code_lines"],
                         f"{f['loop_lemmas']}: {f['loop_lemma_statement_lines']} + {f['loop_lemma_proof_lines']}",
                         f["spec_lines"], f["helper_lines_exclusive"], f["helper_lines_shared"],
                         f["scenario_proof_lines"], f["own_lines"], f["own_lean_per_rust"],
                         f"{t['attempts']} / {t['failed']} ({t['failed_real']} real, {t['failed_mixed']} mixed, {t['failed_probe']} probe)",
                         t["active_min"], t["increment_min"]])
    print(md(rows, ["function", "kind of loop", "arm", "Rust lines", "loop lemmas: stmt + proof lines", "spec",
                    "helpers (own)", "helpers (shared)", "scenario proofs", "own total", "own Lean/Rust",
                    "builds / FAILED", "active min", "increment min"]))
    # 4. mutants
    mfiles = sorted((RES / "mutants").glob("*.json"))
    if mfiles:
        recs = [json.loads(f.read_text()) for f in mfiles]
        unit = load("unit/mutants.out/outcomes.json")
        unit_by = {}
        for o in unit["outcomes"]:
            if isinstance(o["scenario"], dict):
                unit_by[o["scenario"]["Mutant"]["name"]] = o["summary"]
        tot = {"mutants": len(recs), "pipeline_stopped": 0, "shown_false": 0, "translate_failed": 0}
        per_arm = {a: {"only_lose_proof": 0, "all_proofs_kept": 0,
                       "refuted_but_proof_kept": [], "kept_list": [], "only_lose_list": [],
                       "collateral_proofs_lost_total": 0, "own_proofs_lost_total": 0}
                   for a in ARMS}
        rows = []
        for r in recs:
            cl = r["class"]
            fn = (r["function"] or "").split("::")[-1]
            own = {fn} | CALLERS.get(fn, set())
            stopped = not r["detect"].get("scenarios")
            shown = bool(cl["shown_false_by"])
            if r.get("translate", {}).get("rc") not in (0, None):
                tot["translate_failed"] += 1
            if stopped:
                tot["pipeline_stopped"] += 1
            elif shown:
                tot["shown_false"] += 1
            line = [r["index"], r["name"].split(": ", 1)[1][:70], unit_by.get(r["name"], "?"),
                    "STOPPED" if stopped else (",".join(cl["shown_false_by"]) or "-")]
            for a in ARMS:
                p = cl.get(a)
                if not p:
                    line.append("-")
                    continue
                lost = p["proofs_lost"]
                own_lost = [s for s in lost if SCEN_FN[s] in own]
                col = [s for s in lost if SCEN_FN[s] not in own]
                pa = per_arm[a]
                pa["own_proofs_lost_total"] += len(own_lost)
                pa["collateral_proofs_lost_total"] += len(col)
                for s in cl["shown_false_by"]:
                    if s not in lost:
                        pa["refuted_but_proof_kept"].append((r["index"], s))
                if not shown and not stopped:
                    if lost:
                        pa["only_lose_proof"] += 1
                        pa["only_lose_list"].append(r["index"])
                    else:
                        pa["all_proofs_kept"] += 1
                        pa["kept_list"].append(r["index"])
                line.append(f"{len(lost)} ({len(own_lost)} own, {len(col)} other)")
            rows.append(line)
        # per function: how the mutants of each function came out
        byfn = {}
        cross = {}
        for r in recs:
            cl = r["class"]
            fn = (r["function"] or "").split("::")[-1]
            fn = "fill_orders (incl. can_fill)" if fn in ("fill_orders", "can_fill") else fn
            stopped = not r["detect"].get("scenarios")
            shown = bool(cl["shown_false_by"])
            b = byfn.setdefault(fn, {"mutants": 0, "shown_false": 0, "stopped": 0, "not_shown": 0,
                                     **{f"{SHORT[a]}_lost_own": 0 for a in ARMS},
                                     **{f"{SHORT[a]}_lost_other": 0 for a in ARMS}})
            b["mutants"] += 1
            b["stopped" if stopped else ("shown_false" if shown else "not_shown")] += 1
            own = {fn.split(" ")[0]} | CALLERS.get(fn.split(" ")[0], set())
            for a in ARMS:
                lost = cl.get(a, {}).get("proofs_lost", [])
                b[f"{SHORT[a]}_lost_own"] += sum(1 for s in lost if SCEN_FN[s] in own)
                b[f"{SHORT[a]}_lost_other"] += sum(1 for s in lost if SCEN_FN[s] not in own)
            u = unit_by.get(r["name"], "?")
            key = (u, "stopped" if stopped else ("shown false" if shown else "not shown"))
            cross[key] = cross.get(key, 0) + 1
        frows = []
        for fn, b in byfn.items():
            n = b["mutants"]
            frows.append([fn, n, b["shown_false"], b["stopped"], b["not_shown"]] +
                         [f"{b[f'{SHORT[a]}_lost_own'] / n:.1f} + {b[f'{SHORT[a]}_lost_other'] / n:.1f}" for a in ARMS])
        print("\n## Mutants per function\n")
        print(md(frows, ["function mutated", "mutants", "shown false by a scenario", "pipeline stopped", "not shown false",
                         "fable: proofs lost per mutant (own + other)", "opus: proofs lost per mutant (own + other)"]))
        print("\n## Unit tests (cargo-mutants) against scenarios\n")
        print(md([[k[0], k[1], v] for k, v in sorted(cross.items())], ["unit tests", "scenarios", "mutants"]))
        # how strongly each shown-false mutant was shown false
        strength = {"kernel-checked refutation (REFUTED)": 0, "counterexample on the model, replayed on Rust": 0,
                    "only an Examples row failing on Rust": 0}
        for r in recs:
            sc = r["detect"].get("scenarios", {})
            if not r["class"]["shown_false_by"] or not sc:
                continue
            codes = {v["code"] for v in sc.values()}
            if "REFUTED" in codes:
                strength["kernel-checked refutation (REFUTED)"] += 1
            elif "COUNTEREXAMPLE" in codes:
                strength["counterexample on the model, replayed on Rust"] += 1
            else:
                strength["only an Examples row failing on Rust"] += 1
        print("\n## Strength of the evidence for shown-false mutants\n")
        print(md([[k, v] for k, v in strength.items()], ["strongest evidence", "mutants"]))
        S["mutants_strength"] = strength
        S["mutants_per_function"] = byfn
        S["mutants_unit_vs_scenarios"] = {f"{k[0]} / {k[1]}": v for k, v in cross.items()}
        print("\n## Mutants\n")
        print(json.dumps(tot, indent=1))
        print(json.dumps(per_arm, indent=1))
        print(md(rows, ["#", "mutant", "unit tests", "shown false by", "fable proofs lost", "opus proofs lost"]))
        S["mutants"] = {"totals": tot, "per_arm": per_arm}
    (RES / "summary.json").write_text(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
