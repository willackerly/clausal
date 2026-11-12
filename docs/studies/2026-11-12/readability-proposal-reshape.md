# Better canonical forms for Clausal, with no aliases

Scope: read-only, and nothing was run. Every proposed form below is unverified against the parser. `slice/` became `clausal/` while I worked; paths use the new names, and line numbers were read before the rename (`clausal/clausebook.yaml` is still 1050 lines).

## 1. Findings that shape the proposal

**The static grammar already has aliases.** "One canonical sentence per meaning" does not hold today:

- **Articles:** `a`, `an`, `every`, `any` are interchangeable (`clausal/clausal/vocab.py:37`).
- **Two Rule voices:** `<subject> <verb phrase>` and `for <subject>, <then-claim>` are both accepted (`vocab.py`, `clause()`, about line 952). Seven frames have both a `vp_forms` and a `then_forms` entry, so each has two Rule sentences: `always_answers`, `never_changes`, `rejected_unchanged`, `increases_by`, `decreases_by`, `at_most`, `at_least`. This is inferred from the code, not from a compile.
- **Hard-coded pairs:** "is always accepted" / "always succeeds", and "is never accepted" / "is always rejected" (`vocab.py:1009-1010`).
- **Piece forms:** "the total of" / "the aggregate" (`clausebook.yaml:592`); four forms of `l.balances_of` (:259); two each for `l.balance_at` (:275) and `l.the_transfer` (:321).
- **Logical duplicates:** "every X is not P afterwards" and "no X is P afterwards" say the same thing (`clausal/features/ledger_rules.feature:67` and `:166`).
- **One concept, two words:** "successful" (adjective) and "accepted" (class). "is now" and "afterwards" both mark the state after the call.

**The canonical form is sometimes less clear than its own echo.** "is not more than" is echoed as "is at most"; "does not exceed" as "is at most" (`clausebook.yaml:548-574`).

**Defaults are not in the sentence.** `docs/ARCHITECTURE.md:120` and `README.md:25` say the canonical sentence states "accepted or rejected". No form in `clausebook.yaml` or `vocab.py` accepts those words; they appear only in default D2's text and the echo.

**The README's TDFLite rows are not Clausal as the Clausebook defines it.**

- "more-never-loses" (`README.md:67`) is not a form. The frame's forms are "never loses acceptance when {variation}" (`clausebook.yaml:938`).
- `README.md:68` labels the attribute-order sentence `never changes` + `permutation`. `never_changes` takes a measure, not a variation (`clausebook.yaml:712`). The matching frame is 14, `same_answer` (`clausal/lean/Frames/Frames.lean:169-176`).
- I found no `clausebook/abac` pack: a filename search for "abac" to depth 3, outside `private/` and `corpora/`, returned nothing.

**What readers miss is conditions and call coverage.** All five proxy misses were a dropped condition or narrowed calls; wrong claim words were caught 36 of 36 (`trials/sentences/RESULTS.md:12, 87-95`). Two of three false alarms were "smaller"/"larger" echoed as "at most"/"at least" (`RESULTS.md:13`).

## 2. Mechanism

Change only surface strings and the Rule-subject grammar. The `lean:`, `at:`, `check:` and `flat:` templates and `clausal/lean/Frames/*.lean` are untouched. Six rules:

- **R1. One word per concept.** "accepted" / "rejected" only (drop "successful", "always succeeds", "is never accepted"); "the total of" only; `A`/`An` only; "afterwards" only.
- **R2. The calls slot is never empty.** The operation noun carries one of three markers: `A transfer, accepted or rejected,` (the default), `An accepted transfer`, or `A rejected transfer`.
  - The marker is omitted, and narrowing refused, where the claim itself is about this call's acceptance: frames 5 to 8, and frame 4 on the operation's own class.
  - Scenario steps are unchanged.
- **R3. Conditions are fronted.** `If <condition>, <main clause>` replaces `<subject> for which <condition>`.
  - Following Attempto's anaphora convention (from memory), the first mention of the operation noun is "a", later mentions "the".
  - This puts the condition first, as EARS and legal drafting do, and removes the clause sitting between subject and verb.
- **R4. Two-call rules name two calls.** The second call is "the same <operation> <difference>". Variation words become difference phrases ("with an amount no larger"), not clauses ("the amount is smaller").
- **R5. One Rule voice per frame.** Verb-phrase voice when the operation is the grammatical subject; "For a <operation>," voice only when the subject is a quantity or collection of the answer (9 result, 10 result, 11, 15). The Then form is "it " plus the same stem where grammar allows, so the two cannot diverge.
- **R6. Comparisons show the boundary positively.** "at most", "at least", "more than"; no "not more than", "does not exceed", or bare "smaller"/"larger" for a non-strict relation.

