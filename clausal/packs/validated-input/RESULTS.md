# K1, first target: the rule pack "validated input" on the toy parser `kvparse`

What was measured on 2026-11-12, negative results first. Frozen beforehand: `pack.yaml`, `FREEZE.md` (commit
`57fb44b`), `kvparse/expected.json` (commit `19950b3`), the mutants (commit `f328f23`). Commands are run from
`clausal/`.

## 1. Negative results

1. **By the criterion frozen for this step, no seeded bug and no trivial implementation is shown false: 0 of 9.**
   `FREEZE.md` says a mutant is shown false if a pack rule gets the verdict REFUTED, which needs a kernel-checked
   theorem at the counterexample. On every mutant the pipeline's verdict was `COUNTEREXAMPLE FOUND (not confirmed in
   the kernel)` instead: the rule's reading is false at a grid input on the Lean model and false at the same input on
   the compiled Rust (34 rule-and-mutant pairs over the 9 mutants), and no kernel-checked refutation was produced for any.
   - Why the kernel script fails: it steps through the model at the input, and for a loop it needs a hand-proved lemma
     saying what the loop computes. `kvparse` has none (its lemma says only that the loop ends). A lemma written for
     the unmutated loop would not hold of a mutated one either.
   - By the count `mutation/run_mutants.py` uses for the other projects (REFUTED or COUNTEREXAMPLE): **9 of 9**.
   - The frozen criterion was written without knowing this. It is not changed here; both numbers are reported.
2. **The pack reads INCOMPLETE on its first target**: 10 of 11 members stated. VI-7a (round trip as a sequence) cannot
   be stated. `out/report.md` does not say so: the pipeline does not read packs, so the report shows ten rules and
   no sign of the eleventh. Only `python3 -m clausal pack check` prints the line.
3. **The default-value bug (B6) is shown false by VI-7b and VI-10 only**, as the study predicted. VI-7b is a
   workaround member whose content is a specification-level encoder; VI-10 needs the whole reference parse. Without
   those two the suite is satisfied by a parser that accepts the right inputs and answers the wrong record.
4. **Three more mutants are shown false only through the specification's own parser.** With VI-10, VI-7b and the
   three rules that use the `well-formed` word left out (VI-2, VI-3, VI-6): trailing garbage (B1), the limit rejected
   one byte early (B5a) and reject-everything are shown false by nothing (nor is B6). What catches them is the project's word, not
   the pack's sentence.
5. **Two members never showed a mutant false: VI-1 and VI-5.** No mutant panics. VI-5 ("the number of fields of the
   result is at most the field limit") is true of any answer of this type once the call answers; it constrains this
   parser in nothing but that.
6. **VI-4 and the bounded VI-3 are stateable on kvparse only because the parser was given a state.** Core compares a
   value known before the call with a quantity of the state ("X is at most Y"); it has no order comparison of two
   values known before the call. With the limit as a constant both sentences are refused UNBOUND (tried:
   "A parse is accepted only if the length of the message is at most the field limit"). The target was designed
   around this by the builder, after reading the study.
7. **Two frozen expectations were wrong in their reasons, right in their codes.** `expected.json` said VI-5 is proved
   without looking at the code. It is not: every default-scope obligation also asks that the call answers (default
   D1), so VI-4 and VI-5 each needed a proof that the loop ends. That lemma also proves VI-1, which stays TESTED-ONLY
   because its expected verdict was frozen as such and no proof file was written.
8. **Only the grid looks at these rules.** `clausal/evgen.py` has no typed reading of the kvparse words, so no generated
   property test and no bounded check examines a kvparse rule. The grid is 240 inputs (8 size limits by 30 messages)
   written by the builder, who knew the bug list. All 8 unproved rules carry the flag LARGER INPUTS NOT EXAMINED.
9. **All 9 mutants are also caught by the crate's four unit tests**, written by the same builder.

## 2. The study's tests

| Test | Result | Counts against? |
|---|---|---|
| Strip tags, delete the pack | `packs/`, `clausal/pack.py` and the bindings file deleted, `@pack` tags stripped: **0 of 127 verdict codes differ** | no |
| Seeded bug list | REFUTED: 0 of 7 bug mutants. COUNTEREXAMPLE reproduced on the compiled Rust: 7 of 7. See 1.1 | by the frozen criterion, yes |
| Adequacy expectation (trivial implementations) | REFUTED: 0 of 3. COUNTEREXAMPLE: 3 of 3 (return-a-default is B6) | as above |
| Stateability | 1 of 11 members cannot be stated (9%; target at most a third). 0 edits of `clausebook/core.yaml` or `lean/Frames` | no; but see 1.6 |
| Reuse across two targets | not in this step | – |
| Against a hand-written suite by an author blind to the pack | not in this step | – |
| TDFLite recall | not in this step; predicted slot fills in `SECOND_TARGET.md` | – |

## 3. Members on kvparse

`python3 -m clausal pack check`:

    pack validated-input@1 on kvparse: INCOMPLETE: 11 members: 10 stated (3 of them through a workaround word: VI-7b, VI-8, VI-9), 0 waived, 0 not applicable, 1 CANNOT BE STATED (VI-7a: ...)

| Member | Sentence written | Verdict | Mutants it shows false (COUNTEREXAMPLE) |
|---|---|---|---|
| VI-1 | A parse always answers | TESTED-ONLY | none |
| VI-2 | A parse is accepted only if the message is well-formed | TESTED-ONLY | B1, B2, B3, B4, accept-all |
| VI-3 | A parse for which the length of the message is at most the parser's size limit is accepted whenever the message is well-formed | TESTED-ONLY | B5a, reject-all |
| VI-4 | A parse is accepted only if the length of the message is at most the parser's size limit | PROVED-FOR-ALL | B5b, accept-all |
| VI-5 | For a parse, the number of fields of the result is at most the field limit | PROVED-FOR-ALL | none (proof lost on 4) |
| VI-6 | A parse for which the message is not well-formed is rejected and changes nothing | TESTED-ONLY | B1, B2, B3, B4, accept-all |
| VI-7a | – | cannot be stated | – |
| VI-7b | For an accepted parse, the encoding of the result is the bytes of the message | TESTED-ONLY | B1, B2, B3, B4, B6, accept-all |
| VI-8 | A parse is accepted only if every field of the message is a known field | TESTED-ONLY | B2, B4, accept-all |
| VI-9 | A parse is accepted only if no key of the message is repeated in the message | TESTED-ONLY | B3, accept-all |
| VI-10 | A parse agrees with the reference parse | TESTED-ONLY | all 9 |

Every verdict is the one frozen in `kvparse/expected.json` (`python3 kvparse/check_expected.py`).

**What cannot be stated, and the piece each needs.**

| Member or choice | Needs |
|---|---|
| VI-7a, round trip as a sequence | a sequence whose second call takes the first call's *answer* as its input (the tie of core takes the first call's input), and a claim that the last answer is the first input. The draft is refused UNBOUND |
| VI-7b for a lenient parser | a specification-level canonical form of an input. The pack has no sentence |
| VI-9 for first-wins or last-wins | a sentence form for "the value of a repeated key is its first / last occurrence". The pack has no sentence |
| VI-4 and bounded VI-3 for a limit that is a constant | an order comparison of two values known before the call. Not met on kvparse (1.6); will be met by any stateless parser |

Not exercised on kvparse: the `ignore` and `preserve` sentences of VI-8 (the target rejects unknown keys). Their
shapes compiled with ledger words standing in for the slots at the freeze; that is all that is known.

## 4. Mutants

Full table with the falsifying input of every rule: `results/kvparse_mutants.md` (and `.json`).

| Mutant | Shown false by (COUNTEREXAMPLE) | The pack's `by:` | Without VI-10 and VI-7b |
|---|---|---|---|
| B1 trailing garbage accepted | VI-2, VI-6, VI-7b, VI-10 | VI-2, VI-7b, VI-10 | VI-2, VI-6 |
| B2 unknown item skipped | VI-2, VI-6, VI-7b, VI-8, VI-10 | VI-8, VI-2, VI-10 | VI-2, VI-6, VI-8 |
| B3 duplicate key, last wins | VI-2, VI-6, VI-7b, VI-9, VI-10 | VI-9, VI-2, VI-7b, VI-10 | VI-2, VI-6, VI-9 |
| B4 case mismatch | VI-2, VI-6, VI-7b, VI-8, VI-10 | VI-8, VI-2, VI-10 | VI-2, VI-6, VI-8 |
| B5a limit: exactly the limit rejected | VI-3, VI-10 | VI-3 | VI-3 |
| B5b limit: one byte more accepted | VI-4, VI-10 | VI-4 | VI-4 |
| B6 default value returned | VI-7b, VI-10 | VI-7b, VI-10 | **none** |
| reject-everything | VI-3, VI-10 | VI-3 | VI-3 |
| accept-everything | VI-2, VI-4, VI-6, VI-7b, VI-8, VI-9, VI-10 | VI-2 | VI-2, VI-4, VI-6, VI-8, VI-9 |

Every member the pack's `by:` names for a mutant did show it false. No verdict of another project changed on any
mutant. Proofs lost (PROVED-FOR-ALL to TESTED-ONLY, not counted as shown false): VI-5 on B5a, B5b and both trivial
implementations; VI-4 on B5a and reject-everything.

## 5. Cost of the first instantiation

The pack's sentences cost one command. The words they are about cost the rest.

| What | Size |
|---|---|
| Slots of the pack / filled on kvparse | 18 / 14 (the study names 5) |
| Words written for the fills | 1 operation and 12 pieces (`clausebook/local/kvparse.yaml`, 152 lines) |
| The parser | 85 lines, 64 of them code |
| Lean definitions of the words: the format a second time | `lean/Kvparse/Pieces.lean`, 120 lines |
| Rust readings of the words: the format a third time | `wallet-bdd/src/pieces.rs`, 118 lines added |
| Lemmas and the two proofs | `lean/Kvparse/Lemmas.lean` 58 lines; two proof files of about 8 lines each |
| Shared files edited to add the project | 11 (below); `clausebook/core.yaml` and `lean/Frames`: 0 |

Edits outside the project's own files: `projects.yaml` (entry), `clausebook/project.yaml` (load order),
`glossary.yaml` (literal types `size` and `bytes`, actor type `parser`), `lean/lakefile.toml` (library),
`lean/Bdd/AuditLinks.lean` (library root), `wallet-bdd/Cargo.toml`, `evidence/Cargo.toml`, `evidence/kani/Cargo.toml`
(path dependency), `wallet-bdd/src/pieces.rs` (readings), `clausebook/terms.lock.json` (ten sentences), `.gitignore`.

What the target met that the study did not foresee:

- **The parser was rewritten twice to translate.** Aeneas refused the first two versions ("Early returns inside of
  loops are not supported yet"): the field checks moved to a helper, and the loop to a function of its own because a
  length check before it put the loop inside an `if`.
- **The role could not be called `input`.** `clausal book check` refuses a role noun core's own text uses. The role
  is `message`.
- **A bare-hole form would have added a book-check violation** ("the input" standing where an encoding is wanted).
  The word is written "the bytes of the message".
- **The first run did not pass**: it stopped at the book check on the two points above, before any verdict. The
  slot fills were changed and the pack instantiated again; the template was not touched.

## 6. Reproduce

| Number | Command |
|---|---|
| Completeness line, no drift | `python3 -m clausal pack check` |
| The ten lines from the frozen template | `python3 -m clausal pack instantiate validated-input --project kvparse --bindings features/kvparse_rules.pack.validated-input.yaml --dry-run` |
| Expected verdicts met | `./run.sh` then `python3 kvparse/check_expected.py` |
| Strip test and all mutants | `../tools/sem.sh 3 -- python3 packs/validated-input/kvparse_mutants.py` (11 pipeline runs, 42 minutes at load 14 to 18) |
| Tables of section 4 from the stored record | `python3 packs/validated-input/kvparse_mutants.py --resummarise` |
| A constant limit cannot be compared | compile "A parse is accepted only if the length of the message is at most the field limit": UNBOUND |
