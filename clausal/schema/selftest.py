#!/usr/bin/env python3
"""Does the schema + lint reject graphs it should reject? Mutates out/graph.json in memory (ten probes from the schema
review of v1, which accepted seven of them; nine more for version 2.1, frozen as P11 to P19 in trust/FREEZE.md section 4)
and expects every one to be refused. Each 2.1 probe names a fragment of the reason it must be refused FOR; and four graphs
that 2.1 must ACCEPT are checked too, so that a probe is not refused merely because attestation evidence is.

    python3 schema/selftest.py        (after ./run.sh)
"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from clausal import graphlint  # noqa: E402

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
     lambda g: first(g, "binds")["evidence"].append({"kind": "human-asserted", "by": "tool:clausal"})),
    ("a stored `stale` flag on evidence", lambda g: first(g, "formalises")["evidence"][0].update({"stale": True})),
    ("an `accepted` node with no approving review", lambda g: g["nodes"][0].update({"status": "accepted"})),
    ("evidence that refers to a run that does not exist", lambda g: first(g, "formalises")["evidence"][0].update({"run": "run:nope"})),
]


def piece(g):
    return next(n for n in g["nodes"] if "clausebook_entry" in n.get("attrs", {}))


def proved_rule(g):
    return next(v for v in g["verdicts"] if v["node"].startswith("group:rule:") and v["code"] == "PROVED-FOR-ALL")


def att(**kw):
    return lambda g: first(g, "binds")["evidence"].append(kw)


# version 2.1 (what, mutation, a fragment of the reason expected)
PROBES_21 = [
    ("P11 model-asserted evidence whose author is a person", att(kind="model-asserted", by="human:someone", act="reviewed"), "does not match '^model:'"),
    ("P12 human-asserted evidence whose author is a model (a model's attestation written as a person's)",
     att(kind="human-asserted", by="model:claude-fable-5-2", act="approved"), "does not match '^human:'"),
    ("P13 organisation-asserted evidence whose author is a tool", att(kind="organisation-asserted", by="tool:clausal", act="approved"), "does not match '^org:'"),
    ("P14 model-asserted evidence with no act", att(kind="model-asserted", by="model:m"), "'act' is a required property"),
    ("P15 an act outside the table (`refereed`)", att(kind="model-asserted", by="model:m", act="refereed"), "'refereed' is not one of"),
    ("P16 `on_behalf_of` with an unknown prefix (`robot:x`)", att(kind="model-asserted", by="model:m", act="reviewed", on_behalf_of="robot:x"),
     "'robot:x' does not match"),
    ("P17 a rule verdict whose `unreviewed` names a piece that is not a node", lambda g: proved_rule(g)["unreviewed"].append("piece:no-such-entry"),
     "unreviewed id piece:no-such-entry is not in the graph"),
    ("P18 a verdict `pass` / PROVED-FOR-ALL with a non-empty `unreviewed` list", lambda g: proved_rule(g).update({"outcome": "pass"}),
     "outcome `pass` with code PROVED-FOR-ALL"),
    ("P19 a piece node carrying an attestation of another digest",
     lambda g: piece(g)["attrs"]["attestations"].append({"act": "reviewed", "kind": "model", "by": "model:m", "on_behalf_of": None, "at": "2026-11-12T00:00:00+00:00",
                                                         "scope": "x", "digest": {"alg": "sha256-text", "value": "0" * 64}, "evidence_kind": "model-asserted"}),
     "is of another digest than the node's identity"),
]
# ... and what 2.1 must accept: the same shapes, well-formed
ACCEPTED_21 = [
    ("a model's record as model-asserted evidence, on behalf of a person", att(kind="model-asserted", by="model:m", act="reviewed", on_behalf_of="human:someone")),
    ("an organisation's record as organisation-asserted evidence", att(kind="organisation-asserted", by="org:o", act="approved")),
    ("a person's record as human-asserted evidence with its act", att(kind="human-asserted", by="human:someone", act="approved")),
    ("a piece node carrying an attestation of its own digest",
     lambda g: piece(g)["attrs"]["attestations"].append({"act": "reviewed", "kind": "model", "by": "model:m", "digest": piece(g)["interface"]["identity"]})),
]

bad = 0
for what, f in PROBES:
    g = copy.deepcopy(G)
    f(g)
    errs = graphlint.schema_errors(g) + graphlint.lint(g)
    print(f"  {'rejected' if errs else 'ACCEPTED'}  {what}" + (f"   [{errs[0][:90]}]" if errs else ""))
    bad += not errs
for what, f, why in PROBES_21:
    g = copy.deepcopy(G)
    f(g)
    errs = graphlint.schema_errors(g) + graphlint.lint(g)
    hit = [e for e in errs if why in e]
    print(f"  {'rejected' if hit else 'ACCEPTED' if not errs else 'REJECTED FOR ANOTHER REASON'}  {what}" + (f"   [{(hit or errs)[0][:110]}]" if errs else ""))
    bad += not hit
n = len(PROBES) + len(PROBES_21)
print(f"{n - bad} of {n} invalid graphs rejected ({len(PROBES)} of version 2, {len(PROBES_21)} of version 2.1)")
wrong = 0
for what, f in ACCEPTED_21:
    g = copy.deepcopy(G)
    f(g)
    errs = graphlint.schema_errors(g) + graphlint.lint(g)
    print(f"  {'accepted' if not errs else 'REJECTED'}  {what}" + (f"   [{errs[0][:110]}]" if errs else ""))
    wrong += bool(errs)
print(f"{len(ACCEPTED_21) - wrong} of {len(ACCEPTED_21)} valid 2.1 graphs accepted")
sys.exit(1 if bad or wrong else 0)
