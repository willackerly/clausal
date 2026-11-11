# New sentences and generated echoes: results of the proxy trials (plan nodes V4 and V5)

Run on 2026-11-11. **Every author and every reader in these trials is a language model.** Nothing here is evidence about people; the files are set up so that people can take both trials unchanged (last section).

Anyone who is going to take the echo trial should not read this file first: it discusses how the tool reads one sentence that is in that trial.

## Result

- **V4, do new sentences compile:** 0 of 48 rules written without sight of the vocabulary compile as written. After rewording by someone who knows the vocabulary, 27 (56%) compile whole, 3 in part, and 18 (38%) need a piece the vocabulary does not have. The rewordings are rewrites: a median of 20 words changed, in the 30 reworded sentences, whose median length is 22.5 words (21 over all 48).
- **V4, wrong readings:** none of the 30 compiled readings is contradicted by its author's cases (0 of 150). This says little, because every reading was chosen by the reworder and most cases are ones where the rule simply holds. The one reading the tool chose by itself that the authors did not mean (an unspecific "transfer" read as the wallet's) is not contradicted by any case.
- **V5, do readers catch a wrong echo when the tool wrote it:** four model readers caught 55 of 60 mutated echoes (91.7%; 76.7% to 100% when items and readers are both resampled) and raised 3 false alarms in 120 (2.5%; 0% to 7.5%). At these sample sizes this cannot be told apart from the catch rate on K1's hand-written echoes (73 of 80, 91.2%). That is not evidence that the two rates are equal: the banks differ in sentences, error kinds and readers.
- **What slips through:** all five misses are echoes where a condition was dropped or the calls covered were narrowed. The three mutation kinds that put a wrong word in the claim were caught 36 of 36 times.
- **One false alarm points at a reading choice.** E11 is an unspecific "transfer" read as the wallet's, with "all balances" as the two named wallets. The other two (E33, E45) are about wording only: "larger" and "smaller" are echoed as "at least" and "at most", but an equal amount is the same call, so the claim is the same either way. On the faithful items no one flagged in advance there were 0 flags in 100 judgements.

Plan targets, as signals: V4 asks for at least 75% compiling with no new piece (fail below 50%); the measured 56% is after heavy rewording, and 0% without. V5 asks for at least 90% caught and at most 10% false alarms; the false-alarm rate is inside, the catch rate is "unclear" (point estimate above, interval reaching below).

## Who made what

| role | who | note |
|---|---|---|
| V4 authors | 4 models: opus-1, sonnet-1, haiku-1, default-1, 12 rules each | saw a prose description of the code, not the vocabulary; five cases per rule recorded first |
| V4 reworder and case encoder | a fifth model run | had read the vocabulary |
| V5 bank builder | the same fifth run | chose the mutations by hand; the echoes are the tool's |
| V5 readers | 4 models: haiku-1, sonnet-1, opus-1, default-1 | saw only the bank's brief and items |
| analyst (this file, the V5 notes) | a model on the session default | |

The plan asks for V4 rules from at least 20 people and for V5 to be read by people. Neither has happened.

## V4: held-out sentences

`python3 run_v4.py --print` prints the full tables from `results.json`, rule by rule.

| | pooled | opus-1 | sonnet-1 | haiku-1 | default-1 |
|---|---|---|---|---|---|
| Rules (meant true / meant false) | 48 (38 / 10) | 12 (9 / 3) | 12 (10 / 2) | 12 (10 / 2) | 12 (9 / 3) |
| Compile as written | 0 | 0 | 0 | 0 | 0 |
| Compile whole after rewording | 27 (56%) | 7 | 6 | 8 | 6 |
| Compile in part only | 3 (6%) | 0 | 2 | 1 | 0 |
| No rewording keeps the meaning | 18 (38%) | 5 | 4 | 3 | 6 |
| Need a new piece, for all or part | 22 (46%) | 6 | 6 | 4 | 6 |
| Median words changed (min to max) | 20 (4 to 45) | 19 | 21.5 | 19 | 17.5 |
| Authors' cases: agree / silent / contradict | 143 / 7 / 0 | 34 / 1 / 0 | 40 / 0 / 0 | 39 / 6 / 0 | 30 / 0 / 0 |
| Found true or false as the author labelled | 30 of 30 | 7 of 7 | 8 of 8 | 9 of 9 | 6 of 6 |

With 48 rules, 27 compiling is 56% with a 95% Wilson interval of 42% to 69%; the four authors range from 50% to 67%.

**As written, the tool refuses everything.** All 48 are UNBOUND. 35 refusals offered only the list of operation nouns; 13 offered three nearest forms, and in 3 of those one began like the rewording that was eventually used. 17 of the 48 sentences open with a gerund ("Applying a transfer ..."), which the grammar has no place for, so part of the 0% is surface form and part is missing pieces; the trial does not separate the two.

