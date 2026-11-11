# Final form, angle 1: library first

Brainstorm for the owner, 2026-11-10. Not for publication. This file argues one angle as hard as the evidence allows: **the product is a shared, versioned, reviewed library of typed pieces, and every tool exists to serve it.** Where the angle is weak I say so in place, and the last section says what I would not follow.

**Basis and limits.** I read `README.md`, `docs/ARCHITECTURE.md`, `docs/RESULTS.md`, the Stance and Status sections of `docs/PLAN.md`, `brainstorm/inventory.md`, `brainstorm/positioning.md` and `brainstorm/readme-patterns.md` in full, and looked at `slice/vocabulary.yaml` (header) and `slice/lean/lakefile.toml`. I took the diagram notes from their summary only. I ran nothing and did not read `private/` or `tdflite-ideas/`. All package and command names below are placeholders; "Rosette" already names a well-known solver-aided language, so the library needs its own name anyway. I was not told what the other two angles are; I assume "tool first" (a command you point at a crate) and "method first" (a documented method and evidence standard, independent of language).

## The argument in six lines

1. Proof text is becoming free, and the pipeline scripts are 7,255 lines of Python that an agent can rewrite in a week. Neither is an asset.
2. What cannot be regenerated is a definition that people have read, tested against a second reading, and signed. That is the only thing here whose value grows with use.
3. So the library is the product. Its unit is not a Lean definition; it is a **piece**: definition, English form, echo, executable reading, Rust reading, test evidence and signatures, versioned as one thing.
4. "In the manner of Mathlib" is right for the kernel-checked half (lemmas, models) and wrong for the meaning half (frames), which must change slowly like a wire format. The library needs two tiers with opposite change rules.
5. The repository does not yet contain this library. It contains one consumer, no signatures, no shared lemma set, and the English half of every frame in the wrong place. Library first is a statement of destination, and the first six steps are extraction work.
6. My honest verdict: this is the right description of the long-run asset and the wrong thing to ship first. A library with no consumers needs a tool to create them.

## What it is (as this angle would write it)

> A shared library of reviewed building blocks for stating what software must do. Each block is one small idea, such as "never changes", "the total of" or "only if", defined once in Lean, paired with the exact English that reaches it, an independent executable reading, and a record of who has checked that the two mean the same. A plain-English rule is compiled from these blocks, never interpreted whole, so a new rule needs no new definitions and no new trust beyond the blocks it uses. Beneath the blocks sit kernel-checked lemma libraries that make the proofs cheap. Like Mathlib, the value accumulates in the library and the second user pays less than the first. Unlike Mathlib, the part that carries meaning is checked by people, because no kernel can check what an English phrase means, so that part is small, changes rarely, and says of every block what evidence stands behind it. Today: 23 definitions, one consuming project, no signatures.

## What it is not

- **Not a prover, a translator or a test framework.** It uses Lean, Aeneas, Charon, proptest and Kani as shipped and says which it had to work around.
- **Not a library of true statements.** A frame is a definition a person vouches for, not a theorem a kernel checked. A signature records that someone read it; it does not make it right.
- **Not an interpreter of free English.** A sentence outside the vocabulary is refused. Nothing is guessed.
- **Not a vocabulary for your system.** Words such as "account" and "transfer" are bound to your code, by you, in your repository. The library ships the shapes and, at most, starter packs for settled domains.
- **Not a statement about the compiler, the hardware, or code outside the model.** Effects, concurrency and time have no frames, and the library says so on its front page.

## What ships

### The unit: a piece

Today a frame is a Lean definition in `slice/lean/Frames/`, an English form in the slice's `vocabulary.yaml`, a parser rule in `slicegen/vocab.py`, and a checker in `Frames/Check.lean`. A signer reads the English and the Lean together, so shipping them apart means a signature covers half of what was read. The first deliverable is therefore a format, not code.

