#!/usr/bin/env bash
# Make (or refresh) a scratch copy of a slice tree in which mutants and pipeline runs can happen
# without touching the real tree. Same idea as slice/mutation/workcopy.sh, with two differences:
# the SOURCE is a parameter (so that every worker copy is taken from one frozen snapshot, not
# from slice/ while another agent edits it), and compare/work, compare/results and compare/logs
# are never copied.
#
#   harness/workcopy.sh <source slice tree> <dest dir> <real slice dir, for .tools and the Lake packages>
set -euo pipefail
SRC="$(cd "${1:?source}" && pwd)"
DEST="${2:?dest}"
REAL="$(cd "${3:?real slice dir}" && pwd)"
case "$DEST" in "$REAL"|"$REAL"/out*|/) echo "refusing to use $DEST" >&2; exit 2 ;; esac
mkdir -p "$DEST"
rsync -a --delete \
  --exclude '/.tools' --exclude '/lean/.lake' --exclude '/out' --exclude '/review' --exclude '/probe' \
  --exclude '/build' --exclude '/wallet/target' --exclude '/ledger/target' --exclude '/wallet-bdd/target' \
  --exclude '__pycache__' --exclude '/mutation/results*' --exclude '/mutation/logs' \
  --exclude '/compare/work' --exclude '/compare/results' --exclude '/compare/logs' \
  --exclude '/compare/arms/*/target' --exclude '/compare/arms/diff/orig' --exclude '/compare/mutants' \
  "$SRC"/ "$DEST"/
ln -sfn "$REAL/.tools" "$DEST/.tools"
mkdir -p "$DEST/lean/.lake" "$DEST/build" "$DEST/out"
ln -sfn "$REAL/lean/.lake/packages" "$DEST/lean/.lake/packages"
# warm build outputs, so each run in the copy is incremental (APFS clones where possible)
warm() { # <relative dir>
  local from="$SRC/$1"; [[ -d "$from" ]] || from="$REAL/$1"
  [[ -d "$DEST/$1" || ! -d "$from" ]] || cp -cRp "$from" "$DEST/$1" 2>/dev/null || cp -Rp "$from" "$DEST/$1" || true
}
warm lean/.lake/build
for t in wallet/target ledger/target wallet-bdd/target compare/arms/proptests/target compare/arms/kani/target compare/arms/diff/target; do warm "$t"; done
# the pristine crates, renamed, for the differential oracle (compare/arms/diff)
rm -rf "$DEST/compare/arms/diff/orig"; mkdir -p "$DEST/compare/arms/diff/orig"
for c in wallet ledger; do
  mkdir -p "$DEST/compare/arms/diff/orig/$c/src"
  cp "$SRC/$c/src/lib.rs" "$DEST/compare/arms/diff/orig/$c/src/lib.rs"
  printf '[package]\nname = "%s_orig"\nversion = "0.1.0"\nedition = "2021"\n\n[lib]\npath = "src/lib.rs"\n' "$c" > "$DEST/compare/arms/diff/orig/$c/Cargo.toml"
done
# rsync restores original modification times, so a file put back after a mutant looks OLDER than the
# mutant's build output and cargo would keep the stale binary. Touch every Rust source to force a rebuild.
find "$DEST/wallet" "$DEST/ledger" "$DEST/wallet-bdd" "$DEST/compare/arms" -name '*.rs' -not -path '*/target/*' -exec touch {} + 2>/dev/null || true
echo "$DEST"
