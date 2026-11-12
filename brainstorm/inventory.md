# Inventory: what lean-rosette consists of and depends on

Written 2026-11-10 (late evening) as the factual basis for a scope statement. Brainstorming input for the owner, not a public document.

**How this was made, and its limits.**

- **Read, not rerun.** I read the repository (README, `docs/`, `DECISIONS.md`, `clausal/`, `census/`, `census/fork/`, `p2/`, `trials/`, `Rosette/`, `bench/`, `tools/`, `corpora/` scripts, `.github/`). I built and ran nothing. "EXISTS" therefore means "the repository's own reports and logs of 2026-11-10 say it ran, and the code is there", not "I reproduced it".
- **Not read:** `private/` and `tdflite-ideas/`. Everything about the TDFLite pilot below comes from the public counts in `docs/EXPERIMENTS.md` (entries 18, 23) and `docs/PLAN.md`. I could not check that those artefacts exist or work.
- **The slice was moving while I read it.** `git status` shows uncommitted edits to `clausal/lean/Frames/{Check,Frames,Lemmas}.lean`, `clausal/clausal/{vocab,vreport}.py` and `clausal/clausebook.yaml` (the frame-library review fixes). Counts for the frame library and vocabulary are the pre-review ones from `clausal/FINDINGS.md` and may move.
- **Status marks.** EXISTS: works today on the fixtures, with the path. PARTIAL: some of it works, the gap is named. NEEDED: not built.

## The five things a scope statement should not get wrong

These are the places where the current public wording is ahead of, or different from, what is in the tree.

1. **No modified third-party tool is in the end-to-end chain today.** `clausal/translate.sh` runs the unmodified Aeneas release binary (`nightly-2026.11.09-5a392f4`). The five Aeneas patches live in `census/fork/` and were measured only on the census. `census/fork/FORK.md` says in so many words that pointing the slice at the patched binary was "not done and not tested". So the honest sentence is: *the chain works end to end on code written to fit the unmodified tools; widening it to real crates needed five patches, which are measured but not yet wired in.* The owner's phrase "existing tools that had to be modified to make the chain work end to end" overstates this by one step.
2. **"Five patches give 35%" is really "two patches give 35%".** Per `census/fork/FORK.md`: patch (ii) gives +1,368 functions, patch (iv) +117, and (i), (iii) and (v) give +0 on the ten crates as shipped (they matter for Cedar, which still stops in Charon). README says five patches, `docs/RESULTS.md` says four. Both are defensible; the scope statement should say which patches did the work.
3. **The frame library is project-independent by construction and by nothing else.** `clausal/lean/Frames/` imports only Lean core, which is good. But it has exactly one consumer (the slice, two toy crates). Its second-domain evidence is "83 of 85 TDFLite readings are expressible, judged by reading" (`docs/EXPERIMENTS.md` 24), not compiled. P2's crate does not use it. And the English half of each frame (surface form, echo template) is not in the library: it sits in the slice's `clausebook.yaml` and `clausal/vocab.py`. A library that ships definitions without the sentences that reach them is half a library.
4. **There is no shared proof-lemma library.** README says "shared proof lemmas for common loop shapes". What exists is three per-crate lemma sets written independently for three crates (`clausal/lean/Ledger/Lemmas/`, `p2/arm-fable/lean/Lemmas/`, `p2/arm-opus/lean/Lemmas/`). Nothing is factored out. That is raw material for a library, and a good one (two arms proving the same seven loops is a natural experiment in what recurs), but the library is NEEDED, not EXISTS.
5. **A new sentence does not get a verdict.** It gets a reading, an echo and a model search. A verdict needs a hand-written proof and a hand-written cucumber step through the old whole-phrase glossary, which still exists beside the new vocabulary (`clausal/glossary.yaml`, 44 entries, and `clausal/clausebook.yaml`, 87). README is honest about this; the scope statement must be too, because "compiled from reusable pieces" currently describes the statement and not the evidence.

---

## 1. Tooling we built

Sizes are `wc -l` on 2026-11-10 unless a source is given.

### 1a. The software chain (`clausal/`)

| Tool | What it does | Status | Where |
|---|---|---|---|
| Pipeline runner | One command: translate, generate, build, search, link, audit, run on Rust, adequacy, report. Flags `--strict`, `--no-rust`, `--no-adequacy`, `--no-heldout` | EXISTS | `clausal/run.sh` (175 lines) |
| Translation driver | Fetches the pinned Aeneas release (sha256-checked), runs Charon then Aeneas per crate, merges `translation.json`, writes `provenance.json` (input and output hashes, tool versions) | EXISTS. macOS arm64 pins only; no override for a patched binary | `clausal/translate.sh` (132 lines) |
| Sentence compiler | Parses a rule or scenario against the vocabulary, types the pieces, finds the one composition or refuses (UNBOUND, ILL-TYPED, AMBIGUOUS), emits the Lean term and the English echo | EXISTS for the fixtures; controlled grammar (one operation or a `followed by` sequence per clause, `for which` takes one condition). AMBIGUOUS refuses but does not yet show a separating input | `clausal/clausal/vocab.py` (1,191 lines) |
| New-sentence compiler | Compiles sentences from the vocabulary alone, searches them on the model, reports them (informational) | EXISTS; no verdict, no Rust run | `clausal/clausal/newrules.py`, `clausal/heldout/` |
| Flat statement generator | Gherkin parser (including `Rule:`), old whole-phrase binding, Lean statement and check emission, proof stubs | EXISTS. This is the legacy path every proof still targets | `clausal/clausal/core.py`, `emit.py`, `pipeline.py` (1,699 lines) |
| Link generator | Emits `<id>.reading_iff` (compiled reading equals flat statement) and `<rule>.from_scenarios` (rule derived from its scenarios) for the kernel | EXISTS. The rule glue is one fixed script: it fails where a scenario names a computed number (2 of 10 proved rules are hand-proved instead) | `clausal/clausal/links.py`, `clausal/lean/Run/Links.lean` (generated) |
| Counterexample search on the model | Evaluates example rows on the Lean model; boundary-grid search for a satisfying input and a falsifying input | PARTIAL. Grid only, no random sampling or shrinking; found 188 of 212 falsifiable (mutant, rule) pairs in K2 and crashes on non-terminating models | `clausal/lean/Run/Search.lean` (generated), `clausal/rsearch.py`, `Run/ReadingSearch.lean` |
| Audit | Reads the Lean environment: exact statement type per scenario module, axioms, generated sat/unsat/refutation theorems, coverage theorems, link types | EXISTS | `clausal/lean/Bdd/Audit.lean` (133 lines), `Bdd/AuditLinks.lean` (47), `Run/Audit.lean` (generated) |
| Suite adequacy | Generates trivial implementations of each operation's exact type (reject-all, no-op, identity, constant), restates proved scenarios against them, searches, attempts kernel confirmation | EXISTS, informational | `clausal/clausal/adequacy.py` (499 lines), `Run/Adequacy.lean`, `Run/AdequacyAudit.lean` |
| Rust runner | cucumber-rs runs the same feature files on compiled Rust, replays counterexamples, evaluates the Rust reading of each old phrase on a grid | EXISTS for old phrases only: one hand-written step per glossary id. Not compositional | `clausal/wallet-bdd/` (`src/lib.rs` 281, `tests/bdd.rs` 413, `tests/readings.rs` 35) |
| Report emitter | Per-rule and per-scenario blocks, echo, "rests on", vocabulary and trusted-base tables | EXISTS | `clausal/clausal/report.py` (1,714), `vreport.py` (520), `rules.py` (301) |
| Evidence graph emitter and lint | Writes `out/graph.json`; validates against JSON Schema v2; computes staleness; `--what-if <node>` | EXISTS. Whether the schema document covers rule groups and layered evidence is plan node X1, which I did not see closed | `clausal/clausal/report.py`, `graphlint.py` (205), `clausal/schema/refinement-graph.v2.schema.json` |
| Sign-off command | Records a reviewer against a piece's digest; void when the entry or its Lean text changes | EXISTS as a mechanism; **zero signatures** | `python3 -m clausal review`, `clausal/vreport.py` |
| Mutation harness | Applies 45 hand-written Rust mutants and 27 negative controls in scratch copies; separates "shown false" from "proof lost" | EXISTS | `clausal/mutation/run_mutants.py` (655), `workcopy.sh` |
| Effort log | Every `lakebuild.sh` call logged (time, target, ok or failed); Lean-per-Rust line counter | EXISTS | `clausal/lakebuild.sh`, `clausal/effort/` |
| Property-test and bounded-check harness **generator** | From one compiled rule, emit a proptest and a Kani harness | NEEDED (plan node E1). Today the 23 properties and 23 Kani harnesses are hand-written | hand-written versions: `clausal/compare/arms/` |
| Falsifying-input intake | Accept an input from proptest or Kani as an example row and a kernel refutation | PARTIAL: `clausal/compare/harness/confirm.py` does the replay for the K2 experiment; not part of `run.sh` | `clausal/compare/harness/confirm.py` |

