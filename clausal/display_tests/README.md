# Tests of the computed display (plan node Q6)

`expected.json` was committed before `clausal/display.py` existed and before any display was computed: the nine
outcome tables, the gates T1 to T6, and what is reported without being a gate. `run.py` (added with the code) checks
them and writes `results.json`. Nothing in `expected.json` is edited after a run; a gate that fails is reported as
failed.

Before the freeze only this was run: one hand-written Lean file that evaluated `Frames.Check.monotone` and
`decide (Frames.Monotone.at ...)` once each on an operation whose `run` was replaced by `fun _ _ => none`, to see that
such a term elaborates (it does; the first attempt, with the compiler's `{ op with run := run }` text under a
narrowing word, did not, which is why the display wraps the replacement in a reducible function).
