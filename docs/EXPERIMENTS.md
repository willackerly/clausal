# Experiment inventory

Everything tried so far, in order. One entry per experiment: the claim, how it was tested, the result, and where the evidence is. Update an entry when its status changes; add new ones at the end.

Status values: **final** (reviewed and rerun), **preliminary** (results exist, review pending), **running**, **not started**.

## Summary

| # | Experiment | Result | Status |
|---|---|---|---|
| 0 | Original scaffold ("Lean-Ghidra") | Discarded: never ran against Lean | final |
| 1 | H1: hiding ratio finds human lemma boundaries | Negative | final |
| 2 | "Small goal state" baseline | Negative, worse than random | final |
| 3 | H2: statements recur across Mathlib proofs | Negative | final |
| 4 | Kernel-checked lifting | Works | final |
| 5 | Readability of lifted statements | Mixed | final (thin evidence) |
| 6 | Prior-art check | Idea partly published | final |
| 7 | Vertical slice: wallet | Works after review fixes | final |
| 8 | Refinement-graph schema v2 | Fits both sides on small examples | final (thin on maths side) |
| 9 | H3: dominators predict blueprint nodes | Negative | final |
| 10 | Dominator outline of Navier–Stokes | Correct bottleneck map, mostly unreadable | final (one reader) |
| 11 | Reuse in the machine corpus | Negative; dead code is the larger finding | final |
| 12 | Slice with loops (ledger) | Works, but proofs cost about 4x more and loops are under-specified | final (two loops) |
| 13 | Friction census and "packets" | Constants yes, casts no, packets marginal as ported | final |
| 14 | Dead code in the machine corpus | A quarter of the corpus deleted; headline theorems still check | final |
| 15 | Ground truth from the papers | 117 items mapped to Lean; scorer built | final (model-built) |
| 16 | Definition-centred outline | More followable, no more milestones, readers split | final (proxy readers) |
| 17 | Constant threading via big-O | Fits; proofs −2% to −4%; library costs more than it saves | final (one family) |
| 18 | TDFLite pilot (plan T0, T1a, T1b) | Model matches the Go on 400k cases; all six known edge cases surfaced (guided); 15 further behaviours reproduced | final; details private |
| 19 | Trade map: rows, property tests, Kani, proofs (K2) | Sampling and bounded checking catch nearly everything on the fixtures; proofs add the unbounded result | final, reviewed; two toy crates |
| 20 | Rust translation census (K3) | 1% as shipped, 34% with crate-level aborts worked around; three small tool defects dominate | final |
| 21 | `Rule:` support and suite adequacy note (F1) | Works; 7 of 8 operations' suites rule out every trivial implementation | final |
| 22 | Meaning trial on proxy readers (K1) | 93% of wrong readings caught, 0.3% false alarms; harness ready for people | proxy only |
| 24 | Frame library and composable vocabulary (V2, V3) | Built; every old statement proved equivalent; rule lines compile | review in progress |
| 25 | Agent-written loop proofs, two models (P2) | Both proved 7 of 7 loop functions in under 15 minutes; about 6 Lean lines per Rust line | final, independently scored; textbook loops |
| 26 | Aeneas fork spike (A1) | Four small patches: 1% to 35% of census functions translate (nine crates: 3% to 82%) | final; Cedar partly unmeasured |
| 27 | Dead-code tool on three Lean projects (M8) | Works; safest class never wrong; shares depend on the choice of roots | final, reviewed |
| 28 | Detector for re-invented library notions (M7) | Finds the known case unaided; recall unknown; most matches are trivial | exploratory |
| 23 | TDFLite ruled specification (T2, T3r, T4) | Rulings fixed; guarantees 1–5 proved, 8 proved given named facts; 75 test vectors; one-command check | final, reviewed; details private |

## 0. Original scaffold

- **What:** Python profiler scoring tactic states by "working-memory load" `W`, a slicer using `extract_goal`, a linter, a 2x2 agent arena.
- **Why discarded:** the example theorem was `sorry`, the trace was hand-written, analysis used regex, nothing had run in Lean.
- **Where:** deleted on 2026-11-10; described in `DECISIONS.md`.

