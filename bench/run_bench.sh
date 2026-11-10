#!/usr/bin/env bash
# Boundary-recovery benchmark (hypothesis H1).
#
#   bench/run_bench.sh            # Lean pass (raw data) + scoring
#   bench/run_bench.sh score      # scoring only (re-uses out/bench/raw.jsonl)
#
# The Lean pass (Rosette/Bench.lean) writes one JSON line per corpus item to out/bench/raw.jsonl.
# Each item has a deterministic heartbeat budget inside Lean; on top of that this script is a
# wall-clock watchdog: if one item takes longer than ITEM_TIMEOUT seconds, or the Lean process
# dies (stack overflow, out of memory, ...), the item is recorded as failed and the run resumes
# with the next one. bench/score.py then computes ranks and writes out/bench/results.jsonl and
# out/bench/RESULTS.md.
set -u
cd "$(dirname "$0")/.."
export PATH="$HOME/.elan/bin:$PATH"

OUT=${ROSETTE_BENCH_OUTDIR:-out/bench}
RAW=$OUT/raw.jsonl
PROGRESS=$OUT/.progress
LOG=$OUT/lean.log
CORPUS=${ROSETTE_BENCH_CORPUS:-bench/corpus.json}
ITEM_TIMEOUT=${ITEM_TIMEOUT:-300}     # seconds of wall clock per item
START=${ROSETTE_BENCH_START:-0}
mkdir -p "$OUT"

if [ "${1:-all}" != "score" ]; then
  lake build Rosette.Candidates || { sleep 5; lake build Rosette.Candidates; } || exit 1
  N=$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))))' "$CORPUS")
  END=${ROSETTE_BENCH_END:-$N}
  : > "$RAW"; : > "$LOG"
  start=$START
  while [ "$start" -lt "$END" ]; do
    echo "$start starting" > "$PROGRESS"
    ROSETTE_BENCH=1 ROSETTE_BENCH_START=$start ROSETTE_BENCH_END=$END \
      ROSETTE_BENCH_OUT=$RAW ROSETTE_BENCH_PROGRESS=$PROGRESS ROSETTE_BENCH_CORPUS=$CORPUS \
      lake env lean Rosette/Bench.lean >> "$LOG" 2>&1 &
    pid=$!
    why="process exited abnormally"
    while kill -0 "$pid" 2>/dev/null; do
      sleep 2
      age=$(python3 -c 'import os,sys,time; print(int(time.time()-os.path.getmtime(sys.argv[1])))' "$PROGRESS")
      if [ "$age" -gt "$ITEM_TIMEOUT" ]; then
        why="wall-clock timeout (${ITEM_TIMEOUT}s)"
        # `lake env` runs lean as a child process: kill it too, or it keeps writing
        pkill -9 -P "$pid" 2>/dev/null
        kill -9 "$pid" 2>/dev/null
      fi
    done
    wait "$pid"; code=$?
    read -r idx state < "$PROGRESS"
    if [ "$state" = "finished" ]; then break; fi
    if [ "$state" = "done" ]; then start=$((idx + 1)); continue; fi
    # "starting" (died while importing) or "running" (died inside item idx)
    echo "item $idx failed: $why (exit code $code)" | tee -a "$LOG"
    printf '{"idx": %s, "ok": false, "error": "%s (exit code %s)"}\n' "$idx" "$why" "$code" >> "$RAW"
    start=$((idx + 1))
  done
  rm -f "$PROGRESS"
  echo "raw data: $(wc -l < "$RAW") lines in $RAW"
fi

python3 bench/score.py --raw "$RAW" --corpus "$CORPUS" --out "$OUT"
