# Final form, angle 3: standard and method first

Brainstorm for the owner, 2026-11-10. Not for publication. This file argues one angle as hard as honesty allows, then says where it is wrong. It rests on `brainstorm/inventory.md`, `brainstorm/positioning.md`, `docs/SCHEMA.md`, `docs/ARCHITECTURE.md` and the plan; I ran nothing and did not read `private/` or `tdflite-ideas/`.

I was not told what the other two angles are. I assume **tool first** (a product an engineering lead installs) and **library first** (a Mathlib-like commons of frames and lemmas). Section 10 depends on that guess.

"RES" below is a placeholder name for the specification. A standard cannot be called Rosette: the name belongs to a well-known solver-aided language, and a name collision costs a standard more than it costs a tool.

## The verdict up front

- **The argument for this form is real.** The durable assets in this repository are definitions: what "never changes" means, what PROVED FOR ALL INPUTS requires, what the four evidence kinds do and do not guarantee. The code is the replaceable part. `clausal` is 7,255 lines of Python written by agents in two days, and an agent can write it again.
- **As a public posture today it is premature, and I would not announce it.** There is one implementation, one consumer of the frame library, no human signature and no human reader. A standard published in that state is documentation of one tool's behaviour under a grander name.
- **As an internal discipline it is the right one now.** Write the normative documents, build the conformance suite, and make the clean-room verifier (plan node X3) a second implementation that shares no code with the first. That costs little, and it is what keeps the option open.
- **My recommendation:** ship as tool first, build as standard first, and call it a standard only on the day a second party implements any part of it.

## 1. What it is, and what it is not (as this angle would write them)

**What it is.** RES is an open specification for saying what software must do and what the evidence for it is. It fixes four things: a format for behavioural rules written in restricted English and for the typed vocabulary they are compiled from; a small catalogue of statement shapes ("never changes", "only if", "exactly when") with one fixed meaning each; a format for the graph of evidence behind a verdict, in which every link is labelled kernel-checked, tested, tool-trusted or human-asserted; and the words a tool may use for a verdict, with the checks it must have made before using them. A conformance suite tests implementations, and a written method says how to apply it to a codebase. This repository is the reference implementation, for Rust through Aeneas and Lean. Status: draft 0, one implementation, two small example crates, no vocabulary piece signed by a person.

**What it is not.**

- **Not a verifier.** It defines what a verifier must report. Proofs come from Lean, bounded checks from Kani, samples from proptest.
- **Not a guarantee that a conformant tool is right.** Conformance is tested on a finite suite, and by the specification's own vocabulary that is "tested" evidence.
- **Not natural-language understanding.** A sentence either compiles one way from known pieces or is refused. Nothing is guessed.
- **Not a standard in the institutional sense.** No standards body, no second implementation, no certification credit. It is a draft with a change process.
- **Not tied to Rust, Lean or Gherkin in principle, and tied to all three in practice today.** The only other route exercised is a hand-written model of Go code checked by differential testing.

## 2. What ships

### Documents (the product)

| Deliverable | Contents | Made from | State today |
|---|---|---|---|
| **RES-1 Rules and vocabulary** | The Gherkin profile (what `Rule:`, a Scenario Outline and Examples rows mean); the vocabulary file format; piece kinds and hole categories; the six printed defaults (D1 to D6); the three refusals (UNBOUND, ILL-TYPED, AMBIGUOUS) and what each must show; what an echo must contain | `clausal/clausebook.yaml` header, `docs/VOCABULARY.md`, `clausal/DESIGN.md` 14 | Exists as design notes and one YAML file with the format described in a comment block. Not a specification |
| **RES-2 Frame catalogue** | The 14 catalogue frames and the shared modifiers. Per frame: English surface forms, echo template, prose semantics, reference Lean definition, executable reading, separating examples, reader-trial evidence | `clausal/lean/Frames/`, `out/prior_art_vocabulary.md`, the frame half of `clausebook.yaml` | 23 Lean definitions exist, under review with uncommitted fixes. The English half is not with the library. 4 definitions have no surface form. No reader evidence |
| **RES-3 Evidence graph** | Node and edge model, the four evidence kinds, the two built-in rules (meaning and translation links never carry kernel-checked evidence; `binds` carries only human-asserted), computed staleness, the sign-off record | `docs/SCHEMA.md`, `clausal/schema/refinement-graph.v2.schema.json`, `graphlint.py` | The most finished part. Version 2 exists and rejects ten invalid graphs. Rule groups and layered evidence (X1) not confirmed closed |
| **RES-4 Verdicts** | The eight verdicts of `docs/ARCHITECTURE.md` 5, each with the checks required before a tool may print it; "a lost proof is not a detection"; "review, not pass, on unsigned vocabulary" | Architecture 5 and 7, `Bdd/Audit.lean` | Exists as a table and as audit code. The required checks are not yet written as requirements on any tool |
| **RES-5 Conformance** | Conformance classes and levels, the suite, how to claim conformance | See below | Not written |
| **Method handbook** | Rules for experiments; readings and rulings for ambiguous guarantees; the hand-model route for non-Rust code; sign-off roles; red-build policy; proof-writing guide for agents; how to carry a translator patch | `docs/PLAN.md` "Rules for every node", Architecture 12, `census/fork/FORK.md`, `p2/base/TASK.md` | Seven practices written; sign-off roles, red-build policy and "how a loop is specified" are not; the proof guide is scattered; the only worked example of readings-and-rulings is private |

