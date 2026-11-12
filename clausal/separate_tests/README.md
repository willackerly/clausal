# Tests of `clausal separate` (plan node L3)

`python3 -m clausal separate "<sentence A>" ["<sentence B>"]` looks for a concrete input on which one compiled
reading holds and the other fails. The design is in `../SEPARATE.md`.

## What is here

| File | What |
|---|---|
| `cases.json` | Nine cases, each with its expected result. Frozen before the first run of any of them (see below). |
| `run.py` | `--unit`: the comparison logic on hand-made bit strings, no Lean and no Rust. Without it: the cases, checked against `cases.json`; writes `results.json`. |
| `results.json` | The last full run: per case, pass or fail, the failed checks, and the whole structured result. |

Run from `clausal/`:

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
python3 separate_tests/run.py --unit
../tools/sem.sh 3 -- python3 separate_tests/run.py
```

The cases need `lean/` built (the modules `Wallet.Pieces`, `Ledger.Pieces`, `Frames.Lemmas`; a finished `./run.sh` is
enough) and cargo. Each case is one Lean run of a few seconds and one `cargo run --example separate_replay`.

## The freeze

The expected result of every case was written and committed before `separate` was run on any sentence of
`cases.json`. Before that commit the sentences of the cases had only been compiled (no search, no replay), to check
that each one compiles and to read the names of its grid variables.

While the module was being written it was run on three other pairs, which are not test cases:

- "A rejected transfer never changes the ledger" against "A transfer never changes the ledger";
- "A computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum"
  against the same statement written as "whenever ..., and ... only if ...";
- "A computation of the total for which the total of the balances of the ledger is at most the maximum is always
  accepted" against "A computation of the total is accepted whenever the total of the balances of the ledger is at
  most the maximum".

The second and third have the same shape as the cases `same_meaning_proved` and `same_on_fixture_not_proved`, on a
different operation. The equality script `pointwise` was chosen on the second pair. So those two expectations are
predictions from a close analogue, not blind ones.

None of the 48 trial sentences is used here, and nothing here was tuned to them. The sentence of the two `cross_*`
cases built on "A transfer never changes the total of all balances" is the one the scout quotes as the silent
wallet-versus-ledger choice (`docs/studies/2026-11-12/first-wave-scout.md`, finding 6).
