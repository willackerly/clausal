#!/usr/bin/env bash
# One command: regenerate everything and print the per-scenario and per-Rule report.
#
#   Rust (wallet/, ledger/) --Charon+Aeneas--> Lean models (lean/Generated/)
#   features/*.feature + clausebook/ (core, ledger pack, local books) --clausal--> one compiled READING per scenario and per `Rule:` line
#                     (lean/Wallet/Readings.lean: frames of lean/Frames applied to the operation)
#   features/*.feature + glossary.yaml --clausal--> flat Lean statements + executable checks (the old
#                     whole-phrase binding: what the proofs, the search and the refutations of the OLD sentences are about)
#   NEW sentences (no entry in glossary.yaml) --clausal--> a flat proof obligation generated from the pieces
#                     (lean/Wallet/Obligations.lean), a proof stub, and composition trees for the Rust side
#   lake build        kernel-checks the models, the statements, the hand-written loop lemmas
#                     (lean/Ledger/Lemmas/) and the hand-written proofs
#                     (one Lean module per scenario, so one broken proof costs one scenario)
#   clausal book check   the Clausebook itself: core stands alone (no fixture noun; lean/Frames builds alone), and the
#                     registration lint over every accepted surface form reports exactly the recorded violations
#   Run/Search.lean   evaluates Examples rows on the model; boundary-grid search for a
#                     satisfying input and for a counterexample; evaluates every glossary
#                     definition on a grid of arguments
#   Run/FrameTests.lean, Run/FrameToyTests.lean   hand-written instances: the frames no sentence reaches on the wallet
#                     and the ledger, and EVERY frame on a toy operation that gives no answer at one input and
#                     rejects another, each with a claim that is false somewhere (definition against executable
#                     reading; the fixtures alone hardly ever make a frame false and never give a silent call)
#   Run/ReadingSearch.lean   every reading compiled from the composable Clausebook (scenarios and Rule lines), on a
#                     grid of generated inputs, evaluated two ways: the definition of each frame against its
#                     independent executable reading; also the counterexample search for Rule statements
#   Run/Narrowing.lean   narrowed claims ("successful" / "rejected"): kernel-checks what the Clausebook says narrowing settles,
#                     that every control sentence refused as SAYS-NOTHING holds of every operation, that no narrowed claim of a
#                     fixture Rule is shown to; and reports the Frames.Calls value of every claim, against the printed coverage
#   Run/Links.lean    kernel-checks, for every scenario, that the compiled reading is EQUIVALENT to the flat statement
#                     the proofs are about, and for every Rule that its statement follows from its scenarios
#   Run/Audit.lean    kernel-checks theorems derived from the search (satisfiable Givens,
#                     contradictory Givens, refutation at the counterexample, input coverage),
#                     collects axioms, and checks that every proof has the type of its statement
#   cucumber-rs       runs the same feature files against the compiled Rust through ONE generic step that evaluates
#                     the composition tree of each step (build/trees.json) with the per-piece Rust readings
#                     (wallet-bdd/src/pieces.rs); replays each counterexample; evaluates every compiled reading
#                     (scenarios and Rule lines) on the same grid as the Lean side (tests/grid.rs); and evaluates
#                     the older whole-phrase Rust predicates on the same grid as the old glossary's Lean definitions
#   Run/Adequacy.lean, Run/AdequacyAudit.lean
#                     SUITE ADEQUACY NOTE, informational: each scenario stated again with a trivial model
#                     (rejects everything, does nothing, ...) in place of the call; searched on the same
#                     grid, then kernel attempts. Runs beside steps 5-7; a failure here costs the note only.
#   evidence/         GENERATED from the same composition trees (clausal/evgen.py): a property test per reading (proptest,
#                     edge-weighted generators derived from the reading's types and Givens, shrinking) and a Kani harness
#                     per reading and per rung of a fixed size ladder; both assert the same generated predicate, built from
#                     one typed Rust reading per Clausebook piece (evidence/src/typed.rs). What they find false is replayed
#                     on the Lean model (Run/Witness.lean) and becomes a kernel-checked refutation, or a MODEL MISMATCH.
#   clausal report   out/report.md, out/graph.json, and the report printed below (per scenario, then
#                     per Gherkin `Rule:`, the latter generated from out/graph.json)
#
# Exit status: 0 iff every scenario got the verdict it is expected to get
# (PROVED-* by default; @expect-refuted / @expect-unbound / @expect-vacuous otherwise).
#
#   ./run.sh              everything
#   ./run.sh --strict     also fail if a proved scenario rests on a glossary entry nobody has signed off
#   ./run.sh --quick      skip the bounded checks (Kani): the generated property tests still run; for fast iteration
#   ./run.sh --kani-timeout=60 --kani-jobs=6   seconds allowed per Kani harness (default 30) and harnesses run at a time (default 6)
#   ./run.sh --no-rust    skip the cucumber-rs runs (no "tested on Rust" evidence, readings not compared)
#   ./run.sh --no-unit    skip the crate's own unit tests (used by mutation/run_mutants.py, which
#                         wants to know what the SCENARIOS catch on their own)
#   ./run.sh --no-adequacy  skip the suite adequacy note (about 20 s less; every verdict is the same)
#   ./run.sh --no-heldout   skip the NEW sentences of heldout/*.feature (informational: compiled from the Clausebook
#                         alone and searched on generated inputs; they have no flat statement, proof or Rust step)
#
# NOTE: this deletes and recreates out/. Keep nothing there that you want to keep.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
cd "$HERE"

