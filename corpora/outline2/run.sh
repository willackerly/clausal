#!/bin/zsh
# Compile Outline2.lean against the corpus's own toolchain and run it against the BUILT
# environment of corpora/ns.  Nothing in the corpus is built or modified.
#   run.sh heads <names.txt> <out.jsonl>
#   run.sh print <spec.json> <out.jsonl>
set -e
export PATH="$HOME/.elan/bin:$PATH"
IN=${2:A}; OUT=${3:A}
HERE=${0:A:h}; REPO=$HERE/../..; SRC=$REPO/corpora/ns; B=$HERE/build
TC=$(cat $SRC/lean-toolchain)
mkdir -p $B
if [[ ! -x $B/outline2 || $HERE/Outline2.lean -nt $B/outline2 ]]; then
  (cd $HERE && lean +$TC -o $B/Outline2.olean -c $B/Outline2.c Outline2.lean && leanc +$TC -O3 -rdynamic -o $B/outline2 $B/Outline2.c)
fi
LP=$SRC/.lake/build/lib/lean; for d in $SRC/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
ulimit -s 65520
export LEAN_SYSROOT=$(lean +$TC --print-prefix)
cd $SRC   # read-only: the binary only opens .olean files
LEAN_PATH=$LP $B/outline2 $1 $REPO/out/corpus/ns/modules_arg.txt $IN $OUT
