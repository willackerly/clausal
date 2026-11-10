#!/usr/bin/env bash
# Score the two P2 arms independently of their own reports. Writes only under p2/score/.
#
#   p2/score/score.sh                 everything below, in order (several hours under load; mutants dominate)
#   p2/score/score.sh --no-mutants    everything except the mutation run
#
# 1. frozen check   : `shasum -a 256 -c FROZEN.sha256` in each arm (read only), the manifest digest, and a diff of
#                     each arm against p2/base (only lean/Lemmas, lean/Spec/Proofs and effort/attempts.tsv may differ)
# 2. cold rebuild   : mkcopy.sh  -> p2/score/work/<arm>: base's frozen files + the arm's Lemmas and proofs, no Lean
#                     build outputs; then the full ./run.sh there (results/run-<arm>.log)
# 3. audit          : audit.py   -> results/audit-<arm>.json (exact type, module, axioms, kernel replay with
#                     leanchecker, which hand-written declarations each scenario proof reaches)
# 4. lines          : count_lines.py -> results/lines-<arm>.json
# 5. cost           : attempts.py -> results/attempts-<arm>.json (attempt log + the full build logs that
#                     lakebuild.sh left in $TMPDIR, copied once into results/buildlogs/ by step 0 below)
# 6. mutants        : cargo-mutants (unit tests, for reference) and mutants.py (scenarios + both arms' proofs)
# 7. summary        : summarize.py -> results/summary.json and the tables used in p2/RESULTS.md
set -euo pipefail
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
SCORE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
P2="$(cd "$SCORE/.." && pwd)"
cd "$SCORE"
mkdir -p results work
MUTANTS=1; [[ "${1:-}" == "--no-mutants" ]] && MUTANTS=0

# 0. the arms' full build logs (lakebuild.sh writes each to a mktemp file and never deletes it)
if [[ ! -d results/buildlogs ]]; then
  mkdir -p results/buildlogs
  T="${TMPDIR:-/tmp}"
  find "$T" -maxdepth 1 -name 'tmp.*' -newermt '2026-11-10 08:05' ! -newermt '2026-11-10 08:30' -type f | while read -r f; do
    cp -p "$f" "results/buildlogs/log.$(stat -f '%Sm' -t '%Y-%m-%dT%H:%M:%S' "$f").$(basename "$f").log"
  done
fi

for arm in fable opus; do
  A="$P2/arm-$arm"
  echo "== $arm: frozen files"
  ( cd "$A" && shasum -a 256 -c FROZEN.sha256 | grep -vc ': OK$' | sed 's/^/  lines not OK: /' ) || true
  echo "  manifest digest: $(shasum -a 256 "$A/FROZEN.sha256" | cut -d' ' -f1) (base: $(shasum -a 256 "$P2/base/FROZEN.sha256" | cut -d' ' -f1))"
  diff -rq --exclude=.lake --exclude=out --exclude=target --exclude=build --exclude=__pycache__ --exclude=.tools \
    "$P2/base" "$A" | grep -vE "lean/Lemmas|lean/Spec/Proofs/inventory|effort/attempts.tsv" | sed 's/^/  UNEXPECTED: /' || true
  echo "== $arm: cold copy and full ./run.sh"
  ./mkcopy.sh "$A" "work/$arm" >/dev/null
  ( cd "work/$arm" && ./run.sh ) > "results/run-$arm.log" 2>&1 || echo "  run.sh exit $? (see results/run-$arm.log)"
  tail -4 "results/run-$arm.log"
  echo "== $arm: audit, lines, cost"
  python3 audit.py "work/$arm" "results/audit-$arm.json"
  python3 count_lines.py "$A" "results/audit-$arm.json" "results/lines-$arm.json" > /dev/null
  python3 attempts.py "$A" results/buildlogs "results/attempts-$arm.json" > /dev/null
done

if [[ $MUTANTS == 1 ]]; then
  echo "== mutants"
  rm -rf work/mut-src && mkdir -p work/mut-src && rsync -a --exclude target/ "$P2/base/inventory/" work/mut-src/inventory/
  ( cd work/mut-src/inventory && cargo mutants --list --diff --json > "$SCORE/results/mutants-diff.json" \
      && cargo mutants -j 2 --timeout 60 -o "$SCORE/results/unit" > "$SCORE/results/unit-cargo-mutants.log" 2>&1 ) || true
  python3 mutants.py setup --workers 3
  python3 mutants.py run --workers 3 | tee results/mutants-run.log
  python3 mutants.py table
fi
python3 summarize.py > results/summary.md
echo "tables: results/summary.md"
