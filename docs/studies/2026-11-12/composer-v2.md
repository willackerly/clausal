# Clausal compose, version 2: failure classification, design and plan nodes

Read-only study: nothing was run against the 48, nothing built, and no file in the repository was touched. All counts come from `clausal/compose_tests/l4b/results.json` and `REPORT.md`, joined by key with `trials/sentences/results.json`.

## 0. Findings first

1. **No threshold separates right from wrong in the frozen run.** Top-candidate scores are 3 to 19 for the 5 TOP-RIGHT, 8 to 39 for the 20 wrong and -3 to 22 for the 18 unscorable. The share of content words left unaccounted is 0.18 to 0.70 for the right ones and 0.08 to 0.57 for the wrong ones. The "abstain below a score or share" proposal in `clausal/COMPOSE.md` would therefore not have worked on this data.
2. **0 of the 144 top-three candidates accounts for every content word of its sentence.** A strict "no dropped word" rule turns every v1 answer into a question or a decline, so coverage accounting needs an acknowledgement path as well as a block.
3. **None of the 20 wrong readings has a missing piece as its primary cause.** All 20 have an expert rewording, so they are composer failures: 7 scope, 6 wrong frame, 4 wrong operation, 3 dropped condition.
4. **For 3 of the 20 the right sentence was outside v1's search space.** The expert rewording joins clauses with ", and" (`opus-1/r6`, `opus-1/r8`, `haiku-1/R07`), which v1 does not generate.
5. **All 18 unscorable are sentences the book could not say at measurement time, and v1 answered each.** L2 makes 4 of them cleanly expressible, 2 with caveats and 2 in part; 10 remain outside the book. `tied` with `same_input` serves none of the five tied-sequence rules on its own.
6. **Not removed by any merged change:** the wrong system for a bare "transfer", multi-clause sentences, either/or, conjunction of conditions, and argument order.
7. **This study is itself contamination.** The design below is derived from reading the failures on the 48, so the 48 can only be a development set from here on.

## 1. The 20 wrong readings by cause

The primary cause is the first defect that makes the top candidate wrong; this is my judgement from reading, not a measurement.

| Key | Primary | Contributing | What happened |
|---|---|---|---|
| `opus-1/r1` | wrong operation | scope | Wallet transfer for a ledger rule; "whether accepted or rejected" became "A rejected … and is never accepted" |
| `sonnet-1/R4` | wrong operation | dropped condition | Wallet; two of four conditions kept, arguments reversed |
| `haiku-1/R01` | wrong operation | scope | Wallet; "accepted" became the claim "is never accepted" |
| `haiku-1/R08` | wrong operation | scope | `l.apply_batch` anchored, not `l.apply_all`; invented condition "total … is the maximum" |
| `opus-1/r4` | wrong frame | scope | "rejected when amount is larger" became the two-call variation "gives the same answer when the amount is larger" |
| `opus-1/r6` | wrong frame | dropped clause | "no larger than the number of transfers" became "is zero"; second clause gone |
| `opus-1/r7` | wrong frame | no either/or form | One arm taken: "never changes the ledger" |
| `haiku-1/R02` | wrong frame | dropped "every" | "decreases the sender's balance by exactly zero" for "never changes the ledger" |
| `default-1/R03` | wrong frame | scope | "goes down / goes up" unmapped; "When" became an invented "for which" condition |
| `default-1/R07` | wrong frame | near-miss word | Spurious "not"; candidate 2 without it is still wrong ("valid on the ledger" is not "would apply in order") |
| `opus-1/r8` | scope | one-clause limit | Condition of clause 1 attached to the claim of clause 2 |
| `haiku-1/R07` | scope | one-clause limit | Same as `opus-1/r8` |
| `sonnet-1/R6` | scope | wrong frame | "first rejected transfer" became "a rejected batch", an empty scope; all five cases silent |
| `sonnet-1/R7` | scope | if/otherwise | "A successful batch … is rejected and changes nothing" |
| `haiku-1/R05` | scope | either/or | Condition of one arm on the claim of the other |
| `haiku-1/R09` | scope | none | "accepted" read as the claim "and it is accepted" |
| `haiku-1/R10` | scope | missing piece (second half) | "A rejected transfer is accepted exactly when …" |
| `sonnet-1/R8` | dropped condition | missing domain word | "when every transfer is acceptable in sequence" dropped; the candidate says more and is true of the code |
| `haiku-1/R12` | dropped condition | wrong frame | "balance of exactly zero" dropped; "no result" became "the result is the balance" |
| `default-1/R09` | dropped condition | wrong party | One of four conjuncts kept, on the sender instead of the receiver |

