#!/usr/bin/env bash
# Rerun the K3 census from the pinned inputs.   ./rerun.sh [setup|census|probes|side|rewrites|tables|all]
#
#   setup     fetch the ten pinned .crate files (sha256-checked), unpack them into crates/, build tools/fninv,
#             clone the Aeneas Lean library and Mathlib packages from ../slice (APFS clone, needs `../slice/translate.sh --check` run once),
#             fetch the newer Aeneas and the hax binary
#   census    scripts/census.py all        Charon -> Aeneas -> lake build, per crate  (on an idle machine about 10 minutes for nine
#             crates and 10 for cedar-policy-core, which uses data/overrides.json and data/crash_cache/; without the cache,
#             add the bisection: 129 Aeneas runs)
#   probes    the three probe crates behind PROFILE.md, through the same driver
#   side      scripts/compare_new.py, scripts/run_hax.sh and the -filter-trait-methods run   (newer Aeneas on the same LLBC; hax 0.5.0)
#   rewrites  rewrites/run.py             the five rewrites: patch, cargo test, re-translate
#   tables    scripts/std_models.py, scripts/tables.py   -> data/summary.json, CENSUS.md, PROFILE.md, IMPROVEMENTS.md
#
# Writes only under census/, plus: ~/.cache/charon (Charon sysroot), ~/.cache/hax (hax's own Charon/Aeneas, 0.6 GB), ~/.cargo registry.
# Never runs `lake update`: lean-pinned/lake-manifest.json is the slice's manifest and the packages are cloned from the slice.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
SLICE="$HERE/../slice"
PIN="aeneas-nightly-2026.11.09-5a392f4"
NEW_TAG="nightly-2026.11.10-0d21a9e"
NEW_SHA="e1e1fe737a81e954f98a4b259e29f8f4e73365791126483874e0c76c61b1522a"
HAX_SHA="e6bbfd54c32de83638ac3570cc7eeb5cbb64ab07bbff0b27e634e6c010a67101"
UA="census-script (generic client)"
step() { printf '\n== %s\n' "$*"; }

setup() {
  mkdir -p "$HERE/.tools/dl" "$HERE/crates" "$HERE/data/results"
  step "crates"
  python3 - "$HERE" <<'PY'
import json, sys, os, subprocess, hashlib
H = sys.argv[1]
for p in json.load(open(H + '/data/selection/pins.json')):
    n, v = p['name'], p['version']
    f = f'{H}/.tools/dl/{n}-{v}.crate'
    if not os.path.exists(f):
        subprocess.check_call(['curl', '-fsSL', '-A', 'census-script (generic client)', '-o', f, f'https://static.crates.io/crates/{n}/{n}-{v}.crate'])
    assert hashlib.sha256(open(f, 'rb').read()).hexdigest() == p['sha256'], 'checksum mismatch for ' + n
    if not os.path.exists(f'{H}/crates/{n}-{v}'):
        subprocess.check_call(['tar', 'xzf', f, '-C', H + '/crates'])
    print('ok', n, v)
PY
  step "fninv"
  ( cd "$HERE/tools/fninv" && cargo build --release --locked )
  step "pinned tools (from ../slice/.tools)"
  [[ -x "$SLICE/.tools/$PIN/aeneas" ]] || { echo "run ../slice/translate.sh --setup first" >&2; exit 1; }
  mkdir -p "$HERE/.tools/$PIN"
  for f in aeneas charon charon-driver libs rust-toolchain; do ln -sfn "$SLICE/.tools/$PIN/$f" "$HERE/.tools/$PIN/$f"; done
  [[ -d "$HERE/.tools/$PIN/backends" ]] || cp -cR "$SLICE/.tools/$PIN/backends" "$HERE/.tools/$PIN/backends"
  mkdir -p "$HERE/lean-pinned/.lake"
  [[ -d "$HERE/lean-pinned/.lake/packages" ]] || cp -cR "$SLICE/lean/.lake/packages" "$HERE/lean-pinned/.lake/packages"
  step "newer Aeneas $NEW_TAG"
  if [[ ! -x "$HERE/.tools/aeneas-$NEW_TAG/aeneas" ]]; then
    curl -fsSL -o "$HERE/.tools/dl/aeneas-$NEW_TAG-macos-aarch64.tar.gz" "https://github.com/AeneasVerif/aeneas/releases/download/$NEW_TAG/aeneas-macos-aarch64.tar.gz"
    echo "$NEW_SHA  $HERE/.tools/dl/aeneas-$NEW_TAG-macos-aarch64.tar.gz" | shasum -a 256 -c -
    mkdir -p "$HERE/.tools/aeneas-$NEW_TAG" && tar xzf "$HERE/.tools/dl/aeneas-$NEW_TAG-macos-aarch64.tar.gz" -C "$HERE/.tools/aeneas-$NEW_TAG"
  fi
  step "hax 0.5.0"
  if [[ ! -x "$HERE/.tools/hax/cargo-hax" ]]; then
    curl -fsSL -o "$HERE/.tools/dl/cargo-hax-v0.5.0-aarch64-apple-darwin.tar.zst" "https://github.com/cryspen/hax/releases/download/cargo-hax-v0.5.0/cargo-hax-aarch64-apple-darwin.tar.zst"
    echo "$HAX_SHA  $HERE/.tools/dl/cargo-hax-v0.5.0-aarch64-apple-darwin.tar.zst" | shasum -a 256 -c -
    mkdir -p "$HERE/.tools/hax" && tar xf "$HERE/.tools/dl/cargo-hax-v0.5.0-aarch64-apple-darwin.tar.zst" -C "$HERE/.tools/hax"
  fi
}
census()   { step "census";   python3 "$HERE/scripts/select_corpus.py" | tail -1; python3 "$HERE/scripts/census.py" all; }
side()     { step "newer Aeneas"; python3 "$HERE/scripts/compare_new.py"; step "hax"; "$HERE/scripts/run_hax.sh"; }
probes()   { step "probes"
             for p in profile-probes-0.1.0 mixed-group-probe-0.1.0 mixed-group-fixed-probe-0.1.0; do
               CENSUS_CRATES="$HERE/probes" CENSUS_TAG=_probe python3 "$HERE/scripts/census.py" run "$p"
             done; }
rewrites() { step "rewrites"; python3 "$HERE/rewrites/run.py"; }
tables()   { step "tables";   python3 "$HERE/scripts/std_models.py" >/dev/null; python3 "$HERE/scripts/tables.py"; }

flag()     { step "side run: aeneas -filter-trait-methods (nine crates; cedar left out)"
             python3 - "$HERE" <<'PY' | while read -r c; do CENSUS_TAG=_ftm CENSUS_AENEAS_FLAGS=-filter-trait-methods python3 "$HERE/scripts/census.py" run "$c"; done
import json, sys
for p in json.load(open(sys.argv[1] + '/data/selection/pins.json')):
    if p['name'] != 'cedar-policy-core':
        print('%s-%s' % (p['name'], p['version']))
PY
           }
case "${1:-all}" in
  setup) setup ;; census) census ;; probes) probes ;; side) side; flag ;; rewrites) rewrites ;; tables) tables ;;
  all) setup; census; probes; side; flag; rewrites; tables ;;
  *) echo "usage: $0 [setup|census|probes|side|rewrites|tables|all]" >&2; exit 2 ;;
esac
