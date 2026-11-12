# AGENTS.md

Rules for agents working in this repository. For the state of the project and how work is run here, read `docs/HANDOFF.md` first.

- Repo root is a Lean 4 + Mathlib project (library `Rosette`). `clausal/` and anything under `corpora/` are separate Lake projects with their own version pins; do not mix them.
- Use `export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"`. Check single files with `lake env lean <file>`; never run `lake update` or edit a manifest or toolchain file without logging it.
- Data that is meant to come from Lean must come from Lean. No hand-written traces, no regex over source where the elaborator can answer.
- Report negative results as negative. Every headline number must be reproducible from a script in the repo.
- Log judgement calls and system-level installs in `DECISIONS.md` (append only: what, why, how to undo).
- Read `out/FINDINGS.md` before proposing a scoring idea: the proof-per-statement ratio and the "small goal state" idea have both been tested and failed.
- Cold start: `README.md` (what and why), `docs/ARCHITECTURE.md` (design), `docs/RESULTS.md` (results), `docs/EXPERIMENTS.md` (what was tried), `TODO.md` (what is next), `docs/SETUP.md` (toolchains). Update those when an experiment's status changes.
- TDFLite may be named and discussed in tracked files, and `tdflite-ideas/` and `docs/TDFLITE.md` are tracked (owner, 2026-11-11). `private/` stays git-ignored. Never modify the owner's other repositories (`/Users/will/dev/TDFLite`, `private/tdflite-src`), with one exception granted by the owner on 2026-11-12: `/Users/will/dev/TDFLite-Rust`, a separate clone of TDFLite on branch `rust/core`, is where the Rust decision core is to live; agents may work there, branch and make worktrees from it, and the orchestrator may merge to its main when appropriate. Pushing there and merging to main are the orchestrator's acts, not a builder's. `tdf-core` is the owner's top operational priority; keep it de-emphasised in `README.md`.
- Names: the project is Clausal (the language), the Clausebook (the library) and the Clausal compiler. The tool directory is `clausal/` (Python package `clausal/clausal`, run as `python3 -m clausal` from `clausal/` or `clausal/bin/clausal` from anywhere) and the Clausebook file is `clausal/clausebook.yaml`; they were `slice/`, `slicegen` and `vocabulary.yaml` before the rename commit, and frozen records (`clausal/compare/`, `clausal/review/`, `p2/`, raw logs) still say so. The repository and its checkout are still `lean-rosette`, and the Lake package in `clausal/lean` is still named `slice`.
- `.feature` Clausal is strict: one live form per piece per position, every form in the signed book. Wording changes by replacing a form (checked, logged), never by adding a second one; phrasing help belongs in `clausal compose` (plan track Q).
- Work in your own git worktree (`tools/wt.sh <name>`) or scratch copy; one owner per directory; run every `./run.sh`, cargo, Charon or Kani job through `tools/sem.sh 3 -- <command>`; stop only processes started from your own directory.
- Agents may not edit rules, vocabulary or statements to make a proof go through.
