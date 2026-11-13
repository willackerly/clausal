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

# Second part (plan nodes L1c and L1d; the proposer interface)

```sh
python3 -m clausal compose2 "<rough English>" ...                         # as before; the rules below are in it
python3 -m clausal converse "<rough English>" [--gold "<intended reading>"] [--domain D] [--json] [--max N]
python3 -m clausal propose --request "<rough English>" | --check PROPOSAL.json
```

Still no language model anywhere. Code: `clausal/compose2.py` (accounting, generation, clause by clause),
`clausal/cues2.py` (every table of ordinary English), `clausal/dialogue.py` (the dialogue, the oracle author),
`clausal/propose.py` (the proposer interface). Version 1 (`clausal/compose.py`, arm A0) has no changed line.

## What changed in the composer (L1c)

| Rule | What it does | Where |
|---|---|---|
| Phrase cues | A phrase of the author's that says what a shared piece means is accounted for by that piece: "goes through" (an acceptance), "turned down", "leaves ... untouched / as it was", "stays put", "takes ... out of", "adds ... to", "and refused otherwise". 16 patterns over 7 senses | `cues2.PHRASES`, `SENSES` |
| Word cues for the last wave | `equals` ("same", "itself", "identical"; negated: "different"), `each_at_most`, `same_input` ("same", "again"), and more words for an acceptance or a rejection said as a claim | `cues2.CUES2` |
| Function words | Prepositions, particles, coordinators, pronouns and universal determiners are still content words with a status. One no piece took is accounted for only with its neighbour: a preposition with its object, a particle with the word before it, a coordinator when both sides are accounted for, a pronoun as the subject. A preposition whose object is dropped is dropped | `compose2.attach` |
| Roles and domain words | A role said by its type ("the receiving wallet"), an input role said with a participle ("the requested amount"), a domain piece said by a word of its echo outside the parentheses ("every balance": the ledger) | `role_cues`, `cues2.echo_words` |
| Operations said by a verb | "putting money into" (a deposit), "taking out", "sending", "looking up", "all-or-nothing" (a batch applied as a whole), keyed by the operation's noun, and a light verb before the noun ("applying a transfer") | `cues2.OP_SYNONYMS`, `LIGHT` |
| A piece that is the one way to say something | A domain piece that is the one piece making its category from a role that is asked for ("out of the wallet": the wallet's balance), or the one piece of its category under a frame that is asked for ("gives back": the result), is not ADDED. Inside a condition this holds only for a word written in that condition's span | `Pieces.only_maker`, `said_otherwise` |
| Argument order | The author's comparison words say a relation between what stands before and after them; a candidate's comparison piece says a relation between the holes written before and after its own comparison words (read off its form by the same table). The word is mapped only if the two agree, also in strictness; a negation before the author's comparison allows the negated relation. A comparison word is never accounted for by a piece that does not compare, and a piece that compares is ADDED unless a comparison word asks for it | `wrong_order`, `cues2.DIRECTIONS` |
| "only if" | Accounted for only by the frame "is accepted only if", never as a cue for "whenever" or "exactly when" | `cues2.NECESSARY` |
| Post-modifier spans | A preposition right after the operation's noun opens a condition span ("a transfer from an account to itself") | `condition_spans` |
| Clause by clause | The author's sentence is cut before ", and" / ", but". Each clause is composed alone (for the operations it names, else those of the whole sentence), the best 6 (two clauses) or 4 (three) are joined with the book's ", and", every combination is compiled, filtered and accounted against the whole sentence. A word of one clause is mapped only into the same clause of the candidate; the subject restated in a later clause is not ADDED | `gather`, `clause_chunks` |
| Tied sequences | Two anchored operations said at two places with a sequencing word are tried in sequence, and "with the same input" when the sentence has a word for it | `sequences` |
| Generation | Version 1's generator, with two changes made in a subclass: the best 6 claims and conditions of each frame are kept (version 1: the best 30 and 12 overall), and sentences are compiled in an order by evidence per piece (version 1's order counts book words the author did not write against a sentence). 300 sentences are compiled, not 150 | `Gen2`, `order2` |
| Filter | A piece all of whose holes hold constants ("the maximum equals zero") | `filtered` |
| ASK (dropped) order | Those that drop no condition, then the fewest words dropped and pieces added (an added role counts half), then the compile order | `decide` |

The first part's rules stand: the side of a condition, one negation word per negation, the partition, ANSWER only
with full coverage.

## The dialogue and the oracle author (L1d)

`clausal converse` asks one question per turn, at most three. An answer removes candidates and the composer is
asked again.

