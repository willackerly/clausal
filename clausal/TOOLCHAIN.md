# clausal/ toolchain: Rust -> Charon -> Aeneas -> Lean

> **Update (same day, after the wallet slice was implemented).** The example crate described below
> (`rust/`, `checked_add`, `lean/Proofs/CheckedAdd.lean`) has been REPLACED by the wallet crate
> `wallet/` and the scenario pipeline (`./run.sh`, see `README.md`). Paths in this file have been
> updated (`rust/` -> `wallet/`, `Slice.lean` -> `Wallet.lean`); the section "What is proved" about
> `checked_add_spec` / `checked_add_total` is historical: those theorems were removed with the crate.
> `./translate.sh --check` still works (translate, then `lake build`). Versions, pins, timings,
> gotchas and undo steps below are unchanged and still accurate.


> **Update 2026-11-12 (plan node R1).** The `aeneas` executable that translates is now a **setting of
> `translate.sh`**, and its default is the patched build from `census/fork` (five patches), not the
> release binary. Charon, the Aeneas Lean library, the Rust nightly, Lean and Mathlib are unchanged and
> still come from the release tarball. See "The patched translator" below; the rest of this file
> describes the release tools and is still accurate for them.

Status: **working end to end on this machine** (macOS arm64, Darwin 25.6.0) on 2026-11-09,
using prebuilt binaries only. Nothing was built from source; no OCaml/opam needed.

    wallet/src/lib.rs --charon--> build/wallet.llbc --aeneas--> lean/Generated/Wallet.lean
                                                             lean/translation.json
    lean/Proofs/CheckedAdd.lean  (hand-written, kernel-checked, imports Generated.Slice)

One command regenerates and re-checks everything: `./translate.sh --check`.

## Exact versions

