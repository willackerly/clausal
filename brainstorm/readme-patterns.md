# README patterns: what works elsewhere, and what that says about ours

Brainstorm for the owner, 2026-11-10. Nothing here has been applied to `README.md`.

## The short version

1. **Lead with the answer, not the input.** Almost no strong README shows the user's input file first. They show the result (a screenshot, a GIF, an output block) and only then the thing you type. Ours opens with 13 lines of Gherkin before the reader knows why they are reading it.
2. **Lead with a refutation, not a proof.** The most persuasive artefact this repository already produces is in `clausal/features/wallet.feature`: a rule that sounds right, whose two example tests pass, and which is false at `sender = 1, receiver = 18446744073709551615, amount = 1`. "PROVED" on a conservation law is the boring case. Use the surprising one.
3. **The current opening example is a mock-up, and that is the real reason it feels wonky.** The sentence "Internal fund transfers never change aggregate account value" is in no fixture (it appears only in `docs/VOCABULARY.md` and `docs/PLAN.md`), the report block is not the tool's real output format, and it says "5 vocabulary pieces, all signed" where today's real report says "0 of 5 vocabulary pieces signed off by anyone". A project whose pitch is "say what it rests on" should not open on an artefact that rests on nothing. The disclaimer ("This is the target") arrives 20 lines later.
4. **Verification projects mostly show no code at all in the README.** Verus, Dafny, dbt, Alloy, TLA+ and the Mathlib page have zero code blocks. Kani has one 13-line harness. They sell with a one-sentence definition, a screenshot and a status line. Code is for the tutorial.
5. **Nobody in our neighbourhood says what they are not, and it costs them.** Kani, Dafny, Cedar and Alloy leave limits to other pages. Aeneas, hax, Verus and Ogma state limits in the README and read as more trustworthy for it. Slate has the best single line of this kind: "This is not a component library. It is how you build your component library." We need our equivalent and do not have one.
6. **The scope the owner wants stated (tooling, libraries, methodology, checkers, not-yet, upstream tools changed) is not in the README.** The library idea is the fourth section; the Mathlib kinship is not mentioned; the Aeneas patches appear as half a risk bullet.
7. **One README cannot serve three readers.** Pick the engineering lead for the README, let `docs/ARCHITECTURE.md` open for the formal-methods reader (it nearly does already), and give agent builders their own short page. Three outlines with their first 150 words are in section 5.

## 1. How I did this, and what to distrust

Every page below was opened today through a fetch tool that returns a summary of the page, not the rendered page. So: section orders and the position of the first code block are reliable; verbatim quotes are limited to short ones the tool returned; judgements about visual impact are from structure and raw markup, not from seeing the pixels. Two things failed: `cedarpolicy.com` returned only a page title (it is rendered by script), so Cedar is represented by its GitHub README; and awesome-readme credits `themerdev/themer` with a flowchart that I could not confirm (there is one image captioned "visual description").

awesome-readme lists 101 examples. **None is a formal verification tool.** The nearest are NASA's Ogma (runtime verification), Yampa (an embedded language), HMPL (a template language), HTMLHint (static analysis), Size Limit (a CI checker) and dbt (a compiler). I picked 13 with those weighted in.

I did not open our own SVG diagrams, so I have no view on their visual quality.

## 2. Source notes

Each entry: order of sections; above the fold; first code; is / is not; visuals; tone; one thing to copy; one thing to avoid.

### The three the owner named

**Lean's Mathlib page** (lean-lang.org/use-cases/mathlib)
- Order: unheaded intro, What is Mathlib?, Why Mathlib Matters for Research and Industry (five sub-claims: research platform, maintenance, quality assurance, industry, community), Getting Started.
- Above the fold: one framing sentence about why a library matters, then a one-sentence definition ("a community-driven library of formalized mathematics written in Lean").
- Code: none anywhere. Visuals: none.
- Is / is not: "is" in one sentence; no "is not".
- Tone: formal, addressed by name to "decision-makers considering Lean and Mathlib for their organizations".
- Copy: the ordering. What is it (one sentence), why it matters to the person who decides, then how to start. And the "why" is split by *kind of reader concern* (maintenance, quality assurance), not by feature. One scale number ("over two million lines") is stated twice.
- Avoid: it can get away with zero evidence on the page because Mathlib's reputation precedes it. We cannot. Also no limits anywhere.

