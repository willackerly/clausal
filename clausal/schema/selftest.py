#!/usr/bin/env python3
"""Does the schema + lint reject graphs it should reject? Mutates out/graph.json in memory (ten probes from the schema
review of v1, which accepted seven of them; nine more for version 2.1, frozen as P11 to P19 in trust/FREEZE.md section 4, and eight, P20 to P27, in trust/FREEZE-fix1.md; six for the assumption ledger, P28 to P33, in trust/FREEZE-w46.md)
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


def glossary_entry(g):
    return next(n for n in g["nodes"] if n.get("attrs", {}).get("subject_kind") == "glossary-entry")


def proved_composed(g):
    froms = {e["from"] for e in g["edges"] if e["relation"] == "composed_of"}
    return next(v for v in g["verdicts"] if v["node"] in froms and v["code"].startswith("PROVED"))


def node_of(g, i):
    return next(n for n in g["nodes"] if n["id"] == i)


def assumption(g):
    return next(n for n in g["nodes"] if n["kind"] == "assumption")


def assuming_rule(g):
    """A proved Rule verdict whose reading rests on an entry of the assumption ledger."""
    return next(v for v in g["verdicts"] if v["code"] == "PROVED-FOR-ALL" and (node_of(g, v["node"]).get("attrs", {}).get("reading") or {}).get("assumptions"))


def stored(g, n, **kw):
    """What the reviewer's repro wrote on a node: `approved`, kind person, by a model id, of the node's own digest."""
    return {"act": "approved", "kind": "person", "by": "model:selftest-fixture", "on_behalf_of": None, "at": "2026-11-12T00:00:00+00:00", "scope": "x",
            "digest": n["interface"]["identity"], "evidence_kind": "model-asserted", **kw}


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
    # fix round 1 (trust/FREEZE-fix1.md, section A): what a node stores as an attestation is what strict mode reads
    ("P20 a piece node storing an attestation of kind person by a model id", lambda g: piece(g)["attrs"]["attestations"].append(stored(g, piece(g))),
     "kind `person` is not the kind of its signer"),
    ("P21 an old-glossary phrase node storing an attestation of kind person by a model id",
     lambda g: glossary_entry(g)["attrs"].setdefault("attestations", []).append(stored(g, glossary_entry(g))), "kind `person` is not the kind of its signer"),
    ("P22 a stored attestation by a model whose evidence_kind is human-asserted",
     lambda g: piece(g)["attrs"]["attestations"].append(stored(g, piece(g), kind="model", by="model:m", evidence_kind="human-asserted")),
     "evidence_kind `human-asserted` is not that of a model"),
    ("P23 a stored attestation by `human:*`", lambda g: piece(g)["attrs"]["attestations"].append(stored(g, piece(g), by="human:*", evidence_kind="human-asserted")),
     "is not a signer id"),
    ("P24 a stored attestation with an act outside the table (`refereed`)",
     lambda g: piece(g)["attrs"]["attestations"].append(stored(g, piece(g), kind="model", by="model:m", act="refereed")), "act `refereed` is not one of"),
    ("P25 a stored attestation `approved` by a tool",
     lambda g: piece(g)["attrs"]["attestations"].append(stored(g, piece(g), kind="tool", by="tool:clausal", evidence_kind="tested")),
     "a tool can only have authored or tested"),
    ("P26 a proved Rule verdict `pass` with an EMPTY `unreviewed` list over entries no person has reviewed",
     lambda g: proved_rule(g).update({"outcome": "pass", "unreviewed": []}), "does not list"),
    ("P27 a proved scenario verdict composed of old-glossary entries, `pass` with an EMPTY `unreviewed` list",
     lambda g: proved_composed(g).update({"outcome": "pass", "unreviewed": []}), "does not list"),
    # W4, the assumption ledger (trust/FREEZE-w46.md, section 3)
    ("P28 `assumed` evidence on a `binds` edge", att(kind="assumed", by="model:m", artifact="trust/assumptions.yaml#A.x"), "'assumed' is not one of"),
    ("P29 `assumed` evidence with no artifact (the ledger id)", lambda g: first(g, "assumes")["evidence"].append({"kind": "assumed", "by": "model:m"}),
     "'artifact' is a required property"),
    ("P30 an `assumes` edge from a piece to a definition node",
     lambda g: first(g, "assumes").update({"to": next(n["id"] for n in g["nodes"] if n["kind"] == "definition")}), "may not go from"),
    ("P31 a proved Rule verdict whose reading lists an assumption and whose `rests_on` has no `assumed`",
     lambda g: assuming_rule(g)["rests_on"].remove("assumed"), "does not list `assumed`"),
    ("P32 a Rule node whose reading uses a piece that rests on an assumption and does not list the assumption",
     lambda g: node_of(g, assuming_rule(g)["node"])["attrs"]["reading"].update({"assumptions": []}), "does not list the assumption"),
    ("P33 an assumption node that stores a verdict on a usage condition",
     lambda g: assumption(g)["attrs"]["usage_conditions"][0].update({"verdict": "PROVED-FOR-ALL"}), "stores a verdict"),
]
# ... and what 2.1 must accept: the same shapes, well-formed
ACCEPTED_21 = [
    ("a model's record as model-asserted evidence, on behalf of a person", att(kind="model-asserted", by="model:m", act="reviewed", on_behalf_of="human:someone")),
    ("an organisation's record as organisation-asserted evidence", att(kind="organisation-asserted", by="org:o", act="approved")),
    ("a person's record as human-asserted evidence with its act", att(kind="human-asserted", by="human:someone", act="approved")),
    ("a piece node carrying an attestation of its own digest",
     lambda g: piece(g)["attrs"]["attestations"].append({"act": "reviewed", "kind": "model", "by": "model:m", "digest": piece(g)["interface"]["identity"]})),
    ("W4: an organisation's vouch as evidence on an `assumes` edge",
     lambda g: first(g, "assumes")["evidence"].append({"kind": "organisation-asserted", "by": "org:o", "act": "vouched"})),
    ("W4: an assumption node carrying an organisation's vouch",
     lambda g: assumption(g)["attrs"]["attestations"].append({"act": "vouched", "kind": "organisation", "by": "org:o", "evidence_kind": "organisation-asserted"})),
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
