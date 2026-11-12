# Q4: the first batch of rewordings, applied by replacement

Plan node Q4 (with Q8's controls and Q5's report). The rows, the choices and the test were fixed in `FREEZE.md` before
anything was applied. This file says what was built, what was found on the way, and what is left. Numbers are in
"Results"; every one names the command that reproduces it. Run commands from `clausal/`.

## What a writer sees

- **One live form per piece per position.** The old form of each row is gone from the book.
- **A sentence written the old way is refused** with status `UNBOUND`, code `RETIRED-FORM`. The message names each
  retired form and what replaced it. The hint says `write the clause as: "…"` only if the rewritten clause is one
  statement where the refused line stands: in the system of the scenarios beneath the Rule, or, with no scenario
  beneath it, in every system of the book. If it would read in two systems the hint says so and how to say which;
  if it does not compile the hint says to use the form named.
- **A Rule line narrows on its subject only**, and says each frame in one voice: the verb phrase if the frame has one
  with the same holes, else "for <subject>, <Then form>". A Then step is unchanged: it still takes "if it is rejected,".

Example: `For a transfer, if it is rejected, the ledger is unchanged` is refused, with
`write the clause as: "a rejected transfer never changes the ledger"`.

## How it is built

| What | Where |
|---|---|
| Retired forms | `retired: [{in, was, now}]` in the entry the form belonged to, so under that entry's digest. Never read when a sentence is compiled |
| The refusal | `vocab.Compiler.explain`: only after a sentence was refused, it is read once more against the book with the retired forms put back (`Vocabulary.legacy_voc`). If that reads it, the refusal names the forms. The second reading never yields a statement |
| The rewritten clause | `Compiler.canonical` and `Compiler.surface`: the parse tree written back with the live form of each piece. `Compiler.compiles` reads it, with the book as it stands, in every system the line is read in (`_rule`); `Compiler.retired` offers it only if exactly one reads it |
| One sentence, two systems | `Compiler._rule`: an AMBIGUOUS refusal whose readings are of several systems names them and says how to settle it (`Compiler.which_system`) |
| One voice per frame (row 12) | `g.rule_for`, `reads: no_verb_phrase` |
| Narrowing on the subject (row 4) | `g.rule_for`, `narrowing: on_subject` |
| "every X is not P" (row 11) | `every_of`, `negated: { p: none_of }` |
| "never loses that it is accepted" (row 14) | `monotone`, `implied_only: true`; the class says `same_as: accepted`, which the loader checks against the kernel-checked `narrowing:` facts of each operation |
| "if the first call is rejected" (row 15) | a positional form of each class, `first_call_forms` / `first_call_not_forms`; the frame's hole is written `{c:class@first}` |
| "an accepted internal transfer" | a subject takes one narrowing word, then `internal`. Any other pair is refused (`NARROWED-TWICE`) |

Each of the four shape rules is a line of the book: with the line taken out, the sentence compiles again (selftest).

## Rows

| Row | State | Note |
|---|---|---|
| 1 | done | 5 Rule lines |
| 2 | done | no fixture line used the retired forms |
| 3 | done, at a cost | 6 steps. One kind of Rule line that compiled before is now AMBIGUOUS when it stands with no scenario beneath it. See "the same words in two systems" below |
| 4 | done | no fixture line; 4 control lines changed shape |
| 5 | done | "a", "an" both stay (see violations) |
| 6 | done | 2 lines |
| 7 | done | `l.balances_of`: "{l}'s balances" (16 lines); `l.balance_at`: "the balance of {i} in {l}" (1); `l.the_transfer`: "{t}" (2) |
| 8, 9 | done | 7 and 3 lines |
| 10 | done | 4 Rule lines. Parses once in every probe, alone and inside a line of several clauses |
| 11 | done, and wider than the synthesis says | it also changes the scenario `ledger.feature:39` (Then step, line 42) |
| 12 | done | 1 Rule line, which became three clauses (`ledger.feature:66`) |
| 13 | done | 5 steps |
| 14 | done | by refusal; both forms of `monotone` stay |
| 15 | done | 2 Rule lines. Parses once |
| 16 to 18 | not applied here | README text; the proposed sentences are returned to the orchestrator |
| 19 | done in part | see "Not done" |

