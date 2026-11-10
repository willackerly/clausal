# Decision log

Judgement calls made while working autonomously, newest last. Each entry: what was decided, why, and how to undo it.

## 2026-11-09

1. **Discarded the original scaffold.** Everything except the brainstorm PDF moved to `_to_delete/`. Why: none of it had run against Lean (example theorem was `sorry`, trace was hand-written, analysis used regex). Undo: move files back.
2. **Installed `elan` to `~/.elan`** without modifying shell profiles. Why: no Lean on the machine. Undo: `rm -rf ~/.elan`.
3. **New project is Lean 4 + Mathlib at repo root** (`leanprover/lean4:v4.36.0-rc2`, library `Rosette`). Why: Mathlib is the only large corpus with human-chosen lemma boundaries to score against.
4. **Work on proof terms, not tactic text.** Candidate lemmas are sub-terms of the elaborated proof; extraction is re-checked by the kernel. Why: order-independent and sound by construction; the earlier tactic-state metric depended on tactic order and needed text splicing. Cost: term-level statements may be less readable — the demo measures this.
5. **Score = proof size hidden per unit of statement size** ("hiding ratio"), tested against baselines including the earlier small-state idea. Why: a testable formalisation of "short statement, lots hidden". May turn out wrong; the benchmark decides.
6. **Maths first, plus one thin Gherkin → Lean → Rust slice early** as a design probe for the shared data model, rather than a broad multi-domain build.
7. **The slice lives in `slice/` as a separate Lake project with its own pins.** Why: Aeneas pins its own Lean/Mathlib versions; keeping it separate avoids disturbing the maths project.

## slice

- **Aeneas + Charon from the prebuilt macOS arm64 release, not from source.** Release `nightly-2026.11.09-5a392f4` (`aeneas-macos-aarch64.tar.gz`, sha256 `b1d5ffeb…118f9`) unpacked to `slice/.tools/aeneas-nightly-2026.11.09-5a392f4/` (549 MB; tarball kept in `slice/.tools/dl/`). Why: it ships `aeneas`, `charon`, `charon-driver` and the matching Lean library prebuilt, so no OCaml/opam was installed. Undo: `rm -rf slice/.tools`.
- **System install: Rust `nightly-2026-09-17`** (minimal profile + `rustc-dev llvm-tools rust-src miri`, host target only) into `~/.rustup/toolchains/` (1.1 GB). Why: Charon links that exact compiler. The default toolchain is unchanged (still stable). rustup also self-updated to 1.29.3 during the install. Undo: `rustup toolchain uninstall nightly-2026-09-17`.
- **System install: Lean `v4.35.0`** into `~/.elan/toolchains/` (pulled automatically by elan from `slice/lean/lean-toolchain`). Why: it is the version the Aeneas Lean library pins; the root project stays on `v4.36.0-rc2`. Undo: `elan toolchain uninstall leanprover/lean4:v4.35.0`.
- **System side effect: Charon cache** at `~/.cache/charon/miri-sysroot/nightly-2026-09-17` (41 MB, a std sysroot with full MIR, built on first run). Undo: `rm -rf ~/.cache/charon`.
- **`slice/lean` depends on the Aeneas Lean library by path into `slice/.tools/`**, not by git rev. Why: that copy is by construction the one matching the binary and is prebuilt (first `lake build` 9 s; Mathlib comes from the cache, rev `56a00585…` = tag `v4.35.0`). Cost: `./translate.sh --setup` must run before `lake` works there. Undo: switch the `[[require]]` in `slice/lean/lakefile.toml` to a git pin.
- **Generated and hand-written Lean are separate libraries** (`Generated/` is only ever written by Aeneas and wiped on each regeneration; `Proofs/` is hand-written). Why: the two carry different evidence kinds (tool-trusted vs kernel-checked) and must not blur.
- **`translate.sh` also emits `lean/translation.json` (Aeneas `-emit-json`: Rust item -> Lean name, source lines, can_fail/can_diverge) and `lean/provenance.json` (sha256 of Rust inputs and Lean outputs, tool versions).** Why: these are the machine-readable record of the tool-trusted edge for the refinement graph.
- **Example function is `checked_add(u32, u32) -> Result<u32, AddError>` calling std `u32::checked_add`.** Consequence to keep in view: the std call is covered by Aeneas's hand-written Lean model, not by translating std's Rust body, so that model is part of the trusted base.
- **Correction and disk note for the entries above:** the Charon cache is 107 MB (not 41 MB), and Lean `v4.35.0` is 2.8 GB under `~/.elan`. The slice's own Mathlib copy with cached oleans is 7.2 GB at `slice/lean/.lake` (Mathlib was downloaded prebuilt, never compiled). Undo: `rm -rf slice/lean/.lake`. Full details and timings: `slice/TOOLCHAIN.md`.
- **Binding design chosen: hybrid on the external-generator base** (standard `.feature` + `glossary.yaml` + a short hand-written `Vocab.lean` -> generated Lean `Prop` statements, proofs in a separate append-only file, a Lean audit executable, and the same feature file run by cucumber-rs). Why over the Lean-native attribute/elaborator design: it is the only one where the feature file runs as ordinary tests, it is far cheaper for a thin slice (Python emitting applications of named definitions, no Lean metaprogramming), and a YAML phrase table is easier for a non-Lean reader to audit. Grafted from the Lean-native design: Given/Then definitions may not use any model function, a trivial-Then check, per-phrase sign-off hashes, the glossary and each statement printed in the report, and several evidence entries per graph edge with no single "weakest link" ordering. Full design: `slice/DESIGN.md`.
- **Statements use the plain form `∃ outcome posts, f args = ok (...) ∧ Thens`, not Aeneas triple notation.** Why: readable with only ∀/→/∃/∧, and a five-line bridge lemma (checked) lets proofs still use `step*`.
- **Design probes were run, not just reasoned about.** A scratch wallet crate was translated and four one-off `lake env lean` runs (about 3 s each, no loop) checked the statement form, a `step*` proof, model evaluation through `Result.match`, a satisfiability witness and a kernel-checked refutation. Evidence kept in `slice/probe/` (plain files, not in the Lake project). Undo: `rm -rf slice/probe`. Nothing was installed.
- **Findings that changed the design:** Aeneas's outer `Result` is an irreducible ITree-based definition, so `decide` cannot evaluate the model and refutations are proved by showing the call returns a value that fails the Then; `decide` also sticks on `U64.max`, so witnesses close with `simp; scalar_tac`; a Rust enum named `Error` clashes with Aeneas's `Std.Error`, so the wallet enum is `WalletError`.
- **Correction to the probe entry above:** it was seven one-off `lake env lean` runs (about 3 s each, hand-driven, no loop), not four.
- **Slice implemented end to end; one command `slice/run.sh`.** Rust wallet crate -> Charon/Aeneas -> Lean model; `features/*.feature` + `glossary.yaml` -> generated Lean statements; hand-written proofs; kernel-checked refutation and vacuity theorems generated from a boundary-grid search; cucumber-rs on the compiled Rust; `out/report.md` and `out/graph.json`. Details and deviations: `slice/DESIGN.md` section 10.
- **The `checked_add` example crate (`slice/rust`, `slice/lean/Proofs`) was deleted and replaced by `slice/wallet`**, as the task asked ("replace the trivial crate"). Not recoverable from version control (the repo is not under git); it was about 20 lines plus two short theorems, both shown in the earlier toolchain write-up.
- **New crates.io dependencies, in `slice/wallet-bdd` only:** `cucumber 0.23` (feature `output-json`) and `tokio 1`, plus their transitive dependencies, downloaded to `~/.cargo/registry` and built under `slice/wallet-bdd/target`. Built with the default stable toolchain (rustc 1.94); the Charon nightly is used only for `slice/wallet`. Undo: `rm -rf slice/wallet-bdd/target`; the registry cache is shared and harmless. Nothing else was installed system-wide.
- **Audit runs as two `lake env lean` script invocations per pipeline run, not as a `lake exe`.** Why: a native executable would need Mathlib compiled to object code. This is batch use (two runs of about 3 s), not a loop; AGENTS.md rule 1's warm bridges no longer exist in the repo.
- **Derived theorems (`.sat`, `.unsat`, `.refuted`, trivial-Then attempts) are generated into `lean/Run/Audit.lean` and judged by their axioms**, so one failing script cannot block the others; a theorem carrying `sorryAx` counts as absent.
- **A scenario's expected verdict is a tag** (`@expect-refuted`, `@expect-unbound`, `@expect-vacuous`; default proved). `run.sh` exits 0 iff every scenario gets its expected verdict, so the deliberate negative controls do not make the run red.
- **Nobody signed the glossary.** The sign-off mechanism exists (`python3 -m slicegen review`), but I did not sign on the owner's behalf, so every proved scenario carries the flag UNREVIEWED GLOSSARY. That is the honest state of the human-asserted link.
- **Graph schema extended and made a JSON Schema file** (`slice/schema/refinement-graph.schema.json`): node kind `feature`, relation `contains`, optional edge `attrs`, `source.term_path`, open `by` vocabulary. The schema forbids kernel-checked evidence on the English-to-formal and Rust-to-Lean edges.
- **Maths-side fit test done read-only**: `slice/schema/maths_fit.py` reads `out/rosette_tests_candidates.jsonl` and writes one candidate tree into the schema under `slice/schema/`. Nothing in the repo root was modified, built or run. Misfits are listed in `slice/DESIGN.md` section 10.

## review fixes (2026-11-09, after three independent reviews)