## 1. H1: hiding ratio

- **Claim:** among all proof-valued pieces of a proof term, the piece a human factored out ranks high by proof size ÷ statement size.
- **Method:** 323 Mathlib theorem/helper pairs (helper private or `aux`-named, used at most twice). Paste the helper's proof back into the theorem, enumerate candidates, rank.
- **Result:** first pick 7.7%, top-5 47.1%, against 5.9% / 40.9% for proof size alone and 1.9% / 9.0% for random. At chance when the helper is under half its theorem's size. On the "where to stop" task it picks the human cut 4.6% of the time against 22.7% for random.
- **Why it fails:** most of the apparent signal is tree position; the ratio prefers the deepest large piece, humans cut higher.
- **Caveats:** test set favours large marked helpers; a good-but-different lemma counts as a miss.
- **Where:** `Rosette/Bench.lean`, `bench/score.py`, `out/bench/RESULTS.md`, `out/review_benchmark-validity/`.

## 2. "Small goal state" baseline

- **Claim (from the original brainstorm):** good boundaries are where few hypotheses are in play.
- **Result:** fewest-dependencies ranking gets first pick 0.0%, top-5 3.1%. Worse than random.
- **Where:** same files as 1.

## 3. H2: reuse in Mathlib

- **Claim:** closed statements recur across different proofs often enough to factor.
- **Method:** 600 theorems in three areas, 156,984 candidates, hashed up to bound-variable names; two generalisation levels; filters for automation output and library lemmas.
- **Result:** 4,122 statements recur; 98.6% trivial. 18 survive with any saving, 0.2% of proof size, none clearly worth naming.
- **Caveats:** filters are heuristics; no lemma was actually factored; humans had already done the factoring.
- **Where:** `Rosette/Reuse.lean`, `bench/reuse.py`, `out/reuse/REUSE.md`.

## 4. Kernel-checked lifting

- **What:** `#rosette_lift` turns chosen sub-proofs into real auxiliary theorems and rebuilds the original on top; the kernel checks both; results may not use new axioms.
- **Result:** no failures in a 1,274-theorem sweep. Two measurement bugs found in review and fixed (duplicated binders, tree-walk double counting).
- **Where:** `Rosette/Candidates.lean`, `Rosette/Lift.lean`, `Rosette/Tests.lean`, `bench/sweep.lean`.

## 5. Readability demo

- **Method:** lift lemmas from three hand-picked long proofs; one reader rates each statement.
- **Result:** Pell and Erdős–Ginzburg–Ziv give fair outlines. Sobolev gives only exponent arithmetic; its real steps have ~900-node statements. Unfiltered, 25 of 45 statements are junk; filters cut that to 6.
- **Lesson:** analysis proofs need statements shown relative to their surrounding context.
- **Where:** `Rosette/Demo.lean`, `out/demo/`.

## 6. Prior art

- **Result:** the five papers cited in the brainstorm exist (one misdescribed). Closest work, missing from it: Proof-Refactor (arXiv:2606.03743). The ratio appears in Aksenov et al. (arXiv:2603.20396). OpenAI's Navier–Stokes repository is ~38,500 short theorems in flat directories.
- **Gaps that looked open:** repository-scale restructuring, deterministic scoring, selecting what a human must read.
- **Where:** `out/prior_art.md`.

## 7. Vertical slice: wallet

- **Claim:** a Gherkin scenario can get a machine-checked verdict about real Rust.
- **Method:** Rust → Charon/Aeneas → Lean model; `.feature` + `glossary.yaml` → generated Lean statements; hand-written proofs; audit; the same feature file run by cucumber-rs.
- **Result:** 7 scenarios proved for all inputs, 1 proved for an instance, 1 false claim refuted with a counterexample confirmed on compiled Rust, plus unbound and vacuous controls.
- **Review found:** a proof of `True` counted as a proof (fixed); three real bugs survived because scenarios were incomplete (fixed with more scenarios and coverage theorems); a misleading glossary entry passed (partly fixed with a second reading in Rust).
- **Mutation test:** 18 of 18 injected bugs noticed after fixes (11 before). Example rows alone catch 17.
- **Open:** glossary unsigned; straight-line code only.
- **Where:** `slice/FINDINGS.md`, `slice/DESIGN.md`, `slice/mutation/`.

