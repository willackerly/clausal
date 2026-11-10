#!/usr/bin/env python3
"""Rewrite-cost experiment.

rewrites/rewrites.json lists, per rewrite: the crate, the function (file + name + the line it starts at in
the pinned source), the idiom removed and a unified diff in rewrites/patches/ against crates/<crate>-<version>.

For each rewrite this script
  1. copies the pinned crate to work/rewrites/crates/<crate>-<version> and applies the patch (patch -p1)
  2. runs the crate's own tests (`cargo test`, stable toolchain) on the pinned and on the patched source
  3. runs the census pipeline (scripts/census.py, tag _rw<id>) on the patched source
  4. reads the status of the rewritten function before (data/results) and after (data/rewrites)
and writes data/rewrites.json.   Usage: rewrites/run.py [id ...]
"""
import json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = dict(os.environ)
ENV['PATH'] = os.path.expanduser('~/.elan/bin') + ':' + os.path.expanduser('~/.cargo/bin') + ':' + ENV['PATH']
RW = json.load(open(os.path.join(HERE, 'rewrites', 'rewrites.json')))
only = set(sys.argv[1:])


def cargo_test(src, tag, args, extra_env=None):
    log = os.path.join(HERE, 'work', 'rewrites', tag + '.test.log')
    env = dict(ENV, CARGO_TARGET_DIR=os.path.join(HERE, 'work', 'target', 'test-' + tag.split('__')[0]))
    env.update(extra_env or {})
    with open(log, 'w') as f:
        rc = subprocess.call(['cargo', '+stable', 'test'] + args, cwd=src, stdout=f, stderr=subprocess.STDOUT, env=env)
    t = open(log, errors='replace').read()
    passed = sum(int(x) for x in re.findall(r'test result: \w+\. (\d+) passed', t))
    failed = sum(int(x) for x in re.findall(r'test result: \w+\. \d+ passed; (\d+) failed', t))
    return {'rc': rc, 'passed': passed, 'failed': failed}


def status(res, file, name, line=None, near=None):
    cand = [f for f in res['functions'] if f['origin'] == 'source' and f['file'] == file and f['name'] == name]
    if line is not None and len(cand) > 1:
        cand = sorted(cand, key=lambda f: abs(f['line_start'] - line))[:1]
    if not cand:
        return None
    f = cand[0]
    st = 'compiles in Lean' if f.get('ok') else ('fails at %s: %s' % (next((m['stage'] for m in f['msgs']), '?'), (f['msgs'][0]['msg'][:110] if f['msgs'] else '?')))
    return {'ok': bool(f.get('ok')), 'text': st, 'loc': f['loc'], 'line': f['line_start'], 'closure_ok': f.get('ok_closure'), 'no_axiom': f.get('ok_closure_no_axiom'),
            'dep_axioms': f.get('dep_axioms'), 'dep_lib': f.get('dep_lib')}


out = []
prev = {}
pp = os.path.join(HERE, 'data', 'rewrites.json')
if os.path.exists(pp):
    prev = {x['id']: x for x in json.load(open(pp))}
