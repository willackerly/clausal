#!/usr/bin/env bash
# Regenerate the Lean models (lean/Generated/) from the Rust crate of every project declared in projects.yaml.
#
#   ./translate.sh            Rust -> LLBC (Charon) -> Lean (Aeneas)
#   ./translate.sh --check    ...then `lake build` the Lean project (model + proofs)
#   ./translate.sh --setup    only fetch/verify the pinned tools, then exit
#   ./translate.sh [...] --translator=patched|release
#                             which Aeneas binary translates (default: TRANSLATOR below, or $CLAUSAL_TRANSLATOR):
#                             patched = the fork of census/fork (five patches), release = the binary of the tarball
#   ./translate.sh [...] --warnings=error|allow
#                             pass -warnings-as-errors to Aeneas or not (default: AENEAS_WARNINGS below, or
#                             $CLAUSAL_AENEAS_WARNINGS)
#                             Either way a nonzero exit of Aeneas stops the run: "allow" lets warnings pass,
#                             it does not accept the partial file Aeneas writes when an item fails (exit 1).
#
# Which binary ran, its sha256, the patch identifiers and the warnings setting are written to
# lean/provenance.json ("translator"). Charon, the Aeneas Lean library and the Rust pin always come from
# the release tarball; only the `aeneas` executable differs between the two settings.
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
# The crates to translate, in this order: the `crate:` of every project of projects.yaml (plan node X7; cargo crate dirs
# under clausal/ = crate names). $CLAUSAL_CRATES, if set, is used in its place (a list of directories).
CRATES="${CLAUSAL_CRATES:-$(cd "$HERE" && python3 -m clausal projects crates)}"
[[ -n $CRATES ]] || { echo "translate.sh: projects.yaml declares no crate" >&2; exit 1; }

# The translator setting (plan node R1). "patched" is the binary built in census/fork from Aeneas
# AENEAS_FORK_BASE plus the five patch files below (census/fork/patches/, see TOOLCHAIN.md "The patched
# translator"). It is never downloaded and never copied into .tools/: it is looked up (see find_patched) and
# must have exactly this sha256. "release" is .tools/<tag>/aeneas, the binary used before R1.
TRANSLATOR="patched"                   # patched | release
AENEAS_WARNINGS="error"                # error = pass -warnings-as-errors | allow = do not
AENEAS_FORK_BIN="aeneas-p5"
AENEAS_FORK_SHA256="7dca4ee8d2168a98f284ada0a64f8f674dabba7c0b407010ebd29d5a14a458a9"
AENEAS_FORK_BASE="0d21a9ec7bbbb110110cacc14464a47fd71c8705"   # upstream commit the patches sit on (nightly-2026.11.10)
AENEAS_FORK_PATCHES="\
0001-FunsAnalysis-keep-analysing-declaration-groups-after.patch:8f613a71ad32ed0f4b119b6e37a05aa36374914957994fcfa7a7ebd7f870c388
0002-Translate-a-trait-method-signature-that-fails-no-lon.patch:229b5ede1b491b7e2b0aa43300eaf9fc2adfac10ccc14822ea7f86b34bd379d3
0003-Catch-non-CFailure-exceptions-per-function-per-decla.patch:a51e5c59ce71c2e2b1c00459dff518288fdb8fd3d4b909f58fd93f53959bfcb0
0004-Lean-backend-avoid-two-kinds-of-name-capture.patch:20fd4bee37e32b6fb5e3986130e4a1ca208f2a5fff603af7e1bcfb983a677e88
0005-Extraction-reset-the-formatter-after-an-error-in-a-d.patch:2530a59c637cf19ca9b2108706a4d61d413288df7c5d361d0ad0c2ce8b89ab6d"
# -----------------------------------------------------------------------------

TOOLS="$HERE/.tools/aeneas-$AENEAS_TAG"
DL="$HERE/.tools/dl"
BUILD="$HERE/build"
LEAN="$HERE/lean"

MODE="translate"
TRANSLATOR="${CLAUSAL_TRANSLATOR:-$TRANSLATOR}"
AENEAS_WARNINGS="${CLAUSAL_AENEAS_WARNINGS:-$AENEAS_WARNINGS}"
for arg in "$@"; do
  case "$arg" in
    --check) MODE="check" ;;
    --setup) MODE="setup" ;;
    --translator=*) TRANSLATOR="${arg#*=}" ;;
    --warnings=*) AENEAS_WARNINGS="${arg#*=}" ;;
    *) echo "usage: $0 [--check|--setup] [--translator=patched|release] [--warnings=error|allow]" >&2; exit 2 ;;
  esac
