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
| 12 | The property-test generator draws, half the time, a message whose tag is the toy tag under a number already in the case | Without it almost no drawn message verifies and the property tests exercise rejected calls only. It is a fourth copy of the toy formula (Rust crate, Lean word, two Rust readings, generator) |
| 13 | `lean/lakefile.toml`, `Bdd.projectRoots`, three `Cargo.toml` files, `glossary.yaml`, `pieces.rs`, `typed.rs`, `evgen.py`, `evidence/src/main.rs` were edited for the fourth project | The same shared files the third project needed (DESIGN.md 21.6), plus the runner: a new literal type (`message`) needs a generator |

## What the book check says about the new book

- `in.intake`'s `when:` form names one of its three roles. A hole is `{word}` and the two state roles are two words each
  ("expected key", "last counter"), so they cannot be holes of a When form. The operation can be the subject of a Rule line
  and cannot be written as a scenario step. Recorded as a violation of check 1.
- `in.last` has the bare form `{c:sigcounter}` (the role "the last counter" read as its number), like `l.ledger`'s
  `{l:ledger}`. It joins the existing violation "pieces share the skeleton `{}`".

## What is not done

- **U4 has no sentence.** "No counter is accepted twice over any sequence of intakes" needs a frame over sequences of any
  length. None exists and none was added.
- **No signature is checked** (W9). Nobody has vouched; nobody has approved a word.
- **The external-proof link is a link and a hash.** Nothing fetches the file or compares the hash with anything (W8).
- **An opaque function cannot go through the pipeline.** A model with an axiom is not executable, so the search steps
  cannot evaluate it. T1.7 exercises the audit and the allow-list on a real translation, not a run.
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
