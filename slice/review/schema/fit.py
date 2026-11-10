#!/usr/bin/env python3
"""Schema-generality review. Read-only on everything outside this directory.

1. Probes the v1 schema (slice/schema/refinement-graph.schema.json) with mutations.
2. Tries to encode a real recurring statement (4 theorems, 2 proofs) in v1.
3. Migrates the real slice/out/graph.json to the proposed v2 schema and validates it.
4. Builds a v2 maths example from real root exports (Pell lift + a recurring cluster).
5. Shows staleness being computed from digests.
"""
import copy, hashlib, json, sys
from pathlib import Path
import jsonschema

HERE = Path(__file__).resolve().parent
SLICE = HERE.parent.parent
ROOT = SLICE.parent
V1 = json.loads((SLICE / "schema" / "refinement-graph.schema.json").read_text())
V2 = json.loads((HERE / "refinement-graph.v2.schema.json").read_text())
G1 = json.loads((SLICE / "out" / "graph.json").read_text())
val1 = jsonschema.Draft202012Validator(V1)
val2 = jsonschema.Draft202012Validator(V2)
jsonschema.Draft202012Validator.check_schema(V2)


def sha(t):
    return hashlib.sha256(" ".join(t.split()).encode()).hexdigest()


def ok1(g):
    return not list(val1.iter_errors(g))


print("== 1. v1 probes (True = v1 ACCEPTS the mutated graph) ==")
assert ok1(G1)


def mut(desc, f):
    g = copy.deepcopy(G1)
    f(g)
    print(f"  {'ACCEPTS' if ok1(g) else 'rejects'}  {desc}")


def first(g, rel):
    return next(e for e in g["edges"] if e["relation"] == rel)


KC = {"kind": "kernel-checked", "by": "lean-kernel"}
mut("binds edge with kernel-checked evidence", lambda g: first(g, "binds")["evidence"].append(dict(KC)))
mut("kernel-checked evidence with no axioms and no artifact", lambda g: first(g, "refutes").__setitem__("evidence", [dict(KC)]))
mut("edge endpoint that is not a node id", lambda g: first(g, "uses").__setitem__("to", "no-such-node"))
mut("translates edge from a claim to a phrase", lambda g: first(g, "translates").update({"from": "scenario:Spec.wallet.transfer_conserves", "to": "phrase:G-balance"}))
mut("two nodes with the same id", lambda g: g["nodes"].append(copy.deepcopy(g["nodes"][0])))
mut("misspelt evidence field 'axoims'", lambda g: first(g, "refutes")["evidence"][0].update({"axoims": ["sorryAx"]}))
mut("human-asserted evidence by 'slicegen' (a tool)", lambda g: first(g, "binds")["evidence"][0].update({"by": "slicegen"}))
mut("stale: true on every evidence entry, verdict still PROVED-FOR-ALL", lambda g: [x.update({"stale": True}) for e in g["edges"] for x in e["evidence"]])

print("\n== 2. v1 facts about the real graph.json ==")
node_hashes = {n["interface"]["sha256"] for n in G1["nodes"]} | {
    n["implementation"]["sha256"] for n in G1["nodes"] if n["implementation"] and n["implementation"].get("sha256")}
ev = [x for e in G1["edges"] for x in e["evidence"]]
allh = [h for x in ev for h in x.get("inputs_sha256", [])]
print(f"  evidence entries on edges: {len(ev)}; with empty inputs_sha256: {sum(1 for x in ev if not x.get('inputs_sha256'))}")
print(f"  input hashes listed: {len(allh)}; equal to some node/implementation sha256 in the graph: {sum(1 for h in allh if h in node_hashes)}")
print(f"  human-asserted entries whose 'by' is UNREVIEWED: {sum(1 for x in ev if x['kind']=='human-asserted' and x['by']=='UNREVIEWED')} of {sum(1 for x in ev if x['kind']=='human-asserted')}")
print(f"  kernel-checked entries with no axioms: {sum(1 for x in ev if x['kind']=='kernel-checked' and 'axioms' not in x)} of {sum(1 for x in ev if x['kind']=='kernel-checked')}")
dups = [e["id"] for e in G1["edges"] if len({json.dumps(x, sort_keys=True) for x in e["evidence"]}) != len(e["evidence"])]
print(f"  edges with byte-identical duplicate evidence entries: {len(dups)}")
print(f"  nodes whose source has line_start 0: {sum(1 for n in G1['nodes'] if (n['interface'].get('source') or {}).get('line_start') == 0)}")