## Found on the way (none of it is in the synthesis)

1. **Row 11 reaches a scenario.** `Spec.ledger.batch_stops_at_invalid` is written with the same form, so two readings
   change term, not one. Both keep their verdict.
2. **The old whole-phrase glossary binds scenario steps by their exact words.** Eleven `phrase:` texts of
   `glossary.yaml` were reworded in step with the steps; no `lean:` binding changed.
3. **The same words in two systems.** With row 3 the wallet and the ledger both say "it is accepted".
   - Old glossary: a Then that matches several phrases is the one written for the kind of answer the scenario's last
     When gives (`core.bind`).
   - Rust cucumber run: a Then form has one tree per system (`trees.step_entries`, `by_system`), and the generic step
     takes the tree of the system of the scenario's When (`wallet-bdd/tests/bdd.rs`).
   - **A Rule line with no scenario beneath it (found by the reviewer, fix round).** Such a line is read in every
     system. "transfer" names an operation of the wallet and one of the ledger. Before row 3, "For a transfer, it is
     accepted" compiled (ledger) and "For a transfer, the operation succeeds" compiled (wallet): the wording of the
     class was what said which system. Now the first is AMBIGUOUS and the second is refused as retired. The same holds
     with "accepted" or "rejected" on the subject. No fixture line is affected (each has scenarios beneath it).
     - This is the state "A transfer is always accepted" was already in at `891bf01` (AMBIGUOUS, two systems): the
       cause is the shared noun, and row 3 removed the one wording that happened to work around it.
     - Row 3 was kept. The refusal now names the two systems and the two ways to say which: a scenario beneath the
       Rule, or a noun only one system has ("fund transfer" for the ledger; the wallet has none).
     - The book check counted none of this ("never live in one sentence"). It now counts every skeleton shared by two
       systems that share a subject noun: 4 violations, 2 of them older than this batch.
4. **One scenario stopped being a "new sentence".** `readme_transfer_keeps_aggregate`: its Then, reworded, is a phrase
   the old glossary has, so it now has a flat statement. Its hand-written proof was a proof of the generated
   obligation; it was rewritten as a proof of the flat statement (same argument). Mutation controls c33 and c34, which
   used this scenario as their new sentence, now use `n2_short_sender_rejected`.
5. **Row 12 splits a clause.** `ledger.feature:66` said two things of one subject with "and", one of them
   (`never_changes`) in the "for" voice. The Lean reading is byte-identical; the generated flat obligation of that Rule
   has one more conjunct.
6. **Three entries are no longer used by any fixture sentence:** `every_of` (its only uses were with "not"), `g.claims`
   (" and " between two claims; the one clause that used it was split by row 12) and default `D9`. `g.claims` has a
   control in the selftest; the other two have none.
7. **The expert rewordings of the sentence trial are written with the old forms.** 11 of the 30 in
   `trials/sentences/rewordings.py` are now refused. Nothing under `trials/` was edited.

## Results

