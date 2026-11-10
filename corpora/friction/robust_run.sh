#!/bin/zsh
# Robustness variants of the friction export (review fixes).  usage: robust_run.sh <ns|carleson|pfr> <variant> [nshards]
#   split      baseline rules, but HasDeriv*/HasFDeriv*-style "the derivative IS ..." facts are their own
#              side class `derivval` instead of `regularity` (regularity + derivval = baseline regularity)
#   splitinst  split + a Prop-valued instance-implicit argument (NeZero, Nat.AtLeastTwo, BorelSpace, ...)
#              is an instance argument, not a side-condition proof
#   aux        split rules on the proofs that sit OUTSIDE `kind == theorem`: auxiliary theorem constants
#              generated for definitions / instances / structures, and Prop-typed non-theorem declarations
#   preds      table of what every project-defined predicate contains (one process, no shards)
# Needs run.sh to have been run (modules_arg.txt, primary.txt, theorems.txt).  Writes only under
# out/corpus/friction/<corpus>/robust/.  Reads the corpus's BUILT environment; builds nothing in it.
set -e
export PATH="$HOME/.elan/bin:$PATH"
HERE=${0:A:h}; REPO=$HERE/../..; C=$1; V=$2; N=${3:-14}
case $C in
  ns)       ROOTS=NavierStokes,Euler,ComparatorChallenges ;;
  carleson) ROOTS=Carleson ;;
  pfr)      ROOTS=PFR,PFRPalomar ;;
  *) echo "unknown corpus"; exit 1 ;;
esac
SRC=$REPO/corpora/$C; I=$REPO/out/corpus/friction/$C; O=$I/robust; B=$HERE/build/$C
TC=$(cat $SRC/lean-toolchain)
mkdir -p $O/shards $B
if [[ ! -x $B/friction || $HERE/Friction.lean -nt $B/friction ]]; then
  (cd $HERE && lean +$TC -o $B/Friction.olean -c $B/Friction.c Friction.lean && leanc +$TC -O3 -rdynamic -o $B/friction $B/Friction.c)
fi
LP=$SRC/.lake/build/lib/lean; for d in $SRC/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
ulimit -s 65520
export LEAN_SYSROOT=$(lean +$TC --print-prefix)
python3 -I $REPO/bench/friction_robust.py mkconfig
CFGD=$REPO/out/corpus/friction/robust
S=$(date +%s)
case $V in
  preds)
    # depth 8 = opened all the way down; depth 2 = the predicate itself and one more level (an abbreviation of a structure)
    for D in 8 2; do
      LEAN_PATH=$LP $B/friction $CFGD/cfg_split.json $I/modules_arg.txt $ROOTS $I/primary.txt $I/theorems.txt $O/p preds $D > $O/log.preds$D.txt 2>&1 &
    done; wait
    echo "$C preds: $(( $(date +%s) - S )) s, $(wc -l < $O/p.preds8.jsonl) predicates"; exit 0 ;;
  split)     CFG=$CFGD/cfg_split.json; T=$I/theorems.txt ;;
  splitinst) CFG=$CFGD/cfg_splitinst.json; T=$I/theorems.txt ;;
  aux)
    CFG=$CFGD/cfg_split.json; T=$O/aux_targets.txt
    LEAN_PATH=$LP $B/friction $CFG $I/modules_arg.txt $ROOTS $I/primary.txt $I/theorems.txt $O/a auxlist 1 > $O/log.auxlist.txt 2>&1
    python3 -I $REPO/bench/friction_robust.py auxtargets $C ;;
  *) echo "unknown variant"; exit 1 ;;
esac
rm -f $O/shards/$V.*(N)
for k in $(seq 0 $((N-1))); do
  LEAN_PATH=$LP $B/friction $CFG $I/modules_arg.txt $ROOTS $I/primary.txt $T $O/shards/$V $k $N > $O/shards/$V.log.$k.txt 2>&1 &
done; wait
python3 -I $REPO/bench/friction_robust.py merge $C $V
rm -f $O/shards/$V.hyps.*.jsonl $O/shards/$V.consts.*.jsonl $O/shards/$V.heads.*.jsonl
echo "$C $V: $(( $(date +%s) - S )) s"