print("\n== 3. v1 on a real recurring statement (out/reuse, cluster e603d8e562b66b6b) ==")
occ = []
for l in open(ROOT / "out" / "reuse" / "candidates.jsonl"):
    if '"stmtHash":"e603d8e562b66b6b"' in l:
        occ.append(json.loads(l))
print(f"  occurrences: {len(occ)} in {len({o['decl'] for o in occ})} theorems, {len({o['proofHash'] for o in occ})} distinct proofs")
print("  v1 node has ONE implementation with ONE source; maths_fit.py's encoding gives one node per occurrence:")
v1nodes = [{"id": f"lemma:{o['decl']}#{o['id']}", "kind": "statement",
            "interface": {"language": "lean", "text": "Complex.re ⁻¹' Set.Ioi 1 ∈ nhds 2", "source": None,
                          "sha256": sha("Complex.re ⁻¹' Set.Ioi 1 ∈ nhds 2")},
            "implementation": None, "attrs": {}} for o in occ]
g = {"schema": "rosette.refinement-graph/1", "generated_at": "x", "toolchain": {}, "nodes": v1nodes, "edges": [], "verdicts": []}
print(f"    valid v1: {ok1(g)}; nodes: {len(v1nodes)}; distinct interface hashes: {len({n['interface']['sha256'] for n in v1nodes})} -> identity of the shared statement is nowhere in the graph")
cands = [json.loads(l) for l in open(ROOT / "out" / "rosette_tests_candidates.jsonl")]
cands = [c for c in cands if c["record"] == "candidate"]
bt, bh = {}, {}
for c in cands:
    bt.setdefault(c["statement"], set()).add(c["stmtHash"])
    bh.setdefault(c["stmtHash"], set()).add(c["statement"])
print(f"  out/rosette_tests_candidates.jsonl: {len(cands)} candidates; printed text truncated: {sum(1 for c in cands if c['statement'].endswith('…'))}")
print(f"    printed texts with more than one structural hash: {sum(1 for v in bt.values() if len(v) > 1)} of {len(bt)}")
print(f"    structural hashes with more than one printed text: {sum(1 for v in bh.values() if len(v) > 1)} of {len(bh)}")

# ---------------------------------------------------------------- 4. migrate software graph
print("\n== 4. real slice graph.json migrated to v2 ==")
T = G1["toolchain"]
runs = [
    {"id": "run:slicegen", "tool": "slicegen", "version": T["generator"]},
    {"id": "run:lean", "tool": "lean-kernel", "version": T["lean"], "toolchain": {"lean": T["lean"], "mathlib": T["mathlib"]}},
    {"id": "run:translate", "tool": "charon+aeneas", "version": T["aeneas"], "toolchain": {"charon": T["charon"], "aeneas": T["aeneas"], "rustc": T["rustc"]}},
    {"id": "run:cucumber", "tool": "cucumber-rs", "toolchain": {"rustc": "stable 1.94"}},
]
RUN = {"slicegen": "run:slicegen", "lean-kernel": "run:lean", "lean-eval": "run:lean", "charon+aeneas": "run:translate",
       "aeneas-library": "run:translate", "cucumber-rs": "run:cucumber", "cucumber-rs+lean-eval": "run:cucumber"}
KIND = {"feature": "group", "library_model": "function"}
N1 = {n["id"]: n for n in G1["nodes"]}
dropped_unreviewed = relabelled = 0


def dg(h):
    return {"alg": "sha256-text", "value": h}


def scope(s):
    if not s or s == "n/a":
        return {"quantifier": "n/a"}
    if s == "all-inputs":
        return {"quantifier": "all"}
    return {"quantifier": "instances", "n": int(s.split()[0]), "method": s.split()[1]}


