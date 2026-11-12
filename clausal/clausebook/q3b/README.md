# Q3b: the 21 violations of the book check, settled as far as they can be without the owner

Plan node Q3b. `FREEZE.md` fixed the items, the tests and the expected count before the lint was changed and before
the recorded runs. Run commands from `clausal/`. Nothing was signed.

**Count: 21 before, 16 after** (`python3 -m clausal book check`). Five are settled, each for a reason the check now
states and tests. Five more have a recorded proposal and wait for a signature (its separating input is run by
`book check --separate`, by `./run.sh` and before a signature is taken, not by the plain check). Eleven need a
decision about wording or about the rule itself.

| Violations at `492bba6` | Now | Why |
|---|---|---|
| 4, shared across systems | 0 | A sentence is compiled against the books of its own project. No project lists the wallet's and the ledger's local books together |
| 1, seven bare-hole forms (21 pairs) | 0 | The seven are registered at seven different types, and the parser tries a form only where exactly its type is wanted |
| 4 shared skeletons, 1 head collision (7 pairs) | 5 | Unchanged in count. Each pair now has a proposed separation in the book, with a separating input. Unsigned |
| 6 (check 1), 4 (check 3a), 1 (check 3b) | 11 | Not touched: each needs a wording or a rule decision |

## 1. Cross-system: compilation is project-scoped

**What was the case.** `projects.yaml` declared which books a project lists, and the pipeline stopped if a compiled
sentence used an entry of another project's book. But a Rule line was still tried in every system of every loaded
book: the `books` argument of `Compiler.rule` only chose which operations an UNBOUND message listed.

**What is built.**

- `Vocabulary.scoped(books)` (`clausal/vocab.py`): the Clausebook made of exactly the listed books, loaded by the same
  loader from the same texts. `Compiler.rule(rule, hint, books)` and `Compiler.scenario(sc, books)` compile against it.
  The pipeline, `clausal compile`, `clausal duplicates` and the term lock pass the books of the file's project.
- With no project named (`books=None`) a line is read against every loaded book, as before. That is how `controls/`,
  the self-test and a file that no project lists are read.
- The lint asks check 4 per project (`book.scopes_of`, `book.collisions`): two forms are compared only if some
  project lists the books of both. What is shared only between entries no project loads together is printed under
  "not counted". If a loaded book is listed by no project, every book is compared, as before.

**Why the four disappear.** The wallet project lists `core.yaml`, `ledger.yaml` (the pack: no operation) and
`local/wallet.yaml`; the ledger project lists `core.yaml`, `ledger.yaml` and `local/ledger.yaml`. `l.apply`,
`l.accepted` and `l.maximum` are in `local/ledger.yaml`; `w.transfer`, `w.succeeds` and `w.maximum` in
`local/wallet.yaml`. No project loads both files.

**The refusal still fires inside one project** (self-test, "Q3b (1)"; `python3 clausebook/q3b/check.py`):

| Line, no scenario beneath it | wallet | ledger | one project listing both local books (in memory) | wallet, with "transfer" also a noun of `w.deposit` (in memory) | no project named |
|---|---|---|---|---|---|
| A transfer is always accepted | one statement, `w.transfer` | one statement, `l.apply` | AMBIGUOUS | AMBIGUOUS | AMBIGUOUS |
| For a transfer, it is accepted | one statement, `w.transfer` | one statement, `l.apply` | AMBIGUOUS | AMBIGUOUS | AMBIGUOUS |

Given a project that lists both local books, the lint reports the four violations again; so it does when no project
is declared. A noun that two operations of one project carry is reported as a shared skeleton.

**Limits.**

- A sentence in no declared project is still read in every system. `controls/` is such a directory, and so is a
  feature file given to `clausal compile` that no project lists. "A transfer ..." with no scenario is AMBIGUOUS there.
- `clausal compose` and `clausal separate` were not changed: they take a system, not a project, and load every book.
  Today each system's operations are in one project, so the readings are the same; the code does not enforce that.
- The Rust cucumber run (`wallet-bdd`) picks the tree of a shared Then form by the system of the scenario's When, as
  before. It was not changed.
