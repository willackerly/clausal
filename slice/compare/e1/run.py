#!/usr/bin/env python3
"""Plan node E1: the GENERATED harness set (property tests + Kani ladder) on the K2 mutant sets.

    python3 compare/e1/run.py [--only id,id] [--redo] [--jobs 6] [--kani-timeout 30] [--no-kani]

For the unmutated crates (`baseline`) and for every mutant of compare/mutants/ (52 from cargo-mutants, 45 hand-written), in
a scratch copy compare/e1/work/w0 of the two crates, wallet-bdd and the generated evidence crates:
  property test   every compiled reading about the mutated crate: 10,000 cases in scope, seed 20261111, 30 s per reading
  bounded check   the 23 rules of the K2 comparison and the two candidate rules of TRADES.md section 5 (those about the
                  mutated crate): the size ladder of slicegen/evgen.py, 30 s per harness, in two stages: the first rung of
                  every rule, then the other rungs of the rules the first rung did not show false
One JSON file per run in compare/e1/results/raw/. compare/e1/analyse.py joins them with K2's results.

The generated code is frozen when the scratch copy is made (compare/e1/results/frozen.<copy>.json has the digests); nothing
here writes outside compare/e1/. Two invocations may run side by side (--work w1 --reverse for the second).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPARE = HERE.parent
SLICE = COMPARE.parent
sys.path.insert(0, str(SLICE))
sys.path.insert(0, str(COMPARE / "harness"))
from slicegen import evgen, evidence  # noqa: E402
import mutants as M  # noqa: E402

WORK, RAW = HERE / "work", HERE / "results" / "raw"
K2_RULES = [r["id"] for r in json.loads((COMPARE / "rules.json").read_text())["rules"]]
K2_CRATE = {r["id"]: r["crate"] for r in json.loads((COMPARE / "rules.json").read_text())["rules"]}
CANDIDATES = ["Rule.ledger_rules.k2_whole_agrees_with_batch", "Rule.ledger_rules.k2_batch_agrees_with_transfers"]


def reading_of(rule: str) -> str:
    return f"Spec.{K2_CRATE[rule]}.{rule}"


def crate_of(rid: str) -> str:
    return "wallet" if rid.split(".")[1] in ("wallet", "negative_controls") else "ledger"


def setup(work: Path):
    """A scratch copy: the two crates, wallet-bdd, the evidence crates; the generated files written again from the frozen trees."""
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    ig = shutil.ignore_patterns("target", "*.lock.bak")
    for d in ("wallet", "ledger", "wallet-bdd", "evidence"):
        shutil.copytree(SLICE / d, work / d, ignore=ig)
    (work / "build").mkdir()
    shutil.copy(SLICE / "build" / "trees.json", work / "build" / "trees.json")
    trees = json.loads((work / "build" / "trees.json").read_text())
    only = set(reading_of(r) for r in K2_RULES) | set(CANDIDATES)
    evgen.write_all(work, trees, kani_only=only)
    dig = {str(p.relative_to(work)): hashlib.sha256(p.read_bytes()).hexdigest()
           for p in sorted(work.rglob("*")) if p.is_file() and "target" not in p.parts}
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / f"frozen.{work.name}.json").write_text(json.dumps({"made": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "files": dig}, indent=1))
    for c in ("wallet", "ledger"):
        shutil.copy(work / c / "src" / "lib.rs", work / f"{c}.pristine.rs")


def run_one(m, work: Path, a) -> dict:
    # nothing of the previous mutant may still be building in this copy: a `cargo kani` left behind by a harness that was
    # stopped can finish AFTER the sources are put back and leave a stale build (seen once, after a mutant whose loop does
    # not terminate; the stale result was noticed because its Kani counterexample did not reproduce on the compiled Rust)
    evidence.sh(f"pkill -f '{work}/evidence' ; sleep 1; true", work, 30)
    for c in ("wallet", "ledger"):
        shutil.copy(work / f"{c}.pristine.rs", work / c / "src" / "lib.rs")
    gen = json.loads((work / "build" / "evidence_gen.json").read_text())
    t0 = time.time()
    if m is None:
        res, crate = {"id": "baseline", "crate": "all"}, "all"
    else:
        res = {k: v for k, v in m.items() if k not in ("old", "new", "diff")}
        crate = m["crate"]
        M.apply(m, work)
        (work / crate / "src" / "lib.rs").touch()
        rc, out, _ = evidence.sh("cargo build --quiet 2>&1 | tail -20; cargo build --quiet", work / crate, 600)
        res["viable"] = rc == 0
        if rc != 0:
            res["build_output"] = out[-1500:]
            return res
    ids = [i for i in gen["readings"] if crate == "all" or crate_of(i) == crate]
    kani_ids = [i for i in ids if i in set(reading_of(r) for r in K2_RULES) | set(CANDIDATES)]
    ev = evidence.collect(a.no_kani, jobs=a.jobs, kani_timeout=a.kani_timeout, only=ids, root=work, stop_at_failure=m is not None,
                          prop_timeout=30, kani_only=kani_ids)
    res["evidence"] = ev
    res["total_secs"] = round(time.time() - t0, 1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--redo", action="store_true")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--kani-timeout", type=int, default=30)
    ap.add_argument("--no-kani", action="store_true")
    ap.add_argument("--keep", action="store_true", help="reuse the scratch copy as it is (do not regenerate)")
    ap.add_argument("--work", default="w0", help="name of the scratch copy; a second invocation uses another")
    ap.add_argument("--reverse", action="store_true", help="take the mutants from the end of the list (a second invocation meets the first)")
    a = ap.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    work = WORK / a.work
    if not (a.keep and work.exists()):
        setup(work)
    only = set(filter(None, a.only.split(",")))
    items = [None] + M.load()
    items = [m for m in items if not only or (m["id"] if m else "baseline") in only]
    items = [m for m in items if a.redo or not (RAW / f"{m['id'] if m else 'baseline'}.json").exists()]
    if a.reverse:
        items.reverse()
    print(f"{len(items)} runs", flush=True)
    for m in items:
        name = m["id"] if m else "baseline"
        if not a.redo and (RAW / f"{name}.json").exists():      # finished meanwhile by the other invocation
            continue
        try:
            r = run_one(m, work, a)
        except Exception as e:      # noqa: BLE001
            import traceback
            r = {"id": name, "harness_error": repr(e), "traceback": traceback.format_exc()}
        (RAW / f"{name}.json").write_text(json.dumps(r, indent=1, ensure_ascii=False) + "\n")
        print(f"  {name}: {r.get('total_secs', '-')} s" + ("" if r.get("viable", True) else " UNVIABLE")
              + (f" ERROR {r['harness_error']}" if "harness_error" in r else ""), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