def evid(x, frm=None, to=None, realises_of=None):
    global dropped_unreviewed, relabelled
    if x["kind"] == "human-asserted" and x["by"] == "UNREVIEWED":
        dropped_unreviewed += 1          # nobody asserted anything: that is absence of evidence
        return None
    kind = x["kind"]
    if kind == "kernel-checked" and "axioms" not in x:
        kind, relabelled = "tool-trusted", relabelled + 1   # 'constant occurs in term' is read by audit code, not a theorem
    out = {"kind": kind, "by": ("human:" if kind == "human-asserted" else "tool:") + x["by"].replace("reviewer:", ""),
           "scope": scope(x.get("scope"))}
    if x["by"] in RUN:
        out["run"] = RUN[x["by"]]
    for k in ("artifact", "detail"):
        if x.get(k):
            out[k] = x[k]
    if x.get("witness") is not None:
        out["witness"] = x["witness"]
    if kind == "kernel-checked":
        out["axioms"] = x["axioms"]
    ins = []
    for nid in filter(None, [frm, to, realises_of]):   # stamp both ends with the digest the generator held
        ins.append({"node": nid, "end": "interface", "digest": dg(N1[nid]["interface"]["sha256"])})
    out["inputs"] = ins
    return out


def src(s):
    if not s:
        return None
    o = {"file": s["file"]}
    if s.get("line_start"):
        o["line_start"], o["line_end"] = s["line_start"], s.get("line_end", s["line_start"])
    return o


nodes2 = []
for n in G1["nodes"]:
    i = n["interface"]
    generated = n["kind"] in ("statement",) or n["attrs"].get("generated")
    iface = {"language": i["language"], "text": i["text"], "text_complete": True, "identity": dg(i["sha256"])}
    if src(i.get("source")):
        iface["source"] = src(i["source"])
    impls = []
    if n["implementation"]:
        m = n["implementation"]
        im = {"id": "p1" if n["kind"] == "statement" else "body", "language": m["language"], "ref": m["ref"],
              "complete": m["complete"], "hidden": n["kind"] == "statement",
              "realises": [e for e in (evid(x, realises_of=n["id"]) for x in m["realises"]) if e]}
        if src(m.get("source")):
            im["source"] = src(m["source"])
        if m.get("sha256"):
            im["digest"] = dg(m["sha256"])
        if n["attrs"].get("size") is not None and n["kind"] == "statement":
            im["metrics"] = {"size_lines": n["attrs"]["size"]}
        impls.append(im)
    attrs = {k: v for k, v in n["attrs"].items() if k != "size"}
    if n["kind"] == "library_model":
        attrs["library_model"] = True
    if n["kind"] == "definition" and n["attrs"].get("size") is not None:
        iface["metrics"] = {"size_tree": n["attrs"]["size"]}
        iface["budgets"] = [{"measure": "definition expression nodes (DESIGN 4.1 warning threshold)", "value": n["attrs"]["size"], "max": 40,
                             "within": n["attrs"]["size"] <= 40}]
    nodes2.append({"id": n["id"], "kind": KIND.get(n["kind"], n["kind"]), "status": "proposed",
                   "origin": {"by": "tool:slicegen" if generated else "model:unrecorded", "run": "run:slicegen"} if generated
                   else {"by": "model:unrecorded"},
                   "reviews": [], "interface": iface, "implementations": impls, "labels": [], "attrs": attrs})

