#!/usr/bin/env python3
"""EXPLORATORY, written after the measured run (not part of the registered comparison): do other Kani
bounds catch the mutants that arm c missed at the registered bounds? One harness per case, run alone.

    python3 harness/kani_probe_mutants.py        writes results/kani_bounds_probe.mutants.json
"""
import json, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mutants as M
from common import COMPARE, SLICE, SNAPSHOT, WORK, sh
cases = [("hand-r1", "batch_stops_at_invalid", dict(ACCOUNTS=6, BATCH=4)),
         ("hand-r5", "batch_conserves", dict(SUM_ACCOUNTS=2, SUM_BATCH=3)),
         ("cm-l22", "batch_then_total_overflow", dict(SUM_ACCOUNTS=3, SUM_BATCH=1)),
         ("hand-r2", "batch_then_total", dict(SUM_ACCOUNTS=4, SUM_BATCH=1)),
         ("hand-lt2", "batch_then_total_overflow", dict(SUM_ACCOUNTS=3, SUM_BATCH=1))]
out = []
muts = {m["id"]: m for m in M.load()}
for mid, rule, consts in cases:
    work = WORK / "p0"
    rc, o, _ = sh(f"'{COMPARE}/harness/workcopy.sh' '{SNAPSHOT}' '{work}' '{SLICE}'", COMPARE, 600); assert rc == 0, o
    M.apply(muts[mid], work)
    f = work / "compare/arms/kani/src/lib.rs"; s = f.read_text()
    for k, v in consts.items():
        s = re.sub(rf"^const {k}: usize = \d+;", f"const {k}: usize = {v};", s, flags=re.M)
    s = s.replace("kani::unwind(6)", "kani::unwind(10)")
    f.write_text(s)
    sh("cargo kani --only-codegen", work / "compare/arms/kani", 600)
    rc, o, secs = sh(f"cargo kani --harness {rule} --exact --output-format terse -Z unstable-options --harness-timeout 600s", work / "compare/arms/kani", 700)
    st = "timeout" if rc is None or "timed out" in o else "verified" if "VERIFICATION:- SUCCESSFUL" in o else "failed"
    out.append({"mutant": mid, "rule": rule, "bounds": consts, "status": st, "secs": secs, "failed_checks": sorted(set(re.findall(r"^Failed Checks: (.*)$", o, re.M)))})
    print(out[-1], flush=True)
json.dump(out, open(COMPARE / 'results' / 'kani_bounds_probe.mutants.json', 'w'), indent=1)
sh(f"rm -rf '{WORK / 'p0'}'", COMPARE)
