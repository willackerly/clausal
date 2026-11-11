#!/usr/bin/env python3
"""Compare the reviewer's rerun (mrun_results.json) with the builder's slice/mutation/results.json, field by field.
Fields compared for mutants: verdicts_changed, rows_changed (line numbers included), rules_changed, rule_shown_false,
unit_tests, exit, valid. For controls: exit, as_expected, missing_output."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
mine = json.loads((HERE / "mrun_results.json").read_text())
theirs = json.loads((HERE.parent.parent.parent / "mutation" / "results.json").read_text())
tm = {m["id"]: m for m in theirs["mutants"]}
tc = {c["id"]: c for c in theirs["controls"]}
print("baseline exit", mine["baseline"]["exit"], "| verdicts equal to builder's baseline:",
      mine["baseline"]["codes"] == theirs["baseline"]["verdicts"], "| rules equal:", mine["baseline"]["rules"] == theirs["baseline"]["rules"])
same = diff = 0
for i, r in mine["items"].items():
    t = tm.get(i) or tc.get(i)
    keys = (["verdicts_changed", "rows_changed", "rules_changed", "rule_shown_false", "unit_tests", "exit", "valid"]
            if i in tm else ["exit", "as_expected", "missing_output"])
    d = {k: (r.get(k), t.get(k)) for k in keys if r.get(k) != t.get(k)}
    if d:
        diff += 1
        print(f"{i}: DIFFERS {json.dumps(d)[:600]}")
    else:
        same += 1
        extra = f" (shown false: {bool(r['rows_changed'] or r['search_found'])})" if i in tm else f" (exit {r['exit']}, as expected {r['as_expected']})"
        print(f"{i}: identical{extra} [{r.get('secs')} s]")
print(f"{same} identical, {diff} differ, of {len(mine['items'])}")
unlinked = {i: [k for k, v in r.get("verdicts_changed", {}).items() if v == "UNLINKED"] for i, r in mine["items"].items() if i in tm}
print("mutants with a reading UNLINKED (equivalence lost):", {k: v for k, v in unlinked.items() if v})
