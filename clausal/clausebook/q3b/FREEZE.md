# Q3b freeze: written before the runs that measure it

Plan node Q3b: settle what can be settled of the 21 violations `python3 -m clausal book check` reports at `492bba6`.
This file fixes the items, the expected outcomes and the tests before the lint is changed and before the recorded runs.

**What was already looked at when this was written (said so that it is not mistaken for a blind freeze).** The seven
pairs below were chosen by compiling candidate sentences in the ledger project, and `clausal separate` was run once on
each (all seven answered SEPARATED). The recorded run is the one made after this commit, by `book check --separate`.
The project-scoped compiler existed in the working tree; no lint change, no bare-hole test and no pipeline run did.

## 1. Cross-system violations (4)

Keys: `it is accepted|l.accepted,w.succeeds`, `the first call is accepted|l.accepted,w.succeeds`,
`the maximum|l.maximum,w.maximum`, `transfer|l.apply,w.transfer`.

Expected: with every sentence compiled against the books of its own project (`projects.yaml`) and the lint counting a
shared skeleton only between entries that some project loads together, all four are no longer reported, and nothing
else changes in the list. Controls, each in memory:

- C1. `A transfer is always accepted` and `For a transfer, it is accepted` each compile to ONE statement in the wallet
  project and to ONE in the ledger project, and are refused AMBIGUOUS when no project is named (every book read).
- C2. A project that lists both `local/ledger.yaml` and `local/wallet.yaml`: the two lines are refused AMBIGUOUS in it,
  and the lint, given that project list, reports the four violations again.
- C3. The wallet's own book given a second operation that carries the noun "transfer": the line is refused AMBIGUOUS in
  the wallet project.
- C4. The term lock: every sentence of `features/` and `controls/` compiles to the recorded term or refusal (125 of 125).

## 2. Pairs that need a separating pair (7)

One entry each under `separations:` of `clausebook/local/ledger.yaml` (core may hold no fixture noun, and a sentence
is read in one project). Each is unsigned. Expected of each: both sentences compile in the ledger project, each is
read with its own piece and not the other, and `clausal separate` answers SEPARATED with the compiled Rust agreeing
with the Lean model at the input recorded.

| id | sentence read with the first piece | sentence read with the second |
|---|---|---|
| `sep.more_than.exceeds` | For a batch for which the length of the batch is more than the total of the ledger's balances, the number of transfers applied is zero | For a batch for which the total of the ledger's balances is more than the length of the batch, the number of transfers applied is zero |
| `sep.not_more_than.at_most_value` | For a batch for which the length of the batch is at most the total of the ledger's balances, the number of transfers applied is zero | For a batch for which the total of the ledger's balances is at most the length of the batch, the number of transfers applied is zero |
| `sep.not_more_than.result_at_most` | (as above, first) | For a batch, the number of transfers applied is at most the length of the batch |
| `sep.at_most_value.result_at_most` | (as above, second) | For a batch, the number of transfers applied is at most the length of the batch |
| `sep.is.result_is` | A batch for which the total of the ledger's balances is the length of the batch never changes the ledger | For a batch, the number of transfers applied is the length of the batch |
| `sep.within.covers` | For a batch, every transfer at which the batch stopped is a transfer of the batch | For a batch, every transfer of the batch is a transfer at which the batch stopped |
| `sep.same_answer.same_answer_if` | A transfer gives the same answer when the amount is the same or larger | A transfer gives the same answer when the amount is the same or larger, if the first call is rejected |

Expected effect on the count: none. An unsigned separation lifts nothing; the five violations these seven pairs
belong to stay, each naming its proposal. A proposal whose machine check fails is a violation of its own.

## 3. Bare-hole forms (1 violation, 7 pieces, 21 pairs)

Question: can two bare-hole forms of different pieces accept the same text at the same type?

Claim to be proved from the parser and tested: no, when the (category, position) pairs the two forms are registered
under are disjoint, because the parser tries a form only at exactly the category and position it is registered under.

Tests fixed here:

- T1 (parser, over the book). Universe: every span of whole words of every step and Rule line of `features/` and
  `controls/` and of the fourteen sentences above, plus every sample literal of `glossary.yaml` and every role phrase.
  For every system, every operation of it (scenario mode and rule mode) and every (category, position) at which a
  bare-hole form is registered: no text of the universe is read by the bare-hole forms of two different pieces.
  Expected: 0.
- T2 (the sentence-level worry). The same universe: how many texts parse, strictly, at two instances of one generic
  category (`term<num>` and `term<optnum>`, and so on)? Reported whatever it is; not expected to be 0 (a literal
  amount is both). For each, whether a sentence of the universe that contains it compiles to more than one statement
  (expected: none, since such a line is refused AMBIGUOUS).
- T3 (control of the rule). In memory, a second bare-hole form of the same type as `amount_value` (`{x:amount}` as a
  `term<num>`): the lint reports the pair, and a sentence that needs it is refused AMBIGUOUS.

If T1 is 0 and T3 fires: bare-hole forms registered at disjoint types are no violation, as a checked rule of the lint
(21 pairs, 1 violation cleared). Otherwise the violation stays and the reason is reported.

## Expected count

21 before. After: 16 (four cross-system and the bare-hole one cleared), if section 3 holds; 17 if it does not.

## Verdicts

Every verdict code of the baseline graph is expected unchanged (`compare/against/verdicts.py`).
