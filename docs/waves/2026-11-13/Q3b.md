# Q3b: reports as returned by the agents

Builder, reviewer (Opus) and fix round, unedited apart from the session scratch path. Worktree paths under `.worktrees/` have since been removed; the commits are on `main`, or in the local `private/tdf-core` repository for T9.4c.

## Builder

# Q3b: book check violations 21 → 16, verdicts identical to the baseline

Five violations are settled, five more now carry a machine-checked proposal that waits for a signature, and eleven need an owner decision. Nothing was signed. Work is on branch `wave/book2` in `/Users/will/dev/lean-rosette/.worktrees/book2`, not pushed.

## Commits

- `1306fe6`: the freeze (items, tests, expected count), before the lint change and the recorded runs.
- `c6688c4`: the implementation.
- `90a73ad`: results, decision list, outputs of the one full run.

## What changed (paths under `clausal/`)

- **`clausal/vocab.py`**: `Vocabulary.scoped(books)` and `Compiler.for_books`; `Compiler.rule(rule, hint, books)` and `Compiler.scenario(sc, books)` now compile against the books of the sentence's project only. With `books=None` a line is read against every book, as before. The loader accepts an optional `witness:` on a separation.
- **`clausal/pipeline.py`, `newrules.py`, `duplicates.py`, `book.py` (term lock)**: pass the project's books.
- **`clausal/book.py`**:
  - check 4 is asked per project (`scopes_of`, `collisions`);
  - a separation is read in one project (`separation_state`);
  - proposed separations (`witness_state`, `rerun_separation`, new flag `book check --separate`);
  - the bare-hole rule (`registered_types`, `bare_types`);
  - an informational note for frames whose type nothing fixes.
- **`clausal/vreport.py`, `__main__.py`**: `review all` signs no separation.
- **`clausebook/local/ledger.yaml`**: seven `separations:` entries, each with a `witness:`, unsigned.
- **`clausebook/check.expected.json`**: 16 entries (was 21).
- **`clausal/selftest.py`**: six Q3b checks; three existing checks changed (listed under "distrust").
- **New**: `clausebook/q3b/FREEZE.md`, `README.md` (design, results, decision list), `check.py`, `bare.py`.
- **Edited docs**: `clausebook/README.md`, `clausebook/q4/README.md` (pointer), `DESIGN.md` section 22.
- **Removed**: `clausebook/q4/separations.proposed.yaml`, `clausebook/q4/check_separations.py` (superseded).
- **`out/`**: outputs of the full run.

## The three parts

**(1) Cross-system: 4 → 0.** Compilation was not project-scoped: `books` only chose which operations an UNBOUND message listed. It is now. No project lists `local/wallet.yaml` and `local/ledger.yaml` together, so the four skeletons are printed under "not counted".

| Line, no scenario beneath | wallet | ledger | one project listing both local books (in memory) | wallet with "transfer" also a noun of `w.deposit` (in memory) | no project named |
|---|---|---|---|---|---|
| A transfer is always accepted | one statement, `w.transfer` | one statement, `l.apply` | AMBIGUOUS | AMBIGUOUS | AMBIGUOUS |
| For a transfer, it is accepted | one statement, `w.transfer` | one statement, `l.apply` | AMBIGUOUS | AMBIGUOUS | AMBIGUOUS |

Given a project that lists both local books, or no declared project, the lint reports the four again.

**(2) Separating pairs: 7 proposals recorded, count unchanged (5 violations).** Each is two Rule lines about one ledger operation. `clausal separate` answered SEPARATED for all seven and the compiled Rust agreed with the Lean model at the recorded input.
- A proposal lifts nothing; the violation of its pair stays and names it.
- A proposal whose recorded term is stale, or that has no input recorded, is reported as `4 separation not in force`.
- They stand in the ledger's local book, not core: core may name no fixture noun, and a sentence is read in one project.
- Were all seven signed, 11 violations would remain.

**(3) Bare holes: 1 → 0, as a checked rule.** The parser tries a form only at exactly the (category, position) it is registered under, with no subtype, and a `<T>` form is registered once per sort. The seven forms sit at seven different types, so no two can read one text at one type.
- Test over the book: 11252 texts, 12 configurations, 945168 triples asked, 1474 read through a bare-hole form, 0 read by two pieces.
- Control: a second `{x:amount}` form at `term<num>` (in memory) is reported by the lint, the step becomes AMBIGUOUS and its Rule line is refused.
- Stated limit: 29 texts are a `term` at more than one sort ("1", "the amount"). One frame, `equals`, has nothing that fixes `T`, so "the amount equals 1" has two readings that differ only in the bare-hole piece. That sentence is refused, never read one way; the lint prints the frame as informational.

