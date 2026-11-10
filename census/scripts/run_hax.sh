#!/usr/bin/env bash
# Third column: hax 0.5.0's Lean backend (`cargo hax into lean`), which is a driver around its own
# pinned Charon (nightly-2026.10.31) and Aeneas (build-2b9e3ea), run on a copy of each crate.
# Crate-level outcome only; output goes to work/hax/<crate>/proofs/lean and data/hax.json.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
HAX="$HERE/.tools/hax/cargo-hax"
mkdir -p "$HERE/work/hax"
python3 - "$HERE" <<'PY' > "$HERE/work/hax/crates.txt"
import json, sys
for p in json.load(open(sys.argv[1] + '/data/selection/pins.json')):
    print(p['name'], p['version'])
PY
while read -r name ver; do
  d="$HERE/work/hax/$name"
  rm -rf "$d"; cp -R "$HERE/crates/$name-$ver" "$d"
  s=$(date +%s)
  ( cd "$d" && CARGO_TARGET_DIR="$HERE/work/target/hax-$name" "$HAX" hax into -v lean > "$HERE/work/hax/$name.log" 2>&1 )
  echo "$name exit=$? secs=$(( $(date +%s) - s ))"
done < "$HERE/work/hax/crates.txt" | tee "$HERE/work/hax/summary.txt"
python3 - "$HERE" <<'PY'
import json, os, re, sys
H = sys.argv[1]
out = []
for line in open(H + '/work/hax/summary.txt'):
    name, ex, secs = line.split()
    log = re.sub(r'\x1b\[[0-9;]*m', '', open(f'{H}/work/hax/{name}.log', errors='replace').read())
    lean = []
    for d, _, fs in os.walk(f'{H}/work/hax/{name}/proofs/lean'):
        if '.lake' in d: continue
        lean += [os.path.join(d, f) for f in fs if f.endswith('.lean')]
    ndef = nax = nsorry = 0
    for f in lean:
        t = open(f, errors='replace').read()
        if '/Extraction/' in f:
            ndef += len(re.findall(r'^(?:@\[[^\n]*\]\s*)?(?:noncomputable\s+)?def\s', t, re.M))
            nax += len(re.findall(r'^axiom\s', t, re.M))
            nsorry += len(re.findall(r'\bsorry\b', t))
    errs = re.findall(r'aeneas > \[Error\] (.*)', log)
    fatal = bool(re.search(r'Raised at|Fatal error', log))
    ice = len(re.findall(r'internal compiler error', log))
    out.append({'crate': name, 'exit': int(ex.split('=')[1]), 'secs': int(secs.split('=')[1]), 'aeneas_errors': len(errs),
                'aeneas_fatal': fatal, 'last_error': errs[-1][:200] if errs else None, 'rustc_ice': ice,
                'extraction_files': sorted(os.path.relpath(f, f'{H}/work/hax/{name}/proofs/lean') for f in lean if '/Extraction/' in f),
                'defs': ndef, 'axioms': nax, 'sorries': nsorry,
                'hax_error': (re.findall(r'^error: hax: (.*)', log, re.M) or [None])[-1]})
json.dump(out, open(H + '/data/hax.json', 'w'), indent=1)
for o in out: print({k: v for k, v in o.items() if k != 'extraction_files'}, len(o['extraction_files']))
PY