os.makedirs(os.path.join(HERE, 'work', 'rewrites', 'crates'), exist_ok=True)
base_tests = {}
for rw in RW:
    if only and str(rw['id']) not in only:
        if rw['id'] in prev:
            out.append(prev[rw['id']])
        continue
    cdir = '%s-%s' % (rw['crate'], rw['version'])
    tag = '_rw%s' % rw['id']
    root = os.path.join(HERE, 'work', 'rewrites', 'crates' + tag)
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    dst = os.path.join(root, cdir)
    shutil.copytree(os.path.join(HERE, 'crates', cdir), dst, symlinks=True)
    patch = os.path.join(HERE, 'rewrites', 'patches', rw['patch'])
    pr = subprocess.run(['patch', '-p1', '--no-backup-if-mismatch', '-i', patch], cwd=dst, capture_output=True, text=True)
    if pr.returncode != 0:
        raise SystemExit('patch failed for %s: %s' % (rw['id'], pr.stdout + pr.stderr))
    diff = open(patch).read().split('\n')
    plus = sum(1 for l in diff if l.startswith('+') and not l.startswith('+++'))
    minus = sum(1 for l in diff if l.startswith('-') and not l.startswith('---'))
    targs = rw.get('test_args', [])
    if cdir not in base_tests:
        base_tests[cdir] = cargo_test(os.path.join(HERE, 'crates', cdir), rw['crate'] + '__base', targs, rw.get('test_env'))
    after_tests = cargo_test(dst, rw['crate'] + '__rw%s' % rw['id'], targs, rw.get('test_env'))
    env = dict(ENV, CENSUS_CRATES=root, CENSUS_TAG=tag)
    log = os.path.join(HERE, 'work', 'rewrites', 'census%s.log' % tag)
    with open(log, 'w') as f:
        subprocess.call([sys.executable, os.path.join(HERE, 'scripts', 'census.py'), 'run', cdir], stdout=f, stderr=subprocess.STDOUT, env=env)
    before = status(json.load(open(os.path.join(HERE, 'data', 'results', rw['crate'] + '.json'))), rw['file'], rw['function'], rw.get('line'))
    after_res = json.load(open(os.path.join(HERE, 'data', 'rewrites', rw['crate'] + tag + '.json')))
    after = status(after_res, rw['file'], rw['function'], rw.get('line'))
    helpers = [status(after_res, rw['file'], h) for h in rw.get('new_helpers', [])]
    # crate-level effect of the patch: of the functions that failed for this cause in the pinned crate, how many compile now
    def keyed(fs):
        out, seen = {}, {}
        for f in sorted((f for f in fs if f['origin'] == 'source'), key=lambda f: (f['file'], f['name'], f['line_start'])):
            k = (f['file'], f['name'])
            seen[k] = seen.get(k, 0) + 1
            out[(f['file'], f['name'], seen[k])] = f
        return out
    import importlib.util
    spec = importlib.util.spec_from_file_location('report', os.path.join(HERE, 'scripts', 'report.py'))
    report = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(report)
    base = json.load(open(os.path.join(HERE, 'data', 'results', rw['crate'] + '.json')))
    kb, ka = keyed(base['functions']), keyed(after_res['functions'])
    hit = [k for k, f in kb.items() if f['charon'] != 'absent' and not f.get('ok') and rw.get('class') in report.classes_of(f)]
    fixed = [k for k in hit if k in ka and ka[k].get('ok')]
    ok_before = sum(1 for f in kb.values() if f.get('ok'))
    ok_after = sum(1 for f in ka.values() if f.get('ok'))
    b, a = base_tests[cdir], after_tests
    rec = {'id': rw['id'], 'crate': rw['crate'], 'file': rw['file'], 'function': rw['function'], 'line': before and before['line'], 'idiom': rw['idiom'],
           'before': before['text'] if before else 'not found', 'after': (after['text'] if after else 'not found') + ('' if not helpers else '; new helper(s): ' + ', '.join(('ok' if h and h['ok'] else 'FAIL') for h in helpers)),
           'after_ok': bool(after and after['ok'] and all(h and h['ok'] for h in helpers)),
           'after_detail': after, 'helpers': helpers,
           'tests_before': b, 'tests_after': a,
           'tests': ('%d pass, %d fail (pinned: %d pass, %d fail)' % (a['passed'], a['failed'], b['passed'], b['failed'])),
           'loc_before': before['loc'] if before else 0, 'loc_after': (after['loc'] if after else 0) + sum(h['loc'] for h in helpers if h),
           'lines_changed': '+%d/−%d' % (plus, minus), 'class_before': len(hit), 'class_fixed': len(fixed), 'crate_ok_before': ok_before, 'crate_ok_after': ok_after, 'surgery_after': [s['name'] for s in after_res['surgery']], 'note': rw.get('note')}
    out.append(rec)
    print(json.dumps({k: rec[k] for k in ('id', 'function', 'before', 'after', 'tests', 'lines_changed')}))
    json.dump(out, open(pp, 'w'), indent=1)
json.dump(out, open(pp, 'w'), indent=1)
