#!/usr/bin/env python3
"""Seeded samples of theorems for the in-proof recurrence run (level 2).

    python3 mk_samples.py <decls.jsonl> <outdir>

Eligible: kind == theorem, proofSize >= 800 (the threshold of the Mathlib run, out/reuse).
  uniform : 500 eligible theorems drawn uniformly without replacement (seed 20261109).
  dense   : whole modules, consecutive in sorted module-name order, starting at a seeded random
            module of each library, until >= 250 eligible theorems per library (NavierStokes,
            Euler). This mimics the Mathlib run, which took ALL eligible theorems of a few
            directories, so that sibling theorems are in the sample together.
Writes <outdir>/inproof_<name>/sample.txt with lines "<slice>\t<name>".
"""
import json, random, sys, os
from collections import defaultdict
decls = [json.loads(l) for l in open(sys.argv[1])]
out = sys.argv[2]
el = [d for d in decls if d["kind"] == "theorem" and d["proofSize"] >= 800]
el.sort(key=lambda d: d["name"])
rng = random.Random(20261109)
uni = rng.sample(el, 500)
bymod = defaultdict(list)
for d in el:
    bymod[d["module"]].append(d)
dense = []
info = {}
for lib in ("NavierStokes", "Euler"):
    mods = sorted(m for m in bymod if m.split(".")[0] == lib)
    i = rng.randrange(len(mods))
    got, used = [], []
    while len(got) < 250:
        m = mods[i % len(mods)]
        got += bymod[m]; used.append(m); i += 1
    dense += [(lib, d) for d in got]
    info[lib] = {"modules": used, "theorems": len(got)}
for name, rows in (("uniform", [(d["module"].split(".")[0], d) for d in uni]), ("dense", dense)):
    os.makedirs(f"{out}/inproof_{name}", exist_ok=True)
    with open(f"{out}/inproof_{name}/sample.txt", "w") as f:
        for lab, d in sorted(rows, key=lambda r: r[1]["name"]):
            f.write(f"{lab}\t{d['name']}\n")
json.dump({"eligible": len(el), "eligibleProofSize": sum(d["proofSize"] for d in el),
           "theorems": sum(1 for d in decls if d["kind"] == "theorem"),
           "theoremProofSize": sum(d["proofSize"] for d in decls if d["kind"] == "theorem"),
           "seed": 20261109, "dense": info}, open(f"{out}/samples.json", "w"), indent=1)
print(len(el), len(uni), len(dense), {k: (len(v["modules"]), v["modules"][0], v["modules"][-1]) for k, v in info.items()})
