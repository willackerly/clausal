# Clausal readability: presentation without a second text

Read-only review; nothing was built or run. The directory rename landed while I worked, so paths below use `clausal/`. Every concrete case is hand-worked from the fixture description in `trials/meaning/brief.md`, not tool output.

## 1. Findings that shape the proposal

1. **The bad sentence is not what the Clausebook produces.** `README.md:67` puts the frame's name into the sentence ("more-never-loses"). Frame 12's only surface forms are "never loses acceptance when {variation}" and "never loses that {class} when {variation}" (`clausal/clausebook.yaml:932`). Compare `clausal/features/ledger_rules.feature:72`: "A transfer never loses acceptance when the amount is smaller".
2. **`README.md:68` names the wrong frame.** It pairs `never changes` with a `permutation` variation. `Frames.NeverChanges` takes a one-run measure (`clausal/lean/Frames/Frames.lean:26`); a variation needs frame 14, `IndependentOf` (`Frames.lean:170`), whose surface is "gives the same answer when …".
3. **No sentence in the repository carries its defaults.** `docs/HANDOFF_CLAUSAL.md:41` and `docs/PLAN.md` (adjustment 1) say the defaults are "written out in the sentence". No Rule line in `clausal/features/*.feature` contains one. D1 to D10 exist only in the generated Reading (`clausal/clausebook.yaml:74`, `clausal/out/report.md`).
4. **The echo was always a deterministic function of the parse tree.** `echo_rule` (`clausal/clausal/vocab.py:1112`) is called inside `Compiler.rule` on every compile. `docs/HANDOFF_CLAUSAL.md:17` says it "drifts from `.feature` files"; I found no mechanism by which it could. Its measured weakness is different: readers comparing two texts missed 5 of 60 wrong echoes, all in the scope and condition slots, and in 3 of those 5 described a condition the echo did not contain (`trials/sentences/RESULTS.md:95`).
5. **"One canonical sentence per meaning" is already false of the file.** By reading the code, not by running the compiler:
   - `aggregate` has two forms (`clausebook.yaml:589`), `l.balances_of` four (`:255`), and `l.balance_at` and `l.the_transfer` two each.
   - "is always accepted" / "always succeeds" and "is never accepted" / "is always rejected" are hard-coded pairs (`vocab.py:1009-1010`).
   - Three idioms are kept (`clausebook.yaml:1035`).
   - `Compiler.clause` (`vocab.py:952`) accepts both "A transfer never changes X" and "For a transfer, X is unchanged".
6. **"if it is rejected" has two meanings by position.** After "For X," it narrows coverage to rejected calls (`vocab.py:1017`). At the end of frame 16 it is a condition on the first run, with both calls still required to answer (`Frames.lean:193`).
7. **Sign-off is per Clausebook piece, not per sentence.** The piece digest covers the whole YAML entry, including its `echo` template, plus the Lean definitions (`clausal/clausal/vreport.py:147,174`). I found no rule-level signature.
8. **Gherkin limits.** The Rule name is one line; text under it is carried verbatim and not compiled (`clausal/clausal/core.py:114-122`). Data tables on steps are refused (`core.py:241`). Other runners treat the Rule name as a label, and the tag and description are the two extension points that survive (`out/prior_art_vocabulary.md:178-179`).

## 2. Mechanism

One accepted form per meaning stays. Nothing below adds an accepted phrasing, so the reasons for the no-synonyms rule are untouched.

| Layer | What | Signed? | Can it change the Lean? |
|---|---|---|---|
| S1 Sentence | The Clausal words, as today | Yes | It is the only input |
| S2 Layout | Line breaks and indentation from `clausal fmt` | Yes, but the hash is over whitespace-normalised words | No: the compiler receives the same string |
| S3 Checked brackets | Optional `( )` around a nested term | Yes | No: stripped before parsing, then checked against the unique parse |
| D1 Gloss | `=` lines under the rule: covers, assuming, means, silent on | No: regenerated and compared on every compile | No: nothing reads it |
| D2 Outcome table | For two-run frames, the truth table of the frame's `flat` | No | No |
| D3 Cases | One allowed and one forbidden concrete case, plus the nearest neighbouring sentence with an input where they differ | No | No |
| D4 Editor | Hover per piece, colouring from the parse tree, two-run side-by-side view | No | No |