| Question | Asked when | Answer | Effect |
|---|---|---|---|
| system | The noun names operations of two systems | A system | Composed again in it |
| operation | Nothing is anchored | An operation id | Composed again with `--operation` |
| input | Two full candidates differ at an input of the grid | holds / fails | Every compared candidate that answers the other way is removed |
| which | Two full candidates are not shown equal and no input separates them | One, or neither | The other, or both, removed |
| accept | No candidate is full; three are shown with what each drops and adds | One (recorded as an acknowledgement), or none | Ends, or the three are removed and the next three shown |

The oracle author is given the intended reading as a sentence of the book. It answers the system and operation from
it, an input question with that reading's value on the Lean model, and accepts a candidate only if it is the same
Lean term as the gold or Lean's kernel proves them equal. It is not a person: it never errs and never settles for a
near miss, so its numbers bound what the questions can do.

The search for a question is `clausal separate`'s, run once for all compared candidates (`dialogue.Related`); no
Rust is run in a dialogue.

## The proposer interface (L1f is not built)

`clausal/propose.py` states what a proposer is given, what it must return and how that is checked and attested;
the module text is the contract. In short:

- **Given**: the rough sentence and its hash, the system if stated, the digests of the books, and the command that
  prints the tree schema generated from the book.
- **Must return**: `{schema: "clausal-proposal-v1", rough_sha256, proposed_by: {kind, id, ...}, trees: [at most 8
  trees in the L1e JSON], alignment?, no_tree?}`. No field carries sentence text; any other field is refused.
- **Checked**: each tree against the schema of the book as it is now; written with the compiler's writer, compiled,
  and kept only if read back as the same tree; the composer's filters; the composer's coverage of the rough
  sentence. The proposer's `alignment` is recorded and not used. A proposal never chooses.
- **Attested**: one record per rule in `<FILE>.compose.json` with `proposed_by` as returned, the checks, and
  `chosen_by` a person or the rule. The evidence-graph kind and the strict-mode rule are not built.

`check` was exercised by hand on four trees (the right one kept with full coverage; an unknown piece and a prose
field dropped at the schema; a tree with the narrowing removed kept and flagged CONDITION DROPPED). There is no
committed test of it and no adversarial proposer.

## Measurements of the second part

Reproduce from the repository root (`S` is any scratch directory; every job that runs Lean or cargo goes through
`tools/sem.sh 3 --`):

```sh
python3 clausal/compose_tests/v2.py --json                                  # about 25 minutes under load, no Lean
(cd clausal && ../tools/sem.sh 3 -- python3 compose_tests/oracle.py)        # the oracle author on the separate_tests cases
bash clausal/mutation/workcopy.sh $S/clausal
tools/sem.sh 3 -- python3 clausal/compose_tests/dev.py $S/clausal           # the development set; about 15 minutes of composing, then the replay
```

### Tests on the book's fixtures and the builder's snapshots (`compose_tests/v2.py`)

94 checks, all passed. What moved against the first part:

| Test | First part | Second part |
|---|---|---|
| Identity (66 fixture Rule lines come back as themselves, full coverage, locked term) | 66 of 66 | 66 of 66 |
| The 20 refused fixture lines: answered | 0 | 0 |
| Seeded drop (a condition or narrowing deleted from each fixture tree) reported | 43 of 43 | 43 of 43 |
| Generator reach with the identity step off, of 66: answered with the same term | 25 | 32 |
| The same: ASK (reading) / ASK (dropped) / ASK (system) / answered with another term | 22 / 11 / 8 / 0 | 21 / 5 / 8 / 0 |
| The 5 fixture lines of two or more clauses, identity step off: answered with the same term | not measured (the generator wrote one clause) | 3; the other 2 are asked with the fixture's own sentence among those shown |
| Version 1's thirteen sentences (`cases.json`): ANSWER / ASK (dropped) / ASK (system) / DECLINE | 2 / 9 / 1 / 1 | 6 / 5 / 1 / 1 (not judged; none has a dropped word) |

Four expectations of the first part's tests were rewritten because the behaviour they pinned changed on purpose
(each is marked "L1c" in `v2.py`): "to" is no longer dropped; "take out" and "asking for" anchor an operation, so
the operation question is tested on two other sentences; "gives" is now a cue of "the result is"; a comparison with
its sides swapped is no longer a full candidate, so the `--l3` case is "whenever" against "exactly when".
The `--l3` case was not run after the change.

### The oracle author on the `separate_tests` cases (`compose_tests/oracle.py`)

Frozen before its run (`d932994`), with the number of questions predicted per dialogue. One case (`scope`) had been
tried by hand before the freeze. **24 of 24 dialogues end at the gold reading within three questions** (every
candidate of the 12 cases taken in turn as the intended reading): 5 with no question, 17 with one, 2 with two;
0 mispredicted counts. The control (an intended reading that is not among the candidates) ends with a candidate and
is reported as not the gold reading. Output: `compose_tests/oracle_results.json`.

