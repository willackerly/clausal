#!/usr/bin/env bash
# Make (or refresh) a scratch copy of slice/ in which mutants and negative controls can be
# run without touching the real tree. Shares the pinned tools and the Mathlib package cache
# by symlink (read-only use); everything else is copied (APFS clones where possible).
#
#   mutation/workcopy.sh <dest-dir>
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:?usage: workcopy.sh <dest-dir>}"
case "$DEST" in "$HERE"|"$HERE"/out*|/) echo "refusing to use $DEST" >&2; exit 2 ;; esac
mkdir -p "$DEST"
rsync -a --delete \
  --exclude '/.tools' --exclude '/lean/.lake' --exclude '/out' --exclude '/review' --exclude '/probe' --exclude '/compare' \
  --exclude '/build' --exclude '/wallet/target' --exclude '/ledger/target' --exclude '/wallet-bdd/target' --exclude '__pycache__' \
  --exclude '/evidence/target' --exclude '/evidence/kani/target' --exclude '/wallet-shipped' \
  --exclude '/mutation/results*' \
  "$HERE"/ "$DEST"/
ln -sfn "$HERE/.tools" "$DEST/.tools"
mkdir -p "$DEST/lean/.lake" "$DEST/build"
ln -sfn "$HERE/lean/.lake/packages" "$DEST/lean/.lake/packages"
# warm build outputs, so each run in the copy is incremental
[[ -d "$DEST/lean/.lake/build" ]] || { [[ -d "$HERE/lean/.lake/build" ]] && cp -cRp "$HERE/lean/.lake/build" "$DEST/lean/.lake/build" 2>/dev/null || cp -Rp "$HERE/lean/.lake/build" "$DEST/lean/.lake/build" || true; }
for t in wallet/target ledger/target wallet-bdd/target evidence/target evidence/kani/target; do
  [[ -d "$DEST/$t" || ! -d "$HERE/$t" ]] || cp -cRp "$HERE/$t" "$DEST/$t" 2>/dev/null || cp -Rp "$HERE/$t" "$DEST/$t"
done
# rsync restores original modification times, so a file put back after a mutant looks OLDER than the
# mutant's build output and cargo would keep the stale binary. Touch every Rust source to force a rebuild.
find "$DEST/wallet" "$DEST/ledger" "$DEST/wallet-bdd" "$DEST/evidence" -name '*.rs' -not -path '*/target/*' -exec touch {} +
echo "$DEST"
