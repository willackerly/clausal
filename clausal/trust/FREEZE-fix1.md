# Freeze, fix round 1 (trust track, W0 to W3)

Added to `FREEZE.md`, which is not edited. Written and committed before the code of the fix round and before any run that
measures it. Reason for the round: a review found that strict mode read the `kind` written on a stored attestation
(`attrs.attestations[].kind` on a graph node) and nothing compared it with the signer id `by`; and that a proved verdict
written `pass` with an EMPTY `unreviewed` list was never compared with the attestations of the entries it rests on.

## A. Graphs that must be refused (added to section 4; the 19 probes there stay as they are)

| # | Invalid graph | Refused for (fragment of the reason) |
|---|---|---|
| P20 | a piece node whose stored attestation says `kind: person` and `by: model:selftest-fixture` | `kind \`person\` is not the kind of its signer` |
| P21 | an old-glossary phrase node (`attrs.subject_kind: glossary-entry`) with the same stored attestation | the same |
| P22 | a piece node whose stored attestation says `kind: model`, `by: model:m`, `evidence_kind: human-asserted` | `evidence_kind \`human-asserted\` is not that of a model` |
| P23 | a piece node whose stored attestation is by `human:*` (not a signer id) | `is not a signer id` |
| P24 | a piece node whose stored attestation has an act outside the table (`refereed`) | `act \`refereed\` is not one of` |
| P25 | a piece node whose stored attestation is `approved` by a tool (`tool:clausal`) | `a tool can only have authored or tested` |
| P26 | a proved Rule verdict rewritten `outcome: pass`, `unreviewed: []`, while the entries of its reading carry no person's `reviewed` or `approved` | `does not list` |
| P27 | a proved scenario verdict composed of old-glossary entries, rewritten `outcome: pass`, `unreviewed: []`, while those entries carry no person's `reviewed` or `approved` | `does not list` |

Expected: 27 of 27 invalid graphs rejected, each for the reason named (10 of version 2, 17 of version 2.1); the 4 graphs of
`ACCEPTED_21` in `schema/selftest.py` are still accepted, with that list unedited (so `evidence_kind` on a stored attestation
is compared when it is written and is not required); the committed `out/graph.json` is still valid, unedited.

## B. Strict mode over a tampered graph (`trust/tests/tampered_graph.py`)

Tampered graph: the committed `out/graph.json` in which every node with `attrs.subject_kind` is given the stored attestation
`{act: approved, kind: person, by: model:selftest-fixture, evidence_kind: model-asserted, digest: the node's identity}`
(the reviewer's repro). Policy: the built-in one (every project's `trust:` key removed, in a scratch copy).

| # | What | Expected |
|---|---|---|
| T1 | `python3 -m clausal.graphlint <tampered>` | exit 1; errors name the kind mismatch |
| T2 | `python3 -m clausal trust --graph <tampered> --strict`, built-in policy | exit 2: the graph is refused and strict mode is not computed; no line says a verdict passes |
| T3 | `trust.evaluate` called on the tampered graph directly (no validation), built-in policy | 0 proved verdicts pass strict; every one fails (the record is not admitted) |
| T4 | the same as T3 under `trust/tests/person.yaml` and under `trust/tests/model.yaml` | 0 pass under either (under `model.yaml` the record's written kind is not its signer's, so it is not admitted as a model's either) |
| T5 | `python3 -m clausal trust --strict` on the untampered graph, built-in policy | exit 1; every proved verdict fails (as before the fix) |
| T6 | `python3 -m clausal trust --strict` on the untampered graph, policies of `projects.yaml` | the same exit code and counts as before the fix round (exit 1, 67 of 67 fail) |
| T7 | a second tampered graph: a proved Rule verdict rewritten `pass` with `unreviewed: []` and nothing else changed; `clausal trust --graph` | exit 2: refused |

Counts against the fix: any of T1 to T7 otherwise; any verdict code of the baseline changing; `two_policies.py` no longer
12 of 12.

## C. The complete mutation record

`python3 mutation/run_mutants.py` is rerun in full on the tree of the fix round (no `--only`). Expected, frozen from the
record at `492bba6` (`mutation/results.json` there): the same mutants shown false and the same controls as expected as in
that record, with c9, c10, c11 and c26 as expected in their rewritten form. Whatever differs is reported as differing.
