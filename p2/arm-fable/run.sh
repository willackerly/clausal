#!/usr/bin/env bash
# One command: regenerate everything and print the per-scenario and per-Rule report.
#
#   Rust (the crates in crates.txt) --Charon+Aeneas--> Lean models (lean/Generated/)
#   features/*.feature + glossary.yaml --slicegen--> Lean statements + executable checks
#   lake build        kernel-checks the models, the statements, any hand-written helper lemmas
#                     (lean/Lemmas/) and the hand-written proofs (lean/Spec/Proofs/)
#                     (one Lean module per scenario, so one broken proof costs one scenario)
#   Run/Search.lean   evaluates Examples rows on the model; boundary-grid search for a
#                     satisfying input and for a counterexample; evaluates every glossary
#                     definition on a grid of arguments
#   Run/Audit.lean    kernel-checks theorems derived from the search (satisfiable Givens,
#                     contradictory Givens, refutation at the counterexample, input coverage),
#                     collects axioms, and checks that every proof has the type of its statement
#   cucumber-rs       runs the same feature files against the compiled Rust, replays each
#                     counterexample on it, and evaluates the Rust reading of every phrase on
#                     the same grid as the Lean definitions
#   Run/Adequacy.lean, Run/AdequacyAudit.lean
#                     SUITE ADEQUACY NOTE, informational: each scenario stated again with a trivial model
#                     (rejects everything, does nothing, ...) in place of the call; searched on the same
#                     grid, then kernel attempts. Runs beside steps 5-7; a failure here costs the note only.
#   slicegen report   out/report.md, out/graph.json, and the report printed below (per scenario, then
#                     per Gherkin `Rule:`, the latter generated from out/graph.json)
#
# Exit status: 0 iff every scenario got the verdict it is expected to get
# (PROVED-* by default; @expect-refuted / @expect-unbound / @expect-vacuous otherwise).
#
#   ./run.sh              everything
#   ./run.sh --strict     also fail if a proved scenario rests on a glossary entry nobody has signed off
#   ./run.sh --no-rust    skip the cucumber-rs runs (no "tested on Rust" evidence, readings not compared)
#   ./run.sh --no-unit    skip the crate's own unit tests (a mutation harness uses this to see
#                         what the SCENARIOS catch on their own)
#   ./run.sh --no-adequacy  skip the suite adequacy note (about 20 s less; every verdict is the same)
#
# NOTE: this deletes and recreates out/. Keep nothing there that you want to keep.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
cd "$HERE"
CRATES="$( (grep -v '^#' crates.txt || true) | tr '\n' ' ')"

RUST_TESTS=1; UNIT_TESTS=1; ADEQUACY=1; REPORT_ARGS=()
for arg in "$@"; do
  case "$arg" in
    --no-rust) RUST_TESTS=0 ;;
    --no-unit) UNIT_TESTS=0 ;;
    --no-adequacy) ADEQUACY=0 ;;
    --strict)  REPORT_ARGS+=(--strict) ;;
    *) echo "usage: $0 [--strict] [--no-rust] [--no-unit] [--no-adequacy]" >&2; exit 2 ;;
  esac
done

step() { printf '\n== %s\n' "$*"; }

rm -rf out
mkdir -p out
rm -f lean/Run/AdequacyAudit.lean      # written again only if this run's adequacy search produced results

if [[ $UNIT_TESTS == 1 ]]; then
  step "1/8 unit tests of the Rust crates (cargo test)"
  for crate in $CRATES; do
    ( cd "$crate" && cargo test --quiet 2>&1 | grep -E '^(test result: .* [1-9][0-9]* passed|error|warning: unused)' | sed "s/^/$crate: /" || true )
    ( cd "$crate" && cargo test --quiet >/dev/null 2>&1 ) || { echo "$crate unit tests FAILED" >&2; exit 1; }
  done
else
  step "1/8 unit tests of the Rust crates: SKIPPED (--no-unit)"
fi

step "2/8 translate Rust -> Lean (Charon + Aeneas)"
./translate.sh > out/translate.log 2>&1 || { cat out/translate.log; exit 1; }
grep -E '^(aeneas|charon|rustc) ' out/translate.log
echo "wrote lean/Generated/ ($CRATES), lean/translation.json, lean/provenance.json"

