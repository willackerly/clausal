# Scope

What this project consists of, as of 2026-11-10. Draft for `docs/`; paths are from the repository root. The appendix at the end belongs to the brainstorm only.

**Status words.** *Exists*: works today on the two example crates, according to the repository's own reports and logs of 2026-11-10. *Partial*: some of it works, and the gap is named. *Planned*: not built. Nothing here was re-run to write this page, and no result has been reproduced outside the project. The frame library and vocabulary were under review on that date, so their counts may move.

**Name.** The repository is called lean-rosette. A rename is proposed (`brainstorm/NAMING.md`); this page uses the current name. The code says "frame" and "echo" where the proposed public words are "phrase" and "readback".

## What is lean-rosette

lean-rosette is a research prototype. It takes a behavioural rule written as one sentence of restricted English, compiles it from typed vocabulary pieces into a single Lean statement, and prints that statement back in English. On two small Rust crates written for the purpose, it then proves the statement about a Lean model that Aeneas generates from the Rust, or refutes it with a concrete input replayed on the compiled code, and reports the kind of evidence each step rests on.

It is also the measurements made on the way: how much real Rust the translator handles, what each kind of evidence catches, and what proofs cost.

**The checks on the proof link are the strongest part of the project. The checks on the translation link are the weakest**: example rows, a grid, and one small sample. **On current evidence the working product is a fixed reading plus tests**: in the comparison run, no injected bug needed a proof to be caught.

## What it is not

- **Not usable on your own crate.** Every end-to-end result is on a 45-line wallet and an 85-line ledger written to fit the unmodified tools.
- **Not free English.** Sentences outside a fixed grammar and vocabulary are refused. Of the 14 rule lines in the examples, 13 had to be reworded before they compiled.
- **Not a prover, a translator or a test runner.** It drives Lean, Aeneas, Charon, cucumber-rs, proptest and Kani.
- **Not a proof about a running system.** "Proved" means for every input of a generated model of one pure call. The translator, its hand-written models of library functions, the compiler and the hardware are trusted.
- **Not reviewed by people.** No vocabulary entry is signed (0 of 87), and no person has taken the reading trial. Every verdict is therefore recorded as "review". Reviews of the code and the checks were done mostly by a second language model.
- **Not a shared library yet.** The frame definitions have one consumer. No lemma library is shared between crates.
- **Not installable.** One platform (macOS arm64), about 55 GB, four Lean toolchains and three Rust compilers.

## Tooling

