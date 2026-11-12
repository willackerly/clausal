# Applying this work to TDFLite

Architectural notes on how the tooling here could serve the plan in `tdflite-ideas/TDFLite policy core formal verification plans.md`. This is a first pass, written from that document alone: the TDFLite repository has not been read, and nothing here has been built.

## Short version

The slice is close to what TDFLite's plan needs, and the plan's stage 1 can be piloted with it without touching production code. The maths-side scoring work does not transfer. The most useful things to carry over are the audit checks the slice's review forced, because each one corresponds to a way a "proved" claim about the policy core could be hollow.

## How the two line up

| TDFLite plan | What exists here | Fit |
|---|---|---|
| Eight guarantees, each in plain language and as a formal statement | Scenarios bound through a glossary to generated Lean statements | Direct. The plan's two columns are the two ends of a glossary binding |
| D1–D6 scenario tables (policy, resource, subject, result today) | Given / When / Then with example rows and expected verdicts | Direct. Each table is already a scenario |
| Rulings as named parameters; "Lean reports which theorems it affects" | Staleness computed from content digests in the graph | Direct, and gives a report rather than a build failure |
| "What stays assumed" table | Evidence kinds on edges: kernel-checked, tested, tool-trusted, human-asserted | Direct. Each assumption becomes a visible node, not a paragraph |
| Lean model as differential oracle against Go (step 3) | `tested` evidence on an `equivalent` edge; cucumber replay of counterexamples on compiled code | Same idea; the slice does it against Rust, not Go |
| Rust core via hax, refinement proof (steps 4–6) | Rust via plain Aeneas, proofs about generated code | Partial. hax's Lean backend sits on Aeneas, so toolchain lessons carry; contracts-as-attributes are untested here |
| EAL7-style evidence mapping | The graph, filtered by evidence kind | A view over the same data |
| Bundle verification, anti-rollback (step 8) | Nothing | Not covered |

## What the slice's review implies for the TDFLite plan

Each of these was a real failure found here. The plan's gates do not currently rule them out.

1. **Check that each proof proves the stated statement.** The slice accepted `theorem … : True` as a proof of a scenario. The plan's gate (no `sorry`, standard axioms only) would pass that too. Add: the theorem's type must be exactly the generated statement.
2. **Check that the guarantees are not vacuous.** "Permit implies X" holds trivially if nothing ever permits. Every guarantee conditional on Permit needs a checked witness that Permit is reachable, and each Given a witness that it can be satisfied.
3. **Measure what the guarantees leave unconstrained.** Three real bugs survived every proof in the slice because the scenarios said nothing about the success paths. Guarantees 1–7 are properties, not a full specification. Guarantee 8 (compiled engine equals reference) is the one that pins behaviour completely, and it is listed as not holding today (D5). Mutation-test the model and the core against the guarantee set and report what survives.
4. **Give every English phrase two independent readings.** A weakened definition of a glossary term passed silently until each phrase had a second reading compared on a grid. For TDFLite the terms are few and sharp (dominates, subset, non-empty intersection, resolves in the snapshot), which makes this cheap.
5. **Replay counterexamples on the real implementation.** A refutation in the model is only interesting if the Go engines agree. D1–D6 were run on both engines by hand; make that automatic.
6. **A failed proof means "not shown", not "false".** Under one injected bug a still-true scenario lost its proof. Report the two cases differently.

## Things TDFLite has that make this easier than the slice

- **One call, one decision.** The slice's one-When-per-scenario limit is no limit here: `decide` is a single pure function.
- **Stage 1 needs no Rust.** Scenarios can bind to a hand-written Lean model. The generator currently targets Aeneas output only, so it needs a "model target" mode; this is a small change.
- **Integers and sorted sets.** The compiled snapshot works over interned IDs, which is the easy case for Aeneas's arithmetic automation.
- **A ready counterexample.** Guarantee 4 (more entitlements never remove access) is false today because of D4. A pilot should find `[TOP_SECRET, UNCLASSIFIED]` versus `[UNCLASSIFIED, TOP_SECRET]` on its own; if it does not, the search is too weak.

## Things to expect trouble with

- **Loops.** The decision iterates over attributes and values. Everything encouraging in the slice was on straight-line code; the ledger experiment (`docs/EXPERIMENTS.md`, 12) is measuring the cost of loop invariants now and should be read before estimating stage 2.
- **Rust subset.** With the pinned Aeneas, `for` over ranges, iterator adaptors and closures did not translate. The plan already excludes `unsafe`, async and hash-map iteration; add these.
- **Strings.** Intake (D1, D2, D3, D5 live there) is string parsing and case folding. The plan already flags hax's string support; the slice has no evidence either way.
- **Toolchain pins.** Charon needs one exact Rust nightly and Aeneas one exact Lean version, different from other projects on the same machine. Budget a separate Lake project and about 12 GB.
- **Go is outside the proof.** Nothing here reasons about Go. Until stage 2, the link from model to production is `tested` only, and the graph should say so on every guarantee.
- **Non-interference (guarantee 6).** "Deny reveals nothing about the key" is a two-run property. The scenario form here states one run; this needs a different statement shape.

## Suggested pilot (stage 1, no production code)

1. Write the Lean model of the decision **as it behaves today**, from the plan's description and the D1–D6 tables.
2. Write guarantees 1–5 and D1–D6 as a feature file with a glossary of about a dozen terms.
3. Run it. Expected: D1–D6 reproduce today's results as instance verdicts; guarantee 4 is refuted with a D4-style counterexample; guarantee 2 is refuted by D1 or D3.
4. Add the six rulings as parameters. Flip each and record which verdicts change. That table is the decision aid the plan asks for.
5. Apply the audit checks above, plus a mutation run on the model.
6. Only then wire the differential oracle against the Go engines, which needs the TDFLite repository.

Steps 1–5 need no access to TDFLite's code and would show whether the scenario layer earns its place before any Rust is written.

## Open questions

- Is Gherkin the right surface for security guarantees, or do the plan's own tables read better? The binding mechanism does not depend on the syntax.
- hax contracts or plain Aeneas with specifications in Lean? The plan prefers hax; only Aeneas has been exercised here.
- Should the six rulings be scenario tags, model parameters, or both?
- Where does the graph live: in TDFLite's repository as an evidence artefact, or produced on demand?
- Who signs the glossary? For a certification story this is the human-asserted link an evaluator will look at first.