| Part of a piece | Exists today | Gap |
|---|---|---|
| Lean definition with typed holes | Yes, 23 definitions, Lean core imports only | Review fixes uncommitted; `IfThen` may not be fail-closed |
| English surface form and echo template | Yes for 19 of 23 | Lives with the slice, not the library; 4 two-run frames have none |
| Executable second reading | Yes, 23,700 of 23,700 agree | Written by the same builder; should have a different author |
| Rust reading (for tests, Kani, differential check) | **No** | The largest gap; without it a piece gives a statement and no evidence on compiled code |
| Separating examples and definition mutants | Partly: 12 reviewer mutants, tally not written up | No required minimum |
| Reader-trial items for this piece | 54-item bank, wallet and ledger only | Hand-written echoes, model readers only |
| Signatures against a digest | Mechanism exists | 0 of 87 |

### Packages

| Package | Contents | Tier | State |
|---|---|---|---|
| `frames` (Lean, no Mathlib, no Aeneas) | The abstract operation, frames, modifiers, their English, echoes and executable readings | Meaning | Extractable now: 643 lines, own Lake library already |
| `frames-rs` (Rust crate) | The Rust reading of every piece; the generic property-test and Kani harness bodies | Meaning | Not built |
| `aeneas-loops` (Lean) | Loop-shape and collection lemmas over Aeneas's `loop.spec_decr_nat`; `@[step]` specs | Kernel-checked | Not built. Raw material: 227 + 806 + 846 lines in three per-crate sets |
| `aeneas-bridge` (Lean) | Statement form, bridge lemmas, `Check` type, audit helpers | Kernel-checked | Exists in `slice/lean/Bdd/`, copied (not shared) into `p2/` |
| Standard-library models | Lean models and `step` lemmas for unmodelled `std` items | Kernel-checked, **upstream** | Our contribution so far is one six-line lemma |
| `pack-authz`, `pack-ledger` | Starter domain vocabularies for settled domains | Meaning, per-owner | Not built; the bet I am least sure of |
| Conformance corpus | Feature files, mutants, negative controls and expected verdicts that any implementation of the compiler must reproduce | Test data | Exists as fixtures: 35 scenarios, 45 + 52 mutants, 27 controls |

**Push-back on two of the five named pieces.** Standard-library models cannot ship as our package: Aeneas generates its model list at build time, so adding one means a rebuild of the translator. They belong upstream, and our deliverable is a differential test suite for them. Loop lemmas are in the same position by choice: the SymCrypt authors already build Lean libraries on Aeneas, and a second commons would split a small community. If both go upstream, as I think they should, "our" library is about fifty definitions, their English and some packs. That is worth having, and it is a pattern catalogue with evidence attached, closer to Dwyer's patterns or EARS than to Mathlib. The kinship claim should be made about the whole stack, including what we give to Aeneas, not about the part we own.

### Commands (the tool, in service of the library)

| Command | Purpose | Today |
|---|---|---|
| `rule check` | Compile, echo, search, link, audit, report | `slice/run.sh`, fixtures only |
| `rule echo <sentence>` | Reading or refusal, no build | Inside `slicegen/vocab.py` |
| `piece lint` | Refuse a piece missing any part of the table above | Not built; this is the Mathlib linter idea and the cheapest governance there is |
| `piece sign`, `piece card` | Record a signature against a digest; print the evidence card | `slicegen review` exists, unused |
| `vocab lock`, `vocab upgrade` | Pin piece digests per project; report what an upgrade does to each rule | Staleness exists in `graphlint.py`; lock and upgrade do not |
| `corpus rerun` | Re-parse every registered project's sentences against a proposed change | Not built; see versioning |

### Documents

- **Frame reference**: one page per piece with its English, defaults, Lean, a separating example and its evidence card. This is the library's front door and what a non-Lean reader actually adopts.
- **Contribution and signing policy** (does not exist; `docs/ARCHITECTURE.md` section 15 lists it as open).
- **Evidence kinds**: the fixed meaning of kernel-checked, tested, tool-trusted, human-asserted.
- **Rust profile** (`census/PROFILE.md`, exists) and a **proof-writing guide** (scattered across three files today).
- **Readings and rulings method** for ambiguous guarantees, with a public worked example. The only worked example is private.