| Item | Status | Path | Gap or note |
|---|---|---|---|
| Pipeline runner: translate, generate, build, search, link, audit, run on Rust, adequacy, report | Exists | `slice/run.sh` | The example crates only |
| Translation driver: pinned Aeneas release, per-crate run, provenance hashes | Exists | `slice/translate.sh` | macOS arm64 only; cannot take a patched translator |
| Sentence compiler: rule or scenario to a typed reading, a Lean term and an English echo, or a refusal (unbound, ill-typed, ambiguous) | Exists | `slice/slicegen/vocab.py`, `slice/vocabulary.yaml` | Fixed grammar. An ambiguous sentence is refused without an input that separates the readings. A narrowing ("all balances" read as the two wallets in the call) is printed but not tagged |
| New-sentence compiler: compile from the vocabulary alone and search on the model | Partial | `slice/slicegen/newrules.py`, `slice/heldout/` | A reading, an echo and a search. No verdict, no run on compiled Rust |
| Flat statement generator (the older whole-phrase path) | Exists | `slice/slicegen/core.py`, `emit.py`, `pipeline.py`, `slice/glossary.yaml` | Every proof and every Rust test step still goes through this path |
| Link generator: reading proved equal to the flat statement; rule derived from its scenarios | Exists | `slice/slicegen/links.py`, `slice/lean/Run/Links.lean` | 34 of 34 readings linked. 2 of 10 proved rules needed a hand proof |
| Counterexample search on the model | Partial | `slice/lean/Run/Search.lean`, `slice/slicegen/rsearch.py` | A boundary grid only; no random sampling or shrinking |
| Audit of the Lean environment | Exists | `slice/lean/Bdd/Audit.lean`, `Bdd/AuditLinks.lean` | 180 lines |
| Suite adequacy against trivial implementations | Exists | `slice/slicegen/adequacy.py` | Informational |
| Rust runner: the same feature files on compiled Rust, counterexample replay | Partial | `slice/wallet-bdd/` | One hand-written step per old glossary phrase; not built from pieces |
| Report: per-rule blocks, "rests on", vocabulary and trusted-base tables | Exists | `slice/slicegen/report.py`, `vreport.py`, `rules.py`; output in `slice/out/report.md` | A rule block is about 45 lines; no brief form; verdicts are in JSON logs and the graph but there is no documented output schema and no exit code per verdict; the build profile is not recorded |
| Evidence graph, schema and lint, staleness, what-if | Exists | `slice/out/graph.json`, `slice/slicegen/graphlint.py`, `slice/schema/` | Whether the schema covers rule groups is open |
| Sign-off command | Partial | `python3 -m slicegen review` | Works as a mechanism; never used. Records a typed name, a date and a digest, not a cryptographic signature. Signs vocabulary pieces only: nothing records that a requirement's owner confirmed an echo |
| Mutation harness: 45 hand-written mutants, 27 negative controls | Exists | `slice/mutation/` | A separate command; 73 minutes under load |
| Property-test and bounded-check harnesses | Partial | `slice/compare/arms/` | 23 of each, hand-written. Generating them from a rule is planned |
| Translation census: how much of ten real crates translates, and why not | Exists | `census/scripts/`, `census/CENSUS.md` | |
| Translator fork build and measurement | Exists | `census/fork/` | Needs OCaml and opam |
| Model-against-Rust sampler | Partial | `census/fork/scripts/sound_sample.py`, `sound_run.py` | One run: 25 functions, 895 inputs, 0 mismatches |
| Evidence comparison harness (examples, property tests, bounded check, proof on every mutant) | Exists | `slice/compare/harness/` | A rerun takes 2 to 3 hours |
| Agent proof-writing experiment and scoring kit | Exists | `p2/` | One 161-line crate, two models |
| Reading trial: runner, offline page, scorer | Exists | `trials/meaning/` | Taken by 8 model readers and no people |
| Installable command, Linux support, container image | Planned | none | See "Not installable" above |
| CI that runs the chain and its controls | Planned | none | `.github/workflows/` is the stock Lean template |

One further route has been used once: for decision logic that is not Rust, a Lean model written by hand and compared with the real implementation by differential testing. Its only example is on a private Go target and is not part of this inventory.

## Libraries

