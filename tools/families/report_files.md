- `out/families/ns/clusters.jsonl`: every family record (one per distinct member set over all channels), highest score first, with members, levels, skeleton, holes and their fillers per member, usage, lemma shapes and roles with theorem names, and every score component. `clusters_all.jsonl`: the same over all definitions, dead code included. `clusters_planted.jsonl`: ns with the planted controls mixed in.
- `out/families/ns/summary.json`, `summary_all.json`, `funnel.json`, `planted_result.json`; `out/families/{carleson,pfr}/clusters.jsonl`, `summary.json`, `funnel.json`.
- `out/families/<project>/raw/export.jsonl`: the typed trees from Lean (definition bodies, signatures, theorem statements). `features.pkl`: keys, profiles, usage.
- `tools/families/`: `Export.lean` (tree grammar in its header), `tree.py` (keys, anti-unification, roles, printer), `features.py`, `cluster.py`, `report.py`, `planted/`, `run.sh`.

Limits of the method, stated once:

- Anti-unification is first-order with a hole allowed in head position. A family whose members differ by an extra binder, an extra argument or an inserted structure field is not seen by body (this is why `MemClass` / `UniformClass` and `JetRate` / `FiniteJetRate` are missed by body).
- Structures are encoded as nested `∃ field, …`; inserting a field turns the rest of the structure into one compound hole.
- AU candidates are each definition's 60 nearest neighbours by a label-and-edge cosine, and the agglomeration is greedy, so a pair outside the neighbour lists is missed and cluster boundaries depend on order. A cluster is not grown beyond 250 distinct bodies.
- Erased arguments (instances, proofs, implicit types) are not compared. Two definitions that differ only there have equal keys. This is why 22 definitions "are" `Classical.choose`.
- Tags (coarse types) are part of the keys at L0 to L3 and ignored by AU.
- Non-structure inductive types (15 in ns) and instances are not clustered. 7 theorem statements over 2,500 nodes are not profiled.
- Usage counts come from the dead-code tool's term-dependency export, restricted to reachable declarations.
- Member bodies in the tables are the source bodies; skeletons are computed after unfolding project abbreviations, so a member may show `ProblemStatement.Space` where the skeleton shows `EuclideanSpace ℝ (Fin 3)`.
