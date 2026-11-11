# Positioning and audience

Brainstorm for the owner, 2026-11-10. Not for publication. Sources were opened on that date unless marked otherwise.

Marks used: **[opened]** I read the page; **[search]** a search-engine summary only; **[memory]** from my own recall, not checked today; **[prior]** taken from `out/prior_art_vocabulary.md` in this repository, which records its own checks.

## Conclusions first

1. **The cell "structured English requirement, kernel-checked proof about implementation code" is empty.** I found nothing in it. Its neighbours are all occupied and well funded: structured English with property tests (Kiro), structured English with model checking of a design (FRET), free English with a solver (Bedrock Automated Reasoning), formal specification with a kernel proof of real Rust (the SymCrypt work on Aeneas).
2. **It is empty for four reasons, and only one of them is going away.** Proof cost is collapsing. The other three are not: the people who buy proofs today can read formal statements; the people who write Gherkin mostly do not own provable code; and controlled English has a thirty-year record of being easy to read and hard to write.
3. **The niche is narrower than "formally modelled software by default".** As built, it is: pure, single-call decision logic, in a restricted profile of Rust, owned by a team that has a non-expert who must agree to the requirement. That is a real niche (authorisation engines, ledgers, eligibility and pricing rules, protocol state steps, parsers) but a small one.
4. **The project's own strongest evidence points at a domain shape, not a language.** The best real-world result is on access-decision logic written in Go, through the hand-model chain. Cedar is the precedent and Bedrock Automated Reasoning sells to the same shape ("complex rule sets"). I would position on *decision logic* and treat Rust as the first fully mechanised route, not as the identity of the project.
5. **Recommended primary audience: the engineering lead who owns a security-critical decision core** and has to answer "how do you know it does what the policy says" to someone who cannot read code. **Secondary: formal-methods practitioners and people building agent proof pipelines**, because they are the contributors and the credibility gate.
6. **The Mathlib comparison is right for one of three layers and wrong for the other two.** It fits the proof-lemma layer. The frame layer needs the governance of a standard (slow, stable, few definitions, evidence from human readers). Domain vocabularies need the governance of a package registry with named owners. Calling the whole thing "a Mathlib for requirements" would promise a community that the structure cannot produce.
7. **The widening move is to ship the cheap evidence first.** The project's own measurement is that no injected bug needed a proof to be caught. A rule that compiles to a property test and a bounded-checking harness on real Rust today, with a proof where the code fits, is useful to ten times as many teams as a rule that needs the translator to work.

## 1. Who does this today, in their own words

One row per tool. "Leaves to others" is my reading of what the tool does not claim.

### Rust verifiers

| Tool | Positioning, in its words | Reader it addresses | Leaves to others |
|---|---|---|---|
| **Kani** (AWS) | "a bit-precise model checker for Rust"; "Similar to testing, you write a harness, but with Kani you can check all possible values." [opened] https://github.com/model-checking/kani | A Rust developer who already writes tests. The pitch is "a test that covers every value". | Unbounded results (loops and collections need bounds). Where the property came from. Any link to a requirement. |
| **Verus** | "a tool for verifying the correctness of code written in Rust"; it "statically checks that the executable Rust code will always satisfy the specifications"; "under *active development*. Features may be broken and/or missing". [opened] https://github.com/verus-lang/verus | A systems developer willing to write specifications and proof code in Rust syntax and to "be prepared to ask for help". | Whether the specification is the right one. A small trusted checker: it trusts the solver and its own encoding. |
| **Creusot** | "a *deductive verifier* for Rust code. It verifies your code is safe from panics, overflows, and assertion failures. By adding annotations you can take it further and verify your code does the *correct* thing." [opened] https://github.com/creusot-rs/creusot | A Rust developer with a verification background; the showcase is a verified SAT solver. | The same as Verus, with Why3's provers as the trusted part. |
| **Prusti** | "a prototype verifier for Rust that makes it possible to formally prove absence of bugs and correctness of code contracts"; "By default Prusti verifies absence of integer overflows and panics." [opened] https://github.com/viperproject/prusti-dev | A Rust developer who wants "no panics" with little annotation. | Everything beyond contracts. It calls itself a prototype; I could not see recent release activity on the page, so its maintenance state is **unverified**. |
| **Aeneas** | "a verification toolchain for Rust programs. It relies on a translation from Rust's MIR internal language to a pure lambda calculus." "Aeneas currently functionalizes a subset of safe Rust". [opened] https://github.com/AeneasVerif/aeneas | A proof engineer who works in Lean, F*, Coq or HOL4. | Writing the specification and the proof. Unsafe code, concurrency, some loop forms. |
| **hax** (Cryspen) | "a tool for high assurance translations of a large subset of Rust into formal languages"; Lean backend via Aeneas is "Recommended for Lean". [opened] https://github.com/cryspen/hax | Cryptography and protocol engineers; one backend emits ProVerif models. | The proofs, and the specification. `&mut` in return types and under aliasing is excluded. |
| **Dafny** | "a verification-aware programming language that has native support for recording specifications"; it "empowers developers to write provably correct code (w.r.t. specifications)". [opened] https://dafny.org/ | A developer who will write in Dafny and compile out to C#, Java, Go, Python. | Code that already exists in another language. The parenthesis "(w.r.t. specifications)" is the meaning gap, stated honestly and left open. |