edges2 = []
for e in G1["edges"]:
    rel, f, t = e["relation"], e["from"], e["to"]
    seen, evs, occs = set(), [], []
    for x in e["evidence"]:
        if rel == "composed_of":
            occs.append({"role": N1[t]["attrs"].get("step_kind", ""), "at": {"file": x["detail"].split(":")[0], "line_start": int(x["detail"].split(":")[1].split()[0]),
                                                                             "line_end": int(x["detail"].split(":")[1].split()[0])}})
            x = dict(x, detail="")
        if rel == "binds" and x.get("artifact", "").startswith("wallet-bdd"):
            occs.append({"role": "second reading (cucumber step body)", "at": {"file": x["artifact"].split(":")[0], "line_start": int(x["artifact"].split(":")[1]),
                                                                              "line_end": int(x["artifact"].split(":")[1])}})
        k = json.dumps(x, sort_keys=True)
        if k in seen:
            continue
        seen.add(k)
        y = evid(x, f, t)
        if y:
            evs.append(y)
    e2 = {"id": e["id"], "from": f, "to": t, "relation": rel, "evidence": evs}
    if rel == "uses":
        if N1[f]["kind"] == "statement" and N1[t]["kind"] == "statement":
            e2["relation"] = "requires"          # stmt -> .sat: a verdict side condition, not a dependency
            e2["id"] = e["id"].replace("uses:", "requires:", 1)
        else:
            e2["from_end"] = "interface"
    if occs:
        e2["occurrences"] = occs
    edges2.append(e2)

SARIF = {"PROVED-FOR-ALL": "pass", "PROVED-INSTANCE": "pass", "REFUTED": "fail", "COUNTEREXAMPLE": "fail", "VACUOUS": "fail",
         "UNBOUND": "notApplicable", "AMBIGUOUS": "notApplicable", "UNSUPPORTED": "notApplicable", "TESTED-ONLY": "open",
         "VACUOUS-SUSPECTED": "review", "STALE": "review"}
idmap = {e["id"]: e2["id"] for e, e2 in zip(G1["edges"], edges2)}
E2 = {e["id"]: e for e in edges2}
verdicts2 = []
for v in G1["verdicts"]:
    chain = [idmap[c] for c in v["chain"]]
    # everything the scenario's phrases bind to, with no valid review
    unrev = sorted({e["id"] for e in edges2 if e["relation"] == "binds" and not e["evidence"] and any(
        c["from"] == v["node"] and c["to"] == e["from"] for c in edges2 if c["relation"] == "composed_of")})
    verdicts2.append({"node": v["node"], "outcome": SARIF[v["status"]], "code": v["status"], "expected": v.get("expected", ""),
                      "as_expected": v.get("as_expected", True), "flags": [f for f in v["flags"] if not f.startswith("UNREVIEWED")],
                      "chain": chain, "rests_on": v["rests_on"], "unreviewed": unrev, "stale": [],
                      "counterexample": v.get("counterexample")})
G2 = {"schema": "rosette.refinement-graph/2", "generated_at": G1["generated_at"], "runs": runs, "nodes": nodes2, "edges": edges2, "verdicts": verdicts2}
errs = list(val2.iter_errors(G2))
for er in errs[:10]:
    print("  ERROR", list(er.absolute_path)[:4], er.message[:200])
print(f"  v2 valid: {not errs}; {len(nodes2)} nodes, {len(edges2)} edges, {len(verdicts2)} verdicts")
print(f"  'human-asserted by UNREVIEWED' entries dropped (edge now has no human evidence): {dropped_unreviewed}")
print(f"  'kernel-checked' entries with no theorem behind them relabelled tool-trusted: {relabelled}")
print(f"  uses edges stmt -> .sat turned into 'requires': {sum(1 for e in edges2 if e['relation']=='requires')}")
print(f"  binds edges with empty evidence: {sum(1 for e in edges2 if e['relation']=='binds' and not e['evidence'])} of {sum(1 for e in edges2 if e['relation']=='binds')}")
(HERE / "software.v2.graph.json").write_text(json.dumps(G2, indent=1, ensure_ascii=False))

# ---------------------------------------------------------------- 5. maths example
print("\n== 5. maths example in v2 (real data: out/demo Pell 'filtered' + out/reuse cluster) ==")
AX = ["propext", "Classical.choice", "Quot.sound"]
mruns = [
    {"id": "run:demo-filtered", "tool": "Rosette.Demo", "version": "config filtered",
     "toolchain": {"lean": "4.36.0-rc2"}, "config": {"levels_k": [6, 3], "minProofSize": 40, "maxStatementSize": 150, "maxFraction": 0.8},
     "complete": True},
    {"id": "run:reuse", "tool": "Rosette.Reuse", "toolchain": {"lean": "4.36.0-rc2"},
     "config": {"minTheoremProof": 800, "minCandidateProof": 20, "theorems": 600}, "complete": True},
]
P = "Pell.exists_of_not_isSquare"


