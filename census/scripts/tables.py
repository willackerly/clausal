#!/usr/bin/env python3
"""Render data/summary.json (+ data/newer_aeneas.json, data/hax.json, data/rewrites.json) into
Markdown tables, and fill them into the *.template.md files:  {{name}} -> table text.
Writes CENSUS.md, PROFILE.md and IMPROVEMENTS.md so that no number in them is typed by hand."""
import json, os, re, sys, collections
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
import report

S, ALLF, R = report.main()
T = {}
# data/rewrites/ and data/flags/ (full results of the side runs) are not kept in git. When they are absent, the tables
# built from them are taken from the last data/tables.json and the probe statuses from data/probes.json.
_old_tables = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'tables.json')
T_OLD = json.load(open(_old_tables)) if os.path.exists(_old_tables) else {}


def pct(a, b):
    return '%.0f%%' % (100.0 * a / b) if b else '–'


def pct1(a, b):
    return '%.1f%%' % (100.0 * a / b) if b else '–'


def table(head, rows, align=None):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join((':--' if (align or 'l' * len(head))[i] == 'l' else '--:') for i in range(len(head))) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out)


def load(name, default=None):
    p = os.path.join(HERE, 'data', name)
    return json.load(open(p)) if os.path.exists(p) else default


crates = list(S['crates'])
pins = {p['name']: p for p in load('selection/pins.json')}

# ---- corpus
rows = []
for c in crates:
    d = S['crates'][c]
    rows.append([c, d['version'], report.GROUP[c], d['source_fns'], d['not_compiled'], d['fns'], d['loc'], d['generated_fns']])
o = S['overall']
rows.append(['**all ten**', '', '', o['source_fns'], o['not_compiled'], o['fns'], o['loc'], o['generated_fns']])
T['corpus'] = table(['crate', 'version', 'set', 'functions in source (non-test)', 'not compiled under default features', '**functions counted**', '**code lines counted**', 'extra functions written by derives/macros'], rows, 'lllrrrrr')

# ---- headline per crate
rows = []
for c in crates + ['business', 'popular', 'overall']:
    d = S['crates'][c] if c in S['crates'] else S[c]
    lab = c if c in S['crates'] else '**%s**' % {'business': 'business five', 'popular': 'popular five', 'overall': 'all ten'}[c]
    rows.append([lab, d['fns'], '%d (%s)' % (d['as_is_ok'], pct(d['as_is_ok'], d['fns'])), '%d (%s)' % (d['charon_ok'], pct(d['charon_ok'], d['fns'])),
                 '%d (%s)' % (d['aeneas_ok'], pct(d['aeneas_ok'], d['fns'])), '**%d (%s)**' % (d['lean_ok'], pct(d['lean_ok'], d['fns'])),
                 '%d (%s)' % (d['closure_ok'], pct(d['closure_ok'], d['fns'])), '%d (%s)' % (d['closure_no_axiom'], pct(d['closure_no_axiom'], d['fns']))])
T['by_function'] = table(['crate', 'functions', 'as is: Lean compiles', 'peeled: Charon extracts', 'peeled: Aeneas translates', 'peeled: Lean compiles', '…and every local callee compiles', '…and no unmodelled external is used'], rows, 'lrrrrrrr')
rows = []
for c in crates + ['business', 'popular', 'overall']:
    d = S['crates'][c] if c in S['crates'] else S[c]
    lab = c if c in S['crates'] else '**%s**' % {'business': 'business five', 'popular': 'popular five', 'overall': 'all ten'}[c]
    rows.append([lab, d['loc'], '%d (%s)' % (d['as_is_ok_loc'], pct(d['as_is_ok_loc'], d['loc'])), '%d (%s)' % (d['charon_ok_loc'], pct(d['charon_ok_loc'], d['loc'])),
                 '%d (%s)' % (d['aeneas_ok_loc'], pct(d['aeneas_ok_loc'], d['loc'])), '**%d (%s)**' % (d['lean_ok_loc'], pct(d['lean_ok_loc'], d['loc'])),
                 '%d (%s)' % (d['closure_ok_loc'], pct(d['closure_ok_loc'], d['loc'])), '%d (%s)' % (d['closure_no_axiom_loc'], pct(d['closure_no_axiom_loc'], d['loc']))])
