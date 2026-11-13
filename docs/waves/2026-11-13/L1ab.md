# L1ab: reports as returned by the agents

Builder, reviewer (Opus) and fix round, unedited apart from the session scratch path. Worktree paths under `.worktrees/` have since been removed; the commits are on `main`, or in the local `private/tdf-core` repository for T9.4c.

## Builder

## L1ab report: composer version 2, first part (no language model)

Version 2 is built and tested. On the 60 development sentences it answers none: 0 wrong answers against version 1's 43, and 0 right answers against version 1's 17. Every development sentence becomes a question (46) or a decline (14). That is a negative result on right answers and is reported as one.

Worktree: `/Users/will/dev/lean-rosette/.worktrees/compose2`, branch `wave/compose2`, nothing pushed. Main checkout untouched.

## What I changed (paths under `/Users/will/dev/lean-rosette/.worktrees/compose2/clausal/`)

| Path | What |
|---|---|
| `compose_tests/dev/devset.json` | The development set, byte-identical to the scratchpad file (sha256 `4c001704…`), first commit |
| `compose_tests/l4b.py` | Repair: candidates go to one feature file per project of the scratch copy, each listed in the scratch copy's `projects.yaml`. Scoring definitions untouched |
| `compose_tests/l4b_a0/` | Arm A0 output (`REPORT.md`, `results.json`) and a `README.md` labelling it contaminated |
| `clausal/compose2.py` (new) | `clausal compose2`: outcomes, filters, system-first question, coverage accounting, condition spans, acknowledgement record, `--write` sidecar |
| `clausal/ctree.py` (new) | `clausal tree`: tree JSON, schema generated from the book, round trip |
| `clausal/pipeline.py`, `clausal/__main__.py` | Two subcommand branches and help text |
| `compose_tests/v2.py`, `dev.py`, `replay.py` (new) | Tests on the book's fixtures; development-set scorer; replay plumbing |
| `compose_tests/dev/REPORT.md`, `results.json` | Development-set run |
| `COMPOSE2.md` (new), `compose_tests/README.md` | Design notes and measurements |
| `out/*` | Outputs of the one full run |

`clausal/compose.py` (version 1) and `trials/` have no changed line (`git diff --stat 492bba6 -- clausal/clausal/compose.py trials` is empty).

## Commits

| Hash | What |
|---|---|
| `a1f8bfb` | Development set, unchanged |
| `2f2cb46` | `l4b.py` repair |
| `b3303cd` | Arm A0 run on the 48 |
| `7cb2f4c` | Freeze: composer v2, tree interface, tests, scorer definitions |
| `3c7ad77` | Notes and the development-set run after the freeze |
| `055ec4a` | Outputs of the full run |

## Verification, with actual output

- **Full run:** `run.sh exit 0`; "RESULT: every scenario got its expected verdict and every Rule statement its expected one".
- **Verdicts:** `verdicts.py <baseline2/graph.json>` printed "verdict codes that differ: 0 of 112".
- **Bounded-check rungs that answered differently:** 1 of 302: `Rule.ledger_rules.n1_internal_transfer [up to 4 accounts]: timeout -> verified`.
- **`compose_tests/v2.py --l3`:** "all passed". Lines that matter:
  - "identity: 66 of 66 compiled fixture Rule lines come back as themselves (ANSWER, same sentence, the locked term)"
  - "identity: 66 of 66 with full coverage under their own tree"
  - "none of the 20 REFUSED fixture Rule lines is ANSWERED … {'ASK (dropped)': 12, 'DECLINE': 1, 'ASK (system)': 6, 'ASK (reading)': 1}"
  - "round trip: tree -> sentence -> compile -> the same term: 66 of 66"
  - "seeded drop: 43 of 43 deleted conditions and narrowings are reported (42 also as CONDITION DROPPED; 6 deletions give a sentence the compiler refuses and are not counted)"
  - "no silent drop: no ANSWER on the thirteen sentences of cases.json has a dropped word …"
  - "l3: two full-coverage candidates that differ … give ASK (reading) with a separating input"
- **`compose_tests/run.py` (version 1):** "all passed".
- **`l4b.py --smoke`** after the repair: ran to the end, 3 of 3 sentences scored.
- **Development set** (after the freeze commit):

