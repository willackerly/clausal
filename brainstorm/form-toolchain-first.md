# Final form, angle 1: toolchain first

Brainstorm for the owner, 2026-11-10. Not for publication. This note argues one angle as hard as the evidence allows: the product is a command-line tool and a CI check that an engineering team installs, with the libraries bundled, adopted the way a linter or a test framework is adopted.

**Basis and limits.**

- **Sources.** `README.md`, `docs/ARCHITECTURE.md`, `docs/RESULTS.md`, the Stance and Status sections of `docs/PLAN.md`, and the four research notes in this folder. Every count below is from `brainstorm/inventory.md` unless marked.
- **Nothing was run.** I did not read `private/` or `tdflite-ideas/`. The one thing I checked in the tree myself is the wording of the refuted wallet rule.
- **The other two angles are my guess.** I was not told what they are. I assume *library first* (the shared vocabulary and lemma library is the product, with a Mathlib-like commons) and *method first* (the product is a documented methodology, an evidence format and a set of checkers, with the tools as a reference implementation). Section 11 is written against those two.
- **All command names, file layouts and sample output here are design sketches.** None is the tool's real output.
- **`rosette` is a placeholder name.** The collision with the Rosette solver-aided language has to be settled before anything is published to a package registry, because a registry name is permanent.

## The argument in brief

1. **A tool is the only form that forces the missing pieces to be built.** The inventory's certain needs 1, 2, 4, 6, 9 and 10 (Rust-side composition, generated harnesses, translator wired in, model-versus-Rust differential test, CI, packaging) are all things a team hits in its first hour with a tool. A library or a method can stay elegant without any of them.
2. **The tool must be useful before the translator works on the user's code.** Aeneas as shipped translates 1% of census functions, and only 9% compile with no unmodelled external. So the day-one product is rules compiled to tests and bounded checks on any Rust, with the proof as the top rung. That first rung does not exist yet (plan node E1).
3. **Frames ship with the tool as numbered editions, in the way a language ships editions.** Upgrading the tool never changes what a sentence means. Changing the edition is a deliberate, reviewed act.
4. **The form's weakness is real.** A green check compresses four evidence kinds into one bit, which is the thing the architecture says never to do. And the form pushes for stable interfaces on a design that is two days old with zero human signatures.
5. **My honest position:** this is the right *delivery* form and the wrong thing to *freeze* first. Ship the tool early as 0.x; do not call anything 1.0 until people have signed a vocabulary and taken the reader trial.

## 1. What it is, and what it is not

### What it is

> **rosette is a command-line tool and CI check for Rust teams that own decision logic.** You write a rule as one English sentence in a `.feature` file. The tool compiles it, from a bundled library of sentence shapes and your project's own vocabulary, into one fixed reading, prints that reading back, and then collects the strongest evidence it can that your code obeys it: the examples run on the compiled code, a generated property test, a generated bounded check, and, where the code fits the supported profile of Rust, a proof checked by Lean's kernel. Each rule gets a verdict and a list of what the verdict rests on, by kind. CI fails when a rule is shown false or when its evidence drops below the level your team declared for it.

### What it is not

- **Not a prover, a translator or a specification language.** It drives Lean, Aeneas, Charon, Kani, proptest and cucumber-rs, and adds the part they leave open: what the sentence means and what the answer rests on.
- **Not a proof of your whole program.** It covers rules about one pure call at a time. I/O, concurrency, time and anything outside the modelled functions are out of scope and are listed as such in every report.
- **Not free-form English.** A sentence built from unknown or ambiguous pieces is refused with a location. It is never guessed at, and no language model sits between the sentence and its meaning.
- **Not proof unless it says proved.** "Sampled" and "bounded" are reported under those names. Only a kernel-checked theorem of exactly the compiled statement is called proved, and even then "for all inputs of the model".
- **Not a substitute for someone reading the echo.** A verdict resting on vocabulary nobody signed is marked unreviewed, and the tool cannot make that review happen.

## 2. Why this form

**For.**