T['by_loc'] = table(['crate', 'code lines', 'as is: Lean compiles', 'peeled: Charon extracts', 'peeled: Aeneas translates', 'peeled: Lean compiles', '…and every local callee compiles', '…and no unmodelled external is used'], rows, 'lrrrrrrr')

# ---- what "as is" does per crate
rows = []
for c in crates:
    d = S['crates'][c]
    a = d['as_is']
    if a is None:
        asis = 'runs to the end; Lean file produced'
    else:
        asis = ('**Charon fails**: ' if a['stage'] == 'charon' else '**Aeneas aborts**: ') + a['msg'].replace('Aeneas aborted the whole crate (fatal exception): ', '').replace('|', '/')
        if a.get('source'):
            asis += ' at `%s:%d`' % (a['source']['file'].replace('/rustc/library/', ''), a['source']['beg'])
        if a.get('n_ice_sites'):
            asis += ' (%d sites)' % a['n_ice_sites']
    sur = '; '.join('`%s`%s' % (x['name'], (' + %d impls' % x['impls_removed']) if x.get('impls_removed') else '') for x in d['surgery']) or '–'
    if len(d['surgery']) > 8:
        k = collections.Counter(x['kind'] for x in d['surgery'])
        sur = '%d removals (%s); list in `data/results/%s.json`' % (len(d['surgery']), ', '.join('%d %s' % (v, kk.replace('_', ' ')) for kk, v in k.items()), c)
    rows.append([c, asis, d['opaque_marks'] or '–', sur, d['lean_lines'] or '–', d['secs']['charon'], d['secs']['aeneas_final'] if d['secs']['aeneas_final'] is not None else '–', (d['lake'] or {}).get('secs', '–')])
T['as_is'] = table(['crate', 'tools as shipped', 'functions marked opaque so Charon finishes', 'removed from the LLBC so Aeneas finishes', 'Lean lines generated', 'Charon s', 'Aeneas s (final run)', 'Lean build s'], rows, 'lllllrrr')

# ---- cedar: everything the peel had to do
if 'cedar-policy-core' in R:
    rc = R['cedar-policy-core']
    rows = []
    for x in rc['surgery']:
        if x['kind'] == 'trait_method':
            rows.append(['method entry removed', '`%s`' % x['name'], 'signature with a trait-type constraint', '–', '–'])
        elif x['kind'] == 'trait_decl_and_impls':
            m = re.search(r'method `(\w+)` \((\w+)\)', x['why'])
            why = {'dyn': '`dyn` in the signature of `%s`', 'gat': 'generic associated type in the signature of `%s`', 'fnptr': 'function pointer in the signature of `%s`'}.get(m.group(2), '%s') % m.group(1) if m else x['why'][:80]
            rows.append(['trait removed with its impls', '`%s`' % x['name'], why, x.get('impls_removed', '–'), len(x.get('removed_funs') or [])])
        elif x['kind'] == 'fun_body_opaque':
            rows.append(['function body made opaque', '`%s`' % x['name'], 'uncaught exception in Aeneas on this body', '–', '–'])
        else:
            rows.append([x['kind'].replace('_', ' '), x['name'], x['why'][:90], '–', '–'])
    T['cedar_surgery'] = table(['step', 'declaration', 'why Aeneas stops on it', 'impls removed', 'local functions removed with them'], rows, 'lllrr')
    T['cedar_marks'] = '%d' % len(rc['opaque_marks'])
    T['cedar_marked_fns'] = '%d' % len(set(m['fn'] for m in rc['opaque_marks']))
    kinds = collections.Counter((re.search(r'\((\w+)\)$', x['why']) or re.search(r'\((\w+)\)', x['why'])).group(1) for x in rc['surgery'] if x['kind'] == 'trait_decl_and_impls' and re.search(r'\((dyn|gat|fnptr)\)', x['why']))
    T['cedar_n_traits'] = '%d' % sum(1 for x in rc['surgery'] if x['kind'] == 'trait_decl_and_impls')
    T['cedar_n_dyn'] = '%d' % kinds.get('dyn', 0)
    T['cedar_n_methods'] = '%d' % sum(1 for x in rc['surgery'] if x['kind'] == 'trait_method')
    T['cedar_n_crash'] = '%d' % sum(1 for x in rc['surgery'] if x['kind'] == 'fun_body_opaque')
    cs = load('cedar_before_mixed_group_fix.summary.json', {})
    ex = (cs.get('mixed_group_experiment') or {}).get('mixed groups moved last, run 2') or {}
    T['cedar_mixed_noerr'] = '{:,}'.format(ex.get('no_error_logged', 0))
    T['cedar_mixed_cands'] = '{:,}'.format(ex.get('candidates', 0))