def tdg(t):
    return {"alg": "sha256-text", "value": sha(t)}


def kc(name):
    return {"kind": "kernel-checked", "by": "tool:lean-kernel", "run": "run:demo-filtered", "artifact": name, "axioms": AX,
            "scope": {"quantifier": "all"}, "detail": "addDecl with synchronous kernel check inside a `lake env lean` session; not stored in an .olean"}


def lemma(suffix, text, stmt_size, hyps, own_before, own_after, expl, rating):
    name = f"{P}.{suffix}"
    idt = tdg(text)
    im = {"id": "p1", "language": "lean-proof", "ref": name, "source": {"decl": name}, "complete": True, "hidden": True,
          "metrics": {"size_dag": own_after} if own_after else {"size_dag": own_before}, "realises": [kc(name)]}
    if own_after:
        im["metrics"]["x_size_dag_before_lifting_children"] = own_before
    return {"id": f"stmt:{name}", "kind": "statement", "status": "proposed",
            "origin": {"by": "tool:rosette.lift", "run": "run:demo-filtered"}, "reviews": [],
            "interface": {"language": "lean", "text": text, "text_complete": True, "identity": idt,
                          "metrics": {"size_dag": stmt_size, "num_hyp_args": hyps},
                          "budgets": [{"measure": "closed statement DAG size (LiftConfig.maxStatementSize)", "value": stmt_size, "max": 150,
                                       "within": stmt_size <= 150}]},
            "implementations": [im],
            "labels": [{"kind": "explanation", "text": expl, "language": "english", "by": "model:rosette-demo-writeup", "about": idt, "reviews": []},
                       {"kind": "rating", "text": rating, "by": "model:rosette-demo-writeup", "about": idt, "reviews": []}],
            "attrs": {}}


root_text = "Pell.exists_of_not_isSquare {d : ℤ} (h₀ : 0 < d) (hd : ¬IsSquare d) : ∃ x y, x ^ 2 - d * y ^ 2 = 1 ∧ y ≠ 0"
root = {"id": f"stmt:{P}", "kind": "statement", "status": "accepted", "origin": {"by": "human:mathlib-authors"},
        "reviews": [{"by": "human:mathlib-maintainers", "decision": "approved", "digest": tdg(root_text), "note": "merged in Mathlib"}],
        "interface": {"language": "lean", "text": root_text, "text_complete": True, "identity": tdg(root_text),
                      "source": {"file": "Mathlib/NumberTheory/Pell.lean", "line_start": 324, "line_end": 386, "decl": P}},
        "implementations": [
            {"id": "mathlib", "language": "lean-proof", "ref": P, "source": {"file": "Mathlib/NumberTheory/Pell.lean", "line_start": 324, "line_end": 386, "decl": P},
             "complete": True, "hidden": False, "metrics": {"size_dag": 7089, "size_tree": 319530, "size_lines": 63},
             "realises": [{"kind": "tool-trusted", "by": "tool:mathlib-olean", "scope": {"quantifier": "all"},
                           "detail": "imported from Mathlib's compiled .olean; not re-checked and axioms not printed by the demo"}]},
            {"id": "filtered", "language": "lean-proof", "ref": f"{P}.filtered", "source": {"decl": f"{P}.filtered"}, "complete": True, "hidden": False,
             "metrics": {"size_dag": 1728}, "realises": [kc(f"{P}.filtered")]}],
        "labels": [{"kind": "name", "text": "Pell's equation has a nontrivial solution", "language": "english", "by": "model:rosette-demo-writeup",
                    "about": tdg(root_text), "reviews": []}],
        "attrs": {}}
