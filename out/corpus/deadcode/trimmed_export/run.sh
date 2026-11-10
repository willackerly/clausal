#!/bin/zsh
# Re-export the declaration graph from the BUILT trimmed corpus with the unchanged exporter of corpora/ns_export.
set -e
export PATH="$HOME/.elan/bin:$PATH"
R=/Users/will/dev/lean-rosette; O=$R/out/corpus/deadcode/trimmed_export; W=$R/corpora/ns_trim/work; N=${1:-6}
LP=$W/.lake/build/lib/lean; for d in $R/corpora/ns/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
MAINS=(NavierStokes.Comparator.navier_stokes_breakdown_R3 NavierStokes.Comparator.navier_stokes_breakdown_periodic Euler.euler_breakdown_R3 Euler.exists_compact_smooth_euler_singularity)
ulimit -s 65520
cd $W
for k in $(seq 0 $((N-1))); do
  LEAN_PATH=$LP $R/corpora/ns_export/export $O/modules_arg.txt $O/shards/decls.$k.jsonl $O/axioms.json $O/export_meta.json $k $N $MAINS > $O/shards/log.$k.txt 2>&1 &
done; wait
cat $O/shards/decls.*.jsonl | LC_ALL=C sort > $O/decls.jsonl
cat $O/shards/log.*.txt > $O/export.log; rm -rf $O/shards
wc -l $O/decls.jsonl
