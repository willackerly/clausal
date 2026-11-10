#!/bin/zsh
# Census supplement export.  usage: census_run.sh <ns|carleson|pfr> [nshards]
# Compiles Census.lean against the corpus's own toolchain, reads the corpus's BUILT environment in
# parallel shards.  Reuses modules_arg.txt / primary.txt / theorems.txt written by run.sh.
# Nothing in the corpus is built or modified; run.sh outputs are not touched.
set -e
export PATH="$HOME/.elan/bin:$PATH"
HERE=${0:A:h}; REPO=$HERE/../..; C=$1; N=${2:-14}
case $C in
  ns)       ROOTS=NavierStokes,Euler,ComparatorChallenges ;;
  carleson) ROOTS=Carleson ;;
  pfr)      ROOTS=PFR,PFRPalomar ;;
  *) echo "unknown corpus"; exit 1 ;;
esac
SRC=$REPO/corpora/$C; I=$REPO/out/corpus/friction/$C; O=$I/census; B=$HERE/build/$C
TC=$(cat $SRC/lean-toolchain)
mkdir -p $O $B
rm -f $O/c.*(N)
if [[ ! -x $B/census || $HERE/Census.lean -nt $B/census ]]; then
  (cd $HERE && lean +$TC -o $B/Census.olean -c $B/Census.c Census.lean && leanc +$TC -O3 -rdynamic -o $B/census $B/Census.c)
fi
LP=$SRC/.lake/build/lib/lean; for d in $SRC/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
ulimit -s 65520
export LEAN_SYSROOT=$(lean +$TC --print-prefix)
S=$(date +%s)
for k in $(seq 0 $((N-1))); do
  LEAN_PATH=$LP $B/census $I/modules_arg.txt $ROOTS $I/primary.txt $I/theorems.txt $O/c $k $N > $O/log.$k.txt 2>&1 &
done; wait
echo "$C: $(( $(date +%s) - S )) s"; cat $O/log.*.txt | tail -$N