## Verification (actual output)

```
book check: registration lint over 139 surface forms of 5 books: 16 violations
  check 1 holes: 6 | 3a: 4 | 3b: 1 | 4 shared skeleton: 4 | across systems: 0 | 4 head collision: 1 | 4 separation not in force: 0 | 5 same term: 0
  not counted: 4 skeletons shared only between entries that no project loads together
  not counted: 21 pairs of 7 pieces whose only shared skeleton is "{}" ... each pair registered at disjoint types
  separations: 7 recorded; 7 PROPOSED
  terms: 125 sentences of features/ and controls/ compiled or refused as recorded
book check: the violations are exactly the expected ones (16 expected)

book check --separate exit 0   (7 of 7 "SEPARATED at the recorded input ... the compiled Rust agrees with the Lean model")
selftest: 93 ok, all checks passed
check_controls.py: 4 controls are stopped by the book check: c39, c40, c41, c42 ... all as meant
full run exit 0: RESULT: every scenario got its expected verdict and every Rule statement its expected one  (12:35)
verdict codes that differ: 0 of 112   (also 0 of 112 on the --quick run)
bounded-check results that differ: 4
```

Bounded-check rungs that answered differently (one rung each, none failed):

| Reading | Verified in baseline | Verified here |
|---|---|---|
| `Rule.ledger_rules.f_scenario_level` | 2 accounts | 2, 4 accounts |
| `Rule.ledger_rules.n1_internal_transfer` | 2 accounts | 2, 4 accounts |
| `Spec.ledger.batch_conserves` | 2x1, 2x2 | 2x1, 2x2, 2x3 |
| `Spec.ledger.batch_then_total_overflow` | 2x1, 2x2, 2x3 | 2x1, 2x2 |

## The 16 that remain, each with its decision

| # | Check | Violation | Decision needed |
|---|---|---|---|
| 1–6 | 1 holes | `always`, `never`, `if_then`, `only_if`, `exactly_when`, `monotone` verb phrases whose words stand for the class | One decision for all six: is `implied:` a declared exemption of check 1 (as `from_operation` is), or do the six get a class hole? |
| 7 | 3a | `g.line`: four written forms | Are the capital and the final full stop spelling, exempt? If not, pick one (strict refuses every frozen sentence ending in a full stop). |
| 8 | 3a | `g.subject`: "a", "an" | Is the article spelling, exempt? If not, which is retired? |
| 9 | 3a | `l.apply`: "transfer", "fund transfer" | Which noun is retired? With project scoping "fund transfer" is no longer needed to say which system; the root README's example uses it. |
| 10 | 3a | `monotone`: two verb phrases | Keep shorthand and long form (an exemption tied to `implied_only`), or retire the shorthand? |
| 11 | 3b | `always`: "X is always accepted" and "for X, it is accepted" | Refuse "for X, <class>" when the class is the operation's acceptance, or accept both and leave it to the duplicate report? |
| 12 | 4 | "{} is more than {}" | Sign `sep.more_than.exceeds`, or reword one form. |
| 13 | 4 | "{} is at most {}" (3 pairs) | Sign `sep.not_more_than.at_most_value`, `sep.not_more_than.result_at_most`, `sep.at_most_value.result_at_most`, or reword. |
| 14 | 4 | "{} is {}" | Sign `sep.is.result_is`, or reword. |
| 15 | 4 | "every {} is a {}" | Sign `sep.within.covers`, or reword. |
| 16 | 4 head | `same_answer_if` takes the head of `same_answer` | Sign `sep.same_answer.same_answer_if`, or reword. |

Two further questions came out of the work, outside the 16:
- Should a sentence in no declared project be refused rather than read against every book?
- Should `equals` get a hole that fixes its type, or should the lint count such a frame?

## Not done, not verified

- Nothing is signed.
- The full mutation run (`mutation/run_mutants.py`) was not rerun; only `check_controls.py`.
- `clausal compose` and `clausal separate` are not project-scoped: they take a system and load every book. Today each system's operations sit in one project, but the code does not enforce that.
- The Rust cucumber side (`wallet-bdd`) was not changed.
- The bare-hole argument is an argument about `vocab.py` as read, plus a test over the fixtures' text. It is not a Lean proof.
- `clausebook/q4/sentences.sh` and `oq3_probe.py` were not rerun.