- **The repository is already shaped like a tool.** `clausal/run.sh` is one command with flags (`--strict`, `--no-rust`, `--no-adequacy`, `--no-heldout`), a report, a machine-readable graph, a sign-off command, a staleness computation and a lint. The checkers table has 20 automatic checks. What is missing is everything around the command: install, a second crate, a second platform, CI.
- **Adoption has a known shape.** Kani's pitch is "similar to testing, you write a harness". Size Limit's is a CI budget. The engineering lead that `positioning.md` recommends as primary audience knows how to evaluate a tool in an afternoon and does not know how to evaluate a method.
- **It answers "nobody else can run it today".** The inventory's item 10 is certain: macOS arm64 only, about 55 GB, four Lean toolchains, three Rust compilers. A project aiming at "the default" that one laptop can run has no claim yet.
- **It makes the reusable pieces load-bearing.** A bundled frame library that every installed copy compiles sentences against has many consumers by construction. Today it has one.

**Against, stated now so it is not buried.**

- **The tool's top rung does not reach real code**, and its lower rungs sit next to Kiro and plain proptest. Section 10, risk 1.
- **The project's best real-world result does not fit this form.** The TDFLite work is a hand-written Lean model of Go, checked by differential testing. A Rust CLI does not ship that.
- **It is the most expensive form to maintain**, on top of a nightly research translator. Section 9.

## 3. What ships

Status marks as in the inventory: EXISTS, PARTIAL, NEEDED.

### Packages

| Deliverable | What it is | Built from | Status |
|---|---|---|---|
| `cargo-rosette` | The command. A `cargo` subcommand, because the adopter already has `cargo` and nothing else | `clausal/run.sh`, `clausal/clausal/` (7,255 lines of Python) | PARTIAL. Works on two fixture crates through a shell script; no install path |
| `rosette-frames` (Lean) | Frame and modifier definitions, their decidable checkers, glue lemmas | `clausal/lean/Frames/` (643 lines, Lean core only) | EXISTS, under review, one consumer |
| `rosette-frames` (English) | Surface forms, echo templates, printed defaults, one file per edition | Today inside the slice's `clausebook.yaml` and `clausal/vocab.py` | PARTIAL. Must move into the same versioned unit as the Lean, or a signature covers half of what was read |
| `rosette-frames` (Rust crate) | An executable Rust reading of each frame, generic over an operation; what generated tests call | Nothing. The Rust side today is one hand-written cucumber step per old phrase | NEEDED. This is inventory need 1 and the biggest single build |
| `rosette-bdd` (Rust crate) | Runner glue: example rows, counterexample replay, generated proptest and Kani harnesses | `clausal/wallet-bdd/`, hand-written harnesses in `clausal/compare/arms/` | PARTIAL to NEEDED (plan node E1) |
| `rosette-bridge` (Lean) | Statement form, bridge lemmas, `Check` type, the audit | `clausal/lean/Bdd/` (388 lines; audit 180) | EXISTS; copied, not shared, into `p2/` |
| `rosette-lemmas` (Lean) | Loop and collection lemmas over Aeneas output | Three independent per-crate sets (ledger 328 lines, two P2 arms 806 and 846) | NEEDED. Raw material only |
| Proof-rung image | A container with the pinned Aeneas, Charon, the exact Rust nightly, Lean, the Mathlib cache and Kani | `clausal/translate.sh`, `docs/SETUP.md` | NEEDED. Without it the proof rung is not installable by anyone else |
| CI action | Runs the fast tier on every change, the proof tier on a schedule or label, posts the summary | Nothing; `.github/workflows/` is the stock Lean template | NEEDED (plan node X2) |

**Opinion on the Python.** The sentence compiler is 1,191 lines and the reporters about 2,500. I would keep the Python as the reference implementation behind a conformance suite (the 14 fixture rule lines, the refusals, the 5 held-out sentences) and rewrite the front end in Rust before 1.0, so that the day-one install is one `cargo install` with no Lean and no Python. I am not certain that is right: the README says one of Lean's attractions is that the tooling can live in the same language, and a Lean front end would shrink the trusted surface. But the day-one user has no Lean, and that decides it for this angle.

### Commands