| Item | Status | Path | Gap or note |
|---|---|---|---|
| Frame definitions: 23 Lean definitions for a catalogue of 14 frames, over one abstract operation with typed holes | Exists | `slice/lean/Frames/` (643 lines) | Imports Lean core only. One consumer. 19 of the 23 can be reached from a sentence. Under review |
| Executable second reading of each frame | Exists | `slice/lean/Frames/Check.lean` | Compared with the definition on generated inputs each run |
| Frames' English: surface forms, echo templates, printed defaults | Partial | `slice/vocabulary.yaml`, `slice/slicegen/vocab.py` | Lives in the pipeline, not with the definitions. This is the half a reader would sign |
| Rust reading of each frame | Planned | none | Needed before any generated test; it will be a second, unproved formalisation |
| Modifiers (27) | Exists | `slice/lean/Frames/Core.lean`, `slice/vocabulary.yaml` | Not audited one by one for assumptions carried over from the ledger |
| Idioms (10 forms that stand for a composition) | Exists | `slice/vocabulary.yaml` | Specific to the examples |
| Domain vocabulary for the wallet and ledger (31 words, 8 bound to model functions) | Exists | `slice/vocabulary.yaml`, `slice/lean/*/Pieces.lean` | Per system by design; not a library. Lean side only. Four function shapes can be bound (`slice/lean/Bdd/Ops.lean`) |
| Old whole-phrase glossary (44 entries) | Exists | `slice/glossary.yaml` | Legacy, and still carries every proof and test step |
| Bridge and audit support for Aeneas models | Exists | `slice/lean/Bdd/` (388 lines) | Copied into `p2/`, not shared |
| Per-crate loop lemmas | Exists | `slice/lean/Ledger/Lemmas/`, `p2/arm-fable/lean/Lemmas/`, `p2/arm-opus/lean/Lemmas/` | Three independent sets. Unsigned, and two rule statements rest on them |
| Shared loop and collection lemma library | Planned | none | Nothing is factored out |
| Models of Rust standard-library items | Upstream | Aeneas's own (347 functions) | Our addition is one six-line lemma, in `slice/lean/Ledger/Lemmas/All.lean`. We have not tested Aeneas's models against the real functions |
| Supported-Rust profile: 16 rules with evidence and probes | Exists | `census/PROFILE.md`, `census/probes/` | A document. Nothing checks a crate against it |
| Mutant and control sets | Exists | `slice/mutation/`, `slice/compare/mutants/`, `p2/score/` | Bound to the example crates |
| Item bank for the reading trial (54 items, 18 with a seeded error) | Exists | `trials/meaning/items.json` | Echoes are hand-written, not the tool's output |
| Frame catalogue and prior-art survey | Exists | `out/prior_art_vocabulary.md` | |

**How far the library idea has got.** The reusable pieces are the intended centre of the project and are not yet the centre of the work. The definitions are independent of any one system by construction and by nothing else: no second system has compiled a rule with them. "Compiled from reusable pieces" describes the statement today, not the evidence: the proofs and the test steps still go through the older whole-phrase glossary.

**On the comparison with Mathlib.** It fits a shared lemma library, which does not exist yet and whose natural home is the Aeneas ecosystem. It does not fit the frames: a Mathlib lemma is correct because the kernel checked it, while a frame is adequate only because a person says its Lean matches its English, and no person has yet said so. A frame library therefore has to stay small and change by new versions, where Mathlib grows and refactors freely.

## Checkers

"Automatic" means it runs inside `slice/run.sh` with no person involved.