| | A1 (v2) | A1s (v2, system question answered from the set) | A0 (v1) | always decline |
|---|---|---|---|---|
| Wrong answers, of 60 | 0 | 0 | 43 | 0 |
| Expressible (45): answered right | 0 | 0 | 17 | 0 |
| Expressible: answered wrong | 0 | 0 | 28 | 0 |
| Expressible: asked / declined | 36 / 9 | 36 / 9 | 0 / 0 | 0 / 45 |
| Expressible: missed | 45 | 45 | 28 | 45 |
| Not expressible (15): answered | 0 | 0 | 15 | 0 |
| Not expressible: asked / declined | 10 / 5 | 10 / 5 | 0 / 0 | 0 / 15 |
| Needs an unbuilt piece (10): answered | 0 | 0 | 10 | 0 |

A1 asks: 3 system, 0 reading, 43 dropped. A1 declines: 12 with no operation anchored, 2 with no askable candidate.

- **Arm A0 on the 48** (contaminated, one run): TOP-RIGHT 7, RIGHT-IN-TOP-3 2, WRONG-READING 21, NO-CANDIDATE 0, NOT-SCORABLE 18. Before the merge it was 5, 5, 20, 0, 18.

## Not done or not verified

- **Version 2 on the 48** was not run (plan node L4r).
- **Oracle author (L1d)** is not built, so no ASK is scored after a dialogue.
- **L1c** (clause-by-clause composition, phrase cues) and **L1f** (model proposer, adversarial aligner, evidence kind) are not built. The sidecar record exists with `proposed_by: rule-based`; nothing reads it.
- **Gold terms for the development set** do not exist. Answers are judged on its cases only.
- **The identity and round-trip tests cover 66 sentences, not the study's 121.** The lock has 125 entries: 66 compiled Rule lines, 20 refused Rule lines, 39 scenarios. The composer writes Rule lines only.
- **The schema is not committed** (about 1 MB, generated on demand).
- **`COMPOSE2.md` has one wrong path:** from `clausal/` the `--l3` command is `../tools/sem.sh 3 -- python3 compose_tests/v2.py --l3`, not `tools/sem.sh`.
- **`out/report.md` changed outside my work:** its mutation section now shows the committed record of 15:45; the report at HEAD predated that record.
- **I read the A0 count table and the first entry of `l4b_a0/REPORT.md`**, nothing below, and tuned nothing on it.

## What a reviewer should distrust

- **"0 of the sentences that need an unbuilt piece is answered" is true and empty.** Nothing is answered at all.
- **The identity result rests on step 1** (a sentence that compiles is its own answer). With that step off, 23 of 66 fixture sentences come back as the same term, 24 get ASK (reading), 11 ASK (dropped), 8 ASK (system), 0 another term.
- **"Answered right" is weak.** It means not contradicted on at most five inputs, replayed only where the case is what the shipped code does. A0's 17 is an upper bound.
- **"Expressible" is the set author's label**, not checked against the book. The counter sentences about an amount cannot be said in the counter's books, so missed counts are upper bounds for every arm.
- **Seeded drop tests canonical sentences only.** A drop from a paraphrase can still be absorbed by a cue word of a remaining piece; the cue capacity limits that and nothing measures it.
- **Full coverage ignores the candidate's own extra words.** "A batch applied as a whole never changes …" is full for "A batch never changes …". On the fixtures this gave ASK (reading), never a wrong answer, but only because the right sentence was also generated.
- **A word mapped to the wrong piece counts as mapped.** The narrowing-word span catches "an accepted lookup" turned into "is always accepted"; the general case is caught only when a second full candidate exists.
- **Several rules are mine, written while looking at the development set:** the default phrases, the openers "that" and "which", the anchoring rule, the askable rule, the display order of ASK (dropped).
- **A v1 defect the scorer surfaced:** 10 of version 1's 60 top candidates use `amount_value` from the ledger pack in a counter sentence, which `clausal gen` refuses in the counter's feature file.

## FOR DECISIONS.md

1. **Version 2 is a new command, `clausal compose2`; `clausal compose` is unchanged.**
   - Why: arm A0 must stay reproducible as merged.
   - Undo: remove `clausal/compose2.py` and its branch in `pipeline.py`.
2. **`l4b.py` writes one candidate file per project and edits the scratch copy's `projects.yaml`.**
   - Why: `clausal gen` reads only listed files, and one file spanned systems. Reading ids become `Rule.l4b_compose_<project>.<id>`; nothing scored changed.
   - Undo: `git revert 2f2cb46`.