# ---- classes
rows = []
tot = S['failed_total']
for cid, d in sorted(S['classes'].items(), key=lambda kv: (-kv[1]['any'], kv[0])):
    ex = d['examples'][0] if d['examples'] else None
    rows.append(['`%s`' % cid, d['title'], d['family'], d['any'], d['any_loc'], d['sole'], d['sole_loc'], ', '.join('%s %d' % (k, v) for k, v in sorted(d['by_crate'].items(), key=lambda kv: -kv[1])[:5]),
                 ('`%s` %s:%d' % (ex['name'], ex['crate'] + '/' + ex['file'], ex['line'])) if ex else ''])
T['classes'] = table(['class', 'what it is', 'family', 'functions (any cause)', 'lines', 'functions (only cause)', 'lines', 'where', 'example'], rows, 'lllrrrrll')
rows = []
for k, d in sorted(S['families'].items(), key=lambda kv: -kv[1]['any']):
    rows.append([k, d['any'], pct1(d['any'], o['fns']), d['any_loc'], d['sole'], d['sole_loc']])
T['families'] = table(['cause family', 'failing functions it appears in', 'share of all counted functions', 'lines', 'functions where it is the only cause', 'lines'], rows, 'lrrrrr')
T['failed_total'] = '%d functions (%d code lines)' % (tot['fns'], tot['loc'])

# ---- stage of failure
rows = []
for c in crates + ['overall']:
    fs = [f for f in ALLF if f['origin'] == 'source' and f['stage'] != 'absent' and (c == 'overall' or f['crate'] == c)]
    k = collections.Counter(f['stage'] for f in fs)
    rows.append([c if c != 'overall' else '**all ten**', len(fs), k['charon'], k['aeneas'], k['lean'], k['ok']])
T['stages'] = table(['crate', 'functions', 'stopped at Charon', 'stopped at Aeneas', 'stopped at Lean', 'through all three'], rows, 'lrrrrr')

