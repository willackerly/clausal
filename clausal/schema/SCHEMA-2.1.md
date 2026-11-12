# Evidence-graph schema 2.1 (plan node W2)

`refinement-graph.v2.1.schema.json`, checked with `clausal/clausal/graphlint.py`. The prose for version 2 is `../../docs/SCHEMA.md`;
this note says only what 2.1 adds. The v2 schema file is kept as it was. Frozen before the code: `../trust/FREEZE.md` section 4.

**Additive.** Every graph valid under 2 is valid under 2.1: `schema` may be `rosette.refinement-graph/2` or `…/2.1`, and nothing
that was allowed is forbidden. Checked on the graph committed before this change (`git show 492bba6:clausal/out/graph.json`) and on
`maths-example.graph.json`.

| Added | Rule (schema or lint) |
|---|---|
| Agent prefix `org:` | an agent matches `^(human\|tool\|model\|org):.+`. The prefix is the signer's kind |
| Evidence kind `model-asserted` | `by` matches `^model:`; `act` required |
| Evidence kind `organisation-asserted` | `by` matches `^org:`; `act` required |
| Evidence fields `act`, `on_behalf_of` | `act` is one of authored, tested, reviewed, approved, vouched; `on_behalf_of` is an agent. It never changes `kind` |
| `binds` edges | may carry `human-asserted`, `model-asserted`, `organisation-asserted` (version 2: `human-asserted` only). Still never `tested` or `kernel-checked` |
| Clausebook entries as nodes | `piece:<id>`, kind `phrase`. The interface text is exactly what an attestation of the entry is an attestation of (the entry's text, the text of each Lean definition it names, the defaults it names), so `interface.identity` IS the digest a record names. `attrs`: `clausebook_entry`, `subject_kind` (piece, separation), `book`, `entry_kind`, `attestations` (every valid record: act, kind, by, on_behalf_of, at, scope, digest, evidence_kind), `void_attestations` |
| Each Lean definition an entry names | a `definition` node, with a `binds` edge from the entry; the edge carries one evidence entry per valid record by a person, a model or an organisation (act authored excepted) |
| Old glossary phrase nodes | `attrs.subject_kind: glossary-entry`, `attrs.attestations` |
| `verdict.unreviewed` | lists `piece:<id>` for every entry the verdict's reading uses that NO PERSON has reviewed or approved. A model's record does not take an entry off the list. Rule verdicts now carry it (version 2 wrote `[]`) |
| lint | a verdict with code `PROVED-*` and a non-empty `unreviewed` may not have outcome `pass`; an attestation stored on a piece node must be of the node's identity |
| lint (fix round 1) | on EVERY node, each entry of `attrs.attestations`: `by` is a signer id, `kind` is the kind of that id, `act` is in the table (a tool: authored or tested only), `evidence_kind`, when written, is that of the kind, `on_behalf_of` is null or an agent id. A verdict with code `PROVED-*` must list in `unreviewed` every entry it rests on (`attrs.reading.pieces` of its node, and the old-glossary phrases it is `composed_of`) whose node stores no well-formed `reviewed` or `approved` by a `human:` signer; an old-glossary entry is listed by its node id or by one of its `binds` edges. So `pass` with an empty list cannot be written over unreviewed entries |
| `verdict.rests_on` | may also list `model-asserted`, `organisation-asserted` |

**What changed in the emitted graph** (one `./run.sh --quick`, same tree, before and after): 940 to 1171 nodes (122 entry nodes, 109
definition nodes), 1474 to 1619 edges (145 `binds`), 120 verdicts. 0 verdict codes changed. 34 rule verdicts went from `pass` to
`review` (each is PROVED-FOR-ALL on entries no person has reviewed); no other outcome changed.

**Not added** (they belong to the assumption ledger and specialist terms, plan nodes W4 and W8): the evidence kinds
`specialist-asserted`, `externally-checked`, `assumed`; the node kind `assumption`; the relation `assumes`.

**Not done.** A reading is not tied to its entries by edges (`composed_of` from a Rule or scenario to `piece:<id>` would add about
1,200 edges); the link is `attrs.reading.pieces` on the Rule or scenario node and the verdict's `unreviewed` list. So
`graphlint --what-if piece:<id>` reaches the definitions an entry binds, and does not yet count the verdicts that rest on it.
Validity of a record is still decided by comparing digests when the stores are read (`vreport.load_attestations`), not by
`graphlint.staleness`: a change to a helper that an entry's Lean definition calls, and that the entry does not name in `defs:`,
leaves the digest unchanged (the hole the trust study names in its section 2). Unchanged by this work.

`python3 schema/selftest.py`: 27 invalid graphs must be rejected (ten of version 2; P11 to P19 of the freeze and P20 to P27 of
`trust/FREEZE-fix1.md`, each for the reason named), and four valid 2.1 shapes must be accepted.
