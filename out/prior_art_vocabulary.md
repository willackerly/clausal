# Prior art check: composable vocabulary track (plan node V1)

Checked 2026-11-10 by web search and direct page fetches. Every claim carries the URL it came from. Three levels of confidence are used:

- **opened**: I fetched the page and read the relevant part.
- **search summary**: I saw only a search-result summary of the source; the source itself was not opened.
- **not verified**: I could not open it, or the page did not contain the detail.

Nothing in the repository was built, run or edited. The frame catalogue in section 1 is a proposal, not a finding.

## Bottom line

- **The frame idea is not new; its target is.** NASA's FRET already does "fixed sentence shapes, each with a published formal reading, echoed back in English and as a diagram". It does it for temporal requirements over signals, checked on models and monitors. Nobody found does it for pre/post claims proved about source code, and FRET has no typed, reusable domain vocabulary and no quantifiers.
- **The proposed frame list has gaps.** Five shapes that existing targets already need are missing from the list in `docs/VOCABULARY.md`: *changes only* (frame condition), *exactly when* (iff), *monotone*, *always answers* (totality, as a frame of its own), and *agrees with* (refinement). The "at most / at least / exactly once" group is the weakest fit to single operations and should be redefined as counting over a collection.
- **`Rule:` works as a carrier, but the universal reading is our convention.** The Gherkin grammar allows Scenario Outlines with Examples under a Rule and allows tags on a Rule. All four runners parse it. No runner gives the Rule line any semantics, and I found no existing convention for marking a Rule as universally quantified.
- **The Cedar claim is correct**, with more detail than the TDFLite plan gives. Section 5 lists what to copy for T4.
- **hax versus Aeneas is no longer a choice between two translators.** Since hax 0.4 (29 Sep 2026) the hax Lean backend *is* Charon plus Aeneas, with contracts and a different proof library layered on top. For T6 the recommendation is plain Aeneas now; reasons in section 6.
- **Closest to the whole chain:** no single system. The nearest on each side are FRET (meaning link, on models), the Aeneas-at-scale report and the FVS skills (proof link on real Rust, with human review of statements), Kiro (requirements to universal properties, tested not proved) and Amazon Bedrock Automated Reasoning checks (echo-back and distinguishing scenarios, on SMT rules not code).

## 1. Property specification pattern catalogues

### What the catalogues contain

**Dwyer, Avrunin, Corbett (ICSE 1999).** Opened: the patterns site.

- Occurrence patterns: Absence ("aka Never"), Universality ("aka Globally, Henceforth"), Existence ("aka Eventually, Future"), Bounded Existence. https://matthewbdwyer.github.io/psp/patterns/occurrence.html
- Order patterns: Precedence, Response ("Follows", "Leads-To"), Precedence Chain, Response Chain, Constrained Chain. https://matthewbdwyer.github.io/psp/patterns/order.html
- Five scopes: Global, Before, After, Between, After-until. A scope includes its starting state and excludes its ending state. https://matthewbdwyer.github.io/psp/patterns/scopes.html
- Mappings exist to LTL, CTL, GIL, QRE and INCA. Globally-scoped LTL forms as restated by the fetch (not verbatim): Absence `G ¬P`, Universality `G P`, Existence `F P`, Response `G (P → F S)`, Precedence `¬P W S`. https://matthewbdwyer.github.io/psp/patterns/ltl.html
- Survey result: over 500 collected specifications, 92% were instances of the patterns (search summary of the ICSE paper, DOI 10.1145/302405.302672). The per-pattern frequency breakdown was **not verified**.

**Konrad and Cheng (ICSE 2005), real-time.** Search summary only: patterns for duration, periodic and bounded real-time properties in MTL, TCTL and RTGIL, with a structured English grammar. DOI 10.1109/ICSE.2005.1553580. Individual pattern names **not verified** from the paper.

**Grunske (ICSE 2008), probabilistic (ProProST).** Search summary: eight patterns from a survey of 152 academic and 48 industrial properties, with a structured English grammar. DOI 10.1145/1368088.1368094. Pattern names **not verified**.

**Autili, Grunske, Lumpe, Pelliccione, Tang (IEEE TSE 2015).** Search summary: a unified catalogue of all known qualitative, real-time and probabilistic patterns "plus 40 newly identified or extended patterns", with one structured English grammar and a tool (PSPWizard). DOI 10.1109/TSE.2015.2398877. A later paper that reuses the catalogue (opened via ar5iv) lists these qualitative and real-time patterns: Absence, Universality, Existence, Bounded Existence, Minimum Duration, Maximum Duration, Recurrence, Precedence, Precedence Chain (N-1 and 1-N), Constrained Precedence Chain, Response, Response Chain, Constrained Response, Constrained Response Chain, Response Invariance, Until; with the same five scopes. Example sentence form: "Globally, if {P} [has occurred] then in response {S} [eventually holds] within t ms." https://ar5iv.labs.arxiv.org/html/2211.03817

**FRET's template space** is the modern successor: scope × condition × timing, originally 8 × 2 × 7 = 112 templates (search summary of NASA papers), later 160, and 560 with the probabilistic extension (opened: https://arxiv.org/html/2512.15788v1).

### How they map to single-operation frames

All of these catalogues are about traces. Our frames are about one call of one operation. The correspondence is real but indirect:

| Planned frame | Nearest catalogue pattern | Fit |
|---|---|---|
| never changes / preserves | Universality of "measure equals its initial value", proved per step | Good, provided the echo says "per operation". The global claim needs induction over steps, which is a separate statement |
| always | Universality, Global scope | Good |
| never | Absence | Good; define as *always not* so there is one definition |
| if-then | Response with zero delay (FRET: condition + `immediately`) | Good |
| only if | Precedence, degenerate: the condition is necessary for the outcome | Good; this is also FRET's "only" scopes |
| rejected-and-unchanged | No catalogue pattern. It is a postcondition plus a frame condition | Ours; needed |
| at most / at least (a bound) | Real-time bounded patterns, with a quantity in place of time | Acceptable |
| at most once / exactly once | Bounded Existence | **Poor.** Bounded Existence counts occurrences along a trace. In a single operation there is nothing to count unless a collection is named |
| Given … | Scope (Before, After, Between) | Only Global and "while condition holds" make sense for one operation |

### Patterns we would be wrong to omit

These are not in the list in `docs/VOCABULARY.md`. Each is forced by a target already in the plan.

1. **Changes only (frame condition).** "A deposit does not touch a bystander" is already a wallet scenario. Without this frame every "increases X by n" is silent about everything else. Not in Dwyer because it is not a trace property.
2. **Exactly when (if and only if).** English "if" is routinely meant as "exactly when". The ambiguity generator (V6) needs both readings to exist as frames.
3. **Monotone.** TDFLite guarantee 4, "giving a subject more entitlements never takes access away", is a claim about two inputs to one function. No single-run frame states it.
4. **Always answers (totality).** `docs/VOCABULARY.md` folds this into every frame. Keep that, but also expose it alone: Cedar proves termination as a named property (section 5), and "the total of a ledger can always be computed" is already a ledger scenario.
5. **Agrees with (refinement or equivalence).** T4 and T6 are both "X gives the same answer as the model". Cedar's "sound slicing" has the same shape.
6. **Independent of (two-run).** Already listed as open in `docs/VOCABULARY.md` and planned as T5. Cedar's "order independence" has this shape too, so it is not only for secrecy.

A cross-check: Cedar's seven proved properties (opened: https://arxiv.org/html/2407.01688v1) are forbid-trumps-permit (*if-then*), default deny (*only if*, contrapositive), explicit allow (*only if*), order independence (*independent of*), sound slicing (*agrees with*), validation soundness (*if-then* across two operations), termination (*always answers*). Three of the seven need frames missing from the planned list.

Deliberately still out: Existence, Response with delay, Precedence over time, chains, and all real-time and probabilistic patterns. One caution: Response is the canonical order pattern, so the first stateful or asynchronous target will need it.

### Proposed first catalogue

Notation: `op` takes a state `s` and an input `a` and yields an outcome `o` that is either `accepted s' r` or `rejected e s'`. `G` is the Given condition, true if absent. Every frame is fail-closed: it also asserts that `op` returns an outcome (no panic, no divergence) for every `s, a` satisfying `G`.

| # | Frame (surface words) | One-line formal reading | Source pattern |
|---|---|---|---|
| 1 | always answers | `∀ s a, G s a → ∃ o, op s a = o` | Termination; fail-closed base of all others |
| 2 | never changes M / preserves M | `∀ s a, G s a → M (state o) = M s` (accepted or rejected) | Universality, per step |
| 3 | changes only X | `∀ s a, G s a → ∀ part ∉ X, part (state o) = part s` | Frame condition (Dafny `modifies`, JML `assignable`; named from memory) |
| 4 | always Q / never B | `∀ s a, G s a → Q s a o`; *never B* is *always ¬B* | Universality / Absence |
| 5 | if C then Q | `∀ s a, G s a ∧ C s a → Q s a o` | Response, zero delay; EARS event/unwanted |
| 6 | Q only if C | `∀ s a, G s a ∧ Q s a o → C s a` | Precedence (necessary condition); FRET "only" |
| 7 | Q exactly when C | frames 5 and 6 together | — |
| 8 | rejected and unchanged when C | `∀ s a, G s a ∧ C s a → ∃ e, o = rejected e s` | Ours; EARS unwanted behaviour |
| 9 | changes M by exactly f / the result is f | `∀ s a, G s a → M (state o) = f (M s) a` (or `result o = f s a`) | Functional postcondition |
| 10 | M is at most k / at least k | `∀ s a, G s a → M o ≤ k s a` (or `≥`) | Bounded patterns, quantity for time |
| 11 | at most n / at least n / exactly n of XS are P | `count P (XS o) ≤ n`, `≥ n`, `= n`; "once" is `n = 1`; "every" is `n = |XS|`; "no" is `n = 0` | SBVR quantifier keywords; Bounded Existence moved from time to a collection |
| 12 | more A never loses Q (monotone) | `∀ s a a', a ≤ a' ∧ Q (op s a) → Q (op s a')` | — |

Second tier, specified now and built when T4 to T6 need them:

| # | Frame | One-line formal reading |
|---|---|---|
| 13 | agrees with REF | `∀ s a, G s a → op s a = REF s a` |
| 14 | independent of H / reveals nothing about H | `∀ s s' a, s =(all but H) s' → view (op s a) = view (op s' a)` |

Notes on the proposal:

