#!/usr/bin/env bash
# Run each single-file reproduction through Charon and one Aeneas binary:  repro/run.sh <variant> [file.rs ...]
# Prints, per file: the Aeneas exit code, whether a Lean file was written, the number of errors, the fatal exception if any.
FORK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; . "$FORK/env.sh"
V="$1"; shift; cd "$FORK/repro"; FILES="${*:-*.rs}"
mkdir -p out/$V
for f in $FILES; do
  n="${f%.rs}"
  "$FORK/aeneas/charon/bin/charon" rustc --preset=aeneas --dest-file "out/$n.llbc" -- "$f" --crate-name="$n" --crate-type=rlib --edition=2021 --allow=unused > "out/$n.charon.log" 2>&1
  rm -rf "out/$V/$n"; "$FORK/bin/aeneas-$V" -backend lean -dest "out/$V/$n" -no-progress-bar -print-error-emitters "out/$n.llbc" > "out/$V/$n.log" 2>&1; rc=$?
  lean=$(find "out/$V/$n" -name '*.lean' 2>/dev/null | wc -l | tr -d ' ')
  printf '%-24s %-5s aeneas rc=%s lean files=%s errors=%s fatal=%s\n' "$n" "$V" "$rc" "$lean" "$(sed 's/\x1b\[[0-9;]*m//g' "out/$V/$n.log" | /usr/bin/grep -c '^\[Error')" "$(/usr/bin/grep -m1 'Fatal error' "out/$V/$n.log" | cut -c1-110)"
done
