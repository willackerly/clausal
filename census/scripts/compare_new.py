#!/usr/bin/env python3
"""Side-by-side: run the newer Aeneas release on exactly the LLBC the pinned Aeneas was given
(as-is LLBC and, where a peel was needed, the peeled LLBC) and compare the outputs.

The newer release ships the same Charon (0.1.315, 454586e), so the Charon column is identical by
construction and only the Aeneas step is repeated. Output: data/newer_aeneas.json
"""
import json, os, re, subprocess, sys, shutil, difflib, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW = os.path.join(HERE, '.tools', 'aeneas-nightly-2026.11.10-0d21a9e', 'aeneas')
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def run(llbc, dest, log):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    t = time.time()
    with open(log, 'w') as f:
        rc = subprocess.call([NEW, '-backend', 'lean', '-dest', dest, '-subdir', 'Generated', '-emit-json', '-no-progress-bar', '-print-error-emitters', llbc],
                             cwd=os.path.dirname(llbc), stdout=f, stderr=subprocess.STDOUT)
    return rc, round(time.time() - t, 1)


def errors(log):
    t = ANSI.sub('', open(log, errors='replace').read())
    return len(re.findall(r'^\[Error\]', t, re.M)), bool(re.search(r'^Fatal error', t, re.M))


out = []
for name in sorted(os.listdir(os.path.join(HERE, 'work', 'run'))):
    W = os.path.join(HERE, 'work', 'run', name)
    sp = os.path.join(W, 'state.json')
    if not os.path.exists(sp):
        continue
    st = json.load(open(sp))
    rec = {'crate': name}
    asis = os.path.join(W, name.replace('-', '_') + '.llbc')
    if os.path.exists(asis):
        rc, secs = run(asis, os.path.join(W, 'new_asis'), os.path.join(W, 'new_asis.log'))
        n, fatal = errors(os.path.join(W, 'new_asis.log'))
        old_n, old_fatal = errors(os.path.join(W, 'aeneas.0.log'))
        rec['as_is'] = {'new_rc': rc, 'new_errors': n, 'new_fatal': fatal, 'pinned_errors': old_n, 'pinned_fatal': old_fatal}
    if st.get('final_round') is not None:
        llbc = os.path.join(W, st['llbc'])
        d = os.path.join(W, 'new_peeled')
        rc, secs = run(llbc, d, os.path.join(W, 'new_peeled.log'))
        n, fatal = errors(os.path.join(W, 'new_peeled.log'))
        old_n, old_fatal = errors(os.path.join(W, 'aeneas.%d.log' % st['final_round']))
        a = open(os.path.join(W, 'lean', 'Generated', st['lean_file'])).read().split('\n')
        bp = os.path.join(d, 'Generated', st['lean_file'])
        b = open(bp).read().split('\n') if os.path.exists(bp) else []
        diff = [l for l in difflib.unified_diff(a, b, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
        rec['peeled'] = {'new_rc': rc, 'secs': secs, 'new_errors': n, 'new_fatal': fatal, 'pinned_errors': old_n, 'pinned_fatal': old_fatal,
                         'lean_lines_pinned': len(a), 'lean_lines_new': len(b), 'diff_lines': len(diff), 'diff_sample': diff[:12]}
    out.append(rec)
    print(rec['crate'], rec.get('as_is'), {k: v for k, v in rec.get('peeled', {}).items() if k != 'diff_sample'})
json.dump(out, open(os.path.join(HERE, 'data', 'newer_aeneas.json'), 'w'), indent=1)
