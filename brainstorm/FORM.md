# FORM: what lean-rosette should become

Judge's synthesis for the owner, 2026-11-10. Not for publication. I read `README.md`, `docs/ARCHITECTURE.md`, `docs/RESULTS.md`, the Stance and Status sections of `docs/PLAN.md`, every file in `brainstorm/`, and the refuted rule in `clausal/features/wallet.feature`. I ran nothing. I did not read `private/` or `tdflite-ideas/`. Counts are from `brainstorm/inventory.md` unless marked otherwise.

## The answer in five lines

1. **The question of form depends on one experiment.** Every form's distinctive claim rests on the hypothesis that a person catches a wrong reading when it is echoed back. No person has been tested. Run that trial before choosing a public form. It is the cheapest decisive experiment the project has.
2. **Recommended form: a tool now, a catalogue later, the checkers throughout.** Adoption comes through a tool. The lasting value builds up in a small catalogue of frames, together with the evidence that people read them correctly. The checkers are the most credible thing in the repository at every stage.
3. **Your instinct is right about where the value ends up, and the Mathlib analogy is wrong about what that value is.** The pieces will matter most. But there will be 15 to 50 of them, nothing like Mathlib's scale, and their value is trust, not saved work. The part that really is like Mathlib (loop and collection lemmas) belongs in the Aeneas ecosystem.
4. **The better analogy for the vocabulary is Creative Commons licences**: a few composable pieces, each with a formal text, a plain-English text and a machine-readable form, changed only by issuing a new version. That analogy also raises a question Mathlib hides: which text governs.
5. **Aim the default at formal statements, not proofs.** "Every rule has one fixed formal reading and graded evidence" can become the default. "Every rule is proved" cannot, and your own K2 result says it need not: no injected bug needed a proof to be caught.

## 1. The three proposals compared

| | Library first | Toolchain first | Standard first |
|---|---|---|---|
| **Adoption path** | Lean and Aeneas users, who need the English layer least. Gets consumers only through a tool. | A `cargo` subcommand; rungs 0 to 2 work on any Rust. Known adoption shape (Kani). Needs E1 and Rust readings, not built. | Through other implementers. None observed. |
| **Defensibility** if AWS or the Aeneas group enters the empty cell | Medium. 643 lines of Apache-2.0 Lean copy in an afternoon; reader evidence and signatures do not. | **Weakest.** Kiro ships the lower rungs already; a fixed reading would be a feature for them. | **Strongest if adopted**: a neighbour consuming it is a win. Worth nothing if not. |
| **Maintenance cost** | Few hours, scarce people (readers, a second signer). | **Highest.** Three nightly pins, two platforms, three implementations per frame, support. | Little code, many people (editor, trials). The tool is still needed underneath. |
| **Fit with today** | Frames exist; their English is in the slice. One consumer, 0 of 87 signed, no shared lemmas. | Closest in shape (`run.sh`, report, graph, sign-off). Two crates written to fit, macOS only, about 55 GB. | Schema v2, verdict table and controls are most of a suite. But schema went v1 to v2 in two days and 13 of 14 rule lines needed rewording: too soon to freeze. |
| **Honesty about trust** | Borrowed authority: "in the library" read as "correct". Mathlib earns that from its kernel; frames cannot. | CI squeezes four evidence kinds into one bit; "unsigned" becomes an ignored warning. | Fixes what "proved" means across tools. But levels invite teams to stop at "tested" and call themselves conformant. |
| **Right as** | A description of the long-run asset | The way to deliver | An internal discipline |

What the table hides:

- **The three proposers agree, and that agreement is weak evidence.** All three say "ship a tool, keep the repository library-shaped underneath". All three built on `positioning.md` and `inventory.md`, which had already recommended E1 first, so their agreement repeats those notes rather than confirming them.
- **All three name the same three risks**: the proof rung does not reach real code; the meaning link has no human evidence; the top rung depends on a research translator (1% of census functions as shipped, 35% with patches, none sent). No choice of form removes these. Only work and experiments do.

## 2. Recommended form

### The shape over time

| | Now (internal) | First public release (0.1) | Maturity |
|---|---|---|---|
| **Centre of gravity** | Two experiments: people reading echoes, and one rule producing evidence on Rust that was not written to fit | The **tool**, with the frame catalogue published beside it as a separate versioned unit | The **catalogue and the evidence contract**, used by more than one tool. Ours is the reference implementation |
| **Ships** | Nothing new in public. The README is corrected to real output only | `check` and rungs 0 to 3 on any Rust. Rung 4 on profile crates. Catalogue edition 0, signed provisionally, with its human-trial result. A two-page evidence contract. At least four worked examples | Catalogue edition 1 with two signers per frame. Lemma work living upstream. An authorisation pack only if it has earned its place |
| **Gate to the next stage** | Human trial result (whatever it is). One external crate end to end, failures listed | One consumer of the catalogue or contract that is not ours, or a second unrelated codebase. Clean-room re-check (X3) | none |

