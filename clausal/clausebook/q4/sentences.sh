#!/usr/bin/env bash
# Plan node Q4: the 48 frozen sentences (trials/sentences/authors.json), compiled AS WRITTEN by the compiler before the
# first batch and by this tree's, in PRIVATE copies of trials/sentences (nothing under trials/ is written or edited), and
# the 30 expert rewordings of trials/sentences/rewordings.py, which were written with the old forms.
#   usage (from clausal/):  bash clausebook/q4/sentences.sh [rev-before, default 891bf01] [directory, default a new temporary one]
# No Lean is run: the compiler is Python.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUSAL="$(cd "$HERE/../.." && pwd)"; REPO="$(cd "$CLAUSAL/.." && pwd)"
REV="${1:-891bf01}"; D="${2:-$(mktemp -d)}"
NEEDS="clausal clausebook glossary.yaml features controls"
for tag in before after; do
  mkdir -p "$D/$tag/work"
  cp "$REPO"/trials/sentences/*.py "$REPO"/trials/sentences/*.json "$D/$tag/"
done
( cd "$REPO" && git archive "$REV" $(for n in $NEEDS; do echo "clausal/$n"; done) clausal/lean/translation.json ) | tar -x -C "$D/before/work"
mkdir -p "$D/after/work/clausal/lean"
for n in $NEEDS; do cp -R "$CLAUSAL/$n" "$D/after/work/clausal/"; done
cp "$CLAUSAL/lean/translation.json" "$D/after/work/clausal/lean/"
for tag in before after; do
  echo "== $tag ($([[ $tag == before ]] && echo "$REV" || echo "this tree"))"
  ( cd "$D/$tag" && python3 check_author.py authors.json --compile > as_written.txt 2>&1; tail -1 as_written.txt
    python3 "$HERE/sentences_measure.py" | tail -2 )
done
( cd "$D/before" && python3 "$HERE/sentences_migrate.py" dump "$D/rewordings_before.json" > /dev/null )
echo "== the rewordings this tree refuses, rewritten by following the refusals"
( cd "$D/after" && python3 "$HERE/sentences_migrate.py" check "$D/rewordings_before.json" | tail -1 )
echo "(private copies and full output: $D)"
