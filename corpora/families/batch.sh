#!/bin/zsh
# usage: batch.sh FID FAMFILE   -- every automatic step for a family, one Lean process at a time
cd ${0:A:h}
fid=$1; fam=$2
./run.sh $fam > /dev/null 2>&1
python3 family.py gen $fid $fam | tail -1
python3 absgen.py gen $fid
steps=(${fid}_api_spec ${fid}_down_spec ${fid}_abs)
if [[ -f subst/$fid.tr.json ]]; then python3 trgen.py gen $fid; steps+=(${fid}_tr); fi
for f in $steps; do ./run.sh $f > /dev/null 2>&1; done
if [[ -f subst/$fid.re.json ]]; then ./re.sh $fid $fam | tail -3; fi
python3 family.py collect $fid 2>&1 | cut -c1-330
python3 absgen.py collect $fid | cut -c1-400
if [[ -f subst/$fid.tr.json ]]; then python3 trgen.py collect $fid | cut -c1-300; fi
