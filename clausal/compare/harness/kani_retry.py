#!/usr/bin/env python3
"""Re-run, with a longer limit, every Kani harness that timed out (or errored) in the main run.

    python3 harness/kani_retry.py [--jobs 4] [--timeout 900] [--only id,id]

The main run gives each harness 180 s while eight other pipeline runs (and other agents) share the
machine, so a timeout there can be load, not difficulty. The first attempt is kept in the raw file
under `first_attempt`; the retried result replaces it and is marked `retried`.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mutants as M  # noqa: E402
from common import COMPARE, RESULTS, SLICE, SNAPSHOT, WORK, sh  # noqa: E402

RAW = RESULTS / "raw"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = set(filter(None, a.only.split(",")))
    todo = []
    for p in sorted(RAW.glob("*.json")):
        r = json.loads(p.read_text())
        rules = [k for k, v in (r.get("c") or {}).get("rules", {}).items() if v["status"] in ("timeout", "error") and not v.get("retried")]
        if rules and (not only or r["id"] in only):
            todo.append((p, rules))
    print(f"{len(todo)} mutants, {sum(len(x[1]) for x in todo)} harnesses to retry", flush=True)
    mutants = {m["id"]: m for m in M.load()}

    def worker(i):
        work = WORK / f"k{i}"
        for p, rules in todo[i::a.jobs]:
            r = json.loads(p.read_text())
            rc, out, _ = sh(f"'{COMPARE}/harness/workcopy.sh' '{SNAPSHOT}' '{work}' '{SLICE}'", COMPARE, 600)
            assert rc == 0, out
            if r["id"] != "baseline":
                M.apply(mutants[r["id"]], work)
            d = work / "compare" / "arms" / "kani"
            sh("cargo kani --only-codegen 2>&1 | tail -3", d, 900)
            for rule in rules:
                rc, out, secs = sh(f"cargo kani --harness {rule} --exact --output-format terse -Z unstable-options --harness-timeout {a.timeout}s", d, a.timeout + 120)
                failed = re.findall(r"^Failed Checks: (.*)$", out, re.M)
                vt = re.search(r"Verification Time: ([0-9.]+)s", out)
                status = ("timeout" if rc is None or "CBMC timed out" in out else "verified" if "VERIFICATION:- SUCCESSFUL" in out
                          else "failed" if "VERIFICATION:- FAILED" in out and failed else "error")
                first = r["c"]["rules"][rule]
                r["c"]["rules"][rule] = {"status": status, "secs": secs, "verification_secs": float(vt.group(1)) if vt else None,
                                         "failed_checks": sorted(set(failed)), "tail": "" if status in ("verified", "failed") else out[-600:],
                                         "retried": True, "retry_timeout": a.timeout, "first_attempt": {k: first[k] for k in ("status", "secs")}}
                print(f"  {r['id']} {rule}: {first['status']} -> {status} ({secs} s)", flush=True)
            p.write_text(json.dumps(r, indent=1, ensure_ascii=False) + "\n")

    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(worker, range(a.jobs)))


if __name__ == "__main__":
    main()