## What a reviewer should distrust

- **The freeze is not blind.** The seven pairs were chosen by compiling candidates, and `clausal separate` was run on each once before the freeze commit; `FREEZE.md` says so. The project-scoped compiler also existed in the working tree at that point.
- **Three existing self-test expectations were changed:**
  - "Q4 fix (book check)" expected the four cross-system skeletons to be reported; two Q3b checks replace it.
  - The X7 check on listed operations now uses "A refund earns interest" instead of "A deposit earns interest".
  - The sign-off storage check expects `review all` to sign every entry except separations.
  - The in-memory separation id was also renamed, because `sep.more_than.exceeds` is now a real entry.
- **Two fixture refusal messages changed**, same status and code (UNBOUND): `Rule.wallet.interest` and `Rule.counter_rules.bump_resets` are now refused for the claim, where they were refused as "no rule clause" with a list of operations. The term lock compares status and code only, so it does not see this.
- **An unsigned separation with a valid witness is no longer a violation of its own.** This changes the earlier rule that any recorded separation not in force is a violation. The pair's violation still stands and names the proposal.
- **The bare-hole exemption is weaker than "no sentence is read two ways".** It covers one text at one type; the `equals` case rests on the compiler's refusal.
- **A Rule line whose condition is AMBIGUOUS is refused as UNBOUND**, not AMBIGUOUS, so the message does not say why. Found, not fixed.
- **`controls/` and files listed by no project are still read against every book**, so "A transfer …" with no scenario is still AMBIGUOUS there.
- **`out/report.md` differs from the baseline report in the mutation table.** `mutation/results.json` at HEAD is the 15:45 run and the baseline report shows the 05:58 run. I attribute the differences to that; verdict codes are identical.
- **The removal sweep's three headline numbers are unchanged, but 31 removals now end in LOADFAIL where 22 did.** A piece named by a separation cannot be taken out without the book failing to load, so for those the sweep shows a load failure rather than a changed sentence.
- **Three of the seven Q4 proposals paired a wallet sentence with a ledger sentence**, which no project reads together. I also claim that copying them into `core.yaml` would have broken "core stands alone", by the noun-scan rule; I did not run that.

## FOR DECISIONS.md

1. **Project scoping as a scoped Vocabulary.**
   - What: a sentence is compiled against a Clausebook built from exactly its project's books, by the same loader.
   - Why: one mechanism covers operations, forms, subject words and sorts; filtering each lookup would miss some.
   - Undo: in `vocab.py` make `Compiler.for_books` return `self`; restore `listed_operations` from `492bba6`.
2. **Scenarios are scoped too**, not only Rule lines.
   - Why: the task says compilation, and the lint's per-project check would otherwise be inexact for `when` forms.
   - Undo: drop the `books` argument in `pipeline.py`, `newrules.py`, `duplicates.py`, `book.compiled_terms`.
3. **No project named still means every book.**
   - Why: `controls/`, the self-test and held-out files have no project; refusing them is an owner question.
   - Undo: not applicable (unchanged behaviour).
4. **Lint check 4 per project, with a fallback scope of every book** when a loaded book is in no project's list.
   - Why: only entries one project loads together can meet in a sentence; the fallback leaves nothing unchecked.
   - Undo: call `book.lint(voc, pr=[])`, or revert `book.py`.
5. **Proposals live in `clausebook/local/ledger.yaml`, all seven with ledger sentences.**
   - Why: core may name no fixture noun, a separation is read in one project, and one operation per pair gives a common input.
   - Undo: delete the `separations:` block.
6. **An unsigned separation that separates and has a valid `witness:` is not a `4 separation not in force` violation.**
   - Why: the task asks for recorded, unsigned proposals; otherwise seven violations would be added for doing so.
   - Undo: in `book.lint`, append "nobody has signed it" whenever there is no sign-off.
7. **The witness check is in two parts.** Every `book check` compares term hashes; `--separate` reruns `clausal separate`.
   - Why: `book check` runs in step 3 of `run.sh` with no Lean build yet.
   - Undo: none needed; `--separate` is opt-in.
8. **`review all` signs no separation.**
   - Why: controls c10, c11 and c26 sign everything as a test reviewer, which put the proposals in force and failed the book check; a bulk sign-off should not lift lint violations.
   - Undo: restore `ids = all_ids(voc)` in `vreport.review`.