**Gherkin structure, considered and rejected for conditions.**

- Carrying a condition in a `Background` or description line leaves a Rule title that reads as an unconditional claim.
- Runners and reports show the title alone, which reproduces the least-caught error (dropped condition).
- `out/prior_art_vocabulary.md` section 3 and its "What to avoid" item 10 also say to avoid Background inside a Rule.
- What R3 keeps is that the `If` clause uses the same condition forms as a scenario's `Given`.

**Default D1 (the call must answer) stays outside the sentence.** "Accepted or rejected" does not say that a crash falsifies the rule. I propose the compiler report any operation lacking a companion rule "A <operation> always gives an answer". That adds a signed sentence and changes no other statement.

## 3. The 25 frames

| # | Frame | Current (Rule / Then) | Proposed (Rule / Then) | Risk introduced |
|---|---|---|---|---|
| 1 | `always_answers` | always answers / it answers | always gives an answer / it gives an answer | "Answer" may be read as "accepts". |
| 2 | `never_changes` | never changes M / M is unchanged | Unchanged, with the R2 marker; "For a X, M is unchanged" refused in Rules | Marker repeated on every rule may be skimmed. |
| 3 | `changes_only` | (none) / of C, only X and Y change | changes at most X and Y among C / of C, at most X and Y change | "Only X and Y change" implies they do change; Lean does not (`Frames.lean:32-34`). "At most" may be read as a count. |
| 4 | `always` (class) | is always accepted, always succeeds / {class} | is always accepted / unchanged | None new. |
| 4 | `never` (class) | is never accepted, is always rejected / negated class | is always rejected / unchanged | A reader may count a crash as a rejection; Lean does not. |
| 5 | `if_then` | is accepted whenever K | Unchanged | Now sits beside fronted "If K, a X is always accepted"; they differ only on calls outside K that give no answer (`clausal/lean/Frames/Lemmas.lean:47-77`). |
| 6 | `only_if` | is accepted only if K | Unchanged | "Only if" read as "if" (pre-existing). |
| 7 | `exactly_when` | is accepted exactly when K | Unchanged | "When" read as time. |
| 8 | `rejected_unchanged` | is rejected and changes nothing / it is rejected and nothing is changed | Rule unchanged / it is rejected and changes nothing | "Nothing" means the operation's own state only. |
| 9 | `increases_by` | increases M by exactly T / M is increased by T | Rule unchanged / M is increased by exactly T | None; the Then form now also says "exactly". |
| 9 | `decreases_by` | decreases M by exactly T / M is decreased by T | Rule unchanged / M is decreased by exactly T | Implies M was at least T (already true in Lean). |
| 9 | `becomes` | (none) / M is now T | leaves M equal to T / M is afterwards T | "Leaves" may suggest M was already T. |
| 9 | `result_is` | (none) / A is T | For a X, A is T (For voice only) | The marker sits oddly inside a "For" phrase. |
| 10 | `result_at_most` | (none) / A is at most T | Unchanged | None. |
| 10 | `result_at_least` | (none) / A is at least T | Unchanged | None. |
| 10 | `at_most` | never leaves M above T / M is afterwards at most T | Unchanged | I rejected "keeps M at most T": it implies M was within T before, which is why `n4` is false (`ledger_rules.feature:51-53`). |
| 10 | `at_least` | never leaves M below T / M is afterwards at least T | Unchanged | Same. |
| 11 | `every_of` | (none) / every C P afterwards | afterwards, every C P; "every C is not P" refused | Refusing every-not moves `n5` to `NoneOf` (definitionally equal, not textually). |
| 11 | `none_of` | (none) / no C P afterwards | afterwards, no C P | Fronted "afterwards" could be read as covering a later clause. |
| 12 | `monotone` | never loses acceptance when V / never loses that C when V | If a X {class}, the same X {difference} also {class} | "The same X" may be read as the identical call; a first call that crashes falsifies the rule, and the sentence does not say so. |
| 13 | `agrees_with` | agrees with R | gives the same answer and leaves the same {state} as R | Longer. "Agrees with" hid that the state is compared too (`Frames.lean:163-167`). |
| 14 | `same_answer` | gives the same answer when V | A X and the same X {difference} give the same answer | "Answer" excludes the state afterwards (true in Lean). |
| 15 | `within` | (none) / every C is a D | Unchanged | Lists are compared as sets (pre-existing). |
| 15 | `covers` | (none) / every D is a C | Unchanged | Same. |
| 16 | `same_answer_if` | gives the same answer when V, if C | If a X {class}, the same X {difference} gives the same answer | Close to frame 12's wording; "also accepted" against "the same answer" must be told apart. |