**Scoring artefacts sit in the "right" ten, not the wrong twenty.**
- `clausal/COMPOSE.md` already records that five of the ten agreeing candidates do not say what the author wrote (`sonnet-1/R3`, `default-1/R02`, `default-1/R06`, `opus-1/r2`, `sonnet-1/R9`).
- `opus-1/r2` (TOP-RIGHT) and `haiku-1/R09` (wrong) have the same defect, "and it is accepted"; they differ only in whether a case happened to expose it.
- `sonnet-1/R8` is the one wrong reading that is arguably a scorer strictness effect ("says more").

## 2. The 18 unscorable by cause

All 18 are "sentence outside the book" at the time of the run. Their cases are unencoded because the trial runner found no rewording, which makes NOT-SCORABLE a scoring artefact layered on a real failure to decline.

| Missing piece (from `trials/sentences/results.json`) | Keys | After L2 (`clausal/clausebook/l2/README.md`) |
|---|---|---|
| Comparison of two values before the call | `opus-1/r3`, `haiku-1/R03`, `default-1/R04`, `default-1/R10` | Expressible with `equals`; two are near-verbatim fixture rules (`l2_same_account_rejected`, `l2_zero_amount_rejected`) |
| Same, plus conjunction of conditions | `sonnet-1/R10` | Still missing (conjunction not built) |
| "Every balance" in a claim | `sonnet-1/R5`, `default-1/R05` | Expressible with `each_at_most`, with caveats: R5 needs two operations; R05's premise cannot be a condition |
| Same, plus invariant over any sequence | `opus-1/r5`, `haiku-1/R04` | In part only: per-operation claim yes, invariant frame not built |
| Tied sequence, same input | `opus-1/r9`, `sonnet-1/R11` | Still missing: r9 needs "when both succeed", refused as NARROWED-TIE; R11 needs a comparison of two calls' answers |
| Tied sequence, reverse or other order | `opus-1/r12`, `sonnet-1/R12`, `default-1/R12` | Still missing: no `reverse` tie, no comparison of two sequences |
| Condition on another operation's answer | `opus-1/r10` | Still missing |
| Further reference function | `haiku-1/R11` | Still missing |
| Further measure of the state | `default-1/R08` | Still missing |
| Answer class other than accepted or rejected | `default-1/R11` | Still missing |

Wrong anchoring also shows in what v1 printed for these: `haiku-1/R04` anchored "a batch applied as a whole" from the words "whole number", and `opus-1/r5` anchored a lookup for "any sequence of operations".

## 3. What the merged book changes would already remove

These are projections from reading; the frozen composer was not re-run on the new book.

| Change | Removes | Does not remove, or adds |
|---|---|---|
| Q4 row 2: "is never accepted" retired | The spurious conjunct in `opus-1/r1`, `haiku-1/R01`, `default-1/R01` | Its replacement "is always rejected" carries "always" and now ranks beside "is always accepted" (`clausal/COMPOSE.md`, post-merge note) |
| Q4 row 1: "accepted" is the live narrowing word | The author's "an accepted transfer" matches the subject form (`haiku-1/R01`, `haiku-1/R09`, `default-1/R01`, `default-1/R03`) | "it is accepted" as a claim still matches the same token |
| Q4 row 3: "it is accepted" shared across systems | Bare "For a transfer, it is accepted" becomes AMBIGUOUS and is not offered | Whether "it is rejected" (the two artefactual RIGHT-IN-TOP-3) is affected was not checked |
| Q1: vacuous narrowed rules refused | "A rejected transfer always answers" (`haiku-1/R03`, `default-1/R10`). Probably every "rejected batch" candidate (`sonnet-1/R6`, `default-1/R11`, `default-1/R08`), since `clausal/clausebook/local/ledger.yaml:36-37` declares `rejected: { no_call: true }` for the batch | Self-defeating but non-vacuous candidates (`sonnet-1/R7`, `haiku-1/R10`) |
| L2 `equals`, `each_at_most` | Makes 4 + 2 of the 18 expressible | No cue was written for them; trivial conditions now appear ("the sender … equals the sender …") |
| L2 `tied` | Nothing on the 48 by itself | — |
| None | — | Wrong system for a bare "transfer" (4 of 20 wrong; an open owner decision in `clausal/clausebook/q4/README.md`), multi-clause (3 unreachable), either/or (3), conjunction of conditions (3), argument order |