**S2 Layout.**
- The sentence runs from `Rule:` to the first line ending in a full stop; free description follows a blank line.
- `fmt` breaks only at parse-tree joints: clause joins (", and"), "for which", the frame's verb phrase, and the frame's second-hole keyword (when, only if, whenever, exactly when, ", if").
- Indentation is tree depth. Sentences under the width limit stay on one line.
- The compiler refuses any other layout. This matters because a hand-placed break can suggest a parse the compiler did not take.

**S3 Checked brackets.** A bracket pair must coincide with a node of the parse, and the sentence must parse uniquely without it. The moment a bracket selects a parse it has become grammar, and this proposal does not cover that.

**D1 Gloss.** It sits in the description so it shows in diffs and cucumber reports. It has fixed slots and a closed set of "covers" values, one per constructor of `Calls` (`clausal/lean/Frames/Core.lean:29`). A stale gloss is a compile error.

**D3 Cases.** A case is (state, input, outcome). Whether the rule allows it is found by evaluating the frame's own `.at` statement on a constant operation returning that outcome. The case is therefore computed from the Lean meaning, not assembled from English templates. Neighbours come from the five mutation kinds already in `trials/meaning/banks/generated-echoes-v1/mutate.py:188`. Cases are not pinned in the file because they depend on the search grid version.

**Is the gloss the echo coming back?** Partly, yes.
- **Where it is:** the "means" and "covers" lines are `echo_rule`'s output, shortened and moved into the file. A wrong template misleads every reader the same way.
- **What differs is operational only:** the gloss is never an input, it is compared byte for byte on compile, its templates sit inside the signed piece digest, and no reader is asked to compare two texts.
- **What is new in kind:** D2 and D3. They come from evaluating the statement, and they target the scope slot that readers missed.

## 3. Ten sentences

The words change only in T1 to T3, where the README sentence is not in the Clausebook's forms; that is a correction, not this mechanism. The ABAC domain words are invented here because `clausebook/abac` does not exist.

**T1. `README.md:67`: more entitlements**
```
Rule: A key release
        never loses acceptance
        when the subject gains an entitlement.

  = covers   every pair of calls related as below; both must answer   [D1 D2 D10]
  = run 2    same request and policy; the subject holds all it held in run 1, or more
  = means    if run 1 is accepted, run 2 is accepted
  = silent   when run 1 is rejected
```
| run 1 | run 2 | rule |
|---|---|---|
| accepted | accepted | allowed |
| rejected | accepted | allowed |
| rejected | rejected | allowed |
| accepted | rejected | **forbidden** |
| either gives no answer | | **forbidden** |

Lean: `Frames.Monotone op more accepted` (`Frames.lean:154`), the frame the README names. "Or more" is printed because existing variations are non-strict (`clausebook.yaml`, `l.smaller_amount` echo), which caused two of the three false alarms in the echo trial (`trials/sentences/RESULTS.md:13`).

**T2. `README.md:68`: attribute order**
```
Rule: A key release
        gives the same answer
        when only the order of attributes differs.

  = covers   every pair of calls related as below; both must answer   [D1 D2 D10]
  = run 2    same token and manifest contents, attributes in any order
  = means    the two answers are equal
```
Lean: `Frames.IndependentOf` with the answer as the view. This is a different frame from the README's label, for the reason in finding 2. "In a token or manifest" becomes one variation covering both, or two "and" clauses; that is a Clausebook decision.

