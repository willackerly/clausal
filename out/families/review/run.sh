#!/bin/zsh
# Review copy of corpora/families/run.sh: compiles the copied files under out/families/review/lean
# into out/families/review/build, against the BUILT ns environment (read only). One lean process at a time.
set -e
export PATH="$HOME/.elan/bin:$PATH"
HERE=${0:A:h}; REPO=$HERE/../../..; SRC=$REPO/corpora/ns; B=$HERE/build
TC=$(cat $SRC/lean-toolchain)
mkdir -p $B
LP=$B:$SRC/.lake/build/lib/lean; for d in $SRC/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
for f in "$@"; do
  s=$(date +%s)
  rm -f $B/$f.out; (cd $HERE/lean && FAM_OUT=$B/$f.out LEAN_PATH=$LP lean +$TC -DmaxErrors=100000 -o $B/$f.olean $f.lean) > $B/$f.log 2>&1 || true
  echo "== $f  $(( $(date +%s) - s )) s  errors=$(grep -c ': error' $B/$f.log)  sorry=$(grep -ci 'sorry' $B/$f.log)"
done
