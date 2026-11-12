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
   (L3). For a pair that differs, each separating input and what the compiled Rust did there are printed with the
   question the author has to answer. When L3 returns two inputs for a pair they are numbered, and the question
   asks about each by number and values, with its own direction: the two can point opposite ways (one candidate
   holds on the first and fails on the second), so one question about "the input above" would rule out the wrong
   candidate for one of them. The same is in the JSON as `questions[].inputs` (`n`, `values`, and the ranks of the
   candidate that `holds` and the one that `fails`). Nothing is chosen unless the author chooses (`--choose K`, or the prompt when
   the command runs on a terminal).

The Clausebook is read through its existing loader only (`vocab.Vocabulary`, `Parser.forms_for`, `Parser.lexical`,
`op_roles`), so the restructuring of the book (C1) should change little here.

## The guarantee

Every sentence printed compiles as written. `compose.checked` recompiles each candidate just before output and
raises if one is refused or comes back as another Lean term. The reading shown under a candidate is the compiler's
own echo of that sentence, not text made by the composer.

"As written" means with no system given, which is how a Rule line with no scenario beneath it is compiled. A
sentence that reads in two systems ("A transfer is always accepted") is AMBIGUOUS as written, so it is not offered
as a candidate. It is not dropped silently either: up to five such sentences are printed under NOT OFFERED, whether
or not there are candidates, each with the systems it reads in and the candidate it was ranked ahead of, followed
by the question "which system is your rule about?" and the instruction to run again with `--domain`. A line above
the candidates says so when any of them ranked ahead of a candidate shown. The JSON lists the sentences under
`refused.reads_in_two_systems` and the same with `systems` and `ahead_of_rank` under `refused.ambiguous_as_written`.
Only sentences reached before `--top` candidates had passed are listed, so every one listed ranked ahead of the last
candidate shown. The non-interactive mode still takes the top candidate that compiles as written; a scorer that
wants the cross-system sentence must pass `--domain`. With `--domain D` the candidates are
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

## First measurement, L4(b): the 48 frozen sentences (2026-11-12)

One run, after the freeze commit `395a746`, never repeated or tuned. Each sentence, as its author wrote it, was the
rough input; no system was given; the top three candidates were replayed on the author's five recorded cases with
the trial's own machinery. Script, definitions and how to rerun: `compose_tests/l4b.py`. Output:
`compose_tests/l4b/REPORT.md` (every sentence, wrong readings first) and `results.json`.

| Outcome | Sentences |
|---|---|
| Top candidate agrees with the author on every encoded case | 5 of 48 |
| Not the top one, but the second or third does | 5 of 48 |
| Wrong reading (none of the top three agrees on every case) | 20 of 48 |
| No candidate | 0 of 48 |
| Not scorable: the trial has no encoded case for the sentence | 18 of 48 |

Of the 20 wrong readings, the top candidate contradicts the author on a case in 9, differs only in scope (silent
where the author says the rule holds, or the reverse) in 7, and cannot be evaluated on the cases in 4 (three are
about the wallet's transfer where the cases are about the ledger's; one compares two calls, and a case gives one).
As written, 0 of the 48 compile.

This is a negative result for the first version: it puts a reading the author's cases accept at the top for 5 of
the 30 scorable sentences, and it never declines.

### What a reviewer should distrust in these numbers

- **"Agrees on five cases" is weak, and it flatters the tool.** By the implementer's reading of the ten sentences
  with an agreeing candidate, five of those candidates do not say what the author wrote. "For a transfer, it is
  rejected" agrees with all five cases of "A rejected transfer leaves every account balance exactly as it was"
  (twice: `sonnet-1/R3`, `default-1/R02`), because all five cases are rejected transfers. "The number of transfers
  applied is at most the maximum" agrees for a sentence about the length of the batch (`default-1/R06`). The top
  candidate of `opus-1/r2` adds "and it is accepted". The third candidate of `sonnet-1/R9` is a statement about the
  total that agrees with cases written for a lookup, because the replay ignores a value the reading has no variable
  for. By that reading the top candidate says what the author wrote for 4 of 48 (`sonnet-1/R1`, `sonnet-1/R2`,
  `haiku-1/R06`, `opus-1/r11`) and a lower one does for 1 more (`default-1/R01`). This count is a judgement, not a
  measurement.