### 1b. Experiment harnesses (software side)

| Tool | What it does | Status | Where |
|---|---|---|---|
| K2 trade-map harness | Freezes inputs by digest, runs four evidence arms on every mutant, retries Kani, replays inputs, analyses, costs, builds the report | EXISTS; a full rerun is 2 to 3 hours | `clausal/compare/harness/` (1,439 lines Python), `rerun.sh`, `PREREG.md` |
| Original-versus-mutant oracle | Runs original and mutant on 2.4 million inputs to tell equivalent mutants from unconstrained behaviour | EXISTS (builds only inside a scratch copy) | `clausal/compare/arms/diff` |
| Translation census | Corpus selection by rule and seed, syn-based function inventory, Charon/Aeneas/`lake build` per crate, per-function join, cause classification, generated reports | EXISTS; about 20 minutes idle, Cedar needs about 20 GB of memory | `census/scripts/` (with fork scripts: 3,272 lines Python), `census/tools/fninv/`, `census/rerun.sh` |
| Rewrite-cost runner | Applies a source patch to a pinned crate, runs its tests and the census before and after | EXISTS (9 rewrites) | `census/rewrites/run.py` |
| Fork build and measurement | Builds Aeneas from source per patch level, reruns the census unpeeled, runs Aeneas's own tests, runs single-file reproductions | EXISTS; needs opam and OCaml 5.3 | `census/fork/scripts/`, `census/fork/repro/run.sh`, `env.sh` |
| Soundness sampler | Runs sampled functions in Rust and in the generated Lean on generated inputs and compares | EXISTS as a one-off: 25 functions, 895 inputs. Thin by its own account | `census/fork/scripts/sound_sample.py`, `sound_run.py` |
| P2 scoring kit | Cold-copy rebuild, an audit sharing no code with the slice's, kernel replay with `leanchecker`, attempt and line counters, mutant run | EXISTS | `p2/score/` |
| Meaning trial | Terminal runner, single-file offline web page, reader-kit builder that excludes the key, scorer with intervals, self-tests | EXISTS; taken by 8 model readers, no people | `trials/meaning/` (1,184 lines Python) |
| TDFLite differential check and vector emitter | Model-versus-Go comparison as one command; 75 test vectors in the owner's format | Reported EXISTS in `docs/EXPERIMENTS.md` 23. **Private; not inspected by me** | `private/` (not read) |

### 1c. Mathematics tooling

| Tool | What it does | Status | Where |
|---|---|---|---|
| Candidate enumeration and kernel-checked lifting | Lists proof-valued subterms; turns chosen ones into real lemmas, kernel re-checked | EXISTS; no failures on 1,274 theorems | `Rosette/Candidates.lean`, `Lift.lean` |
| Corpus exporters | Declaration graphs, statements, proof sizes across four Lean versions | EXISTS | `corpora/tools/ExportDecls.lean`, `corpora/ns_export/` |
| Outline builders and validators | Dominator and definition-centred outlines; scoring against blueprints and papers | EXISTS; the method mostly failed as a predictor (five negative results) | `bench/outline*.py`, `validate_outline*.py`, `paper_truth.py` |
| Dead-code tool | What a built Lean project does not need for its roots, confirmed by deleting in a copy and rebuilding; negative control | EXISTS on three projects (plan node M8) | `tools/deadcode/` |
| Re-invented-abstraction finder | Project definitions equivalent to a library notion, each with a kernel-checked equivalence | PARTIAL: exploratory by its own label (rules changed after the first run; summary report on disk is pre-review) | `tools/reinvent/` |
| Reuse and friction measurement | Statement recurrence; where proof bulk sits by kind of side condition | EXISTS; results mostly negative | `bench/reuse.py`, `corpus_reuse.py`, `friction_*.py`, `corpora/friction/` |

**Opinion.** The maths tooling is about 14,000 lines of Lean and Python (`Rosette/` 2,835, `bench/` about 11,000) and shares one thing with the software chain: the graph schema, and even that only as a fit test (`clausal/schema/maths_fit.py`). A scope statement for "formally modelled software by default" should list the dead-code tool as the one maths-side tool with a plausible software use (plan node M6, untested) and say the rest is a separate strand.

---

## 2. Libraries

"Project-independent" is judged by what the code imports and who uses it today.

