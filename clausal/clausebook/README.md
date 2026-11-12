# clausebook/: the Clausebook as a list of books

Plan nodes C1 (the split) and Q3 (every accepted form in the book; `clausal book check`). The assignment of each
entry, written before the split, is in `ASSIGNMENT.md`. Run every command below from `clausal/`.

## What is here

| File | What it holds | Entries |
|---|---|---|
| `project.yaml` | the books this project loads, in order | – |
| `core.yaml` | 25 frames, 23 modifiers, 3 coverage entries, 7 grammar entries, 10 defaults, 1 frame with no surface form | 68 signable |
| `ledger.yaml` | the ledger pack: 10 accounting words, 4 literal readings, 2 idioms | 16 |
| `local/ledger.yaml` | the ledger fixture: 5 operations, 19 words, 1 idiom | 25 |
| `local/wallet.yaml` | the wallet fixture: 3 operations, 4 words | 7 |
| `<book>.signoff.json` | sign-offs of that book's entries (none exists yet) | – |
| `check.expected.json` | the violations `book check` reports today, accepted as known debt for Q4 | 34 |
| `terms.lock.json` | what each sentence of `features/` and `controls/` compiles to | 111 |
| `split-check/` | entry digests before the split, and the script that compares | – |

## The loader

- `vocab.load_project(ROOT, gloss)` loads the books of `project.yaml`. `vocab.Vocabulary(books, gloss)` takes any
  list of `(path, printed name)` pairs, so a third project passes `core.yaml`, the packs it wants and its own book.
- An id is defined once. A book that redefines an entry of another is refused, as is a book whose `needs:` are not
  loaded before it.
- The rest of the compiler sees one merged book (`voc.ops`, `voc.pieces`, `voc.raw[...]`). `voc.book_of(id)` and
  `voc.at(id)` give an entry's book and `file:line`; every message names the entry's own file.
- Each book states what it brings and what it needs:

| Key | Meaning |
|---|---|
| `needs` | books that must be loaded first |
| `lean_imports`, `lean_files` | the Lean modules its definitions live in |
| `sorts` | what `<T>` ranges over; core gives `num`, the pack `balances`, `optnum`, `acct`, `transfer` |
| `uses_types` | the literal and actor types of `glossary.yaml` its holes name; a hole of a type not listed is refused |
| `literal_lean`, `type_echo`, `introduced_by_kind` | how a literal type is written in Lean and named in the echo |
| `categories` (core) | the categories a hole may have |

- Generated Lean imports the books' `lean_imports` in reverse book order (most local first). With today's
  `project.yaml` that is the order the flat file had, so generated files did not change.
- Sign-offs: `python3 -m clausal review <id|all> --reviewer NAME` writes each record to the file beside the book that
  defines the entry. A record found in another book's file does not count.

## Core stands alone

`python3 -m clausal book core --lean` checks three things, and `./run.sh` runs them at step 3:

1. `core.yaml` loads with no other book and no glossary.
2. `core.yaml` and `lean/Frames/*.lean` contain no fixture noun, comments included. The nouns are computed, not
   listed: the actor and literal types of `glossary.yaml`, and from the other books their sorts, operation nouns, role
   names, Lean namespaces and crate names (36 words and phrases today).
3. `lean/Frames`, copied alone into a temporary directory with a lakefile that has no dependency, builds.

Controls of these checks (fix round; before it, only the loader's `uses_types` check had one, c40, and nothing would
have failed if the noun scan found nothing or the build alone always passed). The selftest seeds a copy: a comment
naming `account` and `ledger` in `lean/Frames/Core.lean`, a comment naming `wallet` in `core.yaml`, and
`import Wallet.Pieces` in `lean/Frames/Lemmas.lean` are each reported; a longer word that contains a noun is not.
Mutation control c41 puts the comment into the frame library and expects `./run.sh` to stop at step 3 naming file,
line and noun. Control c42 adds the import and expects both the import check and "lean/Frames does NOT build alone".

## Dependence that remains (stated, not removed)

