# Naming: the verdict on "Rosette" and a shortlist of five

Brainstorm for the owner, 2026-11-10. Not for publication.

**Basis.** I read `README.md`, `docs/ARCHITECTURE.md`, `docs/RESULTS.md`, the Stance and Status sections of `docs/PLAN.md`, `brainstorm/FORM.md` and the other notes in `brainstorm/` (positioning, inventory, readme-patterns, the three form proposals, diagram notes). I did not read `private/` or `tdflite-ideas/`. I ran nothing in the repository.

**What I checked myself, today**, for every name in anyone's top five, for "Rosette", and for "Phraseology" (proposed as a library name):

- crates.io (the name and `cargo-<name>`), PyPI and npm, through their JSON APIs;
- GitHub: whether `github.com/<name>` is an account, and a repository-name search (top eight by stars);
- Lean's package registry (Reservoir): all 1,447 packages listed in `leanprover/reservoir-index`, matched as substrings;
- web searches for "<name> verification" and "<name> rust" (or close variants), US-only, summaries only;
- nameservers for the `.com`, `.dev`, `.io` and `.org` domains of the shortlisted names.

Facts taken from the earlier naming lists and not rechecked are marked *(earlier list)*. Facts from my own memory are marked *(memory)*. I did no trademark search.

## The answer in six lines

1. **Drop "Rosette". A qualifier does not rescue it.** Rosette is a well-known language for verification and synthesis. Its author, Emina Torlak, has already had Rosette's semantics formalised in Lean (Leanette, POPL 2022). She is also a co-author of the Cedar paper that this project names as its precedent: a Lean model, Rust production code, differential testing. So "lean-rosette" reads as her group's project.
2. **None of the candidates is good enough to register as a package today.** Two are good enough to test: **Readback** and **Everycase**. The rest either need explaining or collide with someone else.
3. **Recommendation: Readback** for the project and the command, and **the Phraseology** for the catalogue of shared pieces. It names the one thing no neighbour does: the rule is said back with one fixed meaning before anyone trusts the verdict. It also stays true at every level of evidence.
4. **Runner-up: Everycase.** It is the clearest name to a stranger and the only candidate free on every registry I checked. But it overclaims. Today most rules would carry the label "tested only" under a banner that says "every case".
5. **Choose between them with five strangers**, ideally the same people who take the echo trial. Write the decision rule down before the first session (section 3).
6. **Name two things, not five**: the tool and the catalogue. The report and the method keep plain descriptive names. The proof-lemma layer gets no brand, because it should go to the Aeneas ecosystem.

## 1. Keeping "Rosette"

### What the name already means

| Namesake | What it is | Why it matters here | Source |
|---|---|---|---|
| **Rosette**, Torlak, University of Washington | A solver-aided language on Racket. It adds `verify`, `solve` and `synthesize` queries and uses Z3. The repository was created in July 2014, has 709 stars and was last pushed on 2026-10-16. Course material for UW's CSE 507 (Computer-Aided Reasoning for Software) is built on it | Same field, same vocabulary ("verify"), and actively maintained. Formal-methods readers learn it in courses | https://github.com/emina/rosette ; https://docs.racket-lang.org/rosette-guide/ch_essentials.html ; https://courses.cs.washington.edu/courses/cse507/23au/doc/L01.pdf |
| **Leanette** | Porncharoenwase, Nelson, Wang and Torlak, "A Formal Foundation for Symbolic Evaluation with Merging", POPL 2022. It formalises Rosette's symbolic semantics in Lean, with a verified reference evaluator | "Rosette in Lean" already exists as published research | https://unsat.cs.washington.edu/papers/porncharoenwase-leanette.pdf ; https://github.com/uw-unsat/leanette-popl22-artifact |
| **Cedar's verification-guided development** | "How We Built Cedar: A Verification-Guided Approach" (FSE 2024): an executable Lean model, Rust production code, and differential random testing between them. Torlak is a co-author, with an AWS affiliation | This is the precedent `positioning.md` leads with, and it is the method behind the project's best real-world result | https://arxiv.org/abs/2407.01688 |
| **Rosette**, Babel Street | Commercial text analytics, including name matching and name *translation*. Bought from BasisTech in 2022. The client libraries are still active (`rosette-api/python` was pushed in October 2026) | A second collision, this time with the "translation" sense of the name | https://www.babelstreet.com/rosette ; https://github.com/rosette-api/python |
| **Rosette**, actor language | "Reflective actor-based language" | A second programming language with this name | https://github.com/leithaus/Rosette |
| **Registries** | crates.io `rosette`: "Translate a text file to any language" (2021). PyPI `rosette`: "Minimal Rosette Implementation" (2017). npm `rosette`: 0.0.0. `github.com/rosette`: an empty organisation created in 2025 | Every package name is taken | https://crates.io/crates/rosette ; https://pypi.org/project/rosette/ ; https://www.npmjs.com/package/rosette |
| **The Rosetta family** | Apple's Rosetta 2 binary translator (named after the stone); the RosettaCommons protein-modelling suite; Rosetta Code *(memory)*; Rosetta Stone language courses *(memory)* | Computing's most-used translation metaphor, so it is neither distinctive nor surprising | https://en.wikipedia.org/wiki/Rosetta_(software) ; https://docs.rosettacommons.org/docs/latest/development_documentation/test/rosetta-tests |
| **Reservoir** | No package name contains "rosette" | The only place where the name is free | `leanprover/reservoir-index` |

