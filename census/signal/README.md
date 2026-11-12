# census/signal/ — libsignal-protocol v0.105.4 as an eleventh census row (plan node S1a)

Question (docs/studies/2026-11-12/signal.md, sections 3 and 4): does the Rust that DeepMind verified at machine-code
level pass through Charon and Aeneas at all? The study predicted not; this directory measures it.

| File | What |
|:--|:--|
| `frozen.json` | target commit, definitions, the three entry points, the ratchet file, the criterion. Committed before any tool was run on the crate. |
| `run.sh` | the exact commands: `setup`, `tools`, `build`, `side`, `report`, `clean` |
| `signal_census.py` | the census driver (`../scripts/census.py`, imported unchanged) pointed at the workspace member, with the patched Aeneas of `../fork` |
| `signal_report.py` | `RESULT.md`, `result.json`, `functions.tsv` from the per-function results |
| `work/` | git-ignored: the clone, cargo's registry, the target directory, LLBC, generated Lean, Lake packages (copy-on-write clones) |

## Design notes

- **Not from crates.io.** `libsignal-protocol` is a member (`rust/protocol`) of the `signalapp/libsignal` workspace and
  is not published. The row is the workspace at tag `v0.105.4`; the Cargo package version is `0.1.0`. The driver copies
  the whole workspace and runs the inventory and Charon in `rust/protocol`; Charon's file names are mapped back to the
  crate root. Only `rust/protocol/src` is in the denominator (`tests/`, `benches/`, `examples/`, `fuzz/` and
  `#[cfg(test)]` code are excluded, as in the census). Code that `build.rs` generates from the `.proto` files (prost) is
  not source and is not in the denominator, like cedar's generated parsers.
- **Translator.** The reported row uses `aeneas-p5` (the fork spike's patches (i)-(v) on Aeneas `0d21a9ec`) with the
  release Charon 0.1.315 and the Aeneas Lean library of nightly-2026.11.09 on Lean v4.35.0, exactly as
  `../fork/scripts/fork_census.py` mode `shipped`: one Charon run, one Aeneas run, nothing marked or removed.
- **An `async fn` counts as one function**: the census join attaches every LLBC declaration inside the function's span
  (the function and its coroutine body) to it, and all of them have to be translated for the function to count.
- **Cargo home.** `CARGO_HOME` is `work/cargo-home`, so the crate's dependencies do not land in `~/.cargo` and go away
  with `./run.sh clean`.
- **Not part of the ten.** The row is not added to `data/selection/pins.json` or to the generated `CENSUS.md` tables:
  the ten crates were drawn by a seeded rule and this one was chosen by hand.

## Run

    ./run.sh setup && ./run.sh tools && ./run.sh build && ./run.sh side && ./run.sh report
    ./run.sh clean        # removes work/