| Command | Does | Needs installed | Today |
|---|---|---|---|
| `cargo rosette init` | Writes `rosette.toml`, `rules/`, a vocabulary skeleton, a bindings module, a CI workflow | cargo | NEEDED |
| `cargo rosette check` | Compiles every rule line; prints the echo or a refusal (unbound, ill-typed, ambiguous). Seconds | cargo | EXISTS as `vocab.py` and `newrules.py`; ambiguous refuses but shows no separating input |
| `cargo rosette test` | Example rows on compiled Rust, then a generated property test per rule | cargo | PARTIAL: rows exist for old phrases; generation NEEDED |
| `cargo rosette bound` | Generated Kani harness per rule, with the bound printed | Kani | NEEDED (hand-written today) |
| `cargo rosette prove` | Profile lint, translate, build, search, link, audit, replay | proof image | EXISTS on the fixtures; profile lint NEEDED; patched translator not wired in |
| `cargo rosette report` | Text, a brief form, JSON, and the evidence graph | cargo | EXISTS except the brief form; a rule block is about 45 lines today |
| `cargo rosette gate` | Compares verdicts with the declared floors and the lock file; sets the exit code | cargo | PARTIAL: `--strict` only |
| `cargo rosette sign` / `status` | Record a reviewer against a piece digest; show what is unsigned or stale | cargo | EXISTS as a mechanism; never used (0 of 87) |
| `cargo rosette vocab add` / `explain` | Add a domain word with its two readings; show a piece's definition, echo and examples | cargo | PARTIAL (documented by hand in `clausal/README.md`) |
| `cargo rosette edition diff` | Show what a frame edition change does to each rule and signature | cargo | NEEDED (plan node V9 underneath) |
| `cargo rosette selftest` | Negative controls that must fail; ten invalid graphs that must be rejected | proof image | EXISTS, outside `run.sh` |
| `cargo rosette mutate` | Mutation run: which injected bugs no rule shows false | proof image | EXISTS; 73 minutes on two toy crates, so nightly only |
| `cargo rosette recheck <bundle>` | Clean-room re-check of a released evidence bundle on another machine | proof image | NEEDED (plan node X3) |
| `cargo rosette doctor` | Versions, pins, the trusted base as installed | cargo | NEEDED |

### Documents

| Document | Status |
|---|---|
| Getting started: first rule in fifteen minutes | NEEDED |
| The frame reference: every frame with its English, its Lean, its defaults and separating examples | PARTIAL (`docs/VOCABULARY.md`, `out/prior_art_vocabulary.md`) |
| Writing Rust that translates | EXISTS (`census/PROFILE.md`, 16 rules) |
| Reading a report; what each evidence kind means | PARTIAL (`docs/ARCHITECTURE.md` 2, 5, 8) |
| Signing: who signs what | NEEDED; open in `docs/ARCHITECTURE.md` 15 |
| Gate policy: what turns the build red and who owns a lost proof | NEEDED; open programme question |
| Proof-writing guide for agents and people | NEEDED as one document; scattered today |
| The trusted base, per release | PARTIAL (`docs/ARCHITECTURE.md` 8) |
| Contributor guide | NEEDED. `AGENTS.md` describes a different project and names components that do not exist |

### Services

None at 1.0, on purpose. A hosted prover would mean taking custody of customers' security-critical source, and a hosted signing service would mean being an identity provider. The only hosted things are static: a release page, the container image, the frame reference, and a binary cache for the Lean build of the bundled libraries.

## 4. Who installs what, and the first day

### The ladder

The tool must give an answer at every rung, and say which rung it reached.

| Rung | Evidence | Works on | Install |
|---|---|---|---|
| 0 | The sentence compiles; the echo is printed | Any project | `cargo install` |
| 1 | Example rows pass on the compiled Rust | Any Rust | same |
| 2 | Generated property test, edge-weighted | Any Rust the bindings can call | same |
| 3 | Generated bounded check | Rust that Kani accepts, to a stated bound | Kani |
| 4 | Kernel-checked proof about the generated model | Rust in the supported profile | proof image |

This order follows the project's own measurement. In K2, edge-weighted property tests found 212 of 212 falsifiable pairs, Kani 209, the Lean model search 188, and no mutant was caught by proof alone. A tool that leads with rung 4 leads with its most expensive and least available evidence.

### People

| Person | Installs or touches | First day |
|---|---|---|
| Engineer on the team | `cargo-rosette`, later Kani | Runs `init`; writes six domain words and their Rust bindings; writes three rules; reads three echoes; sees one rule refuted with an input |
| Requirement owner (policy, product, security) | Nothing. Reads the echo in a pull request | Confirms or disputes one echo; signs a handful of one-line domain words |
| Whoever owns CI | The action and the image | Adds the fast tier to pull requests; schedules the proof tier |
| Proof author, person or agent | The proof image | Not on day one. Arrives when a rule is declared `requires = "proved"` |

