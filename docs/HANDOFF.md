# Handoff: state at the end of phase 1, and how to start phase 2

Written 2026-11-11 for a cold start with no memory of the earlier sessions. Read this first, then `README.md`, `docs/ARCHITECTURE.md` and `docs/PLAN.md` (the "Phase 2" section).

Nothing is running. Everything public is committed and pushed to `github.com/willackerly/lean-rosette` (branch `main`).

## What this project is, in three sentences

The goal is plain-language rules about software, each proved against the code that runs, with an honest account of what each answer rests on. Rules are written in Gherkin, compiled from a vocabulary of reusable typed pieces into Lean statements, and proved about a Lean model that Aeneas generates from Rust. A second, smaller strand studies how to make large formal proofs navigable.

The owner's stance, which governs how results are used: the destination is fixed; report measured results and trades, never a go/no-go; fail closed; toy fixtures build infrastructure and prove nothing general; people decide judgement calls and language models are labelled proxies.

## Where phase 1 ended

| Area | State | Read |
|---|---|---|
| Pipeline (`slice/`) | One command takes a rule written in the vocabulary and returns its reading in English, example rows on compiled Rust, a generated property test, a generated bounded check, a proof slot, and what each link rests on. Two toy crates. 25 frames, 96 vocabulary entries, **none signed** | `slice/FINDINGS.md`, `slice/DESIGN.md`, `slice/out/report.md` |
| Phrasing gap | 0 of 48 rules by authors who had not learned the vocabulary compiled as written; 27 after rewriting; 18 need a new piece | `trials/sentences/RESULTS.md` |
| Echo-back | Model readers catch about 92% of wrong echoes. No person has taken the trial | `trials/meaning/` |
| Proof cost | About 6 lines of Lean per line of Rust for loops; two models each proved 7 of 7 loop functions unaided in under 15 minutes on textbook loops | `p2/RESULTS.md` |
| Evidence layers | Generated tests and bounded checks find everything hand-written ones found. No injected bug needed a proof to be caught; proof adds the all-inputs result. A false rule can pass every layer if the failing case is larger than every size tried | `slice/E1_TRADES.md`, `slice/compare/TRADES.md` |
| Translator | Unpatched Aeneas handles 1% of functions in ten real crates; five small patches give 35% (82% outside one crate). The patches are **not wired into the pipeline** and **not sent upstream** | `census/CENSUS.md`, `census/fork/FORK.md`, `census/PROFILE.md` |
| TDFLite (private) | Lean model of the Go decision logic matches the Go on about 400,000 cases; the owner ruled on ten questions; guarantees 1–5 proved under the rulings, 8 given named facts; 75 test vectors; ten proposed Go changes, none applied | `private/tdflite-pilot/` (git-ignored): `OWNER_SUMMARY.md`, `t2/RULINGS.md`, `t2/AFTER-REVIEW.md`, `t3r/README.md` |
| Mathematics | Five ways of scoring proof structure failed against human judgement. A dead-code tool works on three projects. Generalising families of look-alike definitions paid in one family of seven | `out/FINDINGS.md`, `out/corpus/FINDINGS.md`, `out/deadcode/M8.md`, `out/families/FAMILIES.md` |
| Identity | A brainstorm recommends a tool-first form, the name "Readback" (and dropping "Rosette", which collides with an existing verification language), and an engineering lead who owns decision logic as the first audience. **None of it is decided** | `brainstorm/SUMMARY.md` |

Every question tested, with its answer: `docs/RESULTS.md`. How each was tested: `docs/EXPERIMENTS.md` (31 entries).

## Decisions waiting for the owner