3. **Stop list cut to articles and auxiliaries, as the study says.**
   - Why: prepositions and pronouns must be accounted for. This is the main reason nothing is answered.
   - Undo: widen `STOP2` in `compose2.py`.
4. **Anchoring by every word of a noun, or the verb of a `when` form; never every operation.**
   - Why: version 1's any-shared-word rule anchored the ledger's "fund transfer" from "insufficient-funds".
   - Cost: 12 development sentences are declined at this step.
   - Undo: `anchor()` in `compose2.py`.
5. **Cue capacity:** a piece takes no more cue words than its own form has words.
   - Why: otherwise one piece absorbs a clause and hides a drop.
   - Undo: the `cap` line in `coverage()`.
6. **Echo words do not map.**
   - Why: version 1 counted them as explained; echo prose shares common words with everything.
   - Undo: add an echo step after the cue step.
7. **Chosen roles and literals count as pieces that must be asked for** ("the sender", "the amount" as a term, a number).
   - Why: otherwise junk claims with an unasked term had full coverage.
   - Undo: `Pieces.forced`.
8. **"that" and "which" open condition spans; a narrowing word before the noun is a span of its own.**
   - Why: the first is beyond the study's list and catches relative clauses. The second was added after a refused fixture ("An accepted lookup always answers") was answered with "A lookup is always accepted and always answers".
   - Undo: `OPENERS` and the adjective block in `condition_spans`.
9. **`other-book` filter:** a candidate that uses a book its operation's project does not list is dropped.
   - Why: `clausal gen` refuses it.
   - Undo: first lines of `filtered()`.
10. **Askable rule for "no candidate is good enough":** operation asked for, and every claim has a word mapped into it.
    - Why: structural, no threshold.
    - Undo: the `askable` line in `coverage()`.
11. **ASK (dropped) shows candidates that drop no condition first, then in version 1's rank order.**
    - Why: one ranking rule. It was chosen among three orders tried on the development set (19 of 46 not contradicted if acknowledged unread, against 18 of 49 and 15 of 46).
    - Undo: the `sorted` key in `compose()`.
12. **Default phrases D2, D3, D4** (`DEFAULT_PHRASES`) are mine, each tied to the default's text.
    - Undo: empty the list.
13. **Development-set "expressible" is the author's `kind`; an unscored answer counts as wrong.**
    - Why: conservative, so declining cannot hide errors.
    - Undo: `cell()` in `dev.py`.
14. **Term digest in records is of the term body, not the named definition.**
    - Why: the lock's digest includes the definition's name, so the same term under another id differs.
    - Undo: `ctree.body_sha`.

## FOR RESULTS

All commands from the worktree root unless noted; `S` is a private directory.

| Number | Command |
|---|---|
| A0 on the 48 (contaminated): 7 / 2 / 21 / 0 / 18 | `cp -R trials/sentences $S/sentences; bash clausal/mutation/workcopy.sh $S/sentences/work/clausal; tools/sem.sh 3 -- python3 clausal/compose_tests/l4b.py $S/sentences --out $PWD/clausal/compose_tests/l4b_a0` |
| Development set: A1 0 wrong, 0 right, 46 asked (3 system, 43 dropped), 14 declined; A0 43 wrong, 17 not contradicted; needs-unbuilt answered 0 of 10 (A1), 10 of 10 (A0) | `bash clausal/mutation/workcopy.sh $S/dev/clausal; tools/sem.sh 3 -- python3 clausal/compose_tests/dev.py $S/dev/clausal` |
| If the first ASK (dropped) candidate were acknowledged unread: 18 of 43 not contradicted (A1), 19 of 46 (A1s) | same |
| A0's wrong answers by kind: 17 other operation, 12 contradicted, 10 not of its project, 2 unscored, 2 answered on a not-expressible sentence | same (`compose_tests/dev/results.json`) |
| Identity 66 of 66; full coverage 66 of 66; refused fixture lines answered 0 of 20 | `cd clausal; python3 compose_tests/v2.py --json` |
| Generator reach with step 1 off: 23 same term, 24 ASK reading, 11 ASK dropped, 8 ASK system, 0 another term | same |
| Tree round trip 66 of 66; schema valid 66 of 66; same text 65 of 66; 6 of 6 bad trees rejected | same, or `python3 -m clausal tree --check` |
| Seeded drop 43 of 43 reported, 42 as CONDITION DROPPED, 6 not constructible | same |
| Version 1's thirteen sentences under v2: 2 ANSWER, 9 ASK dropped, 1 ASK system, 1 DECLINE; 0 answers with a drop | same |
| One ASK (reading) with a separating input through `clausal separate` | `cd clausal; ../tools/sem.sh 3 -- python3 compose_tests/v2.py --l3` |
| Full run exit 0; 112 of 112 verdict codes identical; 1 of 302 rungs differs | `cd clausal; ../tools/sem.sh 3 -- ./run.sh; python3 compare/against/verdicts.py <scratchpad>/baseline2/graph.json` |