### Conformance classes

Three classes, so a tool can implement one part:

- **Reader.** Sentence plus vocabulary in; reading, echo and applied defaults out, or the right refusal.
- **Producer.** Emits an evidence graph and verdicts. Levels by strongest evidence produced: T (tested: rows and sampling), B (bounded checking), K (kernel proof). The levels are the ladder that `positioning.md` asks for.
- **Verifier.** Takes a released bundle and recomputes every verdict from the evidence, without trusting the producer.

### The conformance suite

Most of it already exists as this project's self-checks, which is the best evidence for this angle:

| Suite part | Tests | Source in the repository |
|---|---|---|
| Sentence corpus with expected reading or refusal | Reader | 14 rule lines, 35 scenarios, 5 held-out sentences, `features/negative.feature` |
| Frame vectors: inputs on which each frame holds or fails | Any implementation of a frame, in any logic | The executable readings in `Frames/Check.lean` (23,700 evaluations agree today); the reviewer's 12 frame mutants |
| Graphs that must be rejected | Producer, Verifier | The ten invalid graphs in `clausal/schema/selftest.py` |
| Liar tests: a proof of `True`, a `sorry`, a vacuous Given, a trivial Then, an unlinked proof | Producer K, Verifier | The checks in `Bdd/Audit.lean`, each traced to a real failure; the 27 negative controls |
| Wrong-echo items | Reader's echo, with human readers | `trials/meaning/items.json`, 54 items, 18 unfaithful |

### Packages and commands (the reference implementation)

| Package | What it is | From |
|---|---|---|
| `res-frames` | Lake package, Lean core only: definitions, executable readings, glue lemmas, and the English forms and echo templates in the same versioned unit | `clausal/lean/Frames/` plus the frame entries of `clausebook.yaml` |
| `res-read` | The Reader: `res read <feature> --vocab <file>` | `clausal/vocab.py`, `newrules.py` |
| `res-run` | The Producer for Rust, Aeneas and Lean: `res run`, `res run --strict` | `clausal/run.sh` and the rest of `clausal` |
| `res-check` | The Verifier: `res check <bundle>`, `res check --what-if <node>` | `graphlint.py`, the independent audit in `p2/score/audit.py`, `leanchecker` replay. Plan node X3; not built |
| `res-conformance` | Runs the suite against any implementation through a small command contract | `schema/selftest.py`, negative controls |
| `res review` | Records a sign-off against a digest | `python3 -m clausal review` |

### Services

None at 1.0. A static page listing each frame with its version, definition, echo and evidence is enough. A hosted registry or signing service is a commitment to run something indefinitely, and nothing in the evidence justifies it.

## 3. Who adopts what, and their first day