**electrikhq/slate**
- Order: banner, one-line tagline, badges, link row, rule, one-paragraph definition, the "is not" line, a status line, table of contents, Why Slate, Screenshots, Features, Quick start (four numbered steps), Usage, Components, Theming, AI and agents, Requirements, Documentation, Development, Contributing, Security, License.
- Above the fold: banner image, a bold line of four noun phrases, a row of links to docs, then "**Slate** is a set of ... components that you can customize, extend, and build on", then "This is not a component library. It is how you build your component library.", then "> **Status:** 3.0.0 stable."
- First code: `composer require ...` under Quick start, after Why, Screenshots and Features.
- Visuals: banner; seven screenshots stacked. In raw markup the layout devices are modest: three `<p align="center">` blocks, a horizontal rule, and tables. No columns, no image widths.
- Tone: short declaratives.
- Copy: (a) the header stack: definition, is-not, status, in three consecutive lines; (b) the "Why" section as a two-column table, "You want ..." / "Slate gives you ...", six rows. That table is the best device I saw for a lead-with-value opening, and it adapts directly (see rules of thumb).
- Avoid: seven full-size screenshots in a row before any explanation; a contents list of 12 items for a page that is mostly tables.

**dmunish/notecharts**
- Order: banner, three badges (one is "Try on Colab"), opening paragraph, four-image gallery, Why notecharts?, Key Features, Installation, Usage (Palette Browser, Templates, With DataFrames, Full Control, Saving Charts), Notes, License, Links.
- Above the fold: banner, a one-sentence statement of what it brings, a gallery of results.
- First code: one-line `pip install`; the first real code is under Usage.
- Is / is not: by contrast with two named alternatives, positioned as "the thinner, more faithful option". Caveats are held in a short Notes section near the end (security, connectivity).
- Copy: the walkthrough is a ladder. Each step adds exactly one idea (browse, use a template, bring your own data, take full control, save). Results gallery comes before any explanation.
- Avoid: nothing structural. It is a small library and the pattern is sized for one; do not mistake its brevity for a target.

### From awesome-readme

**NASA/ogma** (runtime verification; the closest relative on the list)
- Order: definition, Features, two GIFs, contents, Installation, Usage per target (each with its own "Current limitations" subsection), Contributions, Acknowledgements, License.
- Above the fold: "Ogma is a tool to facilitate the integration of safe runtime monitors into other systems." then "Ogma extends Copilot ...".
- First code: `apt-get install`. Then a great deal of code.
- Is / is not: limits are attached to the feature they limit ("preliminary", "not guaranteed correct; the user must check the output").
- Copy: **limits live next to the capability they qualify**, in a subsection with a fixed name. And the second sentence names what it builds on.
- Avoid: the README is the manual. It runs very long, and the value statement is never revisited.

**ivanperez-keera/Yampa** (embedded language)
- Order: title, badges, one-sentence definition, link row, Features, Installation, Examples, Related projects (games, use in industry), Documentation (with Publications), Contributions, History.
- First code: install commands; then one concept shown in three equivalent styles.
- Copy: "Use in industry" with shipped products, and "Publications" as a section. For research infrastructure, who relied on it is the proof.
- Avoid: feature bullets that are adjectives ("robust, elegant, stable").

**hmpl-language/hmpl** (template language)
- Order: banner, tagline, badges, links, Introduction, Example, Basic usage, Usage with DOM, Why HMPL?, Features, Installation, tools, community, roadmap.
- First code: immediately after the introduction, about six lines.
- Copy: for a *language*, a tiny example straight after the definition does work, because the syntax is the product.
- Avoid: the same code shown twice (once plain, once commented); star-history charts; "can be a great alternative to" named rivals with no evidence.