- Frames 4 to 8 are the planned list. Frames 1, 3, 7, 12, 13 and 14 are the additions argued above. Frame 11 replaces "at most, at least, exactly once" as a temporal idea with a counting quantifier, which is what the existing ledger step "exactly 2 transfers are applied" already is.
- "Every", "each", "some" and "no" should be binders with a named domain (frame 11), not free words. This is the answer SBVR and ACE both reached (section 2).
- Two-operation sentences such as "two batches one after the other conserve the total" should be derived from frame 2 by composition, not given a frame.
- That is 12 plus 2. V2's fail line is 20.

## 2. Controlled natural languages for specification

| Language | Scope and ambiguity handling | What users found hard | Typed compositional vocabulary? |
|---|---|---|---|
| **Attempto Controlled English** | One reading per sentence, fixed by interpretation rules. A quantifier "opens its scope that extends to the end of the sentence"; "for every …" at the front scopes over the whole sentence; "and binds stronger than or"; "Prepositional phrases modify the verb not the noun"; braces override. Opened: https://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html | The Zurich course deck concedes the rules "do not always lead to natural interpretation" (search summary). Kuhn's work: CNLs are easier to read than to write, hence predictive editors; a 64-person study found ACE easier to understand than a formal OWL syntax (search summary, arXiv:1211.3643 and the 2010 evaluation-framework chapter) | No. Content words are a lexicon of nouns and verbs mapped to first-order predicates, not typed pieces bound to code |
| **EARS** | Five sentence templates: ubiquitous, state-driven (While), event-driven (When), optional feature (Where), unwanted behaviour (If/Then), plus combinations. Rules: zero or many preconditions, zero or one trigger, one system, one or more responses. Opened: https://alistairmavin.com/ears/ | By design it constrains syntax only; a well-formed EARS sentence can state the wrong behaviour and nothing warns you (search summary of commentary) | No. No semantics at all |
| **FRET / FRETish (NASA)** | Five fields: scope, condition, component, timing, response. Omitted fields take defaults: scope global, condition true, timing *eventually*. Each combination has a fixed formal reading. See below | No quantifiers ("quantifiers in the language would have been incredibly useful"); mode changes awkward; parent-child links unchecked; repeated definitions in large sets. Opened: https://arxiv.org/html/2503.24040v1 | No. The response is a Boolean expression over declared variables. Templates are typed by field, the vocabulary is flat |
| **SBVR Structured English** | Explicit keywords for modality ("It is obligatory that") and quantity ("each", "at least one", "at most one", "exactly one"), each mapped to a logical formulation; scope is by nesting order. Search summary only: https://brcommunity.com/articles.php?id=b286 | Not found | Partly. It has a typed vocabulary of terms and fact types (a business glossary), which is the closest to "domain words signed per project". It has no modifiers-as-functions and no link to code |
| **Grammatical Framework** | An abstract syntax (typed, language-independent) with concrete syntaxes per language; ACE itself has been implemented in GF and ported to five languages. Search summary: https://research.chalmers.se/publication/131247 | "All grammars leak": defining a fragment as a subset of a full language is hard (search summary, https://ar5iv.arxiv.org/html/1406.4057) | Yes in mechanism: GF abstract syntax is exactly a typed grammar of composable meanings. I found no GF grammar that targets statements about program behaviour in a proof assistant. **Not verified** in depth |
| **Amazon Bedrock Automated Reasoning checks** | An LLM-extracted policy of typed variables (bool, int, number, enum) and SMT rules. Several models translate independently; disagreement yields `TRANSLATION_AMBIGUOUS` with `differenceScenarios`, "Scenarios (up to 2) that illustrate how the different interpretations differ in meaning". A fidelity report grounds every rule in numbered source statements. Opened: https://docs.aws.amazon.com/bedrock/latest/userguide/automated-reasoning-checks-concepts.html | The docs warn that a `VALID` result "covers only the parts of the input captured through policy variables"; untranslated content passes silently unless you look | Flat typed variables with prose descriptions. No composition |
| **nl2spec** | LLM translates free English to temporal logic and maps each subformula back to the fragment of English it came from; the user edits fragment-level translations. Opened (abstract): https://arxiv.org/abs/2303.04864 | — | No |

Conclusion on the question asked: **none offers the typed, three-kind vocabulary (domain word, modifier, frame) of `docs/VOCABULARY.md`.** GF supplies the mechanism, SBVR the glossary discipline, FRET the frames. The combination is not something I found.

### FRET in detail: how close, and what to copy