**How much rewording.** The smallest is 4 words ("An accepted transfer never changes the sum of all balances in the ledger" became "A successful transfer never changes the total of all balances of the ledger"). The median rewording changes 20 words; the 30 reworded sentences have a median length of 22.5 words. Of the 27 whole rewordings, 23 say what the sentence says as far as its cases show and 4 say more. One of the 23 (haiku-1/R08) is exact on correct code only: where the author wrote "applying its transfers one at a time", the reading's reference is another operation of the same code, so it is a relation between two code operations.

**Pieces the vocabulary lacks**, by how many rules need them:

| rules | piece |
|---|---|
| 5 | a comparison between two values known before the call (sender is receiver; amount is zero) |
| 5 | "every balance" or "every account" inside a claim about a quantity |
| 5 | a sequence of calls whose inputs are tied (the same input again, the reverse, the other order) |
| 2 | an invariant over any sequence of any operations |
| 2 | a conjunction of two conditions |
| 2 | comparing the answers or final states of two sequences |
| 1 each | eight more, listed by `run_v4.py --print` |

**Wrong readings.** None by the plan's definition (a compiled reading contradicted by one of its author's cases). The nearest thing:

- "A transfer never changes the total of all balances" is two authors' ledger rules with only the words the grammar cannot place removed.
- The tool compiles it as the **wallet's** two-party transfer and reports no ambiguity.
- No case contradicts that reading. One case of five (a transfer naming a missing account) cannot be expressed in it, which is the only signal.

**Why the wrong-reading check is weak here.** 143 of the 150 cases are ones where the rule holds on correct code, and a holding case cannot expose a reading that is too weak. Only 2 of the 10 rules meant false compiled (both were found false by the search, the property test and Kani); the other 8, and 10 of the 38 meant true, need a missing piece. The rules that would stress the readings most are the ones that did not compile.

**"Found true" is not "proved".** The 28 compiled rules meant true were not falsified on the search grid or in 10,000 property-test cases each. Kani verified 49 of 63 generated harnesses, failed 6 (the two false rules) and gave no answer in 30 s for 8.

Two gaps in the pipeline turned up: a rule whose clauses are about two different operations is compiled and echoed but neither searched nor given a harness; and the replay reports a call outside "successful" or "rejected" as "holds".

## V5: the echo trial on the tool's own echoes

The bank is `../meaning/banks/generated-echoes-v1/`: 45 items, each a Rule line that compiles, shown with an echo printed by the tool. 30 echoes are the tool's output unchanged. 15 are the tool's echo generator run on the rule's composition tree after one mechanical mutation, three items for each of five kinds. The full report, which names items and so gives the key away, is `REPORT.md` in that directory (git-ignored); `SUMMARY.md` there has the rates with no item named.

| | caught | false alarms |
|---|---|---|
| pooled, 4 proxy readers | 55 of 60 (91.7%) | 3 of 120 (2.5%) |
| 95% interval, judgements taken as independent (too narrow) | 81.9% to 96.4% | 0.9% to 7.1% |
| 95% interval, items resampled | 83.3% to 98.3% | 0.0% to 5.8% |
| 95% interval, items and readers resampled | 76.7% to 100% | 0.0% to 7.5% |
| per reader (haiku-1, sonnet-1, opus-1, default-1) | 12, 14, 14 and 15 of 15 | 1, 0, 2 and 0 of 30 |

| mutation kind (3 items each) | caught | items and readers resampled |
|---|---|---|
| a quantity becomes a neighbouring one | 12 of 12 | 100% (every judgement the same) |
| a party becomes the other party | 12 of 12 | 100% |
| strict becomes non-strict or the reverse | 12 of 12 | 100% |
| every call becomes successful calls only | 10 of 12 | 50% to 100% |
| a condition is dropped | 9 of 12 | 33% to 100% |

- **What slips through.** The five misses are all of the last two kinds, where the claim line of the echo is right and the difference is in the slot that says which calls are covered or what is assumed. In three of the five the reader's reason describes a condition that the echo does not contain: the reader restated the rule and attributed it to the echo, at stated confidence 0.85.
- **Dropped conditions were missed in K1 too.** K1 caught them 19 of 24 (79%). K1's weakest kind was a wrong quantity (4 of 8, a single item, E25); here a wrong quantity was caught 12 of 12.
- **Split items.** Readers were unanimous on 38 of 45 items. The seven splits are the four missed mutated items and three unmutated ones.
- **False alarms.** All three are on unmutated echoes that the bank builder had flagged before any reader answered, as places where the tool's reading says something the sentence does not plainly say (one is the wallet reading above; two are a strict word echoed as non-strict, which states the same claim because an equal amount is the identical call). On the 25 faithful items with no flag: 0 of 100. One reader who did not flag the two comparison items saw the same difference and judged it harmless.
- **The wallet reading got past three of four readers.** They accepted the echo's "wallet" framing of a sentence that does not say which transfer. The echo shows what the tool chose; it did not prompt these readers to ask whether another choice existed.

**Machine-written against hand-written.** K1's hand-written echo items: 73 of 80 caught (91.2%), 0 of 160 false alarms, eight proxy readers. V5: 55 of 60 (91.7%), 3 of 120. The tool's echoes are several times longer and proxy readers caught wrong ones about as often. The comparison is loose: different sentences, different error kinds, no composition errors in V5, and V5's rules are lines that already compiled and so sit close to the echo's own wording.

