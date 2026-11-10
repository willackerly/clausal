#!/bin/zsh
# Rebuild the exporter and re-export the declaration graph of corpora/ns (about 3.5 min on 18 cores).
# Prerequisite: corpora/ns built (`lake exe cache get && lake build`, about 18 min).
set -e
export PATH="$HOME/.elan/bin:$PATH"
HERE=${0:A:h}; NS=$HERE/../ns; O=$HERE/../../out/corpus/ns; N=${1:-14}
MAINS=(NavierStokes.Comparator.navier_stokes_breakdown_R3 NavierStokes.Comparator.navier_stokes_breakdown_periodic Euler.euler_breakdown_R3 Euler.exists_compact_smooth_euler_singularity)
cd $HERE && lean -c Export.c Export.lean && leanc -O3 -rdynamic -o export Export.c
cd $NS
LP=$NS/.lake/build/lib/lean; for d in .lake/packages/*/.lake/build/lib/lean; do LP=$LP:$NS/$d; done
mkdir -p $O/shards
(cd .lake/build/lib/lean && find NavierStokes Euler ComparatorChallenges NavierStokes.olean Euler.olean -name '*.olean' | sed 's/\.olean$//; s#/#.#g' | sort -u) > $O/modules_built.txt
grep -v '^ComparatorChallenges' $O/modules_built.txt > $O/modules_arg.txt   # challenge files restate the main theorems with sorry
ulimit -s 65520
for k in $(seq 0 $((N-1))); do
  LEAN_PATH=$LP $HERE/export $O/modules_arg.txt $O/shards/decls.$k.jsonl $O/axioms.json $O/export_meta.json $k $N $MAINS > $O/shards/log.$k.txt 2>&1 &
done; wait
cat $O/shards/decls.*.jsonl | LC_ALL=C sort > $O/decls.jsonl
cat $O/shards/log.*.txt > $O/export.log; rm -rf $O/shards
python3 $HERE/stats.py $O $MAINS > /dev/null
wc -l $O/decls.jsonl