Evidence of production use: a July 2026 Kani paper says proof harnesses run on every change to Firecracker and that the Rust standard library campaign generated over 16,000 harnesses [search] https://arxiv.org/abs/2607.01504. A secondary write-up says that campaign found no previously unknown memory-safety bug and that its one code bug came from random testing [search, **unverified**] https://www.youngju.dev/blog/2026-07-16-rust-std-verification-null-result.en. Verus in production at Microsoft and AWS is widely asserted; I found no primary source today, so **unverified**.

What these seven have in common: **the reader is always the person who writes the code**, the requirement is always written in the tool's own notation, and none of them says anything about where the specification came from or who agreed to it.

### Policy and security logic

| Tool | Positioning, in its words | Reader it addresses | Leaves to others |
|---|---|---|---|
| **Cedar, verification-guided development** (AWS) | "First, we create an executable formal model of each core component in Lean. Second, we implement Cedar's production code in Rust"; "We confirm that the code matches the model by using differential random testing"; "we only need to trust Lean's minimal proof-checking kernel." Model 1,673 lines, proofs 5,714, Rust 24,915. [opened] https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development/ | Customers who must trust an authorisation engine; and engineers considering the method. | A proof about the Rust. The Rust is tested against the model, not proved. The properties are chosen and read by experts. |
| **Amazon Bedrock Automated Reasoning checks** | Uses "mathematical techniques to validate natural language content against policies you define"; aimed at "Regulated industries such as healthcare, human resources, and financial services" and "Complex rule sets such as mortgage approvals, zoning laws, insurance eligibility". Marketed as "up to 99% verification accuracy". [opened] https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html ; headline claim [search] https://aws.amazon.com/blogs/aws/minimize-ai-hallucinations-and-deliver-up-to-99-verification-accuracy-with-automated-reasoning-checks-now-available | A compliance or product owner with a policy document and a chatbot. | Any statement about code. It checks an LLM's *answer* against rules extracted from a document. Its own caveat is the one this project should quote: "A `VALID` result guarantees validity only for the parts of the input captured through policy variables." |
| **Kiro** (AWS) spec-driven development | "A property is a universal statement about how your system should behave"; "Kiro extracts properties from your EARS-formatted requirements"; "It provides evidence of correctness, not a proof"; "It is not formal verification". [opened] https://kiro.dev/docs/specs/correctness/ | A developer working with a coding agent, any language. | Proof. A fixed meaning for the requirement sentence: an LLM extracts the property, and nothing pins how the same sentence is read next time. |
| **NASA FRET** | "a framework for the elicitation, specification, formalization, and analysis of system requirements"; "It enables users to specify unambiguous requirements using restricted English sentences", "allowing users with different expertise to review and understand the precise meaning of each requirement". [opened] https://github.com/NASA-SW-VnV/fret | Requirements engineers in aerospace who already write "shall" statements. | The code. It exports formulas to model checkers and monitors over signal-level models. No quantifiers, no typed domain vocabulary [prior]. |

### Design-level and whole-stack

| Tool | Positioning, in its words | Reader it addresses | Leaves to others |
|---|---|---|---|
| **TLA+** | "a high-level language for modeling programs and systems--especially concurrent and distributed ones"; "useful for eliminating fundamental design errors, which are hard to find and expensive to correct in code." [opened] https://lamport.azurewebsites.net/tla/tla.html | Engineers designing distributed systems. AWS chose it partly because it rests on "basic set theory and predicates, with which all engineers are familiar" [search] https://cacm.acm.org/magazines/2015/4/184701-how-amazon-web-services-uses-formal-methods/fulltext | The code, entirely. Asked how they know the code matches the design, the AWS authors' answer is reported as "we do not know" [search, via Lamport's abridged version] https://lamport.azurewebsites.net/tla/amazon-excerpt.html |
| **seL4** | "Machine-checked mathematical proofs from high-level specifications to binary code"; "What the seL4 proofs assume: assembly code, boot code, machine interface, hardware, and DMA. This is where manual validation and scrutiny can focus on." The proofs "go beyond what these certification schemes require". [opened] https://sel4.systems/Verification/ | Builders of defence, aerospace and automotive systems choosing a kernel; and certifiers. | Reuse. The proof stack is one artefact for one kernel, at a cost I recall as roughly 20 person-years for under 10,000 lines of C [memory, **unverified**]. The abstract specification is read by experts. |

seL4's assumptions page is the best existing model for this project's "Rests on" block: a short, named list of what is not proved, presented as where scrutiny should go.

### 2026: agents writing proofs for Rust

