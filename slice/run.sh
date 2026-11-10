#!/usr/bin/env bash
# One command: regenerate everything and print the per-scenario and per-Rule report.
#
#   Rust (wallet/, ledger/) --Charon+Aeneas--> Lean models (lean/Generated/)
#   features/*.feature + vocabulary.yaml --slicegen--> one compiled READING per scenario and per `Rule:` line
#                     (lean/Wallet/Readings.lean: frames of lean/Frames applied to the operation)
#   features/*.feature + glossary.yaml --slicegen--> flat Lean statements + executable checks (the old
#                     whole-phrase binding: what the proofs, the search and the refutations are about)
#   lake build        kernel-checks the models, the statements, the hand-written loop lemmas
#                     (lean/Ledger/Lemmas/) and the hand-written proofs
#                     (one Lean module per scenario, so one broken proof costs one scenario)
#   Run/Search.lean   evaluates Examples rows on the model; boundary-grid search for a
#                     satisfying input and for a counterexample; evaluates every glossary
#                     definition on a grid of arguments
#   Run/ReadingSearch.lean   every reading compiled from the composable vocabulary (scenarios and Rule lines), on a
#                     grid of generated inputs, evaluated two ways: the definition of each frame against its
#                     independent executable reading; also the counterexample search for Rule statements
#   Run/Links.lean    kernel-checks, for every scenario, that the compiled reading is EQUIVALENT to the flat statement
#                     the proofs are about, and for every Rule that its statement follows from its scenarios
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
#   ./run.sh --no-unit    skip the crate's own unit tests (used by mutation/run_mutants.py, which
#                         wants to know what the SCENARIOS catch on their own)
#   ./run.sh --no-adequacy  skip the suite adequacy note (about 20 s less; every verdict is the same)
#   ./run.sh --no-heldout   skip the NEW sentences of heldout/*.feature (informational: compiled from the vocabulary
#                         alone and searched on generated inputs; they have no flat statement, proof or Rust step)
#
# NOTE: this deletes and recreates out/. Keep nothing there that you want to keep.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
cd "$HERE"

RUST_TESTS=1; UNIT_TESTS=1; ADEQUACY=1; HELDOUT=1; REPORT_ARGS=()
for arg in "$@"; do
  case "$arg" in
    --no-rust) RUST_TESTS=0 ;;
    --no-unit) UNIT_TESTS=0 ;;
    --no-adequacy) ADEQUACY=0 ;;
    --no-heldout) HELDOUT=0 ;;
    --strict)  REPORT_ARGS+=(--strict) ;;
    *) echo "usage: $0 [--strict] [--no-rust] [--no-unit] [--no-adequacy] [--no-heldout]" >&2; exit 2 ;;
  esac
done

step() { printf '\n== %s\n' "$*"; }

rm -rf out
mkdir -p out
rm -f lean/Run/AdequacyAudit.lean      # written again only if this run's adequacy search produced results

if [[ $UNIT_TESTS == 1 ]]; then
  step "1/8 unit tests of the Rust crates (cargo test)"
  for crate in wallet ledger; do
    ( cd "$crate" && cargo test --quiet 2>&1 | grep -E '^(test result: .* [1-9][0-9]* passed|error|warning: unused)' | sed "s/^/$crate: /" || true )
    ( cd "$crate" && cargo test --quiet >/dev/null 2>&1 ) || { echo "$crate unit tests FAILED" >&2; exit 1; }
  done
else
  step "1/8 unit tests of the Rust crates: SKIPPED (--no-unit)"
fi

step "2/8 translate Rust -> Lean (Charon + Aeneas)"
./translate.sh > out/translate.log 2>&1 || { cat out/translate.log; exit 1; }
grep -E '^(aeneas|charon|rustc) ' out/translate.log
echo "wrote lean/Generated/Wallet.lean, lean/Generated/Ledger.lean, lean/translation.json, lean/provenance.json"

step "3/8 slicegen gen: features + glossary -> Lean statements, checks, search script"
python3 -m slicegen gen

