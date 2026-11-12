# K1: seeded bugs and trivial implementations against the pack's rules on kvparse

Written by `packs/validated-input/kvparse_mutants.py` (2026-11-12 12:28:57). Each row is one pipeline run in a scratch copy: `./run.sh --no-unit --quick --no-adequacy --no-heldout`.
The kvparse rules are examined by the grid search on the Lean model and the same grid on the compiled Rust only (240 inputs:
8 size limits x 30 messages, written by the builder, who knew the bug list). No generated property test or bounded check looks at them.

Two columns, and they are not the same thing:

- **REFUTED** is the frozen criterion (`FREEZE.md`): the rule's verdict on the mutant is REFUTED, a counterexample confirmed by a
  kernel-checked theorem.
- **COUNTEREXAMPLE** is the verdict `COUNTEREXAMPLE FOUND (not confirmed in the kernel)`: the rule's reading is false at a grid input on
  the Lean model, and false at the same input on the compiled Rust. `mutation/run_mutants.py` counts both verdicts as shown false.

Baseline: exit 0, 127 verdicts; pack rules: VI-1 TESTED-ONLY, VI-2 TESTED-ONLY, VI-3 TESTED-ONLY, VI-4 PROVED-FOR-ALL, VI-5 PROVED-FOR-ALL, VI-6 TESTED-ONLY, VI-7b TESTED-ONLY, VI-8 TESTED-ONLY, VI-9 TESTED-ONLY, VI-10 TESTED-ONLY

**Strip test**: `packs/`, `clausal/pack.py` and the bindings file deleted, `@pack` tags stripped: exit 0, 127 verdicts, **0 verdict codes differ from the baseline**.

| Mutant | What | Unit tests | REFUTED (frozen criterion) | COUNTEREXAMPLE, not confirmed in the kernel | Expected by the pack | Proof lost |
|---|---|---|---|---|---|---|
| B1 | trailing garbage accepted: after a field, a byte that is not `;` ends the record instead of rejecting it | caught | **NONE** | VI-2, VI-6, VI-7b, VI-10 | VI-2, VI-7b, VI-10 | – |
| B2 | unknown item skipped: a field with a key that is neither `a` nor `b` is passed over instead of rejected | caught | **NONE** | VI-2, VI-6, VI-7b, VI-8, VI-10 | VI-8, VI-2, VI-10 | – |
| B3 | duplicate key, last wins: a repeated key is accepted and its last value kept | caught | **NONE** | VI-2, VI-6, VI-7b, VI-9, VI-10 | VI-9, VI-2, VI-7b, VI-10 | – |
| B4 | case mismatch: the keys `A` and `B` are taken for `a` and `b` | caught | **NONE** | VI-2, VI-6, VI-7b, VI-8, VI-10 | VI-8, VI-2, VI-10 | – |
| B5a | length off by one: an input of exactly the limit is rejected | caught | **NONE** | VI-3, VI-10 | VI-3 | VI-4, VI-5 |
| B5b | length off by one: an input one byte longer than the limit is accepted | caught | **NONE** | VI-4, VI-10 | VI-4 | VI-5 |
| B6 | default value returned: a record is accepted and the default record is answered (= T-default of the adequacy expectation) | caught | **NONE** | VI-7b, VI-10 | VI-7b, VI-10 | – |
| T-reject-all | trivial implementation: rejects every input | caught | **NONE** | VI-3, VI-10 | VI-3 | VI-4, VI-5 |
| T-accept-all | trivial implementation: accepts every input with one fixed value | caught | **NONE** | VI-2, VI-4, VI-6, VI-7b, VI-8, VI-9, VI-10 | VI-2 | VI-5 |

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

By the frozen criterion (REFUTED): 0 of 9 mutants are shown false by a pack rule; not: B1, B2, B3, B4, B5a, B5b, B6, T-reject-all, T-accept-all.
By either verdict: 9 of 9; not: none.

Where each is false (the grid input the rule's block names; `the_parser` is the size limit):

- B1: VI-2 at `{"the_parser": "4", "the_message": "\"a=1x\""}, on the compiled Rust too (reproduced)`; VI-6 at `{"the_parser": "4", "the_message": "\"a=1x\""}, on the compiled Rust too (reproduced)`; VI-7b at `{"the_parser": "4", "the_message": "\"a=1x\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "4", "the_message": "\"a=1x\""}, on the compiled Rust too (reproduced)`
- B2: VI-2 at `{"the_parser": "3", "the_message": "\"c=1\""}, on the compiled Rust too (reproduced)`; VI-6 at `{"the_parser": "3", "the_message": "\"c=1\""}, on the compiled Rust too (reproduced)`; VI-7b at `{"the_parser": "3", "the_message": "\"c=1\""}, on the compiled Rust too (reproduced)`; VI-8 at `{"the_parser": "3", "the_message": "\"c=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "3", "the_message": "\"c=1\""}, on the compiled Rust too (reproduced)`
- B3: VI-2 at `{"the_parser": "7", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`; VI-6 at `{"the_parser": "7", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`; VI-7b at `{"the_parser": "7", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`; VI-9 at `{"the_parser": "7", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "7", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`
- B4: VI-2 at `{"the_parser": "3", "the_message": "\"A=1\""}, on the compiled Rust too (reproduced)`; VI-6 at `{"the_parser": "3", "the_message": "\"A=1\""}, on the compiled Rust too (reproduced)`; VI-7b at `{"the_parser": "3", "the_message": "\"A=1\""}, on the compiled Rust too (reproduced)`; VI-8 at `{"the_parser": "3", "the_message": "\"A=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "3", "the_message": "\"A=1\""}, on the compiled Rust too (reproduced)`
- B5a: VI-3 at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`
- B5b: VI-4 at `{"the_parser": "2", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "2", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`
- B6: VI-7b at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`
- T-reject-all: VI-3 at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "3", "the_message": "\"a=1\""}, on the compiled Rust too (reproduced)`
- T-accept-all: VI-2 at `{"the_parser": "0", "the_message": "\"\""}, on the compiled Rust too (reproduced)`; VI-4 at `{"the_parser": "0", "the_message": "\"a\""}, on the compiled Rust too (reproduced)`; VI-6 at `{"the_parser": "0", "the_message": "\"\""}, on the compiled Rust too (reproduced)`; VI-7b at `{"the_parser": "0", "the_message": "\"a\""}, on the compiled Rust too (reproduced)`; VI-8 at `{"the_parser": "0", "the_message": "\"=1\""}, on the compiled Rust too (reproduced)`; VI-9 at `{"the_parser": "0", "the_message": "\"a=1;a=2\""}, on the compiled Rust too (reproduced)`; VI-10 at `{"the_parser": "0", "the_message": "\"\""}, on the compiled Rust too (reproduced)`

Verdicts of other projects that changed on a mutant: none.