### Day one, as a design sketch

```text
$ cargo rosette init
$ cargo rosette check
  rules/transfer.feature:3  A transfer for which the amount is not more than
                            the sender's balance is always accepted
    Reading   for every pair of wallets and every transfer whose amount is at
              most the sender's balance, the call returns and is accepted
    Uses      1 frame (always), 1 modifier, 3 domain words; 0 of 3 words signed
$ cargo rosette test
    REFUTED on the compiled code
    input     sender = 1, receiver = 18446744073709551615, amount = 1
    Rests on  meaning       unreviewed (3 unsigned words)
              evidence      sampled, 1 failing input, replayed
```

The rule line is real: it is in `clausal/features/wallet.feature` (line 135, tagged `@expect-refuted`, with two passing example rows beneath it). The failing input is as quoted in `readme-patterns.md` from today's report; `clausal/out/report.md` was not on disk when I looked (another agent's run was in progress), so I did not check it myself. The reading text, the command line and the layout are invented.

Note what the real rule line looks like. The scenario title under it says "A transfer the sender can afford always succeeds", which is what a person would write. The line that compiles is "A transfer for which the amount is not more than the sender's balance is always accepted". That distance is the writing problem in one example. The day-one moment to design for is that one: a plausible sentence, two passing examples, and an input that breaks it, inside fifteen minutes, with nothing installed but a cargo subcommand.

### What day one is today

Clone the repository on an Apple-silicon Mac, install four toolchains, run `./translate.sh --setup`, run `clausal/run.sh`, and read a report about a 45-line wallet and an 85-line ledger. It cannot be pointed at another crate. A new sentence gets a reading and a model search, and no verdict.

### The part of day one I am least sure of: bindings

A domain word has to be tied to the user's code. Today that is a Lean piece bound to an Aeneas model function, plus a Rust predicate per old whole phrase. For this form to work without the translator, the **Rust reading has to come first**: a small Rust function per domain word, typed as a measure, a condition, a collection or an operation by traits from the `rosette-frames` crate. The Lean reading is then needed only at rung 4, and there are two ways to get it:

- **Generate it** by passing the binding through the translator. Cheap for the user, but the "second independent reading" is gone: the two readings now share a source.
- **Write it by hand** and compare the two on generated inputs, as the phrase grid does today. Independent, but it puts Lean in front of the engineer.

I would generate by default, label the link "tool-trusted" in the report, and let a project opt into the independent reading for the words it cares about. That is a weakening of the current design and the owner should decide it deliberately.

**A second caution on day one.** Writing bindings is writing step definitions, which is the part of BDD that teams abandoned. And of the 14 fixture rule lines, 13 had to be reworded to compile, by the person who built the vocabulary. A stranger's first three sentences will be refused more often than not. `check` has to be fast, its refusals have to name the nearest known form, and the plan's "suggest mode" (V7) stops being optional.

## 5. Governing and versioning the reusable pieces

The model is not Mathlib. It is closer to **a language's standard library and editions**: a small core that ships with the tool, changes rarely, and never changes meaning under a project without the project asking.

### Four layers, four rules

| Layer | Where it lives | Who may add or change | Who signs | Version |
|---|---|---|---|---|
| Frames and modifiers (46 of 77 pieces today) | Bundled in the tool, in numbered editions | The tool's maintainers, through a public proposal | Two editors of different kinds: one for the English, one for the Lean. A project then *accepts* an edition | Edition number, independent of the tool version |
| Lemmas and bridge | Bundled Lean packages | Open contribution; the kernel checks them | Nobody. Kernel-checked | Follows the Aeneas pin; deprecation with a grace period |
| Domain packs | Not in 1.0 | (later) a named owner per pack | The pack's owner | Semantic versions, pinned to an edition |
| Project words and idioms | The project's repository | The project | The requirement owner for the English; a second person for the binding | Digest per piece in `rosette.lock`; stale when the bound code changes |

### What a frame must have to be admitted

Enforced by the tool's own CI, in the way a linter refuses a rule without tests:

