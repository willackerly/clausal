# `clausal compose2`, `clausal converse`, `clausal tree`, `clausal propose`: composer version 2 (plan nodes L1a to L1e; L1f as an interface only)

**The second part (L1c clause by clause, phrase cues, argument order, cues for the pieces of the last wave; L1d the dialogue and the oracle author; the proposer interface) is the section "Second part" at the end of this file. The text between here and there describes the first part as it was measured at `0f1c9dd`; where the second part changed a rule, that section says so.**

```sh
python3 -m clausal compose2 "<rough English>" [--domain D] [--operation ID] [--json] [--no-l3] [--acknowledge K --by NAME] [--write FILE.feature]
python3 -m clausal tree "<rule sentence>" [--domain D]     # the parse tree of a sentence that compiles, as JSON
python3 -m clausal tree --from FILE.json                    # the sentence a tree spells, compiled and read back as the same tree
python3 -m clausal tree --schema [--out FILE]               # the JSON schema of the trees, generated from the book
python3 -m clausal tree --check                             # the round trip on every compiled fixture Rule line
```

No language model is used anywhere. Design followed: `docs/studies/2026-11-12/composer-v2.md`, sections 4.1 and 4.2
(outcomes, filters, coverage) and the tree interface of 4.3. Code: `clausal/compose2.py`, `clausal/ctree.py`, five lines
in `clausal/pipeline.py` and `clausal/__main__.py`. Tests and measurements: `compose_tests/v2.py`, `compose_tests/dev.py`.

**Version 1 is untouched.** `clausal/compose.py` (`clausal compose`) has no changed line: it is arm A0. Version 2 imports
its generator, ranking rule, cue table and limits as they are, and changes what is done with the candidates.

## The result in one paragraph

Version 2 gives **no wrong answer** where version 1 gives 43 on the 60 development sentences, and it gives **no right
answer either**: it answers 0 of the 60. Every development sentence becomes a question (58) or a decline (2); before the
fix round it was 46 and 14. It
answers a sentence only when the sentence is a sentence of the book already, or when every word of it is a form word,
a cue word or a default of one candidate, and ordinary English as the development author wrote it never is. By the
study's own signal ("A1 failing to beat A0 counts against the rule changes themselves") this is a negative result on
right answers and a positive one on wrong answers. What stands between the two is listed under "What blocks an answer".

## What it does

1. **A sentence of the book is its own answer.** The rough sentence is compiled as written. If it compiles: ANSWER,
   itself. If two systems read it: ASK (system).
2. **Anchor, and the system first.** An operation is anchored by *every* word of one of its nouns ("transfer",
   "batch applied as a whole"), or by the verb of its `when` form ("withdrawing", "bumping"). An operation whose noun
   contains a named noun is tried too ("batch applied as a whole" for "batch"). Nothing anchored: ASK (operation) if the
   sentence has a word of a system of the book, DECLINE if it has none (fix round, below). Nothing is generated either
   way. Version 1's fallbacks (any shared word of a noun, any word of an echo, then every operation) are gone. If the anchored
   operations are in two systems and no word that only one system has ("ledger", "account", "wallet") settles it:
   ASK (system), before anything is generated.
