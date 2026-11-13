# The computed display (plan node Q6)

```sh
python3 -m clausal show "<sentence>" [--json] [--no-refusal] [--no-separate] [--no-rust]
```

For a compiled Rule line, and for each claim of it, the display shows:

| Line | What it says | Computed from |
|---|---|---|
| `covers` | Which calls the claim is about, and whether a call that gives no answer breaks it. | What `Frames.Op.observe` and the claim's executable reading do with an accepted answer, a rejected answer and no answer. That is the behaviour of the claim's `Frames.Calls` value. |
| `sequence` | Only for a claim about a sequence of calls ("a batch followed by a computation of the total"). That 'accepted', 'rejected' and the answer are those of the last call, which call that is, and what each call of the sequence does on the generated inputs. | Each operation of the sequence run in order at every grid point, compared with the sequence's own `run` and `accepted`. |
| `outcomes` | Only for a claim that compares two calls (frames 12, 14, 16). Each of the nine combinations of first-call and second-call outcome (accepted, rejected, no answer), marked allowed or forbidden. | The executable reading of the claim at one pair of different calls, with every pair of outcomes substituted. |
| `allowed` | One concrete case the rule allows. | The search grid. |
| `forbidden` | One concrete case the rule forbids. | The search grid, then substituted outcomes. |
| `neighbour` | The nearest neighbouring sentence that allows the forbidden case. | The neighbour's own executable reading at that case. `clausal show` also runs `clausal separate` on the pair. |

It is printed in the per-Rule block of the report (`out/report.md`, `python3 -m clausal rules`) and by
`python3 -m clausal show`. It is not written into a `.feature` file, a book or a statement, and the compiler does not
read it.

Code: `clausal/display.py`, `clausal/displaytext.py` (the words, and printing from a stored graph),
`clausal/display_lib.lean.txt` (the Lean that is the same for every rule). Tests: `display_tests/`.

## Where the display comes from

Three things only: the frame's statement at a call (`F.at`, `lean/Frames/Frames.lean`), the executable reading of the
same frame (`Frames.Check.F` and `Frames.Op.observe`, `lean/Frames/Check.lean`), and the operation the claim was
compiled to, which carries the claim's scope and its `Calls` value.

For a claim about a sequence it also uses the operations of the sequence, each as the compiler holds it (see "The sequence
line").

The display asks one kind of question: what does this claim say if the call does X? To ask it, Lean evaluates the
claim of the operation with its `run` replaced:

```lean
@[reducible] def Disp.withRun (op : Frames.Op σ α ρ) (run : σ → α → Option (ρ × σ)) : Frames.Op σ α ρ :=
  { op with run := run }
```

The scope, the notion of acceptance and the `Calls` value stay as compiled. The claim's Lean text is built from the
frame's `at:` and `check:` templates in the book, in the way `Compiler.claim` builds `Claim.any_run` for the vacuity
check of plan node Q1 (`display.any_texts`).

Two kinds of outcome are put in:

- **The model's own outcome** at each point of the search grid (`clausal/rsearch.py`; the `sample` values of
  `glossary.yaml`).
- **Substituted outcomes**: every distinct outcome the model gives anywhere on that grid (answer and state after), and
  "no answer". A substituted case is the same call made to do what the model does at another input. The code does not
  do it. The display labels it so.

The display does not read the echo (`Reading.echo`, `Claim.echo`, `echo_rule`), the book's `flat:` text or its
`coverage:` texts. `display_tests/run.py --unit` checks that neither module mentions them, and that no module of the
compiler mentions the display.

## The sequence line

`Frames.Op.andThen` gives a sequence the answer of its last call (`accepted := second.accepted`), and no answer when
either call gives none. Narrowing words and the words "accepted" and "rejected" in a frame therefore speak of the last
call. "A rejected batch followed by a computation of the total ..." is about sequences whose computation of the total
is rejected, whatever the batch did. A covers line that says "ONLY calls that are rejected" does not tell the reader
that, and a reader can take the batch for the call narrowed.

The display does not take this from the book's text about sequences, and it does not take it from the name `andThen`
in the operation's term either. It runs the calls:

```lean
def DU87.steps : DU87.S → DU87.A → Array Nat := fun st inp =>
  match (L.applyBatch).run st inp.1 with
  | none => #[2]
  | some (r0, st0) => #[if decide ((L.applyBatch).accepted r0) then 0 else 1] ++
    (match (L.total).run st0 inp.2 with
    | none => #[2]
    | some (r1, st1) => #[if decide ((L.total).accepted r1) then 0 else 1])
```

Each operation is the Lean the compiler holds for it (`ops[k]["lean"]`), each answer is judged by its own operation's
`accepted`, and each input is the part of the sequence's input the compiler gives that call (for a sequence with a
tie, the tie applied to the first call's input). `Disp.seqReport` compares this at every grid point with the outcome
of the sequence's own `run` judged by the sequence's own `accepted`: the sequence must give no answer exactly when a
call gave none, and otherwise be accepted exactly when its last call is. The line is printed only if that holds at
every point; otherwise it prints NOT SETTLED and `clausal display` stops the run. The counts after "Of the N in
scope" are the generated calls in scope of the claim, by what each call of the sequence did.

An allowed or forbidden case that is the model's own outcome is printed with what each call did. A substituted case is
not: the outcome substituted is the whole sequence's.

What is compared is the kind of outcome (accepted, rejected, no answer), not the answer's value.

## The outcome table

