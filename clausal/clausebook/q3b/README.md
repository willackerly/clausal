# Q3b: the 21 violations of the book check, settled as far as they can be without the owner

Plan node Q3b. `FREEZE.md` fixed the items, the tests and the expected count before the lint was changed and before
the recorded runs. Run commands from `clausal/`. Nothing was signed.

**Count: 21 before, 16 after** (`python3 -m clausal book check`). Five are settled, each for a reason the check now
states and tests. Five more have a recorded, machine-checked proposal and wait for a signature. Eleven need a
decision about wording or about the rule itself.

| Violations at `492bba6` | Now | Why |
|---|---|---|
| 4, shared across systems | 0 | A sentence is compiled against the books of its own project. No project lists the wallet's and the ledger's local books together |
| 1, seven bare-hole forms (21 pairs) | 0 | The seven are registered at seven different types, and the parser tries a form only where exactly its type is wanted |
| 4 shared skeletons, 1 head collision (7 pairs) | 5 | Unchanged in count. Each pair now has a proposed separation in the book, with a separating input. Unsigned |
| 6 (check 1), 4 (check 3a), 1 (check 3b) | 11 | Not touched: each needs a wording or a rule decision |

## 1. Cross-system: compilation is project-scoped

**What was the case.** `projects.yaml` declared which books a project lists, and the pipeline stopped if a compiled
sentence used an entry of another project's book. But a Rule line was still tried in every system of every loaded
book: the `books` argument of `Compiler.rule` only chose which operations an UNBOUND message listed.

**What is built.**

- `Vocabulary.scoped(books)` (`clausal/vocab.py`): the Clausebook made of exactly the listed books, loaded by the same
  loader from the same texts. `Compiler.rule(rule, hint, books)` and `Compiler.scenario(sc, books)` compile against it.
  The pipeline, `clausal compile`, `clausal duplicates` and the term lock pass the books of the file's project.
- With no project named (`books=None`) a line is read against every loaded book, as before. That is how `controls/`,
  the self-test and a file that no project lists are read.
- The lint asks check 4 per project (`book.scopes_of`, `book.collisions`): two forms are compared only if some
  project lists the books of both. What is shared only between entries no project loads together is printed under
  "not counted". If a loaded book is listed by no project, every book is compared, as before.

**Why the four disappear.** The wallet project lists `core.yaml`, `ledger.yaml` (the pack: no operation) and
`local/wallet.yaml`; the ledger project lists `core.yaml`, `ledger.yaml` and `local/ledger.yaml`. `l.apply`,
`l.accepted` and `l.maximum` are in `local/ledger.yaml`; `w.transfer`, `w.succeeds` and `w.maximum` in
`local/wallet.yaml`. No project loads both files.

**The refusal still fires inside one project** (self-test, "Q3b (1)"; `python3 clausebook/q3b/check.py`):

| Line, no scenario beneath it | wallet | ledger | one project listing both local books (in memory) | wallet, with "transfer" also a noun of `w.deposit` (in memory) | no project named |
|---|---|---|---|---|---|
| A transfer is always accepted | one statement, `w.transfer` | one statement, `l.apply` | AMBIGUOUS | AMBIGUOUS | AMBIGUOUS |
| For a transfer, it is accepted | one statement, `w.transfer` | one statement, `l.apply` | AMBIGUOUS | AMBIGUOUS | AMBIGUOUS |

Given a project that lists both local books, the lint reports the four violations again; so it does when no project
is declared. A noun that two operations of one project carry is reported as a shared skeleton.

**Limits.**

- A sentence in no declared project is still read in every system. `controls/` is such a directory, and so is a
  feature file given to `clausal compile` that no project lists. "A transfer ..." with no scenario is AMBIGUOUS there.
- `clausal compose` and `clausal separate` were not changed: they take a system, not a project, and load every book.
  Today each system's operations are in one project, so the readings are the same; the code does not enforce that.
- The Rust cucumber run (`wallet-bdd`) picks the tree of a shared Then form by the system of the scenario's When, as
  before. It was not changed.
- One refusal message changed, with the same status and code: `Rule.wallet.interest` ("A deposit earns interest") is
  refused for its claim ("earns interest"), where it was refused as no rule clause with a list of operations. The
  line was tried in three systems before and the longest message won.

## 2. Pairs that need a separating pair: seven proposals, in the book, unsigned

They are entries under `separations:` of `clausebook/local/ledger.yaml`. They cannot stand in core: core may name no
fixture noun (`book core`), and their sentences are about operations. A separation is now read in one project, one
that lists the book it is written in (`book.separation_state`).

