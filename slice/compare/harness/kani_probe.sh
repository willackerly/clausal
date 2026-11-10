#!/bin/bash
# EXPLORATORY, written after the measured run (not part of the registered comparison): how far do the
# Kani bounds go on the UNMUTATED code when a harness runs alone?
#   harness/kani_probe.sh <out.tsv> <harness> <ACCOUNTS,BATCH,SUM_ACCOUNTS,SUM_BATCH> ...
# One configuration at a time, 600 s limit each; appends "harness A B SUM_A SUM_B seconds result" to out.tsv.
# Needs work/snapshot (harness/snapshot.sh). Scratch crates are made under $TMPDIR.
export PATH="$HOME/.cargo/bin:$PATH"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC=$HERE/arms/kani
SNAP=$HERE/work/snapshot
out="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"; h=$2; shift 2
cd "$(mktemp -d)"
for cfg in "$@"; do
  IFS=, read a b sa sb <<< "$cfg"
  d=$PWD/c_${h}_${a}_${b}_${sa}_${sb}; rm -rf $d; mkdir -p $d/src
  sed "s#../../../#$SNAP/#" $SRC/Cargo.toml > $d/Cargo.toml
  u=$(( (a > b ? a : b) + 3 )); [ $sa -gt $a ] && u=$(( sa + 3 ))
  sed "s/^const ACCOUNTS: usize = .*/const ACCOUNTS: usize = $a;/; s/^const BATCH: usize = .*/const BATCH: usize = $b;/; s/^const SUM_ACCOUNTS: usize = .*/const SUM_ACCOUNTS: usize = $sa;/; s/^const SUM_BATCH: usize = .*/const SUM_BATCH: usize = $sb;/; s/kani::unwind(6)/kani::unwind($u)/" $SRC/src/lib.rs > $d/src/lib.rs
  ( cd $d; cargo kani --only-codegen >/dev/null 2>&1
    s=$(python3 -c 'import time;print(time.time())')
    res=$(cargo kani --harness $h --exact --output-format terse -Z unstable-options --harness-timeout 600s 2>&1 | grep -E '^VERIFICATION|timed out' | tr '\n' ' ')
    e=$(python3 -c "import time;print(round(time.time()-$s,1))")
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$h" "$a" "$b" "$sa" "$sb" "$e" "$res" >> $out )
  rm -rf $d
done