### Services

Almost none, deliberately. A static index of packs in a git repository, and the reader-trial page (already a single offline file in `trials/meaning/`) hosted so volunteers can take it. No hosted prover, no accounts. A library that needs a server to be trusted has moved its trust to the server.

## Who adopts what, and day one

| Adopter | Installs | Day-one experience this form aims at | Honest state |
|---|---|---|---|
| Lean and Aeneas user | `require frames` in a lakefile (seconds; no Mathlib) | States their own theorems with shared frames; gets the executable reading and non-vacuity checks for nothing | Possible within days of extraction. This is the only adopter who can act now |
| Engineering lead with a Rust decision core | `frames-rs` and the CLI | Writes three rules from the frame reference, gets an echo and a generated property test and Kani harness on their own crate, no translator | Not possible. macOS arm64 only, about 55 GB, four Lean toolchains, and no Rust readings |
| Requirement owner or signer | Nothing; reads a page | Reads a piece's card, takes a ten-minute trial, signs | Mechanism exists, never used |
| Pack author | `frames` and the lint | Binds domain words, runs the lint, publishes with a named owner | Not possible |
| Agent builder | CLI | A rule file the agent may not edit, refusals that say what to change | Rules exist as written policy; enforced by hash only in P2 |

The weakness is plain in that table: the adopter the library can serve today is the one who needs the English layer least.

## Governance and versioning

### Two tiers, opposite rules

| | Kernel-checked tier (lemmas, bridge, models) | Meaning tier (frames, modifiers, their English) |
|---|---|---|
| What settles correctness | The kernel | Nobody; evidence from second readings and readers |
| Who may add | Anyone; one reviewer; lint passes | Proposal with two unrelated consuming projects ("split on the second use", promoted to policy) |
| Change policy | Mathlib-style: refactor freely, deprecate with a grace period | Append-only. A piece is never edited in place and never deleted |
| Pinned to | One Aeneas release, hence one Lean and Mathlib | Nothing but Lean core; built in CI across every Lean version a consumer uses |

### Identity is the digest, not the version number

The existing mechanism already binds a signature to a digest of the entry and its Lean text. Keep that as the identity of a piece and treat the package version as a label for a set of digests. Three classes of change:

| Class | What changed | Effect on signatures | Check |
|---|---|---|---|
| **E**, equivalent | Lean definition, with a shipped theorem `old ↔ new` | Carried, recorded as "carried by theorem X", not as re-signed | Kernel (plan node V9, not built) |
| **T**, text | English form or echo template | Reader evidence for that form is void; formal signatures stand | People. **No kernel check is possible, and V9 does not cover this case** |
| **M**, meaning | Anything else | New piece id; the old piece stays, marked superseded | A separating input is shipped with the change |

### Adding is not safe either

A grammar is not conservative under extension. A new surface form can turn a sentence that had one parse into an AMBIGUOUS refusal in someone else's project. So "minor version means additive" is false for this library, and Mathlib's remedy (everything builds together in one repository) is not available because consumers live elsewhere. The substitute is a registered corpus of consumers' rule files, re-parsed on every proposed change, in the way the Rust project runs proposed compiler changes across published crates. Idioms make this worse: the fixtures already carry 10, every fixture scenario uses one, and each is another English claim. I would keep idioms out of the shared tier entirely.

### Who may sign

- **Formal signature**: a named person who reads Lean attests the definition matches the reference description. Two for a core piece, from different organisations. At the start there is one organisation, so early signatures should be labelled provisional and say why.
- **Reader evidence**: not a signature. A trial result with an interval, by human readers, per English form. Model readers are recorded as instruments and never count.
- **Domain signature**: the system's owner, for pack and project words only.
- **Authorship label**: agent-authored proposals are disclosed, as Mathlib requires, and the second reading must come from a different author than the definition.

### How a change reaches a project