1. A Lean definition over the abstract operation, with typed holes and no catch-all relation.
2. A decidable checker in Lean, by a different author, agreeing on generated inputs (today 23,700 of 23,700).
3. A Rust checker, agreeing with the Lean checker on a shared vector set.
4. A surface form, an echo template, and the text of every default it applies.
5. Separating examples against each neighbouring frame (if against only-if against exactly-when).
6. A set of weakened variants that the second reading must catch. The reviewer's 12 frame mutants are the start of this; I could not find the tally.
7. Reader evidence: the frame's items in the meaning-trial bank, with a result from people. **No frame can pass this today.**
8. Need shown in two unrelated systems. The existing "split on the second use" rule, promoted to an admission rule.

By that list the honest count for a first edition is not 23. It is the 19 frames reachable from a sentence, minus whatever the review in progress changes, and none of them passes item 7.

### Who signs, and what the signature means

- **Upstream signature.** Two named editors sign each frame's English against its Lean. It ships with the release as a signatures file over content digests. It says: "this definition is what the editors take the phrase to mean."
- **Project acceptance.** A project records which edition it accepts. That is a reviewed dependency decision, like accepting a licence. It does not claim that the project's people re-read 46 definitions.
- **Project signature.** The requirement owner signs each domain word and idiom. This is the only signature that needs a person who cannot read Lean, and the echo is what they sign against.
- **The report keeps the three apart.** "Meaning: frames edition 1, signed upstream by two editors; 3 of 3 project words signed by a named person; echo confirmed by the rule's author on a date." Not one word "signed".

### How a change propagates

- **Tool upgrade, same edition.** Meaning cannot change. The lock file's piece digests are compared; a mismatch is a tool bug and fails the run.
- **Edition revision that preserves meaning.** The new definition ships with a kernel-checked equivalence to the old one. Signatures carry over, and the report says they were carried by an equivalence proof. This is plan node V9 and it is not built.
- **Edition change that alters meaning.** `cargo rosette edition diff` lists every rule whose reading changes, shows old and new echo side by side, and where it can, an input on which they differ. Every affected signature is void and every affected proof is stale. Nothing is migrated automatically.
- **Old editions stay supported** for a stated number of releases. That is a real cost (section 9) and it is the price of not voiding strangers' signatures.
- **Project-local frames are allowed and are labelled.** A team that needs a shape the edition lacks can define one. The report marks it "local frame, not in any edition". Two unrelated projects carrying the same local frame is the trigger for a proposal.

### Where I would push back on the owner

- **"Kinship with Mathlib" should be claimed for `rosette-lemmas` only.** That layer is ordinary Lean, the kernel settles correctness, and refactoring is safe. The SymCrypt group has built tactics and libraries for the same job; contributing there may beat starting a second one. For frames, Mathlib's working attitude to compatibility would void every signature it touched.
- **A first edition should be small and boring.** Fewer frames, each with more evidence, beats 23 definitions with none.
- **Versioning is hypothetical with one consumer.** The edition machinery should be designed now and built when a second project exists. Building it first is the kind of work that looks like progress.

## 6. What 1.0 would have to contain

A 1.0 is a promise that sentences keep their meaning and that the commands keep working. Each line below is a condition, with what the inventory says about it.

| # | Condition | Today |
|---|---|---|
| 1 | A new sentence from known pieces gets a verdict on compiled Rust with no hand-written step | No. The largest gap; the 44-entry legacy glossary carries every proof and step |
| 2 | Property test and bounded check generated from the compiled rule; failing inputs fed back as rows and refutations | No (E1). 23 of each are hand-written |
| 3 | A generated differential test of the Lean model against compiled Rust on every proof run | No. One sample of 25 functions and 895 inputs |
| 4 | The translator that the census measured is the one in the chain: patches upstream, or the fork wired into `translate` | No. The slice runs the unmodified release; five reports prepared, none sent |
| 5 | A profile lint that says before translation why a function will not translate | No. The profile is prose |
| 6 | Frame edition 1: English and Lean in one versioned unit, admission checks enforced, two upstream signatures per frame | Mechanism exists; 0 signatures; English lives in the slice |
| 7 | The reader trial taken by people, and its result published whatever it is | No. 8 model readers, 0 people |
| 8 | Three external Rust crates the team did not write, end to end, with the failures listed | No. Two fixtures written to fit; no idiomatic Rust has met a frame |
| 9 | Linux x86_64 and macOS arm64; one install command for rungs 0 to 2; one image for rung 4 | macOS arm64 only |
| 10 | The CI action, and this repository gated by its own tool including the negative controls | No (X2) |
| 11 | Written gate policy and sign-off roles, used in anger at least once | Neither written |
| 12 | A shared lemma package covering the loop shapes seen so far, and a decision on how a loop is specified | No. Two rule statements rest on unsigned lemmas |
| 13 | A stable JSON result and exit codes, under a schema with a version | Graph schema v2 exists; coverage of rule groups unconfirmed (X1) |
| 14 | A clean-room re-check of a release bundle by someone else | No (X3) |
| 15 | Legacy glossary retired; one vocabulary, one statement per scenario | No |
| 16 | The numbers in the README generated from a run | No. 23 against 19 frames; 3, 4 or 5 patches; 34% against 35% |