Why the centre moves from tool to catalogue: code is the cheap part (`clausal` is 7,255 lines agents wrote in two days), and the likeliest occupant of the empty cell is a large neighbour (AWS has Kiro, Cedar's Lean work and Bedrock Automated Reasoning). A rival tool loses to them. A catalogue with reader evidence and a fixed meaning for "proved" is something they could adopt, which counts as success. So design the catalogue as data any tool can read, from the start.

### Deliverables under your four headings

Stages: **Now**, **0.1**, **Later**. Status words as in the inventory.

**TOOLING**

| Deliverable | Today | Stage |
|---|---|---|
| Rust reading per piece. From it, per rule: a property test, a Kani harness and a differential test of the model against compiled Rust (E1) | NEEDED. 23 tests and 23 harnesses are hand-written | **Now**: the next build |
| `check`: sentence to reading, echo, or refusal. An ambiguous sentence comes with an input that separates the readings (V6) | PARTIAL. Works on fixtures; refuses ambiguity but shows no separating input | 0.1 |
| Proof rung: translate, build, search, link, audit, replay, with the patched Aeneas wired in | PARTIAL. Fixtures only, unpatched translator | 0.1, profile crates |
| Hand-model route: rules bound to a hand-written Lean model of non-Rust code, checked by differential testing | PARTIAL. Done once, privately, on Go | 0.1 as a documented route, tooling later |
| Brief report (at most eight lines per rule), JSON, evidence graph | PARTIAL. A rule block is about 45 lines | 0.1 |
| `sign`, `status`, lock file of piece digests | PARTIAL. The mechanism exists and has never been used | Now (use it), 0.1 (lock) |
| One install for rungs 0 to 3; a container image for rung 4; Linux | NEEDED | 0.1 |
| CI action that reports counts by evidence kind, never a single green | NEEDED (X2) | 0.1 |

Not ours to build: a prover, a translator, a test runner, or a language model between the sentence and its meaning (suggest mode, V7, stays outside the trusted path and after 0.1). The maths tools go to their own repository.

**LIBRARIES**

| Deliverable | Today | Stage |
|---|---|---|
| **Frame catalogue**: each frame and modifier as one versioned unit containing the Lean definition, the English form and echo, the executable reading, the Rust reading, separating examples and an evidence card | PARTIAL. The Lean exists; the English is in the slice; the Rust reading is missing | Now (extract), 0.1 (edition 0) |
| Bridge and audit support (`Bdd/`), shared rather than copied | EXISTS, copied into `p2/` | 0.1 |
| Loop and collection lemmas over Aeneas output | NEEDED. Three per-crate sets are raw material | Offer upstream. Measure whether it lowers the cost of about 6 Lean lines per Rust line |
| Standard-library models | Upstream (Aeneas generates its model list at build time). Ours: one six-line lemma | Contribute them; we ship differential tests for them |
| Rust profile, plus a lint that checks a crate against it | Profile EXISTS, lint NEEDED | 0.1 |
| Authorisation domain pack | NEEDED, unproven | Later, and only if two unrelated engines share it |

Project vocabularies are not part of the library. They live in the project's own repository, with its owner.

**CHECKERS**

| Deliverable | Today | Stage |
|---|---|---|
| Proof-link audit: exact type, axioms, non-vacuity, trivial Then, coverage, reading-to-statement link, rule from scenarios, kernel refutation | EXISTS, automatic | Keep. This is the asset that formal-methods readers will respect first |
| Differential test of the model against compiled Rust on generated inputs | NEEDED. One sample: 25 functions, 895 inputs | **Now**, with E1. This is the weakest link with the most valuable fix |
| Kernel replay (`leanchecker`) in the main run | PARTIAL (P2 only) | 0.1 |
| Negative controls and the invalid-graph self-test as `selftest` | EXISTS, outside `run.sh` | 0.1 |
| Guard: a change that touches rules or vocabulary together with proofs needs a named person | PARTIAL (hash check in P2) | 0.1 |
| Mutation run, with "shown false" counted apart from "proof lost" | EXISTS, 73 minutes | Nightly in CI |
| Clean-room verifier that shares no code with `clausal` (X3), built by an agent from the documents alone | NEEDED | Before maturity |
| Piece lint, and re-parsing every registered rule file when the vocabulary changes | NEEDED | Later, when a second consumer exists |

**DOCUMENTED METHODOLOGY**

| Deliverable | Today | Stage |
|---|---|---|
| Sign-off roles; gate and red-build policy; how a loop is fully specified | NEEDED | **Now**, one page each |
| Contributor and agent guide to replace `AGENTS.md`, which describes another project | NEEDED | **Now** |
| Readings and rulings for ambiguous requirements, with a public worked example | PARTIAL. The only example is private | 0.1 |
| Hand-model route, with "model checked by differential testing" named as an evidence level with pass bars | PARTIAL (Architecture section 12) | 0.1 |
| Proof-writing guide for agents, as one document | Scattered across three files | 0.1 |
| Writing Rust that translates | EXISTS (`census/PROFILE.md`) | Regenerate at each pin |
| Experiment rules (frozen before data, items not chosen by the builder, and the rest) | EXISTS | Keep |

**What the four headings miss**

| Deliverable | Today | Stage |
|---|---|---|
| **Evidence contract**: what each verdict requires before a tool may print it, the four evidence kinds, the graph schema, a signature attestation | Schema v2 EXISTS. The verdict table is prose. Requirements and attestation NEEDED | **Now**, two pages |
| **Trials and item banks**: the reading trial, the authoring trial (V4), wrong-echo items for each frame, results published with intervals | Harness EXISTS. 54 items. 0 people | **Now**: run it with people |
| **Worked-example corpus**: the fixtures, one external crate, one public hand-model example, the mutant sets. It doubles as the regression and conformance suite | PARTIAL: wallet, ledger, inventory | Grows with every release |
| **Upstream ledger**: every third-party tool changed, worked around or evaluated, and its status | PARTIAL. Five Aeneas patches, two of which do all the measured work; none sent | **Now**: send them |
| **Governance records**: signatures, a catalogue change log by class (equivalent, wording, meaning), an index to `DECISIONS.md` | PARTIAL | 0.1 |

The trials row is not a side item. The data it produces is what makes the catalogue worth more than a list of Dwyer-style patterns, and it is the part a large neighbour cannot copy quickly.

### Where I part from the proposers

- **The human trial comes before the first public release, not at 1.0.** All three defer it, following the stance. The harness is one offline page and takes a reader about ten minutes. Everything else (editions, signatures, the README's second paragraph) is being designed around a result nobody has. Set the bar that would change the form before the data arrives.
- **Your library is smaller than the word suggests**: 15 to 50 definitions plus the evidence about them. The definitions are not what is hard to copy; the reader data, signatures and worked examples are.
- **Keep the hand-model route first-class.** Toolchain-first drops it, but it produced your best real result and fits "decision logic in any language". The report already labels that model link as tested, so it costs no honesty.
- **Governance as pages, not machinery**, until a second consumer exists: no edition tooling, conformance classes or Rust rewrite yet. Keep library-first's best point, which the others missed: adding a surface form can make someone else's sentence ambiguous, so even additions need checking.
- **I agree with all three** on E1 next, sending the patches, a provisional owner signature now, English and Lean in one versioned unit, and a verifier sharing no code with `clausal`.

## 3. The Mathlib analogy

**Where it holds.**

- **The proof-lemma tier.** Loop and collection lemmas over Aeneas models are ordinary Lean: kernel-checked, better when general, safe to refactor, and where work is really saved (lemmas are over half of all hand-written Lean). Their natural commons is the Aeneas ecosystem, where the SymCrypt group already builds such libraries.
- **Curation habits**: linters as policy, naming conventions, reviewer and maintainer roles, AI disclosure, a scope rule ("in the core only if two unrelated systems need it").
- **The intent** that the second user pays less than the first.

**Where it misleads.**

- **Truth.** A Mathlib lemma is correct because the kernel checked it. A frame is adequate because people say its Lean matches its English. "In the library" will be read as "right".
- **Change.** Mathlib refactors freely. A changed frame voids signatures everywhere, so frames must be append-only.
- **Economics.** Mathlib's value is volume, each result saving later work. A frame's value is trust (sign once, reuse everywhere), and there will be few.
- **Subject and motive.** Mathematics is shared and people want it formalised. "Account" and "transfer" differ in every codebase, and nobody formalises them for their own sake.
- **One repository.** Mathlib builds all its users together. Here consumers are scattered and the grammar is not safe to extend, so changes must be tested against other people's rule files.

**A better analogy for the vocabulary: Creative Commons licences** (from memory, not checked today).

- **Three layers per licence**: legal code, a human-readable deed and machine-readable metadata. Here: the Lean definition, the English echo and the executable readings.
- **A few composable elements**, with combinations that do not exist (share-alike with no-derivatives). Here: typed pieces and the ill-typed refusal.
- **New versions are new licences**, and old ones stay valid.
- **Trust comes from careful drafting and an institution, not from a checker.** It is used by millions of people who never read the legal code.

The analogy also forces a question Mathlib never raises. CC states that the deed is not the licence. **Which text governs a frame?** If the Lean governs, the echo is a deed: a person confirming it confirms a summary, and every report should say so.

**A better analogy for the adoption path: gradual typing.** TypeScript became a default because it was useful at its loosest setting and could be tightened file by file. Rules with declared evidence floors work the same way. Shared declarations for other people's code (DefinitelyTyped) are the nearest model for domain packs.

**Suggested public sentence:** "The proof lemmas are meant to grow the way Mathlib has, and we contribute them to Aeneas's ecosystem. The vocabulary is closer to Creative Commons licences: a few pieces, each with a formal text, an English text and a machine check, changed only by issuing a new version."

## 4. What it is, and what it is not

**What it is (60 words, form not status).**

> lean-rosette compiles a one-sentence rule about decision logic into one fixed formal reading, built from a small shared vocabulary of signed definitions and echoed in English. It collects the strongest evidence it can that the code obeys the rule (examples, generated tests, bounded checks and, where the code translates, a Lean proof) and reports what each verdict rests on.

The status line goes directly under it: *Today: two example crates written to fit; a new sentence gets a reading but no verdict; 0 of 87 vocabulary entries signed; no human reader yet.*

**What it is not.**

- **Not a prover, translator or test runner.** It drives Lean, Aeneas, Kani and proptest, and offers its patches upstream.
- **Not an interpreter of free English.** A sentence outside the vocabulary is refused, never guessed.
- **Not a proof about your running system.** "Proved" means for every input of a model of one pure call. I/O, concurrency, time, the compiler and code outside the model are named and not covered.
- **Not a badge.** Evidence is reported by kind (kernel-checked, tested, tool-trusted, human-asserted) and never folded into one green.
- **Not a library of truths.** A frame is a definition people vouch for, not a theorem a kernel checked.
- **Not a substitute for a person.** If nobody reads the echo or signs the vocabulary, the report says so, and the verdict is worth less.

## 5. Decisions only you can make

1. **Which text governs a frame, the Lean or the English?** My suggestion: the Lean governs, and the echo is a subordinate deed. Signers of frames must read Lean; requirement owners confirm echoes.
2. **Will you lift the deferral on people tests for the echo trial, and what result would change the form?** For example: if people catch fewer than about 70% of wrong echoes, does the English layer become an index for experts (like FRET) instead of the trust mechanism? Fix the bar before the data.
3. **Is the identity "decision logic, any language, Rust mechanised first" or "a Rust tool"?** The answer decides whether the Go-style hand-model route is in the product.
4. **Will you sign the wallet and ledger vocabulary provisionally this week, and who could be a second signer of a different kind?** About an hour. It exercises staleness and `--strict`, which have never run.
5. **Send the five Aeneas reports, and contribute lemmas and models to that ecosystem rather than own them?** That is, is owning a library a goal in itself, or is it enough that the library exists?
6. **For domain words, should the Rust reading come first with a generated Lean reading (cheaper, but no independent second reading), or the Lean reading first with an independent Rust one?**
7. **In the product, may a rule fail a build?** If so, at which declared floor, and who owns a proof lost to a change that falsified nothing (92 of 295 lost proofs in K2)?
8. **Will any of the TDFLite work become a public worked example, sanitised or on a stand-in target?** The method's only example is private.
9. **Is success being adopted by a large neighbour (AWS, the Aeneas group), or being adopted against them?** The answer decides whether the catalogue is designed as data others can read from now on.
10. **Rename before anything goes to a package registry, and move the maths strand to its own repository?**

## What I am unsure of

- **Whether the human trial is as cheap as I say.** Recruiting readers who did not write the items, and keeping the answer key from them, may be the real cost.
- **The CC and TypeScript facts are from memory.**
- **Whether any large neighbour would consume an outside catalogue at all.** Section 2 leans on this.
- **Whether frames generalise past the fixtures.** The only evidence is 83 of 85 TDFLite readings judged expressible by reading.
- **Every count is taken from the inventory.** `clausal/out/report.md` was not on disk when I looked, because another run was in progress.
