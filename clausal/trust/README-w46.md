# The assumption ledger and trust test 1 (plan nodes W4 and W6)

Built from `docs/studies/2026-11-12/trust.md` sections 1c, 5 and 6. What was frozen before the code and the run:
`FREEZE-w46.md` (commit `fa3fd9c`), on top of W0's `test1/` (commit `09966fe`). This note says what there is, where it departs
from the study or the freeze, what the test measured and what it does not establish. `README.md` in this directory is about
W0 to W3 and is not edited.

**No person has signed anything.** The one record this work adds is a model's (`clausebook/local/intake.attest.json`).

## What there is

| Piece | Where | What it does |
|---|---|---|
| Ledger | `trust/assumptions.yaml`, `clausal/ledger.py` | An entry states an assumed fact, its class, the Lean axioms a proof may use because of it, whether what the word is bound to here is a stand-in, the words attached to it, its usage conditions (each a Rule id, or `unstated`), what is not covered, an optional external-proof link with a hash, a review date. `python3 -m clausal ledger` prints it |
| `assumes:` | a key of a Clausebook entry (operation, piece or idiom) | Names ledger entries. It is in the entry's text, so under its digest. `clausal gen`, `clausal book check` and `clausal report` stop if it names an entry the ledger does not hold, if `attached_to` and `assumes:` disagree, or if a usage condition names no Rule |
| Who vouches | `trust/assumptions.attest.json`, subject kind `assumption`, `clausal attest assumption:<id> --act vouched --as …` | A record of the entry's current digest. A person's or an organisation's `vouched` is a vouch; a model's or a tool's is not. Void when the entry changes, or after `review_by`. None exists: printed AWAITED |
| Usage conditions | `ledger.state`, `report.assumption_state` | Each stated condition is an ordinary Rule of a feature file. Its verdict is read from the run when the graph is built. Nothing is stored |
| Axiom allow-list | `vreport.lclean(links, name, allow)` | A theorem counts only if its axioms are the standard three plus the `lean_axioms` of the entries the sentence's words name. Anything else: rejected, as before |
| Flags | on the Rule verdict, in the graph and the block | `ASSUMES:`, `ASSUMPTION-AXIOM-USED:`, `ASSUMPTION-CONDITION-NOT-MET:`, `ASSUMPTION-CONDITION-UNSTATED:`, `ASSUMPTION-NOT-VOUCHED:` + id. No verdict code changes. A proved Rule on an open assumption is `review`, never `pass` |
| Graph | `report.ledger_nodes`, `schema/refinement-graph.v2.1.schema.json`, `clausal/graphlint.py` | Node kind `assumption` (identity = the digest a vouch names); `assumes` from the word's node, evidence kind `assumed`; `requires` to each condition's Rule; `attrs.reading.assumptions` on the Rule; `assumed` in `rests_on` |
| Block | `clausal/rules.py` (`ranked_rests`) | A rule that rests on an assumption prints `Rests on   heaviest first`: the assumption with its conditions and their verdicts, then the rest by tier. Other rules' blocks are unchanged |
| Strict mode | `clausal/trust.py` | `{subject: assumption, act: vouched, …}` and `{every_condition: <code>}` are evaluated; each unmet requirement names who is awaited |
| Fourth project | `sigintake/`, `clausebook/local/intake.yaml`, `lean/Intake/`, `features/intake.feature`, `trust/sigintake.yaml` | Trust test 1 |
| Controls | `trust/tests/test1_controls.py`, result in `trust/tests/test1_controls.result.json` | The seven controls of the study |

## The fixture

`sigintake/src/lib.rs`, 45 lines. State: (expected key, last counter). Message: (payload, counter, tag, hint). `verify` is a
toy with a body: the tag is three hex digits, one each from the key, the payload and the counter. `intake` accepts iff the tag
verifies under the expected key and the message's counter is above the last counter; then the last counter is the message's.

The state is handed over as two `&mut` values. That is the one two-part shape the pipeline reads (`Bdd.opMut2`), and it lets
"the expected key" and "the last counter" be the operation's two roles, so the frozen sentences are read with holes that
are typed like every other domain word's. `intake` never writes the key.

## Departures from the study or the freeze, each a judgement call

