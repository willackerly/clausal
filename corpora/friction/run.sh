#!/bin/zsh
# Friction census export.  usage: run.sh <ns|carleson|pfr> [nshards]
# Compiles Friction.lean against the corpus's own toolchain (native binary), then reads the
# corpus's BUILT environment in parallel shards.  Nothing in the corpus is built or modified.
set -e
export PATH="$HOME/.elan/bin:$PATH"
HERE=${0:A:h}; REPO=$HERE/../..; C=$1; N=${2:-14}
case $C in
  ns)       ROOTS=NavierStokes,Euler,ComparatorChallenges; FIND=(NavierStokes Euler NavierStokes.olean Euler.olean); EXCL='^ComparatorChallenges' ;;
  carleson) ROOTS=Carleson; FIND=(Carleson Carleson.olean); EXCL='^$' ;;
  pfr)      ROOTS=PFR,PFRPalomar; FIND=(PFR PFRPalomar PFR.olean); EXCL='^PFRPalomar.Challenge$' ;;
  *) echo "unknown corpus"; exit 1 ;;
esac
SRC=$REPO/corpora/$C; O=$REPO/out/corpus/friction/$C; B=$HERE/build/$C
TC=$(cat $SRC/lean-toolchain)
mkdir -p $O/shards $B
rm -f $O/shards/*
date +%s > $O/export_start.txt
# compile (once per toolchain)
if [[ ! -x $B/friction || $HERE/Friction.lean -nt $B/friction ]]; then
  (cd $HERE && lean +$TC -o $B/Friction.olean -c $B/Friction.c Friction.lean && leanc +$TC -O3 -rdynamic -o $B/friction $B/Friction.c)
fi
LP=$SRC/.lake/build/lib/lean; for d in $SRC/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
(cd $SRC/.lake/build/lib/lean && find $FIND -name '*.olean' | sed 's/\.olean$//; s#/#.#g' | sort -u | grep -v "$EXCL") > $O/modules_arg.txt
python3 -I - $REPO/out/corpus/$C/decls.jsonl $O <<'EOF'
import json, sys
src, o = sys.argv[1], sys.argv[2]
with open(o + '/primary.txt', 'w') as p, open(o + '/theorems.txt', 'w') as t:
    for l in open(src):
        d = json.loads(l)
        p.write(d['name'] + '\n')
        if d['kind'] == 'theorem':
            t.write(d['name'] + '\n')
EOF
ulimit -s 65520
export LEAN_SYSROOT=$(lean +$TC --print-prefix)   # the binary must load the corpus toolchain's core .olean files
for k in $(seq 0 $((N-1))); do
  LEAN_PATH=$LP $B/friction $REPO/bench/friction_families.json $O/modules_arg.txt $ROOTS $O/primary.txt $O/theorems.txt $O/shards/f $k $N > $O/shards/log.$k.txt 2>&1 &
done; wait
date +%s > $O/export_end.txt
python3 -I $REPO/bench/friction_merge.py $C
rm -f $O/shards/f.hyps.*.jsonl $O/shards/f.consts.*.jsonl $O/shards/f.heads.*.jsonl   # merged; logs and per-shard meta stay