| Adopter | What they take | Day one | Honest state |
|---|---|---|---|
| Engineering lead with a decision core | The reference implementation. The standard is invisible to them except that every label in the report links to a public definition | Writes one rule, sees the echo, gets a refutation or "tested only" | Works only on code written to fit: macOS arm64, about 55 GB, three Rust compilers. A new sentence gets no verdict |
| Builder of an agent or spec-driven pipeline | RES-1, RES-2 and the Reader class | Runs the sentence corpus against their own parser in an afternoon; adopts the echo and the refusals so an agent cannot quietly weaken a rule | Plausible and untested. Nobody has asked for it |
| Maintainer of another verifier (Verus, Kani, Dafny, an Isabelle route) | RES-2 frame vectors, RES-3, RES-4 | Encodes three frames in their logic, runs the vectors, emits a graph the Verifier accepts | The frames exist only in Lean. Vectors cannot pin a universally quantified meaning, so a non-Lean encoding is "tested equivalent" at best |
| Auditor or reviewer | `res check` and RES-3 | Recomputes the verdicts of a bundle on their own machine; reads the "rests on" block against a public definition of each kind | X3 is not built; no auditor-facing view exists (inventory section 6, item 16) |
| A second language through a hand model | Method handbook, RES-3, RES-4 | Follows the four steps of Architecture 12 and reports the model link as tested | Done once, on Go, and the worked example is private |

**Pushback on my own table.** Only the first row is a person who exists today, and that person adopts a tool. The other four are the reason to have a standard and none of them has been observed. This is the angle's central weakness.

## 4. Governance and versioning of the reusable pieces

Follow the four layers in `positioning.md`. The standard governs the first directly, sets the format for the rest, and owns none of the content below the first.

### Core frames and modifiers (normative, in RES-2)

**Who may add one.** Anyone may propose. A frame enters the catalogue only when all of these are present, and a linter refuses it otherwise:

1. Two unrelated systems need it (the existing "split on the second use" rule, promoted to policy). Today no frame meets this: the library has one consumer.
2. A Lean definition importing Lean core only.
3. An executable reading written by a different author from the definition.
4. Surface forms and an echo template, in the same versioned unit.
5. Separating examples: for each neighbouring frame, an input where the two differ.
6. Wrong-echo items for the trial bank, and results from human readers.
7. A statement of which defaults it applies.

**Who may sign one.** Two signers of different kinds: one who reads only the English and the examples, one who reads the Lean. An editor merges. Agents may author and may not sign; the schema already rejects a non-human author on human-asserted evidence.

**What a version is.** A frame is identified by a digest over its Lean definition, surface forms, echo template and defaults. Three kinds of change:

| Change | Requirement | Effect on downstream signatures |
|---|---|---|
| Formal side only, meaning preserved | A kernel-checked equivalence with the previous definition, shipped in the release (plan node V9, not built) | Carried forward automatically, with the equivalence recorded as the evidence |
| English side (surface form or echo wording) | Re-run of the reader trial for that frame | Void. No proof can show two English sentences mean the same |
| Meaning | New frame identifier; the old one deprecated and never redefined | Old signatures stay valid for the old frame; projects migrate rule by rule |

**How a change reaches a project.** A project pins a catalogue version in a lock file. `res upgrade --what-if` lists every rule, proof and signature that would go stale, using the staleness rule already in `graphlint.py`. Equivalence certificates clear most of the list; the rest is a named re-signing job for a named person.

**What I am unsure of.** Staleness has never run in anger because nothing is signed, and `docs/SCHEMA.md` says it over-approximates. The scheme above is design, not experience. The frame review happening now (the fail-closed `IfThen` question) is the first real instance and would be a good first test.

### Lemmas and standard-library models

Not in the standard. They are kernel-checked, so they need Mathlib-style contribution and free refactoring, and their natural home is upstream Aeneas. The standard says only how a report must list the hand-written models a verdict rests on.

### Domain packs and project words

The standard defines the file format and the sign-off record and nothing else. Owners are named per pack or per project. A domain pack for authorisation is the first one worth trying, after 1.0.

### The specification itself

One editor. Changes by written proposal with a reason and an undo, which is the existing `DECISIONS.md` habit. A normative change needs a conformance test that distinguishes old from new behaviour. No compatibility promise before 1.0.

## 5. What "1.0" would have to contain

I would refuse the label until every line is true:

