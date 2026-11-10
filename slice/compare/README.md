# slice/compare: four kinds of evidence for the same rules (plan node K2)

The same 23 universal rules of `../features/wallet.feature` and `../features/ledger.feature` are
discharged four ways, and every arm is then run against the same mutants of the two Rust crates:

| Arm | Where | Runs on |
|---|---|---|
| a. example rows | `../wallet-bdd` (cucumber-rs), unchanged | compiled Rust |
| b. property-based tests | `arms/proptests` (proptest, 10,000 cases per rule, two generator profiles) | compiled Rust |
| c. bounded model checking | `arms/kani` (Kani 0.68, one harness per rule) | the Rust's MIR, via CBMC |
| d. Lean proofs | `../run.sh`, unchanged | the Lean model Aeneas generates from the Rust |

**Read `TRADES.md`** for the results: what each arm catches by kind of rule, what only one arm catches,
what nothing catches, and what each costs. `PREREG.md` is what was fixed before the measured run.

    ./rerun.sh 9            # everything, from the frozen commit of slice/ (2 to 3 hours; see the script)

    harness/snapshot.sh     slice/ at the commit in SLICE_COMMIT -> work/snapshot (plus arms/ and harness/)
    harness/workcopy.sh     one scratch copy of the snapshot (shares ../.tools and the Lake packages by symlink)
    harness/mutants.py      mutants/cargo-mutants.json (every mutant cargo-mutants lists) and mutants/hand-written.json
    harness/freeze.py       digests of everything PREREG.md fixes -> results/frozen.json
    harness/run.py          every arm on every mutant -> results/raw/<mutant>.json (+ results/raw/lean/<mutant>/ logs)
    harness/kani_retry.py   Kani harnesses that timed out, again with 900 s
    harness/confirm.py      lost proofs: replay another arm's falsifying input on the Lean model -> results/raw/confirm/
    harness/analyse.py      results/results.json (per mutant, arm and rule), summary.json, tables.md
    harness/cost.py         lines written and wall-clock per rule and arm -> results/cost.json, cost.md
    harness/report.py       TRADES.md from TRADES.template.md and the generated tables
    harness/facts.py        prints the numbers the prose of TRADES.md quotes, to check after a rerun
    harness/trim.py         cuts the pipeline logs kept under results/raw down to their tails
    harness/kani_probe.sh, kani_probe_mutants.py
                            EXPLORATORY, after the run: Kani at other bounds (results/kani_bounds_probe.*)
    mutants/                the two mutant sets, and hand-witnesses.json (falsifying inputs written by hand, with reasons)
    arms/diff               NOT an arm: original against mutant on 2.4 million inputs, to tell equivalent
                            mutants from behaviour no rule constrains (builds only inside a scratch copy)
    rules.json              the 23 rules and the kind assigned to each
    work/                   scratch copies (git-ignored, several GB; safe to delete)

Nothing here writes outside `slice/compare/`: mutants are applied and pipelines run only in
`work/w*`, copies of the committed `slice/` tree. Tools needed beyond the slice's own:
`cargo install --locked cargo-mutants kani-verifier && cargo kani setup` (see `../../DECISIONS.md`,
"K2 trade map", for what that installs and how to undo it).
