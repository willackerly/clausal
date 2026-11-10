#!/bin/zsh
# Bundle-mining export.  usage: bundles_run.sh <ns|carleson|pfr>
# Compiles Bundles.lean against the corpus's own toolchain (native binary), then reads the corpus's
# BUILT environment in one process.  Nothing in the corpus is built or modified.
set -e
export PATH="$HOME/.elan/bin:$PATH"
HERE=${0:A:h}; REPO=$HERE/../..; C=$1
case $C in
  ns)       ROOTS=NavierStokes,Euler,ComparatorChallenges ;;
  carleson) ROOTS=Carleson ;;
  pfr)      ROOTS=PFR,PFRPalomar ;;
  *) echo "unknown corpus"; exit 1 ;;
esac
SRC=$REPO/corpora/$C; F=$REPO/out/corpus/friction/$C; O=$F/bundles; B=$HERE/build/$C
TC=$(cat $SRC/lean-toolchain)
mkdir -p $O $B
if [[ ! -x $B/bundles || $HERE/Bundles.lean -nt $B/bundles ]]; then
  (cd $HERE && lean +$TC -o $B/Bundles.olean -c $B/Bundles.c Bundles.lean && leanc +$TC -O3 -rdynamic -o $B/bundles $B/Bundles.c)
fi
LP=$SRC/.lake/build/lib/lean; for d in $SRC/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
ulimit -s 65520
export LEAN_SYSROOT=$(lean +$TC --print-prefix)
# modules_arg.txt and theorems.txt were written by run.sh (the hypothesis-level export)
LEAN_PATH=$LP $B/bundles $F/modules_arg.txt $ROOTS $F/theorems.txt $O/b 2> $O/log.txt
tail -1 $O/log.txt