**T3. `README.md:66`: only if**
```
Rule: A key release
        is accepted only if
        every attribute of the data is satisfied by the subject under its rule.

  = covers   every call, accepted or rejected; the call must answer   [D1 D2]
  = means    if accepted, then before the call every data attribute was satisfied   [D5 D8]
  = silent   on whether a satisfied request is accepted
  = allowed    subject {secret}, data {secret}: rejected
  = forbidden  subject {secret}, data {secret, nato} under allOf: accepted
  = not the same as  "... is accepted exactly when ...": differs on the allowed case above
```
Lean: `Frames.OnlyIf op accepted C` (`Frames.lean:62`).

**R1. Two-run frame: `ledger_rules.feature:98`**
```
Rule: A transfer
        gives the same answer
        when the amount is larger,
        if it is rejected.

  = covers   every pair of calls related as below; both must answer   [D1 D2 D10]
  = run 2    same ledger, sender and receiver; amount the same or larger
  = means    if run 1 is rejected, run 2 gives the same answer
  = note     "if it is rejected" is a condition on run 1; it does not narrow coverage
```
Allowed: `[5,5]`, `0->1:6` rejected and `0->1:9` rejected. Forbidden: the first rejected, the second accepted.

**R2. Narrowed to rejected, three clauses: `ledger.feature:130`**
```
Rule: A transfer
        is accepted exactly when the transfer is valid on the ledger,
      and a rejected transfer
        never changes the ledger,
      and for a successful transfer,
        the amount of the transfer has moved between its accounts in the ledger
        and no other balance changed.

  = clause 1 covers  every call; must answer                           [D1 D2]
  = clause 2 covers  ONLY rejected calls; no-answer calls are outside   [asked for]
  = clause 3 covers  ONLY accepted calls; no-answer calls are outside   [asked for]
```

**R3. Nested condition: `ledger_rules.feature:32`**
```
Rule: A transfer
        is accepted only if
        the amount of the transfer is not more than
        the balance of account (the sender of the transfer) of the ledger.

  = covers   every call; must answer   [D1 D2]
  = means    if accepted, then before the call amount <= sender's balance   [D8]
  = allowed    [100,20,0], 0->0:30: rejected
  = forbidden  [5,5], 1->0:6: accepted
```

**R4. Condition with "some" and "not": `ledger_rules.feature:115` (expected refuted)**
```
Rule: A batch applied as a whole
        for which some transfer of the batch is not valid on the ledger
        is always rejected.

  = covers    every call in scope; must answer   [D1 D2]
  = assuming  at least one transfer is not valid on the ledger as it stands
              BEFORE the batch starts   [D8 D9]
  = forbidden [5,0,0], [0->1:5, 1->2:5]: accepted
```
The forbidden case is what correct code does, which is why the rule is refuted.

**R5. Collection frame: `ledger_rules.feature:67`**
```
Rule: For a batch,
        every transfer at which the batch stopped
        is not valid on the ledger afterwards.

  = covers   every call; must answer   [D1 D2]
  = means    no stopped-at transfer is valid on the ledger AFTER the call   [D7 D9]
```

**R6. If-then: `ledger_rules.feature:154`**
```
Rule: A transfer is accepted whenever the transfer is valid on the ledger.

  = covers   every call, valid or not; must answer   [D1 D2]
  = silent   on the answer when the transfer is not valid
  = not the same as  "A transfer for which the transfer is valid on the ledger
                      is always accepted": differs on an invalid transfer that
                      gives no answer (forbidden here, outside that rule)
```

**R7. Sequence: `ledger.feature:304`**
```
Rule: A batch followed by a computation of the total
        is accepted exactly when
        the total of the balances of the ledger is at most the maximum.

  = covers   every call of the sequence; every step must answer   [D1 D2]
  = means    the LAST call's answer is an acceptance exactly when the condition
             held BEFORE the first call   [D8]
```

**Why the Lean is identical for R1 to R7.** The compiler input is the Rule line joined with single spaces, brackets removed and the full stop stripped; `vocab.py:916` already strips it. That string equals today's `rule.name`. The test is that the generated readings under `clausal/lean/Generated` are byte-identical before and after `fmt` on all four feature files. I did not run it.

