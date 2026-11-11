#!/bin/zsh
# M9 families, generalisation: everything, one Lean process at a time (about 40 minutes).
# Reads the built corpus (corpora/ns) and out/families/ns/clusters.jsonl; writes corpora/families/build and out/families/gen.
cd ${0:A:h}
./run.sh Tool Abs
for p in "F02076 F2076" "F00073 F73" "F00042 F42" "F00019 F19" "F00046 F46" "F00079 F79" "F00015 F15"; do ./batch.sh ${=p}; done
python3 a0gen.py gen && ./run.sh A0 > /dev/null 2>&1; python3 a0gen.py collect
# wall-clock timing is recorded but no longer reported (needs a quiet machine)
./timing.sh F02076 F00042 F00073 F00046 F00079 F00015 > build/timing.txt
# post-review checks: Mathlib-only F00042, circularity of every re-derivation, elaboration cost of the new library
REPLAY_PROOFS=subst/F00042_mathlib.re.json REPLAY_FAM=F00042 python3 replay.py lean/F00042_mathlib.lean _M "" - $(python3 -c "import json; print(' '.join(json.load(open('subst/F00042_mathlib.re.json'))))")
python3 checkgen.py gen
./run.sh F00042_mathlib LibHB_F15 LibHB_F19 LibHB_F42 LibHB_F46 LibHB_F73 LibHB_F79 LibHB_F2076 Circ > /dev/null 2>&1
python3 replay_log.py build/F00042_mathlib.log > ../../out/families/gen/F00042_mathlib_hb.jsonl
python3 checkgen.py collect
python3 measure.py && python3 report.py
