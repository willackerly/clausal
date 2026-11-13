# K1: seeded bugs and trivial implementations against the pack's rules on kvparse

Written by `packs/validated-input/kvparse_mutants.py` (2026-11-12 14:12:53). Each row is one pipeline run in a scratch copy: `./run.sh --no-unit --quick --no-adequacy --no-heldout`.
The kvparse rules are examined by the grid search on the Lean model and the same grid on the compiled Rust only (240 inputs:
8 size limits x 30 messages, written by the builder, who knew the bug list). No generated property test or bounded check looks at them.

## Read this first: what the pipeline does NOT show false

**3 of 3 mutants that are not in the frozen list (R1, R2, R3) are shown false by NO pack rule in a pipeline run**, while rules of the pack are false of them at inputs of 3 to 5 bytes.
On 2 of them (R1, R2) the run exits 0 and every verdict is the baseline's: a green run.
On R3 the run exits 1 and no rule is found false: VI-4, VI-5 lost their proof (PROVED-FOR-ALL to TESTED-ONLY; the hand-written loop lemma no longer checks on the changed loop). A lost proof says the code changed, not that a rule is false; the rules that lost it are still true of this mutant.
The grid's 30 messages were written to hit the frozen bug list; the counts for the frozen list below measure that targeting,
not what the suite finds of a bug nobody listed. Table: section "Mutants that are not in the frozen list".

Three columns, and they are not the same thing:

- **REFUTED** is the frozen criterion (`FREEZE.md`): the rule's verdict on the mutant is REFUTED, a counterexample confirmed by a
  kernel-checked theorem.
- **COUNTEREXAMPLE** is the verdict `COUNTEREXAMPLE FOUND (not confirmed in the kernel)`: the rule's reading is false at a grid input on
  the Lean model, and false at the same input on the compiled Rust. `mutation/run_mutants.py` counts both verdicts as shown false.
- **Wider search** is NOT a verdict and not part of `./run.sh` (`wallet-bdd/tests/kv_wide.rs`, added in the fix round): the rule is false,
  on the compiled Rust through the Rust readings of the words, at a byte string of length 0 to 2 or at a one-byte edit of a record of the
  format. Not evaluated on the Lean model. Its input set was chosen after R1 and R2 were known.

Baseline: exit 0, 127 verdicts; pack rules: VI-1 TESTED-ONLY, VI-2 TESTED-ONLY, VI-3 TESTED-ONLY, VI-4 PROVED-FOR-ALL, VI-5 PROVED-FOR-ALL, VI-6 TESTED-ONLY, VI-7b TESTED-ONLY, VI-8 TESTED-ONLY, VI-9 TESTED-ONLY, VI-10 TESTED-ONLY

Baseline, wider search: 10 limits x 429505 messages x 10 rules = 42950500 evaluations, 0 could not be evaluated; rules false: none.

**Strip test**: `packs/`, `clausal/pack.py` and the bindings file deleted, `@pack` tags stripped: exit 0, 127 verdicts, **0 verdict codes differ from the baseline**.

## The frozen list

