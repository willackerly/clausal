#!/usr/bin/env python3
"""Census pipeline for one Aeneas binary of the fork spike. Reuses census/scripts/census.py unchanged (imported),
with its paths redirected under census/fork/ and its peel switched off.

    fork_census.py <variant> <mode> tools <crate>-<version>     Charon + Aeneas, no Lean build
    fork_census.py <variant> <mode> build <crate>-<version>     lake build of the generated Lean + per-function join

variant  base | p1 | p2 | p3 | p4 | p5       -> binary bin/aeneas-<variant>  (p5 = the four patches asked for plus the formatter reset)
mode     shipped   tools exactly as invoked by the census's "as is" round: one Charon run, one Aeneas run, nothing removed
         cw        cedar only, "Charon workarounds": the census's Charon-side marks are kept (functions holding a rustc-ICE
                   site are marked #[charon::opaque]; the two generated LALRPOP parsers are opaque, data/overrides.json),
                   and then ONE Aeneas run with nothing removed from the LLBC (no trait surgery, no crash cache, no bisection)
Outputs: runs/<variant>-<mode>/work/run/<crate>/ (logs, LLBC, Lean), runs/<variant>-<mode>/results/<crate>.json
"""
import importlib.util, json, os, sys

FORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.dirname(FORK)
variant, mode, action, cdir = sys.argv[1:5]
spec = importlib.util.spec_from_file_location('census', os.path.join(CENSUS, 'scripts', 'census.py'))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

RUN = os.path.join(FORK, 'runs', '%s-%s' % (variant, mode))
os.makedirs(os.path.join(RUN, 'data'), exist_ok=True)
C.HERE = RUN                                     # work/ and data/ lookups go under runs/<variant>-<mode>/
C.RESULTS = os.path.join(RUN, 'results')
C.LEAN = os.path.join(FORK, 'lean', variant)
C.AENEAS = os.path.join(FORK, 'bin', 'aeneas-' + variant)
C.aeneas_run.__defaults__ = (C.AENEAS,) + C.aeneas_run.__defaults__[1:]
C.bisect_crash = lambda *a, **k: ([], 0)         # no search for crashing bodies
C.predict_surgery = lambda D: []                 # no up-front removals
overrides = None
if mode == 'shipped':
    C.mark_opaque = lambda *a, **k: False        # no opaque marks: Charon runs once
elif mode == 'cw':
    overrides = json.load(open(os.path.join(CENSUS, 'data', 'overrides.json'))).get(C.re.sub(r'-\d+\.\d+\.\d+.*$', '', cdir))
    # the builtin-trait list the driver reads for big crates (unused once predict_surgery is off, but it is opened)
    src = os.path.join(CENSUS, 'data', 'std_models.json')
    dst = os.path.join(RUN, 'data', 'std_models.json')
    if not os.path.exists(dst):
        os.symlink(src, dst)
else:
    raise SystemExit('mode?')
name = C.re.sub(r'-\d+\.\d+\.\d+.*$', '', cdir)
if action == 'tools':
    res = C.run_crate(cdir, max_rounds=1, do_lean=False, overrides=overrides)
else:
    res = C.finish(name, do_lean=True, build=True)
res['tools'] = {'aeneas': 'source build, variant ' + variant, 'charon': '0.1.315 (454586e), release binary', 'rust': 'nightly-2026-09-17', 'lean': 'v4.35.0 + Aeneas library of nightly-2026.11.09'}
json.dump(res, open(os.path.join(C.RESULTS, name + '.json'), 'w'), indent=1)
fs = [f for f in res['functions'] if f['origin'] == 'source']
print(variant, mode, action, name, 'fns', len(fs), 'aeneas_ok', sum(1 for f in fs if f['aeneas'] == 'ok'), 'ok', sum(1 for f in fs if f.get('ok')),
      'loc_ok', sum(f['loc'] for f in fs if f.get('ok')), 'as_is', (res.get('as_is') or {}).get('msg', '')[:150],
      'aeneas_rc', [r['rc'] for r in res['rounds'] if r['stage'] == 'aeneas'], 'secs', [r['secs'] for r in res['rounds']], 'lake', res.get('lake'))
