# p2/base: the slice pipeline on one new crate, for plan node P2

A working copy of the `slice/` pipeline (Gherkin scenarios -> Lean statements about the Aeneas model of real
Rust -> kernel-checked verdicts), taken on 2026-11-10 at 07:37 EST. Its wallet and ledger fixtures and their
proofs and lemma libraries were removed. In their place is one new crate, `inventory/`, whose seven loop
functions are the subject of the P2 proof-writing task. **If you are writing proofs, read `TASK.md` first.**

    ./run.sh                    # regenerate everything; per-scenario and per-Rule report (about 20 s warm)
    ./run.sh --no-rust --no-adequacy   # the same without cucumber-rs and the suite adequacy note (faster)
    ./lakebuild.sh <Lean module>       # `lake build` of one module, the attempt logged in effort/attempts.tsv
    ./workcopy.sh <dest-dir>           # your own working copy (shares the tool and Mathlib caches by symlink)
    python3 effort/count.py            # hand-written Lean against Rust code lines
    shasum -a 256 -c FROZEN.sha256     # nothing frozen has changed

## Layout

    crates.txt              the Rust crates under test (one: inventory)
    inventory/              the Rust under test: src/lib.rs (161 lines, 7 functions with loops) + unit tests in tests/
    features/inventory.feature   7 Rules, 16 universal scenarios (Scenario Outlines with Examples)
    glossary.yaml           phrase -> Lean definition / model function, and how arguments are wired
    lean/Vocab/Inventory.lean    the Lean side of the glossary (namespace IVocab), incl. three reference definitions
    bdd/                    cucumber-rs runner: src/lib.rs (the Rust reading of each phrase), tests/bdd.rs (steps),
                            tests/readings.rs (the two readings compared on a grid)
    lean/Generated/         Aeneas output, never edited
    lean/Bdd/               fixed support: bridge lemmas, executable Check, the audit
    lean/Spec/Statements.lean, Checks.lean   GENERATED each run from features/ + glossary.yaml
    lean/Spec/Proofs/inventory/<scenario>.lean   one proof module per scenario (sorry stubs in the frozen task)
    lean/Lemmas/            helper lemmas written by whoever writes the proofs (empty in the frozen task)
    lean/Run/               GENERATED scripts run once per pipeline run (search, audit, adequacy)
    slicegen/               generator and reporter (untrusted Python)
    effort/                 attempts.tsv (every ./lakebuild.sh call), count.py
    schema/                 JSON Schema of out/graph.json
    TASK.md, SCENARIOS.tsv, FROZEN.sha256   the frozen P2 task
    DESIGN.md, TOOLCHAIN.md design notes and toolchain pins of the slice, written for the earlier wallet and
                            ledger fixtures (which are not in this copy); paths there say lean/Wallet, lean/Ledger

## What changed from slice/ (pipeline only)

- The Lean library `Wallet` (statements, checks, proofs) is called `Spec`; the glossary definitions live in
  library `Vocab`; helper lemmas in library `Lemmas`. Proof modules are `Spec.Proofs.<feature>.<scenario>`.
- The crate list is `crates.txt` (was hard-coded in translate.sh, run.sh and slicegen). The runner directory
  `wallet-bdd/` is `bdd/` (package `scenario-bdd`).
- Report prose no longer names the wallet or ledger; the mutation harness is not included.
- An empty project (no crate, no feature, no glossary entry) runs end to end.

Toolchain, pins and their undo steps: `TOOLCHAIN.md`. `.tools` and `lean/.lake/packages` are symlinks into
`slice/` (shared, read-only use: never run `lake update` here).