**Modifiers.**

- "successful" becomes "accepted".
- "T is not more than M" becomes "T is at most M".
- "M plus T does not exceed Z" becomes "M plus T is at most Z".
- The ledger variations become "with an amount no larger", "with an amount no smaller", "with any other amount", "on a ledger that agrees at the account", "on the ledger with accounts added at its end".

The worst-reading text in the fixtures is a ledger-pack noun, not a core frame: "the balance of account the sender of the transfer of the ledger" (`ledger_rules.feature:32`). The wallet pack already uses "the sender's balance" (`clausal/features/wallet.feature:135`). Any `clausebook/abac` pack should make its terms role names from the start.

## 4. Ten rewrites

Identity argument for all ten: the composition tree is unchanged and the Lean templates are untouched, so the rendered Lean is the same text. A check exists in principle: the rule `key` (`vocab.py:995`) and the generated readings file should match before and after, apart from the doc comment. I did not run it.

| # | Source | Current | Proposed | Why the Lean is identical |
|---|---|---|---|---|
| 1 | `README.md:67` | Adding an entitlement to a subject more-never-loses an accepted key-release decision. | If a key release is accepted, the same key release with more entitlements for the subject is also accepted. | `Frames.Monotone op v accepted`, as the README's labels intend. The variation is a hypothetical abac word. |
| 2 | `README.md:68` | Attribute order in a token or manifest never changes the key-release decision. | A key release and the same key release with its attributes in another order give the same answer. | `Frames.IndependentOf op permutation (answer)`. The README's `never changes` label cannot type-check. |
| 3 | `README.md:66` | Key release is accepted only if subject attributes satisfy every data attribute under its rule. | A key release is accepted only if the subject's attributes satisfy every attribute of the data under that attribute's rule. | `Frames.OnlyIf op accepted K`. Only the article and the pack condition's wording change ("its" had three possible referents). |
| 4 | `ledger_rules.feature:29` | An internal transfer never changes the total of all balances of the ledger | An internal transfer, accepted or rejected, never changes the total of all balances of the ledger | `calls = .every` is already the default (`clausal/lean/Frames/Core.lean:48`); the marker writes it out. |
| 5 | `:72` (two-run) | A transfer never loses acceptance when the amount is smaller | If a transfer is accepted, the same transfer with an amount no larger is also accepted | `Monotone L.apply L.smallerAmount accepted`; `smallerAmount` is already "at most" (`clausebook.yaml:421`). |
| 6 | `:144` (rejected) | For a rejected transfer, the total of all balances of the ledger is now zero | A rejected transfer leaves the total of all balances of the ledger equal to zero | `Becomes (L.apply).rejected …`; same modifier, same frame. Still expected refuted. |
| 7 | `:169` (nested) | For a batch for which no transfer of the batch is valid on the ledger, the number of transfers applied is zero | If no transfer of a batch is valid on the ledger, then for the batch, accepted or rejected, the number of transfers applied is zero | `ResultIs (op.given (noneOf …)) applied 0`; the condition moved, the tree did not. |
| 8 | `:157` | A transfer for which the transfer is not valid on the ledger is rejected and changes nothing | If a transfer is not valid on the ledger, the transfer is rejected and changes nothing | `RejectedUnchanged (op.given (¬valid))`. |
| 9 | `:84` | A lookup agrees with the reference lookup | A lookup, accepted or rejected, gives the same answer and leaves the same ledger as the reference lookup | `AgreesWith L.lookup L.refLookup`. |
| 10 | `:32` | A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger | A transfer is accepted only if the amount of the transfer is at most the balance of account the sender of the transfer of the ledger | `OnlyIf … (t ≤ m)`; the `not_more_than` piece keeps its Lean. |

Row 7 is the weak case: "then for the batch, accepted or rejected," is clumsy, and I expect no measured gain there. With a pack fix outside core, row 10 could read "…only if the amount is at most the sender's balance".

## 5. What could go wrong

