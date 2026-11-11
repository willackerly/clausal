#!/bin/zsh
# usage: re.sh FID FAMFILE   -- re-derive member lemmas: corpus STATEMENT verbatim, proof from subst/FID.re.json
# writes lean/FID_re.lean (new proofs, measured in pairs) and lean/FID_re_spec.lean (the corpus proofs replayed for heartbeats)
cd ${0:A:h}
fid=$1; fam=$2
names=($(python3 -c "import json,sys; print(' '.join(json.load(open('subst/$fid.re.json'))))"))
REPLAY_PROOFS=subst/$fid.re.json REPLAY_FAM=$fid python3 replay.py lean/${fid}_re.lean _R $fam - $names
python3 replay.py lean/${fid}_re_spec.lean _S "" - $names
for f in ${fid}_re ${fid}_re_spec; do ./run.sh $f > /dev/null 2>&1; done
grep -c '"same":true' build/${fid}_re.log
grep "error" build/${fid}_re.log | cut -c1-300 | head -30
python3 replay_log.py build/${fid}_re.log > ../../out/families/gen/${fid}_re_hb.jsonl
python3 replay_log.py build/${fid}_re_spec.log > ../../out/families/gen/${fid}_re_spec_hb.jsonl