| Work | What it shows | What it leaves open |
|---|---|---|
| **SymCrypt on Aeneas and Lean** (Microsoft). Ho, Fournet, Protzenko and others, arXiv:2609.15648; blog 13 July 2026 | 16.7 KLOC of Rust (SHA-3, ML-KEM) with safety, panic-freedom and functional correctness in 237 KLOC of Lean. "An agent may propose a proof script, but Lean independently verifies whether the proof is valid." "Human effort focuses on reviewing formalization of standards and main properties." "Engineers do not need to open Lean to see what has been verified" (dashboards). Code is in Windows insider builds. [opened] https://arxiv.org/abs/2609.15648 , https://www.microsoft.com/en-us/research/blog/verifying-rust-cryptography-in-symcrypt-from-standards-to-code/ | The meaning link is expert review of Lean against a public standard. That works because cryptography has standards and test vectors. It also reports models that "try to 'cheat' with unsound assumptions or weakened goals" [prior]. |
| **Runtime Verification experience report**, arXiv:2605.30106 | Rust to Lean through Aeneas or hax, with commercial AI provers; every proof kernel-checked. [search; prior records it as opened] https://arxiv.org/abs/2605.30106 | Specifications are written by proof engineers. |
| **FVS, formal verification skills** (Beneficial AI Foundation) | "FVS helps AI coding assistants write Lean 4 specifications and proofs." The human will "choose the targets, review the statements and decide when proof work begins"; the prover "reports VERIFIED only after a cheat audit". [opened] https://github.com/Beneficial-AI-Foundation/formal-verification-skills | Statement review is by a person reading Lean, helped by a fresh reviewing agent. No controlled language, no fixed vocabulary. |
| **Rust standard library verification contest** (Rust Foundation, AWS) | Tool-agnostic challenges with rewards; 29 challenges and 450+ PRs by March 2026; a Foundation article titled "How the Rust Standard Library Verification Contest Scaled Past Manual Proof Engineering". [search] https://rustfoundation.org/?p=120341 , https://github.com/model-checking/verify-rust-std | Safety properties only. I could not confirm how much of the scaling is due to agents: **unverified**. |
| **Intent formalization** (Lahiri, Microsoft Research, March 2026) | Names the problem this project works on: there is "no oracle for specification correctness other than the user". Proposes proxies: tests, mutation analysis, user feedback; lists "natural language explanations of formal properties ... and specification templates" as largely unexplored. [opened] https://risemsr.github.io/blog/2026-03-05-shuvendu-intent-formalization | A mechanism. This is an agenda, and it is the most useful external citation for the README's "why it matters". |
| **Spec-driven agent toolkits** (GitHub Spec Kit and others) | "specifications become executable"; the spec, not the code, is the source of truth. [search] https://github.github.com/spec-kit/ | I found nothing on how acceptance criteria are checked beyond tests an agent writes. **Unverified** in depth. |

**What 2026 changed for positioning.** A year ago "agents can write the proofs" was the news. It is now a published result at Microsoft scale, with a working audit loop. This project cannot lead with it and should not spend README space on it. What remains unclaimed is the step before the proof: who reads the statement, in what form, and on what evidence anyone believes the reading.

## 2. The map

Rows: how the requirement is expressed. Columns: the strongest evidence the tool produces. Entries in *italics* give evidence about a model or a design, not about implementation code.

| | Tests (examples, sampling) | Bounded or model checking | Solver (SMT) | Proof-assistant kernel |
|---|---|---|---|---|
| **Formal language only** | property tests written as code | *TLA+ with TLC*; *Alloy* | Dafny; Cedar's policy analysis | seL4; Cedar's Lean model (*Rust by differential test*); Aeneas, hax; SymCrypt |
| **Annotations in code** | runtime contracts, proptest | Kani | Verus, Creusot, Prusti | rare |
| **Structured English** | Gherkin and Cucumber (examples only); Kiro (EARS to property tests) | *FRET*; hardware "FV Gherkin" with an LLM in the loop [prior] | nothing found for code | **nothing found** |
| **Free English** | agent-written tests (Spec Kit style) | nl2spec to temporal logic [prior] | Bedrock Automated Reasoning (about LLM answers, not code) | agent drafts Lean from standards prose, expert reviews the Lean (SymCrypt, FVS) |

### Where the empty region is

The bottom-right block of the structured-English row: **structured English with a fixed meaning, checked against implementation code by a solver or a kernel.** Three cells are empty, not one:

- structured English to a bounded check on real code (a rule that compiles to a Kani harness);
- structured English to solver-checked contracts (a rule that compiles to a Verus or Creusot specification);
- structured English to a kernel-checked theorem (this project's stated target).

A fifth column would sharpen the picture: *what the evidence is about* (a design, a hand-written model, a generated model, the source, the binary). FRET and TLA+ are strong on the requirement side and say nothing about code. The Rust verifiers are strong on code and say nothing about requirements. Nobody spans both. That span, with the trust in each link itemised, is the claim worth making.

### Is it empty for a reason? Yes, four

**1. The people who pay for proofs can already read the statement.** Every kernel-proof success above has an expert-readable source of truth: a cryptographic standard with test vectors, a kernel's abstract specification, a policy language's seven properties. In those settings the meaning gap is closed by a handful of experts and a public document, and English would add a layer to audit without removing one. *This reason is weakening* only if proof spreads to code whose requirement has no standard behind it. That is the bet.

**2. The people who write structured English mostly do not own provable code.** Gherkin lives in product and QA teams working on web services, in every language but Rust, where behaviour is dominated by I/O, databases and time. The project's frames describe "one pure call". The overlap between "organisations with Gherkin on the wall" and "organisations with a pure Rust core worth proving" is, I believe, small. **I could not find data either way; this is my judgement and it is the largest uncertainty in the document.** *This reason is not weakening.*

**3. Controlled English is easy to read and hard to write.** The prior-art notes record this for Attempto ("easier to read than to write, hence predictive editors"), for Grammatical Framework ("all grammars leak"), and for EARS (syntax only, so a well-formed sentence can still be wrong). FRET survives because its users already wrote "shall" sentences and because NASA mandates requirements documents. A refusal ("unbound", "ill-typed", "ambiguous") is correct behaviour and is also the moment an author gives up. *Not weakening*, though an agent that rewrites a refused sentence into known forms changes the economics; that is the planned "suggest mode" and it is untested.

**4. The cost-benefit of the last column has been poor, and this project's own numbers agree.** `slice/compare/TRADES.md` as summarised in the architecture: "No bug needed a proof to be caught." Kiro's product bet is exactly that structured English plus property tests is where the value is, and it says so: "evidence of correctness, not a proof". The proof column buys one thing: a result that does not depend on a sample or a size bound. The buyers of that one thing are assurance cases, certification, and anyone facing an adversary who searches for the unsampled input. *This reason is weakening fast on the cost side* (agents write the proofs) and not at all on the benefit side.

**My reading.** The region is not empty by oversight. It is empty because, until about a year ago, anyone who could afford the right-hand column had no use for the English row, and anyone who used the English row could not afford the right-hand column. Cheap proofs remove the second half of that sentence. They do not remove the first. So the project has to find, or create, people who need both: a proof, and a non-expert who must agree to the statement. Section 3 is about who those are.

**A consequence I would act on.** The two cheaper empty cells (structured English to a Kani harness; to a property test with a *fixed* reading, which Kiro does not have) are reachable now, need no translator, and work on any Rust. Occupy them first and present the kernel proof as the top rung of a ladder the user is already standing on. Node E1 in the plan is this; I would move it ahead of everything except finishing the vocabulary review.

## 3. Candidate audiences

For each: their problem as they would say it; what they must believe; their first objection; what would earn trust.

### A. Engineering lead for a security-critical decision core

*Authorisation and policy engines, ledgers and settlement, entitlement and pricing rules, key-management state, protocol steps, parsers and validators. Rust first; the Go result shows the method is not confined to it.*

- **Problem, in their words.** "Security review and the customer keep asking how we know the engine does what the policy document says. I show them tests. They ask what about the cases we did not think of. I have no answer that a non-engineer can check."
- **Must believe.** That their critical logic can be isolated into a pure core. That the sentence form can say what their policy actually says. That the cost per rule is closer to a test than to a research project.
- **First objection.** "Your translator handles a third of real functions with your own patches, and you have shown two toy crates. My code has traits, async and a database." Second: "Your own results say property tests find the bugs."
- **Earns trust.** One external crate they recognise, taken end to end, with the translation failures listed. A report on *their* code, even if half the rules come back "tested only". The false-rule demonstration: a plausible rule refuted with an input that fails on compiled code. The honest "Rests on" block.

### B. Assurance and certification engineers

*Safety and security case authors under IEC 61508, ISO 26262, DO-178C with its formal-methods supplement DO-333, Common Criteria.*

- **Problem.** "Traceability from requirement to verification evidence is done by hand in a spreadsheet, and it goes stale the day after the audit. Formal evidence earns credit only if I can explain what was proved and what was assumed."
- **Must believe.** That the evidence graph maps onto the artefacts their standard names. That "tool-trusted" links can be argued to an assessor.
- **First objection.** "None of these tools is qualified. Lean, Aeneas and your audit code carry no certification credit. And who signed the vocabulary, under what process?" This objection is correct today.
- **Earns trust.** An evidence package in a form they recognise (a claim-argument-evidence structure, a requirements trace matrix), generated from the graph. Staleness shown working. A clear statement of which tool outputs are relied on and which are independently re-checked, since re-checking is the standard route around tool qualification. Context: a qualified Rust compiler exists (Ferrocene: ISO 26262 ASIL D, IEC 61508 SIL 3 per its 2026 release notes [search] https://ferrous-systems.com/blog/ferrocene-26-05-0/), so Rust is entering this world, slowly. I found nothing today on formal-methods credit for Rust specifically: **unverified, and a gap worth a proper search**.
- **My view.** High value per customer, very long sales cycle, and they adopt what a standard or a prime contractor tells them to. A design input now; not the first audience.

### C. Formal-methods practitioners

*People who use Lean, Aeneas, Verus, Dafny, Isabelle. Includes the Aeneas and hax teams.*

- **Problem.** "Proofs are getting cheap. My bottleneck is specification review, and nobody outside my team can do it. Also, every project re-proves the same loop lemmas."
- **Must believe.** That a frame library does not lose expressiveness they need. That the chain adds no unsoundness. That this is not a wrapper around their tool with a marketing layer.
- **First objection.** "Controlled English hides the quantifiers I need to see. I would rather read the Lean. And 23 frames will not express my invariant." Then: "Show me the trusted base."
- **Earns trust.** The trusted-base table, first. The audit code, short enough to read. The negative controls. The translator patches offered upstream with the census numbers. The negative results kept in the open (five failed proof-structure metrics is a credibility asset with this audience). A plain statement that the echo has only been tested on model readers.
- **My view.** They will not be the users of the English layer; they are the suppliers of everything beneath it and the first people asked "is this real?". If they shrug, audiences A and B never hear of it.

### D. Teams building coding agents and spec-driven workflows

*Kiro, Spec Kit, and in-house agent pipelines.*

- **Problem.** "The agent writes the code and the tests, so the tests prove nothing. I need a statement the agent cannot quietly weaken, that a person can approve in seconds, and that fails loudly."
- **Must believe.** That a fixed reading of an English rule is worth more than an LLM's extraction of a property from it. That the check is fast enough to sit in an agent loop.
- **First objection.** "We work in TypeScript and Python. Property tests are good enough and they run in seconds." For most of this audience that is true and will stay true.
- **Earns trust.** A demonstration of the specific failure they fear: an agent told to make the build green re-proves around a bug, and the mutation and adequacy checks catch it. The project has this result already ("shown false" counted separately from "proof lost"). A rule format an agent can target, with refusals that tell it what to fix.
- **My view.** The largest population and the one for whom the timing argument is strongest. Also the one least likely to need the proof column. Reachable through the cheap rungs of the ladder (section 2), not through Lean.

### E. Regulators and auditors receiving evidence

- **Problem.** "I receive a thousand pages asserting compliance. I cannot tell what was tested, what was proved, and what was assumed."
- **Must believe.** That the report's evidence labels mean the same thing from one submission to the next.
- **First objection.** "I cannot evaluate the tool. Who stands behind the vocabulary?"
- **Earns trust.** Stable, published definitions of the evidence kinds and the frames; third-party reproduction; an institution behind the frame library. None of this exists yet.
- **My view.** The ultimate reader of the "Rests on" block, and the reason the frame library needs standard-like governance (section 4). Not reachable directly for years.

### Recommendation

**Primary: A, narrowed to decision logic.** They own both the requirement and the code, they have a non-expert who must agree to the statement (the reason the English row matters), their code is the most likely to be pure, and the project's best evidence is in their domain. Cedar gives them a precedent they have heard of.

**Secondary: C.** They decide whether the project is taken seriously, they are the only source of contributors for the lemma library and the translator work, and they can use the lower layers today.

Treat **D** as the growth path once rules produce cheap evidence without the translator, and **B and E** as constraints on the design of the report.

I am moderately confident in A over D. The case for D is market size and timing. The case against is that D can be satisfied by a product that already ships and says in its own documentation that it is not proof. If the owner's real aim is "the default", D is where the default gets set, and the honest route there is the ladder.

### What that implies for the top of the README

The current opening is strong on the idea and risky on status: "Get back a proof that the code does it for every input" reads as a present-tense capability, and the reader in audience C will find "This is the target" seven screens later and stop trusting the rest.

1. **Line one: the claim, scoped.** Name the kind of code ("decision logic in Rust") and the three possible answers.
2. **Line two: status, in numbers.** "Research prototype. Works end to end on two small crates and 35 scenarios; a new sentence still needs hand-written glue." Before the example, not after it.
3. **The report block stays where it is.** It is the best thing in the document. Make it a real run's output, and say so; if it is a mock-up of the target, label it in the caption.
4. **Add the refuted case next to it.** A false rule with its counterexample is more persuasive than a proved one, to every audience.
5. **A "who this is for, and who it is not for yet" block of four lines.** For: a pure core, a restricted Rust profile, a requirement owner who does not read code. Not yet: async, I/O, concurrency, anything the translator rejects.
6. **A comparison table against four named neighbours** (Kiro, FRET, Cedar's method, agent proof pipelines on Aeneas), one line each: what they give, what this adds, what they do better. The neighbours are well known; naming them borrows their context.
7. **The trusted-base table moves up**, above "Why Gherkin, Lean and Rust". For audiences B and C it is the product.
8. **What it is made of**, as the owner asked: tooling, libraries, method, checkers, and the list of upstream tools patched. One short table. This is where the Mathlib kinship is stated, in one sentence, with its limit.
9. **The mathematics strand leaves the main README** for its own page. It is good work and it splits the reader's attention at the point where they are deciding what the project is.

On the list the owner shared (https://github.com/matiassingers/awesome-readme [opened]): the features praised most often are a one-sentence description, a table of contents, a real demo (screenshot or recording), copy-paste usage, and, less often, a comparison with alternatives and an architecture diagram. The entry closest in kind is NASA's Ogma (clear description, feature list, demo recordings, simple install). Two things to take: a short terminal recording of a rule being proved and a false rule being refuted, and badges that carry honest state (scenarios proved, share of census functions translating) in place of decorative ones. One thing not to take: most of that list optimises for adoption of finished tools. A research prototype earns more from a visible "does not work yet" section, which this README already has and should keep above the fold.

## 4. The Mathlib comparison

### What Mathlib is, organisationally

- **One repository, one library.** Everything builds together at every commit, so a change that breaks a downstream file is fixed in the same change.
- **A scope rule.** The contribution guide asks whether material is "typically taught or studied in a mathematics department?" and says Mathlib should not be seen as "all of mathematics and related areas"; other areas belong in "standalone repositories depending on mathlib". [opened] https://leanprover-community.github.io/contribute/index.html
- **Maintainers and reviewers as distinct roles.** "A PR reviewer does *not* have to be a maintainer!" Review is the bottleneck: the page reports over 2,600 open PRs. [opened, same page]
- **Naming conventions and a style guide, enforced by linters**, so that a lemma's name can be guessed from its statement. [memory for the detail; the guide links to both documents]
- **Deprecation with a grace period.** "Growing Mathlib" (Baanen, Ballard, Commelin, Chen, Rothgang, Testa, arXiv:2508.21593) lists "a deprecation system for breaking changes", linters, and tooling to triage contributions as how it grows without overloading maintainers. [opened, abstract] https://arxiv.org/abs/2508.21593 . The period is several months; maintainers have discussed four to six [search, Zulip archive] https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/Deprecation.20policy.html . Beyond that grace period the working attitude to backward compatibility has been described there as "there is no compatibility" [search].
- **A norm of generality and refactoring.** Definitions are restated in more general form as understanding improves, and the library is refactored to match. [memory]
- **A rule on AI use.** Disclose it; "It is essential that you understand all the content written by an AI"; low-quality generated PRs may be closed without comment. [opened, contribution guide]
- **A community with its own motive.** Contributors are mathematicians who want their subject formalised. Nobody is paid per lemma.

Two things make this work that are easy to miss. First, **the kernel settles correctness**, so human review is spent on design, naming and generality. Second, **the subject is shared**: a group is the same thing to every contributor, and a century of textbooks settled the definitions before anyone formalised them.

### What fits

| Mathlib practice | Carries over to | Why |
|---|---|---|
| One curated library, reviewed, linted | Frames and modifiers; the proof-lemma library | A few dozen shared definitions benefit from one home and one standard |
| Naming conventions | Frames and their English forms | A sentence form should be guessable from the frame, and the reverse |
| Linters as policy | Every frame must ship a second executable reading, an echo template, separating examples, and negative controls | The project already requires these; make the machine refuse a frame without them |
| A scope rule | "A frame belongs in the core only if two unrelated systems need it" | The existing "split on the second use" rule, promoted to a contribution policy |
| Standalone repositories that depend on the core | Domain vocabularies | Exactly Mathlib's answer for areas outside its scope |
| Disclosure of AI authorship | Proofs, lemmas and proposed frames | The trust model already distrusts proof text; the same label belongs on frame proposals |
| Reviewer role separate from maintainer | Meaning reviewers (domain people) separate from Lean reviewers | The architecture document already asks "who may sign what" |

The **proof-lemma layer** is the closest fit of all: lemmas about loop shapes over Aeneas models, and models of standard-library functions, are ordinary Lean mathematics. The kernel checks them, generality helps, refactoring is safe. The SymCrypt paper says its authors built Lean "tactics and libraries" for the same purpose [opened, abstract]. That is where a Mathlib-style commons could really form, and the right move may be to contribute to theirs, not to start a second one.

### What does not fit

**1. The kernel does not check a frame's correctness.** Whether "never changes" means what an English reader takes it to mean is a fact about readers. Mathlib review can lean on the kernel and argue about style. Frame review has nothing to lean on except second readings and trials with people. So the scarce resource is different in kind: not maintainer hours but evidence from human readers, per frame, per English form. No amount of community enthusiasm substitutes for it.

**2. Stability has the opposite sign.** Mathlib refactors freely and gives downstream a few months. Here a changed frame voids every signature built on it, in every project (the architecture document says so). Frames need the change discipline of a standard or a wire format: versioned, rarely changed, with a kernel-checked equivalence proof as the only cheap path for a revision. Plan node V9 is the right test. A culture of "there is no compatibility" would destroy the thing that makes a signed vocabulary worth having.

**3. Software has no shared subject.** "Group" is one thing. "Account", "transfer", "accepted" are different things in every codebase, bound to different functions. Domain words are closer to type bindings for someone else's code than to mathematical definitions: they have an owner, they go stale when the code changes, and nobody outside the project can review them. The nearest organisational models are a package registry with named maintainers, and community type-definition repositories for libraries, not Mathlib.

**4. Size.** Mathlib is on the order of a couple of hundred thousand theorems [memory, **unverified**]. The frame library is 23 definitions and might reach fifty. That is a pattern catalogue. Its real ancestors are Dwyer's specification patterns and EARS: small, cited for decades, governed by almost nobody. A catalogue of that size needs an editor and a change process more than a community.

**5. Motive.** Who contributes a frame? A team that needed one. They will contribute it if upstreaming is cheaper than carrying it, and not otherwise. Mathlib's intrinsic motivation has no obvious counterpart, except among formal-methods people, who will contribute lemmas, not vocabulary.

**6. Toolchain pinning.** Mathlib moves with Lean. The pipeline here is pinned to the translator's Lean version, and the repository already runs four Lean versions side by side. A shared library that several projects consume across different pins is an operational problem Mathlib does not have, because Mathlib *is* the pin.

### The structure I would propose instead

| Layer | Contents | Governance model | Change policy |
|---|---|---|---|
| Core frames and modifiers | A few dozen definitions, each with a second reading and reader-trial evidence | A standard: small editorial group, two signers of different kinds, public change log | Rare; versioned; a revision either carries a kernel-checked equivalence or lists every affected rule |
| Proof lemmas and library models | Loop shapes, collection lemmas, models of standard-library functions | Mathlib-like: open contribution, kernel-checked, linted, refactored freely | Deprecation with a grace period |
| Domain packs | Shared vocabularies for a domain with settled concepts: authorisation (principal, resource, permit, forbid), double-entry ledgers, state machines, round-trip parsing | A registry: each pack has a named owner and its own signers | Semantic versioning; packs pin a core version |
| Project words | Bindings to one system's code | Private to the project | Staleness computed from the code |

**Domain packs are the interesting bet and the one I am least sure of.** They are where "software domains are not one subject" might be partly wrong: authorisation has a small, fairly settled set of concepts, and Cedar's seven proved properties map onto frames already [prior]. If two unrelated authorisation engines can share a pack, the library story is real. If they cannot, the reusable part of this project is fifty definitions and a method, which is still worth having but is not a Mathlib.

**How I would state the kinship in public:** "Like Mathlib, the value accumulates in a shared library. Unlike Mathlib, the part of it that carries meaning must change slowly and be checked against human readers, because no kernel can check it." One sentence, with the limit attached.

## 5. Value propositions

### Variant 1: for the engineering lead (concrete)

> State a rule about your decision logic in a sentence your policy owner can read, and get back a proof that the Rust obeys it for every input, or the input that breaks it, with each step from sentence to compiled code labelled as proved, tested or trusted.

**Strongest objection.** By the project's own measurements, property tests and bounded checking found every injected bug, and the proof route covers a third of real functions with patches. So for most code the honest answer today is "tested only", which Kiro and a property-testing library already give, in any language. The reply has to be the ladder: the same sentence yields the test now and the proof where the code fits.

### Variant 2: for the agent era (the "why now")

> When agents write the code and the proofs, the one thing a person can still check is the statement; this makes the statement a plain sentence built from a few dozen reviewed definitions, and tells you which parts of the verdict a machine checked and which a person asserted.

**Strongest objection.** The premise that a person catches a wrong reading when it is echoed back has been tested only on language models (93%). If people skim and approve, the English layer converts an unreadable formal statement into a readable false sense of agreement, which is worse. An expert will also say they would sooner read ten lines of Lean than trust an echo. Until the human trial runs, this variant rests on a hypothesis and must say so.

### Variant 3: for assurance (the evidence ledger)

> A ledger of what your software claims rest on: every requirement traced to the code, every link labelled kernel-checked, tested, tool-trusted or assumed, and marked stale the moment anything beneath it changes.

**Strongest objection.** Traceability tools exist and are entrenched, and an assessor gives credit for evidence from qualified tools under a named standard. A ledger whose strongest entries come from an unqualified research translator and a prover with no certification history is informative and earns no credit. It also invites the reply "so your ledger says most of it is trusted or assumed", which is true and is the point, but it is a hard sell.

### Which to lead with

Variant 1 as the first line, because it names a user, an object and an outcome. Variant 2 as the "why now" paragraph, because it is the only one that explains why this was not built ten years ago and why it differs from the Aeneas agent pipelines. Variant 3 is a feature of the report; lead with it only when speaking to audience B.

A shorter form I would test as a tagline: **"Proofs are getting cheap. Knowing what was proved is not."** Its objection: it is a diagnosis, and Microsoft Research has already published the same diagnosis under the name intent formalization. It works only with the concrete example directly beneath it.

## 6. How narrow is this, and what would widen it

Stated plainly, the project today serves code that is all of: Rust; inside the translatable profile; pure and single-call; small enough that six lines of Lean per line of loop is affordable; and owned by a team with a requirement owner who does not read code. Each condition removes most candidates. The owner's phrase "formally modelled software the default" describes a destination several widenings away.

In order of leverage:

1. **Cheap evidence first, from the same sentence.** A rule that compiles to a property test and a bounded-checking harness on real Rust needs no translator and no proof. This turns the first-day experience from "does my crate translate?" into "my rule found an input". It also puts the project in direct, favourable comparison with Kiro: the same workflow, with a fixed reading in place of an LLM's extraction. This is the single change that most widens the audience.
2. **Name the hand-model chain as a first-class route.** The Go result used a model checked by differential testing. That is Cedar's method. Presented as "the weaker chain, labelled as such", it brings in decision logic in any language, and it is honest because the report already distinguishes tested from tool-trusted links.
3. **One domain pack, for authorisation.** It is the owner's domain, the project's best evidence, Cedar's precedent, and Bedrock Automated Reasoning's commercial territory. A pack that two unrelated engines can use would be the first proof that vocabulary is reusable beyond frames.
4. **A rule format agents can target.** Refusals that say what to change, and a guarantee that an agent cannot weaken a rule to pass. That is the entry to audience D.
5. **Effects.** A stated pattern for the shell around a pure core (what is assumed about it, how it is tested), since the architecture document says real defects live there and the one real defect found so far was outside the model. Without this, an informed critic's first question has no answer.
6. **The human echo trial.** Not a widening, a precondition. Variant 2, the frame library's claim to carry meaning, and the whole English row rest on it.

What would *not* widen it: more frames, more proved toy scenarios, or more of the mathematics strand.

## What I am unsure of

- Whether teams that own security-critical Rust use Gherkin at all. I believe few do. If so, Gherkin is a familiar *notation* to borrow, not an existing *user base* to convert, and the README should not imply the latter.
- Whether people catch wrong readings. Everything about the English layer depends on it and there is no human data.
- Whether authorisation vocabulary is really shareable across engines, or only looks so from one engine.
- Verus's production use, Prusti's maintenance state, the role of agents in the standard-library contest, how Spec Kit checks acceptance criteria, and whether any certification scheme has yet given formal-methods credit for Rust: all **unverified** today.
- Kiro's property extraction: I rely on its documentation. I did not run it, and it may pin readings more firmly than the documentation suggests.
- The seL4 effort figures and the Mathlib size are from memory.
- I did not read `private/` or `tdflite-ideas/`, as instructed, so what I say about the access-decision result rests only on the public summaries in the README, the architecture document and the results table.

## Sources

Opened today:

- Kani: https://github.com/model-checking/kani
- Verus: https://github.com/verus-lang/verus
- Creusot: https://github.com/creusot-rs/creusot
- Prusti: https://github.com/viperproject/prusti-dev
- Aeneas: https://github.com/AeneasVerif/aeneas
- hax: https://github.com/cryspen/hax
- Dafny: https://dafny.org/
- Cedar and Lean: https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development/
- Kiro correctness properties: https://kiro.dev/docs/specs/correctness/
- Bedrock Automated Reasoning checks: https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html
- FRET: https://github.com/NASA-SW-VnV/fret
- TLA+: https://lamport.azurewebsites.net/tla/tla.html
- seL4 verification: https://sel4.systems/Verification/
- SymCrypt paper (abstract): https://arxiv.org/abs/2609.15648
- SymCrypt blog: https://www.microsoft.com/en-us/research/blog/verifying-rust-cryptography-in-symcrypt-from-standards-to-code/
- Formal verification skills: https://github.com/Beneficial-AI-Foundation/formal-verification-skills
- Intent formalization: https://risemsr.github.io/blog/2026-03-05-shuvendu-intent-formalization
- Mathlib contribution guide: https://leanprover-community.github.io/contribute/index.html
- Growing Mathlib (abstract): https://arxiv.org/abs/2508.21593
- Awesome README: https://github.com/matiassingers/awesome-readme

Search summaries only (not opened):

- Kani paper, July 2026: https://arxiv.org/abs/2607.01504
- Runtime Verification experience report: https://arxiv.org/abs/2605.30106
- Rust standard library contest: https://rustfoundation.org/?p=120341 ; https://github.com/model-checking/verify-rust-std
- Secondary write-up of the contest's results: https://www.youngju.dev/blog/2026-07-16-rust-std-verification-null-result.en
- Bedrock "up to 99%" announcement: https://aws.amazon.com/blogs/aws/minimize-ai-hallucinations-and-deliver-up-to-99-verification-accuracy-with-automated-reasoning-checks-now-available
- AWS and TLA+: https://cacm.acm.org/magazines/2015/4/184701-how-amazon-web-services-uses-formal-methods/fulltext ; https://lamport.azurewebsites.net/tla/amazon-excerpt.html
- Mathlib deprecation discussion: https://leanprover-community.github.io/archive/stream/287929-mathlib4/topic/Deprecation.20policy.html
- Ferrocene qualification: https://ferrous-systems.com/blog/ferrocene-26-05-0/
- Spec Kit: https://github.github.com/spec-kit/
- Barriers to formal methods adoption (surveys, not used for specific claims): https://arxiv.org/abs/1812.08815v1

From this repository: `README.md`, `docs/ARCHITECTURE.md`, `docs/RESULTS.md`, `docs/PLAN.md` (Stance, Status, Track V), `out/prior_art_vocabulary.md`.
