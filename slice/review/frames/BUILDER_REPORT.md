# Builder's report for the frame library (V2/V3), as returned on 2026-11-10

## summary
V2 and V3 are built in `slice/` and the final `./run.sh` from scratch exits 0 with every scenario verdict unchanged. The catch: the glossary grew (44 entries became 87), the Rust side is still one step per old whole phrase, and no one has read the echoes.

**Key numbers**

| | |
|---|---|
| Frames | 23 Lean definitions covering all 14 catalogue frames; 19 reachable from a sentence. Not yet reachable: counting with a number, monotone, agrees with a reference, independent of (two runs) |
| Pieces by kind | 31 domain words (8 operations), 27 modifiers, 19 frames = 77, plus 10 idioms |
| Old 44 whole-phrase entries | now read with 73 entries (31 domain, 21 modifiers, 11 frames, 10 idioms). 26 of the 36 old Given/Then phrases compose from regular forms; 10 needed an idiom |
| NEW ↔ OLD | 34 of 34 readings proved equivalent to the old statement by the kernel, standard axioms only; 33 non-vacuity theorems |
| Strengthened by the defaults | 0 scenario statements (the old ones were already fail-closed), so there is no "new implies old" list |
| Scenario verdicts | all 35 as before: 24 PROVED-FOR-ALL, 6 PROVED-INSTANCE, 3 REFUTED, 1 UNBOUND, 1 VACUOUS |
| Rule lines | 13 of 14 compile (the 14th is the deliberately unbound one). 10 PROVED-FOR-ALL (8 by generated glue, 2 by hand-written proof), 3 REFUTED in the kernel, 1 UNBOUND |
| Definition vs executable reading | agree on 23,700 of 23,700 evaluations (fixtures), 2,801 of 2,801 (held-out sentences), and on all 10 hand-written instances for the four frames with no surface |
| Five new ledger rules | 5 of 5 compile with no vocabulary change; 4 have no counterexample on the grid, 1 (meant false) has one; none is proved |
| Mutation harness | all 45 mutants identical to the previous run in every recorded field except shifted line numbers; 27 of 27 controls as expected |
| cucumber-rs | unchanged: 14 rules, 81 scenarios, 365 steps |
| TDFLite coverage | 83 of 85 readings expressible with the built frames and no one-off frame |

**How it is put together**

- **Frame library** (`slice/lean/Frames/`, core Lean only, so it can be lifted out): an abstract operation, typed holes, and the fail-closed defaults written in one place. No frame takes an arbitrary before/after relation.
- **Each frame** has a Lean definition, a slot-structured English template and a Bool checker; the definition and the checker are compared on generated inputs every run.
- **Refusals**: a sentence that does not compose gets UNBOUND, ILL-TYPED (naming the two types) or AMBIGUOUS, with file:line.
- **Rule ↔ scenarios**: the outline scenarios beneath a rule are its parts. A generated kernel-checked theorem derives the rule statement from them by cases on their Givens; a hand-written proof may stand in where that script fails. Only this direction is claimed.
- **Old proofs carry over**: each proved scenario is one theorem whose type is the compiled reading, obtained through the equivalence. A reading without its equivalence gets the verdict UNLINKED.
- **Echo**: every rule and scenario prints its slot-structured reading first, with every default applied; the Lean is folded underneath in `out/report.md`.

**Three before/after examples**