A project commits a lock file of piece digests. `vocab upgrade` reports, per rule: unaffected; carried by equivalence; reading changed, with the separating input; or newly ambiguous. Nothing upgrades silently, and because pieces are append-only a project can stay on its lock indefinitely. The cost is that superseded pieces accumulate for ever, which is the right cost for a signed vocabulary.

## What 1.0 would have to contain

I would not call it 1.0 on less than this. Each line is checkable.

1. **The 14 catalogue frames**, every one reachable from a sentence (4 of 23 definitions are not today) and every one with a Rust reading.
2. **Every core piece signed by two people and backed by a human reader trial** with its interval published. Today: 0 signatures, 0 human readers.
3. **Three consumers compiled, not judged by reading**: the fixtures, the P2 inventory crate ported from its old glossary, and one external crate from the census that the builder did not write. The "83 of 85 TDFLite readings expressible" figure is a judgement and private; it cannot count publicly.
4. **Sentences written by someone other than the vocabulary's builder.** The 5-of-5 result was the builder's own sentences, and 13 of 14 rule lines had to be reworded to compile.
5. **One executed upgrade drill** of each class (E, T, M) across two projects, plus one corpus rerun that catches a seeded ambiguity.
6. **Generated property test, Kani harness and model-versus-Rust differential check** from the Rust readings (plan node E1, with inventory needs 1, 2 and 6). Without this a piece yields no evidence on compiled code.
7. **A factored loop-lemma library with a measured effect**: a fourth crate proved at clearly less than six Lean lines per Rust line. I do not know that this is achievable; if it is not, that is a finding about the library thesis and should be reported as one.
8. **The Aeneas patches sent upstream**, or the fork wired into the chain. Today no modified tool is in the end-to-end path, and two of the five patches do all the measured work.
9. **The old 44-entry glossary retired.** It still carries every proof and every cucumber step.
10. **CI with the negative controls, a clean-room re-check, and Linux packaging.**
11. **Either one domain pack used by two unrelated codebases, or the pack idea dropped from the 1.0 claim.**

## Deliberately excluded

- A new prover, translator or solver, and any hosted proving service.
- Free-English interpretation; suggest and interpret modes stay outside the trusted path.
- Frames for effects, concurrency and time. Out because no target has forced a definition, and a frame nobody has used twice fails its own admission rule. The front page must say that real defects live there.
- Project domain words in the shared tier, and idioms.
- The mathematics strand, except possibly the dead-code tool.
- The Go hand-model route as tooling. It stays a documented method; the library does not pretend to cover it.
- Certification claims of any kind.

## How it stays honest about trust

- **Every piece carries an evidence card** printed in the reference and in every report: who signed which digest, reader-trial rate with interval and reader count, definition mutants killed, consumers. An unsigned piece says UNREVIEWED, as today.
- **A release states its own counts** ("14 frames, 9 signed by two people, 6 with human trial data"). No release note may say "verified".
- **Carried signatures are distinguished from fresh ones**, so equivalence proofs cannot quietly age a review.
- **The second reading is described as what it is**: it catches a definition wrong in one place, not one wrong the same way in both.
- **The specific danger of this form is authority.** "It is in the standard library" will be read as "it is correct". Mathlib earns that reading from the kernel; this library cannot. A popular frame with a subtle defect would be wrong in every project at once, and the review in progress has already found a likely one (`IfThen`). The defence is the card, and the habit of printing the reading beside every verdict.

## What it costs to maintain

These are guesses and should be read as such.

- **Meaning tier: low in hours, high in people who are hard to find.** A few dozen definitions need an editor for perhaps a day a week. The real cost is reader trials, since every new English form needs fresh human readers, and a second formal signer outside the owner's organisation. Neither can be bought with agent time.
- **Kernel-checked tier: the recurring bill.** It is pinned to an Aeneas nightly, which pins Lean and Mathlib (about 7 GB a copy). Every translator bump means rebuilding and repairing lemmas. Agents can do the repair, as P2 suggests, but someone must own the red build, and the red-build policy is unwritten.
- **Corpus reruns and CI**: machine time, plus triage when a change breaks a consumer.
- **Fork carrying**, until upstream takes the patches: OCaml 5.3 and opam on every build machine.
- **Governance itself.** A constitution, roles and a change process for a library with one author and one consumer is overhead ahead of need. I would write the rules as one page and expect to rewrite them when a second organisation appears.