**htmlhint/HTMLHint** (static analysis)
- Order: hero GIF, title, tagline, badges, contents, Installation and Usage, Example output, Configuration, Docs.
- Copy: a section literally called "Example output". Checkers are understood by what they print.
- Avoid: the "what is it" is only a tagline. Fine for a linter, fatal for us.

**ai/size-limit** (CI checker)
- Order: title, logo, definition, bullets, output screenshot, Who Uses Size Limit, How It Works (five numbered steps), Usage by case, Reports, Config, API.
- Above the fold: definition ("a performance budget tool for JavaScript"), what it does in CI, a screenshot of the output.
- First code: `npm install`, after Who Uses and How It Works.
- Copy: **the order "what it prints, who relies on it, how it works in five steps, then usage"**. Who-uses entries carry a number and a link to the commit.
- Avoid: usage split four ways by project type before the reader has succeeded once.

**dbt-labs/dbt-core** (compiler)
- Order: logo, badge, a warning callout about versions, bold one-sentence tagline, architecture diagram, About v2, Understanding dbt (with a second diagram), Getting started, community.
- Code: none.
- Copy: one diagram directly under the tagline that shows input, tool and output. And "Understanding dbt" explains the central noun ("models") in three plain sentences.
- Avoid: the first thing a newcomer reads is a migration warning for existing users.

**treeverse/dvc**
- Order: logo, link row, badges, definition with five capability bullets, Quick start, How DVC works, extension, Installation, community.
- First code: not a code block. A two-column table, "Task | Terminal", six rows.
- Is / is not: three analogies ("Git for data", "Makefiles for ML"), each immediately qualified by how it differs from the thing named.
- Copy: the Task/Terminal table. A whole workflow in one screen, each command labelled with its purpose. Also: analogy plus its limit in the same breath.
- Avoid: twelve badges.

**Day8/re-frame**
- Order: logo, an epigraph, Overview, Documentation, Current version, Getting help. About 450 words.
- Code: effectively none.
- Copy: a README can be short and send people to real documentation, provided the documentation exists. It has a point of view and states it.
- Avoid: in-jokes and swagger ("unfair advantage") that only work once you are loved.

**feberts/python-game-server**
- Order: badges, title, one-line description, **one diagram**, Features, Use cases, Quick start, Implementing clients, Adding new games, Operating the server, About.
- First code: about 25 lines, under Implementing clients.
- Copy: one diagram, directly under the one-line description, before anything else. "Use cases" as its own short section.
- Avoid: the first code block has placeholder comments instead of working lines.

**themerdev/themer**
- Order: logo, title, intro, one explanatory image, contents, Getting started (a comparison table of its two front ends), CLI, API, catalogues, Prior art, Contributing.
- Copy: a "Prior art" section near the end. Cheap, generous, and it answers "how is this different" for the informed reader.
- Avoid: catalogues inline in the README.

**vhesener/Closures** (credited by awesome-readme for its "cognitive funnel")
- Order: logo, badges, two-sentence pitch, Usage Overview (three steps of rising complexity), Dive Deeper, Installation, Background.
- Copy: the funnel: pitch, simplest possible example, one step up, one more, then "dive deeper" links, and **installation after the examples**. Also a modest stance: it "makes no claim" to be better than the pattern it replaces.
- Avoid: full licence text inline.

**github-changelog-generator**
- Order: contents, title, slogan, "What's the point of a changelog?", "Why should I care?", Installation, Usage, Output example, migrating, Features, Alternatives, FAQ.
- Copy: question headings for the "why" ("What's the point of ...?"), an output example, and an FAQ whose first entry is the strongest objection ("why use this if GitHub Releases exists?").
- Avoid: "None satisfied my requirements" about alternatives, with no reasons.

**Skydio/revup**
- Order: logo, badges, one-sentence summary, GIF, Features, Compatibility, Installing, Tutorial (five steps), More features, Configuring, Appendix (background, peer projects, disclaimer).
- Copy: an **Appendix** inside the README for philosophy and peer projects, which keeps the top clean without deleting the thinking.
- Avoid: nothing notable.

### Adjacent projects