| # | What | Why |
|---|---|---|
| 1 | The project is `sigintake`; the feature file, the book and the Lean namespace say `intake` | The task names the project; the frozen ledger entry and policy name `Rule.intake.…` and `local/intake.yaml` |
| 2 | The Feature title was changed from the one committed in the freeze to `Intake` | A Rule id is made from the Feature title, not from the file name. With the first title the ids were `Rule.signed_message_intake_on_a_toy_verifier.…` and the frozen ledger entry named Rules that did not exist. No Rule line changed |
| 3 | `assumes:` is on the WORD (a Clausebook entry), not on a Rule line | The study's section 1c. A Rule rests on an assumption because it uses the word; a second way to say so would be a second place to forget it |
| 4 | Assumption records are in `trust/assumptions.attest.json`, not in `trust/<project>.attest.json` | The ledger is one file, not one per project; whether a project admits a vouch is its policy's business |
| 5 | The `assumes` edge leaves the word's node (`piece:<id>`), not its `definition` node | The pointer is in the entry, and an entry can name several definitions |
| 6 | `ASSUMPTION-NOT-VOUCHED` is computed from records by persons and organisations, in every policy | The graph does not depend on the policy (W3). What a project admits is evaluated afterwards, by `trust.py` |
| 7 | A scenario whose reading uses a word that says `assumes:` stops the report | Only Rule verdicts carry the flags; a scenario verdict would hide the assumption. No such scenario exists |
| 8 | Refusal R12 of W1 (`subject.kind: assumption`: reserved) is now tested with `specialist-term`; the W3 self-test's "cannot be evaluated" case likewise | W4 builds the kind that was reserved |
| 9 | Two violations of the registration lint are recorded as known debt in `clausebook/check.expected.json` | See "What the book check says", below |
| 10 | T1.1 and T1.2 are run with `./run.sh --quick --no-unit` | The crate's own unit tests fail on both mutants and would stop the run at step 1, before any sentence is looked at |
| 11 | T1.7 is run at reduced scope | Frozen as such. `./run.sh` cannot finish on a model with an axiom in it |
| 17 | (fix round) T1.7 is counted NOT PASSED, and the script passes it only on a theorem of U1 as generated | The freeze asks for "a Lean file stating U1 (SM-2) for the variant and proving it" and W0 for "PROVED with the flag once the axiom is listed". The first report counted a theorem of a hand-written statement weaker than U1, whose type check compared it with itself. U1 as generated has no proof of the variant |
| 18 | (fix round) The block of a rule that rests on an assumption gained a row `Outcome`, a clause on the proof rung and on `STRONGEST HELD`, a note in the `assuming` slot and a mark on a usage condition that is the rule itself; the project table counts the proved rules that are proved given an assumption | A reviewer read the block as a non-expert and found lines that say "fully verified". The frozen content of the assumption item (section 4 of the freeze) is all still printed; lines were added, none removed. Blocks of rules on no assumption are unchanged |
| 12 | The property-test generator draws, half the time, a message whose tag is the toy tag under a number already in the case | Without it almost no drawn message verifies and the property tests exercise rejected calls only. It is a fourth copy of the toy formula (Rust crate, Lean word, two Rust readings, generator) |
| 13 | `lean/lakefile.toml`, `Bdd.projectRoots`, three `Cargo.toml` files, `glossary.yaml`, `pieces.rs`, `typed.rs`, `evgen.py`, `evidence/src/main.rs` were edited for the fourth project | The same shared files the third project needed (DESIGN.md 21.6), plus the runner: a new literal type (`message`) needs a generator |
| 14 | `lean/Intake/Lemmas/Verify.lean` (a step lemma for the toy `verify`) was added to `audit_imports` AFTER control T1.2 had been run once and had not passed | See "Measured": the first round found the counterexample and could not confirm it in the kernel. Without the lemma no false rule about `intake` can be refuted in the kernel, since `intake` calls `verify`. It changes whether a generated script succeeds, never a statement |
| 15 | `counter/check_expected.py` matches the counter's own nodes instead of any node id containing "counter" | Three of the fourth project's Rule ids contain the word (`accept_only_if_counter_above`, `counter_set`, `counter_set_frozen_wording`) and were reported as verdicts "that name the counter". `counter/expected.json` is unchanged |
| 16 | The self-test's scratch copies of `clausebook/` leave out `*.attest.json` | Two W1 checks count the records of a store they fill themselves; the tree now holds one record of its own (the model's, on `in.verifies`) |

## What the book check says about the new book

- `in.intake`'s `when:` form names one of its three roles. A hole is `{word}` and the two state roles are two words each
  ("expected key", "last counter"), so they cannot be holes of a When form. The operation can be the subject of a Rule line
  and cannot be written as a scenario step. Recorded as a violation of check 1.
