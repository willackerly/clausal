# clausebook/: the Clausebook as a list of books

Plan nodes C1 (the split), Q3 (every accepted form in the book; `clausal book check`), Q4 (the first batch of
rewordings, applied by replacement; `q4/README.md`) and L2 (three new pieces in core: `equals`, `each_at_most`,
`tied` with the tie `same_input`; `l2/README.md`). The assignment of each entry, written before the split, is in
`ASSIGNMENT.md`. Run every command below from `clausal/`.

**Read `q4/README.md` first if a sentence that used to compile is now refused.** Since Q4 the book holds one live form
per piece per position; the forms it replaced are recorded under `retired:` of their entries, and a sentence written
with one is refused with the form (and, where it could be checked, the sentence) to write. The Q3 sections below
describe the book as Q3 left it; where Q4 changed a form they say so.

## What is here

| File | What it holds | Entries |
|---|---|---|
| `project.yaml` | the books this project loads, in order | – |
| `core.yaml` | 26 frames, 26 modifiers, 3 coverage entries, 7 grammar entries, 10 defaults, 1 frame with no surface form (25, 23 and 68 before L2) | 72 signable |
| `ledger.yaml` | the ledger pack: 10 accounting words, 4 literal readings, 2 idioms | 16 |
| `local/ledger.yaml` | the ledger fixture: 5 operations, 19 words, 1 idiom | 25 |
| `local/wallet.yaml` | the wallet fixture: 3 operations, 4 words | 7 |
| `local/counter.yaml` | the counter fixture (plan node X7, `../projects.yaml`): 1 operation, 1 word; needs core only | 2 |
| `abac.yaml` | the access-control pack (plan node T9.7a): labels, the three rule kinds, entitlement, obligations. **Not in `project.yaml`**: loaded only for the overlay project `tdf` (`../tdf/README.md`), so nothing in this file's checks reads it | 23 |
| `local/tdf.yaml` | the TDFLite decision core: 2 operations on one function, 5 words. Not in `project.yaml` either | 7 |
| `<book>.attest.json` | attestation records about that book's entries (`../trust/README.md`; none exists yet). They replace `<book>.signoff.json`, which is refused if found | – |
| `check.expected.json` | the violations `book check` reports today (34 before Q4), each listed with its reason in `q4/README.md` | 21 |
| `terms.lock.json` | what each sentence of `features/` and `controls/` compiles to | 125 (111 before L2, 121 before the E2 probe and the three counter rules) |
| `q4/` | the freeze of the first batch, its results, and the scripts that reproduce the numbers | – |
| `q3b/` | the violations settled without the owner (project-scoped compilation, the bare-hole rule), the proposed separations' checks, and the decision list for the rest | – |
| `split-check/` | entry digests before the split, and the script that compares | – |
| `l2/` | the freeze of the three L2 pieces and their fixture rules, the design note and results, and the script that reports where the new forms coincide with a trial sentence | – |

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
| `categories` (core) | the categories a hole may have (L2 added `tie`: how the second input of a sequence is got from the first) |

- Generated Lean imports the books' `lean_imports` in reverse book order (most local first). With today's
  `project.yaml` that is the order the flat file had, so generated files did not change.
- Attestation records (plan node W1; they replace sign-offs): `python3 -m clausal attest <id|all> --act <act> --as <kind-prefixed id>
  --scope "…"` writes each record to the store beside the book that defines the entry. A record found in another book's store is
  refused. An entry is REVIEWED only by a person's record of act reviewed or approved; a model's record is kept under its own kind.

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
| "is always accepted", "always succeeds" | `always`, `vp_forms`, with `implied: { c: accepted }` (Q4: "always succeeds" retired) |
| "is never accepted", "is always rejected" | `never`, `vp_forms`, with `implied` (Q4: "is never accepted" retired) |
| the list of frames whose class is the operation's own acceptance | `implied: { c: accepted }` on `if_then`, `only_if`, `exactly_when`, `monotone` |
| `ARTICLES`: a, an, every, any | `g.subject`, `forms` (Q4: "every", "any" retired) |
| `SUBJECT_WORDS`: successful, rejected, internal | `subject_forms` of those three modifiers (Q4: the word of `successful` is "accepted") |
| `NARROW_PREFIXES`: "if it is accepted,", "if it is rejected," | `claim_forms` of `successful`, `rejected` (Q4: read before a Then step only) |
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
- Refusal and hint texts that quote the words. Since Q4 (row 19) the words they quote are read from the book: the
  UNBOUND message of a Rule clause lists the live articles and subject words, the NARROWED-TWICE and SAYS-NOTHING
  refusals quote the live word of each modifier. The sentences around those words are still Python.
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

The lint reads every accepted surface form of the loaded books (136 since L2; 131 after Q4; 135 when this was written): the forms of the pieces in every position,
the idioms, the `when` forms and nouns of the operations, and the grammar entries.