step "4/8 lake build: model, statements, hand-written proofs (kernel)"
(
  cd lean
  [[ -d .lake/packages/mathlib ]] || lake update
  ls .lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean >/dev/null 2>&1 || lake exe cache get
  # The models, statements and executable checks must build.
  # So must the frame library and the compiled readings (lean/Wallet/Readings.lean): a reading that does not
  # type-check is a fault of the vocabulary or of the generator, never a verdict.
  lake build Generated Frames Bdd Ledger.Vocab Ledger.Pieces Wallet.Pieces Wallet.Bridge Wallet.Checks Wallet.Readings > ../out/build.log 2>&1 || { cat ../out/build.log; exit 1; }
  # The hand-written proofs (one module per scenario) may be broken, e.g. because the
  # Rust changed under them. Lake builds every module it can; a module that fails
  # costs its own scenario its proof and nothing else. A broken loop lemma
  # (Ledger/Lemmas/*.lean) costs every scenario proof that depends on it.
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

step "5/8 evaluate rows and search for counterexamples on the Lean model; every compiled reading on generated inputs, two ways"
# The reading search (definition of each frame against its executable reading, and the counterexample search for
# Rule statements) runs beside the row / counterexample search of the flat statements.
( cd lean && lake env lean Run/ReadingSearch.lean > ../out/rsearch.log 2>&1 ) &
RS_PID=$!
# hand-written instances of the frames no sentence reaches (count, monotone, agrees with, independent of)
( cd lean && lake env lean Run/FrameTests.lean > ../out/frametests.log 2>&1 ) &
FT_PID=$!
( cd lean && lake env lean Run/Search.lean > ../out/search.log 2>&1 ) || { cat out/search.log; exit 1; }
wait "$RS_PID" || true
wait "$FT_PID" || true
grep -q '^RSEARCH' out/rsearch.log || { echo "the reading search produced no result:" >&2; head -40 out/rsearch.log; exit 1; }
python3 -m slicegen derive

step "6/8 audit: derived theorems (sat / unsat / refuted), axioms, glossary checks"
# Exit status is ignored on purpose: the trivial-Then attempts are expected to fail.
# The report reads the AUDIT line and treats any theorem with sorryAx, or of the wrong type, as absent.
( cd lean && lake env lean Run/Audit.lean > ../out/audit.log 2>&1 ) || true
grep -q '^AUDIT' out/audit.log || { echo "audit produced no result:" >&2; cat out/audit.log; exit 1; }
echo "audit ok ($(grep -c ': error:' out/audit.log || true) expected-to-fail attempts logged in out/audit.log)"
# The glue: each compiled reading against its flat statement (NEW <-> OLD), each Rule against its scenarios.
# Exit status ignored: a script that fails costs its own theorem (it then counts as absent), nothing else.
( cd lean && lake env lean Run/Links.lean > ../out/links.log 2>&1 ) || true
grep -q '^LINKS' out/links.log || { echo "the link audit produced no result:" >&2; head -40 out/links.log; exit 1; }
echo "links ok ($(grep -c ': error:' out/links.log || true) glue scripts failed; see out/links.log)"

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
  ( cd wallet-bdd && rustc --version > ../out/rustc.txt 2>/dev/null ) || true      # the compiler behind "tested on Rust"
  ( cd wallet-bdd && cargo test --quiet --test bdd > ../out/cucumber.log 2>&1 ) || true
  [[ -s out/cucumber.json ]] || { cat out/cucumber.log; echo "cucumber-rs produced no JSON" >&2; exit 1; }
  grep -E '^[0-9]+ (rules|scenarios|steps)|^-- counterexample replay' out/cucumber.log || true
  ( cd wallet-bdd && cargo test --quiet --test readings 2>&1 | grep -E '^readings:' ) \
    || { echo "the Rust readings of the glossary phrases could not be evaluated" >&2; exit 1; }
else
  step "7/8 cucumber-rs: SKIPPED (--no-rust)"
fi

[[ -z $ADEQ2_PID ]] || wait "$ADEQ2_PID" || true

# NEW sentences (informational): rules that are in no fixture, compiled from the existing vocabulary pieces alone
# and searched on generated inputs through the frames' two readings. Never changes the exit status.
if [[ $HELDOUT == 1 ]] && compgen -G "heldout/*.feature" > /dev/null; then
  python3 -m slicegen compile heldout/*.feature > /dev/null || true
  ( cd lean && lake env lean Run/NewReadings.lean > ../out/new_sentences.log 2>&1 ) || true
  echo "new sentences (heldout/, informational): $(python3 -m slicegen compile heldout/*.feature --collect | tail -1)"
fi

step "8/8 report"
python3 -m slicegen report ${REPORT_ARGS[@]+"${REPORT_ARGS[@]}"}
