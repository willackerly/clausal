#!/usr/bin/env bash
# Counting lock for heavy builds, shared by every agent on this machine.
#   tools/sem.sh <slots> -- <command...>
# Waits until one of <slots> slots is free, runs the command, frees the slot. A slot whose holder
# process is gone is reclaimed. Lock directory: $TMPDIR-independent, /tmp/clausal-sem.
set -uo pipefail
N="${1:?usage: sem.sh <slots> -- cmd}"; shift; [[ "${1:-}" == "--" ]] && shift
L=/tmp/clausal-sem; mkdir -p "$L"
while :; do
  for i in $(seq 1 "$N"); do
    s="$L/slot$i"
    if mkdir "$s" 2>/dev/null; then echo $$ > "$s/pid"; trap 'rm -rf "$s"' EXIT; "$@"; exit $?; fi
    p="$(cat "$s/pid" 2>/dev/null || echo)"
    if [[ -n "$p" ]] && ! kill -0 "$p" 2>/dev/null; then rm -rf "$s"; fi
  done
  sleep 10
done