## 8. Schema v2

- **What:** nodes with an interface and implementations; edges with evidence (kernel-checked, tested, tool-trusted, human-asserted); staleness computed from digests.
- **Result:** validates the slice's graph (109 nodes, 275 edges) and an 11-node maths example assembled by script.
- **Open:** the maths tooling does not emit it; nine open questions listed in the doc.
- **Where:** `docs/SCHEMA.md`, `slice/schema/`.

## 9. H3: dominators predict blueprint nodes

- **Claim:** statements that large regions of a proof can only be reached through are the ones humans put in a blueprint.
- **Method:** PFR (1,118 declarations, 219 blueprint nodes) and Carleson (3,199, 180). Score every theorem by graph features; compare with blueprint membership.
- **Result so far:** graph-only model AUC 0.85 / 0.87, but dominator features add +0.001. The signal is proof size. Blueprint theorems have larger statements than average, so dividing by statement size hurts. "Has a docstring" does as well as the best graph score. Lean reachability recovers 87–94% of the human `\uses` edges.
- **Where:** `bench/validate_outline.py`, `out/corpus/validation/VALIDATION.md`.

## 10. Dominator outline of Navier–Stokes

- **Method:** dominator tree of the 52,505-declaration graph from each headline theorem.
- **Result so far:** one very wide hub. 13 statements cover 54% of the Navier–Stokes proof mass, 19 cover 33% of Euler. Of the 15 heaviest chapter statements, one reader rated 2 milestones, 9 technical, 4 unreadable. Chapter boundaries are mostly chosen objects whose content is in a structure defined elsewhere.
- **Lesson:** definitions, not lemmas, are the interface a reader cannot skip.
- **Where:** `bench/outline.py`, `out/corpus/outline/`.

## 11. Reuse in the machine corpus

- **Claim:** a generator that never names a fact repeats substantive sub-proofs, so machine proofs hold more reuse than Mathlib.
- **Result:** not supported. Non-trivial repeated statements are 0.15% and 0.03% of proof size in two samples (Mathlib 0.20%). Identical theorem statements 0.9%. A deduplication or generalisation pass could remove at most 3.7% of theorems, realistically half that. 468 theorems were re-derived from general statements through the kernel.
- **What is specific to the machine corpus:** copy-and-modify (13 cloned files; parallel estimates for different parameter ranges), and dead code: 32.4% of theorems are used by no headline theorem.
- **Final numbers for 9 and 10** are in `out/corpus/FINDINGS.md`; the review reproduced them and removed two overstated side claims.
- **Where:** `bench/corpus_reuse.py`, `corpora/ns_reuse/`, `out/corpus/reuse/REUSE.md`, `out/corpus/FINDINGS.md`.

## 12. Slice with loops (ledger)

- **Claim:** the slice still works when the Rust has loops and a collection.
- **Method:** an 85-line ledger over `Vec<u64>` with two `while` loops and a batch of transfers; 23 scenarios; multi-step scenarios; 27 ledger mutants including 5 written by the reviewer.
- **Result:** 16 scenarios proved for all inputs (including "any batch conserves the total" and "a rejected whole batch leaves the ledger unchanged"), 5 proved for literal values, 2 false claims refuted with counterexamples confirmed on compiled Rust. Scenarios with two operations in sequence work.
- **Cost:** 389 lines of hand-written Lean for 65 code lines of Rust (6.0 per line; wallet 1.6). Each loop needed an invariant, a second pure version of the computation and a proof linking them: a reviewer estimated 50–90 lines and about an agent-hour per loop. Once that lemma exists, further properties are cheap.
- **Review found:** atomicity was unspecified, so a version with no rollback could be re-proved to a green run (fixed with new scenarios); four of five reviewer mutants were noticed only because a proof stopped compiling, which is now reported separately and not counted as detection; non-vacuity witnesses were degenerate (empty ledger); cost figures were understated (corrected).
- **Lessons:** (1) an agent writing proofs will prove around a bug unless a scenario forbids it; (2) scenarios do not yet determine what a loop computes, and the exact behaviour is proved only in unsigned helper lemmas; (3) iterator chains and closures do not translate. (Range loops do; see experiment 20.)
- **Caveats:** two loops, one flat collection, no nesting, traits or generics; scenarios, proofs and most mutants written by the same agent.
- **Where:** `slice/ledger/`, `slice/DESIGN.md` section 12, `slice/mutation/results.md`, `slice/review/loops/`, `slice/review/loops-fix/`.

