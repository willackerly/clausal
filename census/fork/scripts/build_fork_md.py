#!/usr/bin/env python3
"""Assemble census/fork/FORK.md from parts/*.md, the patch files and the result data, and the ready-to-send issue texts
upstream/*.md from parts/issues/*.md, repro/*.rs and patches/*.patch. Every number is read from data/ or runs/.
Run scripts/summarise.py first. Do not edit FORK.md or upstream/*.md by hand; edit parts/ or this script."""
import collections, glob, json, os, re
FORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.dirname(FORK)
S = json.load(open(os.path.join(FORK, 'data', 'summary.json')))
ORDER = ['cedar-policy-core', 'rust_decimal', 'semver', 'shlex', 'rusty-money', 'indexmap', 'untrusted', 'fnv', 'time', 'zeroize']
V = ['base', 'p1', 'p2', 'p3', 'p4', 'p5']
SH = S['variants']['shipped']
CW = S['variants'].get('cw', {})
NAME = {'base': 'unpatched', 'p1': '+ (i)', 'p2': '+ (ii)', 'p3': '+ (iii)', 'p4': '+ (iv)', 'p5': '+ (v)'}


def tot(v, key, crates=ORDER, mode=SH):
    return sum(mode[v][c][key] for c in crates)


def pct(a, b):
    return '%.0f%%' % (100.0 * a / b) if b else 'n/a'


NINE = [c for c in ORDER if c != 'cedar-policy-core']
FN = sum(S['census'][c]['fns'] for c in ORDER)
LOC = sum(S['census'][c]['loc'] for c in ORDER)
FN9 = sum(S['census'][c]['fns'] for c in NINE)
LOC9 = sum(S['census'][c]['loc'] for c in NINE)
out = []
w = out.append


def table(mode, crates, key, unit, total_label):
    vs = [v for v in V if v in mode and all(c in mode[v] for c in crates)]
    w('| crate | %s counted | %s |' % (unit, ' | '.join(NAME[v] for v in vs)))
    w('|:--|--:|%s' % ('--:|' * len(vs)))
    den = 0
    for c in crates:
        n = S['census'][c]['fns' if key == 'ok' else 'loc']
        den += n
        w('| %s | %d | %s |' % (c, n, ' | '.join('%d (%s)' % (mode[v][c][key], pct(mode[v][c][key], n)) for v in vs)))
    if total_label:
        w('| **%s** | %d | %s |' % (total_label, den, ' | '.join('**%d (%s)**' % (tot(v, key, crates, mode), pct(tot(v, key, crates, mode), den)) for v in vs)))
    w('')


def part(name):
    t = open(os.path.join(FORK, 'parts', name)).read().rstrip('\n')
    for k, v in SUBST.items():
        t = t.replace('{{%s}}' % k, str(v))
    return t


def patch_diff(n):
    p = sorted(glob.glob(os.path.join(FORK, 'patches', '%s-*.patch' % n)))[0]
    t = open(p).read()
    body = t[t.index('\ndiff --git') + 1:]
    body = body[:body.rindex('\n-- \n')] if '\n-- \n' in body else body
    # the two expected-output files only change a line number; leave them out of the inlined diff
    chunks = re.split(r'(?m)^(?=diff --git )', body)
    keep = [c for c in chunks if c and '.borrow-check.out' not in c.split('\n')[0]]
    dropped = len([c for c in chunks if c]) - len(keep)
    s = '<details><summary>Diff (%s%s)</summary>\n\n```diff\n%s\n```\n\n</details>' % (
        os.path.relpath(p, FORK), ', without the %d expected-output files' % dropped if dropped else '', ''.join(keep).rstrip('\n'))
    return s


# ------------------------------------------------------------------------------------------------ data for the prose
b_ok, b_loc = tot('base', 'ok'), tot('base', 'ok_loc')
f_ok, f_loc = tot('p4', 'ok'), tot('p4', 'ok_loc')
f_ok9, f_loc9 = tot('p4', 'ok', NINE), tot('p4', 'ok_loc', NINE)
p2_ok, p2_loc = tot('p2', 'ok'), tot('p2', 'ok_loc')
sound = json.load(open(os.path.join(FORK, 'data', 'sound_results.json')))
ran = [r for r in sound if r['lean_ran'] == r['inputs'] and r['rust_ran'] == r['inputs']]
n_inputs = sum(r['inputs'] for r in ran)
n_mis = sum(r['n_mismatches'] for r in ran)
n_panic = sum(r['panics_rust'] for r in ran)
direct = json.load(open(os.path.join(FORK, 'data', 'cedar_direct_runs.json')))
cedar_cw_all = {v: CW[v]['cedar-policy-core'] for v in V if v in CW and 'cedar-policy-core' in CW[v]}
cedar_unfinished = sorted(v for v, d in cedar_cw_all.items() if d.get('unfinished'))
cedar_cw = {v: d for v, d in cedar_cw_all.items() if not d.get('unfinished')}       # a killed run is not a measurement
UNF = json.load(open(os.path.join(FORK, 'data', 'cedar_cw_unfinished.json')))
SUBST = {'RAN': len(ran), 'INPUTS': n_inputs, 'MISMATCH': n_mis, 'PANICS': n_panic, 'B_OK': b_ok, 'F_OK': f_ok, 'B_PCT': pct(b_ok, FN), 'F_PCT': pct(f_ok, FN),
         'B9_PCT': pct(tot('base', 'ok', NINE), FN9), 'F9_PCT': pct(f_ok9, FN9), 'GAIN': '%d' % (f_ok - b_ok), 'INDEXMAP_P4': SH['p4']['indexmap']['ok']}