# ---- features
NAMES = {'for_range': '`for i in a..b`', 'for_iter': '`for x in <iterator or collection>`', 'while_loop': '`while`', 'while_let': '`while let`', 'loop_loop': '`loop`', 'nested_loop': 'a loop inside a loop',
         'return_in_loop': '`return` inside a loop', 'try_in_loop': '`?` inside a loop', 'labeled_break': 'labelled `break`', 'closure': 'a closure', 'try_op': '`?` anywhere', 'match': '`match`',
         'unsafe_block': '`unsafe` block', 'unsafe_fn': '`unsafe fn`', 'ptr_cast': 'cast to a raw pointer', 'as_cast': '`as` cast', 'index': 'indexing `a[i]`', 'index_range': 'range indexing `a[i..j]`',
         'float': 'float literal or type in the body', 'sig_float': 'float in the signature', 'sig_dyn': '`dyn Trait` in the signature', 'dyn_in_body': '`dyn Trait` in the body', 'sig_impl_trait': '`impl Trait` in the signature',
         'sig_fn_trait': '`Fn`/`FnMut`/`FnOnce` in the signature', 'sig_iterator': '`Iterator`/`IntoIterator` in the signature', 'trait_bounds': 'trait bounds on type parameters', 'type_params': 'type parameters on the function',
         'lifetime_params': 'lifetime parameters on the function', 'const_fn': '`const fn`', 'sig_mut_ref': '`&mut` in the signature', 'sig_string': '`str`/`String` in the signature', 'sig_formatter': '`fmt::Formatter` in the signature (Display/Debug impls)',
         'sig_box': '`Box` in the signature', 'sig_rc': '`Rc`/`Arc` in the signature', 'sig_cell': '`Cell`/`RefCell` in the signature', 'interior_mut': 'interior mutability type in the body', 'sig_map': 'hash/B-tree map or set in the signature',
         'sig_vec': '`Vec` in the signature', 'str_literal': 'a string literal', 'macro_call': 'any macro call', 'method_call': 'any method call', 'sig_hrtb': '`for<\'a>` in the signature', 'async_fn': '`async fn`'}
rows = []
for k, d in S['features'].items():
    rows.append([NAMES.get(k, k), d['fns'], d['ok'], pct(d['ok'], d['fns']), d['loc'], pct(d['ok_loc'], d['loc'])])
rows.sort(key=lambda r: -r[1])
onc = S['overall_without_cedar']
rows.insert(0, ['*(all counted functions of the nine crates)*', onc['fns'], onc['lean_ok'], pct(onc['lean_ok'], onc['fns']), onc['loc'], pct(onc['lean_ok_loc'], onc['loc'])])
T['features'] = table(['the function contains …', 'functions', 'compile in Lean', 'rate', 'code lines', 'rate by lines'], rows, 'lrrrrr')
rows = [['`%s!`' % k, v[0], v[1], pct(v[1], v[0])] for k, v in list(S['macros'].items())[:20]]
T['macros'] = table(['macro called in the body', 'functions', 'compile in Lean', 'rate'], rows, 'lrrr')
rows = [['`.%s()`' % k, v[0], v[1], pct(v[1], v[0])] for k, v in S['methods'].items() if v[0] >= 12][:70]
for k in list(S['methods']):
    if k not in ('map', 'iter', 'collect', 'into_iter', 'debug_list', 'entries', 'field', 'debug_struct', 'finish', 'ok_or', 'map_err', 'unwrap', 'expect', 'clone', 'get', 'len', 'push', 'copied', 'cloned', 'as_bytes', 'strip_prefix', 'split', 'find', 'starts_with', 'contains'):
        continue
T['methods'] = table(['method called in the body', 'functions', 'compile in Lean', 'rate'], rows, 'lrrr')

# ---- std reliance
rows = [['`%s`' % x['name'], x['fns'], x['crates']] for x in S['lib_models'][:60]]
T['lib_models'] = table(['Aeneas library name used by a compiling function', 'functions', 'crates'], rows, 'lrr')
rows = [['`%s`' % x['rust_name'].replace('|', '\\|'), x['fns'], x['crates']] for x in S['axioms_used'][:50]]
T['axioms_used'] = table(['external item with no model (emitted as a Lean `axiom`)', 'compiling functions that use it', 'crates'], rows, 'lrr')
T['axioms_declared'] = ', '.join('%s %d' % (k, v) for k, v in S['axioms_declared'].items())
sm = load('std_models.json', {})
T['std_models_counts'] = ', '.join('%d %s' % (len(v), {'fun': 'functions', 'type': 'types', 'trait': 'traits', 'trait_impl': 'trait impls', 'const': 'constants'}.get(k, k)) for k, v in sm.items())
mods = collections.defaultdict(list)
for x in sm.get('fun', []):
    if not re.match(r'^[A-Za-z_{]', x['rust']) or '\n' in x['rust'] or '::' not in x['rust']:
        continue
    p = re.sub(r'\{[^{}]*(\{[^{}]*\}[^{}]*)*\}', lambda m: '{' + re.sub(r'^\{(impl )?', '', m.group(0))[:-1][:48] + '}', x['rust'])
    parts = x['rust'].split('::')
    mods['::'.join(parts[:2])].append(x['rust'])
