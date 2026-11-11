#!/usr/bin/env python3
"""Plan node E1: the FEED-BACK on a sample of mutants. The whole pipeline (./run.sh) in a scratch copy of slice/ with one
mutant applied: the generated harnesses find a falsifying input on the compiled Rust, it is evaluated on the Lean model,
and the verdicts change (or a MODEL MISMATCH is reported).

    python3 compare/e1/feedback.py hand-la6:full cm-l36 hand-r4 cm-l22 cm-l34       (":full" = with the Kani ladder)

One JSON file per mutant in compare/e1/results/feedback/, with the log beside it. Run one at a time.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPARE = HERE.parent
SLICE = COMPARE.parent
sys.path.insert(0, str(SLICE))
sys.path.insert(0, str(COMPARE / "harness"))
from slicegen import evidence  # noqa: E402
import mutants as M  # noqa: E402

OUT = HERE / "results" / "feedback"
PATH = 'export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"; '


def verdicts(graph: Path) -> dict:
    g = json.loads(graph.read_text()) if graph.exists() else {"verdicts": []}
    return {v["node"]: v["code"] for v in g["verdicts"] if v["node"].startswith(("scenario:", "group:rule:"))}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base = verdicts(SLICE / "out" / "graph.json")
    by_id = {m["id"]: m for m in M.load()}
    work = HERE / "work" / "fb"
    for arg in sys.argv[1:]:
        mid, _, mode = arg.partition(":")
        m = by_id[mid]
        rc, out, _ = evidence.sh(f"'{SLICE}/mutation/workcopy.sh' '{work}'", SLICE, 900)
        assert rc == 0, out
        M.apply(m, work)
        t0 = time.time()
        rc, out, secs = evidence.sh(PATH + "./run.sh --no-unit --no-adequacy" + ("" if mode == "full" else " --quick"), work, 3600)
        (OUT / f"{mid}.log").write_text(out)
        ev = evidence.load(work / "out") or {}
        after = verdicts(work / "out" / "graph.json")
        wit = [{"reading": i, "source": w["source"], "values": w["values"], "rust": w["rust"], "model": w.get("model"), "mismatch": w.get("mismatch")}
               for i, _, w in evidence.witness_list(ev)]
        res = {"id": mid, "description": m["description"], "mode": mode or "quick", "exit": rc, "secs": secs,
               "steps_reached": re.findall(r"^== (\w+)/8", out, re.M),
               "fed_back": re.findall(r"^  fed back: (\S+) is false at an input found by the generated (.+?);", out, re.M),
               "model_mismatch_lines": re.findall(r"^  MODEL MISMATCH: .*$", out, re.M),
               "verdicts_changed": {k: [base.get(k), v] for k, v in after.items() if base.get(k) != v},
               "no_verdict": not after, "witnesses": wit,
               "evidence_summary": evidence.summary_line(ev) if ev.get("readings") else ev.get("error", "the generated evidence step did not run"),
               "tail": out[-1200:]}
        (OUT / f"{mid}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
        print(f"{mid}: exit {rc}, {secs} s, fed back {len(res['fed_back'])}, verdicts changed {len(res['verdicts_changed'])}, "
              f"mismatch {len(res['model_mismatch_lines'])}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