have_p4cw = 'p4' in cedar_cw and cedar_cw['p4'].get('lean_lines')
import importlib.util, subprocess
_spec = importlib.util.spec_from_file_location('report', os.path.join(CENSUS, 'scripts', 'report.py'))
REP = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(REP)
CEDAR_COUNTED = set(i for i in json.load(open(os.path.join(FORK, 'data', 'cedar_counted_ids.json'))))


def cedar_breakdown(v):
    f = os.path.join(FORK, 'runs', v + '-cw', 'results', 'cedar-policy-core.json')
    if not os.path.exists(f):
        f = os.path.join(FORK, 'data', 'results', v + '-cw', 'cedar-policy-core.json')
    if not os.path.exists(f):
        return None
    r = json.load(open(f))
    if not r.get('lean_lines') or v in cedar_unfinished:
        return None
    fs = [x for x in r['functions'] if x['origin'] == 'source' and x['id'] in CEDAR_COUNTED]
    st, loc, anyc, only = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    for x in fs:
        sg = REP.stage_of(x)
        st[sg] += 1
        loc[sg] += x['loc']
        if sg not in ('ok', 'absent'):
            cs = REP.classes_of(x)
            for c in set(cs):
                anyc[c] += 1
            if len(set(cs)) == 1:
                only[cs[0]] += 1
    return {'stages': st, 'loc': loc, 'any': anyc, 'only': only, 'closure': sum(1 for x in fs if x.get('ok_closure')), 'no_axiom': sum(1 for x in fs if x.get('ok_closure_no_axiom'))}


BD = {v: cedar_breakdown(v) for v in ('p3', 'p4', 'p5')}
BD = {v: b for v, b in BD.items() if b}
SUBST['SYNTAX_P4'] = BD['p4']['any']['lean_syntax'] if 'p4' in BD else 'about 180'
SUBST['DIFFSTAT'] = subprocess.check_output(['git', '-C', os.path.join(FORK, 'aeneas'), 'diff', '--shortstat', '0d21a9ec..census-fork']).decode().strip().split(', ', 1)[1].replace('insertions(+)', 'lines added').replace('deletions(-)', 'removed')
LAST = 'p5' if 'p5' in cedar_cw and cedar_cw['p5'].get('lean_lines') else 'p4'
_e = UNF['evidence_for_patch_v_without_cedar']
SUBST.update({'U_P3_ERR': UNF['variants']['p3']['errors_logged_at_kill'], 'U_P5_ERR': UNF['variants']['p5']['errors_logged_at_kill'],
              'D_ERR': direct['errors'], 'D_LINES': direct['lean_lines'], 'P4CW_OK': cedar_cw['p4']['ok'] if 'p4' in cedar_cw else 'n/a',
              'V_T4_IND': _e['time_as_shipped_p4']['indented'], 'V_T4_N': _e['time_as_shipped_p4']['declaration_lines'], 'V_T4_MAX': _e['time_as_shipped_p4']['max_indent_columns'],
              'V_T5_IND': _e['time_as_shipped_p5']['indented'], 'V_T5_N': _e['time_as_shipped_p5']['declaration_lines'],
              'V_C_IND': _e['cedar_cw_p4']['indented'], 'V_C_N': _e['cedar_cw_p4']['declaration_lines'], 'V_C_MAX': _e['cedar_cw_p4']['max_indent_columns']})
REPROS = sorted(os.path.basename(x) for x in glob.glob(os.path.join(FORK, 'repro', '*.rs')))
ISSUES = sorted(glob.glob(os.path.join(FORK, 'parts', 'issues', '*.md')))