L1 = lemma("filtered_1", "Pell.exists_of_not_isSquare.filtered_1 {d : ℤ} (hd : ¬IsSquare d) (M : ℤ) (hM : {q | |q.num ^ 2 - d * ↑q.den ^ 2| < M}.Infinite) : ∃ x y, x ^ 2 - d * y ^ 2 = 1 ∧ y ≠ 0",
           130, 2, 5166, 208, "infinitely many q with |N(q)| < M implies a solution exists (the pigeonhole half of the theorem; a continuation, not a `have`)", "meaningful")
L11 = lemma("filtered_1.filtered_1", "Pell.exists_of_not_isSquare.filtered_1.filtered_1 {d : ℤ} (m : ℤ) (hm : {q | q.num ^ 2 - d * ↑q.den ^ 2 = m}.Infinite) (hm₀ : m ≠ 0) : ∃ x y, x ^ 2 - d * y ^ 2 = 1 ∧ y ≠ 0",
            115, 2, 3812, None, "infinitely many q with N(q) = m, m ≠ 0, implies a solution exists", "meaningful")
L2 = lemma("filtered_2", "Pell.exists_of_not_isSquare.filtered_2 {d : ℤ} (h₀ : 0 < d) (hd : ¬IsSquare d) : let ξ := √↑d; Irrational ξ",
           38, 2, 367, 104, "√d is irrational (verbatim the author's `have hξ`)", "meaningful")
L22 = lemma("filtered_2.filtered_2", "Pell.exists_of_not_isSquare.filtered_2.filtered_2 {d : ℤ} (h₀ : 0 < d) : √↑d ^ 2 = ↑d",
            55, 1, 54, None, "√d ^ 2 = d", "technical")
mnodes = [root, L1, L11, L2, L22]


def stamp(n, end="interface"):
    return {"node": n["id"], "end": end, "digest": n["interface"]["identity"]}


def lift_edges(child, parent, pimpl, role, head):
    name = child["implementations"][0]["ref"]
    return [
        {"id": f"uses:{parent['id']}[{pimpl}]->{child['id']}", "from": parent["id"], "to": child["id"], "relation": "uses",
         "from_end": "implementation", "from_implementation": pimpl,
         "occurrences": [{"role": role, "implementation": pimpl, "attrs": {"head": head}}],
         "evidence": [{"kind": "tool-trusted", "by": "tool:rosette.lift", "run": "run:demo-filtered", "scope": {"quantifier": "n/a"},
                       "inputs": [stamp(child)],
                       "detail": f"getUsedConstantsAsSet of the kernel-checked rewritten proof contains {name}"}]},
        {"id": f"lifted_from:{child['id']}->{parent['id']}", "from": child["id"], "to": parent["id"], "relation": "lifted_from",
         "to_end": "implementation", "occurrences": [{"role": role, "attrs": {"head": head, "term_path": "not exported by Rosette/Demo.lean"}}],
         "evidence": [{"kind": "tool-trusted", "by": "tool:rosette.lift", "run": "run:demo-filtered", "scope": {"quantifier": "n/a"},
                       "inputs": [stamp(child), stamp(parent)],
                       "detail": "proof is the parent's sub-term abstracted over its interface (closeOver)"}]}]


medges = (lift_edges(L1, root, "filtered", "haveBody", "Exists.casesOn") + lift_edges(L11, L1, "p1", "haveBody", None)
          + lift_edges(L2, root, "filtered", "haveValue", "irrational_nrt_of_notint_nrt") + lift_edges(L22, L2, "p1", "arg", "Real.sq_sqrt"))

# recurring statement: one node, two implementations, four parents
stext = {json.loads(l)["stmtHash"]: json.loads(l)["statement"] for l in open(ROOT / "out" / "reuse" / "statements.jsonl")}
cl = next(c for c in json.load(open(ROOT / "out" / "reuse" / "clusters.json"))["E"] if c["key"] == "e603d8e562b66b6b")
roots = {}
for l in open(ROOT / "out" / "reuse" / "candidates.jsonl"):
    if '"role":"root"' in l:
        r = json.loads(l)
        if r["decl"] in cl["decls"]:
            roots[r["decl"]] = r