- **The pack is a pack in the book only.** Its Lean definitions are `lean/Ledger/Pieces.lean`, stated on the generated
  types `ledger.Ledger` and `ledger.Transfer`. A second crate cannot use it as it is.
- **Literal and actor types stay in `glossary.yaml`**, shared with the old whole-phrase glossary.
- **`internal`** (core) takes its membership test, its parties and its echo line from the operation's own `internal:`
  field. An operation without the field cannot be called internal.
- **The Rust readings are not split.** `wallet-bdd/src/pieces.rs`, `evidence/src/typed.rs` and `clausal/evgen.py` hold
  core and fixture pieces in one file each.
- **Generated proof scripts name fixture lemmas** (`L.mkBatch_val`, `Vocab.mkWallet` in `links.py` and `oblig.py`), and
  `rsearch.py` imports `Wallet.Vocab` and `Ledger.Vocab`.
- **`rsearch.py` and `trees.py` name a role `the <role>`** as an internal label. The accepted phrase comes from the
  book (`g.role`); changing it there needs those two labels changed too.
- **A second project's fixtures**: `pipeline.State` still reads `features/` and one `glossary.yaml`. Only the book
  loader takes a list.

## Q3: where each accepted form now lives

| Was in Python (`vocab.py`) | Is now in `core.yaml` |
|---|---|
| "is always accepted", "always succeeds" | `always`, `vp_forms`, with `implied: { c: accepted }` |
| "is never accepted", "is always rejected" | `never`, `vp_forms`, with `implied` |
| the list of frames whose class is the operation's own acceptance | `implied: { c: accepted }` on `if_then`, `only_if`, `exactly_when`, `monotone` |
| `ARTICLES`: a, an, every, any | `g.subject`, `forms` |
| `SUBJECT_WORDS`: successful, rejected, internal | `subject_forms` of those three modifiers |
| `NARROW_PREFIXES`: "if it is accepted,", "if it is rejected," | `claim_forms` of `successful`, `rejected` |
| " for which ", " followed by " | `subject_forms` of `given`, `and_then` |
| "for <subject>, <claim>", "<subject> <verb phrase>" | `g.rule_for`, `g.rule_vp` |
| ", and " between clauses, " and " between claims | `g.clauses`, `g.claims` |
| "the <role>" | `g.role` |
| first letter lowered, final full stop dropped | `g.line`, two switches |
| "every account the … names is an account of the …" (echo of `internal`) | the operation's `internal:` field (local book) |
| the Lean text of the four scoping modifiers: `.given (fun st inp => …)`, `.andThen`, `.beside`, `.internal m p` (fix round; they were still constants of `vocab.py` after the first build, in scenarios and in Rule subjects) | the `lean:` text of `given`, `and_then`, `beside`, `internal`, filled by `Compiler.scoped` |

- **Under the digest.** The grammar entries and the ten defaults are entries: `review` signs them by id, and a reading
  lists the grammar entries it was read through and every default printed with it among its pieces. Changing a form or
  a default's text voids that entry's sign-off only.
- **Control.** `python3 -m clausal.selftest` takes each of 24 forms and texts out of the book in memory; the sentence
  written with it then fails to compile, and compiles with the book intact.
- **Control, scoping modifiers (fix round).** A scenario's Givens, its second When and its bystanders are read with
  `given`, `and_then` and `beside`; a scenario that needs one the book does not have is refused (UNBOUND). The selftest
  takes each of `given`, `and_then`, `internal`, `beside` out of core: every fixture sentence that lists it among its
  pieces (46, 7, 3, 1) stops compiling. It then changes each one's `lean:` text: exactly those sentences compile to
  another term. Before the fix, 38, 3 and 1 scenarios compiled unchanged without the entry, and the `lean:` text of
  the four was never read.
- **The `lean:` of `and_then` was corrected to the text that is emitted**: `({op}).andThen {op2}`, not
  `({op}).andThen ({op2})`. The compiler never wrote the second pair of brackets, so the entry a reviewer would have
  signed was not the emitted text. No compiled term changed (the term lock is untouched); the entry's digest did
  (it was already one of the 13 entries `split-check/digests.py` reports as differing from the flat book, because Q3 gave it `subject_forms`).
