#!/usr/bin/env bash
# Freeze the slice tree that the comparison is run on: the COMMITTED slice/ at a named commit
# (not the working tree, which another agent may be editing), plus this directory's arms and
# harness as they are now. Everything else (worker copies, results) is derived from it.
#
#   harness/snapshot.sh [<commit>]        default: the commit recorded in PREREG.md, else HEAD
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"      # slice/compare
SLICE="$(cd "$HERE/.." && pwd)"
REPO="$(cd "$SLICE/.." && pwd)"
COMMIT="${1:-$(cat "$HERE/SLICE_COMMIT" 2>/dev/null || git -C "$REPO" rev-parse HEAD)}"
SNAP="$HERE/work/snapshot"
rm -rf "$SNAP"; mkdir -p "$SNAP"
git -C "$REPO" archive "$COMMIT" slice | tar -x -C "$SNAP" --strip-components=1
rm -rf "$SNAP/compare"; mkdir -p "$SNAP/compare"
rsync -a --exclude 'target' --exclude '/diff/orig' "$HERE/arms" "$SNAP/compare/"
rsync -a --exclude '__pycache__' "$HERE/harness" "$SNAP/compare/"
echo "$COMMIT" > "$SNAP/compare/SLICE_COMMIT"
echo "$COMMIT" > "$HERE/SLICE_COMMIT"
echo "snapshot of slice/ at $COMMIT in $SNAP"
