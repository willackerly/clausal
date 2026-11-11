#!/bin/zsh
# Shared setup: source with PROJECT=<ns|carleson|pfr> set.  Nothing in the corpus is built or modified.
export PATH="$HOME/.elan/bin:$PATH"
HERE=${0:A:h}; REPO=$HERE/../..
case $PROJECT in
  ns)       ROOTS=NavierStokes,Euler ;;
  carleson) ROOTS=Carleson ;;
  pfr)      ROOTS=PFR,PFRPalomar ;;
  *) echo "unknown project $PROJECT"; exit 1 ;;
esac
SRC=$REPO/corpora/$PROJECT
TC=$(cat $SRC/lean-toolchain)
B=$HERE/build/$PROJECT
O=$REPO/out/reinvent/$PROJECT
mkdir -p $B $O/raw
LP=$B:$SRC/.lake/build/lib/lean; for d in $SRC/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
export LEAN_SYSROOT=$(lean +$TC --print-prefix)
ulimit -s 65520