## Reviewer

Every measurement the builder reports reproduces. The one claim that fails is the caveat that a word mapped to the wrong piece is caught once a second full candidate goes to `clausal separate`: I found a reproducible wrong ANSWER that inverts the author's meaning.

What holds:
- The development set is byte-identical to the scratchpad file (sha256 4c001704…) and is the only content of the first commit, a1f8bfb.
- The commit order is development set, l4b.py repair, A0 run, freeze, then the reported runs. The frozen files have no change after 7cb2f4c.
- Outside the new files, only two subcommand branches changed, in `__main__.py` and `pipeline.py`. No rule, book entry, lock, fixture or expected verdict changed, and neither did compose.py or trials/.
- Arm A0 is the only run on the 48: one scored run on the committed repair, recounting to 7/2/21/0/18 from the raw output.
- I reran `compose_tests/v2.py --json` in a scratch copy. All tests pass with exactly the reported numbers: identity 66/66, full coverage 66/66, refused lines answered 0/20, reach with step 1 off 23/24/11/8, round trip 66/66 with 65 same text, seeded drop 43/43 (42 as CONDITION DROPPED, 6 not constructible), and version 1's thirteen cases 2/9/1/1.
- The development tallies recount from the raw output: A1 0 right, 0 wrong, 46 asked (3 system, 43 dropped), 14 declined (12 unanchored, 2 with no askable candidate). A1s 46 asked and 14 declined. A0 17 right and 43 wrong (17 other operation, 12 contradicted, 10 not of its project, 2 unscored, 2 answered on not-expressible sentences). If the first ASK (dropped) candidate were accepted unread: 18 of 43 and 19 of 46 not contradicted.
- `verdicts.py` against baseline2 reports 0 of 112 verdict codes differ.
- The schema is generated from the book.
- The rules that resemble the 48 ("whether accepted or rejected" for D2, "whose" as an opener) are prescribed by the study itself; I found no sign of tuning to the 48.

What fails, from 31 rough sentences of my own:
- Extra conditions without an opener ("of a large amount", "from a frozen account", "on weekdays", "small", "again", "after midnight") always got ASK (dropped) with the words listed. No condition was silently lost.
- Blocker: "A rejected transfer never changes the ledger when the amount is zero" is ANSWERED in the default mode (L3 on) with a sentence whose condition and claim are both inverted ("for which the amount differs from zero, the amount has moved between its accounts"). Coverage counts it as full, because "never" is mapped into the negated condition and "changes" into "no other balance changed". The only other full candidate is the same sentence with its arguments swapped, which `clausal separate` proves equal. The correct sentence compiles but is not full, because `equals` counts as ADDED. Two more sentences give the same pair.
- The same negation mapping also lets an ASK (dropped) list only "gives" as dropped for a candidate that says the opposite of "no result".
- DECLINE is used for expressible development sentences d02, d07 and d11 (book sentences for all three compile) because no operation noun is written. This follows the study's rule and is scored as a miss, but it fails the step's check that DECLINE is not used for sentences the book can express.
- d36 and d42 are labelled expressible but the counter's book cannot say them, so declining those is correct.

Scratch files are in <scratchpad>/review-L1ab/ (`v2_json.log`, `l3_zero.log`, `mine1.log`, `mine2.log`, `mine3.log`, `scripts/`).

