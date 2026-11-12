#!/usr/bin/env bash
# Plan node S1a: libsignal-protocol v0.105.4 as an eleventh census row.   ./run.sh [setup|tools|build|axioms|side|report|clean|all]
#
#   setup    clone libsignal at tag v0.105.4 (commit checked), export it to work/crates/, build tools/fninv,
#            clone (APFS, copy-on-write) the patched Aeneas binary and the Lean packages from the main checkout's census/fork
#   tools    Charon + patched Aeneas (variant p5, mode shipped)     build    lake build + per-function join
#   side     the unpatched release Aeneas on the same LLBC (variant pinned)
#   axioms   axiom_check.py: Lean's own answer to "which axioms is this function on" -> axioms.json
#   report   signal_report.py -> RESULT.md, result.json, functions.tsv (with axioms.json, the only tracked outputs)
#   clean    delete work/ (everything fetched or built)
#
# Needs, once, in the main checkout: clausal/translate.sh --setup (pinned Charon/Aeneas) and the fork build of
# census/fork/FORK.md (bin/aeneas-p5, backends-pinned, lean/p5/.lake/packages). Nothing is written outside census/signal/work
# and census/tools/fninv/target, except the Charon sysroot cache in ~/.cache/charon and rustup's toolchains.
# Network: github.com (the tag) and crates.io / github.com (the crate's dependencies, fetched by cargo). Never runs `lake update`.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; CENSUS="$HERE/.."; W="$HERE/work"
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
MAIN="${MAIN_CENSUS:-$(cd "$(git -C "$HERE" rev-parse --git-common-dir)/.." && pwd)/census}"
SEM="$CENSUS/../tools/sem.sh"
TAG=v0.105.4; COMMIT=b2a5c30f3245c1bcad04b27b1e752a38321c793d; CDIR=libsignal-protocol-0.105.4
MODE="${SIGNAL_MODE:-shipped}"
# refuse a path that would break the comments of the generated Lean (guard.py); `clean` is always allowed
[[ "${1:-all}" == clean ]] || python3 "$HERE/guard.py" path "$HERE"
step() { printf '\n== %s\n' "$*"; df -h "$HERE" | tail -1; }

setup() {
  mkdir -p "$W/dl" "$W/crates" "$W/bin" "$W/lean"
  step "source"
  [[ -d "$W/dl/libsignal" ]] || git clone -q --depth 1 --branch "$TAG" https://github.com/signalapp/libsignal.git "$W/dl/libsignal"
  [[ "$(git -C "$W/dl/libsignal" rev-parse HEAD)" == "$COMMIT" ]] || { echo "tag $TAG is not $COMMIT" >&2; exit 1; }
  if [[ ! -d "$W/crates/$CDIR" ]]; then mkdir -p "$W/crates/$CDIR"; git -C "$W/dl/libsignal" archive HEAD | tar -x -C "$W/crates/$CDIR"; fi
  step "fninv"
  ( cd "$CENSUS/tools/fninv" && "$SEM" 3 -- cargo build --release --locked )
  step "patched Aeneas and Lean packages (copy-on-write clones from $MAIN/fork)"
  [[ -x "$MAIN/fork/bin/aeneas-p5" ]] || { echo "no $MAIN/fork/bin/aeneas-p5: build the fork first (census/fork/FORK.md)" >&2; exit 1; }
  [[ -x "$W/bin/aeneas-p5" ]] || cp -c "$MAIN/fork/bin/aeneas-p5" "$W/bin/aeneas-p5"
  [[ -d "$W/backends-pinned" ]] || cp -cRp "$MAIN/fork/backends-pinned" "$W/backends-pinned"
  for V in p5 pinned; do
    L="$W/lean/$V"
    if [[ ! -d "$L" ]]; then
      mkdir -p "$L/.lake" "$L/Generated"
      cp -cRp "$MAIN/fork/lean/p5/.lake/packages" "$L/.lake/packages"
      cp "$CENSUS/lean-pinned/lean-toolchain" "$L/"
      sed 's|"dir": "\.\./\.tools/[^"]*"|"dir": "../../backends-pinned/lean"|' "$CENSUS/lean-pinned/lake-manifest.json" > "$L/lake-manifest.json"
      sed 's|path = ".*"|path = "../../backends-pinned/lean"|' "$CENSUS/lean-pinned/lakefile.toml" > "$L/lakefile.toml"
    fi
  done
  "$W/bin/aeneas-p5" -version
}
tools()  { step "Charon + Aeneas (p5, $MODE)"; "$SEM" 3 -- python3 "$HERE/signal_census.py" p5 "$MODE" tools; }
build()  { step "lake build + join (p5, $MODE)"; "$SEM" 3 -- python3 "$HERE/signal_census.py" p5 "$MODE" build; }
side()   { step "unpatched release Aeneas on the same LLBC"; "$SEM" 3 -- python3 "$HERE/signal_census.py" pinned "$MODE" tools
           "$SEM" 3 -- python3 "$HERE/signal_census.py" pinned "$MODE" build; }
axioms() { step "axiom cross-check by Lean"; python3 "$HERE/axiom_check.py" "p5-$MODE"; }
report() { step "report"; python3 "$HERE/signal_report.py"; }
clean()  { step "clean"; rm -rf "$W"; df -h "$HERE" | tail -1; }
case "${1:-all}" in
  setup) setup ;; tools) tools ;; build) build ;; axioms) axioms ;; side) side ;; report) report ;; clean) clean ;;
  all) setup; tools; build; axioms; side; report ;;
  *) echo "usage: $0 [setup|tools|build|axioms|side|report|clean|all]" >&2; exit 2 ;;
esac