| Library | Contents today | Status | Project-independent? | Who would maintain it | How it would be versioned |
|---|---|---|---|---|---|
| **Frame library** | Abstract operation `Op` with fail-closed `HoldsAt`; typed holes (`Measure`, `Cond`, `Coll`, `Variation`, ...); 23 definitions for the 14 catalogue frames; 7 glue lemmas | EXISTS; under review, uncommitted fixes in the tree. The review tried a fail-closed `IfThen` in a scratch copy only, which suggests the committed one is not | **Yes by imports** (Lean core only, its own Lake library `Frames`). One consumer. | A small named group, as Mathlib has maintainers; changes need more than one signer (open question in `docs/ARCHITECTURE.md` 15) | Its own package and repository with semantic versions, where a major version is "a frame's meaning changed" and a minor version is "meaning-preserving, with a kernel-checked equivalence to the previous definition". That equivalence is plan node V9 and is not built |
| Frames' executable second readings | One decidable checker per frame, compared with the definition on generated inputs each run (23,700 of 23,700 agree on the fixtures) | EXISTS for 19 frames through sentences; the other 4 (count with a number, monotone, agrees-with, independent-of) on ten hand-written instances | Yes, same library | Same group; ideally a different author from the definition | With the frame library, same version |
| Frames' English (surface forms, echo templates, defaults text) | 19 surface forms, slot-structured echo | PARTIAL: lives in the slice's `clausebook.yaml` and `clausal/vocab.py`, not with the library | **No, though it should be.** This is the half a reader signs | Same group | Must ship in the same versioned unit as the Lean definition, or a signature covers only half of what was read |
| **Modifiers** | 27 (`the total of`, `every ... of`, `successful`, `rejected`, `for which`, `followed by`, bystander, ...) | EXISTS in `clausal/lean/Frames/Core.lean` and `clausebook.yaml` | Mostly; I did not audit each of the 27 for hidden ledger assumptions | With the frame library | With the frame library |
| Idioms | 10 surface forms that stand for a composition (`has a balance of`) | EXISTS | **No.** Every fixture scenario uses one; each is an extra English claim to sign | Project | With the project vocabulary |
| **Domain vocabulary: wallet, ledger** | 31 domain words, 8 of them operations bound to Aeneas model functions | EXISTS | No, by design | The system's owner | In the system's repository, digest per piece, signature void on change (mechanism exists) |
| Domain vocabulary: inventory (P2) | Old whole-phrase glossary for a 161-line crate | EXISTS in the old format only; not ported to frames | No | Project | Not versioned (P2 froze by content hash, no commit) |
| Domain vocabulary: TDFLite | 85 formal readings of 8 guarantees; rulings as parameters | Reported EXISTS, private, hand-written Lean, **not expressed through the frame library** (83 of 85 judged expressible) | No | The owner | Private |
| Old whole-phrase glossary | 44 entries; the flat statements every proof is about and the key of every cucumber step | EXISTS, legacy. It is off the English-to-verdict path but still load-bearing | No | Should be retired once the Rust side is compositional | n/a |
| **Bridge and audit support** | Statement form `∃ outputs, call = ok ... ∧ Thens`, bridge lemmas so `step*` still works, executable `Check` type, model-function-to-`Op` adapters | EXISTS: `clausal/lean/Bdd/` (388 lines) | Yes in intent; depends on the Aeneas library. Copied, not shared, into `p2/` | Tooling maintainers | With the pipeline, pinned to an Aeneas release |
| **Proof lemma library for loop shapes** | Nothing shared | **NEEDED.** Raw material: ledger lemmas (328 lines in 6 modules, 227 code lines), P2 Fable lemmas (806 lines), P2 Opus lemmas (846 lines). Confident it is needed because loop lemmas are over half of all hand-written Lean and the 6-lines-per-Rust-line cost did not fall between experiments | Would be, if built on Aeneas's `loop.spec_decr_nat` | Whoever maintains the Rust profile; candidates for upstreaming to Aeneas | Pinned to the Aeneas library version it is proved against |
| Per-crate loop lemmas | Invariants, a pure `runN` model, `@[step]` specs per Rust function | EXISTS for ledger and (twice) inventory. Unsigned, and two rule statements rest on them | No | The crate's proof author (person or agent) | With the crate; they appear in no statement, which is the recorded open problem |
| **Lean models of Rust standard-library items** | Aeneas's own: 347 functions, 88 trait impls, 44 types, 49 traits (`census/data/std_models.json`) | Used as is. **Our additions: one six-line `step` lemma for `Vec<u64>::clone`** (`clausal/lean/Ledger/Lemmas/All.lean`). Plan node A3 (models for the most-used unmodelled items) not started | Yes | Upstream Aeneas; a fork cannot add a model without a rebuild (the list is generated at build time). `aeneas -split-files` is an untried route that needs neither | Coupled to the Aeneas binary, which pins Lean and Mathlib |
| **Supported-Rust profile** | 16 rules (0 to 15), each with evidence and a before/after probe; the modelled-library table | EXISTS as a document generated from data: `census/PROFILE.md`, `census/probes/profile-probes-0.1.0/` | Yes | Whoever carries the translator pin; must be regenerated at every pin change | Version = the Aeneas and Charon pin it was measured against. It is not yet a lint: nothing checks a crate against it before translation |
| **Mutant and control sets** | 45 hand-written Rust mutants, 27 negative controls; 52 cargo-mutants mutants; 107 for inventory | EXISTS: `clausal/mutation/`, `clausal/compare/mutants/`, `p2/score/` | No (fixture-bound) | Pipeline maintainers | With the fixtures |
| **Item bank for the meaning trial** | 54 items (30 rule-and-echo, 24 glossary), 18 unfaithful, hand-written echoes; bank format supports further domains | EXISTS: `trials/meaning/items.json`; key git-ignored. Echoes are hand-written, not the tool's (that is V5) | The format is; the bank is wallet and ledger | Trial organiser, separate from the item author | Bank id plus content hash (`wallet-ledger-k1`, sha256 prefix in `SUMMARY.md`) |
| Frame catalogue and prior-art survey | 14-frame catalogue with sources (FRET, property patterns) | EXISTS: `out/prior_art_vocabulary.md` | Yes | Frame maintainers | Document |
| Test-vector corpus (TDFLite) | 75 vectors | Reported EXISTS, private | No | Owner | Private |

**Opinion on the Mathlib kinship.** It holds for the frame library and, if it gets built, the loop-lemma library: both are small formal objects many projects would import and none would want to re-derive. It does not hold for domain vocabularies, which are per-system and closer to a project's test fixtures than to a shared library. The scope statement should name two shared libraries (frames with their English; loop and collection lemmas over the translator's output) and one per-project artefact (the domain vocabulary), and not blur them. One difference from Mathlib matters: a Mathlib lemma is checked by the kernel and needs no signature, while a frame's meaning is human-asserted. Versioning a signed library is a harder social problem than versioning a proved one, and nothing here has tried it.

---

## 3. Checkers

