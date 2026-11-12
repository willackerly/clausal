# `clausal compose`, suggest mode (plan node L1, first version)

```sh
python3 -m clausal compose "<rough English>" [--domain D] [--top N] [--ask K | --no-ask] [--choose K] [--write FILE.feature]
python3 -m clausal compose "<rough English>" --json [--domain D] [--top N] [--ask K] [--write FILE.feature]
```

Given a sentence in ordinary English, the command lists sentences of the Clausebook that are close to it, best
first. It is a phrasing aid for the author: the `.feature` language stays strict (one live form per piece per
position), and the composer is where an author is met. It is not a step of `run.sh` and it changes no verdict.

Code: `clausal/compose.py` (new), three lines in `clausal/pipeline.py` (`main`) and two in `clausal/__main__.py`
(help text). Tests and the first measurement: `compose_tests/`.

## What it does

No language model is used. The steps, all deterministic:

1. **Tokenise.** Lower-case words, minus a stop list, through a fixed suffix stripper (`stem`, `STOP`, `IRREGULAR`).
2. **Anchor.** The operations whose noun has a token in the sentence; if none, those whose `when` form or echo has
   one; if none, every operation (of `--domain`, if given).
3. **Generate.** For each anchored operation, the typed holes of the book's forms are filled top-down, to `DEPTH`
   pieces. Leaves are the operation's roles ("the ledger", "the amount") and numbers written in the rough sentence.
   The subject is `<a|an> [successful|rejected|internal] <noun> [followed by <a noun>] [for which <condition>]`;
   what is said of it is one claim or two joined by "and". A frame that has a Rule voice is written in it
   ("A transfer never changes ..."); a frame that has none is written "For a transfer, ...".
4. **Rank** by the rule below.
5. **Verify.** The best `COMPILE_LIMIT` sentences are compiled by the ordinary compiler (`vocab.Compiler.rule`), in
   rank order, until `--top` have passed. A sentence is kept only if it compiles and the composition the compiler
   found is the one it was generated from. Readings with the same Lean term are merged.
6. **Ask** (interactive mode). The top `--ask` candidates (default 3) are compared pairwise by `clausal separate`
   (L3). For a pair that differs, the separating input and what the compiled Rust did there are printed with the
   question the author has to answer. Nothing is chosen unless the author chooses (`--choose K`, or the prompt when
   the command runs on a terminal).

The Clausebook is read through its existing loader only (`vocab.Vocabulary`, `Parser.forms_for`, `Parser.lexical`,
`op_roles`), so the restructuring of the book (C1) should change little here.

## The guarantee

Every sentence printed compiles as written. `compose.checked` recompiles each candidate just before output and
raises if one is refused or comes back as another Lean term. The reading shown under a candidate is the compiler's
own echo of that sentence, not text made by the composer.

"As written" means with no system given, which is how a Rule line with no scenario beneath it is compiled. A
sentence that reads in two systems ("A transfer is always accepted") is AMBIGUOUS as written, so it is not offered;
the JSON lists up to five such sentences under `refused.reads_in_two_systems`. With `--domain D` the candidates are
compiled in that system (as the pipeline compiles a Rule whose scenarios are in it) and such a sentence is offered
with a note and `compiles_as_written: false`; `--write` refuses it.

## The ranking rule (frozen)

`R` is the set of tokens of the rough sentence. A candidate has parts: its pieces (operation, scoping modifiers,
frames, modifiers, domain words) and its leaves.

- `strong(p)`: tokens of the literal words of the form of `p` the candidate uses, of an operation's nouns, of a
  leaf's words, and of `CUES[p]`.
- `weak(p)`: tokens of the echo of `p` (for an operation also its `when` form).

```
score = 4 * |tokens of R in strong(p) for some part p|
      + 2 * |tokens of R in weak(p) for some part p and in no strong(p)|
      - 2 * |pieces that have cue words, none of them in R|
      - 2 * |tokens of the candidate sentence that are not in R|
      - 1 * |pieces|
```