**Kani** (README and book)
- Order: logo, badges, definition, two bullets (safety, correctness), Installation, How to use Kani (a 13-line harness), GitHub Action, Citing, Security, Contributing, License.
- Above the fold: "The Kani Rust Verifier is a bit-precise model checker for Rust." then what it checks, split into Safety and Correctness with a concrete example each (`unwrap()` on `None`).
- Is / is not: nothing in the README beyond "will try to prove". The book's front page is better: a "Project Status" paragraph, and the sentence that model checking "will prove a property, disprove it with a counterexample, or run out of resources". The book also has a tool-comparison page (fuzzing, property testing, model checking) that says what each is good at and that Kani "does not support verifying concurrent code".
- Copy: the three-outcome sentence; and the comparison page's fairness to proptest and fuzzing. Our own measurements (`clausal/compare/TRADES.md`) say the same thing and we should be as plain.
- Avoid: limits one click away from the pitch.

**Verus**
- Order: badges, logos, definition, screenshot, Status, Try Verus, Documentation, Examples, Getting in touch.
- Above the fold: "Verus is a tool for verifying the correctness of code written in Rust." Developers write specifications; Verus checks them statically for all executions.
- Code: none. One editor screenshot.
- Is / is not: a section called **Status**, second on the page: under active development, features "may be broken and/or missing", supports "a subset of Rust". Followed at once by the list of papers and projects that use it.
- Copy: **Status as the second heading, immediately followed by evidence of use.** Candour and credibility in adjacent lines.
- Avoid: no example of what a specification looks like anywhere on the page.

**Aeneas**
- Order: a fresco, title, definition, Project Structure, Installation, Documentation, Usage, **Targeted Subset And Current Limitations**, Backend Support, adding models, Formalization.
- Is / is not: limits are split into two groups: things they plan to fix, each marked as technical not fundamental, and things that need different theory (unsafe code, concurrency).
- Copy: that split. "Not yet" and "not by this approach" are different statements and readers need both.
- Avoid: no statement of value at all. It defines itself by its mechanism (MIR to a pure lambda calculus). A reader who does not already want it learns nothing.

**hax**
- Order: badges, logo, title, definition, "Try out hax online now!", Supported Backends (logo grid with status markers: stable, active development, experimental), Learn more, Usage, Installation, Supported Subset of the Rust Language, Publications, Contributing.
- Copy: **a per-component status grid.** One glance says what is solid and what is experimental. Also a playground link in line two.
- Avoid: status carried only by coloured emoji.

**Cedar** (GitHub README)
- Order: title, logo, badges, definition, **Expressive / Performant / Analyzable** (three short value sections), Using Cedar, crates, Quick Start (a five-line policy, a small JSON, two commands, ALLOW and DENY), Documentation, Building, What's New, compatibility.
- Copy: three one-word value headings, then a quick start whose example shows **both outcomes** (ALLOW and DENY). An example with only the happy outcome teaches half the tool.
- Avoid: the formal verification behind Cedar, its most unusual asset, is not mentioned in the README. They undersell the thing we would lead with.

**Dafny** (dafny.org and the README)
- Order: definition, promise, animated demo, Community, Try Dafny, Read more.
- Above the fold: "verification-aware programming language"; the verifier "constantly looks over your shoulder", flags errors, shows counterexamples, "congratulates you"; assurance that reduces "costly late-stage bugs".
- Code: none as text; a demo GIF.
- Copy: the value is stated as an experience (what happens while you type) and as a cost avoided, in two sentences.
- Avoid: no limits, no status, no named users.