## What model authors and readers can and cannot tell us

**Can:**

- That the whole pipeline runs on sentences nobody on the building side wrote, and on echoes nobody edited; and where it stops (refusal messages, the two pipeline gaps).
- Which pieces are missing for plausible rules about these fixtures. Four model authors independently needed the same three pieces five times each.
- That surface form matters: none of four models, asked for plain English, produced a sentence the grammar accepts.
- That an unspecific noun can compile silently as the other fixture's operation.
- Which kinds of wrong echo a careful comparison of wording finds, and which it reads past. The dropped-condition result has now appeared in two banks.
- That the harness, the brief and the scoring work end to end on a generated bank, so the people trial needs no new code.

**Cannot:**

- How often a person's sentence compiles, or how much rewording a person tolerates. The 56% is what the vocabulary can say when an expert rewrites the sentence, not what an author gets.
- Whether a person would accept the rewordings as their own meaning. No author, model or person, was shown their rewording; "fit" was judged by the reworder against five cases.
- How often people catch a wrong echo. Model readers do not tire, do not skim as people do, and sometimes describe text that is not there; none of these has a known counterpart rate in people.
- How often the tool's echo is wrong in use. The unfaithful items are five mechanical mutations chosen by hand, single-piece only.
- Anything about independence. The four authors and four readers are four models from one family, the reworder, bank builder and analyst are a fifth run from the same family, and the one reader with a perfect score is on the builder's model setting.
- Anything about real systems. The wallet and ledger are fixtures; four of the authored rules are trivially true only because the fixture's maximum is the type's maximum.

Both trials are exploratory by the plan's own rules: the V5 items were chosen by the bank builder (rule 2), and neither item set was committed before its measured run (rule 1; the V5 material hash `478d24c8...51c6` was fixed before the readers answered, and the answers are stored against it).

## Trades these results put on the table

| choice | gain | cost |
|---|---|---|
| Widen the grammar's surface (gerund subjects, synonyms such as accepted / successful, sum / total) | some of the 0% as written may be only this; cheap to measure on the same 48 | more forms to keep unambiguous |
| Add the three pieces five rules each need | touches 15 of the 22 rules that need a new piece; 5 of the 15 also need a second piece | each new piece needs its echo, its executable reading and its place in the V5 mutation set |
| Report an ambiguity when a noun names operations in two fixtures | removes the one silent wrong choice found | more questions to the author |
| Make an empty Assuming slot, or a narrowed Applies-to, stand out when the sentence had a condition | aims at all five misses | longer echoes |
| State how "larger" and "smaller" are read in two-call rules | removes two of three false alarms, or turns them into a fixed convention | none found |

## Next actions

1. Recompile the same 48 sentences after each grammar or vocabulary change (`check_author.py authors.json --compile`), so the 0% as written has a trend.
2. Have a second reworder work blind on the same 48 rules, to see how much of "27 compile" is one reworder's choices.
3. Show each author their rewording and its echo and record whether they accept it. This is the missing half of V4 and needs no new tooling beyond the echo.
4. Build bank version 2: mutations drawn by a seeded rule, at least eight items per kind, composition-level mutants, and an echo change aimed at dropped conditions tested against the current echo.
5. Run both trials with people when available, as below.
6. Update the V4 and V5 rows in `docs/PLAN.md` (outside this step's directories).

## Redoing it with people, unchanged

**Authors (V4).**

1. Give the author `AUTHOR_BRIEF.md` (one page) and `author_template.json`, and nothing else from this repository.
2. Check what comes back: `python3 check_author.py THEIR_FILE.json`.
3. Compile it exactly as written: make the scratch copy (see `README.md`), then `python3 check_author.py THEIR_FILE.json --compile`. This is the "compile as written" row and needs no judgement.
4. The rest is the organiser's work and is the same as for the model authors: add the author to `authors.json`, write a rewording (or the missing piece) per rule in `rewordings.py`, encode the five cases in `cases.py`, and run `python3 run_v4.py`. People and models are reported in separate columns.

The exact prompt the four model authors received was not passed to this step. `AUTHOR_BRIEF.md` is written from what `authors.json` records about it (a prose description of the code, twelve rules, a true or false label, five cases first) and from the description of the code in the V5 brief. It is the brief to use from now on, for people and for any further model authors.

**Readers (V5).** From `../meaning/`:

```sh
python3 build_html.py --bank banks/generated-echoes-v1 --kit /some/folder   # reader kit: take_trial.py, items.json, brief.md, trial.html; no key
python3 take_trial.py --bank banks/generated-echoes-v1 --reader NAME        # terminal
open banks/generated-echoes-v1/trial.html                                   # browser, offline
python3 score.py --bank banks/generated-echoes-v1                           # REPORT.md, SUMMARY.md, results.json in the bank
python3 run_tests.py --bank banks/generated-echoes-v1                       # the whole chain on this bank, in a temporary directory
```

The reader sends back one file, which goes in `banks/generated-echoes-v1/responses/`. People are scored by the same code and reported in their own section, never pooled with the models.