3. **Generate and rank** with version 1's generator and ranking rule, unchanged.
4. **Compile and filter** the best 150. Dropped: sentences the compiler refuses (this includes Q1), sentences that use
   a book the operation's project does not list (`other-book`), a narrowed subject with the opposite claim
   (`opposite-narrowing`, decided with the book's `narrowing:` facts), "by exactly zero" (`by-zero`), a piece with the
   same term in two holes (`same-sides`).
5. **Account** for every word of the rough sentence against every candidate that is left (next section).
6. **Decide.**

| Outcome | Rule |
|---|---|
| ANSWER | The sentence compiles as written; or exactly one candidate has full coverage; or the first three with full coverage are all SAME-TERM or PROVED-EQUAL under `clausal separate` and there are no more than three |
| ASK (system) | Step 1 or 2 above |
| ASK (operation) | Nothing is anchored, and the sentence has a word of a system (its name, a word of a noun of one of its operations, a role, a role's type). The operations of that system are listed with their ids; if words of several systems are written, the operations of each. `--operation ID` (an id, or a noun) answers it |
| ASK (reading) | Two or more candidates have full coverage and are not shown equal. The separating inputs and what the compiled Rust did there are printed. NONE-FOUND and NOT-SEARCHED ask too |
| ASK (dropped) | No candidate has full coverage and at least one is askable. Up to three are shown, those that drop no condition first, then in version 1's rank order, each with its dropped words, added pieces and dropped conditions |
| DECLINE | Nothing anchored and no word of a system in the sentence, or no candidate is askable. Printed: the words nothing accounts for, the nearest pieces, the operations |

No score threshold is used. The rule for "no candidate is good enough" is structural: a candidate is **askable** only
if its operation is asked for by a word of the author's and every one of its claims has a word of the author's mapped
into it.

## Coverage accounting

Every word of the rough sentence that is not an article or an auxiliary (`STOP2`, printed with every result) gets
exactly one status against a candidate; the function asserts it.

| Status | Meaning |
|---|---|
| MAPPED, via `form` | The candidate's sentence writes this word for one of its pieces. Matched occurrence by occurrence, in the author's order first |
| MAPPED, via `cue` | The word is in version 1's cue table for a piece of the candidate, and that piece has not already taken as many words as its own form has (the cue capacity) |
| MAPPED, via `noun`, `when`, `opener` | A word of another noun of the operation; the verb of its `when` form; a word that opens a condition span that is matched (below) |
| DEFAULT | The word is in a phrase that a named default of the candidate's reading covers (`DEFAULT_PHRASES`: D2, D3, D4), and the reading applies that default |
| DROPPED | Nothing of the candidate accounts for it |

The reverse: a piece of the candidate that no word is mapped to is **ADDED**. A role or a literal counts as a piece
when it was a choice ("the sender" where "the receiver" could stand, "the amount" as the term of a claim, a number).
Exempt: a role that is the one filler of its hole ("of the ledger"), a piece a form implies, a piece whose form writes
no word of its own, grammar words.

**Condition spans.** "if", "when", "whenever", "unless", "only", "as long as", "provided", "whose", "for which",
"that", "which" open a span that runs to the next opener or punctuation mark. A narrowing word before the operation's
noun ("an accepted lookup") is a span of one word. Each span must be matched, one to one, with a condition unit of the
candidate (a narrowing word; "for which" with its condition; the condition, variation or first-call class of a frame)
that a word of the span is mapped to. A span left over is printed first, as `CONDITION DROPPED: ...`, whatever the
statuses of its words. A form word of the candidate that introduces no condition ("only" of "only X and Y change")
opens nothing.

A run of narrowing words before the noun ("an accepted internal transfer") is a span each. When a span could be matched
with two units, the unit its words are mapped inside is tried before a unit it reaches only through the frame's own
words ("when ..., if ..." of a frame with two conditions).

**The side of a condition** (fix round). A word is mapped to a piece written *inside* a condition unit only if the word
is written in the condition span that is matched with that unit. This holds for form words and cue words alike. A word
outside every span is never mapped into a condition, and a word of one span is never mapped into the unit of another.
The accounting is repeated without the mappings it refuses until none is left; the refused ones are printed with the
candidate (`not mapped (...)`, `refused_mappings`). Not checked: a role that is the one filler of its hole ("of the
ledger"), since nothing was chosen there. A frame is not inside the condition it introduces.

**One negation word, one negation** (fix round). "not", "no", "never" (and "n't", "cannot", "none", "nothing", which are
read as these): a piece takes one through a cue only while it has taken fewer negation words than it says negations
(one, or as many as its form writes).

**Full coverage** is no DROPPED word, no ADDED piece and no CONDITION DROPPED. Only a full candidate can be an ANSWER.
An operation given with `--operation` is not an ADDED piece; the result and the record say that the author stated it
(`operation_stated`).

**Acknowledgement.** `--acknowledge K --by NAME` records that NAME accepts candidate K of an ASK (dropped) with its
dropped words, added pieces and dropped conditions. With `--write` the sentence goes into the feature file and one
record per rule goes into `<FILE>.compose.json`, keyed by the digest of the Lean term: the rough sentence and its
hash, the digests of the books, the outcome, the coverage word by word, the acknowledgement, who chose. `--write`
refuses an ASK without an acknowledgement and an acknowledgement without a name. The record is what the harness saw
typed; it is not a signature.

## The tree interface (L1e)

A tree names pieces by id and roles by phrase (format in the module text of `ctree.py`). `clausal tree --from` checks
it against the schema, writes the sentence with the compiler's own writer (`Compiler.canonical`, `surface`: the live
form of each piece), compiles it, and refuses unless the composition the compiler finds is the tree it was given.

The schema is generated from the loaded books on demand (about 1 MB; not committed, so it cannot drift). It has one
clause shape per subject the book can write (each operation; each sequence of two with the same state types; each tied
sequence), and under each the pieces of every category with their holes, the roles of that subject and the literal
types. `ctree.validate` checks the keywords the schema uses; the `jsonschema` package, where installed, accepts the
schema as draft 2020-12 and agrees on the fixture trees.

What the schema cannot say, so the compile step stays: Q1 refusals, a narrowing word on a tied sequence, a sentence two
systems read, and whether the sentence is read back as the same tree.

## Measurements

All reproduce from `clausal/`:

```sh
python3 compose_tests/v2.py --json                 # about 5 minutes, no Lean
tools/sem.sh 3 -- python3 compose_tests/v2.py --l3 # adds one ASK (reading) through clausal separate
python3 -m clausal tree --check
```

Gold for these is the book's own fixtures: the 66 Rule lines of `features/` and `controls/` that
`clausebook/terms.lock.json` records as compiled. The study says 121 lock sentences; the lock has 125, of which 66 are
compiled Rule lines, 20 are refused Rule lines and 39 are scenarios. The composer writes Rule lines only, so the
scenarios are not part of any test here.

| Test | Result |
|---|---|
| Identity: each compiled fixture Rule line, given as the rough sentence, comes back as itself, with the locked term | 66 of 66 |
| Identity: coverage of each under its own tree is full | 66 of 66 |
| Identity: with no system given, answered as itself or asked the system question | 66 of 66 |
| The 20 refused fixture Rule lines: answered | 0 (12 ASK dropped, 6 ASK system, 1 ASK reading, 1 DECLINE) |
| Round trip, tree to sentence to compile to the same Lean term | 66 of 66 |
| Round trip: the sentence written is the fixture's own text | 65 of 66 (the other is "fund transfer", a second noun of the same operation; same term) |
| Fixture trees valid against the generated schema | 66 of 66 |
| Trees the schema must reject (unknown piece, role of another operation, missing hole, unknown narrowing, prose in a field, another system's operation) | 6 of 6 rejected, and none is written |
| Seeded drop: one condition or narrowing deleted from each fixture tree, the original sentence as rough input | 43 of 43 reported (43 also as CONDITION DROPPED; 42 before the fix round); 6 more deletions give a sentence the compiler refuses and are not counted |
| Fix round: the reviewer's three sentences with "never ... when / if the amount is zero" | 3 of 3 ASK (dropped), the condition as written shown first, no full candidate with the condition inverted |
| Fix round: side of a condition, negation and operation-question checks in `v2.py` | 19 of 19 |
| Version 1's thirteen sentences (`cases.json`): answers with a dropped word | 0 (2 ANSWER, 9 ASK dropped, 1 ASK system, 1 DECLINE) |

**What the generator reaches, with step 1 switched off** (informational; `identity=False`): of the 66 fixture
sentences, 25 are answered with the same term, 22 get ASK (reading), 11 ASK (dropped), 8 ASK (system), and none is
answered with another term (before the fix round: 23, 24, 11, 8). So the identity result above rests on step 1, not on generation: without it, about a third
come back.

### The development set (`compose_tests/dev/`)

```sh
bash clausal/mutation/workcopy.sh <scratch>/clausal
tools/sem.sh 3 -- python3 clausal/compose_tests/dev.py <scratch>/clausal    # about 5 minutes
```

60 sentences by an author who had seen neither the tool nor the 48, committed unchanged as the first commit of this
work. Version 2 was developed while looking at its output on them, so these are development numbers. Definitions are
frozen in the text of `dev.py`, committed before the reported run. A1 is version 2; A1s is version 2 after the one
system question is answered from the set; A0 is version 1's top candidate.

Rerun after the fix round (freeze `2066b40`). A1o is A1s with the operation question answered by the operation the
set's cases call.

| | A1 | A1s | A1o | A0 | always decline |
|---|---|---|---|---|---|
| Wrong answers, of 60 | 0 | 0 | 0 | 43 | 0 |
| Expressible (45): answered right | 0 | 0 | 0 | 17 | 0 |
| Expressible: answered wrong | 0 | 0 | 0 | 28 | 0 |
| Expressible: asked | 43 | 43 | 43 | 0 | 0 |
| Expressible: declined | 2 | 2 | 2 | 0 | 45 |
| Expressible: missed (no right answer) | 45 | 45 | 45 | 28 | 45 |
| Not expressible (15): answered | 0 | 0 | 0 | 15 | 0 |
| Not expressible: asked | 15 | 15 | 15 | 0 | 0 |
| Not expressible: declined (correct) | 0 | 0 | 0 | 0 | 15 |
| Needs an unbuilt piece (10): answered | 0 | 0 | 0 | 10 | 0 |

- A1 asks: 3 system, 12 operation, 0 reading, 43 dropped. A1 declines: 0 with no operation named, 2 with no askable
  candidate (d36, d42: counter sentences with a written number, which the counter's project has no book for).
- Before the fix round the 12 operation questions were declines: expressible declined was 9 and is 2; not expressible
  declined (the correct outcome there) was 5 and is 0. **The operation question trades correct declines for questions**:
  d54, d56, d57, d58 and d60 are now asked which operation they are about.
- After the operation question (A1o): 9 of the 12 become ASK (dropped); 3 stay asked because their cases call no single
  operation. None is answered. Of the 7 expressible ones, the first candidate shown is not contradicted for 1 (d11).
- Answers with a dropped word or condition: 0, because there are 0 answers.
- If the first candidate of each ASK (dropped) were acknowledged unread: A1 18 of 43 not contradicted, 25 wrong; A1s 19
  of 46; A1o 20 of 55. That is what an author who clicks through would get, and it is about what version 1 gives.
- A0's 43 wrong answers: 17 about another operation than the cases call, 12 contradicted by a case, 10 not a sentence
  of their project, 2 unscored, and 2 not contradicted but given for a sentence that is not expressible.

### Arm A0 on the 48 (`compose_tests/l4b_a0/`, contaminated)

Version 1 on the merged book, one run in a private copy, after the repair of `l4b.py`: TOP-RIGHT 7, RIGHT-IN-TOP-3 2,
WRONG-READING 21, NO-CANDIDATE 0, NOT-SCORABLE 18 (before the merge: 5, 5, 20, 0, 18). Version 2 was not run on the 48.

## What blocks an answer

Read off `compose_tests/dev/REPORT.md`; a judgement, not a count.

- **Function words.** With the stop list cut to articles and auxiliaries, "to", "of", "in", "by", "it" must each be
  mapped. "A deposit adds exactly the amount to the wallet balance" is one word ("to") from an answer.
- **Verbs the cue table does not have.** "leaves ... untouched", "lowers", "goes through", "turned down". The table is
  version 1's, frozen; phrase cues are plan node L1c.
- **Operations named by a verb phrase.** "Putting money into a wallet", "Sending money", "Asking for the balance":
  nothing is anchored, so 12 sentences get the operation question at step 2 (they were declined before the fix round).
- **Two clauses.** The generator writes one clause (L1c).
- **The counter cannot say an amount.** Its project lists no pack, and "the amount" as a term and a written number are
  the ledger pack's `amount_value`. Every counter candidate with one is filtered as `other-book`. Version 1 offers
  them: 10 of its 60 top candidates are sentences `clausal gen` refuses in the counter's feature file.

## What a reviewer should distrust

- **"0 of the sentences that need an unbuilt piece is answered" is true and empty**: nothing is answered at all.
- **"Answered right" is weak.** It means not contradicted on at most five recorded inputs, replayed only where the case
  is what the shipped code does. A0's 17 are an upper bound on right readings.
- **"Expressible" is the set author's label.** It was not checked against the book, and at least the counter sentences
  about an amount cannot be said. Missed counts are upper bounds for every arm.
- **Seeded drop tests canonical sentences only.** The rough input is the fixture sentence itself. A drop from a
  paraphrase can still be absorbed by a cue word of a remaining piece; the cue capacity limits that and nothing measures it.
- **A word mapped to the wrong piece counts as mapped.** The earlier text here said the general case "is caught only
  when a second full candidate exists and `clausal separate` is asked". A reviewer refuted that: for "A rejected transfer
  never changes the ledger when the amount is zero" two full candidates existed, both with the condition and the claim
  inverted, `clausal separate` proved them equal, and the outcome was ANSWER. `clausal separate` compares candidates
  with each other, never with the author's sentence, so **agreement among full candidates is no evidence that any of
  them is right**. The fix round closes the route that was found (a word outside a condition mapped into it; a second
  negation word absorbed by one negation). What is still open:
  - A span runs to the next opener or punctuation mark, so in "a transfer that is rejected never changes ..." the claim
    is inside the span, and a negation written in the claim can still be mapped into that span's own condition.
  - "unless" opens a span like "if". "... never changes the balance unless it is accepted" is shown "An accepted
    withdrawal never changes ..." with only "it" dropped: the opposite condition, and the dropped list does not say so.
  - A stemmed form word counts wherever the candidate writes it: "changes" is mapped to "no other balance changed".
  - Nothing compares the polarity of the author's claim with the candidate's.
- **Full coverage does not look at the candidate's own extra words.** "A batch applied as a whole never changes ..." is
  full for "A batch never changes ...". With step 1 off this gave ASK (reading) on the fixtures, never a wrong answer,
  but only because the right sentence was also generated.
- **`DEFAULT_PHRASES`, `OPENERS` beyond the study's list ("that", "which"), the anchoring rule and the askable rule
  are this implementer's**, written while looking at the development set.
- **The fix-round rules were written against the reviewer's sentences** and five of this implementer's. No set measures
  how often the side rule turns a right ANSWER into a question; on the fixtures with step 1 off it turned none (25
  answered against 23 before).
- **ASK (operation) is asked of any sentence with a system word**, "The ledger should always be correct" included. The
  study's rule was DECLINE whenever nothing is anchored.
- **The order in which ASK (dropped) shows candidates** was chosen among three tried on the development set (fewest
  dropped and added: 18 of 49 not contradicted if acknowledged unread; fewest added then rank: 15 of 46; drops no
  condition then rank, kept: 19 of 46).

## Not done

- Oracle author and answer feedback (L1d), so no ASK is scored after a dialogue and no "questions per resolved
  sentence" is reported.
- Clause-by-clause composition, phrase cues, argument order, cues for the L2 pieces (L1c).
- The model proposer, the adversarial aligner, the neighbour comparison and the evidence-graph kind (L1f). The sidecar
  record exists with `proposed_by: rule-based`; nothing reads it yet.
- Gold terms for the development set. Answers are judged on its cases, not against a gold reading.
- Version 2 on the 48 (L4r) and anything of L5.
- The kind of a missing piece is recognised by five phrases only (`MISSING_KINDS`) and is advisory.

## Fix round (review of the first version)

| Defect | What was wrong | What changed |
|---|---|---|
| Wrong ANSWER in the default mode | "never" outside "when the amount is zero" was mapped through the `not` cue to the negated `equals` inside the condition; both full candidates were inverted and `clausal separate` proved them equal | The side of a condition; one negation word, one negation. The three sentences are now ASK (dropped) with "A rejected transfer for which the amount of the transfer equals zero never changes the ledger" first (ADDED: `equals`, because "is" is on the stop list) |
| Dropped list understated an inverted candidate | "no" of "gives no result" was absorbed by the negated `l.is_account`, which already had the author's "not" | One negation word, one negation: that candidate now lists "gives, no" as dropped |
| DECLINE for sentences the book can say | Nothing anchored meant DECLINE | ASK (operation), with `--operation`. d02, d07 and d11 are asked which operation; DECLINE is left for sentences with no word of any system |

Also changed: "can't", "won't", "shan't" are read as "can not", "will not", "shall not" (the word list showed "ca").