- `in.last` has the bare form `{c:sigcounter}` (the role "the last counter" read as its number), like `l.ledger`'s
  `{l:ledger}`. It joins the existing violation "pieces share the skeleton `{}`".

## Measured (commands in the last section; the one full `./run.sh` and the controls are on the tree of this commit)

- **Sayable with today's pieces: 7 of 7**, with the local book as first written. SM-1, 2, 3, 5, 8 and SM-10 compile as frozen. SM-9 as
  frozen ("For a successful intake, …") is refused, `UNBOUND` / `RETIRED-FORM`, as predicted from the book; with the one word
  replaced by the live form ("accepted") it compiles. No core piece was added. Usage conditions that compile: 3 of 3 stated
  (U1, U2, U3); U4 is unstated. The Feature title had to be changed for the ids (departure 2); no Rule line was.
- **Verdicts.** SM-1, 2, 3, 5, 8, 9 (live wording) and 10: PROVED-FOR-ALL, each by a hand-written proof of its generated
  obligation (`lean/Wallet/RuleProofs/intake/`, standard axioms only), with the generated bounded check holding for every
  input (no size bound) and 10,000 property-test cases each. Every one is outcome `review`, none `pass`.
- **The whole run.** `./run.sh`: exit 0. 0 of the baseline's 112 verdict codes differ; 10 verdicts are new (8 Rules, 2
  functions). Graph: 1171 to 1195 nodes, 1619 to 1640 edges, 120 to 130 verdict records against the tree before this step (`2e72b55`); the wave's baseline (`492bba6`) had 940 nodes and 1474 edges. One `assumption` node, one `assumes` edge, three `requires` edges. 13 bounded-check rungs of the
  baseline answered differently (all "no answer in time" to "verified").
- **The seven controls: 6 of 7 passed; T1.7 did NOT pass as frozen.** (The first report of this step said 7 of 7. That
  count is withdrawn: see T1.7 below.) In the first round, on the tree of commit `ac2dfbe`, **T1.2 did not pass** either: the
  mutant that takes the key from the message was shown false on the Lean model and on the compiled Rust (`expected key 0,
  last counter 0, message 1/1/273/1`), but the generated refutation script could not step through `verify`, so the verdict
  was COUNTEREXAMPLE where the freeze asks for REFUTED. After departure 14 it is REFUTED. Every round is in
  `tests/test1_controls.result.json`.
- **T1.1** (verify step deleted): U1 and U2 REFUTED in the kernel at `expected key 0, last counter 0, message 1/1/273/0`,
  reproduced on the compiled Rust; both rules that use `in.verifies` flagged `ASSUMPTION-CONDITION-NOT-MET`; the assumption
  item reads "0 of 4 proved in this run, 3 NOT PROVED, 1 cannot be stated" where the unmutated run reads "3 of 4 proved in
  this run, 1 cannot be stated". (U3 is TESTED-ONLY there, not refuted: its proof no longer compiles.)