Each pair is two Rule lines about the same operation, so that one input can be given to both. Where both pieces are
conditions the two lines are the same words with the two holes exchanged, which is the confusion the pair is about.

| id | The sentence that holds at the input | Input (state; argument) | Grid | Only first / only second / both / neither |
|---|---|---|---|---|
| `sep.more_than.exceeds` | `more_than` | ledger `[2, 1]`; batch `[0->1:1]` | 297 | 72 / 18 / 207 / 0 |
| `sep.not_more_than.at_most_value` | `not_more_than` | ledger `[1, 0]`; batch `[0->1:1, 0->1:1]` | 297 | 18 / 72 / 199 / 8 |
| `sep.not_more_than.result_at_most` | `result_at_most` | ledger `[1, 0]`; batch `[0->1:1]` | 297 | 0 / 80 / 217 / 0 |
| `sep.at_most_value.result_at_most` | `result_at_most` | ledger `[1, 0]`; batch `[0->1:1]` | 297 | 0 / 26 / 271 / 0 |
| `sep.is.result_is` | `is` | ledger `[]`; batch `[0->1:1]` | 297 | 221 / 3 / 69 / 4 |
| `sep.within.covers` | `within` | ledger `[]`; batch `[0->1:1, 1->0:1]` | 297 | 203 / 0 / 94 / 0 |
| `sep.same_answer.same_answer_if` | `same_answer_if` | ledger `[1, 0]`, transfer `0->1:1`; second call: ledger `[1, 0]`, transfer `0->1:2` | 4356 | 0 / 5 / 4351 / 0 |

"Holds" means: the sentence, read as a statement about one call on that input, is true there and the other is false.
The sentences are in the book and in `FREEZE.md`.

**What "PROPOSED" means in the lint.** A separation that (a) separates: both lines compile in its project, each is
read with its own piece and not the other, each is written with the shared skeleton; (b) records a `witness:` whose
two term hashes are the hashes of what the two lines compile to today; and (c) has no sign-off. It lifts nothing: the
violation of its pair stays and names it. It is not reported as `4 separation not in force`. A separation with no
sign-off and no `witness:`, or whose recorded term is stale, is reported as before.

**The machine check, in two parts.**

- Every `book check`: (a) and (b) above. No Lean.
- `book check --separate`: runs `clausal separate` on the two lines again. It fails unless the verdict is SEPARATED,
  the recorded input is the first separating input of its direction on the grid, and the compiled Rust answered at
  that input as the Lean model did. Run it under `tools/sem.sh`.

**To adopt one:** `python3 -m clausal review <id> --reviewer <name>`. The sign-off is of the entry (its two lines and
its witness), the book text of both pieces and the two compiled terms; a change to any of them voids it. Were all
seven signed, 11 violations would remain (`python3 clausebook/q3b/check.py`).

**Superseded.** `q4/separations.proposed.yaml` and `q4/check_separations.py` are removed. Three of those seven pairs
took one sentence from the wallet and one from the ledger, which no project reads together; and the file's
instruction, to copy an entry into `core.yaml`, would have put operation nouns into core.

## 3. Bare-hole forms: type-directed resolution is sound, with one stated limit

**The question.** Seven forms have no literal word: `always` "{c:class}", `l.ledger` "{l:ledger}", `l.the_transfer`
"{t:transfer}", `amount_value` "{x:amount}", `index_number` "{x:index}", `balances_value` "{x:balances}",
`amount_result` "{x:amount}". Can two of them, of different pieces, accept the same text at the same type?

**Answer: no, when the types they are registered at are disjoint. Argument from the parser:**

1. The loader registers each form under one key, (category, position) (`Vocabulary._add`). A form written with `<T>`
   is registered once per sort, each time with that sort put into its category and into every hole.
2. In a strict parse, `Parser.forms_for(cat, voice)` returns exactly the forms registered under that key: equality of
   category, no subtype, no coercion. (The relaxed mode compares base categories; it produces only the ILL-TYPED
   message and never a reading.)
3. `Parser.parse(cat, text, voice)` builds a reading of `text` only from a form `forms_for` returned.

So a bare-hole form reads a text only where exactly its own (category, position) is wanted. Two bare-hole forms
whose sets of (category, position) are disjoint never both read a text where one type is wanted.

**The seven:** claim (Then), measure<balances>, item<transfer>, term<num>, term<acct>, term<balances>,
term<optnum>. Pairwise different: 21 of 21 pairs disjoint.

**Tested with the parser itself** (`python3 clausebook/q3b/bare.py`; also run by the self-test):

