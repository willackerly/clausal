#!/usr/bin/env python3
"""Second pass for the Lean arm: where a rule's proof is lost on a mutant and the pipeline's own search
did not show the rule false, take the falsifying input another arm found and REPLAY it as an extra
Examples row of that rule: on the Lean model (the pipeline evaluates every row on the model) and on the
compiled Rust (cucumber). Only then is "proof lost" upgraded to "proof lost, confirmed false".

    python3 harness/confirm.py [--jobs 6] [--only id,id] [--redo]

Sources of the input, in this order: arm b plain, arm b edge (the shrunk failing case); arm c (Kani's
concrete playback values, decoded per harness); `mutants/hand-witnesses.json` (inputs written by hand
after reading the mutant's diff, for rules that no arm falsified: {mutant id: {rule: {column: cell}}}).
Writes results/raw/confirm/<id>.json. Run harness/analyse.py first (it reads results/results.json),
and again afterwards.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mutants as M  # noqa: E402
from common import COMPARE, MUTANTS, RESULTS, RULE, SLICE, SNAPSHOT, WORK, feature_index, rows_by_scenario, scenario_spans, sh  # noqa: E402

OUT = RESULTS / "raw" / "confirm"
MAXU = 2 ** 64 - 1


def kani_values(work: Path, rule: str):
    """The concrete values of Kani's counterexample, in the order the harness draws them (little-endian integers)."""
    rc, out, _ = sh(f"cargo kani --harness {rule} --exact -Z concrete-playback --concrete-playback=print -Z unstable-options --harness-timeout 600s",
                    work / "compare" / "arms" / "kani", 900)
    m = re.search(r"let concrete_vals: Vec<Vec<u8>> = vec!\[(.*?)\];", out, re.S)
    if not m:
        return None
    vals = []
    for v in re.findall(r"vec!\[([0-9, ]*)\]", m.group(1)):
        b = bytes(int(x) for x in v.split(",") if x.strip())
        vals.append(int.from_bytes(b, "little"))
    return vals


def kani_row(rule: str, vals):
    """Decode Kani's values into a row of the rule's Examples table. Mirrors the order of kani::any() calls in arms/kani/src/lib.rs."""
    src = (COMPARE / "arms" / "kani" / "src" / "lib.rs").read_text()
    const = {k: int(v) for k, v in re.findall(r"^const (\w+): usize = (\d+);", src, re.M)}
    it = iter(vals)
    nxt = lambda: next(it)  # noqa: E731
    bal = lambda bs: "[" + ", ".join(str(b) for b in bs) + "]"  # noqa: E731
    tr = lambda t: f"{t[0]}->{t[1]}:{t[2]}"  # noqa: E731
    wallet3 = {"transfer_conserves", "transfer_short", "transfer_no_room"}
    wallet2 = {"withdraw_too_much", "deposit_overflow", "withdraw_covered", "deposit_with_room"}
    if rule in wallet3:
        a, b, amount = nxt(), nxt(), nxt()
        return {"a": str(a), "b": str(b), "amount": str(amount)}
    if rule in wallet2:
        a, amount = nxt(), nxt()
        return {"a": str(a), "amount": str(amount)}
    sums = {"batch_conserves", "whole_conserves", "batch_then_total", "batch_then_total_overflow", "two_batches_conserve"}
    n_acc = const["SUM_ACCOUNTS"] if rule in sums else const["MOVE_ACCOUNTS"] if rule == "transfer_valid_moves" else const["ACCOUNTS"]
    before = [nxt() for _ in range(n_acc)]
    n = nxt()
    bs = before[:n]

    def batch(size):
        ln = nxt()
        ts = [(nxt(), nxt(), nxt()) for _ in range(size)]
        return "[" + ", ".join(tr(t) for t in ts[:ln]) + "]"
    if rule in ("transfer_valid_moves", "transfer_invalid_rejected"):
        return {"balances": bal(bs), "t": tr((nxt(), nxt(), nxt()))}
    if rule in ("balance_of_account", "balance_no_account"):
        return {"balances": bal(bs), "i": str(nxt())}
    if rule == "total_is_sum":
        return {"balances": bal(bs), "sum": str(sum(bs))}
    if rule == "total_overflow":
        return {"balances": bal(bs)}
    if rule == "two_batches_conserve":
        return {"balances": bal(bs), "first": batch(const["TWO_BATCH"]), "second": batch(const["TWO_BATCH"])}
    b = batch(const["SUM_BATCH"] if rule in sums else const["BATCH"])
    if rule == "batch_then_total":
        return {"balances": bal(bs), "sum": str(sum(bs)), "batch": b}
    return {"balances": bal(bs), "batch": b}


