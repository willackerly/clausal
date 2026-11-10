#!/usr/bin/env python3
"""Three before/after examples in full, cut from the corpus source and from lean/Native.lean."""
import json, sys, re
R = sys.argv[1]
fam = {f['name'].split('.', 2)[2]: f for f in json.load(open(R + '/out/corpus/lesssim/family.json'))}
nat = open(R + '/corpora/lesssim/lean/Native.lean').read().split('\n')
def native(short):
    i = next(k for k, l in enumerate(nat) if re.match(r'theorem ' + re.escape(short) + r'(\s|$)', l))
    j = i
    while j < len(nat) and nat[j].strip(): j += 1
    return '\n'.join(nat[i:j])
def orig(short):
    f = fam[short]
    src = open(R + '/corpora/ns/' + f['module'].replace('.', '/') + '.lean').read().split('\n')
    return '\n'.join(src[f['line'] - 1:f['endLine']])
for title, short in [('Example 1 (best case, a finite sum): step 9', 'physical_vector_sum_jet_bound_of_weighted'),
                     ('Example 2 (several uniform parameters, multiplication by a bounded factor): step 4', 'UniformClass.edge_absorbed'),
                     ('Example 3 (a step that got larger): step 12', 'potentialIncrement_bound')]:
    print(f'### {title}\n\nOriginal (`{fam[short]["module"]}`, lines {fam[short]["line"]}–{fam[short]["endLine"]}):\n\n```lean\n{orig(short)}\n```\n\nNative (`corpora/lesssim/lean/Native.lean`):\n\n```lean\n{native(short)}\n```\n')