| Check | Failure it prevents | Status | Path |
|---|---|---|---|
| A proof's type is exactly the generated statement | A theorem of type `True` counted as a proof | Exists, automatic | `slice/lean/Bdd/Audit.lean` |
| Standard axioms only; `sorry` counts as absent | A proof resting on something unchecked | Exists, automatic | `slice/lean/Run/Audit.lean` |
| Non-vacuity witness, kernel-checked | A claim true because its conditions never hold | Exists, automatic | `slice/lean/Run/Audit.lean` |
| Trivial-Then check | A Then that says nothing | Exists, automatic | `slice/lean/Run/Audit.lean` |
| Input coverage | Inputs no proved scenario mentions | Exists, automatic | `slice/lean/Run/Audit.lean` |
| Suite adequacy | A rule set that "reject everything" also satisfies | Exists, automatic, informational | `slice/slicegen/adequacy.py` |
| Second reading of each frame | A weakened frame definition | Exists, automatic | `slice/lean/Run/ReadingSearch.lean`, `Run/FrameTests.lean` |
| Second reading of each domain phrase, Lean against Rust | A weakened domain definition | Partial | `slice/wallet-bdd/tests/readings.rs` (old phrases only) |
| Reading proved equivalent to the proved statement | A recompiled sentence quietly weakened | Exists, automatic | `slice/lean/Run/Links.lean` |
| Rule derived from its scenarios | A rule called proved when only its scenarios are | Exists, automatic | `slice/lean/Run/Links.lean`, `slice/lean/Wallet/RuleProofs/` |
| Kernel-checked refutation at the found input | "False" reported because of a search bug | Exists, automatic | `slice/lean/Run/Audit.lean` |
| Counterexample replay on compiled Rust | A refutation that is an artefact of the model | Exists, automatic | `slice/wallet-bdd/` (old-phrase scenarios) |
| Example rows on model and on compiled Rust | Model and code disagreeing on stated cases | Exists, automatic | `slice/wallet-bdd/`, `slice/lean/Run/Search.lean` |
| Model against compiled Rust on generated inputs | A translator or library-model error away from the examples | Partial | `census/fork/scripts/sound_run.py` (one sample; nothing for the example crates) |
| Mutation run, with "shown false" counted apart from "proof lost" | Rules that leave behaviour unconstrained; an agent proving around a bug | Exists, separate command | `slice/mutation/run_mutants.py` |
| Negative controls that must fail | A check that cannot fail | Exists, separate command | `slice/mutation/run_mutants.py` |
| Graph schema lint and self-test | A malformed evidence graph | Exists, separate command | `slice/schema/selftest.py` |
| Staleness of proofs and signatures | Evidence outliving a changed definition | Exists, never exercised | `slice/slicegen/graphlint.py` |
| Unsigned-vocabulary flag and `--strict` | "Proved" resting on a reading nobody reviewed | Exists, automatic | `slice/run.sh` |
| Provenance digests | A model regenerated from different source or tools | Partial | `slice/lean/provenance.json` (recorded, not compared between runs) |
| Kernel replay with `leanchecker` | Tampering during elaboration. It runs the same kernel, so it is no defence against a kernel bug | Partial | `p2/score/` only |
| Guard against agents editing rules, vocabulary or axioms | A proof obtained by weakening the claim | Partial | `p2/score/` (by hash); a written rule elsewhere |
| The English echo matches the Lean reading | A printer or parser error that shows a person one thing and proves another | **None.** Only a person comparing the two | none |
| CI running the chain and its controls | Regressions between sessions | Planned | none |
| Clean-room re-check from a released bundle | Results that hold on one machine only | Planned | none |

Most of these exist because a review pass found the failure they prevent. The reviewer was usually a second language model, sometimes the owner.

## What a "proved" verdict trusts today

| Trusted | Nature | Bound today |
|---|---|---|
| Frame and modifier definitions; domain-word definitions (`Pieces.lean`) | 643 lines shared; a few lines per domain word | Second executable readings; printed in the report. Unsigned |
| The sentence parser and the English printer (`slicegen`) | About 7,400 lines of Python | The Lean it writes is type-checked and linked to the proved statement. Its choice of pieces and its English are checked by nobody |
| The statement form, bridge lemmas and audit | 388 and 180 lines of Lean | Kernel-checked; negative controls |
| Loop specifications | Per-crate lemmas | Kernel-checked as lemmas; what they say a loop does is unsigned |
| Lean's kernel | Small, widely used | Not replayed in the main run |
| Charon and Aeneas | A research translator, pinned | Example rows; one sample of 25 functions on 895 inputs, on other crates |
| Aeneas's models of standard-library functions | Hand-written | Listed in the report; not tested by us |
| The build | Model from Charon's nightly compiler; test binary from rustc 1.94.0 | Versions recorded. Profile, features and overflow-check setting are not |
| rustc and the hardware | Large | Assumed |

Tested and bounded verdicts rest on hand-written harnesses, proptest and Kani.

## Documented methodology

