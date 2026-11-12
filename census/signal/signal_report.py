#!/usr/bin/env python3
"""S1a result tables from work/runs/*/results/libsignal-protocol.json  ->  RESULT.md, result.json, functions.tsv.
Stage and cause-class definitions are the census's (scripts/report.py, imported unchanged); the items and the
criterion are read from frozen.json."""
import collections, glob, importlib.util, json, os, sys

SIG = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.dirname(SIG)
spec = importlib.util.spec_from_file_location('report', os.path.join(CENSUS, 'scripts', 'report.py'))
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
FROZEN = json.load(open(os.path.join(SIG, 'frozen.json')))
ROWS = [('p5-shipped', 'patched translator (p5), as shipped'), ('p5-cw', 'patched translator (p5), Charon-side workarounds'),
        ('pinned-shipped', 'unpatched release Aeneas, same LLBC (side row)'), ('pinned-cw', 'unpatched release Aeneas, Charon-side workarounds (side row)')]


def pct(a, b):
    return '%d (%.1f%%)' % (a, 100.0 * a / b) if b else '%d' % a


def load(row):
    p = os.path.join(SIG, 'work', 'runs', row, 'results', 'libsignal-protocol.json')
    if not os.path.exists(p):
        return None
    r = json.load(open(p))
    for f in r['functions']:
        for k, v in (('ok', False), ('ok_closure', False), ('ok_closure_no_axiom', False), ('dep_axioms', []), ('dep_local', [])):
            f.setdefault(k, v)
        f['stage'] = R.stage_of(f)
        f['classes'] = R.classes_of(f) if f['stage'] not in ('ok', 'absent') else []
    return r


def summarise(r):
    src = [f for f in r['functions'] if f['origin'] == 'source']
    comp = [f for f in src if f['stage'] != 'absent']
    st = collections.Counter(f['stage'] for f in src)
    d = {'source_fns': len(src), 'absent': st['absent'], 'counted': len(comp), 'counted_loc': sum(f['loc'] for f in comp),
         'stopped_charon': st['charon'], 'stopped_aeneas': st['aeneas'], 'stopped_lean': st['lean'], 'through': st['ok'],
         'through_loc': sum(f['loc'] for f in comp if f['stage'] == 'ok'),
         'closure_ok': sum(1 for f in comp if f['ok_closure']), 'no_axiom_beneath': sum(1 for f in comp if f['ok_closure_no_axiom']),
         'as_is': r.get('as_is'), 'lean_lines': r.get('lean_lines'), 'lake': r.get('lake'), 'axioms_in_file': len(r.get('axioms', [])),
         'rounds': [{k: x.get(k) for k in ('stage', 'round', 'rc', 'secs', 'fatal', 'errors', 'stuck', 'ices', 'n_marks') if k in x} for x in r['rounds']],
         'opaque_marks': len(r.get('opaque_marks', [])), 'surgery': len(r.get('surgery', [])), 'tools': r.get('tools'),
         'async_fns': sum(1 for f in comp if f.get('feat', {}).get('async')) if comp and isinstance(comp[0].get('feat'), dict) else None}
    d['share_no_axiom_counted'] = d['no_axiom_beneath'] / d['counted'] if d['counted'] else 0.0
    d['share_no_axiom_all_source'] = d['no_axiom_beneath'] / d['source_fns'] if d['source_fns'] else 0.0
    by = collections.defaultdict(list)
    for f in src:
        by[(f['file'], f['name'])].append(f)

    def item(file, name):
        fs = by.get((file, name), [])
        return [{'file': file, 'name': name, 'line': f['line_start'], 'stage': f['stage'], 'no_axiom_beneath': f['ok_closure_no_axiom'],
                 'decls': [(x['name'], x['body']) for x in f.get('decls', [])], 'classes': f['classes'],
                 'msgs': [m['stage'] + ': ' + m['msg'][:240] for m in f['msgs'][:4]]} for f in fs] or [{'file': file, 'name': name, 'stage': 'NOT FOUND IN INVENTORY'}]
    d['entry_points'] = [x for e in FROZEN['entry_points'] for x in item(e['file'], e['name'])]
    d['entry_point_helpers'] = [x for e in FROZEN['informational_only']['entry_point_helpers'] for x in item(*e.split(':'))]
    d['ratchet'] = [x for f in sorted(src, key=lambda f: (f['file'], f['line_start'])) if f['file'] in FROZEN['ratchet_files'] for x in item(f['file'], f['name']) if x.get('line') == f['line_start']]
    d['ratchet_keys'] = [x for f in sorted(src, key=lambda f: (f['file'], f['line_start'])) if f['file'] in FROZEN['informational_only']['files'] for x in item(f['file'], f['name']) if x.get('line') == f['line_start']]
    d['by_file'] = {}
    for f in comp:
        b = d['by_file'].setdefault(f['file'], collections.Counter())
        b['counted'] += 1
        b[f['stage']] += 1
        b['no_axiom'] += bool(f['ok_closure_no_axiom'])
    fail = [f for f in comp if f['stage'] != 'ok']
    d['classes'] = [{'class': c, 'title': R.CLASSES[c][0], 'primary': sum(1 for f in fail if f['classes'][0] == c), 'any': sum(1 for f in fail if c in f['classes'])}
                    for c in R.CLASSES if any(c in f['classes'] for f in fail)]
    d['classes'].sort(key=lambda x: -x['primary'])
    d['entry_points_translate'] = sum(1 for x in d['entry_points'] if x['stage'] == 'ok')
    d['not_a_route_a_target'] = bool(d['entry_points_translate'] == 0 and d['share_no_axiom_counted'] < FROZEN['criterion']['threshold'])
    return d, src