**Suggested staging**, so something ships long before all sixteen hold:

- **0.1, "rules as tests".** Rungs 0 to 2 on any Rust. Conditions 1 and 2 (property tests only), 9 for the cargo part, 13. No Lean on the user's machine. This is the release that tests whether anyone wants the product.
- **0.2.** Rung 3; the gate; the CI action.
- **0.5.** Rung 4 from the image on profile crates, with conditions 3, 4 and 5.
- **1.0.** Everything above, and in particular 6, 7 and 8.

I would not let a date pull condition 7 out of 1.0. If people do not catch wrong echoes, the English layer turns an unreadable formal statement into a readable false sense of agreement, and a stable release would be distributing that.

## 7. What is deliberately excluded

- **The mathematics strand.** About 14,000 lines sharing only a graph schema with the chain. Its own repository, or its own page. The dead-code tool is the one piece with a plausible future here.
- **Code that is not Rust.** The hand-model chain used on Go stays a documented method, not a command. This excludes the project's best real-world result from the product, and I count that as a real loss (section 11).
- **Any language model inside the tool.** No suggest or interpret mode in 1.0, no bundled proof agent. `prove` reports which proofs are missing and calls a hook; the team brings its own author. The guide for that author ships.
- **A hosted service, accounts, a registry.** Section 3.
- **Domain packs.** Unproven with one domain. At most one experimental authorisation pack outside the stable surface.
- **Effects, I/O, concurrency, time.** Out by approach for now, and named in every report. An informed reader looks for these first.
- **The compilation link.** A stated assumption.
- **An auditor's view of the evidence.** The graph is published; no assessor-facing format is promised.
- **An editor plugin.** `check` is fast enough to run on save from a task; a language server waits for demand.
- **A new prover, translator, or test runner.** Wrapped, pinned, credited.

## 8. Staying honest about trust

A CI check is a compression machine, and the architecture says evidence kinds must never be folded together. This is where the toolchain form most needs rules against itself.

- **No single green.** The status line a pull request shows is a count by kind: "12 rules: 4 proved, 5 bounded to n=4, 2 sampled, 1 refused; 3 of 9 words unsigned". The tool offers no badge that says "verified".
- **Floors are declared per rule, in the repository.** `requires = "sampled" | "bounded" | "proved"`. The gate fails when a rule is refuted, or when it falls below its floor. A rule with no floor never fails the build for lack of a proof, and the report says it has no floor.
- **A lost proof is "not shown".** In K2, 92 of 295 lost proofs belonged to rules nothing showed false. So a lost proof fails the gate only where the floor is "proved", and the message says "proof lost, rule not shown false" in those words.
- **Unsigned is visible by default and fatal under `--strict`.** Today every verdict in the repository is formally "review". Shipping with `--strict` off by default is right for adoption and is also the path by which "unreviewed" becomes a warning everyone ignores. I would make the unsigned count part of the status line so it cannot scroll away.
- **"Proved" always carries "of the model".** With the translator version, the patch list and the standard-library models the proof touched, named in the report. Aeneas's models are untested by us and the report should say that until condition 3 holds.
- **Bounded says its bound.** Kani verified ledger rules only up to 2 to 4 accounts and 1 to 3 transfers.
- **The tool's own claims are checkable.** `selftest` runs the controls that must fail. `recheck` re-derives a bundle elsewhere. `doctor` prints the trusted base as installed.
- **Agents may not move the goalposts.** The gate fails if a change touches rules, vocabulary or the lock file together with proofs, unless a named person approved it. In the slice this is a written rule with no mechanical guard; in P2 it was enforced by hash.
- **Documentation shows real output only.** The current README's opening block says "all signed" where the real report says "0 of 5". A tool that sells evidence cannot have mock output in its own README.
- **Present tense for what installs today.** The release notes of each 0.x list which rungs work on a stranger's crate.