All measured 2026-11-12. Rows that the fix round changed were measured again on the fix-round commit; the full-run rows below it are of `5e2ee50` (the fix round's own full run is under "Fix round").

| What | Result | Command |
|---|---|---|
| Fixture lines rewritten | 51 of 226, as frozen | `python3 clausebook/q4/count.py 891bf01` |
| Lean reading of every scenario and Rule line of `features/` | 85 compilations (83 compiled, 2 refused, as before); 83 Lean statements, 81 identical, 2 differ (row 11: `Rule.ledger_rules.n5_stopped_at_invalid`, `Spec.ledger.batch_stops_at_invalid`). The script prints 3 differences: the third is the message of a line refused before and now (`Rule.wallet.interest`), which lists "accepted" where it listed "successful" | `python3 compare/against/readings.py 891bf01` |
| New AMBIGUOUS or ILL-TYPED | 0 | same |
| Term lock, `features/` and `controls/` | 111 sentences; 109 unchanged (same term, or same refusal status and code); the 2 row-11 terms rewritten | `git diff 891bf01 -- clausebook/terms.lock.json` |
| Verdict codes, `--quick` run | 97 of 97 identical to the baseline | `python3 compare/against/verdicts.py <baseline graph.json>` |
| Verdict codes, full run | 97 of 97 identical to the baseline; 9 of 83 readings differ in bounded-check rungs (listed under "Full run") | same; `python3 compare/against/bounded.py <baseline graph.json>` |
| `clausal book check` violations | 34 before, 21 now. 17 after the batch; 4 more since the fix round counts skeletons shared across systems (2 of those 4 existed before the batch and were not counted; 2 come from row 3) | `python3 -m clausal book check` |
| Proposed separating pairs | 7 of 7 separate; signed, they would leave 16 violations | `python3 clausebook/q4/check_separations.py` |
| Rule lines that compiled at `891bf01` and are AMBIGUOUS now, with no scenario beneath them | "For a [accepted / rejected] transfer, it is accepted" (and the same claim joined to others). Not counted over all sentences. A probe of 1386 generated lines (7 subjects, conditions over 7 to 9 measures each, "the maximum" among them; none says "it is accepted") has 0 AMBIGUOUS before and after the fix | selftest, "Q4 fix" checks; the probe is the reviewer's and is not in the repo |
| Sentences quoted in the two READMEs | 6 quoted texts begin like a Rule line; 2 compile, 2 are no sentence of the book (meant), **2 are refused as retired** (`README.md:53`, `:54`; the root README is not edited here) | `python3 clausebook/q4/docs_check.py` (exit 1 while any is retired) |
| Selftest | all checks pass, among them 21 old Rule lines refused with the clause to write, the 4 shape lines, Q8's 4 controls, Q5, and the 4 checks of the fix round (48 offered clauses, each one statement where it was offered) | `python3 -m clausal.selftest` |
| Removal sweep | 246 removals; 0 leave a sentence that uses the entry unchanged; 11 change no recorded term | `python3 mutation/removal_sweep.py` |
| Mutation controls whose text changed | c17, c20, c24, c27, c33, c34, c35, c39: 8 of 8 as expected | `python3 mutation/run_mutants.py --only c17,c20,c24,c27,c33,c34,c35,c39 --jobs 2` |
| Controls the book check stops | c39 to c42, as meant | `python3 mutation/check_controls.py` |
| The 48 frozen sentences, as written | 0 of 48 before; 0 of 48 now; none is refused for a retired form. **Contaminated measure** (critique B11): the batch's rules coincide with wording in up to 13 of them | `bash clausebook/q4/sentences.sh` |
| The 30 expert rewordings | 30 compile before; 19 now; 11 refused as `RETIRED-FORM`, each with the clause to write. Rewritten by following the refusals, 11 of 11 compile to the Lean they had before | same |
| Duplicate report (Q5) | 83 compiled sentences, 2 groups: `ledger_rules.feature:14` with `:29`; `:67` with `:166` (the same sentence since row 11) | `python3 -m clausal duplicates` |
| Open question 3 | 3 candidate wordings, each 11 of 11 probe sentences compile to today's statement | `python3 clausebook/q4/oq3_probe.py` |

### Full run

One full `./run.sh` (12 min 5 s, load average about 5 to 6, other agents building), exit 0: "every scenario got its
expected verdict and every Rule statement its expected one". 39 scenarios, 46 rule statements (28 PROVED-FOR-ALL,
15 REFUTED, 1 UNBOUND, 2 TESTED-ONLY).

- **Verdict codes: 97 of 97 identical to the baseline** (39 scenarios, 46 rule groups, 12 functions), the two row-11
  readings among them (`python3 compare/against/verdicts.py <baseline graph.json>`).
