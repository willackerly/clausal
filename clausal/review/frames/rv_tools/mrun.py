#!/usr/bin/env python3
"""Reviewer (V2/V3 review, second pass): rerun a seeded sample of the slice's Rust mutants and ALL controls with the
slice's own harness (mutation/run_mutants.py, imported unchanged from the scratch copy rv/), ONE run at a time, and
keep the full per-item results (the harness prints only a summary under --only).
Sample: random.Random(31337).sample(all 45 mutant ids, 12).
usage: mrun.py [ids...]   (default: the sample, then the 27 controls)"""
import json
import os
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RV = HERE.parent / "rv"
sys.path.insert(0, str(RV / "mutation"))
import run_mutants as R  # noqa: E402

R.BEFORE_REVIEW = False
ids_all = [m[0] for m in R.MUTANTS + R.LEDGER_MUTANTS]
SAMPLE = sorted(random.Random(31337).sample(ids_all, 12), key=ids_all.index)
want = sys.argv[1:] or SAMPLE + [c[0] for c in R.CONTROLS]
out_path = HERE / "mrun_results.json"
res = json.loads(out_path.read_text()) if out_path.exists() else {"sample_seed": 31337, "sample": SAMPLE, "items": {}}
work = RV / "build" / "mutation" / "w0"
t = time.time()
if "baseline" not in res:
    base = R.run_one(("baseline", None, work, None))
    res["baseline"] = base
    out_path.write_text(json.dumps(res, indent=1, ensure_ascii=False))
    print(f"baseline exit {base['exit']} ({round(time.time() - t)} s)", flush=True)
base = res["baseline"]
if base["exit"] != 0:
    sys.exit("baseline failed")
items = {m[0]: ("mutant", m) for m in R.MUTANTS + R.LEDGER_MUTANTS} | {c[0]: ("control", c) for c in R.CONTROLS}
for i in want:
    if i in res["items"]:
        continue
    t = time.time()
    kind, item = items[i]
    r = R.run_one((kind, item, work, base))
    r["secs"] = round(time.time() - t)
    res["items"][i] = r
    out_path.write_text(json.dumps(res, indent=1, ensure_ascii=False))
    if kind == "mutant":
        print(f"{i}: shown false {'yes' if R.shown_false(r) else 'NO'}; exit {r['exit']}; rules false {r['rule_shown_false']} ({r['secs']} s)", flush=True)
    else:
        print(f"{i}: {'as expected' if r['as_expected'] else 'NOT AS EXPECTED'} exit {r['exit']} missing {r['missing_output']} ({r['secs']} s)", flush=True)
os.system(f"rm -rf '{RV / 'build' / 'mutation'}'")
print("done", flush=True)