## 9. What it costs to maintain

I have no measured figures for any of this. The sizes are from the inventory; the effort judgements are mine and rough.

**The pin treadmill, which is the dominant cost.**

- Aeneas is a nightly research tool that pins its own Lean and Mathlib. Charon needs one exact Rust nightly. Kani brings another. One small crate currently needs three Rust compilers.
- Every Aeneas bump means: rebase five patches (334 lines) unless upstream took them; rerun its 122 extraction tests; rerun the census (about 20 minutes idle, about 20 GB of memory for Cedar); regenerate the profile, which is only valid for the pin it was measured on; rerun the soundness sample; rebuild the image; rebuild the Lean cache.
- Aeneas output changes break proofs. Users' proofs, not ours. A tool release that upgrades the translator can turn a customer's "proved" into "proof lost" with no change on their side. That needs a stated policy, and probably translator pins that move a few times a year, not nightly.

**The surface.**

- Two platforms at least, and Windows will be asked for.
- Three implementations of every frame (Lean definition, Lean checker, Rust checker) plus its English, kept in agreement.
- Supported old editions.
- A JSON schema and exit codes that CI systems depend on.

**The codebase as it stands.**

- About 7,255 lines of Python written by agents in two days, with no CI and timings taken under heavy load. Hardening it, or rewriting the front end, is most of a first release.
- `DECISIONS.md` is 1,122 lines and unindexed. `AGENTS.md` is stale. A contributor cannot start from either.

**The human parts.**

- An editor for the frame edition, with a second signer of a different kind. Small in hours, hard to staff.
- Support. Refusals are correct behaviour and are also the moment a user files an issue.

**My guess at the standing cost:** two full-time engineers for the tool and the pins, a part-time frame editor, and agent time for proofs and porting. I hold that loosely. If the Aeneas patches go upstream and the project can ride release tarballs, the first number drops. If the fork has to be carried with an OCaml toolchain in CI, it rises.

**What would cut the cost most:** sending the five prepared upstream reports. Two of them (ii and iv) account for all of the measured gain, 1,368 and 117 functions. This is the owner's step and nothing else on this page is as cheap.

## 10. The three biggest risks of this form

### Risk 1: the proof rung does not reach users' code, so the product becomes a property-test generator

- **Evidence.** 1% of census functions translate as shipped; 35% with patches, which is 82% of nine crates and none of the tenth; 9% with no unmodelled external. Loops cost about six lines of Lean per line of Rust and that did not fall across two experiments. No frame has met idiomatic Rust.
- **Consequence.** Most teams' rules would sit at "sampled" or "bounded" indefinitely. At those rungs the neighbours are Kiro, which says of itself "evidence of correctness, not a proof", and a property-testing library with no English at all. The differentiator left is the fixed reading and the echo, which is the untested part.
- **And the population may be small anyway.** `positioning.md` names its largest uncertainty: teams with Gherkin on the wall and teams with a pure Rust core worth proving may barely overlap.
- **What would tell us early.** Release 0.1 to five outside teams and count how many write a fourth rule.

### Risk 2: freezing too early, on a meaning link no person has tested

- **Evidence.** 0 of 87 vocabulary entries signed. 0 human readers. The frame library is under review with uncommitted fixes, and the committed `IfThen` may not be fail-closed. 13 of 14 rule lines needed rewording. Staleness and `--strict` have never been exercised.
- **Consequence.** A toolchain wants stable commands, a stable file format and a stable frame edition, because that is what adopters are promised. Every one of those would be frozen around a design whose central hypothesis is open. If people skim echoes and approve them, the tool ships a ritual.
- **The form makes this worse than the other angles do.** A linter's users do not read the rule definitions. This tool's safety depends on someone reading them, and the tool form trains people not to.
- **Mitigation.** Long 0.x; condition 7 gates 1.0; the owner signs the wallet and ledger vocabulary now, which costs an hour and exercises machinery that has never run.

### Risk 3: a product built on a research translator, maintained by very few people