9. **Bare-hole exemption by disjoint registered types**, with equal types still a violation and `equals` printed as informational rather than counted.
   - Why: the exemption is exactly what the parser guarantees; whether a type-free frame is a violation is an owner call.
   - Undo: remove the `typed` block in `book.lint`; the one violation returns under the key `{}|always,…`.
10. **Removed the Q4 proposal file and its script.**
    - Why: the ids collide with the book entries, and three pairs cannot be read in one project.
    - Undo: `git checkout 492bba6 -- clausal/clausebook/q4/separations.proposed.yaml clausal/clausebook/q4/check_separations.py` and rename the ids.
11. **Changed three self-test expectations** (listed under "distrust").
    - Why: each tested behaviour this task changes on purpose.
    - Undo: revert `selftest.py`.
12. **`clausebook/check.expected.json` rewritten** with `--update-expected` (21 → 16).
    - Undo: `git checkout 492bba6 -- clausal/clausebook/check.expected.json`.
13. **Added `DESIGN.md` section 22** and edited `clausebook/README.md` and `clausebook/q4/README.md` (pointers).
    - Why: section 21 said `books` changes no reading, which is no longer true.
    - Undo: revert those hunks.

## FOR RESULTS

All commands run from `clausal/`; measured 2026-11-12.

| Number | Command |
|---|---|
| Book check violations: 21 at `492bba6`, 16 now (6 / 4 / 1 / 4 / 1) | `python3 -m clausal book check` |
| Not counted: 4 cross-project skeletons; 21 bare-hole pairs of 7 pieces | same |
| Term lock: 125 of 125 as recorded | same (check 5) |
| Cross-system lines: 2 of 2 one statement per project; AMBIGUOUS in the merged project and with no project; lint across systems 0 / 4 / 4 | `python3 clausebook/q3b/check.py` |
| Separations: 7 recorded, 7 separate, 7 with a current input, 0 signed; 11 violations if all were signed | same |
| Separations rerun: 7 of 7 SEPARATED at the recorded input, Rust agrees | `tools/sem.sh 3 -- python3 -m clausal book check --separate` |
| Grid counts per pair (only first / only second / both / neither): 72/18/207/0; 18/72/199/8; 0/80/217/0; 0/26/271/0; 221/3/69/4; 203/0/94/0 (297 inputs each); 0/5/4351/0 (4356 inputs) | same |
| Bare holes T1: 11252 texts, 12 configurations, 945168 triples, 1474 read, 0 by two pieces | `python3 clausebook/q3b/bare.py` |
| Bare holes T2: 29 texts read as `term` at more than one sort; 1 frame with free type (`equals`, 2 forms) | same; `python3 -m clausal book check` |
| Self-test: 93 checks pass | `python3 -m clausal.selftest` |
| Controls stopped by the book check: c39–c42, as meant | `python3 mutation/check_controls.py` |
| Removal sweep: 260 removals, 0 leave a using sentence unchanged, 12 change no term (same at `492bba6`); LOADFAIL 31 vs 22 | `python3 mutation/removal_sweep.py` |
| Verdict codes: 112 of 112 identical to the baseline, quick and full run (39 scenarios, 60 rule groups, 13 functions) | `python3 compare/against/verdicts.py <baseline graph.json>` |
| Bounded-check rungs: 4 of 96 readings differ, listed above | `python3 compare/against/bounded.py <baseline graph.json>` |
| Full run: exit 0, 12 min 35 s | `tools/sem.sh 3 -- ./run.sh` |

Baseline graph: `<scratchpad>/baseline2/graph.json`. Design, tables and the decision list are in `/Users/will/dev/lean-rosette/.worktrees/book2/clausal/clausebook/q3b/README.md`.

## Reviewer

The builder's report holds up. I reran every cheap check and each matches what the builder reports.

Numbers that recount:
- `clausal book check`: 21 violations at 492bba6 and 16 at HEAD. Exactly the 5 frozen keys are gone: the 4 cross-system ones and the bare-hole one.
- `clausebook/q3b/check.py`: wallet → w.transfer, ledger → l.apply, AMBIGUOUS in a project listing both and with no project; lint across systems 0/4/4; 11 violations if all seven were signed.
- `clausebook/q3b/bare.py`: 11252 texts, 945168 triples, 1474 read, 0 read by two pieces; T2 29.
- Self-test: 93 ok. `check_controls.py`: c39–c42 as meant.
- Against the baseline graph: verdicts 0 of 112 differ, and the 4 bounded-rung differences match the report. Removal sweep: 260/0/12, LOADFAIL 31 vs 22.
- Compiling every fixture at both revisions gives identical Lean terms and statuses for all 99 readings. Only the two disclosed refusal messages changed.
- The 48 frozen sentences: 0 of 48 compile, output identical to baseline, so nothing was tuned to them.

