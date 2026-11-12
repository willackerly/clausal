# Freeze for W4 (assumption ledger) and W6 (trust test 1)

Added to `FREEZE.md` and `FREEZE-fix1.md`, which are not edited. Committed before any code of W4 was written and before the
pipeline (`clausal gen` included) was run on any sentence of test 1. The seven sentences, the ledger entry, the policy and the
seven controls were frozen by W0 (`test1/`, commit `09966fe`); this file adds only what W0 left open. Nothing here is signed
by a person.

## 1. The fixture and its names

- The task names the fourth project `sigintake` (W0 and the study say `intake`). Project and crate: `sigintake`. The feature
  file is `features/intake.feature` and the local book `clausebook/local/intake.yaml`, so that the rule ids the frozen
  ledger entry names (`Rule.intake.…`) and the book the frozen policy names (`local/intake.yaml`) are the ones that exist.
- The policy `trust/sigintake.yaml` is `test1/intake.policy.yaml` with the line `project: intake` changed to
  `project: sigintake` and a different header comment. Nothing else.
- The ledger `trust/assumptions.yaml` holds the entry of `test1/assumptions.yaml`, unchanged.
- The crate `sigintake/src/lib.rs` is committed with this file, before anything was translated for the pipeline. (It was
  put through Charon and Aeneas once, in a scratch directory, to see that it translates: it does, with no axiom.) The state
  is the pair (expected key, last counter), handed over as two `&mut` values, the one two-part shape the pipeline reads.
- The local book is committed with this file as first written, NOT compiled. It is the project's own file and is not frozen:
  every later change to it is listed in the report of the step.

## 2. Sentences and expected verdicts

`features/intake.feature`, committed with this file. Rule ids and expectations:

| # | id | Sentence | Expected |
|---|---|---|---|
| SM-1 | `always_answers` | as frozen | PROVED-FOR-ALL |
| SM-2 | `accept_only_if_verified` (U1) | as frozen | PROVED-FOR-ALL |
| SM-3 | `unverified_rejected_unchanged` (U2) | as frozen | PROVED-FOR-ALL |
| SM-5 | `unsigned_part_ignored` (U3) | as frozen | PROVED-FOR-ALL |
| SM-8 | `accept_only_if_counter_above` | as frozen | PROVED-FOR-ALL |
| SM-9 | `counter_set_frozen_wording` | as frozen ("For a successful intake, …") | UNBOUND, code RETIRED-FORM |
| SM-9 | `counter_set` | the same with "successful" replaced by "accepted" | PROVED-FOR-ALL |
| SM-10 | `same_message_again_rejected` | W0's wording | PROVED-FOR-ALL |

- SM-9: `core.yaml` records "successful {op}" as retired for "accepted {op}" (entry `successful`, plan node Q4). That is read
  from the book, not from a compile. So the frozen line is expected to be refused and to be told the live form, and the line
  with that one word replaced is the canonical sentence. If the frozen line compiles after all, that is reported as a
  prediction that failed.
- A sentence that does not compile is reported as not sayable with the missing piece named. It is not reworded, no core piece
  is added, and its expectation stays as written here: the run is then not green, and that is the result.
- A sentence that compiles and is not proved stays expected PROVED-FOR-ALL and is reported as not shown.
- Counts against (W0): fewer than 3 of the 4 usage conditions compile (U4 is frozen as unstated, so all of U1 to U3 must).

## 3. The ledger (W4)

**File.** `trust/assumptions.yaml`, `assumptions:` a list. An entry has exactly the keys `id`, `statement`, `class`,
`lean_axioms`, `stand_in`, `attached_to`, `usage_conditions`, `not_covered`, `external_proof`, `review_by`.

**Entries that must be refused** (the load fails; `clausal gen`, `clausal book check` and `clausal report` stop):

| # | Entry or tree | Reason expected (fragment) |
|---|---|---|
| L1 | a key outside the list (`status: settled`) | `unknown key` |
| L2 | a missing key (`statement`) | `missing key` |
| L3 | `class: fact` | `class` |
| L4 | a usage condition with neither a rule nor `unstated` (`{id: U9, rule: null}`) | `unstated` |
| L5 | a usage condition naming a rule no feature file has | `is not a Rule` |
| L6 | a stored verdict on a condition (`{id: U1, rule: R, verdict: PROVED-FOR-ALL}`) | `unknown key` |
| L7 | a Clausebook entry with `assumes: [A.nope]`, an id the ledger does not hold | `the ledger does not hold` |
| L8 | a ledger entry whose `attached_to` names an entry that does not say `assumes:` it (or the reverse) | `attached_to` |
| L9 | `external_proof` with a missing field or a `sha256` that is not 64 hex digits | `external_proof` |
| L10 | two entries with one id | `twice` |
| L11 | `lean_axioms` naming one of the standard three (`propext`) | `standard` |
| L12 | `review_by` that is not a date | `review_by` |

