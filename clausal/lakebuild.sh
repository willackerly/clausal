#!/usr/bin/env bash
# `lake build <targets>` inside lean/, with every attempt logged, so that proof effort is measured
# and not remembered:  effort/attempts.tsv  gets one line per call:
#   UTC time <TAB> targets <TAB> ok|FAILED <TAB> seconds <TAB> number of error lines <TAB> note
#
#   ./lakebuild.sh Ledger.Lemmas.Batch
#   NOTE="second try at the invariant" ./lakebuild.sh Wallet.Proofs.ledger.batch_conserves
#
# A warm `lake build` of one module takes a few seconds; this is not a cold `lake env lean` per check.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
mkdir -p "$HERE/effort"
log="$(mktemp)"
t0=$(date +%s)
( cd "$HERE/lean" && lake build "$@" ) > "$log" 2>&1
rc=$?
t1=$(date +%s)
errs=$(grep -c '^error:' "$log" || true)
printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" "$([[ $rc == 0 ]] && echo ok || echo FAILED)" \
  "$((t1 - t0))" "$errs" "${NOTE:-}" >> "$HERE/effort/attempts.tsv"
grep -E '^(error|warning):|^✖|^- |sorry' "$log" | head -${LINES_SHOWN:-60}
[[ $rc == 0 ]] && echo "ok ($((t1 - t0)) s)" || { echo "FAILED ($((t1 - t0)) s); full log: $log"; }
exit $rc
