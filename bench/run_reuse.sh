#!/usr/bin/env bash
# H2 (reuse) pipeline, end to end:
#
#   bench/run_reuse.sh
#
#   1. Lean pass 1 (Rosette/Reuse.lean, ROSETTE_REUSE=1): enumerate the theorems of the slices, hash
#      every closed sub-statement, run `rfl` / `exact?` on the recurring ones.     (about 20-30 min)
#   2. bench/reuse.py: cluster, classify, write REUSE.md and probe_keys.json (the statements that no
#      filter explains).
#   3. Lean probe pass (ROSETTE_REUSE_PROBE=...): try one call of simp / norm_num / ring / fun_prop /
#      positivity / omega / linarith / simp_all / measurability / aesop on those statements.
#   4. bench/reuse.py again: final REUSE.md, clusters.json, summary.json.
#
# Environment: ROSETTE_REUSE_OUT (default out/reuse) and the knobs listed in Rosette/Reuse.lean.
set -eu
cd "$(dirname "$0")/.."
export PATH="$HOME/.elan/bin:$PATH"
OUT=${ROSETTE_REUSE_OUT:-out/reuse}
mkdir -p "$OUT"
lake build Rosette.Candidates || { sleep 5; lake build Rosette.Candidates; }
rm -f "$OUT/probe.jsonl" "$OUT/probe_keys.json"
ROSETTE_REUSE=1 ROSETTE_REUSE_OUT="$OUT" lake env lean Rosette/Reuse.lean
python3 bench/reuse.py "$OUT" > /dev/null
ROSETTE_REUSE_PROBE="$OUT/probe_keys.json" ROSETTE_REUSE_OUT="$OUT" lake env lean Rosette/Reuse.lean
python3 bench/reuse.py "$OUT" > /dev/null
echo "wrote $OUT/REUSE.md"