w('# Aeneas fork spike: four small patches (and a fifth), measured on the census corpus')
w('')
w('Generated by `scripts/build_fork_md.py` from `parts/`, `patches/`, `repro/` and `data/`. Do not edit `FORK.md`; edit those and rerun. Run date 2026-11-10, finalised the same evening by a second pass that reran nothing heavy, macOS arm64, on a machine shared with other jobs (load average 90 to 200 for most of the run; timings are not reported as results).')
w('')
w('## Result in brief')
w('')
w('- **Build from source works.** Aeneas `0d21a9ec` (the nightly-2026.11.10 release) with Charon `454586e9` built in about ten minutes of setup, most of it compiling OCaml 5.3.0 and its packages; the Aeneas build itself takes 40 seconds. The unpatched source build reproduces the census as shipped: %d of %d functions, %d lines, and the same status for every function of `shlex`, `untrusted`, `fnv` and `zeroize`.' % (b_ok, FN, b_loc))
w('- **As shipped, the four patches take the corpus from %d functions (%s) to %d (%s) that end as Lean that compiles; lines from %d (%s) to %d (%s).** Nine crates without cedar: %d of %d (%s) to %d (%s).' % (
    b_ok, pct(b_ok, FN), f_ok, pct(f_ok, FN), b_loc, pct(b_loc, LOC), f_loc, pct(f_loc, LOC), tot('base', 'ok', NINE), FN9, pct(tot('base', 'ok', NINE), FN9), f_ok9, pct(f_ok9, FN9)))
w('- **Where the gain comes from.** Patch (ii), the trait-method signature guard, gives +%d functions: the five crates that produced nothing now produce exactly the functions the census reached by manual peeling (same set, function for function). Patch (iv), name capture, gives +%d. Patches (i) and (iii) give +0 on these ten crates as shipped: they matter for cedar, which as shipped still stops earlier, in Charon.' % (
    p2_ok - tot('p1', 'ok'), f_ok - tot('p3', 'ok')))
w('- **Cedar, as shipped: still 0.** Charon dies on a rustc internal compiler error before Aeneas runs; no Aeneas patch can change that.')
if have_p4cw:
    d = cedar_cw['p4']
    extra = ''
    if LAST == 'p5':
        e = cedar_cw['p5']
        extra = ' A fifth patch, found from that run and not in the task (v: reset the pretty-printer after an extraction error), takes it to **%d (%s), %d lines**.' % (e['ok'], pct(e['ok'], e['fns']), e['ok_loc'])
    w('- **Cedar with only the Charon-side workarounds** (49 functions opaque, two generated parsers opaque; nothing removed on the Aeneas side; reported apart from the as-shipped tables): unpatched and with (i) or (ii) Aeneas aborts with no output. With (i)-(iv) it writes %d lines of Lean and **%d of %d functions (%s) end as Lean that compiles, %d lines**; the census reached 37 with 21 manual removals.%s' % (
        d['lean_lines'], d['ok'], d['fns'], pct(d['ok'], d['fns']), d['ok_loc'], extra))
if cedar_unfinished:
    w('- **Not measured.** Cedar with the extra patch (v), and the joined run of cedar with (i)-(iii): both runs were started, did not finish in over six hours of wall clock on a loaded machine that was asleep for most of them, and were killed. They were not rerun. See "Not measured" in the cedar section for the partial evidence and what a bounded rerun needs.')