- **Row 11, rerun.** `Rule.ledger_rules.n5_stopped_at_invalid`: PROVED-FOR-ALL before and after (its hand-written proof
  of the obligation still has the obligation's type; the obligation differs only in brackets).
  `Spec.ledger.batch_stops_at_invalid`: PROVED-FOR-ALL before and after (the generated equivalence between the new
  reading and the unchanged flat statement is kernel-checked). Neither has a bounded-check difference.
- **Bounded checks (Kani): 9 of 83 readings answered differently** (`python3 compare/against/bounded.py <baseline graph.json>`).
  In every one a rung that was verified in the baseline timed out here (30 s limit); no rung failed, none was gained.
  The generated Rust check of each of the nine is unchanged (`git diff 891bf01 -- evidence/src/checks.rs` touches
  only the two row-11 checks and the split clause of `batch_count`). Sizes are accounts x transfers:

| Reading | Verified in the baseline | Verified here |
|---|---|---|
| `Rule.ledger.batch_total` | 2x1, 2x2, 4x1, 2x3 | 2x1, 2x2 |
| `Rule.ledger_rules.some_valid_conserves` | 2x1, 2x2, 4x1, 2x3 | 2x1, 2x2 |
| `Spec.ledger.batch_conserves` | 2x1, 2x2, 2x3 | 2x1, 2x2 |
| `Spec.ledger.batch_then_total_overflow` | 2x1, 2x2, 4x1, 2x3 | 2x1, 2x2, 2x3 |
| `Spec.ledger.whole_conserves` | 2x1, 2x2, 4x1, 2x3 | 2x1, 2x2, 2x3 |
| `Rule.ledger_rules.n1_internal_transfer` | 2, 4 | 2 |
| `Rule.ledger_rules.readme_internal_transfers` | 2, 4 | 2 |
| `Spec.ledger_rules.f_other_account_untouched` | 2, 4 | 2 |
| `Spec.ledger_rules.readme_transfer_keeps_aggregate` | 2, 4 | 2 |

### Fix round (after review)

Three defects were reported by a reviewer on another model. What was done:

1. **Row 3 makes a Rule line read in two systems; the book check did not count it.** True. Row 3 kept; the refusal now
   says what the two systems are and how to say which; the book check counts it (4 violations, above). See "the same
   words in two systems".
2. **A refusal offered a clause that does not compile where it stands.** True: the rewritten clause was compiled in the
   one system of the retired form. It is now compiled in every system the refused line is read in, and offered only if
   exactly one reads it. Selftest: 48 offers (25 old Rule lines, each with no scenario and under a scenario of each
   system), every one a single statement in the place it was offered for.
3. **The root README quotes two sentences now refused; `clausal/README.md` said 4 scenarios have no old entry.** True.
   The count is corrected (3 of the 4). The root README is not edited here: see "Not done". `docs_check.py` finds such
   sentences from now on.

One full `./run.sh` on the fix (8 min 29 s, load average about 6 to 7), exit 0, same closing line and the same counts
of verdicts as above. Verdict codes: 97 of 97 identical to the baseline. Bounded checks: 3 of 83 readings answered
differently from the baseline, each by one rung verified or timed out (30 s), none failed:

| Reading | Verified in the baseline | Verified here |
|---|---|---|
| `Rule.ledger_rules.some_valid_conserves` | 2x1, 2x2, 4x1, 2x3 | 2x1, 2x2, 2x3 |
| `Spec.ledger.batch_conserves` | 2x1, 2x2, 2x3 | 2x1, 2x2, 4x1, 2x3 |
| `Spec.ledger.batch_then_total` | 2x1, 2x2 | 2x1, 2x2, 2x3 |

**Q5 on the critique's pair.** "A batch applied as a whole is always accepted" and "For a batch applied as a whole, it
is accepted" are reported together, with "DIFFERENT Lean text, equal after unfolding" (selftest). The pair can still be
written; see violation 3b below.

**Open question 3.** A variation worded "the amount is the same or smaller on the same ledger", or "only the amount
differs and it is the same or smaller" (with or without a comma), parses once in every probe. None is adopted: which
words state "same ledger, same sender and receiver" best is a reader question (Q7). The second begins with the form of
`l.only_amount_differs`.

**Open question 4.** Settled by rows 4 and 15: "if it is rejected" is part of no Rule line. It remains a prefix of a
Then step, with one meaning (narrowing).

## The 21 violations that remain, and why

A separating pair can clear only check 4, and there only a pair of pieces that one system reads. Nothing was signed.

| Check | Violation | Why it remains |
|---|---|---|
| 1 | `always` "is always accepted"; `never` "is always rejected"; `if_then`, `only_if`, `exactly_when` "is accepted …"; `monotone` "never loses acceptance when" (6) | The form says the class with its own words and the book declares it (`implied:`). No pair can separate a form from itself. Owner's decision: treat `implied` as a declared exemption (as `from_operation` is), or reword |
| 3a | `g.subject`: "a", "an" | Row 5 keeps both |
| 3a | `g.line`: 4 written forms (capital or not, full stop or not) | No row. Making it strict would refuse every frozen sentence that ends in a full stop |
| 3a | `l.apply`: nouns "transfer", "fund transfer" | No row. The README's example sentence uses "fund transfer" |
| 3a | `monotone`: two verb phrases | Row 14 keeps the wording. The second is needed for a class that is not the operation's acceptance (`ledger_rules.feature:78`) |
| 3b | `always`: "X is always accepted" and "for X, it is accepted" | The verb phrase has no class hole, so the Then form stays readable in a Rule line ("for a lookup …, there is no result" has no other form). Q5 reports the pair |
| 4 | "{} is more than {}": `more_than`, `exceeds` | Needs a signed separating pair. Proposed, checked |
| 4 | "{} is at most {}": `not_more_than`, `at_most_value`, `result_at_most` (3 pairs; 1 before row 8) | Needs 3 signed pairs. Proposed, checked |
| 4 | "{} is {}": `is`, `result_is` | Needs a signed pair. Proposed, checked |
| 4 | "every {} is a {}": `within`, `covers` | Needs a signed pair. Proposed, checked |
| 4 | "{}": seven bare-hole forms, 21 pairs | Told apart by the type of the hole alone. 21 signed pairs, or a rule for bare holes: owner's decision. Not proposed |
| 4 across systems | "transfer": `l.apply` (ledger), `w.transfer` (wallet) | Older than the batch; not counted until the fix round. A Rule line about "a transfer" with no scenario beneath it is read in both systems. No pair can separate one sentence from itself. Owner's decision: a noun of its own for one of the two operations, or a rule that such a line must name its system |
| 4 across systems | "the maximum": `l.maximum`, `w.maximum` | As above (older than the batch). No line that reads both was found (3 tries by hand, and the 1386-line probe); it is counted by the rule, not by a witness |
| 4 across systems | "it is accepted": `l.accepted`, `w.succeeds` | Row 3. Witness: "For a transfer, it is accepted". Clears with the noun, or by taking row 3 back |
| 4 across systems | "the first call is accepted": the same two pieces | Rows 3 and 15. No witness found (the wallet has no variation to say it with); counted by the rule |
| 4 head | `same_answer_if` takes the head of `same_answer` ("gives the same answer when") | New check (Q8 control 1). Needs a signed pair. Proposed, checked |

## Not done

- **The root `README.md` quotes two sentences the book now refuses** (lines 53 and 54, rows 7a and 8), under the heading
  "Real rules and machine verdicts produced by the pipeline". It was not edited here (the orchestrator owns it). The
  sentences to put there are the fixture lines `ledger.feature:13` and `wallet.feature:135`; each compiles to the Lean
  the old sentence had. Line 69 ("… are never accepted", an example for a pack that does not exist yet) uses the verb
  phrase row 2 retired; "… are always rejected" is the live one.
- **The cross-system double reading stays** (above). Nothing in the book lets a wallet Rule line about a transfer stand
  with no scenario beneath it.

- **Row 19, the rest of the echo.** The scaffolding of the echo ("applies to", "every …", "a plain Scenario: …") is
  still Python text under no signature. The words it quotes from forms ("always answers", "followed by", the article)
  are now read from the book.
- **The full mutation harness** (83 runs, about two hours under load) was not rerun; `mutation/results.json` is from
  before the batch. Only the 8 controls whose text changed were run.
- **`trials/sentences/rewordings.py`** was not edited; `run_v4.py` will meet 11 refusals until it is.
- **`every_of` and `D9` have no fixture and no control** (finding 6).
- **No person read any new wording.** That is Q7.
- **Historical documents** (`DESIGN.md`, `FINDINGS.md`, `review/`, `compare/`) still quote the old forms.
