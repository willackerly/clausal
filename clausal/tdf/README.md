# tdf/: the first Clausal layer for the TDFLite decision core (plan node T9.7a)

Guarantees 1 to 5 of the key-release decision, at the ID level, and its three witnesses, as canonical Clausal
sentences about the Rust decision core `tdf-core` as Aeneas extracted it. Run every command from `clausal/`.

The crate, its extracted model and the proofs of T9.3 are in a local repository that is not tracked. So this is
split in two:

| Tracked here | What |
|---|---|
| `../clausebook/abac.yaml` | the access-control pack: 23 words (labels, the three states of an object, defined, satisfied under the three rule kinds, the three kinds one at a time, entitled, released, obligations, two relations between calls) |
| `../clausebook/local/tdf.yaml` | the local book: 2 operations on the one decision function, 5 words |
| `lean/Abac/Pieces.lean`, `lean/Tdf/Pieces.lean` | the Lean meaning of every word (human-asserted) |
| `features/tdf.feature` | 29 Rule lines and 3 scenarios |
| `expected.json` | the verdict expected of each, and the link it belongs to, committed before the run (commit `e92dab2`; fix round `59548b3`) |
| `links.yaml` | the links: which sentences, together, say exactly what which statements of T9.3 say (frozen with `expected.json`) |
| `lean/TdfLinks/` | one module per link: the hand-written proof of its two-way claim |
| `lean/TdfProofs/` | one module per sentence that needs something by hand (a one-way proof, a refutation, a scope that is met); `Support.lean` |
| `types.yaml` | the project's actor and literal types |
| `verdicts.md`, `verdicts.json` | the recorded verdict table of the last run |
| `projects.local.example.yaml` | the overlay entry, to copy |
| `check_controls.py`, `readme_sentences.py` | the 13 negative controls of the run; the README's three planned sentences |

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
| Hand-written proof of the obligation counted only with the exact type and standard axioms | yes | yes, for a sentence in no link; **and only if it reaches every theorem its `through` lists** |
| Link to the statements of another development (`links.yaml`): a two-way claim, proved by hand, audited | the old statement of the whole-phrase glossary (`reading_iff`) | yes: see "How a sentence is linked to T9.3" |
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
counted proof and no test. `UNLINKED` is also the verdict of a sentence whose link to T9.3 is not counted.

## The sentences

`features/tdf.feature`. 26 of 32 compile as written; 6 are stated and tagged `@expect-unbound`.

| Guarantee | Lines that compile | Relation to T9.3 | Stated, not sayable today |
|---|---|---|---|
| 1 deny is the default | three: an unresolved request is never entitled; an unlabelled one only if the policy admits unlabelled objects; a labelled one only if the subject holds something | the three together ↔ `core_g1` ∧ `decide_total` (link `g1`) | the two grounds in one line |
| 2 only defined values grant | one | ↔ `core_g2` ∧ `decide_total` (link `g2`) | – |
| | the same of the release | one-way | |
| 3 the three rule kinds | one: for a labelled request, entitled exactly when every label is satisfied under its attribute's rule | ↔ `core_g3_entitled`, given totality and that the model's attribute check computes the pack's rule (link `g3`) | one line per rule kind about the check of ONE attribute |
| | three, one per rule kind, about the DECISION: a request all of whose labels are of allOf (anyOf, hierarchy) attributes is entitled exactly when ... | one-way (T9.3 has no statement of exactly this) | |
| 4, 4b more never takes access away | four: each form, for the entitlement and for the release | each pair ↔ `core_g4` (`core_g4b`) ∧ `decide_total` (links `g4`, `g4b`) | – |
| 5 obligations | five: released implies entitled; released implies every listed obligation was declared; nothing listed when not entitled; when entitled, the list is the specification's; entitled with every required obligation declared implies released | the five together ↔ `core_g5` (link `g5`) | the first part as one equivalence |
| | released only if every required obligation was declared | one-way | |
| witnesses | three scenarios at a named policy and request; three false universal lines, each refuted at the witness | at the named input; one of the false lines is false exactly when `witness_withheld` holds (link `w_withheld`) | "is sometimes accepted" |
| (a finding) | the allOf line with its scope said as "every label ... is of an allOf attribute": REFUTED at an unresolved request | at the named input | |

19 PROVED-FOR-ALL (14 in a link, 5 one-way), 3 PROVED-INSTANCE, 4 REFUTED, 6 UNBOUND; every verdict as frozen (`verdicts.md`).

### Edits to `clausebook/core.yaml` and `lean/Frames`: 0

### What could not be said, and the piece each needs (none was added)