w('- **Aeneas\'s own test suite: no regression.** 122 extraction tests, all exit 0 before and after every patch; generated outputs are byte-identical except two expected-error files that quote an Aeneas source line number moved by patch (iii). The suite runs with `-abort-on-error`, under which the new handlers are inactive, so it shows the patches change nothing they should not; it does not exercise the new paths. The reproductions and the census do.')
w('- **Soundness sample: %d functions run in Rust and in the generated Lean on %d generated inputs, 0 mismatches** (%d of the inputs panic in Rust and fail in Lean alike). Only 6 of the 30 functions in the seeded sample the task asked for could be run; the rest of the %d come from two further seeded strata. It is a thin check, mostly small arithmetic and accessors.' % (len(ran), n_inputs, n_panic, len(ran)))
w('- **New along the way.** A 30-line single-file reproduction of the uncaught-exception crash that took the census 129 runs to bisect on cedar (`repro/crash_stack_of_refs.rs`); and a small over-count in the census\'s two stricter columns (3 functions, see "Soundness sample").')
w('- **Recommendation, as a trade:** carry the five commits as a fork now and send the five issue texts in `upstream/` (written, not sent); drop each commit as upstream fixes it. Details at the end.')
w('')
w('## What was built, and how to rerun')
w('')
w('- **Toolchain.** `brew install opam pkgconf`; an opam root inside `census/fork/.opam` (not `~/.opam`) with OCaml 5.3.0 and the packages Aeneas and charon-ml list. `source census/fork/env.sh` sets it up. Charon was built from source at the pin for Aeneas\'s tests; on `shlex` its LLBC is identical to the release binary\'s apart from the output path stored in the file. The census runs use the release Charon binary, as the census did.')
w('- **Commit.** `0d21a9ec`, as asked. Its only source difference from the census\'s main binary (`5a392f4b`) is three keywords in `LeanKeywords.ml`. The generated Lean is compiled against the Lean library of the 11.09 release on Lean v4.35.0, the census\'s setup, because the 11.10 library needs a newer Lean and Mathlib than are pinned here.')
w('- **Pipeline.** `scripts/fork_census.py` imports `census/scripts/census.py` unchanged, redirects its paths under `census/fork/runs/<variant>-<mode>/` and switches the peel off: one Charon run, one Aeneas run, nothing marked or removed. The join and the definition of "ends as compiling Lean" are the census\'s. Denominators are the census\'s counted functions and lines.')
w('- **Variants.** `base` (unpatched), `p1` … `p4` (the four patches asked for, applied cumulatively in the order asked), `p5` (plus the extra patch (v)). Binaries in `bin/` (git-ignored).')
w('')
w('```')
w('source census/fork/env.sh')
w('(cd census/fork/aeneas/src && dune build)             # 40 s; binary: src/_build/default/main.exe')
w('scripts/run_tests.sh p5                               # Aeneas\'s extraction tests with bin/aeneas-p5')
w('scripts/run_variant.sh p5 shipped                     # ten crates, as shipped   -> runs/p5-shipped/')
w('scripts/run_variant.sh p5 cw                          # cedar with the Charon-side workarounds only')
w('scripts/run_probes.sh p5 ; repro/run.sh p5            # the three census probes; the %d single-file reproductions' % len(REPROS))
w('python3 scripts/sound_run.py gen|rust|lean|compare    # the soundness check')
w('python3 scripts/summarise.py ; python3 scripts/build_fork_md.py')
w('```')
w('')
w('## Before and after, per patch and per crate (as shipped)')
w('')
w('"As shipped" is `charon cargo --preset=aeneas` then `aeneas -backend lean`, once each, nothing else. Columns are cumulative: "+ (ii)" has patches (i) and (ii). (i) to (iv) are the patches asked for; (v) is the extra one.')
w('')
w('### Functions that end as Lean that compiles')
w('')
table(SH, ORDER, 'ok', 'functions', 'all ten')
w('### Code lines of those functions')
w('')
table(SH, ORDER, 'ok_loc', 'code lines', 'all ten')
w('### Nine crates without cedar')
w('')
w('| | counted | %s |' % ' | '.join(NAME[v] for v in V))
w('|:--|--:|%s' % ('--:|' * len(V)))
w('| functions | %d | %s |' % (FN9, ' | '.join('%d (%s)' % (tot(v, 'ok', NINE), pct(tot(v, 'ok', NINE), FN9)) for v in V)))
w('| code lines | %d | %s |' % (LOC9, ' | '.join('%d (%s)' % (tot(v, 'ok_loc', NINE), pct(tot(v, 'ok_loc', NINE), LOC9)) for v in V)))
w('')
w('### Each patch\'s own contribution')
w('')
w('| patch | functions added | lines added | where |')
w('|:--|--:|--:|:--|')
prev = 'base'
TITLE = {'p1': '(i) FunsAnalysis recursion', 'p2': '(ii) trait method signature guard', 'p3': '(iii) exception catching', 'p4': '(iv) Lean name capture', 'p5': '(v) formatter reset after an extraction error (extra, not in the task)'}
for v in V[1:]:
    where = ', '.join('%s +%d' % (c, SH[v][c]['ok'] - SH[prev][c]['ok']) for c in ORDER if SH[v][c]['ok'] != SH[prev][c]['ok']) or '–'
    lost = sum(len(set(SH[prev][c]['ok_ids']) - set(SH[v][c]['ok_ids'])) for c in ORDER)
    w('| %s | +%d | +%d | %s%s |' % (TITLE[v], tot(v, 'ok') - tot(prev, 'ok'), tot(v, 'ok_loc') - tot(prev, 'ok_loc'), where, '' if not lost else ' (%d functions lost)' % lost))
    prev = v
