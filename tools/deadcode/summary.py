#!/usr/bin/env python3
"""Cross-project table from the JSON written by deadcode.py.

  summary.py <project.json>[@RUN] [<project.json>[@RUN] ...] [--run name=RUN ...]   -> out/deadcode/COMPARE.md

One column per project, every figure read from out/deadcode/<name>/{analysis.json, graph_check.json,
runs/<run>/{result,verify,timing}.json, runs/control/result.json}.  `--run pfr=term` picks the safe-delete
run shown for a project (default: `term` if present, else `held`, else `dead`).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deadcode as dc  # noqa: E402


def load(p):
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    args = sys.argv[1:]
    runs = {}
    cfgs = []
    i = 0
    while i < len(args):
        if args[i] == '--run':
            k, v = args[i + 1].split('=')
            runs[k] = v
            i += 2
        else:
            cfgs.append(args[i])
            i += 1
    cols = []
    for c in cfgs:
        want = None
        if '@' in c:                      # projects/ns.json@term : a second column for another run
            c, want = c.split('@')
        P = dc.Project(c)
        A = load(os.path.join(P.out, 'analysis.json'))
        AN = load(os.path.join(P.out, 'analysis_noscope.json'))
        G = load(os.path.join(P.out, 'graph_check.json'))
        CT = load(os.path.join(P.out, 'runs', 'control', 'result.json'))
        run = want or runs.get(P.name)
        if not run:
            for cand in ('term', 'held', 'dead'):
                if os.path.exists(os.path.join(P.out, 'runs', cand, 'result.json')):
                    run = cand
                    break
        rd = os.path.join(P.out, 'runs', run) if run else None
        R = load(os.path.join(rd, 'result.json')) if rd else None
        V = load(os.path.join(rd, 'verify.json')) if rd else None
        T = load(os.path.join(rd, 'timing.json')) if rd else None
        cols.append(dict(P=P, A=A, AN=AN, G=G, CT=CT, R=R, V=V, T=T, run=run))
    f = lambda x: format(x, ',')
    pc = dc.pct
    rows = []

    def row(label, fn):
        out = []
        for c in cols:
            try:
                out.append(str(fn(c)))
            except (KeyError, TypeError, ZeroDivisionError):
                out.append('—')
        rows.append('| %s | %s |' % (label, ' | '.join(out)))

    def other_targets(c):
        R = c['R']
        ot = R.get('otherTargets') or R.get('defaultTargets') or load(os.path.join(c['P'].out, 'runs', c['run'], 'other_targets.json'))
        if not ot:
            return 'not built'
        how = 'in the loop' if R.get('buildAll') else 'built once on the final state'
        return ('build (%s)' % how) if ot['exit'] == 0 else 'DO NOT BUILD'

    row('Lean', lambda c: c['A']['lean'])
    row('roots', lambda c: '%s (%s)' % (f(c['A']['roots']['roots']), c['A']['roots']['how'].split(' (')[0].split(' of the')[0][:60]))
    row('modules', lambda c: f(c['A']['modules']))
    row('source lines', lambda c: f(c['A']['sourceLines']))
    row('declarations', lambda c: f(c['A']['declarations']))
    row('… declarations missing from the export (name declared twice, Lean kept one)', lambda c: f(c['A']['nameClashes']['sourceLevelDeclarationsMissingFromExport']))
    row('reachable from a root (term graph)', lambda c: f(c['A']['reachable']))
    row('term graph = kernel closure', lambda c: 'yes' if c['G']['sound'] and not c['G']['graphReachableNotInKernelClosure'] else 'NO')
    row('**unreachable declarations**', lambda c: '**%s (%s%%)**' % (f(c['A']['unreachable']), c['A']['unreachablePct']))
    row('… lines of unreachable declarations', lambda c: '%s (%s%% of all lines)' % (f(c['A']['declLinesUnreachable']), pc(c['A']['declLinesUnreachable'], c['A']['sourceLines'])))
    row('… unreachable theorems', lambda c: '%s of %s (%s%%)' % (f(c['A']['byKind']['theorem']['unreachable']), f(c['A']['byKind']['theorem']['all']),
                                                               pc(c['A']['byKind']['theorem']['unreachable'], c['A']['byKind']['theorem']['all'])))
    for k, lab in (('1-dead', 'class 1 (no other use found)'), ('2-named', 'class 2, named in kept source (not in its term)'),
                   ('2-command', 'class 2, held by a command / shared source'), ('2-attribute', 'class 2, in an elaboration table in scope')):
        row(lab, lambda c, k=k: '%s (%s%% of unreachable)' % (f(c['A']['classes'][k]['declarations']), pc(c['A']['classes'][k]['declarations'], c['A']['unreachable'])))
    row('class 1 without the scope rule', lambda c: f(c['AN']['classes']['1-dead']['declarations']))
    row('class 3: wholly unreachable modules', lambda c: '%s (%s declarations, %s lines)' % (
        f(c['A']['modulesSummary']['whollyUnreachable']), f(c['A']['modulesSummary']['whollyUnreachableDecls']), f(c['A']['modulesSummary']['whollyUnreachableLines'])))
    row('class 4: near-identical module pairs', lambda c: '%s (%s declarations in the less-used modules)' % (
        c['A']['clones']['near-identical']['pairs'], f(c['A']['clones']['near-identical']['cloneDecls'])))
    row('class 4: same-statement module pairs', lambda c: c['A']['clones']['same-statements']['pairs'])
    row('unreachable with a needed twin statement', lambda c: f(c['A']['shape']['withNeededTwin']))
    row('unreachable used by nothing at all', lambda c: '%s (%s%%)' % (f(c['A']['shape']['tops']), pc(c['A']['shape']['tops'], c['A']['unreachable'])))
    row('negative control: used declarations whose deletion broke the build', lambda c: dc.fmt_rate(sum(1 for r in c['CT'] if r['failed']), len(c['CT'])))
    row('safe-delete run shown', lambda c: '`%s`' % c['run'])
    row('… planned / could not be cut', lambda c: '%s / %s' % (f(c['R']['planned']), f(c['R']['notSeparable'])))
    row('… deleted with the roots building', lambda c: '%s (%s%% of declarations)' % (f(c['R']['deleted']), pc(c['R']['deleted'], c['A']['declarations'])))
    row('… hidden dependencies (restored)', lambda c: dc.fmt_rate(c['R']['hiddenRate']['k'], c['R']['hiddenRate']['n']))
    row('… restored only as dependency of a hidden one', lambda c: f(c['R']['restoredAsDependencyOfHidden']))
    row('… other build targets (default targets, comparator files)', other_targets)
    row('… restored because another build target uses them / as dependency of those', lambda c: ('%s / %s' % (
        f(c['R']['numNeededByOtherTargets']), f(len(c['R']['restoredAsDependencyOfOtherTargets'])))) if c['R'].get('buildAll') else 'not tried')
    for k in ('1-dead', '2-attribute', '2-named', '2-command'):
        row('… hidden in class %s' % k, lambda c, k=k: '%s of %s' % (c['R']['byClass'][k]['hidden'], f(c['R']['byClass'][k]['deleted'])))
    row('… axioms of the roots unchanged', lambda c: ('yes, %d roots' % c['R']['axioms']['roots']) if c['R']['axioms']['identical'] else 'NO')
    row('… files after', lambda c: '%s (−%s)' % (f(c['R']['sizes']['after']['files']), f(c['R']['sizes']['before']['files'] - c['R']['sizes']['after']['files'])))
    row('… lines after', lambda c: '%s (−%s%%)' % (f(c['R']['sizes']['after']['lines']), pc(c['R']['sizes']['before']['lines'] - c['R']['sizes']['after']['lines'], c['R']['sizes']['before']['lines'])))
    row('… lines in the import closure of the roots, before → after', lambda c: (lambda cl: '%s → %s (−%s%%)' % (
        f(cl['linesBefore']), f(cl['linesAfter']), pc(cl['linesBefore'] - cl['linesAfter'], cl['linesBefore'])))(dc.run_closure_lines(c['P'], c['run'], c['R'])))
    row('… declarations after', lambda c: '%s (−%s%%)' % (f(c['R']['sizes']['after']['declarations']), pc(c['R']['deleted'], c['R']['sizes']['before']['declarations'])))
    row('… re-export of the trimmed build matches the prediction', lambda c: 'yes' if (c['V']['namesEqual'] and not c['V']['declarationsWithDifferentTermDependencies'])
        else ('yes, up to %d renumbered anonymous instances' % len(c['V']['onlyPredicted']) if c['V'].get('namesEqualUpToInstanceNumbering') and not c['V'].get('declarationsWithDifferentTermDependenciesUpToInstanceNumbering') else 'NO'))
    row('clean build, original copy (wall s / module-s)', lambda c: '%s / %s' % (f(round(c['T']['original']['seconds'])), f(round(c['T']['original']['sumModuleSeconds']))))
    row('clean build, trimmed copy (wall s / module-s)', lambda c: '%s / %s (%+.1f%% module-s)' % (
        f(round(c['T']['trimmed']['seconds'])), f(round(c['T']['trimmed']['sumModuleSeconds'])),
        100.0 * (c['T']['trimmed']['sumModuleSeconds'] - c['T']['original']['sumModuleSeconds']) / c['T']['original']['sumModuleSeconds']))
    row('… load average at the start and end of those builds', lambda c: '%.0f to %.0f' % (c['T']['loadBefore'][0], c['T']['loadAfter'][0]))
    out = ['| | ' + ' | '.join('%s (`%s`)' % (c['P'].name, c['run']) for c in cols) + ' |', '|---|' + '---|' * len(cols)] + rows
    dst = os.path.join(dc.REPO, 'out', 'deadcode', 'COMPARE.md')
    open(dst, 'w').write('# Dead-code tool: projects side by side\n\nGenerated by `tools/deadcode/summary.py`; every figure is read from the JSON files under `out/deadcode/<project>/`.\n\n' + '\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