| Mutant | What | Unit tests | Pipeline exit | REFUTED (frozen criterion) | COUNTEREXAMPLE, not confirmed in the kernel | Wider search (not a verdict) | Expected | Proof lost |
|---|---|---|---|---|---|---|---|---|
| B1 | trailing garbage accepted: after a field, a byte that is not `;` ends the record instead of rejecting it | caught | 1 | **NONE** | VI-2, VI-6, VI-7b, VI-10 | VI-2, VI-6, VI-7b, VI-10 | VI-2, VI-7b, VI-10 | – |
| B2 | unknown item skipped: a field with a key that is neither `a` nor `b` is passed over instead of rejected | caught | 1 | **NONE** | VI-2, VI-6, VI-7b, VI-8, VI-10 | VI-2, VI-6, VI-7b, VI-8, VI-9, VI-10 | VI-8, VI-2, VI-10 | – |
| B3 | duplicate key, last wins: a repeated key is accepted and its last value kept | caught | 1 | **NONE** | VI-2, VI-6, VI-7b, VI-9, VI-10 | VI-2, VI-6, VI-7b, VI-9, VI-10 | VI-9, VI-2, VI-7b, VI-10 | – |
| B4 | case mismatch: the keys `A` and `B` are taken for `a` and `b` | caught | 1 | **NONE** | VI-2, VI-6, VI-7b, VI-8, VI-10 | VI-2, VI-6, VI-7b, VI-8, VI-10 | VI-8, VI-2, VI-10 | – |
| B5a | length off by one: an input of exactly the limit is rejected | caught | 1 | **NONE** | VI-3, VI-10 | VI-3, VI-10 | VI-3 | VI-4, VI-5 |
| B5b | length off by one: an input one byte longer than the limit is accepted | caught | 1 | **NONE** | VI-4, VI-10 | VI-4, VI-10 | VI-4 | VI-5 |
| B6 | default value returned: a record is accepted and the default record is answered (= T-default of the adequacy expectation) | caught | 1 | **NONE** | VI-7b, VI-10 | VI-7b, VI-10 | VI-7b, VI-10 | – |
| T-reject-all | trivial implementation: rejects every input | caught | 1 | **NONE** | VI-3, VI-10 | VI-3, VI-10 | VI-3 | VI-4, VI-5 |
| T-accept-all | trivial implementation: accepts every input with one fixed value | caught | 1 | **NONE** | VI-2, VI-4, VI-6, VI-7b, VI-8, VI-9, VI-10 | VI-2, VI-4, VI-6, VI-7b, VI-8, VI-9, VI-10 | VI-2 | VI-5 |

Either verdict (REFUTED or COUNTEREXAMPLE), with the members that pin the value or use the specification's parser left out:

| Mutant | Any pack rule | Without VI-10 | Without VI-10, VI-7b | Without VI-10, VI-7b and the rules that use the well-formed word (VI-2, VI-3, VI-6) |
|---|---|---|---|---|
| B1 | VI-2, VI-6, VI-7b, VI-10 | VI-2, VI-6, VI-7b | VI-2, VI-6 | **NONE** |
| B2 | VI-2, VI-6, VI-7b, VI-8, VI-10 | VI-2, VI-6, VI-7b, VI-8 | VI-2, VI-6, VI-8 | VI-8 |
| B3 | VI-2, VI-6, VI-7b, VI-9, VI-10 | VI-2, VI-6, VI-7b, VI-9 | VI-2, VI-6, VI-9 | VI-9 |
| B4 | VI-2, VI-6, VI-7b, VI-8, VI-10 | VI-2, VI-6, VI-7b, VI-8 | VI-2, VI-6, VI-8 | VI-8 |
| B5a | VI-3, VI-10 | VI-3 | VI-3 | **NONE** |
| B5b | VI-4, VI-10 | VI-4 | VI-4 | VI-4 |
| B6 | VI-7b, VI-10 | VI-7b | **NONE** | **NONE** |
| T-reject-all | VI-3, VI-10 | VI-3 | VI-3 | **NONE** |
| T-accept-all | VI-2, VI-4, VI-6, VI-7b, VI-8, VI-9, VI-10 | VI-2, VI-4, VI-6, VI-7b, VI-8, VI-9 | VI-2, VI-4, VI-6, VI-8, VI-9 | VI-4, VI-8, VI-9 |

By the frozen criterion (REFUTED): 0 of 9 mutants of the frozen list are shown false by a pack rule; not: B1, B2, B3, B4, B5a, B5b, B6, T-reject-all, T-accept-all.
By either verdict: 9 of 9; not: none. The grid was written with this list in hand: read the next section before this number.

## Mutants that are not in the frozen list

R1 and R2 are a reviewer's (another model), written after the first run. R3 is the builder's, written in the fix round as a mutant
the wider search cannot see (its input is two byte edits from a record). `Expected` is what is false at the mutant's input by the definitions.

