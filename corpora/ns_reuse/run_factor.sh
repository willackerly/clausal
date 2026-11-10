#!/bin/zsh
# Kernel checks of the factoring experiments: run_factor.sh F1_ExactDuplicates [F2_CylinderAlgebra ...]
# Each file is one cold `lean` start (seconds, except F1 which imports the whole corpus).
export PATH="$HOME/.elan/bin:$PATH"
HERE=${0:A:h}; O=$HERE/../../out/corpus/reuse/factor; cd $HERE; ulimit -s 65520
[[ -f ReuseCheck.olean ]] || lean -o ReuseCheck.olean ReuseCheck.lean
for f in "$@"; do
  rm -f $O/$f.jsonl
  LEAN_PATH=$(cat $HERE/../ns_export/lean_path.txt):$HERE REUSE_CHECK_OUT=$O/$f.jsonl lean Factor/$f.lean > $O/$f.log 2>&1
  echo "exit $?" >> $O/$f.log
  echo "$f: $(grep -c '"ok":true' $O/$f.jsonl 2>/dev/null) ok, $(grep -c '"ok":false' $O/$f.jsonl 2>/dev/null) failed"
done