## 13. Friction census and packets

- **Claims (from an earlier chat, unmeasured):** analysis proofs bloat from constant tracking (A), real/extended-real casts (B), domain surgery (C) and measurability side-conditions (D); machine proofs unfold abstractions humans keep; bundling side-conditions into structures would help.
- **Method:** hypothesis-level export of 42,254 theorems across the machine corpus, Carleson and PFR; shares of hypotheses and proof mass per family; bundle mining; one structure defined and nine real theorems restated against it, kernel-checked.
- **Result:** A supported (about 9% of machine proof mass, constants re-exported through chains up to 13 lemmas deep). B not supported for the machine corpus (0.07%); it describes Carleson. C not supported. D partly, 6–15% depending on the rule. Unfolding: cannot tell from proof terms. Packets: statements shrink 6–10% net and hypotheses by a third, but ported proofs grow 7.6%.
- **Unpredicted:** 54% of proof mass is proving equations; type-class instance arguments are 27% of machine proof nodes against 17% in Carleson, unexplained.
- **Review changed:** several verdicts were softened (D's size, unfolding moved to "cannot tell", claims about packets being rare withdrawn after the machine corpus's own predicates were opened).
- **Caveats:** one machine and one comparable human project; nothing is attributable to machine authorship; the packet test was a mechanical port.
- **Where:** `corpora/friction/`, `bench/friction_*.py`, `out/corpus/friction/`, `out/corpus/FINDINGS.md`.

## 14. Dead code in the machine corpus

- **Claim:** a large part of the machine corpus is not needed for its headline theorems and can be removed safely.
- **Method:** reachability from the four headline theorems; deletion in a copy; rebuild; negative control; seeded sample for hidden dependencies.
- **Result:** 233 files, 24.7% of source lines and 30.2% of theorems deleted; headline theorems compile with the same axioms. 2.7% of sampled "unreachable" theorems were in fact needed by `simp` at elaboration time; 1,810 declarations held back.
- **Where:** `bench/deadcode.py`, `out/corpus/deadcode/`.

## 15. Ground truth from the papers

- **What:** the numbered results of the Navier–Stokes and Euler papers mapped to Lean declarations with evidence and confidence, plus a scorer for any outline or ranking.
- **Result:** 117 items, 333 mappings. Sampled accuracy: no wrong mapping among 10 at certain/probable in the reviewer's sample; "guess" unreliable. Built and checked by models only.
- **Where:** `out/corpus/papers/`, `bench/paper_truth.py`.

## 16. Definition-centred outline

- **Claim (plan node M2):** an outline built around definitions is readable where a lemma-based one was not.
- **Result:** for Navier–Stokes, 28% of the proof sits beneath statements whose definitions are all printed (0% before); Euler stays unreadable. Six proxy readers rated no more milestones (6.7% against 8.3%); "opaque" fell from 83% to 17% but "unreadable" rose from 1% to 48%. Reader agreement dropped sharply and results flip by model.
- **Caveats:** readers are models; formats differ in length and content, so the arm cannot isolate the effect of showing definitions.
- **Where:** `bench/outline2.py`, `out/corpus/outline2/`.

## 17. Constant threading via big-O

- **Claim:** stating hand-threaded constants through one relation compresses the proofs.
- **Result:** Mathlib's big-O over a set fits; 11 of 13 conclusions restated with nothing weakened; proofs shrink 2.4–4.2%; the supporting library costs about eight times the saving; no measured saving outside the family. The corpus had re-invented the relation at least three times.
- **Where:** `corpora/lesssim/`, `out/corpus/lesssim/LESSSIM.md`.

