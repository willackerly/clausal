#!/usr/bin/env python3
"""List the Rust standard-library items the pinned Aeneas Lean library models, read from the
`@[rust_fun "..."]`, `@[rust_type "..."]`, `@[rust_trait "..."]`, `@[rust_trait_impl "..."]`
attributes in backends/lean/Aeneas.  Output: data/std_models.json"""
import os, re, json, collections
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(HERE, '.tools', 'aeneas-nightly-2026.11.09-5a392f4', 'backends', 'lean', 'Aeneas')
out = collections.defaultdict(list)
for d, _, fs in os.walk(LIB):
    if '.lake' in d:
        continue
    for f in fs:
        if not f.endswith('.lean'):
            continue
        t = open(os.path.join(d, f), errors='replace').read()
        for m in re.finditer(r'rust_(fun|type|trait|trait_impl|const|global)\s*\n?\s*"([^"]+)"', t):
            out[m.group(1)].append({'rust': m.group(2), 'file': os.path.relpath(os.path.join(d, f), LIB)})
for k in out:
    seen = set()
    out[k] = [x for x in sorted(out[k], key=lambda x: x['rust']) if not (x['rust'] in seen or seen.add(x['rust']))]
json.dump(out, open(os.path.join(HERE, 'data', 'std_models.json'), 'w'), indent=1)
print({k: len(v) for k, v in out.items()})
mods = collections.Counter()
for x in out['fun']:
    p = re.sub(r'\{[^{}]*\}', '{impl}', x['rust'])
    mods['::'.join(p.split('::')[:3])] += 1
for k, v in mods.most_common(60):
    print(v, k)