| Thing | Version | Where it lives |
|---|---|---|
| Aeneas | `nightly-2026.11.09-5a392f4` (GitHub release asset `aeneas-macos-aarch64.tar.gz`, sha256 `b1d5ffeb85646b3a1944977068354a9f0ef257307dc3d391d874f19528b118f9`) | `clausal/.tools/aeneas-nightly-2026.11.09-5a392f4/aeneas` |
| Aeneas, patched (the default translator since R1) | upstream `0d21a9ec7bbbb110110cacc14464a47fd71c8705` (nightly-2026.11.10) + the five patch files of `census/fork/patches/`; binary sha256 `7dca4ee8d2168a98f284ada0a64f8f674dabba7c0b407010ebd29d5a14a458a9`; prints `aeneas 81c0b10c-dirty` | `census/fork/bin/aeneas-p5` (git-ignored build output; built from source, see below) |
| Charon | `0.1.315 (454586e9b770231e66d2062993e632dfc06463e2)`, shipped in the same tarball (`charon`, `charon-driver`) | same directory |
| Rust for Charon | `nightly-2026-09-17` = `rustc 1.100.0-nightly (923c95cdf 2026-09-16)`, components `rustc-dev llvm-tools rust-src miri`, host target only | `~/.rustup/toolchains/nightly-2026-09-17-aarch64-apple-darwin` (1.1 GB) |
| Aeneas Lean library | the copy shipped in the same tarball (`backends/lean`, with prebuilt `.lake/build`) | `clausal/.tools/aeneas-nightly-2026.11.09-5a392f4/backends/lean` |
| Lean | `leanprover/lean4:v4.35.0` (copied from the Aeneas library's `lean-toolchain`) | `~/.elan/toolchains/` (installed automatically by elan) |
| Mathlib | tag `v4.35.0`, rev `56a005855ea17e0b0958f73ec801ae140b0a1679` (transitive, via Aeneas) | `clausal/lean/.lake/packages/mathlib`, oleans from the Mathlib cache |

`clausal/lean/lake-manifest.json` pins all nine transitive packages; its revs are identical to the
manifest shipped inside the Aeneas tarball (checked with `diff`).

The repo root uses Lean `v4.36.0-rc2`; the slice uses `v4.35.0`. They do not share a `.lake`.

## Layout

    clausal/
      translate.sh            regenerate (and optionally check) everything
      TOOLCHAIN.md            this file
      rust/                   cargo library crate `slice` (the real code)
        rust-toolchain.toml   same nightly as Charon, so `cargo test` uses the compiler Charon uses
      build/wallet.llbc        Charon output (intermediate, ignored)
      lean/                   Lake project `slice`
        lean-toolchain        leanprover/lean4:v4.35.0
        lakefile.toml         requires `aeneas` by path into .tools/ (exact match to the binary)
        Generated/Wallet.lean  AENEAS OUTPUT - never edit
        translation.json      AENEAS OUTPUT - Rust item -> Lean name/file/source-lines map
        provenance.json       sha256 of translation inputs and outputs + tool versions
        Proofs/CheckedAdd.lean  hand-written theorems
        Proofs/Audit.lean     `#print axioms` for each theorem
      .tools/                 downloaded tools (ignored, 700 MB)
        .lake/                Mathlib + deps with cached oleans (ignored, 7.2 GB)

## Every command, in order, with timings (wall clock, this machine)

All with `export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"`.

1. Find a binary (there is a macOS arm64 asset on every nightly):
   `curl -s "https://api.github.com/repos/AeneasVerif/aeneas/releases?per_page=5"`
2. Download and unpack - **13 s + 1 s** (158 MB, 549 MB unpacked):

       mkdir -p clausal/.tools/dl clausal/.tools/aeneas-nightly-2026.11.09-5a392f4
       curl -fsSL -o clausal/.tools/dl/aeneas-macos-aarch64.tar.gz \
         https://github.com/AeneasVerif/aeneas/releases/download/nightly-2026.11.09-5a392f4/aeneas-macos-aarch64.tar.gz
       tar xzf clausal/.tools/dl/aeneas-macos-aarch64.tar.gz -C clausal/.tools/aeneas-nightly-2026.11.09-5a392f4

3. Install the Rust nightly named in the tarball's `rust-toolchain` - **37 s**:

       rustup toolchain install nightly-2026-09-17 --profile minimal -c rustc-dev -c llvm-tools -c rust-src
       rustup component add --toolchain nightly-2026-09-17-aarch64-apple-darwin miri

4. Charon (run inside `clausal/rust`) - **12.7 s the first time** (it builds a full-MIR sysroot
   into `~/.cache/charon/miri-sysroot/nightly-2026-09-17`), **~1.5 s afterwards**:

       charon cargo --preset=aeneas --dest-file ../build/wallet.llbc

5. Aeneas - **0.3-0.5 s**:

       aeneas -backend lean -dest clausal/lean -subdir Generated -emit-json \
         -warnings-as-errors -no-progress-bar clausal/build/wallet.llbc

6. Lake project, first time (inside `clausal/lean`) - **1 min 46 s** total: installs Lean v4.35.0
   via elan, clones Mathlib + 8 packages, and Mathlib's post-update hook runs
   `lake exe cache get` itself (9031 files). Mathlib was never compiled.

       lake update

7. Build - **9 s first time, 3-7 s after** (1807 jobs, all but ours replayed from prebuilt
   oleans; the Aeneas library's shipped `.lake/build` is accepted as-is, not rebuilt):

       lake build

8. Rust tests (the "tested" shadow of the theorems) - **< 1 s**: `cargo test` in `clausal/rust`.

Steps 2-5 and 6-7 are what `./translate.sh --check` does; the fresh-download path of
`--setup` was exercised in a scratch directory (10.6 s, checksum OK).

## The patched translator (plan node R1)

**What changed.** `translate.sh` has two more pins, `TRANSLATOR` and `AENEAS_WARNINGS`, and runs the
`aeneas` executable they select. Nothing under `clausal/.tools/` is modified or added.

| setting | values | default | override for one run |
|---|---|---|---|
| `TRANSLATOR` | `patched`: `census/fork/bin/aeneas-p5`. `release`: `.tools/aeneas-<tag>/aeneas`, the binary used before R1 | `patched` | `./translate.sh --translator=release`, or `CLAUSAL_TRANSLATOR=release ./run.sh` |
| `AENEAS_WARNINGS` | `error`: pass `-warnings-as-errors`. `allow`: do not | `error` | `./translate.sh --warnings=allow`, or `CLAUSAL_AENEAS_WARNINGS=allow ./run.sh` |

- **Only the `aeneas` executable differs.** `charon`, `charon-driver`, the `rust-toolchain` pin and the
  Lean library required by `lean/lakefile.toml` are the release's (`nightly-2026.11.09-5a392f4`) under
  both settings. The patched binary is built on the next upstream commit (`0d21a9ec`); `census/fork/FORK.md`
  says its only source difference from the release commit is three Lean keywords.
- **The binary is pinned by sha256** (`AENEAS_FORK_SHA256`). A file with another hash is refused; there is
  no silent fallback to the release binary.
- **The five patches are pinned by file name and sha256** (`AENEAS_FORK_PATCHES`). Where the checkout has
  `census/fork/patches/`, the files are hashed on every run and a difference stops the run. This checks
  the patch files against the pin, not the binary against the patch files: that the binary was built from
  them rests on `census/fork/FORK.md` ("Carrying the fork").
- **Where the binary is looked for**, first hit wins: `$CLAUSAL_AENEAS_PATCHED`; `../census/fork/bin/`
  of this checkout; beside the real directory behind a symlinked `.tools` (git worktrees made by
  `tools/wt.sh`, working copies made by `mutation/workcopy.sh`); the main checkout of this git worktree.
- **What is recorded.** `lean/provenance.json` has a `translator` object: `variant`, `version` (what
  `aeneas -version` prints), `binary_sha256`, `warnings_as_errors`, `release` (the tag Charon and the
  Lean library come from) and, for `patched`, `base_commit` and `patches` (five `{id, sha256}`). Its
  `aeneas` string, which the report prints, names the variant too. `lean/translation.json` carries
  Aeneas's own `aeneas_version`.
- **The version string `81c0b10c-dirty` is misleading.** `81c0b10c` is the fork's fourth patch commit and
  "dirty" is the fifth patch, not yet committed when the binary was built. Identify the binary by its
  sha256, not by this string. A rebuild from the committed branch may print another string; any rebuild
  with another hash needs a new pin.

**Is `-warnings-as-errors` dropped?** No, it did not need to be. Both fixtures translate with the patched
binary and the flag on, exit 0, and `Generated/Wallet.lean` and `Generated/Ledger.lean` are byte-identical
to the release binary's with the flag on and with it off. The flag stays on by default because it is the
stricter check.

**What `--warnings=allow` does and does not do (corrected in the R1 fix round).** It only stops Aeneas from
turning warnings into a stop at the first one. It is **not enough** for a crate that needs patch 0002 or
0003 (plan node R2). Measured with the patched binary on the three repro crates of `census/fork/repro/`
(`abort_copied`, `crash_stack_of_refs`, `mixed_group`):

| flag | Aeneas exit | output |
|---|---|---|
| `-warnings-as-errors` | 2 | no `.lean` file |
| (none) | 1 | a partial `.lean` file; the log has `[Error]` lines and "Generated the partial file (because of N errors...)" |

So the items the patches let Aeneas skip are logged as errors, not warnings. Aeneas fails either way; the
flag only decides whether it writes nothing (exit 2) or a partial file (exit 1). `translate.sh` stops on any
nonzero exit of Aeneas, under both settings: it prints the exit code, leaves `lean/Generated` incomplete
and **removes `lean/provenance.json`** at the start of every translation, so a failed run never leaves the
previous run's provenance beside half-written output (restore with
`git checkout -- lean/Generated lean/provenance.json lean/translation.json`). There is no setting that
accepts a partial file. R2 needs one (accept exit 1, record in the provenance file that the model is
partial and which items were skipped); that is a decision about what the pipeline trusts and was not
made in R1. For the two fixtures the setting changes nothing: they translate with exit 0 under both.

**What a fresh machine must do to obtain the patched binary.** There is no download: it is built from
source. `census/fork/` in git holds the five patch files, `env.sh` and `FORK.md`; the clone, the opam
root and `bin/` are git-ignored. The commands are those of `census/fork/FORK.md`, "Carrying the fork"
(macOS arm64, about ten minutes, most of it compiling OCaml):

    brew install opam pkgconf gmp
    cd census/fork
    git clone https://github.com/AeneasVerif/aeneas.git aeneas
    git -C aeneas checkout -b census-fork 0d21a9ec7bbbb110110cacc14464a47fd71c8705
    git -C aeneas am "$PWD"/patches/000*.patch

    export OPAMROOT="$PWD/.opam"
    opam init --bare --no-setup -y
    opam switch create aeneas ocaml-base-compiler.5.3.0 -y
    source env.sh

    git clone https://github.com/AeneasVerif/charon.git aeneas/charon
    git -C aeneas/charon checkout "$(tail -1 aeneas/charon-pin)"      # 454586e9
    opam install -y --deps-only aeneas/charon/charon-ml aeneas/src
    (cd aeneas/charon && make build)        # needs the Rust nightly of ../../clausal/translate.sh --setup
    (cd aeneas && make build-bin-dir)
    mkdir -p bin && cp aeneas/src/_build/default/main.exe bin/aeneas-p5
    shasum -a 256 bin/aeneas-p5 && bin/aeneas-p5 -version

Then:

- **The rebuilt binary may not have the pinned sha256** (the embedded version string may differ, and
  nobody has checked that the OCaml build is reproducible across machines). If it does not, check
  it instead by behaviour: `./translate.sh --translator=release`, keep `lean/Generated/`, then point
  `CLAUSAL_AENEAS_PATCHED` at the new binary with its hash as `AENEAS_FORK_SHA256` and confirm that
  `lean/Generated/*.lean` is byte-identical. Commit the new pin with a line in `DECISIONS.md`.
- **The binary links Homebrew's `gmp` dynamically** (`/opt/homebrew/opt/gmp/lib/libgmp.10.dylib`), so
  copying it from another machine works only if `brew install gmp` has been run and the architecture is
  the same. The release binary carries its own copy in `libs/`.
- **Without the binary** `./translate.sh`, `./translate.sh --setup` and `./run.sh` stop (exit 1) with a
  message naming this section. On a fresh clone the order is therefore:
  `./translate.sh --setup --translator=release` (downloads the release tarball, installs the Rust nightly;
  this still needs no OCaml), then either build the patched binary as above and run `./run.sh`, or stay on
  the release binary with `CLAUSAL_TRANSLATOR=release ./run.sh`.
  `CLAUSAL_TRANSLATOR=release ./run.sh` runs the pipeline on the release binary; for the two fixtures the
  generated models are the same bytes.
- These build steps were not rerun for R1. `FORK.md` says the opam steps were reconstructed from logs and
  not executed a second time, and that the `git am` and build steps were.

**Undo.** Set `TRANSLATOR="release"` in `translate.sh` (or revert the R1 commit) and rerun
`./translate.sh`; `lean/provenance.json` and `lean/translation.json` return to the release values.

## What was proved

`lean/Proofs/CheckedAdd.lean`, about the generated `slice.checked_add`, for all `a b : U32`:

- `checked_add_spec`: if `a + b <= u32::MAX` the result is `ok (Ok s)` with `s = a + b` (as
  naturals); if `a + b > u32::MAX` the result is `ok (Err Overflow)`.
- `checked_add_total`: the function always returns (`ok r`), i.e. it never panics.

`lake build` prints, via `Proofs/Audit.lean`:
`depends on axioms: [propext, Classical.choice, Quot.sound]` for both - no `sorryAx`.

## Trust boundary (what the kernel check does and does not cover)

- **kernel-checked**: the two theorems, about the Lean term `slice.checked_add`.
- **tool-trusted**: that `Generated/Wallet.lean` means what `wallet/src/lib.rs` means. This rests on
  rustc's MIR, Charon, Aeneas, and - specific to this example - Aeneas's hand-written Lean model
  of `u32::checked_add` (`Aeneas/Std/Scalar/CheckedOps/Add.lean`: `Option.ofResult (x + y)`).
  The Rust body of `core::num::checked_add` is NOT translated; the library model stands in for
  it. `provenance.json` records the hashes on both sides of this edge.
- **tested**: `cargo test` (2 examples) runs the real compiled code.

## Gotchas

- **The release tarball is self-contained.** It ships `aeneas`, `charon`, `charon-driver`,
  `libs/libgmp.10.dylib`, the `rust-toolchain` file Charon needs, and the Lean library with a
  prebuilt `.lake/build`. The binaries ran without quarantine/codesign trouble (downloaded with
  curl, which sets no quarantine attribute; a browser download would).
- **Charon needs the exact nightly, with `rustc-dev`.** `charon-driver` links
  `librustc_driver-*.dylib` from that toolchain. `charon toolchain-version` prints what it wants.
  The upstream `rust-toolchain` also lists 7 cross targets; they are not needed for a host build.
- **Without the `miri` component Charon still works but warns** (`cargo miri setup failed ...
  falling back to rustc's default sysroot`), which means std function bodies have no MIR. Irrelevant
  for this example (the std call is modelled by Aeneas), but it would bite as soon as real std
  code needs translating, so `miri` is installed.
- **Charon writes outside the repo**: `~/.cache/charon/miri-sysroot/` (107 MB).
- **Use `--preset=aeneas`** on `charon cargo` (the option set Aeneas expects). Running without
  it was not tried.
- **`derive`s are translated too.** `#[derive(Debug, PartialEq, Eq)]` on the error enum yields
  five extra Lean definitions (trait impls). Harmless here; on real code each derive is extra
  surface that must be supported by the Aeneas std model.
- **Generated files use the Lean module system** (`module` / `public import Aeneas` /
  `@[expose] public section`). A plain (non-module) file can import them. But closing a goal
  of the form `(do let o <- ok x; ...) = ok y` with `rfl` failed with a confusing "type mismatch"
  (probable cause, not confirmed: `Result`'s bind is not exposed across the module boundary);
  rewriting with the library's simp lemmas works (`simp only [lift, bind_ok]`).
  `-use-lean-modules false` exists if this becomes a nuisance.
- **File/module naming**: Aeneas names the file after the crate (`Slice.lean`) and the namespace
  after the crate in lower case (`slice`). With `-dest lean -subdir Generated` the module is
  `Generated.Slice`. The lakefile uses `globs = ["Generated.+"]` so new generated files are
  picked up without edits.
- **`lake update` already fetches the Mathlib cache** (Mathlib post-update hook), so a separate
  `lake exe cache get` is only needed if that hook is interrupted; `translate.sh --check` covers
  both cases.
- **Path dependency, not git.** `lakefile.toml` requires `aeneas` by path into `.tools/`. That is
  the exact library the binary was released with and it is prebuilt; the cost is that
  `.tools/` must exist (run `./translate.sh --setup`) before `lake` works in `clausal/lean`.
  Alternative if a git pin is preferred: `git = "https://github.com/AeneasVerif/aeneas"`,
  `rev = "5a392f4"` (short hash from the tag; resolve to the full hash), `subDir = "backends/lean"`
  - untested here.
- **`-emit-json` is worth keeping**: `translation.json` maps every Rust item to its Lean name,
  file and source line range, and flags `can_fail` / `can_diverge` / `is_opaque`. That is the
  machine-readable form of the tool-trusted edge.
- **Not tried**: traits with generics, external crates. (Historical note: this line used to list
  loops and `&mut` borrows too; see the next item.)
- **Loops and collections (added with the `ledger/` crate, same pins).** Translated at the first
  attempt, in 0.9 s (Charon) + 1.2 s (Aeneas): `Vec<u64>` field, `&[T]` argument, `while` loops with
  `break` and early `return`, `v[i]` reads and writes, `v.len()`, `checked_add`, `Vec::clone`,
  a `&mut self` method calling another `&mut self` method inside a loop. Probed one at a time in a
  scratch crate, also fine: `?` on `Option`, `for x in slice`, `Vec::get`, `slice::get`, `Vec::push`,
  `Result<_, enum>` returns. **Failed** with this Aeneas: `for i in 0..n` (no builtin information for
  the trait `core::iter::range::Step`), `slice.iter().sum()` (no builtin information for `Iterator`),
  `iter().try_fold(...)` with a closure (internal error in `SymbolicToPureTypes`). So index-based
  `while` loops are the form to write.
- **A loop is not translated to a recursive function** in this version. `while` gives
  `<fn>_loop.body` (attribute `@[rust_loop_body]`, one iteration, returns
  `ControlFlow.cont state | ControlFlow.done result`) and `<fn>_loop` (`@[rust_loop]`), defined as
  `loop (fun state => <fn>_loop.body ...) initial`; the function itself becomes a `@[reducible]`
  one-liner calling `<fn>_loop`. `translation.json` lists all three under the same `rust_name`, and
  marks all of them `can_diverge: true`. The source span of a loop can be wrong (`apply_batch_loop`
  is reported as lines 1-70).
- **`translate.sh` now takes a crate list** (`CRATES="wallet ledger"`); Aeneas writes one
  `translation.json` per run, so the per-crate files are kept in `build/` and merged into
  `lean/translation.json` with a `crate` field on every item.
- **No `step` lemma for `Vec<u64>::clone`** ships with the Aeneas library (`Slice.clone_spec`
  exists); `lean/Ledger/Lemmas.lean` has the six-line missing one.
- **Repo `AGENTS.md` "zero cold-start" rule**: it names `src/daemon/...` bridges that no longer
  exist (moved to `_to_delete/`). Checks here use `lake build` inside `clausal/lean` (3-7 s warm),
  never `lake env lean` in a loop.

- **Disk**: the slice costs about 12 GB in total - `clausal/lean/.lake` 7.2 GB (Mathlib oleans),
  Lean v4.35.0 2.8 GB, Rust nightly 1.1 GB, `.tools` 0.7 GB, Charon cache 0.1 GB.

## Undo

    rm -rf clausal/.tools clausal/build clausal/wallet/target clausal/wallet-bdd/target clausal/lean/.lake
    rustup toolchain uninstall nightly-2026-09-17
    elan toolchain uninstall leanprover/lean4:v4.35.0
    rm -rf ~/.cache/charon
