#!/bin/zsh
# M7 detector, end to end, for one built project: run.sh <ns|carleson|pfr>
# Reads the project's built .olean files only; writes under tools/reinvent/build and out/reinvent/<project>.
# Needs out/corpus/<project>/decls.jsonl (source lines, proof sizes, dependencies) from the corpus export node.
# Synthetic controls (positive, negative, coincidence): planted.sh, which uses PFR's environment; run it before `run.sh pfr`.
# Name-clash side check: lean --run NameClash.lean <names.txt>, not part of this script.
set -e
P=$1; H=${0:A:h}; cd $H
./export.sh $P defs 6                               # skeletons of library and project definitions
python3 stage1.py $P                                # stage 1: candidates by rule (shape, thin wrapper)
python3 names.py $P
./export.sh $P thms 3 $H/../../out/reinvent/$P/raw/names.txt   # statement skeletons for the API-copy signal
python3 stage2.py $P --jobs 6                       # stage 2: kernel-checked equivalences, fixed portfolio
python3 stage3.py $P --jobs 4                       # stage 1c counts, stage 3 cost and sampled derivations
python3 report.py $P                                # out/reinvent/$P/REPORT.md