**TLA+** (Lamport's page; the tools README)
- Lamport's page: first person, defines TLA+ as "a high-level language for modeling programs and systems", says it removes design errors that are costly once they reach code, then eight one-line links (High-Level View, Industrial Use, Learning, tools).
- The tools README: four headings, no example specification.
- Copy: "Industrial Use" as a top-level destination; a single sentence about cost avoided.
- Avoid: a landing page that is only a router. It works because of who wrote it.

**Alloy** (alloytools.org)
- Opens "Alloy is an open source language and analyzer for software modeling", then release notes. No model shown, no visualisation, no mention of bounded analysis.
- Copy: nothing.
- Avoid: all of it. A tool whose whole appeal is a picture of a counterexample shows no picture.

## 3. Patterns across the set

- **First screen = definition + result + status.** The best ones (Slate, Verus, Size Limit, python-game-server, dbt) fit a one-sentence definition, one image or output block, and a status line into the first screen.
- **The first code block is nearly always the install command, and it comes after "why".** Where real code appears early (HMPL, Kani, Cedar) it is 5 to 13 lines and it is the product's own surface syntax.
- **Verification tools avoid showing specifications.** I read this as a weakness they share, not a pattern to copy: specifications look frightening. That is our opening. Our "specification" is an English sentence. We can show it in line three without frightening anyone. Showing the Gherkin scaffolding around it throws that advantage away.
- **Output examples beat input examples** for checkers (HTMLHint, Size Limit, changelog generator, Cedar's ALLOW/DENY).
- **Limits are credible when they are structured**: next to the capability (Ogma), split into not-yet and not-by-this-approach (Aeneas), or as a status grid (hax). They are not credible as a general hedge ("under active development").
- **Use and users appear early in the research tools that are trusted** (Verus, Yampa, Size Limit). We have one real target and should say so in the first screen, with its limits.
- **"What it is not" is rare and powerful.** Only Slate does it in a line. Kani's book and Aeneas do it in a section.

## 4. Rules of thumb for our README

1. **First screen budget: about 120 words and one block.** A one-sentence statement of what you get; one result block of at most eight lines; one status sentence with numbers; three links.
2. **The first block is output, and it is real.** It must be copied from a run, trimmed with visible ellipses and nothing added. If the real report cannot be quoted in eight lines (today it cannot: a rule block is about 45 lines), that is a product gap. Add a brief report form to the tool. Do not hand-draw one in the README.
3. **Show both outcomes within the first two blocks**: one refuted with its input, one proved. Refuted first.
4. **The input, when it appears, is one sentence.** A `Rule:` line is the input. The Scenario Outline, placeholders and Examples table are scaffolding and belong in "Try it" or the docs, introduced as "the same rule, in the file format many test teams already use".
5. **No code a reader must parse before the "why".** Lean appears nowhere in the README for the engineering lead. For the formal-methods reader, the first Lean is the statement a sentence compiles to, at most twelve lines, after the trusted-base table.
6. **One diagram above the second heading.** The chain diagram, if it reads at a glance. Not three diagrams in the same style in three consecutive sections.
7. **Say what it is not, in a line, in the first screen.** Candidate: "This is not a new prover or a new translator. It is the part between a requirement and a proof that those leave to chance."
8. **State limits where the claim is made, in the same sentence, with a number.** "Proved for all inputs *of the model*; the model is generated by Aeneas and cross-checked on the example rows." Limits stated beside a specific claim read as precision. Limits gathered in an apologetic section read as weakness. Never state a limit with an adjective where a number exists.
9. **Separate today from target by tense and by place, never by a trailing disclaimer.** Present tense only for what a visitor can run today. One section, clearly named ("Where this is going"), holds everything else. No mock output anywhere. If a target picture is wanted, label it in its caption as a design sketch.
10. **Split not-yet from not-by-this-approach** (Aeneas's pattern). Not yet: new sentences end to end, generated test harnesses, signed vocabulary. Not by this approach: compiler correctness, hardware, code outside the model, concurrency and effects.
11. **A status table by component, not a status paragraph** (hax's pattern, in words not emoji): tooling, libraries, checkers, methodology, each with "works on the fixtures / built, under review / designed / not started".
12. **Name what you build on in the second paragraph**, and what you had to change in it. For an informed reader, "we carry five patches to Aeneas and they took coverage from 1% to 35%" is both a credential and a warning, and both are useful.
13. **One reader per document.** A three-line router under the fold sends the other two readers elsewhere.
14. **Process and history go to an appendix or another file.** How the work is run, and the proof-navigation strand, are not what a first-time visitor came for.
15. **Every number in the README must match the generated report on the day.** Better, generate the status block from `clausal/out`.

## 5. Critique of the current README

Blunt, in order of importance.

**The opening example.** The owner's complaint is right, and I think the cause is five things at once:

- *It is input before payoff.* The reader meets a Scenario Outline before knowing what comes back.
- *The wrong part of Gherkin is on show.* The value is in the one-line `Rule:`. What fills the screen is the scaffolding: angle-bracket placeholders, and an Examples table whose rows (`0 | 1 | 30`) look like a toy and need explaining (are 0 and 1 accounts or amounts?). The same claim is then stated three times: Rule, Then, Reading.
- *The sentence is stilted.* "Internal fund transfers never change aggregate account value" reads as a sentence built to exercise two modifiers, not something an engineer would say. The real fixtures say "A transfer never changes the total of all balances", which is better English.
- *It is not real.* Covered in the short version above: not in the fixtures, not the tool's output format, and "all signed" contradicts "0 of 5 signed". I would treat this as the most serious problem in the file. It is honest only by virtue of a sentence 20 lines later.
- *It is the dull case.* A conservation law being true surprises nobody.

Also worth weighing: the word "Gherkin" in line 11. For some engineering leads it means test files they already have. For others it means brittle step definitions and abandoned BDD programmes. For a formal-methods reader it signals "controlled natural language", a field with a long record of disappointment. I am unsure of the proportions. I would stop leading with the word and lead with "a sentence".

**The tagline.** Good content, too long (38 words in bold), and the distinctive clause ("a plain account of what that answer rests on") is last. "Tests show that some cases work. This shows that no case fails" is the best line in the file, but "no case fails" claims more than the chain supports: it is no case of the model. The rest of the README is scrupulous about this, and the second sentence is not.

**No "what it is not".** A visitor cannot tell in the first screen whether this is a prover, a test framework, a translator or a methodology. It is partly all four, and that is precisely why it needs saying.

**Status is under-weighted at the top and excellent at the bottom.** "Research prototype, November 2026, Apache-2.0" is one unbolded line. "Where it stands" is the strongest section in the document and is the eighth thing on the page. Lift a two-sentence version with numbers into the first screen and keep the full section.

**The scope is not stated.** The owner's list (tooling, libraries, documented methodology, checkers, not-done-yet, existing tools modified) does not appear as a list. Specifically:
- The reusable pieces, which the owner regards as a large part of the final product, are section four, framed as "why it can scale", not as a deliverable.
- Mathlib is not mentioned.
- The methodology (the TDFLite pattern for code that is not Rust, in ARCHITECTURE section 12) is not in the README as a thing the project offers.
- The checkers (ARCHITECTURE section 7, the most distinctive table in the repository) get one bullet.
- Upstream changes get half a bullet under risks.

**A caution on the Mathlib kinship.** It is fair as a statement of design intent: a shared library that grows, where the second user pays less than the first. It is weak as a claim, for two reasons a formal-methods reader will spot at once. Mathlib has two million lines and hundreds of contributors; this has 23 frames, one author and no signatures. And the trust model differs in kind: a Mathlib lemma is true because the kernel checked it, while a frame is *adequate* because a person says its Lean definition means the English phrase. The closer relatives on that axis are a standard or a controlled vocabulary (specification pattern catalogues, requirement templates). I would write "meant to grow the way Mathlib has" and state the difference in the next sentence. Saying it first disarms the objection.

**Two projects in one README.** "Also here: making large proofs navigable" is a different project with a different reader, and "It has been humbling" is the wrong note three quarters of the way down a pitch. One line and a link. Related: the repository name and `AGENTS.md` still describe the older project ("Operational Constitution for Lean-Ghidra Agents", proof slicing, quadrants). A public visitor who opens `AGENTS.md` will think they are in a different repository. There is also a PDF about decompiling proofs in the root.

**The name.** "Rosette" is already a well-known solver-aided programming language in the verification community. Formal-methods readers will assume a connection. Not a README fix, but the README is where it bites.

**"How the work is done" is internal.** It tells a visitor about the owner's process, not about the product. Move to `docs/PLAN.md` or a contributing file.

**No "Try it".** The only runnable command is three lines at the bottom under "Find your way around", with no heading, no prerequisites, no time or disk estimate and no expected output. With four pinned Lean toolchains and an exact Rust nightly, a visitor needs to be told what they are in for, or shown the committed `clausal/out/report.md` as the way to see results without building.

**Unexplained names.** "TDFLite" appears with no gloss. "Vector180" appears in a table.

**Numbers do not agree.** The README says 23 frames; today's `clausal/out/report.md` says 19 frames, 27 modifiers and 31 domain words. The README says five patches; `docs/RESULTS.md` says four; `docs/PLAN.md` says three defects in one place and five reports in another, and 34% in one place against 35% elsewhere. Each has an innocent explanation. Together, in a project that sells evidence hygiene, they are the kind of thing a sceptical reviewer screenshots.

**Diagrams.** Three in three consecutive sections and none in the first screen. I have not looked at them.

**What is good and should survive.** The three-reason "Why it matters". The sentence "A proof of the wrong statement is worthless, and it looks exactly like a proof of the right one." The "Rests on" idea. "Where it stands", including the open risks. The absence of badges and hype. The length (about 1,500 words) is right; the distribution is wrong.

## 6. Three candidate outlines

### A. For an engineering lead of security-critical Rust (my recommendation for the README)

Sections:
1. Statement, refuted rule, proved rule, status (first screen)
2. Why this matters (the existing three reasons, cut to 80 words)
3. What you get back: the "rests on" block from a real run, and the chain diagram
4. What this is not, and when not to use it (four bullets, with the not-yet / not-by-this-approach split)
5. What is in the box: a status table with rows for tooling, libraries, checkers, methodology
6. Where it stands (existing section, numbers regenerated)
7. What we had to change upstream, and what is not built yet
8. Try it: read the committed report first; then prerequisites, time, command, expected output. The `.feature` file appears here for the first time.
9. Where this is going (one paragraph, future tense, including the library ambition)
10. Other readers: formal methods (ARCHITECTURE), agent builders, documentation map

First 150 words or so:

> # lean-rosette
>
> **State a requirement in one English sentence. Learn whether your Rust code meets it for every input, and see what that answer rests on.**
>
> Here is a rule about a small wallet crate. It sounds right:
>
> > A transfer the sender can afford is always accepted.
>
> Its two example tests pass. The rule is false:
>
> ```text
> Verdict   REFUTED (false at a concrete input, kernel-checked)
>           counterexample   sender = 1, receiver = 18446744073709551615, amount = 1
> ```
>
> The receiving balance would overflow, so the code rejects the transfer. A neighbouring rule, *a transfer never changes the total of all balances*, comes back **proved for all inputs**, with a list of what that rests on: what a proof kernel checked, what was tested, what depends on a tool, and what depends on a person's say-so.
>
> **Research prototype.** This runs end to end on two small example crates (14 rules: 10 proved, 3 refuted, 1 refused as not understood). It cannot yet be pointed at your own crate. [What works and what does not](#where-it-stands).

The two verdict lines are copied from today's `clausal/out/report.md`. The counts are from the same file. Note the proved rule's real block currently ends "0 of 5 vocabulary pieces signed off by anyone", and the README should show that line, not hide it.

### B. For a formal-methods practitioner

Sections:
1. Definition, is / is not, status in numbers
2. The three gaps: meaning, proof, model (ARCHITECTURE section 1)
3. The chain of assurance as a table, with evidence kinds. For this reader, the trusted-base table is the hook.
4. One rule traced through: sentence, pieces, Lean statement, theorem, audit (first Lean here, twelve lines at most)
5. The vocabulary as a library: frames, modifiers, domain words; typed holes; refusal; second readings; how it differs from Mathlib and from requirement-pattern catalogues
6. How the tool checks itself (the "failure it prevents" table)
7. Relation to Kani, Verus, Aeneas, hax, Dafny: what is used, what is not replaced, what each does better
8. Measurements, including the negative ones
9. Upstream changes; limits; open design questions
10. Reproduce

First 150 words or so:

> # lean-rosette
>
> **A pipeline, and a growing library, for stating requirements in controlled English and discharging them in Lean 4 against Aeneas-generated models of Rust, with the trusted base reported link by link.**
>
> It is not a new prover, translator or specification language. It uses Charon and Aeneas, Lean's kernel and cucumber-rs, and works on what those leave open: whether the theorem proved is the requirement its owner meant.
>
> A sentence is never interpreted whole. It is compiled, fail-closed, from typed pieces defined once in Lean: frames such as *never changes* and *exactly when*, modifiers, and domain words bound to model functions. The reading is echoed in English, proved equivalent to the statement the proof is about, and searched for counterexamples that are replayed on the compiled Rust.
>
> Today: two fixture crates, 35 scenarios. Loops cost about six lines of Lean per line of Rust. Aeneas as shipped translated 1% of functions in ten real crates, 35% with patches carried here. Nobody has yet signed the vocabulary.

This reader forgives roughness and punishes vagueness, so the numbers go in the first screen. "Controlled English" is the term they will use whatever we call it, so use it and get credit for knowing the literature.

### C. For a builder of coding agents

Sections:
1. Pitch, the verdict set, status
2. The loop: what the agent may write (code, proofs), what it may not touch (rules, vocabulary), what comes back. One diagram.
3. Verdicts as an interface: a short excerpt of the machine-readable result (first code here, about ten lines)
4. How it resists gaming (the self-check table, cut to the rows about agents)
5. What agents have done so far, with costs
6. The cheap inner loop and the expensive outer loop: tests and bounded checks for fast feedback, proof for the final answer
7. What integration would need; honest state of packaging
8. Limits and direction

First 150 words or so:

> # lean-rosette for agent builders
>
> **A coding agent will make any build green. This gives it a target it cannot bend: a requirement in English, compiled to a Lean statement the agent may prove but may not edit.**
>
> For each rule the pipeline returns one of a fixed set of verdicts (proved for all inputs, refuted with a counterexample, tested only, not understood) and a machine-readable graph of the evidence behind it. Only a kernel-checked theorem of exactly the generated type counts as proved, so proof text is untrusted whoever wrote it.
>
> What has been measured: on a crate neither had seen, two language models each proved all seven loop functions in under fifteen minutes. The known hazard is an agent proving around a bug that no rule forbids. Mutation runs and a suite-adequacy check exist to expose that, and "shown false" is counted separately from "proof lost".
>
> Research prototype: two small Rust crates today, not your codebase yet.

I am least sure of this one. It is the most fashionable pitch and possibly the largest audience, and the measured result is the weakest of the three (textbook loops, two fixture crates). I have also not checked what the command-line surface returns (exit codes, a stable result file), so section 3 may describe something that needs building. I would write it as a page under `docs/`, not as the README.

## 7. What I would do, in order

1. Replace the opening with the refuted-rule version (outline A), using real output only.
2. Add the is-not line and the two-sentence status to the first screen.
3. Add "What is in the box" as a status table covering the owner's six scope headings, and put the library ambition and the Mathlib comparison there, with the trust-model difference stated.
4. Move the proof-navigation strand and "How the work is done" out; fix or remove the stale `AGENTS.md`.
5. Add "Try it" with the committed report as the zero-install path.
6. Reconcile the numbers, ideally by generating the status block.
7. Give the tool a brief report form so the README never needs a hand-drawn block again.

## 8. Things I am unsure of

- Whether leading with a refutation undersells the proof side. I think not, since the proved rule follows two lines later, but the owner's goal is "formally modelled by default", and a counterexample finder is not that.
- Whether the engineering lead is the right primary reader today. The honest state (two fixture crates, cannot be pointed at your crate) gives that reader nothing to do. The formal-methods reader can act now: read, criticise, contribute frames. If the next six months are about collaborators, not adopters, outline B should be the README.
- How "Gherkin" lands with each audience. Worth asking three real people.
- Whether a hero image helps. The pattern says yes; I have not seen our diagrams.
- Layout judgements about Slate and notecharts are from structure, not from seeing the rendered pages.