| Check | Rule | How it is decided |
|---|---|---|
| 1 holes | a form's holes are the piece's holes, same names and categories, none filled by a literal | The piece's holes are its declared `args`, or else the holes of its `lean` text. A list hole may be written as several holes of its item category. Holes the operation supplies (`from_operation`) and the plural of a per-actor measure are exempt by declaration |
| 2 order | holes change order only where categories differ | against the piece's first form: the holes that moved must have pairwise different categories |
| 3a | one live form per piece per position | one per field (`forms`, `not_forms`, `then_forms`, `vp_forms`, `subject_forms`, `claim_forms`, `when`, `nouns`, grammar `forms`), and the two switches of `g.line` |
| 3b | one form in a Rule line | a piece with both a verb-phrase form and a Then form (read through "for <subject>, <claim>"); a modifier written both on the subject and before the claim |
| 4 | no skeleton shared by two pieces | The skeleton is the form with every hole blanked; hole categories are ignored. Compared: pieces of the same system, or one of them shared; and pieces of two systems that share a Rule subject noun (`4 shared skeleton across systems`: a Rule line about that noun with no scenario beneath it is read in both systems); since Q3b, in each case only entries of books that one project lists together. A same-system pair is exempt only while a SEPARATION of it is in force (below); a cross-system pair cannot be separated |
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
a Rule line) to a reading that uses its own piece and not the other; and the entry has an attestation record of act reviewed or approved by a person
(`python3 -m clausal attest sep.more_than.exceeds --act approved --as human:<id> --scope "…"`, stored in the book's `.attest.json`
like every other entry; a model's record does not put a separation in force) whose digest is of the entry's text, the book text of both pieces and the Lean each sentence compiles to.
Changing a sentence, a piece, or anything that changes either reading voids it. A separation that is recorded and not
in force is reported as a violation of its own (`4 separation not in force`, with the reason), so it cannot sit in a
book unnoticed. The first build accepted any two non-empty strings (`input`, `signed_by`); that form is now refused by
the loader.

**Since Q3b (`q3b/README.md`).** Three things changed in check 4.

- *It is asked per project.* A sentence is compiled against the books its own project lists (`projects.yaml`,
  `vocab.Compiler.rule(..., books=)`), so two forms are compared only if some project lists the books of both. A
  skeleton shared by entries that no project loads together is listed and not counted. If a loaded book is listed by
  no project, every book is compared as before.
- *A separation is read in one project*: one that lists the book it is written in. Core may name no fixture noun, so
  a separation of two core pieces stands in the local book of the project whose operations its sentences are about.
- *Proposals.* A separation may record a separating input (`witness:`: the input, which sentence holds on it, the size
  of the grid searched, and the sha256 of the two Lean terms), found by `clausal separate`. A separation that
  separates, whose recorded terms are today's, and that nobody signed is a PROPOSAL: it lifts nothing (the violation
  of its pair stays and names it) and is not reported as `4 separation not in force`. Unsigned with no input recorded,
  or with a recorded term that is no longer what its sentence compiles to, it is reported as before.
  The plain check does not run the input (it compares the two term hashes) and says so in what it prints.
  `book check --separate` runs `clausal separate` on each again and fails if the recorded input is not one it finds or
  the compiled Rust disagrees with the Lean model there; `./run.sh` runs it after the Rust step, and
  `clausal review <id>` runs it before it signs a separation and signs nothing unless it is confirmed. Seven are recorded (`local/ledger.yaml`), none signed.
- *Bare holes.* Two forms with no literal word are not a violation when the (category, position) pairs the parser has
  them registered under are disjoint (`book.registered_types`). At a common type they are one.

What this does not do: it does not show that NO sentence is read both ways (the compiler refuses a sentence with two
readings as AMBIGUOUS where it meets one; the lint shows one sentence per piece, which is what the synthesis asks
for), and a sign-off is whatever `clausal review` records, as for every other entry.

Reported but not counted: skeletons shared only by pieces of two systems that share no Rule subject noun (none today.
Until the Q4 fix round every cross-system skeleton was left out, as "never live in one sentence". That was false: the
wallet and the ledger both call an operation "transfer", so "the maximum", "it is accepted", "the first call is
accepted" and the noun itself are now counted, 4 violations), and forms that are an instance of another piece's skeleton (80 today, in
`--json`; this is the head-collision question the readability synthesis leaves open for Q8).

### The violations before Q4 (34), by synthesis row

After Q4 there are 17, and a new check, "4 head collision" (a Rule verb phrase that is an instance of another frame's
verb phrase: it takes that frame's head). They are listed one by one, each with why it remains, in `q4/README.md`.

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
python3 -m clausal duplicates                 # Q5: sentences with the same statement once the operation's acceptance is unfolded
python3 clausebook/q3b/check.py               # Q3b: cross-system lines per project; the proposed separations; the count were they signed
python3 clausebook/q3b/bare.py                # Q3b: no text is read by two bare-hole forms at one type (the parser, over every span)
python3 clausebook/q3b/bare.py --control      # ... and a second piece at one type IS reported, with the same form text or another
python3 clausebook/q3b/bogus.py               # Q3b: a recorded input that does not separate is not confirmed, and cannot be signed (Lean, cargo)
python3 -m clausal book check --separate      # Q3b: `clausal separate` again on every recorded separation (Lean, cargo: under tools/sem.sh)
bash clausebook/q4/sentences.sh               # Q4: the 48 frozen sentences as written, before and after, in private copies
```