| Mutant | What | Unit tests | Pipeline exit | REFUTED (frozen criterion) | COUNTEREXAMPLE, not confirmed in the kernel | Wider search (not a verdict) | Expected | Proof lost |
|---|---|---|---|---|---|---|---|---|
| R1 | (reviewer's; sibling of none of the six, a digit-range off by one) `:` is taken as a digit, value 10 | MISSED | 0 | **NONE** | **NONE** | VI-2, VI-6, VI-7b, VI-10 | VI-2, VI-6, VI-7b, VI-10 | – |
| R2 | (reviewer's; sibling of B1) one trailing newline is accepted | MISSED | 0 | **NONE** | **NONE** | VI-2, VI-6, VI-7b, VI-10 | VI-2, VI-6, VI-7b, VI-10 | – |
| R3 | (builder's, fix round; sibling of R2, outside the wider search by construction) a trailing `\r\n` is accepted | MISSED | 1 | **NONE** | **NONE** | **NONE** | VI-2, VI-6, VI-7b, VI-10 | VI-4, VI-5 |

The three inputs at which these mutants differ from the parser, evaluated by the wider search's program at every limit
(`KV_WIDE_AT`; the third is not in the wider search's set). Rules false there, on the compiled Rust:

| Mutant | `a=:` | `a=1\x0a` | `a=1\x0d\x0a` |
|---|---|---|---|
| R1 | VI-2, VI-6, VI-7b, VI-10 | **NONE** | **NONE** |
| R2 | **NONE** | VI-2, VI-6, VI-7b, VI-10 | **NONE** |
| R3 | **NONE** | **NONE** | VI-2, VI-6, VI-7b, VI-10 |

Shown false by a pack rule in a pipeline run (either verdict): 0 of 3.
A pack rule false in the wider search (not a verdict): 2 of 3 (R1, R2); not: R3.

## Where each is false

Pipeline (the grid input the rule's block names; `the_parser` is the size limit):

- B1: VI-2 at `{"the_parser": "4", "the_message": "\"a=1x\""}, on the compiled Rust too (reproduced)`; VI-6 at `{"the_parser": "4", "the_message": "\"a=1x\""}, on the compiled Rust too (reproduced)`; VI-7b at `{"the_parser": "4", "the_message": "\"a=1x\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "4", "the_message": "\"a=1x\""}, on the compiled Rust too (reproduced)`
- B2: VI-2 at `{"the_parser": "3", "the_message": "\"c=1\""}, on the compiled Rust too (reproduced)`; VI-6 at `{"the_parser": "3", "the_message": "\"c=1\""}, on the compiled Rust too (reproduced)`; VI-7b at `{"the_parser": "3", "the_message": "\"c=1\""}, on the compiled Rust too (reproduced)`; VI-8 at `{"the_parser": "3", "the_message": "\"c=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "3", "the_message": "\"c=1\""}, on the compiled Rust too (reproduced)`
- B3: VI-2 at `{"the_parser": "7", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`; VI-6 at `{"the_parser": "7", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`; VI-7b at `{"the_parser": "7", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`; VI-9 at `{"the_parser": "7", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "7", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`
- B4: VI-2 at `{"the_parser": "3", "the_message": "\"A=1\""}, on the compiled Rust too (reproduced)`; VI-6 at `{"the_parser": "3", "the_message": "\"A=1\""}, on the compiled Rust too (reproduced)`; VI-7b at `{"the_parser": "3", "the_message": "\"A=1\""}, on the compiled Rust too (reproduced)`; VI-8 at `{"the_parser": "3", "the_message": "\"A=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "3", "the_message": "\"A=1\""}, on the compiled Rust too (reproduced)`
- B5a: VI-3 at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`
- B5b: VI-4 at `{"the_parser": "2", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "2", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`
- B6: VI-7b at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`
- T-reject-all: VI-3 at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`
- T-accept-all: VI-2 at `{"the_parser": "0", "the_message": "\"\""}, on the compiled Rust too (reproduced)`; VI-4 at `{"the_parser": "0", "the_message": "\"a\""}, on the compiled Rust too (reproduced)`; VI-6 at `{"the_parser": "0", "the_message": "\"\""}, on the compiled Rust too (reproduced)`; VI-7b at `{"the_parser": "0", "the_message": "\"\""}, on the compiled Rust too (reproduced)`; VI-8 at `{"the_parser": "0", "the_message": "\"=1\""}, on the compiled Rust too (reproduced)`; VI-9 at `{"the_parser": "0", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "0", "the_message": "\"\""}, on the compiled Rust too (reproduced)`
- R1: nowhere on the grid
- R2: nowhere on the grid
- R3: nowhere on the grid

Wider search (the first input in its order: shortest message, then byte order, then smallest limit; and at how many of its messages):

- B1: VI-2 at `limit 4, "a=0\x00"` (81700 messages); VI-6 at `limit 4, "a=0\x00"` (81700 messages); VI-7b at `limit 4, "a=0\x00"` (81700 messages); VI-10 at `limit 4, "a=0\x00"` (81700 messages)
- B2: VI-2 at `limit 3, "\x00=0"` (53340 messages); VI-6 at `limit 3, "\x00=0"` (53340 messages); VI-7b at `limit 3, "\x00=0"` (53340 messages); VI-8 at `limit 3, "\x00=0"` (53340 messages); VI-9 at `limit 3, ";=0"` (210 messages); VI-10 at `limit 3, "\x00=0"` (53340 messages)
- B3: VI-2 at `limit 7, "a=0;a=0"` (200 messages); VI-6 at `limit 7, "a=0;a=0"` (200 messages); VI-7b at `limit 7, "a=0;a=0"` (200 messages); VI-9 at `limit 7, "a=0;a=0"` (200 messages); VI-10 at `limit 7, "a=0;a=0"` (200 messages)
- B4: VI-2 at `limit 3, "A=0"` (220 messages); VI-6 at `limit 3, "A=0"` (220 messages); VI-7b at `limit 3, "A=0"` (220 messages); VI-8 at `limit 3, "A=0"` (220 messages); VI-10 at `limit 3, "A=0"` (220 messages)
- B5a: VI-3 at `limit 3, "a=0"` (120 messages); VI-10 at `limit 3, "a=0"` (120 messages)
- B5b: VI-4 at `limit 2, "a=0"` (120 messages); VI-10 at `limit 2, "a=0"` (120 messages)
- B6: VI-7b at `limit 3, "a=0"` (120 messages); VI-10 at `limit 3, "a=0"` (120 messages)
- T-reject-all: VI-3 at `limit 3, "a=0"` (120 messages); VI-10 at `limit 3, "a=0"` (120 messages)
- T-accept-all: VI-2 at `limit 0, ""` (429385 messages); VI-4 at `limit 0, "\x00"` (429504 messages); VI-6 at `limit 0, ""` (429385 messages); VI-7b at `limit 0, ""` (429505 messages); VI-8 at `limit 0, "\x00"` (288170 messages); VI-9 at `limit 0, ";"` (414 messages); VI-10 at `limit 0, ""` (429505 messages)
- R1: VI-2 at `limit 3, "a=:"` (22 messages); VI-6 at `limit 3, "a=:"` (22 messages); VI-7b at `limit 3, "a=:"` (22 messages); VI-10 at `limit 3, "a=:"` (22 messages)
- R2: VI-2 at `limit 4, "a=0\x0a"` (120 messages); VI-6 at `limit 4, "a=0\x0a"` (120 messages); VI-7b at `limit 4, "a=0\x0a"` (120 messages); VI-10 at `limit 4, "a=0\x0a"` (120 messages)
- R3: nowhere in its set

Mutants for which a rule the pipeline found false is NOT false in the wider search: none.

Verdicts of other projects that changed on a mutant: none.
