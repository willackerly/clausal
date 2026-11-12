# Clausal readability: recommended design, synthesised from three proposals and one critique

**Recommendation in one line:** change the canonical wording of the pieces and add no second form for now. The owner's example sentence is not Clausal as the Clausebook defines it, and every proposed alias that would have helped a reader was shown by the critique to invite a second reading.

**Basis.** I took the proposals' and the critique's findings as given, and spot-checked only these files myself:

- `docs/HANDOFF.md`, and `docs/PLAN.md:24-125`.
- `clausal/clausebook.yaml`, lines 74-96, 390-457, 548-575, 589-594, 655-668 and 930-975.
- `clausal/clausal/vocab.py`, lines 1003-1020 and 1045-1052.
- `README.md:52-68`.

I ran no compiler, build or trial. Nothing below is built.

## 0. What the evidence says before any design

- **The example is not a Clausal sentence.** "more-never-loses" (`README.md:67`) is the frame's name used as a verb. The frame's registered forms are "never loses acceptance when {v}" and "never loses that {c} when {v}" (`clausal/clausebook.yaml:938`).
- **`README.md:68` names the wrong frame.** It labels an order-independence rule `never changes`, which takes a measure. The matching frame is 14, "gives the same answer when {v}" (`clausebook.yaml:965`).
- **No ABAC pack exists.** There is no `clausebook/abac`, so none of the TDFLite rows in the README compiles today.
- **"One canonical sentence per meaning" is false of the present book.**
  - Hard-coded pairs live in `vocab.py:1009-1010`.
  - "the total of" and "the aggregate" are two forms of one piece (`clausebook.yaml:592`).
  - Seven frames have two Rule voices (all three proposals; critique section 4).
  - The hard-coded forms are under no signature (`clausal/clausal/vreport.py:147-178`, per the aliases proposal).
- **A narrowed rule can be true of every possible operation and still compile unflagged.** The critique checked this in the Lean kernel on a standalone copy of `clausal/lean/Frames/Core.lean` and `Frames.lean`.
- **The printed coverage text is wrong for two sentence shapes** (critique 2.2).
- **Readers miss conditions and call coverage, not claim words.** All five proxy misses were of those two kinds (`trials/sentences/RESULTS.md:87-95`).

The last three points make every change to how "accepted" and "rejected" read riskier, so they come first in the plan.

## 1. The rule that replaces "no synonyms in the static grammar"

**Proposed rule: one live form per piece per position, every form in the signed book; wording is improved by replacement, never by addition.**

### Allowed

| Kind | What it is | Admitted how | Checked how | Stored how |
|---|---|---|---|---|
| **Replacement** | A piece's canonical form is reworded; the old form stops being accepted and the refusal names the new one | Owner or pack owner; logged in `DECISIONS.md`. Free before H1; after H1 it voids the piece's signature | Registration lint; every `.feature` recompiles to byte-identical Lean | The `forms:` field of the piece in `clausal/clausebook.yaml` |
| **Positional form** | The same piece in a different grammatical position (Rule verb phrase, Then claim, adjective before the operation noun), at most one per position, on the same word stem | Same as replacement | Same, plus holes identical in name and category | Same entry, one field per position |
| **Composite** | The three existing idioms with a `means:` composition (`clausebook.yaml:1035-1050`) | No new ones in the first batch | Same lint | As today |
| **Computed display** | A "covers" line, an outcome table for two-run frames, and concrete allowed and forbidden cases | Generated only | Computed from the frame's `.at` statement and the claim's `Calls` value (`clausal/lean/Frames/Core.lean:29`, `clausal/lean/Frames/Check.lean`); never from `echo_rule` | Report and editor; never compiler input |

### Registration lint (`clausal book check`, not built)

These are the aliases proposal's checks 1, 2, 3, 5 and 6, applied to every form:

1. Holes are exactly the piece's holes: same names, same categories, none filled by a literal.
2. Holes may be reordered only if their categories are pairwise different.
3. At most one live form per piece per position.
4. No two forms of different pieces share a literal skeleton, unless a separating input is shown and the pair is signed as such.
5. Every existing `.feature` recompiles to the same term.