**Digest of an entry** (what a vouch is a vouch OF; study section 2): sha256 of the statement, the class, the axiom list,
`stand_in`, the conditions (id, rule, `unstated`, and for a stated condition the `lean_sha256` of its sentence in
`clausebook/terms.lock.json`), `not_covered`, the external proof's fields and `review_by`. Rewording the statement, adding or
dropping a condition, or a condition's sentence compiling to another term, voids every record about the entry.

**Records.** Subject kind `assumption` is built by W4 (it was reserved in W1: refusal R12 is now tested with
`specialist-term`, which stays reserved). Store: `trust/assumptions.attest.json`. Subject: `{kind: assumption,
book: trust/assumptions.yaml, id, digest: {alg: sha256-text, …}}`. A record whose act is `vouched` is the vouch; a tool cannot
vouch (existing rule). A vouch dated after `review_by`, or read after `review_by` has passed, is void.

**Nothing is stored about a condition's verdict.** It is read from the verdicts of the run when the graph is built.

**The axiom allow-list.** A theorem counts only if its axioms are among the standard three plus the `lean_axioms` of the
ledger entries that the pieces of the sentence it proves name with `assumes:`. Any other axiom: the proof is rejected, as
before. A proof that uses a listed axiom keeps its code and is flagged.

**Flags on a Rule verdict** (no verdict code changes; the list is `flags` in the graph and on the rule's block):

| Flag | When |
|---|---|
| `ASSUMES:<id>` | a piece of the reading names the entry |
| `ASSUMPTION-AXIOM-USED:<id>` | the proof uses an axiom of the entry's `lean_axioms` |
| `ASSUMPTION-CONDITION-NOT-MET:<id>` | a stated usage condition of the entry has a verdict other than PROVED-FOR-ALL in this run |
| `ASSUMPTION-CONDITION-UNSTATED:<id>` | a usage condition of the entry has no rule |
| `ASSUMPTION-NOT-VOUCHED:<id>` | no valid record of act `vouched` by a person or an organisation exists for the entry's current digest |

A proved verdict that rests on an assumption has headline "PROVED FOR ALL INPUTS, GIVEN 1 ASSUMPTION" and `assumed` among
`rests_on`. Like `unreviewed`, the last flag is about persons and organisations and is the same under every policy; what a
project's strict mode admits is the policy's business.

**A scenario** whose reading uses a word that says `assumes:` is not built: `clausal report` stops with an error naming it
(fail closed) rather than print a scenario verdict that hides the assumption.

**Strict mode.** `{subject: assumption, act: vouched, …}` is evaluated like any requirement, over the assumption entries a
proved verdict rests on. `{every_condition: <code>}` is met for a verdict iff every usage condition of every entry it rests
on has that code; an unstated condition does not have it. So under the frozen policy `assumption.usage` is unmet for every
rule that uses `in.verifies` for as long as U4 cannot be stated. `specialist-term` still fails closed if demanded. For
each unmet requirement the output names who is awaited: the roots the requirement allows, with their signer or "nobody named".

**Schema 2.1, added** (additive: the committed graph validates unchanged): node kind `assumption`; relation `assumes`
(phrase to assumption) and `requires` from an assumption to a rule's group node; evidence kind `assumed` (`artifact`, the
ledger id, required; allowed on `assumes` edges only); `assumed` in `rests_on`. Invalid graphs that must be rejected (added
to P1 to P27):

| # | Invalid graph | Fragment |
|---|---|---|
| P28 | `assumed` evidence on a `binds` edge | schema refusal of the kind on that relation |
| P29 | `assumed` evidence with no `artifact` | `'artifact' is a required property` |
| P30 | an `assumes` edge from a piece to a definition node | `may not go from` |
| P31 | a proved Rule verdict whose reading lists an assumption and whose `rests_on` has no `assumed` | `does not list \`assumed\`` |
| P32 | a Rule node whose reading uses a piece with an `assumes` edge and does not list that assumption | `does not list the assumption` |
| P33 | an assumption node that stores a usage condition with a verdict written on it | `stores a verdict` |

