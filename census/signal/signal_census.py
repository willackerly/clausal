#!/usr/bin/env python3
"""Plan node S1a: libsignal-protocol (libsignal tag v0.105.4, workspace member rust/protocol) as an eleventh census row.

    signal_census.py <variant> <mode> tools     Charon + Aeneas, no Lean build
    signal_census.py <variant> <mode> build     lake build of the generated Lean + per-function join

variant  p5      the patched translator (census/fork, patches i-v): work/bin/aeneas-p5        <- the reported row
         pinned  the unpatched release Aeneas of the pipeline (clausal/.tools), on the LLBC of the p5 run (side row)
mode     shipped one Charon run, one Aeneas run, nothing marked or removed (same as census/fork/scripts/fork_census.py)
         cw      Charon-side workarounds only: functions holding a rustc-ICE site are marked #[charon::opaque] and Charon
                 is rerun; then ONE Aeneas run with nothing removed. Only used if `shipped` gives no LLBC.

census/scripts/census.py is imported unchanged; only its paths are redirected under census/signal/work/ (git-ignored).
The crate is a workspace member, so the copy made by the driver is the whole workspace and the inventory and Charon
run in its rust/protocol directory. Outputs: work/runs/<variant>-<mode>/{work,results}.
"""
import importlib.util, json, os, shutil, sys

SIG = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.dirname(SIG)
REPO = os.path.dirname(CENSUS)
WORK = os.path.join(SIG, 'work')
CDIR = 'libsignal-protocol-0.105.4'
NAME = 'libsignal-protocol'
MEMBER = os.path.join('rust', 'protocol')
variant, mode, action = sys.argv[1:4]
sys.path.insert(0, SIG)
import guard
guard.check_path(SIG)                            # a "/-" or "-/" in the work path breaks the generated Lean's comments
spec = importlib.util.spec_from_file_location('census', os.path.join(CENSUS, 'scripts', 'census.py'))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

PIN = os.path.join(REPO, 'clausal', '.tools', 'aeneas-nightly-2026.11.09-5a392f4')
RUN = os.path.join(WORK, 'runs', '%s-%s' % (variant, mode))
os.makedirs(os.path.join(RUN, 'data'), exist_ok=True)
C.HERE = RUN
C.RESULTS = os.path.join(RUN, 'results')
C.CRATES_DIR = os.path.join(WORK, 'crates')
C.LEAN = os.path.join(WORK, 'lean', variant)
C.CHARON = os.path.join(PIN, 'charon')
C.AENEAS = {'p5': os.path.join(WORK, 'bin', 'aeneas-p5'), 'pinned': os.path.join(PIN, 'aeneas')}[variant]
C.aeneas_run.__defaults__ = (C.AENEAS,) + C.aeneas_run.__defaults__[1:]
C.bisect_crash = lambda *a, **k: ([], 0)         # no search for crashing bodies
C.predict_surgery = lambda D: []                 # no up-front removals
# cargo's registry and git checkouts for this crate's dependencies stay inside work/ (deleted by `run.sh clean`)
C.ENV['CARGO_HOME'] = os.path.join(WORK, 'cargo-home')

# the crate root inside the workspace copy
_inventory, _charon_run, _mark_opaque = C.inventory, C.charon_run, C.mark_opaque
C.inventory = lambda src: _inventory(os.path.join(src, MEMBER))
if variant == 'p5':
    C.charon_run = lambda src, *a, **k: _charon_run(os.path.join(src, MEMBER), *a, **k)
else:
    def reuse_llbc(src, out_llbc, log, marks, tgt, extra_args=()):
        # side row: same Charon output as the reported row, so the two rows differ only in the Aeneas binary
        p5 = os.path.join(WORK, 'runs', 'p5-' + mode, 'work', 'run', NAME, os.path.basename(out_llbc))
        open(log, 'w').write('LLBC copied from %s\n' % p5)
        if os.path.exists(p5):
            shutil.copy(p5, out_llbc)
        return 0, 0.0, os.path.exists(out_llbc)
    C.charon_run = reuse_llbc
if mode == 'shipped':
    C.mark_opaque = lambda *a, **k: False        # no opaque marks: Charon runs once
elif mode == 'cw':
    C.mark_opaque = lambda src, f, *a, **k: _mark_opaque(os.path.join(src, MEMBER), f, *a, **k)
else:
    raise SystemExit('mode?')

# Charon names local files by absolute path or relative to the workspace root; the inventory is relative to the crate root
_span_of = C.span_of
def span_of(meta, files):
    sp = _span_of(meta, files)
    if sp and sp['local']:
        f = sp['file']
        i = f.find(MEMBER + os.sep)
        if i >= 0 and (i == 0 or f[i - 1] == os.sep):
            sp['file'] = f[i + len(MEMBER) + 1:]
    return sp
C.span_of = span_of
_parse_aeneas_log = C.parse_aeneas_log
def parse_aeneas_log(text):
    # the same mapping for the source locations Aeneas prints
    entries, fatal = _parse_aeneas_log(text)
    for e in entries:
        for sp in (e['source'], e['def_span'], (e['source'] or {}).get('macro_site')):
            if sp and sp['file'].startswith(MEMBER + os.sep):
                sp['file'] = sp['file'][len(MEMBER) + 1:]
    return entries, fatal
C.parse_aeneas_log = parse_aeneas_log
# the driver opens this list for an LLBC over 500 MB (unused once predict_surgery is off)
if not os.path.exists(os.path.join(RUN, 'data', 'std_models.json')):
    os.symlink(os.path.join(CENSUS, 'data', 'std_models.json'), os.path.join(RUN, 'data', 'std_models.json'))

if action == 'tools':
    res = C.run_crate(CDIR, max_rounds=1, do_lean=False, overrides=None)
else:
    res = C.finish(NAME, do_lean=True, build=True)
    hit = guard.lake_log_hit(os.path.join(RUN, 'work', 'run', NAME + C.TAG, 'lake.log'))
    if hit:                                      # finish() has already written its join: do not leave it to be reported
        os.remove(os.path.join(C.RESULTS, NAME + C.TAG + '.json'))
        sys.exit(hit)
res['version'] = '0.105.4 (libsignal tag v0.105.4, commit b2a5c30f; Cargo package version 0.1.0)'
res['tools'] = {'aeneas': {'p5': 'census/fork source build 0d21a9ec + patches (i)-(v), binary aeneas-p5', 'pinned': 'release nightly-2026.11.09-5a392f4'}[variant],
                'charon': '0.1.315 (454586e), release binary', 'rust': 'nightly-2026-09-17', 'lean': 'v4.35.0 + Aeneas library of nightly-2026.11.09', 'mode': mode}
json.dump(res, open(os.path.join(C.RESULTS, NAME + '.json'), 'w'), indent=1)
fs = [f for f in res['functions'] if f['origin'] == 'source']
print(variant, mode, action, NAME, 'fns', len(fs), 'charon_ok', sum(1 for f in fs if f['charon'] == 'ok'), 'aeneas_ok', sum(1 for f in fs if f['aeneas'] == 'ok'),
      'ok', sum(1 for f in fs if f.get('ok')), 'as_is', (res.get('as_is') or {}).get('msg', '')[:200],
      'rc', [(r['stage'], r['rc']) for r in res['rounds']], 'secs', [r['secs'] for r in res['rounds']], 'lake', res.get('lake'))