| Practice | Status | Path | Gap or note |
|---|---|---|---|
| Rules for every experiment (frozen before data, items not chosen by the builder, a lost proof is not a detection) | Exists | `docs/PLAN.md`, "Rules for every node" | Freezing at a commit was not met in two experiments, which froze by digest and say so |
| Build, review on a different model, fix, rerun | Exists | `docs/PLAN.md`, `docs/SETUP.md` | |
| Decision log with reason and undo | Exists | `DECISIONS.md` | Complete, with no index |
| Fail-closed defaults; when to split a vocabulary piece | Exists | `docs/VOCABULARY.md`, `docs/ARCHITECTURE.md` section 4 | |
| How to add a sentence | Exists | `slice/README.md` | Documents the gap as well as the path |
| Writing Rust that translates | Exists | `census/PROFILE.md` | Tied to one translator version |
| Carrying and dropping a translator patch | Exists | `census/fork/FORK.md` | |
| Evidence-graph schema | Exists | `docs/SCHEMA.md` | |
| Running a reading trial | Exists | `trials/meaning/README.md` | |
| Setup, pins, undo steps | Exists | `docs/SETUP.md`, `slice/TOOLCHAIN.md` | One platform |
| Readings and rulings for ambiguous requirements | Partial | `docs/ARCHITECTURE.md` section 12, `docs/VOCABULARY.md` | The only worked example is private |
| Method for code that is not Rust (hand model, differential check) | Partial | `docs/ARCHITECTURE.md` section 12 | "Model checked by differential testing" has no pass bars |
| Proof-writing guide for agents | Partial | `slice/README.md`, `slice/DESIGN.md`, `p2/base/TASK.md` | Spread over three files |
| What each verdict requires (an evidence contract) | Partial | `docs/ARCHITECTURE.md` section 5 | The verdict table is prose |
| Contributor and agent rules | Partial | `AGENTS.md` | To be rewritten: it describes an earlier project |
| Who may sign what, what a signature attests, which text governs | Planned | none | Open in `docs/ARCHITECTURE.md` section 15 |
| Red-build policy | Planned | none | Open in `docs/PLAN.md` |
| How a loop is fully specified | Planned | none | Open; exact loop behaviour sits in unsigned lemmas until decided |
| A threat model: which ways of cheating each checker addresses | Planned | none | The checkers imply one; it is not written |

## Not done yet, and we are confident it is needed

Ordered by how certain the need is. The first nine rest on a finding already in the repository.

| # | Need | Why |
|---|---|---|
| 1 | A Rust reading per vocabulary piece, so a new sentence runs on compiled code with no hand-written step | Without it, "built from reusable pieces" covers statements only |
| 2 | Property tests and bounded checks generated from a compiled rule, with failing inputs fed back | Property tests found 212 of 212 false rule-and-mutant pairs and the pipeline's own search 188; 23 of each harness are hand-written |
| 3 | A generated test of the model against the compiled Rust | The translation link has one small sample behind it |
| 4 | Signatures, roles for signing, and a record that a requirement's owner confirmed an echo | 0 of 87 entries signed |
| 5 | The patched translator in the chain, or the patches upstream | 1% of functions in ten real crates translate as shipped |
| 6 | A second, real Rust codebase | No frame, proof or step has met Rust that was not written to fit |
| 7 | A shared loop and collection lemma library, and a decision on how a loop is specified | About 6 lines of Lean per line of Rust, unchanged across two experiments |
| 8 | People as readers and authors | The reading trial has had model readers only |
| 9 | CI, a clean-room re-check, and an installation others can use | Nothing reruns the chain; one machine; one platform |
| 10 | Versioning for the frame library | A change to one frame voids every signature built on it |
| 11 | Standard-library models for common unmodelled items | 382 of 4,385 census functions compile with no unmodelled dependency |
| 12 | Retiring the old glossary | Two vocabularies and two statements per scenario |
| 13 | A separating input when a sentence is ambiguous; a tag on every narrowing | Refusal exists; the question does not |
| 14 | Sentence forms for claims that compare two runs | Definitions exist with no surface form |
| 15 | A policy and tooling for proofs lost under change | 92 of 295 lost proofs belonged to rules nothing showed false |
| 16 | A pattern for effects and I/O around a pure core | The one real defect found so far was outside the model |
| 17 | An evidence bundle a third party can re-check offline, with build identity | The graph has the content; no such bundle is designed |
| 18 | Machine-readable verdicts, exit codes and per-stage timings | Needed by CI and by code-writing agents; only a Markdown report exists |