1. **Two implementations of the Reader and two of the Verifier that share no code**, both passing the suite. An agent-written second implementation counts only if it was built from the documents alone, by an agent that never saw `clausal/`. That is cheap and is also a test of whether the documents are complete.
2. **A second Producer route reported in the public format**: either a Kani-and-proptest Producer at level B that needs no translator (plan node E1, and inventory items 1, 2 and 6), or the hand-model route on a public, non-sensitive target.
3. **A frozen catalogue of about 14 frames**, each with all seven admission items, including human reader results. Zero frames qualify today.
4. **At least one vocabulary signed by a person**, with one frame change taken through the upgrade path so that staleness, `--strict` and signature carry-forward have each run once for real.
5. **A second real codebase** not written to fit (plan node S1), with its refusals and translation failures published.
6. **RES-3 at a version that validates rule groups, suite adequacy and layered evidence**, with a standard attestation envelope for sign-offs in place of ad hoc JSON.
7. **A clean-room re-check on a second platform**, and CI that runs the suite and the negative controls. The current workflows are the stock Lean template.
8. **One set of numbers.** Today the documents disagree on frames (23 or 19 or 14), patches (three, four or five) and coverage (34% or 35%). A specification that cannot count its own frames will not be trusted.
9. **The methodology gaps closed**: sign-off roles, red-build policy, how a loop is fully specified, and one public worked example of readings and rulings.

Realistically this is a 0.x series for a year or more. Items 3 and 4 need people, and people tests are deferred by the owner's stance.

## 6. Deliberately excluded

- **How proofs are found.** Tactics, agents, prompts and lemma libraries are implementation matters. The standard says only what counts as a proof.
- **The translator.** Aeneas, the five patches and the Rust profile belong to the reference implementation. The standard requires that the translation link be named and its evidence kind stated.
- **Free English, and any reading produced by a language model without a refusal path.**
- **Time, concurrency, and effects around a pure core.** Frames describe one pure call. Excluding these means excluding where real defects live, and the document must say so in its first page.
- **Any claim of certification credit.**
- **A hosted service, an editor plug-in, a package registry.**
- **The mathematics strand**, except that the graph format should not prevent it. `maths_fit.py` on 11 nodes is a fit test and no more.
- **A numeric trust score.** The four kinds are unordered by design, and a standard is where pressure for a single number will arrive first.

## 7. How it stays honest about trust

A standard helps honesty in one way and endangers it in another.

**The help.** The words get fixed, public meanings. Today "proved" means whatever each tool's README says. RES-4 would make PROVED FOR ALL INPUTS mean: a kernel-accepted theorem whose type is exactly the generated statement, standard axioms only, conditions shown satisfiable, reading linked to statement. Each clause is there because a reviewer found the failure it prevents. That list is the most valuable thing this project has produced, and a specification is the natural place for it.

**The danger.** A label is only as good as the weakest tool allowed to print it. Rules I would write in:

- **Conformance is "tested", and the claim must say so**, with the suite version and digest. The specification applies its own vocabulary to itself.
- **No self-certified K level.** A Producer's kernel-checked claims count only when a Verifier that shares no code has recomputed them. `p2/score/audit.py` is the precedent.
- **A report must print the trusted base in full**, including hand-written library models and the audit code, with sizes. (The architecture document says the audit is about a hundred lines; it is 180. The specification should require the number to be generated.)
- **"Human-asserted" cannot be enforced by a schema.** A `human:` prefix is a string. The specification should say that plainly and require a signed attestation, and still admit that it proves who signed and not that they read.
- **An unsigned verdict is "review".** The reference implementation's own reports say this on every verdict today, and the standard's front page should carry that count: 0 of 87.
- **Publish the suite's blind spots.** The second reading catches a definition wrong in one place and not one wrong the same way in both. Frame vectors cannot establish a universal meaning.

## 8. What it costs to maintain

Estimates, low confidence.

| Item | Cost | Recurs |
|---|---|---|
| Writing RES-1 to RES-5 from existing material | Three to five weeks of editing by one person with agent help; most content exists as design notes | Once |
| Editor of the specification and catalogue | A few hours a week when quiet; every frame proposal is a real review | Continuous |
| Reader trials with people | The scarce resource. Per frame and per English form: tens of readers, recruited, with the key kept away from the item author | Per frame and per wording change |
| Conformance suite | Grows with every review finding; each normative change needs a test | Continuous |
| Reference implementation | The larger cost by far: every Aeneas pin change regenerates the profile, re-runs the census and re-pins Lean and Mathlib; five patches to carry or upstream; packaging beyond one platform | Continuous |
| Second implementations for 1.0 | Days if agent-built from the documents; unknown if a real second party | Once, then per change |

The standard does not remove the cost of the tool. It adds an editor and a trial programme on top. Anyone who hopes "standard first" is the cheap form is wrong; it is the form with the smallest code liability and the largest people liability.

## 9. The three biggest risks of this form

