# Tests of `clausal compose` (plan node L1) and the first L4(b) measurement

Design: `../COMPOSE.md`.

| File | What |
|---|---|
| `run.py` | Self-tests: tokeniser, the compile guarantee, a regression snapshot of the top candidate, repeatability, scoping, `--write`, the model hook, the NOT OFFERED block for sentences that read in two systems. `--l3` adds questions through `clausal separate`, including a pair whose two separating inputs point opposite ways. |
| `cases.json` | Thirteen rough sentences written by the implementer, each with the top candidate recorded (`run.py --record`). |
| `l4b.py` | The first L4(b) measurement on the 48 frozen sentences, through the existing trial machinery. `--smoke` checks its plumbing on three sentences that are not from the trial. |
| `l4b/` | Output of the one measured run: `results.json`, `REPORT.md`. |

## Version 2 (plan nodes L1a, L1b, L1e): `../COMPOSE2.md`

| File | What |
|---|---|
| `v2.py` | Tests of `clausal compose2` and `clausal tree` on the book's own fixtures: identity, tree round trip and schema, seeded drop, filters, the system question, decline, condition spans, the acknowledgement record. `--l3` adds one ASK (reading) through `clausal separate`. |
| `dev/devset.json` | The development set: 60 sentences by an author who had seen neither the tool nor the 48. Committed unchanged; never edited. |
| `dev.py`, `replay.py` | The development set through version 2 and version 1, judged on the set's cases on the compiled Rust in a scratch copy. Output: `dev/REPORT.md`, `dev/results.json`. Development numbers. |
| `l4b_a0/` | Arm A0: version 1 on the merged book, one run on the 48 frozen sentences in a private copy. Contaminated; a baseline only. |

## Version 2, second part (plan nodes L1c, L1d): `../COMPOSE2.md`, "Second part"

| File | What |
|---|---|
| `oracle.py`, `oracle_results.json` | The oracle author on the `separate_tests` cases: every candidate of every case in turn as the intended reading; the dialogue must end at it within three questions. Frozen with the predicted question counts before its run. |
| `dev/gold.json` | Gold readings for the development set where one can be assigned (28 of the 45 labelled expressible), by the builder, before any L1c change. |
| `dev/before_l1c/` | The development set through the composer as the first part left it, with the dialogue and the oracle author: the "before" of the second part. `dev/REPORT.md` is the "after". |
| `l4r.py` | Arm A1 on the 48 frozen sentences (contaminated): version 2 with the dialogue and the oracle author, scored on the authors' cases with the plumbing of `l4b.py`. `--gold` makes the gold readings from the trial's rewordings by following the compiler's refusals; `--smoke` checks the plumbing on three sentences that are not of the 48. |
| `l4r_a1/` | `gold.json` (committed before the run), and the output of the one run: `results.json`, `REPORT.md`. |

`l4b.py` was repaired for the project list (2026-11-12): the candidates go to one feature file per project of the
scratch copy, each listed in the scratch copy's `projects.yaml`. What it scores is unchanged.

## Version 1

```sh
cd clausal
python3 compose_tests/run.py                 # about 5 s, no Lean
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
python3 compose_tests/run.py --l3            # one Lean run and one cargo run more
```

## `cases.json` is a regression snapshot, not a blind test

The thirteen sentences were written by the implementer before any trial sentence was read, and the ranking rule
and cue table were adjusted while looking at their output. The recorded top candidate is what the frozen rule
gives, right or wrong. By the implementer's own reading it is wrong for five of them:

- "looking up an account that does not exist returns nothing": the top candidate says only that such a lookup
  answers; "there is no result" is second.
- "applying a batch as a whole either applies everything or leaves the ledger untouched": the book has no "or"
  between claims; the top candidate ("never changes the ledger") is false of the code.
- "the lookup returns the same answer no matter how many accounts are added to the ledger": the top candidate uses
  "the ledger agrees at the account"; "the ledger is extended" is second.
- "money is never created or destroyed by a batch": the top candidate is "never changes the ledger"; the total is
  second.
- "the answer never depends on anything": names no operation; the list is noise.

## The freeze

The ranking rule, the cue table, the stop list, the stemmer, the limits and the form choice (`compose.py`), and
the scoring definitions of `l4b.py`, were committed before `compose` was run on any of the 48 sentences. Before
that commit the implementer had read the trial's machinery (`run_v4.py`, `try_compile.py`, the header of
`cases.py`, the trial README) and not `authors.json`, the case tables, `rewordings.py`, `units.py`, `RESULTS.md` or
`results.json`.

## The L4(b) run

One run, after the freeze commit `395a746`: `l4b/REPORT.md` (every sentence with its three candidates and the
judgement of each case, wrong readings first) and `l4b/results.json`. Headline: top candidate agrees on every
encoded case for 5 of 48, a lower candidate does for 5 more, 20 wrong readings, 0 without a candidate, 18 with no
encoded case. What to distrust and what would be changed: `../COMPOSE.md`, "First measurement". To rerun (about
80 s warm; the result is deterministic given the tree):

```sh
S=<a private directory>
cp -R trials/sentences $S/sentences
bash clausal/mutation/workcopy.sh $S/sentences/work/clausal
tools/sem.sh 3 -- python3 clausal/compose_tests/l4b.py $S/sentences            # writes clausal/compose_tests/l4b/
tools/sem.sh 3 -- python3 clausal/compose_tests/l4b.py $S/sentences --smoke    # plumbing only, three sentences not from the trial
```
