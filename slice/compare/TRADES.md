# K2 trade map: what each kind of evidence catches on the wallet and the ledger, and what it costs

2026-11-10. Plan node K2 (`docs/PLAN.md`). This is a map of trades, not a verdict on whether proof is
worth it. Two toy crates cannot settle which evidence a kind of rule should get; they can show where
each method ran out, and that is what is reported.

- **Compared:** the 23 universal rules of `slice/` as committed at `aa6f42a` (7 wallet, 16 ledger),
  discharged four ways: (a) their example rows on compiled Rust, (b) property-based tests, (c) Kani,
  (d) the existing Lean proofs.
- **Mutants:** every mutant cargo-mutants 27.1.0 generates for the two crates (52), and, labelled
  separately, the 45 hand-written ones of `slice/mutation/`.
- **Fixed beforehand:** `PREREG.md` (rules, kinds, bounds, seeds, what counts as detection). The arms,
  bounds, rules and mutant lists are unchanged since they were frozen at 2026-11-10T08:40:35+00:00 (checked when this file was built); digests in `results/frozen.json`. Deviations are
  listed in section 9. An independent review reproduced every number and corrected several conclusions;
  its corrections are applied here and its scripts and data are in `review/`.
- **Regenerate:** `./rerun.sh`. The tables below are generated (`results/tables.md`, `results/cost.md`);
  the prose and the numbers quoted in it are hand-written from them. Raw data: `results/results.json`
  (per mutant, arm and rule), `results/summary.json`, `results/cost.json`, `results/raw/`.

## In short

1. **On the unmutated code all four arms discharge all 23 rules.** Kani does so only up to a size on the
   ledger: 4 accounts and 3 transfers for ten rules; 2 accounts and 2 transfers for `batch_conserves`,
   `whole_conserves`, `batch_then_total` and `batch_then_total_overflow`; 2 accounts and 1 transfer per
   batch for `two_batches_conserve`; 3 accounts for `transfer_valid_moves`. The seven wallet harnesses
   have no size bound.
2. **Tool mutants (52; all compile, none equivalent): the arms are nearly indistinguishable when a
   mutant counts as caught through any rule.** Example rows 50, proptest 45 with plain generators and 50
   with edge-weighted ones, Kani 50, Lean 47 (its own search, which is also its figure under PREREG.md's
   definition). Lean reaches 49 only by counting `cm-l14` and `cm-l34`, whose lost proofs were confirmed
   false on the compiled Rust alone (the pipeline crashes evaluating their models), 10 of the 12 inputs
   written by hand from the diff. Two mutants are caught by no arm.
3. **They differ in which rule notices.** Counting (mutant, rule) pairs in which some arm shows the
   rule false, tool set:

| Kind of rule | Pairs where some arm shows the rule false | a. rows | b. plain | b. edge | c. Kani | d. Lean (of which by its own search) |
|---|---|---|---|---|---|---|
| safety / never-changes (6 rules) | 91 | 45 | 83 | 91 | 88 | 85 (74) |
| exact-result (6 rules) | 36 | 36 | 30 | 36 | 36 | 35 (34) |
| rejection-and-unchanged (9 rules) | 53 | 43 | 48 | 53 | 53 | 53 (52) |
| progress (1 rule) | 19 | 14 | 16 | 19 | 19 | 18 (17) |
| bound (1 rule) | 13 | 6 | 11 | 13 | 13 | 12 (11) |
| all 23 rules | 212 | 144 | 188 | 212 | 209 | 203 (188) |

   The Lean column includes 15 pairs confirmed by replay: 3 on the Lean model with proptest's inputs,
   and 12 on the compiled Rust only under `cm-l14` and `cm-l34` (10 with inputs written by hand).
   Counting only replays that fail on the Lean model, as PREREG.md defines confirmation, Lean has 191 of
   212 (safety 77, exact 34, rejection 52, progress 17, bound 11).

   Example rows notice half of the broken safety rules and all of the broken exact results. Plain random
   integers miss boundary comparisons. Kani misses what needs a third account, at the bound it was
   registered with (after the run, shapes chosen knowing the mutants find every such case in under a
   minute; section 4). The Lean pipeline's own search misses what its grid does not contain, and cannot
   complete on three mutants (one model does not build; on two non-terminating models its search crashes
   after the proofs have been checked).
4. **No mutant in either set is caught by proof alone.** Every rule the Lean arm shows false is also
   shown false by another arm. The two mutants built to be wrong at one magic amount (hand-written
   `d6`, `la6`) are found only by Kani; their proofs are lost, and that counts as detection for the Lean
   arm only once Kani's input is replayed on the Lean model.
5. **A proof that still checks on a mutant says less here than the count suggests.** The proof still
   checks in 404 (mutant, rule) pairs of the tool set, but in 396 of them the rule never calls the
   mutated function, so nothing the proof is about has changed. The other 8 are all wallet pairs, where
   Kani has no size bound and verifies the same 8. On the ledger no proof survived a mutant of a
   function its rule calls: in 92 such pairs the proof is lost although no arm shows the rule false
   (Kani verifies it within its bound and 20,000 generated cases find nothing), and 3 more have no
   model. On the hand-written set, 23 of the 336 surviving pairs are of a rule that calls the mutated
   function, all on the wallet; 124 ledger proofs are lost with no arm showing the rule false. What the
   proofs give that no other arm gives is the unbounded result on the unmutated ledger, not something
   measured on these mutants.
6. **Nothing catches 2 tool mutants and 2 hand-written ones** (section 5, with the rule each
   suggests). All four are caught only by literal-value scenarios. A third tool mutant is caught only
   because it can fail to terminate.
7. **Per rule, a property and a Kani harness cost about the same (properties 9 to 27 lines, harnesses 10
   to 23, medians 12 and 11). Example rows are 3 to 8 lines on top of a 5-to-11-line Gherkin statement,
   and the proof text is the shortest (3 to 10 lines); the difference is what stands behind it.** A
   ledger proof rests on 9 to 187 lines of hand-written lemmas (two loop invariants). Kani takes 73 s
   for the 16 ledger harnesses run one after another (1 to 9 s each, with the load at about 35), and its
   bound for rules about totals is small; proptest takes about a second.

## 1. The unmutated code

Every arm discharges every rule. "c (wall-clock)" is each harness run alone after the main run (the
load from other agents was then about 35); inside the main run the same harnesses took 2 to 111 s.

| Rule | Kind | Rows | a | b plain | b edge | c (wall-clock) | d |
|---|---|---|---|---|---|---|---|
| transfer_conserves | exact-result | 2 | pass | pass | pass | verified (0 s) | PROVED-FOR-ALL |
| withdraw_too_much | rejection-and-unchanged | 2 | pass | pass | pass | verified (0 s) | PROVED-FOR-ALL |
| deposit_overflow | rejection-and-unchanged | 2 | pass | pass | pass | verified (0 s) | PROVED-FOR-ALL |
| withdraw_covered | exact-result | 3 | pass | pass | pass | verified (0 s) | PROVED-FOR-ALL |
| deposit_with_room | exact-result | 3 | pass | pass | pass | verified (0 s) | PROVED-FOR-ALL |
| transfer_short | rejection-and-unchanged | 2 | pass | pass | pass | verified (0 s) | PROVED-FOR-ALL |
| transfer_no_room | rejection-and-unchanged | 2 | pass | pass | pass | verified (0 s) | PROVED-FOR-ALL |
| batch_conserves | safety / never-changes | 6 | pass | pass | pass | verified (7 s) | PROVED-FOR-ALL |
| batch_first_invalid | rejection-and-unchanged | 3 | pass | pass | pass | verified (6 s) | PROVED-FOR-ALL |
| batch_count_bounded | bound | 3 | pass | pass | pass | verified (4 s) | PROVED-FOR-ALL |
| batch_stops_at_invalid | progress | 5 | pass | pass | pass | verified (5 s) | PROVED-FOR-ALL |
| transfer_valid_moves | exact-result | 3 | pass | pass | pass | verified (9 s) | PROVED-FOR-ALL |
| transfer_invalid_rejected | rejection-and-unchanged | 5 | pass | pass | pass | verified (3 s) | PROVED-FOR-ALL |
| total_is_sum | exact-result | 5 | pass | pass | pass | verified (1 s) | PROVED-FOR-ALL |
| total_overflow | rejection-and-unchanged | 3 | pass | pass | pass | verified (1 s) | PROVED-FOR-ALL |
| balance_of_account | exact-result | 2 | pass | pass | pass | verified (1 s) | PROVED-FOR-ALL |
| balance_no_account | rejection-and-unchanged | 2 | pass | pass | pass | verified (1 s) | PROVED-FOR-ALL |
| whole_conserves | safety / never-changes | 2 | pass | pass | pass | verified (6 s) | PROVED-FOR-ALL |
| whole_first_invalid | rejection-and-unchanged | 1 | pass | pass | pass | verified (4 s) | PROVED-FOR-ALL |
| whole_rejected_unchanged | safety / never-changes | 4 | pass | pass | pass | verified (4 s) | PROVED-FOR-ALL |
| batch_then_total | safety / never-changes | 3 | pass | pass | pass | verified (7 s) | PROVED-FOR-ALL |
| batch_then_total_overflow | safety / never-changes | 2 | pass | pass | pass | verified (4 s) | PROVED-FOR-ALL |
| two_batches_conserve | safety / never-changes | 1 | pass | pass | pass | verified (8 s) | PROVED-FOR-ALL |

## 2. Detection, mutant by mutant

A mutant is counted for an arm if the arm detects it through at least one of the 23 rules. For the Lean
arm the two ways are shown separately: "shown false by the pipeline" (its own search on the Lean model
found a failing input) and "confirmed" (the proof is lost, and an input from another arm, replayed as
an extra Examples row, fails on the Lean model or, where the pipeline cannot evaluate the model, on the
compiled Rust).