done
case "$TRANSLATOR" in patched|release) ;; *) echo "translator must be patched or release, not '$TRANSLATOR'" >&2; exit 2 ;; esac
case "$AENEAS_WARNINGS" in error|allow) ;; *) echo "warnings must be error or allow, not '$AENEAS_WARNINGS'" >&2; exit 2 ;; esac

step() { printf '\n== %s\n' "$*"; }
sha() { shasum -a 256 "$1" | cut -d' ' -f1; }

# The patched binary is git-ignored build output of census/fork. Candidates, in order; the first that exists is
# taken and must then have the pinned sha256 (a wrong file is an error, never skipped):
#   1. $CLAUSAL_AENEAS_PATCHED               an explicit path
#   2. ../census/fork/bin/                    this checkout
#   3. beside the real .tools/               a git worktree or a working copy whose .tools is a symlink to the
#                                             main checkout (tools/wt.sh, mutation/workcopy.sh)
#   4. the main checkout of this worktree    (git common dir)
find_patched() {
  local c real common
  if [[ -n "${CLAUSAL_AENEAS_PATCHED:-}" ]]; then echo "$CLAUSAL_AENEAS_PATCHED"; return; fi
  c="$HERE/../census/fork/bin/$AENEAS_FORK_BIN"
  [[ -e "$c" ]] && { echo "$c"; return; }
  if real="$(cd "$HERE/.tools" 2>/dev/null && pwd -P)"; then
    c="$real/../../census/fork/bin/$AENEAS_FORK_BIN"
    [[ -e "$c" ]] && { echo "$(cd "$(dirname "$c")" && pwd -P)/$AENEAS_FORK_BIN"; return; }
  fi
  if common="$(git -C "$HERE" rev-parse --path-format=absolute --git-common-dir 2>/dev/null)"; then
    c="$(dirname "$common")/census/fork/bin/$AENEAS_FORK_BIN"
    [[ -e "$c" ]] && { echo "$c"; return; }
  fi
  return 1
}

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

# ---- 1b. which aeneas binary translates ---------------------------------------
if [[ "$TRANSLATOR" == "patched" ]]; then
  AENEAS="$(find_patched)" || {
    echo "the patched translator ($AENEAS_FORK_BIN) was not found: build it (TOOLCHAIN.md, \"The patched translator\")," >&2
    echo "or set CLAUSAL_AENEAS_PATCHED=/path/to/it, or choose the unpatched one with --translator=release" >&2; exit 1; }
  [[ -x "$AENEAS" ]] || { echo "not an executable file: $AENEAS" >&2; exit 1; }
  AENEAS_SHA="$(sha "$AENEAS")"
  [[ "$AENEAS_SHA" == "$AENEAS_FORK_SHA256" ]] || {
    echo "patched translator $AENEAS has sha256 $AENEAS_SHA, pinned is $AENEAS_FORK_SHA256" >&2
    echo "(a rebuilt binary needs a new pin in translate.sh, see TOOLCHAIN.md)" >&2; exit 1; }
  # The tracked patch files, where this checkout has them, must be the ones the pin names.
  PATCHDIR="$HERE/../census/fork/patches"
  if [[ -d "$PATCHDIR" ]]; then
    for entry in $AENEAS_FORK_PATCHES; do
      f="$PATCHDIR/${entry%%:*}"
      [[ -f "$f" && "$(sha "$f")" == "${entry##*:}" ]] || {
        echo "patch file $f is missing or differs from the pin in translate.sh" >&2; exit 1; }
    done
  fi
  AENEAS_LABEL="$("$AENEAS" -version | sed 's/^aeneas //') (patched: ${AENEAS_FORK_BASE:0:8} + 5 patches, binary sha256 ${AENEAS_FORK_SHA256:0:12}; Charon and Lean library of $AENEAS_TAG)"
else
  AENEAS="$TOOLS/aeneas"
  AENEAS_SHA="$(sha "$AENEAS")"
  AENEAS_LABEL="$("$AENEAS" -version | sed 's/^aeneas //')"