rows = []
for k, v in sorted(mods.items(), key=lambda kv: -len(kv[1])):
    names = sorted(set(re.sub(r'.*::', '', n) for n in v))
    rows.append(['`%s`' % k, len(v), ', '.join('`%s`' % n for n in names[:40]) + (' …' if len(names) > 40 else '')])
T['std_models'] = table(['module', 'modelled functions', 'method / function names'], rows, 'lrl')
T['std_traits'] = ', '.join('`%s`' % x['rust'] for x in sm.get('trait', []) if '::' in x['rust'] and '\n' not in x['rust'])
T['std_types'] = ', '.join('`%s`' % x['rust'] for x in sm.get('type', []) if '::' in x['rust'] and '\n' not in x['rust'])

# ---- improvements
rows = []
for i, d in enumerate(S['improvements'], 1):
    rows.append([i, '`%s`' % d['id'], d['title'], d['lower'], d['lower_loc'], d['upper'], d['upper_loc'],
                 ', '.join(('%s %d' % (c, d['by_crate'][c])) if 'by_crate' in d else c for c in d['crates'][:5])])
T['improvements'] = table(['rank', 'id', 'improvement', 'functions unlocked (lower bound)', 'lines', 'functions it appears in (upper bound)', 'lines', 'crates'], rows, 'lllrrrrl')
rows = [[d['family'], d['any'], d['sole']] for d in S['axiom_families']]
T['axiom_families'] = table(['missing model', 'functions that compile, with all local callees, but rest on it', '…and on nothing else'], rows, 'lrr')
fl = {}
fd = os.path.join(HERE, 'data', 'flags')
if os.path.isdir(fd):
    rows = []
    tot = [0, 0, 0]
    for c in crates:
        fp = os.path.join(fd, c + '_ftm.json')
        if not os.path.exists(fp):
            continue
        r = json.load(open(fp))
        fs = [f for f in r['functions'] if f['origin'] == 'source' and f['charon'] != 'absent']
        ok = sum(1 for f in fs if f.get('ok'))
        d = S['crates'][c]
        def nerr(path):
            try:
                return len(re.findall(r'^error: .*\.lean:\d+', open(path, errors='replace').read(), re.M))
            except OSError:
                return 0
        e0 = nerr(os.path.join(HERE, 'work', 'run', c, 'lake.log'))
        e1 = nerr(os.path.join(HERE, 'work', 'run', c + '_ftm', 'lake.log'))
        r['_lean_errors'] = (e0, e1)
        rows.append([c, d['fns'], d['lean_ok'], ok, '%+d' % (ok - d['lean_ok']), e0, e1])
        tot[0] += d['fns']; tot[1] += d['lean_ok']; tot[2] += ok
        tot.append((e0, e1))
    if rows:
        rows.append(['**crates run**', tot[0], tot[1], tot[2], '%+d' % (tot[2] - tot[1]), sum(x[0] for x in tot[3:]), sum(x[1] for x in tot[3:])])
        T['flag_ftm'] = table(['crate', 'functions', 'compile, default flags', 'compile, `-filter-trait-methods`', 'difference', 'Lean errors, default', 'Lean errors, with the flag'], rows, 'lrrrrrr')