## 18. TDFLite pilot (plan nodes T0, T1a, T1b)

Details are private (`private/tdflite-pilot/`, git-ignored); only counts appear here.

- **Method:** an agent barred from the owner's plan wrote a Lean model of both decision engines, string intake and the key-release wrapper from the Go source (about 1,750 lines of core Lean), and checked it against the real Go by differential testing. A second agent wrote down every reasonable formal reading of the eight plain-English guarantees and searched for counterexamples, replaying each on the real Go. A third, on a different model and with access to the plan, scored the result.
- **Result:** model and Go agree on 271,355 generated cases, and on 134,000 fresh cases in the independent check; 24 of 24 deliberate model mutants were detected. 85 readings were written; 20 are proved on the model, 28 unrefuted, the rest have counterexamples, all confirmed on Go. All six edge cases known from an earlier manual review surfaced, each also as an ambiguity question. 15 further behaviours were found and all reproduce on the real Go.
- **Honest limit on "blind":** the agents never opened the plan, but the task text listed the kinds of awkward input to generate, and that list points at all six known cases. This measures guided discovery. A hint-free generator written afterwards by the scorer reached all six within about 12,000 inputs.
- **Layer census:** five of the six known cases are in string intake, none solely in the integer core that a first proof stage would cover.
- **Lesson for the method:** writing down all readings of an English guarantee and separating them with concrete inputs produced 22 ambiguity questions for the owner. That is the "surface ambiguity, do not resolve it silently" rule working on a real target.

## 19. Trade map (plan node K2)

- **Question:** what does each kind of evidence catch, and at what cost? Not whether proof is worth it.
- **Method:** the 23 universal rules of the fixtures discharged four ways (example rows, property-based tests, bounded model checking with Kani, Lean proofs) against 52 tool-generated mutants and, separately, the 45 hand-written ones.
- **Result (tool-generated set, mutants caught):** example rows 50 of 52; property tests 45 with plain generators and 50 with edge-weighted ones; Kani 50; Lean 47 by its own search (49 when inputs found elsewhere are replayed). By rule and mutant pair, edge-weighted property tests found all 212 falsified pairs, Kani 209, Lean's own search 188, example rows 144.
- **What proofs add here:** the unbounded guarantee on the unmutated code. No mutant was caught by proof alone. Kani was the sole finder of the two single-magic-value bugs. Kani shows a ledger rule holds only up to small sizes (3 accounts by 3 transfers gave no answer in 10 minutes).
- **Lost proofs:** of 295 proofs lost on the tool set, 203 are of rules that really are false and 92 of rules nothing shows false.
- **Unconstrained behaviour:** 4 mutants are caught by nothing, because no universal rule says a whole batch is ever accepted or fixes the count. Two candidate rules are proposed.
- **Cost per rule:** a property test 9–27 lines, a Kani harness 10–23, Lean proof text 3–10 lines resting on up to 187 lemma lines for the ledger.
- **Where:** `slice/compare/TRADES.md`, `PREREG.md`, raw results and rerun script alongside.

## 20. Rust translation census (plan node K3)

- **Method:** ten pinned crates (five business-logic, five sampled from popular pure-logic crates), 4,385 non-test functions, each run through Charon, Aeneas and a Lean build.
- **Result:** as shipped, 64 functions (1%) end as Lean that compiles; six of ten crates produce no Lean at all because one error aborts the crate. With crate-level aborts worked around, 1,469 functions (34%). Excluding Cedar, 76%; Cedar alone 1%.
- **Cause:** tool robustness more than Rust idiom. One missing recursive call in Aeneas accounts for 2,214 of 2,916 failing functions; an unguarded method-signature translation aborts whole crates; exceptions in late passes are not caught per function.
- **Deliverables:** `census/PROFILE.md` (16 rules for writing translatable Rust, each with evidence and a before/after), `census/IMPROVEMENTS.md` (18 tool improvements ranked by functions unlocked, with file and line), `census/CENSUS.md`.
- **Correction to experiment 12:** `for i in 0..n` does translate; it was recorded as failing only because the slice passes a warnings-as-errors flag.
- **Caveats:** "compiles" is not "usable": 1,087 of the 1,469 depend on a failed callee or an unmodelled library item. Ten crates, Cedar 57% of the functions.

