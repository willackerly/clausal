#!/bin/zsh
# M9 families generalisation: compile files against the BUILT ns environment (read only).
# usage: run.sh File1 File2 ...   (module names in dependency order, without .lean)
# One `lean` process per file; oleans go to corpora/lesssim/build.  No lake, no corpus rebuild.
set -e
export PATH="$HOME/.elan/bin:$PATH"
HERE=${0:A:h}; REPO=$HERE/../..; SRC=$REPO/corpora/ns; B=$HERE/build
TC=$(cat $SRC/lean-toolchain)
mkdir -p $B
LP=$B:$SRC/.lake/build/lib/lean; for d in $SRC/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
for f in "$@"; do
  echo "== $f"
  s=$(date +%s)
  rm -f $B/$f.out; (cd $HERE/lean && FAM_OUT=$B/$f.out LEAN_PATH=$LP lean +$TC -DmaxErrors=100000 -o $B/$f.olean $f.lean) 2>&1 | tee $B/$f.log
  echo "   $(( $(date +%s) - s )) s"
done
