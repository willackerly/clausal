# kvparse: the fourth project, first target of the rule pack "validated input" (plan node K1)

A toy byte-level parser in the Rust profile, written to be the first target of `packs/validated-input/`. It is a
fixture: nothing uses it.

| File | What |
|---|---|
| `src/lib.rs` | the code under test: `Parser { limit }.parse(&[u8]) -> Option<Record>`, 85 lines with comments, one loop |
| `tests/unit.rs` | four example-based unit tests |
| `expected.json`, `check_expected.py` | the verdict each instantiated rule is expected to get, committed before the first run; `python3 kvparse/check_expected.py` after `./run.sh` |
| `../clausebook/local/kvparse.yaml` | its words: one operation, twelve pieces |
| `../lean/Kvparse/Pieces.lean` | the Lean definition of each word: **the format written out a second time** |
| `../lean/Kvparse/Lemmas.lean` | what is proved of the code: the parse answers; an oversize input gets no record |
| `../features/kvparse_rules.feature` | ten Rule lines, written by `python3 -m clausal pack instantiate` |
| `../features/kvparse_rules.pack.validated-input.yaml` | the bindings of that instantiation |
| `../wallet-bdd/src/pieces.rs` (section "the parser's own words") | the Rust reading of each word: the format a third time |

**The format.** One or two fields separated by `;`. A field is a key, `=`, one decimal digit. Keys `a` and `b`, each
at most once, `a` before `b`. Nothing after the last field. Longer than the parser's limit: rejected.

**Why the parser has a state.** The core comparison "X is at most Y" takes a value known before the call on the left
and a quantity of the state on the right. The size limit is therefore a field of a `Parser` struct and not a
constant, so that VI-4 of the pack can be written. A parser with a constant limit could not state VI-4 today.

**Why the role is `message`.** `clausal book check` refuses a role noun that core's own text uses, and core says
"input" throughout. The pack's slot is still called `input_value`; the project's word is "the message".

**What is not there.** No typed Rust reading of the kvparse words (`clausal/evgen.py`, `evidence/src/typed.rs`), so no
generated property test and no bounded check looks at a kvparse rule: the grid search on the Lean model and the same
grid on the compiled Rust are the only evidence beside the two proofs.