- Universe: 11252 texts. Every span of whole words of the 280 steps and Rule lines of `features/`, `controls/` and
  the separations; every sample literal of `glossary.yaml`; every role phrase.
- Configurations: 12. Each system in scenario mode, and in rule mode once per operation.
- T1: 945168 (configuration, text, type) triples asked. 1474 have a reading through a bare-hole form. **0 are read
  by the bare-hole forms of two pieces.**

**The rule in the lint.** `book.registered_types` reads the parser's own table. A pair of bare-hole forms is not
counted iff both are in that table and their type sets are disjoint. A pair registered at a common type is a
violation ("4 shared skeleton (no literal word, and registered at one type)") and needs a separation like any other.
Control (self-test, in memory): a second form "{x:amount}" at `term<num>` is reported; the step "the amount is at
most the wallet's balance" becomes AMBIGUOUS and its Rule line is refused, where both read today.

**The limit (T2).** The same text can be read by two bare-hole forms at two DIFFERENT types: 29 texts of the
universe are a `term` at more than one sort ("1" is an account number, a number and an optional number; "the amount"
is a number and an optional number). Which reading is taken is decided by what fixes `T` around it: the other hole of
the frame, or the type the frame's result must have.

- No other generic category has such a text: only `term`.
- One frame has nothing that fixes `T`: `equals` ("{a:term<T>} equals {b:term<T>}", "... differs from ..."). Both
  holes are terms and the result is a condition. "the amount equals 1" has two readings, with `amount_value` and
  with `amount_result`.
- That sentence is refused, never read one way: the step is AMBIGUOUS; a Rule line that contains it is refused
  (self-test, "the limit of the rule"). The lint prints the frames of this kind under "informational".
- The fixtures use `equals` with a hole that does fix `T` ("the amount of the transfer equals zero").

So the rule is sound for what it says (one text, one type), and what it does not cover is a refusal, not a misreading.

**Found on the way.** A Rule line whose condition is AMBIGUOUS is refused as UNBOUND ("no composition ... reads
... as a claim"), not as AMBIGUOUS: the subject parser drops a condition that does not parse to one tree. The line is
refused either way; the message does not say why. Not changed here.

## The 16 that remain, each with the decision it needs

| # | Check | Violation | Decision needed from the owner |
|---|---|---|---|
| 1 to 6 | 1 holes | `always` "is always accepted"; `never` "is always rejected"; `if_then`, `only_if`, `exactly_when` "is accepted ..."; `monotone` "never loses acceptance when" | One decision for the six: is `implied:` (the form's words stand for the class) a declared exemption of check 1, as `from_operation` is? If not, the six verb phrases need a class hole |
| 7 | 3a | `g.line`: four written forms | Are the capital first letter and the final full stop spelling, exempt from "one form"? If not, pick one (strict would refuse every frozen sentence that ends in a full stop) |
| 8 | 3a | `g.subject`: "a", "an" | Is the article spelling, exempt? If not, which one is retired |
| 9 | 3a | `l.apply`: nouns "transfer", "fund transfer" | Which noun is retired. With project-scoped compilation "fund transfer" is no longer needed to say which system; the root README's example uses it |
| 10 | 3a | `monotone`: "never loses acceptance when", "never loses that {c} when" | Keep both as shorthand and long form (an exemption tied to `implied_only`), or retire the shorthand |
| 11 | 3b | `always`: "X is always accepted" and "for X, it is accepted" | Refuse "for X, <class>" when the class is the operation's acceptance (as row 14 did for `monotone`), or accept both and leave it to the duplicate report |
| 12 | 4 | "{} is more than {}": `more_than`, `exceeds` | Sign `sep.more_than.exceeds`, or reword one form |
| 13 | 4 | "{} is at most {}": `not_more_than`, `at_most_value`, `result_at_most` | Sign `sep.not_more_than.at_most_value`, `sep.not_more_than.result_at_most`, `sep.at_most_value.result_at_most` (all three), or reword |
| 14 | 4 | "{} is {}": `is`, `result_is` | Sign `sep.is.result_is`, or reword one form |
| 15 | 4 | "every {} is a {}": `within`, `covers` | Sign `sep.within.covers`, or reword one form |
| 16 | 4 head | `same_answer_if` takes the head of `same_answer` | Sign `sep.same_answer.same_answer_if`, or reword one verb phrase |

Two more questions came out of the work and are not among the 16:

- Should a sentence in no declared project (a `controls/` file, a held-out file) be refused outright rather than read
  against every book?
- Should `equals` be given a hole that fixes its type, or should the lint count a frame whose type nothing fixes?

## Results

Measured 2026-11-12 on this branch. RESULTS_PLACEHOLDER
