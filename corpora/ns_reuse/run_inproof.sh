#!/bin/zsh
# In-proof recurrence on a sample of theorems, sharded over processes.
#   run_inproof.sh <sample> enum|exact|probe
# Stages (bench/corpus_reuse.py prepares the inputs of each one and merges its outputs):
#   enum   enumerate candidates of out/corpus/reuse/inproof_<sample>/shards/<k>/sample.txt
#   exact  `exact?` on the keys in shards/<k>/exact_keys.json   -> shards/<k>/exact.jsonl
#   probe  one-tactic probe on shards/<k>/probe_keys.json       -> shards/<k>/probe.jsonl
# Each shard is one cold `lean` start (import of the whole corpus + Mathlib); no iterative loop.
# The whole pipeline for one sample is run_inproof_all.sh.
export PATH="$HOME/.elan/bin:$PATH"
HERE=${0:A:h}; O=$HERE/../../out/corpus/reuse/inproof_$1; STAGE=$2
cd $HERE; ulimit -s 65520
export LEAN_PATH=$(cat $HERE/../ns_export/lean_path.txt)
for d in $O/shards/*(/); do
  (
    export ROSETTE_REUSE_OUT=$d
    case $STAGE in
      enum)  ROSETTE_REUSE=1 ROSETTE_REUSE_EXACT=0 ROSETTE_REUSE_NOLGG=1 ROSETTE_REUSE_DECLS=$d/sample.txt \
               lean ReuseNS.lean > $d/enum.log 2>&1; echo "exit $?" >> $d/enum.log ;;
      exact) [[ -f $d/exact_keys.json ]] && { ROSETTE_REUSE_EXACTMODE=1 ROSETTE_REUSE_PROBE=$d/exact_keys.json \
               lean ReuseNS.lean > $d/exact.log 2>&1; echo "exit $?" >> $d/exact.log } ;;
      probe) [[ -f $d/probe_keys.json ]] && { ROSETTE_REUSE_PROBE=$d/probe_keys.json \
               lean ReuseNS.lean > $d/probe.log 2>&1; echo "exit $?" >> $d/probe.log } ;;
    esac
  ) &
done
wait