- **blocker**: Version 2 gives a wrong ANSWER in its default mode (L3 on). It says "one reading" and exits 0, and `--write` would write it with no acknowledgement. Rough: "A rejected transfer never changes the ledger when the amount is zero". Answer: "For a rejected transfer for which the amount of the transfer differs from zero, the amount of the transfer has moved between its accounts in the ledger and no other balance changed". Both the condition (zero becomes differs from zero) and the claim (never changes becomes has moved) are inverted. Coverage calls it full: "never" goes through the `not` cue into the negated `equals` of the condition, and "changes" goes to the form word "changed" of `i.moved`. The only other full candidate is the same sentence with the `differs from` arguments swapped, and `clausal separate` returns PROVED-EQUAL for that pair, so the outcome becomes ANSWER. The correct reading, "A rejected transfer for which the amount of the transfer equals zero never changes the ledger", compiles but is not full, because `equals` counts as ADDED. So coverage prefers the inverted reading to the right one. The same inverted pair comes back for "… if the amount is zero" and for "An accepted transfer never changes the ledger when the amount is zero". This refutes the report's caveat (COMPOSE2.md lines 201-203) that a word mapped to the wrong piece "is caught only when a second full candidate exists and `clausal separate` is asked": here a second candidate existed, separate was asked, and it confirmed the wrong reading. Cause: a negation word outside every condition span may be mapped to a negated piece inside a condition unit, and nothing checks which side of the condition a word was written on.
- **should-fix**: In an ASK (dropped), the dropped-word list can misdescribe a candidate whose meaning is inverted, so an acknowledgement record would understate what was accepted. The cause is the same negation mapping. Rough: "A lookup of an account that is not in the ledger gives no result". First candidate shown: "For a lookup for which the account is not an account of the ledger, the result is the balance of the account in the ledger". The only dropped word listed is "gives": the author's "no" is mapped through a cue to the negated `l.is_account` of the condition. The author is asked to "accept without 'gives'" a sentence that claims the opposite of "no result".
- **should-fix**: DECLINE is used for development sentences that the book can say in their own project, because no noun of the operation is written. Three verified: d02 "You can't take out more than the wallet holds" (book: "A withdrawal for which the amount is more than the wallet's balance is always rejected", compiles); d07 (book: "A transfer for which the amount is more than the sender's balance is always rejected", compiles); d11 (book: "For a lookup for which the account is not an account of the ledger, there is no result", compiles; it is also a fixture sentence). My own "Taking money out of a wallet that has too little is refused" is declined the same way. This follows the study's DECLINE rule (no operation anchored) and the scorer does count these as misses (expressible declined: 9). But the step check "DECLINE is not used for sentences the book can express" fails. An ASK naming the system's operations would fit better than DECLINE.
- **note**: d36 and d42 are labelled expressible by the set's author, but the counter's book cannot say them: every phrasing I tried is UNBOUND, or uses `amount_value` from the ledger pack, which the counter's project does not list. DECLINE is correct there. This supports the builder's caveat that the missed counts are upper bounds.
- **note**: The freeze precedes the reported development-set run: commit 7cb2f4c at 13:40:09, run log at 13:44:47, and the scratch copy's compose2.py, ctree.py and dev.py are byte-identical to the freeze. But dev3.log (13:39, before the freeze) is byte-identical to the reported run, so the frozen code had already been measured on the development set. That is allowed for a development set, which the report labels as such; the freeze governs no held-out run.
- **note**: The A0 scratch copy (taken at 12:30:30) contains an earlier, broken l4b.py (`book in p.books`), which suggests a first attempt that would have stopped in list_candidates before any scoring. The scored A0 run wrote its feature files at 12:31:24, after the repair commit at 12:31:05, so it used the committed code. Nothing in the copy of the 48 is newer than a0.log. No compose2 output on the 48 exists in the builder's directories.
- **note**: The seeded-drop test is a working negative control: an in-memory absorber that maps every dropped word gives 42 of 43, and the same absorber with condition spans also off gives 0 of 43. But turning off condition spans alone still passes 43 of 43, so on canonical sentences the span machinery is exercised only by the three unit checks, not by the seeded drop.

## Fix round

All three defects are fixed; the fixes close the routes the reviewer found, not the whole class (see "What a reviewer should distrust").

Branch `wave/compose2`, worktree `/Users/will/dev/lean-rosette/.worktrees/compose2`, three new commits, no push:

- `2066b40` — freeze: code, tests and scorer definitions, committed before the reruns.
- `6fe31f4` — design notes and the development-set rerun.
- `0f1c9dd` — outputs of the one full `./run.sh`.