RUST_TESTS=1; UNIT_TESTS=1; ADEQUACY=1; HELDOUT=1; KANI=1; REPORT_ARGS=(); EV_ARGS=()
for arg in "$@"; do
  case "$arg" in
    --no-rust) RUST_TESTS=0 ;;
    --no-unit) UNIT_TESTS=0 ;;
    --no-adequacy) ADEQUACY=0 ;;
    --no-heldout) HELDOUT=0 ;;
    --quick) KANI=0; EV_ARGS+=(--quick) ;;
    --kani-timeout=*) EV_ARGS+=(--kani-timeout "${arg#*=}") ;;
    --kani-jobs=*) EV_ARGS+=(--jobs "${arg#*=}") ;;
    --strict)  REPORT_ARGS+=(--strict) ;;
    *) echo "usage: $0 [--strict] [--quick] [--kani-timeout=N] [--kani-jobs=N] [--no-rust] [--no-unit] [--no-adequacy] [--no-heldout]" >&2; exit 2 ;;
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

step "3/8 clausal gen: features + glossary -> Lean statements, checks, search script"
python3 -m clausal gen
# Plan nodes C1 and Q3: THE BOOK ITSELF. Core stands alone (clausebook/core.yaml loads with no other book and no glossary,
# names no fixture noun, and lean/Frames builds in a directory of its own), and the registration lint over every accepted
# surface form reports exactly the violations recorded as known debt (clausebook/check.expected.json), among them that
# every sentence of features/ and controls/ compiles to the term recorded for it (clausebook/terms.lock.json).
# A difference is a fault of the book or an unrecorded change of wording: the run stops.
python3 -m clausal book check --lean --quiet || { echo "the Clausebook check failed (python3 -m clausal book check)" >&2; exit 1; }