- **T1.7** (reduced scope): **NOT PASSED.** The variant translates with `axiom sigverify.verify` in a `noncomputable
  section`. The control asks for a theorem of U1 for the variant. U1 as generated (the obligation of SM-2, with the word
  rebound to the axiom's answer) says that every call answers and that an accepted one verifies. **It has no proof of the
  variant, with or without the axiom on the allow-list**: a kernel-checked theorem (`T17.needs`) shows that it implies the
  external verifier returns an answer at every input, and the model's axiom says nothing of the kind. So the outcome W0
  expected ("PROVED with the flag once the axiom is listed") was not obtained. To make U1 provable of an opaque function
  a second fact would have to be assumed (the function returns), and no ledger entry states one.
  What the control does show, on a statement that is NOT U1: for a hand-written, weaker statement (only the calls that
  answer; its type check compares the theorem with the statement the script itself wrote), the audit reports the axiom
  `sigintake.sigverify.verify`; with the ledger as frozen the theorem does not count (non-standard axioms); with the axiom
  listed it counts and the flag computation returns `ASSUMPTION-AXIOM-USED`; with another axiom listed it does not count.
  That is evidence that `lclean` admits a listed axiom and no other. It is not a verdict on a rule. The usage conditions
  were not evaluated on the variant, so the other flags listed in the result say nothing about it. `./run.sh` on the
  variant stops at step 4 (`Intake/Pieces.lean`: "failed to compile definition … depends on 'sigintake.intake', which is
  'noncomputable'").
- **The model record** is in no count labelled signed: every sigintake reading has "0 signed"; `in.verifies` is listed
  under `model-asserted; not a person's review`; every proved rule that uses it lists it as unreviewed.
- **Self-tests.** `python3 -m clausal.selftest`: 100 of 100, among them L1 to L12 (14 ledgers refused), the vouch, the flags,
  the allow-list, strict mode over a made-up graph, the block, and (fix round) the lines of the block that say the proof
  does not cover the assumption. `python3 schema/selftest.py`: 33 of 33 invalid graphs
  rejected, 6 of 6 valid ones accepted. `trust/tests/two_policies.py`: 12 of 12 (74 proved verdicts);
  `trust/tests/tampered_graph.py`: 9 of 9.

## What is not done

- **U4 has no sentence.** "No counter is accepted twice over any sequence of intakes" needs a frame over sequences of any
  length. None exists and none was added.
- **No signature is checked** (W9). Nobody has vouched; nobody has approved a word.
- **The external-proof link is a link and a hash.** Nothing fetches the file or compares the hash with anything (W8).
- **An opaque function cannot go through the pipeline.** A model with an axiom is not executable, so the search steps
  cannot evaluate it. T1.7 exercises the audit and the allow-list on a real translation, not a run, and on a statement
  weaker than U1.
- **No rule has been PROVED through a listed axiom.** The allow-list path (`lean_axioms`, the flag `ASSUMPTION-AXIOM-USED`,
  the sentence "THE PROOF USES THE AXIOM …") has run in the self-test and in T1.7 on a hand-written statement only. No
  entry of the ledger lists an axiom and no verdict in `out/graph.json` carries the flag.
- **Only the block of a rule that rests on an assumption says so in the places listed under departure 18.** The rules
  table of the report, the per-rule heading and the SARIF-style outcome of other rules were not changed; the row
  `Outcome` is not printed for a rule that rests on no assumption, though most of those are `review` too (unreviewed
  pieces).
- **The reader test of W5 is not run**, and the "three heaviest of n" fold is not built: the block prints every item, ordered.
- **Scenarios** that rest on an assumption are refused, not reported.
- **`graphlint --what-if assumption:<id>`** reaches the `requires` and `assumes` edges; verdicts are tied to an assumption by
  `attrs.reading.assumptions`, not by an edge, so it does not count them.
- **The mutation record was not rerun.** `projects.yaml` and the ledger are under the digest it is stamped with, so the
  report says the record is out of date. No mutant of `sigintake` is in `mutation/run_mutants.py`; the two of this test are in
  `trust/tests/test1_controls.py`.
- `docs/SCHEMA.md` still describes version 2 only.

## What test 1 does NOT establish

- **The verifier is a toy.** `sigintake::verify` is a formula anyone can compute. The proofs of SM-2, SM-3 and SM-5 are about
  that formula and the control flow around it. Nothing is shown about a signature scheme, a library, or unforgeability, and
  the ledger entry is marked STAND-IN for that reason.
- **"A nonce is never reused" is not stated.** SM-8 and SM-9 say what one call does to the counter; SM-10 says the same
  message twice in a row is rejected the second time. None of them says that no counter is accepted twice over an arbitrary
  sequence of calls. That is U4, printed CANNOT BE STATED on every rule that uses the word.
- **That the expected key is the right key**, and that a real library's verify is the scheme's verify, are listed under
  `not_covered` and checked by nothing.
- **Whether U1 to U3 are the right usage conditions, or all of them**, is the judgement of whoever vouches. Nobody has.
- **One model's reading of one word** is on record. It is not a review by a person and is in no count labelled signed.

## Commands

    python3 -m clausal ledger                       # the entries, the words on them, who has vouched
    python3 -m clausal attest assumption:<id> --act vouched --as <human:|org:>ID --scope "…"
    python3 -m clausal attest check                 # every store, the ledger's included
    python3 -m clausal trust --strict               # strict mode from out/graph.json and the policies
    python3 -m clausal rules | less                 # the blocks; a rule on an assumption prints it first
    python3 -m clausal.selftest                     # L1 to L12, the vouch, the flags, the allow-list, strict mode, the block
    python3 schema/selftest.py                      # P1 to P33 rejected; six valid 2.1 shapes accepted
    python3 trust/tests/test1_controls.py --work <dir outside the tree>      # the seven controls (two quick runs and more)
    python3 trust/tests/test1_controls.py --work <dir> --collect             # writes trust/tests/test1_controls.result.json
