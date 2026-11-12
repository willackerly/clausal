# Separating inputs (plan node L3)

```sh
python3 -m clausal separate "<sentence A>" "<sentence B>"      # two sentences
python3 -m clausal separate "<sentence>"                        # one sentence, every system it compiles in
        [--json] [--no-rust] [--no-prove]
```

Given two candidate readings of one rough sentence, the command answers one question: is there a concrete input
(state and arguments) on which one reading holds and the other fails? It is a tool for the author and for
`clausal compose` (L1). It is not a step of `run.sh` and it changes no verdict.

Code: `clausal/separate.py` (new), `wallet-bdd/examples/separate_replay.rs` (new), three lines in
`clausal/pipeline.py` (`main`) and two in `clausal/__main__.py` (help text). Tests: `separate_tests/`.

## What it reuses

| Step | Existing code | What `separate.py` adds |
|---|---|---|
| Compile | `vocab.Compiler.rule(rule, domain_hint)`, called once per system | Builds the `Rule` object in memory. The compiler is not changed. |
| Search on the Lean model | `newrules.script` and `rsearch.search_file`: each reading on the grid of `glossary.yaml` `param_types.*.sample`, through the definition of each frame; `rsearch.parse` | Compares the two `RBITS` strings point by point. |
| Equality | none | Two kernel attempts at `A ↔ B`, appended to the same Lean script. |
| Replay on the compiled Rust | `trees.reading_entry`, `pieces::eval_point`, `pieces::run_seq` | A small example binary that evaluates given points and prints what the call answered and left. |

Everything is written under `build/separate/<key>/` (git-ignored): `Separate.lean`, `separate.log`, `replay.json`.
The report prints the two commands that rerun the Lean script and the Rust replay.

## Verdicts

Each pair of compiled readings gets exactly one verdict.

| Verdict | Meaning | How it is decided |
|---|---|---|
| `SEPARATED` | An input of the grid on which one holds and the other fails. | The first grid point for each direction that occurs (A holds and B fails; B holds and A fails). |
| `SAME-TERM` | The two sentences compile to the same Lean term. No input can separate them. | Text equality of the compiled definitions. No search is run. |
| `PROVED-EQUAL` | Different terms, and Lean's kernel accepted a proof of `A ↔ B`. | `#print axioms` of the generated theorem shows no `sorryAx`. |
| `NONE-FOUND` | Different terms, no proof, no separating grid point. Not "equal". | The bounds are printed: every variable with every value tried. |
| `DIFFERENT-OPERATIONS` | The readings are about different operations, so no input is an input of both. | The two grids have different variables, or the readings are in different systems. Each reading gets an input of its own where it holds and one where it fails, if the grid has them. |
| `NOT-SEARCHED` | A reading has no search result. | The reason is printed (for instance a rule whose clauses are about operations with different inputs). |

A reading holds at a point when every one of its claims does. A claim says nothing about a call outside its scope,
so it counts as holding there; the report says when the input is outside what a reading is about.

## Output

`--json` prints one object:

- `candidates`: per sentence and system, `COMPILED` with the Lean definition, the composition key, the operations
  and the echo; or the compiler's refusal with its message.
- `cross_system`: present when a sentence contains an operation noun that names operations in more than one system
  ("transfer" is `w.transfer` and `l.apply`). It says where the sentence compiles, where it is refused and why.
- `comparisons`: per pair, `verdict`, `why`, `same_term`, `proved_equal_by`, `counts` (points where both hold,
  both fail, only A holds, only B holds), `bounds`, and `separating`: a list of inputs, each with
  - `values`: the input, by grid variable;
  - `holds`, `fails`: which reading is which;
  - per reading (`a`, `b`): `holds`, `in_scope`, the Lean bits, and `rust`: the bits on the compiled Rust, whether
    they agree with the Lean bits, and `calls`: the operations run, the inputs, the state before, whether the call
    answered, the answer, whether it counts as accepted, and the state after.
- `lean`, `rust`: the files written and the commands that rerun them.

Without `--json` the same is printed as text.

## The cross-system case

The compiler tries every system and reports `AMBIGUOUS` only if the sentence parses in more than one. A sentence
that parses in one system only is read there without a question, even when its noun also names an operation of
another system. `separate` reports both situations:

- **The sentence compiles in more than one system** ("A transfer is always accepted"). Both candidates are listed
  and the pair is `DIFFERENT-OPERATIONS`, with an input for each.
- **The sentence compiles in one system only** ("A transfer never changes the total of all balances"). The
  `cross_system` entry says that the noun names operations in two systems, that the rest of the sentence is in the
  words of one of them, and gives the other system's refusal. There is no second candidate to compare. To compare
  against the other system, give the reworded sentence as the second argument ("... of the ledger"); the pair is
  then `DIFFERENT-OPERATIONS`.

There is no mapping from a pair of wallets and an amount to a ledger and a transfer in the Clausebook, so the tool
does not invent a common input.

## Bounds

The bounds are the grid: the sample values of each literal type in `glossary.yaml`. Today that is six `u64`
values, five account numbers, eleven ledgers of at most four accounts, six transfers and 27 batches of at most four
transfers. A reading that compares two calls is searched on the square of its grid. `NONE-FOUND` always prints them.

## Equality attempts

Two generic scripts are tried, in order, on every pair that has a common grid and different terms:

1. `rfl`: `Iff.rfl` (equal by unfolding definitions).
2. `pointwise`: unfold the two readings and the frames they use, move the quantifiers over state and input to the
   front, and close the statement at one call with `grind`.

Neither names anything about a fixture. A pair whose equality needs a fact about the code (for instance that the
operation always answers) is not proved and stays `NONE-FOUND`. A failed attempt is the ordinary outcome and is
not reported as an error.

## Limits and things not done

- **One sentence that is ambiguous inside one system is not split into its trees.** `Compiler.clause` returns a
  refusal, not the alternatives, and this module may not change the compiler. The refusal and its message are
  shown as the candidate. A caller that already holds two `Reading` objects (L1 will) can use `compare` and
  `lean_script` directly.
- **The search is the grid only.** There is no property test with shrinking and no bounded check (Kani) asserting
  that the two readings agree. The scout lists both as the stronger "none found"; they need new code in `evgen.py`
  and `evidence/src/main.rs`, which other nodes of this wave are editing.
- **The first separating point is the first in grid order, not the smallest by any measure.** The samples are
  ordered smallest first, so it is usually small.
- **Readings with the same grid variables are compared even when their operations differ.** "A batch followed by a
  computation of the total ..." and "A batch ..." start from the same ledger and batch, so they are compared, and
  the report shows which operations each ran. This is deliberate; it is not `DIFFERENT-OPERATIONS`.
- **The answer and the state after come from the compiled Rust, not from the Lean model.** The Lean side prints
  only whether each claim holds. The report says whether the Rust bits equal the Lean bits at the point.
- **Scenario readings are not handled**, only rule sentences.
- **The Lean libraries must already be built** (`Wallet.Pieces`, `Ledger.Pieces`, `Frames.Lemmas`). If they are
  not, the pair is `NOT-SEARCHED` and `separate.log` holds Lean's message. That path was not exercised.

## Tests

See `separate_tests/README.md`. Nine cases with expectations frozen in commit `b3c0f1f`, before the first run of
any of them, and a unit test of the comparison logic.
