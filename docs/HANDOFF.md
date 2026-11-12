# Handoff: state at the end of phase 1, and how to start phase 2

Written 2026-11-11 for a cold start with no memory of the earlier sessions, and updated the same day when the identity was settled and the phase 2 strategy adjusted. Read this first, then `README.md`, `docs/ARCHITECTURE.md` and `docs/PLAN.md` (the "Phase 2" section). `docs/HANDOFF_CLAUSAL.md` is the record of the identity work and the six adjustments; everything in it that was adopted is folded into this file and the plan.

Nothing is running. Everything public is committed and pushed to `github.com/willackerly/lean-rosette` (branch `main`; the repository keeps its old name until the rename).

## What this project is, in three sentences

The goal is plain-language rules about software, each proved against the code that runs, with an honest account of what each answer rests on. Rules are written in **Clausal**, a strict dialect of Gherkin; each sentence is built from **the Clausebook**, a library of reusable typed pieces, and the **Clausal compiler** turns it into both Rust tests and a Lean statement proved about a Lean model that Aeneas generates from Rust. A second, smaller strand studies how to make large formal proofs navigable.

The names are new (2026-11-11); the code is not renamed yet. Clausal sentences live in `clausal/features/`, the Clausebook is `clausal/clausebook.yaml` with `clausal/lean/Frames/`, and the compiler is `clausal/clausal` with `clausal/run.sh`. `README.md` describes the goal first and the present state last; the commands `clausal compose`, `cargo clausal test` and `clausal prove` do not exist under those names.

The owner's stance, which governs how results are used: the destination is fixed; report measured results and trades, never a go/no-go; fail closed; toy fixtures build infrastructure and prove nothing general; people decide judgement calls and language models are labelled proxies.

## Where phase 1 ended

| Area | State | Read |
|---|---|---|
| Pipeline (`clausal/`) | One command takes a rule written in the vocabulary and returns its reading in English, example rows on compiled Rust, a generated property test, a generated bounded check, a proof slot, and what each link rests on. Two toy crates. 25 frames, 96 vocabulary entries, **none signed** | `clausal/FINDINGS.md`, `clausal/DESIGN.md`, `clausal/out/report.md` |
| Phrasing gap | 0 of 48 rules by authors who had not learned the vocabulary compiled as written; 27 after rewriting; 18 need a new piece | `trials/sentences/RESULTS.md` |
| Echo-back | Model readers catch about 92% of wrong echoes. No person has taken the trial | `trials/meaning/` |
| Proof cost | About 6 lines of Lean per line of Rust for loops; two models each proved 7 of 7 loop functions unaided in under 15 minutes on textbook loops | `p2/RESULTS.md` |
| Evidence layers | Generated tests and bounded checks find everything hand-written ones found. No injected bug needed a proof to be caught; proof adds the all-inputs result. A false rule can pass every layer if the failing case is larger than every size tried | `clausal/compare/e1/E1_TRADES.md`, `clausal/compare/TRADES.md` |
| Translator | Unpatched Aeneas handles 1% of functions in ten real crates; five small patches give 35% (82% outside one crate). The patches are **not wired into the pipeline** and **not sent upstream** | `census/CENSUS.md`, `census/fork/FORK.md`, `census/PROFILE.md` |
| TDFLite | Lean model of the Go decision logic matches the Go on about 400,000 cases; the owner ruled on ten questions; guarantees 1–5 proved under the rulings, 8 given named facts; 75 test vectors; ten proposed Go changes, none applied | `private/tdflite-pilot/` (git-ignored): `OWNER_SUMMARY.md`, `t2/RULINGS.md`, `t2/AFTER-REVIEW.md`, `t3r/README.md` |
| Mathematics | Five ways of scoring proof structure failed against human judgement. A dead-code tool works on three projects. Generalising families of look-alike definitions paid in one family of seven | `out/FINDINGS.md`, `out/corpus/FINDINGS.md`, `out/deadcode/M8.md`, `out/families/FAMILIES.md` |
| Identity | **Decided 2026-11-11:** language first. Clausal (the language), the Clausebook (the public library), the Clausal compiler (`clausal`, `cargo clausal`). "Readback" is dropped: the canonical sentence lives in the `.feature` file, so there is no separate echo to drift. README rewritten and figures regenerated from `docs/diagrams/gen_diagrams.py`. Names were free on crates.io when checked; **nothing is registered**, and the repository and packages are not renamed | `README.md`, `docs/HANDOFF_CLAUSAL.md`, `DECISIONS.md` |

Every question tested, with its answer: `docs/RESULTS.md`. How each was tested: `docs/EXPERIMENTS.md` (31 entries).

## Decisions waiting for the owner