## 4. The "rests on" block of a rule that rests on an assumption

Rendered from `out/graph.json` alone, like the rest of the block. Items are numbered and ordered by tier, then by the order
assumed, meaning, translation, compilation, proof:

- tier 0, open: an assumption with no vouch (the flag above), or with a condition not met or unstated; meaning with a piece
  no person has reviewed;
- tier 1, nothing in this run checks it: an assumption that is vouched with every condition proved; a translation with no
  cross-check in this run; the compiler;
- tier 2: the rest.

An assumption item prints: the statement, the id, STAND-IN if so, the word it hangs on, who vouches or AWAITED, each usage
condition with its id, its verdict code in this run (or CANNOT BE STATED with the reason) and its sentence, the count
"n of m proved here", `not_covered`, the external proof link with its hash and "not checked here" or "none", `review_by`,
and how many other Rule statements rest on it. The blocks of rules that rest on no assumption are unchanged.

This is the part of W5 the task asks for. The reader test of W5 is not run and the three-heaviest fold is not built.

## 5. The seven controls, as they will be run

`trust/tests/test1_controls.py`, each in a scratch copy made by `mutation/workcopy.sh`; result in
`trust/tests/test1_controls.result.json`. "Flagged" means the flag `ASSUMPTION-CONDITION-NOT-MET:A.sig.unforgeable` on the
verdict in `out/graph.json` and the changed condition line in the rule's block.

| # | Change | Counts as passed iff |
|---|---|---|
| T1.1 | `intake` with the verify step deleted (it accepts on the counter alone) | one `./run.sh --quick`: U1 (`accept_only_if_verified`) is REFUTED; every Rule verdict whose reading uses `in.verifies` carries the flag; the assumption item of their blocks no longer reads as in the unmutated run |
| T1.2 | `intake` verifies under a key made from the message's hint instead of the expected key | one `./run.sh --quick`: `accept_only_if_verified` is REFUTED |
| T1.3 | the body of `In.verifies` in `lean/Intake/Pieces.lean` is edited (16 to 8 in one place) | `clausal attest check` lists the model record as VOID and no valid record of `in.verifies` remains |
| T1.4 | a record `signer: {kind: person, id: model:claude-fable-5-2}` on `in.verifies`, appended to the store | `clausal attest check` exits 1 and the reason names the kind and the id; the entry is still unreviewed |
| T1.5 | `python3 -m clausal trust --strict` on the unmutated run | exit 1; every proved sigintake verdict fails; the output names the owner (`meaning.core` or `meaning.domain`: approval by root `owner`) and the specialist (`assumption.vouch`: root `crypto`, nobody named) as awaited |
| T1.6 | the entry `A.sig.unforgeable` is deleted from `trust/assumptions.yaml` | `clausal gen` exits non-zero naming `in.verifies` and the id; `./run.sh --quick` exits non-zero before step 4 |
| T1.7 | `verify` moved to a second crate that is not translated, so Aeneas emits `axiom sigintake.sigverify.verify`; the word bound to that axiom's answer | see below |

T1.7 is run at reduced scope and is reported as such. A model with an axiom in it cannot be evaluated by the search steps
(`docs/studies/2026-11-12/packs.md` section 2b says so), so `./run.sh` cannot finish on the variant. What is run: the real
translation of the variant crate; a Lean file stating U1 (SM-2) for the variant and proving it; the project's own audit
(`Bdd.Audit`) asked for that theorem's axioms; `vreport.lclean` and the flag computation asked whether the proof counts,
with the ledger as frozen (`lean_axioms: []`) and with the axiom listed. Passed iff the audit reports the axiom, the proof
does not count with `lean_axioms: []` (reason: non-standard axioms), and it counts and is flagged
`ASSUMPTION-AXIOM-USED:A.sig.unforgeable` once listed. Whether `./run.sh` stops on the variant, and where, is reported.

Also checked by the script: the model record is in no count labelled signed or sign-off (the pieces of every sigintake Rule
are "0 signed" in the graph and the blocks; `in.verifies` is listed under `model-asserted`).

## 6. What test 1 cannot establish, stated before it is run

- The verifier is a toy. A proof of U1 to U3 is about `sigintake::verify`, which anyone can compute. Nothing is shown about
  any signature scheme, any library, or unforgeability.
- U4 (no counter accepted twice over any sequence of intakes) has no frame. SM-10 is about two calls with the same input
  and is not U4.
- No person has approved a word or vouched for the assumption; the model record is one model's reading of one entry.
