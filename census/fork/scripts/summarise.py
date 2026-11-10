#!/usr/bin/env python3
"""Per-variant, per-crate counts for the fork spike -> data/summary.json and data/tables.md

The denominator is the census's: the functions the census counted for each crate (census/data/results/<crate>.json, source
functions that reach the compiler), with the census's code-line counts. A function "ends as compiling Lean" exactly as in the
census: every Charon declaration of it has a Lean definition, none is an axiom / has a `sorry` / has an Aeneas error logged
against it, and `lake build` reports no error inside them (field `ok` of the per-function record).
"""
import json, os, sys
FORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.dirname(FORK)
ORDER = ['cedar-policy-core', 'rust_decimal', 'semver', 'shlex', 'rusty-money', 'indexmap', 'untrusted', 'fnv', 'time', 'zeroize']
VARIANTS = ['base', 'p1', 'p2', 'p3', 'p4', 'p5']
LABEL = {'base': 'unpatched (source build of 0d21a9ec)', 'p1': '+ (i) FunsAnalysis recursion', 'p2': '+ (ii) trait method signature guard',
         'p3': '+ (iii) per-function exception catching', 'p4': '+ (iv) Lean name capture', 'p5': '+ (v) formatter reset after an extraction error (extra)'}


def load(variant, mode, crate):
    p = os.path.join(FORK, 'runs', '%s-%s' % (variant, mode), 'results', crate + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    out = {'variants': {}, 'census': {}}
    counted = {}
    for c in ORDER:
        r = json.load(open(os.path.join(CENSUS, 'data', 'results', c + '.json')))
        fs = {f['id']: f for f in r['functions'] if f['origin'] == 'source' and f['charon'] != 'absent'}
        counted[c] = fs
        out['census'][c] = {'fns': len(fs), 'loc': sum(f['loc'] for f in fs.values()),
                            'peeled_ok': sum(1 for f in fs.values() if f.get('ok')), 'peeled_ok_loc': sum(f['loc'] for f in fs.values() if f.get('ok'))}
    for mode in ('shipped', 'cw'):
        for v in VARIANTS:
            for c in ORDER:
                r = load(v, mode, c)
                if r is None:
                    continue
                fs = [f for f in r['functions'] if f['origin'] == 'source' and f['id'] in counted[c]]
                # an Aeneas round that was killed (negative return code) or timed out is not a measurement
                unfinished = any(x['stage'] == 'aeneas' and (x['rc'] == 'timeout' or (isinstance(x['rc'], int) and x['rc'] < 0)) for x in r['rounds'])
                ok = [f for f in fs if f.get('ok')]
                aen = [f for f in fs if f['charon'] == 'ok' and f['aeneas'] == 'ok']
                d = {'fns': len(counted[c]), 'loc': out['census'][c]['loc'], 'ok': len(ok), 'ok_loc': sum(counted[c][f['id']]['loc'] for f in ok),
                     'aeneas_ok': len(aen), 'aeneas_ok_loc': sum(counted[c][f['id']]['loc'] for f in aen),
                     'ok_closure': sum(1 for f in fs if f.get('ok_closure')), 'ok_closure_no_axiom': sum(1 for f in fs if f.get('ok_closure_no_axiom')),
                     'ok_ids': sorted(f['id'] for f in ok),
                     'as_is': (r.get('as_is') or {}).get('msg'), 'lean_lines': r.get('lean_lines'), 'lake': r.get('lake'),
                     'aeneas_errors': [x.get('errors') for x in r['rounds'] if x['stage'] == 'aeneas'],
                     'secs': {x['stage'] + str(x['round']): x['secs'] for x in r['rounds']}}
                if unfinished:
                    d['unfinished'] = True
                out['variants'].setdefault(mode, {}).setdefault(v, {})[c] = d
    json.dump(out, open(os.path.join(FORK, 'data', 'summary.json'), 'w'), indent=1)
    lines = []

    def table(mode, crates, title, total_label):
        V = [v for v in VARIANTS if v in out['variants'].get(mode, {})]
        lines.append('### ' + title + '\n')
        for key, unit in (('ok', 'functions'), ('ok_loc', 'code lines')):
            lines.append('| crate | %s counted | %s |' % (unit, ' | '.join(LABEL[v] for v in V)))
            lines.append('|:--|--:|%s' % ('--:|' * len(V)))
            tot = {v: 0 for v in V}
            den = 0
            for c in crates:
                n = out['census'][c]['fns' if key == 'ok' else 'loc']
                den += n
                row = []
                for v in V:
                    d = out['variants'][mode][v].get(c)
                    if d is None:
                        row.append('not run')
                        continue
                    if d.get('unfinished'):
                        row.append('did not finish')
                        continue
                    tot[v] += d[key]
                    row.append('%d (%.0f%%)' % (d[key], 100.0 * d[key] / n))
                lines.append('| %s | %d | %s |' % (c, n, ' | '.join(row)))
            if len(crates) > 1:
                lines.append('| **%s** | %d | %s |' % (total_label, den, ' | '.join('**%d (%.0f%%)**' % (tot[v], 100.0 * tot[v] / den) for v in V)))
            lines.append('')
    table('shipped', ORDER, 'As shipped (one Charon run, one Aeneas run, nothing removed): functions and code lines that end as compiling Lean', 'all ten')
    table('shipped', [c for c in ORDER if c != 'cedar-policy-core'], 'The same, nine crates without cedar', 'nine crates')
    if 'cw' in out['variants']:
        table('cw', ['cedar-policy-core'], 'cedar-policy-core with the Charon-side workarounds only (49 functions opaque for the rustc ICE, two generated parsers opaque), nothing removed on the Aeneas side', '')
    open(os.path.join(FORK, 'data', 'tables.md'), 'w').write('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