**1. A standard nobody implements.** Standards succeed when they codify what several parties already do, and this one would codify what one two-day-old prototype does. The neighbours (Kiro with EARS, FRET, SARIF, in-toto) have institutions and users; this has neither. The likely outcome is a well-written specification with one implementation, which is a README with section numbers. The fallback is still worth having: even unadopted, the documents and suite make the reference tool more trustworthy. The mistake would be to market the fallback as the goal.

**2. Freezing the wrong things.** Everything that would be frozen is still moving. The schema went from version 1 to version 2 inside two days because version 1 accepted 7 of 8 broken graphs. The frame definitions are being changed by a review as I write. 13 of 14 rule lines had to be reworded to compile, which says the sentence forms are far from natural. No person has read an echo. Standardising before the human trial risks fixing an English layer that people skim and approve, which `positioning.md` rightly calls worse than no English layer.

**3. The standard displaces the work that would make it worth adopting.** The inventory's "certain" list is Rust-side composition, generated tests and harnesses, a first signature, the translator in the chain, and a second real codebase. None is specification work. A project of this size that spends its next month on normative prose will have a better description of a chain that still gives a new sentence no verdict. A further cost: conformance levels invite teams to stop at level T and call themselves conformant, which gives Kiro's result with more ceremony.

## 10. What the other two angles get right that this one gets wrong

**Tool first gets right:**

- **Adoption follows a result on the user's own code.** The best first experience in this repository is a plausible rule refuted with a concrete input (sender 1, receiver at the u64 maximum, amount 1). That is a tool doing something, and no document produces it.
- **The binding constraint is engineering.** 1% of real functions translate as shipped; a new sentence cannot run on compiled Rust. A tool-first project fixes these because its users hit them. A standard-first project can describe them accurately forever.
- **Formats harden correctly only under use.** The checks in Architecture 7 each came from a reviewer attacking a running pipeline. More running, on more code, is where the next ten come from.

**Library first gets right:**

- **The owner's instinct that the pieces are the product.** What accumulates across projects is the frames with their English, and the loop lemmas. A specification of a format accumulates nothing by itself.
- **The proof-cost problem is a library problem.** Six lines of Lean per line of Rust, unchanged across two experiments, with lemmas over half of the hand-written Lean. A shared lemma library, probably contributed to Aeneas, is the only thing here aimed at that number. The standard excludes it by design.
- **Contributors exist for it.** Formal-methods people will contribute lemmas and models. Nobody has a motive to contribute to a specification.

**What this angle gets right that they do not.** It is the only one that treats the reference implementation as replaceable, which is the correct assumption when agents write code. It is the only one that gives the frame layer the governance it needs: `positioning.md` already concluded frames need the change discipline of a standard, because no kernel checks meaning and free refactoring would void signatures. And it is the only one in which a second prover or language is anything but a fork.

## 11. What I would actually do

1. **Do not announce a standard.** Keep the README tool-shaped, with a scope table (tooling, libraries, method, checkers, not yet, upstream changes).
2. **Adopt three standard-first disciplines now, because they are cheap and improve the tool:**
   - Move the frames' English into the same versioned unit as their Lean (inventory section 2: "half a library").
   - Write RES-4 as requirements. It is a two-page document and the project's strongest content.
   - Build X3 as a Verifier that shares no code with `clausal`, and package the existing negative controls as a suite it must pass.
3. **Run the one cheap experiment that tests this angle.** Give a fresh agent only the draft documents and the sentence corpus, and have it build a Reader. Every place it has to guess is a hole in the specification, and the result says whether "several implementations" is real.
4. **Revisit the label when a second party, human and external, implements or consumes any part.** The Aeneas or hax teams emitting the evidence graph, or an agent pipeline adopting the Reader, would each be enough.

## What I am unsure of

- **Whether a second implementer will ever exist.** This decides the whole angle and I have no evidence either way.
- **Whether frame meaning can be made prover-neutral.** I proposed executable readings plus vectors as the neutral definition. That may be too weak to be worth calling a standard, and a Lean-only normative definition may be the honest answer.
- **Whether signature carry-forward by kernel-checked equivalence is sound as a social matter.** The signer agreed to an English sentence and a definition; a proof that a new definition is equivalent keeps the formal half, and I think that is enough, but the owner should decide.
- **The cost figures in section 8.** The reader-trial cost in particular is a guess; no human trial has run.
- **The state of X1.** I did not run the lint, so I do not know whether schema version 2 validates today's graph.
- **What the other two angles actually are.**
