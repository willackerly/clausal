#!/bin/zsh
# M7 synthetic controls: planted.sh   (run before `run.sh pfr`; uses PFR's built environment, read only)
# Compiles planted/ReinventPlanted.lean into tools/reinvent/build/pfr and runs the three stages on it.
# Needs out/reinvent/pfr/raw/defs.jsonl (from `./export.sh pfr defs 6`, the first step of `run.sh pfr`).
# Output: out/reinvent/planted/.  Expected outcomes: planted/expected.json.
set -e
H=${0:A:h}; cd $H
[[ -f $H/../../out/reinvent/pfr/raw/defs.jsonl ]] || ./export.sh pfr defs 6
PROJECT=pfr; source $H/env.sh
(cd $H && LEAN_PATH=$LP lean +$TC -o $B/ReinventPlanted.olean planted/ReinventPlanted.lean)
./export.sh pfr defsproj 1 "" ReinventPlanted ReinventPlanted
mv $O/raw/planted.jsonl $O/raw/planted_defs.jsonl
python3 stage1.py pfr $O/raw/planted_defs.jsonl
python3 names.py pfr
./export.sh pfr thms 2 $O/raw/names.txt ReinventPlanted ReinventPlanted
mv $O/raw/planted.jsonl $O/raw/planted_thms.jsonl
python3 stage2.py pfr --planted
python3 stage3.py pfr --planted
python3 report.py planted