# ---- emitters
rows = [['`%s`' % x['emitter'], x['msg'].replace('|', '/'), x['fns'], '`%s`' % x['class'], x['example']] for x in S['emitters'][:45]]
T['emitters'] = table(['Aeneas source line that raised it', 'message', 'functions', 'class', 'example'], rows, 'llrll')

# ---- newer aeneas, hax
na = load('newer_aeneas.json')
if na:
    rows = []
    for x in sorted(na, key=lambda x: crates.index(x['crate']) if x['crate'] in crates else 99):
        if x['crate'] not in crates:
            continue
        a, p = x.get('as_is') or {}, x.get('peeled') or {}
        rows.append([x['crate'], 'aborts' if a.get('pinned_fatal') else ('ok' if a else '–'), 'aborts' if a.get('new_fatal') else ('ok' if a else '–'),
                     p.get('pinned_errors', '–'), p.get('new_errors', '–'), p.get('lean_lines_pinned', '–'), p.get('lean_lines_new', '–'), p.get('diff_lines', '–')])
    T['newer'] = table(['crate', 'pinned 11.09, as is', 'newer 11.10, as is', 'errors logged, pinned (peeled LLBC)', 'errors logged, newer', 'Lean lines, pinned', 'Lean lines, newer', 'differing lines'], rows, 'lllrrrrr')
hx = load('hax.json')
if hx:
    rows = []
    for x in hx:
        out = 'Lean files written' if x['extraction_files'] else 'no Lean written'
        why = ('rustc ICE under Charon (%d)' % x['rustc_ice']) if x['rustc_ice'] else (('Aeneas aborts: ' + (x['last_error'] or '')) if x['aeneas_fatal'] and not x['extraction_files'] else (x['hax_error'] or ''))
        rows.append([x['crate'], x['exit'], out, why.replace('|', '/')[:120], x['aeneas_errors'], x['defs'], x['axioms'], x['sorries'], x['secs']])
    T['hax'] = table(['crate', 'exit code', 'outcome', 'reason', 'Aeneas errors logged', '`def`s in extraction', '`axiom`s', '`sorry`s', 'seconds'], rows, 'lrllrrrrr')

rw = load('rewrites.json')
if rw:
    rows = []
    for x in rw:
        rows.append([x['id'], '`%s` %s:%s' % (x['function'], x['crate'] + '/' + x['file'], x['line']), x['idiom'], x['before'].replace('|', '/'), x['after'].replace('|', '/'), '%s' % x['tests'], '%d → %d' % (x['loc_before'], x['loc_after']), x['lines_changed'],
                     '%d of %d' % (x.get('class_fixed', 0), x.get('class_before', 0)), '%d → %d' % (x.get('crate_ok_before', 0), x.get('crate_ok_after', 0))])
    T['rewrites'] = table(['#', 'function', 'idiom removed', 'before', 'after the rewrite', "crate's own tests (`cargo test`)", 'function code lines', 'patch lines (+/−)', 'functions of the crate with this cause that now compile', 'functions of the crate that compile'], rows, 'llllllllll')