Items 1 to 3 are one piece of work.

## What we modified or improved in other tools

**No modified third-party tool is in the end-to-end chain today.** `slice/translate.sh` runs the unmodified Aeneas release. The patches below were measured on the census only.

| Tool | What we did | Effect measured | Status |
|---|---|---|---|
| Aeneas, patch 0001 | Keeps analysing declaration groups after a mixed group | +0 functions on the ten crates as shipped | Upstream report prepared, not sent |
| Aeneas, patch 0002 | A trait-method signature that fails drops that method, not the whole crate | +1,368 functions | Prepared, not sent |
| Aeneas, patch 0003 | Catches further exceptions per function | +0 as shipped | Prepared, not sent |
| Aeneas, patch 0004 | Lean backend: avoids two kinds of name capture | +117 functions | Prepared, not sent |
| Aeneas, patch 0005 | Resets the formatter after an extraction error | +0 on the ten crates | Prepared, not sent |
| Aeneas Lean library | One `step` lemma for `Vec<u64>::clone` | Needed by the ledger proofs | Local; not offered upstream |
| Charon | Worked around, not patched: 49 functions and two generated parsers marked opaque for one crate | Lets that crate past a compiler crash | Local (`census/data/overrides.json`); no upstream report |
| Lean toolchain | Worked around: four pinned versions side by side; audits run as scripts | none | Local |
| hax 0.5.0 | Evaluated | Stops on the same crates with the same errors | Set aside |

The five patches are in `census/fork/patches/` (334 lines added, 53 removed), with reports in `census/fork/upstream/`. Aeneas's own 122 extraction tests are unchanged. The patches have not been run through `ocamlformat` or checked against the upstream tracker for duplicates.

Functions that end as compiling Lean, per crate (`census/fork/FORK.md`). This counts translation only. It says nothing about whether a model is faithful, and no function here has been proved.

| Crate | Functions | Unpatched | With the five patches |
|---|---|---|---|
| cedar-policy-core | 2,503 | 0 | 0 |
| time | 774 | 0 | 703 (91%) |
| indexmap | 630 | 0 | 475 (75%) |
| rust_decimal | 242 | 0 | 217 (90%) |
| semver | 80 | 0 | 54 (68%) |
| rusty-money | 60 | 0 | 27 (45%) |
| shlex | 34 | 22 (65%) | 22 (65%) |
| zeroize | 32 | 27 (84%) | 27 (84%) |
| untrusted | 26 | 11 (42%) | 20 (77%) |
| fnv | 4 | 4 | 4 |
| **All ten** | 4,385 | 64 (1%) | 1,549 (35%) |

Used as shipped: Lean and Lake, Mathlib (through Aeneas), cucumber-rs, proptest, Kani, cargo-mutants. Designs borrowed without code: NASA FRET, Dwyer's property patterns, Cedar's differential-testing method, Gherkin's `Rule:`.

## Out of scope

**Deliberately**

- **Free-form English.** No language model sits between a sentence and its meaning.
- **The compilation link.** Verified compilation of Rust is an open problem; rustc and the hardware stay a stated assumption.
- **Concurrency.** No frame covers it and the translator does not handle it.
- **Time** ("eventually", "until") and protocol state machines. Frames describe one pure call, or a short fixed sequence of calls.
- **Building a prover, a translator or a test runner.**
- **A hosted service.**

**For now**

- **Effects and I/O.** This is where real defects are likely to be, so it is listed as a limit and as need 16, not as a judgement that it does not matter.
- **Claims that compare two runs** (need 14).

## Figures that need a caveat when cited