- Two refusal messages changed, with the same status and code (UNBOUND): `Rule.wallet.interest` ("A deposit earns
  interest") and `Rule.counter_rules.bump_resets` ("A bump resets the counter") are refused for the claim ("earns
  interest", "resets the counter"), where each was refused as no rule clause, with a list of operations. Each line was
  tried in three systems before and the longest message won; its own system's refusal was always about the claim.
  The self-test that checked the list of operations now uses a subject that is an operation of no project.

## 2. Pairs that need a separating pair: seven proposals, in the book, unsigned

They are entries under `separations:` of `clausebook/local/ledger.yaml`. They cannot stand in core: core may name no
fixture noun (`book core`), and their sentences are about operations. A separation is now read in one project, one
that lists the book it is written in (`book.separation_state`).

Each pair is two Rule lines about the same operation, so that one input can be given to both. Where both pieces are
conditions the two lines are the same words with the two holes exchanged, which is the confusion the pair is about.

| id | The sentence that holds at the input | Input (state; argument) | Grid | Only first / only second / both / neither |
|---|---|---|---|---|
| `sep.more_than.exceeds` | `more_than` | ledger `[2, 1]`; batch `[0->1:1]` | 297 | 72 / 18 / 207 / 0 |
| `sep.not_more_than.at_most_value` | `not_more_than` | ledger `[1, 0]`; batch `[0->1:1, 0->1:1]` | 297 | 18 / 72 / 199 / 8 |
| `sep.not_more_than.result_at_most` | `result_at_most` | ledger `[1, 0]`; batch `[0->1:1]` | 297 | 0 / 80 / 217 / 0 |
| `sep.at_most_value.result_at_most` | `result_at_most` | ledger `[1, 0]`; batch `[0->1:1]` | 297 | 0 / 26 / 271 / 0 |
| `sep.is.result_is` | `is` | ledger `[]`; batch `[0->1:1]` | 297 | 221 / 3 / 69 / 4 |
| `sep.within.covers` | `within` | ledger `[]`; batch `[0->1:1, 1->0:1]` | 297 | 203 / 0 / 94 / 0 |
| `sep.same_answer.same_answer_if` | `same_answer_if` | ledger `[1, 0]`, transfer `0->1:1`; second call: ledger `[1, 0]`, transfer `0->1:2` | 4356 | 0 / 5 / 4351 / 0 |

"Holds" means: the sentence, read as a statement about one call on that input, is true there and the other is false.
The sentences are in the book and in `FREEZE.md`.

**What "PROPOSED" means in the lint.** A separation that (a) separates: both lines compile in its project, each is
read with its own piece and not the other, each is written with the shared skeleton; (b) records a `witness:` whose
two term hashes are the hashes of what the two lines compile to today; and (c) has no sign-off. It lifts nothing: the
violation of its pair stays and names it. It is not reported as `4 separation not in force`. A separation with no
sign-off and no `witness:`, or whose recorded term is stale, is reported as before.

**The machine check, in two parts, and what each says (fix round).**

- Every `book check`: (a) and (b) above. No Lean. It does NOT run the recorded input: a `witness:` at which both
  sentences hold, with current hashes, passes it. So it no longer prints "machine-checked": each violation that has a
  proposal says "the two sentences compile apart; the recorded input is NOT run by this check", and the summary says
  the inputs were not run.
- `book check --separate`: runs `clausal separate` on the two lines again. It fails unless the verdict is SEPARATED,
  the recorded input is one this run found in the recorded direction, and the compiled Rust answered at that input as
  the Lean model did. Run it under `tools/sem.sh`. `./run.sh` now runs it after the Rust step (not with `--no-rust`,
  which says so) and stops if one is not confirmed; its output is `out/book-separate.log`.
- `clausal review <separation id>` runs the same rerun first and signs nothing unless it is confirmed. So no
  sign-off can be taken on an input that does not separate. A sign-off is void when the entry (with its witness),
  either piece or either compiled term changes; a later change of the Lean model or the Rust that changes the answer
  at the input changes no digest, and is caught by the rerun of `./run.sh`, not by the plain check.
- The control: `tools/sem.sh 3 -- python3 clausebook/q3b/bogus.py` records, in a copy, the empty ledger and the
  empty batch (grid 1) for `sep.more_than.exceeds`. The plain lint still lists it as a proposal (16 violations, 0
  not in force); the rerun answers NOT CONFIRMED; `review` exits 1 and writes nothing.

**To adopt one:** `tools/sem.sh 3 -- python3 -m clausal review <id> --reviewer <name>` (it runs Lean and cargo). The sign-off is of the entry (its two lines and
its witness), the book text of both pieces and the two compiled terms; a change to any of them voids it. Were all
seven signed, 11 violations would remain (`python3 clausebook/q3b/check.py`).

**Superseded.** `q4/separations.proposed.yaml` and `q4/check_separations.py` are removed. Three of those seven pairs
took one sentence from the wallet and one from the ledger, which no project reads together; and the file's
instruction, to copy an entry into `core.yaml`, would have put operation nouns into core.

## 3. Bare-hole forms: type-directed resolution is sound, with one stated limit

**The question.** Seven forms have no literal word: `always` "{c:class}", `l.ledger` "{l:ledger}", `l.the_transfer`
"{t:transfer}", `amount_value` "{x:amount}", `index_number` "{x:index}", `balances_value` "{x:balances}",
`amount_result` "{x:amount}". Can two of them, of different pieces, accept the same text at the same type?

**Answer: no, when the types they are registered at are disjoint. Argument from the parser:**

1. The loader registers each form under one key, (category, position) (`Vocabulary._add`). A form written with `<T>`
   is registered once per sort, each time with that sort put into its category and into every hole.
2. In a strict parse, `Parser.forms_for(cat, voice)` returns exactly the forms registered under that key: equality of
   category, no subtype, no coercion. (The relaxed mode compares base categories; it produces only the ILL-TYPED
   message and never a reading.)
3. `Parser.parse(cat, text, voice)` builds a reading of `text` only from a form `forms_for` returned.

So a bare-hole form reads a text only where exactly its own (category, position) is wanted. Two bare-hole forms
whose sets of (category, position) are disjoint never both read a text where one type is wanted.

**The seven:** claim (Then), measure<balances>, item<transfer>, term<num>, term<acct>, term<balances>,
term<optnum>. Pairwise different: 21 of 21 pairs disjoint.

**Tested with the parser itself** (`python3 clausebook/q3b/bare.py`; also run by the self-test):

- Universe: 11252 texts. Every span of whole words of the 280 steps and Rule lines of `features/`, `controls/` and
  the separations; every sample literal of `glossary.yaml`; every role phrase.
- Configurations: 12. Each system in scenario mode, and in rule mode once per operation.
- T1: 945168 (configuration, text, type) triples asked. 1474 have a reading through a bare-hole form. **0 are read
  by the bare-hole forms of two pieces.**
- T1 counts pieces (fix round). It first kept the bare-hole forms of a type as a table from form text to piece, so a
  second piece with the same text at the same type overwrote the first and T1 could not report it: the lint's own
  control case (a second `"{x:amount}"` at `term<num>`) gave 0 exceptions. It now keeps (form text, piece) pairs and
  attributes a reading to the piece of the parser's node. The three numbers above are unchanged. Controls
  (`python3 clausebook/q3b/bare.py --control`, and the self-test): with `amount_twin` `"{x:amount}"` added at
  `term<num>`, 340 exceptions; with `idx_num` `"{x:index}"` there, 336; each names `amount_value` and the twin.

**The rule in the lint.** `book.registered_types` reads the parser's own table. A pair of bare-hole forms is not
counted iff both are in that table and their type sets are disjoint. A pair registered at a common type is a
violation ("4 shared skeleton (no literal word, and registered at one type)") and needs a separation like any other.
Control (self-test, in memory): a second form "{x:amount}" at `term<num>` is reported; the step "the amount is at
most the wallet's balance" becomes AMBIGUOUS and its Rule line is refused, where both read today.

**The limit (T2).** The same text can be read by two bare-hole forms at two DIFFERENT types: 29 texts of the
universe are a `term` at more than one sort ("1" is an account number, a number and an optional number; "the amount"
is a number and an optional number). Which reading is taken is decided by what fixes `T` around it: the other hole of
the frame, or the type the frame's result must have.

- No other generic category has such a text: only `term`.
- One frame has nothing that fixes `T`: `equals` ("{a:term<T>} equals {b:term<T>}", "... differs from ..."). Both
  holes are terms and the result is a condition. "the amount equals 1" has two readings, with `amount_value` and
  with `amount_result`.
- That sentence is refused, never read one way: the step is AMBIGUOUS; a Rule line that contains it is refused
  (self-test, "the limit of the rule"). The lint prints the frames of this kind under "informational".
- The fixtures use `equals` with a hole that does fix `T` ("the amount of the transfer equals zero").

So the rule is sound for what it says (one text, one type), and what it does not cover is a refusal, not a misreading.

**Found on the way.** A Rule line whose condition is AMBIGUOUS is refused as UNBOUND ("no composition ... reads
... as a claim"), not as AMBIGUOUS: the subject parser drops a condition that does not parse to one tree. The line is
refused either way; the message does not say why. Not changed here.

## The 16 that remain, each with the decision it needs

| # | Check | Violation | Decision needed from the owner |
|---|---|---|---|
| 1 to 6 | 1 holes | `always` "is always accepted"; `never` "is always rejected"; `if_then`, `only_if`, `exactly_when` "is accepted ..."; `monotone` "never loses acceptance when" | One decision for the six: is `implied:` (the form's words stand for the class) a declared exemption of check 1, as `from_operation` is? If not, the six verb phrases need a class hole |
| 7 | 3a | `g.line`: four written forms | Are the capital first letter and the final full stop spelling, exempt from "one form"? If not, pick one (strict would refuse every frozen sentence that ends in a full stop) |
| 8 | 3a | `g.subject`: "a", "an" | Is the article spelling, exempt? If not, which one is retired |
| 9 | 3a | `l.apply`: nouns "transfer", "fund transfer" | Which noun is retired. With project-scoped compilation "fund transfer" is no longer needed to say which system; the root README's example uses it |
| 10 | 3a | `monotone`: "never loses acceptance when", "never loses that {c} when" | Keep both as shorthand and long form (an exemption tied to `implied_only`), or retire the shorthand |
| 11 | 3b | `always`: "X is always accepted" and "for X, it is accepted" | Refuse "for X, <class>" when the class is the operation's acceptance (as row 14 did for `monotone`), or accept both and leave it to the duplicate report |
| 12 | 4 | "{} is more than {}": `more_than`, `exceeds` | Sign `sep.more_than.exceeds`, or reword one form |
| 13 | 4 | "{} is at most {}": `not_more_than`, `at_most_value`, `result_at_most` | Sign `sep.not_more_than.at_most_value`, `sep.not_more_than.result_at_most`, `sep.at_most_value.result_at_most` (all three), or reword |
| 14 | 4 | "{} is {}": `is`, `result_is` | Sign `sep.is.result_is`, or reword one form |
| 15 | 4 | "every {} is a {}": `within`, `covers` | Sign `sep.within.covers`, or reword one form |
| 16 | 4 head | `same_answer_if` takes the head of `same_answer` | Sign `sep.same_answer.same_answer_if`, or reword one verb phrase |

Two more questions came out of the work and are not among the 16:

- Should a sentence in no declared project (a `controls/` file, a held-out file) be refused outright rather than read
  against every book?
- Should `equals` be given a hole that fixes its type, or should the lint count a frame whose type nothing fixes?

## Results

Measured 2026-11-12. The full run and `book check --separate` are of commit `c6688c4`; the rest of the tree as committed
after it (the two self-test expectations that `review all` changed).

| What | Result | Command |
|---|---|---|
| `clausal book check` violations | 21 at `492bba6`; 16 now (6 holes, 4 one form per position, 1 one form in a Rule line, 4 shared skeleton, 1 head collision); exit 0 against `check.expected.json` | `python3 -m clausal book check` |
| Not counted, and why | 4 skeletons shared only between entries no project loads together; 21 pairs of 7 bare-hole forms at disjoint types | same |
| Term lock | 125 of 125 sentences of `features/` and `controls/` compile to the recorded term or refusal, with every `features/` sentence compiled against its project's books | same (check 5) |
| Cross-system lines | 2 lines: one statement in the wallet project, one in the ledger project, AMBIGUOUS in a project listing both local books, AMBIGUOUS with no project; lint across systems: 0 with the declared projects, 4 with the project of both, 4 with no project declared | `python3 clausebook/q3b/check.py` |
| Separations | 7 recorded, 7 separate in the ledger project, 7 with an input recorded for today's terms, 0 signed; were all signed: 11 violations | same |
| Separations, run again | 7 of 7 SEPARATED at the recorded input, the compiled Rust agreeing with the Lean model; counts in the table of section 2 | `tools/sem.sh 3 -- python3 -m clausal book check --separate` |
| Bare-hole forms, T1 | 11252 texts, 12 configurations, 945168 triples asked, 1474 read through a bare-hole form, 0 read by two pieces | `python3 clausebook/q3b/bare.py` |
| Bare-hole forms, T1 controls | a second piece at `term<num>` is reported: 340 exceptions with the same form text (`"{x:amount}"`; 0 before the fix round), 336 with another (`"{x:index}"`); 0 on the book | `python3 clausebook/q3b/bare.py --control` |
| Bogus separating input (control) | plain lint: 16 violations, still a proposal, 0 not in force; rerun: NOT CONFIRMED; `review`: exit 1, nothing written; the book as it stands: CONFIRMED | `tools/sem.sh 3 -- python3 clausebook/q3b/bogus.py` |
| Bare-hole forms, T2 | 29 texts read as a `term` at more than one sort; no text of another generic category; 1 frame with nothing to fix `T` (`equals`, 2 forms) | same; `python3 -m clausal book check` ("informational") |
| Self-test | 94 checks, all pass; 7 are Q3b checks (two of them replace one Q4 check; one is of the fix round), 3 more were changed (see below) | `python3 -m clausal.selftest` |
| Controls the book check stops | c39 to c42, as meant | `python3 mutation/check_controls.py` |
| Removal sweep | 260 removals; 0 leave a sentence that uses the entry unchanged; 12 change no recorded term. Same three numbers at `492bba6`. 31 removals now end in LOADFAIL where 22 did: an entry named by a separation cannot be taken out without the book failing to load | `python3 mutation/removal_sweep.py` |
| Verdict codes, `--quick` run | 112 of 112 identical to the baseline | `python3 compare/against/verdicts.py <baseline graph.json>` |
| Verdict codes, full run | 112 of 112 identical to the baseline (39 scenarios, 60 rule groups, 13 functions); run exit 0, 12 min 35 s | same |
| Bounded-check rungs, full run | 4 of 96 readings answered differently from the baseline, each by one rung verified or timed out, none failed (below) | `python3 compare/against/bounded.py <baseline graph.json>` |

Bounded-check rungs that answered differently (30 s limit, other agents building):

| Reading | Verified in the baseline | Verified here |
|---|---|---|
| `Rule.ledger_rules.f_scenario_level` | 2 accounts | 2, 4 accounts |
| `Rule.ledger_rules.n1_internal_transfer` | 2 accounts | 2, 4 accounts |
| `Spec.ledger.batch_conserves` | 2x1, 2x2 | 2x1, 2x2, 2x3 |
| `Spec.ledger.batch_then_total_overflow` | 2x1, 2x2, 2x3 | 2x1, 2x2 |

**Self-test checks changed.** (1) "Q4 fix (book check)" expected the four cross-system skeletons to be reported on the
book as it stands; it is replaced by the two "Q3b (1)" checks. (2) The check that an UNBOUND line lists its project's
operations used "A deposit earns interest"; it uses "A refund earns interest", and a new check states what the first
sentence now gets. (3) The sign-off storage check expected `review all` to sign every entry; it expects every entry
but the separations. The id of the separation the separation control writes into core in memory was renamed, since
`sep.more_than.exceeds` is now an entry of the ledger's local book.
(4) Fix round: the separation control ("book check 4, THE CONTROL") signs its in-memory separations with the
confirmation given (`review(..., confirm=)`), because `review` now runs `clausal separate` before it signs and those
entries record no input; that control is of the lint given a sign-off record, and its expectations are unchanged. The
gate has its own check ("Q3b fix round"), and the bare-hole check now also runs T1 on the two twins.

**`review all` signs no separation.** Found by `mutation/check_controls.py`: controls c10, c11 and c26 sign every
entry as a test reviewer, which signed the seven proposals, lifted five violations and made the book check fail on
its expected list. A separation is now signed only by its own id.

## Fix round (review of `90a73ad`)

Two defects, both fixed; the numbers of the count (21 to 16), the 16 keys and the term lock are unchanged.

1. **T1 of `bare.py` could not see two pieces with the same form text at one type.** Fixed as described in section 3
   (T1 counts pieces). Before: the twin `"{x:amount}"` at `term<num>` gave 0 exceptions. After: 340. The book: 0,
   with the same 945168 triples asked and 1474 read.
2. **The plain `book check` printed "PROPOSED, machine-checked" and never ran the recorded input.** The plain check
   still does not run it (it would need Lean and cargo in a check that has neither). Changed instead: (a) what it
   prints says exactly what it checked; (b) `./run.sh` runs `book check --separate` after the Rust step and stops on
   an unconfirmed input; (c) `clausal review <separation>` runs the rerun and signs nothing unless it is confirmed,
   so a separation with no recorded input can no longer be signed either. Control: `clausebook/q3b/bogus.py`.
   The wording of 5 of the 16 entries of `check.expected.json` changed with the label (`what`); their keys, which are
   what the check compares, did not.

Runs of the fix round (this tree, 2026-11-12):

| What | Result | Command |
|---|---|---|
| `clausal book check` | 16 violations, the same 16 keys; exit 0 | `python3 -m clausal book check` |
| Self-test | 94 checks, all pass | `python3 -m clausal.selftest` |
| Separations, run by `./run.sh` | 7 of 7 recorded inputs confirmed (`out/book-separate.log`), in the `--quick` run and in the full run | `tools/sem.sh 3 -- ./run.sh` |
| Controls the book check stops | c39 to c42, as meant | `python3 mutation/check_controls.py` |
| Verdict codes, `--quick` and full run | 112 of 112 identical to the baseline, both runs; full run exit 0, 13 min 14 s | `python3 compare/against/verdicts.py <baseline graph.json>` |
| Bounded-check rungs, full run | 2 of 96 readings answered differently, each one rung timed out that the baseline verified, none failed: `Rule.ledger_rules.readme_internal_transfers` (4 accounts), `Spec.ledger.batch_then_total_overflow` (2x3) | `python3 compare/against/bounded.py <baseline graph.json>` |

Not rerun in the fix round: the removal sweep (`mutation/removal_sweep.py`); it reads no code this round changed
except the wording of a lint message.

## Not done, not verified

- Nothing is signed. The five check-4 violations stay until a person signs.
- The full mutation run (`mutation/run_mutants.py`, 45 mutants and 49 controls) was not rerun. `check_controls.py`
  (the book check on each control's patch) was.
- `clausal compose` and `clausal separate` are not project-scoped (section 1, limits). The separating inputs were found
  by `clausal separate` reading every book in the ledger's system; the lint requires the two terms it compared to be the
  terms the lines compile to in the ledger project, and they are.
- The argument of section 3 is an argument about `vocab.py` as read, with a test. It is not a Lean proof.
- T1's universe is the text of the fixtures, not every text. The argument does not depend on the universe; the test does.
- The root `README.md`, `docs/` and `TODO.md` were not edited.