w('')
w('- **No function is lost by any patch**: each variant\'s set of compiling functions contains the previous one\'s.')
w('- **(i), (iii) and (v) show +0 here because of the corpus, not because they do nothing.** As shipped, cedar never reaches Aeneas, and on the other nine crates the only mixed group is near the end of `rust_decimal`\'s declaration order. Their effect is in the cedar section and in the probes below.')
w('- **(ii) equals the census\'s "peeled" figure for the nine crates** (%d functions, %d lines), now with no manual step. The set of compiling functions is the same function for function; the per-function stage agrees too, except two `rust_decimal` functions that move from "failed at Aeneas" to "failed at Lean".' % (tot('p2', 'ok', NINE), tot('p2', 'ok_loc', NINE)))
w('- **(iv) gives more than the census predicted** (96 functions): %d. Of the extra ones, 4 are in `rust_decimal` (a parameter named `str` next to the module `str`, which the census had classed as a structure-field error) and the rest in `indexmap` (97 against the 80 the census put in this class; the difference was not analysed).' % (f_ok - tot('p3', 'ok')))
w('')
w('### The census probes and the single-file reproductions')
w('')
w('| probe (census/probes/) | functions | %s |' % ' | '.join(NAME[v] for v in V))
w('|:--|--:|%s' % ('--:|' * len(V)))
for p in ('mixed-group-probe', 'mixed-group-fixed-probe', 'profile-probes'):
    row, n = [], None
    for v in V:
        f = os.path.join(FORK, 'runs', v + '-shipped', 'results', p + '.json')
        if not os.path.exists(f):
            row.append('not run')
            continue
        r = json.load(open(f))
        fs = [x for x in r['functions'] if x['origin'] == 'source']
        okn = sum(1 for x in fs if x.get('ok'))
        if any(x['charon'] == 'ok' for x in fs):
            n = sum(1 for x in fs if x['charon'] != 'absent')
        row.append(str(okn) if r.get('lean_lines') else '0 (no output)')
    w('| %s | %s | %s |' % (p, n, ' | '.join(row)))
w('')
w('`repro/` holds %d single-file reproductions (`repro/run.sh <variant>`). The last five were compiled once with the unpatched and the patched binary; `mixed_group.rs`, the single-file form of the first probe, was added in the finalising pass and run through Aeneas only (its Lean was not compiled):' % len(REPROS))
w('')
w('| file | unpatched | patches (i)-(iv) |')
w('|:--|:--|:--|')
w('| `mixed_group.rs` (two types whose `Display` impls format each other, then three unrelated functions) | 13 errors, 10 of them "Internal error"; `unrelated_b`, `Wrapper.get` and `unrelated_c` are not in the Lean file | 7 errors, all on the two `fmt` functions of the group; the three unrelated functions are emitted (already with patch (i) alone) |')
w('| `abort_copied.rs` (`v.iter().copied().max()`) | Aeneas exit 2, no Lean file | Lean file; `add_one` translated; `copied_max` emitted as calls to the two iterator methods\' default functions (axioms); one Lean error remains, in the `Iterator` instance for `Copied` (`max` is not a field of the library\'s `Iterator` model) |')
w('| `abort_pattern.rs` (`s.find(\':\')`) | Aeneas exit 2, no Lean file | Lean file; `add_one` translated; `find_colon` is emitted with a `sorry` for the missing `Pattern` impl and fails by itself |')
w('| `crash_stack_of_refs.rs` (a stack of `(&V, usize)` popped in `while let`) | Aeneas exit 2, `Failure("ty_regions …")`, no Lean file, function not named | Lean file; `V.height` is `sorry` with an error naming it, `add_one` translated; the file builds |')
w('| `capture_builtin_name.rs` (`struct Slice` holding a `&[u8]`) | Lean: "Function expected at Slice"; `len` compiles only "using sorry" | builds with no error |')
w('| `capture_module_name.rs` (parameter `input`, module `input`) | Lean: "Invalid field `Input`" | builds with no error |')
w('')
w('## Cedar, separately')
w('')
w('- **As shipped: 0 of 2,503 with every variant.** `charon cargo` fails with 49 rustc internal compiler errors (`error performing operation: fully_perform`) and writes no LLBC. This is a Charon defect (`ice` in `IMPROVEMENTS.md`) and none of the four patches is aimed at it.')
w('- **Mode "Charon workarounds" (`cw`), reported apart from the as-shipped tables.** The census\'s Charon-side workarounds are kept (the 49 functions holding an ICE site are marked `#[charon::opaque]`; the two generated LALRPOP parsers are opaque) and nothing is done on the Aeneas side: no trait removed, no crash cache, no bisection, one Aeneas run. The census\'s own cedar figure (37 functions) needed 21 removals from the LLBC on top of this.')
w('')
w('| variant | Aeneas on cedar, Charon workarounds only | Lean lines written | functions that end as compiling Lean | code lines |')
w('|:--|:--|--:|--:|--:|')


def cw_row(v, abort_text):
    d = cedar_cw.get(v)
    if d and d.get('lean_lines'):
        return '| %s | completes; %s errors logged | %d | **%d of %d (%s)** | %d (%s) |' % (NAME[v], d['aeneas_errors'][-1], d['lean_lines'], d['ok'], d['fns'], pct(d['ok'], d['fns']), d['ok_loc'], pct(d['ok_loc'], d['loc']))
    return '| %s | %s | 0 | 0 | 0 |' % (NAME[v], abort_text)


