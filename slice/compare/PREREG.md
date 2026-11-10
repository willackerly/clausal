# K2 trade map: what was fixed before the measured run

Written 2026-11-10, before `harness/run.py` was run on any mutant. `harness/freeze.py` records the
digests of everything named here in `results/frozen.json`; `harness/analyse.py` refuses to report a
run as "as registered" if a digest differs. No git commit was made (several agents share the working
tree and the owner asked for no commits); the digests stand in for the commit that
`docs/PLAN.md` rule 1 asks for.

This is a trade map, not a test with a pass mark. Nothing below is a threshold.

## What is compared

**The code and the rules: `slice/` as committed at `SLICE_COMMIT`** (not the working tree, which another
agent was restructuring while this ran). The rules are the 23 Scenario Outlines of
`features/wallet.feature` (7) and `features/ledger.feature` (16) that are expected to be proved for all
inputs. `rules.json` lists them with the KIND assigned to each from its English, before any result:

| Kind | Meaning | Rules |
|---|---|---|
| safety / never-changes | something is the same before and after, whatever the input | 6 |
| exact-result | under the Givens the operation succeeds and the result or new state is fully determined | 6 |
| rejection-and-unchanged | under the Givens the operation is refused and the state is as it was | 9 |
| progress | the operation does not stop short of what it can do | 1 |
| bound | a returned number stays within a limit | 1 |

Progress and bound have one rule each. Nothing can be said about a kind from one rule; they are
reported and labelled as single cases.

Kind is a property of the whole rule. `transfer_conserves` and `transfer_valid_moves` are filed under
exact-result although one of their Thens is a conserved total; `two_batches_conserve` is filed under
safety although one of its Thens is a bound; the two rules about a pure query that returns nothing
(`total_overflow`, `balance_no_account`) are filed under rejection although "unchanged" is true by typing.

## The four arms

| Arm | What runs | What "the rule is discharged" means on the unmutated code |
|---|---|---|
| a. example rows | cucumber-rs (`wallet-bdd/tests/bdd.rs`), the rule's own Examples rows on the compiled Rust | every row passes |
| b. property-based tests | `arms/proptests`: one proptest property per rule, 10,000 generated cases, shrinking, seed 20261110, debug build (overflow and index checks on) | no failing case |
| c. bounded model checking | `arms/kani`: one Kani 0.68.0 harness per rule, CaDiCaL, 180 s per harness | VERIFICATION SUCCESSFUL |
| d. Lean proof | the existing pipeline, `./run.sh --no-unit`, unchanged | verdict PROVED-FOR-ALL |

**Arm b has two generator profiles and both are always reported.** The properties are identical; only
the distribution of integers differs. `plain`: uniform over the range the Givens allow. `edge`: the
same ranges, with half of the draws within 3 of an end of the range. `plain` is the registered primary
reading of "written directly from the English rule"; `edge` is what a tester adds after one more
thought, and costs 6 lines. Collections have 0 to 6 elements in both.

**Arm c is bounded in collection size only; every integer is fully symbolic.** The bounds were chosen
by one rule, on the unmutated code, before any mutant was run: the largest sizes at which the harness
verifies within about a minute on this machine.

| Harnesses | Accounts at most | Transfers per batch at most |
|---|---|---|
| wallet (7) | no collection: unbounded | - |
| ledger rules that do not assert a total (10) | 4 | 3 |
| `batch_conserves`, `whole_conserves`, `batch_then_total`, `batch_then_total_overflow` | 2 | 2 |
| `two_batches_conserve` | 2 | 1 per batch |
| `transfer_valid_moves` (one transfer; asserts the total) | 3 | - |

The smaller bounds are a measured limit, not a choice of convenience: with 3 accounts and 2 transfers
`batch_conserves` did not finish in 240 s (CaDiCaL, Kissat and MiniSat tried; CBMC's SMT back end
crashed with Z3). This is itself a result and is reported in TRADES.md.

## Mutants

1. **Tool set: every mutant `cargo mutants --list` (v27.1.0) generates for `wallet/` and `ledger/`**:
   52 (13 + 39), in `mutants/cargo-mutants.json` with the diff cargo-mutants prints. None is dropped.
   A mutant that does not compile is reported as unviable. A mutant on which no arm reports anything is
   run through a differential oracle (`arms/diff`: original against mutant on about 2.4 million inputs)
   and then read: it is reported either as equivalent (with the argument) or as behaviour no rule
   constrains.
2. **Hand-written set, labelled separately: the 45 mutants of `slice/mutation/run_mutants.py`**
   (18 wallet and 22 ledger by the builder of the rules, 5 ledger by the reviewer), in
   `mutants/hand-written.json`. The rules, example rows and search grid were revised knowing these
   mutants, so results on this set are a regression check, not a detection rate.

Not done: bugs transplanted from real fix commits (`docs/PLAN.md` K2 mentions them; this task did not
ask for them and the two crates have no history of fixes).

## What counts as detection

For each mutant, arm and rule, the raw outcome is recorded; "detected by rule R" then means:

| Arm | Detected | Recorded but NOT detection |
|---|---|---|
| a | an Examples row of R that passes on the unmutated code fails, or does not finish | failing literal-value scenarios (they are not universal rules; listed in their own column) |
| b | R's property has a failing case within 10,000 (the shrunk input is kept), or does not finish in 120 s | - |
| c | R's harness reports a failed check (an assertion of the rule, a panic, an overflow, an index out of range, or an unwinding assertion) | timeout: no answer either way |
| d | **shown false**: the pipeline's own search finds an input on which R's statement is false on the Lean model (verdict REFUTED when the kernel confirms it, COUNTEREXAMPLE otherwise); or **proof lost and confirmed false**: R's proof no longer checks, R's statement is unchanged, and a concrete input found by another arm is confirmed to falsify R (replayed as an extra Examples row on the Lean model and on the compiled Rust) | **proof lost, not shown false**: the proof no longer checks and no falsifying input is known |

For arm d the sub-case is always given, because they are different evidence: a counterexample found by
the pipeline's grid is testing on the model; a lost proof with a confirmed counterexample is what the
proof itself contributes. A proof that still checks on the mutant is recorded as "still proved": then R
is true of the mutant and no arm can rightly detect the mutant through R. Any arm that reports a
detection through a rule that is still proved is listed as a disagreement between readings of the rule.

A mutant's wall-clock per arm is recorded as measured, on a machine that other agents were also using.

## Cost

Per rule and arm: lines written for that rule (marked blocks in the arm's source; the Gherkin of the
scenario; the tactic lines of its proof), the shared lines amortised over the rules that use them
(step definitions and glossary; generator and harness helpers; the lemma library, attributed to the
proofs that import each module), and wall-clock on the unmutated code. The hand-written Lean line counts
come from `slice/effort/count.py`'s counting rules; build attempts and hours are quoted from
`slice/DESIGN.md` 12.4 and 12.8 and are the builder's own tally, not re-measured here.

## What the author knew when writing the arms

The properties (arm b) and harnesses (arm c) were written by the agent that ran this comparison, which
had read the hand-written mutant list and the rules' Lean definitions first. They were written, built
and passing on the unmutated code before `cargo mutants --list` was first run. So the tool set is
blind in the sense that matters (the properties were not written against it), and the hand-written set
is not. The collection sizes for arm b (0 to 6) were chosen knowing that two of the reviewer's mutants
need a fourth element.
