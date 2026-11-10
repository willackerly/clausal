#!/usr/bin/env python3
"""Maths-side worked example for the refinement-graph schema (v2), built from REAL exports of the root project.

Reads, read-only:
  ../../out/demo/generated/Pell.exists_of_not_isSquare.filtered.md   (transcribed below; that export is Markdown, not JSON)
  ../../out/reuse/{candidates.jsonl, statements.jsonl, clusters.json, run.json}
Writes maths-example.graph.json next to this script and validates it with the same schema and lint as the
software graph (slicegen/graphlint.py). Nothing in the repo root is modified.

    python3 schema/maths_fit.py

What it encodes:
  (a) Pell.exists_of_not_isSquare with TWO proofs (Mathlib's, and the decomposed `.filtered` one that calls lifted
      lemmas), and 5 of its 12 kernel-checked lifted lemmas, one of which the lift produced TWICE under two names
      (`filtered_5` and `filtered_2.filtered_2`, both `√↑d ^ 2 = ↑d`): one node, two implementations;
  (b) a statement that recurs in 4 Mathlib theorems with 2 distinct proofs (out/reuse cluster e603d8e562b66b6b):
      one node identified by its structural hash, two implementations, four `lifted_from` edges.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
from slicegen import graphlint  # noqa: E402

REUSE = ROOT / "out" / "reuse"
AX = ["propext", "Classical.choice", "Quot.sound"]
P = "Pell.exists_of_not_isSquare"


def sha(t):
    return hashlib.sha256(" ".join(t.split()).encode()).hexdigest()


def tdg(t):
    return {"alg": "sha256-text", "value": sha(t)}


run_json = json.loads((REUSE / "run.json").read_text())
runs = [
    {"id": "run:demo-filtered", "tool": "Rosette.Demo", "version": "config filtered", "toolchain": {"lean": run_json["leanVersion"]},
     "config": {"levels_k": [6, 3], "minProofSize": 40, "maxStatementSize": 150, "maxFraction": 0.8}, "complete": True,
     "note": "out/demo/generated/Pell.exists_of_not_isSquare.filtered.md"},
    {"id": "run:reuse", "tool": "Rosette.Reuse", "toolchain": {"lean": run_json["leanVersion"]},
     "config": {"minTheoremProof": run_json["minTheoremProof"], "minCandidateProof": run_json["minCandidateProof"],
                "theorems": run_json["theorems"]},
     "complete": not run_json["truncated"], "note": "out/reuse/"},
]


def kc(name):
    return {"kind": "kernel-checked", "by": "tool:lean-kernel", "run": "run:demo-filtered", "artifact": name, "axioms": AX,
            "scope": {"quantifier": "all"}, "method": "script-session",
            "detail": "addDecl with synchronous kernel check inside a `lake env lean` session; not stored in an .olean"}


def impl(id_, name, size, before=None):
    m = {"size_dag": size}
    if before:
        m["x_size_dag_before_lifting_children"] = before
    return {"id": id_, "language": "lean-proof", "ref": name, "source": {"decl": name}, "complete": True, "hidden": True,
            "metrics": m, "realises": [kc(name)]}


def lemma(name, text, stmt_size, hyps, size, before, expl, rating):
    """One lifted lemma. `text` is the statement as printed, without the constant's name. The node's identity is a
    digest of name + printed text: the export has no structural hash for lifted lemmas, and printed text alone is not
    an identity (see the two `√↑d ^ 2 = ↑d` lemmas below)."""
    full = f"{P}.{name} {text}"
    idt = tdg(full)
    return {"id": f"stmt:{P}.{name}", "kind": "statement", "status": "proposed",
            "origin": {"by": "tool:rosette.lift", "run": "run:demo-filtered"}, "reviews": [],
            "interface": {"language": "lean", "text": full, "text_complete": True, "identity": idt,
                          "metrics": {"size_dag": stmt_size, "num_hyp_args": hyps},
                          "budgets": [{"measure": "closed statement DAG size (LiftConfig.maxStatementSize)", "value": stmt_size,
                                       "max": 150, "within": stmt_size <= 150}]},
            "implementations": [impl("p1", f"{P}.{name}", size, before)],
            "labels": [{"kind": "explanation", "text": expl, "language": "english", "by": "model:rosette-demo-writeup", "about": idt, "reviews": []},
                       {"kind": "rating", "text": rating, "by": "model:rosette-demo-writeup", "about": idt, "reviews": []}],
            "attrs": {"identity_note": "name + printed text: Rosette/Demo.lean does not export the structural hash of a lifted lemma"}}


root_text = "{d : ℤ} (h₀ : 0 < d) (hd : ¬IsSquare d) : ∃ x y, x ^ 2 - d * y ^ 2 = 1 ∧ y ≠ 0"
root = {"id": f"stmt:{P}", "kind": "statement", "status": "accepted", "origin": {"by": "human:mathlib-authors"},
        "reviews": [{"by": "human:mathlib-maintainers", "decision": "approved", "digest": tdg(root_text),
                     "note": "merged in Mathlib (an illustration of an accepted node; the exports do not record reviews)"}],
        "interface": {"language": "lean", "text": root_text, "text_complete": True, "identity": tdg(root_text),
                      "source": {"file": "Mathlib/NumberTheory/Pell.lean", "decl": P}},
        "implementations": [
            {"id": "mathlib", "language": "lean-proof", "ref": P, "source": {"file": "Mathlib/NumberTheory/Pell.lean", "decl": P},
             "complete": True, "hidden": False, "metrics": {"size_dag": 7089, "size_tree": 319530},
             "realises": [{"kind": "tool-trusted", "by": "tool:mathlib-olean", "scope": {"quantifier": "all"},
                           "detail": "imported from Mathlib's compiled .olean; not re-checked by the demo, axioms of the original not printed"}]},
            {"id": "filtered", "language": "lean-proof", "ref": f"{P}.filtered", "source": {"decl": f"{P}.filtered"}, "complete": True,
             "hidden": False, "metrics": {"size_dag": 1728}, "realises": [kc(f"{P}.filtered")]}],
        "labels": [{"kind": "name", "text": "Pell's equation has a nontrivial solution", "language": "english",
                    "by": "model:rosette-demo-writeup", "about": tdg(root_text), "reviews": []}],
        "attrs": {"lean_names": [P]}}
L1 = lemma("filtered_1", "{d : ℤ} (hd : ¬IsSquare d) (M : ℤ) (hM : {q | |q.num ^ 2 - d * ↑q.den ^ 2| < M}.Infinite) : ∃ x y, x ^ 2 - d * y ^ 2 = 1 ∧ y ≠ 0",
           130, 2, 208, 5166, "infinitely many q with |N(q)| < M implies a solution exists (a continuation of the proof, not a `have`)", "meaningful")
L11 = lemma("filtered_1.filtered_1", "{d : ℤ} (m : ℤ) (hm : {q | q.num ^ 2 - d * ↑q.den ^ 2 = m}.Infinite) (hm₀ : m ≠ 0) : ∃ x y, x ^ 2 - d * y ^ 2 = 1 ∧ y ≠ 0",
            115, 2, 3812, None, "infinitely many q with N(q) = m, m ≠ 0, implies a solution exists", "meaningful")
L2 = lemma("filtered_2", "{d : ℤ} (h₀ : 0 < d) (hd : ¬IsSquare d) : let ξ := √↑d; Irrational ξ",
           38, 2, 104, 367, "√d is irrational (verbatim the author's `have hξ`)", "meaningful")
# The lift produced two lemmas that PRINT identically. Their closed statements have different sizes (55 and 70 nodes),
# so they are not known to be the same statement: two nodes, and an `equivalent` edge that nothing yet supports.
L22 = lemma("filtered_2.filtered_2", "{d : ℤ} (h₀ : 0 < d) : √↑d ^ 2 = ↑d", 55, 1, 54, None, "√d ^ 2 = d", "technical")
L5 = lemma("filtered_5", "{d : ℤ} (h₀ : 0 < d) : √↑d ^ 2 = ↑d", 70, 1, 112, None, "√d ^ 2 = d", "technical")
nodes = [root, L1, L11, L2, L22, L5]


def stamp(n):
    return {"node": n["id"], "end": "interface", "digest": n["interface"]["identity"]}


def lift_edges(child, parent, pimpl, role, head):
    cimpl, name = "p1", child["implementations"][0]["ref"]
    occ = {"role": role, "implementation": pimpl, "attrs": {"term_path": "not exported by Rosette/Demo.lean"}}
    if head:
        occ["attrs"]["head"] = head
    return [
        {"id": f"uses:{parent['id']}[{pimpl}]->{child['id']}", "from": parent["id"], "to": child["id"], "relation": "uses",
         "from_end": "implementation", "from_implementation": pimpl, "occurrences": [occ],
         "evidence": [{"kind": "tool-trusted", "by": "tool:rosette.lift", "run": "run:demo-filtered", "scope": {"quantifier": "n/a"},
                       "inputs": [stamp(child)],
                       "detail": f"the kernel-checked rewritten proof calls {name}"}]},
        {"id": f"lifted_from:{child['id']}->{parent['id']}[{pimpl}]", "from": child["id"], "to": parent["id"], "relation": "lifted_from",
         "to_end": "implementation", "occurrences": [dict(occ, implementation=cimpl)],
         "evidence": [{"kind": "tool-trusted", "by": "tool:rosette.lift", "run": "run:demo-filtered", "scope": {"quantifier": "n/a"},
                       "inputs": [stamp(child), stamp(parent)],
                       "detail": "the lemma's proof is a sub-term of the parent's proof, abstracted over its free variables (closeOver)"}]}]


edges = (lift_edges(L1, root, "filtered", "haveBody", "Exists.casesOn") + lift_edges(L11, L1, "p1", "haveBody", None)
         + lift_edges(L2, root, "filtered", "haveValue", "irrational_nrt_of_notint_nrt")
         + lift_edges(L22, L2, "p1", "arg", "Real.sq_sqrt") + lift_edges(L5, root, "filtered", "arg", "Real.sq_sqrt"))
edges.append({"id": f"equivalent:{L22['id']}->{L5['id']}", "from": L22["id"], "to": L5["id"], "relation": "equivalent",
              "evidence": [],        # claimed, not evidenced
              "attrs": {"why_claimed": "the two statements print identically",
                        "why_unsupported": "their closed statements differ in size (55 and 70 DAG nodes), so the printer is hiding a difference; "
                                           "no structural hash is exported for lifted lemmas and no proof of equivalence exists"}})

# ---- a statement recurring in several Mathlib theorems (out/reuse)
KEY = "e603d8e562b66b6b"
occs = [json.loads(l) for l in open(REUSE / "candidates.jsonl") if f'"stmtHash":"{KEY}"' in l]
stext = {}
for l in open(REUSE / "statements.jsonl"):
    r = json.loads(l)
    stext[r["stmtHash"]] = r["statement"]
cl = next(c for c in json.load(open(REUSE / "clusters.json"))["E"] if c["key"] == KEY)
roots = {}
for l in open(REUSE / "candidates.jsonl"):
    if '"role":"root"' in l:
        r = json.loads(l)
        if r["decl"] in cl["decls"]:
            roots[r["decl"]] = r
sid = {"alg": "lean-struct64", "value": KEY}
proofs = sorted({o["proofHash"] for o in occs})
shared = {"id": f"stmt:lean-struct64:{KEY}", "kind": "statement", "status": "candidate",
          "origin": {"by": "tool:rosette.reuse", "run": "run:reuse"}, "reviews": [],
          "interface": {"language": "lean", "text": cl["statement"], "text_complete": True, "identity": sid,
                        "digests": [{"alg": "lean-struct64-L1", "value": occs[0]["h1"]}, {"alg": "lean-struct64-L2", "value": occs[0]["h2"]}],
                        "metrics": {"size_dag": cl["statementSize"], "num_args": 0, "num_hyp_args": 0, "x_net_saving": cl["net"]}},
          "implementations": [
              {"id": f"t{i + 1}", "language": "lean-term", "digest": {"alg": "lean-proof64", "value": ph}, "complete": True, "hidden": True,
               "metrics": {"size_dag": next(o["proofSizeDag"] for o in occs if o["proofHash"] == ph),
                           "size_tree": next(o["proofSizeTree"] for o in occs if o["proofHash"] == ph)},
               "realises": [{"kind": "tool-trusted", "by": "tool:rosette.candidates", "run": "run:reuse", "scope": {"quantifier": "all"},
                             "detail": "a sub-term of a compiled Mathlib proof; its statement was obtained by inferType and never re-checked as a standalone lemma"}]}
              for i, ph in enumerate(proofs)],
          "attrs": {"class": cl["class"], "exact?": cl["exact"], "inLib": cl["inLib"]}}
nodes.append(shared)
shared_edges = []
for d in cl["decls"]:
    r = roots[d]
    pid = {"alg": "lean-struct64", "value": r["stmtHash"]}
    text = stext[r["stmtHash"]]
    nodes.append({"id": f"stmt:{d}", "kind": "statement", "status": "accepted", "origin": {"by": "human:mathlib-authors"},
                  "reviews": [{"by": "human:mathlib-maintainers", "decision": "approved", "digest": pid, "note": "merged in Mathlib (illustration)"}],
                  "interface": {"language": "lean", "text": text, "text_complete": not text.endswith("…"), "identity": pid,
                                "source": {"decl": d}, "metrics": {"size_dag": r["statementSize"]}},
                  "implementations": [{"id": "mathlib", "language": "lean-proof", "ref": d, "source": {"decl": d}, "complete": True,
                                       "digest": {"alg": "lean-proof64", "value": r["proofHash"]},
                                       "metrics": {"size_dag": r["proofSizeDag"], "size_tree": r["proofSizeTree"]},
                                       "realises": [{"kind": "tool-trusted", "by": "tool:mathlib-olean", "scope": {"quantifier": "all"},
                                                     "detail": "imported from Mathlib's compiled .olean; not re-checked here"}]}]})
    for o in [o for o in occs if o["decl"] == d]:
        e = {"id": f"lifted_from:{shared['id']}->stmt:{d}[mathlib]", "from": shared["id"], "to": f"stmt:{d}", "relation": "lifted_from",
             "to_end": "implementation",
             "occurrences": [{"role": o["role"], "implementation": f"t{proofs.index(o['proofHash']) + 1}", "at": {"decl": d},
                              "attrs": {"candidate_id": o["id"], "head": o["headConst"], "term_path": "not exported by Rosette/Reuse.lean"}}],
             "evidence": [{"kind": "tool-trusted", "by": "tool:rosette.reuse", "run": "run:reuse", "scope": {"quantifier": "n/a"},
                           "inputs": [{"node": shared["id"], "end": "interface", "digest": sid},
                                      {"node": f"stmt:{d}", "end": "implementation", "implementation": "mathlib",
                                       "digest": {"alg": "lean-proof64", "value": r["proofHash"]}}],
                           "detail": "the sub-term's closed statement has this structural hash (Rosette.statementHash)"}]}
        shared_edges.append(e)
edges += shared_edges
verdicts = [
    {"node": L2["id"], "outcome": "review", "code": "LIFT-KERNEL-CHECKED", "flags": ["MACHINE-PROPOSED", "UNREVIEWED-LABELS"],
     "chain": [e["id"] for e in edges if L2["id"] in (e["from"], e["to"]) and root["id"] in (e["from"], e["to"])],
     "rests_on": ["kernel-checked", "tool-trusted"], "unreviewed": [L2["id"]], "stale": [],
     "detail": "the lemma and the proof that calls it are kernel-checked; whether it is worth keeping, and its English reading, await a person"},
    {"node": shared["id"], "outcome": "open", "code": "CANDIDATE-ONLY",
     "flags": [f"RECURS-IN-{len(cl['decls'])}-THEOREMS", f"{len(proofs)}-DISTINCT-PROOFS"],
     "chain": [e["id"] for e in shared_edges], "rests_on": ["tool-trusted"], "unreviewed": [shared["id"]], "stale": [],
     "detail": "enumerated only: no standalone lemma was created or kernel-checked"},
]
G = {"schema": "rosette.refinement-graph/2", "generated_at": "2026-11-09", "runs": runs, "nodes": nodes, "edges": edges, "verdicts": verdicts}
errs = graphlint.schema_errors(G) + graphlint.lint(G)
for e in errs:
    print("ERROR", e)
(HERE / "maths-example.graph.json").write_text(json.dumps(G, indent=1, ensure_ascii=False) + "\n")
print(f"maths-example.graph.json: {len(nodes)} nodes, {len(edges)} edges, {len(verdicts)} verdicts; {'valid' if not errs else 'INVALID'}")
print("  '√↑d ^ 2 = ↑d': 2 lemmas that print identically (statement sizes 55 and 70): 2 nodes, 1 `equivalent` edge with no evidence")
print(f"  recurring statement {KEY}: 1 node, {len(shared['implementations'])} implementations, {len(shared_edges)} lifted_from edges, "
      f"{len(occs)} occurrences in {len(cl['decls'])} theorems")
s = graphlint.what_if(G, L2["id"])
print(f"  if the statement of filtered_2 were edited: {len(s['edges'])} edges, {len(s['implementations'])} implementations, "
      f"{len(s['verdicts'])} verdicts and {len(s['labels'])} labels go stale")
for k in ("edges", "implementations", "verdicts", "labels"):
    for x in s[k]:
        print(f"    {k[:-1]}: {x}")
sys.exit(1 if errs else 0)
