# Tests of the computed display (plan node Q6)

`expected.json` was committed before `clausal/display.py` existed and before any display was computed: the nine
outcome tables, the gates T1 to T6, and what is reported without being a gate. `run.py` (added with the code) checks
them and writes `results.json`. Nothing in `expected.json` is edited after a run; a gate that fails is reported as
failed.

Before the freeze only this was run: one hand-written Lean file that evaluated `Frames.Check.monotone` and
`decide (Frames.Monotone.at ...)` once each on an operation whose `run` was replaced by `fun _ _ => none`, to see that
such a term elaborates (it does; the first attempt, with the compiler's `{ op with run := run }` text under a
narrowing word, did not, which is why the display wraps the replacement in a reducible function).

## What is here

| File | What |
|---|---|
| `expected.json` | Frozen first (commit `be514e2`): nine outcome tables, gates T1 to T6, what is reported without a gate. |
| `run.py` | The gates, in one Lean run (about a minute), and a negative control. `--unit`: the parts that need no Lean. Writes `results.json`. |
| `results.json` | The last run: per gate pass or fail with its numbers. |

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
python3 display_tests/run.py --unit
python3 display_tests/run.py
```

`run.py` needs `lean/` built. Gate T1b also needs `out/rsearch.log` and `build/rsearch_grid.json` of a finished
`./run.sh`; without them it fails and says the reading search is absent.

## What the run covers

- every compiled Rule line of `features/*.feature`, with its neighbours;
- every `@says-nothing` line of `controls/narrowing.feature`, compiled with the refusal off, and every `@covers` line;
- the nine sentences of `expected.json`.

## Negative controls

- **A tampered table.** The script of a rule the model breaks is generated with the run-substituted executable reading
  replaced by `true`. The run must report that the table differs from `Claim.check` on the grid and from the frame's
  definition. It does: 5 of 88 pairs, and 257 of 900 substituted outcomes.
- **A flipped cell.** `--unit` builds a three-point reading search by hand and checks that a table with one cell
  flipped, in either direction, is reported by the comparison of gate T1b.

## One count in the freeze was wrong

`expected.json` says gate T2b is about "9 lines". `controls/narrowing.feature` has 8 `@covers` lines. The 9 was a
miscount made before any code ran. `expected.json` is not edited. `run.py` applies the gate as worded ("each `@covers`
line") and prints both numbers and `count_as_frozen: false`.
