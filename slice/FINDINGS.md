# Vertical slice: findings (2026-11-09)

The chain works end to end on a small example: English scenarios → Lean statements → proofs about Lean code that Aeneas generated from real Rust. Assembled from the final agent's report, which was blocked from writing this file.

## Run it
`cd slice && ./run.sh` (about 15 s warm). Exits 0 when every scenario gets its expected verdict. `./run.sh --strict` currently exits 1 on purpose, because nobody has signed the glossary. Output: `slice/out/report.md` and `slice/out/graph.json`.

## Scenario verdicts (45-line Rust wallet: deposit, withdraw, transfer)

| Scenario | Verdict |
|---|---|
| A covered transfer moves the money and conserves the total | PROVED-FOR-ALL |
| Withdrawing more than the balance is rejected and changes nothing | PROVED-FOR-ALL |
| A deposit that would overflow is rejected and changes nothing | PROVED-FOR-ALL |
| A covered withdrawal succeeds and takes exactly the amount | PROVED-FOR-ALL |
| A deposit with room succeeds and adds exactly the amount | PROVED-FOR-ALL |
| Transferring more than the sender has is rejected and changes nothing | PROVED-FOR-ALL |
| A transfer the receiver has no room for is rejected and changes nothing | PROVED-FOR-ALL |
| Transferring more than you have is rejected (literal values) | PROVED-INSTANCE |
| A transfer the sender can afford always succeeds (deliberately false) | REFUTED |
| A deposit earns interest (phrase not in the glossary) | UNBOUND |
| A withdrawal both covered and not covered (contradictory Givens) | VACUOUS |
| A deposit does not touch a bystander (control for an empty Then) | PROVED-FOR-ALL, 1 of 2 Thens substantive |

The false scenario passes both of its example rows as ordinary tests. The search found `a = 1, b = u64::MAX, amount = 1`; the kernel checked that the statement is false there, and the same input fails on the compiled Rust.

## What PROVED does and does not guarantee
PROVED means Lean's kernel accepted a proof whose type is exactly the generated statement, using only Lean's three standard axioms, and a second checked theorem shows the Givens can be satisfied.

It does not mean the Rust does what the English says. Four things are trusted, not proved:

| Trusted | Risk limited by | Not covered |
|---|---|---|
| Glossary: each phrase means its Lean definition | 14 one-line entries printed in the report; each compared on a grid with a second reading in Rust; sign-off voided when an entry changes | nobody has signed; both readings wrong the same way |
| Aeneas translation, including its hand-written models of `checked_add` and `-` | example rows and counterexamples run on both model and Rust | agreement checked on 21 rows only |
| Lean kernel plus ~120 lines of audit code | both are small | a bug in either |
| rustc | standard | miscompilation; proofs see a nightly's view, tests run on stable |

The statement generator and the proof text are not trusted: Lean type-checks the first and only kernel acceptance counts for the second.

## What the review found and what changed
- **A proof of the wrong statement counted as a proof.** Replacing a proof with `theorem … : True` still gave PROVED. Fixed: the audit now requires the exact statement type.
- **Three real Rust bugs survived every proof.** The first eight scenarios left most success paths unspecified. Fixed with four more scenarios and a checked coverage theorem per operation.
- **A misleading glossary entry passed silently.** Fixed in part: each phrase now has a second reading in Rust, compared on a grid.

## Mutation test (18 hand-picked bugs injected into the Rust)

| Scenario set | Noticed |
|---|---|
| First 8 scenarios | 11 of 18 |
| Current 12 scenarios | 18 of 18 |

- The example rows alone catch 17 of the 18. The proofs caught one bug the tests miss: a deposit of exactly 1,000,003 that credits one unit too few.
- The crate's own unit tests miss three.
- A proof can fail when nothing is wrong, so a failed proof means "not shown", never "false".

## Schema
`docs/SCHEMA.md` holds version 2 of the refinement graph: nodes with a statement and one or more implementations, edges carrying evidence of four kinds (kernel-checked, tested, tool-trusted, human-asserted), and staleness computed from content digests. It validates the slice's real graph (109 nodes, 275 edges) and a small maths example (11 nodes from the Pell demo), the latter assembled by hand.

## Limitations
- The code is three straight-line functions: no loops, collections, traits or I/O. Whether proofs stay short on real code is the largest unknown.
- The glossary is unreviewed, so every PROVED rests on one agent's reading of the English.
- The counterexample search is a small boundary grid; a bug away from boundaries shows only as a failed proof.
- The 18 mutants were chosen by the agent that wrote the scenarios.
- The maths side does not yet emit the schema itself.
- Toolchain: Charon needs one exact Rust nightly and Aeneas pins Lean 4.35.0, so the slice carries its own Mathlib (about 12 GB in all).

## Next steps
1. Try code with a loop over a collection, where proofs need invariants.
2. Have the maths side write the graph directly.
3. Read and sign the 14 glossary entries (`python3 -m slicegen review all --reviewer NAME`), then make `--strict` the default.

Detail: `slice/DESIGN.md`, `slice/TOOLCHAIN.md`, `slice/mutation/results.md`, reviewers' evidence in `slice/review/`.