# ---- probes (probes/profile-probes-0.1.0, run through the same pipeline)
PR = {}
pp = os.path.join(HERE, 'data', 'rewrites', 'profile-probes_probe.json')
if os.path.exists(pp):
    pr = json.load(open(pp))
    for f in pr['functions']:
        if f['origin'] != 'source':
            continue
        mod = f['path'].split('::')[0]
        if f.get('ok'):
            ax = sorted(set(a.split('.')[-1] for a in f.get('dep_axioms', [])))
            st = 'translates and compiles' + (' (calls with no model, emitted as axioms: %s)' % ', '.join('`%s`' % a for a in ax[:5]) if ax else '')
            if not f.get('ok_closure'):
                st += ' (a function it calls does not)'
        else:
            m = f['msgs'][0] if f['msgs'] else {'stage': '?', 'msg': '?'}
            msg = re.sub(r'uses excluded declaration (\S+)', r'uses \1, removed from the input because Aeneas aborts the crate on it', m['msg'])
            st = '**fails** at %s: %s' % ({'aeneas': 'Aeneas', 'lean': 'Lean', 'charon': 'Charon'}.get(m['stage'], m['stage']), msg[:150].replace('|', '/').replace('`', "'"))
        PR[mod + '.' + f['name']] = {'ok': bool(f.get('ok')), 'text': st, 'axioms': f.get('dep_axioms', []), 'noax': f.get('ok_closure_no_axiom')}
    json.dump(PR, open(os.path.join(HERE, 'data', 'probes.json'), 'w'), indent=1)
    pairs = []
    for k in sorted(PR):
        if k.endswith('_before'):
            a = k[:-7] + '_after'
            pairs.append(['`%s`' % k[:-7], PR[k]['text'], PR[a]['text'] if a in PR else '–'])
    T['probe_pairs'] = table(['probe (`probes/profile-probes-0.1.0/src/lib.rs`)', 'idiom as usually written (`_before`)', 'profile form (`_after`)'], pairs, 'lll')
    oks = [['`%s`' % k, PR[k]['text']] for k in sorted(PR) if k.endswith('_ok')]
    T['probe_ok'] = table(['probe', 'result'], oks, 'll')
    T['probe_counts'] = '%d probe functions: %d translate and compile, %d do not' % (len(PR), sum(1 for v in PR.values() if v['ok']), sum(1 for v in PR.values() if not v['ok']))

# ---- improvement notes, spliced in rank order
IMP = {d['id']: d for d in S['improvements']}


def imp_text(i):
    d = IMP.get(i)
    if d is None:
        return 'no function of this corpus'
    cr = ', '.join(('%s %d' % (c, d['by_crate'][c])) if 'by_crate' in d else c for c in d['crates'][:6])
    if d['lower'] == d['upper']:
        return '%d functions, %d code lines (%s)' % (d['lower'], d['lower_loc'], cr)
    return '%d functions and %d code lines as the only cause, %d functions and %d lines counting every appearance (%s)' % (d['lower'], d['lower_loc'], d['upper'], d['upper_loc'], cr)


np_ = os.path.join(HERE, 'scripts', 'IMPROVEMENT_NOTES.md')
if os.path.exists(np_):
    blocks = {}
    cur = None
    for line in open(np_).read().split('\n'):
        if line.startswith('@@ '):
            cur = line[3:].strip()
            blocks[cur] = []
        elif cur is not None:
            blocks[cur].append(line)
    ranked = [d['id'] for d in S['improvements'] if d['id'] in blocks]
    T['TOP_FIVE'] = '\n'.join('\n'.join(blocks[i]).strip() + '\n' for i in ranked[:5])
    T['FURTHER'] = '\n'.join('\n'.join(blocks[i]).strip() + '\n' for i in ranked[5:])
    T['top_five_ids'] = ', '.join('`%s`' % i for i in ranked[:5])

if not PR and os.path.exists(os.path.join(HERE, 'data', 'probes.json')):
    PR = json.load(open(os.path.join(HERE, 'data', 'probes.json')))

# ---- the mixed-group reproduction (probes/mixed-group-probe and its rewrite)
def probe_rows(tag):
    pth = os.path.join(HERE, 'data', 'rewrites', tag + '_probe.json')
    if not os.path.exists(pth):
        return {}
    out = collections.OrderedDict()
    for f in sorted((f for f in json.load(open(pth))['functions'] if f['origin'] == 'source'), key=lambda f: f['line_start']):
        owner = re.sub(r'.*\{impl (.*)\}$', r'\1', f['path']) if '{impl' in f['path'] else ''
        owner = owner.replace('fmt::Display for ', 'Display for ')
        nm = ('<%s>::' % owner if ' for ' in owner else (owner + '::' if owner else '')) + f['name']
        if f.get('ok'):
            st = 'compiles'
        else:
            m = f['msgs'][0] if f['msgs'] else {'stage': '?', 'msg': '?'}
            st = '**fails** (%s): %s' % ({'aeneas': 'Aeneas', 'lean': 'Lean'}.get(m['stage'], m['stage']), m['msg'][:70].replace('|', '/').replace('`', "'"))
        out[nm] = st
    return out