### The development set (`compose_tests/dev/`), before and after

"Before" is the composer as the first part left it (`0f1c9dd`), with the dialogue and the oracle author added and
nothing else changed (`d932994`; record in `compose_tests/dev/before_l1c/`). "After" is the frozen second part
(`3147bb4`; `compose_tests/dev/REPORT.md`). Gold readings: `dev/gold.json`, 28 of the 45 sentences labelled
expressible. **Development numbers: every rule of the second part was written while looking at these sentences.**

| All 60 sentences, each in one row | A1 + oracle, before | A1 + oracle, after | A0 |
|---|---|---|---|
| Answered wrong | 0 | 1 | 43 |
| Wrong after questions | 0 | 0 | 0 |
| Answered right (no question; not contradicted on the replayable cases) | 0 | 5 | 17 |
| Right after questions (ends at the gold reading within three) | 10 | 10 | 0 |
| Asked | 48 | 44 | 0 |
| Declined | 2 | 0 | 0 |
| Declined but expressible | 2 | 0 | 0 |

- **The one wrong answer (d10) is the gold reading.** "Depositing an amount and then withdrawing the same amount
  puts the wallet back where it started" is answered "A deposit followed by a withdrawal with the same input never
  changes the wallet's balance", the same term as its gold. All five of its cases are sequences of two calls, which
  the replay does not evaluate, and the definition frozen in `dev.py` counts an unscored answer as wrong. The
  definition was left as frozen.
- **At the gold reading: 10 of 28 before, 16 of 28 after** (6 with no question: d01, d05, d10, d18, d23, d32).
  Gained: d01, d10, d15, d16, d18, d32, d34. **Lost: d31**, which the oracle reached at the third question before
  and does not reach now (joined two-clause candidates fill the first nine shown).
- Questions per sentence that ends at gold: 1.30 before, 0.75 after. Kinds asked over all 28 dialogues after:
  system 3, which 2, accept 43, input 0. **No input question was asked on the development set**, before or after:
  the separating-input question is exercised only by the `separate_tests` cases.
- 12 of the 28 are still unresolved after three questions (d02, d04, d07, d12, d19, d27, d31, d33, d35, d38, d39,
  d45).
- No sentence labelled not expressible is answered (15 of 15 asked). The 2 declines of the first part (d36, d42)
  are now ASK (dropped).
- A0's 17 "answered right" are not contradicted on the cases; 5 of them are the gold reading, 2 are separated from
  it (d35, d45) and 7 are not separated on the grid and not shown equal.
- If the first candidate of each ASK (dropped) were acknowledged unread: 17 of 42 not contradicted (first part: 18
  of 43).
- Composing the 60 sentences took 465 s before and 919 s after (twice the sentences compiled, and the clauses of a
  two-clause sentence composed separately).
- Of A0's 17 "answered right" (not contradicted on the cases), 5 are the gold reading, 7 are not separated from it on
  the grid and not shown equal, 2 are separated from it (d35, d45), and 3 have no gold reading.

### Arm A1 on the 48 frozen sentences (`compose_tests/l4r_a1/`). CONTAMINATED

One run, after the freeze of the composer (`3147bb4`) and of the gold readings (`c34d7b1`), from a private copy.
Nothing was changed after it. Version 2 was designed from version 1's failures on these sentences and the last
wave's wording changes coincide with some of them, so this is a development measure.

```sh
P=<a private directory>; cp -R trials/sentences $P/sentences; bash clausal/mutation/workcopy.sh $P/sentences/work/clausal
python3 clausal/compose_tests/l4r.py $P/sentences --gold                   # the gold readings; no composer is run
tools/sem.sh 3 -- python3 clausal/compose_tests/l4r.py $P/sentences        # the run (23 minutes of composing)
```

Gold readings: the trial's 30 expert rewordings, migrated to the current book by following the compiler's
refusals (11 needed it, none stuck). The other 18 have none.

| All 48 sentences, each in one row | A1 (version 2 + oracle author) | A0 (version 1, top candidate) |
|---|---|---|
| Answered wrong | 1 | 41 |
| Wrong after questions | 0 | 0 |
| Answered right (no question; every encodable case agrees) | 3 | 7 |
| Right after questions (ends at the gold reading within three) | 9 | 0 |
| Asked | 34 | 0 |
| Declined | 1 | 0 |
| Declined but expressible | 1 | 0 |

**Read this table with the fix round** (the last section of this file; `l4r_a1/RECOUNT.md`, `l4r_a1_sens/REPORT.md`):
"right after questions" counts a pick by the oracle author from the candidates shown (all 9), which A0 was never
offered (its 0 means "asks nothing"); 4 of the 9 are SCOPE-DIFFERS on the authors' cases, the standard of the "answered
right" row; and 1 of the 9 (`opus-1/r4`) rests on a cue word that is in two frozen sentences and in no development
sentence.