- **`Rosette.interfaceOf` no longer lists a variable twice.** Cause: `Lean.collectFVars` on a bare free variable skips its visited check. Statements such as `∀ {ι} {ι} (s : Set ι), …` are gone; dependency counts, statement sizes and hashes changed for about 30% of candidates. Regression test in `Rosette/Tests.lean`.
- **Candidate enumeration is DAG-aware.** A subterm that occurs at several tree positions is one candidate (field `occurrences`), recorded at its first position; a `have` value keeps the `haveValue` role wherever it is first met. Why: the tree walk produced up to 89% duplicate candidates and hit its budgets on proofs that are small as DAGs. Consequence: candidate counts and rank denominators in every document dropped. `Rosette.Lift` now rewrites every identical copy of a lifted subterm, not only the selected position.
- **`addTheoremChecked` forces the kernel check on** (`debug.skipKernelTC := false`), and `liftConst` rejects a result that depends on an axiom the original does not (so not on `sorryAx`). `LiftResult.truncated` reports a partial enumeration.
- **H1 verdict strengthened to "not supported"**, and the phrase "usable shortlisting signal" withdrawn. `bench/score.py` gained a depth-only baseline, a split by helper/theorem size, the nesting-chain task with a random-on-chain baseline, and looser hit definitions. Secondary pools and the tree-size ratio are labelled exploratory. The ground-truth target definition (type inferred for the inlined body) was left as is; the review's measurement of its effect is quoted in the caveats.
- **H2 pipeline is now two Lean passes** (`bench/run_reuse.sh`). Pass 1 fixes the `exact?` call (it ran outside the goal's local context and its failures were mislabelled as timeouts). Pass 2 tries one call each of ten standard tactics on the statements that survive every filter; those closed form a new class `one-tactic`. Why two passes: the filters live in Python and probing everything would take about an hour. Generalised (L1/L2) clusters made of near-whole theorem bodies are no longer counted as candidates for a shared lemma.
- **Demo re-rated for the Sobolev theorem only.** Pell and Erdős–Ginzburg–Ziv lift exactly the same lemmas as before; the Sobolev runs lift more distinct lemmas, and the 14 new statements were rated by the same rule (one rater).
- **`Rosette.lean` imports every module.** Building the library therefore compiles `Rosette.Tests` and `Rosette.Demo`, which run at compile time (about 1.5 minutes together) and rewrite `out/rosette_tests_candidates.jsonl` and `out/demo/generated/`. The corpus scan, benchmark and reuse collection stay behind environment variables.
- **Scripts that lived in the session scratchpad were moved into `bench/`**: `sweep.lean` (robustness sweep of `Rosette.Lift`), `mk_corpus_md.py` (assembles `bench/CORPUS.md`).
- **The reviewers' scratch directories `out/review_*` were left in place** as their evidence; nothing in the pipeline reads them.

## after the maths-core results (2026-11-09)

- **Accepted the negative result.** The hiding ratio and cross-proof reuse both failed on Mathlib (`out/FINDINGS.md`, which I assembled because the final agent was blocked from writing it). Not tuning the score further on Mathlib.
- **Pivot of the maths track: from "chunk one long proof with a score" to "find hierarchy and a small readable interface in a machine-generated corpus".** Why: the prior-art check measured OpenAI's Navier–Stokes/Euler repository at about 38,500 theorems of median 10 lines, so its problem is missing hierarchy, not long proofs; single-proof extraction is already published (Proof-Refactor). Method: dominators in the lemma dependency graph (a statement through which a large mass of proof must pass), validated against the human-written PFR blueprint. Undo: none needed; `Rosette/` stays as is.
- **New corpora live under `corpora/`** as separate projects with their own pins (the OpenAI repo is on Lean 4.34.0-rc2). Expect several GB of disk and a long build.
- **Replaced the root `AGENTS.md`.** The old one was still being fed to agents and pointed at discarded code.
- **After the two reviews of the slice: every invalidating or material finding was reproduced and fixed, none was disputed.** Reviewer evidence was moved from `slice/out/review_*` to `slice/review/`, because `run.sh` deletes `slice/out/`. Details: `slice/DESIGN.md` section 11.
- **A proof counts only if its type is exactly its scenario's statement.** The Lean audit now reports type, kind and declaring module per theorem. Before, `theorem <scenario> : True` was reported PROVED-FOR-ALL (reproduced in a scratch copy, exit 0). Standing negative control c1.
- **`lean/Wallet/Proofs.lean` was replaced by one Lean module per scenario** under `lean/Wallet/Proofs/`. Why: one broken proof used to cost every scenario its proof. The five existing proofs were moved unchanged.
- **Four universal scenarios added, each with a proof**, so that every return path of `deposit`, `withdraw` and `transfer` is constrained. Two of the four proofs needed a second attempt (surplus tactic after `step*`).
- **Input coverage is a generated kernel-checked theorem, not a heuristic.** Per group of universal scenarios with the same When and variables: for every input of the When there exist the remaining parameters such that some scenario's Givens hold. My first formulation assumed the shared Givens and was vacuous for a single-scenario group; it was replaced before any result was recorded.
- **The second reading of each Given/Then phrase became a pure Rust predicate** (`slice/wallet-bdd/src/lib.rs`) and is compared with the Lean definition on an argument grid (1,953 points). Why: a weakened or narrowed Lean definition used to pass silently. Cost: the readings are still two hand-written texts by the same author; agreement is tested, not proved.
- **A proved scenario whose glossary entries are unsigned has graph outcome `review`, not `pass`**, and `./run.sh --strict` fails on it. The default run still exits 0, so the unsigned state does not block work. I still did not sign on the owner's behalf; the sign-off command was exercised only in scratch copies with a test reviewer name.
- **Mutation harness added (`slice/mutation/run_mutants.py`), run on demand, not part of `run.sh`** (about 3 minutes). It works in scratch copies under `slice/build/mutation/` that share `.tools` and the Mathlib package cache by symlink; the real tree is never modified. 18 mutants and 11 negative controls. Result recorded in `slice/mutation/results.md`.
- **Graph schema version 2 adopted in full; version 1 schema file and the version-1 maths example were deleted** (superseded; the repo is not under git, so they are not recoverable, but `slice/review/schema/` holds the reviewer's migration of the old graph). Additions beyond the reviewer's proposal: relation `covers`, verdicts on function nodes, `evidence.method`, and a written staleness propagation rule. Described in `docs/SCHEMA.md`.
- **"Kernel-checked" is now reserved for evidence that names a theorem and its axioms.** Facts read out of the Lean environment by the audit (which constants a statement mentions) are tool-trusted; the "kernel-checked by instantiation" entries on example rows were dropped, because no instance theorem exists.
- **In the maths example, two lifted lemmas that print identically were kept as two nodes** joined by an `equivalent` edge with no evidence. Why: their statement sizes differ (55 and 70 nodes), so the printer hides a difference; merging them by printed text would have asserted something unknown.
- **Hand-written slice files carry the origin `model:slice-build-agent`** (set in `slice/glossary.yaml`). Coarse, but true: no person wrote or reviewed them.
- **`docs/SCHEMA.md` was created; `slice/FINDINGS.md` was NOT written by me.** The file-writing tool refused it ("subagents should return findings as text, not write report files"). I did not work around the refusal; the full findings are in the structured result returned to the workflow, which can write the file.
- **No new system-level installs** in this step. Nothing in the repo root was edited, built or run, except appending here and creating `docs/SCHEMA.md`; root files under `out/demo` and `out/reuse` were read only.

## machine corpus

### human ground-truth corpora (PFR, Carleson), 2026-11-09

- **Cloned `teorth/pfr` at HEAD `1ef23c3c` into `corpora/pfr`** (Lean 4.36.0-rc2, Mathlib `8fe7ce47`, toolchain already installed). Why HEAD: its Mathlib pin has a published cache, so no older commit was needed. `lake exe cache get` (100 s) then `lake build` (62 s wall). Undo: `rm -rf corpora/pfr out/corpus/pfr`.
- **Cloned `fpvandoorn/carleson` at HEAD `4dc72b29` (shallow) into `corpora/carleson`** as the second validation set. Undo: `rm -rf corpora/carleson out/corpus/carleson`.
- **System-level install: elan fetched toolchain `leanprover/lean4:v4.36.0-rc1`** (Carleson's pin) into `~/.elan/toolchains`. Undo: `elan toolchain uninstall leanprover/lean4:v4.36.0-rc1`. Each corpus also holds its own unpacked Mathlib under `.lake/packages` (several GB each); the download cache is shared in `~/.cache/mathlib`.
- **The exporter is a stand-alone script, `corpora/tools/ExportDecls.lean`, run with `lake env lean --run` from inside the corpus**, not a sibling Lake package. Why: a sibling package would resolve and unpack its own Mathlib; the script needs only core `Lean` and the corpus's `LEAN_PATH`. No corpus source file is modified. It is one cold start per export (about 20 s for PFR), not an iterative loop; the warm daemons named in `AGENTS.md` rule 1 do not exist in this repository.
- **Both corpora use the Lean module system, so every project module is imported directly** (list taken from the built `.olean` files). Importing only the root would hide proof bodies of non-exported theorems.
- **`PFRPalomar.Challenge` is left out of the PFR import list.** It restates the six headline theorems with `sorry` under the same names as `PFRPalomar.Solution`; with both loaded the `sorry` versions won and the axiom report showed `sorryAx`.
- **What counts as auto-generated** (dropped as a node, edges re-attached to the parent declaration or inlined): names that are internal after removing the private prefix, auxiliary recursors, `noConfusion`, constructors, recursors, structure projections, notation/macro/delaborator objects (by type), and anything without a declaration range. Structure fields therefore appear as edges to the structure. `to_additive`, `simps` and `ext` outputs are kept as ordinary declarations.
- **"Positive class" is reported two ways**: blueprint-tagged theorems over all project theorems, and over theorems outside `Mathlib/`, `ForMathlib/`, `Tactic/`, `Examples` folders (PFR's upstreaming staging area), since the blueprint does not try to cover the staging library.

### machine-generated corpus (OpenAI Navier–Stokes/Euler), 2026-11-09

- **Cloned `openai/NavierStokesAndEuler` at `f9e8bc5b` into `corpora/ns`** (full clone, 45 MB of source). Licence: Apache-2.0 (`LICENSE`, also stated in `formalization.yaml`); used for local analysis only, nothing redistributed. No release or build cache is shipped, so it was built locally: `lake exe cache get` (168 s) then `lake build` (1,068 s wall, 11,424 jobs, exit 0, no errors). Disk: 16 GB (8.3 GB project build, the rest Mathlib). Undo: `rm -rf corpora/ns corpora/ns_export out/corpus/ns`.
- **System-level install: elan fetched toolchain `leanprover/lean4:v4.34.0-rc2`** (the corpus's pin) into `~/.elan/toolchains`. Undo: `elan toolchain uninstall leanprover/lean4:v4.34.0-rc2`.
- **Separate exporter for this corpus: `corpora/ns_export/Export.lean`, compiled to a native binary** (`lean -c`, `leanc -rdynamic`) instead of reusing `corpora/tools/ExportDecls.lean` under `lean --run`. Why: 95,123 project constants; compiled and split over 14 processes the export takes 3.3 min. Field names were aligned with the PFR/Carleson export where the meaning is the same (`line`, `statementHash`, `numExtType`, `numAux`, ...); differences are listed in `out/corpus/ns/README.md` (hash is hex here, `kind: instance` also covers unregistered local instances, no `directAxioms`/`fieldsSize`/`isUnsafe`). No corpus source file was modified.
- **`ComparatorChallenges.NavierStokes` and `ComparatorChallenges.Euler` are built but not imported for the export.** They restate the headline theorems with `sorry` (the only two `sorry` warnings in the build log). All other 2,657 modules are imported.
- **A reference to another declaration's body auxiliary (a shared `match_N`) is not an edge to that declaration.** The first export drew such edges and over-reached by 53 declarations below the main Navier–Stokes theorem; after the change the reachable set equals the raw constant closure exactly.
- **Structure fields and constructors are edges to the structure, and constructor types count on the structure's type side.** Auto-generated objects are recognised by kernel kind, name shape and, for ambiguous names such as `ext` or `inj`, by having no source range of their own.

### dominator outline of the machine corpus (`bench/outline.py`, `out/corpus/outline/`), 2026-11-10

- **No installs; nothing built or run in Lean.** The analysis reads `out/corpus/ns/decls.jsonl` only (Python 3 standard library; `networkx`, already present, is used for a cross-check in the tests and for the Louvain fallback). Undo: `rm -rf out/corpus/outline bench/outline.py`.
- **Proof mass = `proofSize + auxProofSize`**, not `proofSize` alone. Why: 18% of the corpus's proof content sits in auxiliaries the exporter folded into their parents.
- **Edges are the union of statement and proof dependencies.** Dropping statement dependencies changes the reachable set by 13 declarations and the shape not at all.
- **"Spine" and "hub" are my terms**: a dominator-tree child carrying at least 90% of its parent's mass is collapsed into a chain; the end of the chain from the root is the hub, and chapters are its children that dominate 20 or more declarations. The 90% and 20 thresholds are arbitrary.
- **The outline is grown best-first by dominated mass** (40 entries, 3 levels below the hub, entries under 0.1% of the mass or dominating nothing excluded). It does not use statement length or docstrings, so unreadable statements are not filtered out; that is deliberate, to report what the graph alone gives.
- **Full statements are printed for two of the four roots** (`navier_stokes_breakdown_R3`, `euler_breakdown_R3`); the periodic and compact-support variants share almost their whole graph and are printed as names. All four are complete in `outline.json`.
- **Ratings of the 15 heaviest chapter statements are hand-written** in `out/corpus/outline/ratings.json` by the agent after reading the source, one reader, no second opinion. `verdict.md` in the same folder is also hand-written and is prepended to the generated `OUTLINE.md`; its numbers were copied from `shape.json`/`relaxations.json` and will not update if the script's parameters change.
- **No statements were re-printed in Lean** and no file was added to the ns export package.

## slice: loops

Second example crate `slice/ledger` (Vec of balances, two while loops, batch of transfers), added beside the wallet on 2026-11-09/10. Everything is under `slice/`; nothing in the repo root, `corpora/` or `out/` was touched, built or run, except appending here. No pin was edited and `lake update` was not run. Detail: `slice/DESIGN.md` section 12.

- **`Vec` and slices were used as asked; no fallback to arrays was needed.** The pinned Aeneas translated the 85-line crate at the first attempt. Index-based `while` loops were chosen because `for i in 0..n`, `iter().sum()` and `try_fold` with a closure do not translate with this Aeneas (probed one at a time; recorded in `slice/TOOLCHAIN.md`).
- **Batch semantics: both variants were written.** `apply_batch` stops at the first rejected transfer and returns the count; `apply_all` is all-or-nothing by cloning the balances and putting them back. Rollback by clone, not by undoing transfers, because it translates and its proof is short. A self-transfer (`from == to`) is rejected, because the read-then-write code would otherwise create money.
- **One glossary, one statements file for both crates; the Lean library that holds them is still called `Wallet`.** Why: renaming would have meant editing the nine wallet proof files and the mutation controls that point at them, for no gain in what is measured. Cost: `lean/Wallet/Proofs/ledger/` is a confusing path. Undo: rename the library and the imports.
- **Several Whens are now allowed (`Given*, When+, Then+`), by the smallest extension I could argue sound**: one nested `∃ outputs, call = ok outputs ∧` per When; each When runs on the state the previous one left; `the result` in a Then is the last When's. It claims that every call returns and nothing about intermediate results. Deliberately not done: a Then between two Whens, kernel refutation of a multi-When scenario, input coverage for one. The wallet's generated statements are character-for-character unchanged.
- **A Then about `the result` must declare which result type it speaks about**; a mismatch with the (last) When is reported as UNSUPPORTED instead of breaking the Lean build for every scenario. This added an `outcome_type` line to two wallet glossary entries; the phrase digests used for sign-off are unaffected.
- **Loop invariants and helper lemmas live in one hand-written file, `slice/lean/Ledger/Lemmas.lean`, registered as `@[step]` lemmas and imported by the generated audit script.** Why: the generated refutation script can then use them, so a false claim about a loop can still be refuted in the kernel. They are untrusted (kernel-checked, in no statement). If the file fails to compile, the run names it, drops every proof that imports it and keeps the wallet's.
- **I wrote the ledger's batch computation a second time as a pure recursive function (`runN`) and proved the loop computes it.** Why: with invariants alone, the three literal-value scenarios could not be proved and the counterexample to the false batch claim could not be confirmed in the kernel (Aeneas's `loop` cannot be evaluated by `decide`, `rfl` or `simp`). I first recorded those as TESTED-ONLY / COUNTEREXAMPLE, then spent about 60 more lines of Lean to turn them into PROVED-INSTANCE / REFUTED. Both states are described in DESIGN.md 12.5; the cost is the finding.
- **Two deliberately false ledger scenarios, not one.** `total_always_available` is refuted from the invariant lemma alone; `batch_all_valid_all_applied` needs the exact-result lemma. Keeping both shows the difference.
- **No scenario was weakened to make a proof go through.** Two glossary definitions were changed during the work, both for reasons unrelated to provability: `l[i]!` became a named helper `bal` (the `!` form panics in the interpreter on out-of-range grid points), and the result-type declarations above.
- **The helper definitions `LVocab.valid`, `bal` and `total` restate part of what the code checks**, in terms of lists and numbers and without mentioning any model function. That is unavoidable for "a valid transfer", but it means the glossary for the ledger is less obviously independent of the code than the wallet's.
- **Mutation harness extended, still run on demand**: 22 ledger mutants (11 of them loop bugs) and 4 more negative controls; results in `slice/mutation/results.md`. The old results files `results-before-review.*` were left as they are.
- **Coverage for `total` is reported as NOT SHOWN although its two scenarios do cover every ledger.** The coverage generator groups scenarios by identical variable lists and these two differ; I recorded the limit instead of special-casing it.
- **`slice/FINDINGS.md` was not edited** (the task said to return the account, not to write a findings file). Its "Limitations" still says there are no loops; that line is now out of date.
- **No new system-level installs and no new crates.io dependencies.** `slice/ledger/target` and `slice/ledger/Cargo.lock` are new build outputs; undo with `rm -rf slice/ledger/target`.

## machine corpus

### H3 validation judgement calls (2026-11-10, `bench/validate_outline.py`, `out/corpus/validation/`)
- **What:** no installs. Analysis uses the Python packages already present (numpy 2.3.5, scipy 1.16.3, scikit-learn 1.9.0, networkx 3.6.1). No Lean was run; all inputs are the exported `decls.jsonl` and `blueprint.json`.
- **Roots:** dominator tree is computed from a virtual root over every headline theorem listed in each corpus's `axioms.json` (12 in PFR, 4 in Carleson), not from one theorem. Why: both projects have several end results. Undo: pass a single name in `load()`.
- **Negative class / evaluation sets:** primary set is theorems only (tagged vs untagged). The task's literal wording (tagged declarations of any kind vs untagged theorems) is reported as `SPEC`; it makes "is a definition" a perfect cue, so it is not the primary set. Also reported: mainline only (staging folders removed, same path filter as the corpus export) and mainline-reachable.
- **k:** number of blueprint nodes (219, 180), fixed across evaluation sets. In PFR mainline k exceeds the number of positives, capping precision@k at 0.66.
- **Proof mass:** `proofSize + auxProofSize` for every declaration, own proof included in dominated and transitive mass.
- **PageRank:** both directions reported, since "reversed graph" is ambiguous.
- **Cycles:** Carleson has two 2-cycles from `mutual` theorems; kept, handled by condensation.
- **Cross-validation:** folds grouped by module, so declarations of one file never appear in both train and test.
- **Source text read in two diagnostics only** (docstring cites blueprint numbering; docstring contains `$`). These are contamination checks, not features or labels.
- **Undo:** delete `out/corpus/validation/`, `bench/validate_outline.py`, `bench/validate_outline_extra.py`.

## friction census

- **Started a census testing the owner's pasted thread (2026-11-10).** The thread claims analysis proofs bloat from constant tracking, real/extended-real casts, domain surgery and measurability side-conditions, and proposes bundling them into "packets"; it gave no data (its "30% / 70%" split is unsourced). Why now: the machine corpus (Navier–Stokes) and a human analysis corpus (Carleson) are both built, so the claims are measurable. Includes one real experiment: define a packet structure and restate a cluster of real theorems against it, kernel-checked. Outputs in `out/corpus/friction/`. Undo: `rm -rf corpora/friction out/corpus/friction bench/friction_*`.
- **(later the same day) The lemma file was split into one module per Rust function, `slice/lean/Ledger/Lemmas/{Basic,Apply,Batch,Total,Balance,All}.lean`; where the entries above say `Lemmas.lean`, read `Lemmas/`.** Why: the first mutation run showed that with one file any ledger mutant cost all sixteen ledger scenarios their proofs, so "proof lost" said nothing about which scenario was affected.
- **A scenario was added after the first mutation run: `whole_example_accept` (a good batch applied as a whole is accepted).** Why: the mutant "apply_all rejects every batch" made no scenario statement false; the run only failed because a hand-written lemma, stronger than any scenario, stopped proving. That is a gap in the scenarios, and a lemma must not be what closes it. The mutation run was then repeated in full; `slice/mutation/results.*` are from the second run.
- **The mutation summary separates "a proof is lost" from "a counterexample is found".** A lost proof only says the proof no longer compiles; I had first counted every changed verdict of a deliberately false scenario as a counterexample found, which overstated the search by one mutant per crate. The summary is recomputed from the recorded verdicts (`run_mutants.py --resummarise`), with no rerun.

## baseline documents (2026-11-10)

- **Wrote `README.md`, `TODO.md`, `docs/EXPERIMENTS.md`, `docs/SETUP.md`, `docs/TDFLITE.md`** at the owner's request. Results from the three runs still in flight are marked preliminary or running and must be updated when they finish.
- **`docs/TDFLITE.md` is written from the plan document alone.** The TDFLite repository was not read.
- **Extended `.gitignore`** to exclude cloned corpora, downloaded tools and build output. The repo is still not under git; that is the owner's call.

## version control (2026-11-10)

- **Initialised git and published to `github.com/willackerly/lean-rosette` (public), as the owner asked.**
- **Held back from the public repo via `.gitignore`, pending the owner's say-so:** `tdflite-ideas/` and `docs/TDFLITE.md` (they describe unresolved edge cases in TDFLite's key-release decision, and the TDFLite repo is public), and the brainstorm PDF (it contains personal remarks). They remain on disk, untracked. Undo: remove the lines from `.gitignore` and commit.
- **Also untracked:** `_to_delete/`, the template `.github/` workflows from `lake new` (one of them opens automatic Mathlib-update PRs), compiled exporters, and regenerable data files over about 20 MB.
- **No licence file yet.** Until one is added the public repo is "all rights reserved" by default.
- **Deleted `_to_delete/`** (owner confirmed). **Added `LICENSE` (Apache-2.0).** **Commit author email switched to GitHub's no-reply address** for this repo (local git config), and the initial commit was rewritten and force-pushed so the Gmail address is no longer in the history.

### recurrence / deduplication analysis of the machine corpus (`corpora/ns_reuse`, `out/corpus/reuse`), 2026-11-10

- **The "ns analysis package" for this step is a new directory `corpora/ns_reuse/`** (no Lake project of its own: stand-alone Lean files run with the corpus's `LEAN_PATH` from `corpora/ns_export/lean_path.txt`, toolchain pinned by a copied `lean-toolchain`). Why: nothing in `corpora/ns` or `corpora/ns_export` is edited, and no second Mathlib is unpacked. Undo: `rm -rf corpora/ns_reuse out/corpus/reuse bench/corpus_reuse.py`. No system-level install.
- **`Rosette/Candidates.lean` and `Rosette/Reuse.lean` were not edited.** `corpora/ns_reuse/mk_reuse_ns.py` assembles `ReuseNS.lean` from them by text substitution; they compiled on Lean 4.34.0-rc2 with no API change.
- **The in-proof traversal was made DAG-aware for this corpus**, which the Mathlib run was not. Why: with the original tree walk 43 of the first 129 sampled theorems hit the 300,000-visit budget and 4 more ran out of heartbeats, with proof DAG sizes of only 1–3 thousand, and the two processes were stopped after 25 minutes. Consequence: nested candidates keep only their first tree position, which can only lower the measured saving. The Mathlib numbers were NOT recomputed with the new traversal (that would mean running in the repo-root Lake project, which this step must not touch).
- **The in-proof run is sharded over processes** (8 per sample; `exact?` and the one-tactic probe are separate second passes driven by key lists). Each shard is one cold `lean` start that imports the whole corpus plus Mathlib; this is a batch job, not an iterative loop, and the warm daemons named in `AGENTS.md` rule 1 do not exist. The anti-unifier pass (levels L1/L2 of `out/reuse/REUSE.md`) was dropped because it is not meaningful inside one shard.
- **"About 500 theorems with the largest proofs" was read as: proof DAG size ≥ 800** (the Mathlib run's threshold; 16,885 of 38,601 theorems), sampled twice with seed 20261109: 500 uniformly, and 501 as whole consecutive modules (the like-for-like counterpart of the Mathlib directory slices).
- **`exact?` in this environment also finds the project's own lemmas.** The strict column of the comparison keeps the Mathlib rule (closed by `exact?` = trivial); a second column treats a statement closed by a PROJECT lemma as not trivial, so that an inline re-proof of a named project lemma is counted as redundancy.
- **Kernel checks use `Environment.addDeclCore`, not `Lean.addDecl`.** On this toolchain `addDecl` type-checks asynchronously and only logs a kernel error; the first version of the harness therefore reported 312 of 312 for the cloned-module test, where the synchronous check gives 168. All factoring results were rerun with the synchronous check.
- **Statement keys ignore universe levels.** Six exact-statement "duplicates" differ in universe polymorphism and are reported as failures of the mechanical check rather than fixed by hand.
- **The 20-largest-cluster verdicts and the 14-cluster SV-P sample in `out/corpus/reuse/judgements.json` are my own reading of the source**, not a mathematician's.

## composable vocabulary (2026-11-10, decided by the owner in conversation)

- **One frame library shared across projects**; logical frames and generic modifiers are defined and signed once.
- **Fail-closed defaults**: "never" and "always" cover every input, including rejected ones; weaker readings must be explicit.
- **First authors are product-minded senior engineers**; product and compliance authors are on the roadmap.
- **Two modes**: *suggest* (loose sentence to precise candidates the author accepts) and *interpret* (a fixed source such as a signed contract is left untouched; formal sentences state how it is read).
- Recorded in `docs/VOCABULARY.md` with a worked example; summarised at the top of `README.md`. Implementation is queued behind the loops experiment because that run is still changing `slice/`.

## slice: loops (adversarial review, 2026-11-10)

- **Reviewed in scratch copies only.** Two copies of `slice/` made with `mutation/workcopy.sh` under the session scratchpad (tools and Mathlib package cache shared by symlink). In `slice/` itself only `slice/review/loops/` was written. No pin edited, no `lake update`, nothing run in the repo root.
- **Five reviewer mutants were aimed at what the scenario set leaves open, not sampled blindly**: three bugs that need a third loop iteration or a fourth account (outside the search grid of batches of at most 2 and ledgers of at most 3), one atomicity bug in `apply_all`, one miscount. They measure the gaps I expected from reading the statements; they are not an unbiased kill rate.
- **"Survives" is judged against the scenario statements, not the run's exit status.** All five make `./run.sh` exit non-zero, but four only because a hand-written lemma (which is stronger than every scenario) stops compiling. For one of them (`r3`) I re-proved the lemma and two scenario proofs against the mutant and the run then exits 0 with every scenario PROVED, so I report it as a survivor. I did not do the same for `r1`; I argue it from the statements.
- **`lake env lean` was run a handful of times on one reviewer file in a scratch copy**, as `run.sh` itself does; the warm daemons named in `AGENTS.md` rule 1 do not exist in this tree.
- **The machine was heavily loaded by the other job** (load average near 100), so my timings (86 s for `./run.sh`, 27 minutes for the mutation harness) are not comparable with the builder's and I do not report them as findings.
- **Gherkin stays the surface; one-line claims use its `Rule:` keyword** (owner's preference, Claude's recommendation). **Time words deferred** until a target needs them; TDFLite's decision core does not. Both recorded as decisions 5 and 6 in `docs/VOCABULARY.md`.

### friction export (2026-11-10, `corpora/friction/`, `bench/friction_*`, `out/corpus/friction/`)

- **No installs, nothing built in any corpus.** `corpora/friction/Friction.lean` imports only `Lean` and is compiled three times, once per corpus toolchain (`lean +<toolchain> -c`, `leanc`), into `corpora/friction/build/<corpus>/`. It loads the built environments with `importModules`. `LEAN_SYSROOT` is set per run so the binary loads the matching core library. Undo: `rm -rf corpora/friction out/corpus/friction bench/friction_*`.
- **Lean was started cold three times per verification run** (`lean` on a scratch `#check` file written to `out/corpus/friction/<corpus>/verify_check.lean`, run with the corpus `LEAN_PATH`, not through `lake`). One process per corpus, not a loop; the warm daemons of `AGENTS.md` rule 1 do not exist here.
- **Theorems = `kind == theorem` in the existing `decls.jsonl`**; the name lists are passed to the exporter so the inclusion rule cannot drift. Prop-valued instances are therefore out.
- **Body auxiliaries are inlined at their use sites** (a non-primary project constant with a value whose nearest primary name-prefix is the theorem, or which has none). A foreign declaration's auxiliary is left as a constant.
- **Classification is by Expr shape and head constant, lemmas by the class of their own statement**, not by name patterns. Name matching is used only for explicit lists (cast functions, rewrite glue, tactic certificate namespaces/modules) and for one substring rule (`cutoff`/`bump`/`mollif` in a constant name, so that project-defined cutoffs are seen).
- **Side-condition classes are finiteness, positivity, measurability, integrability, regularity, support.** `topo` (IsOpen, IsCompact, Monotone, Convex, bounded-set predicates), `tc` (Prop-valued type classes), `prob` (independence, identical distribution) and `cert` (norm_num result predicates) are named classes but not side conditions. Moving `topo` into the side set would raise the side-condition share; it was left out because the chat's claim (D) lists only measurability/integrability/continuity/smoothness.
- **Judgement calls inside the lists:** `Summable`, `MeasureTheory.BoundedCompactSupport` count as integrability; `HasDerivAt`-style statements and `LipschitzWith` as regularity; `IsProbabilityMeasure`, `IsMarkovKernel`, `SigmaFinite` as finiteness; `BorelSpace`, `SecondCountableTopology`, `PseudoMetrizableSpace`, `MeasurableSingletonClass` as measurability; `NeZero`, `Fact (0 < x)` as positivity.
- **`0 < 0` is not positivity.** First run put 23% of PFR's proof mass under positivity; the cause was linarith's final contradiction, whose argument has type `0 < 0`. The shape rule now requires the subject not to be the literal. After the change PFR positivity is 6.3%.
- **Set inclusion is `mem`, not `order`.** In the Mathlib used by Carleson and PFR `⊆` on `Set` elaborates to `LE.le` (confirmed with `pp.explicit`); a carrier-type rule reclassifies it.
- **Cast flag excludes ℝ≥0∞-valued norms.** With `enorm`/`nnnorm`/`edist` in the cast list 52% of Carleson's proof nodes were in a cast region; they are now a separate `enorm` flag (43% remains, from real coercions and because the region is inherited from the theorem statement).
- **Proof mass uses fractional shares on the DAG** (a node reached under k labels gives 1/k to each) after opening each binder once. Tree-weighted counts explode on shared terms; first-reach attribution depends on traversal order. A first version re-opened binders on every revisit and double counted bodies; fixed by caching the opened binder.
- **Class budget:** the walk packs labels into 64 bits, so at most 16 classes and 7 side-condition classes.
- **Hand check:** 15 theorems per corpus, chosen by a fixed hash order within feature categories (statement at most 700 nodes and 16 binders so they are readable), one reader, 45/45 agree. Three exporter defects were found by reading the sample and fixed before the final run (nested `∃ C, 0 < C` under `∀` not counted; `Fact (0 < P)` classed as logic; `⊤` of `ℕ∞` in `ContDiff ℝ ∞` indistinguishable from `⊤ : ℝ≥0∞`, now a separate `ennrealTop` flag).

## slice: loops (fixes after the adversarial review, 2026-11-10)

- **All six material findings were reproduced and treated as real.** The five reviewer mutants were added to `slice/mutation/run_mutants.py` (`r1`..`r5`) and run against the tree as it was: four change no example row and give the search nothing, exactly as reported (`slice/review/loops-fix/before_fix_reviewer_mutants.log`).
- **"Noticed" now means a scenario is shown false, not that the run fails.** The mutation summary and the report give two figures: a row differs on the compiled Rust or the search finds a counterexample (counted as detection), and "the run fails only because a proof or lemma stopped compiling" (not counted). Why: a lemma can say more than any scenario, and the review showed a lost proof can be won back by re-proving around the bug. The run's exit status is unchanged; only what is claimed for it changed.
- **No pure model in the glossary.** The review asks for a decision on whether a trusted pure model of the batch may appear in the glossary, since without one loops get only safety properties. I did not add one: it is the owner's design rule (no restating the code in a Then) and the vocabulary work is deciding the same question. Instead I added the strongest properties I could state without one: "a batch stops only at a transfer that is not valid on the ledger it left" (progress) and "a rejected whole batch leaves the ledger unchanged" (atomicity). Consequence, stated in the report: the scenarios still do not determine which ledger a batch leaves, nor that every counted transfer was applied. Undo: delete the scenarios `batch_stops_at_invalid`, `whole_rejected_unchanged`, `whole_example_rollback_late`, `batch_then_total_overflow`, their proof files, the glossary entries `LT-stops-at-invalid` and `LT-same-if-rejected` (glossary.yaml, `lean/Ledger/Vocab.lean`, `wallet-bdd`), and the lemmas `runN_stops` and `Ledger.apply_batch.stops`.
- **The new scenarios, rows and grid points were written knowing the reviewer's five mutants.** The search grid gained two four-account ledgers and four batches of three and four transfers; three example tables gained rows with three to five elements. So "all five are now shown false" is a fix confirmed, not an unbiased detection rate.
- **`batch_then_total` was retitled, not widened** ("... when that total fits"), and its overflow twin was added as a second two-When scenario. No scenario was weakened and no existing statement changed other than by that title.
- **The non-vacuity witness is now chosen, not the first found.** The search prefers a satisfying input where no list is empty and the operation changes the state it returns. This changes which witness the `.sat` theorems use for most scenarios, including the wallet's; it changes no statement and no verdict.
- **"Coverage" was renamed, not strengthened.** The report section now says "some proved universal scenario applies to every input" and lists, per operation, what the proved Thens say about the returned value and about the state. I did not add a kernel check that the Thens determine the result: a `simp` attempt at that would mostly fail for uninteresting reasons and read as a finding.
- **Effort is now logged, not remembered.** `slice/lakebuild.sh` appends every build attempt to `slice/effort/attempts.tsv`; `slice/effort/count.py` counts hand-written Lean per crate against Rust code lines. The builder's earlier attempt counts and hour estimates remain unverifiable and are labelled so.
- **The mutation harness was run from a snapshot copy of `slice/`** (made with `mutation/workcopy.sh` in the session scratchpad) so that editing documentation meanwhile could not change what a job copied; results and logs were copied back. The snapshot's digest equals the tree's.
- **`slice/FINDINGS.md` was not edited**; its "no loops" limitation and its counts describe the wallet-only state.

## plan (2026-11-10)

- **Drafted `docs/PLAN.md`**: a dependency graph of hypotheses in four tracks (proof cost, vocabulary, TDFLite, mathematics), each with a test, thresholds fixed in advance and a model. Thresholds are first guesses.
- **Mathematics stays in this repository** as a long-term, lower-intensity track (owner's wish; Claude agrees). Split later if it gains its own users or its corpora slow the software side.
- **Sent the draft for critique by two agents on Opus 5.5** (method, strategy), deliberately a different model from the author, and started plan node V1 (prior-art check for the vocabulary track). The plan will be revised from their findings.

## friction census

### bundle mining and the packet experiment (2026-11-10, `bench/friction_bundles.py`, `corpora/friction/{Bundles,Callsites}.lean`, `corpora/friction/packet/`, `out/corpus/friction/BUNDLES.md`)

- **No installs; nothing in any corpus was built or edited.** Two more native exporters were compiled against the corpus toolchains into `corpora/friction/build/<corpus>/` (`bundles`, `callsites`), and five sibling Lean files were compiled against the built ns environment into `corpora/friction/build/ns/packet/`. Undo: `rm -rf corpora/friction/{Bundles.lean,Callsites.lean,bundles_run.sh,packet_run.sh,packet} corpora/friction/build/*/{bundles,Bundles.*,callsites,Callsites.*} corpora/friction/build/ns/packet out/corpus/friction/*/bundles out/corpus/friction/BUNDLES.md bench/friction_bundles.py`.
- **A new exporter instead of reusing `hyps.jsonl`.** The existing shape keys number variables per hypothesis, so two hypotheses cannot be tied to the same variable. `Bundles.lean` writes keys with telescope indices. Its class rule was re-implemented in Python and agrees with the first exporter on every whole Prop binder (105,235 in ns, 4,778 in Carleson, 0 disagreements); statement sizes agree for every theorem.
- **Hypotheses are split through top-level `∧`; conclusions through `∧` and `∃`.** Why: a conjunction hypothesis is already a small bundle, and "is the bundle produced" needs the conjuncts of conclusions.
- **Two bundle notions.** Per-variable bundles are mined exhaustively (closed itemsets). Variable-group bundles identify variables by binder name and are grown greedily; this is a heuristic, chosen because exhaustive mining over whole telescopes blows up on theorems with 20 identical hypotheses, and because the machine corpus reuses binder names consistently.
- **"Side-condition bundle" is read loosely by default** (at least one side-condition atom), since the task's own example `{0 < C, C ≤ K}` contains an order atom. The strict reading is reported next to it.
- **Saving is split into naming and merging.** The task's metric (bundle as one hypothesis) credits a bundle with the size of its atoms; almost all of that would also be obtained by giving each large hypothesis a name. Both parts are reported.
- **Node shares are given for theorems of at most 100,000 statement nodes.** Why: ns statement tree sizes sum to 3.3 × 10¹¹, of which a handful of theorems hold nearly everything; a share of that total is meaningless.
- **Atoms over 3,000 tree nodes get no key and are not mined** (5,077 of 105,283 in ns). Why: the key is a full serialisation.
- **"Already packaged" is a syntactic field match** against every structure, class and conjunctive Prop definition in the environment (6,278 structures and 496 definitions for ns). It does not find a structure that states the same facts differently.
- **Experiment bundle: the frame bundle `{0 ≤ T, 0 < c, coercivity of Q, Q₁ = dQ/dt}`**, the top-ranked bundle with no packaging structure. The two `CompleteSpace` instances that co-occur with it were left out of the structure: they are instance arguments, not hypotheses.
- **The packet is a Prop-valued structure over unbundled data** (`Frame T Q Q₁ c : Prop`), not a structure that also contains `T`, `Q`, `Q₁`, `c`. Why: it is exactly "the bundle as one hypothesis", which is what the mining metric scores, and it keeps the corpus's definitions usable unchanged. A data-carrying packet was not built.
- **Cluster rule fixed before reading proofs:** first module, by number of carriers, whose carriers contain a connected component of at least 8. It selected `Euler.FixedEndpointStrong` (9 theorems).
- **All nine were re-proved directly, not only three**, because the port was mechanical (a scripted rename of the source proofs). The three designated ones are still reported separately.
- **A third variant with packet-level wrappers for 17 operations was added** to measure the "API per operation" cost rather than argue about it.
- **Lean was started cold for these files** (one process per file, about ten runs in total, 3–25 s each). This is not an iterative proof-search loop, and the warm daemons named in `AGENTS.md` rule 1 do not exist in this repository.
- **Loops result recorded (plan node P1).** I added the ledger addendum to `slice/FINDINGS.md` and updated `docs/EXPERIMENTS.md` and the README, since the run's agents could not edit those. Plan revision waits for the critiques.

## friction census

### the census itself (2026-11-10, `bench/friction_census.py`, `corpora/friction/Census.lean`, `out/corpus/friction/CENSUS.md`)

- **No installs; nothing in any corpus was built or edited.** A second native exporter, `corpora/friction/Census.lean`, was compiled against each corpus toolchain into `corpora/friction/build/<corpus>/census` and run by `corpora/friction/census_run.sh` (9 s / 9 s / 21 s wall). Why a second exporter and not more Python: the unfolding proxies and the literal / ε-shape / `∃ C` detectors need per-theorem constant sets and Expr shapes that `hyps.jsonl` does not carry, and the rule is no regex over text. `run.sh` and its outputs were not touched. Lean starts cold once per shard, as in the export; no warm daemon exists here. Undo: `rm -rf corpora/friction/Census.lean corpora/friction/census_run.sh corpora/friction/build/*/[Cc]ensus* out/corpus/friction/*/census out/corpus/friction/{CENSUS.md,census.json} bench/friction_census*`.
- **`bench/friction_census.py` is run without `-I`** because numpy is in the user site-packages. It reads only files this repository produced.
- **"Support library" of ns = modules that import no project module** (72 modules, 2,010 theorems; import graph from the environment header). The repository has no support folder and the Navier–Stokes and Euler halves do not import each other, so there is no shared library to point at. Carleson's analogue is its `ToMathlib` folder.
- **Verdict thresholds are judgement, not a test.** "Supported" would need the family to be a material share of machine proof mass (I used about 5% as the bar) with the content the chat described; "partly" means the pattern is there but small, or large but with different content. B and C are judged on direct measures; their region figures are upper bounds and are reported as such.
- **Claim A producer = conclusion with a real-typed ∃ carrying `0 < C` or `0 ≤ C`** (the export's `exRealPos`). A stricter row requires C to be used as an upper bound. A hash-ordered sample showed one non-constant (`∃ T, 0 < T ∧ T ≤ Tmax ∧ …`) among five.
- **"Constant taken as a parameter" cannot be told from any positive real parameter structurally.** Reported three ways: any real binder with `0 < x`; that plus an inequality conclusion mentioning it; that plus a binder name matching `C*`, `K*`, `M*`, `c*`. The last is a heuristic on binder names read from the Expr.
- **"Named real constant" = project definition with result type ℝ / ℝ≥0 / ℝ≥0∞ and only ℕ / ℤ arguments.** Added because Carleson handles constants this way (`C2_1_2 a`), which the chat's framing leaves out.
- **Five unfolding proxies instead of the three or four asked for.** The fifth (equation-lemma rewrites, project bundles) is the only direct trace of unfolding in a proof term, and it is weak: `simp [foo]`, `unfold`, `dsimp`, `show` on non-recursive definitions leave nothing in the term. Stated in the document.
- **ε-shape detector tightened after reading its hits**: the first version accepted any `… ≤ r` with the positive parameter somewhere in `r` and fired on `∃ C, … ≤ C * f h`; it now needs the right-hand side to be the variable itself or a coercion of it.
- **Intervals are theorem bootstraps (B = 1000, percentile), as asked; a module-level bootstrap is reported for the key rows.** Neither covers variation between projects: there is one machine corpus.
- **Subject control = three checks** (theorems mentioning `Mathlib.MeasureTheory`; theorems with a claim-D hypothesis; support library against `ToMathlib`), not a matched design. No difference is attributed to machine authorship.
- **Examples are chosen by SHA-1 order of the theorem name** among matches whose stored statement is complete and at most 420 characters. The cap biases towards short statements (for `∃ C` in ns, 186 of 946 pass).
- **The verdict text is hand-written** in `bench/friction_census_verdict.md` with placeholders filled from the computed numbers; the wording of a verdict will not change by itself if a number moves.
- **Plan revised to draft 2 after two critiques (Opus 5.5) and the vocabulary prior-art check.** Adopted: cheap falsification tests first (Track K); a hollowness gate on every proved verdict; a blind TDFLite pilot moved ahead of the frame library; a harder second target (Track S); rebuilt proof-cost test; larger samples with separated pass/fail bands; people on judgement nodes. Not adopted as written: hard deadlines that would end the maths track (the owner wants it kept long-term; it has a spring-2027 review instead), and a 3-lines-per-line cost cap for P2 (measured cost is 6; reported, not gated).
- **README target report now shows a hollowness caution**, since the flagship rule is also true of a ledger that rejects every transfer.

### review fixes for the declaration-graph work (2026-11-10, `out/corpus/`, `bench/outline.py`, `bench/validate_outline*.py`, `bench/corpus_reuse.py`, `corpora/tools/ExportDecls.lean`)

Filed under "## machine corpus". No installs. Undo for everything below: restore from `out/corpus/_before_fix/` (exports, validation outputs, outline verdict and reports as they stood before these fixes) and revert the scripts named.

- **PFR/Carleson exporter changed and both corpora re-exported** (two cold `lake env lean --run` batch runs via `corpora/tools/run_pfr.sh` and `run_carleson.sh`; the warm daemons of `AGENTS.md` rule 1 do not exist here). A use of another declaration's body auxiliary (`_proof_N`, `_simp_N`, `match_N`, hygienic `irreducible_def` wrappers) used to become an edge to that declaration; it now inlines the auxiliary's own dependencies, as `corpora/ns_export/Export.lean` does. Derived objects (constructors, projections, recursors, equation lemmas) still become an edge to their parent and their bodies are still ignored, so the 36 Carleson edges the reviewer's over-approximate closure finds through `eq_def`/`_mutual` bodies are deliberately not added. Result: Carleson -294 +112 edges, PFR -6 +1; the reviewer's 294 false edges are exactly the ones removed.
- **Validation intervals are now a module-cluster bootstrap** (whole files resampled). Wider than before; still test-set sampling only.
- **Validation gained three models** (surface without docstring, size only, surface plus length) and a single-root table. `src_lines` and `stmt_chars` come from the Lean export (declaration range, pretty-printed signature), not from source text.
- **`VALIDATION.md` is now generated** by `bench/validate_outline_report.py` from `results.json`, `extra.json` and the score tables, so its numbers cannot drift; only wording and the per-example descriptions are hand-written. The "ten examples" lists were kept as the same declarations (facts re-read from the new scores), not re-selected.
- **Outline: a chapter is now a child of the hub OR a side branch of a spine node.** Why: the paper's comparison step `no_global_solution_one` hangs off a spine node and was missed. Consequence: Navier-Stokes 59 -> 61 chapters, 62.2% -> 65.0% of mass; Euler unchanged.
- **Ratings: 16 statements, not 15.** The newly found chapter was rated (milestone) after reading its source; the displaced lightest one was kept rather than dropped. The Euler lemma `initialDatum_no_global_solution` was re-labelled from milestone to "restatement of the headline theorem" on the second reader's argument. Waypoints carry a `printed` field (readable / opaque); the opaque/readable split is my reading, guided by the second reader's list.
- **Object-plus-statements cuts (relaxation b') are limited to objects mentioned in the statements of at most 10 declarations**, to keep the interface small enough to read and the run under a minute. Objects with more statement-level users (for example `profile`) are not tested.
- **Paper-step coverage table uses the second reader's filename-keyword mapping** unchanged; it is rough and only for Navier-Stokes.
- **Minor reuse findings were recorded as review notes in `REUSE.md`, not fixed in code**: the two "substantive" totals live in `bench/reuse.py` (the Mathlib run's script, not mine to change here), and F1/F6 were not rerun with a transitive circularity check.
- **The Navier-Stokes export was not re-run.** The reviewer's finding about 103 structures with unexplained value-side edges changes no immediate dominator below the Navier-Stokes root and 5 below the Euler root; it is listed as a limitation.

## owner's steer on the plan (2026-11-10)

- **Stance recorded in `docs/PLAN.md` (draft 3):** the destination (proofs between English and working code) is fixed and the question is how good and what trades; report, don't gate; do not overfit to the wallet; rules come in suites, so hollowness is a suite-level note; a restricted Rust profile is fine and forking a tool is an option; people tests deferred to subagent proxies on infrastructure people can use later.
- **TDFLite source:** owner OK'd reading it. A private copy was cloned from the local checkout `~/dev/tdflite` into `private/tdflite-src` at commit `4aca7ca` (the commit the verification plan refers to). The owner's own checkout is untouched. `private/` is git-ignored. Undo: `rm -rf private`.

## overnight autonomous session (2026-11-10, owner offline until 10:00 Eastern)

- **Assembled `out/corpus/FINDINGS.md`** from the finished machine-corpus run and marked experiments 9–11 final.
- **Launched the first step of the plan as one workflow**: blind TDFLite pilot (model written from the Go source by an agent barred from the plan documents, then scored by a second model against the six known edge cases), K2 trade map, K3 translation census, `Rule:` support plus the suite adequacy note in the slice, and the K1 meaning trial on subagent proxy readers with a harness people can use later. All TDFLite material is written under `private/` (git-ignored); public notes carry counts only.
- **Call: blind pilot uses commit `4aca7ca`**, the one the owner's plan refers to, so results are comparable with the known edge cases, not the latest branch.
- **Call: K2 and K3 may install tools** (cargo-mutants, proptest, Kani, a second Aeneas release) and log them here.

## friction census

### fixes after the adversarial review (2026-11-10, `bench/friction_robust.py`, `corpora/friction/robust_run.sh`, `out/corpus/friction/ROBUSTNESS.md`)

- **No installs; nothing in any corpus was built or edited.** `corpora/friction/Friction.lean` was changed (below) and recompiled into `corpora/friction/build/<corpus>/friction`. Under the baseline config the new binary reproduces every stored row of the Carleson and PFR exports exactly (2,675 and 978 rows, 0 differing); ns was not re-run under the baseline config, but its node total under the variant equals the stored one. `hyps.jsonl` and the other baseline files were not rewritten. Undo: restore `Friction.lean` from before this entry (the diff is the `predScan` block, the `auxlist` / `preds` modes, the `instProp` config field and the label layout), and `rm -rf corpora/friction/robust_run.sh bench/friction_robust.py bench/friction_robust_head.md out/corpus/friction/{robust,robust.json,ROBUSTNESS.md} out/corpus/friction/*/robust`.
- **All eleven review findings were reproduced; none was rejected.** One was corrected in size: proof content outside theorems is 7.6% of ns proof nodes, not 18.5%. The 18.5% used the corpus export's size fields, which count the data terms of definitions and compiler-generated lemmas (`eq_N`, `injEq`, `sizeOf_spec`, `congr_simp`). I count `_proof_N` auxiliaries and Prop-typed non-theorem declarations only.
- **Variant exports instead of re-running the baseline with new rules.** The first census's numbers stay reproducible as "the first rule"; each review point is a separate variant (`split`, `splitinst`, `aux`, `preds`) written under `<corpus>/robust/`. Why: the review's point was that the headline depended on rule choices, so the honest presentation is the same data under several rules, not a new single rule.
- **Derivative-value facts (`HasDerivAt`, `HasFDerivAt`, `HasDerivWithinAt`, … 11 heads) are a class of their own in the variants, still listed as a side class.** Why: keeping it a side class makes regularity + derivative-value equal baseline regularity (to 0.15%), so the split is a decomposition and not a new partition. Whether "the derivative of f is g" is a side condition is left to the reader; D is reported both ways.
- **Claim D is reported as a range over four rules (outer/inner × with/without derivative-value facts), with an upper bound from project predicates and a figure including non-theorem proofs.** No single number is designated the headline.
- **Project predicates are opened by a syntactic scan, not by re-running the classifier with unfolding switched on.** `predScan` δ-unfolds project definitions with their arguments, replaces a one-constructor inductive by its field types, and recurses through ∧ / ∨ / ↔ and whatever the usual peel removes, to depth 8 (and separately to depth 2). Output is a table per predicate; Python joins it to hypothesis and conclusion heads. Why not reclassify: a predicate with a smoothness field, a bound field and a positivity field has no single class, and forcing one would hide exactly what the review asked to see. Consequence: "contains a smoothness fact" is unweighted, and the D upper bound (20.3%) charges whole theorems.
- **Hidden `∃ C` producers are reported at two depths** (1,509 within two levels, 1,675 at any depth). Two levels is enough for an abbreviation of a structure (`MeanClass := MemClass …`); deeper hits include large certificate structures where the constant is one field among many.
- **Matched stratum = statement mentions `eLpNorm` / `MemLp` / `Lp` or an integral, and no derivative / `ContDiff` constant**, the reviewer's definition, taken from the statement constant sets of `Census.lean`. I kept it rather than design another so that the review's numbers could be checked exactly (they match).
- **Instance share standardised both ways** (ns at Carleson's size mix, Carleson at ns's), six size bins. The two answers (+6.3, +8.9) bracket the size effect; neither is preferred.
- **Verdicts changed:** A from "partly supported" to "supported as a pattern, moderate in size"; D keeps "partly supported" with "size not robust"; unfolding from "not supported" to "cannot tell"; packets from "marginal" to "marginal as tested". B and C unchanged. The 5%-of-proof-mass bar for "material" is unchanged; A now clears it only when hidden producers are included (5.1% direct, about 9% with them).
- **The source-level tactic counts in the unfolding section are regex over source**, against the rule for this census. They are quoted as a cross-check that motivated the verdict change, labelled as such, and no figure in any table depends on them.
- **Not done:** certificate output inside the positivity class was not separated (the `splitinst` variant removes instance arguments only); the bundle miner was not re-run with shared-atom collapsing (`BUNDLES.md` states the family structure in words, from `MINING.md`); no packet-native proofs were written.
- **`BUNDLES.md` is hand-edited**, not generated; its new net figures are arithmetic on numbers already in the document and in `packet_measure.jsonl`.
- **Lean was started cold** once per shard per variant (three variants × three corpora) and twice per corpus for the predicate tables, single processes of 2–25 s. The warm daemons named in `AGENTS.md` rule 1 do not exist in this repository.

## K2 trade map

### installs and working area (2026-11-10, `slice/compare/`)

- **System-level installs (three), all outside the repository.** (1) `cargo install --locked cargo-mutants` -> `~/.cargo/bin/cargo-mutants` v27.1.0 (15 s). (2) `cargo install --locked kani-verifier` -> `~/.cargo/bin/cargo-kani`, `~/.cargo/bin/kani` v0.68.0 (7 s). (3) `cargo kani setup` -> `~/.kani/kani-0.68.0` (352 MB, bundles CBMC 6.11.0) and the Rust toolchain `nightly-2026-08-21-aarch64-apple-darwin` in `~/.rustup/toolchains/` (13 s). Why: the task names both tools; Kani needs its own pinned nightly. Logs: `slice/compare/logs/install-*.log`, `kani-setup.log`. Undo: `cargo uninstall cargo-mutants kani-verifier; rm -rf ~/.kani; rustup toolchain uninstall nightly-2026-08-21-aarch64-apple-darwin`.
- **Everything is written under `slice/compare/` only.** Pipeline runs and mutations happen in scratch copies under `slice/compare/work/` (git-ignored by `slice/compare/.gitignore`), which share `slice/.tools` and `slice/lean/.lake/packages` by symlink, read-only. `slice/` itself, the pins and the Lake manifests are not touched; `lake update` is never run. Undo: `rm -rf slice/compare`.
- **Friction census closed.** Appended its findings to `out/corpus/FINDINGS.md`, marked experiment 13 final. The run's reviewer softened several of the builder's verdicts; the published numbers are the post-review ones.
- **Launched the maths-track step in parallel** (owner wants the maths kept for the long term): a ground truth for the machine corpus built from its own papers; a definition-centred outline rated blind by proxy readers against the old outline with one rubric; a dead-code report confirmed by deleting and rebuilding in a copy (`corpora/ns_trim/`, the original untouched); and a compression experiment on hand-threaded constants (a "≲"-style relation, proofs written natively against it). Why the last: it is the one friction pattern the census found real and specific to the machine corpus, and it is a direct test of "can a different angle compress the complexity".
- **Call: two heavy workflows run at once** on one machine. Cost: slower builds. Benefit: both finish before the owner returns.

## maths: constant-threading experiment

- **Family frozen by rule before any design (2026-11-10).** Producers are the census set (946 theorems whose conclusion has a real `∃` with a sign conjunct, `concl.exRealPos > 0` in `out/corpus/friction/ns/hyps.jsonl`); depth is the longest producer-to-producer chain through `valueDeps` of `out/corpus/ns/decls.jsonl` (reproduces the census histogram, maximum 13, three heads). Head: the deepest producer, ties broken by lexicographically smallest full name, giving `NavierStokes.ActualPhysicalStageBounds.CycleInputs.potential_bound`. Family: one longest path down from it, at each step the direct producer dependency one level lower, ties by smallest name. 13 theorems, listed in `out/corpus/lesssim/family.json`; scripts `corpora/lesssim/chain.py`, `family.py`. The alternative, the head's whole 31-theorem cone, was not taken: the chain is what the census reported and the task's "longest chain" names it.
- **Runner.** Files under `corpora/lesssim/lean/` are compiled one `lean` process each against the built corpus environment (`corpora/lesssim/run.sh`, same method as `corpora/friction/packet_run.sh`, about 13 s per file of which most is import). No lake, no corpus rebuild, no installs. AGENTS.md's warm-bridge rule names daemons that this checkout does not run; the task text allows this method.

## K1 item bank (item author, 2026-11-10)

Judgement calls made while writing the K1 paper-prototype items (30 echo items, 24 glossary items, domain brief). The bank itself was returned to the workflow, not written to the repo (the task said create no files). Nothing here says which items are wrong.

- **Glossary items: defect between phrase and definition, not between English and Lean.** Each definition's English sentence is a faithful paraphrase of the Lean shown with it; a seeded defect is in what the definition means relative to the phrase. A reader who cannot read Lean can still catch every defect. Undo: rewrite the seeded items so the English matches the real definition and only the Lean is altered (that measures Lean reading instead).
- **Real definitions with a latent problem were kept out of the "faithful" set**, so that a reader who flags a real problem is not scored as a false alarm. Two found while authoring, worth fixing in the glossary regardless of K1: (1) `LVocab.moved` holds for a zero-amount transfer naming an account that does not exist (because `bal` reads a missing account as 0), e.g. `[3]`, `0->5:0`, unchanged ledger; (2) `appliedAll` / `appliedNone` / `appliedExactly` constrain the count the batch *reports*, not what was applied, so a batch that reports the full length without applying anything satisfies "every transfer of b is applied" (other Thens usually catch it). Undo: none needed; these are notes.
- **Cross-item cues limited, not removed.** Where one of a complementary pair of glossary phrases was seeded, its partner was left out of the bank. Milder cues remain within and between the two banks (a real glossary has them too); the answer key notes the cross-bank ones so the analyst can run the banks separately or together and report which.
- **The brief states the house reading** ("never/always" include rejected calls; change judged before/after one call; every call must return) and defines valid, internal, aggregate, covers, room and total. Without them several items have no single right answer. It deliberately does not explain "only if". Undo: drop the "How rules are read" paragraph; expect more disagreement on the faithful items that spell out defaults.
- **Disagreeing inputs are often behaviours of a hypothetical faulty implementation** (start state, input, end state, result), because on the correct code a faithful reading and a wrong one often both hold. The answer key says which kind each is.
- **Order**: Python `random.Random(20261110)`, echo list shuffled first, then glossary list; ids E01–E30 and G01–G24 assigned after shuffling.
- **The repo is public**: the answer key should not be committed before the reader runs (proxy or human) have taken the trial.

## maths: constant-threading experiment (continued)

- **Relation: Mathlib's own, not a new one.** `f =O[𝓟 S] g` (big-O along the principal filter of the set of parameters the constant must be uniform in) unfolds to exactly the corpus's shape; parameters the constant may depend on are bound outside. The task says to use Mathlib if it fits, and it does for 12 of the 13.
- **Sample of 10 outside the family frozen before reading any of them**: `random.Random(20261110).sample(sorted(946 producers minus the 13), 10)`; list in `out/corpus/lesssim/sample.json`. Drawn from all ∃C theorems, not only those the shape rule accepts, so that the sample also tests the rule.

## maths: paper ground truth

Builder: model agent, 2026-11-10. Output: `out/corpus/papers/` (`truth.json`, `TRUTH.md`, `BASELINES.md`, `baselines.json`, `src/`) and `bench/paper_truth.py`. Nothing else in the repository was written; `corpora/ns` was read only.

- **Installs: none.** `curl`, `pdftotext` (poppler, already at `/opt/homebrew/bin`) and `numpy` (already present) were used. No Lean process was started; all Lean-side data is read from the existing export `out/corpus/ns/decls.jsonl` and from the corpus sources.
- **Papers fetched from the two URLs in the corpus README** (cdn.openai.com, PDFs dated 2026-09-08; sha256 in `truth.json`). The PDFs and extracted text stay in the session scratch directory. The repository holds paraphrases written by the builder and no quotation longer than a phrase.
- **Item set for Euler widened by the builder.** The Euler paper has 5 numbered results. Added: the 7 numbered claims inside Propositions 3.1 and 4.1, 12 equation-numbered definitions from the paper's notation index, 7 numbered subsections of Sections 5 and 6. For Navier-Stokes, 6 equation-numbered definitions were added to the 80 numbered results. This is a builder's selection (against Rule 2 for a measured node); each item carries a `kind` so a later scorer can drop them.
- **Renumbering established from content, not from the old manuscript**, which is not in the repository. Six of 44 rows rest on a statement comparison, 28 on docstring content, 10 on topic only.
- **Confidence scale.** `certain` = cited in the published numbering or TeX label, named in the README, or statement read against the paper; `probable` = old-numbering citation with matched content, or a docstring describing the content; `guess` = name only. After verification a `match` raises a mapping to `certain`.
- **Mapping granularity.** 1 to 5 declarations per item (statement, closing theorem, definition), not the full set of declarations implementing it. A complete item-to-module map was left as a next action.
- **Verification sample chosen by seed, read by the builder.** `random.Random(20261110)` over all 333 mappings, 20 drawn: 12 match, 7 partial, 1 weak. The builder script refuses to write `truth.json` if the recorded verification list stops matching the seeded draw. No second reader was available in this step; labelled as a model proxy and as non-independent.
- **"Largest proof beneath it" defined as proof mass reachable through dependencies** (exact, by bit sets; equals the dominator file's figure at the root, 24,565,760). "Own proof size" and "docstring, ordered by mass beneath" were added as rows because the first saturates early.
- **"Has a docstring" is a set, not a ranking**: reported as the whole set, as a mean over 200 seeded random orders, and ordered by mass beneath.
- **Near hits count either direction of dependency.** They are inflated by hubs (50 random declarations are one step from 12 of 85 Navier-Stokes items), so every table carries random-order reference rows and the write-up treats exact hits as the result.
- **Negative results reported as found**: the dominator outline reaches 8 of 85 Navier-Stokes items and 4 of 31 Euler items exactly; 32 of the 85 mapped Navier-Stokes items have no target below the whole-space headline theorem.

## slice: Rule and adequacy note

Builder: model agent, 2026-11-10 (owner offline). Plan nodes F1, the first check of V2, and X1a for the slice. Written only under `slice/` (not `slice/compare/`) and here. No system-level install; no pin, lockfile or `lake update` touched. Detail: `slice/DESIGN.md` section 13.

- **`Rule:` runs under the pinned cucumber-rs (0.23.0, gherkin 0.16.0): confirmed by running it**, not from the documentation. A Scenario Outline with Examples under a `Rule:`, a Rule-level Background, the `Example:` keyword and a tag on the Rule were run in a scratch copy; feature file, log and JSON are kept in `slice/review/rule-probe/`. Two facts that shaped the code: the JSON writer reports a Background as a separate element on the scenario's line (the report now merges the two), and it does not copy a Rule's tags onto its scenarios (so the generator does the inheriting itself).
- **The rule line is carried, not compiled.** No runner gives it meaning and there is no frame library yet, so the rule text and the description under it go into the report and the graph verbatim, and every block says so. What is proved is each scenario beneath the rule. Consequence: nothing checks that a rule line says what its scenarios say. Undo: none needed; this is the absence of a feature.
- **Scenario ids do not include the Rule**, so regrouping scenarios under Rules moved no proof file and changed no statement. Rule ids are `Rule.<feature>.<slug of the text>` (or `@id:` on the Rule).
- **Tag inheritance.** Feature and Rule tags apply to the scenarios beneath them; `@id:` is never inherited; a scenario's own `@expect-*` wins over its Rule's, which wins over the Feature's. One deliberately false scenario in each feature now gets `@expect-refuted` from its Rule (the third keeps its own tag) so both paths are exercised.
- **Feature files regrouped mechanically, no scenario added, removed or reworded.** A script moved each scenario block (with the tags and comments above it) under a Rule and re-indented it; one comment that said "the three scenarios above" was reworded. 5 Rules in the wallet, 9 in the ledger. Rule texts are the builder's wording and are unreviewed. Undo: `git checkout slice/features`.
- **New tag `@control`** on `features/negative.feature`: its scenarios get verdicts as before but are left out of the adequacy note. Without it, the control "a deposit does not touch a bystander" would count as the deposit suite's progress scenario.
- **What "trivial implementation" means here (the builder's reading of the four kinds in the plan).** reject-all: always a rejecting value, state unchanged. no-op: always a success value, state unchanged. identity: answers as the real model does but never changes the state (chosen over "state unchanged with any answer", which is what the other kinds already are). constant: every listed result value, with the state unchanged or reset to a fixed one. Each is a Lean definition whose type is `type_of%` the generated model, so "of the same type" is checked by Lean.
- **Added a `trivial:` section to `glossary.yaml`** saying which result values count as a rejection or a success, plus one hand-written model for `apply_batch` ("reports the whole batch as applied, changes nothing", which is not a constant). This is new vocabulary-file content written by the builder and unsigned. It is used by no statement that gets a verdict and voids no sign-off digest. Undo: delete the section; the note then reports "not computed".
- **"Rules out" is decided by search, with kernel confirmation where the generated script goes through.** A scenario rules out a trivial model when the counterexample grid holds an input on which the scenario, restated with the trivial model in place of the call, is false. "Still allows" therefore means "not shown false on the grid" unless the block says "proved": for constant models and single-When scenarios a kernel proof that the scenario holds of the trivial model for all inputs is attempted, and a kernel refutation at the found input. Pairs with several Whens and the identity variant get no kernel attempt.
- **Only PROVED scenarios are counted**, universal ones for "rules out", literal examples separately ("ruled out only by a literal example"). Unproved scenarios are listed as not counted.
- **The note is in the graph without a schema change**: trivial models are `function` nodes, each restated scenario is a `statement` node, a found input is an `example` that `refutes` it, the per-Rule line is a `note` label plus `attrs` on a `group` node for the Rule, and there is one verdict per operation with the new codes `SUITE-RULES-OUT-TRIVIAL` / `SUITE-ALLOWS-TRIVIAL` (outcome `pass`/`review`, or `open`). `docs/SCHEMA.md` is outside this task's write area and does not yet mention Rule groups or these codes.
- **The note cannot fail a run.** Its two Lean scripts are not imported by anything, run in the background beside steps 5 to 7, and their exit status is ignored. `./run.sh --no-adequacy` skips them. Cost: 21 s and 12 s of wall time measured alone on a lightly loaded machine, beside a run that took 33 s before; the whole run was not re-measured on an idle machine (other jobs held the load average at 60 to 100 for the rest of the session).
- **Two more one-shot `lake env lean` runs per pipeline run** (`Run/Adequacy.lean`, `Run/AdequacyAudit.lean`), the same pattern as the existing `Run/Search.lean` and `Run/Audit.lean`. `AGENTS.md` rule 1 forbids `lake env lean` inside an iterative loop; these are once per run, and the daemons that rule names no longer exist (already noted in `slice/TOOLCHAIN.md`).
- **Per-Rule block is generated from the graph file.** `slicegen report` writes `out/graph.json`, reads the file back, and renders the blocks from what it read (`slicegen/rules.py`, which imports nothing else from the generator); `python3 -m slicegen rules` prints the same from a stored graph. The run fails if a block disagrees with the verdicts computed in memory. To make that possible the graph gained a few `attrs` (example rows' results, scenario names) and the real `rustc --version` of the cucumber build (it used to say "default stable toolchain").
- **Echo-back is not printed** (out of scope until the frame library exists); the generated Lean statement of each scenario is printed as before, now beneath its Rule's block.
- **Mutation harness changed in four places, reported as such**: (1) the helper that removes scenarios now finds them by id instead of by text offsets, because the files were regrouped; (2) control c3 matches each count of the tally separately, because the tally's order follows scenario order; (3) control c14's patch text is re-indented; (4) mutant runs pass `--no-adequacy` (the note feeds no verdict and no exit status; the baseline and every control run the whole pipeline). Five controls added (c16 to c20). `mutation/workcopy.sh` no longer copies `slice/compare/` (another agent's directory, 200 MB and growing) into each scratch copy.
- **Coverage theorem names moved.** `Coverage.g1..g3` are numbered by scenario order, so the regrouping renumbered three of them; their statements are the same up to the order of disjuncts. Every scenario verdict, flag and counterexample is identical to the run before the change (compared field by field).
- **Rule verdict headline is about the scenarios.** A block says "SCENARIOS PROVED FOR ALL INPUTS", not "PROVED FOR ALL INPUTS" as in the README target, because the rule line itself is not compiled and so has no verdict of its own.
- **Evidence kept**: `slice/review/rule-probe/` (the cucumber-rs run), `slice/review/rule-adequacy/` (final run log, mutation run log, and `compare_with_previous.py`, which re-derives "nothing that existed before has changed" from git and the current outputs). Fast checks without Lean: `python3 -m slicegen.selftest`.
- **Not done, on purpose**: no scenario was added to close the gap the note reports for `apply_all` (it would be a new rule and new vocabulary, which this task did not ask for); the generated `lean/Run/Adequacy*.lean` (1.3 MB) and the larger `out/graph.json` (2.9 MB, was 1.6 MB) were left for the owner to decide whether to track; nothing was committed.

## K1 meaning trial (proxy)

Calls made while turning the proxy run into the harness under `trials/meaning/` (2026-11-10, owner offline). Nothing was installed.

- **Key-revealing files are git-ignored in `trials/meaning/`**: `key.json`, `responses/`, `REPORT.md`, `results.json`, `analyst_notes.md`, `item_flags.json`. Why: the repo is public, no person has taken the trial, and the readers' reasons and the report's item lists give the key away as surely as the key does (the item author asked for the same). A key-free `SUMMARY.md` with the headline rates is not ignored. Cost: those files exist only on this machine, with no backup in git. Undo: delete the lines in `trials/meaning/.gitignore`.
- **Data was extracted, not retyped.** The item bank, key and reader answers were pulled byte for byte from this workflow's own task text in the session transcript and written by a script. Undo: none needed.
- **haiku-1's answers were recovered and are scored.** The workflow recorded an empty list; the reader's transcript shows 54 answers submitted and then replaced by a second, empty submission. The first submission is stored with a caveat. Why: leaving it out removes the weakest reader and the only false alarm. The report's sensitivity table gives the rates without it (119/126 caught, 0/252 false alarms, against 134/144 and 1/288 with it). Undo: `python3 score.py --exclude-reader haiku-1`, or delete `responses/haiku-1.json`.
- **No item was dropped or re-keyed.** Six items are flagged for the item author in `item_flags.json` (one as key-debatable, five for review) and listed in the report. Only the key-debatable one (G10) is left out, and only in one labelled sensitivity row. Undo: empty the `flags` object.
- **Human presentation differs from the proxies'.** People see one item at a time, shuffled within each part, Part A before Part B, with no going back. The proxies saw all 54 at once in bank order. Items, brief and question text are identical (the question text is copied from the workflow's reader prompt). Why: the task asked for one item at a time in a per-reader shuffled order. Undo: `take_trial.py --seed` cannot reproduce bank order; that would need a small change to `make_order`.
- **Confidence is asked of people as 50 to 100 and stored as 0 to 1**, to match the proxies' 0-to-1 field. A reason is required only when the judgement is not-faithful.
- **A catch for the wrong reason counts as a catch.** Reasons are recorded and shown for missed and wrongly flagged items but not marked. Marking them is a judgement call for a person (plan rule 4).
- **Pooled intervals: both Wilson and an item-resampling bootstrap are reported**, because judgements of the same item by several readers are not independent and the Wilson interval on pooled counts is too narrow.
- **The proxy run is labelled exploratory under plan rule 1**: the item set was not committed before the readers answered. Before people take it, commit `items.json`, `brief.md` and the hash.
- **Further banks go in `trials/meaning/banks/<name>/`** and fixes to an existing bank go in a new bank version, because the hash in every answers file covers the items and the brief.
- **`trial.html` carries a self-test** (`trial.html#selftest`) used by `run_tests.py` in headless Chrome with a throwaway profile; the owner's own Chrome profile was not touched. Undo: remove the `selftest` function from `trial.template.html` and the browser step from `run_tests.py`.

## maths: constant-threading experiment (results and calls, 2026-11-10)

- **Result in one line**: 11 of 13 chain theorems re-proved natively against `=O[𝓟 S]`, 2 through an escape hatch, none failed; proofs −4.2% in elaborated nodes (−27% on the six steps that only pass a constant along, ±0 on analytic steps, +17.5% at interfaces with explicit constants); the 15-lemma library (8,603 nodes) costs more than the family saves (1,073). Report: `out/corpus/lesssim/LESSSIM.md`.
- **Call: an escape hatch counts as "went through", and is reported separately.** Step 7 concludes the project structure `JetData`, whose fields take the constants as arguments; its statement is kept. Restating `JetData` and re-proving its 57-line consumer outside the family was judged out of scope.
- **Call: `∀ j ≤ m` stays outside the relation and the exponent `p` stays existential.** Jets of order `j` live in a type depending on `j`; Mathlib has no "up to a power of a slow scale" relation. Both are reported as limits of the fit, not hidden behind a new definition.
- **Call: multi-parameter statements use pattern-matching lambdas; the projection form is also checked and measured** (`Variants.lean`), because the two differ by 24% in statement nodes.
- **Call: the shape rule is run in Lean on all 946 producers** (`ShapeBody.lean`), not on the truncated shape strings of the census export. It is a rule about statements; the sample shows it overstates "library unchanged" (4 of 7 rule-fits went through unchanged).
- **Call: for the sample, theorems outside the rule get a reason and no attempt; S5 and S10 get a kernel-checked equivalence of statements but no native proof; S8 is checked only at `E : Type`** because `jet_comp` inherits `Type` from the corpus lemma it wraps. The library was not changed after the family, so that "unchanged" means what it says.
- **Call: two private corpus lemmas (`potential_gain`, `mean_gain`) are reached with `open private`** for step 13, as the original proof uses them; nothing in the corpus is modified.
- **Call: after measuring, two trivial `ring` calls in new code were replaced by `simp only [mul_assoc]`** (one library lemma −698 nodes, one sample proof). Tactic choice moves node counts by this much; said in the report's limits.
- **Not done**: reader ratings of statements (no proxy readers were used); a fully native corpus without `∃ C` neighbours; the other two depth-13 heads.
- **Installs**: none. Writes: `corpora/lesssim/`, `out/corpus/lesssim/`, this file.

## K3 translation census

Work is in `census/` (plan node K3). Entries are in the order the calls were made, 2026-11-10.

- **Corpus chosen by a script, before any translation was run** (`census/scripts/select_corpus.py`, output `census/data/selection/corpus.json`). Business set: `cedar-policy-core 4.14.1`, `rust_decimal 1.43.0`, `semver 1.0.28` (named in the task); small parser = `shlex 2.0.1` (first crate by downloads in crates.io category `parser-implementations` that is a hand-written parser, at most 3,000 lines, no mandatory dependency; `syn`, `serde_json`, `toml` precede it and fail that test); money = `rusty-money 0.5.1` (first crate by downloads under keyword `money` that is about money amounts; `chinese-number` precedes it). Popular set: the 200 most-downloaded crates, minus six exclusion classes applied by name and description only (proc-macro/build helpers, OS/FFI bindings, async/network/logging, synchronisation primitives, macro- or data-only crates, crates already in the business set) leaves 93; `random.Random(20261110).sample(sorted(eligible), 5)` drew `indexmap 2.14.2`, `untrusted 0.9.0`, `fnv 1.0.7`, `time 0.3.55`, `zeroize 1.9.1`. Why: plan rule 2 (items not chosen by the builder). The exclusion classes are my judgement; the per-crate assignment is in the script. Undo: nothing to undo; rerun the script to reproduce.
- **Tools reused, not reinstalled.** The pinned Charon/Aeneas in `slice/.tools` are used through symlinks in `census/.tools/aeneas-nightly-2026.11.09-5a392f4/`; the Aeneas Lean library and the slice's Mathlib packages were APFS-cloned (`cp -c`, no extra disk until they diverge) into `census/.tools/.../backends` and `census/lean-pinned/.lake/packages`, so `lake build` in the census can never write into `slice/`. `census/lean-pinned/lake-manifest.json` is a copy of the slice's manifest; `lake update` was never run. Undo: `rm -rf census/.tools census/lean-pinned/.lake`.
- **Newer Aeneas downloaded side by side**: `nightly-2026.11.10-0d21a9e` (sha256 `e1e1fe737a81e954f98a4b259e29f8f4e73365791126483874e0c76c61b1522a`) into `census/.tools/aeneas-nightly-2026.11.10-0d21a9e/`. It ships the same Charon (0.1.315, 454586e) and needs the same Rust nightly; the only upstream commit between the two is the Lean bump to v4.36.0-rc2. Nothing installed system-wide for it. Undo: delete the directory.
- **Charon and Aeneas sources cloned read-only** into `census/upstream/{charon,aeneas}` at the pinned commits (`454586e9`, `5a392f4b`), git-ignored. Undo: `rm -rf census/upstream`.
- **A function inventory independent of Charon is the denominator.** `census/tools/fninv` (Rust, `syn`) lists every `fn` with a body in the crate's non-test sources, with its line span and syntactic features. Why: if Charon defined the function list, anything it dropped silently would vanish from the count. Consequences: functions under a `cfg` that the default feature set switches off are counted as "not compiled" and left out of the rates; functions written by macros and derives are not in the inventory and are reported as a separate group.
- **Two levels are reported for every crate: "as is" and "peeled".** As is = `charon cargo --preset=aeneas` then `aeneas -backend lean`, nothing else. On five of the ten crates that gives no Lean at all, because Aeneas raises an uncaught exception on one standard-library trait method signature and aborts the crate (a sixth, cedar-policy-core, stops earlier, in Charon). Peeled = the same LLBC with the offending declaration removed (`Iterator::copied`, `Iterator::cloned`, `Iterator::try_fold`: the method entry; `core::str::pattern::Pattern`: the trait and its impls), which is what Aeneas would do if `translate_method_sig` in `src/Translate.ml` caught the error the way the function-signature loop three lines above it does. Every removal is logged per crate with the message that caused it. Why: without it the per-function census would be a column of zeros with one cause, and the profile could not be written. Trade: peeled numbers describe a tool with one small fix applied, not the tool as shipped; both are in every table.
- **Charon is run with `--no-dedup-serialized-ast`** so that a declaration can be removed from the LLBC file without breaking back-references. This only changes the serialisation.
- **Charon `--exclude` was tried first for the peel and dropped**: it removes the function body but can leave the trait's method entry in place (`Iterator::copied` in indexmap), so the crash stays.
- **`-print-unknown-externals` is not used**: it crashes this Aeneas (`Can't convert the name of a tuple to a pattern`).
- **Lean is given `-DmaxErrors=10000000`** in `census/lean-pinned/lakefile.toml` (`moreLeanArgs`). Lean stops a file at 100 errors, which silently truncated the first runs. `set_option maxErrors` inside the file and `leanOptions` in the lakefile did not lift the limit.

## tdflite pilot (blind)

Entries from the blind modelling task T1a part 1 (2026-11-10, owner offline). All work
product is under the git-ignored `private/tdflite-pilot/`; details live there
(`MODEL.md`), not here. No system-level installs were made.

- **Which Go code counts as "the two engines".** What: modelled the string reference
  evaluator in `pkg/pdp/classification` and the compiled path `pkg/pdp/snapshot` +
  `pkg/pdp/snapshot/snapconform` as the lite key access service calls it, plus the
  wrapper in `internal/lite/kas` and the bundle bridge in `internal/lite/bundlesource`.
  `pkg/pdp/snapshot_engine.go` and `pkg/pdp/core` were read and left out. Why: on
  reading, those files are the delegation / token-exchange facade and are not on the
  key-release call path. Undo: nothing to revert; extend the model if they are wanted.
- **Core Lean only.** What: the Lean project has no dependencies (no Mathlib, no
  Plausible); random and bounded-exhaustive cases come from seeded Python generators
  and are checked against the real Go through a JSON differential harness. Why: avoids
  any download, and the oracle is the Go code rather than a Lean property. Undo: add a
  `require` to `private/tdflite-pilot/lean/lakefile.toml`.
- **Running the real Go.** What: copied the TDFLite module (without `.git`) to
  `private/tdflite-pilot/go-scratch/TDFLite/` and added one `_test.go` file in package
  `kas` there, so the harness can call unexported functions; built with the vendored
  dependencies, offline. The read-only source copy is untouched (`git status` clean).
  Why: a `replace` directive cannot reach unexported or `internal/` code. Undo:
  `rm -rf private/tdflite-pilot/go-scratch`.
- **Go's Unicode case tables.** What: dumped `unicode.ToLower/ToUpper/SimpleFold` from
  the installed Go 1.26.0 into a generated Lean file instead of using Lean's ASCII-only
  case functions. Why: the Go code lowercases arbitrary strings, and "strings stay
  strings" was a requirement. Undo: regenerate or delete `TdfModel/CaseTable.lean`.
- **Scope beyond the minimum.** What: also modelled the vocabulary part of bundle
  validation (compared by error count) and the snapshot package's two-phase core that
  has no production caller. Why: later theorem statements will likely need "the policy
  passed validation" as a hypothesis and a view of every decision path in the package.
  Undo: ignore `TdfModel/Validate.lean` and the `core` outputs.
- **Build route.** What: built the model with plain `lake build` inside
  `private/tdflite-pilot/lean` (never in the repo root or `corpora/`, no `lake update`,
  no pin edits). Why: the project imports no Mathlib, so the warm-server rule in
  AGENTS.md (which exists to avoid Mathlib cold starts) has nothing to save here.
  Undo: n/a.
- **Data retention.** What: kept the main-seed cases, both result files and every
  comparison summary (about 42 MB); deleted the per-seed and exhaustive case files
  after each run. Why: they are regenerable from the recorded seeds. Undo:
  `private/tdflite-pilot/scripts/run_all.sh`.
- **Blindness.** What: did not open `tdflite-ideas/`, `docs/`, `README.md`, `TODO.md`,
  `slice/`, `out/`, this file (append only), or any design note / ADR / issue file in
  the TDFLite source; read Go code and code comments only. File NAMES in the TDFLite
  root and two path names in this repo's `.gitignore` were visible in listings.

## maths: definition-centred outline

Builder: model agent, 2026-11-10 (owner offline). Output: `out/corpus/outline2/` (`OUTLINE2.md`, `outline2.json`, `METHOD.md`, `metrics.json`, `rating_items.json`, `lean/`), `bench/outline2.py`, `corpora/outline2/` (`Outline2.lean`, `run.sh`, `build/`). Nothing else was written; `corpora/ns` was read only (the helper opens its `.olean` files; nothing was built or changed there). No ratings were made.

- **Installs: none.** The Lean helper is compiled with the corpus's own toolchain (4.34.0-rc2, already installed) into `corpora/outline2/build/` (172 MB). Undo: `rm -rf corpora/outline2 out/corpus/outline2 bench/outline2.py`.
- **Lean is cold-started 8 times per full run** (one `heads` pass, seven `print` passes of 15 to 25 s), in batch, not in an iterative loop. The warm daemons named in `AGENTS.md` rule 1 do not exist in this repository; same reading of the rule as the earlier exporters.
- **What counts as a concept**: structures, inductive types and Prop-valued definitions. Type-valued definitions are treated as notation and printed in a glossary, never as chapters. Without this the carriers (`Plane`, `Space`) win every round.
- **Region of a concept** = what its producers dominate, plus its consumers' own proofs. "Producer" looks through `Nonempty`, `∃`, `∧`, subtypes, products and `¬` in the conclusion; this is read from `Expr` in Lean, not from text.
- **Selection is a greedy "balanced split"**, 14 rounds: gain = newly covered mass plus the smaller side of each cut of an existing cell. Chosen over plain marginal coverage because the heavy regions are nested (profile, witness, certificate, profile data all sit on one 21.5% region) and plain coverage would keep one of them and then pick consumers only. Consequence: three chapters with about 27% regions each remain.
- **14 concept chapters, 4 statements each, plus a goal chapter and the closing chain**; 3 supporting definitions per chapter (6 for the goal). These were fixed after looking at the structure of the graph and before `bench/paper_truth.py` was run on the result. There is no version control here, so this rests on my word; after the scores were seen only reporting fields were added (the uncut figure, the export-length median, `textStatementOnly`), and the selection Lean printed before scoring is the one on disk.
- **Order is foundations first** (dependency height of the constructing statement), with the goal printed as chapter 0. The task allowed either direction; this one lets each chapter use only what precedes it.
- **A statement is shown under one chapter only**, the later one in dependency order.
- **Consumers are ranked by proof mass beneath them, with no length filter.** This keeps the rule free of readability judgements; the cost is long statements, 15 of 58 and 28 of 57 cut for display.
- **Display cuts**: field types at 300 characters, defining clauses at 700, statements at 900; full text is in `outline2.json`. A definition or statement that is cut does not count as self-contained. The uncut figure is reported beside the strict one (Navier-Stokes 44.0% against 28.0%, Euler 7.0% against 0.35%).
- **"Self-contained after one level of unfolding" is my operational definition**: every project definition visible in the printed statement is printed in full in the outline. The old outline scores 0% on it because it prints no definitions; its earlier "about 10%" was a hand rating. The two are reported side by side and not as a like-for-like gain.
- **"Visible" is a token test on Lean's printed text** (last name component present), applied to the constants Lean reports for the expression. This is a filter on Lean output, not a parse of source.
- **Euler root**: `exists_compact_smooth_euler_singularity`, to match the baselines in `out/corpus/papers/`. The old `OUTLINE.md` printed the other Euler root in full; `outline.json` has both.
- **Rating items**: 15 per outline per paper by `random.Random(20261110)` from all eligible entries, then shuffled by the same generator. New entries are shown with their chapter context because that is what a reader sees; this makes the two sources distinguishable by format, which is stated in the file. Old entries are the name, kind and statement trimmed as `OUTLINE.md` prints them, without mass figures or the hand ratings.
- **Results reported as found**: Navier-Stokes 12 of 85 paper items exactly (old 8) but a tie at depth 50; 28.0% of proof mass beneath self-contained statements; Euler 7 of 31 (old 4), 0.35% self-contained, median statement 863 characters. The Euler outline is not readable.

## tdflite pilot (blind)

Part 2 (T1a): testing the eight plain-English guarantees against the Lean model. Entries carry
no behavioural detail; all detail is in the git-ignored `private/tdflite-pilot/`.

- **Search written in core Lean with `StdGen`, not Plausible.** What: a `gsearch` executable
  (bounded-exhaustive + seeded random tiers, own shrinker) next to the model. Why: the model
  has no dependencies and adding Plausible would need a manifest change (`lake update` is off
  limits). Undo: delete `private/tdflite-pilot/lean/{Search.lean,TdfProps*,TdfProofs*}` and
  restore `lakefile.toml` from `lakefile.toml.part1`.
- **Extended part 1's `lakefile.toml` instead of creating a second Lake package.** What: three
  targets appended (`TdfProps`, `gsearch`, `TdfProofs`); part 1's file kept as
  `lakefile.toml.part1`. Why: one build tree, no path dependency, no new manifest. Undo: copy
  the backup over `lakefile.toml`.
- **Search space and generators fixed in `SEARCH.md` before any property result was read.**
  What: generators derived from the shape of the model's input types; one smoke run was used
  for crash/timing checks and only its input and permit tallies were read. Why: the task
  requires the space not to be tuned afterwards. Anything changed after results is recorded in
  `SEARCH.md` §6 and in the report.
- **Each violated reading is reported in the most restricted input class in which it is
  violated** (any policy / policy that passes the modelled `Validate` / validated policy with
  token-shaped claims). Why: lets the owner see whether a counterexample needs an input the
  loader would refuse. Undo: n/a (reporting choice; all counts are in `data/search-summary.tsv`).
- **Readings are described, never classified as defect or intended.** Why: owner's stance for
  this pilot (report, do not gate).
- **Counterexamples replayed on the real Go through part 1's harness in the scratch copy**
  (`go-scratch/TDFLite`), plus one extra `_test.go` helper for a case part 1's harness
  deliberately does not compare. The read-only source copy was not modified.
- **Plain `lake build` inside `private/tdflite-pilot/lean`** (no Mathlib there, so the warm-server
  rule in AGENTS.md has nothing to save); never built in the repo root or `corpora/`, no
  `lake update`, no pin edits. Search processes were run with `nice -n 5` because the machine
  was heavily loaded by other agents.
- **No system-level installs.**

## K3 translation census

- **hax installed as a third column** (it took one download): `cargo-hax` 0.5.0 from the GitHub release (sha256 `e6bbfd54c32de83638ac3570cc7eeb5cbb64ab07bbff0b27e634e6c010a67101`) unpacked into `census/.tools/hax/`; nothing put on `PATH`. **System-level side effect:** on first use it downloaded its own Charon (nightly-2026.10.31) and Aeneas (build-2b9e3ea) into `~/.cache/hax` (0.6 GB). It needs the Rust nightly already installed. The GitHub repository `cryspen/hax` now redirects to another owner; the binary was taken from the redirected release page as is. Reported at crate level only, and its generated Lake project was not built (that needs `lake update`). Undo: `rm -rf ~/.cache/hax census/.tools/hax`.
- **cedar-policy-core: Charon itself fails** (49 rustc internal compiler errors raised by Charon's new type-annotation recovery, then a panic, no LLBC). To get per-function data the functions containing those 49 sites are marked `#[charon::opaque]` in a copy of the source (`census/work/run/cedar-policy-core/src`, never in `census/crates/`) and counted as failed at Charon. Why not "evaluator/authorizer modules only", which the task allowed: `--start-from crate::authorizer` still hits 3 of the sites, and marking keeps the whole crate in the census.
- **On cedar only, the trait methods that make Aeneas abort are removed up front from their signatures** (trait-type constraint; generic associated type; `dyn` or function pointer in a method of a local trait) instead of one Aeneas run each: one run on its 1.5 GB LLBC takes many minutes. The prediction was checked against the one-at-a-time procedure on the other crates: same removals on all nine, except that it would also have removed `core::error::Error::source` on `time`, which Aeneas tolerates because the trait is modelled in its library; so the `dyn`/function-pointer prediction skips the 49 traits the library models. Remaining aborts on cedar are peeled one at a time as elsewhere. The cedar run was restarted three times while this was worked out (about an hour of machine time).
- **A function that Lean compiles only "using sorry" is counted as failed.** When a type declaration fails, Lean recovers by putting `sorry` in it, and every definition that mentions the type then compiles with a warning instead of an error. The first tables missed this and overstated indexmap and untrusted. The root cause is traced to the failed declaration.
- **A function passed by name is not charged for its wrapper.** rustc makes an `impl FnOnce for <fn item>` shim with the span of the wrapped function; Aeneas often cannot translate it. The failure is charged to the function that passes it, not to the function passed.
- **Unused closure variants are ignored**: Aeneas emits only the `Fn`/`FnMut`/`FnOnce` method of a closure that is called; the absent ones do not count against the function.
- **Failure classes are assigned by message and by the Aeneas source line that raised it** (`aeneas -print-error-emitters`), not by reading each function. Three anonymous messages ("Invalid inputs for binop", "Improperly typed constant value", "Unreachable" in the cast printer) are classed as floating point after checking that every occurrence in the corpus is on `f32`/`f64`.
- **A probe crate backs the profile** (`census/probes/profile-probes-0.1.0`, about 190 tiny functions in before/after pairs, run through the same pipeline). Why: the census shows correlations (functions with a `for` loop fail more often), a probe isolates the idiom. The owner's stance on toy examples is kept by labelling which evidence is which in `PROFILE.md`; no rate is computed from probes.
- **Side run with `aeneas -filter-trait-methods`** (an existing flag that removes most "not a field of structure" errors in user impls of `Iterator`), reported next to the default-flag numbers, not instead of them.
- **What is left for git and what is not.** Git-ignored because large and regenerable by `census/rerun.sh`: the generated Lean (`census/lean-pinned/Generated/`), the flattened `data/functions.jsonl`, and the full per-function results of the side runs (`data/rewrites/`, `data/flags/`; their summaries `data/rewrites.json`, `data/probes.json`, `data/tables.json` are kept, and the three documents regenerate from the kept files alone). Not ignored: scripts, templates, patches, probe crates, documents and `data/results/` (about 22 MB, of which cedar is 15 MB). Nothing was staged, committed or pushed by this node.

## maths: dead code

### plan node M4 (2026-11-10, `bench/deadcode.py`, `out/corpus/deadcode/DEADCODE.md`, working copy `corpora/ns_trim/`)

- **No installs. `corpora/ns` was not modified or rebuilt** (`git status` there is clean; nothing under its `.lake` is newer than this run). The working copy is `corpora/ns_trim/work`: sources copied, `.lake/packages` a symlink to `corpora/ns/.lake/packages`, and the project's own `.lake/build` an APFS clone (`cp -c`) of the original build, so Lake replayed the unchanged build instead of spending 20 minutes on a first build. `lake build --no-build` was run first to confirm Lake would touch nothing in the shared packages. `/corpora/ns_trim/` added to `.gitignore`. Undo: `rm -rf corpora/ns_trim out/corpus/deadcode bench/deadcode.py` and drop the `.gitignore` line.
- **"Unused" is defined on two graphs, both from Lean.** Term dependencies from `decls.jsonl`, plus the references the elaborator resolved in the source, read from the `.ilean` files of the existing build (each use of a constant with the declaration that contains it). The second graph was added because the first cannot see a lemma named in `simp only [...]` whose use leaves no trace in the proof term. Attribute text (`@[simp]`, `abbrev`, `instance`) is read from the source inside Lean's declaration ranges and cross-checked against the environment by `corpora/ns_trim/attrs/Attrs.lean` (simp set 1,264 = 1,264; reducible 901 against 900).
- **"Classified dead" excludes three groups, reported separately and not deleted in the main run:** 176 lemmas named in the source of a reachable proof but absent from its term; unreachable declarations carrying `@[simp]`, being an instance or an `abbrev`, or named by a `variable` / `export` / `open` command of a file that stays; and whatever those need. 13,625 of the 15,435 unreachable declarations are left as dead.
- **Stage 2 sample is drawn from all unreachable theorems, not only from the dead class**, so that it tests the term graph and the exclusions at once. Every declaration that depends on a sampled one is deleted with it (otherwise the build breaks for an uninteresting reason), which makes the deletion 4,992 declarations for 300 sampled.
- **Broken deletions are restored one build at a time from the observed error, not from the prediction**, so the report can say the prediction was 7 of 7. Cost: five builds for stage 2 instead of two.
- **Deleting a module rewrites imports**: an importer gets the deleted module's own imports in its place (recursively), so no file loses a transitive import. The two root files are left alone unless one of their imports is deleted.
- **One kind of edit goes beyond deleting declarations: `open X` is trimmed when nothing left declares namespace `X`.** Without it five files failed with "unknown namespace" in stage 2. 17 `open` commands are edited in the full deletion. Listed in the report as a hidden dependency of its own kind.
- **Relative to the four headline theorems means the paper-form results go too.** The root files also import 34 modules of results stated in the papers' own form (local theorem, appendix lemmas, `Euler.EulerSingularity`); 27 of them are deleted in the full run. The report gives the count that serves them (1,365 declarations) so a reader who wants them can keep them. That variant was not compiled.
- **Negative control is 20 single-declaration deletions, each built at the nearest dependent module.** One of the 20 (a private local instance used by 9 declarations) built anyway; reported as a finding about instance shortcuts, not hidden.
- **Not done: deleting the held classes (a "stage 4").** Each round rebuilds most of the corpus and the machine ran at load 70–190 (the full-deletion build took 45 minutes). The sample gives the estimate instead: 496 held declarations were deleted in stage 2 and one broke the build.
- **Build time after trimming is an estimate, not a measurement.** No quiet-machine build was possible. Reported: the measured wall time under load, labelled as such, and two estimates (per-module times normalised by the slowdown of modules whose text did not change; original per-module times scaled by kept lines).
- **The a/b/c rule was revised twice after the 40-item sample had been drawn and read** (what counts as serving a paper-form result; what counts as an orphaned development). Agreement on that sample (39 of 40) is therefore not an independent check, and the reader was the analysing agent, a model proxy, not blind. Stated in the report.
- **`bench/outline.py` was not edited.** `deadcode.py outline` imports it and points its two path globals at a copy of the graph and a separate output directory. Its clustering section depends on Python's string-hash seed, so the comparison is run with `PYTHONHASHSEED=0` on both graphs.
- **Lean was started cold** three times outside Lake: the attribute export (one process, 6.5 minutes under load) and the exporter of `corpora/ns_export` on the trimmed build (six shards). Everything else is `lake build` on module targets. The warm daemons of `AGENTS.md` rule 1 do not exist in this repository.
- **Final state of the working copy:** `corpora/ns_trim/work` holds the trimmed corpus (full deletion applied and built, 2,424 files). `python3 bench/deadcode.py reset` puts the original sources back; stale `.olean` files of the 233 deleted modules remain in its build directory and are harmless.
- **The trimmed build was re-exported with the existing exporter** (`out/corpus/deadcode/trimmed_export/run.sh`, six cold shards, about 25 minutes under load) so that the "after" declaration count and graph come from Lean and not from subtraction. It matches the prediction exactly.

## maths: outline ratings (proxy)

Scorer: model agent, 2026-11-10 (owner offline). Wrote `out/corpus/outline2/ratings/` (six reader files, `READING.md`), `out/corpus/outline2/RATINGS.md`, `out/corpus/outline2/ratings_summary.json`, `bench/outline_ratings.py`. Nothing else touched; no Lean run (the script only counts labels on entries Lean printed earlier).

- **Installs: none.** Uses the numpy already present. Undo: `rm -rf out/corpus/outline2/ratings out/corpus/outline2/RATINGS.md out/corpus/outline2/ratings_summary.json bench/outline_ratings.py`.
- **All six readers are model proxies** and each file says so (`"kind": "proxy"`, `"model"`: opus, sonnet or default). The exact model ids were not passed to me, so only the family name is recorded; "default" is the workflow's default subagent model.
- **Reader file layout** `outline-ratings/1`: one JSON per reader with `reader`, `kind` (proxy or human), `model`, `ratings[{id,label,reason}]`. A human file with `"kind": "human"` is picked up on rerun, may cover a subset of entries, and adds "humans only" and "proxies only" sections. Checked with a dummy human file in the scratchpad, not left in the repo.
- **Intervals**: percentile bootstrap, 10,000 draws, seed 20261110, resampling readers and entries together, entries within the four outline-by-paper strata the sample was drawn from. Entries-only and readers-only intervals are printed beside it for the differences so the source of the width is visible.
- **Readers are treated as a sample of six** although they are two copies each of three models (mean kappa 0.82 within a model, 0.59 across). The intervals therefore understate uncertainty about mathematicians; stated in the report, with a per-model table. I did not cluster the bootstrap by model: three clusters is too few for it to mean anything.
- **Fleiss' kappa is computed on entries every reader rated**; reported for four labels and three collapses (opaque+unreadable merged, milestone against rest, readable against not), overall and per outline.
- **Disagreement ranking**: entropy of the label distribution per entry, plus a flag for entries with readers on both sides of the readable line.
- **Interpretation lives in `ratings/READING.md`**, hand-written and dated, copied into `RATINGS.md` by the script so a rerun does not lose it; it is marked as written against six proxies.
- **Results as found**: milestone 8.3% old, 6.7% new (difference -1.7 points, -15.0 to +11.7). Opaque-or-unreadable 84.4% old, 65.6% new (-18.9, -43.3 to +4.4: unclear). Opaque -66.1 points, unreadable +47.2, technical-step +20.6, each with an interval excluding zero. Kappa 0.78 on the old outline, 0.36 on the new. The net result flips with the model: default -38.3, opus -25.0, sonnet +6.7.
- **Not done**: the statement-only arm and any human rating. One declaration (`initialDatum_no_global_solution`) is in both samples (R22 new, R49 old) because the sampling rule allows it; left in.
- **(part 2, later) Post-hoc additions are labelled as such, not folded into the pre-registered
  plan.** What: after the first results I added one reading, one input class used only to
  split counts, and "canonicalising" steps in the counterexample minimiser; I also fixed a
  defect in my own minimiser and re-ran the random tiers. Why: to separate causes the first
  results had mixed, and to show cleaner counterexamples. Each item is recorded in
  `private/tdflite-pilot/SEARCH.md` §6. Undo: the pre-registered readings and their totals are
  unaffected; ignore the rows named there.
- **(part 2) Bounded-exhaustive tier run once, random tiers run from temporary copies of the
  build tree.** What: the machine was at load 80-100 from other agents, so I let the long tier
  finish on the first build and ran the short tiers from throwaway copies
  (`private/tdflite-pilot/lean-b2..b5`, deleted afterwards). Why: rebuilding the binary in
  place would have disturbed the running processes. Undo: `scripts/run_search.sh` re-runs
  every tier from the one final build.
- **(part 2) `REPORT.md` was NOT written to disk.** What: the task asks for
  `private/tdflite-pilot/REPORT.md`; the harness refused the write ("subagents should return
  findings as text, not write report files"). I did not route around the refusal with another
  tool; the full report text is in the step's structured output instead, and the per-finding
  detail it cites is in `private/tdflite-pilot/data/findings-raw.md` and
  `data/report-tables.md` (both generated by the pipeline scripts). Why: a refused write is a
  control, not an obstacle to engineer past. Undo / follow-up: save the `summary` field of the
  step output as `private/tdflite-pilot/REPORT.md` if a file is wanted.
- **(part 2) Hand-written illustrative cases are kept separate from the search.** What:
  `scripts/gen_illustrative.py` restates some results with an everyday vocabulary; each case is
  checked mechanically against every reading and replayed on the real Go, and counts toward no
  statistic. Why: machine-minimised inputs are short but hard to read.

## K3 translation census

- **Rewrite experiment: the cause was fixed before cedar-policy-core finished.** The five functions were taken from the most common single cause class in the nine crates done at that point (names captured in the generated Lean), one per distinct instance, first affected function in file order. Two more rewrites (loop exits) were added because renames say little about the cost of restructuring. Why not wait: one cedar run takes about an hour here, and re-running cedar once per rewrite was out of reach in any case.
- **Rewrites that needed a second try are reported as such**: the `indexmap` rename first failed the crate's own `unnameable_types` lint; the `rusty-money` loop rewrite first exposed a second Aeneas error. First attempts are described in `census/CENSUS.md` (and `census/rewrites/attempts/`).
- **"The crate's own tests" for `time` are its 448 documentation tests**: `cargo test` on the published `time 0.3.55` does not compile its integration tests even unpatched.

## maths: outline ratings (proxy)

- **Maths step finished (04:50).** Results recorded in `out/corpus/FINDINGS.md` and experiments 14–17. The two reviewers' corrections had not been applied by the run, so I sent one agent to apply them and rerun the generating scripts; headline numbers in my write-up are already the reviewers' corrected ones.
- **Call: model readers are not used as evidence of mathematical quality from here on.** Experiment 16 showed agreement of 0.36 and a verdict that flips by model. They remain useful for mechanical checks.

## tdflite pilot (scoring)

T1b (score the blind pilot against the plan's known edge cases) and T0 (layer census), 2026-11-10,
owner offline. All detail is in the git-ignored `private/tdflite-pilot/score/`; nothing here
describes behaviour. No system-level installs, no `lake update`, no pin edits.

- **Worked only in copies under `private/tdflite-pilot/score/`.** What: rebuilt the pilot's Lean
  model from a source copy (`score/lean`, plain `lake build`, core Lean only, no Mathlib) and ran
  the real Go from a fresh copy of the pristine source (`score/go/TDFLite`), so neither the
  pilot's directories nor the read-only source were touched. Undo: delete `score/lean/.lake` and
  `score/go/TDFLite`.
- **Read the blind agents' own session transcripts for the blindness audit.** What: extracted
  their task prompts and tool-call logs (not their reasoning) into `score/audit/` and scanned
  them for reads of forbidden paths. Why: the audit asks for evidence of what they saw, and the
  transcripts are the only complete record. Undo: delete `score/audit/`.
- **No `SCORE.md`; the scoring record is data.** What: the subagent rules forbid writing report
  `.md` files (part 2's equivalent write was refused by the harness), so the score table, new
  findings, audits and census are in `score/score.json` and four `.tsv` files, generated by
  `score/scripts/build_score.py` from the run outputs. Follow-up: render `SCORE.md` from
  `score.json` if a prose file is wanted.
- **Fidelity audit reuses the pilot's two harness adapters, nothing else.** What: my own case
  generator, seeds and comparator; the pilot's Go test file and Lean runner are reused because
  they are the only route into unexported Go code. Cross-checked by a separate Go test that calls
  the real functions directly, and by three deliberately broken model variants (all detected).
- **A hint-free generator was added to estimate discoverability.** What: a uniform grammar
  generator whose hit rates indicate how often each known case appears without aimed inputs.
  Caveat: I designed it knowing the cases, so it is an estimate, not a blind measurement.
- **The plan's T1b target is reported as a signal, not a verdict.** The measured count is given
  next to the target, with the blindness caveat found in the audit.
- **Census follows where the code makes each choice at commit 4aca7ca.** One item lands in a
  different layer from the sentence in `docs/PLAN.md` T0; the code references are in the
  private record.
- **Deleted the 100,000-case result files after summarising them** (about 150 MB; regenerable
  from seed 554 with `score/scripts/gen_fidelity.py`).

## maths step: review corrections applied

2026-11-10. The two independent reviews of the maths-track outputs (constant threading; paper truth, outline, dead code) listed corrections that nobody had applied. Applied here; no conclusion was changed beyond what the reviewers wrote.

- **`out/corpus/lesssim/LESSSIM.md` (hand edits; `all.sh` not rerun).** Statement source counts corrected like for like (lines 104 → 93, −10.6%, was 111 → 93; tokens 1,427 → 1,428; lexical +5.2%; characters +3.1%; per-row lines for steps 1, 2, 4, 5 from the reviewer's `review/py/source_check.py`); "62 binders → 13" replaced by "the `∃ C, 0 ≤ C ∧` prefix disappears from 12 conclusions" (binding sites about 40 → 42); "11 of 13 conclusions restated", with 8 of 13 native proofs never handling an explicit constant; proof saving given as −2.4% to −4.2% (matchers charged or not); extrapolation restated as "no measured saving outside the family; 0.1% is an optimistic ceiling", break-even marked undefined at the sample's rate; sample: 1 of 7 rule-fits written against the relation; library accounting notes (5,728 adapter nodes, uncredited `weaken_bound`/`add_bounds`, 535 unused nodes, 8:1 pessimistic for a closed cluster); step 4's saving partly a relocation; the other depth-13 heads (one cone contains 8 of the 13, the other none); the two post-measurement `ring` swaps labelled exploratory; `JetRate` "equivalent to `IsBigO` when `q ^ r` is eventually nonnegative". Derived by me from the corrected line count: source lines saved 53 → 46 (35 proof + 11 statement). `tables.md`, `source_measure.json` and `source_measure.py` still carry the docstring slicing bug; fixing the script is a next action, not done here.
- **`out/corpus/papers/`.** `items_ns.py`: `physical_normalCoefficient_class` moved from 9.2 (guess) to 7.7 (probable); `admissible_iff` and `radial_heat_equation` `states` → `part`; B.6 note rewritten. `build_truth.py`: renumbering row "Lemma 9.2" → Lemma 7.7, probable. `TRUTH.md`: the reviewer's four text changes, plus counts that follow (states 120 / part 153, was 122 / 151; Navier-Stokes mappings 193 probable / 13 guess, was 192 / 14; renumbering rows 9 guess, was 10). Reran `build_truth.py` and `paper_truth.py --baselines`.
  - **Call: `build_truth.py` gained `MOVED_AFTER_DRAW`.** Moving the mapping shifts file order, so the guard "verification list does not match the seeded draw" fired. The draw is now reproduced on the order as of the draw (the moved mapping put back at the end of 9.2 for the draw only); the guard still runs and the 20 verified mappings are unchanged. Undo: delete `MOVED_AFTER_DRAW` and its loop. The alternative, re-drawing and re-verifying 20 mappings, would have replaced the builder's verified sample.
  - Headline exact hits unchanged (dominator outline 8 of 85 and 4 of 31). Near hits moved by one in a few cells: `ns_r3` and `ns_periodic` at k=50 50 → 49; own proof size at k=1000 56 → 55 (also 69 → 68, 81 → 80 at k=2000, 5000; 42 → 43 at k=500 in the probable table); random-row near means in the second decimal. `TRUTH.md` and `METHOD.md` cells updated.
- **Outline.** `bench/outline2.py` caption sentence; `METHOD.md`: the Navier-Stokes "reads as a strategy" bullet, the "two cuts that remove the gain" bullet, the trimming paragraph, and the dominator near cell 8 / 50 → 8 / 49 and random near 23.3 → 23.25 from the rerun. `--no-lean` rerun: `outline2.json` and `rating_items.json` byte-identical; `OUTLINE2.md` differs only in the corrected sentence; `metrics.json` in the script hash and three near values. `bench/outline_ratings.py` title and format line, `ratings/READING.md` two sentences; rerun: `ratings_summary.json` byte-identical, `RATINGS.md` differs only in the corrected text.
- **Dead code.** `DEADCODE.md`: re-export differences (42 declarations in `numAux`/`auxProofSize`, one in `extValueByRoot`), "outline does not change on the predicted graph" in the result list and the Outline rerun section, class (b) relabelled "support with no term use" (table, heading, bullet). `bench/deadcode.py`: label in `tables` (rerun, `tables.md` line 121 only); new `compare` subcommand, which regenerated `trimmed_export/compare.json` over every field and reproduces the reviewer's 42 / 40 reachable / 18,689 → 31,196; new `control-reparse`, which rescans the stored control logs with whole messages (control 4 `errorNamesDeclaration` false → true; 19 of 20 failed, unchanged). No Lake build was run and `corpora/ns_trim/work` was not touched.
- **Not applied, with reasons.** (1) The reviewers asked for the same softening in "the outline report summary" and "the M4 summary"; those sentences are in the workflow's returned text, not in any file of the repository, so there was nothing to edit. The nearest in-file sentences were corrected instead. (2) Reviewer next actions (charge matchers to statements in the tables, fix `source_measure.py`, migrate a closed cluster, delete the 244 held declarations in unimported modules) are new work, not corrections. (3) Earlier `DECISIONS.md` entries that repeat the old wording ("11 of 13 re-proved natively", "10 on topic only") were left as written; this entry supersedes them.
- **Installs**: none. Backups of every file as it was before this step are in the session scratchpad only.

## K2 trade map

### the comparison itself (2026-11-10, `slice/compare/`: `TRADES.md`, `PREREG.md`, `harness/`, `arms/`, `results/`)

- **Compared the committed `slice/` at `aa6f42a`, not the working tree.** Why: another agent was restructuring the feature files, glossary and `slicegen` while this ran (uncommitted changes to 80 files), so the working tree was not a fixed thing to measure. `harness/snapshot.sh` extracts the commit with `git archive`; every scratch copy is taken from that snapshot. Consequence: the 23 rules are the scenario outlines as committed, before the `Rule:` restructuring. Undo / redo on a newer tree: `harness/snapshot.sh <commit> && ./rerun.sh`.
- **No git commit was made to freeze the design** (plan rule 1 asks for one). Why: several agents share the working tree and index, and the owner asked for no commits. Instead `harness/freeze.py` wrote sha256 digests of the arms, bounds, rules and mutant lists to `results/frozen.json` before the first mutant was run; `--check` shows they have not changed since.
- **"The same rules" = the 23 Scenario Outlines expected to be proved for all inputs** (7 wallet, 16 ledger). Literal-value scenarios and the deliberately false ones are not rules; a literal scenario failing is reported in its own column and never counted as detection by arm (a). The KIND of each rule was assigned by me from its English before any result (`rules.json`); progress and bound have one rule each and are labelled as single cases.
- **Property-based arm: two generator profiles, both always reported.** `plain` (uniform over the range the Givens allow) is the registered reading of "written directly from the English rule"; `edge` adds 6 lines that put half of the draws within 3 of an end of the range. Why both: the choice decides whether boundary mutants are caught (45 against 50 of the 52 tool mutants), and reporting one would hide that. Collections have 0 to 6 elements; I chose 6 knowing two reviewer mutants need a fourth element, and say so.
- **Arms (a) and (b) run debug builds** (overflow and index checks on). Why: the Lean model treats overflow and out-of-range indexing as failure, so a release build would compare different semantics.
- **Kani bounds were set by one rule on the unmutated code** (largest size that verifies in about a minute): 4 accounts and 3 transfers; 2 and 2 for the rules that compare a total; 3 accounts for `transfer_valid_moves`; 1 transfer per batch for `two_batches_conserve`. The small bounds for totals are a measured solver limit, reported as a result, not a convenience.
- **Tried and dropped: an SMT back end for Kani.** `z3-solver` (4.13 and 5.4) was installed with pip into a virtualenv under `slice/compare/work/solvers-venv` (not system-level); CBMC 6.11's SMT conversion crashed with `map::at: key not found` on these harnesses with both. Undo: `rm -rf slice/compare/work/solvers-venv`.
- **Added a differential oracle that the task did not ask for** (`arms/diff`: original against mutant on about 2.4 million inputs). Why: "equivalent" and "behaviour no rule constrains" cannot be told apart from the arms' silence. It is not an arm and detects nothing by itself.
- **cargo-mutants was used only to generate mutants** (`--list --json --diff`); its own test loop was not run. Viability was decided by `cargo build` of the mutated crate. All 52 build.
- **Lean-arm detection was split three ways and a lost proof never counts by itself:** shown false by the pipeline's own search; proof lost and confirmed false (another arm's input, or a hand-written one, replayed as an extra Examples row on the Lean model and the compiled Rust: `harness/confirm.py`); proof lost, not shown false. Three further calls made when the data showed the need: a failing Examples row on the model counts as "shown false" although the pipeline does not change its verdict for it; a mutant whose generated model does not build (`cm-l26`) is "no model", not detection; where the pipeline crashes evaluating a non-terminating model (`cm-l14`, `cm-l34`), confirmation on the compiled Rust alone is accepted and labelled as such.
- **Ten hand-written falsifying inputs** (`mutants/hand-witnesses.json`: 2 for `cm-l14`, 8 for `cm-l34`, the two mutants whose loop stops terminating): rows and proptest report these rules only as hangs, which have no shrunk input, and the input Kani reports for an unwinding failure need not loop for ever. Written from the diff, labelled as hand-written wherever they are used, and confirmed on the compiled Rust only.
- **Kani timeouts were retried once, alone, with 900 s** (`harness/kani_retry.py`): three harnesses, all on `cm-l34`; two then failed, one still timed out. The tables use the retried results and keep the first attempt.
- **`results/raw/` was trimmed** (`harness/trim.py`): per-mutant JSON kept whole; of the pipeline's own logs only `proofs.json`, `search.json` and the last 150 lines of `run.log` (139 MB down to 11 MB; two non-terminating models alone wrote 900,000-line stack traces).
- **Kani unwinding-assertion failures count as detection, as registered,** and the two pairs that rest on one alone are named in `TRADES.md`.
- **The run was not delayed for a quiet machine.** Load average was 40 to 110 on 18 cores from other agents. Timings are reported as measured, with quieter measurements beside them where I had them; no detection result depends on a timeout.
- **`harness/run.py` was restarted once mid-run** to move 27 queued mutants off a worker waiting on a hanging mutant (`cm-l34`, about an hour by itself). Nine runs in flight were repeated; nothing else was discarded.
- **Not done, and said so in `TRADES.md`:** bugs transplanted from real fix commits (named in the plan, not in this task; the crates have no fix history); re-proving the lost-but-true proofs; timings on an idle machine.
- **Undo for the whole node:** `rm -rf slice/compare` plus the uninstall line above. Nothing outside `slice/compare/` and this file was written; `slice/` itself, the pins and both Lake manifests are untouched.

## K3 translation census

- **cedar: the two LALRPOP grammar modules are made opaque for Charon** (`--opaque crate::parser::text_to_cst::grammar --opaque crate::validator::cedar_schema::parser::grammar`, recorded in `census/data/overrides.json`). They are generated into `OUT_DIR` at build time, are not source functions (not in the inventory), and hold several thousand generated parser functions; with them one Aeneas run on cedar was still going after about 50 minutes and 60 GB of memory. Trade: functions that call into the parser see an opaque callee. This is the fourth restart of cedar.
- **cedar: an uncaught OCaml exception inside one function body also aborts the crate** (`Failure("ty_regions shouldn't be called on erased or body regions")`, raised in the symbolic interpreter; no source location). The driver finds the function by bisection: all local bodies opaque, bodies restored for one subset at a time, eight Aeneas runs in parallel per split, until single functions reproduce the exception. Each such body is then made opaque (signature kept) and the function is counted as failed at Aeneas with the exception as the cause. A first attempt that guessed from a trace of the functions started last was wrong (the exception came back) and was dropped.

## K2 trade map

### after the measured run (2026-11-10, `slice/compare/`)

- **Costs on the unmutated code were measured a second time, alone.** Why: one mutant rerun by itself gave the identical outcome in 82 s against 514 s inside the main run, so the first cost figures were mostly machine load. `results/raw/baseline.json` is now the run alone; the first is kept as `results/baseline.under-load.json`, and the cost table prints both. The per-mutant times in `TRADES.md` section 2 are still the loaded ones and are labelled so.
- **Added an exploratory probe of Kani's bounds, clearly outside the registered comparison** (`harness/kani_probe.sh`, `harness/kani_probe_mutants.py`, `results/kani_bounds_probe.*`). Why: the alone timings showed the bounds I had registered under load were far lower than Kani needed for rules without a total, and I did not want the report to present "beyond Kani's bound" misses as a limit of the tool. Result: each size-bound miss is found in 3 to 5 s at another bound; showing that a total rule holds at 3 accounts and 2 transfers takes 9 minutes. The registered figures were NOT changed; the probe is reported next to them.
- **Scratch copies were deleted at the end** (about 30 GB under `slice/compare/work/`); only `work/snapshot` (8 MB) remains. `./rerun.sh` recreates what it needs.

## K3 translation census

- **A third way one declaration loses most of a crate: mixed declaration groups.** Aeneas's function analysis stops at the first declaration group that mixes functions with types or trait impls; every function later in the declaration order then fails with "Internal error". On cedar that was 2,151 source functions (counts before the fix kept in `census/data/cedar_before_mixed_group_fix.summary.json`). Moving such groups to the end of the order (emulating "skip the group and go on") was tried on cedar and then **left out of the reported numbers**: with it, Aeneas translates far more of cedar (about 1,559 of 2,503 counted functions log no error, against 37) but then dies in a pure micro-pass with uncaught exceptions spread over many functions (6 of 8 bisection chunks), and the search for them was not going to finish in the time left. The step is in `census/scripts/census.py` behind `CENSUS_MOVE_MIXED=1`. Reported cedar figures are therefore the run without it; the Aeneas-stage bound from the incomplete runs is in `census/data/cedar_before_mixed_group_fix.summary.json`. `rust_decimal` has one such group, fifth from the end of its order (4 functions affected), and is likewise reported without the move.
- **When a trait is removed in the peel, everything declared under its impls is removed with it** (methods, their closures), and those methods are counted as failed with the trait as the cause. Why: Aeneas cannot print the name of an item nested in an impl that is gone and dies in extraction. Trade: this removes more than the real fix would (the fix would drop only the methods whose signature fails), so cedar's peeled figure is on the low side.
- **The six bisected crash functions are kept in `census/data/crash_cache/cedar-policy-core.json`** so that a rerun does not repeat the search (129 Aeneas runs). The file also holds call sites used only by the mixed-group experiment.
- **Mistake to know about (06:57 local):** one `pkill -f 'aeneas -backend lean'` of mine was not restricted to `census/` paths. Any Aeneas process another agent had running at that moment on this machine was killed with mine (the slice's mutation and comparison jobs start short Aeneas runs). All my other kills were path-restricted. If a slice job reports an Aeneas failure around 06:57, rerun it.
- **Machine load.** For most of the night the load average was 50–120 on 18 cores (other agents' Lean builds plus these runs). Timings in `census/CENSUS.md` are order-of-magnitude only, and cedar's long runs were stretched by it.

## K2 trade map

### independent review of TRADES.md (2026-11-10, `slice/compare/review/`)

- **Wrote only under `slice/compare/review/` and appended this section.** Nothing else in `slice/compare/` or `slice/` was changed; `harness/freeze.py --check` still passes. `review/.gitignore` ignores `review/work/` (scratch copies, about 11 GB during the run, deleted at the end). Undo: `rm -rf slice/compare/review` and delete this section.
- **Snapshot taken independently** with `git archive aa6f42a slice` into `review/work/snapshot`, not the builder's `work/snapshot`; the two trees are identical except two reporting scripts of the harness. The arms were copied from `compare/arms` (digests match `results/frozen.json`).
- **Random sample of 15 mutants, seed 4417** (picked before the draw): `random.Random(4417).sample(ids, 15)` over all 97 ids of both mutant sets in file order, not stratified; recorded in `review/sample.json`. The draw included `cm-l34` (non-terminating, the slowest mutant) and two Kani size-bound misses (`hand-lt2`, `hand-r1`); kept as drawn. The unmutated baseline was rerun too.
- **The rerun reuses the builder's harness** (`harness/run.py`, same arms, same proptest seed) copied to `review/harness/` with only its paths changed. So it tests that the results REPRODUCE, not that the harness logic is right. The independent check of the logic is `review/recompute.py`, written from PREREG.md's definition of detection without importing `harness/analyse.py`. Confirmation by replay and the Kani retries were not rerun; the builder's confirm records are applied to both sides.
- **"The rule calls the mutated function"** is decided from the static call graph of the two crates (`apply_all` -> `apply_batch` -> `apply`; `batch_then_total*` -> `apply_batch` and `total`) and the function each mutant names. Used only to split the "still proved" pairs (`review/still_proved_reached.json`).
- **PREREG.md read strictly for the Lean arm's "confirmed"**: it asks for an input found by another arm and replayed on the Lean model and the compiled Rust. Under that reading the tool-set Lean figure is 47 of 52 mutants (not 49) and 191 of 212 pairs (not 203). Both readings are reported; the builder's added rule is labelled, not called wrong.
- **Ran an exploratory Kani ladder** (`review/kani_ladder.py`, results in `review/kani_ladder.json`): one fixed pair of shapes for the total rules (4 accounts x 1 transfer; 2 accounts x 3 transfers) and 6 x 4 for the others, on all 10 pairs the registered bounds missed and on the unmutated code. Shapes chosen by me KNOWING the mutants (4 accounts because `r2` sums three; 3 transfers because `r5` acts in the third iteration), so not blind; run under load 50 to 70.
- **No review document written as Markdown**: findings and corrections (with replacement text) go in this node's structured output; scripts and data are in `review/`.

## K3 translation census

- **cedar's dominant failure was reproduced in a 100-line probe crate** (`census/probes/mixed-group-probe-0.1.0`: two types whose `Display` impls format each other) together with its rewrite (`mixed-group-fixed-probe-0.1.0`: recursion in inherent methods, trait impls forward). Why: it turns "2,210 cedar functions fail with Internal error" into something that can be attached to an upstream issue and into a rule authors can follow (profile rule 0). The rewrite was not tried on cedar itself.
- **Idiom-rate tables leave cedar out** (CENSUS.md "How functions with a given idiom fare", and the "N of M functions containing … compile" figures in PROFILE.md): nearly all cedar functions fail for a cause unrelated to their content, which would drown every idiom's rate. Cause-class counts and all headline tables include cedar.
- **Four extra rewrites beyond the five asked for** (two loop-exit, two function-passed-by-name), because the five for the most common rewritable cause are renames and say little about the cost of changing code. They are labelled as extras.
- **Reran the builder's Kani retry step for `cm-l34` only** (`review/harness/kani_retry.py --only cm-l34`, 900 s), because the 180 s outcome of two of its harnesses differed between the two runs (load); after the retry both runs agree. Trimmed the review's two 930,000-line logs of `cm-l34` to their last 150 lines (`review/results/raw/lean/cm-l34/`). Scratch copies under `review/work/` deleted; only the 8 MB snapshot remains.

## K2 trade map: review corrections applied

- **Applied all 24 corrections of the independent review to `slice/compare/TRADES.template.md` and regenerated `TRADES.md`** with `harness/report.py` (2026-11-10). No number in a generated table changed; only prose. `harness/freeze.py --check` still passes. Nothing outside `slice/compare/` was touched except this entry; `slice/run.sh` was not run.
- **Every quoted original matched the template** (modulo its hard line breaks), so the reviewer's replacement text went in verbatim, with two exceptions where I changed wording to say what the data says: (a) In short 5, "On the hand-written set: 23 surviving pairs, all wallet" became "23 of the 336 surviving pairs are of a rule that calls the mutated function, all on the wallet" (336 proofs survive there; 23 is the reached subset); (b) section 8, "one fixed pair of shapes ... found every pair the registered bounds missed" now also names the 6 x 4 shape used for the progress rule (`r1`) and says no single shape found them all, as `review/kani_ladder.json` shows.
- **Five edits beyond the list, same intent** (Kani-bounded results labelled as bounded; the ladder): "lost-but-true" in section 9 and next action 5 became "lost proofs whose rule no arm shows false"; next action 4 cites the review ladder and that its shapes were not blind; next action 3 says 10 of the 12 Rust-only confirmations used hand-written inputs that PREREG.md does not count; the header says a review was applied and where its scripts are.
- **Generated tables left as they are.** The Lean column of the detection tables still shows the credited figures (49 mutants, 203 pairs); the strict reading (47 of 52, 191 of 212) is given in prose beside each table instead of changing `harness/analyse.py`. Trade: one reading in the tables, two in the text. Undo: restore the template from the `>` lines' counterpart in a diff against the previous TRADES.md; no data file changed.
- **Spot-checked before applying:** the 188 / 15 / 92 and 90 / 7 / 125 splits, 8 and 23 reached still-proved pairs, 124 ledger + 1 wallet lost-not-shown-false on the hand set, 18 still-proved pairs under `cm-l14`/`cm-l34`, and the ladder times, against `results/results.json`, `review/still_proved_reached.json` and `review/kani_ladder.json`. The "396 of 404 never call the mutated function" split rests on the reviewer's static call graph and was not re-derived.

## plan step 1 finished (2026-11-10, about 07:30)

- **Wrote up experiments 18–22** in `docs/EXPERIMENTS.md`, README and `slice/FINDINGS.md`. TDFLite results are public as counts only; the detail and a summary for the owner are in `private/tdflite-pilot/` (`OWNER_SUMMARY.md`, `REPORT.md`).
- **Call: "blind" is reported as "guided".** The pilot agents never opened the owner's plan, but my task text listed the kinds of awkward input to generate and that list points at all six known cases. Recorded as a limit of the result, not hidden.
- **Two report files were refused by the harness** (the pilot's `REPORT.md` and the scorer's `SCORE.md`); I saved the first from the agent's returned text and assembled the owner summary from the scorer's tables.
- **A census agent's broad `pkill` at about 06:57 may have killed another agent's Aeneas run.** I re-ran `slice/run.sh` afterwards: all 35 scenarios get their expected verdict.
- **Launched plan step 2**: frame library with echo-back and kernel-checked equivalence to the old statements; agent-written loop proofs on a new crate with rules by a separate author, two model arms; an Aeneas fork spike patching the three census defects (text for upstream prepared, nothing sent); TDFLite rulings as parameters with a worksheet for the owner (private). These may still be running at 10:00.
- **Call: installing OCaml (opam) for the fork spike is allowed** and will be logged by that agent with its undo.

## P2 base (author)

- **Copied `slice/` to `p2/base/` at 07:37 EST and never read `slice/` again.** Left out `out/`, `compare/`, `review/`, mutation logs, `build/`, Cargo `target/` dirs and `lean/.lake/build`. Then removed the wallet and ledger crates, their features, glossary entries, Vocab files, proofs, `Ledger/Lemmas/`, generated files, `probe/`, `FINDINGS.md`, the mutation harness and results, and the schema's maths example and selftest. Undo: `rm -rf p2/`.
- **Symlinked, did not copy, the two big caches**, as the task said: `p2/base/.tools` -> `slice/.tools` and `p2/base/lean/.lake/packages` -> `slice/lean/.lake/packages`, as absolute links so working copies made elsewhere also resolve. Trade: no extra 7.9 GB, but if the agent restructuring `slice/` moves or rebuilds those two directories, every P2 copy breaks or shares the rebuild. Fix then: point the two links at the new place (`ln -sfn`). Nothing in P2 writes to them: `lake build` replayed every dependency.
- **Pipeline changes beyond deleting** (all in `p2/base`, `slice/` untouched): the Lean library `Wallet` (statements, checks, proofs) is renamed `Spec`; glossary definitions go in library `Vocab`; an empty library `Lemmas` (with a README, because Lake fails on a missing directory) is for the proof writers' helper lemmas. The crate list moved into `crates.txt`, read by `translate.sh`, `run.sh`, `slicegen` and `effort/count.py`. `wallet-bdd/` is now `bdd/` (package `scenario-bdd`). Report prose and paths that named the wallet or ledger were made generic, and the ledger-specific "not checked" paragraphs were replaced by one about reference definitions. For an empty project, the generated statements file imports `Aeneas` when the glossary imports nothing, and an empty `crates.txt` is tolerated. Why: so a reader of the P2 report is not sent to files that do not exist, and so the pipeline runs with no crate (checked: exit 0, 0 scenarios). Checked that the renamed proof bookkeeping still works, in a throwaway copy, with a dummy straight-line function: its scenario became PROVED-FOR-ALL through a proof importing a `Lemmas` module, and breaking that module cost only that proof. The copy was deleted.
- **Domain: an inventory allocator** (warehouse of bins `Vec<Bin>`, each bin `product: u32, qty: u64`). Why: it gives seven natural loops whose exact results have short, readable statements (sums, first match, pointwise update, greedy take, a fold over orders, a distinct count, a majority). A token bucket would have put time in the state; a scheduler over fixed queues would have needed `Vec<Vec<_>>` literals the generator cannot write yet. Crate `p2/base/inventory/`: 161 lines (128 code lines), 9 unit tests, translates with the pinned Charon/Aeneas under `-warnings-as-errors`, including the nested loop.
- **The seven loop functions and the category each was written for**: `stock_of` simple accumulation (`checked_add`, early `return None`); `find_bin` search with early exit; `restock` in-place update of the collection (`saturating_add`); `take` in-place greedy update with a two-part loop condition (medium); `fill_orders` a loop calling `stock_of` (through the private `can_fill`) and `take`, both of which loop; `product_count` a nested loop; `dominant_product` the loop whose correctness needs a non-obvious invariant (a single pass that picks a candidate, then a counting pass). Labels kept out of `TASK.md`; nothing in the task's files names the algorithm or an invariant.
- **Name clash, harmless**: cucumber depends on a crates.io crate also called `inventory` (0.3.25). Cargo keeps the two apart (both appear in `bdd/Cargo.lock`) and everything builds. Renaming the crate would have avoided the confusion at the cost of re-doing the glossary names. Not done.
- **Rules and scenarios**: one `Rule:` per function, 16 universal Scenario Outlines (2 to 3 per function), 46 example rows; every function has at least one exact-result scenario. **Reference definitions in the vocabulary**, written to state exact results and listed at the top of `lean/Vocab/Inventory.lean`: `stockIn`/`stock` (sum of a product's units, unbounded), `takeFrom` (greedy take on (product, units) pairs, structural recursion), `fillFrom` (orders in turn, using the other two). The other exact results use plain definitions: the first index satisfying a predicate, a pointwise `map` with `min (u + a) U64.max`, a `filter` length, and `toFinset.card`. Trade: the scenarios for `take` and `fill_orders` are only as trustworthy as `takeFrom`/`fillFrom`, which are unsigned like the whole glossary.
- **Two glossary adjustments before freezing**, found by the first full run: `IVocab.binHolds` added to `proof_hints.simp` (without it the generated non-vacuity theorem `find_first_bin.sat` failed, and that scenario could never have become PROVED); "no bin holds ..." restated as the negation of "some bin holds ..." (same meaning; lets the coverage theorem pair the two). After both, all 16 `.sat` theorems kernel-check and no Then follows from its Givens alone. Coverage stays NOT SHOWN for `dominant_product` (its two scenarios have different variable lists; informational, the same limit the ledger's `total` had).
- **Checked the statements are true (testing, not proof)**: 46/46 rows pass on the compiled Rust and on the Lean model; the boundary grid finds no counterexample; the two readings of the 23 Given/Then phrases agree on 20,072 grid points; 1,000,000 random inputs on the compiled Rust (overflow checks on) and 30,000 on the Lean model (interpreter, through the generated checks) found no failure, with every Given exercised both ways. The random-test sources are in the scratchpad, not in `p2/`.
- **Frozen by content hash, not by commit** (I commit nothing): `p2/base/FROZEN.sha256` lists 39 files (Rust, unit tests, feature, glossary, Vocab, `bdd/` readings, the generated model/statements/checks, the pipeline, `TASK.md`, `SCENARIOS.tsv`). sha256 of `FROZEN.sha256` itself: `1ba3568cc64f960873c1ab4cd0443e4d96c735fb733a37256a99a3377e8005d9` (taken after a last cosmetic fix: the report header and a translate.sh comment no longer say `slice/`). A full `./run.sh` in a fresh copy leaves every listed file unchanged (generated files are byte-identical between runs).
- **Calls left to whoever launches the attempts**: the per-attempt budget (tokens, wall-clock), which `TASK.md` says must be written down first; the arm directories (`TASK.md` suggests `p2/<arm>` via `p2/base/workcopy.sh`). **Independence rule in `TASK.md`**: no reading of other copies or of `slice/`. `DESIGN.md`/`TOOLCHAIN.md` stay in the copy, and they describe how the ledger's loops were proved in prose (`loop.spec_decr_nat`, a pure model for exact results). Both arms see the same text; recorded here because it is generic know-how a strict reading of "unaided" might exclude.

## Aeneas fork spike

- **System install: `brew install opam` (opam 2.6.1) and `brew install pkgconf`.** Why: there was no OCaml toolchain on the machine and Aeneas is OCaml; opam asked for `pkgconf` to build `zarith`/`conf-gmp` (`gmp` was already installed). Undo: `brew uninstall opam pkgconf`.
- **opam state is kept out of `~/.opam`.** The opam root is `census/fork/.opam` (`OPAMROOT`, set by `census/fork/env.sh`), one switch `aeneas` with OCaml 5.3.0 and the packages Aeneas and charon-ml list (no `ocamlformat`, no `odoc`). `opam init` was run with `--no-setup`, so no shell profile was edited. Undo: `rm -rf census/fork/.opam`.
- **Side effect in `~/.rustup`, not intended:** running `rustup` inside the Charon clone made rustup read Charon's `rust-toolchain` file and add seven cross-compilation targets to the existing `nightly-2026-09-17` toolchain (`aarch64-unknown-linux-gnu`, `i686-unknown-linux-gnu`, `powerpc64-unknown-linux-gnu`, `riscv64gc-unknown-none-elf`, `x86_64-apple-darwin`, `x86_64-pc-windows-msvc`, `x86_64-unknown-linux-gnu`). Nothing uses them. Undo: `rustup target remove --toolchain nightly-2026-09-17 <each of the seven>`.
- **Everything else is under `census/fork/`** (git-ignored there: the Aeneas and Charon clones, build output, binaries, run directories, Lake projects). The Aeneas clone has its push URL set to an invalid value; nothing was pushed, no issue or pull request was opened.
- **Built at commit `0d21a9ec` (the nightly-2026.11.10 release), as asked, but the generated Lean is compiled against the Lean library of nightly-2026.11.09 on Lean v4.35.0**, the one the census used. Why: the 11.10 library needs Lean v4.36.0-rc2 and a newer Mathlib, which would mean fetching new pins; the only source change between the two commits is three added entries in `src/extract/LeanKeywords.ml`, and the census had already found the two binaries' output identical on all ten crates. Trade: a name that collides with one of those three keywords would be escaped differently; none occurs in the corpus.
- **Charon: built from source at the pin (`454586e9`) for Aeneas's test suite; the census runs use the release's Charon binary of the same commit**, so that the LLBC inputs are the census's inputs byte for byte in origin. Aeneas itself needs only the `charon-ml` OCaml library from that source tree.
- **The census driver is reused unchanged**: `census/fork/scripts/fork_census.py` imports `census/scripts/census.py` and redirects its paths under `census/fork/runs/<variant>-<mode>/`, switches the peel off (no opaque marks, no LLBC surgery, no bisection, one Aeneas run), and compiles in a private Lake project per variant (`census/fork/lean/<variant>`, packages APFS-cloned from `census/lean-pinned`, Aeneas library cloned to `census/fork/backends-pinned`). Nothing under `census/` outside `fork/` is written.
- **Cedar gets a second, labelled mode ("Charon workarounds", `cw`).** Why: as shipped, cedar stops in Charon (the rustc ICE), so no Aeneas patch can change its as-shipped number; that row is reported and stays 0. To see what the Aeneas patches do on cedar, `cw` keeps only the census's Charon-side workarounds (49 functions marked opaque, the two generated parsers opaque) and removes nothing on the Aeneas side. It is reported separately from the as-shipped tables.

## P2 arm fable

2026-11-10, 08:07-08:25 EST. Working copy `p2/arm-fable` (made with `p2/base/workcopy.sh`; `.tools` and
`lean/.lake/packages` are the shared symlinks). Nothing installed, nothing outside that directory written
except this entry. Result: 16 of 16 scenarios PROVED-FOR-ALL, 7 of 7 functions, `FROZEN.sha256` 39/39 OK.

- **Budget as given by the launcher**: about 150 min wall-clock, at most about 25 min per scenario. Used
  about 17 min in all (first logged build 13:09:16Z, last 13:23:19Z).
- **Builds made to fail on purpose are in the count.** `lakebuild.sh` prints goal states only when a build
  fails, so to read the goals left by `step*` I built with the goals open. 7 of the 14 FAILED lines in
  `effort/attempts.tsv` are such probes (their NOTE says "probe" or "view"). Why: the rule is that every
  build goes through the log; there is no other sanctioned way to see a goal. Undo: nothing to undo; when
  comparing arms, read FAILED as "failed or probe".
- **Loop specs are stated once per function and shared by its scenarios**, in `lean/Lemmas/*.lean`
  (one module per function; `Fill` imports `Take` and `Stock`, `Dominant` and `Count` reuse counting lemmas
  from `Restock`/`Stock`). A broken shared module would lose several proofs at once; the alternative
  (one self-contained file per scenario) would have tripled the lemma text. Undo: none needed.
- **`saturating_add`**: its definition in the Aeneas library is not `@[expose]`d, but a non-`module` file can
  still unfold it; `Lemmas.sat_val` proves `(saturating_add x y).val = min (x + y) U64.max` by `show` plus
  `BitVec.toNat_ofNat`. No axiom was added.
- **Deprecated names left in** (`if_pos`, `if_neg`, `ite_cond_eq_false`): they compile with warnings under
  Lean v4.35.0. Not cleaned up, to avoid extra builds in the measured log. Undo: rename per the warnings.
- Did not read `slice/` proofs or lemmas, `p2/arm-opus`, or the `slice/DESIGN.md` copy; read `TOOLCHAIN.md`
  and the Aeneas library (`Std/WP.lean` for `loop.spec_decr_nat`, `Std/Alloc/Vec.lean`, `Scalar/*`).

## P2 arm opus

2026-11-10, 08:07-08:26 EST. Working copy `p2/arm-opus` (made with `p2/base/workcopy.sh`; `.tools` and
`lean/.lake/packages` are the shared symlinks). Nothing installed; nothing written outside that directory
except this entry. Result: 16 of 16 scenarios PROVED-FOR-ALL, 7 of 7 functions fully proved, final
`./run.sh` exit 0, `FROZEN.sha256` 39/39 OK.

- **Budget as given by the launcher**: about 150 min wall-clock, at most about 25 min per scenario. Used
  14 min from making the copy to the last proof build (first logged build 13:11:35Z, last proof build
  13:21:51Z). No function took more than about 5 min.
- **Proof style: equational loop lemmas, not Aeneas's WP loop rule.** Every loop is specified by a lemma
  "the loop called from state s returns `ok` of (something stated with list functions or the reference
  definitions)", proved by induction on the remaining length, using two 2-line lemmas that unfold the
  `loop` combinator once (`PL.loop_cont`, `PL.loop_done` in `lean/Lemmas/Basic.lean`). Why: `fill_orders`
  calls `stock_of` and `take`, and `ok`-equations compose by rewriting. Trade: `effort/count.py` counts
  "loop invariants used" by occurrences of `loop.spec_decr_nat`, so it prints 0 for this arm although 9 loop
  lemmas carry invariants. Undo: none needed; read that row as "not applicable".
- **Three post-hoc probe builds are in the log** (`Lemmas.ProbeStep`, NOTE starts with "PROBE"), made after
  all 16 proofs were in, to answer "which Aeneas automation works on which loop" (`step*` with
  `loop.spec_decr_nat`). Two are FAILED on purpose (lakebuild prints goals only on failure). The module was
  deleted before the final `./run.sh`; it is not counted in the line totals. Proof cost alone: 16 attempts,
  8 FAILED. Undo: ignore the three PROBE lines when comparing arms.
- **AGENTS.md's "route verification through KiminaBridge/PantographWorker"** was not followed: those
  services do not exist (TOOLCHAIN.md); TASK.md's `./lakebuild.sh` (warm `lake build`, logged) was used
  for every check; I ran no `lake env lean` myself (`run.sh` runs its own generated scripts that way).
- **Independence**: did not read `slice/` proofs or lemmas, or `p2/arm-fable`. While checking this file's
  format at 08:25, after all proofs were done, I saw the "P2 arm fable" entry above; it played no part in
  the proofs.
- Deprecated names (`if_false`, `ite_cond_eq_true/false`) left in with warnings, to avoid extra builds.

## owner back (2026-11-10 morning); clock reset to 10:00 Eastern on Wednesday 2026-11-11

- **TDFLite rulings taken.** The owner accepted every suggested ruling in the private worksheet (the six from the owner's plan and three new ones). A tenth, on obligation triggers, was delegated to Claude with the instruction to stay conservative; decided fail-closed, with the reasoning and the remediation it implies recorded in `private/tdflite-pilot/t2/RULINGS.md`. One conditional suggestion was resolved toward its fail-closed branch on the owner's stated stance. Details stay private. These are rulings on the model and specification; nothing in the TDFLite repository was changed.
- **Obligations roadmapped** as plan node T7 (proof of capability versus declaration, trigger scoping, parity), not tackled now.

## V2/V3 frame library

Plan nodes V2 (frame library) and V3 (recompile regression), 2026-11-10. Everything written is under `slice/` (not `slice/compare/`) plus this section. No system-level install; no pin, manifest or `lake update` touched. Detail: `slice/DESIGN.md` section 14, `slice/FINDINGS.md` last addendum.

- **The old whole-phrase glossary was kept, in a smaller role, instead of being replaced.** What: every scenario now has two Lean statements, the reading compiled from the composable vocabulary (`<id>.reading`, the one shown and judged) and the old flat statement (`<id>.stmt`, unchanged); a generated kernel-checked `<id>.reading_iff` ties them, and a reading without it gets the verdict UNLINKED. Why: the task asks for a kernel-checked equivalence NEW ↔ OLD and for the existing proofs to carry over rather than be rewritten; it also kept the search, the refutations, the adequacy note and the 81 cucumber scenarios working untouched. Trade: two statements and two vocabularies in the tree; a NEW sentence has no flat statement, so it gets a reading, an echo and a search but no proof path and no Rust step. Undo: delete `slice/vocabulary.yaml`, `slice/slicegen/{vocab,links,rsearch,vreport,newrules}.py`, `slice/lean/Frames`, `slice/lean/{Wallet,Ledger}/Pieces.lean`, `slice/lean/Bdd/{Ops,Bridge,AuditLinks}.lean`, `slice/lean/Wallet/{Bridge,Instances,RuleProofs}`, `slice/lean/Run/FrameTests.lean`, `slice/heldout/`, and `git checkout` the modified files listed by `git status slice`.
- **13 of the 14 `Rule:` lines were reworded** so that they compose from vocabulary pieces (only "A transfer never changes the total of all balances" stood as written); each Rule also got an `@id:` tag for a short Lean name, and two got an `@expect-…` tag on the rule line. No scenario text changed, so the cucumber runs are as before. Why: the old lines were free prose ("…, or is rejected and takes nothing") that no controlled grammar reads; the alternative, leaving them uncompiled, defeats the task. Trade: the compound rules are long and stiff. Undo: `git checkout slice/features`.
- **How a Rule relates to its scenarios (decided): one direction only.** The outline scenarios beneath a Rule that are meant to hold are its parts; a generated kernel-checked `<rule>.from_scenarios : S₁ → … → Sₙ → R` proves the rule statement from them by cases on their Givens; a hand-written proof of exactly `R` may stand in where the script fails; a false `R` is refuted in the kernel at the input the reading search found. The converse (the rule entails its scenarios) is not claimed. Why: a rule is one sentence and its suite says more; and the forward direction is what makes "the rule line is proved for every input" true. 
- **`run.sh` now also fails when a rule statement misses its expected verdict** (PROVED-FOR-ALL unless tagged `@expect-refuted`, `@expect-unbound` or `@expect-unproved`). Consequence, deliberate: controls c8 and c17 (remove progress scenarios) changed their expected exit status from 0 to 1, because the rule statements proved from those scenarios are then no longer proved. Their original expectations are kept as patterns. Why this and not "report only": a rule line that silently loses its proof would otherwise pass. Undo: make `RuleVerdict.as_expected` always true in `slice/slicegen/vreport.py` and restore the two controls.
- **Two rule statements are proved by hand from the loop lemmas, not from their scenarios** (`slice/lean/Wallet/RuleProofs/ledger/{total_fits,batch_then_total}.lean`, 8 and 10 proof lines). Why: their scenarios name a sum with a `u64` outline parameter, which the fixed glue script cannot produce from a number. Trade: those two rules rest on the unsigned lemma library (the open problem already recorded for the ledger). Undo: delete the two files and tag the two Rules `@expect-unproved`.
- **Fail-closed default for `successful` / `rejected`.** A scenario always includes "the call gives an answer" (added as an explicit `AlwaysAnswers` conjunct when every Then is under "if it is rejected / accepted"); a Rule clause whose subject is "a successful …" or "a rejected …" does NOT (the author narrowed the claim; the echo prints "not default: … calls that give no answer are outside this clause"). Why: it keeps every old scenario statement equivalent and follows the owner's decision that a weaker reading has to be asked for.
- **Measures may depend on the input** (`Measure σ α μ := σ → α → μ`), a departure from the catalogue's `M : state → value`. Why: "the balance of the sender's account" names its part by the input; without it the single-transfer rule cannot be stated as a rule.
- **Which answers count as accepted is part of each operation's binding** (`slice/lean/*/Pieces.lean`): wallet `Ok(())`; ledger `apply` / `apply_all` `true`; `total` and `balance` "a value is returned"; `apply_batch` every answer (it never rejects). This differs from the adequacy note's hand-made list, which treats a count of 0 as a rejection for its own purposes. Unsigned, like everything else.
- **Idioms (10) are a fourth sort of entry.** A surface form with the composition it means (`"{w:wallet} has a balance of {t}"` means `is(w.balance(w), t)`); no Lean of its own. Why: scenario texts were to stay as they are, and 10 of the 36 old Given/Then phrases are not the regular form of any one piece. Trade: every fixture scenario uses at least one, and an idiom is one more English claim to sign.
- **A bystander is a modifier** (`Frames.Op.beside`), so that the old control "a deposit does not touch a bystander" still compiles (its second Then is true by construction and is still flagged).
- **Frames 12 to 14 and counting with a number were built as definitions with executable readings and ten hand-written test instances, with NO surface form.** Why: the TDFLite readings need them; no fixture does, and their hole types (a relation between two inputs, a reference function) have no domain word here. They are listed in the report as "no surface form yet".
- **Two edits to legacy files:** three `deriving instance DecidableEq` lines moved from `slice/lean/Wallet/Vocab.lean` to the new `slice/lean/Wallet/Instances.lean` (both the old glossary and the new domain words need them and deriving twice clashes); `mention: 'ledger [A-Z][a-z]+'` added to the ledger actor in `slice/glossary.yaml` (how the vocabulary sees the actor written). No definition, proof or line of Rust changed.
- **Five new ledger rules are in `slice/heldout/`, not in `slice/features/`**, and are informational (`./run.sh --no-heldout` skips them). Why: with no cucumber step and no proof they would fail the regression run by construction. They were written by me, in one pass, without running the compiler on drafts, and none needed a vocabulary change; this is not the V4 test (authors who do not know the vocabulary). A second file, `heldout/frames.feature`, holds seven sentences written only to exercise frames no fixture reaches; it is not counted among the five.
- **Mutation harness changes** (`slice/mutation/run_mutants.py`): seven new controls c21 to c27; c8, c17 as above; c20's patch text follows the reworded rule line; per-run timeout 900 s raised to 3600 s (c22 ran out at machine load 150); mutant runs pass `--no-heldout`; each mutant now also records `rules_changed` / `rule_shown_false`, beside the unchanged scenario columns. "A scenario is shown false" means what it meant.
- **TDFLite coverage check: counts and generic frame names only.** The per-reading classification of the 85 readings of `private/tdflite-pilot/REPORT.md` was done by reading that file and its `SEARCH.md`; nothing from them was copied into `slice/`, this file or any output, and the table itself was not written to disk.
- **Glue-script heartbeat budget** lowered from 1,000,000 to Lean's default 200,000 per theorem after a control with a broken definition spent 167 s of CPU failing; every glue theorem of the unchanged tree still checks.

## tdflite T2 (private work)

Plan node T2 (rulings as parameters, decision table) and an owner worksheet, run 2026-11-10 about 07:40–10:00. Everything written is under `private/tdflite-pilot/t2/` (git-ignored); nothing about specific behaviours is recorded here.

- **Counts.** 13 ruling parameters (the plan's six rulings with their facets, plus four further ones); 49 variants measured; 74 kernel-checked theorems (63 general, 11 instantiations at named ruling sets), 41 headline statements audited, standard axioms only, no `sorry`, no `native_decide`. The "today" setting is proved equal to the pilot's model (8 equalities of whole results) and re-run on 54,998 pilot and scorer cases with 0 differences. Search inputs per variant: up to 720,000 engine, 360,000 key-access and 360,000 rewrap inputs from the pilot's generators and seeds; 1,866 result files.
- **Copied, not imported, the pilot's Lean model** into `t2/lean` so that building never writes into the pilot's directory. Undo: delete `private/tdflite-pilot/t2/`.
- **Coverage was cut during the run** because the machine was shared and its load average was 40–160: the bounded-exhaustive tier was run on every 7th subject for two variants only, and the engine tier for the secondary variants got 4 seeds, 1 seed or none. The decision table's coverage section lists exactly what each variant has. Undo: `scripts/run_table.sh` re-runs what is missing (finished outputs are skipped).
- **Stopped and restarted my own job dispatcher four times** to reorder the queue, matching the process by the full path of my own script under `private/tdflite-pilot/t2/`; no other process was touched. A second executable name (`t2exh`) was added so a rebuild could not replace a binary that was running.
- **A file appeared in my directory mid-run** (`t2/RULINGS.md`, written by another session after the owner read the worksheet). I did not edit it, did not edit the worksheet after the owner read it, and added one measured variant and a set of theorem instantiations for the recorded set; later additions are in the decision table, not the worksheet.
- **Read-only look at the owner's TDFLite checkout** (`git log` / `git diff` of decision-path files against `4aca7ca`); its changed documentation files were outside that scope and were not read.
- No system-level installs. No `lake update`, no pin edits, no build in the repo root or `corpora/`.

## tdflite T3r (private work)

- **Ran 2026-11-10** (plan nodes T3r and T4). All output is under `private/tdflite-pilot/t3r/` (git-ignored); details stay private. No TDFLite checkout was modified; Go was run only in scratch copies.
- **Counts.** 162 kernel-checked theorems, 62 headline statements audited (standard axioms only, no `sorry`, no `native_decide`). Guarantees 1 to 5 proved on the ruled model; guarantee 8 proved given 8 named facts that were executed but not proved; guarantees 6 and 7 not statable in the model. The ruled model is proved equal to a 216-line readable specification for every input. Suite check: 4 of 4 trivial decision functions excluded by a proved guarantee.
- **Vectors.** 68 (40 in the owner's corpus format, 28 extended). On the real Go at the pilot's commit: 32 already give the ruled verdict, 36 do not, and those 36 are exactly the ones built to differ.
- **Change list.** 10 proposed diffs (291 lines added, 42 removed, 9 files), applied only in scratch: each applies and compiles alone; together 68 of 68 vectors give the ruled verdict and 17,612 generated cases match the ruled model with 0 differences; 1 existing test breaks.
- **Repeatable check (T4).** One command; 7,500 generated cases plus the vectors; 0 disagreements between the model of today and the Go at the pilot's commit (147 s) and at the owner's current checkout (113 s, through a scratch copy).
- **AGENTS.md rule 1.** The warm bridge is not running; `lake build` on a core-Lean package was used, `lake env lean` was not.

## Aeneas fork spike

### patches, runs and checks (2026-11-10, `census/fork/`)

- **Patch (ii) removes the failing method, not the trait, and also guards the impls of a trait whose declaration fails.** Why: catching the signature error alone moved the crate-level abort to extraction (`Not_found` in `trait_impl_is_builtin` on impls of `Pattern`). Trade: users of a removed method or impl fail one by one. Undo: drop commit 2 of `census/fork/patches/`.
- **Patch (iii) is wider than "the pure micro-passes".** It catches non-`CFailure` exceptions in five places (symbolic interpreter, function translation, micro-passes, type annotations, extraction of a declaration group). Why: on cedar each of them in turn aborts the crate; the micro-pass handler alone still leaves cedar with no output. A function caught this way is emitted as `sorry` or `axiom` with a logged error, which the census counts as failed. The handlers are off under `-abort-on-error`.
- **Patch (iv) qualifies builtin names only when the crate itself declares a type or trait with that last name component.** A first version qualified on any declaration; `core::result::Result` is in nearly every crate, so it rewrote `Result` in 39 of Aeneas's test outputs. Trade: an external type named like a builtin is not covered. Second amendment after a reproduction showed it: builtin functions in a shadowed type's namespace (`Slice.len`) are qualified too.
- **Cedar "Charon workarounds" runs for (ii) and (iii) were stopped by me before the join**, to give the final-state run the machine (load average 140 to 200 from other jobs; one cedar Aeneas run took 73 minutes). What is reported for them comes from direct runs of the same binaries on the same LLBC (`census/fork/data/cedar_direct_runs.json`): (ii) aborts, (iii) completes and writes 399,785 lines; the Lean build and per-function join exist only for the (iv) run, if it finished (FORK.md says which).
- **Processes killed: only my own, by process id**, after checking each id's command line or working directory was under `census/fork/` (a superseded p4 census pass, three abandoned Lean jobs, the two cedar runs above). No pattern kill was used.
- **Soundness sample: three seeded strata instead of one.** Sample A is the 30 asked for (seed 20261110); only 6 can be run, because most functions call something that did not translate or depend on an axiom. Sample B continues the same generator over the functions the census marks closed; sample C is a seeded draw of the functions only patch (iv) unlocks. Within B and C I ran the ones whose inputs can be written as literals and marked the others "not attempted": that is my selection and is stated in FORK.md. 25 functions, 895 inputs, 0 mismatches.
- **The Lean side of the soundness check runs a verbatim extract, not the generated file.** `lake` writes no `.olean` for a module with an error, so the dependency closure of each sampled function is copied verbatim from the generated file into `census/fork/lean/sound/Generated/Sound<Crate>.lean` and evaluated with `#eval` in one batch `lake build` per crate (no per-input Lean process).
- **A census defect found and not fixed** (outside my write scope): `census/scripts/census.py` computes "every local callee compiles" with a cached provisional value on recursion cycles; recomputed, the two stricter columns of `CENSUS.md` are 933 and 379 functions, not 936 and 382 (all three in `rust_decimal`'s parser). The headline column is unaffected.
- **Not done:** `make verify` on Aeneas's test outputs (needs the Lean v4.36.0-rc2 pin), `ocamlformat` on the patches, a Charon fix for cedar's ICE, any issue or pull request (texts are in `census/fork/FORK.md`, unsent).
- **Disk:** `census/fork/` holds about 8 Lake project copies whose packages are APFS clones (little real space), the opam root (0.7 GB), the Aeneas and Charon build trees (1.5 GB), and LLBC files and cargo target directories under `runs/` (about 10 GB, most of it cedar). All git-ignored. Undo everything: `rm -rf census/fork/{.opam,aeneas,bin,lean,backends-pinned,runs,work,tests-wt,logs}` (the tracked scripts, patches, data and FORK.md stay).

## tdflite T2 review (private work)

Independent check of plan node T2, run 2026-11-10 about 09:58–10:55 by a reviewing agent. Everything written is under `private/tdflite-pilot/t2/review/` (git-ignored) plus this section. Builds and runs used scratch copies in the session scratchpad. Nothing about specific behaviours is recorded here.

- **Counts.** Clean rebuild succeeded. 74 of 74 theorems use standard axioms only, with no `sorry` and no `native_decide`. The "today" setting equals the pilot's model on 54,998 case-file inputs (0 differences). A 200-case sample (recorded seed) replayed on the real Go through the pilot's harness agreed on 200 of 200 whole records; a negative control at another ruling setting differed on 88 of 200. Replaying today's counterexamples on Go gave 540 of 540 agreements. 729 re-run result files were byte-identical to the builder's, and an independent re-aggregation matched 958 of 958 flip-table rows. Of 11,566 stored counterexamples, 11,531 fail as stated under independent predicates; the other 35 are explained (one equality reading's reverse direction, and an input order that JSON does not preserve).
- **Corrections proposed, not applied.** 13 for the worksheet (4 high, 6 medium, 3 low) and 7 small ones for the decision table and README, written as exact replacement text in `t2/review/REVIEW.md`. Why not applied: the owner has already ruled on the worksheet, and the task limits writes to `t2/review/`. None reverses a ruling. Two bear on what the owner accepted. Undo: delete `private/tdflite-pilot/t2/review/`.
- **Scope cut under load.** The bounded-exhaustive tier and the engine random tier were not re-run. The rewrap tier was re-run for 7 of 49 variants (every one whose figures the worksheet quotes); the key-access tier for all 49.
- **Read-only look at the owner's TDFLite checkout** (`git --no-optional-locks` rev-parse, rev-list, diff, show, status). Nothing was changed there.
- No system-level installs (the Go and Lean toolchains were already present). No `lake update`, no pin edits, no build in the repo root or `corpora/`. No process was killed.

## P2 scoring

2026-11-10, 08:27 to 11:25 EST. Scorer: Opus 5.5 in a scoring role; it wrote neither the task nor any proof.
Written: `p2/score/` (scripts, results, git-ignored scratch copies under `work/`), `p2/RESULTS.md` and this
entry. The arm directories were only read. Nothing was installed: cargo-mutants 27.1.0 and the toolchain's
`leanchecker` were already present.

- **Scored in scratch copies, never in the arm directories.**
  - What: `p2/score/mkcopy.sh` builds each scoring copy from p2/base's frozen files plus the arm's `lean/Lemmas/`
    and `lean/Spec/Proofs/` only, with no Lean build outputs.
    - "Rebuild from scratch" here means every module of the project itself (model, vocabulary, statements, checks,
      lemmas, proofs).
    - Mathlib and the Aeneas library come from the shared prebuilt cache, through the same two symlinks
      `workcopy.sh` uses.
    - Cargo `target/` directories are APFS-cloned from base, to save compile time.
  - Why: the arms' own copies hold warm builds and logs that the score must not depend on or change.
  - Undo: `rm -rf p2/score/work` (it is git-ignored by `p2/score/.gitignore`).
- **The audit was written fresh**, not taken from `lean/Bdd/Audit.lean`, so the pipeline does not grade itself.
  - What: `p2/score/audit.py` checks:
    - the type is exactly the `.stmt` constant;
    - the declaring module;
    - the axioms are exactly `propext`, `Classical.choice` and `Quot.sound`.

    In addition, the toolchain's `leanchecker` replays every lemma module and proof module through the kernel.
  - Trade: leanchecker was not negative-controlled; the claim rests on its source (`Kernel.Environment.replay`).
- **My own line-counting rule**, stated at the top of `p2/score/count_lines.py`.
  - What it does: proof files without comments; declarations located by Lean's declaration ranges; declarations
    classified by the generated functions their types mention.
  - Why not `effort/count.py`: it counts comments in proof files and finds loop invariants only through
    `loop.spec_decr_nat`, so it reports 0 invariants for the opus arm.
  - The totals agree with count.py: lemma code lines 668 / 673, proof lines 115 / 93.
- **The arms' full build logs were read from the system temp directory.**
  - What: `lakebuild.sh` leaves every attempt's full `lake build` output in a `mktemp` file. I copied the 46 files
    from 08:05 to 08:30 out of `$TMPDIR` into `p2/score/results/buildlogs/` and left the originals alone. Each was
    matched to its line in `effort/attempts.tsv` by time and module names: 27/27 for fable, 19/19 for opus.
  - Why: to tell probes from mistakes using the errors themselves, not the arms' notes.
  - The rule (in `attempts.py`): a FAILED build is a "probe" only if its NOTE says so AND every error is
    "unsolved goals". Under this rule, fable's self-reported "7 probes" becomes 4 pure probes plus 4 builds that
    were labelled probes but also contained real errors.
- **Mutants: the tool's complete list, nobody's choice.**
  - Source: cargo-mutants 27.1.0 lists 107 mutants for `inventory/src/lib.rs`
    (`p2/score/results/mutants-diff.json`).
  - Run 1 (reference only): cargo-mutants' own run with the crate's unit tests.
  - Run 2, `p2/score/mutants.py`, per mutant:
    - a copy with no proofs runs `./run.sh --no-unit --no-adequacy`, which shows what the scenarios catch on
      their own;
    - each arm's lemmas and proofs are built against the mutated model.
  - "Shown false" means a REFUTED or COUNTEREXAMPLE verdict, or an Examples row failing on the compiled Rust. A
    proof that stops compiling is never counted as detection (PLAN rule 5).
  - Mutants that make a loop run forever crash the pipeline's search with a stack overflow. They are recorded as
    "pipeline stopped", not as detection.
- **Results of the mutant run** (for the record; details in `p2/RESULTS.md` section 6):
  - 92 of 107 mutants are shown false by a scenario, 10 stop the pipeline and 5 are not shown false, the same
    for both arms.
  - In both arms all 5 of those only lose proofs: 3 equivalent mutants, and 2 real bugs in `dominant_product`
    (#88 and #89) that the rows and the grid miss.
  - The 2 bugs' counterexamples (`[7,7,3]` and `[7,7,7,3,3]`, p = 7) were confirmed with a throwaway Rust program
    in the session scratchpad, not in the repository.
- **A fifth set of worker copies** (`work/mutw5-*`) was used after the run to rebuild both arms' proofs on the 3
  equivalent mutants and keep the Lean errors (`results/mutant-errors/`), because the main run did not keep them.
- **The harness was restarted once**, at 09:12, after 18 of 107 mutants.
  - What: from 3 workers to 4, and the per-mutant `translate.sh` dropped in favour of the translation inside the
    detection copy's own `run.sh` (same tool, same input).
  - Only my own process groups were killed, by explicit pid, never by pattern. Mutants in flight were redone from
    the start; the 18 finished records were kept.
  - Why: the machine's load average was 100 to 175 (another agent's slice mutation run and mine), and each mutant
    took about 6 minutes.
  - Consequence: the per-mutant times in `results/mutants/*.json` say nothing about the pipeline's speed.
- **The freeze is a digest, not a commit.** No commit of `p2/` exists, so `RESULTS.md` names the digest of
  `FROZEN.sha256` (`1ba3568c…005d9`). PLAN rule 1 asks for a commit, so that part is not met. Undo, if wanted:
  commit `p2/` (ignored files excluded) and add the commit to `RESULTS.md`.
- **The plan's P2 target is read as a signal, not a gate.** The crate has 7 functions, not 6, so "at least 5 of
  6" was read as "at least 5 of 7, per arm". Both arms got 7 of 7, so the reading changes nothing.

## tdflite T3r review (private work)

Independent check of plan nodes T3r and T4, run 2026-11-10 about 10:30–11:20 by a reviewing agent. Everything written is under `private/tdflite-pilot/t3r/review/` (git-ignored) plus this section; Go ran only in scratch copies there. Nothing about specific behaviours is recorded here.

- **Counts.** Clean rebuild succeeded; 162 theorems; all 280 theorem constants in the ruled modules use standard axioms only. Own random search (own generator, seed and oracle): 300,000 iterations, 11 properties, 0 counterexamples; the named facts checked directly on 46,801 compiled policies and 34,646 deciders, 0 failures. 68 of 68 vectors classified as stated on the pilot's commit and 68 of 68 at the ruled verdict with all changes; each of 10 changes applies and vets alone; module tests as reported (1 and 2 failing packages). 12,000 own cases: 0 differences in either comparison. The repeatable check gave 0 disagreements on both checkouts and exited 1 on a negative control.
- **Corrections proposed, not applied.** 12 (1 high, 6 medium, 5 low), with exact replacement text, in `t3r/review/REVIEW.md`, plus one tested patch and 8 extra vectors. Why not applied: the task limits writes to `t3r/review/`. None reverses a ruling.
- **Read-only look at both TDFLite trees** (`git --no-optional-locks` rev-parse and status, before and after; unchanged). No process outside my directory was touched. No `lake update`, no pin edits; `lake build` on a copy of the core-Lean package (the warm bridge is not running); `lake env lean` was run once, for a one-off audit file that failed to elaborate, and then replaced by a `lake build` target.

## V2/V3 frame library (continued)

- **The final mutation run used 12 jobs** (`python3 mutation/run_mutants.py --jobs 12`, 73 minutes at machine load 80 to 180; the harness deletes its scratch copies under `slice/build/mutation` when it ends). A first full run was stopped by me after 12 minutes, before its baseline had finished, to add one reporting theorem per proved reading (`<id>.reading_holds`, `<rule>.holds`), and restarted; it was stopped through its task handle, and I checked that no process was left with a working directory under `slice/build/mutation`. No process outside `slice/` was touched.
- **`rule_shown_false` was recomputed from the stored verdicts** (`run_mutants.py --resummarise`, no run repeated), so that a deliberately false rule that only loses its kernel confirmation under a mutant is not counted as newly found false.

## tdflite T3r (final)

- **Ran 2026-11-10**, after the independent review. All output is under `private/tdflite-pilot/t3r/` (git-ignored); details stay private. No TDFLite checkout was modified (HEAD, status and index time of both source trees unchanged before and after); Go was run only in scratch copies.
- **Corrections.** 12 proposed by the review (1 high, 6 medium, 5 low); 12 applied, 1 of them in a different form from the one proposed because the proposed text failed on this machine. 2 of the 12 changed the proposed diffs; the others changed wording, one script, one data file and the vector set. No ruling was reversed.
- **Wording superseded.** The earlier "tdflite T3r (private work)" entry says guarantees 1 to 5 are proved "on the ruled model" and that the named facts "were executed". Corrected: guarantees 1 to 4 are proved of the ruled reference-form engine and guarantee 5 of the key-access decision; guarantee 8 is proved given 8 named facts whose consequences were executed but which are not proved; guarantees 6 and 7 are not statable in the model. The reference-form engine is proved equal to the 216-line specification for every input; the other engine form and the key-access decision equal it given the named facts.
- **Counts after the rerun.** Lean: build succeeds, 162 theorems, 62 headline statements audited, standard axioms only. Vectors: 75 (42 in the owner's corpus format, 32 extended, 1 guard not computed by the model); on the real Go at the pilot's commit 35 already give the ruled verdict and 40 do not, exactly the ones built to differ. Change list: 10 proposed diffs (350 lines added, 64 removed, 11 files), each applies and vets alone; together 75 of 75 vectors give the ruled verdict and 17,612 generated cases match the ruled model with 0 differences; module tests 43 pass and 1 fails before, 42 pass and 2 fail after (1 existing test breaks).
- **Repeatable check (T4).** 7,500 generated cases plus the vectors: 0 disagreements between the model of today and the Go at the pilot's commit and at the owner's current checkout; exit status 1 on a negative control.
- **AGENTS.md rule 1.** The warm bridge is not running; `lake build` on a core-Lean package was used, `lake env lean` was not.
- **T3r finished (11:30).** Written up as experiment 23, counts only. The owner's next reading is `private/tdflite-pilot/t3r/README.md`. Nothing in any TDFLite checkout was modified; the reviewer verified both trees are unchanged.
- **Next heavy slot goes to the maths nodes M7 and M8** (re-invented abstractions; dead-code tool for any Lean project), since plan step 2 is still using the other slot.

## after the laptop slept (2026-11-10, about 18:00)

- **What the sleep cost:** four agents died on a network error: the frame library's reviewer, the Aeneas fork spike (after it had written its report), and both maths tools (M7, M8). Completed work was unaffected.
- **Two orphaned translator runs** from the dead fork-spike agent had been using about ten cores for over six hours on one crate. I stopped those two processes by PID. Nothing else was touched.
- **Relaunched:** the maths tools (told to continue from partial work); a slice workflow that reviews and fixes the frame library first, then makes new sentences run end to end, adds layered evidence (E1) and runs proxy sentence and echo trials (V4, V5); a small agent to finalise the fork report without rerunning the hung jobs; a small agent to apply the reviewer's corrections to the private rulings worksheet.
- **Call: builds run one at a time per agent from here on.** Load reached about 200 on 18 cores.
- **Disk:** the repo directory is 172 GB (census 93 GB, mostly fork-spike run output; corpora 41 GB); 112 GB free. The fork finaliser is asked to keep large run output out of git; pruning it is a housekeeping item.