Order: higher score; then the longer common subsequence of the rough tokens and the candidate's tokens (the
author's word order); then fewer pieces; then the shorter sentence; then alphabetical.

Two hard rules beside the score. Nothing the author did not ask for narrows the rule: a scoping piece (successful,
rejected, internal, "for which", "followed by") is generated only if one of its cue words is in `R`. A second claim
is joined by "and" only if both frames have a cue word in `R`.

Limits: at most 10 candidates returned (`CANDIDATE_LIMIT`), 5 by default; depth 4; beam 30 claims, 12 conditions,
8 for any other category; pairs among the best 8 claims of a voice; 150 sentences compiled per run.

## The cue table

`compose.CUES` gives ordinary-English cue words for the 25 frames, the scoping modifiers and the shared modifiers
(comparisons, the total, negation, quantifiers). Each line carries a comment with the meaning that justifies it
(the frame's Lean reading and echo). Domain words have no entry: their cues are the words of their own forms and
echo in the book. The table was written from the book and adjusted on thirteen sentences of the implementer's own
(`compose_tests/cases.json`); the 48 trial sentences, their rewordings and the trial's results file were not read
before the freeze. A cue only moves a candidate in the list. What a candidate means is what the compiler says.

## Which form is canonical

The book still has pieces with several forms and frames with two Rule voices. Until the ruling (Q3, Q4), the
composer writes:

- the first form of a piece as listed in the book, among forms with the same holes; the next one if the first
  would say a word twice in a row ("the transfer the transfer is valid" becomes "the transfer is valid");
- the Rule voice of a frame that has one, and "For <subject>, <Then form>" otherwise;
- "is always accepted" and "is never accepted", of the four verb phrases hard-coded in `vocab.Compiler.rule_part`.
  These two are the only forms the composer names itself (`FIXED_VPS`), because the loader does not carry them;
  Q3 moves them into the book, and the table then goes.
- a scope restriction on the subject ("a rejected transfer"), never the Then prefix "if it is rejected,".

## Where a language model could sit

`compose.model_hook` is the one marked place. Its contract: given the rough sentence, the book and the ranked
sentences, it may return further sentences and a reordering. It is trusted for nothing: each proposal would go
through the same compile check and be dropped unless it compiles, the reading shown is always the compiler's echo,
it cannot add a form, and the author still answers the separating questions. This version's hook returns nothing
and `compose` asserts that; no model is called anywhere.

## Output

`--json` prints one object: `tokens`, `operations_tried`, `anchored`, `generated`, `compiled`, `refused` (counts
and the cross-system sentences), `candidates` (rank, sentence, system, score, the words accounted for and not,
pieces no word asks for, words that are not the author's, pieces, composition key, operations, echo, Lean
definition, `compiles_as_written`), `chosen` (0, the top candidate, "rank (no human choice)"; or `--choose`),
`questions` (with `--ask K`), `limits`. Exit status 3 when there is no candidate.

`--write FILE.feature` appends `Rule: <sentence>` (making the file if needed), parses the file and compiles the new
rule; if that fails the file is put back. It needs a chosen candidate and is never implied.

## Limits and things not done

- **One clause.** No ", and" between clauses, no "if it is rejected," prefix, at most two claims, at most two
  operations in sequence. A rough sentence that says two things gets candidates for one of them.
- **Bag of words.** The rule does not see word order except as a tie-break, so "the amount is more than the
  balance" and "the balance is more than the amount" score the same. The separating question is what tells them
  apart.
- **A beam.** Fillers are cut to the beam at each category before they are combined, so the best sentence overall
  can be lost.
- **Scenarios are not composed**, only Rule lines.
- **Idioms** are generated, but the composition key is not predicted for them, so for an idiom the check is "it
  compiles" and not "it compiles to the generated tree".
- **Questions cost a Lean run each** (about 3 s a pair) and need `lean/` built and cargo; `--no-ask` skips them.
- **No interactive refinement.** The answer to a question is not fed back to narrow the list; the author picks.