## 21. `Rule:` support and suite adequacy note (plan node F1)

- **Result:** the pinned cucumber-rs runs Scenario Outlines under `Rule:`. The 33 fixture scenarios are regrouped under 14 Rules with every verdict unchanged. For each operation the proved rules are checked as a suite against 53 trivial implementations (reject everything, do nothing, identity, constant): 7 of 8 operations' suites rule out all of them; the whole-batch operation's suite still allows "always rejects", matching a gap found earlier by hand. The report now has one block per Rule with verdict, examples, suite line and a "rests on" block generated from the graph.
- **Not yet:** the rule line itself is not compiled; that needs the frame library.
- **Where:** `slice/`, `slice/out/report.md`.

## 22. Meaning trial on proxy readers (plan node K1)

- **Method:** 30 rule-and-echo items and 24 glossary items written by one model, 18 of them deliberately unfaithful; eight naive model readers saw only the rule, the echo and a short brief.
- **Result:** 134 of 144 unfaithful readings caught (93.1%, interval reaching below 90%); 1 false alarm in 288. All ten misses are on four single-piece items (a wrong quantity, a dropped condition). Composition errors were all caught, but the five items were visible as wording differences.
- **Caveats:** readers are models of the same family as the author; eight runs behave like about four readers; two answer-key entries are debatable. Not evidence about people.
- **Infrastructure:** a terminal runner, a single-file browser version and a scorer that keep the answer key away from readers, so people can take the identical trial.
- **Where:** `trials/meaning/`.

## 23. TDFLite ruled specification (plan nodes T2, T3r, T4)

Details are private (`private/tdflite-pilot/t2/`, `t3r/`); counts only here. Nothing in the TDFLite repository was changed.