def add_row(work: Path, rule: str, row: dict):
    """Append `row` to the Examples table of the rule. Returns (feature file name, line number of the new row)."""
    f = work / "features" / f"{RULE[rule]['crate']}.feature"
    lines = f.read_text().splitlines()
    a, b = next((s[0], s[1]) for s in scenario_spans("\n".join(lines)) if s[2] == rule)
    hdr = next(k for k in range(a - 1, b) if lines[k].strip().startswith("|"))
    cols = [c.strip() for c in lines[hdr].strip().strip("|").split("|")]
    assert sorted(cols) == sorted(row), f"{rule}: columns {cols} but the input has {sorted(row)}"
    last = max(k for k in range(hdr, b) if lines[k].strip().startswith("|"))
    lines.insert(last + 1, "      | " + " | ".join(row[c] for c in cols) + " |")
    f.write_text("\n".join(lines) + "\n")
    return f.name, last + 2


def confirm_one(rec, work: Path, hand):
    todo = {}
    for rule, o in rec["rules"].items():
        if o["d"]["outcome"] not in ("proof lost, not shown false", "no model", "proof lost, confirmed false"):
            continue
        src = next(((a, o[a]["row"]) for a in ("b_plain", "b_edge") if o[a].get("row")), None)
        if not src and rule in hand.get(rec["id"], {}):          # a hand-written input (mutants/hand-witnesses.json says why)
            src = ("hand", hand[rec["id"]][rule])
        if not src and o["c"]["detected"]:
            src = ("c", None)
        if src:
            todo[rule] = src
    if not todo:
        return None
    rc, out, _ = sh(f"'{COMPARE}/harness/workcopy.sh' '{SNAPSHOT}' '{work}' '{SLICE}'", COMPARE, 600)
    assert rc == 0, out
    mutant = next(m for m in M.load() if m["id"] == rec["id"])
    M.apply(mutant, work)
    res = {"id": rec["id"], "rules": {}}
    # inputs from Kani first (needs the mutated crate, not the feature file)
    for rule, (source, row) in list(todo.items()):
        if source == "c":
            vals = kani_values(work, rule)
            try:
                row = kani_row(rule, vals) if vals else None
            except StopIteration:
                row = None
            todo[rule] = (source, row)
            if row is None:
                res["rules"][rule] = {"source": "c", "row": None, "confirmed": False, "note": "Kani gave no concrete values that could be decoded"}
    placed = {}
    for rule, (source, row) in sorted(todo.items(), key=lambda kv: -next(s[0] for s in scenario_spans((work / "features" / f"{RULE[kv[0]]['crate']}.feature").read_text()) if s[2] == kv[0])):
        if row is None:
            continue
        # the feature file's generator limits usize literals to u32::MAX
        placed[rule] = (source, row) + add_row(work, rule, row)       # bottom-up, so earlier line numbers stay valid
    # every insertion shifts the rows below it: read each new row's line number from the final file
    for rule, (source, row, fname, _) in list(placed.items()):
        lines = (work / "features" / fname).read_text().splitlines()
        a, b = next((s[0], s[1]) for s in scenario_spans("\n".join(lines)) if s[2] == rule)
        last = max(k for k in range(a - 1, b) if lines[k].strip().startswith("|"))
        placed[rule] = (source, row, fname, last + 1)
    rc, out, secs = sh("./run.sh --no-unit", work, 1800)
    keep = OUT / "lean" / rec["id"]
    keep.mkdir(parents=True, exist_ok=True)
    (keep / "run.log").write_text(out)
    for f in ("search.json", "cucumber.json", "proofs.json"):
        if (work / "out" / f).exists():
            shutil.copy(work / "out" / f, keep / f)
    for f in (work / "features").glob("*.feature"):
        shutil.copy(f, keep / f.name)
    search = json.loads((work / "out" / "search.json").read_text()) if (work / "out" / "search.json").exists() else {}
    g = json.loads((work / "out" / "graph.json").read_text()) if (work / "out" / "graph.json").exists() else {"verdicts": []}
    verdicts = {v["node"].split("Spec.", 1)[1]: v["code"] for v in g["verdicts"] if v["node"].startswith("scenario:")}
    rust = rows_by_scenario(work / "out" / "cucumber.json", feature_index(work))
    for rule, (source, row, fname, line) in placed.items():
        key = f"{RULE[rule]['crate']}.{rule}"
        srow = next((r for r in (search.get(f"Spec.{key}") or {}).get("rows", []) if r.get("line") == line), None)
        check = srow.get("check") if srow else None
        rrow = (rust.get(rule) or {}).get(str(line), {})
        if check is None and not rrow:
            # the pipeline stopped before it evaluated rows (the model does not build, or evaluating it crashed):
            # replay the row on the compiled Rust alone, with a time limit
            (work / "out").mkdir(exist_ok=True)
            (work / "out" / "cucumber.json").unlink(missing_ok=True)
            rc2, _, _ = sh(f"cargo test --quiet --test bdd -- --tags '@id:{rule}'", work / "wallet-bdd", 90)
            if rc2 is None:
                rrow = {"status": "fail", "message": "the scenario did not finish within 90 s on the compiled Rust"}
            else:
                rrow = (rows_by_scenario(work / "out" / "cucumber.json", feature_index(work)).get(rule) or {}).get(str(line), {})
        on_model = check not in (None, "pass", "givenFalse")
        on_rust = rrow.get("status") == "fail" and "GIVEN-FALSE" not in rrow.get("message", "")
        res["rules"][rule] = {"source": source, "row": row, "line": line, "lean_model_check": check, "lean_model_returned": (srow or {}).get("returned"),
                              "rust_row": rrow.get("status"), "rust_message": rrow.get("message", "")[:200], "verdict_with_row": verdicts.get(key),
                              "pipeline_exit": rc, "confirmed": bool(on_model or (check is None and on_rust)),
                              "confirmed_on": "Lean model and compiled Rust" if on_model and on_rust else "Lean model" if on_model else
                                              "compiled Rust only (the pipeline gave no row result)" if (check is None and on_rust) else None}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--only", default="")
    ap.add_argument("--redo", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    recs = [r for r in json.loads((RESULTS / "results.json").read_text())["mutants"] if r.get("rules")]
    hand = json.loads((MUTANTS / "hand-witnesses.json").read_text()).get("witnesses", {}) if (MUTANTS / "hand-witnesses.json").exists() else {}
    only = set(filter(None, a.only.split(",")))
    recs = [r for r in recs if (not only or r["id"] in only) and (a.redo or not (OUT / f"{r['id']}.json").exists())]

    def worker(i):
        for r in recs[i::a.jobs]:
            try:
                res = confirm_one(r, WORK / f"c{i}", hand)
            except Exception as e:  # noqa: BLE001
                import traceback
                res = {"id": r["id"], "rules": {}, "harness_error": repr(e), "traceback": traceback.format_exc()}
            if res is not None:
                (OUT / f"{r['id']}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
                print(f"  {r['id']}: " + ", ".join(f"{k}: {'confirmed' if v['confirmed'] else 'NOT confirmed'} ({v['source']})" for k, v in res["rules"].items())
                      + (f" ERROR {res['harness_error']}" if "harness_error" in res else ""), flush=True)

    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(worker, range(a.jobs)))


if __name__ == "__main__":
    main()
