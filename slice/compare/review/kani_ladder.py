#!/usr/bin/env python3
"""REVIEW, exploratory (not part of the registered comparison): does ONE fixed two-shape ladder of Kani
bounds, the same for every mutant, catch all 10 (mutant, rule) pairs that arm c missed at the registered
bounds, and what does verifying the UNMUTATED code cost at those shapes?

TRADES.md section 4 probed 5 of the 10 pairs, each at a shape picked for that mutant. Here every
missed pair is run at every applicable shape of one ladder:
  A  accounts-heavy   SUM_ACCOUNTS=4, SUM_BATCH=1, TWO_BATCH=1   (rules that compare a total)
  B  transfers-heavy  SUM_ACCOUNTS=2, SUM_BATCH=3, TWO_BATCH=3   (rules that compare a total)
  C  other rules      ACCOUNTS=6, BATCH=4
unwind raised to 10 throughout. The shapes were chosen by the reviewer KNOWING the missed mutants (4
accounts because hand-r2 sums only three; 3 transfers because hand-r5 acts in the third iteration), so this
is not a blind ladder either.

    python3 review/kani_ladder.py [--jobs 3]     -> review/kani_ladder.json
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "harness"))
import mutants as M  # noqa: E402  (review copy: paths point at review/)
from common import COMPARE, SLICE, SNAPSHOT, WORK, sh  # noqa: E402

SHAPES = {"A": dict(SUM_ACCOUNTS=4, SUM_BATCH=1, TWO_BATCH=1), "B": dict(SUM_ACCOUNTS=2, SUM_BATCH=3, TWO_BATCH=3),
          "C": dict(ACCOUNTS=6, BATCH=4)}
TOTAL_RULES = {"batch_conserves", "whole_conserves", "batch_then_total", "batch_then_total_overflow", "two_batches_conserve"}
MISSED = {"cm-l22": ["batch_then_total_overflow"], "cm-l23": ["batch_then_total_overflow"],
          "hand-lt2": ["batch_then_total_overflow"], "hand-r1": ["batch_stops_at_invalid"],
          "hand-r2": ["batch_then_total", "batch_then_total_overflow"],
          "hand-r5": ["batch_conserves", "whole_conserves", "batch_then_total", "two_batches_conserve"]}
BASE_RULES = sorted({r for rs in MISSED.values() for r in rs})


def shapes_for(rule):
    return ["A", "B"] if rule in TOTAL_RULES else ["C"]


def run_target(i, target, rules, timeout):
    work = WORK / f"kl{i}"
    rc, o, _ = sh(f"'{COMPARE}/harness/workcopy.sh' '{SNAPSHOT}' '{work}' '{SLICE}'", COMPARE, 600)
    assert rc == 0, o
    if target != "baseline":
        M.apply(next(m for m in M.load() if m["id"] == target), work)
    d = work / "compare" / "arms" / "kani"
    orig = (d / "src" / "lib.rs").read_text()
    out = []
    for shape in ("A", "B", "C"):
        todo = [r for r in rules if shape in shapes_for(r)]
        if not todo:
            continue
        s = orig
        for k, v in SHAPES[shape].items():
            s, n = re.subn(rf"^const {k}: usize = \d+;", f"const {k}: usize = {v};", s, flags=re.M)
            assert n == 1, k
        s = s.replace("kani::unwind(6)", "kani::unwind(10)")
        (d / "src" / "lib.rs").write_text(s)
        sh("cargo kani --only-codegen 2>&1 | tail -3", d, 900)
        for rule in todo:
            rc, o, secs = sh(f"cargo kani --harness {rule} --exact --output-format terse -Z unstable-options --harness-timeout {timeout}s", d, timeout + 120)
            st = ("timeout" if rc is None or "timed out" in o else "verified" if "VERIFICATION:- SUCCESSFUL" in o
                  else "failed" if "VERIFICATION:- FAILED" in o else "error")
            rec = {"target": target, "rule": rule, "shape": shape, "bounds": SHAPES[shape], "status": st, "secs": secs,
                   "failed_checks": sorted(set(re.findall(r"^Failed Checks: (.*)$", o, re.M))), "tail": "" if st in ("verified", "failed") else o[-400:]}
            print(json.dumps(rec), flush=True)
            out.append(rec)
    sh(f"rm -rf '{work}'", COMPARE)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=300)
    a = ap.parse_args()
    targets = [("baseline", BASE_RULES)] + list(MISSED.items())
    res = []
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        for r in ex.map(lambda it: run_target(it[0], it[1][0], it[1][1], a.timeout), enumerate(targets)):
            res.extend(r)
    (HERE / "kani_ladder.json").write_text(json.dumps({"shapes": SHAPES, "timeout_s": a.timeout, "results": res}, indent=1) + "\n")


if __name__ == "__main__":
    main()