step "3/8 slicegen gen: features + glossary -> Lean statements, checks, search script"
python3 -m slicegen gen

step "4/8 lake build: model, statements, hand-written proofs (kernel)"
(
  cd lean
  [[ -d .lake/packages/mathlib ]] || lake update
  ls .lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean >/dev/null 2>&1 || lake exe cache get
  # The models, statements and executable checks must build.
  lake build Generated Bdd Vocab Spec.Checks > ../out/build.log 2>&1 || { cat ../out/build.log; exit 1; }
  # The hand-written proofs (one module per scenario) may be broken, e.g. because the
  # Rust changed under them. Lake builds every module it can; a module that fails
  # costs its own scenario its proof and nothing else. A broken helper lemma module
  # (Lemmas/*.lean) costs every scenario proof that depends on it.
  rc=0; lake build > ../out/proofs.log 2>&1 || rc=$?
  cd .. && python3 -m slicegen proofs "$rc"
)

# Suite adequacy note, step 1 (informational): started here, in the background, because it needs only the
# executable checks built above. Its exit status is never looked at; the report says so if it produced nothing.
ADEQ_PID=""
if [[ $ADEQUACY == 1 ]]; then
  ( cd lean && lake env lean Run/Adequacy.lean > ../out/adequacy.log 2>&1 ) &
  ADEQ_PID=$!
fi

step "5/8 evaluate rows and search for counterexamples on the Lean model"
( cd lean && lake env lean Run/Search.lean > ../out/search.log 2>&1 ) || { cat out/search.log; exit 1; }
python3 -m slicegen derive

step "6/8 audit: derived theorems (sat / unsat / refuted), axioms, glossary checks"
# Exit status is ignored on purpose: the trivial-Then attempts are expected to fail.
# The report reads the AUDIT line and treats any theorem with sorryAx, or of the wrong type, as absent.
( cd lean && lake env lean Run/Audit.lean > ../out/audit.log 2>&1 ) || true
grep -q '^AUDIT' out/audit.log || { echo "audit produced no result:" >&2; cat out/audit.log; exit 1; }
echo "audit ok ($(grep -c ': error:' out/audit.log || true) expected-to-fail attempts logged in out/audit.log)"

# Suite adequacy note, step 2 (informational): kernel attempts for what the search found, in the background.
ADEQ2_PID=""
if [[ -n $ADEQ_PID ]]; then
  wait "$ADEQ_PID" || true
  python3 -m slicegen adequacy || true
  if [[ -s lean/Run/AdequacyAudit.lean ]]; then
    ( cd lean && lake env lean Run/AdequacyAudit.lean > ../out/adequacy-audit.log 2>&1 ) &
    ADEQ2_PID=$!
  fi
fi

if [[ $RUST_TESTS == 1 ]]; then
  step "7/8 cucumber-rs: the same feature files against the compiled Rust"
  python3 -m slicegen steps > out/steps.log || { cat out/steps.log; echo "step regexes differ from the glossary" >&2; exit 1; }
  echo "step regexes identical to the glossary's: $(grep -c '^ok' out/steps.log) of $(wc -l < out/steps.log | tr -d ' ')"
  ( cd bdd && rustc --version > ../out/rustc.txt 2>/dev/null ) || true      # the compiler behind "tested on Rust"
  ( cd bdd && cargo test --quiet --test bdd > ../out/cucumber.log 2>&1 ) || true
  [[ -s out/cucumber.json ]] || { cat out/cucumber.log; echo "cucumber-rs produced no JSON" >&2; exit 1; }
  grep -E '^[0-9]+ (rules|scenarios|steps)|^-- counterexample replay' out/cucumber.log || true
  ( cd bdd && cargo test --quiet --test readings 2>&1 | grep -E '^readings:' ) \
    || { echo "the Rust readings of the glossary phrases could not be evaluated" >&2; exit 1; }
else
  step "7/8 cucumber-rs: SKIPPED (--no-rust)"
fi

[[ -z $ADEQ2_PID ]] || wait "$ADEQ2_PID" || true

step "8/8 report"
python3 -m slicegen report ${REPORT_ARGS[@]+"${REPORT_ARGS[@]}"}