- **Rulings (T2):** the open edge cases became parameters of the model, with a decision table showing what each option does to the guarantees and to existing behaviour. The owner ruled on all of them (ten rulings: six from the owner's plan, four new).
- **Specification:** the ruled decision is also written as a 216-line plain specification, proved equal to the engine-shaped model for every input.
- **Guarantees:** 162 kernel-checked theorems, standard axioms only. Guarantees 1–4 are proved (3 as an exact equivalence), 5 as the decision can check it, 8 given eight named facts about the snapshot compiler and case folding that were tested on tens of thousands of compiled policies but not proved in general. Guarantees 6 and 7 cannot be stated without modelling more of the system. All four trivial decision functions are excluded by a proved guarantee.
- **Test vectors:** 75, most in the owner's conformance-corpus format. On the real Go today, 35 already give the ruled verdict and 40 do not; those 40 are exactly the ones built to differ.
- **Proposed changes:** ten diffs, one per ruling, tried only in scratch copies. With all applied, 75 of 75 vectors and 17,612 generated cases match the ruled model; one existing test breaks, by design.
- **Repeatable check (T4):** one command compares the model of today with the Go at any checkout in under 20 seconds warm; it reports no disagreement at the pilot commit or at the owner's current checkout, and fails on a negative control.
- **Review:** an independent reviewer found 12 corrections, one of them a real defect in a proposed change (it turned a Deny into a Permit on a path outside the model); all applied and a guard vector added.
- **Lesson:** the review caught the one place where the work stepped outside what the model covers. Changes to code the model does not describe need their own evidence.

## 24. Frame library and composable vocabulary (plan nodes V2, V3)

Status: built; the independent review and fixes are in progress, so numbers may move.

- **What:** a project-independent Lean library of 23 frame definitions covering the 14 catalogue frames, each with a Lean definition, a slot-structured English template and an executable checker compared with the definition on generated inputs every run. Vocabulary in three kinds: 31 domain words, 27 modifiers, 19 frames reachable from a sentence, plus 10 idioms.
- **Regression:** all 34 recompiled readings are proved equivalent to the old statements by the kernel; none needed strengthening; all 35 scenario verdicts, the mutation results and the controls are unchanged.
- **Rule lines compile:** 13 of 14 (the last is the deliberately unbound one); 10 proved, 3 refuted in the kernel. Each rule and scenario prints its reading in plain English with every default applied.
- **New sentences:** five new ledger rules compiled first time with no vocabulary change (written by the builder, who knows the forms).
- **Costs and gaps, as the builder reports them:** the glossary grew from 44 entries to 87; the Rust side is still one step per old phrase, so a new sentence cannot yet run on compiled Rust; monotone, agrees-with and independent-of have definitions but no sentence form; nobody has read the echoes.
- **Coverage check on a second domain:** 83 of 85 formal readings of the TDFLite guarantees are expressible with the built frames (judged by reading; counts only, details private).
- **Where:** `slice/lean/Frames/`, `slice/vocabulary.yaml`, `slice/out/report.md`, `slice/review/frames/BUILDER_REPORT.md`.

## 25. Agent-written loop proofs on two models (plan node P2)

- **Method:** a separate author (Opus 5.5) wrote a new 161-line inventory crate with 7 loop functions (accumulation, early-exit search, in-place update, a loop calling loops, a nested loop, a majority-vote loop), 16 universally quantified scenarios and the vocabulary, then froze them by hash. Two arms (Fable, Opus 5.5) each had to find the invariants and helper lemmas alone, without the ledger's proofs. A third agent re-derived every number in cold copies.
- **Result:** both arms proved all 16 scenarios, so 7 of 7 functions each; frozen files unchanged; standard axioms only; every module replayed through the kernel.

| | Fable | Opus 5.5 |
|---|---|---|
| Hand-written Lean lines | 783 | 766 |
| Lean lines per Rust code line | 6.1 | 6.0 |
| Failed builds / attempts | 14 / 27 | 8 / 16 |
| First to last proof build | 14.1 min | 10.3 min |

- **Cost did not fall:** about 6 Lean lines per Rust line, the same as the ledger. In-place updates were the most expensive kind (7.5–9), read-only loops the cheapest (3.4–6.5). Loop lemmas are over half of all hand-written Lean.
- **Mutants:** of 107 tool-generated mutants, 92 are shown false by a scenario; 10 stop the pipeline (9 make a loop never end); 3 are equivalent; 2 real bugs in the majority-vote function are caught by nothing but a lost proof.
- **Caveats:** one run per arm on textbook loops; both recognised the majority-vote algorithm. This shows the time budget did not bind, not that unfamiliar invariants are easy. Model comparison is descriptive.
- **Where:** `p2/RESULTS.md`, `p2/base/`, `p2/arm-fable/`, `p2/arm-opus/`, `p2/score/`.

## 26. Aeneas fork spike (plan node A1)

- **Method:** Aeneas built from source; the three defects found by the census patched one commit each, plus a name-capture fix and a formatter fix found on the way; the ten-crate census rerun as shipped after each patch; Aeneas's own tests run before and after.
- **Result (functions ending as Lean that compiles, as shipped):**

| | Counted | Unpatched | All patches |
|---|---|---|---|
| All ten crates | 4,385 | 64 (1%) | 1,549 (35%) |
| Nine without Cedar | 1,882 | 64 (3%) | 1,549 (82%) |

- **Where the gain comes from:** guarding one trait-method signature translation gives +1,368 functions; the name-capture fix +117. The other patches matter for Cedar and for making failures per-function.
- **Checks:** 122 extraction tests, no regression. A soundness sample of 25 functions on 895 inputs showed no mismatch between Rust and the generated Lean; it is a thin check of small functions.
- **Cedar:** still 0 as shipped, because Charon fails first. With Charon-side workarounds and four patches, 996 of 2,503 functions (40%); the run with all five patches was interrupted and is unmeasured.
- **Prepared, not sent:** five upstream issue texts with reproductions and patches, in `census/fork/upstream/`.
- **Trade:** carrying the fork buys about 1,485 functions now at the cost of a source build per machine and rebasing five small patches; upstream-only costs nothing to carry but arrives on someone else's schedule.
- **Where:** `census/fork/FORK.md`, `patches/`, `repro/`, `upstream/`.

## 27. Dead-code tool on three Lean projects (plan node M8)

- **What:** `tools/deadcode/` takes a built Lean project and a list of root theorems, finds what the roots do not need, sorts it by how safe it is to delete, deletes it in a copy, rebuilds, puts back what the build needs, and checks the roots rest on the same axioms. Runs on Lean 4.34 and 4.36.

| | Navier–Stokes (machine) | PFR (human) | Carleson (human) |
|---|---|---|---|
| Roots | 4 headline theorems | 247 blueprint-tagged | 236 blueprint-tagged |
| Not needed by the roots | 29.4% of declarations | 24.2% | 17.7% |
| Deleted, everything still builds, same axioms | 15,144 declarations, −26.2% of lines | 179, −6.8% | 540, −8.9% |
| Needed although the dependency graph missed them | 0.15% | 4.6% | 2.9% |
| Negative control (deleting something used breaks the build) | 19 of 20 | 20 of 20 | 20 of 20 |

- **The safest class was never wrong about the roots:** 0 of 14,583 deletions had to be put back for a root.
- **Hidden dependencies are real and findable:** `simp` lemmas, coercion instances, names used in `variable` and `open` commands, tactic code. Lean's own reference index and traces locate most of them.
- **Not a machine-versus-human measure.** The roots decide the result. With a handful of headline roots, both human projects also come out at 26.8% unneeded, against 29.4% for the machine corpus. In the human projects about four fifths of what the blueprint does not need is staging material for Mathlib.
- **Build time barely moves:** 1–6% saved for 7–20% of lines deleted.
- **Review found and fixed:** trimming broke the human projects' comparator files (the tool now builds other targets too and restores what they need); on Lean 4.36 two files declaring the same name silently lose one (now reported and protected).
- **Where:** `tools/deadcode/`, `out/deadcode/M8.md`, `COMPARE.md`, per-project `REPORT.md`.

## 28. Detector for re-invented library notions (plan node M7)

Exploratory: the rules changed after the first run and again after review.

- **What:** `tools/reinvent/` proposes project definitions that match a Mathlib notion by shape, asks Lean to prove each pair equal, then counts project theorems that restate a library theorem.
- **Result:** in the machine corpus, 12,891 definitions examined, 290 candidate pairs, 90 proved equal to a library term; in Carleson 12 of 451; in PFR none. The known case (a home-made big-O) is found without being told its name and is the only one of the 90 needing a real argument; 92 of 103 proofs close by `rfl`. Fifteen machine-corpus theorems are shown to be copies of a library theorem.
- **Reading the 90 (a model's reading, not evidence):** 16 rebuild a library notion, 40 are a specific object built with a general library operation, 30 are coincidences of small formulas, 4 are plain use of the library.
- **A large miss:** the reviewer found a project definition equal to a Mathlib one and used by 798 theorems, more than any confirmed case. The tool misses it because the library writes that definition without its last argument. Recall is therefore unknown.
- **Controls:** planted positives 3 of 3 (builder's) and 3 of 5 (reviewer's); planted negatives 0 of 3 confirmed; two deliberate coincidences are confirmed, showing that a proved equality does not imply shared meaning.
- **Where:** `tools/reinvent/`, `out/reinvent/REPORT.md` and per-project reports.

## Ideas ruled out or parked

| Idea | Why |
|---|---|
| Tune the hiding ratio further on Mathlib | Fails on controls, not just on headline numbers |
| Tactic-text slicing with `extract_goal` | Its own docs say the output may not type-check; term-level lifting is sound |
| Library-layer removal, module graphs, clustering as outline methods | Tried in experiment 10; none gives a narrow interface |
| LLM-judged readability as the main metric | Published already; kept as a possible comparison, not the core |
| Model readers as a stand-in for mathematicians on outline quality | Experiment 16: agreement 0.36 on the new outline and the verdict flips by model. Usable for checking truncation and undefined names, not for judging milestones |