- **Evidence.** One nightly pin; five unsent patches; a Charon failure on Cedar caused by a compiler regression days old; a standard-library model list that is generated at build time and cannot be extended without a rebuild; our only addition to those models is one six-line lemma.
- **Consequence.** The top rung's correctness and availability are decided upstream. A change there can break every user's proofs. If the Aeneas maintainers decline the patches or change direction, the project carries an OCaml fork for good.
- **Mitigation.** Treat the Aeneas team as the most important relationship the project has; send the reports; keep rungs 0 to 3 fully independent of the translator so the tool survives a bad quarter upstream.

## 11. What the other two angles would get right

As said at the top, these are my assumed readings of the other two.

### Library first

- **It puts the durable asset first.** If the project stops, a tool rots within a year of its pins. A reviewed set of frames with separating examples and reader evidence would still be citable, as Dwyer's patterns and EARS are.
- **It sets the right pace for frames.** A tool release cycle pushes for more frames per release. A library that calls itself a standard pushes for fewer, each better evidenced. On this, library first is simply right, and section 5 borrows its discipline.
- **It can have more than one consumer.** A frame library usable from Verus or Creusot specifications, or from Kiro-style workflows, has a wider reach than one bundled in our CLI. Bundling quietly makes us the only consumer again.
- **It fits the contributors who exist.** Formal-methods people will contribute lemmas and criticise definitions. They will not contribute to a Rust CLI.
- **Where it is weaker.** A library with one consumer and no installable tool has no users to tell it which frames matter, and the inventory already shows the failure: the English half of the library is not in the library.

### Method first

- **It matches the best evidence.** The strongest real result is on Go, by a hand model, differential testing, readings and rulings. That is a method, it is language-independent, and it produced 22 ambiguity questions the owner found useful. The toolchain form excludes it.
- **It is honest about maturity.** Two days old, proxy readers only, numbers that disagree between files. A methods paper with a reference implementation claims exactly as much as the evidence supports. A tool with a version number claims more.
- **Its checkers are the distinctive contribution.** The "failure each check prevents" table is the most original thing in the repository and it is tool-independent. The SymCrypt and FVS pipelines need the same checks.
- **It reaches assurance people and auditors,** who adopt what a standard names, not what a team installs.
- **It costs almost nothing to maintain.**
- **Where it is weaker.** Methods are adopted by the people who wrote them. "Formally modelled software by default" is not reached by a document, and the certain needs in the inventory are engineering, not writing.

### What I would take from each, even under this angle

- From library first: frame editions governed like a standard, published separately from the tool even though bundled with it, with the Lean and the English in one unit that other tools could consume.
- From method first: the evidence kinds, the verdict set and the checker list written as a specification the tool conforms to; and the hand-model chain documented in public on a non-sensitive target, so the project's best result is not hidden behind a Rust-only CLI.

## 12. If this angle were the README

The owner's link to awesome-readme was covered in `readme-patterns.md`; I did not re-read the list. Under this angle the README follows the checker pattern that note found in Size Limit, HTMLHint and Kani:

1. One sentence: what it is, for whom.
2. Real output: the refuted wallet rule, then the proved one, each with its "rests on" lines, including the "0 of 5 vocabulary pieces signed off by anyone" line that `readme-patterns.md` quotes from the real report.
3. A status line with numbers and the rung table, saying which rungs work on a stranger's crate. Today: none.
4. The five "is not" bullets.
5. Install and the first three commands. Until 0.1 exists this section says "read the committed report" and nothing else.
6. What is in the box: tooling, libraries, checkers, method, upstream changes, each with a status word.
7. The trusted base.

It would be a shorter README than today's, and it would look empty at the install step until E1 lands. That emptiness is the most accurate thing it could say.

## What I am unsure of

- **Whether rungs 0 to 2 alone are a product anyone wants.** This angle depends on it and nothing here tests it.
- **The binding design in section 4.** Rust-first bindings with a generated Lean reading give up the independent second reading by default. It may be the wrong trade.
- **Rewriting the front end in Rust.** Argued from the day-one install; it throws away two days of working Python and may not be worth it before the grammar settles.
- **The maintenance estimate.** A guess.
- **How much a frame edition would really need to change.** With one consumer there is no data; the review in progress is the first instance.
- **Whether a team will ever turn `--strict` on.** If not, the meaning link is decorative in practice.
- **What the other two angles actually are.**
