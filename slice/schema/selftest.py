#!/usr/bin/env python3
"""Does the schema + lint reject graphs it should reject? Mutates out/graph.json in memory eight ways
(the probes the schema review ran against v1, which accepted seven of them) and expects every one to be refused.

    python3 schema/selftest.py        (after ./run.sh)
"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from slicegen import graphlint  # noqa: E402

G = json.loads((HERE.parent / "out" / "graph.json").read_text())
assert not graphlint.schema_errors(G) + graphlint.lint(G), "out/graph.json itself is not valid"


def first(g, rel):
    return next(e for e in g["edges"] if e["relation"] == rel)


KC = {"kind": "kernel-checked", "by": "tool:lean-kernel", "axioms": [], "artifact": "x"}
PROBES = [
    ("a `binds` edge (English to Lean) carrying kernel-checked evidence", lambda g: first(g, "binds")["evidence"].append(dict(KC))),
    ("kernel-checked evidence with no axioms and no theorem named",
     lambda g: first(g, "refutes").__setitem__("evidence", [{"kind": "kernel-checked", "by": "tool:lean-kernel"}])),
    ("an edge whose endpoint is not a node", lambda g: first(g, "uses").__setitem__("to", "no-such-node")),
    ("a `translates` edge from a claim to a phrase",
     lambda g: first(g, "translates").update({"from": "scenario:Spec.wallet.transfer_conserves", "to": "phrase:G-balance"})),
    ("two nodes with the same id", lambda g: g["nodes"].append(copy.deepcopy(g["nodes"][0]))),
    ("a misspelt evidence field (`axoims`)", lambda g: first(g, "formalises")["evidence"][0].update({"axoims": ["sorryAx"]})),
    ("human-asserted evidence whose author is a tool",
     lambda g: first(g, "binds")["evidence"].append({"kind": "human-asserted", "by": "tool:slicegen"})),
    ("a stored `stale` flag on evidence", lambda g: first(g, "formalises")["evidence"][0].update({"stale": True})),
    ("an `accepted` node with no approving review", lambda g: g["nodes"][0].update({"status": "accepted"})),
    ("evidence that refers to a run that does not exist", lambda g: first(g, "formalises")["evidence"][0].update({"run": "run:nope"})),
]
bad = 0
for what, f in PROBES:
    g = copy.deepcopy(G)
    f(g)
    errs = graphlint.schema_errors(g) + graphlint.lint(g)
    print(f"  {'rejected' if errs else 'ACCEPTED'}  {what}" + (f"   [{errs[0][:90]}]" if errs else ""))
    bad += not errs
print(f"{len(PROBES) - bad} of {len(PROBES)} invalid graphs rejected")
sys.exit(1 if bad else 0)