**Wrong answers first.**

- `opus-1/r3`, "A transfer from an account to itself is always rejected and changes nothing", answered "A
  transfer for which the receiver of the transfer equals the sender of the transfer is rejected and changes
  nothing". **Cause: the scoring rule, not the reading, as far as can be checked.** The sentence has no gold reading
  (the trial had no piece for it) and none of its cases is encodable, and the definition frozen in `l4r.py` counts
  an answer with no encodable case as wrong. Checked after the run: `clausal separate` proves the answer equal to
  the fixture rule `l2_same_account_rejected` ("... the sender of the transfer equals the receiver of the transfer
  ..."), which the pipeline proves for all inputs. Whether it is what the author meant was not judged by anyone
  but the builder. The development set has a near twin of this sentence (d15), and the cue that reaches it ("to
  itself") was written for d15.
- No dialogue ended at a reading other than the gold.

**Right answers.**

- Answered alone: `sonnet-1/R3` and `default-1/R02` (the same sentence, "A rejected transfer leaves every account
  balance exactly as it was") and `default-1/R01`. All three are the gold reading, and all three were already
  TOP-RIGHT for A0. The first two differ from the development sentence d16 by two words.
- After questions: 9 (`opus-1/r1`, `r4`, `r8`, `sonnet-1/R1`, `haiku-1/R01`, `R02`, `R07`, `R09`, `default-1/R06`),
  13 questions in all: 8 by accepting a candidate with dropped words (CHOSEN), 1 (`opus-1/r4`) by a system and a
  "which" question. **All nine end with the oracle picking the gold reading out of a list** (corrected in the fix
  round: the "which" question is a pick too, between "is rejected and changes nothing" and "is always rejected", which
  the grid does not separate). Seven of the nine were wrong readings for A0 by the cases; by the gold reading, A0's top
  candidate was already the gold for one of the nine (`sonnet-1/R1`).
- At the gold reading in all: 12 of 30.

**What A1 does not reach.**

- 17 of the 30 sentences with a gold reading are unresolved after three questions: the gold is not among the nine
  candidates shown. Three of them were TOP-RIGHT for A0 (`opus-1/r2`, `sonnet-1/R2`, `haiku-1/R06`). So **on
  answers without a question A1 has 3 right where A0 has 7**; by the study's signal that counts against the rule
  changes, and the 40 fewer wrong answers count for them.
- 1 decline on a sentence with a gold reading (`haiku-1/R12`, meant false): after two rounds of "none" no
  candidate was left that is askable.
- The 18 sentences with no gold reading: 17 asked (11 ASK dropped, 4 system, 1 operation, 1 reading), 1 answered
  (`opus-1/r3`). A0 answered all 18.
- **The ", and" sentences.** The study names three whose expert rewording has two clauses and which version 1
  could not write: `opus-1/r8` is reached (CHOSEN, a joined two-clause sentence proved equal to the gold);
  `haiku-1/R07` is reached with a one-clause sentence proved equal to the gold; `opus-1/r6` is not reached.
  Joined candidates were among those shown for 8 of the 34 unresolved sentences.
- No input question was asked on the 48 either (kinds: accept 63, system 1, operation 1, which 1).

**About the measure itself.**

- 7 of the 30 gold readings are not RIGHT on their author's own cases by `l4b.py`'s rule (6 SCOPE-DIFFERS: a
  case the author calls "holds" where the narrowed gold is silent; 1 NOT-EVALUABLE: a three-clause gold about two
  operations, for which no predicate is generated). An A1 answer equal to one of those would have been counted
  wrong. None occurred.
- Replay: 225 requests, 220 answers (the 5 missing are that three-clause gold).

## What a reviewer should distrust (second part)

- **Some cues fit the frozen sentences and no development sentence** (found by the reviewer of this part; the fix
  round at the end of this file): 21 of the 172 entries of `cues2.py`. One tally of A1 depends on one of them.
- **The development numbers are fitted.** Every table of `cues2.py`, the attachment rule, the forced-piece rule,
  the compile order and the limits (300 sentences compiled, 6 per frame, 6 or 4 per clause) were written or chosen
  while looking at the 60 development sentences, by the same builder who wrote their gold readings.
- **The development set is close to the 48.** Its author had not seen the 48, but wrote some of the same sentences:
  d16 is `sonnet-1/R3` and `default-1/R02` but for two words, d15 is `opus-1/r3` but for a clause. All four of
  A1's answers without a question on the 48 are sentences with such a twin or a near neighbour (d14 for
  `default-1/R01`). A1's 3 right answers there say little about sentences unlike the development set.
- **Full coverage is not correctness.** A word is counted as accounted for when a rule here says so. The rules
  added in this part are more generous than the first part's: a preposition goes with its object, a pronoun with
  the subject, "every" with the next word, a role's word asks for the one piece made from it. Each widens what
  can be answered and what can be answered wrongly. What is measured: on the development set 6 answers, all the
  gold reading; on the 48, 4 answers, 3 the gold reading and 1 equal to a proved fixture rule. Ten answers.
- **Near misses seen while building**, each closed by a rule and none measured further: "The ledger's total equals
  the sum of all account balances" was answered "A computation of the total never changes the ledger" until
  comparison words were barred from pieces that do not compare; "A withdrawal should go through when the wallet has
  enough to cover it, and be refused when it doesn't" was answered with "the maximum" for "the amount" until the
  lone-piece rule was narrowed; "... only if ..." was answered "exactly when" for one edit. The same kind of error
  can exist for phrasings nobody tried.
- **The oracle is an upper bound, and picking is all it did.** All 9 "right after questions" on the 48 and 9 of the
  10 on the development set end with the oracle picking the gold reading out of a list it is shown (the 48: 8 by
  accepting a candidate that does not account for every word, 1 by "which"; the development set: 8 and 1, and d16 by
  the system question alone). The row counts "the gold reading is among the candidates shown", not "the questions
  found it". See the fix round at the end of this file.
  It accepts by term equality or a kernel proof, so it accepted "For a lookup for which zero is at most the
  balance of account the account of the ledger, the result is ..." for `haiku-1/R07`: proved equal to the gold,
  and not a sentence a person would pick. A person can also accept a wrong candidate; the oracle cannot.
- **The separating-input question was never asked outside `separate_tests`** (0 on the development set, 0 on the
  48). The "which" question was asked 3 times in all. The path where the composer itself prints questions with
  the compiled Rust (`compose2` with the search on) ran for 2 sentences.
- **Gold for the development set is the builder's.** After the scorer fix no gold is contradicted by a case, which
  is the only check it got.
- **A scorer rule was changed after the "before" run**: a sentence of several clauses about one operation was
  judged WRONG-OPERATION. No answer of the "before" run had two clauses; three gold sentences did.
- **Unscored counts as wrong in both scorers**, which makes both wrong answers of this part (d10, `opus-1/r3`)
  answers the cases cannot judge.
- **`clausal propose` has no committed test** and no adversarial proposer; `check` was tried by hand on four trees.
- **Slower.** Composing takes about twice as long as the first part (919 s against 465 s for the 60 sentences),
  and `v2.py` about 25 minutes under load.
- **The full pipeline run was made at `3147bb4` plus the gold file.** The commits after it add results and notes.

## Proposals after A1 (nothing below was done)

1. Give an answer that no case can judge its own row ("unscored") in `dev.py` and `l4r.py`.
2. Have a non-builder write gold readings for the sentences the last wave made expressible (the study counts 4
   to 6 of the 18), so that an answer like `opus-1/r3` can be scored.
3. ASK (dropped) shows near-duplicates: the two sides of "equals" swapped, "the maximum" or "zero" for "the
   amount", a second claim added. Collapse those, and show candidates that differ in frame first; 17 of 30 golds on
   the 48 and 12 of 28 on the development set were not among the first nine.
4. Limit how many joined two-clause candidates are shown (they displaced the one-clause gold of d31).
5. Treat an argument the sentence leaves unsaid ("has enough": the amount) as a named default to acknowledge,
   not as an ADDED piece.
6. Ask the separating-input question between the best ASK (dropped) candidates as well; it is the one question a
   person can answer without reading a sentence of the book, and it is never reached now.
7. Measure the dialogue with people (H2 part two), since CHOSEN depends on recognising the right sentence.
8. Split `v2.py` so that the fast checks run without the reach measurements.
9. (fix round) Decide each of the 21 frozen-only cue entries on evidence that is not the 48: keep an entry only if
   a sentence of a NEW development set (written by someone who has seen neither the 48 nor the study) asks for it, or
   if it is the book's own wording ("at most"); record the decision per entry. Until then the tables stay as frozen.
10. (fix round) Add `cue_audit.py --check` and a rule to the freeze procedure: a cue table may not be frozen while it
    has an entry matched by a held-out sentence and by no development sentence, unless the entry is listed with a reason.
11. (fix round) Report "right after questions" in two rows from now on, in `dev.py` and `l4r.py`: reached by an input
    question, and picked from a list; and give version 1 the same oracle over its candidates in the same table.
12. (fix round) Score a dialogue's final sentence on the cases as well as against the gold, and say both in the row.

## Not done (second part)

- The model proposer, the neighbour comparison, the adversarial tests, the evidence-graph kind and the strict-mode
  rule (L1f). `clausal/propose.py` is the interface and a checker only.
- Gold readings for the 18 sentences of the 48 without one, and a second, blind reworder for any gold.
- Either / or between claims, a conjunction of conditions, an if / otherwise other than "and refused otherwise",
  conditions said only by a relative clause on a role ("a wallet that has enough money").
- Anything of L5.

# Fix round of the second part (review by another model)

Three defects were reported against the second part. None is a wrong answer of the composer; all three are about what
the numbers on the 48 can be taken to mean. **The composer is unchanged**: `compose2.py`, `dialogue.py`, `propose.py`
are byte-identical to the freeze `3147bb4`, and `cues2.py` differs from it in its opening text only (checked by
comparing the syntax trees without docstrings). Arm A1's run, results and generated report are not touched. What was
added is an audit, a sensitivity run that is not an arm, a recount of the committed results, and corrections to
this file and to the text of `cues2.py`.

## 1. Where the cues have support (`compose_tests/cue_audit.py`, `cue_audit.json`)

The text of `cues2.py` said its lines were written looking at the development set "and at nothing of
trials/sentences". No file of `trials/sentences` was opened while building, but the claim was **not true in effect**:
the study this part follows quotes words of the frozen sentences ("rejected when amount is larger", "no larger than
the number of transfers", "goes down / goes up"), and version 1's report on the 48 was written earlier in the same
stream. The text is corrected. The reviewer's check is committed as `cue_audit.py`: every entry of the tables against
the 48 frozen and the 60 development sentences (lexing only; no composer run).

Of 172 entries: 118 are matched by a development sentence, **21 by a frozen sentence and by no development sentence**
(12 of them by exactly one frozen sentence), 33 by no sentence of either set (general English, tested on nothing);
14 whole patterns match nothing in either set.

| Table | Entry | Frozen sentences (dev: none) |
|---|---|---|
| PHRASES, unchanged | "leaves ... unchanged" | `haiku-1/R01`, `opus-1/r7` |
| PHRASES, unchanged | "leaving ... untouched" | `sonnet-1/R2` |
| PHRASES, up / down | "goes up", "goes down" (the study quotes both; the development set has "go down") | `default-1/R03` |
| LIGHT verb | "applying" a batch | 9: `default-1/R07`, `haiku-1/R06`, `haiku-1/R11`, `opus-1/r10`, `opus-1/r6`, `opus-1/r7`, `sonnet-1/R11`, `sonnet-1/R6`, `sonnet-1/R7` |
| LIGHT verb | "applies" a transfer; "apply" a transfer | `haiku-1/R05`; `default-1/R07` |
| DIRECTIONS | "no larger than" (quoted by the study) | `opus-1/r6` |
| DIRECTIONS | "larger than" (quoted by the study) | `opus-1/r4`, `opus-1/r6` |
| DIRECTIONS | "at most" (also the book's own form) | `haiku-1/R04` |
| DIRECTIONS | "exceed"; "exceeds" | `default-1/R09`, `sonnet-1/R4`; `sonnet-1/R5` |
| DIRECTIONS | "within" | `opus-1/r11` |
| CUES2 `never` | "reject" | 19 |
| CUES2 `each_at_most` | "exceed" | `default-1/R09`, `sonnet-1/R4`, `sonnet-1/R5` |
| CUES2 `same_input` | "again" | `sonnet-1/R11` |
| CUES2 `never_changes` | "restore" | `sonnet-1/R12` |
| CUES2_NEG `equals` | "other" | `default-1/R03`, `default-1/R12`, `haiku-1/R09`, `opus-1/r2`, `sonnet-1/R2` |
| COORDINATORS | "but" | `haiku-1/R10` |
| DETERMINERS | "any"; "both" | 7; 4 |

The 18 entries above "but" are the reviewer's list; "but", "any" and "both" were found by extending the check to
the function-word sets. "Frozen-only" is a mechanical test. It does not show an entry was written for a frozen sentence
("at most", "any" and "exceeds" are plain English the builder would write anyway), and it cannot clear an entry that
a development sentence happens to match as well. What can be said without guessing at intent: for "larger", "goes
up" and "goes down" the study had put the frozen wording in front of the builder, and by the reviewer's reading of
the drafts "larger" was in the first draft of the table, before any development loop ran. Not audited: version 1's table, and the patterns inside
`compose2.py` (openers, role patterns, the clause splitter).

## 2. What A1 is without those entries (`compose_tests/l4r_sens.py`, `l4r_a1_sens/`). NOT AN ARM

The 21 entries were removed in the running process (`compose_tests/ablate.py`; a removed pattern match is skipped on
the author's words only, the book's own forms are still read whole) and `l4r.run_main` was run as it is. The list,
the removal rules and the control were committed (`8246d35`) before the run. This is a second pass of a composer over
the 48; it is reported as a sensitivity analysis, it replaces nothing, and nothing was changed after it.

| All 48 sentences | A1 as measured | Without the 21 frozen-only entries |
|---|---|---|
| Answered wrong | 1 | 1 |
| Wrong after questions | 0 | 0 |
| Answered right | 3 | 3 |
| Right after questions | 9 | **8** |
| Asked | 34 | 35 |
| Declined | 1 | 1 |
| At the gold reading (of 30) | 12 | 11 |

- **One row moves, and it is the one the reviewer named.** `opus-1/r4` ("... when the amount is larger than the
  sender's balance") goes from "right after questions" to "asked": without "larger" as a comparison word the
  sentence is ASK (dropped) after the system question, the gold reading is not among the first six candidates
  shown, and the dialogue is unresolved after three questions. The nearest shown is the same condition with "is
  rejected and changes nothing" for "is always rejected". **So 1 of A1's 9 depends on a cue that fits frozen
  sentences only, and 8 is the count that does not.**
- 6 more sentences differ in the first candidate shown and in nothing that is counted (`opus-1/r6`, `opus-1/r7`,
  `opus-1/r9`, `sonnet-1/R6`, `default-1/R03`, `default-1/R09`); all six are "asked" in both runs. The other 41 are
  the same in everything compared.
- The four answers without a question are the same four, so "answered right 3, answered wrong 1" does not rest on
  a frozen-only entry.
- **Control.** The development set with the same 21 entries removed (`compose_tests/dev_sens.py`): 60 of 60
  sentences give what the committed development run records (outcome, question, every shown candidate with its
  dropped and added words; for the 28 with a gold reading every turn of the dialogue and its end); no removed match
  occurred. So the development tallies do not depend on any of the 21 entries, which is another way of saying that
  no development sentence asked for them. The ablation itself was checked with an empty list (the reimplemented
  `cues2.directions` gives the frozen function's output) and on the book's forms (read whole).

## 3. What "right after questions" counts (`compose_tests/l4r_recount.py`, `l4r_a1/RECOUNT.md`)

A recount of the committed results; no composer is run, no tally of `l4r.py` is changed.

**(a) All nine end with a pick.** In each of the 9 dialogues the last turn is the oracle author naming, in a list
it is shown, the candidate that is the gold reading (the same Lean term, or proved equal): 8 "accept" turns and 1
"which" turn (`opus-1/r4`, between "is rejected and changes nothing" and "is always rejected", two readings the grid
does not separate). The earlier text of this file said 8 of 9. Between 2 and 6 candidates were put before the oracle
in each. No sentence was reached by a question about an input. The row counts **"the gold reading, or a sentence
proved equal to it, is among the candidates shown within three questions"**.

**(b) A0 was never offered a pick**, so its 0 in that row means "version 1 asks nothing". The nearest like-for-like,
measured in this round (`l4r_recount.py --a0`: the oracle's own test, `dialogue.Oracle.is_gold`, over the three
candidates of the committed A0 run; Lean, no composer):

| The 48 | A1 (version 2 + oracle author) | A0 (version 1) |
|---|---|---|
| RIGHT on the cases, no question, no pick | 3 | 7 (TOP-RIGHT) |
| RIGHT on the cases, a pick allowed | 8 (3 + 5; up to three lists of three) | 9 (TOP-RIGHT 7 + RIGHT-IN-TOP-3 2; one list of three) |
| At the gold reading, no question, no pick (of 30) | 3 | 4 |
| At the gold reading, a pick allowed (of 30) | 12 (up to three lists); 11 without the frozen-only entries | 5 (one list of three) |

So with a pick allowed and the same standard, **A1 is 12 against A0's 5 at the gold reading, and 8 against 9 by the
cases**. It is still not the same test: the dialogue shows up to three lists, the committed A0 run kept three
candidates. For 9 of the 25 sentences where none of A0's three is shown equal to the gold, one of the three is
neither separated from the gold on the grid nor proved equal (NONE-FOUND), so 5 is a count of what was shown, not a
ceiling. A0's five: `default-1/R01`, `haiku-1/R06`, `sonnet-1/R1`, `sonnet-1/R2` (top), `opus-1/r11` (among three);
A1 does not reach three of them (`haiku-1/R06`, `opus-1/r11`, `sonnet-1/R2`).

**(c) Two standards were mixed in one table.** "Answered right" and A0's TOP-RIGHT mean RIGHT on the author's cases
(every encodable case agrees); "right after questions" means at the gold reading. Of the 9, the final sentence is
RIGHT on the cases for 5 (`opus-1/r1`, `opus-1/r8`, `sonnet-1/R1`, `haiku-1/R07`, `default-1/R06`) and
**SCOPE-DIFFERS for 4** (`opus-1/r4`, `haiku-1/R01`, `haiku-1/R02`, `haiku-1/R09`): a case the author calls "holds"
where the gold reading is silent. By the cases standard those 4 would not count, in A1's "answered right" or in A0's
TOP-RIGHT. The report said only that 7 of the 30 gold readings are not RIGHT; it did not say that 4 of them are in
the row. The frozen definition in `l4r.py` is left as it is; the table above gives both.

**The same on the development set**, from `compose_tests/dev/results.json`: of its 10 "right after questions", 9
end with a pick (8 accept, 1 which) and 1 (d16) with the system question alone; A0's top candidate was already the
gold reading for 4 of the 10 (d14, d17, d29, d30).

## What the second part's numbers on the 48 are, after this round

- Answered without a question: 4 (3 RIGHT on the cases and the gold reading, 1 unscorable and counted wrong), with
  or without the frozen-only entries. A0: 7 TOP-RIGHT, 4 at the gold reading.
- The gold reading is among the candidates the dialogue shows for 12 of 30 (11 without the frozen-only entries);
  among A0's three for 5.
- By the authors' cases with a pick allowed: 8, against A0's 9.
- 41 fewer wrong answers than A0 (1 against 41 by the frozen rule) is unchanged by this round and is the part of the
  result that rests on nothing found here.

## What a reviewer should distrust (fix round)

- **The sensitivity run is a lower bracket by a mechanical rule, not a clean measure.** It removes plain English
  together with the quoted words, and it cannot remove what the builder learned from the study in other ways (which
  frames to try first, that "applying" says nothing, that two-clause sentences matter). A1 remains contaminated as
  labelled; 8 is "A1 without the entries a check can find", not "A1 uncontaminated".
- **The audit matches entries, not rules.** The attachment rules, the limits and the patterns inside `compose2.py`
  were not audited against the 48.
- **`ablate.py` was written for this round** and is tested by the control and by three hand checks only. A removed
  phrase match is skipped; the pattern is not tried again from the same start for another ending.
- **The A0 oracle count uses candidates generated at `b3303cd`** and compiles them with the current book; none
  failed to compile (verdicts: 46 SEPARATED, 18 NONE-FOUND, 17 DIFFERENT-OPERATIONS, 4 SAME-TERM, 3 NOT-SEARCHED,
  2 PROVED-EQUAL over 90 candidates).
- **`v2.py` was not rerun** (25 minutes): no code it runs was changed; that is shown by the comparison with
  `3147bb4`, not by the tests.
- **The 48 have now been passed twice** by a composer of this part (A1, and the sensitivity run). Nothing was
  tuned between or after, but a third use of them as a measure is worth less again.

# After the merge with the trust stream (INT3 fix round, 2026-11-13)

`python3 compose_tests/v2.py` on the merged tree: **one self-check fails**, "none of the REFUSED fixture Rule lines
is ANSWERED". It is left failing and its expectation is not changed. The numbers above ("the 20 refused fixture
lines: answered 0") are those of this stream's own branch and are not rewritten.

- **Cause.** The trust stream added a fixture this stream's branch did not have:
  `Rule.intake.counter_set_frozen_wording` (`features/intake.feature:32`), "For a successful intake, the last
  counter is now the counter of the message", refused on purpose with the code `RETIRED-FORM`: the book replaced
  the word 'successful' on the subject by 'accepted' (`clausebook/core.yaml`, `successful`). It is the only refused
  fixture line whose refusal is about the wording and not about what is said; the 20 this stream had are
  `SAYS-NOTHING` (12), `NARROWED-TWICE` (6) and `UNBOUND` (2).
- **What the composer gives** (`python3 compose_tests/refused_lines.py`, `compose_tests/refused_lines.json`; a
  record, with no expectation): 21 refused lines, 1 ANSWERED. The answer is "For an accepted intake, the last
  counter is now the counter of the message": the fixture line `Rule.intake.counter_set`, its term the one
  `terms.lock.json` records, coverage full (no DROPPED, no ADDED, no CONDITION DROPPED). That is the replacement the
  compiler's own refusal names, and the piece `successful` is written with its live word by design
  (`clausal/compose.py`, `subjects`). The other 20 get what they got on this stream's branch: 12 ASK (dropped),
  6 ASK (system), 1 ASK (reading), 1 DECLINE.
- **Not decided here.** Whether the check should say "no refused line is answered, except that a line refused for
  a retired form only is answered with its live form and the locked term", or whether a retired form in a rough
  sentence should be a question and not an answer, is the owner's call. Until then `v2.py` exits 1 on main.
