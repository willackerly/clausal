# Clausal

**A formal-English specification language—100% valid Gherkin—that dual-compiles to Rust BDD tests and Lean 4 proofs over the code you ship.**

Code generation and formal proof synthesis are getting dramatically cheaper. **Knowing what was actually proved is now the bottleneck.** An AI agent—or a well-meaning engineer—can write a thousand lines of Lean 4 tactics that pass the kernel while quietly proving a weakened precondition, a vacuous edge case, or the wrong state transition. To a product owner, security reviewer, or compliance officer who does not read dependent types, a proof of the wrong statement looks identical to a proof of the right one.

**Clausal** is a strict, compositional dialect of Gherkin (`features/*.feature`) where every English sentence carries **one fail-closed mathematical and executable meaning**. Composed interactively from **the Clausebook**—an **ever-growing public library of typed, human-signed vocabulary pieces** shared across projects—a single **Clausal** `.feature` file executes today via `cucumber-rs` and `proptest` on your compiled binary, and compiles via **the Clausal compiler** (`clausal` / `cargo clausal`) into unbounded **Lean 4 kernel proofs**.

![Clausal: formal-English Gherkin dual-bound to Lean proofs and Rust tests](docs/diagrams/how-it-works.vector180.svg)

Apache-2.0 · [Architecture](docs/ARCHITECTURE.md) · [Vocabulary](docs/VOCABULARY.md) · [Schema](docs/SCHEMA.md) · [Results](docs/RESULTS.md) · [Plan](docs/PLAN.md) · [Handoff](docs/HANDOFF.md) · [State of Play](#state-of-play--roadmap)

---

## What it looks like

Two unrelated systems write their rules in the same language. Each binds its own nouns and functions once; the logical words ("never changes", "always", "only if") come from **the Clausebook** and mean the same thing in both.

### Example 1: a ledger (`clausal/wallet`, `clausal/ledger`)

These are real rules and real verdicts from the pipeline in [`clausal/README.md`](clausal/README.md), run against Rust code with state transitions and batch loops. A verdict answers one question: **is this sentence true of the code that ships, for every input?**

| Rule, as written in the `.feature` file | True of the shipped code? | Verdict | What the verdict tells you |
|---|---|---|---|
| `A transfer never changes the total of all balances` | **Yes** | **Proved** for every input | Money is neither created nor destroyed by a transfer, whether the transfer is accepted or rejected. Checked by the Lean 4 kernel, and run on the compiled Rust. |
| `A batch never changes the total of the ledger's balances` | **Yes** | **Proved** for every input | The same holds across a loop over any number of accounts and transfers, including batches that stop or roll back part-way. |
| `A transfer for which the amount is at most the sender's balance is always accepted` | **No** | **Refuted**, with the input `sender = 1, receiver = u64::MAX, amount = 1` | The requirement was wrong, not the code: it forgot that the receiver's balance can overflow. The hand-written example rows all passed. The counterexample is replayed on the compiled Rust, so it is a fact about the program, not about a model. |
| `A computation of the total is always accepted` | **No** | **Refuted**, with balances that sum past `2^64 - 1` | The same kind of finding: a sentence that sounds safe and is false at the edge. |

A **Refuted** verdict is the tool doing its job. Each one is a sentence someone would have signed, shown false by a concrete input before anyone relied on it. The alternative outcomes are worse: the rule is quietly weakened until a proof goes through, or it stays in a document nobody checks.

The other direction works too. When a bug is put into the Rust (45 machine-generated mutations of the two crates), some rule is shown false with a concrete input for 45 of 45.

A third outcome, a sentence the compiler declines to read at all, is described in [Architecture](docs/ARCHITECTURE.md#composition-and-refusal).

### Example 2: access-control key release (TDFLite, an early adopter)

TDFLite is an attribute-based access control server in which every decision gates the release of a cryptographic key. Its guarantees use the same core words as the ledger, with a domain pack (`clausebook/abac`) for its own notions. **The pack is not built yet, so the sentences below are planned wording, not compiled rules.**

| Planned rule | Core pieces reused | Need addressed |
|---|---|---|
| `A key release is accepted only if every attribute of the data is satisfied by the subject under its rule` | `only if`, `accepted` | Fail-closed authorisation across `anyOf`, `allOf` and hierarchical levels |
| `A key release never loses acceptance when the subject gains an entitlement` | `never loses acceptance when` | More entitlements never remove access; where that is false, the counterexample is a concrete request |
| `A key release gives the same answer when only the order of the attributes differs` | `gives the same answer when` | No dependence on the order of attributes in a token or manifest |
| A malformed or unrecognised attribute name is always rejected | `always rejected` | Silent normalisation and prefix-spoofing at intake |

What has been done: a Lean model of the production Go engine's decision logic was checked against the engine on about 400,000 generated cases, and testing its plain-language guarantees surfaced 6 known edge cases and 15 further divergences. A verified Rust core is in progress.

---

## Vision, `GOAL`, and Formal `SCOPE`

To avoid blurring steady-state language and platform goals with today's research-prototype baseline, this document separates **`GOAL`** (what **Clausal**, **the Clausebook**, and **the Clausal compiler** are being built to deliver) from **`SCOPE`** (the formal boundaries and public reuse model they operate under), and inventories current completion at the bottom under [**State of Play & Roadmap**](#state-of-play--roadmap).

### Vision

Establish an open, human-readable **formal-English specification language (`Clausal`)** that policy owners, auditors, and engineers can read directly—and that compilers, fuzzers, and theorem provers can check mechanically—by compounding **human-reviewed meaning**, **executable BDD**, and **kernel-checked proof automation** in a shared public commons (**the Clausebook**).

### `GOAL` (Target Language, Library & Compiler)

1. **The Language (`Clausal`) — Readable English That Cannot Drift:** Teams stipulate `Rule:` and `Scenario:` claims in `features/*.feature` using `clausal compose` (interactive CLI / LSP). Every **Clausal** sentence is valid Gherkin syntax, and its defaults are strict: a claim covers every call, accepted or rejected, unless the sentence narrows it. Tests and proofs share **one exact text**.
2. **The Standard Library (`Clausebook`) — Compounding Public Meaning:** Need addressed: formalising requirements from scratch in every codebase does not scale. Projects import—and contribute back to—**the Clausebook**, a versioned public catalogue of logical frames, modifiers, domain packs (`clausebook/ledger`, `clausebook/abac`, `clausebook/quota`), Rust BDD/property adapters, and companion `@[step]` Lean lemmas. Signing off a shared **Clausebook** entry once amortizes semantic review across every organization and rule that uses it.
3. **The Toolchain (`clausal` / `cargo clausal`) — Graded Verdicts Over Shipping Code:** Point the **Clausal compiler** at a profiled Rust crate (extracted to Lean 4 via Charon + Aeneas) or a polyglot production service (checked via differential oracle testing against a proved Lean reference model) to grade every **Clausal** rule in CI:
   - **Proved for every input** (`clausal prove`: checked by the Lean 4 kernel over the code model, audited against vacuity and custom axioms),
   - **Checked within stated bounds** (`clausal test`: `cucumber-rs` scenarios, high-count `proptest` fuzzing, or bounded `Kani` bit-vector checks on the compiled binary, with sample counts and unwind bounds printed),
   - **Refuted with a concrete counterexample** (replayed on both the Lean model and the compiled binary to confirm the bug or over-broad rule is real), or
   - **Refused as unbound or ambiguous** (never guessed by an LLM or silently approximated).

### `SCOPE` (Formal Boundaries & Explicit Trust Model)

- **In `SCOPE` — Deterministic Decision, State, and Policy Cores:** Authorization and attribute-based access control (ABAC) engines, financial ledgers and accounting invariants, quota/rate-limit state machines, canonical binary/wire validators, and cryptographic key-release guards.
- **In `SCOPE` — Open Language & Multi-Project Reuse:** **Clausal** `.feature` grammar, shared **Clausebook** combinators (`Frames.Op`), typed modifiers, domain clause packs, dual Lean/Rust bindings, and reusable Lean 4 proof automation published as content-hashed packages.
- **Explicitly Bounded — The Meaning Gap:** No theorem prover can mathematically prove that prose matches the intent inside a human's head. **Clausal** *shrinks, isolates, and closes* that gap at authoring time: `clausal compose` builds explicit, fail-closed sentences exclusively from signed **Clausebook** pieces conformance-tested across Lean and Rust.
- **Explicitly Out of `SCOPE` (Stated in Every Report, Never Hidden):** Distributed network liveness, wall-clock side channels, `rustc`/LLVM miscompilation, and CPU/hardware faults. Every verdict report logs compiler and ISA execution as explicit assumptions, listed beside the result.

---

## Architecture

Four mechanisms carry the claims above. Each is listed with the gap it addresses; the design in full, with its weak points, is in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

| Mechanism | Gap addressed |
|---|---|
| 1. A closed loop of five links from intent to running binary | A requirement, its tests, its formal statement and the code drift apart when each is a separate document |
| 2. The Clausebook, a composer and a compiler that refuses | English is ambiguous, and a language model translating English to logic can be confidently wrong |
| 3. Evidence in four graded tiers | Proof is expensive, tests are cheap, and one green mark hides which of them a result rests on |
| 4. A self-audit that treats every proof as adversarial | An agent asked for a passing build can weaken the statement or prove something else |

### 1. The five-link loop

**Gap addressed:** a prose policy, a test suite, a hand-written formal specification and the code are four artefacts that drift apart.

Human intent enters from the left as a Clausal sentence, and the shipping Rust enters from the right. They meet at an unbounded Lean 4 kernel proof above, and at tests, fuzzing and counterexample replay on the binary below. One sentence is the input to all of it.

![The Clausal five-link loop: intent from the left, Rust from the right, verdict at center](docs/diagrams/chain.vector180.svg)

| # | Link in the loop | Artefacts connected | Mechanism | Evidence class |
|---|---|---|---|---|
| **1** | **Clausal Composition** | `Domain Intent` → `Clausal (.feature)` | Interactive composer (`clausal compose` / LSP) turns rough rules into canonical, fail-closed **Clausal** sentences built from signed **Clausebook** pieces—so steady-state BDD runs the formalized sentences directly | `human-asserted` |
| **2** | **Statement Compilation** | `Clausal (.feature)` → `Lean Statement` | Typed `Frames.Op` **Clausal compiler** (zero raw `Prop` escape hatches) + allowlisted Lean equivalence audit (`reading ↔ stmt`) | `kernel-checked` |
| **3** | **Kernel Proof & Spec Audit** | `Lean Statement` ↔ `Lean Code Model` | Unbounded Lean 4 kernel proof over pure extracted/reference functions + automated audit gates against `sorry`, custom axioms, vacuity, and trivial-Then specs | `kernel-checked` |
| **4** | **Model Extraction** | `Rust Source Code` → `Lean Code Model` | **Route A (Rust):** Charon + patched Aeneas MIR extraction (`tool-trusted`). **Route B (Go/C++/Polyglot):** Proved Lean reference oracle paired with differential fuzzing | `tool-trusted` |
| **5** | **Dual-Bound BDD & Replay** | `Clausal (.feature)` + `Running Binary` ↔ `Lean Code Model` | Executes `.feature` `Scenario:` steps via `cucumber-rs` (`#[given]`, `#[when]`, `#[then]`) and `Rule:` invariants via `proptest` on the compiled binary, plus **witness replay** confirming the binary and Lean model agree *(with `rustc` + ISA logged explicitly as `assumed`)* | `tested` *(+ `rustc`/ISA `assumed`)* |

### 2. The Clausebook, the composer and the compiler

**Gap addressed:** controlled languages are easy to read and hard to write, and free translation from English to logic by a language model cannot be trusted.

Sentences are built from typed, signed pieces. A composer helps an author reach a sentence the book permits; a deterministic compiler turns that sentence into both targets, or refuses.

![The Clausebook: typed pieces that make Clausal dual-bind to Lean and Rust](docs/diagrams/vocabulary.vector180.svg)

- **100% Valid Gherkin Surface + `clausal compose`:** Every **Clausal** file is syntactically standard `.feature` Gherkin—highlighted by GitHub/IDEs and runnable by Cucumber runners out of the box. `clausal compose` guides authors slot-by-slot through signed **Clausebook** frames, modifiers, and local nouns; when a rough draft is ambiguous (e.g., all calls vs. accepted calls only), it generates a concrete separating witness and writes the chosen canonical **Clausal** sentence straight into `features/*.feature`.
- **Inside the Clausal Compiler (`clausal` / `cargo clausal`) — Zero LLM Guesswork, Dual Targets:** No language model writes the logic. The compiler slot-checks every phrase against **the Clausebook**'s algebraic sorts (`Op σ α ρ`, `Measure σ α V`, `Cond σ α`, `AnswerClass ρ`, `Variation σ α`), refuses unbound or ill-typed sentences, and emits **both** a fail-closed Lean 4 `Frames.Op` theorem (`clausal prove`) and executable Rust `cucumber-rs` + `proptest` harnesses (`clausal test`) locked together by a Lean-vs-Rust conformance grid check:

![Inside the Clausal compiler: one Gherkin sentence, dual formal and executable targets](docs/diagrams/compiler.vector180.svg)

- **Dual-Governance Scaling ("Creative Commons for Meaning, Mathlib for Lemmas"):** Meaning pieces in **the Clausebook** are content-hashed (changing semantics requires either a Lean kernel proof of `↔` preserving downstream sign-offs, or a new hash); `@[step]` proof lemmas cannot alter theorem statements and grow freely gated only by the Lean 4 kernel.

### 3. Graded evidence

**Gap addressed:** a team should not need a proof to get started, and a result should say which kind of evidence it rests on.

Proof is the ceiling, not the entry ticket. On the mutation benchmarks ([`clausal/compare/e1/E1_TRADES.md`](clausal/compare/e1/E1_TRADES.md)), generated property tests and bounded checks caught every injected bug that hand-written tests caught, in seconds. Proofs add what no sample can: a result for every input and every collection size.

![The Clausal compiler turns one .feature rule into four graded tiers of evidence](docs/diagrams/evidence.vector180.svg)

One **Clausal** `.feature` rule drives all four tiers—starting with `cargo test` (`cucumber-rs` + `proptest`) on any Rust crate on day one, without needing Lean open, and climbing to unbounded Lean 4 kernel proofs on critical cores—while replaying any failing witness across both the Lean model and the compiled binary.

### 4. Self-audit

**Gap addressed:** proofs, loop invariants and bindings may be written by autonomous agents, and an agent asked for a passing build may get one the wrong way.

The audit ([`clausal/lean/Bdd/Audit.lean`](clausal/lean/Bdd/Audit.lean) and [`clausal/lean/Bdd/AuditLinks.lean`](clausal/lean/Bdd/AuditLinks.lean)) treats every proof and binding as adversarial until checked. Each row below is a failure a reviewer actually found, and the gate that now stops it.

| Way a result could be hollow | Audit gate | Outcome |
|---|---|---|
| Agent leaves `sorry`, `admit`, or custom `axiom` in a helper file | `collectAxioms` walk over transitive constant closure; permits only Lean's standard axioms (`propext`, `Quot.sound`, `Classical.choice`) | Proof rejected |
| Agent proves `theorem rule_name : True` or a subtly altered type | Kernel comparison of declared theorem type against the exact compiled **Clausal** statement constant | Proof rejected (standing control `c1`) |
| Agent smuggles a proof of `stmt` inside the `reading ↔ stmt` equivalence | Constant-closure allowlist inspection ensuring equivalence uses only frame/vocabulary definitions, never target theorems | Marked `UNLINKED` (control `c30`) |
| Contradictory preconditions make `Given → Then` vacuously true | Automated witness search + kernel-checked `.sat` theorem proving at least one valid state/input satisfies the `Given` | Flagged `VACUOUS` |
| Weak `Then` clause passes a broken no-op or reject-all stub | Suite-adequacy check testing compiled **Clausal** rules against trivial mutations (`no-op`, `reject-all`, `constant`, `identity`) | Flagged `TRIVIAL-SPECS` |
| Implementation or Clausebook piece edited after review/proof | SHA-256 content digests across `.feature` rules, Clausebook entries, Rust MIR, and Lean outputs in `out/graph.json` | Downstream verdicts marked `stale` |

---

## Core Design Principles

1. **One language, one `.feature` file, zero drifting middlemen.** Stipulate unambiguous rules in **Clausal** at authoring time so steady-state BDD and Lean 4 execute and prove the exact same words.
2. **Models propose; kernels and binaries dispose.** Language models are welcome to suggest **Clausal** drafts, Rust implementations, loop invariants, and Lean tactic scripts—and trusted for none of them.
3. **Fail closed in prose and in logic.** Unbound words are refused (`UNBOUND`). Universal words (`always`, `never`) cover both accepted and rejected calls unless explicitly narrowed in the **Clausal** sentence itself.
4. **Meaning scales with the Clausebook, not rule count.** Sign off composable **Clausebook** pieces once (with Lean + Rust bindings); write hundreds of **Clausal** rules across repositories with zero new semantic primitives.
5. **Never collapse orthogonal evidence into one green badge.** Human semantic sign-off (`1`), kernel statement & proof checks (`2`–`3`), model extraction (`4`), binary BDD/fuzzing (`5`), and compiler/ISA assumptions are reported separately—and negative empirical results are published honestly in [`docs/RESULTS.md`](docs/RESULTS.md).

---

## State of Play & Roadmap

Everything above marked `GOAL` is the target **Clausal** + **Clausebook** language and compiler platform. Here is the exact, reproducible inventory of what runs in this repository today (the code and directories were renamed to `clausal` on 2026-11-11; the repository and its checkout are still named `lean-rosette`) versus what remains to be built.

### Working Today (Reproducible Now)

- **The pipeline ([`clausal/README.md`](clausal/README.md)):** one command compiles `.feature` rules and scenarios for a declared list of projects (three today: `wallet`, `ledger`, and a small `counter` added to show a third project needs no change to the core book), translates the Rust through Charon and a patched Aeneas into Lean 4 (`v4.35.0`), runs the rules and scenarios on the compiled Rust, generates property tests and bounded `Kani` checks from each rule, and audits every proof. Current run: 39 scenarios and 60 rule statements, each at its expected verdict (34 rules proved for every input, 21 refuted with a concrete input, 3 tested only, 2 refused). Of 45 machine-generated bugs in the Rust, a rule or scenario is shown false for 45; 49 of 49 negative controls behave as expected.
- **The Clausebook, split and checked ([`clausal/clausebook/`](clausal/clausebook/)):** 122 entries in five books: a core of frames, modifiers and defaults that builds with no reference to any project, a ledger pack, and one local book per project. Every accepted wording lives in a book, and `clausal book check` enforces one live form per piece per position. The compiler refuses a rule that is unbound, ambiguous, or true of any code at all ("says nothing"). **No entry is signed by a person yet.** Agent loop proofs were measured earlier ([`p2/RESULTS.md`](p2/RESULTS.md): two models each proved 7 of 7 loop functions unaided, about 6 Lean lines per Rust line).
- **Patched Rust-to-Lean translator (`census/fork/`):** five small patches raise clean function translation across a 10-crate census from 1% to 35% (82% outside one outlier crate; [`census/fork/FORK.md`](census/fork/FORK.md)); the patched translator is now what the pipeline uses, pinned by hash. A probe of `libsignal-protocol` ([`census/signal/`](census/signal/)) found none of its three entry points translate.
- **TDFLite Production Policy Validation (Stage 1 — Route B):** Built a pure Lean 4 specification and executable evaluator for TDFLite's ABAC key-release core; matched the production Go implementation across ~400,000 differential inputs while surfacing 6 known edge cases and 15 additional divergences.
- **Lean Proof Structure & Dead-Code Tooling (`Rosette/`, `tools/deadcode/`, `tools/reinvent/`, `tools/families/`):** Companion research strand analyzing proof modularity across Mathlib, PFR, Carleson, and a 95,123-constant machine-generated Navier–Stokes Lean corpus—shipping a general dead-code analyzer verified across 3 projects (`M8`), a library re-invention detector (`M7`), and documented negative results on size-ratio lemma scoring ([`out/FINDINGS.md`](out/FINDINGS.md)).

### Not Built Yet (Closing the `GOAL`)

- **A composer that works (`clausal compose`):** in the blind authoring trial ([`trials/sentences/RESULTS.md`](trials/sentences/RESULTS.md)), **0 of 48 rules written by authors who had not seen the vocabulary compiled as written**. A first rule-based composer exists and every sentence it prints compiles, but on those 48 its top suggestion matched the author's intent for only 5, with 20 wrong readings, and it never declines to answer ([`clausal/COMPOSE.md`](clausal/COMPOSE.md)). A second version is being designed. `clausal separate`, which finds a concrete input on which two candidate readings differ, works.
- **Leaving the toy crates:** proving an external open-source Rust crate end to end and replaying its commit history, and completing TDFLite's verified Rust decision core with its `clausebook/abac` pack.
- **People in the loop:** no Clausebook entry is signed by a person, and comprehension trials (92% catch rate by model readers on the earlier echo design) have not been taken by people. Sign-off of the core book, a redesigned trial, and strict-by-default staleness are next.
- **Packaging and trust:** a standalone `clausal` / `cargo clausal` CLI and a public `clausebook` registry; a record of who vouches for what (people, models, specialists, external proofs), with each project choosing whose word it accepts; rule packs for recurring situations such as validated input.

### Build-Out Priority Order (Phase 2)

1. **Authoring:** composer version 2, measured on fresh sentences; readable wording, tested on people before any second form is admitted.
2. **People and real code:** the owner signs the core book and strict mode goes on; an external crate end to end; the access-control core to completion.
3. **Release:** standalone `clausal` CLI and public **Clausebook** registry `0.1`; the mathematics strand moves to a companion repository, cross-linked.

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
cd clausal && ./run.sh      # runs the end-to-end vertical slice; report in clausal/out/report.md
```
