# out/corpus/ns: declaration graph of openai/NavierStokesAndEuler

Corpus: `corpora/ns`, commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, Apache-2.0, Lean 4.34.0-rc2, Mathlib `85e3a25e`.
Exporter: `corpora/ns_export/Export.lean` (compiled stand-alone, reads the built environment); rerun with `corpora/ns_export/run.sh`.

| file | content |
|---|---|
| `decls.jsonl` | one line per project declaration (52,505), sorted by name |
| `axioms.json` | `collectAxioms` for the four headline theorems |
| `main_theorems.json` | headline theorems and what the README/formalization.yaml says they are |
| `stats.json` | shape statistics computed from `decls.jsonl` by `corpora/ns_export/stats.py` |
| `export_meta.json` | counts per class of constant (primary, folded auxiliaries, dropped) |
| `modules_arg.txt` | the 2,657 modules imported (all built modules except the two `ComparatorChallenges.*`) |
| `build.log`, `export.log` | raw logs |

## Fields of `decls.jsonl`

- `name` (full kernel name; private ones start `_private.<module>.0.`), `userName`, `module`, `line`, `endLine`
- `kind`: theorem / def / instance / structure / inductive (no axiom or opaque exists in the corpus).
  `instance` = definition whose result type is a class; `instanceAttr` says whether it is a registered global instance (only 25 of 1,517 are; the rest are local or private).
- `isPrivate`, `hasDocstring`, `isClass`, `typeIsProp`
- `statement`: `ppSignature` output, width 100, cut at 2,000 characters (`statementChars` is the uncut length, `statementTruncated`). For structures and inductives the constructor types are appended after `\n| `.
- `statementSize`: Expr node count of the type as a tree (plus constructor types). It explodes on shared terms (maximum 2.4e10); **use `statementDagSize`** (distinct subterms) for comparisons.
- `proofSize`: distinct subterms of the value (0 if none). `proofTreeSizeLog2`: floor log2 of the tree size. `auxProofSize`: same measure summed over the folded body auxiliaries (`_proof_N`, `match_N`, ...), `numAux` their number.
- `typeDeps`, `valueDeps`: project declarations used in the type (plus constructor types) and in the value (plus body auxiliaries). All targets are names in this file; no self edges; the union graph is acyclic.
- `numExtType`, `numExtValue`, `extTypeByRoot`, `extValueByRoot`: distinct non-project constants used, by library root.
- `statementHash`: 64-bit structural hash of the type, ignoring binder names, binder kinds and metadata, universe parameters by position.

## How auxiliaries are handled

95,123 constants live in project modules. 52,505 are exported. The rest:
- 25,185 body auxiliaries: folded into the parent's value side. A reference from another declaration to such an auxiliary (a shared `match_N`) is replaced by the auxiliary's own dependencies, not by an edge to the parent.
- 719 constructors: folded into the parent's type side.
- 16,285 derived (recursors, projections, `casesOn`, `noConfusion`, `eq_N`, `injEq`, ...): a reference becomes an edge to the parent.
- 412 notation/macro objects: dropped. 14 auxiliaries of Mathlib declarations realised in project modules: counted as external. 3 orphans (`_private.<module>.0._proof_N`): inlined.

Check: for `navier_stokes_breakdown_R3` the set reachable in this graph equals the raw constant closure computed without any folding (23,747 declarations, no difference either way); for `euler_breakdown_R3` it is 13,108 against 13,106, the two extra coming from unused auxiliaries of a reached declaration (`corpora/ns_export/RawClosure.lean`).