- **The 18 unscorable sentences are not neutral.** They are the sentences for which the trial runner found no
  compiling rewording that keeps the meaning (a piece is missing from the book), so no case was encoded. The
  composer printed three candidates for each. By the implementer's reading none of the 18 top candidates states the
  author's sentence. Counted that way, 38 of 48 top candidates are wrong.
- **The authors are language models**, and the case encodings were made by the trial runner, also a model.
- **The modifier adjustment is the script's own.** A "successful" or "rejected" subject reports "holds" outside its
  scope; the script turns that into "out of scope" with the trial's reference model, as `run_v4.py` does for its
  own units, but keyed on the candidate's modifier. It is not applied to a sequence of two operations.

### What went wrong, by kind (from reading the report; examples are keys in `REPORT.md`)

1. **Words about coverage are read as claims or scope.** "whether it is accepted or rejected" produced "A rejected
   transfer ... and is never accepted" (`opus-1/r1`). "An accepted transfer" produced "... and is never accepted"
   ahead of "A successful transfer ..." (`haiku-1/R01`, `default-1/R01`).
2. **The wrong system.** "the total of all balances" is, word for word, the wallet's form, so a sentence about the
   ledger got wallet candidates first (`opus-1/r1`, `sonnet-1/R4`, `haiku-1/R01`, `default-1/R01`).
3. **Sentences that say two or three things.** One clause with at most two claims cannot carry "lowers the sender,
   raises the receiver, and leaves every other account untouched", or "X, while Y" (`opus-1/r8`, `haiku-1/R07`,
   `default-1/R03`, `sonnet-1/R7`).
4. **Which way round.** "rejected when the amount is larger than the sender's balance" became a variation ("when
   the amount is larger") or a comparison with the arguments in the wrong places (`opus-1/r4`, `sonnet-1/R4`,
   `default-1/R09`, `haiku-1/R10`).
5. **Self-defeating and empty candidates are offered.** "For a rejected transfer, it is accepted";
   "A rejected transfer is accepted exactly when ..."; "... increases the balance ... by exactly zero";
   "for which zero is not more than the total ..." (`sonnet-1/R3`, `haiku-1/R10`, `haiku-1/R02`, `sonnet-1/R9`).
6. **No way to say "nothing fits".** A candidate was printed for every sentence, including all 18 the book cannot
   express, with scores as low as -3.
7. **"either ... or" and "if ... otherwise"** have no form, and the composer picked one half (`opus-1/r7`,
   `haiku-1/R05`, `sonnet-1/R7`).

### Proposals (not done; the frozen version was not changed after the run)

Each needs its own freeze and a fresh test set: the 48 are now seen, so any gain on them after a change is
contaminated (L5 is the clean test).

- **Abstain.** Print "no candidate" below a score threshold or when a named share of the content words is not
  accounted for, with the words left over. Threshold chosen on sentences that are not the 48.
- **Drop candidates the tools already know to be empty or self-defeating**: a reading whose scope is empty or that
  holds of every call (Q1's check), a "rejected" subject with an acceptance claim, "by exactly zero".
- **Treat coverage words as scope, not claims.** "accepted or rejected", "whether ... or not", "in every case" ask
  for no modifier; "an accepted X" asks for "successful". This needs phrase cues, not single tokens.
- **Decide the system first.** When a noun names operations in two systems, score the systems on the domain words
  of the whole sentence (ledger, account, wallet) before generating, or ask the cross-system question first.
- **Compose clause by clause.** Split the rough sentence at commas, "and", "while", ";" and compose each part with
  the subject carried over; join with ", and". This is the largest gap.
- **Use word order inside comparisons.** Score a condition by the order of its arguments in the rough sentence, not
  only as a tie-break of the whole sentence.
- **Use L3 before printing, not only for the question.** Run the reading search on the top candidates and show
  beside each whether it is false of the code on the grid; drop one of two candidates that are proved equal.
- **Feed the answer back.** After the author answers a separating question, remove the candidates the answer rules
  out and ask the next one.
- **A language model at the marked hook**, proposing sentences and reordering, each proposal compiled and none
  trusted. The measured comparison is this table against the same table with the hook on.
- **Score with more than five cases.** Agreement on the author's five cases let "For a transfer, it is rejected"
  count as right. L4 should also run the reading search and count a candidate that the code refutes, when the
  author meant the rule to be true, as wrong.
