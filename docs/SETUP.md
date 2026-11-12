# Setup and cold start

How to get from a fresh shell, or a fresh machine, to running things. Developed on macOS arm64, 18 cores; nothing has been tried on another platform.

## Every shell

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
```

`elan` was installed without touching shell profiles, so this line is needed each time (or add it to your profile).

## What is installed outside the repo

| Thing | Where | Why | Undo |
|---|---|---|---|
| elan | `~/.elan` | Lean toolchain manager | `rm -rf ~/.elan` |
| Lean 4.36.0-rc2 | `~/.elan/toolchains` | root project, PFR | `elan toolchain uninstall …` |
| Lean 4.36.0-rc1 | same | Carleson | same |
| Lean 4.35.0 | same | slice (Aeneas's pin) | same |
| Lean 4.34.0-rc2 | same | Navier–Stokes corpus | same |
| Rust nightly-2026-09-17 | `~/.rustup/toolchains` | Charon needs this exact compiler | `rustup toolchain uninstall nightly-2026-09-17` |
| Charon sysroot cache | `~/.cache/charon` | built on first run | `rm -rf ~/.cache/charon` |
| Mathlib download cache | `~/.cache/mathlib` | shared by all projects | safe to delete; re-downloads |
| cucumber, tokio crates | `~/.cargo/registry` | slice test runner | shared cache |

Charon, the Aeneas Lean library and the release `aeneas` binary come from a prebuilt release under `clausal/.tools/` and need no OCaml. Since plan node R1 the default translator is a patched `aeneas` built from source in `census/fork/` (git-ignored: `census/fork/aeneas`, `census/fork/.opam`, `census/fork/bin/aeneas-p5`); building it needs `brew install opam pkgconf gmp` and an opam switch with OCaml 5.3.0 kept inside `census/fork/.opam` (undo: `rm -rf census/fork/.opam census/fork/aeneas census/fork/bin`, `brew uninstall opam pkgconf gmp`). The pipeline also runs on the release binary alone (`CLAUSAL_TRANSLATOR=release`), with no OCaml.

## Projects and their pins

Each of these is a separate Lake project. Do not run `lake update` in any of them, and do not mix their toolchains.

| Project | Path | Lean | Disk | Build |
|---|---|---|---|---|
| Rosette (root) | `.` | 4.36.0-rc2 | 7 GB | `lake exe cache get && lake build Rosette` (1 min after cache) |
| Clausal | `clausal/lean` | 4.35.0 | 16 GB with tools | with the patched translator present (`census/fork/bin/aeneas-p5`, see `clausal/TOOLCHAIN.md`): `cd clausal && ./translate.sh --setup && ./run.sh`. Without it: `cd clausal && ./translate.sh --setup --translator=release && CLAUSAL_TRANSLATOR=release ./run.sh` |
| Navier–Stokes | `corpora/ns` | 4.34.0-rc2 | 16 GB | `lake exe cache get && lake build` (18 min) |
| PFR | `corpora/pfr` | 4.36.0-rc2 | several GB | `lake exe cache get && lake build` (1 min) |
| Carleson | `corpora/carleson` | 4.36.0-rc1 | several GB | same |

Total in this directory is about 55 GB, nearly all of it Mathlib copies and build output that can be regenerated.

## Rebuilding from nothing

1. Install elan: `curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --no-modify-path --default-toolchain none`.
2. Root: `lake exe cache get`, then `lake build Rosette`.
3. Clausal: follow `clausal/TOOLCHAIN.md`. `cd clausal && ./translate.sh --setup --translator=release` downloads the Aeneas release and installs the Rust nightly. The default translator is the patched binary, which is not downloaded: build it from source as in `clausal/TOOLCHAIN.md`, "The patched translator" (about ten minutes, needs opam), then `./run.sh`. Until it is built, plain `./translate.sh --setup` and `./run.sh` exit 1 saying the patched translator was not found; `CLAUSAL_TRANSLATOR=release ./run.sh` runs on the release binary (same generated models for the two fixtures).
4. Corpora: clone at the commits recorded in `DECISIONS.md` under "machine corpus" (`openai/NavierStokesAndEuler@f9e8bc5b`, `teorth/pfr@1ef23c3c`, `fpvandoorn/carleson@4dc72b29`), fetch the cache, build, then run the exporters in `corpora/tools/` and `corpora/ns_export/`. Each `out/corpus/<name>/README.md` has the exact commands.

Always use `lake exe cache get`. Compiling Mathlib from source takes hours.

## Checking a single Lean file

```sh
lake env lean Rosette/Something.lean      # about 7 s with `import Mathlib`
lake build Rosette.Something              # needed before another file can import it
```

## Things that will surprise you

- `ConstantInfo.value?` returns nothing for theorems unless called with `(allowOpaque := true)`.
- Building `Rosette` compiles `Rosette.Tests` and `Rosette.Demo`, which run at compile time and rewrite files under `out/`. Run `python3 out/demo/assemble.py` afterwards.
- `clausal/run.sh` deletes and recreates `clausal/out/`. Reviewer evidence was moved to `clausal/review/` for that reason.
- Aeneas does not translate `for` over ranges, `iter().sum()` or closures with the pinned version; use index-based `while` loops.
- Aeneas's result type cannot be evaluated by `decide`; refutations are proved, not computed.
- The Navier–Stokes and PFR repositories each contain "challenge" files restating the main theorems with `sorry`; the exporters leave them out.
- Large data files, cloned corpora and downloaded tools are untracked (see `.gitignore`); they must be regenerated, not checked out.

## Working with agents

Multi-agent runs here follow one pattern: build, evaluate, independent sceptical review, then a fix-and-rerun pass. Agents can write data, scripts and per-experiment reports, but have been blocked from creating top-level `FINDINGS.md` files; whoever orchestrates has to assemble those from the final agent's output.
