#!/usr/bin/env python3
"""The verdicts of the third project against counter/expected.json (written before the run). Run from clausal/ after ./run.sh:

    python3 counter/check_expected.py [path/to/graph.json]

Exit 1 if a verdict code differs, a verdict is missing, the refuted rule's block does not say that its input was
reproduced on the compiled Rust, or another verdict names the counter."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from clausal import rules  # noqa: E402

exp = json.loads((HERE / "expected.json").read_text())
path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "out" / "graph.json"
g = json.loads(path.read_text())
bad, seen = [], set()
codes = {}
for v in g["verdicts"]:
    codes.setdefault(v["node"], []).append(v["code"])
blocks = {b["node"]: "\n".join(rules.render(b)) for b in rules.blocks(g)}     # render gives the block's lines
for rid, e in exp["rules"].items():
    node = f"group:rule:{rid}"
    seen.add(node)
    got = codes.get(node)
    ok = got == [e["code"]]
    text = blocks.get(node, "")
    if "block_must_say" in e and e["block_must_say"] not in " ".join(text.split()):
        ok = False
        bad.append(f"{rid}: its block does not say `{e['block_must_say']}`")
    print(f"  {'ok ' if ok else 'BAD'}  {rid}: expected {e['code']}, got {got}")
    if got != [e["code"]]:
        bad.append(f"{rid}: expected {e['code']}, got {got}")
for node, e in exp["functions"].items():
    seen.add(node)
    got = sorted(codes.get(node, []))
    print(f"  {'ok ' if got == sorted(e['codes']) else 'BAD'}  {node}: expected {sorted(e['codes'])}, got {got}")
    if got != sorted(e["codes"]):
        bad.append(f"{node}: expected {sorted(e['codes'])}, got {got}")
others = sorted(n for n in codes if "counter" in n.lower() and n not in seen)
if others:
    bad.append(f"verdicts that name the counter and are not in expected.json: {others}")
print(f"counter: {len(exp['rules'])} rule verdicts and {len(exp['functions'])} function verdict(s) expected; "
      + ("all as expected" if not bad else f"{len(bad)} NOT AS EXPECTED: " + "; ".join(bad)))
sys.exit(1 if bad else 0)
