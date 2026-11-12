# Tests of `clausal compose` (plan node L1) and the first L4(b) measurement

Design: `../COMPOSE.md`.

| File | What |
|---|---|
| `run.py` | Self-tests: tokeniser, the compile guarantee, a regression snapshot of the top candidate, repeatability, scoping, `--write`, the model hook, the NOT OFFERED block for sentences that read in two systems. `--l3` adds questions through `clausal separate`, including a pair whose two separating inputs point opposite ways. |
| `cases.json` | Thirteen rough sentences written by the implementer, each with the top candidate recorded (`run.py --record`). |
| `l4b.py` | The first L4(b) measurement on the 48 frozen sentences, through the existing trial machinery. `--smoke` checks its plumbing on three sentences that are not from the trial. |
| `l4b/` | Output of the one measured run: `results.json`, `REPORT.md`. |

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