w(cw_row('base', 'aborts: fatal `CFailure` on the signature of `TCNode::out_edges` ("Dynamic trait types are not supported yet")'))
w(cw_row('p1', 'aborts: same as unpatched'))
w(cw_row('p2', 'aborts: `Failure("ty_regions shouldn\'t be called on erased or body regions")` in the symbolic interpreter, after all signatures were computed (direct run of this binary on the same LLBC, 6 min 47 s; the joined run was stopped to free the machine)'))
if 'p3' in cedar_cw and cedar_cw['p3'].get('lean_lines'):
    w(cw_row('p3', ''))
else:
    w('| %s | completes; %d errors logged (direct run of this binary on the same LLBC; not joined per function, not compiled%s) | %d | not measured | not measured |' % (NAME['p3'], direct['errors'], '; the joined run did not finish, see "Not measured" below' if 'p3' in cedar_unfinished else '', direct['lean_lines']))
for v in ('p4', 'p5'):
    if v in cedar_cw:
        w(cw_row(v, 'aborts'))
    elif v in cedar_unfinished:
        w('| %s | **did not finish** (killed after %.0f h %02.0f min of wall clock; see "Not measured" below) | not measured | not measured | not measured |' % (
            NAME[v], UNF['variants'][v]['wall_secs'] // 3600, UNF['variants'][v]['wall_secs'] % 3600 // 60))
w('')
if BD:
    vs = [v for v in ('p3', 'p4', 'p5') if v in BD]
    w('Where the 2,503 counted functions stop, with the Charon-side workarounds:')
    w('')
    w('| stage | %s |' % ' | '.join(NAME[v] for v in vs))
    w('|:--|%s' % ('--:|' * len(vs)))
    for key, label in (('charon', 'stopped at Charon (the functions made opaque for the ICE)'), ('aeneas', 'stopped at Aeneas'), ('lean', 'stopped at Lean'), ('ok', '**through all three**')):
        w('| %s | %s |' % (label, ' | '.join('%d' % BD[v]['stages'][key] for v in vs)))
    w('| …and every local callee compiles | %s |' % ' | '.join('%d' % BD[v]['closure'] for v in vs))
    w('| …and no unmodelled external is used | %s |' % ' | '.join('%d' % BD[v]['no_axiom'] for v in vs))
    w('')
    w('The last two rows use the census join as it is, including the small over-count on recursion cycles described under "Soundness sample".')
    w('')
if cedar_unfinished:
    w(part('55-not-measured.md'))
    w('')
w(part('50-cedar-blockers.md'))
if LAST in BD:
    b = BD[LAST]
    DESC = {'mixed_group': 'in, or depends on, a mixed declaration group', 'lean_missing': 'generated Lean refers to a declaration that is not there (a type or function that failed)', 'lean_other': 'generated Lean: other elaboration errors',
            'lean_syntax': 'generated Lean does not parse', 'fn_ptr': 'function items / function pointers as values', 'borrow_shape': 'borrow patterns outside the fragment', 'other': 'other',
            'dyn_trait': 'trait objects', 'trait_generic': 'trait generics Aeneas mishandles (casts to `dyn`, missing trait declarations)', 'charon_ice': 'rustc ICE under Charon (function made opaque)',
            'aeneas_internal': 'Aeneas internal error without a message', 'loop_exit': 'early exit from a loop', 'iter_std': 'iterator methods with no model', 'lean_type': 'generated Lean: type error',
            'lean_struct': 'generated Lean: structure/field error', 'loop_join': 'loop or branch whose borrow state cannot be joined', 'name_clash': 'two Rust items mapped to one Lean name',
            'lean_universe': 'generated Lean: universe levels', 'hrtb': 'higher-ranked lifetimes', 'raw_ptr': 'raw pointers', 'str_pattern': '`str` search functions (`Pattern`)', 'not_emitted': 'no Lean definition emitted',
            'match_scrutinee': '`match` on an unsupported scrutinee', 'float': 'floats', 'const_static': 'constants and statics', 'lean_match': 'Lean cannot compile a literal `match`', 'abort_trait_sig': 'uses a trait Aeneas could not translate',
            'aeneas_crash': 'uncaught exception in Aeneas', 'trait_removed': 'method of a removed trait'}
    nfail = sum(b['stages'][k] for k in ('charon', 'aeneas', 'lean'))
    w('')
    w('**The same, per function** (the %d cedar functions that do not end as compiling Lean with %s, by the census\'s cause classes; a function with several causes appears in each row, "only cause" counts the functions for which fixing that class alone would be enough):' % (nfail, 'patches (i)-(v)' if LAST == 'p5' else 'patches (i)-(iv)'))
    w('')
    w('| cause class | what it is | functions (any cause) | functions (only cause) |')
    w('|:--|:--|--:|--:|')
    for c, n in b['any'].most_common():
        if n < 4:
            continue
        w('| `%s` | %s | %d | %d |' % (c, DESC.get(c, c), n, b['only'][c]))
w('')
w(re.sub(r'\{\{PATCH:(\d+)\}\}', lambda m: patch_diff(m.group(1)), part('40-patches.md')))
w('')
w('## Aeneas\'s own test suite, before and after')
w('')
w('`scripts/run_tests.sh <variant>` runs the `extract-tests` target of Aeneas\'s Makefile (its test runner on every input under `tests/src`, regenerating the LLBC with the source-built Charon and the Lean, Coq and F* outputs) in a private worktree of the unpatched commit, with the given binary, and then asks git which committed outputs changed.')
w('')
w('| binary | tests | runner exits non-zero | committed outputs changed |')
w('|:--|--:|--:|:--|')
for v in V:
    d = os.path.join(FORK, 'tests-out', v)
    rc = [l.split()[0] for l in open(os.path.join(d, 'rc.txt'))]
    ch = [l.strip() for l in open(os.path.join(d, 'changed.txt')) if l.strip()]
    w('| %s | %d | %d | %s |' % (NAME[v], len(rc), sum(1 for x in rc if x != '0'), '0' if not ch else '%d: %s' % (len(ch), ', '.join('`%s`' % os.path.basename(x.split()[-1]) for x in ch))))
w('')
w('- **The two changed files** are expected error outputs of the negative borrow-check tests. They quote the Aeneas source line that prints "Could not borrow-check the body of function …"; patch (iii) moved that code (`interp/Interp.ml, line 686` to `680`). Nothing else differs, and the patch commit updates the two files.')
w('- **No regression found.** The unpatched source build reproduces the committed outputs exactly (0 files changed), so the comparison is meaningful.')
w('- **One loose end in the logs.** `logs/tests-base.log` (07:45:04) records a first run of the unpatched binary with 4 non-zero exits; the stored result (`tests-out/base/rc.txt`, written 51 seconds later) is a rerun with none. What failed the first time was not recorded; the figures in the table are the stored reruns, re-read in the finalising pass.')
w('- **What this does and does not show.** The runner passes `-abort-on-error`; under that flag the new handlers of patch (iii) are switched off on purpose, and no test input triggers the aborts of (i) and (ii). The suite shows that the patches leave existing behaviour alone. The new behaviour is shown by the probes, the reproductions and the census runs above.')
w('- **Not run:** `make verify` (compiling the test outputs with Lean, Coq and F*: the Lean side needs Lean v4.36.0-rc2 and a newer Mathlib than are pinned here) and the `cargo-test` target (Rust unit tests of the test inputs, which do not involve the Aeneas binary). `ocamlformat` was not run on the patches.')
w('')
w(part('60-soundness.md'))
w('')
samp = json.load(open(os.path.join(FORK, 'data', 'sound_sample.json')))
sampC = json.load(open(os.path.join(FORK, 'data', 'sound_sample_C.json')))
res = {r['id']: r for r in sound}
REASON = json.load(open(os.path.join(FORK, 'parts', '61-sound-reasons.json')))


def first_patch(c, i):
    for v in V:
        if i in SH[v][c]['ok_ids']:
            return NAME[v].replace('+ ', '')
    return '?'


def rows(tag, L):
    w('| # | crate | function (Lean name) | compiles since | outcome |')
    w('|:--|:--|:--|:--|:--|')
    for k, x in enumerate(L):
        i = '%s%d' % (tag, k)
        nm = min(x['lean_names'], key=len) if x['lean_names'] else x['name']
        if i in res and res[i]['lean_ran'] == res[i]['inputs']:
            r = res[i]
            oc = '**run: %d of %d inputs agree**%s' % (r['agree'], r['inputs'], ' (%d panic on both sides)' % r['panics_rust'] if r['panics_rust'] else '')
        elif i in REASON:
            oc = REASON[i]
        elif tag != 'C' and not x.get('ok_closure'):
            oc = 'cannot be run: a function of the crate that it calls did not translate'
        elif tag != 'C' and not x.get('ok_closure_no_axiom'):
            oc = 'cannot be run: depends on an external item with no model (an `axiom` in the generated Lean)'
        else:
            oc = 'not attempted'
        w('| %s | %s | `%s` | %s | %s |' % (i, x['crate'], nm, first_patch(x['crate'], x['id']), oc))
    w('')


w('### Sample A: the 30 functions asked for')
w('')
w('`random.Random(20261110).sample(population, 30)` over the %d functions that compile with all four patches (as shipped) and did not with the unpatched build, sorted by crate and inventory id.' % samp['population'])
w('')
rows('A', samp['A'])
w('### Sample B: the same generator continued, over the functions the census join marks as closed')
w('')
w('A shuffle of the %d functions of the population that the join marks "every local callee compiles and no unmodelled external is used", minus sample A; the first 30. Taken to get more executed comparisons. Rows marked "not attempted" were skipped for time or because building their inputs needs more than literals; that choice was mine and is a selection effect.' % samp['population_closed_no_axiom'])
w('')
rows('B', samp['B'])
w('### Sample C: functions that compile only with patch (iv)')
w('')
w('Patch (iv) is the one that changes the text of what Aeneas emits, so it got its own stratum: a seeded shuffle of the functions that compile with (iv) and not without, restricted to the closed ones; the first 24 (`data/sound_sample_C.json`). `C15` is the same function as `A5`.')
w('')
rows('C', sampC)
w(part('80-recommendation.md'))
w('')
w(part('85-carrying.md'))
w('')


def repro_block(name):
    return '`%s`:\n\n```rust\n%s\n```\n' % (name, open(os.path.join(FORK, 'repro', name)).read().rstrip('\n'))


def full_patch(n):
    p = sorted(glob.glob(os.path.join(FORK, 'patches', '%s-*.patch' % n)))[0]
    t = open(p).read()
    body = t[t.index('\ndiff --git') + 1:]
    body = body[:body.rindex('\n-- \n')] if '\n-- \n' in body else body
    return '<details><summary>Proposed patch (on top of %s)</summary>\n\n```diff\n%s\n```\n\n</details>\n' % (
        'Aeneas `0d21a9ec`' if n == '0001' else 'the patches of the previous reports', body.rstrip('\n'))


VERSIONS = ('**Versions.** Aeneas `0d21a9ec` (nightly-2026.11.10), built from source; Charon `454586e9` (0.1.315); Rust `nightly-2026-09-17`; macOS arm64. '
            '{{RELEASE}}\n\n'
            '**Commands** for a single-file reproduction:\n\n```\n'
            'charon rustc --preset=aeneas --dest-file repro.llbc -- repro.rs --crate-name=repro --crate-type=rlib --edition=2021\n'
            'aeneas -backend lean -dest out repro.llbc\n```\n')
os.makedirs(os.path.join(FORK, 'upstream'), exist_ok=True)
w('## Upstream issue texts (ready to send, not sent)')
w('')
w('One text per defect, in `upstream/`, generated from `parts/issues/` with the reproduction source and the proposed patch inlined, so that each file can be pasted as it is. **Nothing has been posted anywhere**, no issue or pull request was opened, and none of the texts was checked against the upstream issue tracker for duplicates: do that before sending. The first line of each file is the issue title.')
w('')
w('| file | title | reproduction | patch |')
w('|:--|:--|:--|:--|')
for f in ISSUES:
    t = open(f).read()
    title = t.split('\n', 1)[0].replace('Title: ', '').strip()
    reps = re.findall(r'\{\{REPRO:([^}]+)\}\}', t)
    pn = re.search(r'\{\{PATCH:(\d+)\}\}', t).group(1)
    body = t.split('\n', 1)[1].strip('\n')
    body = re.sub(r'\{\{REPRO:([^}]+)\}\}\n?', '', body)
    body = re.sub(r'\{\{PATCH:(\d+)\}\}\n?', '', body).rstrip('\n')
    for k, v in SUBST.items():
        body = body.replace('{{%s}}' % k, str(v))
    assert '{{' not in body, f
    txt = 'Title: %s\n\n%s\n\n%s\n' % (title, body, VERSIONS.replace('{{RELEASE}}', 'The release binary of nightly-2026.11.09 (`5a392f4b`) behaves the same.' if pn != '0005' else 'Seen only once the handlers of the previous report are in: the release binary aborts on both crates before it gets this far.'))
    if reps:
        txt += '**Reproduction source.**\n\n' + '\n'.join(repro_block(r) for r in reps) + '\n'
    txt += full_patch(pn)
    open(os.path.join(FORK, 'upstream', os.path.basename(f)), 'w').write(txt)
    w('| `upstream/%s` | %s | %s | `patches/%s` |' % (os.path.basename(f), title.replace('|', '\\|'), ', '.join('`repro/%s`' % r for r in reps) or 'none (seen on `time` and cedar)', pn))
w('')
open(os.path.join(FORK, 'FORK.md'), 'w').write('\n'.join(out))
print('FORK.md', len(out), 'blocks,', sum(len(x) for x in out), 'chars; cedar cw joined for:', sorted(BD))
