#!/usr/bin/env bash
# Run Aeneas's own extraction test suite (the `extract-tests` target of its Makefile) with a given aeneas binary,
# in a private git worktree of the unpatched commit, and report (a) tests whose runner exits non-zero and
# (b) committed test outputs that the run changed.
#   scripts/run_tests.sh <variant>        binary: bin/aeneas-<variant>; worktree: tests-wt/<variant>; report: tests-out/<variant>/
set -uo pipefail
FORK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
. "$FORK/env.sh"
V="$1"; BASE=0d21a9ec
WT="$FORK/tests-wt/$V"; OUT="$FORK/tests-out/$V"
BIN="$FORK/bin/aeneas-$V"; RUNNER="$FORK/aeneas/bin/test_runner"; CHARON="$FORK/aeneas/charon/bin/charon"
mkdir -p "$FORK/tests-wt" "$OUT"
if [[ ! -d "$WT" ]]; then git -C "$FORK/aeneas" worktree add -q --detach "$WT" "$BASE"; fi
cd "$WT"
git checkout -q -- tests && git clean -qfd tests
mkdir -p tests/llbc
ls tests/src | grep -v -e '\.out$' -e '~$' -e '^\.' -e '#$' > "$OUT/inputs.txt"
export RUNNER CHARON BIN OUT
xargs -P 6 -I{} sh -c '"$RUNNER" "$CHARON" "$BIN" tests/llbc tests/src/"{}" > "$OUT/{}.log" 2>&1; echo "$? {}"' < "$OUT/inputs.txt" | sort -k2 > "$OUT/rc.txt"
git status --porcelain tests | grep -v '^?? tests/llbc' > "$OUT/changed.txt"
git diff --stat -- tests > "$OUT/diffstat.txt"
git diff -- tests > "$OUT/changes.diff"
echo "$V: $(wc -l < "$OUT/inputs.txt") tests, $(grep -vc '^0 ' "$OUT/rc.txt") non-zero exit, $(wc -l < "$OUT/changed.txt") files changed"
