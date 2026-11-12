# Q4 freeze: the first batch of rewordings, written before any of it is applied

Plan node Q4 (docs/PLAN.md, "Refresh of 2026-11-12 (draft 7)"). Design source: `docs/studies/2026-11-12/readability.md`,
section 2, rows 1 to 15 and 19. Rows 16 to 18 are README text and are not applied here.

This file is committed before the book, the compiler or any `.feature` file is changed. The tree it describes is commit
`891bf01` (branch `wave/book`). Counts are of the 226 `Rule:` and step lines of `clausal/features/*.feature`, by
`python3 clausebook/q4/count.py` (output kept in `count.before.txt`; `python3 clausebook/q4/count.py 891bf01` reproduces it
later). A line that two rows rewrite is counted under both; 51 different lines are rewritten.

## The rule applied

Replacement, never addition: the old form leaves the book, a sentence written with it is refused, and the refusal names the
new form. Fixture lines are rewritten word for word; no meaning, statement, expected verdict or tag is changed, and no
frozen trial sentence (`trials/sentences/authors.json`, `raw/`) is touched or read for wording.

## Rows

| Row | Piece | Old form (stops being accepted) | New form | Lines rewritten (Rule, step) |
|---|---|---|---|---|
| 1 | `successful`, on a Rule subject | "successful {op}" | "accepted {op}" | 5 (5, 0) |
| 2 | `always`, `never`, verb phrases | "always succeeds"; "is never accepted" | "is always accepted"; "is always rejected" (both exist today) | 0 |
| 3 | `w.succeeds` | "the operation succeeds" | "it is accepted" | 6 (0, 6) |
| 4 | `successful`, `rejected`, before the claim of a Rule line | "for X, if it is accepted, C"; "for X, if it is rejected, C" | refused in a Rule line; "for an accepted X, C"; "for a rejected X, C". A Then step keeps the prefix | 0 |
| 5 | `g.subject` | "every {op}", "any {op}" | "a {op}", "an {op}" | 0 |
| 6 | `aggregate` | "the aggregate {ns}" | "the total of {ns}" | 2 (1, 1) |
| 7a | `l.balances_of` | "the balances of {l}", "all balances of {l}", "account value of {l}" | "{l}'s balances" | 16 (11, 5) |
| 7b | `l.balance_at` | "the balance of account {i} of {l}" | "the balance of {i} in {l}" | 1 (0, 1) |
| 7c | `l.the_transfer` | "the transfer {t}" | "{t}" | 2 (0, 2) |
| 8 | `not_more_than` | "{t} is not more than {m}" | "{t} is at most {m}" | 7 (2, 5) |
| 9 | `sum_within` | "{m} plus {t} does not exceed {z}" | "{m} plus {t} is at most {z}" | 3 (0, 3) |
| 10 | `l.smaller_amount`, `l.larger_amount` | "the amount is smaller"; "the amount is larger" | "the amount is the same or smaller"; "the amount is the same or larger" | 4 (4, 0) |
| 11 | `every_of` with "not" | "every X is not P afterwards" | refused; "no X is P afterwards" (`none_of`) | 2 (1, 1) |
| 12 | `always_answers`, `never_changes`, `rejected_unchanged`, `increases_by`, `decreases_by`, `at_most`, `at_least` | in a Rule line, "for X, <Then form>" | refused in a Rule line; "X <verb phrase>" | 1 (1, 0) |
| 13 | Then forms of `increases_by`, `decreases_by`, `rejected_unchanged` | "{m} is increased by {t}"; "{m} is decreased by {t}"; "it is rejected and nothing is changed" | "{m} is increased by exactly {t}"; "{m} is decreased by exactly {t}"; "it is rejected and changes nothing" | 5 (0, 5) |
| 14 | `monotone` | "never loses that it is accepted when {v}" | refused; "never loses acceptance when {v}". Both forms of the piece stay (wording unchanged) | 0 |
| 15 | `same_answer_if` | "gives the same answer when {v}, if it is accepted / rejected" | "gives the same answer when {v}, if the first call is accepted / rejected" | 2 (2, 0) |
| 19 | forms and printed texts still in Python | refusal and hint texts that quote surface words; the retired forms themselves | read from the book, under the entry's digest | 0 |

