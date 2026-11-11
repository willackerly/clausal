#!/bin/zsh
# usage: timing.sh FID ...   -- wall time of the re-derived file, the corpus-proof file and an imports-only file, 3 runs each, one at a time
cd ${0:A:h}
export PATH="$HOME/.elan/bin:$PATH"
SRC=../ns; B=$PWD/build; TC=$(cat $SRC/lean-toolchain)
LP=$B:$PWD/$SRC/.lake/build/lib/lean; for d in $PWD/$SRC/.lake/packages/*/.lake/build/lib/lean; do LP=$LP:$d; done
for fid in "$@"; do
  # imports of the union of both files, nothing else
  (grep -h '^import' lean/${fid}_re.lean lean/${fid}_re_spec.lean | sort -u) > lean/${fid}_imp.lean
  grep -v '^run_cmd Fam.reportPairs' lean/${fid}_re.lean > lean/${fid}_re_t.lean   # the measuring block is not part of the proofs
  for v in imp re_spec re_t; do
    for k in 1 2 3; do
      s=$(python3 -c 'import time; print(time.time())')
      (cd lean && LEAN_PATH=$LP lean +$TC -DmaxErrors=100000 ${fid}_$v.lean > /dev/null 2>&1)
      e=$(python3 -c 'import time; print(time.time())')
      echo "$fid $v $k $(( e - s )) $(uptime | sed 's/.*load averages: //')"
    done
  done
done
