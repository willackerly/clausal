#!/usr/bin/env python3
"""M7 stage 2 driver.  usage: stage2.py <project> [--planted] [--jobs N] [--only id,id]
Writes one batch file per job under tools/reinvent/build/<project>/batch, runs one `lean` per batch against
the project's built environment (read only), and collects the `RV` result lines into
out/reinvent/<project|planted>/stage2.jsonl.  Order of attempts per candidate: equivalence without side
conditions; with the side conditions of the match (if any); implication D -> L (if the match had extra
conjuncts)."""
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '..', '..')


def env(project):
    src = os.path.join(REPO, 'corpora', project)
    tc = open(os.path.join(src, 'lean-toolchain')).read().strip()
    b = os.path.join(HERE, 'build', project)
    lp = [b, os.path.join(src, '.lake/build/lib/lean')]
    pk = os.path.join(src, '.lake/packages')
    for d in sorted(os.listdir(pk)):
        lp.append(os.path.join(pk, d, '.lake/build/lib/lean'))
    e = dict(os.environ)
    e['PATH'] = os.path.expanduser('~/.elan/bin') + ':' + e['PATH']
    e['LEAN_PATH'] = ':'.join(lp)
    return tc, b, e


def ensure_confirm(project):
    tc, b, e = env(project)
    o = os.path.join(b, 'Confirm.olean')
    srcf = os.path.join(HERE, 'Confirm.lean')
    if not os.path.exists(o) or os.path.getmtime(o) < os.path.getmtime(srcf):
        subprocess.run(['lean', '+' + tc, '-o', o, srcf], env=e, check=True, cwd=HERE)


def run_batches(project, tag, lines_per_job, extra_imports=()):
    """lines_per_job: list of lists of command lines.  Returns parsed RV records."""
    tc, b, e = env(project)
    ensure_confirm(project)
    bd = os.path.join(b, 'batch')
    os.makedirs(bd, exist_ok=True)
    mods = [m for m in open(os.path.join(b, 'modules.txt')).read().split() if m != 'ReinventPlanted']
    hdr = ''.join('import %s\n' % m for m in list(mods) + list(extra_imports)) + 'import Confirm\n' \
        'set_option maxRecDepth 2000\nset_option linter.all false\n'
    procs = []
    for k, lines in enumerate(lines_per_job):
        f = os.path.join(bd, '%s_%d.lean' % (tag, k))
        open(f, 'w').write(hdr + '\n'.join(lines) + '\n')
        lg = open(f + '.out', 'w')
        procs.append((subprocess.Popen(['lean', '+' + tc, '-D', 'maxHeartbeats=0', f], env=e, stdout=lg,
                                       stderr=subprocess.STDOUT, cwd=bd), f))
    out = []
    for p, f in procs:
        p.wait()
        for line in open(f + '.out', errors='replace'):
            if line.startswith('RV '):
                try:
                    out.append(json.loads(line[3:]))
                except Exception:
                    pass
    return out


def cmd(c, mode, sides):
    ps = ' '.join('p%d' % i for i in range(c['np']))
    fn = (lambda body: '(fun %s => %s)' % (ps, body)) if c['np'] else (lambda body: '(%s)' % body)
    simpset = ', '.join(dict.fromkeys(c['unfold'] + c['rw']))
    cid = c['id'] + ('s' if sides else '')
    return 'reinvent_equiv "%s" %s %d "%s" %s sides [%s] using "%s"' % (
        cid, c['D'], c['np'], mode, fn(c['rhs']), ', '.join(fn(s) for s in sides), simpset)


def main():
    project = sys.argv[1]
    planted = '--planted' in sys.argv
    jobs = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 6
    only = set(sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else None
    out = os.path.join(REPO, 'out/reinvent', 'planted' if planted else project)
    cands = [json.loads(l) for l in open(os.path.join(out, 'candidates.jsonl'))]
    if only:
        cands = [c for c in cands if c['id'] in only]
    per = [[] for _ in range(jobs)]
    for i, c in enumerate(cands):
        L = per[i % jobs]
        L.append(cmd(c, 'iff', []))
        if c['sides']:
            L.append(cmd(c, 'iff', c['sides']))
        if c['isProp'] and c['extras']:
            L.append(cmd(c, 'imp', []))
    t0 = time.time()
    res = run_batches(project, 'eq', per, ['ReinventPlanted'] if planted else [])
    by = {}
    for r in res:
        by.setdefault(r['id'].rstrip('s'), []).append(r)
    n = 0
    with open(os.path.join(out, 'stage2.jsonl'), 'w') as f:
        for c in cands:
            rs = by.get(c['id'], [])
            plain = next((r for r in rs if r['mode'] == 'iff' and not r['id'].endswith('s')), None)
            side = next((r for r in rs if r['mode'] == 'iff' and r['id'].endswith('s')), None)
            imp = next((r for r in rs if r['mode'] == 'imp'), None)
            if plain is None:
                verdict = 'no result'
            elif plain['status'] == 'proved':
                verdict = 'proved'
            elif side is not None and side['status'] == 'proved':
                verdict = 'proved under side condition'
            elif plain['status'] == 'refuted':
                verdict = 'refuted'
            elif plain['status'] == 'illformed':
                verdict = 'ill-typed'
            elif imp is not None and imp['status'] == 'proved':
                verdict = 'implication only'
            else:
                verdict = 'not proved'
            best = plain if verdict == 'proved' else side if verdict == 'proved under side condition' else \
                imp if verdict == 'implication only' else plain
            c2 = dict(c)
            c2.update(verdict=verdict, tactic=(best or {}).get('tactic'), thm=(best or {}).get('thm'),
                      stdAxioms=(best or {}).get('stdAxioms'), stmt=(best or {}).get('stmt'),
                      msg=(plain or {}).get('msg'))
            f.write(json.dumps(c2, ensure_ascii=False) + '\n')
            n += 1
    print('%s: %d candidates, %d result lines, %.0f s' % (project, n, len(res), time.time() - t0))


if __name__ == '__main__':
    main()