Two refusals are added from the critique:

- **Vacuity:** a narrowed rule whose reading holds for every `run` of the operation's types is refused (critique 2.1).
- **Narrowing in Rules:** the only narrowing form is the adjective before the operation noun.

### Still forbidden

- A second form for the same piece in the same position (sum/total, succeeds/accepted).
- Any accepted form that lives in Python and not in the book.
- Fronted conditions or variations ("If …,", "When …,", "Given that …,").
- A parenthetical after the subject (", if it is rejected," or ", accepted or rejected,").
- A project's second noun for a domain word.
- "Equivalent term" rewrites, where a tool changes the Lean term or the file text.
- Any text under a Rule that is generated from `echo_rule` and pinned in the file.
- `fmt` changing words in a file.

### How this answers the earlier rule's reasons (`docs/PLAN.md:41`, `:78`)

- **Inconsistency between projects:** one form per position means two projects cannot write one meaning two ways in a Rule.
- **Ambiguity:** forms are checked at registration, where today nothing is (`vocab.py:170-185`, per the aliases proposal).
- **Authors who have not seen the vocabulary:** still `clausal compose`. Nothing here helps them, and no proposal claimed otherwise.
- **Signed text is tested text:** the compiler reads the words as written, and with one form there is no second copy to drift.

### What this does not give the owner

It does not give equivalent aliases in the ordinary sense. Every such alias on the table failed the critique. Q9 defines the gate through which one could be admitted later.

## 2. First batch

Every row is a design, and none is run by me unless the check column says "verified by the critique". Rows 1 to 3 need Q1 first, because making "accepted" the adjective makes a vacuous sentence easier to write.