1. *"Given Alice has a balance of ‹a› / And ‹amount› is not more than Alice's balance / When Alice withdraws ‹amount› / Then the operation succeeds / And Alice's balance is decreased by ‹amount›"*
   - Old: `∀ a amount alice, Vocab.hasBalance alice a → Vocab.covers alice amount → ∃ outcome alice', wallet.Wallet.withdraw alice amount = ok (outcome, alice') ∧ Vocab.succeeds outcome ∧ Vocab.decreasedBy alice alice' amount`
   - New: `∀ a, Frames.Always (W.withdraw.given (fun st inp => W.balance st = a.val ∧ inp.val ≤ W.balance st)) (fun ans => W.accepted ans) ∧ Frames.DecreasesBy (…same operation…) (fun st inp => W.balance st) (fun st inp => inp.val)`
   - Echo: applies to a withdrawal of ‹amount› from Alice, every call accepted or rejected [default D2]; assuming the balance of Alice is ‹a›, ‹amount› is at most the balance of Alice; then the call gives an answer [default D1], the answer is Ok, the balance of Alice after the call plus ‹amount› equals the balance before it, exactly.

2. *"When the batch ‹batch› is applied to ledger Main as a whole / Then if it is rejected, ledger Main is unchanged"*
   - Old: `∀ balances batch main, LVocab.holds main balances → ∃ outcome main', ledger.Ledger.apply_all main batch = ok (outcome, main') ∧ LVocab.unchangedIfRejected outcome main main'`
   - New: `∀ balances, Frames.AlwaysAnswers (L.applyAll.given …) ∧ Frames.NeverChanges ((L.applyAll.given …).rejected) (fun st inp => L.balances st)`
   - Echo: then the call gives an answer [default D1]; if the call is rejected, the balances of ledger Main after the call equal the balances before it; not default: only rejected calls are covered by that line.

3. *"Then it is accepted / And the amount of ‹t› has moved between its accounts in ledger Main and no other balance changed / And the total of ledger Main's balances is unchanged"*
   - Old: `… LVocab.accepted outcome ∧ LVocab.moved main main' t ∧ LVocab.totalUnchanged main main'`
   - New: five frames on `L.apply.given (… ∧ L.valid st inp)`: `Always`, `DecreasesBy` (the sender's balance), `IncreasesBy` (the receiver's), `ChangesOnly` (the accounts, except sender and receiver), `NeverChanges` (the aggregate).
   - Echo: one line per frame, e.g. "the accounts of ledger Main are the same accounts after the call, and every one of them other than the sending account and the receiving account has the balance it had before".

**What a new sentence needs**

- Nothing, to get a statement, an echo and a search, if it can be said with existing forms.
- A proof, to get a verdict (free only when it follows from scenario theorems by cases).
- A Rust step, to run under cucumber.

The five rules, all of which compiled on the first attempt:
1. "An internal transfer never changes the total of all balances of the ledger"
2. "A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger"
3. "For a lookup for which the account is not an account of the ledger, there is no result"
4. "A batch never leaves the total of all balances of the ledger above the maximum" (meant false; counterexample: ledger [2^64−1, 1], empty batch)
5. "For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards"

**TDFLite coverage (counts and generic frame names only)**

| Frame | Readings |
|---|---|
| agrees with a reference | 28 |
| monotone | 15 |
| only if | 11 |
| counting over a named collection (every / no) | 11 |
| always / never under a condition | 9 |
| independent of / invariant under a change of input (two runs) | 7 |
| the result is | 1 |
| always answers | 1 |

