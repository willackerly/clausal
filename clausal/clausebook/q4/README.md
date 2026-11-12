# Q4: the first batch of rewordings, applied by replacement

Plan node Q4 (with Q8's controls and Q5's report). The rows, the choices and the test were fixed in `FREEZE.md` before
anything was applied. This file says what was built, what was found on the way, and what is left. Numbers are in
"Results"; every one names the command that reproduces it. Run commands from `clausal/`.

## What a writer sees

- **One live form per piece per position.** The old form of each row is gone from the book.
- **A sentence written the old way is refused** with status `UNBOUND`, code `RETIRED-FORM`. The message names each
  retired form and what replaced it. The hint gives the clause (or the step) rewritten, if the rewritten text was
  checked to compile; otherwise it says to use the form named.
- **A Rule line narrows on its subject only**, and says each frame in one voice: the verb phrase if the frame has one
  with the same holes, else "for <subject>, <Then form>". A Then step is unchanged: it still takes "if it is rejected,".

Example: `For a transfer, if it is rejected, the ledger is unchanged` is refused, with
`write the clause as: "a rejected transfer never changes the ledger"`.

## How it is built

| What | Where |
|---|---|
| Retired forms | `retired: [{in, was, now}]` in the entry the form belonged to, so under that entry's digest. Never read when a sentence is compiled |
| The refusal | `vocab.Compiler.explain`: only after a sentence was refused, it is read once more against the book with the retired forms put back (`Vocabulary.legacy_voc`). If that reads it, the refusal names the forms. The second reading never yields a statement |
| The rewritten clause | `Compiler.canonical` and `Compiler.surface`: the parse tree written back with the live form of each piece. Offered only if `Compiler.compiles` reads it with the book as it stands |
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
| 3 | done | 6 steps. See "the same words in two systems" below |
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

All measured on commit `5e2ee50` plus the two echo lines of the following commit, 2026-11-12.

| What | Result | Command |
|---|---|---|
| Fixture lines rewritten | 51 of 226, as frozen | `python3 clausebook/q4/count.py 891bf01` |
| Lean reading of every scenario and Rule line of `features/` | 85 compilations; 83 identical, 2 differ (row 11: `Rule.ledger_rules.n5_stopped_at_invalid`, `Spec.ledger.batch_stops_at_invalid`) | `python3 compare/against/readings.py 891bf01` |
| New AMBIGUOUS or ILL-TYPED | 0 | same |
| Term lock, `features/` and `controls/` | 111 sentences; 109 unchanged (same term, or same refusal status and code); the 2 row-11 terms rewritten | `git diff 891bf01 -- clausebook/terms.lock.json` |
| Verdict codes, `--quick` run | 97 of 97 identical to the baseline | `python3 compare/against/verdicts.py <baseline graph.json>` |
| Verdict codes, full run | 97 of 97 identical to the baseline; 9 of 83 readings differ in bounded-check rungs (listed under "Full run") | same; `python3 compare/against/bounded.py <baseline graph.json>` |
| `clausal book check` violations | 34 before, 17 now (one of them of a check that is new) | `python3 -m clausal book check` |
| Proposed separating pairs | 7 of 7 separate; signed, they would leave 12 violations | `python3 clausebook/q4/check_separations.py` |
| Selftest | all checks pass, among them 21 old Rule lines refused with the clause to write, the 4 shape lines, Q8's 4 controls, Q5 | `python3 -m clausal.selftest` |
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

**Q5 on the critique's pair.** "A batch applied as a whole is always accepted" and "For a batch applied as a whole, it
is accepted" are reported together, with "DIFFERENT Lean text, equal after unfolding" (selftest). The pair can still be
written; see violation 3b below.

**Open question 3.** A variation worded "the amount is the same or smaller on the same ledger", or "only the amount
differs and it is the same or smaller" (with or without a comma), parses once in every probe. None is adopted: which
words state "same ledger, same sender and receiver" best is a reader question (Q7). The second begins with the form of
`l.only_amount_differs`.

**Open question 4.** Settled by rows 4 and 15: "if it is rejected" is part of no Rule line. It remains a prefix of a
Then step, with one meaning (narrowing).

## The 17 violations that remain, and why

A separating pair can clear only check 4. Nothing was signed.

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
| 4 head | `same_answer_if` takes the head of `same_answer` ("gives the same answer when") | New check (Q8 control 1). Needs a signed pair. Proposed, checked |

## Not done

- **Row 19, the rest of the echo.** The scaffolding of the echo ("applies to", "every …", "a plain Scenario: …") is
  still Python text under no signature. The words it quotes from forms ("always answers", "followed by", the article)
  are now read from the book.
- **The full mutation harness** (83 runs, about two hours under load) was not rerun; `mutation/results.json` is from
  before the batch. Only the 8 controls whose text changed were run.
- **`trials/sentences/rewordings.py`** was not edited; `run_v4.py` will meet 11 refusals until it is.
- **`every_of` and `D9` have no fixture and no control** (finding 6).
- **No person read any new wording.** That is Q7.
- **Historical documents** (`DESIGN.md`, `FINDINGS.md`, `review/`, `compare/`) still quote the old forms.
