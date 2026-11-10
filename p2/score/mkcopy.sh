#!/usr/bin/env bash
# Make a scratch scoring copy of one P2 arm, cold (no Lean build outputs), under p2/score/work/.
#
#   p2/score/mkcopy.sh <arm-dir> <dest-dir>
#
# Everything frozen and every other pipeline file comes from p2/base (whose FROZEN.sha256 is checked
# first); only the arm's lean/Lemmas/ and lean/Spec/Proofs/ are taken from the arm. The arm directory is
# only read. The two shared caches (.tools, lean/.lake/packages) are symlinked exactly as workcopy.sh does;
# nothing writes to them. Cargo target/ dirs are APFS-cloned from base to save compile time (they are
# Rust build caches; the Lean side is rebuilt from nothing).
set -euo pipefail
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
P2="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE="$P2/base"
ARM="$(cd "${1:?arm dir}" && pwd)"
DEST="${2:?dest dir}"
[[ "$DEST" = /* ]] || DEST="$PWD/$DEST"
case "$DEST" in "$P2"/score/work/*) ;; *) echo "refusing: dest must be under $P2/score/work" >&2; exit 2 ;; esac
( cd "$BASE" && shasum -a 256 -c FROZEN.sha256 >/dev/null ) || { echo "base FROZEN.sha256 does not verify" >&2; exit 1; }
rm -rf "$DEST"
mkdir -p "$DEST"
rsync -a \
  --exclude '/.tools' --exclude '/lean/.lake' --exclude '/out' --exclude '/build' \
  --exclude 'target/' --exclude '__pycache__' \
  --exclude '/lean/Spec/Proofs' --exclude '/lean/Lemmas' --exclude '/effort/attempts.tsv' \
  "$BASE"/ "$DEST"/
mkdir -p "$DEST/lean/Spec" "$DEST/build" "$DEST/lean/.lake"
cp -Rp "$ARM/lean/Spec/Proofs" "$DEST/lean/Spec/Proofs"
cp -Rp "$ARM/lean/Lemmas" "$DEST/lean/Lemmas"
: > "$DEST/effort/attempts.tsv"
ln -sfn "$(cd "$BASE/.tools" && pwd -P)" "$DEST/.tools"
ln -sfn "$(cd "$BASE/lean/.lake/packages" && pwd -P)" "$DEST/lean/.lake/packages"
for t in $(grep -v '^#' "$BASE/crates.txt" || true) bdd; do
  [[ -d "$BASE/$t/target" ]] && { cp -cRp "$BASE/$t/target" "$DEST/$t/target" 2>/dev/null || cp -Rp "$BASE/$t/target" "$DEST/$t/target"; }
done
( cd "$DEST" && shasum -a 256 -c FROZEN.sha256 >/dev/null ) || { echo "copy FROZEN.sha256 does not verify" >&2; exit 1; }
echo "$DEST"