| # | Piece | Old form | New form | Check it must pass |
|---|---|---|---|---|
| 1 | `successful` modifier (`clausebook.yaml:658`, `vocab.py:1049`) | "A successful transfer" | "An accepted transfer" | Byte-identical Lean on all fixtures (verified by the critique in a scratch copy); Q1 refusal in place first |
| 2 | `always` / `never` on the acceptance class (`vocab.py:1009-1010`) | "is always accepted", "always succeeds"; "is never accepted", "is always rejected" | "is always accepted"; "is always rejected" | Same Lean. Known risk: a reader may count a crash as a rejection |
| 3 | Wallet acceptance class (`clausebook.yaml:231`) | "the operation succeeds" | "it is accepted" | Same Lean; lint check 4 against `l.accepted` (`:395`) |
| 4 | Narrowing in Rule lines (`vocab.py:1014-1017`) | "For X, if it is rejected, …" and "For X, if it is accepted, …" | Refused in Rules; write "For a rejected X, …" | Same Lean. Removes the shape whose printed coverage is wrong (critique 2.2, B8). Scenario Then steps keep the prefix |
| 5 | Articles (`vocab.py:37`) | a, an, every, any | A / An | Same Lean. Breaks "Any …" and "Every …" Rule lines; count unmeasured |
| 6 | `aggregate` (`clausebook.yaml:592`) | "the total of {ns}", "the aggregate {ns}" | "the total of {ns}" | Same Lean. Breaks `clausal/features/ledger_rules.feature:14` and the README example |
| 7 | `l.balances_of` (`:255`, four forms), `l.balance_at` (`:275`), `l.the_transfer` (`:321`) | several each | One each, chosen by the pack owner in C1; prefer role names ("the sender's balance", as `clausal/features/wallet.feature:135`) | Lint check 4: `l.bal_of` and `l.balance_at` share a skeleton with different meanings (0 against absent), so that pair must be resolved, not exempted |
| 8 | `not_more_than` (`:548`) | "{t} is not more than {m}" | "{t} is at most {m}" | Identical Lean on all 85 compilations, no new AMBIGUOUS (verified by the critique) |
| 9 | `sum_within` (`:571`) | "{m} plus {t} does not exceed {z}" | "{m} plus {t} is at most {z}" | Same run as row 8 |
| 10 | Variations `l.smaller_amount`, `l.larger_amount` (`:413-430`) | "the amount is smaller" / "is larger" (the Lean is non-strict) | "the amount is the same or smaller" / "the same or larger" | Same Lean. Does not state "on the same ledger"; see open question 3 |
| 11 | `every_of` with "not" | "every X is not P afterwards" | Refused; write "no X is P afterwards" | The one term change: `ledger_rules.feature:67` moves from `EveryOf … ¬valid` to `NoneOf … valid`. Rerun its verdict; all other readings byte-identical |
| 12 | One Rule voice per frame: `always_answers`, `never_changes`, `rejected_unchanged`, `increases_by`, `decreases_by`, `at_most`, `at_least` | Verb-phrase voice and "For a X, <Then claim>" both accepted | Verb-phrase voice only in Rules; "For" voice only for frames with no verb-phrase form | Same Lean; the refusal names the canonical sentence |
| 13 | Then forms of `increases_by`, `decreases_by`, `rejected_unchanged` | "M is increased by T"; "it is rejected and nothing is changed" | "M is increased by exactly T"; "it is rejected and changes nothing" | Same Lean; the stem matches the Rule form |
| 14 | `monotone`, frame 12 (`:938`) | "never loses acceptance when {v}"; "never loses that {c} when {v}" | Wording unchanged. "never loses that it is accepted" is refused in favour of the short form, or the two emit the same term | Today the two give different Lean text (`(L.apply).accepted ans` against `L.said ans`, critique 2.3) |
| 15 | `same_answer_if`, frame 16 | "gives the same answer when {v}, if it is rejected" | "gives the same answer when {v}, if the first call is rejected" | Same Lean. Unparsed; a candidate, see open question 4 |
| 16 | `README.md:67` | "Adding an entitlement to a subject more-never-loses an accepted key-release decision." | "A key release never loses acceptance when the subject gains an entitlement." | Marked "planned" until `clausebook/abac` exists (T9); the variation must say which gain (open question 5) |
| 17 | `README.md:68` | "Attribute order in a token or manifest never changes the key-release decision." (`never changes`) | "A key release gives the same answer when only the order of the attributes differs." (frame 14) | As row 16 |
| 18 | `README.md:66` | "Key release is accepted only if subject attributes satisfy every data attribute under its rule." | "A key release is accepted only if every attribute of the data is satisfied by the subject under its rule." | As row 16. The passive keeps "its" on the attribute (critique A5) |
| 19 | Hard-coded forms and coverage text | Python strings in `vocab.py`; `defaults:` and `weakenings:` outside the digest | All in the book and under the sign-off digest | Removing a book entry makes its sentence fail; digest covers the text. Must land before H1 |

**Notes on the batch.**

- **More-never-loses family (rows 14 to 17).** The readable sentence already exists. The gain comes from using the real form with a well-worded variation, and from the computed outcome table in Q6, which is the only element in any proposal that shows a reader a vacuous narrowing.
- **Row 8 homographs.** The aliases proposal says `more_than` and `exceeds` read alike "with the arguments reversed". From `clausebook.yaml:551-562`, both mean "left is strictly more than right"; only the hole categories are swapped. The same holds for `not_more_than` and `at_most_value` after row 8. So these pairs are one relation at two type signatures, and are candidates for a signed exemption under lint check 4. I did not test this in the parser.
- **The 48 frozen sentences.** I did not read them. Each row follows from a rule: one form per position, one word per concept, boundaries stated positively, or one word sequence with one meaning. The critique counted, by regex, that the proposals' changes coincide with up to 13 of the 48 (5 use "accepted" as an adjective, which is row 1). Any rise in L4(a) after this batch must be reported as contaminated, and L5's fresh sentences are the test.

## 3. Plan nodes