Nothing changed that should not have. features/, controls/, terms.lock.json, glossary, the Lean sources and the meaning of every book entry are untouched; local/ledger.yaml only gained the separations block. No sign-off file exists, the lint calls all seven separations UNSIGNED, and `review all` signs none of them. FREEZE.md has a single commit, and it comes before the implementation and the run.

Project scoping:
- In a real wallet feature file (scratch copy), "A fund transfer is always accepted" and "A batch never changes the total of the ledger's balances" are refused UNBOUND, not read in the ledger.
- A noun bound twice inside one project is still refused AMBIGUOUS: I tried w.withdraw given the noun "transfer" and l.lookup given "batch", and the lint reports each pair.

Bare-hole rule: I wrote six overlapping bare-hole forms of my own: a different hole type at term<acct>, a generic term<T>, a then-form claim against `always`, a wallet-local form at term<optnum>, a ledger-local twin, and a generic measure<T>. The lint reported every one. Its argument (exact match on category and position, relaxed mode gives only ILL-TYPED) agrees with vocab.py.

Separations: I wrote my own model of `apply_batch`/`apply` from the Rust code, checked against the Lean definitions of the frames. With it:
- each of the seven recorded inputs separates: one reading holds, the other fails;
- every grid count reproduces exactly (72/18/207/0 … 0/5/4351/0);
- each recorded input is the first separating input on the grid.

I did not run the heavy `--separate` check (Lean and Rust).

