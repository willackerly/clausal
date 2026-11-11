#!/bin/zsh
# M9 families, clustering step, end to end.   run.sh
# Reads the built projects (corpora/{ns,carleson,pfr}) and the dead-code tool's result (out/deadcode/) only;
# writes under tools/families/build and out/families/.  Nothing in a corpus is built or modified.
set -e
H=${0:A:h}; cd $H
for p in ns carleson pfr; do
  ./export.sh $p 4                 # typed trees of every project definition, structure and theorem statement
  python3 features.py $p           # shape keys, signature keys, API profiles (shapes and roles), usage
  python3 cluster.py $p            # clusters at each level, generalisations, triage score -> clusters.jsonl
done
python3 cluster.py ns --all        # every definition, dead code included (cloned-module control)
./planted.sh                       # synthetic families mixed into ns -> clusters_planted.jsonl, planted_result.json
python3 report.py                  # out/families/ns/CLUSTERS.md