## 4. Version 2

### 4.1 Declining

**Three outcomes, decided mechanically, with no tuned score threshold.**

| Outcome | Rule |
|---|---|
| ANSWER | Exactly one reading survives: every surviving candidate is SAME-TERM or PROVED-EQUAL under L3, every content word is mapped or covered by a named default, and no piece is added that no word asks for |
| ASK (system) | The operation noun names operations in two systems and no domain word of the sentence settles it. Asked before generation |
| ASK (reading) | Two or more surviving candidates are SEPARATED: the L3 input and what the Rust did are shown. NONE-FOUND also asks, and prints the grid bounds |
| ASK (dropped) | The best candidates leave words dropped: "your sentence also says X; this sentence does not. Accept without it?" |
| DECLINE | No operation is anchored (never fall back to every operation), or no candidate survives the filters. Output: the unmapped words, the nearest pieces, and the kind of missing piece if recognisable |

**Filters before any outcome:**
- Q1 refusals.
- A narrowing word with the opposite claim ("a rejected X is accepted …").
- "by exactly zero" style empties.
- A condition whose two sides are the same term.

**Scoring, so that declining cannot hide errors.**
- Every test sentence carries a gold label: expressible (with gold terms) or not expressible (should decline).
- The headline is right answers over all expressible sentences; a decline or an unresolved question on an expressible sentence counts as a miss.
- Reported first: wrong answers over all sentences, including any answer on a not-expressible sentence.
- ASK is scored with an oracle author: the gold reading is evaluated at the separating input and answers the question mechanically, capped at three questions. The outcome after the dialogue is scored, and questions per resolved sentence is reported.
- Two computed controls sit in every table: "always decline" (headline 0) and "never decline" (v1's behaviour).
- Declines are split into correct (not expressible) and missed (expressible), and never pooled.

### 4.2 Coverage accounting

- **Each content token gets exactly one status.** MAPPED (piece id, and whether via a form word, the cue table or a model alignment), DEFAULT (covered by a named default such as D2 for "whether accepted or rejected"), or DROPPED. The tool asserts the partition.
- **The stop list shrinks** to articles and auxiliaries and is printed in the output. v1's list is in `clausal/clausal/compose.py:81`.
- **The reverse direction is kept.** Every piece of the candidate is supported by a token or listed as ADDED (v1's `unsupported_pieces`).
- **Condition spans.** Words after "if, when, whenever, unless, only, as long as, provided, whose, for which, that is/are" open a span. A candidate with no condition or narrowing piece mapped from a span prints "CONDITION DROPPED: …" on the first line. This aims at the dropped-condition miss recorded twice in `trials/sentences/RESULTS.md` (all 5 reader misses).
- **A candidate with DROPPED words is never an ANSWER.** It can be chosen only by a recorded acknowledgement, stored in the provenance record (4.3).
- **Model alignments are a separate, visible status.** If a model says "goes down" maps to `decreases_by`, the line reads "read 'goes down' as 'is decreased by exactly' (proposed by model)". Whether these may count toward ANSWER is decided by the seeded-drop test in node L1b, not assumed.

### 4.3 Where a language model enters

**Role.** The model proposes parse trees and never text that reaches a file.
- It receives the rough sentence, the forms and echoes of the anchored system's books, and the operation's roles.
- It returns trees as JSON (piece ids and hole fillers), optionally a word-to-piece alignment, optionally "no tree: missing piece of kind K".
- Its decline is advisory; the decline rule in 4.1 is the tool's.

**Enforcement: generate-then-compile-filter on trees first; constrained decoding only if that fails.**
- The JSON schema is generated from the book, with enums of piece ids and of role names per operation, so structured output gives a first mechanical constraint with any model.
- The tool writes the sentence from the tree with the live forms (`Compiler.surface` and `Compiler.canonical`, as the Q4 refusal hints already do), compiles it, and keeps it only if the composition found equals the proposed tree (v1's "another composition" check).
- At most two repair rounds, each fed the compiler's refusal.
- Grammar-constrained decoding against the forms is the fallback, because it has three costs:
  - It needs an exported grammar, which is a second reading of the book that can drift each wave.
  - Typed holes (`term<T>`, `from_operation`) need sort-indexed nonterminals.
  - It still cannot express the Q1, NARROWED-TIE or cross-system refusals, so the compile step stays either way.
- If the grammar is built, it gets its own check: every sentence of `clausal/clausebook/terms.lock.json` is accepted, and a sample of grammar strings is compiled with the pass rate reported.

**Checks the model cannot influence:**
- The echo is the compiler's.
- Coverage is computed by the tool.
- L3 compares model candidates with rule-based candidates and with mechanical neighbours of the proposal: condition removed, scope widened or narrowed, strict or non-strict, party swapped, a near domain word substituted. The neighbour comparison is what catches a single plausible wrong proposal such as "valid on the ledger" for "would apply in order" (`default-1/R07`, candidate 2).

**Attestation.** One record per composed rule in a sidecar beside the feature file, keyed by the term digest:
- **Proposer:** `proposed_by: {kind: model, id: <model field of the API response>, provider, date, prompt_sha, parameters, on_behalf_of: <person>}`.
- **Inputs:** the rough sentence and its hash, and the book digests.
- **Checks:** compiled, tree equal, coverage with acknowledged drops, each question with its input and who answered.
- **Chooser:** `chosen_by: human:<name> | rank`.

How the record is treated:
- In the evidence graph it is its own kind (`model-proposed`, agent `model:<id>`), never `human-asserted` (`clausal/clausal/report.py:868`).
- The sign-off record `{reviewer, date, digest}` (`clausal/clausal/vreport.py:224`) gains `kind` and `on_behalf_of`, so a model attestation can be recorded without satisfying strict mode unless a project's policy says so. This follows the last entry of `DECISIONS.md`.
- It is the harness's statement, not a cryptographic one, and the record should say so.

### 4.4 Evaluation

**Contamination inventory:**
- v1 was measured on the 48 and its report read.
- This design was derived from them.
- The Q4 rewordings coincide with up to 13 (overlap not computed, `docs/studies/2026-11-12/readability-critique.md`, B11).
- L2's pieces were chosen from their missing-piece list, and its implementer saw the first words of about ten.
- 11 of the 30 expert rewordings are now refused as retired forms.

**L4 becomes a development measure.**
- The 48 stay unedited.
- Gold moves to a new file outside `trials/`: the 30 rewordings migrated by following the refusals (Q4 reports 11 of 11 compile to the same Lean), gold for the 6 newly expressible written by a non-builder, and the rest labelled "should decline".
- Every L4 number is printed with the word "contaminated" and is not used in a decision.

**L5 is the number.**
- **Authors:** people if H2 recruits any, reported in their own column. Otherwise at least two model families other than the builder's, given only `trials/sentences/AUTHOR_BRIEF.md`.
- **Size:** at least 96 sentences (8 authors of 12), giving roughly ±10 points at 50%.
- **Brief:** one amendment before use, at least two of the five cases must be "false here" or "does not apply".
- **Two strata:** L5a on the ledger and wallet; L5b on a system whose pack was not shaped by the 48 (the counter now, `clausebook/abac` or the R2 crate when they exist). L5a alone tests phrasing, not reuse.
- **Gold:** two blind reworders who know the book and never see composer output. A candidate is RIGHT if it is SAME-TERM or PROVED-EQUAL with a gold; "not separated on the grid and agrees on all cases" is a weaker class reported apart; it is WRONG if separated from every gold or contradicted by a case. Reworders who separate make the sentence "ask is correct".
- **Frozen in one commit before any L5 file is opened:** composer and book commits, cue table, prompt, model id and parameters, limits, decline rules, scorer, gold protocol and decision rule. The sentences are held outside the builders' directories with their hash committed.
- **Arms, paired on the same sentences:** A0 is v1 as merged (`a7325a1`); A1 is v2 without a model; A2 is v2 with the proposer, run three times with the worst run as headline.
- **Controls the evaluation must pass:** the 121 lock sentences fed as rough input return themselves, and a planted composer that drops every condition is flagged by the scorer.

**Signals, frozen first, and reported as trades in line with the owner's stance.** A result counts against using a model at all if any of these holds on L5:
1. A2 gives more wrong answers than A1.
2. A2's gain in right answers over A1 is under 10 points, or its paired interval includes zero.
3. Any seeded dropped condition is hidden by a model alignment.
4. The top answer differs between identical runs on more than 10% of sentences.
5. A2 answers more of the not-expressible sentences than A1.
6. A2 needs more oracle questions per resolved sentence than A1.

A1 failing to beat A0 counts against the rule changes themselves.

## 5. Plan nodes

| Node | What | Test | Needs |
|---|---|---|---|
| L1a | Outcomes ANSWER / ASK / DECLINE, the filters, system-first question | Identity test 121 of 121. A reviewer-written set of at least 20 sentences needing unbuilt pieces (from the eleven in `clausal/clausebook/l2/FREEZE.md`): none answered. 0 answers with a dropped word | L3, Q1 |
| L1b | Coverage accounting, condition spans, acknowledgement record | Partition holds on every run. Seeded drop (delete one condition or narrowing from each gold tree): 100% reported under lexicon mapping; the model-alignment rate measured with an adversarial aligner | L1a |
| L1c | Clause-by-clause composition, phrase cues for coverage words, argument order in comparisons, cues for the L2 pieces | Development set written by a non-builder, not the 48: the ", and" sentences become reachable; no change to the identity test | L1a |
| L1d | Oracle author and answer feedback (an answer removes candidates and the next question is asked) | On `clausal/separate_tests/` cases the dialogue ends at the gold reading within three questions | L3 |
| L1e | Tree JSON interface and schema generated from the book | Round trip tree to sentence to compile to the same term: 121 of 121 | Q3 |
| L1f | Model proposer, neighbour comparison, attestation record, evidence kind | A fake adversarial proposer (non-compiling tree, retired form, a tree that surfaces to another composition, prose in a field, a false alignment): 5 of 5 dropped or flagged. Model id taken from the response. Selftest: a model attestation never satisfies strict mode | L1b, L1e |
| L1g | Grammar export and constrained decoding (only on trigger) | Trigger: under half of proposals compile after two repairs. Lock sentences accepted; sampled strings compiled, rate reported | L1f |
| L4r | The 48 with the new scorer, three arms, labelled contaminated | Gold migrated outside `trials/`; A0 reproduced on the new book and reported as the baseline | L1a–L1f |
| L5p | Protocol freeze, brief amendment, authors, two reworders | One commit before any L5 file is opened; hash of the sentence set committed | L4r, H2 |
| L5 | The measured run, strata a and b | Tables of section 4.4; wrong answers first; the six signals evaluated as frozen | L5p |

H2 part two can draw its items from L1a's ASK output once L1d exists.

## 6. Not checked

- **The frozen composer on the merged book.** Nothing was run on the 48, so every "would remove" in section 3 is a projection.
- **Whether Q1 refuses "a rejected batch".** Inferred from the `no_call` declaration, not from a compile.
- **Whether "it is rejected" is shared across systems after Q4 row 3**, and so whether the two artefactual RIGHT-IN-TOP-3 would still be offered.
- **Whether `internal` could stand for "both accounts exist and differ" in `sonnet-1/R10`.**
- **Whether the expert sentence for the other 17 wrong readings was generated and cut by the beam, or never generated.**
- **Whether `compose_tests/l4b.py` still runs** with 11 rewordings refused and `trials/sentences/rewordings.py` unedited.
- **Whether any model API available here supports the recursive schema the tree format needs.** No model was called.
- **`clausal/clausal/separate.py` beyond its header and entry function**, including its cost per pair at the volume the neighbour comparison would need (`clausal/COMPOSE.md` gives about 3 s a pair).
- **The overlap of the 13 Q4-coincident sentences with the 20 wrong and 18 unscorable.** The critique did not compute it and neither did I.
- **`private/`**, `docs/studies/2026-11-12/first-wave-scout.md`, the three readability proposals, and `clausal/SEPARATE.md` were not read.