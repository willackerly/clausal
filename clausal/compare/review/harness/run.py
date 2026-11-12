#!/usr/bin/env python3
"""Run every arm on every mutant (and on the unmutated tree), in scratch copies of the frozen snapshot.

    python3 harness/run.py [--jobs 8] [--only id,id] [--arms a,b,c,d] [--redo]

One JSON file per mutant in results/raw/<id>.json (and `baseline.json` for the unmutated tree);
a mutant that already has one is skipped unless --redo. harness/analyse.py turns them into
results/results.json and the tables of TRADES.md.

Per mutant, in a fresh copy work/w<N> of work/snapshot:
  viable   `cargo build` of the mutated crate (the pinned nightly). A mutant that does not build is "unviable".
  oracle   compare/arms/diff: does the mutant behave differently from the original on any input tried?
           NOT an arm; used to tell equivalent mutants from unconstrained behaviour.
  arm a    cucumber-rs: the feature files' Examples rows (and literal scenarios) on the compiled Rust.
  arm b    compare/arms/proptests: 10,000 cases per rule, two generator profiles (plain, edge).
  arm c    compare/arms/kani: one harness per rule, each run on its own with a timeout.
  arm d    ./run.sh --no-unit: the whole Lean pipeline (translation, proofs, search on the model, audit, report).
Only the rules of the mutated crate are run in arms b and c (a wallet mutant cannot change a ledger rule).
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mutants as M  # noqa: E402
from common import COMPARE, RESULTS, RULES, SLICE, SNAPSHOT, WORK, feature_index, rows_by_scenario, sh  # noqa: E402

RAW = RESULTS / "raw"
T_BDD, T_PROP, T_KANI, T_LEAN = 300, 120, 180, 1800     # seconds: cucumber run, one proptest property, one Kani harness, the pipeline
SEED, CASES = 20261110, 10000


def fresh(work: Path):
    rc, out, _ = sh(f"'{COMPARE}/harness/workcopy.sh' '{SNAPSHOT}' '{work}' '{SLICE}'", COMPARE, 600)
    if rc:
        raise RuntimeError(out)
    shutil.rmtree(work / "out", ignore_errors=True)
    (work / "out").mkdir()
    shutil.rmtree(work / "build" / "replay", ignore_errors=True)


def arm_a(work: Path, index):
    """Examples rows on the compiled Rust. If the whole run hangs, each scenario is run on its own to find which."""
    rc, out, build_secs = sh("cargo test --quiet --test bdd --no-run 2>&1 | tail -5", work / "wallet-bdd", 900)
    rc, out, secs = sh("cargo test --quiet --test bdd", work / "wallet-bdd", T_BDD)
    res = {"build_secs": build_secs, "secs": secs, "hang": rc is None, "rows": rows_by_scenario(work / "out" / "cucumber.json", index)}
    if rc is None:
        res["rows"], res["hung_scenarios"] = {}, []
        for name, spans in index.items():
            for (_, _, sid, tags, kind, title) in spans:
                (work / "out" / "cucumber.json").unlink(missing_ok=True)
                rc2, _, s2 = sh(f"cargo test --quiet --test bdd -- --tags '@id:{sid}'", work / "wallet-bdd", 60)
                if rc2 is None:
                    res["hung_scenarios"].append(sid)
                    res["rows"][sid] = {"hang": {"status": "fail", "message": "the scenario did not finish within 60 s"}}
                else:
                    res["rows"].update(rows_by_scenario(work / "out" / "cucumber.json", index))
    return res


def arm_b(work: Path, crate: str):
    d = work / "compare" / "arms" / "proptests"
    rc, out, build_secs = sh("cargo build --quiet 2>&1 | tail -5", d, 900)
    res = {"build_secs": build_secs, "build_ok": rc == 0}
    for profile in ("plain", "edge"):
        which = "" if crate == "all" else f"--crate {crate}"
        rc, out, secs = sh(f"./target/debug/k2-proptests --profile {profile} --cases {CASES} --seed {SEED} {which} --timeout-secs {T_PROP}", d, T_PROP * 25)
        rules = {}
        for line in out.splitlines():
            if line.startswith("{"):
                r = json.loads(line)
                rules[r["rule"]] = r
        res[profile] = {"secs": secs, "rules": rules}
    return res


def arm_c(work: Path, crate: str):
    d = work / "compare" / "arms" / "kani"
    rc, out, build_secs = sh("cargo kani --only-codegen 2>&1 | tail -3", d, 900)
    res = {"build_secs": build_secs, "build_ok": rc == 0, "rules": {}}
    t0 = time.time()
    for r in RULES:
        if crate != "all" and r["crate"] != crate:
            continue
        rc, out, secs = sh(f"cargo kani --harness {r['id']} --exact --output-format terse -Z unstable-options --harness-timeout {T_KANI}s",
                           d, T_KANI + 120)
        failed = re.findall(r"^Failed Checks: (.*)$", out, re.M)
        vt = re.search(r"Verification Time: ([0-9.]+)s", out)
        if rc is None or "CBMC timed out" in out:
            status = "timeout"
        elif "VERIFICATION:- SUCCESSFUL" in out:
            status = "verified"
        elif "VERIFICATION:- FAILED" in out and failed:
            status = "failed"
        else:
            status = "error"
        res["rules"][r["id"]] = {"status": status, "secs": secs, "verification_secs": float(vt.group(1)) if vt else None,
                                 "failed_checks": sorted(set(failed)), "tail": "" if status in ("verified", "failed") else out[-600:]}
    res["secs"] = round(time.time() - t0, 2)
    return res


def arm_d(work: Path, keep: Path):
    rc, out, secs = sh("./run.sh --no-unit", work, T_LEAN)
    res = {"exit": rc, "secs": secs, "timeout": rc is None, "tail": out[-1500:],
           "steps_reached": re.findall(r"^== (\d)/8", out, re.M)}
    o = work / "out"
    keep.mkdir(parents=True, exist_ok=True)
    (keep / "run.log").write_text(out)
    for f in ("proofs.json", "search.json", "cucumber.json", "report.md", "proofs.log", "search.log", "build.log"):
        if (o / f).exists():
            shutil.copy(o / f, keep / f)
    g = json.loads((o / "graph.json").read_text()) if (o / "graph.json").exists() else {"verdicts": []}
    res["verdicts"] = {v["node"].split("Spec.", 1)[1]: v["code"] for v in g["verdicts"] if v["node"].startswith("scenario:")}
    res["proofs"] = json.loads((o / "proofs.json").read_text()) if (o / "proofs.json").exists() else None
    res["translated"] = "wrote lean/Generated/Wallet.lean" in out
    if (o / "search.json").exists():
        s = json.loads((o / "search.json").read_text())
        res["search"] = {k.split("Spec.", 1)[1]: {"bad": v.get("bad"), "tried": v.get("tried"),
                                                  "rows": [{"line": r.get("line"), "check": r.get("check")} for r in v.get("rows", [])]}
                         for k, v in s.items() if isinstance(v, dict) and "Spec." in k}
    else:
        res["search"] = None
    return res


def oracle(work: Path, crate: str):
    lib = (work / crate / "src" / "lib.rs").read_text() if crate != "all" else ""
    extra = ",".join(sorted({x.replace("_", "") for x in re.findall(r"\b\d[\d_]*\b", lib)}, key=int)[:40])
    d = work / "compare" / "arms" / "diff"
    rc, out, secs = sh(f"cargo run --quiet -- --extra '{extra}' --timeout-secs 120", d, 1200)
    fns = [json.loads(l) for l in out.splitlines() if l.startswith("{")]
    return {"secs": secs, "ok": rc == 0 and len(fns) == 8, "differs": any(f["differs"] for f in fns),
            "witnesses": [f for f in fns if f["differs"]], "tried": sum(f["tried"] for f in fns), "tail": "" if rc == 0 else out[-400:]}


def run_one(mutant, work: Path, arms: str):
    fresh(work)
    index = feature_index(work)
    t0 = time.time()
    if mutant is None:
        res = {"id": "baseline", "crate": "all"}
        crate = "all"
    else:
        res = {k: v for k, v in mutant.items() if k not in ("old", "new", "diff")}
        crate = mutant["crate"]
        M.apply(mutant, work)
        rc, out, secs = sh("cargo build --quiet 2>&1 | tail -30", work / crate, 600)
        rc2, _, _ = sh("cargo build --quiet", work / crate, 600)
        res["viable"] = rc2 == 0
        res["build_output"] = "" if rc2 == 0 else out[-1500:]
        if not res["viable"]:
            return res
    res["oracle"] = oracle(work, crate)
    if "a" in arms:
        res["a"] = arm_a(work, index)
    if "b" in arms:
        res["b"] = arm_b(work, crate)
    if "c" in arms:
        res["c"] = arm_c(work, crate)
    if "d" in arms:
        res["d"] = arm_d(work, RAW / "lean" / res["id"])
    res["total_secs"] = round(time.time() - t0, 1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", default="")
    ap.add_argument("--arms", default="a,b,c,d")
    ap.add_argument("--redo", action="store_true")
    ap.add_argument("--prefix", default="w", help="scratch copies are work/<prefix><N>; use another prefix for a second concurrent invocation")
    a = ap.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    only = set(filter(None, a.only.split(",")))
    items = [None] + M.load()
    items = [m for m in items if (not only or (m["id"] if m else "baseline") in only)]
    items = [m for m in items if a.redo or not (RAW / f"{m['id'] if m else 'baseline'}.json").exists()]
    # ledger mutants take longest (Kani): interleave so that workers finish together
    print(f"{len(items)} runs, {a.jobs} jobs", flush=True)

    def worker(i):
        for m in items[i::a.jobs]:
            name = m["id"] if m else "baseline"
            if not a.redo and (RAW / f"{name}.json").exists():      # finished meanwhile by another invocation
                continue
            try:
                r = run_one(m, WORK / f"{a.prefix}{i}", a.arms)
            except Exception as e:  # noqa: BLE001
                import traceback
                r = {"id": name, "harness_error": repr(e), "traceback": traceback.format_exc()}
            (RAW / f"{name}.json").write_text(json.dumps(r, indent=1, ensure_ascii=False) + "\n")
            print(f"  {name}: {r.get('total_secs', '-')} s" + ("" if r.get("viable", True) else " UNVIABLE") + (f" ERROR {r['harness_error']}" if "harness_error" in r else ""), flush=True)

    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(worker, range(a.jobs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
