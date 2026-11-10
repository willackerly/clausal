#!/usr/bin/env bash
# One census pass for one Aeneas binary:  scripts/run_variant.sh <variant> [shipped|cw] [crates...]
#   shipped (default): all ten crates, tools as invoked by the census's "as is" round
#   cw: cedar-policy-core with the census's Charon-side workarounds and no Aeneas-side removals
set -uo pipefail
FORK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; CENSUS="$FORK/.."
. "$FORK/env.sh"
V="$1"; MODE="${2:-shipped}"; shift; shift || true
# private Lake project per variant (packages are APFS clones of the census's; the Aeneas Lean library is fork/backends-pinned)
if [[ ! -d "$FORK/backends-pinned" ]]; then cp -cRp "$CENSUS/.tools/aeneas-nightly-2026.11.09-5a392f4/backends" "$FORK/backends-pinned"; fi
L="$FORK/lean/$V"
if [[ ! -d "$L" ]]; then
  mkdir -p "$L/.lake" "$L/Generated"
  cp -cRp "$CENSUS/lean-pinned/.lake/packages" "$L/.lake/packages"
  cp "$CENSUS/lean-pinned/lean-toolchain" "$L/"
  sed 's|"dir": "\.\./\.tools/[^"]*"|"dir": "../../backends-pinned/lean"|' "$CENSUS/lean-pinned/lake-manifest.json" > "$L/lake-manifest.json"
  sed 's|path = ".*"|path = "../../backends-pinned/lean"|' "$CENSUS/lean-pinned/lakefile.toml" > "$L/lakefile.toml"
fi
if [[ $# -gt 0 ]]; then CRATES="$*"; elif [[ "$MODE" == cw ]]; then CRATES="cedar-policy-core-4.14.1"; else
  CRATES=$(python3 -c "import json;print(' '.join('%s-%s'%(p['name'],p['version']) for p in json.load(open('$CENSUS/data/selection/pins.json'))))"); fi
mkdir -p "$FORK/logs/$V-$MODE"
echo $CRATES | tr ' ' '\n' | xargs -P 5 -I{} sh -c "python3 '$FORK/scripts/fork_census.py' $V $MODE tools {} > '$FORK/logs/$V-$MODE/{}.tools.log' 2>&1"
for c in $CRATES; do python3 "$FORK/scripts/fork_census.py" $V $MODE build $c 2>&1 | tee "$FORK/logs/$V-$MODE/$c.build.log" | tail -1; done
