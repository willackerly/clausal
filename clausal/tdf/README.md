# tdf/: the first Clausal layer for the TDFLite decision core (plan node T9.7a)

Guarantees 1 to 5 of the key-release decision, at the ID level, and its three witnesses, as canonical Clausal
sentences about the Rust decision core `tdf-core` as Aeneas extracted it. Run every command from `clausal/`.

The crate, its extracted model and the proofs of T9.3 are in a local repository that is not tracked. So this is
split in two:

| Tracked here | What |
|---|---|
| `../clausebook/abac.yaml` | the access-control pack: 15 words (labels, the three states of an object, defined, satisfied under the three rule kinds, entitled, released, obligations, two relations between calls) |
| `../clausebook/local/tdf.yaml` | the local book: 2 operations on the one decision function, 4 words |
| `lean/Abac/Pieces.lean`, `lean/Tdf/Pieces.lean` | the Lean meaning of every word (human-asserted) |
| `features/tdf.feature` | 23 Rule lines and 3 scenarios |
| `expected.json` | the verdict expected of each, committed before the run (commit `e92dab2`) |
| `lean/TdfProofs/` | one module per proved or refuted sentence; `Support.lean` |
| `types.yaml` | the project's actor and literal types |
| `verdicts.md`, `verdicts.json` | the recorded verdict table of the last run |
| `projects.local.example.yaml` | the overlay entry, to copy |
| `check_controls.py`, `readme_sentences.py` | the negative controls of the run; the README's three planned sentences |

| Not tracked | What |
|---|---|
| `../projects.local.yaml` | the overlay: where the crate, the model and the T9.3 proofs are on this machine |
| `../build/overlay/tdf/` | the project's Lean workspace and the outputs of its run |

## The overlay

`projects.local.yaml` is an untracked second list of projects (format: `projects.local.example.yaml`). A project in
it is run by `python3 -m clausal overlay run` (`../clausal/overlay.py`), which `./run.sh` calls after its report
when the file exists.

**With no overlay file `./run.sh` does what it did.** The only tracked changes outside this directory and the two
books are: `run.sh` (the report's exit status is kept in a variable, and one `if [[ -f projects.local.yaml ]]`
block after it), `clausal/pipeline.py` (the command `overlay`), `clausal/overlay.py` (new), `.gitignore`.
`projects.yaml`, `clausebook/project.yaml`, `glossary.yaml`, `lean/lakefile.toml`, `lean/Bdd/AuditLinks.lean`, the
Rust-side crates, `clausebook/core.yaml` and `lean/Frames/` are untouched.

**With an overlay file the eight steps of `./run.sh` are the same too.** An overlay project is isolated, not merged:

- **Its own book.** The books it lists and no other. The two new books are not in `clausebook/project.yaml`, so
  `clausal gen`, `book check`, the term lock and the removal sweep of the tracked projects never load them.
- **Its own types** (`types.yaml`), not `glossary.yaml`.
- **Its own Lean workspace**, `build/overlay/<name>/lean`: `lean/Frames` and `lean/Bdd/{Ops,Audit,AuditLinks}.lean`
  by symbolic link, the sources the overlay names by symbolic link, generated `Local/Readings.lean`,
  `Local/Obligations.lean`, `Run/Links.lean`. The lakefile and the manifest are generated from
  `lean/lakefile.toml` and `lean/lake-manifest.json` (same toolchain file, same pins, the package cache by symbolic
  link, the Aeneas library by absolute path). `lake update` is never run.
- **Its own feature directory.** `tdf/features/`, not `features/`: `projects check` stops the run on a file under
  `features/` that no tracked project lists.

This is the minimal design that keeps the tracked run reproducible. It is NOT the third project of DESIGN.md
section 21: nothing was added to the declared list, and the limits of 21.4 (one merged book, one library of
generated Lean, shared Rust readings) were avoided rather than lifted.

### What an overlay project gets

| Step | Tracked project (`./run.sh`) | Overlay project |
|---|---|---|
| Compile each Rule line and scenario | yes | yes, the same compiler (`vocab.Compiler`) |
| Flat obligation; reading ↔ obligation kernel-checked; the audit of types, axioms and `uses_proof` | yes | yes, the same generators (`oblig.py`) and the same audit (`lean/Bdd/AuditLinks.lean`) |
| Hand-written proof of the obligation counted only with the exact type and standard axioms | yes | yes |
| Non-vacuity | at the input the search found | a hand-written `<id>.sat : <id>.in_scope` (generated statement: some input is in scope) |
| Refutation | at the input the search found, generated script | a hand-written `<id>.refuted : ¬ <id>.obligation`, carried to `¬ reading`; the input is named by a person |
| Which theorems of another development a proof goes through | no | yes: the theorems of the `through:` roots the proof term reaches |
| Translation, unit tests | yes | no: the model is the file the overlay names |
| Reading search on a grid; frame definition against executable reading; a counterexample found by the run | yes | **no** |
| Narrowing check (what the books say narrowing settles; the Calls value of every claim against the printed coverage) | yes | yes, the same generator and reader (`narrowing.py`), with no control sentences |
| Rust side (cucumber, generated property tests, Kani), mutation, adequacy note | yes | **no** |
| `out/report.md`, `out/graph.json` | yes | no: `build/overlay/<name>/out/verdicts.json`, and the table written by `--record` |