def main():
    out = {'frozen': FROZEN, 'rows': {}}
    md = ['# S1a result: libsignal-protocol v0.105.4 through the census', '',
          'Generated by `signal_report.py` from the per-function results of `./run.sh`. Do not edit; rerun. Definitions and the criterion are in `frozen.json`, the commands in `run.sh`, notes in `README.md`.', '']
    primary_src = None
    for row, title in ROWS:
        r = load(row)
        if r is None:
            continue
        d, src = summarise(r)
        out['rows'][row] = d
        if primary_src is None and row.startswith('p5'):
            primary_src = src
    if not out['rows']:
        raise SystemExit('no results under work/runs')
    md += ['## Where functions stop', '',
           '| row | source functions | not in Charon output | counted | stopped at Charon | stopped at Aeneas | stopped at Lean | through all three | compile with every local callee | no axiom beneath |', '|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|']
    for row, title in ROWS:
        d = out['rows'].get(row)
        if d:
            c = d['counted']
            md.append('| %s | %d | %d | %d | %s | %s | %s | %s | %s | **%s** |' % (title, d['source_fns'], d['absent'], c, pct(d['stopped_charon'], c), pct(d['stopped_aeneas'], c),
                                                                             pct(d['stopped_lean'], c), pct(d['through'], c), pct(d['closure_ok'], c), pct(d['no_axiom_beneath'], c)))
    md += ['', 'Percentages are of counted functions. "No axiom beneath" over all source functions: ' +
           '; '.join('%s %.1f%%' % (row, 100 * d['share_no_axiom_all_source']) for row, d in out['rows'].items()) + '.', '']
    for row, title in ROWS:
        d = out['rows'].get(row)
        if not d:
            continue
        md += ['## ' + title, '', '- Tool runs: ' + '; '.join('%s round %s: exit %s, %ss%s' % (x['stage'], x['round'], x['rc'], x['secs'], (', fatal: ' + str(x['fatal'])) if x.get('fatal') else '') for x in d['rounds']),
               '- As shipped: ' + (('**no output**: ' + d['as_is']['msg'][:400]) if d['as_is'] else 'Charon and Aeneas both produced output'),
               '- Generated Lean: %s lines, %s axioms in the file; lake: %s' % (d['lean_lines'], d['axioms_in_file'], d['lake']),
               '- Functions marked opaque for Charon: %d; declarations removed for Aeneas: %d' % (d['opaque_marks'], d['surgery']), '']
        for key, head in (('entry_points', 'The three entry points'), ('entry_point_helpers', 'Their helpers (informational)'), ('ratchet', 'Functions in `src/ratchet.rs`'), ('ratchet_keys', '`src/ratchet/keys.rs` (informational)')):
            md += ['### ' + head, '', '| function | line | stopped at | no axiom beneath | first message |', '|:--|--:|:--|:--|:--|']
            for x in d[key]:
                md.append('| `%s` `%s` | %s | %s | %s | %s |' % (x['file'], x['name'], x.get('line', ''), {'ok': 'through'}.get(x['stage'], x['stage']), {True: 'yes', False: 'no'}.get(x.get('no_axiom_beneath'), ''),
                                                             (x.get('msgs') or [''])[0].replace('|', '\\|').replace('\n', ' ')[:200]))
            md.append('')
        md += ['### By file', '', '| file | counted | Charon | Aeneas | Lean | through | no axiom beneath |', '|:--|--:|--:|--:|--:|--:|--:|']
        for f, b in sorted(d['by_file'].items()):
            md.append('| `%s` | %d | %d | %d | %d | %d | %d |' % (f, b['counted'], b['charon'], b['aeneas'], b['lean'], b['ok'], b['no_axiom']))
        md += ['', '### Failure causes (census classes; a function can have several, "primary" is the first)', '', '| class | primary | any |', '|:--|--:|--:|']
        for c in d['classes']:
            md.append('| %s | %d | %d |' % (c['title'], c['primary'], c['any']))
        md.append('')
    md += ['## Outcome against the frozen criterion', '', '> ' + FROZEN['criterion']['not_a_route_a_target_if'] + ' (threshold %.0f%%)' % (100 * FROZEN['criterion']['threshold']), '']
    p5 = [(row, d) for row, d in out['rows'].items() if row.startswith('p5')]
    for row, d in p5:
        md.append('- %s: entry points that translate: %d of %d; no axiom beneath: %.1f%% of counted functions (%d of %d). Criterion for "not a Route A target" %s.' % (
            row, d['entry_points_translate'], len(FROZEN['entry_points']), 100 * d['share_no_axiom_counted'], d['no_axiom_beneath'], d['counted'], 'MET' if d['not_a_route_a_target'] else 'NOT met'))
    verdict = bool(p5) and all(d['not_a_route_a_target'] for _, d in p5)
    out['outcome'] = 'not a Route A target' if verdict else 'criterion for "not a Route A target" not met'
    md += ['', '**Outcome: %s.**' % out['outcome'], '']
    open(os.path.join(SIG, 'RESULT.md'), 'w').write('\n'.join(md))
    json.dump(out, open(os.path.join(SIG, 'result.json'), 'w'), indent=1, sort_keys=True)
    if primary_src is not None:
        with open(os.path.join(SIG, 'functions.tsv'), 'w') as o:
            o.write('file\tline\tname\tkind\tloc\tstage\tcompiles_with_callees\tno_axiom_beneath\tclasses\tfirst_message\n')
            for f in sorted(primary_src, key=lambda f: (f['file'], f['line_start'])):
                o.write('\t'.join(str(x) for x in (f['file'], f['line_start'], f['name'], f['kind'], f['loc'], f['stage'], int(f['ok_closure']), int(f['ok_closure_no_axiom']), ','.join(f['classes']),
                                                   (f['msgs'][0]['stage'] + ': ' + f['msgs'][0]['msg'].replace('\t', ' ').replace('\n', ' ')[:200]) if f['msgs'] else '')) + '\n')
    print('\n'.join(md[4:8]))
    print(out['outcome'])


if __name__ == '__main__':
    main()