1. **Name, form and audience** (`brainstorm/SUMMARY.md`, five questions). The README still says lean-rosette.
2. **Sign the vocabulary**, starting with the shared frames and modifiers: `cd slice && python3 -m slicegen review`. Nothing has ever been signed, so the staleness and strict-mode machinery is untested.
3. **Take the echo trial as a person** (`trials/meaning/README.md`), and recruit two or three others.
4. **Send the five Aeneas reports** (`census/fork/upstream/`, text only) and decide whether to carry the fork.
5. **TDFLite:** confirm the third D4 sub-choice and the guarantee-4 wording (`private/tdflite-pilot/t2/AFTER-REVIEW.md`); the eight decisions listed in `private/tdflite-pilot/t3r/README.md`.
6. **Publish or keep private:** `tdflite-ideas/`, `docs/TDFLITE.md` and the brainstorm PDF are untracked on purpose.
7. **Whether the mathematics strand moves to its own repository.**

## Phase 2 in one paragraph

Three things, agreed with the owner on 2026-11-11: close the phrasing gap so that sentences people naturally write compile; put a person in the loop for sign-off and the echo trial; and leave the toy crates for a real one that translates today. The nodes, their tests and their order are in `docs/PLAN.md` under "Phase 2".

## How to run work here

These are lessons from phase 1, not preferences.

- **Build, review, fix, as one unit.** Every substantial piece is built by one agent, checked by a second on a different model (Opus 5.5 reviewing Fable or the reverse), and the corrections are applied and rerun before anything is written up. Reviews found real defects every time, including a proof of `True` being counted as a proof and a proposed code change that turned a Deny into a Permit.
- **One owner per directory.** Anything that runs a pipeline does it in a scratch copy: `slice/run.sh` deletes and recreates `slice/out/`.
- **At most two heavy workflows at once**, with builds run one at a time inside each. The first night's load reached 200 on 18 cores and made every timing meaningless. Take timings alone, in a quiet window.
- **Freeze before measuring.** Thresholds, item sets and budgets go in a commit before the measured run. Test items come from a tool, a rule or a different author, never from the builder.
- **A lost proof is not a detection.** Only a rule shown false by a concrete input counts.
- **Agents may not edit rules, vocabulary or statements to get a proof through.**
- **The laptop sleeping kills agents that are mid-request.** Check `pmset -g log` and the workflow journals after any gap; relaunch what died; look for orphaned processes started from this directory and stop only those.
- **Agents cannot create top-level report files** named like `FINDINGS.md` or `REPORT.md`; they return the text and the orchestrator writes it.
- **Messaging a workflow agent that has already finished starts it again** and it will overwrite its own outputs.
- **Process kills must match a path inside the agent's own directory.** A broad kill once took out another agent's job.
- **Log every judgement call and system install** in `DECISIONS.md` (append only: what, why, how to undo).

## Privacy rules

- `private/`, `tdflite-ideas/`, `docs/TDFLITE.md` and the brainstorm PDF are git-ignored. Never copy their content into a tracked file, a commit message or `DECISIONS.md`. TDFLite results are public as counts only.
- Never modify `/Users/will/dev/tdflite` or `private/tdflite-src`. Never push, open issues or post on the owner's behalf except to this repository's `main`.
- Commits use the owner's GitHub no-reply address (set in this repository's local git config).

## Housekeeping left over

- **Disk:** the working directory is about 170 GB, mostly regenerable: `census/` run output, trimmed corpus copies under `corpora/*_trim/`, several Mathlib copies. Prune before starting heavy work.
- **Stale wording:** `private/tdflite-pilot/t3r/SPEC.md` sections 4 and 10 still carry the worksheet's earlier D4 wording.
- **Figures:** `docs/ARCHITECTURE.md` still uses the older chain figure; `brainstorm/diagrams/chain-v2b` is the better layout, with one arrow to verify against the pipeline first.
- **`docs/SCHEMA.md`** does not yet describe rule groups, suite verdicts or the evidence ladder.
- **Unmeasured:** Cedar with all five translator patches (about 80 minutes on a quiet, awake machine); clean build timings for the dead-code tool.
- **Setup details:** `docs/SETUP.md`. Four Lean toolchains, one Rust nightly, an opam root under `census/fork/.opam`, Kani and cargo-mutants are installed; each is logged in `DECISIONS.md` with its undo.