| Sentence | Missing |
|---|---|
| `g1_two_grounds` | a connective between two conditions: `or`, and `and` inside a condition |
| `g3_hierarchy`, `g3_all_of`, `g3_any_of` (about the check of one attribute) | an operation with more than one input. `tdf_core::rules::satisfied` takes a subject, an attribute and the bound values; an operation entry has one input role, and `lean/Bdd/Ops.lean` has no constructor for more. This is outside core: a constructor, and the compiler's `input:` |
| `g5_exact` | `exactly when` (and `only if`) between classes of the SAME answer. Core's forms are "is accepted exactly when {k:cond}": the left side is the operation's own acceptance and the right side a condition on the input. Also `and` |
| `w_sometimes` | a frame that says a call of some kind exists |
| (not written as a line) the witness of T9.3 also says the released decision lists an obligation | a number other than zero: core has `zero` and no numeral; the ledger pack reads a numeral as an amount |

**Corrected in the fix round.** The first report read two of these rows as "core cannot say guarantee 3 per kind" and "core cannot
say the `if` half of guarantee 5". That was wrong: what is blocked is those WORDINGS. The content is sayable with pack words and
no core edit, and now is:

* guarantee 5, the "if" half: `g5_entitled_declared_released`, with the local word "required obligation of the request under the
  policy" and the pack word "is declared by the client of the request". With it the five lines of guarantee 5 are proved equivalent
  to `core_g5` (link `g5`), so `g5_exact`'s content is said, in five lines instead of one.
* guarantee 3 per rule kind, about the decision: `g3_all_of_decision`, `g3_any_of_decision`, `g3_hierarchy_decision`, with three
  conditions ("the request carries only labels of allOf attributes of the policy", ...) and three properties of a label.
  **A finding on the way:** with the scope said as "every label of the request is of an allOf attribute of the policy" the sentence
  compiles and is FALSE (`g3_all_of_unscoped`, REFUTED): a request with no label is in that scope, "every label is held" is true
  of it, and an unresolved request is never entitled. Saying "carries a label and every label is ..." needs `and` between two
  conditions, which core does not have; so the conjunction is inside the three pack conditions, and their echoes say so.

Four consequences of today's pieces that shaped the wording, each a finding and not a block:

1. **One function, two operations.** "is accepted" has one meaning per operation, and "only if", "exactly when",
   "whenever" and "never loses acceptance" speak only of that. Guarantees 1 to 4 are about the entitlement bit and
   guarantee 5 about the release bit, so `decide` is declared twice: `key release` and `entitlement decision`.
2. **One input, so no "the subject", "the object", "the data".** An operation takes one input and a Rule line
   names roles, so the sentences say "label of the request", "the subject of the request".
3. **The three rule kinds are in a word's meaning**, `abac.satisfied` (`lean/Abac/Pieces.lean`, `ruleSatisfied`), for the general
   sentence `g3_entitled`: a reader who signs it signs that definition. The three sentences per kind say each kind without that
   definition, for requests whose labels are all of one kind; a request with labels of several kinds is covered only by `g3_entitled`.
4. **"every X is a Y" is a claim only.** Inside a condition ("for which every ...", "only if every ...") core takes a property of the
   item, so "is declared by the client of the request" exists beside the collection "declared obligation of the request".

## What this layer sees of the object (corrected in the fix round)

A request, as `decide` receives it, carries either the mark *unresolved* or a list of identifiers. Whether a string bound to the
object was a label of the policy, and which identifier it became, is settled by the intake before `decide` is called. **Nothing in
this layer is a statement about strings**, and the words say so now:

| Word | Lean meaning | What the echo said before | What it says now |
|---|---|---|---|
| the request is unresolved | `r.bound = .Unresolved` | some bound string is not a label of the policy, including "a value the policy does not define" | the request records its labels as not resolved; why is not seen here |
| the request carries a label | `r.bound = .Labels ids`, `ids` not empty | every bound string resolved, and there is at least one | the request records a list of labels with at least one in it; an identifier need not be a value of the policy |
| the request carries no label | `r.bound = .Labels ids`, `ids` empty | every bound string resolved, and there is none | the request records a list of labels, and it is empty |

The Lean meanings were not changed (the statements of T9.3 are about the mark and the list); the echoes were replaced. So a request
that records the label 99, where 99 is not a value of the policy, **carries a label** and is **not unresolved**. It is denied, and the
sentence that says so is `g2_defined` (entitled only if every label is defined by the policy), not `g1_unresolved`. That a string the
policy does not know arrives as *unresolved* is a property of the intake and is not shown here.

