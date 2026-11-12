# `clausal compose2` and `clausal tree`: composer version 2, first part (plan nodes L1a, L1b, L1e)

```sh
python3 -m clausal compose2 "<rough English>" [--domain D] [--json] [--no-l3] [--acknowledge K --by NAME] [--write FILE.feature]
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
answer either**: it answers 0 of the 60. Every development sentence becomes a question (46) or a decline (14). It
answers a sentence only when the sentence is a sentence of the book already, or when every word of it is a form word,
a cue word or a default of one candidate, and ordinary English as the development author wrote it never is. By the
study's own signal ("A1 failing to beat A0 counts against the rule changes themselves") this is a negative result on
right answers and a positive one on wrong answers. What stands between the two is listed under "What blocks an answer".

## What it does

1. **A sentence of the book is its own answer.** The rough sentence is compiled as written. If it compiles: ANSWER,
   itself. If two systems read it: ASK (system).
2. **Anchor, and the system first.** An operation is anchored by *every* word of one of its nouns ("transfer",
   "batch applied as a whole"), or by the verb of its `when` form ("withdrawing", "bumping"). An operation whose noun
   contains a named noun is tried too ("batch applied as a whole" for "batch"). Nothing anchored: DECLINE. Version 1's
   fallbacks (any shared word of a noun, any word of an echo, then every operation) are gone. If the anchored
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
| ASK (reading) | Two or more candidates have full coverage and are not shown equal. The separating inputs and what the compiled Rust did there are printed. NONE-FOUND and NOT-SEARCHED ask too |
| ASK (dropped) | No candidate has full coverage and at least one is askable. Up to three are shown, those that drop no condition first, then in version 1's rank order, each with its dropped words, added pieces and dropped conditions |
| DECLINE | Nothing anchored, or no candidate is askable. Printed: the words nothing accounts for, the nearest pieces, the operations |

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

**Full coverage** is no DROPPED word, no ADDED piece and no CONDITION DROPPED. Only a full candidate can be an ANSWER.

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
| Seeded drop: one condition or narrowing deleted from each fixture tree, the original sentence as rough input | 43 of 43 reported (42 also as CONDITION DROPPED); 6 more deletions give a sentence the compiler refuses and are not counted |
| Version 1's thirteen sentences (`cases.json`): answers with a dropped word | 0 (2 ANSWER, 9 ASK dropped, 1 ASK system, 1 DECLINE) |

**What the generator reaches, with step 1 switched off** (informational; `identity=False`): of the 66 fixture
sentences, 23 are answered with the same term, 24 get ASK (reading), 11 ASK (dropped), 8 ASK (system), and none is
answered with another term. So the identity result above rests on step 1, not on generation: without it, about a third
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

| | A1 | A1s | A0 | always decline |
|---|---|---|---|---|
| Wrong answers, of 60 | 0 | 0 | 43 | 0 |
| Expressible (45): answered right | 0 | 0 | 17 | 0 |
| Expressible: answered wrong | 0 | 0 | 28 | 0 |
| Expressible: asked | 36 | 36 | 0 | 0 |
| Expressible: declined | 9 | 9 | 0 | 45 |
| Expressible: missed (no right answer) | 45 | 45 | 28 | 45 |
| Not expressible (15): answered | 0 | 0 | 15 | 0 |
| Not expressible: asked | 10 | 10 | 0 | 0 |
| Not expressible: declined (correct) | 5 | 5 | 0 | 15 |
| Needs an unbuilt piece (10): answered | 0 | 0 | 10 | 0 |

- A1 asks: 3 system, 0 reading, 43 dropped. A1 declines: 12 with no operation anchored, 2 with no askable candidate.
- Answers with a dropped word or condition: 0, because there are 0 answers.
- If the first candidate of each ASK (dropped) were acknowledged unread: 18 of 43 not contradicted, 25 wrong (A1s: 19
  of 46). That is what an author who clicks through would get, and it is about what version 1 gives.
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
  nothing is anchored, so 12 sentences are declined at step 2.
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
- **A word mapped to the wrong piece counts as mapped.** "A rejected bump ..." against "A bump ... is always rejected"
  maps "rejected" to the claim. The narrowing-word span catches that case; the general case is caught only when a
  second full candidate exists and `clausal separate` is asked.
- **Full coverage does not look at the candidate's own extra words.** "A batch applied as a whole never changes ..." is
  full for "A batch never changes ...". With step 1 off this gave ASK (reading) on the fixtures, never a wrong answer,
  but only because the right sentence was also generated.
- **`DEFAULT_PHRASES`, `OPENERS` beyond the study's list ("that", "which"), the anchoring rule and the askable rule
  are this implementer's**, written while looking at the development set.
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