## Choices this freeze makes (each is a judgement call, to be logged)

- **Row 7a, which of four forms.** "{l}'s balances". The synthesis prefers role names ("the sender's balance"); it also
  keeps the ledger sentence ("the total of the ledger's balances") visibly apart from the wallet one ("the total of all
  balances"), which matters because "transfer" is a noun of both systems.
- **Row 7b.** `l.balance_at` keeps "the balance of {i} in {l}", so it no longer shares a skeleton with `l.bal_of`
  ("the balance of account {k} of {l}", 0 against absent). This resolves the pair by wording; it is not exempted.
- **Row 7c.** `l.the_transfer` keeps the bare "{t}", because in a Rule line the item is the role phrase "the transfer"
  and "the transfer the transfer" is not a sentence.
- **Row 11 reaches one scenario.** The synthesis names `ledger_rules.feature:67` as the one term change. The Then step
  `ledger.feature:42` is written with the same form, so its reading changes too (`EveryOf … ¬ valid` to `NoneOf … valid`).
  Both are rerun and reported. If the scenario's verdict code changes, the row is applied to Rule lines only and that is
  reported.
- **Row 12, which frames.** A Then form is refused in a Rule line when its frame has a verb phrase with the same holes.
  `always` keeps both ("for a lookup …, there is no result" has no verb phrase), so its check-3b violation stays.
- **Row 12 splits one clause.** `ledger.feature:66` says two things of one subject in the "for" voice, one of which
  (`never_changes`) has a verb phrase. It becomes two clauses with the same subject.
- **Row 4 and `internal`.** "for an internal X, if it is accepted, C" was the one way to narrow an internal operation in
  a Rule line. With the prefix gone it is written on the subject, in one order only: "an accepted internal X".
- **Row 15 needs a positional form of each class** ("the first call is accepted" beside "it is accepted"): allowed by
  section 1 of the synthesis (one form per position, same stem), stored in the class's own entry.
- **Refusal.** Status `UNBOUND`, code `RETIRED-FORM`. Each retired form is recorded in the entry it belonged to
  (`retired:`), so it is under that entry's digest.
- **Old whole-phrase glossary (`glossary.yaml`).** A scenario step keeps its flat statement only while a glossary phrase
  matches it, so the `phrase:` of each rewritten step is reworded in step. No `lean:` binding changes.

## Open questions attempted

- **Open question 3 (a variation wording that states the same state).** Candidates, tried against the parser only, not
  adopted without the owner: "the amount is the same or smaller on the same ledger"; "only the amount differs and it is
  the same or smaller". Reported: parses once, is ambiguous, or is refused.
- **Open question 4.** Settled if rows 4 and 15 land: "if it is rejected" is then no part of any Rule line.

## What must hold afterwards (the test, fixed now)

1. Every scenario and Rule line of `features/` and `controls/` compiles to a Lean statement byte-identical to the one at
   `891bf01` (`python3 compare/against/readings.py 891bf01`), except the two readings of row 11.
2. No sentence that compiled is refused, and none becomes AMBIGUOUS or ILL-TYPED, except control lines whose own
   purpose is a form this batch retires (each listed).
3. Every verdict code equals the baseline (`python3 compare/against/verdicts.py <baseline graph.json>`), the two row-11
   readings reported separately. Bounded-check rungs that answer differently are listed.
4. `python3 -m clausal book check`: zero violations, or each remaining one listed with why it remains.
5. Q8: the four mechanical negative controls of the synthesis (section 3) are refused, each for the stated reason, in
   `python3 -m clausal.selftest`.
6. The 48 frozen sentences are compiled as written in a private copy (`check_author.py authors.json --compile`). The
   count before is 0 of 48 (`trials/sentences/RESULTS.md`). Any rise is contaminated (critique B11) and is labelled so.

No threshold is a number to reach. Items 1 to 3 are pass or fail; 4 to 6 are reported as found.