### The case for keeping it

- **It is already in place**: the public repository URL, the Lean library `Rosette`, the schema id `rosette.refinement-graph/2`, and every document.
- **It is short and easy to say and spell.**
- **The allusion can be made to fit.** The Rosetta Stone is one text in three scripts, and this project's rule exists in English, Lean and Rust. A rosette is also a prize ribbon, a mark awarded after judging, which suits a verdict. I could not find out whether either meaning was intended, because `DECISIONS.md` does not say why the name was chosen.
- **Most engineering leads have never heard of the other Rosette**, and Lean's registry has no package by that name.
- **Renaming has a cost**: a day of churn while agents are running long jobs in the trees that carry the name.

### The case against

1. **It collides with the readers who decide whether the project is credible.** `positioning.md` names formal-methods practitioners as that gate. They are exactly the people who know Rosette, and their first question will be "is this related?". The answer is no.
2. **It collides with the specific people closest to this work.** Torlak's group put Rosette into Lean, and Torlak co-wrote the Cedar method that this project follows. `FORM.md` names AWS as the likeliest neighbour to move into the empty cell. To that neighbour, the name looks either careless or borrowed.
3. **The qualifier makes it worse.** "lean-rosette" reads as "Rosette for Lean" or "Rosette ported to Lean", which is what Leanette is.
4. **The allusion is used up.** The Rosetta name is already on a binary translator that ships with every Mac, a protein suite, a programming chrestomathy and a language course.
5. **It says nothing about what the tool does.** The brief says clear beats clever, and this name is neither.
6. **Inside the repository, the name never belonged to the software chain.** `Rosette/` is the maths strand's library for lifting lemmas out of proofs (its lakefile keyword is `math`). The chain lives in `slice/`. Every form proposal moves the maths strand out, and the name would leave with it.
7. **Every package registry name is taken.**

### Does a qualifier fix it?

No.

| Variant | Problem |
|---|---|
| `lean-rosette` (today) | Reads as "Rosette in Lean", which already exists |
| `rosette-rules`, `rosette-rs`, "Rosette Verifier" | Every citation and search still begins with "Rosette", and the question "is this Torlak's?" comes every time |
| "Rosetta", "Stele", "Triglot" | They keep the overused metaphor. Triglot also counts three layers where the chain has five or six |

Only removing the word fixes it. Also leave "lean" out of the next name. The cheap levels of evidence need no Lean, and `FORM.md` wants the catalogue to be data any tool can read.

### Verdict

**Rename the software project before anything reaches a package registry, a paper or a talk.** Rename the maths library when it moves to its own repository: it has the same collision but is less urgent. The repository also still carries an older identity ("Lean-Ghidra" in `AGENTS.md`), and both can be retired in one go.

Stop adding "rosette" to new public identifiers now. Do the rename itself once the name is chosen and the long jobs have finished. It touches:

- the repository name (GitHub redirects the old URL after a rename *(memory)*);
- the README title and the documents;
- the evidence-graph schema id `rosette.refinement-graph/2` and the tool ids such as `tool:rosette.lift` in `docs/SCHEMA.md` (bump the id or accept both);
- the maths strand: the `Rosette` Lean library, `#rosette_lift`, the `ROSETTE_CORPUS` variable, and `corpora/ns_reuse/mk_reuse_ns.py`, which builds a file from `Rosette/` sources by text substitution;
- `AGENTS.md`.

## 2. The shortlist

The five names below are the union of the three earlier top-five lists, minus the names that the checks ruled out. Hallmark, Proofmark and Ruleproof are in section 4, with the evidence.

### At a glance

| | Readback | Everycase | Holdsfor | Plainrule | Rulestone |
|---|---|---|---|---|---|
| Guessable from the name alone | Partly ("repeat it back to confirm"); engineers may think of GPU readback | **Yes** ("checks every case") | No | Partly: it names the input, not the checking | Partly; sounds like a rules engine |
| True at every level of evidence | **Yes** | **No**: false for "tested only" | **Yes** | Yes | Yes |
| Names what is distinctive here | **Yes**: the fixed reading | No: Kani already says "all possible values" | Partly | No | No |
| crates.io / PyPI / npm / GitHub account / Reservoir | Taken / taken / taken / free / free (`cargo-readback` free) | **All free** | All free | All free | All free |
| GitHub repos with the name | 179, mostly GPU and FPGA | 2 | 0 | 0 | 4, two of them rule engines |
| Domains (.com .dev .io .org) | All four registered | .com held by a broker; .org a live site; .dev and .io free | All four free | .com registered; three free | .com and .io registered |
| Search | Poor (GPU, FPGA, aviation) | Good | Good, awkward to type | Good | Poor |
| Names for the parts | Strong, from one real practice | Weak | Weak (but the best verdict wording) | Weak | Contrived |

### 2.1 Readback

**Tagline.** *Say the rule in plain English. Readback says back exactly what it was taken to mean, then tells you whether the code obeys it and what that answer rests on.*

**Names for the parts**

| Part | Name | Note |
|---|---|---|
| Project and command | Readback: `readback check`, `cargo readback test`, `cargo readback prove` | Publish the cargo subcommand as `cargo-readback` (free). Someone else has reserved the bare `readback` crate |
| The English text of a reading | "the readback" | Replaces "echo" in text users see. "Reading" stays as the name of the formal reading |
| Catalogue of shared pieces | **the Phraseology** (package `readback-phraseology`); its entries are "phrases" | Phraseology is aviation's word for its fixed set of radio phrases, each with one meaning, changed only by the issuing authority *(memory)*. That carries the trust model `FORM.md` asks for: a governed standard, not a library of proved truths. The public word "phrase" also avoids "frame", which in verification means the frame rule of separation logic *(earlier list)*. Code can keep `Frames` internally |
| Domain words | "your vocabulary" | Per project, not branded |
| Evidence format | "the evidence report" with its "Rests on" block; "the evidence graph" for the machine form | I would not borrow aviation's "clearance": it reads as permission, or as security clearance |
| Method | "read back, then check" | Plain words until someone outside the project uses it |
| Proof lemmas | No brand; contributed to the Aeneas ecosystem | Call them `readback-lemmas` only while they live here |

**Three sentences, using real fixtures**

- "Readback refuted the transfer rule: both example rows pass, but it fails at sender = 1, receiver = 18446744073709551615, amount = 1."
- "Check the readback before you sign. It prints every default it added to your sentence, including 'accepted or rejected' and 'the call returns'."
- "'Never changes' is in the Phraseology and 'interest' is in no vocabulary, so Readback refused 'A deposit earns interest' as unbound."

**Collisions**