## The three biggest risks of this form

**1. A library of one.** Reuse is asserted by construction ("46 of 77 shared by design") and observed nowhere. One consumer, two toy crates written to fit, sentences written by the builder. If the second and third consumers each need new frames or reworded English, the library is a project-local vocabulary with a grand name. The worst version: domain packs turn out not to be shareable, and the reusable core is fifty definitions.

**2. The meaning evidence never arrives.** The whole content of the meaning tier is human-asserted adequacy, and there are no humans in the record: 0 signatures, 0 human readers, a 93% proxy result whose interval reaches below its own target. If people skim echoes and approve, a signed library converts an unreadable formal statement into readable false agreement, and gives it institutional weight.

**3. The valuable half is hostage to upstream.** The lemma and model layers are worth something only while Aeneas translates the code, and it handled 1% of census functions as shipped. Five patches are prepared and none sent; standard-library models cannot be added without a rebuild; four Lean toolchains run side by side. If Aeneas changes its loop encoding, the lemma library is rewritten. A library first project that does not control, or closely co-operate with, its translator has a product it cannot keep building.

## What the other two angles get right that this one gets wrong

**Tool first.**
- **Value on day one.** K2 found that no injected bug needed a proof and that edge-weighted property tests found 212 of 212 falsifiable pairs. A command that turns a sentence into a failing input on real Rust is useful before any library exists. Library first offers a first-time visitor a catalogue to read.
- **Consumers come from tools.** Nobody adopts a vocabulary; they adopt a command that happens to use one. Mathlib had Lean users before it had governance.
- **The next piece of work is tooling either way.** Rust-side composition and generated harnesses are what make a piece yield evidence. Library first has to build them and then call them servants.
- **It does not freeze early.** Frames are still being corrected. Standard-like stability applied now would lock in definitions with no reader evidence behind them.

**Method first.**
- **The best real result used no library.** The TDFLite work was hand-written Lean, 85 readings not expressed through frames, and its most useful output was 22 ambiguity questions and the owner's rulings. That is a method.
- **The most credible asset is the checkers.** Each exists because a reviewer found the failure it prevents. They are discipline, portable to any prover or language, and they are what a formal-methods reader will respect first.
- **It is not tied to Rust or Aeneas**, so risk 3 does not touch it.
- **It is honest about what kind of thing a frame catalogue is**: a small set of patterns with a way of testing them, which needs an editor and a document more than a community.

## Where I would not follow this angle

- I would not lead publicly with "a Mathlib for requirements". State the kinship in one sentence with its limit attached, as the positioning note recommends.
- I would not write the governance before the second consumer exists. Do the cheap things that exercise the machinery now: extract `frames` with its English into one unit, have the owner sign a few dozen pieces provisionally, port the P2 crate through the frames, and build `piece lint`.
- I would treat lemma and model work as contributions to Aeneas's ecosystem first and our package second.
- I would let the tool lead adoption and keep the repository library-shaped underneath, so that when a second project arrives the pieces are already the unit of versioning.

## What I am unsure of

- Whether a factored loop-lemma library lowers proof cost at all. The six-lines figure held across two experiments, and the only evidence that lemmas recur is that two models proved the same seven textbook loops.
- Whether class T changes (English only) can be governed in practice. Every wording improvement costs a new reader trial, which may mean the English never improves.
- Whether the corpus rerun is workable when the consumers that matter most are private.
- Whether authorisation vocabulary is shareable across engines. Everything about packs rests on it and nothing has tested it.
- Whether upstream would accept loop lemmas or models from this project; nobody has asked.
- All cost estimates above.