- 50 of the 83 need monotone, agrees-with or independent-of, which here are definitions with tests and no sentence form.
- Missing frames (2 readings): containment between a collection of the input and a collection of the answer; two-run independence conditioned on the first run's answer.
- Also missing, but a modifier, not a frame: "some X of XS" as a condition.
## files
- /Users/will/dev/lean-rosette/slice/out/report.md
- /Users/will/dev/lean-rosette/slice/vocabulary.yaml
- /Users/will/dev/lean-rosette/slice/lean/Frames/Core.lean
- /Users/will/dev/lean-rosette/slice/lean/Frames/Frames.lean
- /Users/will/dev/lean-rosette/slice/lean/Frames/Check.lean
- /Users/will/dev/lean-rosette/slice/lean/Frames/Lemmas.lean
- /Users/will/dev/lean-rosette/slice/lean/Wallet/Pieces.lean
- /Users/will/dev/lean-rosette/slice/lean/Ledger/Pieces.lean
- /Users/will/dev/lean-rosette/slice/lean/Wallet/Readings.lean
- /Users/will/dev/lean-rosette/slice/lean/Run/Links.lean
- /Users/will/dev/lean-rosette/slice/lean/Run/ReadingSearch.lean
- /Users/will/dev/lean-rosette/slice/lean/Run/FrameTests.lean
- /Users/will/dev/lean-rosette/slice/lean/Wallet/RuleProofs/ledger/total_fits.lean
- /Users/will/dev/lean-rosette/slice/lean/Wallet/RuleProofs/ledger/batch_then_total.lean
- /Users/will/dev/lean-rosette/slice/lean/Bdd/Ops.lean
- /Users/will/dev/lean-rosette/slice/lean/Bdd/AuditLinks.lean
- /Users/will/dev/lean-rosette/slice/slicegen/vocab.py
- /Users/will/dev/lean-rosette/slice/slicegen/links.py
- /Users/will/dev/lean-rosette/slice/slicegen/rsearch.py
- /Users/will/dev/lean-rosette/slice/slicegen/vreport.py
- /Users/will/dev/lean-rosette/slice/slicegen/newrules.py
- /Users/will/dev/lean-rosette/slice/features/wallet.feature
- /Users/will/dev/lean-rosette/slice/features/ledger.feature
- /Users/will/dev/lean-rosette/slice/heldout/new_rules.feature
- /Users/will/dev/lean-rosette/slice/heldout/frames.feature
- /Users/will/dev/lean-rosette/slice/mutation/run_mutants.py
- /Users/will/dev/lean-rosette/slice/mutation/results.md
- /Users/will/dev/lean-rosette/slice/run.sh
- /Users/will/dev/lean-rosette/slice/DESIGN.md
- /Users/will/dev/lean-rosette/slice/FINDINGS.md
- /Users/will/dev/lean-rosette/slice/README.md
- /Users/will/dev/lean-rosette/DECISIONS.md
## howToRun
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
cd /Users/will/dev/lean-rosette/slice

./run.sh                      # everything; report in out/report.md. Exit 0 iff every scenario AND every rule statement got its expected verdict
./run.sh --no-heldout         # the same without the new sentences of heldout/ (informational)
python3 -m slicegen compile heldout/new_rules.feature    # compile new sentences from the vocabulary alone; run.sh also runs lean/Run/NewReadings.lean and collects the results
python3 -m slicegen review <piece-id|all> --reviewer NAME   # sign off a vocabulary piece (void when its entry or Lean text changes)
python3 mutation/run_mutants.py --jobs 12                # 45 Rust mutants + 27 controls; writes mutation/results.{json,md}
python3 -m slicegen.selftest                             # parser and bookkeeping checks, no Lean

Where to look: out/report.md (per-Rule blocks with the echo first, then the frame library, vocabulary, regression and new-sentences sections); DESIGN.md section 14; the last addendum of FINDINGS.md.
## verified
Run in this session:
- Final `./run.sh` from scratch: exit 0 in 1 min 51 s warm, at load average 58 to 120 from other agents. Output: 35 scenarios (24 PROVED-FOR-ALL, 6 PROVED-INSTANCE, 3 REFUTED, 1 UNBOUND, 1 VACUOUS); 14 rule statements (10 PROVED-FOR-ALL, 3 REFUTED, 1 UNBOUND); 34 of 34 readings equivalent to their flat statement; frames agree on 23,700 of 23,700 evaluations; 12 of 12 held-out sentences compiled.
- The link audit checks that each generated theorem has exactly the expected type and uses only propext, Classical.choice and Quot.sound.
- Full mutation run (73 minutes, 12 jobs, load 80 to 180): compared field by field with the previous `results.json` from git. All 45 mutants are identical except the changed example rows now sit at shifted line numbers (same rows, same counts). A scenario is shown false of 17 of 18 wallet and 26 of 27 ledger mutants; `d6` and `la6` still fail only through a lost proof.
- Controls: 27 of 27 as expected in the full run. c10, c11 and c21 failed in a first partial run (a piece id clashing with the `all` keyword of the review command; a wrong expectation of mine) and c22 timed out; all four were fixed and re-run before the full run.
- cucumber-rs: 14 rules, 81 scenarios (79 passed, 1 skipped, 1 failed, as before), 365 steps; step regexes identical to the glossary for 44 of 44.
- `python3 -m slicegen.selftest` and `python3 schema/selftest.py` pass; the graph validates against the schema.
- Frame tests for the four frames with no surface: 10 instances, definition and checker agree on every evaluation, with both true and false claims among them.