Verdict codes: `PROVED-FOR-ALL`, `PROVED-INSTANCE`, `REFUTED`, `UNBOUND`, `UNLINKED` mean what they mean in the
report, with the differences of the table; `STATED-ONLY` is a sentence that compiles and is linked and has no
counted proof and no test.

## The sentences

`features/tdf.feature`. 20 of 26 compile as written; 6 are stated and tagged `@expect-unbound`.

| Guarantee | Lines that compile | Stated, not sayable today |
|---|---|---|
| 1 deny is the default | three: an unresolved object is never entitled; an unlabelled one only if the policy admits unlabelled objects; a labelled one only if the subject holds something | the two grounds in one line |
| 2 only defined values grant | one, and the same of the release | – |
| 3 the three rule kinds | one: for a labelled object, entitled exactly when every label is satisfied under its attribute's rule | one line per rule kind about the check of one attribute |
| 4, 4b more never takes access away | four: each form, for the entitlement and for the release | – |
| 5 obligations | four: released implies entitled; released implies every listed obligation was declared; nothing listed when not entitled; when entitled, the list is the specification's | the equivalence (released exactly when entitled and every listed obligation declared) |
| witnesses | three scenarios at a named policy and request; three false universal lines, each refuted at the witness | "is sometimes accepted" |

### Edits to `clausebook/core.yaml` and `lean/Frames`: 0

### What could not be said, and the piece each needs (none was added)

| Sentence | Missing |
|---|---|
| `g1_two_grounds` | a connective between two conditions: `or`, and `and` inside a condition |
| `g3_hierarchy`, `g3_all_of`, `g3_any_of` | an operation with more than one input. `tdf_core::rules::satisfied` takes a subject, an attribute and the bound values; an operation entry has one input role, and `lean/Bdd/Ops.lean` has no constructor for more. This is outside core: a constructor, and the compiler's `input:` |
| `g5_exact` | `exactly when` (and `only if`) between classes of the SAME answer. Core's forms are "is accepted exactly when {k:cond}": the left side is the operation's own acceptance and the right side a condition on the input. Also `and` |
| `w_sometimes` | a frame that says a call of some kind exists |
| (not written as a line) the witness of T9.3 also says the released decision lists an obligation | a number other than zero: core has `zero` and no numeral; the ledger pack reads a numeral as an amount |

Three consequences of today's pieces that shaped the wording, each a finding and not a block:

1. **One function, two operations.** "is accepted" has one meaning per operation, and "only if", "exactly when",
   "whenever" and "never loses acceptance" speak only of that. Guarantees 1 to 4 are about the entitlement bit and
   guarantee 5 about the release bit, so `decide` is declared twice: `key release` and `entitlement decision`.
2. **One input, so no "the subject", "the object", "the data".** An operation takes one input and a Rule line
   names roles, so the sentences say "label of the request", "the subject of the request".
3. **The three rule kinds are in a word's meaning**, `abac.satisfied` (`lean/Abac/Pieces.lean`, `ruleSatisfied`),
   not in three sentences. A reader who signs `g3_entitled` signs that definition.

### The README's three planned sentences: 0 of 3 compile as written

`python3 tdf/readme_sentences.py`.

| README | Result | Nearest line that compiles |
|---|---|---|
| A key release is accepted only if every attribute of the data is satisfied by the subject under its rule | UNBOUND: "the data", "the subject", "its rule" are not roles (finding 2) | A key release is accepted only if every label of the request is satisfied by the subject of the request under the policy (compiles; not in the feature file, no verdict) |
| A key release never loses acceptance when the subject gains an entitlement | UNBOUND: the pack's word for the relation is "the subject holds more values" (in this pack an entitlement is what a decision grants, a subject holds values) | A key release never loses acceptance when the subject holds more values (`g4_more_values_release`, PROVED-FOR-ALL) |
| A key release gives the same answer when only the order of the attributes differs | UNBOUND: the pack has no such relation; T9.3 has no statement about order | – |

## How a sentence is linked to T9.3

For each compiled sentence the generator writes the flat obligation and the script
`<id>.reading_iff_obligation : reading ↔ obligation` (kernel-checked; the audit checks that it uses a proof of
neither side). The hand-written module `lean/TdfProofs/<item>.lean` proves the obligation **from the theorems of
T9.3** (`T93.core_g1`, ..., each of type exactly its frozen statement). Nothing about the model is proved again:
`TdfProofs/Support.lean` holds the passage between the pack's words and the terms of those statements (the rule
kinds: `satisfied_iff`; "holds more values or higher levels": `atOrAbove_abs`; what the model answers at the
three fixtures, through `T93.decide_refines`). The run lists, per sentence, the `T93` theorems its proof term
reaches (`verdicts.md`, "through").

## Reproduce

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
cp tdf/projects.local.example.yaml projects.local.yaml      # then put the local path in place of <TDF>
python3 -m clausal overlay                                  # the overlay as read
python3 -m clausal overlay run tdf                          # verdict per sentence; exit 1 if one differs from tdf/expected.json
python3 -m clausal overlay run tdf --record tdf/verdicts    # ... and rewrite tdf/verdicts.{json,md}
python3 -m clausal overlay lint tdf                         # the registration lint over this project's merged book
python3 tdf/check_controls.py                               # six seeded faults, each must lose its verdict
python3 tdf/readme_sentences.py                             # needs no overlay
```
