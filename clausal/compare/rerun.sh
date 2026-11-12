#!/usr/bin/env bash
# Rerun the whole K2 comparison: freeze the slice, regenerate the mutants, run the four arms on every
# mutant, confirm lost proofs, count the cost, rebuild TRADES.md from the template.
#
#   ./rerun.sh [jobs]          default 8 parallel pipeline copies (each ~1.3 GB under work/)
#
# Needs: the slice's own toolchain (see ../TOOLCHAIN.md; ../run.sh must pass), cargo-mutants and
# Kani on PATH:
#   cargo install --locked cargo-mutants kani-verifier && cargo kani setup
# Takes 2 to 3 hours with 9 jobs on an 18-core machine that other work is also using; most of it is
# the Lean pipeline (one full run per mutant) and Kani on the ledger.
# Results that already exist under results/raw are kept (delete results/raw to start again).
# To compare a different commit of slice/: harness/snapshot.sh <commit> first.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
JOBS="${1:-8}"

harness/snapshot.sh                                  # slice/ at the commit in SLICE_COMMIT -> work/snapshot
python3 harness/mutants.py                           # mutants/cargo-mutants.json, mutants/hand-written.json
python3 harness/freeze.py --check || echo "NOTE: the frozen files differ from results/frozen.json (see PREREG.md)"
python3 harness/run.py --jobs "$JOBS"                # results/raw/<mutant>.json, results/raw/baseline.json
python3 harness/kani_retry.py --jobs 4               # Kani harnesses that timed out, once more with 900 s
python3 harness/analyse.py                           # results/results.json (needed by the next step)
python3 harness/confirm.py --jobs 6                  # lost proofs: replay another arm's input (or mutants/hand-witnesses.json) on the Lean model
python3 harness/analyse.py                           # results/results.json, summary.json, tables.md
python3 harness/cost.py --time-proofs                # results/cost.json, cost.md, proof_times.json
python3 harness/trim.py                              # cut the kept pipeline logs down to their tails
python3 harness/report.py                            # TRADES.md from TRADES.template.md + the tables
python3 harness/facts.py                             # the numbers the prose of TRADES.md quotes: check them by eye