Not verified:
- No person or proxy reader has looked at an echo.
- Nothing is signed (0 of 87 entries).
- No run on an idle machine.
- The TDFLite classification is my reading of the pilot's descriptions; none of those readings was compiled.
- The new rules are searched on a small grid only and are not proved.
- Rule falsity under mutants was confirmed in the kernel for only 2 of the 30 mutants where a rule statement was newly found false.
## judgementCalls
- Kept the old whole-phrase glossary as an intermediate instead of replacing it: every scenario has the compiled reading (shown and judged) and the old flat statement (what the proofs, search and Rust steps are about), tied by a kernel-checked equivalence. This is what let the old proofs carry over untouched; the cost is two vocabularies in the tree.
- Reworded 13 of the 14 Rule lines so they compose from pieces (only 'A transfer never changes the total of all balances' stood as written) and gave each Rule an @id tag. No scenario text changed. The compound rules became long.
- Rule-to-scenario relation is one direction only: the outline scenarios entail the rule. The converse is not claimed, because a rule says less than its suite.
- run.sh now also fails when a rule statement misses its expected verdict. As a deliberate consequence, controls c8 and c17 changed their expected exit status from 0 to 1: removing a progress scenario now costs the rule its proof.
- Two rule statements (total_fits, batch_then_total) are proved by hand from the loop lemmas, because the glue script cannot produce the u64 that their scenarios name as a sum. They therefore rest on the unsigned lemma library.
- A scenario always includes 'the call gives an answer'; a Rule clause whose subject is 'a successful ...' or 'a rejected ...' does not, and the echo prints that as a removed default.
- Measures may depend on the input (so 'the sender's account balance' can be stated in a rule), a departure from the catalogue's state-only measure.
- Which answers count as accepted is fixed per operation in the domain files: apply_batch never rejects; a lookup is accepted when it returns a value. This differs from the adequacy note's own list.
- Introduced idioms as a fourth sort of entry (10): a surface form plus the composition it means. Needed because scenario texts had to stay as they were for cucumber; every fixture scenario uses at least one.
- Added a bystander modifier so the old 'deposit does not touch a bystander' control still compiles.
- Built monotone, agrees-with, independent-of and counting-with-a-number as Lean definitions with checkers and hand-written tests, but with no sentence form: no fixture needs them and their hole types have no domain word here.
- Put the five new rules in heldout/ as an informational step, not in features/, because without a Rust step and a proof they would fail the regression run by construction. I wrote them myself in one pass without running the compiler on drafts.
- Added heldout/frames.feature (seven sentences) only to exercise frames no fixture reaches; it is not counted among the five.
- Mutation harness: seven new controls (c21 to c27), per-run timeout raised from 900 s to 3600 s, mutant runs skip the held-out step, and each mutant also records which rule statements were found false, beside the unchanged scenario columns.
- Two small edits to legacy files: three DecidableEq derivations moved from Wallet/Vocab.lean to a shared Wallet/Instances.lean, and a 'mention' pattern added to the ledger actor in glossary.yaml.
- TDFLite: reported counts and generic frame names only; the per-reading table was not written to disk and nothing from the private files was copied.
- Stopped my first full mutation run after 12 minutes (before its baseline finished) to add the one-theorem-per-reading step, then restarted. It was stopped through its task handle and I checked no process was left under slice/build/mutation.
- Nothing was committed; no install, pin edit or lake update. All judgement calls are in DECISIONS.md under '## V2/V3 frame library' and '(continued)'.
## caveats
- The glossary grew: 44 entries became 87 (77 pieces and 10 idioms). The gain is that 46 of the 77 are shared and new sentences stop adding entries; here that rests on five builder-written sentences on two toy crates, not on a measurement.
- The Rust side is not compositional. Cucumber steps and the Rust second readings are still one per old whole phrase, so a new sentence gets a statement, an echo and a model search but no run on compiled Rust. This is the largest gap to the README target.
- The five new rules were written by the builder, who knows the forms; rule 2 shows the stiffness ('the balance of account the sender of the transfer of the ledger'). This is not the V4 test with authors who do not know the vocabulary.
- The rule statements add no detection: across 45 mutants a rule was never found false where no scenario was, and for 13 mutants a scenario was shown false and no rule was.
- Kernel refutation of a rule exists only for a clause about every call of a single operation.
- Agreement between a frame's definition and its checker is a test on generated inputs, not a proof. The four frames with no surface are tested on 10 hand-written instances only.
- The glue script handles suites that split by cases on Givens. It cannot instantiate a parameter that names a computed number; where it fails the rule needs a hand proof or stays NOT-PROVED.
- The equivalence removes the generator and the old glossary from what a verdict rests on; it adds no evidence about the Rust. Reading and flat statement share the Aeneas model and the search grid.
- TDFLite: 83 of 85 is frame-level expressibility judged by reading, with no TDFLite domain words built. 50 of the 83 need frames that have no sentence form yet. The two guarantees the pilot says its model cannot state are outside the 85 and outside single-call frames.
- Root-level docs (README.md, docs/VOCABULARY.md, docs/PLAN.md) still say the vocabulary is not implemented; they are outside slice/ and were not edited.
- Timings were taken on a machine loaded by other agents and say little about an idle one.
## nextSteps
- Give the Rust side a compositional reading: one Rust predicate per piece and a generic cucumber step that evaluates a composition tree, so a new sentence runs on compiled Rust and the idioms that exist only to keep old step texts can go.
- Run K1/V5 on the generated echoes (proxy readers now, people later). Seeds already exist as controls: c21 (frame weakened), c22 (domain word changed), c25 (rule says more than its scenarios).
- Run V4 properly: 40 rules by authors who do not know the vocabulary, with intent recorded first. `python3 -m slicegen compile` already reports compiled / UNBOUND / ILL-TYPED / AMBIGUOUS per sentence with the nearest forms.
- Give monotone, agrees-with and independent-of a surface: domain words for 'a relation between two inputs' and 'a reference function', plus rule forms. Add the two frames the TDFLite readings lacked (containment between an input collection and an answer collection; two-run independence conditioned on the first answer) and the 'some X of XS' condition.
- Let a new sentence reach a verdict without the old glossary: generate its flat proof obligation from the pieces, so heldout/ rules can move into features/ with a proof stub.
- Have someone sign the 87 entries (`python3 -m slicegen review`), starting with the 46 shared ones, then make --strict the default.
- Extend kernel refutation of rules to clauses about successful or rejected calls and to sequences, and find out why it failed for 28 of the 30 mutants where a rule was found false.
- Lift lean/Frames into its own Lake package and run the V9 drill (change a frame with and without changing its meaning; the per-piece digest and the equivalence theorems are the hooks).
- Update the root README, docs/VOCABULARY.md and docs/PLAN.md status lines, which still say nothing is implemented.