Every check that guards a verdict. "Automatic" means it runs inside `clausal/run.sh` with no person involved.

| Check | Failure it prevents | Automatic? | Status | Where |
|---|---|---|---|---|
| Exact statement type, from the scenario's own module | A theorem of type `True` counted as a proof (this happened) | Yes | EXISTS | `clausal/lean/Bdd/Audit.lean`; independent second implementation in `p2/score/audit.py` |
| Axioms: only `propext`, `Classical.choice`, `Quot.sound`; `sorryAx` counts as absent | A proof resting on something unchecked | Yes | EXISTS | `Bdd/Audit.lean`, `Run/Audit.lean` |
| Kernel replay of every constant | Trusting the elaborator's acceptance | No (P2 scoring only) | PARTIAL: `leanchecker` used in `p2/score/`, not in `run.sh` | `p2/score/` |
| Non-vacuity: kernel-checked witness that the Givens can hold | A claim true because its conditions never hold | Yes | EXISTS; a review found the witnesses can be degenerate (empty ledger) | `Run/Audit.lean` (`.sat`, `.unsat`) |
| Trivial-Then check | A Then that says nothing | Yes | EXISTS (`features/negative.feature` control) | `Run/Audit.lean` |
| Input coverage: no input of an operation falls outside its proved scenarios | Bugs on paths no scenario mentions (three survived the first review) | Yes | EXISTS (`Coverage.g*`) | `Run/Audit.lean` |
| Suite adequacy against trivial implementations | A safety rule that "rejects everything" also satisfies | Yes, informational, never fails the run | EXISTS: 53 trivial implementations, 7 of 8 operations fully constrained | `clausal/adequacy.py` |
| Second reading of each frame (definition against executable checker) | A subtly weakened frame definition | Yes | EXISTS. Catches a definition wrong in one place, not one wrong the same way in both; the reviewer's 12 frame mutants are the test of its power and I did not find the tally written up | `Run/ReadingSearch.lean`, `Run/FrameTests.lean` |
| Second reading of each domain phrase (Lean against Rust predicate) | A weakened domain definition | Yes | PARTIAL: exists for the 44 **old** phrases on a grid; the new pieces have no Rust reading | `wallet-bdd/tests/readings.rs`, `Run/Search.lean` |
| Reading-to-statement link (`reading ↔ stmt`, type checked) | A recompiled sentence quietly weakened; verdict UNLINKED otherwise | Yes | EXISTS, 34 of 34 | `Run/Links.lean`, `Bdd/AuditLinks.lean` |
| Rule from scenarios (`from_scenarios`) | A rule line claimed proved when only its scenarios are | Yes | EXISTS for 8 rules; 2 by hand proof | `Run/Links.lean`, `lean/Wallet/RuleProofs/` |
| Kernel-checked refutation at the found input | "False" reported on the strength of a search bug | Yes | EXISTS; through a loop only via a hand-proved exact-result lemma | `Run/Audit.lean` |
| Counterexample replay on compiled Rust | A refutation that is an artefact of the model | Yes | EXISTS for old-phrase scenarios | `wallet-bdd/` |
| Example rows on model and on Rust, compared | Model and code disagreeing on the stated examples | Yes | EXISTS: 81 cucumber scenarios, 365 steps | `wallet-bdd/`, `Run/Search.lean` |
| **Differential model-versus-code on generated inputs (Rust)** | A translator or library-model error away from the examples | No | **PARTIAL to NEEDED.** One one-off sample (25 functions, 895 inputs, 0 mismatches) on census crates; nothing for the slice's own crates beyond rows and the phrase grid. Aeneas's std models are "not yet separately tested" (`docs/ARCHITECTURE.md` 8) | `census/fork/scripts/sound_run.py` |
| Differential model-versus-code (Go) | A hand-written model that drifts from production | One command, by report | Reported EXISTS (about 400,000 cases, 24 of 24 model mutants detected, fails on a negative control). Private, not inspected | `private/` |
| Mutation run | A rule set that leaves real behaviour unconstrained | No: separate command, 73 minutes under load | EXISTS | `clausal/mutation/run_mutants.py` |
| "Shown false" counted apart from "proof lost" | An agent re-proving around a bug to a green run | Yes in the mutation and K2 reports | EXISTS | `mutation/results.md`, `compare/harness/analyse.py` |
| Negative controls that must fail | A check that cannot fail | No: in the mutation harness, not in `run.sh` | EXISTS: 27 of 27 as expected | `mutation/run_mutants.py` |
| Graph schema and lint self-test | A malformed or unlintable evidence graph | Separate command | EXISTS: must reject ten deliberately invalid graphs | `clausal/schema/selftest.py` |
| Staleness | A signature or proof outliving a changed definition | Computed on demand | EXISTS in `graphlint.py`; **unexercised in anger** because nothing is signed | `clausal/graphlint.py` |
| Unsigned-vocabulary flag and `--strict` | A "proved" resting on a reading nobody reviewed | Yes | EXISTS; every verdict today carries UNREVIEWED | `run.sh --strict` |
| Provenance digests | A model silently regenerated from different source or tools | Yes, recorded; not compared against a previous run | PARTIAL | `clausal/lean/provenance.json` |
| Frozen-inputs check | Experiment inputs changed after the data was seen | Yes within K2 and P2 | EXISTS: `compare/harness/freeze.py`, `p2/base/FROZEN.sha256` | as named |
| Agents did not edit rules, vocabulary or axioms | A proof obtained by weakening the claim | P2 only (frozen-file diff) | PARTIAL: enforced by hash in P2; in the slice it is a written rule with no mechanical guard | `p2/score/` |
| Clean-room re-check from a released bundle | Results that hold only on the builder's machine | n/a | NEEDED (plan node X3) | none |
| CI running the pipeline and the controls | Regressions between sessions | n/a | NEEDED (plan node X2). The three workflows in `.github/workflows/` are the stock Lean project template for the repo root; none runs `clausal/` | none |

**Opinion.** The checks that guard the *proof* link are the strongest part of the project and are real. The checks on the *translation* link are the weakest: rows, a grid, and one thin sample. Given that the project's own trusted-base table lists Aeneas, Charon and hand-written std models as tool-trusted, a generated differential test of model against compiled Rust (which E1's generators would make nearly free) is the most valuable missing checker, ahead of anything on the meaning link.

---

## 4. Documented methodology

