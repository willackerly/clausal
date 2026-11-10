#!/bin/zsh
# Whole in-proof pipeline for one sample:  run_inproof_all.sh <sample> [shards=8]
set -e
HERE=${0:A:h}; R=$HERE/../..; S=$1; N=${2:-8}
python3 $R/bench/corpus_reuse.py inproof $S split $N
$HERE/run_inproof.sh $S enum
python3 $R/bench/corpus_reuse.py inproof $S merge
$HERE/run_inproof.sh $S exact
python3 $R/bench/corpus_reuse.py inproof $S after-exact
$HERE/run_inproof.sh $S probe
python3 $R/bench/corpus_reuse.py inproof $S after-probe