| Id | Work | Test | Target | Needs |
|---|---|---|---|---|
| **Q1** | Refuse a narrowed rule whose reading holds for every `run`. Put the critique's kernel theorems in the project build | The four sentences in critique 2.1 are refused with a reason; every current fixture still compiles | 4 of 4 refused; 0 fixture regressions | One `lake build` |
| **Q2** | Fix printed coverage: derive it from each claim's `Calls` value, not from clause-level modifiers (`vocab.py:1121-1152`); put the text under the digest | For every fixture rule and both faulty shapes, the printed "covers" equals the `Calls` constructor in the emitted Lean; a narrowed two-run rule no longer prints "both must give an answer" | 0 mismatches | — |
| **Q3** | Move every accepted form into the book; build `clausal book check` | Run on today's book and list the violations (expected: rows 2, 6 and 7, and the comparison homographs) | After Q4: zero violations, or each exception signed with a separating input | Before H1; shares the file with C1 |
| **Q4** | Apply the first batch in a scratch copy; rewrite the affected Rule lines | Generated readings byte-identical before and after, except `ledger_rules.feature:67`; no new AMBIGUOUS or ILL-TYPED; verdicts unchanged | 100% identical apart from the one named rule | Q1, Q2, Q3; second-model review |
| **Q5** | Duplicate-meaning report keyed on the term with the operation's acceptance unfolded | It lists `ledger_rules.feature:14` and `:29` (before Q4), and "A transfer is always accepted" against "For a transfer, it is accepted" | Every pair named in critique 2.3 and aliases finding 3 is found | — |
| **Q6** | Computed display from `.at` and `Check.observe`: covers line, two-run outcome table, one allowed and one forbidden case with the nearest neighbouring sentence | Table agrees with the executable reading on the search grid; a vacuous narrowed rule (with Q1 switched off) shows no forbidden row; the monotone table has a "no answer" row | 100% agreement | L3 |
| **Q7** | Measured comprehension trial, before and after; design below | Thresholds frozen in a commit before any run | See below | Q4, Q6, H2 recruits |
| **Q8** | Mechanical negative controls; list below | Each is refused with a message naming the reason | 4 of 4 refused | Q1, Q3 |
| **Q9** | Gate for any later second form (positional or fronted) | Admitted only on a people result of "helped" in Q7's design on dropped-condition and narrowing items; owner decision logged in `DECISIONS.md` | No admission without that result | Q7 |
| **Q10** | TDFLite rows as the internal worked example: draft `clausebook/abac` words so rows 16 to 18 compile; list what `README.md:69` needs (an "or" between two conditions, which no form provides; this goes to L2) | Each README TDFLite row compiles against the draft pack or is labelled "planned" | 3 of 4 rows compile; the fourth has an L2 entry | T9, C1; no change to the README's emphasis |
| **Q11** | Correct the statement that defaults are "written out in the sentence" (`docs/PLAN.md:41`, `docs/HANDOFF_CLAUSAL.md:41`, `docs/ARCHITECTURE.md:120`, `README.md:25`) until open question 1 is settled; add the compiler report for any operation lacking the companion rule "A <operation> always answers" | Docs match what the compiler accepts | 0 claims of an unaccepted form | — |

**Order:** Q1 and Q2; then Q3 with C1; then Q4, Q5 and Q11, all before H1; then Q6, Q8, Q7; then Q9. Q10 runs alongside T9.

### Q7: trial design

- **Bank:** a new bank under `trials/meaning/banks/`, built on the pattern of `banks/generated-echoes-v1/`.
- **Item:** one Rule sentence and one concrete case (state, input, answer, state after, or "the call gives no answer"). The question is whether the case breaks the rule.
- **Key:** computed by the executable frame readings in `clausal/lean/Frames/Check.lean`, never written by hand.
- **Arms:**
  - A, today's forms.
  - B, the first-batch forms.
  - C, B plus the Q6 display.
  - Each composition is rendered from the same parse tree. A reader sees each composition in one arm only, counterbalanced by seed.
