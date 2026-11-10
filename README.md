# lean-rosette

Tools and experiments for making large formal proofs navigable by people, and for tying plain-English claims to machine-checked statements about real code.

The project started from a brainstorm (`Decompiling Lean Proofs Like Code.pdf`): AI-generated Lean proofs are verified but hard to read, so could they be "decompiled" into libraries of small, meaningful pieces? Several versions of that idea have now been tested against real data. Most of the scoring ideas failed; the tooling and the software-side slice work. This file is the map.

**Status: research prototype, 2026-11-10.** Apache-2.0. Three background runs were still in progress when this was written; their rows below are marked.

## Start here

| If you want | Read |
|---|---|
| What has been tried and what happened | `docs/EXPERIMENTS.md` |
| What to do next | `TODO.md` |
| Why each call was made, and how to undo it | `DECISIONS.md` |
| To get a machine working | `docs/SETUP.md` |
| The shared graph format | `docs/SCHEMA.md` |
| How this applies to TDFLite | `docs/TDFLITE.md` |
| Rules for agents working here | `AGENTS.md` |

## Results so far

| Question | Answer | Status | Detail |
|---|---|---|---|
| Does "proof hidden per unit of statement" find the lemma boundaries humans choose inside a proof? | No. First pick 7.7%; at chance for small helpers; worse than random at choosing where to stop | Final, reviewed | `out/FINDINGS.md` |
| Does the original "small goal state" idea find them? | No. Worse than random | Final, reviewed | `out/FINDINGS.md` |
| Do statements recur across proofs in human-written Mathlib? | Not usefully: 0.2% of proof size after removing trivia | Final, reviewed | `out/reuse/REUSE.md` |
| Can pieces of a proof be lifted into real lemmas soundly? | Yes. Kernel-checked, no failures on 1,274 theorems | Final, reviewed | `Rosette/Lift.lean` |
| Are the lifted statements readable? | Sometimes: good for Pell and Erdős–Ginzburg–Ziv, poor for a Sobolev inequality | One rater, three theorems | `out/demo/README.md` |
| Was the idea new? | Partly not. Single-proof extraction is published (Proof-Refactor); the ratio is published as a descriptive measure | Checked by web search | `out/prior_art.md` |
| Can English scenarios be bound to proofs about real Rust? | Yes on a 45-line wallet: 7 proved for all inputs, a false claim refuted with a counterexample | Final, reviewed | `slice/FINDINGS.md` |
| Does that survive loops and collections? | In progress | Running | `slice/ledger/` |
| Do dominators in the lemma graph predict what humans put in a blueprint? | Preliminary no: graph signal is mostly proof size; "has a docstring" does as well | Awaiting review | `out/corpus/validation/VALIDATION.md` |
| Does the machine-generated Navier–Stokes proof have a recoverable outline? | Preliminary partial: 13 statements cover 54% of the proof, but most are not readable on their own | Awaiting review | `out/corpus/outline/` |
| Is there more redundancy in machine proofs than in Mathlib? | In progress | Running | `out/corpus/reuse/` |
| Where do analysis proofs spend their bulk (casts, measurability, constants)? Do "packets" help? | In progress | Running | `out/corpus/friction/` |

The recurring lesson: sizes and graph positions are measurable but do not by themselves identify what a mathematician finds meaningful. In the machine corpus the content sits in definitions, so an outline has to present those, not lemma signatures.

## Layout

| Path | What it is |
|---|---|
| `Rosette/`, `Rosette.lean`, `lakefile.toml` | Root Lean 4 + Mathlib project: candidate enumeration, lifting, Mathlib benchmarks |
| `bench/` | Benchmark corpus and scoring scripts (Python and shell) |
| `out/` | Results: `FINDINGS.md`, per-experiment reports, raw data, reviewers' evidence |
| `out/corpus/` | Exports and analyses of the external corpora |
| `corpora/` | External Lean projects, each with its own pins: `ns` (OpenAI Navier–Stokes/Euler, machine-generated), `pfr`, `carleson` (human-written, with blueprints), plus exporters |
| `slice/` | Gherkin → Lean → Rust vertical slice; separate Lake project and Rust crates |
| `docs/` | Schema, experiment inventory, setup, TDFLite notes |
| `tdflite-ideas/` | The owner's TDFLite verification plan (input, not produced here) |

## Quick commands

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"

# Root project (about 1 minute; also regenerates demo outputs)
lake build Rosette

# Try the lifter on any theorem: add to a scratch .lean file importing Rosette.Lift
#   #rosette_lift Pell.exists_of_not_isSquare (k := 5)

# Mathlib benchmarks
bench/run_bench.sh        # boundary recovery (H1)
bench/run_reuse.sh        # reuse (H2), about 20 minutes

# Vertical slice
cd slice && ./run.sh      # report in slice/out/report.md
```

`docs/SETUP.md` has toolchains, disk use and how to rebuild the corpora.

## How the work is done

- Each idea is stated as a hypothesis, measured on real Lean data, attacked by independent reviewers, then fixed and rerun. Negative results are kept.
- Data comes from Lean's own environment, not from text matching.
- Judgement calls and system installs go in `DECISIONS.md` with an undo step.
