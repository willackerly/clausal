#!/usr/bin/env python3
"""Verification of the friction export.

usage: friction_verify.py <ns|carleson|pfr> [--check]

1. Whole-corpus consistency checks against the existing declaration export and internal invariants.
2. A deterministic, feature-stratified sample of 15 theorems; for each one the source text, the
   `#check` output (with --check: one `lean` run per corpus on a scratch file outside the corpus;
   nothing is built), the signature recorded by the earlier export, and the exporter's telescope are
   written side by side to out/corpus/friction/<corpus>/verify_sample.md for reading by hand.
   Hand verdicts live in out/corpus/friction/<corpus>/verify_verdicts.json (written by the reader).
"""
import hashlib, json, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SURG = {'indicator', 'restrict', 'support', 'cutoff'}


def h(name):
    return hashlib.sha1(name.encode()).hexdigest()


def hyps(d):
    return [b for b in d.get('binders', []) if b['isProp']]


CATS = [
    ('conclusion is an existential over a real constant with a positivity conjunct', lambda d: d['concl']['exRealPos'] > 0),
    ('hypothesis mentions a cast function', lambda d: any('cast' in b['flags'] for b in hyps(d))),
    ('hypothesis or conclusion is a finiteness fact', lambda d: any(b['fin'] for b in hyps(d)) or d['concl']['fin'] != ''),
    ('hypothesis or conclusion mentions indicator/restrict/support/cutoff', lambda d: any(SURG & set(b['flags']) for b in hyps(d)) or bool(SURG & set(d['concl']['flags']))),
    ('measurability hypothesis', lambda d: any(b['cls'] == 'measurability' for b in hyps(d))),
    ('integrability hypothesis', lambda d: any(b['cls'] == 'integrability' for b in hyps(d))),
    ('regularity hypothesis', lambda d: any(b['cls'] == 'regularity' for b in hyps(d))),
    ('positivity hypothesis about a variable', lambda d: any(b['pos'] and b['subjVar'] is not None for b in hyps(d))),
    ('negation peeled somewhere', lambda d: any('N' in b['peel'] for b in hyps(d)) or 'N' in d['concl']['peel']),
    ('private theorem', lambda d: d['name'].startswith('_private.')),
    ('Prop-valued instance binder', lambda d: any(b['kind'] == 'inst' and b['isProp'] for b in d['binders'])),
    ('hypothesis mentions the ENNReal top element', lambda d: any('ennrealTop' in b['flags'] for b in hyps(d))),
    ('unconstrained', lambda d: True),
    ('unconstrained', lambda d: True),
    ('unconstrained', lambda d: True),
]


