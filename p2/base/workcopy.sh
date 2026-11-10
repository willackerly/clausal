#!/usr/bin/env bash
# Make (or refresh) your own working copy of this directory, so that several people or agents can
# work on the same frozen task without touching each other's files. Shares the pinned tools and the
# Mathlib package cache by symlink (read-only use); everything else is copied (APFS clones where
# possible). A refresh never deletes your proofs, lemmas or attempt log.
#
#   ./workcopy.sh <dest-dir>
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${1:?usage: workcopy.sh <dest-dir>}"
case "$DEST" in "$HERE"|"$HERE"/*|/) echo "refusing to use $DEST" >&2; exit 2 ;; esac
mkdir -p "$DEST"
# The real targets of the two shared caches (this copy may itself hold symlinks to them).
TOOLS="$(cd "$HERE/.tools" && pwd -P)"
PKGS="$(cd "$HERE/lean/.lake/packages" && pwd -P)"
rsync -a \
  --exclude '/.tools' --exclude '/lean/.lake' --exclude '/out' --exclude '/build' \
  --exclude 'target/' --exclude '__pycache__' \
  --exclude '/lean/Spec/Proofs' --exclude '/lean/Lemmas' --exclude '/effort/attempts.tsv' \
  "$HERE"/ "$DEST"/
# proof stubs, lemmas and the attempt log: copied the first time only, never overwritten
for d in lean/Spec/Proofs lean/Lemmas; do
  [[ -e "$DEST/$d" || ! -e "$HERE/$d" ]] || { mkdir -p "$(dirname "$DEST/$d")"; cp -Rp "$HERE/$d" "$DEST/$d"; }
done
[[ -e "$DEST/effort/attempts.tsv" ]] || : > "$DEST/effort/attempts.tsv"
ln -sfn "$TOOLS" "$DEST/.tools"
mkdir -p "$DEST/lean/.lake" "$DEST/build"
ln -sfn "$PKGS" "$DEST/lean/.lake/packages"
# warm build outputs, so the first build in the copy is incremental
[[ -d "$DEST/lean/.lake/build" ]] || { [[ -d "$HERE/lean/.lake/build" ]] && { cp -cRp "$HERE/lean/.lake/build" "$DEST/lean/.lake/build" 2>/dev/null || cp -Rp "$HERE/lean/.lake/build" "$DEST/lean/.lake/build"; } || true; }
for t in $(grep -v '^#' "$HERE/crates.txt" || true) bdd; do
  [[ -d "$DEST/$t/target" || ! -d "$HERE/$t/target" ]] || cp -cRp "$HERE/$t/target" "$DEST/$t/target" 2>/dev/null || cp -Rp "$HERE/$t/target" "$DEST/$t/target"
done
echo "$DEST"
