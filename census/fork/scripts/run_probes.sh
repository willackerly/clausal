#!/usr/bin/env bash
# The three census probe crates through the same driver:  scripts/run_probes.sh <variant>
FORK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export CENSUS_CRATES="$FORK/../probes"
"$FORK/scripts/run_variant.sh" "$1" shipped mixed-group-probe-0.1.0 mixed-group-fixed-probe-0.1.0 profile-probes-0.1.0