sid = {"alg": "lean-struct64", "value": cl["key"]}
proofs = sorted({o["proofHash"] for o in occ})
shared = {"id": f"stmt:lean-struct64:{cl['key']}", "kind": "statement", "status": "candidate", "origin": {"by": "tool:rosette.reuse", "run": "run:reuse"},
          "reviews": [],
          "interface": {"language": "lean", "text": cl["statement"], "text_complete": True, "identity": sid,
                        "digests": [{"alg": "lean-struct64-L1", "value": occ[0]["h1"]}, {"alg": "lean-struct64-L2", "value": occ[0]["h2"]}],
                        "metrics": {"size_dag": cl["statementSize"], "num_args": 0, "num_hyp_args": 0, "x_net_saving": cl["net"]}},
          "implementations": [
              {"id": f"t{i+1}", "language": "lean-term", "digest": {"alg": "lean-proof64", "value": ph}, "complete": True, "hidden": True,
               "metrics": {"size_dag": next(o["proofSizeDag"] for o in occ if o["proofHash"] == ph),
                           "size_tree": next(o["proofSizeTree"] for o in occ if o["proofHash"] == ph)},
               "realises": [{"kind": "tool-trusted", "by": "tool:rosette.candidates", "run": "run:reuse", "scope": {"quantifier": "all"},
                             "detail": "sub-term of a compiled Mathlib proof; statement obtained by inferType, not re-checked standalone"}]}
              for i, ph in enumerate(proofs)],
          "labels": [], "attrs": {"class": cl["class"], "exact?": cl["exact"], "inLib": cl["inLib"]}}
mnodes.append(shared)
for d in cl["decls"]:
    r = roots[d]
    pid = {"alg": "lean-struct64", "value": r["stmtHash"]}
    mnodes.append({"id": f"stmt:{d}", "kind": "statement", "status": "accepted", "origin": {"by": "human:mathlib-authors"},
                   "reviews": [{"by": "human:mathlib-maintainers", "decision": "approved", "digest": pid, "note": "merged in Mathlib"}],
                   "interface": {"language": "lean", "text": stext[r["stmtHash"]], "text_complete": not stext[r["stmtHash"]].endswith("…"), "identity": pid,
                                 "source": {"decl": d}, "metrics": {"size_dag": r["statementSize"]}},
                   "implementations": [{"id": "mathlib", "language": "lean-proof", "ref": d, "source": {"decl": d}, "complete": True,
                                        "digest": {"alg": "lean-proof64", "value": r["proofHash"]},
                                        "metrics": {"size_dag": r["proofSizeDag"], "size_tree": r["proofSizeTree"]},
                                        "realises": [{"kind": "tool-trusted", "by": "tool:mathlib-olean", "scope": {"quantifier": "all"},
                                                      "detail": "imported from Mathlib's compiled .olean; not re-checked here"}]}],
                   "labels": [], "attrs": {}})
    for o in [o for o in occ if o["decl"] == d]:
        medges.append({"id": f"lifted_from:{shared['id']}->stmt:{d}", "from": shared["id"], "to": f"stmt:{d}", "relation": "lifted_from",
                       "to_end": "implementation",
                       "occurrences": [{"role": o["role"], "implementation": f"t{proofs.index(o['proofHash'])+1}",
                                        "at": {"decl": d}, "attrs": {"candidate_id": o["id"], "head": o["headConst"],
                                                                     "term_path": "not exported by Rosette/Reuse.lean"}}],
                       "evidence": [{"kind": "tool-trusted", "by": "tool:rosette.reuse", "run": "run:reuse", "scope": {"quantifier": "n/a"},
                                     "inputs": [{"node": shared["id"], "end": "interface", "digest": sid},
                                                {"node": f"stmt:{d}", "end": "implementation", "implementation": "mathlib",
                                                 "digest": {"alg": "lean-proof64", "value": r["proofHash"]}}],
                                     "detail": "structural-hash equality of the closed statement (Rosette.statementHash)"}]})
