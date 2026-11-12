#!/usr/bin/env bash
# Make a git worktree for one builder, with the heavy caches of clausal/ shared or cloned so the
# first build is incremental. The builder commits on branch wave/<name>; one integrator merges.
#   tools/wt.sh <name>        -> prints the worktree path (.worktrees/<name>)
# Shared by symlink (read-only use): clausal/.tools, clausal/lean/.lake/packages.
# Cloned (APFS): clausal/lean/.lake/build, clausal/build, cargo target directories.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="${1:?usage: wt.sh <name>}"
DEST="$ROOT/.worktrees/$NAME"
if [[ ! -d "$DEST" ]]; then
  git -C "$ROOT" worktree add -q "$DEST" -b "wave/$NAME" "${2:-HEAD}"
fi
S="$ROOT/clausal"; D="$DEST/clausal"
ln -sfn "$S/.tools" "$D/.tools"
mkdir -p "$D/lean/.lake"
ln -sfn "$S/lean/.lake/packages" "$D/lean/.lake/packages"
for t in lean/.lake/build build wallet/target ledger/target wallet-bdd/target evidence/target evidence/kani/target; do
  [[ -e "$D/$t" || ! -d "$S/$t" ]] || { mkdir -p "$(dirname "$D/$t")"; cp -cRp "$S/$t" "$D/$t" 2>/dev/null || cp -Rp "$S/$t" "$D/$t"; }
done
find "$D/wallet" "$D/ledger" "$D/wallet-bdd" "$D/evidence" -name '*.rs' -not -path '*/target/*' -exec touch {} + 2>/dev/null || true
echo "$DEST"