| Figure | Caveat |
|---|---|
| 35% of functions translate with the patches | Two patches do the work; it is 82% of nine crates and none of the tenth. Translation, not proof |
| Property tests found 212 of 212, the bounded check 209, example rows 144 | Rule-and-mutant pairs, from 52 mutants generated by cargo-mutants on two crates we wrote; harnesses written by hand |
| 92 of 295 lost proofs were on rules nothing showed false | "Nothing showed false" is weaker than "still true" |
| 93% of wrong readings caught | Eight model readers, none of them people; hand-written echoes |
| 13 of 14 rule lines needed rewording; 12 of 12 held-out sentences compiled | Both by the vocabulary's builder |
| 23 frames | 14 catalogue frames; 23 Lean definitions, 4 of them unreachable from a sentence |
| Two models proved all seven loop functions in under fifteen minutes | Textbook loops, one small crate |
| All six known edge cases found on the private target | The search was pointed at them; the example cannot be inspected |
| Every timing | Measured on one heavily loaded machine |

## Also in the repository

A separate strand holds tools for navigating large Lean proof developments (`Rosette/`, `bench/`, `tools/deadcode/`). It shares only the evidence-graph format with the rest, and most of its results are negative (`docs/RESULTS.md`).

---

## Appendix: what the target README claims that is not true today

Brainstorm only. The numbers are the small numbers in [`README-target.md`](README-target.md). "Inventory" is [`inventory.md`](inventory.md); plan nodes are in `docs/PLAN.md`; "FORM" is [`FORM.md`](FORM.md). Plan nodes for the needs above: 1 and 2, E1; 4, G1; 5, A2 and A3; 6, S1; 8, K1, V4 and V5; 9, X2 and X3; 10, V9; 11, A3; 13, V6; 14, T5; 15, S2.

