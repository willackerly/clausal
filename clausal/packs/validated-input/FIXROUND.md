# K1, fix round: what was added after a review, and what is frozen before it is measured

A reviewer on another model found three defects in the first measurement (`RESULTS.md` as of commit `89f5d91`).
This file is committed BEFORE the runs that measure the fixes. Nothing in `pack.yaml`, `FREEZE.md`,
`kvparse/expected.json`, the feature file or the nine frozen mutants is changed.

## What was changed (before any run on it)

1. **The specification's encoder is partial** (`lean/Kvparse/Pieces.lean`, `KV.writable`, `KV.encode`;
   `wallet-bdd/src/pieces.rs`, `kv_encode`; echo of `kv.encoding` in `clausebook/local/kvparse.yaml`). The first
   version wrote `48 + digit` for any digit, so a parse that answers the value 10 for `a=:` had `a=:` as "the encoding
   of the result" and VI-7b held of it. Now a record has an encoding only if the format can write it: at least one
   key given, each digit at most 9, digit 0 for a key not given. `KV.encode_inj` (`lean/Kvparse/Lemmas.lean`) proves
   that two records with the same encoding are the same record. This is a change of the meaning of a word of the
   project's local book. It makes VI-7b false in more places and true in none where it was false. The form, the
   sentence and the pack are unchanged.
2. **A wider search** (`wallet-bdd/tests/kv_wide.rs`): the ten rules on the compiled Rust at 10 limits (0 to 8 and
   4294967295) by 429,505 messages: every byte string of length 0 to 2, and every record of the format with every
   one-byte substitution, insertion and deletion. It is not part of `./run.sh` and gives no verdict.
3. **Three mutants outside the frozen list** (`kvparse_mutants.py`, `REVIEW_MUTANTS`): R1 (`:` taken as a digit) and
   R2 (one trailing newline accepted) are the reviewer's, text unchanged. R3 (a trailing `\r\n` accepted) is the
   builder's, chosen to lie outside the wider search.
4. `pack instantiate` and `pack check` say on the completeness line what `stated` does not mean.

## Seen before this freeze (so not a prediction)

- The reviewer's result: R1 and R2 leave the pipeline green (exit 0, every verdict the baseline's).
- The wider search was run ONCE on the unmutated crate while it was being written: no rule false, 0 points that
  could not be evaluated. It was run on no mutant.
- `python3 -m clausal book check` after change 1: the violations are exactly the expected ones.

## Expected (frozen here)

| Item | Pipeline run (`./run.sh --no-unit --quick --no-adequacy --no-heldout`) | Wider search |
|---|---|---|
| unmutated tree | exit 0; the ten verdicts of `kvparse/expected.json`; no verdict code of the baseline of this wave changes | no rule false |
| strip | 0 verdict codes differ | – |
| B1 to B6, T-reject-all, T-accept-all | the same COUNTEREXAMPLE sets as in the first run (`results/kvparse_mutants.md` at `89f5d91`); REFUTED for none | every rule the pipeline finds false is false here too |
| R1 | shown false by no pack rule; exit 0 | VI-2, VI-6, VI-7b, VI-10 (VI-7b only because of change 1) |
| R2 | shown false by no pack rule; exit 0 | VI-2, VI-6, VI-7b, VI-10 |
| R3 | shown false by no pack rule; exit 0 | **no rule** (its input `a=1\r\n` is not in the set); at the named input: VI-2, VI-6, VI-7b, VI-10 |

How the result is counted: R1, R2 and R3 are reported apart from the frozen nine and never added to "9 of 9". A
mutant of this group that no pack rule shows false in a pipeline run is a negative result of the pack on its first
target whatever the wider search says, because the wider search gives no verdict. If the wider search finds a rule
false on the unmutated tree, or misses R1 or R2, that is reported as it is and the search is not adjusted.

## Stateability: the range (measured with the compiler before this freeze; no run involved)

`python3 -m clausal pack instantiate validated-input --project kvparse --bindings features/kvparse_rules.pack.validated-input.yaml <choice> --dry-run`

| Choice | Cannot be stated |
|---|---|
| kvparse as built (limit in the parser's state, canonical-only, duplicates rejected) | 1 of 11 (VI-7a) |
| `--variants canonical=lenient duplicates=last-wins` | 3 of 11 (VI-7a, VI-7b, VI-9) |
| `--slots limit="the field limit"` (a limit that is a constant, not a quantity of the state) | 3 of 11 (VI-7a, VI-3, VI-4) |
| both | 5 of 11 (45%, above the target of a third) |
| `--variants size=unbounded` | 1 of 11, 2 not applicable |
| `--variants size=unbounded canonical=lenient duplicates=last-wins` | 3 of 11, 2 not applicable |
