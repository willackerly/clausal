# census/signal/ — libsignal-protocol v0.105.4 as an eleventh census row (plan node S1a)

Question (docs/studies/2026-11-12/signal.md, sections 3 and 4): does the Rust that DeepMind verified at machine-code
level pass through Charon and Aeneas at all? The study predicted not; this directory measures it.

| File | What |
|:--|:--|
| `frozen.json` | target commit, definitions, the three entry points, the ratchet file, the criterion. Committed before any tool was run on the crate. |
| `run.sh` | the exact commands: `setup`, `tools`, `build`, `side`, `report`, `clean` |
| `signal_census.py` | the census driver (`../scripts/census.py`, imported unchanged) pointed at the workspace member, with the patched Aeneas of `../fork` |
| `signal_report.py` | `RESULT.md`, `result.json`, `functions.tsv` from the per-function results |
| `axiom_check.py` | cross-check of the "no axiom beneath" column by Lean itself (`Lean.collectAxioms`) -> `axioms.json` |
| `RESULT.md` | **the result** (generated). `result.json` is the same in data form, `functions.tsv` has one line per function of the reported row |
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

- **Path mapping.** Charon names the crate's files relative to the workspace root (`rust/protocol/src/...`) and
  Aeneas repeats those names in its log; both are mapped to the crate root before the census join, otherwise no error
  would be attributed to a function.
- **Denominator.** `rust/protocol` also holds two helper packages (`test-support/`, `cross-version-testing/`). The
  census inventory walks them (60 functions); they are other Cargo packages, are not in Charon's output, and
  `signal_report.py` leaves them out, as `frozen.json` says ("in rust/protocol/src").
- **Side row.** `pinned` runs the pipeline's unpatched release Aeneas on a copy of the same LLBC, so the two rows differ
  only in the Aeneas binary. No `cw` row was run: Charon gave an LLBC as shipped.

## Run

    ./run.sh setup && ./run.sh tools && ./run.sh build && ./run.sh axioms && ./run.sh side && ./run.sh report
    ./run.sh clean        # removes work/

Heavy steps go through `tools/sem.sh 3`. Measured on 2026-11-12 on a shared machine: Charon 16 s (after the first
dependency build, about 25 s), patched Aeneas 446 s on a 2.0 GB LLBC, `lake build` 23 s, the axiom check about a minute.
Disk: `work/` shows as about 20 GB in `du`, of which about 14.5 GB are copy-on-write clones of the Lake packages and the
Aeneas library that take no new space; new data is about 5 GB (two copies of the LLBC, the cargo target directory, cargo's
registry).

## Reading the result

All numbers are in `RESULT.md`; nothing here is a second source. What to keep in mind when reading it:

- **The outcome is decided by a conjunction.** The frozen rule says "not a Route A target" only if no entry point
  translates *and* fewer than 10% of functions compile with no axiom beneath them. The first half holds, the second does
  not, so the rule does not fire. That is not the same as "libsignal is a Route A target".
- **Every `async fn` stops at Charon** ("Coroutines are not supported"): the three entry points and their helpers,
  and the async functions of `group_cipher.rs`, `sealed_sender.rs` and `storage/inmem.rs` (the "Charon" column of the
  by-file table). These are the functions that take a store.
- **One type accounts for the largest block of Aeneas failures**: `SignalProtocolError` holds a `Box<dyn Error ...>`,
  Aeneas cannot translate the type ("Dynamic trait types are not supported yet"), and the functions that mention it go
  with it (the first line of the first-message table).
- **The function share over-reads the code share.** The functions with no axiom beneath are mostly accessors and
  constructors (median three lines); by code lines the share is below 10% on the census column.
- **Three readings of "no axiom beneath"** are reported, because the census column is a token scan and misses axioms
  reached through a structure or a trait instance. The frozen definition is the census column; the Lean elaborator's
  strict answer is lower, and both are above the threshold.
- **Not checked:** whether the translated functions mean what the Rust means (no Rust-against-Lean run was done here),
  `spqr`, and the unpatched/patched difference beyond the one side row.