`Op.HoldsAt2` gives the frame's content a relation between the two answers and the two states after, and nothing else:
`Q : ρ → σ → ρ → σ → Prop`. So for a pair of calls that is in scope and related, whether the claim holds depends on the
two outcomes only. The table is therefore computed at one pair (the first pair of two different calls on the grid that
the model satisfies), for every pair of substituted outcomes, and each cell collects the pairs of outcomes of its two
kinds:

| Label | Meaning |
|---|---|
| allowed | The claim holds for every sampled pair of outcomes of these kinds. |
| FORBIDDEN | It fails for every one. |
| allowed only if both calls give the same answer | It holds exactly for the pairs with equal answers. |
| depends on the two answers | Anything else; the counts are printed. |
| (no such outcome among the samples) | The operation has no answer of that kind on the grid. For example an operation that counts has no rejected answer. |

That the table computed at one pair speaks for every pair is tested, not assumed: at every in-scope, related pair of
the grid, the entry for the outcomes the model's two calls really give is compared with the compiler's own executable
reading (`Claim.check`) at that pair (gate T1).

This is the answer to the critique's objection C2. A table built from the frame's `flat:` text has no calls guard and
no answer requirement, so for "An accepted transfer never loses acceptance when the amount is the same or larger" it
would show "accepted then rejected: forbidden". The table built here shows nine allowed cells for that sentence
(gate T2). Objection C3 is answered by the same construction: for frame 16 the rows with a first call outside the
condition still show "no answer: FORBIDDEN" for the second call.

## The cases

- **Allowed**: the first grid point (pair) in scope at which the claim is about the call and holds of the model's own
  outcome. An accepted call is preferred.
- **Forbidden**, in this order:
  1. a grid point at which the model itself breaks the claim (printed "the code BREAKS the rule here");
  2. the allowed case's own call with a substituted answer the claim forbids (an answer that leaves the state unchanged
     is tried first, then the others in grid order), then any in-scope call with one;
  3. a call made to give no answer.
- If none exists the display says the rule forbids nothing on the inputs and outcomes tried. That is what a rule that
  says nothing looks like.

## The neighbour

Neighbouring sentences are made from a single-clause Rule line by one edit (`display.neighbour_sentences`):

1. a domain word or a frame of a claim replaced by another piece of the same category with the same holes;
2. the subject narrowed to accepted or to rejected calls, or its narrowing word taken off;
3. the subject's condition taken off.

Each candidate is compiled by the ordinary compiler with its refusals on, in the books of the sentence's project. It
is kept only if it compiles to a different term about the same operation. Nearest means fewest words inserted, deleted
or replaced; ties keep the order above.

The neighbour shown is the nearest one whose executable reading holds at the forbidden case.

`clausal show` then runs `clausal separate` on the rule and up to three such neighbours, nearest first. If `separate`
finds a separating input on the model for one of them, that neighbour is shown with the input. If it finds none, the
nearest stays and the line says so: the two sentences differ on a substituted outcome and on nothing the model does
within the bounds searched. The report does not run `separate` (one Lean run and one Rust replay per pair).

## In the pipeline

- `clausal gen` writes `lean/Run/Display.lean` and `build/display.json`.
- `./run.sh` runs the script beside the reading search (step 5) and then `python3 -m clausal display`, which writes
  `out/display.json` and stops the run on a fault:
  - a claim of a compiled Rule line with no display (a Lean error);
  - a table, or a one-call reading with the model's outcome put in, that differs from `Claim.check` at a grid point;
  - a table cell inconsistent with the bits the reading search printed for the same pair (`RBITS`, `decide (F.at ...)`);
  - `decide (F.at ...)` and `Frames.Check.F` differing on a substituted outcome;
  - a covers line that is not the claim's `Calls` value;
  - a claim about a sequence with no sequence line, or one whose outcome is not its last call's at some grid point.
- `clausal report` stores each display in the graph (`attrs.reading.display` of the Rule's node). `clausal/rules.py`
  prints it from the graph.

No verdict depends on it.

## Limits

- **The grid is the bound.** Substituted outcomes are those the model gives on the grid. A forbidden case that needs an
  answer the model never gives there is not found. "No forbidden case" is a statement about these samples.
- **A rule whose scope the grid does not reach has no display.** `l2_zero_amount_rejected` (a transfer of amount zero)
  has no grid input in scope; its display says so. The reading search has the same limit.
- **One-call claims have no table.** Their content depends on the state and input, not on the outcome kinds alone.
- **Neighbours are textual edits of a single-clause line.** A rule of several clauses gets none. A neighbour the
  compiler refuses (for example a narrowed form that says nothing) is dropped without a note.
- **Equal answers are compared with `==` on the answer type**, and outcomes are deduplicated with `==` on answer and
  state. An operation whose state, input or answer type has no decidable equality gets a Lean error and no display.
  No fixture has one.
- **Answers are printed with the printer the old glossary names for the model function** (`outcome_show`), else by a
  small type class in the script. A type with neither prints as "(an answer of a type with no printer)".
- **The words around the computed values are constants in `clausal/displaytext.py`.** They are not in the signed book.
  They are not sentences of the language.
- **The probes of the covers line run at the first 12 in-scope grid points**, with every substituted outcome.
- **The sequence line is about kinds of outcome.** It shows that the sequence is accepted, rejected or without an answer
  exactly as its last call is, on the grid. It does not compare the answers' values, and it is a statement about the
  generated calls, like everything else here.
- **A sequence with a tie is named without its tie** ("a transfer followed by a transfer"): the display names the
  operations, not the words of the sentence.
- **Scenario readings have no display**, only Rule lines.
