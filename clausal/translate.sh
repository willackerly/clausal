#!/usr/bin/env bash
# Regenerate the Lean models (lean/Generated/) from the Rust crates (wallet/, ledger/).
#
#   ./translate.sh            Rust -> LLBC (Charon) -> Lean (Aeneas)
#   ./translate.sh --check    ...then `lake build` the Lean project (model + proofs)
#   ./translate.sh --setup    only fetch/verify the pinned tools, then exit
#
# Tools are fetched on first use into .tools/ (see TOOLCHAIN.md). Nothing outside
# clausal/ is written except: the pinned Rust nightly under ~/.rustup, the Lean
# toolchain under ~/.elan, and Charon's sysroot cache under ~/.cache/charon.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"

# ---- pins -------------------------------------------------------------------
AENEAS_TAG="nightly-2026.11.09-5a392f4"
AENEAS_ASSET="aeneas-macos-aarch64.tar.gz"
AENEAS_SHA256="b1d5ffeb85646b3a1944977068354a9f0ef257307dc3d391d874f19528b118f9"
RUST_NIGHTLY="nightly-2026-09-17"      # must equal .tools/<tag>/rust-toolchain
CRATES="wallet ledger"                 # cargo crate dirs under clausal/ (= crate names), translated in this order
# -----------------------------------------------------------------------------

TOOLS="$HERE/.tools/aeneas-$AENEAS_TAG"
DL="$HERE/.tools/dl"
BUILD="$HERE/build"
LEAN="$HERE/lean"

MODE="translate"
case "${1:-}" in
  "") ;;
  --check) MODE="check" ;;
  --setup) MODE="setup" ;;
  *) echo "usage: $0 [--check|--setup]" >&2; exit 2 ;;
esac

step() { printf '\n== %s\n' "$*"; }

# ---- 1. tools ---------------------------------------------------------------
if [[ ! -x "$TOOLS/aeneas" || ! -x "$TOOLS/charon" ]]; then
  [[ "$(uname -s)-$(uname -m)" == "Darwin-arm64" ]] || {
    echo "pins in this script are for macOS arm64; edit AENEAS_ASSET/AENEAS_SHA256" >&2; exit 1; }
  step "fetching Aeneas $AENEAS_TAG"
  mkdir -p "$DL" "$TOOLS"
  curl -fsSL -o "$DL/$AENEAS_ASSET" \
    "https://github.com/AeneasVerif/aeneas/releases/download/$AENEAS_TAG/$AENEAS_ASSET"
  echo "$AENEAS_SHA256  $DL/$AENEAS_ASSET" | shasum -a 256 -c -
  tar xzf "$DL/$AENEAS_ASSET" -C "$TOOLS"
fi

grep -q "channel = \"$RUST_NIGHTLY\"" "$TOOLS/rust-toolchain" || {
  echo "RUST_NIGHTLY ($RUST_NIGHTLY) does not match $TOOLS/rust-toolchain" >&2; exit 1; }

if ! rustup toolchain list | grep -q "^$RUST_NIGHTLY-"; then
  step "installing Rust $RUST_NIGHTLY (rustup, ~1.1 GB under ~/.rustup)"
  rustup toolchain install "$RUST_NIGHTLY" --profile minimal \
    -c rustc-dev -c llvm-tools -c rust-src -c miri
fi

echo "aeneas : $("$TOOLS/aeneas" -version)"
echo "charon : $("$TOOLS/charon" version)"
echo "rustc  : $(rustc "+$RUST_NIGHTLY" --version)"
[[ "$MODE" == "setup" ]] && exit 0

# ---- 2+3. per crate: Rust -> LLBC (Charon) -> Lean (Aeneas) ------------------
# Aeneas writes Generated/<Crate>.lean and a translation.json per run; the per-crate
# JSON files are kept in build/ and merged into lean/translation.json (every function
# and type gets a "crate" field).
mkdir -p "$BUILD"
rm -rf "$LEAN/Generated" "$LEAN/translation.json"
for CRATE in $CRATES; do
  step "charon: $CRATE/ -> build/$CRATE.llbc"
  rm -f "$BUILD/$CRATE.llbc"
  ( cd "$HERE/$CRATE" && "$TOOLS/charon" cargo --preset=aeneas --dest-file "$BUILD/$CRATE.llbc" )
  [[ -s "$BUILD/$CRATE.llbc" ]] || { echo "charon produced no LLBC for $CRATE" >&2; exit 1; }
  step "aeneas: build/$CRATE.llbc -> lean/Generated/"
  "$TOOLS/aeneas" -backend lean -dest "$LEAN" -subdir Generated -emit-json \
    -warnings-as-errors -no-progress-bar "$BUILD/$CRATE.llbc"
  mv "$LEAN/translation.json" "$BUILD/translation.$CRATE.json"
done
ls -1 "$LEAN/Generated"
python3 - "$LEAN/translation.json" $(for c in $CRATES; do echo "$BUILD/translation.$c.json"; done) <<'PY'
import json, sys
out = {"crates": [], "functions": [], "types": [], "globals": [], "trait_decls": [], "trait_impls": []}
for path in sys.argv[2:]:
    d = json.load(open(path))
    out["aeneas_version"], out["charon_version"] = d["aeneas_version"], d["charon_version"]
    out["crates"].append(d["crate"])
    for k in ("functions", "types", "globals", "trait_decls", "trait_impls"):
        out[k] += [dict(x, crate=d["crate"]) for x in d.get(k, [])]
json.dump(out, open(sys.argv[1], "w"), indent=1)
PY

# ---- 4. provenance (inputs/outputs of the tool-trusted edge) ----------------
sha() { shasum -a 256 "$1" | cut -d' ' -f1; }
{
  echo "{"
  echo "  \"aeneas\": \"$("$TOOLS/aeneas" -version | sed 's/^aeneas //')\","
  echo "  \"charon\": \"$("$TOOLS/charon" version)\","
  echo "  \"rustc\": \"$(rustc "+$RUST_NIGHTLY" --version)\","
  echo "  \"inputs\": {"
  first=1
  while IFS= read -r f; do
    [[ $first == 1 ]] || echo ","
    first=0
    printf '    "%s": "%s"' "${f#"$HERE/"}" "$(sha "$f")"
  done < <(for c in $CRATES; do find "$HERE/$c" -path "$HERE/$c/target" -prune -o -type f \( -name '*.rs' -o -name 'Cargo.toml' -o -name 'Cargo.lock' -o -name 'rust-toolchain.toml' \) -print; done | sort)
  echo
  echo "  },"
  echo "  \"outputs\": {"
  first=1
  while IFS= read -r f; do
    [[ $first == 1 ]] || echo ","
    first=0
    printf '    "%s": "%s"' "${f#"$HERE/"}" "$(sha "$f")"
  done < <( { find "$LEAN/Generated" -type f -name '*.lean'; echo "$LEAN/translation.json"; } | sort)
  echo
  echo "  }"
  echo "}"
} > "$LEAN/provenance.json"
echo "wrote lean/provenance.json"

# ---- 5. optional: kernel-check model + proofs --------------------------------
if [[ "$MODE" == "check" ]]; then
  step "lake build (lean/)"
  cd "$LEAN"
  # First run only: fetch dependencies; Mathlib's post-update hook downloads the
  # prebuilt olean cache (never compile Mathlib from source).
  [[ -d .lake/packages/mathlib ]] || lake update
  ls .lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean >/dev/null 2>&1 || lake exe cache get
  lake build
fi