| Mutant set | Mutants | Unviable | Viable | a. rows | b. plain | b. edge | c. Kani | d. Lean (shown false by the pipeline + confirmed with another arm's input) | d: proof lost only, nothing shown false | d: no model (pipeline stops) | No arm at all | ... of which a literal scenario fails | Oracle finds no difference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cargo-mutants, wallet | 13 | 0 | 13 | 13 | 11 | 13 | 13 | 13 (13 + 0) | 0 | 0 | 0 | 0 | 0 |
| cargo-mutants, ledger | 39 | 0 | 39 | 37 | 34 | 37 | 37 | 36 (34 + 2) | 2 | 1 | 2 | 2 | 0 |
| cargo-mutants, both | 52 | 0 | 52 | 50 | 45 | 50 | 50 | 49 (47 + 2) | 2 | 1 | 2 | 2 | 0 |
| hand-written, wallet | 18 | 0 | 18 | 17 | 14 | 17 | 18 | 18 (17 + 1) | 0 | 0 | 0 | 0 | 0 |
| hand-written, ledger (builder) | 22 | 0 | 22 | 19 | 18 | 20 | 21 | 21 (20 + 1) | 1 | 0 | 1 | 1 | 0 |
| hand-written, ledger (reviewer) | 5 | 0 | 5 | 4 | 4 | 4 | 2 | 4 (4 + 0) | 1 | 0 | 1 | 1 | 0 |
| hand-written, all | 45 | 0 | 45 | 40 | 36 | 41 | 41 | 43 (41 + 2) | 2 | 0 | 2 | 2 | 0 |

The '+ 2' of the tool rows are `cm-l14` and `cm-l34`, confirmed on the compiled Rust only, mostly with
hand-written inputs. The '+ 2' of the hand-written rows are `d6` and `la6`, confirmed with Kani's inputs
on the Lean model and the compiled Rust.

Reading it:

- **Tool set.** Of 52 mutants, 50 are caught by rows, by proptest with edge-weighted generators and by
  Kani; 45 by proptest with plain generators; 47 by the Lean arm's own search, or 49 if two
  non-terminating mutants (`cm-l14`, `cm-l34`) are counted on the strength of inputs replayed on the
  compiled Rust only (10 of 12 written by hand; PREREG.md asks for a replay that fails on the Lean
  model); for the last one, `cm-l26`, the generated model does not build. None is unviable, and the
  differential oracle finds a behavioural difference for every one, so none is equivalent.
- **Rows do this well only because a mutant needs just one rule to notice.** With the six
  literal-value scenarios added, rows reach 52 of 52 on the tool set and 43 of 45 on the hand-written
  set (the figure `slice/mutation/results.md` reports); the literal scenarios are not universal rules
  and are listed in their own column in appendix C.
- **Hand-written set.** These were written by the authors of the rules and rows, and the rows and the
  Lean search grid were later extended knowing them, so the row and Lean figures are a regression
  check. The proptest and Kani arms were written after reading this list (`PREREG.md`).
- **The reviewer's five ledger mutants** are the only place where Kani does worse than sampling: it
  catches 2 of 5, against 4 for rows, proptest and Lean. Two of the three it misses (`r1`, `r5`) sit
  beyond the size bound it was registered with (and are found in seconds at another shape: section 4);
  the third, `r4`, is caught through no universal rule by any arm.

Seconds per mutant, measured under load except `cm-w05`, whose raw record is the rerun alone of section
9 (the Lean figure is one whole pipeline run; Kani is the sum of its harnesses, run one at a time):

| Crate (viable mutants) | Arm | Median seconds per mutant | Largest | All mutants |
|---|---|---|---|---|
| wallet (31) | a. example rows | 1.12 | 3.13 | 38.9 |
| wallet (31) | b. proptest, plain | 0.41 | 1.87 | 19.4 |
| wallet (31) | b. proptest, edge | 0.26 | 7.62 | 41.7 |
| wallet (31) | c. Kani | 6.91 | 36.66 | 323.1 |
| wallet (31) | d. Lean | 169.72 | 369.99 | 6630.5 |
| ledger (66) | a. example rows | 0.74 | 300.03 | 656.9 |
| ledger (66) | b. proptest, plain | 1.21 | 240.67 | 428.1 |
| ledger (66) | b. proptest, edge | 2.3 | 960.62 | 1634.7 |
| ledger (66) | c. Kani | 233.31 | 716.45 | 18598.9 |
| ledger (66) | d. Lean | 141.42 | 316.49 | 10244.9 |

## 3. Detection by kind of rule

The unit is a (mutant, rule) pair in which some arm shows the rule false of the mutant; mutants in
brackets. "All pairs" is every rule of the mutated crate times every viable mutant.

Tool set (cargo-mutants):

| Kind of rule | Rules | Rule shown false of a mutant by some arm: pairs (mutants) | a. rows | b. plain | b. edge | c. Kani | d. Lean | Kani timeouts (pairs) | Lean: proof lost, not shown false (of which Kani verifies the rule on the mutant) | Lean: still proved | All pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safety / never-changes | 6 | 91 (22) | 45 (16) | 83 (21) | 91 (22) | 88 (22) | 85 (21); 74 by its own search | 1 | 55 (55) | 88 | 234 |
| exact-result | 6 | 36 (36) | 36 (36) | 30 (30) | 36 (36) | 36 (36) | 35 (35); 34 by its own search | 0 | 3 (3) | 115 | 156 |
| rejection-and-unchanged | 9 | 53 (32) | 43 (30) | 48 (28) | 53 (32) | 53 (32) | 53 (32); 52 by its own search | 0 | 26 (26) | 163 | 247 |
| progress (1 rule) | 1 | 19 (19) | 14 (14) | 16 (16) | 19 (19) | 19 (19) | 18 (18); 17 by its own search | 0 | 1 (1) | 19 | 39 |
| bound (1 rule) | 1 | 13 (13) | 6 (6) | 11 (11) | 13 (13) | 13 (13) | 12 (12); 11 by its own search | 0 | 7 (7) | 19 | 39 |

Hand-written set:

| Kind of rule | Rules | Rule shown false of a mutant by some arm: pairs (mutants) | a. rows | b. plain | b. edge | c. Kani | d. Lean | Kani timeouts (pairs) | Lean: proof lost, not shown false (of which Kani verifies the rule on the mutant) | Lean: still proved | All pairs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| safety / never-changes | 6 | 41 (15) | 21 (11) | 36 (14) | 36 (14) | 34 (13) | 41 (15); 36 by its own search | 0 | 69 (69) | 52 | 162 |
| exact-result | 6 | 18 (18) | 16 (16) | 12 (12) | 16 (16) | 18 (18) | 18 (18); 16 by its own search | 0 | 6 (6) | 111 | 135 |
| rejection-and-unchanged | 9 | 30 (23) | 27 (23) | 28 (21) | 30 (23) | 30 (23) | 30 (23); 30 by its own search | 0 | 28 (28) | 149 | 207 |
| progress (1 rule) | 1 | 6 (6) | 5 (5) | 5 (5) | 6 (6) | 5 (5) | 6 (6); 6 by its own search | 0 | 9 (9) | 12 | 27 |
| bound (1 rule) | 1 | 2 (2) | 0 (0) | 2 (2) | 2 (2) | 2 (2) | 2 (2); 2 by its own search | 0 | 13 (13) | 12 | 27 |

What the two tables say, kind by kind (tool set unless stated):

- **Safety / never-changes.** This is where the arms differ most. Example rows show the rule false in 45
  of 91 pairs: a conservation rule has 1 to 6 rows, and a row notices a broken total only if its batch
  happens to exercise the broken path. Proptest with edge-weighted generators finds all 91; with plain
  generators 83. Kani finds 88: two of its misses need a third account (`batch_then_total_overflow` is
  falsified only by two balances that overflow together and a third that carries the bug, and Kani's
  bound for rules about totals is two accounts), and one is a timeout, still unanswered after 900 s, on
  a loop that does not terminate. The Lean pipeline's own search finds 74, and 77 once proptest's inputs
  are replayed on the Lean model. Counting also 8 pairs under `cm-l14` and `cm-l34` that were confirmed
  on the compiled Rust only (7 with hand-written inputs, 1 with Kani's), it reaches 85.
- **Exact-result.** Rows find all 36. Proptest with plain generators finds 30: the six it misses are
  boundary comparisons (`>` for `>=`, `<` for `<=`, `<` for `==`), wrong only when the amount equals
  the balance, which a uniform draw from 2^64 values does not produce. Weighting the ends of each
  range finds them.
- **Rejection-and-unchanged.** The same pattern, with rows missing 10 of 53.
- **Progress and bound.** One rule each, so these two lines describe `batch_stops_at_invalid` and
  `batch_count_bounded`, not two kinds. The bound rule is the one rows serve worst (6 of 13): a row
  shows a count too large only if the mutant over-counts on that row's batch.

How early sampling finds what it finds: on the tool set the median failing case is the 2nd or 3rd of
10,000 and the latest is the 207th. On the hand-written set the reviewer's `r1` (the batch silently
stops after three transfers) is found at case 3,305 with plain generators and 5,897 with edge-weighted
ones: 10,000 cases was enough, 1,000 would probably not have been.

Per rule, for reference: appendix A.

## 4. What only one arm finds, and why

"Finds" means the arm produced the falsifying input itself; for the Lean arm, its own search.

**At the level of a whole mutant, one arm stands alone only for the two magic-value mutants:**

| Mutant | Found by | Why the others miss it |
|---|---|---|
| hand `d6`: a deposit of exactly 1,000,003 credits one unit too few | Kani only (`deposit_with_room`, 2 s) | Integers are symbolic in Kani, so one value in 2^64 is as easy as any other. No row uses it; 20,000 generated deposits do not hit it; the Lean pipeline's grid does not contain it, so its only signal is a lost proof |
| hand `la6`: the same in `Ledger::apply` | Kani only (6 rules, within its 2- and 3-account bounds) | as above |

For both, replaying Kani's input (`a = 0, amount = 1000003` for `d6`) as an Examples row makes the row
fail on the Lean model and on the compiled Rust, which is what turns "proof lost" into "confirmed
false". cargo-mutants generates no mutant of this kind (it swaps operators and replaces bodies), so
the tool set has no mutant that only one arm finds.

**At the level of a rule, the sole finders are** (with edge-weighted proptest as arm b):

| Arm | Pairs it alone finds | What they are |
|---|---|---|
| Proptest | 3 tool pairs | `batch_then_total_overflow` under `cm-l22` and `cm-l23` (wrong funds comparison in `apply`): the falsifying ledger needs three accounts, beyond Kani's bound of two for total rules and not in the Lean grid; sampling with up to six accounts finds it within a dozen cases. And `two_batches_conserve` under `cm-l34` (a batch loop that does not terminate), where Kani gives no answer in 900 s |
| Kani | 7 hand pairs | the magic-value mutants above |
| Rows | none | every row is one input; the other arms try it or a neighbour |
| Lean, by its own search | none | on these crates its grid is covered by what proptest and Kani try |

Against proptest with plain generators Kani is also alone on 11 tool pairs: three rules under
`cm-l26` (`f / amount` for `f - amount`) that fail only through a division by zero at amount 0, and
eight under the two non-terminating loops.

**What each arm misses although another arm shows the rule false** (pairs):

| Arm | Tool | Hand | The misses are |
|---|---|---|---|
| a. rows | 68 | 28 | mostly safety rules whose rows do not exercise the broken path |
| b. plain | 24 | 14 | boundary comparisons; amount 0; magic values; a loop that fails to terminate only for small amounts |
| b. edge | 0 | 7 | magic values only |
| c. Kani | 3 | 8 | what needs more than its size bound: a third account (`batch_then_total_overflow`; hand `lt2`, `r2` through the two-step rules), a fourth transfer (hand `r1`), a third loop iteration under a total rule (hand `r5`: one unit minted in the third iteration); and one timeout |
| d. Lean, own search | 24 | 7 | 9 pairs because one mutant's model does not build, 12 because evaluating a non-terminating loop crashes the search, 3 three-account cases; on the hand-written set the 7 magic-value pairs |

A bug beyond the bound Kani was run with is not hypothetical here: the reviewer's `r1` and `r5` are
exactly that, and both are found by random batches of up to six transfers. The size 6 was chosen knowing
that two reviewer mutants need a fourth element (PREREG.md), so this comparison favours proptest.

### Kani's bounds, probed after the run (exploratory, not part of the registered comparison)

The bounds in `PREREG.md` were chosen from timings taken while 6 to 12 harnesses ran at once on a
loaded machine, and one size was registered per rule. After the run each question was put to Kani
again, alone (`harness/kani_probe.sh`, `harness/kani_probe_mutants.py`,
`results/kani_bounds_probe.*`):

| Question | Answer |
|---|---|
| Unmutated code, rules without a total: how large can the bound go? | `batch_stops_at_invalid` verifies at 6 accounts and 4 transfers in 5 s, `total_is_sum` at 8 accounts in 2 s. The registered 4 and 3 was far below what Kani can do |
| Unmutated code, `batch_conserves`: accounts against transfers | 2 accounts and 3 transfers: 19 s. 3 accounts and 2 transfers: 529 s. 3 accounts and 3 transfers: no answer in 600 s. More transfers are cheap; a third account is what costs |
| Do other bounds catch the pairs missed at the registered ones? | Yes, each in 3 to 5 s: hand `r1` at 6 accounts and 4 transfers; hand `r5` at 2 accounts and 3 transfers; `cm-l22`, hand `lt2` at 3 accounts and 1 transfer; hand `r2` at 4 accounts and 1 transfer |

So the size-bound misses of Kani in sections 2 to 4 come from the bound it was registered with: at a
shape picked afterwards for each mutant, Kani found each of the 5 pairs probed in 3 to 5 s. An
independent review run (`review/kani_ladder.json`; exploratory, load 50 to 70) then put all 10 missed
pairs through one fixed ladder, the same for every mutant: 4 accounts and 1 transfer, and 2 accounts and
3 transfers, for the total rules; 6 accounts and 4 transfers for `batch_stops_at_invalid`. Every pair
failed at one of the shapes, in 6 to 48 s. No single shape caught all of them: `cm-l22`, `cm-l23`, `lt2`
and `r2` need the first, and `r5` needs the second (at the first it verifies). The shapes were chosen
knowing the mutants, so this is not a blind result. What is limited is the other direction, showing that
a total rule HOLDS at a given size: 9 minutes for one rule at 3 accounts and 2 transfers. At the
review's two shapes the unmutated code took 44 to 243 s per total rule at 4 accounts and 1 transfer, and
45 to 109 s at 2 accounts and 3 transfers; `two_batches_conserve` gave no answer in 300 s at either. The
registered figures are left as they are; a rerun with a ladder of shapes per rule, chosen on a quiet
machine, is the first next action for this arm.

## 5. What nothing catches

No arm shows any universal rule false of these mutants. The differential oracle confirms that each
behaves differently from the original, so none is equivalent: they are behaviour that no arm shows the
23 rules to exclude. For `cm-l36`, the suite adequacy note proves in the kernel that the three
`apply_all` rules hold of a function that rejects everything. For `cm-l39` and `lw3` (3 proofs lost
each) and `r4` (10 lost), it rests on Kani within its bound, sampling and the argument in the table. All
are caught by literal-value scenarios, which is the only reason the existing pipeline goes red on them.

| Mutant | Change | A difference in behaviour | Caught only by the literal scenario | What the rules leave open |
|---|---|---|---|---|
| tool `cm-l36` | `Ledger::apply_all` always returns false (body replaced) | `apply_all([], [])`: true becomes false | `whole_example_accept` | **No universal rule says `apply_all` ever accepts.** `whole_conserves`, `whole_first_invalid` and `whole_rejected_unchanged` are all true of a function that rejects everything |
| tool `cm-l39`, hand `lw3` (the same change) | `applied <= batch.len()`: every batch is rolled back and rejected | as above | `whole_example_accept` | the same |
| hand `r4` | a rejected last transfer (not the first) is counted as applied | the count is one too high | `whole_example_rollback`, `whole_example_rollback_late` | **No universal rule fixes the count.** It is bounded above by the length, and "stopped only at an invalid transfer" says nothing when the count equals the length |

Candidate rules these suggest (input for the rule authors and for F1's adequacy note; argued from
the diffs, not written, run or proved here):

1. *Applying a batch as a whole is accepted exactly when applying the same batch one transfer at a
   time applies every transfer, and then both leave the same ledger.* A two-run rule (the "agrees
   with a reference" frame of the plan's catalogue). It is false of `cm-l36`, `cm-l39` and `lw3`. It
   is NOT false of `r4`, which miscounts in both operations consistently.
2. *A batch followed by one more transfer: if the batch alone is applied in full and the extra
   transfer is valid on the ledger the batch leaves, one more is applied and the ledger is that ledger
   after the transfer; if it is not valid, the count and the ledger are those of the batch alone.*
   Also a two-run rule. With the empty batch it fixes the count and the ledger of every batch, so it
   is false of `r4`, and false of `cm-l34` without relying on non-termination. It is the inductive
   form of the pure model that `DESIGN.md` 12.8 declined to put in the glossary; whether stating it as
   a rule about two runs avoids that objection is for the vocabulary track to decide.

Three more things the rules leave open, found while classifying:

- **`cm-l34` (`i *= 1` in the batch loop) is caught only because it can fail to terminate.** The
  counter stays 0, so the first transfer is applied again and again until it stops being valid, and
  the function then returns 0. Whenever it does return, every universal rule holds: the total is
  conserved, 0 is at most the length, the transfer it stopped at is indeed invalid on the ledger it
  left, and nothing is rejected that should not be. It is noticed only where the repetition runs
  long: a zero-amount transfer stays valid for ever, and a small amount against a large balance
  repeats about 10^18 times (rows: one such row does not finish; proptest with edge-weighted
  generators: hangs; Kani: unwinding assertions; proptest with plain generators: not at all, since a
  uniform amount drains the sender in a step or two). This is the plainest instance of what
  `DESIGN.md` 12.8 records: the universal rules do not say which ledger a batch leaves.
- **`cm-l38` (`applied > batch.len()`: `apply_all` never rolls back and always accepts) is caught, but
  only by `whole_first_invalid`.** The atomicity rule `whole_rejected_unchanged` is true of it,
  because it never rejects. A rule of the form "if rejected, unchanged" needs the companion "is
  rejected when ..." for every way a batch can fail, not only for a bad first transfer.
- **Wallet: nothing survives.** All 13 tool mutants and all 18 hand-written ones are shown false by
  some rule.

## 6. The Lean arm in detail

Every rule of the mutated crate on every mutant, by what happened to its proof:

| Outcome for the rule's proof on the mutant | Tool set | Hand-written set |
|---|---|---|
| still proved | 404 | 336 |
| shown false by the pipeline's own search, kernel-checked refutation | 43 | 21 |
| shown false by the pipeline's own search, on the model only | 145 | 69 |
| proof lost, confirmed false: another arm's input fails on the Lean model and the compiled Rust | 3 | 7 |
| proof lost, confirmed false on the compiled Rust only (the pipeline crashes evaluating the model) | 12 | 0 |
| proof lost, not shown false | 92 | 125 |
| no model (the generated Lean does not build) | 16 | 0 |
| all pairs (every rule of the mutated crate, every mutant) | 715 | 558 |

- **Still proved** means the unchanged proof of the unchanged statement builds against the Aeneas model
  of the mutant: the rule holds of that model for every input and size. That the model means the Rust is
  trusted, as everywhere in arm d. For 18 of the 404 tool pairs (`cm-l14`, `cm-l34`) the pipeline
  crashed before its audit, so these rest on `lake build` alone, without the exact-type and axiom check.
  In 396 of the 404 the rule never calls the mutated function. The other 8 (23 on the hand-written set)
  are all wallet pairs; Kani has no size bound on the wallet and verifies the same pairs on the compiled
  Rust. Kani verifies all 404 (within its bound on the ledger); proptest and rows give "no failure
  found".
- **Proof lost, not shown false.** On the tool set, in all 92 pairs Kani verifies the rule on the mutant
  within its size bound and neither proptest profile finds a failing case. As far as these arms can tell
  the rule still holds, and the proof is broken because the hand-written lemma about the mutated
  function no longer proves. That the rule holds beyond Kani's bound and the samples is not shown. On
  the hand-written set the same is true of all 125.
- **Confirmed on the compiled Rust only** are the rules falsified by the two non-terminating loops
  (`cm-l14`, `cm-l34`): the pipeline's search overflows the stack evaluating the model, so the input
  cannot be replayed there; on the compiled Rust the call does not return within 90 s. Ten of these
  twelve inputs were written by hand from the diff (`mutants/hand-witnesses.json`), because a hang
  has no shrunk input and Kani's reported input need not loop for ever.
- **No model**: `cm-l26` replaces `f - t.amount` by `f / t.amount`; Aeneas emits a call to
  `Aeneas.Std.U64.div`, which the shipped Lean library does not define, so the generated model does
  not build and no rule of either crate gets a verdict. Nine of its sixteen ledger rules are false on
  the compiled Rust. This is not counted as detection.

Three things follow.

- **A lost proof is often not a detection, and by itself does not say which it is.** On the tool set 295
  proofs are lost: 188 of rules the pipeline's own search shows false, 15 of rules shown false only by
  replaying an input from elsewhere, and 92 of rules no arm shows false (Kani verifies them within its
  bound and neither proptest profile fails). On the hand-written set 222 are lost: 90, 7 and 125. Among
  the lost proofs the pipeline's own search does not resolve, 92 of 107 (tool) and 125 of 132 (hand) are
  of rules no arm shows false. This is the figure behind `docs/PLAN.md` rule 5. A mutant in `apply`
  costs 12 rules their proofs whether it falsifies all 12 of them or only 2.
- **A proof that survives is real information, but on these mutants it seldom says more than a
  dependency check.** For 404 pairs of the tool set, the question "does this mutant break this rule?" is
  closed for every input and size on the Lean model. In 396 of them the rule does not call the mutated
  function; the other 8 are wallet pairs that Kani, unbounded there, also closes. On the ledger, every
  mutant of a function a rule calls cost that rule its proof, whether or not the rule became false.
- **The pipeline's own counterexample search is the weak part of the arm, and it is replaceable.** It
  found 188 of the 212 false pairs of the tool set. Every input it missed was produced by proptest, by
  Kani or by reading the diff. Replayed through the unchanged pipeline as extra Examples rows
  (`harness/confirm.py`), 3 of the 24 were shown false on the Lean model. The other 21 are under mutants
  the pipeline cannot evaluate: 9 under `cm-l26` (no model) and 12 under `cm-l14` and `cm-l34`, where
  its search crashes. So replay helps there only once those two pipeline gaps are fixed. `docs/PLAN.md`
  already proposes borrowing counterexample search from existing tools; this measures it.

## 7. Cost

Lines written per rule, by crate and kind (averages; per rule in appendix B). "Lemma lines the proof
rests on" is the full size of the hand-written lemma modules a proof imports; "share" divides each
module among all scenario proofs that import it.

| Crate | Kind | Rules | Gherkin statement lines | a: rows lines | b: property lines | c: harness lines | d: proof lines | d: lemma lines, share | d: lemma lines the proof rests on | b: ms plain / edge | c: seconds | d: seconds to re-check the proof |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| wallet (straight-line) | exact | 3 | 8.3 | 4.7 | 13.7 | 11.0 | 4.7 | 0.0 | 0.0 | 12.3 / 31.0 | 0.4 | 5.5 |
| wallet (straight-line) | rejection | 4 | 8.2 | 4.0 | 13.8 | 10.8 | 4.0 | 0.0 | 0.0 | 11.2 / 31.0 | 0.3 | 5.4 |
| ledger (loops, Vec) | safety | 6 | 6.0 | 5.0 | 10.8 | 12.0 | 5.2 | 13.6 | 174.7 | 36.0 / 131.7 | 6.0 | 5.4 |
| ledger (loops, Vec) | exact | 3 | 6.7 | 5.3 | 15.3 | 15.3 | 5.0 | 6.8 | 63.7 | 19.3 / 48.3 | 3.9 | 5.3 |
| ledger (loops, Vec) | rejection | 5 | 6.6 | 4.8 | 11.8 | 12.0 | 4.2 | 8.9 | 106.2 | 25.2 / 89.4 | 3.2 | 5.4 |
| ledger (loops, Vec) | progress | 1 | 5.0 | 7.0 | 12.0 | 13.0 | 3.0 | 9.1 | 153.0 | 25.0 / 103.0 | 5.3 | 5.3 |
| ledger (loops, Vec) | bound | 1 | 5.0 | 5.0 | 10.0 | 11.0 | 3.0 | 9.1 | 153.0 | 25.0 / 114.0 | 3.6 | 5.3 |

Shared code, written once per arm:

| Arm | Shared code | Lines |
|---|---|---|
| a | cucumber step definitions and the Rust reading of each phrase (`wallet-bdd`), serving all 35 scenarios | 360 + 272 |
| b | generators, runner, shrunk-input printer (`arms/proptests`, outside the rule blocks) | 255 |
| c | symbolic input builders and helpers (`arms/kani`, outside the rule blocks) | 84 |
| d | glossary definitions in Lean (24 wallet, 55 ledger), `glossary.yaml` (411), the lemma library (227 code lines: 2 loop invariants, 18 theorems), and the generator and audit (`slicegen`, not counted) | 79 + 411 + 227 |

Wall-clock on the unmutated code, all 23 rules. Each figure was measured alone after the main run;
in brackets, the same measurement taken inside the main run, with eight other pipeline copies and
other agents' work on the machine:

| Arm | Build | Run | Notes |
|---|---|---|---|
| a. example rows | 5.6 s (61 s) | 0.4 s (2.5 s) | all 35 scenarios of the three feature files |
| b. proptest | 1.4 s (10.9 s) | plain 0.7 s (1.5 s); edge 1.8 s (5.0 s) | 23 properties, 10,000 cases each |
| c. Kani | 7.6 s (44 s) | 75 s (681 s), of which the 16 ledger rules 73 s (663 s) | 23 harnesses run one at a time; per rule in appendix B |
| d. Lean | - | 53 s (273 s) | the whole pipeline: translation, build, search, audit, cucumber, report. Re-checking one proof after an edit: 5 to 6 s; rebuilding the lemma library: 18 s |

What the line counts do not show:

- **Lean (d).** The proof text per rule is the smallest number in the table, and it is small because the
  lemma library carries the difficulty. The effort data of the slice (`DESIGN.md` 12.4 and 12.8,
  `effort/attempts.tsv`; the builder's own tally, not re-measured here): wallet, 9 proofs of 4 to 6
  lines, 2 failed attempts in all; ledger lemma library, about 30 builds of which 17 failed and an
  estimated 1.5 to 2 agent-hours, plus about 60 lines and 11 builds (8 failed) for the exact-result
  part; scenario proofs after that, accepted at the first or second build.
- **Kani (c).** The harness text is as short as a property test, but three things had to be found by
  trial before the ledger harnesses finished at all: a `Vec` built by pushing in a symbolic loop, and
  a clone of a `Vec` of symbolic length, each took a single-transfer harness from 2 s to over a minute
  or to no answer in 5 minutes; and comparing a 128-bit total before and after a batch did not finish
  in 240 s at 3 accounts and 2 transfers with CaDiCaL, Kissat or MiniSat while other harnesses were
  running (CBMC's SMT back end crashed with both Z3 4.13 and 5.4). Roughly 40 minutes went into this.
  The bounds in `PREREG.md` are the result; the probe in section 4 shows they were more cautious
  than they needed to be for rules without a total.
- **Proptest (b).** The one judgement that mattered was the distribution of integers: 6 lines turn
  45 of 52 into 50 of 52.
- **Rows (a).** They are part of the scenario already; their cost is choosing them, and the review
  history of the slice shows that the choice was revised after each of its two reviews.

## 8. What this suggests as the default evidence for each kind of rule

Each line is a trade read off two toy crates (three straight-line functions; two loops over one flat
`Vec<u64>`) and two mutant sets, one of which only swaps operators and replaces bodies. It is a
starting default to be overturned by the first real target, not a finding about real systems.

| Kind of rule | A reasonable default, and what is given up | What would change it |
|---|---|---|
| **Exact-result, rejection-and-unchanged on straight-line integer code** (the wallet) | Rows plus a Kani harness. Kani covers every 64-bit value in under a second for 11 lines, found the magic-value bug, and runs on the real Rust with no model and no glossary in the trusted base (its own trusted base is the Kani compiler, CBMC and the harness's reading of the rule). A Lean proof here costs 4 to 6 lines and gives the same coverage; what it adds is the tie to the signed vocabulary and a proof object, and what it costs is the pipeline (about a minute against under a second) and the trust in the translation. Plain property tests are the weakest choice for these kinds unless the generators are weighted to the ends of each range | arithmetic that is hard to bit-blast (multiplication, division by a variable: not tried here); rules that must be stated in the shared vocabulary for a reader to sign |
| **The same kinds over a collection** (ledger: `apply`, `balance`, `total`, first-transfer-invalid) | Rows plus property tests with edge-weighted generators, plus Kani at a moderate size. Kani at 4 accounts and 3 transfers took 1 to 9 s per rule alone and missed nothing in the tool set, and the probe shows 6 accounts and 4 transfers is still seconds; a proof costs 3 to 6 lines once a lemma about the function exists, and that lemma is the cost | whether the function already has a lemma (then the proof is nearly free and is the only arm with no size bound) |
| **Safety / never-changes over a loop** (conserved totals, atomic rollback) | Property tests first: 11 lines, about a second, and with edge-weighted generators they found every broken total of the tool set, including the cases beyond Kani's registered bound (2 pairs on the tool set; 7 safety pairs on the hand-written set, plus `r1` on the progress rule). Then a proof where the invariant is worth owning: it is the only evidence with neither a sample nor a size bound, and the ledger's two invariants cost roughly an agent-hour each. On the mutants here, every ledger proof whose rule calls the mutated function was lost, including 92 tool pairs in which no arm shows the rule false; what re-proving costs was not measured. Kani splits in two for totals. As a bug-finder it is good here. After the run, one fixed ladder of shapes chosen knowing the mutants (4 accounts and 1 transfer, and 2 accounts and 3 transfers, for the total rules; 6 accounts and 4 transfers for the progress rule) found every pair the registered size bounds missed, in under a minute each; no single shape found them all. The registered bounds found the magic values. As evidence that the rule holds it is weak: 2 accounts and 2 transfers takes 4 to 8 s per rule, 3 accounts and 2 transfers 9 minutes. Rows alone are the weak choice: they noticed about half of the broken totals | a solver that handles sums (an SMT back end that works with CBMC here, or Kani loop contracts), which would move Kani's bound; a second crate, to see whether invariants get cheaper with practice (plan node P2) |
| **Progress** (one rule) | No default can be drawn from one rule. On it, edge-weighted proptest and Kani find all 19 broken cases of the tool set and rows 14, and the rule itself is silent when the whole batch is counted as applied (hand `r4`) | more progress rules; the candidate rules of section 5 |
| **Bound** (one rule) | No default from one rule. It is the cheapest rule to state and to prove (3 lines), and the one rows serve worst (6 of 13) | - |

Two cross-cutting points, with the same caveat:

- **Detection is not where proof paid for itself in this experiment.** No mutant needed a proof to be
  caught. What the proofs supplied was independence from sample and size on the unmutated code. On the
  mutants, 396 of the 404 proofs that still check are of rules that do not call the mutated function,
  and the other 8 are wallet pairs that Kani also verifies without a bound. What they cost was the
  lemmas and 92 proofs lost although no arm shows their rule false. A mutation score cannot weigh those
  against each other: it only counts catches.
- **The arms are better combined than ranked.** Kani and proptest are good at producing inputs; the
  Lean pipeline is good at saying a rule holds for all inputs and weak at finding inputs. Feeding the
  first two into the third (section 6) costs one extra Examples row per input.

## 9. Awkward results and deviations

- **Run under heavy load.** Other agents were using the machine (load average 40 to 110 on 18
  cores) and nine pipeline copies ran side by side. The per-mutant times of section 2 are what was
  measured and are inflated, unevenly: one wallet mutant (`cm-w05`) rerun alone afterwards, with the
  load at about 35, gave the identical outcome in every arm in 82 s against 514 s (pipeline 61 s
  against 371 s; its seven Kani harnesses 2.7 s against 16.4 s). The costs on the unmutated code in
  section 7 were therefore measured again alone; both sets of figures are kept
  (`results/baseline.under-load.json`). The only Kani timeouts are on a mutant that does not
  terminate; two of the three went away when retried alone with a longer limit.
- **A failing Examples row does not change the pipeline's verdict.** With `a = 0, amount = 1000003`
  added to `deposit_with_room` under `d6`, the report says "3 of 4 rows pass on the Lean model" and the
  verdict stays TESTED-ONLY, "counterexample: none". The analysis here counts a failing row on the
  model as "shown false"; the pipeline does not.
- **The pipeline crashes on a model that does not terminate.** `cm-l14` and `cm-l34` (`i *= 1` in the
  two loops) overflow the stack in step 5 (search), after the proofs have been checked, so no verdict
  is printed for any scenario. The lost proofs are read from `out/proofs.json`; rules whose proof
  module still built are counted as still proved.
- **The pipeline cannot build the model of `cm-l26`** (`Aeneas.Std.U64.div` is not in the shipped
  library; the two wallet mutants with `/=` translate and build). Counted as "no model", not as
  detection.
- **Non-termination is awkward for every arm.** Rows and proptest see it as a hang (300 s for the
  cucumber run, then 60 s per scenario; 120 s per property), which has no shrunk input. Kani sees it
  as an unwinding assertion, and the input it reports need not be a counterexample: under `cm-l14`
  the ledger it gives for `total_overflow` keeps adding a non-zero first balance until the sum
  overflows and returns "no result", which is correct; the rule is false on a ledger whose first
  balance is 0. Unwinding failures count as detection, as registered; 9 tool pairs rest on one alone
  (2 under `cm-l14`, 7 under `cm-l34`). These two mutants also account for the largest times in the
  table of section 2 (40 minutes for `cm-l34` alone).
- **Three Kani timeouts in the main run, all on `cm-l34`** (its three total rules, at 180 s under load).
  Retried alone with 900 s (`harness/kani_retry.py`): two then fail on an unwinding assertion after 146
  s and 283 s, and `two_batches_conserve` still gives no answer. The tables use the retried results; the
  first attempts are kept in the raw file. No other harness timed out on any mutant. In a review rerun
  of `cm-l34` the 180 s outcome differed: `batch_conserves` failed in 85 s, `batch_then_total` timed
  out. After the same 900 s retry both runs agree. At 180 s, the Kani outcome on this mutant depends on
  load.
- **Changed after the first freeze, before any mutant was run:** a parsing fix in `harness/run.py` (the
  baseline had failed on a key of `search.json`); `results/frozen.json` was rewritten then. The arms,
  bounds, rules and mutant lists were not touched afterwards (`harness/freeze.py --check`). Added during
  the run, to the analysis only: the three Lean sub-outcomes "an Examples row fails on the model", "no
  model", and confirmation on the compiled Rust when the pipeline cannot evaluate the model.
  `harness/confirm.py`, `harness/kani_retry.py` and `mutants/hand-witnesses.json` were written during
  the run. `confirm.py` and `kani_retry.py` implement the registered definition of detection. The
  hand-written inputs, and confirmation on the compiled Rust alone, do not: PREREG.md asks for an input
  found by another arm, replayed on the Lean model and the compiled Rust. They decide 12 tool pairs and,
  at mutant level, `cm-l14` and `cm-l34` for the Lean arm (49 against 47 of 52). `harness/run.py` was
  restarted once to move the remaining mutants off the worker that was waiting on `cm-l34`; no result
  was discarded except the runs in flight.
- **No unviable mutants, no equivalent mutants, and no case where an arm reports a rule false that
  the kernel still proves.** The last is a check on the three hand-written readings of each rule (Lean
  vocabulary, proptest property, Kani harness): on 97 mutants they never disagreed.
- **The Kani bounds were set too low for rules without a total**, from timings taken under load
  (section 4, probe). The registered results are reported as run; the probe is labelled exploratory.
- **How strong each arm's reading of a rule is.** All three executable readings assert the same
  predicate as the Lean statement: Givens as constraints on the inputs, Thens as assertions, and a panic
  counted as failure, as the statement's `= ok` requires. They differ in the inputs they cover. Proptest
  is weaker than the statement: integers are sampled; ledgers and batches have at most 6 elements; a
  transfer's account numbers are drawn only from 0 to the ledger's length (Lean and Kani take any
  `usize`). Where a Given is enforced by filtering, the sample is skewed: with plain generators about
  92% of the ledgers whose balances add up to a u64 (`total_is_sum`, `batch_then_total`) have at most
  two accounts (simulated). Kani is exhaustive over integers and account numbers, but only within its
  size bounds on the ledger. Rows are single instances. In one respect the executable arms are stronger
  than the statement: a run that is merely slow counts as a failure (120 s per property, 300 s for the
  cucumber run, more than 6 loop iterations under Kani's unwinding check), whereas the statement
  requires only that the call terminate. Every such detection here is under `cm-l14` or `cm-l34`, where
  non-termination is real (`mutants/hand-witnesses.json`), so no count changes. Detection differs
  between arms in two ways. A hang counts for rows and proptest, but a Kani timeout and a pipeline crash
  do not. Only the Lean arm is credited with inputs found elsewhere.
- **Not done:** bugs transplanted from real fix commits (the plan mentions them); a third mutant source
  with constant changes and statement deletions; re-proving the 92 lost proofs whose rule no arm shows
  false (true within Kani's bound and the samples) to measure the repair cost; timing on an idle
  machine.

## 10. Next actions

1. **Write the two candidate rules of section 5** and rerun: by the argument there, the four
   survivors should then be shown false.
2. **Pipeline:** make a failing Examples row a COUNTEREXAMPLE verdict; give the model search a step
   limit so a non-terminating loop is reported as "diverges on this input" instead of a crash; report
   `Aeneas.Std.U64.div` to K3's list of translation gaps.
3. **Adopt the replay:** let the pipeline take falsifying inputs from proptest and Kani
   (`harness/confirm.py` is the prototype). On the tool set it confirmed 15 lost proofs as false (3 by
   replay on the Lean model, 12 on the compiled Rust where the model cannot be evaluated, 10 of them
   with inputs written by hand, which PREREG.md does not count), and on the hand-written set the 7 pairs
   of the two magic-value mutants.
4. **Kani:** rerun arm c with a ladder of shapes per rule (accounts-heavy, transfers-heavy), chosen on a
   quiet machine; the probe and the review ladder of section 4 say its size-bound misses would go,
   though no single shape catches all of them and both sets of shapes were chosen knowing the mutants.
   For showing that a total rule holds at 3 or more accounts, try loop contracts or an SMT solver that
   CBMC 6.11 can drive.
5. **Brittleness:** measure what it costs an agent to repair the 92 lost proofs whose rule no arm shows
   false (input to plan node S2), and whether finer lemma modules reduce the number.
6. **A harder mutant set:** real fix commits, and mutants wrong only at a large size and a rare value
   together, which is the one case where neither sampling nor a bound can help and only a proof (or its
   loss) would speak.
7. **Rerun `cost.py --time-proofs` and the baseline on an idle machine** for clean timings.

## Appendix A. Per rule

Tool set:

| Rule | Kind | Viable mutants of its crate | Rule shown false by some arm | a | b plain | b edge | c | d | c timeout | d proof lost, not shown false | d still proved |
|---|---|---|---|---|---|---|---|---|---|---|---|
| transfer_conserves | exact-result | 13 | 6 | 6 | 4 | 6 | 6 | 6 | 0 | 0 | 7 |
| withdraw_too_much | rejection-and-unchanged | 13 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 10 |
| deposit_overflow | rejection-and-unchanged | 13 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 12 |
| withdraw_covered | exact-result | 13 | 6 | 6 | 4 | 6 | 6 | 6 | 0 | 0 | 7 |
| deposit_with_room | exact-result | 13 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 12 |
| transfer_short | rejection-and-unchanged | 13 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 10 |
| transfer_no_room | rejection-and-unchanged | 13 | 4 | 4 | 2 | 4 | 4 | 4 | 0 | 0 | 9 |
| batch_conserves | safety / never-changes | 39 | 13 | 7 | 12 | 13 | 13 | 12 | 0 | 7 | 19 |
| batch_first_invalid | rejection-and-unchanged | 39 | 10 | 9 | 10 | 10 | 10 | 10 | 0 | 9 | 19 |
| batch_count_bounded | bound | 39 | 13 | 6 | 11 | 13 | 13 | 12 | 0 | 7 | 19 |
| batch_stops_at_invalid | progress | 39 | 19 | 14 | 16 | 19 | 19 | 18 | 0 | 1 | 19 |
| transfer_valid_moves | exact-result | 39 | 10 | 10 | 8 | 10 | 10 | 9 | 0 | 2 | 27 |
| transfer_invalid_rejected | rejection-and-unchanged | 39 | 8 | 8 | 8 | 8 | 8 | 8 | 0 | 3 | 27 |
| total_is_sum | exact-result | 39 | 8 | 8 | 8 | 8 | 8 | 8 | 0 | 0 | 30 |
| total_overflow | rejection-and-unchanged | 39 | 6 | 5 | 5 | 6 | 6 | 6 | 0 | 2 | 30 |
| balance_of_account | exact-result | 39 | 5 | 5 | 5 | 5 | 5 | 5 | 0 | 1 | 32 |
| balance_no_account | rejection-and-unchanged | 39 | 5 | 4 | 3 | 5 | 5 | 5 | 0 | 1 | 32 |
| whole_conserves | safety / never-changes | 39 | 13 | 5 | 12 | 13 | 13 | 12 | 0 | 12 | 14 |
| whole_first_invalid | rejection-and-unchanged | 39 | 13 | 6 | 13 | 13 | 13 | 13 | 0 | 11 | 14 |
| whole_rejected_unchanged | safety / never-changes | 39 | 12 | 3 | 10 | 12 | 12 | 11 | 0 | 13 | 14 |
| batch_then_total | safety / never-changes | 39 | 21 | 14 | 20 | 21 | 21 | 20 | 0 | 7 | 11 |
| batch_then_total_overflow | safety / never-changes | 39 | 18 | 10 | 16 | 18 | 16 | 17 | 0 | 10 | 11 |
| two_batches_conserve | safety / never-changes | 39 | 14 | 6 | 13 | 14 | 13 | 13 | 1 | 6 | 19 |

Hand-written set:

| Rule | Kind | Viable mutants of its crate | Rule shown false by some arm | a | b plain | b edge | c | d | c timeout | d proof lost, not shown false | d still proved |
|---|---|---|---|---|---|---|---|---|---|---|---|
| transfer_conserves | exact-result | 18 | 3 | 3 | 2 | 3 | 3 | 3 | 0 | 0 | 15 |
| withdraw_too_much | rejection-and-unchanged | 18 | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 0 | 16 |
| deposit_overflow | rejection-and-unchanged | 18 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 15 |
| withdraw_covered | exact-result | 18 | 3 | 3 | 2 | 3 | 3 | 3 | 0 | 0 | 15 |
| deposit_with_room | exact-result | 18 | 3 | 2 | 1 | 2 | 3 | 3 | 0 | 1 | 14 |
| transfer_short | rejection-and-unchanged | 18 | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 0 | 16 |
| transfer_no_room | rejection-and-unchanged | 18 | 3 | 3 | 2 | 3 | 3 | 3 | 0 | 0 | 15 |
| batch_conserves | safety / never-changes | 27 | 6 | 3 | 5 | 5 | 5 | 6 | 0 | 9 | 12 |
| batch_first_invalid | rejection-and-unchanged | 27 | 5 | 5 | 5 | 5 | 5 | 5 | 0 | 10 | 12 |
| batch_count_bounded | bound | 27 | 2 | 0 | 2 | 2 | 2 | 2 | 0 | 13 | 12 |
| batch_stops_at_invalid | progress | 27 | 6 | 5 | 5 | 6 | 5 | 6 | 0 | 9 | 12 |
| transfer_valid_moves | exact-result | 27 | 4 | 3 | 2 | 3 | 4 | 4 | 0 | 2 | 21 |
| transfer_invalid_rejected | rejection-and-unchanged | 27 | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 4 | 21 |
| total_is_sum | exact-result | 27 | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 2 | 21 |
| total_overflow | rejection-and-unchanged | 27 | 6 | 6 | 6 | 6 | 6 | 6 | 0 | 0 | 21 |
| balance_of_account | exact-result | 27 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 25 |
| balance_no_account | rejection-and-unchanged | 27 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 25 |
| whole_conserves | safety / never-changes | 27 | 6 | 1 | 5 | 5 | 5 | 6 | 0 | 13 | 8 |
| whole_first_invalid | rejection-and-unchanged | 27 | 6 | 3 | 6 | 6 | 6 | 6 | 0 | 13 | 8 |
| whole_rejected_unchanged | safety / never-changes | 27 | 3 | 2 | 3 | 3 | 3 | 3 | 0 | 16 | 8 |
| batch_then_total | safety / never-changes | 27 | 10 | 6 | 9 | 9 | 8 | 10 | 0 | 11 | 6 |
| batch_then_total_overflow | safety / never-changes | 27 | 9 | 7 | 8 | 8 | 7 | 9 | 0 | 12 | 6 |
| two_batches_conserve | safety / never-changes | 27 | 7 | 2 | 6 | 6 | 6 | 7 | 0 | 8 | 12 |

## Appendix B. Cost per rule

| Rule | Kind | Gherkin statement lines | a: + rows lines (rows) | b: property lines | c: harness lines | d: proof lines | d: lemma lines it rests on (share) | b ms plain / edge | c seconds | d seconds to re-check the proof |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer_conserves | exact | 11 | 4 (2) | 17 | 13 | 6 | 0 | 14 / 41 | 0 | 5.62 |
| withdraw_too_much | rejection | 7 | 4 (2) | 12 | 10 | 4 | 0 | 10 / 27 | 0 | 5.34 |
| deposit_overflow | rejection | 7 | 4 (2) | 12 | 10 | 4 | 0 | 11 / 27 | 0 | 5.49 |
| withdraw_covered | exact | 7 | 5 (3) | 12 | 10 | 4 | 0 | 12 / 26 | 0 | 5.24 |
| deposit_with_room | exact | 7 | 5 (3) | 12 | 10 | 4 | 0 | 11 / 26 | 0 | 5.63 |
| transfer_short | rejection | 9 | 4 (2) | 15 | 11 | 4 | 0 | 11 / 32 | 0 | 5.21 |
| transfer_no_room | rejection | 10 | 4 (2) | 16 | 12 | 4 | 0 | 13 / 38 | 0 | 5.52 |
| batch_conserves | safety | 5 | 8 (6) | 10 | 11 | 3 | 153 (9.1) | 25 / 100 | 7 | 5.17 |
| batch_first_invalid | rejection | 7 | 5 (3) | 11 | 13 | 4 | 153 (9.1) | 31 / 157 | 6 | 5.44 |
| batch_count_bounded | bound | 5 | 5 (3) | 10 | 11 | 3 | 153 (9.1) | 25 / 114 | 4 | 5.31 |
| batch_stops_at_invalid | progress | 5 | 7 (5) | 12 | 13 | 3 | 153 (9.1) | 25 / 103 | 5 | 5.26 |
| transfer_valid_moves | exact | 8 | 5 (3) | 27 | 23 | 5 | 92 (5.0) | 28 / 56 | 9 | 5.3 |
| transfer_invalid_rejected | rejection | 7 | 7 (5) | 15 | 13 | 5 | 92 (5.0) | 27 / 71 | 3 | 5.42 |
| total_is_sum | exact | 6 | 7 (5) | 9 | 11 | 6 | 90 (10.9) | 14 / 55 | 1 | 5.2 |
| total_overflow | rejection | 6 | 5 (3) | 9 | 10 | 3 | 90 (10.9) | 13 / 39 | 1 | 5.35 |
| balance_of_account | exact | 6 | 4 (2) | 10 | 12 | 4 | 9 (4.5) | 16 / 34 | 1 | 5.42 |
| balance_no_account | rejection | 6 | 4 (2) | 13 | 11 | 4 | 9 (4.5) | 17 / 39 | 1 | 5.09 |
| whole_conserves | safety | 5 | 4 (2) | 10 | 11 | 3 | 187 (14.8) | 29 / 97 | 6 | 5.22 |
| whole_first_invalid | rejection | 7 | 3 (1) | 11 | 13 | 5 | 187 (14.8) | 38 / 141 | 4 | 5.47 |
| whole_rejected_unchanged | safety | 5 | 6 (4) | 10 | 11 | 3 | 187 (14.8) | 34 / 114 | 4 | 5.49 |
| batch_then_total | safety | 7 | 5 (3) | 11 | 13 | 10 | 184 (16.9) | 52 / 172 | 7 | 5.44 |
| batch_then_total_overflow | safety | 7 | 4 (2) | 11 | 12 | 7 | 184 (16.9) | 32 / 133 | 4 | 5.56 |
| two_batches_conserve | safety | 7 | 3 (1) | 13 | 14 | 5 | 153 (9.1) | 44 / 174 | 8 | 5.32 |

## Appendix C. Every mutant

Rules are listed by id. "Oracle" is the differential oracle (original against mutant on about 2.4
million inputs). Seconds are wall-clock under load.

Tool set (cargo-mutants 27.1.0, every mutant it lists):

| Mutant | Function | Change | Oracle | a. rows: rules with a failing row | literal scenarios failing (not rules) | b. plain: rules falsified | b. edge: rules falsified | c. Kani: rules failed | d: shown false by the pipeline's search | d: proof lost, confirmed false | d: proof lost, NOT shown false | seconds a / b plain / b edge / c / d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cm-w01 | Wallet::deposit | src/lib.rs:16:9: replace Wallet::deposit -> Result<(), WalletError> with Ok(()) | differs | deposit_overflow, deposit_with_room | - | deposit_overflow, deposit_with_room | deposit_overflow, deposit_with_room | deposit_overflow, deposit_with_room | deposit_overflow, deposit_with_room | - | - | 1 / 0.4 / 0.3 / 7 / 309 |
| cm-w02 | Wallet::withdraw | src/lib.rs:26:9: replace Wallet::withdraw -> Result<(), WalletError> with Ok(()) | differs | withdraw_covered, withdraw_too_much | - | withdraw_covered, withdraw_too_much | withdraw_covered, withdraw_too_much | withdraw_covered, withdraw_too_much | withdraw_covered, withdraw_too_much | - | - | 1 / 0.4 / 0.8 / 16 / 358 |
| cm-w03 | Wallet::withdraw | src/lib.rs:26:16: replace > with == in Wallet::withdraw | differs | withdraw_covered, withdraw_too_much | - | withdraw_too_much | withdraw_covered, withdraw_too_much | withdraw_covered, withdraw_too_much | withdraw_covered, withdraw_too_much | - | - | 2 / 0.5 / 0.3 / 16 / 358 |
| cm-w04 | Wallet::withdraw | src/lib.rs:26:16: replace > with < in Wallet::withdraw | differs | withdraw_covered, withdraw_too_much | - | withdraw_covered, withdraw_too_much | withdraw_covered, withdraw_too_much | withdraw_covered, withdraw_too_much | withdraw_covered, withdraw_too_much | - | - | 1 / 1.0 / 0.6 / 16 / 365 |
| cm-w05 | Wallet::withdraw | src/lib.rs:26:16: replace > with >= in Wallet::withdraw | differs | withdraw_covered | - | - | withdraw_covered | withdraw_covered | withdraw_covered | - | - | 1 / 0.3 / 0.2 / 3 / 61 |
| cm-w06 | Wallet::withdraw | src/lib.rs:29:22: replace -= with += in Wallet::withdraw | differs | withdraw_covered | - | withdraw_covered | withdraw_covered | withdraw_covered | withdraw_covered | - | - | 1 / 1.7 / 0.2 / 19 / 350 |
| cm-w07 | Wallet::withdraw | src/lib.rs:29:22: replace -= with /= in Wallet::withdraw | differs | withdraw_covered | - | withdraw_covered | withdraw_covered | withdraw_covered | withdraw_covered | - | - | 2 / 0.4 / 0.4 / 17 / 370 |
| cm-w08 | transfer | src/lib.rs:35:5: replace transfer -> Result<(), WalletError> with Ok(()) | differs | transfer_conserves, transfer_no_room, transfer_short | transfer_short_example | transfer_conserves, transfer_no_room, transfer_short | transfer_conserves, transfer_no_room, transfer_short | transfer_conserves, transfer_no_room, transfer_short | transfer_conserves, transfer_no_room, transfer_short | - | - | 2 / 0.4 / 4.3 / 16 / 360 |
| cm-w09 | transfer | src/lib.rs:35:20: replace < with == in transfer | differs | transfer_conserves, transfer_no_room, transfer_short | transfer_short_example | transfer_short | transfer_conserves, transfer_no_room, transfer_short | transfer_conserves, transfer_no_room, transfer_short | transfer_conserves, transfer_no_room, transfer_short | - | - | 1 / 0.6 / 6.9 / 17 / 355 |
| cm-w10 | transfer | src/lib.rs:35:20: replace < with > in transfer | differs | transfer_conserves, transfer_no_room, transfer_short | transfer_short_example | transfer_conserves, transfer_no_room, transfer_short | transfer_conserves, transfer_no_room, transfer_short | transfer_conserves, transfer_no_room, transfer_short | transfer_conserves, transfer_no_room, transfer_short | - | - | 3 / 0.9 / 7.6 / 16 / 286 |
| cm-w11 | transfer | src/lib.rs:35:20: replace < with <= in transfer | differs | transfer_conserves, transfer_no_room | - | - | transfer_conserves, transfer_no_room | transfer_conserves, transfer_no_room | transfer_conserves, transfer_no_room | - | - | 2 / 0.5 / 6.8 / 17 / 275 |
| cm-w12 | transfer | src/lib.rs:42:17: replace -= with += in transfer | differs | transfer_conserves | - | transfer_conserves | transfer_conserves | transfer_conserves | transfer_conserves | - | - | 2 / 0.4 / 4.0 / 14 / 288 |
| cm-w13 | transfer | src/lib.rs:42:17: replace -= with /= in transfer | differs | transfer_conserves | - | transfer_conserves | transfer_conserves | transfer_conserves | transfer_conserves | - | - | 1 / 0.7 / 0.5 / 37 / 275 |
| cm-l01 | Ledger::balance | src/lib.rs:19:9: replace Ledger::balance -> Option<u64> with None | differs | balance_of_account | - | balance_of_account | balance_of_account | balance_of_account | balance_of_account | - | balance_no_account | 2 / 0.9 / 3.7 / 598 / 309 |
| cm-l02 | Ledger::balance | src/lib.rs:19:9: replace Ledger::balance -> Option<u64> with Some(0) | differs | balance_no_account, balance_of_account | - | balance_no_account, balance_of_account | balance_no_account, balance_of_account | balance_no_account, balance_of_account | balance_no_account, balance_of_account | - | - | 1 / 1.2 / 5.3 / 628 / 316 |
| cm-l03 | Ledger::balance | src/lib.rs:19:9: replace Ledger::balance -> Option<u64> with Some(1) | differs | balance_no_account, balance_of_account | - | balance_no_account, balance_of_account | balance_no_account, balance_of_account | balance_no_account, balance_of_account | balance_no_account, balance_of_account | - | - | 1 / 1.1 / 5.0 / 608 / 311 |
| cm-l04 | Ledger::balance | src/lib.rs:19:14: replace < with == in Ledger::balance | differs | balance_no_account, balance_of_account | - | balance_of_account | balance_no_account, balance_of_account | balance_no_account, balance_of_account | balance_no_account, balance_of_account | - | - | 2 / 1.0 / 3.2 / 633 / 302 |
| cm-l05 | Ledger::balance | src/lib.rs:19:14: replace < with > in Ledger::balance | differs | balance_of_account | - | balance_no_account, balance_of_account | balance_no_account, balance_of_account | balance_no_account, balance_of_account | balance_no_account, balance_of_account | - | - | 1 / 1.1 / 3.6 / 632 / 299 |
| cm-l06 | Ledger::balance | src/lib.rs:19:14: replace < with <= in Ledger::balance | differs | balance_no_account | - | - | balance_no_account | balance_no_account | balance_no_account | - | balance_of_account | 2 / 1.2 / 5.8 / 640 / 241 |
| cm-l07 | Ledger::total | src/lib.rs:28:9: replace Ledger::total -> Option<u64> with None | differs | batch_then_total, total_is_sum | - | batch_then_total, total_is_sum | batch_then_total, total_is_sum | batch_then_total, total_is_sum | batch_then_total, total_is_sum | - | batch_then_total_overflow, total_overflow | 1 / 0.9 / 3.2 / 552 / 256 |
| cm-l08 | Ledger::total | src/lib.rs:28:9: replace Ledger::total -> Option<u64> with Some(0) | differs | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | - | 1 / 0.7 / 2.7 / 537 / 255 |
| cm-l09 | Ledger::total | src/lib.rs:28:9: replace Ledger::total -> Option<u64> with Some(1) | differs | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | - | 1 / 2.7 / 6.2 / 542 / 259 |
| cm-l10 | Ledger::total | src/lib.rs:30:17: replace < with == in Ledger::total | differs | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | - | 1 / 1.0 / 2.7 / 395 / 201 |
| cm-l11 | Ledger::total | src/lib.rs:30:17: replace < with > in Ledger::total | differs | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | - | 1 / 1.0 / 2.6 / 393 / 199 |
| cm-l12 | Ledger::total | src/lib.rs:30:17: replace < with <= in Ledger::total | differs | batch_then_total, total_is_sum | - | batch_then_total, total_is_sum | batch_then_total, total_is_sum | batch_then_total, total_is_sum | batch_then_total, total_is_sum | - | batch_then_total_overflow, total_overflow | 1 / 1.0 / 2.5 / 415 / 196 |
| cm-l13 | Ledger::total | src/lib.rs:35:15: replace += with -= in Ledger::total | differs | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | - | 1 / 1.2 / 3.7 / 398 / 196 |
| cm-l14 | Ledger::total | src/lib.rs:35:15: replace += with *= in Ledger::total | differs | batch_then_total, total_is_sum | - | batch_then_total, total_is_sum | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - [the pipeline crashed evaluating the model; proofs had been checked] | 300 / 240.7 / 481.6 / 242 / 153 |
| cm-l15 | Ledger::apply | src/lib.rs:44:9: replace Ledger::apply -> bool with true | differs | batch_first_invalid, transfer_invalid_rejected, transfer_valid_moves, whole_first_invalid | batch_example_all, batch_example_stop, whole_example_accept, whole_example_rollback_late, whole_example_rollback | batch_first_invalid, transfer_invalid_rejected, transfer_valid_moves, whole_first_invalid | batch_first_invalid, transfer_invalid_rejected, transfer_valid_moves, whole_first_invalid | batch_first_invalid, transfer_invalid_rejected, transfer_valid_moves, whole_first_invalid | batch_first_invalid, transfer_invalid_rejected, transfer_valid_moves, whole_first_invalid | - | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | 1 / 0.6 / 2.1 / 179 / 155 |
| cm-l16 | Ledger::apply | src/lib.rs:44:9: replace Ledger::apply -> bool with false | differs | batch_stops_at_invalid, transfer_valid_moves | batch_example_all, batch_example_stop, whole_example_accept | batch_stops_at_invalid, transfer_valid_moves | batch_stops_at_invalid, transfer_valid_moves | batch_stops_at_invalid, transfer_valid_moves | batch_stops_at_invalid, transfer_valid_moves | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 2.9 / 2.9 / 162 / 208 |
| cm-l17 | Ledger::apply | src/lib.rs:45:37: replace \|\| with && in Ledger::apply | differs | batch_first_invalid, transfer_invalid_rejected | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | - | transfer_valid_moves | 1 / 26.1 / 3.0 / 318 / 126 |
| cm-l18 | Ledger::apply | src/lib.rs:45:24: replace \|\| with && in Ledger::apply | differs | batch_first_invalid, transfer_invalid_rejected | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | - | transfer_valid_moves | 1 / 3.7 / 5.2 / 375 / 93 |
| cm-l19 | Ledger::apply | src/lib.rs:45:19: replace >= with < in Ledger::apply | differs | batch_stops_at_invalid, transfer_invalid_rejected, transfer_valid_moves | batch_example_all, batch_example_stop, whole_example_accept | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_then_total_overflow | - | 1 / 1.5 / 3.0 / 107 / 99 |
| cm-l20 | Ledger::apply | src/lib.rs:45:32: replace >= with < in Ledger::apply | differs | batch_first_invalid, batch_stops_at_invalid, transfer_invalid_rejected, transfer_valid_moves | batch_example_all, batch_example_stop, whole_example_accept | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | - | - | 1 / 13.0 / 1.0 / 100 / 108 |
| cm-l21 | Ledger::apply | src/lib.rs:45:47: replace == with != in Ledger::apply | differs | batch_first_invalid, batch_stops_at_invalid, transfer_invalid_rejected, transfer_valid_moves | batch_example_all, batch_example_stop, whole_example_accept | batch_conserves, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid | batch_conserves, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid | batch_conserves, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid | batch_conserves, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid | - | batch_count_bounded, batch_then_total_overflow, whole_rejected_unchanged | 0 / 8.4 / 1.4 / 104 / 111 |
| cm-l22 | Ledger::apply | src/lib.rs:49:14: replace < with == in Ledger::apply | differs | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_example_all, batch_example_stop, whole_example_accept, whole_example_rollback | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_then_total_overflow | - | 1 / 2.1 / 3.7 / 177 / 116 |
| cm-l23 | Ledger::apply | src/lib.rs:49:14: replace < with > in Ledger::apply | differs | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_first_invalid | batch_example_all, batch_example_stop, whole_example_accept | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, transfer_invalid_rejected, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_then_total_overflow | - | 1 / 2.0 / 4.5 / 173 / 145 |
| cm-l24 | Ledger::apply | src/lib.rs:49:14: replace < with <= in Ledger::apply | differs | batch_stops_at_invalid, transfer_valid_moves | batch_example_all, whole_example_accept | - | batch_stops_at_invalid, transfer_valid_moves | batch_stops_at_invalid, transfer_valid_moves | batch_stops_at_invalid, transfer_valid_moves | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 0.7 / 3.4 / 219 / 111 |
| cm-l25 | Ledger::apply | src/lib.rs:56:35: replace - with + in Ledger::apply | differs | batch_conserves, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_example_all, batch_example_stop, whole_example_accept | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_rejected_unchanged | - | batch_first_invalid, transfer_invalid_rejected, whole_first_invalid | 1 / 11.8 / 15.8 / 115 / 110 |
| cm-l26 | Ledger::apply | src/lib.rs:56:35: replace - with / in Ledger::apply | differs | batch_conserves, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_example_all, batch_example_stop, whole_example_accept | batch_conserves, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves, whole_rejected_unchanged | - | - | NO MODEL: the generated Lean does not build, so no rule gets a verdict | 0 / 4.0 / 1.5 / 179 / 20 |
| cm-l27 | Ledger::apply_batch | src/lib.rs:64:9: replace Ledger::apply_batch -> usize with 0 | differs | batch_stops_at_invalid | batch_example_all, batch_example_stop, whole_example_accept | batch_stops_at_invalid | batch_stops_at_invalid | batch_stops_at_invalid | batch_stops_at_invalid | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | 0 / 1.0 / 1.1 / 86 / 106 |
| cm-l28 | Ledger::apply_batch | src/lib.rs:64:9: replace Ledger::apply_batch -> usize with 1 | differs | batch_count_bounded, batch_first_invalid, batch_stops_at_invalid | batch_example_all, batch_example_stop, whole_example_accept | batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, two_batches_conserve, whole_first_invalid | batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, two_batches_conserve, whole_first_invalid | batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, two_batches_conserve, whole_first_invalid | batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, two_batches_conserve, whole_first_invalid | - | batch_conserves, batch_then_total, batch_then_total_overflow, whole_conserves, whole_rejected_unchanged | 0 / 1.2 / 0.8 / 107 / 99 |
| cm-l29 | Ledger::apply_batch | src/lib.rs:65:17: replace < with == in Ledger::apply_batch | differs | batch_conserves, batch_count_bounded, batch_stops_at_invalid | batch_example_all, batch_example_stop, whole_example_accept | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | - | batch_first_invalid, whole_first_invalid | 1 / 0.4 / 0.6 / 138 / 117 |
| cm-l30 | Ledger::apply_batch | src/lib.rs:65:17: replace < with > in Ledger::apply_batch | differs | batch_stops_at_invalid | batch_example_all, batch_example_stop, whole_example_accept | batch_stops_at_invalid | batch_stops_at_invalid | batch_stops_at_invalid | batch_stops_at_invalid | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 1.6 / 1.8 / 106 / 133 |
| cm-l31 | Ledger::apply_batch | src/lib.rs:65:17: replace < with <= in Ledger::apply_batch | differs | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_example_all, whole_example_accept | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | - | batch_first_invalid, whole_first_invalid | 1 / 0.4 / 0.6 / 177 / 151 |
| cm-l32 | Ledger::apply_batch | src/lib.rs:66:16: delete ! in Ledger::apply_batch | differs | batch_first_invalid, batch_stops_at_invalid | batch_example_all, batch_example_stop, whole_example_accept | batch_first_invalid, batch_stops_at_invalid, whole_first_invalid | batch_first_invalid, batch_stops_at_invalid, whole_first_invalid | batch_first_invalid, batch_stops_at_invalid, whole_first_invalid | batch_first_invalid, batch_stops_at_invalid, whole_first_invalid | - | batch_conserves, batch_count_bounded, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | 1 / 1.9 / 1.3 / 243 / 141 |
| cm-l33 | Ledger::apply_batch | src/lib.rs:69:15: replace += with -= in Ledger::apply_batch | differs | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_example_all, batch_example_stop, whole_example_accept, whole_example_rollback_late, whole_example_rollback | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | - | batch_first_invalid, whole_first_invalid | 1 / 11.0 / 2.7 / 130 / 152 |
| cm-l34 | Ledger::apply_batch | src/lib.rs:69:15: replace += with *= in Ledger::apply_batch | differs | batch_then_total_overflow | batch_example_all, batch_example_stop, whole_example_accept | - | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, whole_conserves, whole_rejected_unchanged; TIMEOUT: two_batches_conserve | - | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | batch_first_invalid, whole_first_invalid [the pipeline crashed evaluating the model; proofs had been checked] | 300 / 0.7 / 960.6 / 716 / 70 |
| cm-l35 | Ledger::apply_all | src/lib.rs:77:9: replace Ledger::apply_all -> bool with true | differs | whole_first_invalid | whole_example_accept, whole_example_rollback_late, whole_example_rollback | whole_first_invalid | whole_first_invalid | whole_first_invalid | whole_first_invalid | - | whole_conserves, whole_rejected_unchanged | 1 / 0.7 / 1.7 / 186 / 179 |
| cm-l36 | Ledger::apply_all | src/lib.rs:77:9: replace Ledger::apply_all -> bool with false | differs | - | whole_example_accept | - | - | - | - | - | whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 0.7 / 1.5 / 196 / 209 |
| cm-l37 | Ledger::apply_all | src/lib.rs:79:20: replace < with == in Ledger::apply_all | differs | whole_first_invalid | whole_example_accept, whole_example_rollback_late, whole_example_rollback | whole_first_invalid | whole_first_invalid | whole_first_invalid | whole_first_invalid | - | whole_conserves, whole_rejected_unchanged | 1 / 0.7 / 1.4 / 310 / 168 |
| cm-l38 | Ledger::apply_all | src/lib.rs:79:20: replace < with > in Ledger::apply_all | differs | whole_first_invalid | whole_example_rollback_late, whole_example_rollback | whole_first_invalid | whole_first_invalid | whole_first_invalid | whole_first_invalid | - | whole_conserves, whole_rejected_unchanged | 1 / 0.7 / 1.8 / 311 / 156 |
| cm-l39 | Ledger::apply_all | src/lib.rs:79:20: replace < with <= in Ledger::apply_all | differs | - | whole_example_accept | - | - | - | - | - | whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 0.7 / 2.1 / 298 / 162 |

Hand-written set (`slice/mutation/run_mutants.py`; `hand-r*` are the reviewer's):

| Mutant | Function | Change | Oracle | a. rows: rules with a failing row | literal scenarios failing (not rules) | b. plain: rules falsified | b. edge: rules falsified | c. Kani: rules failed | d: shown false by the pipeline's search | d: proof lost, confirmed false | d: proof lost, NOT shown false | seconds a / b plain / b edge / c / d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hand-d1 | deposit | no overflow check: the balance wraps around | differs | deposit_overflow | - | deposit_overflow | deposit_overflow | deposit_overflow | deposit_overflow | - | deposit_with_room | 1 / 0.5 / 0.2 / 10 / 179 |
| hand-d2 | deposit | a successful deposit sets the balance to the amount instead of adding it | differs | deposit_with_room | - | deposit_with_room | deposit_with_room | deposit_with_room | deposit_with_room | - | - | 2 / 1.6 / 0.2 / 5 / 152 |
| hand-d3 | deposit | overflow is reported as insufficient funds | differs | deposit_overflow | - | deposit_overflow | deposit_overflow | deposit_overflow | deposit_overflow | - | - | 1 / 0.3 / 0.3 / 9 / 202 |
| hand-d4 | deposit | a deposit that reaches exactly the maximum is rejected | differs | deposit_with_room | - | - | deposit_with_room | deposit_with_room | deposit_with_room | - | - | 2 / 1.9 / 0.2 / 5 / 153 |
| hand-d5 | deposit | a rejected deposit empties the wallet | differs | deposit_overflow | - | deposit_overflow | deposit_overflow | deposit_overflow | deposit_overflow | - | - | 1 / 0.4 / 0.2 / 5 / 176 |
| hand-d6 | deposit | a deposit of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses) | differs | - | - | - | - | deposit_with_room | - | deposit_with_room | - | 1 / 0.3 / 0.2 / 7 / 170 |
| hand-w1 | withdraw | withdrawing the whole balance is rejected (> became >=) | differs | withdraw_covered | - | - | withdraw_covered | withdraw_covered | withdraw_covered | - | - | 1 / 0.4 / 0.2 / 5 / 164 |
| hand-w2 | withdraw | a successful withdrawal does not take the money | differs | withdraw_covered | - | withdraw_covered | withdraw_covered | withdraw_covered | withdraw_covered | - | - | 1 / 0.3 / 0.2 / 5 / 144 |
| hand-w3 | withdraw | insufficient funds is reported as overflow | differs | withdraw_too_much | - | withdraw_too_much | withdraw_too_much | withdraw_too_much | withdraw_too_much | - | - | 1 / 0.3 / 0.2 / 6 / 145 |
| hand-w4 | withdraw | a rejected withdrawal empties the wallet | differs | withdraw_too_much | - | withdraw_too_much | withdraw_too_much | withdraw_too_much | withdraw_too_much | - | - | 1 / 0.3 / 0.2 / 5 / 118 |
| hand-w5 | withdraw | a successful withdrawal takes one unit too many when it can | differs | withdraw_covered | - | withdraw_covered | withdraw_covered | withdraw_covered | withdraw_covered | - | - | 3 / 1.0 / 0.2 / 5 / 145 |
| hand-t1 | transfer | transferring the whole balance is rejected (< became <=) | differs | transfer_conserves, transfer_no_room | - | - | transfer_conserves, transfer_no_room | transfer_conserves, transfer_no_room | transfer_conserves, transfer_no_room | - | - | 1 / 0.4 / 2.2 / 9 / 144 |
| hand-t2 | transfer | the sender is debited before the receiver's overflow check, so a rejected transfer loses money | differs | transfer_no_room | - | transfer_no_room | transfer_no_room | transfer_no_room | transfer_no_room | - | - | 2 / 1.6 / 0.2 / 5 / 134 |
| hand-t3 | transfer | the receiver is never credited (money vanishes) | differs | transfer_conserves | - | transfer_conserves | transfer_conserves | transfer_conserves | transfer_conserves | - | - | 1 / 0.3 / 1.6 / 6 / 123 |
| hand-t4 | transfer | the sender is never debited (money is created) | differs | transfer_conserves | - | transfer_conserves | transfer_conserves | transfer_conserves | transfer_conserves | - | - | 1 / 0.4 / 1.6 / 7 / 131 |
| hand-t5 | transfer | receiver overflow is reported as insufficient funds | differs | transfer_no_room | - | transfer_no_room | transfer_no_room | transfer_no_room | transfer_no_room | - | - | 1 / 0.3 / 0.2 / 5 / 110 |
| hand-t6 | transfer | insufficient funds is reported as overflow | differs | transfer_short | transfer_short_example | transfer_short | transfer_short | transfer_short | transfer_short | - | - | 1 / 0.3 / 0.2 / 6 / 116 |
| hand-t7 | transfer | no funds check at all (the subtraction panics instead) | differs | transfer_short | transfer_short_example | transfer_short | transfer_short | transfer_short | transfer_short | - | - | 1 / 0.5 / 0.3 / 7 / 115 |
| hand-lt1 | total | LOOP off-by-one bound: the last balance is not added | differs | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | - | 1 / 0.7 / 2.0 / 215 / 145 |
| hand-lt2 | total | LOOP wrong accumulator: the sum is overwritten by each balance instead of accumulated | differs | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | - | 1 / 3.8 / 1.9 / 222 / 134 |
| hand-lt3 | total | LOOP skipped element: summing starts at account 1 | differs | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | - | 1 / 0.6 / 1.2 / 222 / 148 |
| hand-lt4 | total | an overflowing total is reported as u64::MAX instead of absent | differs | batch_then_total_overflow, total_overflow | - | batch_then_total_overflow, total_overflow | batch_then_total_overflow, total_overflow | batch_then_total_overflow, total_overflow | batch_then_total_overflow, total_overflow | - | batch_then_total, total_is_sum | 1 / 2.1 / 1.5 / 233 / 136 |
| hand-lt5 | total | LOOP wrong accumulator: wrapping addition, so an overflowing total wraps around | differs | batch_then_total_overflow, total_overflow | - | batch_then_total_overflow, total_overflow | batch_then_total_overflow, total_overflow | batch_then_total_overflow, total_overflow | batch_then_total_overflow, total_overflow | - | batch_then_total, total_is_sum | 1 / 0.7 / 1.8 / 222 / 141 |
| hand-la1 | apply | no check that sender and receiver differ: a self-transfer creates money | differs | batch_first_invalid, transfer_invalid_rejected | - | batch_conserves, batch_first_invalid, batch_then_total, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid | batch_conserves, batch_first_invalid, batch_then_total, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid | batch_conserves, batch_first_invalid, batch_then_total, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid | batch_conserves, batch_first_invalid, batch_then_total, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid | - | batch_count_bounded, batch_stops_at_invalid, batch_then_total_overflow, transfer_valid_moves, whole_rejected_unchanged | 1 / 8.8 / 1.9 / 184 / 113 |
| hand-la2 | apply | transferring the sender's whole balance is rejected (< became <=) | differs | batch_stops_at_invalid, transfer_valid_moves | batch_example_all, whole_example_accept | - | batch_stops_at_invalid, transfer_valid_moves | batch_stops_at_invalid, transfer_valid_moves | batch_stops_at_invalid, transfer_valid_moves | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 1.4 / 1.7 / 245 / 140 |
| hand-la3 | apply | the receiver is never credited (money vanishes) | differs | batch_conserves, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve | batch_example_all, batch_example_stop, whole_example_accept | batch_conserves, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_conserves, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_conserves, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_conserves, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves | - | batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, transfer_invalid_rejected, whole_first_invalid, whole_rejected_unchanged | 2 / 8.0 / 3.4 / 161 / 97 |
| hand-la4 | apply | the sender is never debited (money is created) | differs | batch_conserves, batch_then_total, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_example_all, batch_example_stop, whole_example_accept | batch_conserves, batch_then_total, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_conserves, batch_then_total, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_conserves, batch_then_total, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_conserves, batch_then_total, transfer_valid_moves, two_batches_conserve, whole_conserves | - | batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total_overflow, transfer_invalid_rejected, whole_first_invalid, whole_rejected_unchanged | 1 / 6.3 / 3.5 / 142 / 107 |
| hand-la5 | apply | receiver bounds check off by one (>= became >): indexing one past the end panics | differs | batch_first_invalid, transfer_invalid_rejected | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, transfer_invalid_rejected, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | - | transfer_valid_moves | 1 / 12.2 / 1.5 / 255 / 126 |
| hand-la6 | apply | a transfer of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses) | differs | - | - | - | - | batch_conserves, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves | - | batch_conserves, batch_then_total, batch_then_total_overflow, transfer_valid_moves, two_batches_conserve, whole_conserves | batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, transfer_invalid_rejected, whole_first_invalid, whole_rejected_unchanged | 1 / 1.1 / 5.5 / 418 / 189 |
| hand-lb1 | apply_batch | LOOP missing early exit: the batch carries on after a rejected transfer and counts it | differs | batch_first_invalid, whole_first_invalid | batch_example_stop, whole_example_rollback_late, whole_example_rollback | batch_first_invalid, whole_first_invalid | batch_first_invalid, whole_first_invalid | batch_first_invalid, whole_first_invalid | batch_first_invalid, whole_first_invalid | - | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | 1 / 0.7 / 1.3 / 261 / 103 |
| hand-lb2 | apply_batch | LOOP off-by-one bound: the last transfer of the batch is never applied | differs | batch_stops_at_invalid | batch_example_all, whole_example_accept | batch_stops_at_invalid | batch_stops_at_invalid | batch_stops_at_invalid | batch_stops_at_invalid | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 2.0 / 1.9 / 161 / 132 |
| hand-lb3 | apply_batch | LOOP skipped element: every second transfer is skipped (i += 2) | differs | - | batch_example_all, batch_example_stop, whole_example_accept, whole_example_rollback | batch_count_bounded, two_batches_conserve | batch_count_bounded, two_batches_conserve | batch_count_bounded, two_batches_conserve | batch_count_bounded, two_batches_conserve | - | batch_conserves, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 4.6 / 2.3 / 192 / 108 |
| hand-lb4 | apply_batch | LOOP wrong result: the batch length is returned instead of the number applied | differs | batch_first_invalid, whole_first_invalid | batch_example_stop, whole_example_rollback_late, whole_example_rollback | batch_first_invalid, whole_first_invalid | batch_first_invalid, whole_first_invalid | batch_first_invalid, whole_first_invalid | batch_first_invalid, whole_first_invalid | - | batch_conserves, batch_count_bounded, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | 1 / 0.6 / 1.3 / 212 / 109 |
| hand-lb5 | apply_batch | LOOP wrong counter: a rejected transfer is counted as applied | differs | batch_first_invalid, batch_stops_at_invalid | batch_example_stop, whole_example_rollback_late, whole_example_rollback | batch_first_invalid, batch_stops_at_invalid, whole_first_invalid | batch_first_invalid, batch_stops_at_invalid, whole_first_invalid | batch_first_invalid, batch_stops_at_invalid, whole_first_invalid | batch_first_invalid, batch_stops_at_invalid, whole_first_invalid | - | batch_conserves, batch_count_bounded, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_rejected_unchanged | 1 / 1.9 / 1.4 / 233 / 153 |
| hand-lb6 | apply_batch | LOOP wrong early exit: the batch stops after the first APPLIED transfer | differs | batch_stops_at_invalid | batch_example_all, whole_example_accept | batch_stops_at_invalid | batch_stops_at_invalid | batch_stops_at_invalid | batch_stops_at_invalid | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 2.0 / 5.1 / 137 / 154 |
| hand-lw1 | apply_all | no rollback: a rejected batch keeps the transfers applied before the failure | differs | whole_rejected_unchanged | whole_example_rollback_late, whole_example_rollback | whole_rejected_unchanged | whole_rejected_unchanged | whole_rejected_unchanged | whole_rejected_unchanged | - | whole_conserves, whole_first_invalid | 1 / 1.9 / 1.9 / 223 / 122 |
| hand-lw2 | apply_all | a rolled-back batch is reported as applied | differs | whole_first_invalid | whole_example_rollback_late, whole_example_rollback | whole_first_invalid | whole_first_invalid | whole_first_invalid | whole_first_invalid | - | whole_conserves, whole_rejected_unchanged | 1 / 0.6 / 1.4 / 264 / 120 |
| hand-lw3 | apply_all | every batch is rolled back and rejected (< became <=) | differs | - | whole_example_accept | - | - | - | - | - | whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 0.7 / 1.7 / 247 / 132 |
| hand-lg1 | balance | lookup bounds check off by one (< became <=): looking up account `len` panics | differs | balance_no_account | - | - | balance_no_account | balance_no_account | balance_no_account | - | balance_of_account | 1 / 0.7 / 1.5 / 253 / 142 |
| hand-lg2 | balance | lookup returns the balance of account 0 whatever the account | differs | balance_of_account | - | balance_of_account | balance_of_account | balance_of_account | balance_of_account | - | balance_no_account | 1 / 0.7 / 1.6 / 222 / 170 |
| hand-r1 | apply_batch | REVIEW LOOP cap: the batch silently stops after three transfers | differs | batch_stops_at_invalid | - | batch_stops_at_invalid | batch_stops_at_invalid | - | batch_stops_at_invalid | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 2.1 / 11.0 / 202 / 177 |
| hand-r2 | total | REVIEW LOOP cap: only the first three accounts are summed | differs | batch_then_total_overflow, total_is_sum, total_overflow | - | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | total_is_sum, total_overflow | batch_then_total, batch_then_total_overflow, total_is_sum, total_overflow | - | - | 1 / 0.8 / 2.4 / 261 / 117 |
| hand-r3 | apply_all | REVIEW atomicity: no rollback once two or more transfers have been applied | differs | whole_rejected_unchanged | whole_example_rollback_late | whole_rejected_unchanged | whole_rejected_unchanged | whole_rejected_unchanged | whole_rejected_unchanged | - | whole_conserves, whole_first_invalid | 1 / 2.3 / 7.7 / 235 / 92 |
| hand-r4 | apply_batch | REVIEW LOOP wrong counter: a rejected LAST transfer (not the first) is counted as applied | differs | - | whole_example_rollback_late, whole_example_rollback | - | - | - | - | - | batch_conserves, batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total, batch_then_total_overflow, two_batches_conserve, whole_conserves, whole_first_invalid, whole_rejected_unchanged | 1 / 0.7 / 1.8 / 276 / 95 |
| hand-r5 | apply_batch | REVIEW LOOP state corruption: one unit is minted to account 0 at the start of the third iteration (conservation is false, but only for batches whose first two transfers apply and that have a third) | differs | batch_conserves, batch_then_total | - | batch_conserves, batch_then_total, two_batches_conserve, whole_conserves | batch_conserves, batch_then_total, two_batches_conserve, whole_conserves | - | batch_conserves, batch_then_total, two_batches_conserve, whole_conserves | - | batch_count_bounded, batch_first_invalid, batch_stops_at_invalid, batch_then_total_overflow, whole_first_invalid, whole_rejected_unchanged | 1 / 5.8 / 6.8 / 273 / 105 |
