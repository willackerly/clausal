#!/bin/zsh
# M9 synthetic controls: planted.sh
# Compiles planted/FamiliesPlanted.lean against the ns project's Mathlib (read only; the .olean goes to
# tools/families/build/ns), exports it, clusters it alone, and checks planted/expected.json.
set -e
H=${0:A:h}; cd $H
PROJECT=ns; source $H/env.sh
(cd $H && LEAN_PATH=$LP lean +$TC -o $B/FamiliesPlanted.olean planted/FamiliesPlanted.lean)
./export.sh ns 1 FamiliesPlanted FamiliesPlanted
python3 features.py ns --planted
python3 cluster.py ns --planted
python3 planted_check.py