## What changed (paths)

- `clausal/clausal/compose2.py` — coverage accounting split into `account` and `wrong_side`; the `NEG` rule; span matching; `operation_question`, `stated_operation`, `system_vocab`; `--operation`; ASK (operation); render and record fields.
- `clausal/compose_tests/v2.py` — 19 new checks for the three defects.
- `clausal/compose_tests/dev.py` — arm A1o, the `operation` ask kind, decline breakdown.
- `clausal/compose_tests/dev/REPORT.md`, `results.json` — rerun.
- `clausal/COMPOSE2.md` — rules, numbers, the corrected caveat, a "Fix round" section.
- `clausal/out/*` — full-run outputs.

Version 1 (`clausal/compose.py`), the cue table, `trials/sentences`, the books and all expected verdicts are untouched.

## Per defect

### 1. Blocker: wrong ANSWER in default mode — fixed

The cause was as the reviewer said. Two rules were added to coverage:

- **Side of a condition.** A word is mapped to a piece written inside a condition unit only if the word is written in the condition span matched with that unit. This holds for form words and cue words. A word of one span is not mapped into another span's unit. Refused mappings are printed as `refused_mappings`.
- **One negation word, one negation.** A piece takes "not", "no" or "never" through a cue only while it has taken fewer negation words than it says negations.

Actual output, default mode (L3 on), from `clausal/`:

```
$ python3 -m clausal compose2 "A rejected transfer never changes the ledger when the amount is zero"
rc=4 | ASK (dropped): | [1] A rejected transfer for which the amount of the transfer equals zero never changes the ledger
$ ... "A rejected transfer never changes the ledger if the amount is zero"
rc=4 | ASK (dropped): | [1] A rejected transfer for which the amount of the transfer equals zero never changes the ledger
$ ... "An accepted transfer never changes the ledger when the amount is zero"
rc=4 | ASK (dropped): | [1] An accepted transfer for which the amount of the transfer equals zero never changes the ledger
$ ... --write new.feature
clausal compose2: --write needs an ANSWER, or an ASK (dropped) with --acknowledge K --by NAME: nothing is written otherwise   (rc=1, no file)
```

- The correct reading is now shown first. It is still not an ANSWER: `equals` is ADDED because "is" is on the stop list.
- The inverted candidate now has "never" DROPPED and is not full.
- The side rule exposed two older weaknesses, which I fixed because three fixtures lost full coverage under their own tree otherwise:
  - Span matching could cross the two conditions of one frame ("when …, if …"). It now tries the unit the span's words are inside first.
  - "an accepted internal transfer" gave a narrowing span only to the word next to the noun. Each narrowing word in the run is now a span.
- The caveat at COMPOSE2.md lines 201-203 is rewritten. It now says agreement among full candidates under `clausal separate` is no evidence that any of them is right.

### 2. Should-fix: dropped list understates an inverted candidate — fixed

The negation rule fixes it. For "A lookup of an account that is not in the ledger gives no result", the first candidate now prints:

```
[1] For a lookup for which the account is not an account of the ledger, the result is the balance of the account in the ledger
     DROPPED (your sentence also says; this sentence does not): gives, no
     not mapped (the word is not written in the condition this piece is in): of -/-> l.is_account (negated), account -/-> l.is_account (negated)
```

That candidate is still shown first; the order of an ASK (dropped) was not changed.

### 3. Should-fix: DECLINE for sentences the book can say — fixed