### The README's three planned sentences: 0 of 3 compile as written

`python3 tdf/readme_sentences.py`.

| README | Result | Nearest line that compiles |
|---|---|---|
| A key release is accepted only if every attribute of the data is satisfied by the subject under its rule | UNBOUND: "the data", "the subject", "its rule" are not roles (finding 2) | A key release is accepted only if every label of the request is satisfied by the subject of the request under the policy (compiles; not in the feature file, no verdict) |
| A key release never loses acceptance when the subject gains an entitlement | UNBOUND: the pack's word for the relation is "the subject holds more values" (in this pack an entitlement is what a decision grants, a subject holds values) | A key release never loses acceptance when the subject holds more values (`g4_more_values_release`, PROVED-FOR-ALL) |
| A key release gives the same answer when only the order of the attributes differs | UNBOUND: the pack has no such relation; T9.3 has no statement about order | – |

## How a sentence is linked to T9.3 (rebuilt in the fix round)

Two steps, both kernel-checked, both audited for type and axioms.

1. **reading ↔ obligation** (generated, as in the tracked run): `<id>.reading_iff_obligation`. The obligation is the reading written
   out flat.
2. **obligations ↔ statements of T9.3** (`links.yaml`; the claim is generated, the proof is by hand in `lean/TdfLinks/<link>.lean`):

       Link.<name>.claim  :=  (obligation 1 ∧ ... ∧ obligation n) ↔ (T93.<a>.stmt ∧ ... ∧ T93.<z>.stmt)

   The run derives the same over the compiled readings (`Link.<name>.readings`), and derives the proof of each sentence FROM the
   link: `<id>.from_link := (Link.<name>).mpr ⟨T93.<a>, ..., T93.<z>⟩`. A sentence of a link has no hand-written proof.

An equivalence of two proved propositions can be had from the two proofs and then says nothing. So a link is counted only if its
proof reaches (a) no theorem whose statement is one of the link's statements and no proof of one of its sentences, and (b) no
theorem of T9.3 outside the link's `given`. `given: []` means the two sides say the same by the meaning of the words alone (links
`g1`, `g2`, `g4`, `w_withheld`); what a link leans on is printed in the verdict table:

| Link | Leans on | Why |
|---|---|---|
| `g3` | `decide_total`; `core_g3_hierarchy`, `core_g3_allOf`, `core_g3_anyOf`, `satisfied_refines`, `idspec_g3_norule`, `deref_val` | the sentence is about labelled requests only, so totality does not come back from it; the pack's "satisfied under its rule" is a definition on the values, and that the model's attribute check computes it is T9.3's |
| `g4b`, `g5` | `mem_nats`, `mem_of_mem_nats` | T9.3 reads a list of identifiers as a list of numbers; lemmas about that reading, not about the model |

**What the link does and does not give.** If a pack word is weakened so that a sentence says less than T9.3, the direction "the
sentences give the statements" stops being provable and every sentence of the link becomes `UNLINKED` (control: `check_controls.py`,
"a pack word weakened and the link repaired"). It does not show that the Lean meaning of a word is what its English echo says: that is
still asserted by a person. And a link proof that re-proved a T9.3 statement from the model's code, using no T9.3 theorem at all,
would pass check (b); none does (the longest is 81 lines with its header, and none unfolds a function of the model).

**One-way sentences** (in no link; `verdicts.md` says "one-way"): `g2_defined_release`, the three lines per rule kind,
`g5_release_required_declared`. Each obligation is proved by hand from theorems of T9.3 and counted only if the proof reaches every
theorem its `through` lists. Nothing shows that such a sentence says as much as any statement of T9.3; each says less than the
statements it follows from. The three scenarios and the three refutations of the witness lines are at a named input, through
`T93.decide_refines` (what the model answers there); the refutation of `g3_all_of_unscoped` is at an unresolved request, through
`T93.core_g1`.

## Reproduce

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
cp tdf/projects.local.example.yaml projects.local.yaml      # then put the local path in place of <TDF>
python3 -m clausal overlay                                  # the overlay as read
python3 -m clausal overlay run tdf                          # verdict per sentence; exit 1 if one differs from tdf/expected.json
python3 -m clausal overlay run tdf --record tdf/verdicts    # ... and rewrite tdf/verdicts.{json,md}
python3 -m clausal overlay lint tdf                         # the registration lint over this project's merged book
python3 tdf/check_controls.py                               # 13 seeded faults, each must lose its verdict (about 5 minutes)
python3 tdf/readme_sentences.py                             # needs no overlay
```