step "4/8 lake build: model, statements, hand-written proofs (kernel)"
(
  cd lean
  [[ -d .lake/packages/mathlib ]] || lake update
  ls .lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean >/dev/null 2>&1 || lake exe cache get
  # The models, statements and executable checks must build.
  # So must the frame library and the compiled readings (lean/Wallet/Readings.lean): a reading that does not
  # type-check is a fault of the Clausebook or of the generator, never a verdict.
  # So must the flat proof obligations of the NEW sentences (lean/Wallet/Obligations.lean): generated text, type-checked here.
  lake build Generated Frames Bdd Ledger.Vocab Ledger.Pieces Wallet.Pieces Wallet.Bridge Wallet.Checks Wallet.Readings Wallet.Obligations > ../out/build.log 2>&1 || { cat ../out/build.log; exit 1; }
  # The hand-written proofs (one module per scenario) may be broken, e.g. because the
  # Rust changed under them. Lake builds every module it can; a module that fails
  # costs its own scenario its proof and nothing else. A broken loop lemma
  # (Ledger/Lemmas/*.lean) costs every scenario proof that depends on it.
  rc=0; lake build > ../out/proofs.log 2>&1 || rc=$?
  cd .. && python3 -m clausal proofs "$rc"
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
# ... and EVERY frame on a toy operation that also gives no answer and rejects, with claims that are false at some
# points (Run/FrameToyTests.lean, core Lean only): the comparison needs false claims and silent calls to catch anything
( cd lean && { lake env lean Run/FrameTests.lean; lake env lean Run/FrameToyTests.lean; } > ../out/frametests.log 2>&1 ) &
FT_PID=$!
( cd lean && lake env lean Run/Search.lean > ../out/search.log 2>&1 ) || { cat out/search.log; exit 1; }
wait "$RS_PID" || true
wait "$FT_PID" || true
grep -q '^RSEARCH' out/rsearch.log || { echo "the reading search produced no result:" >&2; head -40 out/rsearch.log; exit 1; }
# Plan nodes Q1 and Q2: NARROWED CLAIMS. Lean is asked (a) to prove what the Clausebook declares narrowing settles for each
# operation, and to fail on what it does not declare; (b) to prove, for every control sentence the compiler refuses as saying
# nothing, that it holds for every `run`, through the theorem the refusal names; (c) to fail to prove the same of every narrowed
# claim that was NOT refused (every fixture Rule); (d) which calls each claim of each compiled reading is about (`Frames.Calls`),
# which is compared with the coverage the reading prints. A wrong answer is a fault of the book or the generator: the run stops.
( cd lean && lake env lean Run/Narrowing.lean > ../out/narrowing.log 2>&1 ) || true     # failing scripts are expected in it
python3 -m clausal narrowing || { echo "the narrowing check failed (out/narrowing.json, out/narrowing.log)" >&2; exit 1; }
# Plan node E1: LAYERED EVIDENCE. From the same composition trees (build/trees.json) `clausal gen` wrote a property test
# and a bounded-checking harness per compiled reading (evidence/, generated; no test code is written per rule). They run on
# the COMPILED Rust here, before `derive`, so that an input they find false can be fed back: it is evaluated on the Lean
# model through the reading (Run/Witness.lean); if it fails there too it becomes the reading's counterexample and gets the
# usual kernel-checked refutation; if the model disagrees with the Rust it is reported as a MODEL MISMATCH.
if [[ $RUST_TESTS == 1 ]]; then
  step "5b/8 generated evidence on the compiled Rust: property tests (proptest)$([[ $KANI == 1 ]] && echo ' and bounded checks (Kani, size ladder)' || echo '; bounded checks SKIPPED (--quick)')"
  python3 -m clausal evidence ${EV_ARGS[@]+"${EV_ARGS[@]}"} || echo "the generated evidence step failed (see out/evidence.json); the report will say what is missing"
  if [[ -s out/evidence.json ]]; then
    python3 -m clausal witness
    ( cd lean && lake env lean Run/Witness.lean > ../out/witness.log 2>&1 ) || true
    python3 -m clausal witness --collect
  fi
fi
python3 -m clausal derive

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
  python3 -m clausal adequacy || true
  if [[ -s lean/Run/AdequacyAudit.lean ]]; then
    ( cd lean && lake env lean Run/AdequacyAudit.lean > ../out/adequacy-audit.log 2>&1 ) &
    ADEQ2_PID=$!
  fi
fi

if [[ $RUST_TESTS == 1 ]]; then
  step "7/8 cucumber-rs: the same feature files against the compiled Rust (one generic step; composition trees from build/trees.json)"
  # No hand-written step: every step form of the feature files is a composition tree of Clausebook pieces
  # (build/trees.json, written by `clausal gen`), evaluated by the per-piece Rust readings of wallet-bdd/src/pieces.rs.
  python3 -m clausal steps > out/steps.log || { cat out/steps.log; echo "the step forms could not be listed" >&2; exit 1; }
  tail -1 out/steps.log
  ( cd wallet-bdd && rustc --version > ../out/rustc.txt 2>/dev/null ) || true      # the compiler behind "tested on Rust"
  ( cd wallet-bdd && cargo test --quiet --test bdd > ../out/cucumber.log 2>&1 ) || true
  [[ -s out/cucumber.json ]] || { cat out/cucumber.log; echo "cucumber-rs produced no JSON" >&2; exit 1; }
  grep -E '^[0-9]+ (rules|scenarios|steps)|^-- counterexample replay|^generic steps' out/cucumber.log || true
  # every compiled reading (scenarios and Rule lines) at every point of its grid, on the compiled Rust, through the
  # per-piece Rust readings: the same bit string the Lean side printed (RBITS); the report compares the two
  ( cd wallet-bdd && cargo test --quiet --test grid 2>&1 | grep -E '^grid:' ) \
    || { echo "the compiled readings could not be evaluated on the compiled Rust" >&2; exit 1; }
  ( cd wallet-bdd && cargo test --quiet --test readings 2>&1 | grep -E '^readings:' ) \
    || { echo "the Rust readings of the glossary phrases could not be evaluated" >&2; exit 1; }
else
  step "7/8 cucumber-rs: SKIPPED (--no-rust)"
fi

[[ -z $ADEQ2_PID ]] || wait "$ADEQ2_PID" || true

# NEW sentences (informational): rules that are in no fixture, compiled from the existing Clausebook pieces alone
# and searched on generated inputs through the frames' two readings. Never changes the exit status.
if [[ $HELDOUT == 1 ]] && compgen -G "heldout/*.feature" > /dev/null; then
  python3 -m clausal compile heldout/*.feature > /dev/null || true
  ( cd lean && lake env lean Run/NewReadings.lean > ../out/new_sentences.log 2>&1 ) || true
  echo "new sentences (heldout/, informational): $(python3 -m clausal compile heldout/*.feature --collect | tail -1)"
fi

step "8/8 report"
python3 -m clausal report ${REPORT_ARGS[@]+"${REPORT_ARGS[@]}"}