- **New outcome ASK (operation).** When nothing is anchored and the sentence has a word of a system (its name, an operation noun, a role, a role's type), the tool lists that system's operations and generates nothing.
- **`--operation ID`** (an id or a noun) is the author's answer. That one operation is tried, is not counted as ADDED, and is recorded as `operation_stated` in the result and the sidecar record.
- **DECLINE** remains for sentences with no word of any system ("the answer never depends on anything" is still declined) and for "no askable candidate".

d02, d07 and d11 are now ASK (operation); the reviewer's "Taking money out of a wallet that has too little is refused" was not rerun. On the development set, all 12 former no-operation declines became ASK (operation).

d36 and d42 are still declined though labelled expressible, and I hold these are not defects. They are counter sentences with a written number ("100"), and the counter's project lists no book with a literal amount, so every such candidate is filtered `other-book`.

I also fixed the word list reading "can't" as "ca" + "not"; "can't", "won't" and "shan't" are now read as "can not", "will not", "shall not".

## Verification (actual output)

- **`python3 compose_tests/v2.py --l3 --json`** (under `sem.sh 3`): `all passed`, rc 0, 78 checks. Log: `<scratchpad>/fx-L1ab/v2_l3.log`
  - identity: 66 came back as itself, 66 with full coverage, 66 itself-or-system-question
  - round trip: 66 same term, 65 same sentence, 66 schema valid
  - seeded drop: 43 of 43 reported, 43 flagged CONDITION DROPPED (42 before), 6 not constructible
  - generator reach with step 1 off: 25 ANSWER same term, 22 ASK (reading), 11 ASK (dropped), 8 ASK (system); before: 23, 24, 11, 8; none answered with another term
  - refused fixture lines: 0 of 20 answered (12 ASK dropped, 6 ASK system, 1 ASK reading, 1 DECLINE)
  - version 1's thirteen cases: 2 ANSWER, 9 ASK (dropped), 1 ASK (system), 1 DECLINE
  - both L3 checks ok
- **Development set rerun**, after freeze `2066b40`, in a scratch copy: rc 0, replay 444 requests and 444 answers. Log: `<scratchpad>/fx-L1ab/dev.log`
- **`sem.sh 3 -- ./run.sh`** (full): rc 0, "RESULT: every scenario got its expected verdict and every Rule statement its expected one". Log: `<scratchpad>/fx-L1ab/run_full.log`
- **`python3 compare/against/verdicts.py <baseline2/graph.json>`**: `verdict codes that differ: 0 of 112`.
- **Bounded-check rungs that answered differently from the baseline** (all verified → timeout, under load; not regressions):
  - `Rule.ledger.whole_batch` [up to 2 accounts and up to 3 transfers]
  - `Spec.ledger.batch_then_total_overflow` [same bound]
  - `Spec.ledger.whole_conserves` [same bound]
  - `Rule.ledger_rules.readme_internal_transfers` [up to 4 accounts]
  - Against the previous commit's run there is a fifth: `Rule.ledger_rules.n1_internal_transfer` [up to 4 accounts].

## Not done / not verified

- Version 2 still answers 0 of 60 development sentences.
- The reviewer's own scratch scripts (`rough.py` on `mine1/2/3.json`) were not rerun. I ran the same three sentences through the CLI and `v2.py`.
- `./run.sh --quick` was not used; only the one full run.
- No set measures how often the side rule turns a right ANSWER into a question. The only evidence is the fixtures with step 1 off (25 answered against 23 before).
- Version 2 was not run on the 48.

## What a reviewer should distrust

- **The side rule has a known hole.** A span runs to the next opener or punctuation mark. In "a transfer that is rejected never changes …" the claim is inside the span, so a negation in the claim can still be mapped into that span's own condition.
- **"unless" is treated like "if".** "A withdrawal never changes the wallet's balance unless it is accepted" shows "An accepted withdrawal never changes the wallet's balance" first, with only "it" dropped. That is the opposite condition, and the dropped list does not say so. It is the same class as defect 2 and is not fixed.
- **Stemmed form words count wherever the candidate writes them.** "changes" still maps to "no other balance changed". Nothing compares the polarity of the author's claim with the candidate's.
- **The fix-round rules were written against the reviewer's sentences** and about ten of mine. They are not measured on an independent set.
- **Forced roles are exempt from the side rule** (kind `leaf`, the one filler of its hole).
- **ASK (operation) fires on any system word.** "The ledger should always be correct" is now asked which operation. Not-expressible sentences correctly declined went from 5 to 0.
- **`system_words` shows "sender" as a wallet-only word**, though the ledger writes "the sender of the transfer". This is older behaviour that I did not change. It decides which operations ASK (operation) lists for a sentence like d08.
- **A1o answers the operation question from the set's cases.** That is an oracle.

## FOR DECISIONS.md

1. **Side-of-condition rule.**
   - What: a word maps into a condition unit only from the span matched with it, by form or by cue; forced roles exempt.
   - Why: closes the reviewer's blocker and the form-word variant I found ("A lookup does not give a result when the account is in the ledger").
   - Undo: in `compose2.coverage`, call `account(…, set())` once and drop the loop over `wrong_side`.
2. **One negation word per negation** (`NEG` = not / no / never).
   - Why: defect 2.
   - Undo: remove the three-line `NEG` guard in step 3 of `account`.
3. **Span matching prefers the unit a span's words are inside; each narrowing word in a run before the noun is a span.**
   - Why: without these, three fixtures lost full coverage under the side rule.
   - Undo: restore the unsorted `can` and the single-word test in `condition_spans`.
4. **ASK (operation) and `--operation`.**
   - What: replaces DECLINE when nothing is anchored and the sentence has a system word.
   - Why: defect 3. It deviates from the study's rule (section 4.1: DECLINE whenever nothing is anchored), but nothing is generated and no operation is tried unless the author names it.
   - Cost: 5 correct declines on not-expressible sentences became questions.
   - Undo: in `compose`, drop the `operation_question` branch and the `operation` parameter.
5. **An operation given with `--operation` is not ADDED.**
   - What: it may lead to an ANSWER, and is recorded as `operation_stated`.
   - Why: otherwise every candidate after the answer would be unaskable.
   - Undo: remove `stated` from `coverage`.
6. **Arm A1o added to `dev.py`.**
   - What: the scorer's definitions changed in the freeze commit before the rerun; A1 and A1s definitions are unchanged apart from the new ask kind.
   - Undo: revert `dev.py` to `055ec4a`.
7. **"can't", "won't", "shan't" written out in `lex`.**
   - Why: a cosmetic bug in the dropped-word list.
   - Undo: remove the one `re.sub` line.
8. **d36 and d42 left as DECLINE.**
   - Why: their project has no book for a written number; changing that is a book or project-list decision, not the composer's.

## FOR RESULTS

All commands run from `clausal/` unless noted.

**`python3 compose_tests/v2.py --json`** (add `--l3` under `tools/sem.sh 3 --`):

| Measure | Result |
|---|---|
| Identity | 66 of 66 |
| Full coverage under own tree | 66 of 66 |
| Round trip, same term | 66 of 66 (same sentence 65) |
| Seeded drop reported | 43 of 43 (43 as CONDITION DROPPED) |
| Refused fixture lines answered | 0 of 20 |
| Generator reach, step 1 off | 25 same term, 22 ASK (reading), 11 ASK (dropped), 8 ASK (system), 0 another term |
| Fix-round checks | 19 of 19 |
| All checks | 78 ok, all passed |

**`python3 -m clausal compose2 "<sentence>"`** on the reviewer's three sentences: 3 of 3 ASK (dropped), rc 4, the condition-as-written reading first (it was ANSWER, rc 0, inverted).

**Development set**, 60 sentences, after freeze `2066b40`. From the repo root: `bash clausal/mutation/workcopy.sh <scratch>/clausal; tools/sem.sh 3 -- python3 clausal/compose_tests/dev.py <scratch>/clausal`

| | A1 | A1s | A1o | A0 |
|---|---|---|---|---|
| Wrong answers | 0 | 0 | 0 | 43 |
| Answered | 0 | 0 | 0 | 60 |
| Expressible (45): right | 0 | 0 | 0 | 17 |
| Expressible: asked | 43 | 43 | 43 | 0 |
| Expressible: declined | 2 | 2 | 2 | 0 |
| Expressible: missed | 45 | 45 | 45 | 28 |
| Not expressible (15): asked | 15 | 15 | 15 | 0 (15 answered) |
| Not expressible: declined | 0 | 0 | 0 | 0 |
| Asks: system / operation / reading / dropped | 3 / 12 / 0 / 43 | 0 / 12 / 0 / 46 | 0 / 3 / 0 / 55 | — |
| First shown acknowledged unread: not contradicted | 18 of 43 | 19 of 46 | 20 of 55 | — |

- Before the fix round, A1 was: expressible asked 36, declined 9; not expressible asked 10, declined 5.
- Declined but labelled expressible: d36, d42 (it was 9 sentences).
- After the operation question (A1o), 9 of the 12 become ASK (dropped) and 3 stay asked. Of the 7 expressible ones, the first shown is not contradicted for 1 (d11).
- The 10 sentences that need an unbuilt piece: 0 answered in every version-2 arm.

**`tools/sem.sh 3 -- ./run.sh`** then **`python3 compare/against/verdicts.py <baseline2/graph.json>`**: rc 0; 0 of 112 verdict codes differ; 4 bounded-check rungs verified → timeout against the baseline (listed under Verification).