What it does (opened: Conrad, Titolo, Giannakopoulou, Pressburger, Dutle, CPP 2022, https://shemesh.larc.nasa.gov/people/amd/publications/CPP2022-Comp-Framework-FRETish.pdf, pages 1 to 5):

- A requirement is `scope condition component shall timing response`. Scope is one of null, `in`, `notin`, `before`, `after`, `onlyIn`, `onlyBefore`, `onlyAfter`. Timing is one of `immediately`, `next`, `always`, `never`, `eventually`, `within d`, `for d`, `after d`, `until stop`, `before stop`. "When timing is omitted, it is assumed to be eventually."
- For each requirement the tool shows a text explanation in fixed slots, a "semantic diagram", and future-time and past-time temporal-logic formulas. The explanation in the paper's figure reads "ENFORCED: in every interval where flight holds. TRIGGER: first point in the interval if (…) is true and any point in the interval where (…) becomes true (from false). REQUIRES: for every trigger, RES must hold at some point with distance <= 3 from the trigger".
- The "only" scopes mean the requirement must *not* hold outside the scope. That is a separate, explicit word for the converse direction.
- The paper notes the vacuous case explicitly: if the condition never triggers, "the requirement is never triggered and is therefore vacuously true".
- The translation itself is checked twice: by an automated testing framework, and by a PVS proof "of semantic equivalence between FRETish specifications and their temporal logic counterparts". The authors call it "the first formalization of a structured natural language in a theorem prover".
- The probabilistic extension validates its formulas against an oracle on random models and reports that this "caught a real bug" (opened: https://arxiv.org/html/2512.15788v1).

How close: FRET is "frames with echo-back" for temporal requirements. The design decision in `docs/VOCABULARY.md` to have a small set of sentence shapes, each with a signed reading that is printed back, is FRET's design. What differs:

- FRET's atoms are opaque Booleans over signals. There are no domain words bound to code, no modifiers, and no quantifiers, and its users asked for quantifiers.
- FRET's default for a missing timing is the weak one (*eventually*). Ours is the strict one.
- FRET hands formulas to model checkers and runtime monitors (the README says it exports "in various formats, facilitating integration with external formal analysis tools", https://github.com/NASA-SW-VnV/fret). It does not prove anything about source code and has no examples-as-tests.

What to copy from FRET:

1. **Echo-back in fixed slots**, not free prose. For us: *Applies to* (the quantified inputs, including whether rejected calls are covered), *Assuming* (Givens), *Requires* (the Then), *Defaults applied* (every word that was filled in by default).
2. **State defaults in the echo every time.** FRET users were tripped by the silent *eventually*.
3. **A separate word for the converse direction** ("only"), never inferred.
4. **Report vacuity as part of the semantics.** The slice already has a VACUOUS verdict; keep it.
5. **Validate the frame library against an independent second semantics.** FRET did this by testing and then by proof. For us: each frame gets its Lean definition and an independent executable reading, compared on generated inputs. The slice's "second reading in Rust" already does this for phrases; extend it to frames.
6. **A diagram or table per frame** showing a satisfying and a violating case.

## 3. Gherkin `Rule:`

**Reference semantics** (opened: https://cucumber.io/docs/gherkin/reference/):

- "The (optional) `Rule` keyword has been part of Gherkin since v6."
- "The purpose of the `Rule` keyword is to represent one *business rule* that should be implemented."
- "A `Rule` should contain one or more scenarios that illustrate the particular rule."
- `Background` is allowed at Rule level, one per Rule. Free-form description text may sit under `Rule`.
- The reference page says nothing about nesting or about tags on a Rule.

**Grammar** (opened: https://raw.githubusercontent.com/cucumber/gherkin/main/gherkin.berp):

- `Feature! := FeatureHeader Background? ScenarioDefinition* Rule*`
- `Rule! := RuleHeader Background? ScenarioDefinition*`
- `RuleHeader! := Tags? #RuleLine DescriptionHelper`
- `Scenario! := #ScenarioLine DescriptionHelper Step* ExamplesDefinition*`

So: a Rule may contain Scenario Outlines with Examples (an outline is a Scenario with Examples). A Rule may carry tags. Rules do not nest. Once a Feature has a Rule, no top-level scenario may follow it.

**Runner support:**

| Runner | Support | Source |
|---|---|---|
| cucumber-rs 0.23.0 (released 2026-04-23; the version `slice/wallet-bdd/Cargo.toml` pins) | Depends on `gherkin ^0.16`. The book: "No additional work is required on the implementation side to support Rules." `gherkin::Rule` has fields `keyword, name, description, background, scenarios, tags, span, position`. The event enum has `Feature::Rule(Source<Rule>, Rule<World>)`. Known issue in the README: "`Scenario Outline` is treated the same as `Outline` or `Example` in the parser". The book's example shows plain Scenarios under a Rule, not an outline | https://docs.rs/crate/cucumber/latest , https://cucumber-rs.github.io/cucumber/main/writing/rule.html , https://docs.rs/gherkin/latest/gherkin/struct.Rule.html , https://docs.rs/cucumber/latest/cucumber/event/enum.Feature.html , https://github.com/cucumber-rs/cucumber |
| cucumber-jvm | Rule arrived in 6.0.0: "today it comes to Cucumber JVM" | https://github.com/cucumber/cucumber-jvm/blob/main/release-notes/v6.0.0.md |
| cucumber-js | 7.0.0-rc.0 (2020-09-14): "Add support for Gherkin's Rule/Example syntax". 7.1.0 (2021-04-06): "Support tagged rules". Latest release seen: 13.3.0 (2026-10-05) | https://raw.githubusercontent.com/cucumber/cucumber-js/main/CHANGELOG.md |
| behave | Since 1.2.7 a Rule may have a description, an optional Background, and "any number of Scenarios and Scenario Outlines"; tags on Rules are supported. The page is served under 1.4.0.dev0 docs; the 1.2.7 release date was **not verified** | https://behave.readthedocs.io/en/latest/new_and_noteworthy_v1.2.7/ |

Tag inheritance from Rule to its scenarios came with @cucumber/gherkin 18.0.0 (2021-03-24), "[All] Rules can be tagged" (search summary of the changelog; also described in https://cucumber.io/blog/bdd/gherkin-rules/, opened).

Not verified: I did not run a Scenario Outline under a Rule through cucumber-rs. The grammar allows it and the crate's types carry it, but the task forbade running anything. `slice/features/*.feature` contain no `Rule:` line today, so this is untested here. It should be the first check in V2.

**Convention for a universally quantified Rule: none found.** The Cucumber blog treats a Rule as the thing examples illustrate ("Without its examples, a rule may be ambiguous", "Without a rule, an example lacks context") and gives no formal wording convention. A search for Gherkin combined with property-based testing or "for all" found nothing. Consequences:

- Every runner treats the Rule name as a label. Our universal reading is an added convention, and a feature file that fails its proof still passes in a plain cucumber run. The report must be the place where that shows.
- The supported extension points are a tag on the Rule (for example `@proved`) and the description text under it (a place for the echoed reading). Both survive all four runners.
- Avoid Background inside a Rule: behave's notes say a proposal to remove it was pending (dated statement, not re-checked).

## 4. BDD, structured requirements and formal verification

| Work | What it does | Overlap with us | Status of my check |
|---|---|---|---|
| **FRET** with CoCoSim, Kind 2, Copilot | Structured English to temporal logic to model checking or runtime monitors | The meaning link, on models and monitors, not source code | opened (section 2) |
| **Behaviour-driven formal model development**, Snook, Hoang, Dghaym, Butler and others, 2018 on; "Cucumber for Event-B" | Gherkin scenarios executed against Event-B models with ProB; scenarios refined alongside the model | Gherkin against a formal model. Scenarios are run, not generalised and proved; no implementation code | search summary: https://eprints.soton.ac.uk/434774/1/ICECCS2019.pdf |
| Williams, Formal Aspects of Computing 2020 | The same Gherkin-to-Event-B route applied to UK charity regulations | A fixed legal text as source, as in Interpret mode | search summary; Springer page did not open: https://link.springer.com/article/10.1007/s00165-020-00512-5 |
| "Towards Formal Verification of BDD Scenarios Using Timed Automata" (2024) | Scenarios to timed automata, conformance checked | Model checking of scenarios | search summary; page returned 403 |
| **Müller, Liu, Drechsler**, arXiv:2609.15318 (Sep 2026) | "FV Gherkin Scenarios" as a controlled-language spec for hardware; LLM generates RTL and assertions; formal property verification | The nearest "Gherkin to formal properties to proof on the artefact", for hardware. LLM judges, not signed vocabulary | abstract opened: https://arxiv.org/abs/2609.15318v1 ; details not verified |
| Gupte and S., arXiv:2511.11829 (Nov 2025) | An LLM autoformaliser checks LLM-generated Gherkin against natural-language requirements for equivalence and inconsistency; two small experiments | Formalising Gherkin for consistency. No code is proved. A search summary says the target is Lean; the abstract page does not | abstract opened: https://arxiv.org/abs/2511.11829 |
| **Kiro** (AWS) | EARS requirements, from which it "extracts properties", each "a universal statement" of the form "For any …"; a developer reviews them; property-based tests with shrinking. Docs: "It provides evidence of correctness, not a proof" | The closest product to "requirement to universal property with human review and a counterexample on failure". Tested, not proved | opened: https://kiro.dev/docs/specs/correctness/ |
| **Bedrock Automated Reasoning checks** | Section 2 | Echo-back, source grounding and distinguishing scenarios, at SMT level | opened |
| **nl2spec** | Section 2 | Fragment-level confirmation | abstract opened |
| Li, Zetzsche, Somayyajula, arXiv:2501.06283 (Jan 2025) | LLM writes Dafny as a hidden intermediate; user sees only natural language; verified code compiled to the target | Formal layer hidden behind natural language. How the user confirms the spec is not stated in the abstract | abstract opened: https://arxiv.org/abs/2501.06283 |
| Liu, Parthasarathy, Murali, arXiv:2607.13303 (Jul 2026) | "Monty": filters candidate formalisations of natural-language assertions with a conformance score; 541 tasks, precision up to 20 points better than naive prompting | Faithfulness of the meaning link, automated | abstract opened: https://arxiv.org/abs/2607.13303 |
| Hassani, Sabetzadeh, Amyot, arXiv:2508.20744 | LLMs turn food-safety regulations into Gherkin; ten people rated 60 specifications; omissions and hallucinations mean review is still needed | Interpret mode's first half (document to Gherkin), with human ratings | abstract opened: https://arxiv.org/abs/2508.20744 |
| **Ho, Fournet, Protzenko and others**, arXiv:2609.15648 (Sep 2026) | 16.7 KLOC of Rust verified in 237 KLOC of Lean through Aeneas; agents wrote about 5.1k theorems; agents turn standards prose into Lean specs that humans review; "Models still try to 'cheat' with unsound assumptions or weakened goals" | The proof and translation links at scale, and the same audit concern as the slice. Meaning link is expert review of Lean, no controlled language | opened: https://arxiv.org/html/2609.15648v1 |
| **FVS** (Beneficial AI Foundation) | Agent skills for Aeneas Rust in Lean: `/fvs:natural-language`, `/fvs:lean-specify`, an automatic fresh `/fvs:lean-spec-review`, `/fvs:lean-verify`, `/fvs:trust-audit`; "review the statements and decide when proof work begins" | Workflow overlap with the slice is high: explain, specify, independent review, prove, audit. No Gherkin, no vocabulary, no examples-as-tests | README opened: https://github.com/Beneficial-AI-Foundation/formal-verification-skills |
| Klaus, Conejero, Tolmach (Runtime Verification), arXiv:2605.30106 | Rust to Lean through Aeneas or hax, with AI provers; experience report | Proof link; lists extraction limits | opened: https://arxiv.org/html/2605.30106 |
| Beg, O'Donoghue, Monahan, arXiv:2506.11874 | Survey of 35 papers on LLMs formalising software requirements | Background | abstract opened: https://arxiv.org/abs/2506.11874 |

**Who is closest to "Gherkin rule to statement to proof about real code to evidence report"?** Nobody does all four steps. By step:

- Rule to statement, with a published reading: FRET (not Gherkin, not code).
- Statement to proof about real Rust: the Aeneas-at-scale group and FVS (no controlled language; statements written or reviewed as Lean).
- Requirement to universal property with human confirmation, on real code: Kiro (tests, not proofs).
- Gherkin specifically to formal proof on the artefact: Müller et al., for hardware.

A targeted search for a tool that compiles Given/When/Then into Lean, Coq, Isabelle, Dafny, Verus, TLA+ or Kani statements about software found none. That is absence of evidence from a handful of searches, not proof of absence.

**Where we would be duplicating:**

- The pipeline "agent writes the Lean statement, an independent reviewer checks it, then proofs, then a cheat or trust audit" exists in FVS and in the Aeneas report. The slice's audit (exact statement type, axioms check) covers the same risk they name.
- "Find an input on which two readings differ and ask" (V6) exists in Bedrock as `differenceScenarios`, for SMT-level rules.
- "Trace each formal rule to the clause it reads" (Interpret mode) exists in Bedrock's fidelity report.
- "Universal property plus shrinking counterexample from a requirement" exists in Kiro.

## 5. Cedar: is the TDFLite plan's claim right?

The claim in `tdflite-ideas/` (line 301): "This is the approach AWS uses for its Cedar policy language: a Lean model, cross-checked against the production implementation by random testing." **Verified.**

How they do it (opened: "How We Built Cedar: A Verification-Guided Approach", https://arxiv.org/html/2407.01688v1 ; AWS blog of 8 April 2024, https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development/ ; repository, https://github.com/cedar-policy/cedar-spec):

- **Process.** "Verification-guided development": an executable Lean model of each core component, proofs about the model, production code in Rust, and differential random testing (DRT) that the two agree. A release is not shipped unless model, proofs and differential tests are current.
- **Sizes.** Lean model 1,673 lines; Lean proofs 5,714 lines; the Rust it models about 15.7k lines in the paper's table. The validator soundness proof is 4,686 lines and took 18 person-days.
- **Generators.** Type-directed: generate a schema, then a conforming entity store, then policies and requests that fit it. A second generator deliberately produces ill-typed conditions to reach error handling. The generators live in `cedar-policy-generators`, built on the Rust `arbitrary` crate.
- **Harness.** `cargo-fuzz` (libFuzzer, coverage-guided). Targets include authorizer parity, validator parity, parser round-trip, formatter round-trip, parser safety on random bytes, and validation soundness.
- **Scale.** Each target runs daily for 6 hours on 4 vCPUs, "millions of inputs for most targets". Minimised corpus cases are saved and replayed in CI.
- **Speed.** The paper gives median 6 µs for the Lean authorizer against 10 µs for Rust; the blog says 5 and 7. Either way the model is not the bottleneck.
- **Yield.** Proofs found 4 bugs (all in the validator, one a non-termination). DRT and property tests found 21.
- **What it missed.** Generator quality decided coverage: 35.5% of generated conditions were Boolean literals until a better expression generator cut that to 9.7%. Bugs needing unlikely inputs and malformed-syntax parser bugs were missed. The parser is not modelled at all.
- **Design feedback.** DRT exposed a string-size feature whose semantics differed between model and code; the feature was dropped.
- **Their reason for not proving the Rust directly** (at the time): tools such as Aeneas, Kani and Verus were limited in library coverage, supported idioms and scalability.

Not verified: how the compiled Lean model is linked into the Rust fuzz targets. The repository has a `cedar-lean-ffi` directory and the build runs `build_lean_lib.sh` before `cargo build`, which implies linking the Lean library in-process, but the README does not say so. Also not verified in an opened page: that an earlier version of the model was in Dafny (a search summary of a POPL 2024 student poster says so).

For T4, copy: input generators that are aware of the policy structure, with a second generator aimed at error paths; coverage guidance; a saved, minimised corpus replayed in CI; a rule that every disagreement is classified (code defect, model defect, or a ruling); a measured statistic on how trivial the generated inputs are.

## 6. hax's Lean backend versus plain Aeneas, and verified compilation

### What changed

Opened: hax blog index (https://hax.cryspen.com/blog/), the hax 0.4 post of 29 September 2026 (https://hax.cryspen.com/blog/2026/09/29/hax-04-easier-to-install-and-configure-and-a-new-lean-backend/), the core-models post of 3 November 2026 (https://hax.cryspen.com/blog/2026/11/03/core-models-modelling-rust-dependencies-in-rust/), the hax README (https://github.com/cryspen/hax).

- "The new Lean backend does not use the hax engine." Charon produces the intermediate form and "Aeneas translates it into pure functional Lean code". The old backend "remains available as `legacy-lean`".
- What hax adds on top of Aeneas: `hax_lib::requires` and `ensures` become `<fn>.pre` and `<fn>.post`; a generated specification as a Hoare triple over the `RustM` monad (which models panics and overflow); a generated theorem with proof `sorry` in a `Verification` folder that hax does not overwrite; the hax Lean library; a tested, pinned set of Charon, Aeneas, Lean and library versions; a `lake` package.
- The proof library comes from "core-models", Rust models of `core` and `alloc`, covering "35 out of 55 modules of `core`", about 20% of items in those, and 8% of `alloc`. They are validated by property tests against the real library, 100% line coverage, weekly mutation testing, and equivalence tests run in Lean.
- Stated limits: "hax doesn't support all Rust constructs, e.g, `unsafe` code or interior mutability" (https://hax.cryspen.com/manual/lean/quick_start/). Building the extracted code does not prove panic freedom by itself. The README adds that `&mut` in return types or under aliasing is not allowed.
- Roadmap: the next release's goal is robustness. The backend is six weeks old as of this check.

So `tdflite-ideas/` is right that hax's "current Lean backend is built on Aeneas". The practical difference from plain Aeneas is the contract surface and the proof library, not the translation.

### Plain Aeneas today

Opened: Aeneas README (https://github.com/AeneasVerif/aeneas), the September 2026 technical report (https://arxiv.org/html/2609.15648v1), the June 2025 newsletter (https://aeneasverif.github.io/newsletter/2025/06/03/aeneas-newsletter.html), the Runtime Verification report (https://arxiv.org/html/2605.30106).

| Feature | State | Source |
|---|---|---|
| Subset | "Aeneas currently functionalizes a subset of safe Rust" | README |
| Loops | Translated to recursive functions; invariants are written by hand or by an agent. "`return` inside *nested* loops, or `break`/`continue` to *outer* loops are not supported yet" | README; 2609.15648 |
| Iterators | Support for "mutable iterators" and "iterator transformers" was added in the 2026 work | 2609.15648 |
| Closures | Charon translates them "as plain structs with the appropriate Fn{Mut,Once,} impls" (June 2025). Whether Aeneas's Lean output handles them in general: **not verified** | newsletter |
| Traits | "translated to structures"; trait-parameterised hash code was verified. The Runtime Verification team still had to write a monomorphic model for some trait-bounded functions | 2609.15648; 2605.30106 |
| `dyn`, strings | Not mentioned in any opened official page. A downstream issue cites them as unsupported (search summary, dated). Treat as unsupported | **not verified** |
| Arrays, slices | Covered by the reasoning libraries | 2609.15648 |
| Unsafe, raw pointers, interior mutability, concurrency | Not supported; such functions "must be modelled by hand" | 2609.15648 |
| Automation | `step`, `step*`, `scalar_tac`, `grind`, `bv_tac` | 2609.15648 |
| Scale shown | 16.7 KLOC Rust, 237 KLOC Lean; "about a week for an agent and a few days of human review" per additional algorithm; "a few dollars per line of Rust" | 2609.15648 |
| Stability | Nightly binaries; pins one Rust nightly and one Lean version. The slice already records this (`slice/TOOLCHAIN.md`: Aeneas nightly-2026.11.09, Lean 4.35.0). Toolchain drift between hax and Aeneas work was a named obstacle for the Runtime Verification team | 2605.30106 |

### Recommendation for T6 (a small pure decision function over integers and sorted sets)

**Use plain Aeneas now. Keep hax as an option, not the default.** Reasons:

1. The translation is the same tool either way.
2. In this project the contract already has a home: the Gherkin rule and the Lean statement generated from it. hax's attributes would be a second specification surface to keep in step with the first. The TDFLite plan's argument for hax, that contracts sit beside the code where Rust reviewers see them, is real but is the job the Rule line and the report are meant to do.
3. The slice's proofs and audit code are written against Aeneas's own Lean library and monad. hax's backend targets its own library and `RustM`. Proofs are not portable between them without rework. (Inferred from the two descriptions; I did not compare generated output.)
4. Maturity: plain Aeneas has a published 16.7 KLOC verification; the hax-on-Aeneas backend was released six weeks ago and names robustness as its next goal.
5. A function over integers and sorted slices sits inside what Aeneas is shown to handle. Keep it free of strings, `dyn`, closures passed as values, and early exits from nested loops.

Reconsider hax when one of these holds: the core needs library calls that Aeneas's own models lack and core-models covers; Rust reviewers without Lean must sign contracts in the source; or hax's pinned-toolchain manifest becomes the easier way to stay reproducible.

### How far is the compilation link from being more than an assumption?

- **RustCompCert** (Wu, Wang, Yu, Meng; arXiv:2602.07455, February 2026): a CompCert-based compiler for "a sequential subset of Rust" claiming semantics preservation from Rust to assembly plus memory safety from a verified borrow-checking pass. The abstract calls it "ongoing work". Abstract opened: https://arxiv.org/abs/2602.07455. Using it would mean compiling the core with a different compiler from the one that ships.
- **rustc itself**: I found no verified or translation-validated pipeline. A bug study attributes 15.28% of studied rustc bug causes to MIR optimisation errors (search summary, https://arxiv.org/pdf/2503.23985). A 2023 PLDI student poster hand-proved one MIR optimisation as "a first step" (search summary). A 2026 study of soundness bugs in rustc's type checker exists (search result only, https://arxiv.org/pdf/2608.28713).
- Alive2-style validation of the LLVM stage applied to rustc output, and Ferrocene's qualification status: searched, nothing found. **Not verified** either way.

Conclusion: for production rustc the link stays an assumption, bounded only by running the examples and counterexamples on the compiled binary, which the slice does. The plan's "not yet" stands. One cheap improvement is already noted in `slice/FINDINGS.md`: proofs see a nightly's view while tests run on stable; running the example rows on both would narrow that.

## What to copy

1. **FRET's echo format**: fixed slots, defaults listed, a separate word for the converse ("only"), vacuity reported. Section 2.
2. **FRET's double semantics**: every frame gets an independent executable reading, compared with the Lean definition on generated inputs, before it is signed.
3. **Bedrock's `differenceScenarios`** as the shape of V6's question: two candidate readings, one concrete input, the two answers side by side. Also its rule that untranslated text is listed, never dropped.
4. **Bedrock's fidelity report** for Interpret mode: numbered atomic statements from the source, each formal sentence grounded in specific ones, and a coverage figure.
5. **ACE's scope discipline**: quantifier scope fixed by a stated rule, a front position ("for every …") for wide scope, and an explicit override. Do not guess.
6. **SBVR's quantifier keywords** as the whole surface for counting: each, at least n, at most n, exactly n.
7. **Kiro's link from each property back to the requirement and task**, shown on hover; in our case from each report row to the Rule line and vocabulary pieces.
8. **Cedar's DRT recipe** for T4. Section 5.
9. **The Aeneas report's rule** that agents may not edit specifications or axioms without human approval, and its statement-review step. The slice's exact-statement audit is the mechanical half of this.
10. **Gherkin's own extension points**: a tag on the Rule and the description text under it. Nothing else.

## What to avoid

1. **Weak defaults.** FRET's silent *eventually* is the cautionary case. Fail-closed is the right call; print the default anyway.
2. **Syntax without semantics.** EARS shows that templates alone do not stop a wrong requirement.
3. **Natural-looking sentences with unnatural fixed readings.** ACE's own teaching material concedes this. Where the fixed reading may surprise, ask.
4. **Shipping without quantifiers.** FRET's users named this as the gap. Frame 11 and explicit binders should be in the first library.
5. **Template explosion.** FRET went from 112 to 160 to 560 template keys. Keep frames few and get variety from modifiers and composition.
6. **Treating "at most once" and "exactly once" as temporal** before there are traces. Define them as counts over a named collection or leave them out.
7. **Assuming authors can write the controlled language because they can read it.** Kuhn's work says reading is easy and writing is not. Suggest mode is the mitigation; budget for it.
8. **Trusting an LLM-written or LLM-reviewed statement.** The Aeneas report records models weakening goals. Bedrock uses agreement between several models only as a confidence signal.
9. **Letting a `VALID`-style verdict cover only what was translated.** Any clause or word with no reading must appear in the report.
10. **Relying on runners to understand the Rule line.** They do not. Avoid Background inside a Rule.
11. **A second specification surface** (hax attributes beside Gherkin rules) unless there is a reader who needs it.
12. **Naive random inputs in T4.** Cedar's first generator produced mostly trivial conditions.

## What appears to be genuinely open

1. **A typed, signed, reusable vocabulary of domain words, modifiers and frames that compiles to statements about real code.** FRET has frames, SBVR has glossaries, GF has the typing mechanism. I found no system combining them, and none with sign-off that is voided when a definition changes.
2. **Frames for pre/post claims about code, as a catalogue.** The published catalogues are all temporal. The list in section 1 (frame condition, monotone, refinement, independence, counting) has no equivalent that I found presented as a pattern system with structured English.
3. **A Gherkin Rule read as a universally quantified claim, proved, with its Examples as tested instances and one report covering both.** No convention and no tool found for software. The hardware work of Müller et al. is the nearest.
4. **An evidence report that names every link and its kind of evidence** (human-asserted, kernel-checked, tool-trusted, tested). The Aeneas report and FVS discuss trust; I found no generated per-claim report of this kind.
5. **Measured echo-back.** I found no study of whether readers catch a subtly wrong formal reading from a paraphrase. V5 would be new data. I did not search this exhaustively.
6. **Distinguishing inputs at code level.** Bedrock produces distinguishing scenarios over flat SMT variables. Doing it for two Lean readings of a rule about a real operation, with the input then run on the compiled code, was not found.
7. **The compilation link for production rustc.** Open in the field, not only here.

Less open than the plan assumes: the agent-proves-and-audits loop (FVS, the Aeneas report), requirement-to-universal-property with human review (Kiro), source grounding and ambiguity scenarios (Bedrock), and the frame-with-echo idea itself (FRET).

## Could not open or confirm

- Giannakopoulou, Pressburger, Mavridou, Schumann, "Automated formalization of structured natural language requirements", Information and Software Technology 2021: bibliographic record only.
- Dwyer et al. ICSE 1999 pattern frequency table; Konrad and Cheng 2005 pattern names; Grunske 2008 pattern names; Autili et al. 2015 full text.
- Williams 2020 (Springer redirect to login); the timed-automata BDD paper (403).
- SBVR specification text; GF-based specification languages beyond search summaries; ACE's paraphrase facility; Kuhn's studies beyond search summaries.
- Scenario Outline under a Rule executed in cucumber-rs 0.23 (not run, by instruction).
- Mechanism linking Cedar's Lean model into the Rust fuzz targets; the Dafny predecessor.
- Aeneas support for closures as values, `dyn` and strings as of November 2026; hax Lean backend's feature matrix (none is published on the pages opened).
- Alive2 applied to rustc; Ferrocene.
