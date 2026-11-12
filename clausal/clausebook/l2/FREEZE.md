# L2 freeze: the three pieces, their one form each, the fixture rules and their expected verdicts

Written and committed BEFORE any pipeline run (`./run.sh`, grid search, property test, bounded check) on the new
rules. Until this commit the new sentences had only been compiled (sentence to Lean text and echo) and the toy
comparison of `lean/Run/FrameToyTests.lean` had been run. Results go in `README.md` beside this file.

## Pieces and forms (frozen)

| Piece | Kind, book | Position | The one form | Lean |
|---|---|---|---|---|
| `equals` | modifier (condition), core | any step | `{a:term<T>} equals {b:term<T>}` | `{a} = {b}` |
| `equals`, negated | same entry | any step, negated | `{a:term<T>} differs from {b:term<T>}` | `¬ ({a} = {b})` |
| `each_at_most` | frame 17, core | Then; in a Rule through "for <subject>, <claim>" | `each of {ns:nums} is afterwards at most {t:term<num>}` | `Frames.EachAtMost {op} {ns} {t}` |
| `tied` | modifier on the operation, core | Rule subject, after a sequence | `{op} with {t:tie}` | `({op}).tied {t}` |
| `same_input` | the one tie core supplies | fills `{t:tie}` | `the same input` | `Frames.sameInput` |

`tied` needs a word of the new category `tie` to be usable at all; `same_input` is that word. No ledger-pack or
local entry is added. No existing form or entry is changed (one category description, `nums`, gains four words).

The forms were written from the kind of claim (the classification table of `trials/sentences/RESULTS.md` and the
scout's brief), not from the trial sentences. Which of them coincide with a trial sentence is measured after this
commit by compiling the 48 as written, and reported.

## Fixture rules and expected verdicts (frozen)

Expected verdict codes are the report's: PROVED-FOR-ALL, TESTED-ONLY, REFUTED.

| id | file | piece | true? | expected |
|---|---|---|---|---|
| `l2_same_account_rejected` | ledger_rules | equals | true | PROVED-FOR-ALL |
| `l2_zero_amount_rejected` | ledger_rules | equals | false | REFUTED |
| `l2_distinct_accounts_accepted` | ledger_rules | equals (negated) | false | REFUTED |
| `l2_each_within_maximum` | ledger_rules | each_at_most | true (near-trivial: u64) | PROVED-FOR-ALL |
| `l2_each_within_total_bound` | ledger_rules | each_at_most | true (needs conservation) | PROVED-FOR-ALL |
| `l2_each_within_amount` | ledger_rules | each_at_most | false | REFUTED |
| `l2_twice_conserves` | ledger_rules | tied | true | PROVED-FOR-ALL |
| `l2_twice_changes_nothing` | ledger_rules | tied | false | REFUTED |
| `l2_deposit_then_withdraw_answers` | wallet_rules (new file) | tied | true | PROVED-FOR-ALL |
| `l2_deposit_then_withdraw_restores` | wallet_rules | tied | false | REFUTED |

Rule for the five true rules, fixed now: a proof of the generated obligation is attempted for each. One whose
proof file does not compile without `sorry` when this node ends is tagged `@expect-unproved`, its expected verdict
becomes TESTED-ONLY, and it is reported as not shown. That decision is taken from the proof file alone, never from
a test result. No rule's sentence, no Clausebook meaning and no REFUTED expectation is changed after this commit;
if a rule expected REFUTED is not refuted, or a rule stated true is refuted, that is reported as it is.

Counts expected: 10 new Rule lines (8 in `features/ledger_rules.feature`, 2 in the new
`features/wallet_rules.feature`), no new scenario. Every verdict code of the baseline (97) is expected unchanged.

## The eleven pieces needed by one or two trial rules (judged, none built)

| # | Piece (generic name from `trials/sentences/run_v4.py --print`) | Rules | Judgement |
|---|---|---|---|
| 1 | frame: holds after any sequence of any operations (invariant of the state) | 2 | Compose, as a rule pack (K1): one preservation rule per operation ("an X for which P ... P afterwards"). Not a piece: a model of one call has no "any sequence" and no first state |
| 2 | modifier: conjunction of two conditions | 2 | Add later, core. Needs a connective that is not the claim separator " and " |
| 3 | frame: compare the answers or final states of two sequences | 2 | Add later, core: a two-run frame whose two runs are two (tied) sequences. Wait for S1b and K1 to say which comparisons are needed |
| 4 | domain word: a condition naming what another operation answers on the same input | 1 | Reject as a condition (it puts the code inside a scope). The same content is sayable as "agrees with <reference that is the other operation>" |
| 5 | domain word: "every transfer of the batch can be applied in order" | 1 | Add later, local book of the ledger (a fold of `valid`, written without the code) |
| 6 | modifier: a quantity of the state before the call used as the expected result | 1 | Add later, core: one coercion from a measure to a value known before the call. It would also let `equals` compare a measure |
| 7 | modifier: an exact-sum condition (X plus Y is Z) | 1 | Add later, core, as a term "X plus Y" rather than a third sum condition; `sum_within` and `sum_exceeds` could then be retired by replacement |
| 8 | domain word: a further reference function | 1 | Add later, local book, when the rule is wanted. No new kind |
| 9 | domain word: a further measure of the state (the number of accounts) | 1 | Add later, ledger pack. No new kind |
| 10 | modifier: scope a claim by a class of answers other than accepted / rejected | 1 | Reject for now: it is a fourth constructor of `Frames.Calls` and reopens Q1 and Q2 (coverage lines, vacuity). Revisit with S1 |
| 11 | domain word: an answer class ("stopped early") | 1 | Add later, local book. Usable today in "always", "never" and the two-run frames; not as a scope (row 10) |

## Addendum after the freeze (fix round, 2026-11-12): a limit of `tied` the freeze did not state

Nothing above is changed. Added after review of the first L2 commit:

- A narrowing word on the subject of a tied sequence ("an accepted <operation> followed by <operation> with
  <tie>") is REFUSED (UNSUPPORTED, code NARROWED-TIE). The first L2 commit compiled it to a statement about
  sequences whose LAST call is accepted, while the word reads as said of the first call. See `README.md`, section
  `tied` and "Limits".
- No fixture rule, form, entry meaning or expected verdict is affected: none of the ten rules has a narrowing word.