| # | Claim in the target | State today | What exists | Covered by |
|---|---|---|---|---|
| <a id="c1"></a>1 | The project is called Readback | Not done | A recommendation only. No stranger has heard the name; no trademark search; nothing renamed | `NAMING.md` section 3; FORM decision 10 |
| <a id="c2"></a>2 | One `cargo` subcommand, installed with one command, on Linux and macOS | Not built | `slice/run.sh` and `python3 -m slicegen`; macOS arm64 only; about 55 GB | Inventory 6 #10; no plan node |
| <a id="c3"></a>3 | Domain words bound in Rust; readback, example rows and a **generated** property test on a crate you bring; Rust and Lean readings compared | Not built | Rows run for 44 old whole-phrase entries, one hand-written step each; 23 property tests hand-written; new vocabulary pieces have no Rust reading. Who writes generators for types with invariants is undecided | E1; FORM decision 6 |
| <a id="c4"></a>4 | A **generated** bounded check; failing inputs from tests and bounded checks fed back as counterexamples | Not built | 23 Kani harnesses hand-written; `slice/compare/harness/confirm.py` replays inputs for one experiment. No story for unwinding bounds on collections | E1 |
| <a id="c5"></a>5 | Proofs on a profile crate you bring, with the patched translator in the chain | Partial | Proofs work on two crates written to fit, with the **unpatched** release. Wiring the patches in is "not done and not tested" | A2, A3, S1 |
| <a id="c6"></a>6 | A proof image | Not built | `slice/translate.sh --setup`, `docs/SETUP.md` | Inventory 6 #10 |
| <a id="c7"></a>7 | A brief report with the reading beside the verdict, and the label "PROVED for every input of the model of …" | Not built | The lines shown are real, but a rule block is about 45 lines and the block in the target is a trim with four altered lines, marked (a) to (d). Counterexample values are not labelled as balances | FORM, tooling table |
| <a id="c8"></a>8 | Vocabulary signed; phrases signed by two reviewers | Not done | The mechanism and `--strict` exist and have never been used: 0 of 87 signed. No second reviewer is identified | G1; FORM decision 4 |
| <a id="c9"></a>9 | A reader trial with people, with a result | Not run | Harness, offline page and 54 items; 0 human readers; 8 model readers caught 134 of 144. Items use hand-written echoes | K1 with people, V5; FORM decision 2 |
| <a id="c10"></a>10 | The catalogue as its own versioned unit; edition 0 published; a phrase needs two unrelated systems | Partial | 23 Lean definitions in `slice/lean/Frames/`; the English is in the pipeline; one consumer; no Rust reading; under review | V2, V3, V9 |
| <a id="c11"></a>11 | Model run against compiled Rust on generated inputs, each run; library models tested | Partial | Example rows and a grid; one sample of 25 functions on 895 inputs | Inventory 6 #6; no plan node |
| <a id="c12"></a>12 | An ambiguous sentence is refused **with a separating input** | Partial | Ambiguity is refused; no input is shown | V6 |
| <a id="c13"></a>13 | One crate we did not write, end to end | Not done | No frame, proof or step has met Rust that was not written to fit | S1 |
| <a id="c14"></a>14 | The hand-model route as a documented route | Partial | Four steps in `docs/ARCHITECTURE.md` section 12; done once, privately. Moved to the roadmap in the target | T4; FORM decisions 3 and 8 |
| <a id="c15"></a>15 | The five Aeneas patches are submitted upstream | Not done | Five reports prepared; none sent | A2 |
| <a id="c16"></a>16 | A CI action reporting by kind of evidence | Not built | Stock Lean template. On the roadmap in the target, not in 0.1 | X2 |
| <a id="c17"></a>17 | A second, independent verifier | Not built | P2 has an audit that shares no code with the slice's. On the roadmap in the target, not in 0.1 | X3 |
| <a id="c18"></a>18 | Kernel replay in the main run | Partial | `leanchecker` is used in `p2/score/` only | Inventory 3 |
| <a id="c19"></a>19 | Negative controls and invalid graphs as one `selftest` | Partial | Both exist as separate commands | X2 |
| <a id="c20"></a>20 | A lint that checks a crate against the profile | Not built | The profile is a document | Inventory 6 #21 |
| <a id="c21"></a>21 | Append-only phrases with versions; a lock file of digests | Not built | Per-piece digests and staleness exist; frame definitions are being changed in place now | V9 |
| <a id="c22"></a>22 | A new sentence gets tests and a bounded check with no new code | Partial | A new sentence gets a reading, an echo and a model search (12 of 12 held-out sentences, written by the builder). No verdict and no run on compiled Rust | E1; V4 |
| <a id="c23"></a>23 | Method documents; "the Lean governs" | Not written | Experiment rules, the profile, the schema and the hand-model steps exist. Which text governs awaits the owner | FORM decisions 1 and 7 |
| <a id="c24"></a>24 | The figure in "What it rests on" | Draft | `diagrams/chain-v2b` passes its format checks; its small text is near 9 px at README width; it omits the reading-to-statement link | `diagrams/notes.md` |
| <a id="c25"></a>25 | Loop and collection lemmas contributed to the Aeneas ecosystem | Not done | Three per-crate lemma sets, nothing factored out | FORM decision 5 |
| <a id="c26"></a>26 | A guard on changes to rules and vocabulary | Partial | By content hash in P2; a written rule in the slice | Inventory 3 |
| <a id="c27"></a>27 | A per-rule policy on what fails a build | Partial | `--strict` only; undecided | S2; FORM decision 7 |
| <a id="c28"></a>28 | Every narrowing tagged like a default; the readback confirmed by the requirement's owner; `--strict` fails until it is | Not built | The narrowing is visible in the echo's wording only. Sign-off covers vocabulary pieces, not echoes | No plan node |
| <a id="c29"></a>29 | JSON output, exit codes by verdict class, a refusal with nearest forms in machine-readable form | Not built | A Markdown report and `graph.json`. Per-stage timings are not measured; "check takes seconds" was dropped from the target for that reason | No plan node |
| <a id="c30"></a>30 | Build identity in every report (commit, lock file, features, target, profile, overflow setting) | Partial | Tool versions and provenance hashes are recorded; the build profile is not | No plan node |
