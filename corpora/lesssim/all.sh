#!/bin/zsh
# Regenerate everything for the constant-threading experiment (about 2 minutes).
# Reads the built corpus at corpora/ns and the exports under out/corpus; writes only corpora/lesssim/build
# and out/corpus/lesssim.
set -e
HERE=${0:A:h}; REPO=$HERE/../..; O=$REPO/out/corpus/lesssim
mkdir -p $O
python3 -I $HERE/chain.py $REPO > $O/chain.txt          # producers, depths, the three deepest cones
python3 -I $HERE/family.py $REPO > $O/family.txt        # the frozen family (family.json)
python3 -I $HERE/sample.py $REPO > $O/sample.txt        # the seeded sample (sample.json); needs shape_classes.json if present
$HERE/run.sh Lib Native Equiv Measure Variants Sample SampleS8 SampleMeasure JetRate
grep MEASURE $HERE/build/Measure.log | sed 's/^MEASURE //' > $O/measure.jsonl
grep MEASURE $HERE/build/SampleMeasure.log | sed 's/^MEASURE //' > $O/measure_sample.jsonl
python3 -I $HERE/shape_imports.py $REPO                  # producers.txt and lean/Shape.lean (header + ShapeBody.lean)
$HERE/run.sh Shape
python3 -I $HERE/shape_report.py $REPO > $O/shape_table.md
python3 -I $HERE/sample.py $REPO > $O/sample.txt
python3 -I $HERE/source_measure.py $REPO > $O/source_measure.txt
python3 -I $HERE/tables.py $REPO > $O/tables.md
python3 -I $HERE/examples.py $REPO > $O/examples.md
! grep -l "error" $HERE/build/*.log