- **Trap kinds:** rejected call, no-answer call, boundary equality, second run of a two-run rule, dropped condition, narrowed calls. At least eight breaking and eight non-breaking items per kind per arm (the floor in `docs/PLAN.md:96`).
- **Arm C guard:** the displayed case is never the tested case nor of the tested trap kind for that item. Sixteen bare sentences follow arm C, to measure whether readers stopped reading the sentence (critique C7).
- **Reader negative control:** a set of fronted forms, such as "If a batch applied as a whole is rejected, it never changes the ledger, and a batch applied as a whole never changes the total of all balances of the ledger". These are predicted to do worse on dropped-condition items (critique A4). If the trial cannot detect that, it is declared insensitive and licenses nothing.
- **Readers:** the owner and at least two others, reported in their own column as counts; four or more model readers from two families, labelled proxy.
- **Frozen before any run:**
  - The form lists, seed, tree-selection rule and case generator.
  - A power simulation with judgements clustered by reader and item, stating the smallest detectable difference.
  - These decision rules:

    | Outcome | Condition |
    |---|---|
    | Helped | The 95% interval for the error difference on trap items (items and readers resampled) excludes zero in favour of the new arm, and the false-alarm interval does not exclude zero against it |
    | Hurt | The interval excludes zero against the new arm, pooled or on dropped-condition or narrowing items |
    | No measured difference | Anything else |
    | Uninformative | The proxy error in arm A on a trap kind is under 5%; that kind is reported as uninformative for proxies |

- **Why no point thresholds.** The critique simulated the proposals' own "hurt" and family-guard rules and found them firing 41% to 90% and 24% to 75% of the time with no true difference.
- **Use of the result:**
  - Replacements that only remove forms (rows 1 to 9, 11, 12) stand on "no measured difference" and are reverted on "hurt".
  - Rows 10, 13 and 15 change what a reader sees and are reverted on "hurt".
  - Arm C ships only on "helped" or on the owner's decision.
- **Expected limit.** Proxies already catch about 92% (`trials/sentences/RESULTS.md:81`), so the proxy run will probably return "no measured difference". Only the people run can say more, and with three people only the direction is reportable.

### Q8: mechanical negative controls

Each must be refused.

1. **"never changes the answer when {v}" for frame 14.** Tempting, because `README.md:68` wrote it. It takes another frame's head, and the lint must refuse it as a homograph of `never_changes` without a signed separating pair.
2. **"A rejected transfer gives the same answer when the amount is larger" as a form of frame 16.** It compiles today as narrowing and is true of any code (critique 2.1, A3). Q1 must refuse it.
3. **"An accepted transfer never loses acceptance when the amount is larger".** Vacuous once row 1 lands; Q1 must refuse it.
4. **"the balance of {k} in {l}" as a form of `l.bal_of`.** It collides with `l.balance_at` at a different meaning; lint check 4 must refuse it.

Control 1 depends on a head-collision rule that the existing book may itself violate: frames 14 and 16 share "gives the same answer when". Whether it can be stated without exempting half the book is unchecked.

## 4. Rejected, and why

