#!/usr/bin/env python3
"""Cross-check of the census's "no axiom beneath" column by the Lean elaborator (the census column is a token scan of
the generated file). For every function of rust/protocol/src that the join reports as "through", ask Lean:
is each of its definitions in the environment, and which axioms does it depend on (Lean.collectAxioms, transitive)?

Two readings are reported. Strict: a function is "no axiom beneath (Lean)" when all its definitions exist and their axioms are a subset of
{propext, Classical.choice, Quot.sound}. `sorryAx` (Lean recovered from an error somewhere beneath) and every axiom
Aeneas emitted for an external or untranslated item count as an axiom beneath.
Middle ("no value axiom"): as strict, but an opaque external type (`axiom T : Type`) is allowed; opaque functions,
constants and sorryAx are not.

    axiom_check.py [row]        row defaults to p5-shipped;  writes axioms.json (small) and prints the counts
The generated file is copied to work/lean/<variant>/Generated/AxiomCheck.lean with one command appended, and checked with
`lake env lean` (the file has errors, so there is no .olean to import; Lean goes on after errors, so the command runs).
"""
import collections, json, os, subprocess, sys

SIG = os.path.dirname(os.path.abspath(__file__))
row = sys.argv[1] if len(sys.argv) > 1 else 'p5-shipped'
variant = row.split('-')[0]
STD = {'propext', 'Classical.choice', 'Quot.sound'}
res = json.load(open(os.path.join(SIG, 'work', 'runs', row, 'results', 'libsignal-protocol.json')))
gen = os.path.join(SIG, 'work', 'runs', row, 'work', 'run', 'libsignal-protocol', 'lean', 'Generated', 'LibsignalProtocol.lean')
lean_dir = os.path.join(SIG, 'work', 'lean', variant)
CMD = r'''

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut out : Array String := #[]
  for (n, _) in env.constants.map₂.toList do
    if (`libsignal_protocol).isPrefixOf n then
      let ax ← Lean.collectAxioms n
      out := out.push s!"AXCHK\t{n}\t{String.intercalate "," (ax.toList.map toString)}"
      if let some (.axiomInfo v) := env.find? n then
        out := out.push s!"AXKIND\t{n}\t{if v.type.getForallBody.isSort then "type" else "value"}"
  IO.println (String.intercalate "\n" out.toList)
'''
dst = os.path.join(lean_dir, 'Generated', 'AxiomCheck.lean')
open(dst, 'w').write(open(gen).read() + CMD)
env = dict(os.environ, PATH=os.path.expanduser('~/.elan/bin') + ':' + os.environ['PATH'])
p = subprocess.run(['lake', 'env', 'lean', '-DmaxErrors=10000000', 'Generated/AxiomCheck.lean'], cwd=lean_dir, env=env, capture_output=True, text=True)
os.remove(dst)
ax, kind = {}, {}
for l in p.stdout.split('\n'):
    if l.startswith('AXCHK\t'):
        _, n, a = l.split('\t')
        ax[n] = [x for x in a.split(',') if x]
    elif l.startswith('AXKIND\t'):
        _, n, k = l.split('\t')
        kind[n] = k
if not ax:
    sys.exit('no AXCHK lines; lean said:\n' + (p.stdout[-3000:] + p.stderr[-3000:]))
src = [f for f in res['functions'] if f['origin'] == 'source' and f['file'].startswith('src/')]
counted = [f for f in src if f['charon'] != 'absent']
rows, n_through, n_clean, n_census, both, loc_clean, n_mid, loc_mid = [], 0, 0, 0, 0, 0, 0, 0
why = collections.Counter()
ax_all = {}
for f in counted:
    if not (f['charon'] == 'ok' and f['aeneas'] == 'ok' and f['lean'] == 'ok'):
        continue
    n_through += 1
    names = ['libsignal_protocol.' + n for n in f['lean_names']]
    missing = [n for n in names if n not in ax]
    extra = sorted(set(a for n in names for a in ax.get(n, []) if a not in STD))
    clean = bool(names) and not missing and not extra
    ax_all[(f['file'], f['line_start'])] = extra
    n_clean += clean
    # middle reading: an opaque external *type* (an `axiom T : Type` Aeneas emits for a type of another crate) is allowed;
    # opaque functions and constants, and sorryAx, are not
    mid = bool(names) and not missing and all(kind.get(a) == 'type' for a in extra)
    n_mid += mid
    loc_mid += f['loc'] if mid else 0
    loc_clean += f['loc'] if clean else 0
    n_census += bool(f.get('ok_closure_no_axiom'))
    both += bool(clean and f.get('ok_closure_no_axiom'))
    if not clean:
        why['not in the environment' if missing else ('sorryAx' if 'sorryAx' in extra else 'crate axiom')] += 1
    rows.append({'file': f['file'], 'line': f['line_start'], 'name': f['name'], 'loc': f['loc'], 'lean_names': f['lean_names'], 'missing': missing,
                 'axioms': extra[:8], 'n_axioms': len(extra), 'no_axiom_lean': clean, 'no_value_axiom_lean': mid, 'no_axiom_census': bool(f.get('ok_closure_no_axiom'))})
n_sound = sum(1 for x in rows if not x['missing'] and 'sorryAx' not in ax_all[(x['file'], x['line'])])
out = {'row': row, 'constants_checked': len(ax), 'counted': len(counted), 'through': n_through, 'through_in_env_without_sorry_lean': n_sound, 'no_axiom_lean': n_clean, 'no_axiom_lean_loc': loc_clean,
       'share_no_axiom_lean': n_clean / len(counted), 'no_value_axiom_lean': n_mid, 'no_value_axiom_lean_loc': loc_mid, 'share_no_value_axiom_lean': n_mid / len(counted),
       'crate_axioms': dict(collections.Counter(kind.values())), 'no_axiom_census': n_census, 'agree_clean': both,
       'census_only': n_census - both, 'lean_only': n_clean - both, 'through_but_not_clean_why': dict(why), 'functions': rows}
json.dump(out, open(os.path.join(SIG, 'axioms.json'), 'w'), indent=1)
print({k: v for k, v in out.items() if k != 'functions'})