1. ~~Name, form and audience~~ **Decided** (see Identity above). What remains is the owner's to do: register the crate names and domains if wanted, and say when the mechanical rename of the repository may happen.
2. **Sign the Clausebook core:** the 53 shared frames and modifiers, after node C1 has split them from the fixture nouns. `cd slice && python3 -m clausal review <entry-id|all> --reviewer NAME`. Nothing has ever been signed, so the staleness and strict-mode machinery is untested.
3. **Take the meaning trial as a person** (`trials/meaning/README.md`), and recruit two or three others. It is being rebuilt around canonical sentences and separating inputs (node H2), so wait for the new item bank.
4. **Send the five Aeneas reports** (`census/fork/upstream/`, text only) and decide whether to carry the fork.
5. **TDFLite:** confirm the third D4 sub-choice and the guarantee-4 wording (`private/tdflite-pilot/t2/AFTER-REVIEW.md`); the eight decisions listed in `private/tdflite-pilot/t3r/README.md`.
6. **TDFLite files:** the owner cleared talking about the TDFLite work publicly (2026-11-11). `tdflite-ideas/` and `docs/TDFLITE.md` are still git-ignored; say whether to track them. The brainstorm PDF stays untracked.
7. **Whether the mathematics strand moves to its own repository.**

## Phase 2 in one paragraph

Three things, agreed with the owner on 2026-11-11: close the phrasing gap; put a person in the loop for sign-off and the meaning trial; and leave the toy crates for a real one that translates today. The nodes, their tests and their order are in `docs/PLAN.md` under "Phase 2".

The strategy was adjusted the same day, and the adjustments matter for anyone starting a node:

- **The phrasing gap is closed by a composer, not by a wider grammar.** `.feature` Clausal stays canonical and strict, one sentence per meaning. `clausal compose` accepts rough English and writes the canonical sentence, showing a separating input when readings differ. Do not add synonyms to the static parser.
- **Split the Clausebook before anyone signs it** (node C1): core frames and modifiers, a ledger pack, and the fixtures' local nouns.
- **The meaning trial tests canonical sentences and separating inputs,** not a second echo sentence.
- **The real crate and TDFLite's `tdf-core` run against the same unmodified core,** which is the test of reuse.
- **Route B** (a proved Lean model with the production binary tested against it) becomes a named evidence class.
- **The rename is one commit, later;** the mathematics corpus is recommended to move to its own repository (still the owner's decision 7).

## How to run work here

These are lessons from phase 1, not preferences.

- **Build, review, fix, as one unit.** Every substantial piece is built by one agent, checked by a second on a different model (Opus 5.5 reviewing Fable or the reverse), and the corrections are applied and rerun before anything is written up. Reviews found real defects every time, including a proof of `True` being counted as a proof and a proposed code change that turned a Deny into a Permit.
- **One owner per directory.** Anything that runs a pipeline does it in a scratch copy: `clausal/run.sh` deletes and recreates `clausal/out/`.
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

- **TDFLite may be named and its work discussed in public files** (owner, 2026-11-11; this replaces the earlier "counts only" rule).
- `private/`, `tdflite-ideas/`, `docs/TDFLITE.md` and the brainstorm PDF are still git-ignored. Moving any of those files into the tracked tree is a separate step the owner asks for (decision 6).
- Never modify `/Users/will/dev/tdflite` or `private/tdflite-src`. Never push, open issues or post on the owner's behalf except to this repository's `main`.
- Commits use the owner's GitHub no-reply address (set in this repository's local git config).

## Housekeeping left over

- **Disk:** the working directory is about 170 GB, mostly regenerable: `census/` run output, trimmed corpus copies under `corpora/*_trim/`, several Mathlib copies. Prune before starting heavy work.
- **Stale wording:** `private/tdflite-pilot/t3r/SPEC.md` sections 4 and 10 still carry the worksheet's earlier D4 wording.
- **Figures:** the chain, vocabulary, evidence, compiler and hero figures were regenerated on 2026-11-11 (`docs/diagrams/gen_diagrams.py`). `docs/diagrams/pipeline.vector180.svg` is the one older figure left and predates the Clausal names.
- **Rename:** `lean-rosette` to `clausal` and `slicegen` to `clausal`, in one commit, when no agent has a dirty working copy. The GitHub repository name and this directory are the owner's to change.
- **`docs/SCHEMA.md`** does not yet describe rule groups, suite verdicts, the evidence ladder or Route B.
- **Unmeasured:** Cedar with all five translator patches (about 80 minutes on a quiet, awake machine); clean build timings for the dead-code tool.
- **Setup details:** `docs/SETUP.md`. Four Lean toolchains, one Rust nightly, an opam root under `census/fork/.opam`, Kani and cargo-mutants are installed; each is logged in `DECISIONS.md` with its undo.
