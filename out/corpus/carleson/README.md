# Human ground-truth corpora: PFR and Carleson (2026-11-09)

Two human-written, human-blueprinted Lean projects, exported as declaration graphs for validating the
dominator-tree outline. The same files exist in `out/corpus/pfr/` and `out/corpus/carleson/`.

| | PFR | Carleson |
|---|---|---|
| repository, commit | teorth/pfr `1ef23c3c` | fpvandoorn/carleson `4dc72b29` |
| Lean | 4.36.0-rc2 | 4.36.0-rc1 |
| project modules loaded | 75 | 124 |
| project constants in the environment | 2,658 | 7,131 |
| auto-generated, folded into parents | 1,540 | 3,932 |
| declarations exported | 1,118 | 3,199 |
| theorems / instances / defs / structures / inductives / opaque | 978 / 53 / 75 / 8 / 2 / 2 | 2,675 / 71 / 426 / 26 / 1 / 0 |
| edges: used in type / used in value | 1,684 / 4,765 | 15,447 / 25,007 |
| blueprint nodes | 219 | 180 |
| blueprint nodes with a `\lean` tag | 213 | 179 |
| `\lean` names (distinct) | 254 | 249 |
| of which project declarations / Mathlib declarations / unresolved | 247 / 7 / 0 | 236 / 13 / 0 |
| blueprint `\uses` edges, statement / proof | 73 / 425 | 220 / 0 |
| theorems tagged / all theorems | 225 / 978 = 23.0% | 229 / 2,675 = 8.6% |
| same, outside the staging-library folders | 145 / 310 = 46.8% | 224 / 1,486 = 15.1% |
| non-theorems tagged | 22 / 140 | 7 / 524 |
| build wall time (after cache) | 62 s | 155 s |
| export wall time | about 20 s | about 21 s |
| pretty-printer failures, truncated statements | 0, 0 | 0, 0 |

"Staging-library folders" are `PFR/Mathlib`, `PFR/ForMathlib`, `PFR/Tactic`, `PFR/Examples` and
`Carleson/ToMathlib`: material meant for upstreaming that the blueprints do not try to cover.

Axioms: every headline theorem checked depends on `propext`, `Classical.choice`, `Quot.sound` only
(`axioms.json`). Carleson has three declarations that use `sorryAx` directly, all in
`Carleson/ToMathlib/RealInterpolation/LorentzInterpolation.lean`; none is reachable from the headline theorems.

Graph checks: no dangling edge, no self edge, no cycle (PFR). Reachable from PFR's headline theorems:
830 of 1,118 declarations, containing 232 of the 247 tagged ones. From `classical_carleson`: 2,347 of 3,199,
containing 221 of the 236 tagged ones.

## Files
- `decls.jsonl`: one declaration per line. `name` is the full internal name (unique; private names keep
  their `_private.…` prefix), `userName` the name as written. `kind` is `instance` for any registered
  instance, otherwise `constKind`. `statement` is the signature as Lean prints it. `statementSize` is the
  tree node count of the type, `statementDagSize` the count of distinct subterms. `proofSize` is the count
  of distinct subterms of the value (for a definition this is its body), `proofTreeSize` the tree count,
  `auxProofSize`/`numAux` the extra size and number of the declaration's own auxiliary constants.
  `typeDeps`/`valueDeps` are project declarations used in the statement / in the value; edges through
  auxiliaries are re-attached. `extTypeByRoot`/`extValueByRoot` count outside constants by package root.
  `directAxioms` lists axioms referenced directly. `statementHash` ignores binder names, binder kinds,
  metadata and universe-parameter names. `usesLeanMeta` marks tactic/metaprogram code.
- `all_names.jsonl`: every project constant, whether it was treated as auto-generated, and its parent.
- `modules.jsonl`: project modules and their project-internal imports.
- `axioms.json`: axioms of the headline theorems. `export_meta.json`: counts, timings, breakdown of
  auto-generated names by suffix.
- `blueprint.json`: one entry per blueprint node: `label`, `kind`, `title`, chapter/section, `lean`,
  `uses` (statement), `proofUses`, `leanok` flags, and `leanResolved` (each name: `exported`, `external`
  with its module, `project-auxiliary`, or `unresolved`). `blueprint_summary.json`: the counts above.

## Reproduce
`corpora/tools/run_pfr.sh` and `corpora/tools/run_carleson.sh` (after `lake exe cache get && lake build`
in the corpus). Exporter: `corpora/tools/ExportDecls.lean`; blueprint parser: `corpora/tools/parse_blueprint.py`.

## Known limits
- `to_additive`, `simps`, `ext` and `alias` outputs are kept as ordinary declarations.
- Three private names in PFR share a `userName` across modules (`ProbabilityTheory.iIndepFun.κ`,
  `.κ_equiv`, `.fintype_kappa`); none is blueprint-tagged.
- A use of a structure field, constructor or recursor is recorded as an edge to the structure.
- The Carleson blueprint has one unlabelled `remark` node and puts all `\uses` in statements.
- `PFRPalomar.Challenge` (six `sorry` restatements) is not loaded.