mb, ma = probe_rows('mixed-group-probe'), probe_rows('mixed-group-fixed-probe')
if mb:
    names = list(mb) + [n for n in ma if n not in mb]
    rows = [['`%s`' % n, mb.get(n, '–'), ma.get(n, '–')] for n in names]
    T['mixed_probe'] = table(['function, in source order', '`probes/mixed-group-probe` (two `Display` impls use each other)', '`probes/mixed-group-fixed-probe` (recursion moved to inherent methods)'], rows, 'lll')
    T['mixed_probe_before_ok'] = '%d of %d' % (sum(1 for v in mb.values() if v == 'compiles'), len(mb))
    T['mixed_probe_after_ok'] = '%d of %d' % (sum(1 for v in ma.values() if v == 'compiles'), len(ma))

for k, v in T_OLD.items():
    T.setdefault(k, v)
json.dump(T, open(os.path.join(HERE, 'data', 'tables.json'), 'w'), indent=1)
for name in ('CENSUS', 'PROFILE', 'IMPROVEMENTS'):
    tp = os.path.join(HERE, 'scripts', name + '.template.md')
    if not os.path.exists(tp):
        continue
    txt = open(tp).read()
    missing = set()

    def rep(m):
        k = m.group(1)
        if k in T:
            return T[k]
        # scalar lookups: {{n:overall.lean_ok}}  {{p:overall.lean_ok/overall.fns}}
        def val(path):
            cur = S
            if path.startswith('rw.'):      # {{n:rw.3.crate_ok_after}}
                _, i, field = path.split('.')
                return next(x for x in rw if str(x['id']) == i)[field]
            for part in path.split('.'):
                cur = cur[part] if not part.isdigit() else cur[int(part)]
            return cur
        try:
            if k.startswith('imp:'):
                return imp_text(k[4:])
            if k.startswith('probe:'):
                return PR[k[6:]]['text']
            if k.startswith('feat:'):       # {{feat:for_range}} -> "5 of 11 (45%)"
                d = S['features'][k[5:]]
                return '%d of %d (%s)' % (d['ok'], d['fns'], pct(d['ok'], d['fns']))
            if k.startswith('meth:'):
                v = S['methods'][k[5:]]
                return '%d of %d (%s)' % (v[1], v[0], pct(v[1], v[0]))
            if k.startswith('mac:'):
                v = S['macros'][k[4:]]
                return '%d of %d (%s)' % (v[1], v[0], pct(v[1], v[0]))
            if k.startswith('cls:'):        # {{cls:loop_exit}} -> "13 functions, 949 lines"
                if k[4:] in report.CLASSES and k[4:] not in S['classes']:
                    return 'no function in this corpus'
                d = S['classes'][k[4:]]
                return '%d functions, %d lines' % (d['any'], d['any_loc'])
            if k.startswith('n:'):
                return '{:,}'.format(val(k[2:]))
            if k.startswith('p:'):
                a, b = k[2:].split('/')
                return pct(val(a), val(b))
        except Exception:
            pass
        missing.add(k)
        return '**[missing: %s]**' % k
    txt = txt.replace('TOP_FIVE', T.get('TOP_FIVE', 'TOP_FIVE')).replace('FURTHER', T.get('FURTHER', 'FURTHER')) if name == 'IMPROVEMENTS' else txt
    txt = re.sub(r'\{\{([^{}]+)\}\}', rep, txt)
    open(os.path.join(HERE, name + '.md'), 'w').write(txt)
    print(name + '.md written', ('MISSING: %s' % sorted(missing)) if missing else '')
