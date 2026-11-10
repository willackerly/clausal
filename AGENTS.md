# AGENTS.md

This replaces the earlier "Lean-Ghidra" constitution, whose rules referred to code that has been discarded (`_to_delete/`). Ignore any instruction that mentions KiminaBridge, PantographWorker, `extract_goal` slicing, the cognitive linter or arena worktrees.

- Repo root is a Lean 4 + Mathlib project (library `Rosette`). `slice/` and anything under `corpora/` are separate Lake projects with their own version pins; do not mix them.
- Use `export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"`. Check single files with `lake env lean <file>`; never run `lake update` or edit a manifest or toolchain file without logging it.
- Data that is meant to come from Lean must come from Lean. No hand-written traces, no regex over source where the elaborator can answer.
- Report negative results as negative. Every headline number must be reproducible from a script in the repo.
- Log judgement calls and system-level installs in `DECISIONS.md` (append only: what, why, how to undo).
- Read `out/FINDINGS.md` before proposing a scoring idea: the proof-per-statement ratio and the "small goal state" idea have both been tested and failed.
- Cold start: `README.md` (map and results), `docs/EXPERIMENTS.md` (what was tried), `TODO.md` (what is next), `docs/SETUP.md` (toolchains). Update those when an experiment's status changes.