fi
AENEAS_FLAGS=()
[[ "$AENEAS_WARNINGS" == "error" ]] && AENEAS_FLAGS+=(-warnings-as-errors)

echo "aeneas : $AENEAS_LABEL"
echo "translator : $TRANSLATOR, sha256 $AENEAS_SHA, warnings=$AENEAS_WARNINGS, $AENEAS"
echo "charon : $("$TOOLS/charon" version)"
echo "rustc  : $(rustc "+$RUST_NIGHTLY" --version)"
[[ "$MODE" == "setup" ]] && exit 0

# ---- 2+3. per crate: Rust -> LLBC (Charon) -> Lean (Aeneas) ------------------
# Aeneas writes Generated/<Crate>.lean and a translation.json per run; the per-crate
# JSON files are kept in build/ and merged into lean/translation.json (every function
# and type gets a "crate" field).
mkdir -p "$BUILD"
# provenance.json goes too: it describes the outputs of one complete run, so a run that stops half way must
# not leave the previous run's file beside a half-written Generated/.
rm -rf "$LEAN/Generated" "$LEAN/translation.json" "$LEAN/provenance.json"
for CRATE in $CRATES; do
  step "charon: $CRATE/ -> build/$CRATE.llbc"
  rm -f "$BUILD/$CRATE.llbc"
  ( cd "$HERE/$CRATE" && "$TOOLS/charon" cargo --preset=aeneas --dest-file "$BUILD/$CRATE.llbc" )
  [[ -s "$BUILD/$CRATE.llbc" ]] || { echo "charon produced no LLBC for $CRATE" >&2; exit 1; }
  step "aeneas: build/$CRATE.llbc -> lean/Generated/"
  rc=0
  "$AENEAS" -backend lean -dest "$LEAN" -subdir Generated -emit-json \
    ${AENEAS_FLAGS[@]+"${AENEAS_FLAGS[@]}"} -no-progress-bar "$BUILD/$CRATE.llbc" || rc=$?
  if [[ $rc != 0 ]]; then
    # Observed: 2 = stopped early (at the first warning or error under -warnings-as-errors, or on an uncaught
    # exception in the release binary), nothing written for this crate; 1 = finished with errors and wrote a
    # PARTIAL file (some items replaced by placeholders). Neither is accepted: this script has no setting that takes a partial model, so
    # --warnings=allow alone does not get a crate with untranslatable items through (TOOLCHAIN.md).
    echo "aeneas exited $rc on $CRATE (translator=$TRANSLATOR, warnings=$AENEAS_WARNINGS): stopping." >&2
    echo "lean/Generated is incomplete and lean/provenance.json has been removed; fix the crate and rerun," >&2
    echo "or restore the tracked files with: git checkout -- lean/Generated lean/provenance.json lean/translation.json" >&2
    exit "$rc"
  fi
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
{
  echo "{"
  echo "  \"aeneas\": \"$AENEAS_LABEL\","
  echo "  \"charon\": \"$("$TOOLS/charon" version)\","
  echo "  \"rustc\": \"$(rustc "+$RUST_NIGHTLY" --version)\","
  echo "  \"translator\": {"
  echo "    \"variant\": \"$TRANSLATOR\","
  echo "    \"version\": \"$("$AENEAS" -version | sed 's/^aeneas //')\","
  echo "    \"binary_sha256\": \"$AENEAS_SHA\","
  echo "    \"warnings_as_errors\": $([[ "$AENEAS_WARNINGS" == "error" ]] && echo true || echo false),"
  echo "    \"release\": \"$AENEAS_TAG\","
  if [[ "$TRANSLATOR" == "patched" ]]; then
    echo "    \"binary\": \"census/fork/bin/$AENEAS_FORK_BIN\","
    echo "    \"base_commit\": \"$AENEAS_FORK_BASE\","
    echo "    \"patches\": ["
    first=1
    for entry in $AENEAS_FORK_PATCHES; do
      [[ $first == 1 ]] || echo ","
      first=0
      printf '      {"id": "%s", "sha256": "%s"}' "${entry%%:*}" "${entry##*:}"
    done
    echo
    echo "    ]"
  else
    echo "    \"binary\": \"$AENEAS_ASSET:aeneas\","
    echo "    \"patches\": []"
  fi
  echo "  },"
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
