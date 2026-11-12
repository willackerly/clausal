# counter: the third project (plan node X7)

A fixture, not a claim about anything useful. It exists to show that a project is an entry of `../projects.yaml`:
a crate, its books, its feature files and its Lean modules.

| What | Where |
|---|---|
| The crate (22 lines, one function, `bump(&mut self, by: u64) -> bool`, bounded at 100) | `src/lib.rs`, unit tests in `tests/unit.rs` |
| Its local book (one operation `ctr.bump`, one measure `ctr.count`; needs core only, no pack) | `../clausebook/local/counter.yaml` |
| Its domain words in Lean | `../lean/Counter/Pieces.lean` |
| Its three rules | `../features/counter_rules.feature` |
| The hand-written proof of the one true rule | `../lean/Wallet/RuleProofs/counter_rules/rejected_bump_unchanged.lean` |
| The verdicts expected, committed before any run (commit `5a95d55`) | `expected.json` |
| The comparison | `python3 counter/check_expected.py` (from `clausal/`, after `./run.sh`) |

## The rules and what the run gave

| Rule line | Expected | Got |
|---|---|---|
| A rejected bump never changes the counter's count | PROVED-FOR-ALL | PROVED-FOR-ALL (hand-written proof of the generated obligation, carried to the reading by the kernel-checked equivalence); the property test found nothing in 10000 cases; the bounded check verified it with no size bound |
| A bump is always accepted | REFUTED, the input reproduced on the compiled Rust | REFUTED at counter 0, amount 18446744073709551615 (grid search, kernel-checked, fails on the compiled Rust too); the generated property test found counter 51, amount 50; the bounded check failed it too |
| A bump resets the counter | UNBOUND | UNBOUND |
| function `counter.Counter.bump` | INPUTS-NOT-COVERED | INPUTS-NOT-COVERED |

Numbers are those of the one full `./run.sh` of 2026-11-12 (`out/projects.json`, `out/report.md`).

The first pipeline run on these rules stopped at the narrowing check (see below); after that fix, and with the proof
written, the verdicts were as expected on the next run. `expected.json`, the feature file, the crate and the book
were not edited after the freeze commit. `check_expected.py` was: it joined the lines of a rule block wrongly and
crashed; the fix does not touch what is expected.

## What adding it took outside its own files

No edit of `clausebook/core.yaml` and none of `lean/Frames/` (`git diff c211d8b -- clausebook/core.yaml lean/Frames`
is empty). The list of everything else is in `../DESIGN.md`, section 21.6: eleven shared files, of which one is a
defect of the compiler's narrowing check that the third project exposed.
