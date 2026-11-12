#!/usr/bin/env python3
"""The verdicts of the fourth project against kvparse/expected.json (written before the run). Run from clausal/ after ./run.sh:

    python3 kvparse/check_expected.py [path/to/graph.json]

Exit 1 if a rule's verdict code differs or is missing, a function verdict that names kvparse is not the expected one, or
another rule or scenario verdict names kvparse."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
exp = json.loads((HERE / "expected.json").read_text())
path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "out" / "graph.json"
g = json.loads(path.read_text())
bad, seen, codes = [], set(), {}
for v in g["verdicts"]:
    codes.setdefault(v["node"], []).append(v["code"])
for rid, e in exp["rules"].items():
    node = f"group:rule:{rid}"
    seen.add(node)
    got = codes.get(node)
    print(f"  {'ok ' if got == [e['code']] else 'BAD'}  {rid}: expected {e['code']}, got {got}")
    if got != [e["code"]]:
        bad.append(f"{rid}: expected {e['code']}, got {got}")
want = exp["functions"]["every_verdict_naming_kvparse"]
fns = 0
for node in sorted(codes):
    if "kvparse" not in node.lower() or node in seen:
        continue
    if node.startswith("fn:"):
        fns += 1
        print(f"  {'ok ' if codes[node] == [want] else 'BAD'}  {node}: expected {[want]}, got {codes[node]}")
        if codes[node] != [want]:
            bad.append(f"{node}: expected {[want]}, got {codes[node]}")
    else:
        bad.append(f"a verdict names kvparse and is not in expected.json: {node} {codes[node]}")
print(f"kvparse: {len(exp['rules'])} rule verdicts expected, {fns} function verdict(s) found; "
      + ("all as expected" if not bad else f"{len(bad)} NOT AS EXPECTED: " + "; ".join(bad)))
sys.exit(1 if bad else 0)
