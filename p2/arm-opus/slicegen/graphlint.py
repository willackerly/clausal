"""Checks on a refinement graph that JSON Schema cannot express, and staleness.

    python3 -m slicegen.graphlint <graph.json>                      schema + lint
    python3 -m slicegen.graphlint <graph.json> --what-if <node-id>  what goes stale if that node's interface changed

Used by `slicegen report` on out/graph.json and by schema/maths_fit.py on the maths-side example.
The schema is schema/refinement-graph.v2.schema.json; the prose is ../docs/SCHEMA.md.

Staleness is never stored. It is computed:

  * a node END (the interface, or one implementation) is CHANGED if some evidence entry records a
    digest for it that differs from its current digest;
  * a node is SUSPECT if it is changed at its interface, or if its interface `uses` (edge with
    from_end = interface) a suspect node or a changed end: its text is the same but it no longer
    means the same thing;
  * an evidence entry is stale if one of its inputs is a changed end, or (except on the purely
    structural relations uses / composed_of / contains, which record what the text mentions) a
    suspect node;
  * an edge is stale if any of its evidence is; an implementation is stale if any of its `realises`
    evidence is, or if it `uses` (from_end = implementation) a suspect node;
  * a verdict is stale if its node is suspect, or an edge on its chain is stale, or an
    implementation of its node is stale.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

SCHEMA = Path(__file__).resolve().parent.parent / "schema" / "refinement-graph.v2.schema.json"

# relation -> allowed (from-kind, to-kind) pairs
RELATIONS = {
    "contains":    {("group", "group"), ("group", "claim"), ("group", "statement")},
    "composed_of": {("claim", "phrase")},
    "binds":       {("phrase", "definition"), ("phrase", "function")},
    "formalises":  {("statement", "claim")},
    "uses":        {(a, b) for a in ("statement", "definition", "function") for b in ("statement", "definition", "function")},
    "requires":    {("statement", "statement")},
    "translates":  {("function", "function")},
    "models":      {("function", "function")},
    "instance_of": {("example", "statement")},
    "exercises":   {("example", "function")},
    "refutes":     {("statement", "statement"), ("example", "statement")},
    "covers":      {("statement", "function")},
    "lifted_from": {("statement", "statement")},
    "generalises": {("statement", "statement")},
    "equivalent":  {("definition", "definition"), ("statement", "statement")},
}


STRUCTURAL = {"uses", "composed_of", "contains"}


def schema_errors(g: dict) -> list:
    try:
        import jsonschema
    except ImportError:
        return ["python module `jsonschema` is not installed: the graph was NOT checked against the JSON Schema"]
    v = jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text()))
    return [f"schema: {'/'.join(str(x) for x in e.absolute_path)}: {e.message[:200]}" for e in v.iter_errors(g)]


def lint(g: dict) -> list:
    errs = []
    nodes = {}
    for n in g["nodes"]:
        if n["id"] in nodes:
            errs.append(f"duplicate node id {n['id']}")
        nodes[n["id"]] = n
        impl_ids = [im["id"] for im in n["implementations"]]
        if len(impl_ids) != len(set(impl_ids)):
            errs.append(f"node {n['id']}: duplicate implementation ids")
    runs = {r["id"] for r in g["runs"]}
    if len(runs) != len(g["runs"]):
        errs.append("duplicate run ids")

    def check_ev(where, x):
        if "run" in x and x["run"] not in runs:
            errs.append(f"{where}: evidence refers to unknown run {x['run']}")
        for i in x.get("inputs", []):
            n = nodes.get(i["node"])
            if n is None:
                errs.append(f"{where}: evidence input refers to unknown node {i['node']}")
            elif i.get("end") == "implementation" and i.get("implementation") not in [im["id"] for im in n["implementations"]]:
                errs.append(f"{where}: evidence input refers to unknown implementation {i['node']}[{i.get('implementation')}]")

    for n in g["nodes"]:
        if "run" in n["origin"] and n["origin"]["run"] not in runs:
            errs.append(f"node {n['id']}: origin refers to unknown run {n['origin']['run']}")
        for im in n["implementations"]:
            for x in im["realises"]:
                check_ev(f"node {n['id']}[{im['id']}]", x)
    eids = set()
    for e in g["edges"]:
        if e["id"] in eids:
            errs.append(f"duplicate edge id {e['id']}")
        eids.add(e["id"])
        f, t = nodes.get(e["from"]), nodes.get(e["to"])
        if f is None or t is None:
            errs.append(f"edge {e['id']}: endpoint is not a node")
            continue
        if (f["kind"], t["kind"]) not in RELATIONS.get(e["relation"], set()):
            errs.append(f"edge {e['id']}: `{e['relation']}` may not go from a {f['kind']} to a {t['kind']}")
        if e.get("from_end") == "implementation" and e.get("from_implementation") not in [im["id"] for im in f["implementations"]]:
            errs.append(f"edge {e['id']}: from_implementation {e.get('from_implementation')} is not an implementation of {f['id']}")
        if len({json.dumps(x, sort_keys=True) for x in e["evidence"]}) != len(e["evidence"]):
            errs.append(f"edge {e['id']}: duplicate evidence entries")
        for x in e["evidence"]:
            check_ev(f"edge {e['id']}", x)
    for v in g["verdicts"]:
        if v["node"] not in nodes:
            errs.append(f"verdict for unknown node {v['node']}")
        for c in v["chain"]:
            if c not in eids:
                errs.append(f"verdict {v['node']}: chain edge {c} is not in the graph")
        for u in v.get("unreviewed", []):
            if u not in eids and u not in nodes:
                errs.append(f"verdict {v['node']}: unreviewed id {u} is not in the graph")
    return errs


def staleness(g: dict) -> dict:
    """{changed: [(node, end, impl)], suspect: [node], edges: [edge id], implementations: [node[impl]],
        verdicts: [node], labels: [node/kind], reviews: [node]}"""
    cur = {}
    for n in g["nodes"]:
        cur[(n["id"], "interface", None)] = n["interface"]["identity"]
        for im in n["implementations"]:
            if "digest" in im:
                cur[(n["id"], "implementation", im["id"])] = im["digest"]

    def key(i):
        end = i.get("end", "interface")
        return (i["node"], end, i.get("implementation") if end == "implementation" else None)

    all_ev = [x for e in g["edges"] for x in e["evidence"]] + [x for n in g["nodes"] for im in n["implementations"] for x in im["realises"]]
    changed = {key(i) for x in all_ev for i in x.get("inputs", []) if key(i) in cur and cur[key(i)] != i["digest"]}
    suspect = {k[0] for k in changed if k[1] == "interface"}
    iface_uses = [e for e in g["edges"] if e["relation"] == "uses" and e.get("from_end", "interface") == "interface"]
    grew = True
    while grew:
        grew = False
        for e in iface_uses:
            to_end = e.get("to_end", "interface")
            hit = e["to"] in suspect or any(k[0] == e["to"] and k[1] == to_end for k in changed)
            if hit and e["from"] not in suspect:
                suspect.add(e["from"])
                grew = True

    def bad(x, structural=False):
        return any(key(i) in changed or (not structural and key(i)[1] == "interface" and i["node"] in suspect)
                   for i in x.get("inputs", []))

    edges = [e["id"] for e in g["edges"] if any(bad(x, e["relation"] in STRUCTURAL) for x in e["evidence"])]
    impls = set()
    for n in g["nodes"]:
        for im in n["implementations"]:
            if any(bad(x) for x in im["realises"]):
                impls.add(f"{n['id']}[{im['id']}]")
    for e in g["edges"]:
        if e["relation"] == "uses" and e.get("from_end") == "implementation" and e["to"] in suspect:
            impls.add(f"{e['from']}[{e['from_implementation']}]")
    verdicts = [v["node"] for v in g["verdicts"]
                if v["node"] in suspect or any(c in edges for c in v["chain"])
                or any(s.startswith(v["node"] + "[") for s in impls)]
    labels, reviews = [], []
    for n in g["nodes"]:
        labels += [f"{n['id']}/{l['kind']}" for l in n.get("labels", []) if l["about"] != n["interface"]["identity"]]
        reviews += [n["id"] for r in n.get("reviews", []) if r["digest"] != n["interface"]["identity"]]
    return {"changed": sorted(f"{a}:{b}" + (f"[{c}]" if c else "") for a, b, c in changed), "suspect": sorted(suspect),
            "edges": edges, "implementations": sorted(impls), "verdicts": verdicts, "labels": labels, "reviews": reviews}


def what_if(g: dict, node_id: str) -> dict:
    """Staleness of the graph if the interface of `node_id` were edited (everything else as recorded)."""
    g = copy.deepcopy(g)
    n = next(n for n in g["nodes"] if n["id"] == node_id)
    n["interface"]["identity"] = {"alg": n["interface"]["identity"]["alg"], "value": "CHANGED"}
    return staleness(g)


def main(argv) -> int:
    if not argv:
        print(__doc__)
        return 2
    g = json.loads(Path(argv[0]).read_text())
    errs = schema_errors(g) + lint(g)
    for e in errs:
        print("ERROR", e)
    print(f"{argv[0]}: {len(g['nodes'])} nodes, {len(g['edges'])} edges, {len(g['verdicts'])} verdicts; "
          f"{'valid' if not errs else str(len(errs)) + ' errors'}")
    s = what_if(g, argv[2]) if len(argv) == 3 and argv[1] == "--what-if" else staleness(g)
    if len(argv) == 3:
        print(f"if the interface of {argv[2]} changed:")
    for k, v in s.items():
        print(f"  stale {k}: {len(v)}")
        for x in v:
            print(f"    {x}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