- **No wording changed.** Every compiled reading of `features/` and `controls/` has the same Lean, echo and refusal
  as before; only its list of pieces grew a tail (grammar entries and defaults).

**Still in Python, and why it is not an accepted form:**

- Gherkin's own keywords (`core.py`).
- Refusal and hint texts that quote the words (for example "<a / an> [successful | rejected | internal]
  <operation> …" in the UNBOUND message of a Rule clause). They are messages, but they will go stale when Q4 changes
  a form.
- Proof scripts and audit lists that NAME the Lean definitions behind the scoping modifiers (`Frames.Op.andThen_some`,
  `Frames.Op.beside_some` in `links.py` and `oblig.py`; the constants the audit lets a reading mention in `vreport.py`).
  They do not decide what a sentence means: if a book changed the `lean:` of `and_then`, the readings would change and
  these scripts would fail to prove the glue, which is reported as UNLINKED, not accepted silently.
- Taking the pieces `not`, `always_answers` or `never` out of core does not give a refusal: the compiler stops with a
  Python `KeyError` (it names them when it applies default D1 and "not"). The run fails, with a poor message.
- `python3 mutation/removal_sweep.py` takes every entry, form, `implied`, default and switch out in turn (256
  removals) and recompiles the fixtures. No entry leaves a sentence that uses it unchanged. Ten removals change no
  recorded term, because no fixture sentence is written with them: "it answers", "of {c}, only {x} and {y} change",
  "always succeeds", "is never accepted", "it is rejected and nothing is changed", "{m} is afterwards at least {t}",
  "every {op}", "any {op}", the `{line}` form of `g.line`, and the optional full stop. Four of them ("always
  succeeds", "is never accepted", "every", "any") and the full stop have a synthetic sentence among the 24 removal
  controls; the other five have no control.
- The scaffolding of the echo ("applies to", "every …", "a plain Scenario: …", "followed by" between operations,
  "always answers" inside the D1 line). This is printed text under no signature. Moving it is not done.

## `python3 -m clausal book check`

Options: `--lean` (also build `lean/Frames` alone), `--quiet` (counts only), `--json`, `--update-expected`,
`--update-terms`. Exit 0 iff core stands alone and the violations are exactly those of `check.expected.json`.

The lint reads every accepted surface form of the loaded books (135 today): the forms of the pieces in every position,
the idioms, the `when` forms and nouns of the operations, and the grammar entries.

| Check | Rule | How it is decided |
|---|---|---|
| 1 holes | a form's holes are the piece's holes, same names and categories, none filled by a literal | The piece's holes are its declared `args`, or else the holes of its `lean` text. A list hole may be written as several holes of its item category. Holes the operation supplies (`from_operation`) and the plural of a per-actor measure are exempt by declaration |
| 2 order | holes change order only where categories differ | against the piece's first form: the holes that moved must have pairwise different categories |
| 3a | one live form per piece per position | one per field (`forms`, `not_forms`, `then_forms`, `vp_forms`, `subject_forms`, `claim_forms`, `when`, `nouns`, grammar `forms`), and the two switches of `g.line` |
| 3b | one form in a Rule line | a piece with both a verb-phrase form and a Then form (read through "for <subject>, <claim>"); a modifier written both on the subject and before the claim |
| 4 | no skeleton shared by two pieces | The skeleton is the form with every hole blanked; hole categories are ignored. Only pieces that can meet in one sentence are compared (same system, or one of them shared). A pair is exempt only while a SEPARATION of it is in force (below) |
| 5 | same term | each sentence of `features/` and `controls/` compiles to the Lean statement recorded in `terms.lock.json`, or is refused with the recorded status. A sentence not in the lock is reported as new, not as a violation |

**Separations (rewritten in the fix round).** A book may record, under `separations:`, an entry

```yaml
separations:
  - id: sep.more_than.exceeds
    between: [more_than, exceeds]
    inputs:                      # one Rule line per piece
      more_than: "A withdrawal for which the amount is more than the wallet's balance is always rejected"
      exceeds: "A withdrawal for which the wallet's balance is more than the amount always answers"
```

It is in force, and lifts that one pair, only if all of this holds when the lint runs: the two pieces do share a
literal skeleton; each sentence is written with that skeleton; each sentence compiles (it is compiled by the lint, as
a Rule line) to a reading that uses its own piece and not the other; and the entry has a sign-off record
(`python3 -m clausal review sep.more_than.exceeds --reviewer NAME`, stored in the book's `.signoff.json` like every
other entry) whose digest is of the entry's text, the book text of both pieces and the Lean each sentence compiles to.
Changing a sentence, a piece, or anything that changes either reading voids it. A separation that is recorded and not
in force is reported as a violation of its own (`4 separation not in force`, with the reason), so it cannot sit in a
book unnoticed. The first build accepted any two non-empty strings (`input`, `signed_by`); that form is now refused by
the loader. No separation is recorded today: clearing the check-4 debt is Q4's, and needs a person's sign-off.
What this does not do: it does not show that NO sentence is read both ways (the compiler refuses a sentence with two
readings as AMBIGUOUS where it meets one; the lint shows one sentence per piece, which is what the synthesis asks
for), and a sign-off is whatever `clausal review` records, as for every other entry.

Reported but not counted: skeletons shared only by pieces of different systems (2 today: "the maximum", and the noun
"transfer" of `w.transfer` and `l.apply`), and forms that are an instance of another piece's skeleton (80 today, in
`--json`; this is the head-collision question the readability synthesis leaves open for Q8).

### Today's violations (34), by synthesis row

| Check | Count | What | Row of the first batch |
|---|---|---|---|
| 1 | 8 | forms whose class hole is said by the form's own words: "is always accepted", "always succeeds", "is never accepted", "is always rejected", "is accepted whenever / only if / exactly when", "never loses acceptance when" | 2, 14; the three "is accepted …" frames have no row |
| 2 | 0 | – | – |
| 3a | 10 | `aggregate` (2), `always` (2), `never` (2), `monotone` (2), `l.balances_of` (4), `l.balance_at` (2), `l.the_transfer` (2), `l.apply` nouns (2), `g.subject` (4 articles), `g.line` (4 written forms) | 6, 2, 2, 14, 7, 7, 7, none, 5, none |
| 3b | 10 | two Rule voices: `always_answers`, `never_changes`, `rejected_unchanged`, `increases_by`, `decreases_by`, `at_most`, `at_least`, `always`; two narrowing places: `rejected`, `successful` | 12, 12, 12, 12, 12, 12, 12, none, 4, 4 |
| 4 | 5 | "{} is more than {}" (`more_than`, `exceeds`); "{} is at most {}" (`at_most_value`, `result_at_most`); "{} is {}" (`is`, `result_is`); "every {} is a {}" (`within`, `covers`); "the balance of account {} of {}" (`l.bal_of`, `l.balance_at`) | the comparison homographs; 7 |
| 4, no literal word | 1 | seven bare-hole forms told apart by the type of the hole alone: `always`, `l.ledger`, `l.the_transfer`, `amount_value`, `index_number`, `balances_value`, `amount_result` (21 pairs) | none |
| 5 | 0 | – | – |

Violations the synthesis did not predict: the three "is accepted …" frames under check 1, the second noun of
`l.apply` ("fund transfer"), the case and full-stop variants of a Rule line, `always` under 3b, three of the five
skeleton groups, and the bare-hole group.

## Reproduce

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
python3 -m clausal book check --lean          # core alone, the lint, the term lock
python3 -m clausal.selftest                   # the 24 removal controls, the scoping modifiers, the noun scan, separations, sign-off storage
python3 mutation/check_controls.py            # which negative controls the book check stops (meant: c39 to c42 only)
python3 mutation/removal_sweep.py             # every entry and form taken out in turn: no sentence that uses one survives
PYTHONPATH=. python3 clausebook/split-check/digests.py     # entry digests against the flat book
python3 compare/against/readings.py dc38b56   # compiled readings against the commit before the split
python3 compare/against/verdicts.py 5e6cfa7   # verdict codes against the baseline (after a ./run.sh)
```