- **Marker fatigue.** A phrase on most rules may be skimmed, so a narrowed rule is noticed only by its absence. Proxy readers missed narrowing even when the echo printed "ONLY … calls" (`RESULTS.md:92`).
- **D1 stays hidden.** "Accepted or rejected" suggests the call answered. The companion-rule report mitigates this; it does not fix it.
- **Parser ambiguity.** `If C, …` adds a comma, and `clause()` cuts "for" phrases at ", " while `and_splits` cuts at " and ". New AMBIGUOUS results are plausible and unmeasured.
- **Merged comparison surfaces.** "T is at most M" and "M is at most T" share words and are told apart only by type. Not checked for collisions.
- **Existing sentences break.** Removing duplicates breaks the README's own example ("the aggregate account value", `ledger_rules.feature:14`), `Any successful transfer` (`trials/sentences/raw/v4_authored.feature:62`) and every "For a X" rule on a frame that has a verb-phrase form.
- **Frame 5 beside fronted If.** Two sentences an ordinary reader cannot tell apart. This exists today with "for which".
- **Two-call wording moves the burden to packs.** A badly written difference phrase reintroduces the problem.
- **Timing.** No entry is signed (`docs/HANDOFF.md`), so changing forms is free now. After sign-off (node H1), every form change voids signatures.

**On the frozen 48.** I read them (`trials/sentences/authors.json`). Each proposal is justified by R1 to R6, by the echo's own wording, or by `docs/ARCHITECTURE.md:120`. Several coincide with what authors wrote: "accepted" as an adjective, "whether it is accepted or rejected", fronted "If". A rise in as-written compiles on the 48 is therefore not confirmation; fresh sentences (node L5) are needed.

## 6. How to measure

Build a new bank, `trials/meaning/banks/canonical-forms-v1/`, using the existing kit, scoring and intervals (`trials/meaning/README.md`).

- **Items:** a Rule sentence and one concrete case (state, input, answer, state after; or "the call gives no answer"). The reader says whether the case breaks the rule. The schema has two judgement labels, which fits; I did not check whether `score.py` hard-codes their names.
- **Two arms:** each composition is rendered from the same tree under the current and the proposed Clausebook. Each reader sees a composition in one arm only, assigned by seed and counterbalanced.
- **Compositions:** drawn by a seeded rule from the Rule lines in `clausal/features/`, at least eight per family (state, acceptance, two-call, collection).
- **Cases:** per composition, one that separates it from each applicable neighbour, plus controls. Use the five kinds in `banks/generated-echoes-v1/mutate.py:188` and add converse, no-answer, second-call and boundary-equal.
- **Key:** from Lean, by evaluating the executable frame readings (`clausal/lean/Frames/Check.lean`, which I did not open) on each case.

Thresholds, committed before the run:

1. **Mechanical gate:** every feature recompiles with zero AMBIGUOUS or ILL-TYPED, and the generated readings are identical except `n5`.
2. **Helped:** the proposed arm's error rate on separating cases is at most two thirds of the current arm's, and the 95% interval on the difference (items and readers resampled) excludes zero. Otherwise report "no measured difference".
3. **Guards:** control-case errors rise by no more than 3 points; a family that is worse by more than 5 points keeps its current forms.
4. **Ceiling:** if proxies' current-arm error on separating cases is under 5%, the proxy run is declared uninformative.
5. **People** (the owner and at least two others) are reported as counts, separately, with no significance claim.

## 7. Cost (estimates, not measured)

| Work | Estimate |
|---|---|
| Form strings in `clausal/clausebook.yaml` (about 14 frame entries, 4 modifiers, 5 variations) | Half an agent-day |
| Parser: calls slot, fronted If with the article rule, two-call skeletons, one voice per frame, refusals that name the canonical form (`vocab.py` `subjects`, `clause`, `rule_part`, `echo_rule`) | 1 to 1.5 agent-days; the highest-risk part |
| Rewrite about 45 Rule lines in four feature files, docs and README rows; regression that every verdict and reading is identical | Half a day, in a scratch copy |
| Independent review on the other model | Half a day |
| Trial bank, Lean-evaluated key, proxy run | 1 to 1.5 days |
| People | About 30 minutes each |

## 8. Not checked

- **Not run:** the compiler, any build, any trial script.
- **Not opened:** `private/`, `clausal/DESIGN.md`, `clausal/FINDINGS.md` (two grep hits only), `clausal/lean/Frames/Check.lean`, `trials/sentences/raw/evidence.json` and `new_sentences.json`, the meaning trial's `REPORT.md`, `key.json` and `analyst_notes.md`, `docs/TDFLITE.md`, the linked DeepMind PDF.
- **Partly read:** `out/prior_art_vocabulary.md` (sections 2 and 3 and the copy/avoid lists); the TDFLite notes (guarantee table and grep hits); `clausal/features/ledger.feature` and `wallet.feature` (Rule and step lines only).
- **From memory, not sources:** Attempto, EARS, Cedar/Rego and legal-drafting conventions, apart from what `out/prior_art_vocabulary.md` records.