def main():
    corpus = sys.argv[1]
    live = '--check' in sys.argv
    o = os.path.join(REPO, 'out/corpus/friction', corpus)
    src = os.path.join(REPO, 'corpora', corpus)
    rows = [json.loads(l) for l in open(o + '/hyps.jsonl')]
    old = {}
    for l in open(os.path.join(REPO, 'out/corpus', corpus, 'decls.jsonl')):
        d = json.loads(l)
        old[d['name']] = d

    # ---- 1. whole-corpus checks
    chk = {'theorems': len(rows)}
    chk['theoremsInExistingExport'] = sum(1 for d in old.values() if d['kind'] == 'theorem')
    chk['statementSizeMismatch'] = sum(1 for d in rows if d['statementSize'] != old[d['name']]['statementSize'])
    chk['proofSizeMismatch'] = sum(1 for d in rows if d['proofSize'] != old[d['name']]['proofSize'])
    chk['proofSizeRatioSum'] = round(sum(d['proofSize'] for d in rows) / max(1, sum(old[d['name']]['proofSize'] for d in rows)), 5)
    bad_outer = bad_inner = bad_kind = 0
    for d in rows:
        m = d.get('mass')
        if not m:
            continue
        if abs(sum(m['outer'].values()) - m['nodes']) > 0.02 + 1e-3 * len(m['outer']):
            bad_outer += 1
        if abs(sum(m['inner'].values()) - m['nodes']) > 0.02 + 1e-3 * len(m['inner']):
            bad_inner += 1
        if abs(sum(m['kind']) - m['nodes']) > 0.02:
            bad_kind += 1
    chk['outerSharesDoNotSumToNodes'] = bad_outer
    chk['innerSharesDoNotSumToNodes'] = bad_inner
    chk['kindSharesDoNotSumToNodes'] = bad_kind
    chk['withoutMass'] = sum(1 for d in rows if not d.get('mass'))
    chk['withoutBinders'] = sum(1 for d in rows if 'binders' not in d)
    # every mention index is a valid earlier binder; every subjVar is mentioned
    bad_m = 0
    for d in rows:
        for b in d.get('binders', []):
            if any(j >= b['i'] for j in b['mentions']):
                bad_m += 1
            if b['isProp'] and b['subjVar'] is not None and b['subjVar'] not in b['mentions']:
                bad_m += 1
    chk['binderMentionsNotEarlier'] = bad_m
    # root class agrees with the conclusion class
    chk['rootClassDiffersFromConclusionClass'] = sum(1 for d in rows if d.get('rootClass') and d['rootClass'] != d['concl']['cls'])
    json.dump(chk, open(o + '/verify_checks.json', 'w'), indent=1)
    print(corpus, chk)

    # ---- 2. sample
    cand = sorted((d for d in rows if d['statementSize'] <= 700 and len(d['binders']) <= 16), key=lambda d: h(d['name']))
    picked, why = [], {}
    for label, pred in CATS:
        for d in cand:
            if d['name'] not in why and pred(d):
                picked.append(d); why[d['name']] = label
                break
    for d in cand:                      # top up if some category has no member in this corpus
        if len(picked) >= 15:
            break
        if d['name'] not in why:
            picked.append(d); why[d['name']] = 'unconstrained (category empty in this corpus)'
    # live #check (public names only)
    checks = {}
    if live:
        scratch = os.path.join(o, 'verify_check.lean')
        mods = sorted({d['module'] for d in picked})
        lines = ['import ' + m for m in mods]
        lineof = {}
        for d in picked:
            if d['name'].startswith('_private.'):
                continue
            lines.append('#check ' + '.'.join('«' + c + '»' for c in old[d['name']]['userName'].split('.')))
            lineof[len(lines)] = d['name']
        open(scratch, 'w').write('\n'.join(lines) + '\n')
        tc = open(os.path.join(src, 'lean-toolchain')).read().strip()
        lp = [os.path.join(src, '.lake/build/lib/lean')]
        pk = os.path.join(src, '.lake/packages')
        lp += [os.path.join(pk, p, '.lake/build/lib/lean') for p in sorted(os.listdir(pk))]
        env = dict(os.environ, LEAN_PATH=':'.join(lp), PATH=os.path.expanduser('~/.elan/bin') + ':' + os.environ['PATH'])
        r = subprocess.run(['lean', '+' + tc, scratch], capture_output=True, text=True, env=env, cwd=o)
        # `#check` prints one record per command, in order; a record starts at column 0
        recs = []
        for l in r.stdout.split('\n'):
            if l and not l[0].isspace():
                recs.append(l)
            elif recs and l:
                recs[-1] += '\n' + l
        order = [lineof[k] for k in sorted(lineof)]
        if len(recs) == len(order):
            checks = dict(zip(order, recs))
        else:
            print('WARNING: #check output count mismatch', len(recs), len(order), r.stderr[:500])
        json.dump(checks, open(o + '/verify_check_output.json', 'w'), indent=1, ensure_ascii=False)
    elif os.path.exists(o + '/verify_check_output.json'):
        checks = json.load(open(o + '/verify_check_output.json'))

    L = [f'# Hand-check sample: {corpus}\n',
         'Generated by `bench/friction_verify.py`. For each theorem: why it was picked, the source text, the `#check` output '
         '(live Lean run; private theorems cannot be named from another file, so for those only the signature printed by the earlier export is shown), '
         'and the exporter\'s telescope. Verdicts are in `verify_verdicts.json`.\n']
    for k, d in enumerate(picked):
        od = old[d['name']]
        L.append(f"## {k + 1}. `{od['userName']}`\n")
        L.append(f"picked for: {why[d['name']]}; module `{d['module']}`, lines {od['line']}-{od['endLine']}; statementSize {d['statementSize']}, proofSize {d['proofSize']}\n")
        path = os.path.join(src, d['module'].replace('.', '/') + '.lean')
        try:
            sl = open(path).read().split('\n')[od['line'] - 1: od['endLine']]
            out = []
            for s in sl[:14]:
                out.append(s)
                if ':= by' in s or s.rstrip().endswith(':=') or s.rstrip().endswith(' by'):
                    break
            L.append('source:\n```lean\n' + '\n'.join(out) + '\n```')
        except OSError as e:
            L.append(f'source: unreadable ({e})')
        if d['name'] in checks:
            L.append('`#check`:\n```\n' + checks[d['name']].strip() + '\n```')
        else:
            L.append('signature in `decls.jsonl` (no live `#check`):\n```\n' + od['statement'] + '\n```')
        L.append('exporter:\n')
        L.append('| i | name | binder | kind | head | class | peel | pos/fin (var) | flags | mentions | coarse key |')
        L.append('|---|---|---|---|---|---|---|---|---|---|---|')
        names = [b['name'] for b in d['binders']]
        for b in d['binders'] + [dict(d['concl'], i='⊢', name='', bi='', kind='concl', isProp=True)]:
            pf = ''
            if b.get('isProp'):
                pf = (b['pos'] or b['fin'])
                if b['subjVar'] is not None:
                    pf += f" ({names[b['subjVar']]})"
            ment = ' '.join(names[j] if not names[j].startswith('inst') else f'#{j}' for j in b['mentions'])
            L.append(f"| {b['i']} | {b['name']} | {b['bi']} | {b['kind']} | `{b['head']}` | {b.get('cls', '')} | {b.get('peel', '')} | {pf} | {' '.join(b['flags'])} | {ment} | `{b['coarse'].replace('|', '¦')}` |")
        c = d['concl']
        if c['exN']:
            L.append(f"\nconclusion existentials: {c['exN']} bound variables, {c['exReal']} of real type, {c['exRealPos']} with a positivity conjunct")
        hs = [b for b in d['binders'] if b['isProp']][:3]
        for b in hs:
            L.append(f"\nshape key of `{b['name']}`: `{b['shape']}`")
        m = d['mass']
        L.append(f"\nproof: nodes {m['nodes']}, outer {m['outer']}, cast region {m['castRegion']}, surgery region {m['surgRegion']}; "
                 f"non-project constant uses {d.get('constsExt')}\n")
    open(o + '/verify_sample.md', 'w').write('\n'.join(L) + '\n')
    json.dump([{'name': d['name'], 'why': why[d['name']]} for d in picked], open(o + '/verify_sample.json', 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