| Practice | Written down? | Where | Comment |
|---|---|---|---|
| Rules for every experiment (frozen before data; items not chosen by the builder; pass and fail bands with a gap; people decide judgement calls; a lost proof is not a detection; adequacy note per suite; agents may not edit rules to pass) | Yes | `docs/PLAN.md` "Rules for every node" | Rule 1 (freeze at a commit) was not met in K2 or P2, which froze by digest because agents share one working tree. Both say so |
| Build, review on a different model, fix, rerun | Yes | `docs/PLAN.md` "How the work is run"; `docs/SETUP.md` "Working with agents" | Followed, and visibly productive (each checker traces to a review finding) |
| Stance (destination fixed; report, don't gate; do not overfit to the wallet; rules come in suites; restricted profile acceptable; people tests deferred) | Yes | `docs/PLAN.md` "Stance" | |
| Decision log with reason and undo | Yes | `DECISIONS.md` (1,122 lines, 226 KB) | Complete to a fault. Unreadable as a whole; needs an index or per-track split before anyone but the owner uses it |
| Readings and rulings for ambiguous guarantees (write every formal reading, separate them with an input, ask the owner, record the ruling as a parameter) | Yes, as a pattern | `docs/ARCHITECTURE.md` 12; `docs/VOCABULARY.md` "Handling ambiguity"; result in `docs/EXPERIMENTS.md` 18 and 23 | The worked example is private. A public worked example on a non-sensitive target is NEEDED before this counts as documented methodology others can follow |
| Pattern for code that is not Rust (hand model with line trace, differential check, readings, rulings as parameters, vectors) | Yes, four steps | `docs/ARCHITECTURE.md` 12 | "Differentially tested against a Lean model" is not yet a named evidence level with pass bars (open programme question in the plan) |
| Fail-closed defaults and the granularity rule for vocabulary | Yes | `docs/VOCABULARY.md`, `docs/ARCHITECTURE.md` 4, `clausal/DESIGN.md` 14 | |
| How to add a sentence | Yes | `clausal/README.md` "Adding a sentence" | Documents the gap as well as the path |
| How to write Rust that translates | Yes | `census/PROFILE.md` | |
| How to carry and drop a translator patch | Yes | `census/fork/FORK.md` "Carrying the fork" | Good: includes a "drop when the unpatched release gives ..." test per patch |
| Evidence-graph schema | Yes | `docs/SCHEMA.md` (457 lines) | Update for rule groups and layered evidence is plan node X1 |
| Running a reader trial and keeping the key away | Yes | `trials/meaning/README.md` | |
| Setup, pins, undo steps | Yes | `docs/SETUP.md`, `clausal/TOOLCHAIN.md` | One platform only |
| Machine-load and timing rules (two heavy workflows at most; timings in a quiet window) | Yes | `docs/PLAN.md` | Written after being violated; most timings in the repo are still under-load figures and say so |
| **Sign-off roles** (who may sign a domain word, the Lean behind it, a shared frame) | **No** | Listed as open in `docs/ARCHITECTURE.md` 15 and the plan | NEEDED. The mechanism exists and has never been used |
| **Red-build policy** (blocking or advisory, who owns a lost proof) | **No** | Open programme question; "must be fixed before S2" | NEEDED |
| **How a loop is fully specified** (signed reference model or two-run rules) | **No** | Open in both documents | NEEDED. Until decided, exact loop behaviour sits in unsigned lemmas |
| **Disclosure policy** for evidence about unresolved defects | Partly: "TDFLite material stays out of the public repo" | `docs/PLAN.md` Track T | No general policy |
| **Proof-writing guide for agents** (the `step*` recipe, `loop.spec_decr_nat`, what an invariant looks like) | Scattered | `clausal/README.md`, `clausal/DESIGN.md` 12, `p2/base/TASK.md` | NEEDED as one document; it is the most reusable piece of know-how here |
| **Agent constitution** | Yes, and **stale** | `AGENTS.md` | It names a KiminaBridge, a PantographWorker, `src/linter/cognitive_gate.py` and arena worktrees, none of which exist in the repository. At least four agent logs in `DECISIONS.md` record working around it. It should be rewritten to the rules actually in force, or it trains agents to treat the constitution as optional |

---

## 5. Third-party tools

| Tool | Version | How we use it | Detail |
|---|---|---|---|
| **Charon** | 0.1.315 (`454586e9`), shipped in the Aeneas tarball | **As is**, with `--preset=aeneas`; **worked around** for Cedar | Needs one exact Rust nightly with `rustc-dev` and `miri`. On Cedar it dies on a rustc internal compiler error introduced days earlier; the workaround is marking 49 functions and two generated parsers opaque (`census/data/overrides.json`). Not patched. No upstream report prepared for the ICE that I could find |
| **Aeneas** | `nightly-2026.11.09-5a392f4` in the slice; `0d21a9ec` (11.10) for the fork | **As is in the slice. PATCHED in `census/fork/` only.** Configured with `-emit-json` and `-warnings-as-errors` | The warnings-as-errors flag made `for i in 0..n` look untranslatable (corrected in experiment 20); dropping it is part of plan node A3. An existing flag, `-filter-trait-methods`, removes a class of Lean errors and is not used. `-split-files` (hand-completed external declarations) is untried |
| Aeneas patch 0001 | 43-line patch file | Keeps analysing declaration groups after a mixed group, instead of failing every later function | +0 functions as shipped; matters for Cedar. Upstream: **prepared, not sent** (`census/fork/upstream/01-...`), reproduction `repro/mixed_group.rs` |
| Aeneas patch 0002 | 174 | A trait-method signature that fails drops that method with a warning, not the whole crate | **+1,368 functions.** Prepared, not sent (`upstream/02-...`); two reproductions |
| Aeneas patch 0003 | 347 | Catches non-`CFailure` OCaml exceptions per function and per group | +0 as shipped; makes failures per-function. Prepared, not sent (`upstream/03-...`); one 30-line reproduction |
| Aeneas patch 0004 | 203 | Lean backend: a user type named `Slice`, and a parameter named like a module, no longer capture library names | **+117 functions.** Prepared, not sent (`upstream/04-...`); the one patch with a design choice upstream may want done differently |
| Aeneas patch 0005 | 58 | Resets the pretty-printer after an extraction error so later definitions still parse | +0 on the ten crates; effect on Cedar unmeasured (run killed). Prepared, not sent (`upstream/05-...`); no single-file reproduction |
| All five | 334 lines added, 53 removed, 9 source files | Apply with `git am` to both pinned commits; Aeneas's 122 extraction tests unchanged | Not run through `ocamlformat` (upstream CI requires it). Not checked against the upstream tracker for duplicates. The suite runs with `-abort-on-error`, so it does not exercise the new paths |
| **Aeneas Lean library and std models** | Shipped in the tarball, prebuilt | **As is**, required by path; **one gap filled locally** | Missing `step` lemma for `Vec<u64>::clone` written by hand. Its `Result` is not evaluable by `decide`, so refutations are proved, not computed. A Rust enum named `Error` clashes with `Std.Error`. Models are trusted and untested by us |
| **hax** | 0.5.0 | **Evaluated, found to add nothing here** | Its Lean backend sits on Charon and Aeneas and aborts on the same crates with the same errors. Whether its Lean compiles was not measured. The contracts-as-attributes route (plan node T6a) is untried |
| **Lean and Lake** | 4.35.0 (slice), 4.36.0-rc2 (root, PFR), 4.36.0-rc1 (Carleson), 4.34.0-rc2 (Navier-Stokes) | **As is; worked around** | Four toolchains because each dependency pins its own. Audits run as `lake env lean` scripts because a native `lake exe` would need Mathlib compiled to object code. `leanchecker` used for kernel replay in P2 |
| **Mathlib** | `v4.35.0` (transitive through Aeneas) in the slice; `v4.36.0-rc2` at the root | **As is**, prebuilt cache only | The frame library deliberately does not import it. About 7 GB per copy |
| **cucumber-rs** | 0.23.0, with tokio 1 | **As is** | Confirmed by running that it executes a Scenario Outline with Examples under `Rule:` (`clausal/review/rule-probe/`). Gives the rule line no meaning; that reading is ours |
| **proptest** | 1.12.0 | **As is**, hand-written properties, two generator profiles | Edge-weighted generators found all 212 falsifiable pairs; plain ones 188 |
| **Kani** (with CBMC 6.11.0) | 0.68.0 | **As is**, hand-written harnesses, small bounds | Brings its own Rust nightly (2026-08-21). Only finder of the two single-magic-value bugs. Ledger rules verified only up to 2 to 4 accounts and 1 to 3 transfers |
| **cargo-mutants** | 27.1.0 | **As is** | 52 mutants for wallet and ledger, 107 for inventory |
| Rust toolchains | nightly-2026-09-17 (Charon), nightly-2026-08-21 (Kani), stable 1.94 (tests) | As is | Three compilers for one small crate; the Charon one must match exactly |
| OCaml, opam, dune | OCaml 5.3.0, opam 2.6.1 | As is, for the fork build only | Needed on every machine and in CI if the fork is carried; a release tarball needs none of it |
| `syn` | via `census/tools/fninv` | As is | Function inventory (the census denominator) |
| Python 3 and PyYAML | system | As is | PyYAML is the only third-party Python package `clausal` imports; the graph lint is hand-written, with no `jsonschema` dependency. No requirements file records this |
| lean-action, docgen-action, lean-release-tag, mathlib-update-action | GitHub Actions | Stock template for the repo root | Do not exercise the software chain |
| Vector180 | owner's own format | As is | Figures in `docs/diagrams/` |
| Headless Chrome | system, optional | As is | Self-test of `trial.html` |
| **Borrowed designs, not code** | | | NASA FRET (slot-structured echo, second executable reading); Dwyer-style property patterns (frame catalogue); Cedar's differential-testing recipe; Gherkin `Rule:` |
| Go toolchain and TDFLite's engines | not inspected | Presumably as is | Private |

**The honest modification inventory, in one paragraph.** One third-party tool is patched: Aeneas, five commits, about 300 lines, all prepared for upstream and none sent, sending being the owner's step. Two are worked around without a patch: Charon (opaque markers for Cedar) and Lean's toolchain coupling (four pins, script-mode audits). One library has a gap we filled locally: the Aeneas Lean library (one lemma). Everything else is used as shipped. hax was tried and set aside.

---

## 6. Not done yet, confident we will need

Ordered by how certain the need is. "Certain" items are ones where the repository already contains a finding that the absence causes a failure.

| # | Need | Why we are confident | Plan node | Certainty |
|---|---|---|---|---|
| 1 | **Rust-side composition**: a Rust reading per piece, so a new sentence runs on compiled code with no hand-written step | Named in `clausal/DESIGN.md` 14.9 as "the largest gap between this and the README target". Without it the reusable-pieces claim covers statements only | Implied by E1; no node of its own | Certain |
| 2 | **Generated property tests and bounded checks from a compiled rule**, with falsifying inputs fed back as rows and refutations | K2: edge-weighted property tests found 212 of 212 falsifiable pairs, the pipeline's own search 188; Kani alone found two bugs. Hand-writing 23 of each does not scale | E1 | Certain |
| 3 | **Signing workflow with roles** | 87 vocabulary entries and 44 glossary entries, zero signatures. Every verdict in the repository is formally "review". The meaning link is the project's thesis and has no human evidence at all | G1, "who may sign what" (no node) | Certain |
| 4 | **Translator robustness in the chain**: wire the patched Aeneas into `translate.sh`, or get the patches upstream | 1% of real functions translate as shipped; five of ten crates produce nothing | A2 (decision), A3 | Certain |
| 5 | **Onboarding a second real codebase in Rust** | Wallet and ledger are 45 and 85 lines written to fit. The only real target so far is Go, by hand. No frame, proof or step has met idiomatic Rust | S1 | Certain |
| 6 | **Generated differential test of model against compiled Rust** | The translation link is "tool-trusted" with one thin sample behind it; std models are untested; the one real defect found on TDFLite was outside the model | none (closest: T4 for Go, E1) | Certain |
| 7 | **A shared loop and collection lemma library, and a decision on how a loop is specified** | 6 Lean lines per Rust line, unchanged across two experiments and two models; lemmas are over half the hand-written Lean; two rule statements rest on unsigned lemmas | P-track follow-on; open programme question | Certain |
| 8 | **People as readers and authors** | K1 is proxy-only; V4 to V6 untested. "Do readers catch a wrong echo" decides how much weight the meaning link can carry | K1 with people, V4, V5 | Certain |
| 9 | **CI with negative controls, and a clean-room re-check** | Nothing reruns the chain between sessions; all results are from one loaded laptop | X2, X3 | Certain |
| 10 | **Packaging and installation** | macOS arm64 only; about 55 GB; four Lean toolchains and three Rust compilers; `./translate.sh --setup` before `lake` works. Nobody else can run it today | none | Certain |
| 11 | **Frame-library versioning across projects**, with kernel-checked "meaning-preserving" upgrades | A change to one frame voids every signature in every project. The review is changing frame definitions right now, which is the first instance | V9 | Very likely (certain once there is a second project) |
| 12 | **Standard-library models** for the most-used unmodelled items | Only 382 of 4,385 census functions (9%) compile with no unmodelled external | A3 | Very likely |
| 13 | **Retire the old glossary and rename the `Wallet` library** | Two vocabularies and two statements per scenario; the legacy one still carries every proof and step | Follows from 1 | Very likely |
| 14 | **Ambiguity questions with a separating input** | Refusal exists; the question does not. The TDFLite pilot produced 22 such questions by hand and that was its most useful output | V6 | Very likely |
| 15 | **Sentence forms for two-run claims** (monotone, independent-of, agrees-with) | Definitions exist with no surface form; TDFLite guarantees 4 and 6 need them | T5 | Very likely |
| 16 | **Evidence presentation for an auditor** | The graph has the content (862 nodes); no view an evaluator would accept has been designed | open programme question | Very likely |
| 17 | **Proof repair under change, and a red-build policy** | P2 and K2 both show proofs lost to changes that falsify nothing (92 of 295 lost proofs in K2 were of rules nothing shows false) | S2 | Very likely |
| 18 | **Effects and I/O: the shell around a pure core** | Frames describe one pure call; one known TDFLite defect and the one regression a reviewer caught were both outside the model | open programme question | Likely, and large |
| 19 | **Editor and CI integration for authors** (echo on save, refusal messages in the editor) | Follows from the audience being engineers who already use Gherkin tooling | none | Likely |
| 20 | **Suggest and interpret modes** | Owner's decision 4 in `docs/VOCABULARY.md` | V7, V8 | Likely |
| 21 | **A profile lint** that checks a crate against `PROFILE.md` before translation | The profile is prose; authors learn by failing in Aeneas | none | Likely |
| 22 | **A standard attestation format** over content digests | Listed under "use existing tools"; the sign-off file is ad hoc JSON | none | Likely |
| 23 | **Concurrency** | No frame, no link, and the translator does not cover it | "deliberately not yet" by omission | Uncertain timing; certain eventually |
| 24 | **Time** ("eventually", "until") | No target needs it; step invariants have covered the cases so far | deliberately not yet | Uncertain |
| 25 | **The compilation link** | Verified Rust compilation is an open research problem | deliberately not yet | Will stay an assumption; needed only as a stated one |

**Where I would push back.**

- **Items 1, 2 and 6 are one piece of work, and it is the next one.** A Rust reading per piece gives the cucumber step, the property test, the Kani harness and the model-versus-code differential check together. The plan files this under E1 "needs V3" as if it were an extension; it is the thing that makes the vocabulary real.
- **Item 3 is cheap and is blocking the project's own claim.** The owner signing a few dozen one-line pieces, even provisionally, would turn "the mechanism exists" into "the mechanism has been used once and here is what was awkward". Until then staleness, `--strict` and roles are all untested design.
- **Items 18 and 23 are where real defects live** and the scope statement should say plainly that they are out of scope for now and why, since a reader from industry will look for them first.
- **I am unsure about item 11's priority.** With one consumer, versioning is hypothetical; with two it is urgent. It depends entirely on when S1 or a compiled TDFLite vocabulary arrives.

---

## 7. Numbers a scope statement can cite

Each with its source. Where two documents disagree, both are given.

### Vocabulary and frames

| Figure | Value | Source |
|---|---|---|
| Frame definitions in Lean | 23, covering a 14-frame catalogue | `clausal/lean/Frames/Frames.lean`; `clausal/FINDINGS.md` addendum |
| Frames reachable from a sentence | 19 (4 have no surface form) | `clausal/FINDINGS.md` |
| Vocabulary pieces | 77 = 31 domain words + 27 modifiers + 19 frames; plus 10 idioms; 87 entries in all | `clausal/FINDINGS.md`; `clausal/README.md` |
| Shared across projects, by design | 46 of 77 | `clausal/FINDINGS.md` |
| Old whole-phrase glossary | 44 entries | `clausal/glossary.yaml`; `clausal/README.md` |
| Signed entries | 0 of 87 and 0 of 44 | `clausal/README.md` chain table |
| Frame library size | 643 lines of Lean in 4 files (Core 141, Frames 178, Check 226, Lemmas 98) | `wc -l clausal/lean/Frames/*.lean` |
| Definition against executable reading | 23,700 of 23,700 evaluations agree | `clausal/FINDINGS.md` |
| Readings proved equivalent to old statements | 34 of 34 | `clausal/FINDINGS.md` |
| Rule lines compiled | 13 of 14 (the 14th deliberately unbound); 13 had to be reworded | `clausal/FINDINGS.md` |
| Rule statements | 10 proved (8 by generated glue, 2 by hand), 3 refuted, 1 unbound | `clausal/FINDINGS.md` |
| New sentences compiled with no vocabulary change | 5 of 5, written by the vocabulary's builder | `clausal/FINDINGS.md` |
| TDFLite readings expressible with the frames | 83 of 85, judged by reading | `docs/EXPERIMENTS.md` 24 |

### Fixtures and verdicts

| Figure | Value | Source |
|---|---|---|
| Fixture Rust | wallet 45 lines, ledger 85 lines (65 code lines), inventory 161 lines (128 code lines, 7 loop functions) | `clausal/README.md`; `docs/EXPERIMENTS.md` 12, 25; `p2/RESULTS.md` |
| Scenarios and verdicts | 35: 24 proved for all inputs, 6 proved for an instance, 3 refuted, 1 unbound, 1 vacuous | `clausal/FINDINGS.md` |
| Rules | 14 (5 wallet, 9 ledger) | `clausal/README.md` |
| Cucumber run | 81 scenarios, 365 steps | `clausal/FINDINGS.md` |
| Evidence graph | 862 nodes, 1,371 edges, 69 verdicts as read from `clausal/out/graph.json` this evening (other agents were running; `docs/EXPERIMENTS.md` 8 gives 109 nodes and 275 edges for the first wallet-only graph) | `clausal/out/graph.json` |
| Suite adequacy | 53 trivial implementations; 7 of 8 operations' suites rule out all of them | `docs/EXPERIMENTS.md` 21 |
| Negative controls | 27 of 27 behave as expected | `clausal/FINDINGS.md` |
| Hand-written mutants | 45 (18 wallet, 27 ledger); a scenario is shown false of 17 of 18 and 26 of 27 | `clausal/mutation/results.md` |
| Audit code in the trusted base | 180 lines of Lean (`Bdd/Audit.lean` 133, `AuditLinks.lean` 47); the architecture document says "about a hundred" | `wc -l` |

### Proof cost

| Figure | Value | Source |
|---|---|---|
| Hand-written Lean per Rust code line | wallet 1.6; ledger 6.0 (389 lines for 65); inventory 6.1 (Fable) and 6.0 (Opus 5.5) | `docs/EXPERIMENTS.md` 12, 25; `p2/RESULTS.md` |
| Ledger lemma library | 227 code lines (328 with comments, 6 modules) | `clausal/README.md`; `wc -l` |
| Agent proof run | 16 of 16 scenarios, 7 of 7 functions, each arm; 14.1 and 10.3 minutes; 14 of 27 and 8 of 16 builds failed | `p2/RESULTS.md` |
| Interval on that | Wilson 95% for 7 of 7 is about 0.65 to 1.00 | `p2/RESULTS.md` |
| Per-rule cost | property test 9 to 27 lines, Kani harness 10 to 23, Lean proof text 3 to 10 resting on up to 187 lemma lines | `clausal/compare/TRADES.md` |
| Pipeline run time | 1 min 51 s warm, 3 min 56 s cold for new modules, under load; 33 s warm measured before the adequacy note | `clausal/FINDINGS.md`; `clausal/README.md` |

### What each kind of evidence catches (K2)

| Figure | Value | Source |
|---|---|---|
| Rules compared | 23 universal rules | `clausal/compare/TRADES.md` |
| Tool-generated mutants caught | rows 50 of 52; proptest 45 plain, 50 edge-weighted; Kani 50; Lean 47 by its own search | `clausal/compare/TRADES.md` |
| Falsified (mutant, rule) pairs found | edge-weighted proptest 212 of 212; Kani 209; Lean's own search 188; rows 144 | `clausal/compare/TRADES.md` |
| Mutants caught by proof alone | 0 | `clausal/compare/TRADES.md` |
| Lost proofs | 295 on the tool set: 203 of rules really false, 92 of rules nothing shows false | `docs/EXPERIMENTS.md` 19 |
| Mutants nothing catches | 2 tool-generated and 2 hand-written | `clausal/compare/TRADES.md` |

### Translation coverage

| Figure | Value | Source |
|---|---|---|
| Census corpus | 10 crates, 4,385 functions, 44,826 code lines; Cedar is 2,503 of the functions | `census/CENSUS.md` |
| As shipped | 64 functions (1%), 307 lines; 6 of 10 crates produce no Lean | `census/CENSUS.md` |
| Aborts worked around by hand ("peeled") | 1,469 (34%); 76% of the nine crates without Cedar; Cedar 1% | `census/CENSUS.md` |
| With the patches, as shipped | 1,549 (35%), 10,337 lines (23%); nine crates 1,549 of 1,882 (82%) | `census/fork/FORK.md` |
| Contribution per patch | (ii) +1,368; (iv) +117; (i), (iii), (v) +0 on these crates | `census/fork/FORK.md` |
| Stricter readings of "translates" | 936 (21%) with every local callee compiling; 382 (9%) with no unmodelled external | `census/CENSUS.md` |
| Cedar with Charon workarounds and patches (i) to (iv) | 996 of 2,503 (40%) | `census/fork/FORK.md` |
| Patch size | 334 lines added, 53 removed, 9 source files, 5 commits | `census/fork/patches/README.md` |
| Aeneas's own tests | 122 extraction tests, no regression | `census/fork/FORK.md` |
| Soundness sample | 25 functions, 895 inputs, 0 mismatches | `census/fork/FORK.md` |
| Std items modelled by Aeneas | 347 functions, 88 trait impls, 44 types, 49 traits | `census/PROFILE.md` |
| Profile | 16 rules; 18 ranked tool improvements | `docs/EXPERIMENTS.md` 20 |
| Rewrite cost | 9 rewrites, 2 to 9 changed lines for naming, 31 and 42 for loop exits; one 5-line rename took `indexmap` from 378 to 434 functions | `census/CENSUS.md` |

### Meaning link

| Figure | Value | Source |
|---|---|---|
| Trial bank | 54 items, 18 unfaithful | `trials/meaning/SUMMARY.md` |
| Proxy readers | 8 model readers; caught 134 of 144 (93.1%, Wilson 87.7 to 96.2, items resampled 85.4 to 99.3); false alarms 1 of 288 | `trials/meaning/SUMMARY.md` |
| Human readers | 0 | `trials/meaning/SUMMARY.md` |

### Real target (public counts only; artefacts private and not inspected)

| Figure | Value | Source |
|---|---|---|
| Model size | about 1,750 lines of core Lean | `docs/EXPERIMENTS.md` 18 |
| Model against Go | agree on 271,355 generated cases plus 134,000 fresh ones; 24 of 24 model mutants detected | `docs/EXPERIMENTS.md` 18 |
| Readings | 85 written; 20 proved, 28 unrefuted, the rest refuted and confirmed on Go; 22 ambiguity questions | `docs/EXPERIMENTS.md` 18 |
| Known edge cases surfaced | 6 of 6 (search was guided); 15 further behaviours | `docs/EXPERIMENTS.md` 18 |
| Ruled specification | 162 kernel-checked theorems; 75 test vectors; 10 proposed changes, none applied | `docs/EXPERIMENTS.md` 23 |
| Review | 12 corrections, one a real defect in a proposed change on a path outside the model | `docs/EXPERIMENTS.md` 23 |

### Size of what was built

| Figure | Value | Source |
|---|---|---|
| Sentence compiler and reporters (`clausal`) | 7,255 lines of Python | `wc -l clausal/clausal/*.py` |
| Census and fork scripts | 3,272 lines of Python | `wc -l` |
| K2 harness | 1,439 lines of Python | `wc -l` |
| Maths tooling | `Rosette/` 2,835 lines of Lean; `bench/` about 11,000 lines; `tools/` 3,779 lines of Python | `wc -l` |
| Design and decision records | `clausal/DESIGN.md` 1,558 lines; `DECISIONS.md` 1,122 lines; `census/fork/FORK.md` 1,171 | `wc -l` |
| Disk | about 55 GB, nearly all regenerable | `docs/SETUP.md` |
| Elapsed | the repository's first decision entry is dated 2026-11-09; everything above is two days of agent work | `DECISIONS.md` |

**Numbers I would not cite without a caveat.**

- **"35% with five patches".** True of the total, but two patches do the work, and 35% is 82% of nine crates and 0% of the tenth.
- **"93% of wrong readings caught".** Model readers of the same family as the item author, eight runs behaving like about four readers, two debatable key entries, and the interval reaches below the 90% target. It says nothing about people.
- **"All six known edge cases surfaced".** The task text pointed at them; the repository says so itself.
- **"Two models proved all seven loop functions in under fifteen minutes".** Textbook loops both models recognised. It shows the budget did not bind.
- **"23 frames".** 14 catalogue frames; 23 is a count of Lean definitions, and 4 of them cannot be reached from a sentence.
- **Every timing.** Measured at load averages of 35 to 200 on 18 cores.

## What I am unsure of

- Whether the committed `IfThen` frame is fail-closed. The reviewer tested a fail-closed version in a scratch copy; I infer the committed one was not, and the uncommitted edits may already fix it.
- Whether `docs/SCHEMA.md` and the v2 schema still validate today's graph (rule groups, adequacy notes). The graph has a `group` node kind; I did not run the lint.
- Python dependencies outside `clausal/` (census, K2 harness, maths tooling): I checked imports only for `clausal`, the schema scripts and the mutation harness.
- Anything about the private TDFLite artefacts beyond the public counts.
- Whether a Charon upstream report for the Cedar internal compiler error exists anywhere; I found five Aeneas reports and none for Charon.