## 4. What could go wrong

- **The gloss gets read in place of the sentence.** Then the signed text is unread and a wrong template is trusted. The trial below includes a bare-sentence post-test to measure this.
- **A bad canonical form stays bad.** "The balance of account the sender of the transfer of the ledger" reads poorly with or without brackets. Replacing a form is allowed under the rule; adding one is another proposal.
- **Bare-sentence readers see no defaults.** Anyone reading the sentence outside the file (a cucumber label, a quotation) sees none. That is weaker than what the plan states. A mandatory coverage slot in the sentence would meet it literally, at the cost of length; it is a form change outside this angle.
- **Truncated labels.** Multi-line sentences appear in other runners as their first line only.
- **One pair of cases anchors the reader.** It cannot show quantifier scope. A rule false only at large sizes, such as `ledger_rules.feature:137`, will print "no forbidden case found within bounds" beside a false rule.
- **File length and friction.** Rule blocks roughly triple in length, and a refused layout adds a step to every edit.
- **Migration.** Existing free text sits directly under Rule lines with no blank line (`ledger_rules.feature:53, 79, 116, 127`) and would be read as continuation.

## 5. Measuring whether it helped

Build a new bank, `trials/meaning/banks/presentation-v1/`, in H2 part-one shape.

- **Item:** a sentence plus one concrete case; the question is "does this outcome break the rule?". `score.py`'s catch and false-alarm arithmetic applies if "breaks" maps to "not-faithful". The item schema needs an `arm` field, and the runner and HTML need to render it.
- **Arms:** A, the one-line sentence; B, layout; C, layout and gloss; D, layout, gloss and cases. The same items rotate across arms between readers.
- **Items:** drawn by a seeded rule from compiled rules. Four trap kinds with at least eight breaking and eight non-breaking items each: rejected call, no-answer call, boundary equality, and second-run or converse direction. Cases shown in arm D are never the tested case.
- **Post-test:** 16 bare sentences after arm D.
- **Readers:** four labelled proxy models, then the owner and at least two others, reported separately.

Thresholds, to be committed before any run:

| Outcome | Condition |
|---|---|
| Helped | Arm D error on trap items is at most half of arm A's and at least 10 points lower; the resampled 95% interval of the difference (items and readers) excludes zero; false alarms rise by no more than 5 points; median time per item is at most 1.5 times arm A's |
| Hurt | Error or false alarms rise by more than 5 points, or post-test error exceeds arm A's by more than 5 points |
| Unclear | Anything else |

With three people only the direction is reportable.

The alias rule in the task applies to the layout and neighbour rules instead, since I propose no alias list. Both are defined on tree shape and mutation kind, not fitted to the 48 frozen sentences. I read 16 of the 48, for failure kinds only.

## 6. Cost

Estimates, unmeasured, in agent-days with review:

| Piece | Days |
|---|---|
| `fmt`, layout check and full-stop migration | 2 |
| Gloss from `echo_rule` plus compile-time comparison | 1 |
| Outcome tables | 0.5 |
| Cases through constant-operation evaluation and neighbour search (overlaps L3) | 3 to 4 |
| Editor grammar and hover | 2 to 3 |
| Bank, runner changes and proxy run | 2 to 3 |
| **Total** | **11 to 14**, plus people's time |

## 7. Not checked

- I did not run the compiler, `lake`, or any script. Finding 5's "both shapes compile" claim and the byte-identity claim are from reading code.
- I did not read `private/`, or `tdflite-ideas/` beyond the guarantees table. I read only the section headings and keyword matches in `out/prior_art_vocabulary.md`, and 16 of the 48 frozen sentences (`trials/sentences/authors.json`).
- I did not check whether parse nodes keep text spans, which `fmt` needs.
- I did not check how cucumber-rs 0.23 displays a multi-line description.
- I did not check whether any L3 separating-input code exists outside `clausal/clausal/`; a search inside it found none.
- I did not check whether a class form "it is accepted" makes monotone's two forms true synonyms.