# K1, first target: the rule pack "validated input" on the toy parser `kvparse`

What was measured on 2026-11-12, negative results first. Frozen beforehand: `pack.yaml`, `FREEZE.md` (commit
`57fb44b`), `kvparse/expected.json` (commit `19950b3`), the mutants (commit `f328f23`). Commands are run from
`clausal/`.

**Fix round (same day, after a review by another model).** Section 0 is new and comes first: it corrects three
things the first version of this file got wrong or left out. What was frozen for it, before its runs:
`FIXROUND.md` (commit `f1086e2`). Sections 1 to 6 are the first measurement, rerun in full after the fix, with the
changed lines marked "(fix round)".

## 0. Fix round: three corrections, negative results first

1. **A bug that is not on the list passes. 3 of 3 mutants outside the frozen list are shown false by no pack rule in
   a pipeline run, and 2 of them leave the run green** (exit 0, all 127 verdict codes the baseline's,
   `kvparse/expected.json` met, both proofs kept, the crate's four unit tests passing).

   | Mutant | Whose | Pipeline run | Rules false of it, and where | Wider search (not a verdict) |
   |---|---|---|---|---|
   | R1: `:` taken as a digit, value 10 | reviewer's | green; no rule found false | VI-2, VI-6, VI-7b, VI-10 at `a=:` (3 bytes) | VI-2, VI-6, VI-7b, VI-10 |
   | R2: one trailing newline accepted (a sibling of seeded bug B1) | reviewer's | green; no rule found false | VI-2, VI-6, VI-7b, VI-10 at `a=1\n` (4 bytes) | VI-2, VI-6, VI-7b, VI-10 |
   | R3: a trailing `\r\n` accepted | builder's, fix round | exit 1, no rule found false; VI-4 and VI-5 lose their proofs (the loop lemma no longer checks) | VI-2, VI-6, VI-7b, VI-10 at `a=1\r\n` (5 bytes) | **none** |

   - **"9 of 9" below measures the grid, not the suite.** The only search of a kvparse rule is the grid of 240 inputs.
     Its 30 messages were written by the builder with the frozen bug list in hand, one or more per listed bug. The
     nine listed mutants are found at exactly those messages. The count says the grid hits the bugs it was written
     for. It does not say what the instantiated suite finds of a bug nobody listed; the three rows above are the
     only measurement of that, and it is 0 of 3.
   - **The grid cannot write R2's input at all.** The literal type of a message is `"[ !#-~]*"`: printable ASCII. A
     newline, any other control byte and any byte above 0x7F cannot be a grid message. `:` can, and is not one.
   - **The flag on the rules points the wrong way.** All 8 unproved rules carry LARGER INPUTS NOT EXAMINED. The
     three failures are at 3, 4 and 5 bytes; the grid covers those lengths.
   - **`pack check` read "10 stated", and VI-2's comment reads "nothing outside the format is accepted".** A stated
     member is a sentence that compiles. Nothing in that line says the rule was searched past the grid. The line now
     says so itself.
   - **What the fix round adds is a search, not a verdict.** `wallet-bdd/tests/kv_wide.rs` evaluates the ten rules on
     the compiled Rust at 10 limits by 429,505 messages (every byte string of length 0 to 2; every record of the
     format with every one-byte substitution, insertion and deletion). On the unmutated parser no rule is false at
     any of the 42,950,500 points. It finds R1 and R2 and, as predicted when it was frozen, not R3. Limits of it:
     it is not part of `./run.sh`, so R1 and R2 still pass a green run; it uses the Rust readings of the words, so
     nothing it finds is confirmed on the Lean model; its input set was chosen after R1 and R2 were known and
     contains both of their inputs; it sees nothing two or more byte edits from every record and longer than two
     bytes. Feeding its finds back as counterexamples needs a literal type that can write any byte; not done.
   - One frozen expectation of the fix round was wrong: R3 was expected to leave the run at exit 0. It exits 1,
     through the two lost proofs. No rule is found false, as expected.

2. **VI-7b claimed more than it checked** (the study's risk 6: content smuggled through a slot word). Its `says:`
   reads "excludes a wrong or default value and a dropped field". On the first version of the project's encoder that
   was false: `KV.encode` wrote `48 + digit` for any digit, so a parse that answers the value 10 for `a=:` (R1) had
   `a=:` as the encoding of its result and VI-7b held of it. The first version of this file presented VI-7b as one
   of the two members that pin the value. It did not pin it.
   - Fixed in the project's word, not in the pack: `KV.encode` is partial. A record has an encoding only if the
     format can write it (at least one key given, each digit at most 9, digit 0 for a key not given). Same change in
     the Rust reading (`kv_encode`). The sentence, the form and the pack are unchanged.
   - Proved: `KV.encode_inj` (`lean/Kvparse/Lemmas.lean`; axioms `propext`, `Quot.sound`): two records with the
     same encoding are the same record. So where VI-7b holds of an accepted parse, the bytes leave one record the
     answer can be. Not proved: that every encoding is a well-formed message.
   - Measured: under R1, VI-7b is now false at `a=:` (wider search; first version: true there, by the reviewer's
     evaluation). The pipeline still does not find it, because the grid has no such message (correction 1).
   - What stays true of the pack: a slot's `means:` is checked by nothing. VI-7b says what its `says:` reads only
     if the project's encoder is injective and writes only the format. The pack cannot tell.

3. **The stateability figure is a property of how kvparse was built, and it has a range.** "1 of 11 cannot be
   stated" holds for the choices the builder made in the target after reading the study: the limit is a field of
   the parser's state, the format is canonical, unknown and repeated keys are rejected.

   | Choice (same command, `--dry-run`) | Cannot be stated |
   |---|---|
   | kvparse as built | 1 of 11 (9%): VI-7a |
   | lenient format, duplicates last-wins | 3 of 11 (27%): VI-7a, VI-7b, VI-9 |
   | a limit that is a constant (slot `limit` filled with "the field limit") | 3 of 11 (27%): VI-7a, VI-3, VI-4 |
   | both | **5 of 11 (45%): above the target of a third** |
   | no size limit (`size=unbounded`) | 1 of 11, 2 not applicable |

   A stateless parser with a constant limit and a lenient format is an ordinary parser. The figure to carry forward
   is "1 to 5 of 11, depending on the target", not "9%".

**Runs of the fix round.** One full `./run.sh` on the tree: exit 0; 112 of 112 verdict codes of the wave's baseline
identical; 127 of 127 identical to the first measurement's full run (`python3 compare/against/verdicts.py 89f5d91`);
`kvparse/expected.json` met; `book check` as expected; `pack check` no drift. Ten bounded-check rungs of the ledger
answered `timeout` where the earlier full run answered `verified` (machine load about 30); no verdict depends on
them, none is a kvparse rule. Strip test rerun: 0 of 127 verdict codes differ.

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
     (fix round) This number comes from a grid written for these nine: see 0.1 before quoting it.
   - The frozen criterion was written without knowing this. It is not changed here; both numbers are reported.
2. **The pack reads INCOMPLETE on its first target**: 10 of 11 members stated. VI-7a (round trip as a sequence) cannot
   be stated. `out/report.md` does not say so: the pipeline does not read packs, so the report shows ten rules and
   no sign of the eleventh. Only `python3 -m clausal pack check` prints the line.
3. **The default-value bug (B6) is shown false by VI-7b and VI-10 only**, as the study predicted. VI-7b is a
   workaround member whose content is a specification-level encoder (fix round: the first encoder let a wrong value
   through, see 0.2); VI-10 needs the whole reference parse. Without
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
   (fix round) Bugs off the list pass this grid at 3 to 5 bytes: see 0.1.
9. **All 9 mutants are also caught by the crate's four unit tests**, written by the same builder.

## 2. The study's tests

| Test | Result | Counts against? |
|---|---|---|
| Strip tags, delete the pack | `packs/`, `clausal/pack.py` and the bindings file deleted, `@pack` tags stripped: **0 of 127 verdict codes differ** | no |
| Seeded bug list | REFUTED: 0 of 7 bug mutants. COUNTEREXAMPLE reproduced on the compiled Rust: 7 of 7, on a grid written for these seven. See 1.1 and 0.1 | by the frozen criterion, yes |
| (fix round) Mutants outside the list: R1, R2 (reviewer's), R3 (builder's) | shown false by a pack rule in a pipeline run: **0 of 3**; green run on 2 of 3. Wider search, not a verdict: 2 of 3. See 0.1 | **yes** |
| Adequacy expectation (trivial implementations) | REFUTED: 0 of 3. COUNTEREXAMPLE: 3 of 3 (return-a-default is B6) | as above |
| Stateability | 1 of 11 members cannot be stated on kvparse as built (9%; target at most a third); **1 to 5 of 11 over the pack's variants and a constant limit (5 of 11 = 45%, above the target)**: see 0.3. 0 edits of `clausebook/core.yaml` or `lean/Frames` | on kvparse as built, no; for a stateless lenient parser, yes |
| Reuse across two targets | not in this step | – |
| Against a hand-written suite by an author blind to the pack | not in this step | – |
| TDFLite recall | not in this step; predicted slot fills in `SECOND_TARGET.md` | – |

## 3. Members on kvparse

`python3 -m clausal pack check`:

    pack validated-input@1 on kvparse: INCOMPLETE: 11 members: 10 stated (3 of them through a workaround word: VI-7b, VI-8, VI-9), 0 waived, 0 not applicable, 1 CANNOT BE STATED (VI-7a: ...). STATED means only that the sentence compiles with the project's words: it does not mean the rule was examined beyond the project's own search inputs, nor that the words mean what the slots ask (`means:`); the count depends on the variants and on how the project's words are built

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

Every verdict is the one frozen in `kvparse/expected.json` (`python3 kvparse/check_expected.py`). The last column
lists mutants of the frozen list only; no rule shows R1, R2 or R3 false in a pipeline run (0.1).

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

(fix round) Rerun after the encoder change: the same sets. In the wider search every rule the pipeline finds false
is false too; B2 has VI-9 in addition (at `;=0`). The mutants outside the list are in 0.1 and in
`results/kvparse_mutants.md`.

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
| Lean definitions of the words: the format a second time | `lean/Kvparse/Pieces.lean`, 120 lines (fix round: 131) |
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
| Strip test, all mutants (frozen list and R1 to R3), wider search after each | `../tools/sem.sh 3 -- python3 packs/validated-input/kvparse_mutants.py` (fix round: 14 pipeline runs, 72 minutes of pipeline at load about 30, plus 13 wider searches) |
| Wider search on the tree as it is (after `./run.sh` or `python3 -m clausal gen`) | `cd wallet-bdd && cargo test --release --quiet --test kv_wide`: `FALSE: no rule`, exit 0; result in `out/kv_wide.json` |
| `KV.encode_inj` and its axioms | `cd lean && lake env lean` on a file with `import Kvparse.Lemmas` and `#print axioms KV.encode_inj` |
| Stateability range (0.3) | `python3 -m clausal pack instantiate validated-input --project kvparse --bindings features/kvparse_rules.pack.validated-input.yaml [--variants canonical=lenient duplicates=last-wins] [--slots limit="the field limit"] --dry-run` |
| Tables of section 4 from the stored record | `python3 packs/validated-input/kvparse_mutants.py --resummarise` |
| A constant limit cannot be compared | compile "A parse is accepted only if the length of the message is at most the field limit": UNBOUND |