- **crates.io** `readback`: "Trait-based, type-safe Tauri IPC built on specta. This release reserves the crate name." It is version 0.0.0, with 21 downloads, created 2026-06-12. https://crates.io/crates/readback . `cargo-readback` is free.
- **PyPI** `readback` 0.1.0 (2026-07-20): "Validation via echo-confirmation: readback(value, confirm_fn)." Its repository has 0 stars. https://pypi.org/project/readback/ , https://github.com/coldbricks/readback . This is the same idea in miniature, which suggests the metaphor comes naturally to people.
- **npm** `readback`: "Transcribes ATC transmissions into readable text." https://www.npmjs.com/package/readback , https://github.com/borisdiakur/readback (8 stars).
- **GitHub**: `github.com/readback` returns 404, so the account is free. 179 repositories have the word in their names. The most-starred are about GPU and FPGA readback (for example keijiro/MetalAsyncReadback). One is an MCP server for reading Claude Code sessions (https://github.com/affirmitv/cc-readback, 17 stars).
- **Reservoir**: nothing.
- **Web**: "readback verification" returns FPGA bitstream "Verify and Readback" pages (https://docs.amd.com/r/en-US/ug908-vivado-programming-debugging/Bitstream-Verify-and-Readback-for-FPGAs-and-MPSoCs). "readback rust" returns GPU readback code (https://ref.rerun.io/docs/rust/head/src/re_renderer/allocator/gpu_readback_belt.rs.html) and a `ReadBack` trait (https://docs.rs/read_collection/). Apps with the name: two pilot radio-training apps (https://apps.apple.com/mn/app/readback/id6751527692 , https://apps.apple.com/app/id6797188637) and a text-to-speech app (https://apps.apple.com/us/app/readback-text-to-speech/id6747597136).
- **Domains**: `.com`, `.dev`, `.io` and `.org` all have nameservers.
- **Verification and requirements**: nothing uses the name.

**Weaknesses**

- **It cannot be guessed cold.** An engineer may think of GPU readback, a reading app or pilots, so the tagline has to carry the meaning.
- **It says nothing about code or proof.** That helps honesty and hurts the pitch.
- **Search on the bare word cannot be won, and all four domains are taken.** Pages and the repository will need a qualifier such as "Readback rules" or "readback-rules".
- **It names the one link no person has tested yet.** I think this bet is smaller than the earlier lists say. If people catch fewer wrong readbacks than hoped, the readback still exists and the report still prints it; what fails is the claim that it carries trust. But if the human trial misses the owner's bar badly, and the English layer becomes an index for experts (`FORM.md`, decision 2), the name advertises a demoted feature.

### 2.2 Everycase

**Tagline.** *Every case, or the case that breaks it.* While most verdicts are below proof, the README has to add "and how far it got".

**Names for the parts.**

- **Command**: `everycase` or `cargo everycase`.
- **Catalogue**: no natural name. "Everycase phrases", or a neutral "Rule Phraseology".
- **Report**: "the evidence report". A counterexample is "the case".
- **Method**: "every case, or the case".

**Three sentences, using real fixtures**

- "Everycase found the case: sender = 1, receiver = 18446744073709551615, amount = 1."
- "On the two fixture crates, Everycase proves 10 of the 14 rules for every input, refutes 3 and refuses 1."
- "This rule is only tested, on two examples; Everycase has not checked every case." This is the sentence the name makes awkward.

**Collisions**

- **Registries**: crates.io, `cargo-everycase`, PyPI and npm all return 404.
- **GitHub**: `github.com/everycase` returns 404. Two repositories have the name: JonathanSeriesX/everycase, a site about Apple accessories (https://github.com/JonathanSeriesX/everycase , https://everycase.org , 3 stars), and an empty everyCaseGames page.
- **Reservoir**: nothing.
- **Web**: no product of this name. The nearest names are EveryCheck and Everywhere.
- **Domains**: `everycase.com` is held by a domain broker (atom.com nameservers). `everycase.org` is the Apple-accessories site. `.dev` and `.io` have no nameservers.

**Weaknesses**

- **It overclaims below the proof level, which is where most rules are today.** The architecture says never to fold four kinds of evidence into one green light. A name that promises every case does that folding before the report is even read.
- **It is not distinctive.** Kani's README already says "check all possible values". The name describes the payoff and leaves out the fixed reading, which is the part no neighbour offers.
- **"Case" has other meanings**: test case, legal case, phone case. Web searches drift to legal case management *(earlier list)* and phone accessories.
- **It gives no names for the parts.**

### 2.3 Holdsfor

**Tagline.** *Does the rule hold? For every input, for the examples only, or not at all, and on what evidence.*

**Names for the parts.**

- **Command**: `holds` (`holds check wallet.feature`). The crate `holds` is a dormant 2018 crate (https://crates.io/crates/holds), so publish as `cargo-holdsfor`.
- **Verdicts**: "holds for every input", "holds for 2 of 2 examples", "does not hold at …". This is the best verdict wording on the list.
- **Catalogue and report**: no natural names.

**Three sentences, using real fixtures**

- "Holdsfor says the transfer rule does not hold at sender = 1, receiver = 18446744073709551615, amount = 1."
- "The total-of-balances rule holds for every input of the model; its reading rests on 5 pieces nobody has signed."
- "Run `holds check` on the feature file before you merge."

**Collisions.** None found. crates.io, `cargo-holdsfor`, PyPI, npm, the GitHub account, GitHub repository search (0), Reservoir and all four domains are free. The web returned nothing.

**Weaknesses.**

- **It is a sentence fragment that looks like a typo.** People will type "Holds For" or "Holdfor", and it is awkward as a noun: "we checked it with Holdsfor".
- **It needs its tagline.**
- Its real value is the verdict wording, which any name can adopt.

### 2.4 Plainrule

**Tagline.** *One plain rule, one fixed meaning, and graded evidence that the code obeys it.*

**Names for the parts.**

- **Command**: `plainrule`.
- **A compiled sentence**: "a plain rule".
- **Catalogue**: "Plainrule phrases".
- **Report and method**: plain descriptive names.

**Three sentences, using real fixtures**

- "Write it as a plain rule and read what it compiles to."
- "Plainrule refused 'A deposit earns interest': 'interest' is not in the vocabulary."
- "Of the 14 plain rules in the fixtures, 13 had to be reworded before they compiled."

**Collisions.**

- **Registries, GitHub and Reservoir**: crates.io, PyPI, npm and the GitHub account are free, GitHub has 0 repositories with the name, and Reservoir has nothing.
- **Web**: nothing.
- **Domains**: `plainrule.com` is registered; `.dev`, `.io` and `.org` are free.

**Weaknesses.**

- **It advertises what the tool is worst at.** The person who wrote the fixture rule called it "A transfer the sender can afford always succeeds". The line that actually compiles is "A transfer for which the amount is not more than the sender's balance is always accepted". Controlled English is easy to read and hard to write (`positioning.md`), and "plain" promises the writing side.
- **It is bland**, and says nothing about checking.

### 2.5 Rulestone

**Tagline.** *Rules with one fixed meaning, set in stone and checked against the code.*

**Names for the parts.**

- **Command**: `rulestone`.
- **Catalogue**: "the Quarry" *(earlier list)*.
- **Report**: "a tablet".
- **Method**: "cut once, never recut", which does fit append-only frames.
- The catalogue and report names feel forced.

**Three sentences**

- "We checked the ledger rules with Rulestone."
- "'Never changes' is cut in stone: a new meaning gets a new piece, never an edit."
- "Rulestone says the transfer rule fails at sender = 1, receiver = 18446744073709551615, amount = 1."

**Collisions.**

- **Registries, GitHub account and Reservoir**: crates.io, PyPI, npm and the GitHub account are free, and Reservoir has nothing.
- **GitHub repositories**:
  - atlasgurus/rulestone, a Go rule engine (https://github.com/atlasgurus/rulestone).
  - xvalleycorp/RuleStone: "Open-source business rules engine for banking and finance, in Java. Versioned, effective-dated decision tables … Every version set in stone." Created 2026-10-22 (https://github.com/xvalleycorp/RuleStone).
- **Domains**: `rulestone.com` and `rulestone.io` are registered.

**Weaknesses.**

- **It sounds like a business-rules engine**, which is the kind of code this project checks, not the checker. A banking rules engine already uses the same name and the same "set in stone" line.
- **Search engines correct it to "Runestone"** *(earlier list; I did not reproduce this)*.
- It keeps a Rosetta-like lineage we are trying to drop.

## 3. Recommendation, runner-up, and the stranger test

**Recommendation: Readback, with the Phraseology.** Use it as the working name in drafts now. Do not register packages or rename code until the stranger test is done.

Why Readback over Everycase:

- **It matches the project's own thesis.** The README says that as proofs get cheap, the scarce thing is knowing what was proved. Readback names that. Everycase names the proof, and the project's own K2 result says proof is not where most of the value is (no injected bug needed a proof to be caught). Kani already claims exhaustive checking.
- **It is true at every level of evidence.** Everycase is false at every level below proof.
- **Its parts get names from one real practice.** Phraseology and readback come from aviation, so the catalogue can be named without inventing anything. The word "phraseology" also suggests the right governance: an issued standard, not a growing library of truths. That answers the Mathlib question in the name itself.
- **Its namespace problems are the cheap kind.** The cargo subcommand is free, the PyPI and npm holders are small, and nothing in verification uses the name. Everycase's problem, the overclaim, is the expensive kind: it is in every sentence anyone writes about the tool.

**I would switch to Everycase if** strangers cannot say what Readback does even after the tagline. I would also switch if the human echo trial falls well short of the owner's bar.

**Runner-up: Everycase.** If it wins, keep "every case, or the case that breaks it" next to the name everywhere. Put the strongest evidence held in the first column of every report.

### The five-stranger test

**Who.** Five people who have not seen the project:

- two engineers who own backend or decision code;
- one policy or product owner who does not read code;
- one formal-methods person (Lean, Coq, Isabelle or Dafny);
- one security reviewer or auditor.

That matches the audiences in `positioning.md`. Do not use model readers; the project's own rule is that models are instruments, not judges. Running this next to the human echo trial costs about ten extra minutes per person.

**Materials.** For each name, a three-line header (name, tagline, one sentence of status) above two real blocks from today's report:

- the refuted transfer rule;
- the proved total-of-balances rule, with its line "0 of 5 vocabulary pieces signed off by anyone".

Add one rule marked "tested only". Use real output only.

**Procedure.** Show half the people Readback first and half Everycase first.

1. **Cold.** Say the name aloud with no tagline: "A developer tool is called X. What do you think it does?" Write the answer down verbatim.
2. **Spelling.** "Type it as you heard it." Record the spelling.
3. **Header.** Show the header and the blocks. Ask: "In one sentence, what did the tool tell you about each rule?"
4. **Overclaim probe.** Point at the "tested only" rule. Ask: "Did the tool check this rule for every possible input?"
5. **Recall.** After the echo trial or ten minutes of other talk, ask: "What was the tool called?"
6. **Preference, last and weighted least.** "Which name would you be comfortable writing in a security review or a CI config?"

**Decision rule.** Fix it before the first session.

- **Everycase wins** if at least 4 of 5 guess its purpose correctly cold (checking code against a rule, or against all inputs) **and** at most 1 of 5 answers "yes" to the overclaim probe.
- **Readback wins** if at least 4 of 5 describe it correctly after the header **and** at most 1 of 5 still connect it with aviation, audio or graphics after the header.
- **If both pass**, choose Readback. **If neither passes**, use neither name and keep looking, with this test as the filter.
- **If any one person reads an embarrassing or hostile meaning**, discuss it before choosing, whatever the counts.

Five people will find disasters, not preferences. Do not read a 3-to-2 split as a result.

## 4. Names to avoid

| Name | Why | Evidence |
|---|---|---|
| **Rosette**, `lean-rosette`, Rosetta, Stele, Triglot | Section 1. Triglot also needs explaining, and "three" is the wrong count: the hand-model route has no Rust, and the chain has five or more layers. `github.com/triglot` is a 2026 organisation (a multilingual chatbot) | Section 1; https://github.com/Triglot/triglot-mvp |
| **Verdict** | A formally verified Rust project already uses it. Keep "verdict" as the report's own word | crates.io `verdict`: "A formally-verified X.509 certificate validator" (https://crates.io/crates/verdict); the Verus group's work *(earlier list)*. `cargo-verdict`: "Structured cargo verdicts", updated 2026-11-03 (https://crates.io/crates/cargo-verdict) |
| **Hallmark** | Taken in exactly our neighbourhood, at scale | Nutlope/hallmark: 52,714 stars, "Anti-AI-slop design skill for Claude Code, Cursor, and Codex", pushed today (https://github.com/Nutlope/hallmark). tiagocolombo/hallmark, in Rust: agentic review where "Only commits that earn a hallmark leave your machine" (https://github.com/tiagocolombo/hallmark). crates.io: Nix primitives (https://crates.io/crates/hallmark). npm: a Markdown linter (https://www.npmjs.com/package/hallmark). Plus Hallmark Cards *(memory)* |
| **Proofmark** | Crowded with AI-checking tools and one Rust contract tool, and "proof" overclaims | andrewcooke89/proofmark: "Deterministic wiring and contract assertion engine for Rust workspaces" (https://github.com/andrewcooke89/proofmark). PyPI: "Structured LLM output that has been tested, not just typed" (https://pypi.org/project/proofmark/). npm: "Quality gate for AI responses". dugu0011/proofmark: an AI pentester "that proves what it finds". A US trademark application *(earlier list)*: I could not load that page (DNS failure), so this is unverified |
| **Ruleproof** | Fifteen GitHub repositories, all from 2026, nearly all about rules for coding agents. One matches our domain and pitch. "-proof" also reads as "resistant to" | h-a-forster/ruleproof checks whether an agent followed AGENTS.md (https://github.com/h-a-forster/ruleproof). PrinceXDev/ruleproof: "Turn access rules into verifiable API checks … inspect the evidence" (https://github.com/PrinceXDev/ruleproof). stilburn007/ruleproof lints agent instruction files |
| **Rulelib** | Free, but it borrows Mathlib's authority for definitions that people vouch for and no kernel proves (`FORM.md`). "Rule library" is also generic in enterprise rule products | Registries free; margoseltzer/rulelib (Bayesian rule sets) |
| **Phrasebook** | Fine as an ordinary word in prose, not as a package. It also suggests approximate tourist meaning | crates.io `phrasebook`: Fluent localisation, updated 2026-10-21 (https://crates.io/crates/phrasebook); taken on PyPI and npm |
| **Demotic**, Interlinear, Cartouche, Catena, Dragoman, Calque | Each needs a paragraph of explanation, so each fails the brief's rule. Interlinear is also taken on PyPI ("Interlinear text handling", 2026) and npm (an IDE for AI translations of PDFs). Calque is a crates.io placeholder, and a vocabulary allow-list checker *(earlier list)* | Registry checks today |
| **Invariably** | Mostly free, but it is a five-syllable adverb and fits only "always" and "never changes" | `github.com/invariably` is an account; becdetat/invariably (class invariants, 2014) |
| **Rulebound**, Plainspec (my own; tried and dropped) | Clear compounds, both already used by 2026 tools near ours | npm `rulebound`: "A simple rule based testing framework". origo-labs/rulebound: "A supervisor for coding agents (Rust only)". PlainSpec/spec: "Official PlainSpec standard: normative spec text, JSON Schemas, conformance fixtures, and governance" |
| Keystone, Assay, Touchstone, Gloss, Given, Concordance, Decree, Evident, Warrant, Countersign, Upheld, Rulecheck, Proofread, Watertight, Plainproof | Taken on at least one of crates.io, PyPI and npm, several by testing or AI-checking tools | Notable crates.io holders, checked today: `assay`, a Rust testing macro with 80,594 downloads; `decree`, "Durable state-machine workflows … for scripts, AI agents and people"; `evident`, pub/sub with 16,754 downloads; `touchstone`, `keystone`, `gloss`, `given`, `concordance`, `warrant`. The other names are free on crates.io but taken on PyPI or npm |
| "Frames" or "Framelib" as the public name of the catalogue | "Frame" already means the frame rule and frame conditions of separation logic | *(earlier list)*; I agree |

## What I am unsure of

- **No trademark search.** The Hallmark Cards and PROOFMARK points are judgement or second-hand.
- **"Free" means the exact spelling returned 404 today.** I checked no near spellings, apart from `cargo-<name>`.
- **GitHub searches were unauthenticated and limited to the top eight results by stars.** An account that exists may be dormant.
- **Reservoir was read through its index repository.** A Lean package missing from the index would not show.
- **Web searches were US-only and returned summaries.** A small or non-English project could be missed.
- **Why the owner chose "Rosette" is not recorded**, so the case for keeping it may be stronger than I have stated.
- **The GitHub rename redirect, the ICAO detail of "phraseology", Rosetta Code and Rosetta Stone are from memory.**
- **My view that the echo-trial risk to "Readback" is smaller than the earlier lists say is a judgement.**
- **I said none of the names aloud to anyone.** Pronunciation and mishearing are exactly what the stranger test is for.