| Rejected | From | Reason |
|---|---|---|
| Fronted forms ("If/When/Given that …, <claim>") | aliases rows 1, 2, 5, 6; reshape R3 | Across ", and" the parser scopes the condition to one clause and a reader carries it over both (critique A4). "Given that" presupposes the condition (A6). Fronted `given` sits beside `if_then`, from which it differs only on no-answer calls outside the condition |
| "If a X {class}, the same X {difference} also {class}" for frames 12 and 16 | reshape | Same surface as a scope "If" with different behaviour (B2). Needs a second predicate form per class (B3). Drops "on the same ledger" and reads as a sequence (B5) |
| ", if it is rejected," after the subject | aliases row 4 | Reads as narrowing, and its narrowing neighbour is vacuous (A3) |
| ", accepted or rejected," marker | reshape R2 | A call that gives no answer is neither, so the marker states a weaker claim than the Lean (B1); on frame 1 it presupposes what it asserts |
| Class D, a project's second domain noun | aliases row 9 | Moves meaning into a name; the signer signs the name (A9) |
| Class E, equivalent-term aliases | aliases row 10 | Not an alias of one piece; changes the Lean term; `fmt` would change reviewed text (A8). Row 11 of the batch refuses the duplicate form instead |
| Reserved-word count check | aliases check 4 | Refuses the proposal's own aliases under one reading and lets "always" and "never" swap under the other (A1) |
| "gives the same answer and leaves the same {state} as R" for frame 13 | reshape | Begins with frame 14's head; its " and " meets the clause splitter (B6) |
| Gloss lines generated from `echo_rule` and pinned in the file | layers D1 | Would pin the wrong coverage lines of critique 2.2; those strings are under no signature (C1) |
| A "silent on" slot | layers | The worked example was false: run 2 must still answer when run 1 is rejected (C3) |
| Outcome table built from `flat` | layers D2 as specified | `flat` has no calls guard and no answer requirement, so it overstates narrowed rules (C2). The table survives only when built from `.at` |
| Enforced multi-line Rule layout | layers S2 | Gherkin's Rule name is its first line, so every rule would be labelled by its subject alone (C5); needs a new parser |
| Deprecated-but-accepted forms rewritten by `fmt` | aliases class X | Same objection as class E: file text changes after review. A retired form is refused with a message naming its replacement |
| A cap of 12 core aliases | aliases | Moot, since no alias is admitted |
| Point-threshold "hurt" rules and the 5-point family guard | aliases, reshape | Fire on noise (A12, B10) |

## Open questions (the critique is unanswered here)

1. **Defaults in the sentence.** No form accepts "accepted or rejected", and the one proposed marker was rejected. The plan's requirement that fail-closed defaults be written in the sentence is unmet. Q6's covers line and Q11's companion-rule report are partial substitutes outside the sentence.
2. **A correct reserved-word check.** None exists. Vacuity (Q1) and homographs (lint check 4) cover part of what it was for.
3. **Variation wording that states "same state".** No candidate was tested against the parser's ", " and " and " splitting.
4. **"if it is rejected" keeps two meanings across Rule lines and scenario Then steps** unless row 15 lands. Row 15 is unparsed.
5. **Which entitlement gain row 16 means.** The critique argues from the private notes that the rule's verdict on present code depends on it (A10). Not checked against the Go code or the pilot model.
6. **Frame 1 wording** ("always answers" against "always gives an answer") and any replacement for "never loses acceptance": untested candidates for Q7, not in the batch.
7. **Bounded round-trip check** (aliases check 7). It needs a tree-to-sentence function, which does not exist, and it tests parse uniqueness, not reader scope. Not scheduled.
8. **Whether the Q6 display is pinned under the Rule in the file or shown only in the report.** Pinning shows up in diffs; C5 and the anchoring risk argue against it.
9. **Whether Q1's refusal can be decided by a fixed tactic** for every frame. This is the critique's suggestion and is unbuilt.

## Not checked

- **Nothing run.** No compiler, pipeline, `lake` build or trial script. All "identical Lean" claims are the critique's scratch-copy results or designs.
- **Not read:**
  - `clausal/lean/Frames/*.lean`, the `.feature` files, `trials/` (including the 48 sentences and `raw/`).
  - `out/prior_art_vocabulary.md`, `docs/VOCABULARY.md`, `docs/HANDOFF_CLAUSAL.md`, `docs/ARCHITECTURE.md`.
  - `tdflite-ideas/`, `private/`, and the DeepMind PDF.
- **Relayed, not verified.** Line numbers outside the ranges listed at the top are the proposals' and the critique's.
- **Positions per frame.** I did not check which frames have no verb-phrase form, so the list of frames that keep the "For" voice in row 12 is unverified.
- **Breakage counts.** I did not count how many Rule lines rows 4, 5, 6 and 12 break.
- **Privacy.** Open question 5 and row 16's note draw on the critique's paraphrase of git-ignored `tdflite-ideas/`. Check the rule in `AGENTS.md` before copying either into a tracked file.