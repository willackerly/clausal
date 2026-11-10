#!/usr/bin/env python3
"""Regression check for the Rule / adequacy-note change: are the verdicts and the mutation results the same as
before it?

    python3 review/rule-adequacy/compare_with_previous.py [commit]     (default: 5e561a8, the last commit before the change)

Compares, against the files of that commit (read with `git show`, nothing is checked out):
  out/graph.json           every verdict that existed before: code, expected, as_expected, flags, outcome, rests_on,
                           counterexample, detail (line numbers inside messages masked), chain (as a set), unreviewed;
                           and the text of every scenario statement and derived statement
  mutation/results.json    every recorded field of every mutant, and every control that existed before
Exit status 0 iff nothing differs. New things (SUITE-* verdicts, new controls, new nodes) are counted, not compared.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

SLICE = Path(__file__).resolve().parent.parent.parent
COMMIT = sys.argv[1] if len(sys.argv) > 1 else "5e561a8"


def before(rel):
    return json.loads(subprocess.run(["git", "show", f"{COMMIT}:slice/{rel}"], cwd=SLICE, capture_output=True, text=True, check=True).stdout)


def verdicts(g):
    d = {}
    for x in g["verdicts"]:
        if x["code"].startswith("SUITE-"):
            continue
        d[x["node"]] = (x["code"], x.get("expected"), x.get("as_expected"), tuple(x["flags"]), x["outcome"], tuple(x["rests_on"]),
                        json.dumps(x.get("counterexample"), sort_keys=True), re.sub(r"feature:\d+", "feature:N", x.get("detail") or ""),
                        tuple(sorted(x["chain"])), tuple(sorted(x.get("unreviewed", []))))
    return d


bad = 0
old, new = before("out/graph.json"), json.loads((SLICE / "out/graph.json").read_text())
a, b = verdicts(old), verdicts(new)
diff = [k for k in a if a[k] != b.get(k)]
bad += len(diff)
print(f"verdicts before: {len(a)}; identical now: {len(a) - len(diff)}; different: {diff}")
print(f"new verdicts (suite adequacy note, informational): {sum(1 for x in new['verdicts'] if x['code'].startswith('SUITE-'))}")
on, nn = {n["id"]: n for n in old["nodes"]}, {n["id"]: n for n in new["nodes"]}
gone = [i for i in on if i not in nn]
changed = [i for i in on if i in nn and on[i]["interface"]["text"] != nn[i]["interface"]["text"]]
renumbered = [i for i in changed if i.startswith("stmt:Coverage.")]      # numbered by scenario order; same disjuncts, other order
changed = [i for i in changed if i not in renumbered]
bad += len(gone) + len(changed)
print(f"nodes before: {len(on)}; now: {len(nn)}; gone: {gone}; interface text changed: {changed}; "
      f"coverage statements renumbered by the regrouping (not counted as a difference): {renumbered}")

mo, mn = before("mutation/results.json"), json.loads((SLICE / "mutation/results.json").read_text())
om, nm = {m["id"]: m for m in mo["mutants"]}, {m["id"]: m for m in mn["mutants"]}
keys = ["fn", "description", "valid", "unit_tests", "rows_on_rust", "proof_broke", "search_found", "refutation_changed",
        "verdicts_changed", "exit", "killed_by_scenarios"]
mdiff = []
for i in om:
    for k in keys:
        x, y = om[i].get(k), nm.get(i, {}).get(k)
        if isinstance(x, list):
            x, y = sorted(x), sorted(y or [])
        if x != y:
            mdiff.append((i, k))
    if len(om[i]["rows_changed"]) != len(nm.get(i, {}).get("rows_changed", [])):      # row ids are file:line, and lines moved
        mdiff.append((i, "number of rows changed"))
bad += len(mdiff)
print(f"mutants before: {len(om)}; now: {len(nm)}; field differences: {mdiff}")
oc, nc = {c["id"]: c for c in mo["controls"]}, {c["id"]: c for c in mn["controls"]}
cdiff = [i for i in oc if (oc[i]["exit"], oc[i]["as_expected"]) != (nc.get(i, {}).get("exit"), nc.get(i, {}).get("as_expected"))]
bad += len(cdiff)
print(f"controls before: {len(oc)}; behaving as before: {len(oc) - len(cdiff)}; different: {cdiff}; "
      f"new controls: {[(i, 'as expected' if nc[i]['as_expected'] else 'NOT AS EXPECTED') for i in nc if i not in oc]}")
print(f"baseline verdicts of the mutation run identical: {mo['baseline']['verdicts'] == mn['baseline']['verdicts']}")
bad += mo["baseline"]["verdicts"] != mn["baseline"]["verdicts"]
print("RESULT: " + ("nothing that existed before has changed" if not bad else f"{bad} DIFFERENCES"))
sys.exit(1 if bad else 0)