Defects:
- **Should-fix, bare.py:** T1 keys forms by their text, so a twin with the same text at the same type (the builder's own control, a second "{x:amount}" at term<num>) is invisible to it: 0 exceptions, exit 0.
- **Should-fix, the "machine-checked" label:** the plain book check (the one run.sh runs) prints "PROPOSED, machine-checked" after checking only term hashes. A recorded input at which both readings hold still passes.
- **Notes:**
  - the lint says "no sentence is compiled against both", which is false for controls/ and held-out files;
  - the removal sweep no longer tests 9 core entries, which now end in LOADFAIL because separations name them;
  - stale wording in projects.yaml and projects.py, and DECISIONS.md not appended;
  - the freeze commit holds only the descriptions of the tests, not the test files;
  - several witnesses are weak: different sentence shapes, vacuous conditions;
  - sentences.sh and readings.py were already broken before Q3b.

Scratch scripts and outputs are in <scratchpad>/review-Q3b/.

- **should-fix**: bare.py T1 (the test half of the bare-hole soundness claim, also asserted by the self-test) cannot see two pieces that have the same form text at the same (category, position). It builds `bare[(c, v)][f.text] = piece`, so a second piece with the same text overwrites the first, and `got` never holds two owners. That is exactly the builder's own control case (a second "{x:amount}" at term<num>): T1 reports 0 exceptions and exits 0. A twin with different text ("{x:index}" at term<num>) is caught, with 336 exceptions. The self-test runs that control only through the lint, not through bare.py. The lint rule itself is sound, and on today's book the 7 registered types are pairwise distinct, so the result 0 is still right. But the test is weaker than reported, and blind to the most natural collision.
- **should-fix**: The plain `book check`, which run.sh step 3 runs, labels every proposal "PROPOSED, machine-checked". It checks only that the two term hashes are current; it never checks that the recorded input separates. I recorded an input at which both readings hold (ledger [], batch [], grid 1) for sep.more_than.exceeds. The book check still exits 0 with 16 violations, the same label, and 0 'separation not in force'. Only the opt-in `--separate` catches it. A person who signs on the strength of that label lifts the violation even with a bogus witness. The two-part check is disclosed (decision 7), but the printed label claims more than the plain check does.
- **note**: The lint's justification for dropping the 4 cross-system skeletons, "(no sentence is compiled against both)", is false for sentences that no project lists: controls/, held-out files given to `clausal compile`, and the trials. Those are still compiled against every book, and "A transfer is always accepted" and "For a transfer, it is accepted" are AMBIGUOUS there. This fails closed (a refusal, not a misreading) and the builder raises it as an owner question, but the wording of the lint overstates it.
- **note**: The removal sweep no longer tests 9 core entries. At 492bba6, removing not_more_than, more_than, exceeds, at_most_value, result_at_most, same_answer, same_answer_if, within or covers was caught because using sentences changed (36 changed sentences in all). Now each removal ends in LOADFAIL, because a separation's `between` names the entry, and the sweep counts LOADFAIL as noticed. The headline numbers (260 / 0 / 12) are unchanged, but for these entries they now rest on the proposals, not on the sentences. The builder disclosed the LOADFAIL count (31 vs 22), not this loss of coverage.
- **note**: Some docs still describe the old behaviour. projects.yaml lines 22-24 say "the books are loaded as one merged book, so the refusal AMBIGUOUS between two projects stays". The clausal/clausal/projects.py module docstring (line 12) says the same, and the books_of docstring still says books only choose the operations a refusal lists. DESIGN.md section 22 was added, but these files were not updated. DECISIONS.md was not appended either; the report gives the text under 'FOR DECISIONS.md'.
- **note**: The freeze commit 1306fe6 contains only FREEZE.md, which describes the tests. The test code itself (clausebook/q3b/check.py, clausebook/q3b/bare.py, the six self-test checks) and check.expected.json were committed together with the implementation in c6688c4. FREEZE.md was not edited afterwards and comes before the runs (graph generated 17:52Z, after c6688c4), and it states that it is not blind. Even so, the report's 'freeze (items, tests, expected count)' is true only of the descriptions.
- **note**: Before signing, the owner should know how weak several witnesses are. Three pairs set two sentences of different shapes against each other (not_more_than/result_at_most, at_most_value/result_at_most, is/result_is), and two sentences hold at every grid point (result_at_most 297/297, within 297/297). Most of the recorded inputs separate because one sentence's 'for which' condition is false, so it holds vacuously. Each input is a valid separating input, but in those cases it mostly shows that two different sentences mean different things, not that a reader would tell the shared skeleton apart.
- **note**: Two existing tools crash, and both problems predate Q3b (they come from X7): clausebook/q4/sentences.sh and compare/against/readings.py copy the tree without projects.yaml, so projects.load raises FileNotFoundError. I worked around both. The 48 frozen sentences compile 0 of 48, with output identical to 492bba6. All 99 fixture readings compile to the same Lean terms and statuses as at 492bba6; only the two disclosed refusal messages changed (Rule.wallet.interest and Rule.counter_rules.bump_resets).

## Fix round

Both defects are real and both are fixed in commit `7710396` on `wave/book2` (worktree `/Users/will/dev/lean-rosette/.worktrees/book2`, not pushed). The book check still reports 16 violations with the same 16 keys, and all 112 baseline verdict codes are identical after one full `./run.sh` (exit 0).

## Per defect

### Defect 1: `bare.py` T1 could not see two pieces with the same form text at one type — fixed

- **Cause:** T1 kept the bare-hole forms of a type as a table from form text to piece, so a second piece with the same text overwrote the first.
- **Fix:** `clausal/clausebook/q3b/bare.py` now keeps (form text, piece) pairs and attributes a reading to the piece on the parser's node. A new `--control` mode runs T1 on the book with a twin added in memory, once with the same text and once with another spelling.
- **Self-test:** the bare-hole check now runs T1 on both twins, not only the lint.

Output of `python3 clausebook/q3b/bare.py --control`:
```
T1 on the book as it stands: 0 exceptions
T1 with `amount_twin` "{x:amount}" added at term<num> (same text): 340 exceptions, pieces [('amount_twin', 'amount_value')]; ...
T1 with `idx_num` "{x:index}" added at term<num> (another spelling): 336 exceptions, pieces [('amount_value', 'idx_num')]; ...
controls: both twins are reported, and the book has no exception
```
The reviewer's repro (`t_bare_twin.py`) now prints `rc 1 ... T1 exceptions 340` for the same-text twin, where it printed `rc 0 ... 0`. On the book, T1 is unchanged: 945168 triples asked, 1474 read through a bare-hole form, 0 read by two pieces.

### Defect 2: the plain `book check` printed "PROPOSED, machine-checked" without running the recorded input — fixed

The plain check still does not run the input; that needs Lean and cargo, about 27 s. Three things changed instead:

- **Label:** each violation with a proposal now reads "PROPOSED and unsigned (the two sentences compile apart; the recorded input is NOT run by this check, `book check --separate` runs it)". The summary adds a line saying the inputs were not run. "machine-checked" is no longer printed.
- **`run.sh`:** it runs `book check --separate --quiet` after the Rust step and stops if an input is not confirmed. Output goes to `out/book-separate.log`. With `--no-rust` it prints that the inputs were not run.
- **Signing gate:** `clausal review <separation id>` runs `clausal separate` first and signs nothing, writes nothing and exits 1 unless the input is confirmed (`clausal/clausal/vreport.py`, `review(..., confirm=)`).

Control with the reviewer's bogus witness, in a temporary copy of the book (`tools/sem.sh 3 -- python3 clausebook/q3b/bogus.py`):
```
bogus input {'the_ledger': '[]', 'the_batch': '[]'} (grid 1), term hashes unchanged
1 plain lint: 16 violations, 0 'separation not in force'; the pair's violation says: ...no separating pair signed; PROPOSED and unsigned (the two sentences compile apart; the recorded input is NOT run by this check, `book check --separate` runs it)
2 rerun (book check --separate): NOT CONFIRMED: the recorded separating input (...) is not one this run found
3 clausal review sep.more_than.exceeds: exit 1; sign-off file unchanged; violations after: 16; it printed: NOT signed: ...
4 the book as it stands: 16 violations; rerun of sep.more_than.exceeds: CONFIRMED at {'the_ledger': '[2, 1]', 'the_batch': '[0->1:1]'}
control: as expected
```

## What changed (paths under `clausal/`)

- `clausebook/q3b/bare.py`: T1 keyed on (form text, piece); `run()`, `control_voc()`, `--control`.
- `clausebook/q3b/bogus.py`: new, the bogus-witness control.
- `clausal/book.py`: label and summary wording, docstring.
- `clausal/vreport.py`: the signing gate.
- `run.sh`: the separation rerun after step 7.
- `clausal/selftest.py`: one new check ("Q3b fix round"), the bare-hole check extended, and the older separation control now injects the confirmation.
- `clausebook/check.expected.json`: the `what` text of 5 entries, regenerated with `--update-expected`; keys and counts are identical.
- `clausebook/q3b/README.md` (fix-round section, results), `clausebook/README.md`, `DESIGN.md` (section 21, item 3).
- `out/*`: outputs of the full run.

## Verification

- **Book check:** `python3 -m clausal book check --quiet` prints "16 violations" and "the violations are exactly the expected ones (16 expected, ...)".
- **Self-test:** `python3 -m clausal.selftest` prints "all checks passed", 94 checks.
- **Quick run:** `./run.sh --quick` exits 0, prints "separations: 7 of 7 recorded separating inputs confirmed by clausal separate", and `verdicts.py` reports "verdict codes that differ: 0 of 112".
- **Full run:** `./run.sh` exits 0 in 13 min 14 s, prints the same 7 of 7 line and "RESULT: every scenario got its expected verdict and every Rule statement its expected one"; `verdicts.py` reports 0 of 112 differing.
- **Controls:** `python3 mutation/check_controls.py` reports c39 to c42 stopped by the book check, "all as meant".
- **Bounded-check rungs that answered differently under load (not regressions):** 2 of 96 readings, each one rung timed out that the baseline verified, none failed:
  - `Rule.ledger_rules.readme_internal_transfers`: up to 4 accounts.
  - `Spec.ledger.batch_then_total_overflow`: 2 accounts and 3 transfers.

## Not done, not verified

- The removal sweep (`mutation/removal_sweep.py`) was not rerun; this round changed only the wording of a lint message among the things it reads.
- The plain `book check` still does not run a recorded input. It now says so; it is not made to.
- The signing gate was exercised for real once, on the bogus witness (refused). No real signature was taken, so the confirmed path of `review` was only run with an injected confirmation in the self-test.
- Nothing was signed.

## What a reviewer should distrust

- **Stale answers at a signed input:** a later change to the Lean model or the Rust that changes the answer at a signed input changes no digest. Only the rerun in `./run.sh` catches it; a plain `book check`, or `./run.sh --no-rust`, does not.
- **Rerun on an in-memory book:** `rerun_separation` calls `separate.separate`, which loads the book from disk rather than the vocabulary passed in. For an altered book it matches readings by term hash. The bogus control changes only the witness, so it is unaffected, but an altered sentence would be compared against the on-disk book.
- **The older self-test separation control** now signs with an injected "confirmed". It tests the lint given a sign-off record and no longer exercises the real `review` path for separations.
- **T1 attribution** relies on a node read through a bare-hole form carrying the owning piece's id. The unchanged count of 1474 readings is the evidence for that.
- **The "confirmed" test in `run.sh`** is the exit status of `book check --separate`; the "7 of 7" line is a grep count over its log.

## FOR DECISIONS.md

Earlier Q3b decisions stand as reported by the earlier steps, except decision 7 (the two-part machine check), which is superseded by items 2 to 4 below. New or changed in this round:

1. **`bare.py` T1 counts pieces, not form texts.**
   - Why: keyed on text, a same-text twin at one type was invisible.
   - Undo: `git checkout 90a73ad -- clausal/clausebook/q3b/bare.py`, and revert the bare-hole lines of `selftest.py`.
2. **The plain `book check` keeps not running the recorded input, and its label was changed to say so.**
   - Why: running the input needs Lean and cargo (about 27 s), and the plain check is run where neither is built (step 3 of `run.sh`, before `lake build`).
   - Undo: restore the two strings in `book.lint` (`offer`) and `cmd_check`, then `python3 -m clausal book check --update-expected`.
3. **`./run.sh` runs `book check --separate` after the Rust step and fails on an unconfirmed input; it is skipped, with a printed line, under `--no-rust`.**
   - Why: this is the only place a drift of the model or the Rust at a recorded input is caught.
   - Cost: about 27 s per run, `--quick` included.
   - Undo: remove the block after `wait "$ADEQ2_PID"` in `run.sh`.
4. **`clausal review <separation>` runs `clausal separate` first and refuses to sign an unconfirmed separation.**
   - Consequence: a separation with no recorded `witness:` can no longer be signed, and signing one needs Lean and cargo (run it under `tools/sem.sh`).
   - Why: a signature lifts a violation, so it should not be possible on an input that does not separate.
   - Undo: remove the gate loop in `vreport.review`.
5. **The wording (`what`) of 5 entries of `clausebook/check.expected.json` was regenerated.**
   - Why: the label changed. The check compares `(check, key)` only, and those are identical (16 of 16, same counts).
   - Undo: `git checkout 90a73ad -- clausal/clausebook/check.expected.json`.
6. **The older self-test control "book check 4, THE CONTROL" signs its in-memory separations with an injected confirmation.**
   - Why: those entries record no input, and the control is about the lint given a sign-off; its expectations are unchanged.
   - Undo: drop the `confirm=` argument at `selftest.py` line 664 (the control then fails unless the gate is removed too).

## FOR RESULTS

All commands run from `clausal/` at commit `7710396`; `<baseline>` is `<scratchpad>/baseline2/graph.json`.

| Measured | Result | Command |
|---|---|---|
| Book check violations | 21 at `492bba6`; 16 now, same 16 keys as before the fix round; exit 0 | `python3 -m clausal book check` |
| Bare-hole T1 on the book | 11252 texts, 12 configurations, 945168 triples asked, 1474 read through a bare-hole form, 0 read by two pieces | `python3 clausebook/q3b/bare.py` |
| Bare-hole T1 controls | same-text twin at `term<num>`: 340 exceptions (0 before the fix); other-spelling twin: 336; book: 0 | `python3 clausebook/q3b/bare.py --control` |
| Bogus separating input | plain lint 16 violations, still a proposal, 0 not in force; rerun NOT CONFIRMED; `review` exit 1, nothing written; real book CONFIRMED | `tools/sem.sh 3 -- python3 clausebook/q3b/bogus.py` |
| Separations rerun | 7 of 7 confirmed at the recorded input, Rust agreeing with the Lean model (27 s) | `tools/sem.sh 3 -- python3 -m clausal book check --separate` |
| Separations rerun inside the pipeline | 7 of 7, in the `--quick` run and the full run | `tools/sem.sh 3 -- ./run.sh` (line "separations:", `out/book-separate.log`) |
| Self-test | 94 checks, all pass (93 before; one new) | `python3 -m clausal.selftest` |
| Controls stopped by the book check | c39, c40, c41, c42, as meant | `python3 mutation/check_controls.py` |
| Verdict codes against the baseline | 112 of 112 identical, `--quick` and full run; full run exit 0, 13 min 14 s | `python3 compare/against/verdicts.py <baseline>` |
| Bounded-check rungs, full run | 2 of 96 readings differ, each one rung timed out, none failed (listed above) | `python3 compare/against/bounded.py <baseline>` |
| Were all 7 separations signed | 11 violations would remain (unchanged) | `python3 clausebook/q3b/check.py` |

Logs of this round: `<scratchpad>/q3b-fix-full.log`, `<scratchpad>/q3b-fix-quick.log`, `<scratchpad>/q3b-fix-selftest.log`.