mverd = [
    {"node": L1["id"], "outcome": "review", "code": "LIFT-KERNEL-CHECKED", "flags": ["UNREVIEWED-LABELS", "MACHINE-PROPOSED"],
     "chain": [medges[0]["id"], medges[1]["id"]], "rests_on": ["kernel-checked", "tool-trusted"], "unreviewed": [L1["id"]], "stale": []},
    {"node": shared["id"], "outcome": "open", "code": "CANDIDATE-ONLY", "flags": ["RECURS-IN-4-THEOREMS", "2-DISTINCT-PROOFS"],
     "chain": [e["id"] for e in medges if e["from"] == shared["id"]], "rests_on": ["tool-trusted"], "unreviewed": [shared["id"]], "stale": []},
]
M2 = {"schema": "rosette.refinement-graph/2", "generated_at": "2026-11-09", "runs": mruns, "nodes": mnodes, "edges": medges, "verdicts": mverd}
errs = list(val2.iter_errors(M2))
for er in errs[:10]:
    print("  ERROR", list(er.absolute_path)[:5], er.message[:200])
ids = [n["id"] for n in mnodes]
assert len(ids) == len(set(ids)) and all(e["from"] in ids and e["to"] in ids for e in medges)
print(f"  v2 valid: {not errs}; {len(mnodes)} nodes, {len(medges)} edges")
print(f"  shared statement: 1 node, {len(shared['implementations'])} implementations, {sum(1 for e in medges if e['from']==shared['id'])} lifted_from edges")
(HERE / "maths.v2.graph.json").write_text(json.dumps(M2, indent=1, ensure_ascii=False))


# ---------------------------------------------------------------- 6. staleness from digests
def stale(g):
    cur = {}
    for n in g["nodes"]:
        cur[(n["id"], "interface", None)] = n["interface"]["identity"]
        for im in n["implementations"]:
            if "digest" in im:
                cur[(n["id"], "implementation", im["id"])] = im["digest"]
    out = {"edges": [], "labels": [], "reviews": [], "realises": []}

    def bad(x):
        return any(cur.get((i["node"], i.get("end", "interface"), i.get("implementation"))) not in (None, i["digest"]) for i in x.get("inputs", []))
    for e in g["edges"]:
        if any(bad(x) for x in e["evidence"]):
            out["edges"].append(e["id"])
    for n in g["nodes"]:
        out["labels"] += [f"{n['id']}/{l['kind']}" for l in n.get("labels", []) if l["about"] != n["interface"]["identity"]]
        out["reviews"] += [n["id"] for r in n.get("reviews", []) if r["digest"] != n["interface"]["identity"]]
        out["realises"] += [f"{n['id']}/{im['id']}" for im in n["implementations"] if any(bad(x) for x in im["realises"])]
    return out


print("\n== 6. staleness computed from digests (v2) ==")
print("  maths, untouched:", {k: len(v) for k, v in stale(M2).items()})
m = copy.deepcopy(M2)
t = next(n for n in m["nodes"] if n["id"] == L2["id"])
t["interface"]["text"] = t["interface"]["text"].replace("Irrational ξ", "Irrational (ξ + 1)")
t["interface"]["identity"] = tdg(t["interface"]["text"])
s = stale(m)
print("  maths, statement of filtered_2 edited:", {k: len(v) for k, v in s.items()})
for k, v in s.items():
    for x in v:
        print("     ", k, x[:110])
print("  software, untouched:", {k: len(v) for k, v in stale(G2).items()})
g = copy.deepcopy(G2)
t = next(n for n in g["nodes"] if n["id"] == "def:Vocab.covers")
t["interface"]["text"] = t["interface"]["text"].replace("≤", "<")
t["interface"]["identity"] = dg(sha(t["interface"]["text"]))
s = stale(g)
print("  software, Vocab.covers changed from ≤ to <:", {k: len(v) for k, v in s.items()})
for x in s["edges"]:
    print("      edge", x[:120])
print("  (v1 on the same edit: every evidence entry has stale=false stored, and no entry names def:Vocab.covers's hash:",
      N1["def:Vocab.covers"]["interface"]["sha256"] not in set(allh), ")")
