#!/usr/bin/env python3
"""Aggregate data/results/*.json into data/summary.json and the tables used by CENSUS.md,
PROFILE.md and IMPROVEMENTS.md.

    report.py            write data/summary.json, data/functions.jsonl and tables/*.md
    report.py --unclassified   list failure messages that fall into the catch-all classes
"""
import json, os, re, sys, collections, glob

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ['cedar-policy-core', 'rust_decimal', 'semver', 'shlex', 'rusty-money', 'indexmap', 'untrusted', 'fnv', 'time', 'zeroize']
GROUP = {'cedar-policy-core': 'business', 'rust_decimal': 'business', 'semver': 'business', 'shlex': 'business', 'rusty-money': 'business',
         'indexmap': 'popular', 'untrusted': 'popular', 'fnv': 'popular', 'time': 'popular', 'zeroize': 'popular'}

# ----------------------------------------------------------------------------- cause classes
# (id, title, family).  Order of RULES matters: first match wins.
CLASSES = collections.OrderedDict([
    ('charon_ice', ('rustc internal compiler error under the Charon driver', 'tool robustness')),
    ('abort_trait_sig', ('uses a std trait method whose signature makes Aeneas abort the crate (removed in the peel)', 'iterators and closures')),
    ('str_pattern', ('string search APIs built on `core::str::pattern::Pattern` (split, find, starts_with, strip_prefix, trim_matches, contains ...)', 'strings and formatting')),
    ('iter_std', ('iterator adapters / iterator traits with no model (missing builtin information, Iterator methods not in the Lean library)', 'iterators and closures')),
    ('loop_exit', ('`return`, `?` or a labelled `break` that leaves a loop from inside (early return in a loop, return in nested loops, break to outer loop)', 'loops')),
    ('loop_join', ('loop or branch whose borrow state cannot be joined (context matching, fixed point, region-abstraction joins)', 'loops')),
    ('borrow_shape', ('borrow patterns outside the supported fragment (nested borrows, non-endable abstraction, copying a mutable borrow, dangling loans)', 'borrows')),
    ('raw_ptr', ('raw pointers, pointer casts, `&raw`, inline assembly (unsafe code)', 'unsafe')),
    ('dyn_trait', ('trait objects (`dyn Trait`)', 'trait objects')),
    ('fn_ptr', ('function pointers / function items used as values (arrow types)', 'iterators and closures')),
    ('closure', ('closure or function-item shim whose signature or body Aeneas cannot translate', 'iterators and closures')),
    ('hrtb', ('higher-ranked lifetime bounds (`for<\'a> Fn(&\'a ..)`) related to a free lifetime', 'generics with trait bounds')),
    ('trait_generic', ('generic code over traits: associated types / trait-type constraints / trait clauses Aeneas mishandles', 'generics with trait bounds')),
    ('match_scrutinee', ('`match` on a scrutinee Aeneas does not support (a `char`; an enum it will not expand)', 'pattern matching')),
    ('const_static', ('constants and statics Aeneas cannot evaluate or find (array constants, promoted consts, statics)', 'constants')),
    ('float', ('floating point', 'floats')),
    ('fmt', ('formatting machinery (`core::fmt`: Formatter, Arguments, write!/format!)', 'strings and formatting')),
    ('name_clash', ('name generation: two Rust items map to one Lean name', 'tool robustness')),
    ('lean_shadow', ('generated Lean resolves a name to the wrong thing: a user type named like an Aeneas builtin (`Slice`), or a parameter named like a module of the crate', 'generated Lean')),
    ('lean_match', ('generated Lean: a `match` on integer literals that Lean cannot compile (signed integers with negative literal patterns)', 'generated Lean')),
    ('lean_universe', ('generated Lean does not elaborate: universe level metavariables', 'generated Lean')),
    ('lean_syntax', ('generated Lean does not parse', 'generated Lean')),
    ('lean_struct', ('generated Lean: structure/field problems (duplicate field, not a field, invalid projection)', 'generated Lean')),
    ('lean_type', ('generated Lean: type errors in the emitted term', 'generated Lean')),
    ('lean_missing', ('generated Lean refers to a declaration Aeneas did not emit', 'generated Lean')),
    ('lean_other', ('generated Lean: other elaboration errors', 'generated Lean')),
    ('external_dep', ('needs an item of an external crate that is not translated', 'external crates')),
    ('mixed_group', ('the function is in, or depends on, a declaration group that mixes functions with types or trait impls (Aeneas has no analysis for it)', 'tool robustness')),
    ('aeneas_crash', ('Aeneas dies with an uncaught exception on the body of this function', 'tool robustness')),
    ('trait_removed', ('method of an impl of a trait that Aeneas aborts the crate on (the trait and its impls were removed in the peel)', 'trait objects')),
    ('aeneas_internal', ('Aeneas internal error / unimplemented case without a specific message', 'tool robustness')),
    ('not_emitted', ('not emitted, no logged reason', 'tool robustness')),
    ('other', ('other', 'other')),
])

RULES = [
    # (class, stage regex, message regex, emitter regex or None)
    ('trait_removed', r'aeneas', r'^calls a method of an impl that was removed with its trait', None),
    ('aeneas_crash', r'aeneas', r'uncaught exception', None),
    ('trait_removed', r'aeneas', r'^in an impl of `', None),
    ('charon_ice', r'charon', r'rustc ICE|internal compiler error', None),
    ('str_pattern', r'.', r'core::str::pattern|str::pattern::|into_searcher', None),
    ('abort_trait_sig', r'.', r'uses excluded declaration|Could not find: trait_decl: .*method|Could not find: (trait_decl_id|trait_impl_id|fun_decl_id)', None),
    ('iter_std', r'.', r'builtin information|core::iter::|Iterator', None),
    ('loop_exit', r'.', r'Early returns inside of loops|Returns inside of nested loops|Breaks to outer loops|Continue to outer loops', None),
    ('loop_join', r'.', r'Could not match the contexts|Joining region abstractions|fixed.?point|Could not find var for symbolic value|No loan updated', None),
    ('borrow_shape', r'.', r'[Nn]ested borrows|non-endable|copy a mutable borrow|dangling|shared loan|Could not read a borrow|Inconsistent projection|borrow', None),
    ('raw_ptr', r'.', r'raw pointer|&raw |cast_expose|cast_with_exposed|Raw ptr casts|InlineAsm|ptr_metadata|unop: cast', None),
    ('dyn_trait', r'.', r'Dynamic trait types|dyn ', None),
    ('fn_ptr', r'.', r'Arrow types', None),
    ('hrtb', r'.', r'higher-ranked lifetime|lifetime constraint relating', None),
    ('match_scrutinee', r'.', r'Unsupported switch scrutinee|Not allowed to expand enumerations', None),
    ('const_static', r'.', r'unexpected constant|Found unexpected constant|Could not find: [a-z_0-9]+::.*[A-Z_]{3,}|Invalid inputs for binop|global', None),
    ('float', r'.', r'\bfloat|\bf32\b|\bf64\b', None),
    ('name_clash', r'.', r'Name clash|registering the name', None),
    ('lean_shadow', r'lean', r"type expected, got\s*\(?(Slice|Array|Vec|Str)\b|Function expected at\s*(Slice|Array|Vec|Str)\b|Invalid field `(\w+)`: The environment does not contain `[\w.]+\.\3\.\3`", None),
    ('lean_match', r'lean', r'Failed to compile pattern matching|pattern contains metavariables', None),
    ('lean_universe', r'lean', r'universe level metavariables', None),
    ('lean_syntax', r'lean', r'unexpected token|expected term|unexpected identifier', None),
    ('lean_struct', r'lean', r'is not a field of structure|has already been declared|Invalid field|is not a structure|fields missing|not a structure', None),
    ('lean_missing', r'lean', r'[Uu]nknown (identifier|constant)', None),
    ('lean_shadow', r'lean', r"invalid occurrence of datatype '[\w.]*\.(Slice|Array|Str|Vec)' being declared", None),
    ('lean_type', r'lean', r"[Tt]ype mismatch|Function expected|expected a product type|Application type mismatch|failed to synthesize|has type|don't know how to synthesize", None),
    ('lean_other', r'lean', r'.', None),
    ('trait_generic', r'aeneas', r'trait|clause|associated', None),
    ('aeneas_internal', r'aeneas', r'^(Unimplemented|Unreachable|Internal error[:,] please file an issue|Internal error)\b', None),
    ('not_emitted', r'aeneas', r'not emitted|no Lean definition|emitted as opaque', None),
]
# refinement of the anonymous Aeneas errors by the Aeneas source line that raised them
EMITTER_CLASS = {
    'llbc/RegionsHierarchy.ml:302': 'fn_ptr', 'llbc/RegionsHierarchy.ml:315': 'fn_ptr', 'symbolic/SymbolicToPureTypes.ml:398': 'fn_ptr',
    'llbc/RegionsHierarchy.ml:318': 'dyn_trait',
    'symbolic/SymbolicToPureValues.ml:870': 'borrow_shape', 'symbolic/SymbolicToPureValues.ml:888': 'borrow_shape',
    'extract/Extract.ml:487': 'float',
}
# rules keyed on the Aeneas source line first (message alone is ambiguous)
EMITTER_FIRST = {
    'symbolic/SymbolicToPureTypes.ml:724': 'mixed_group',   # lookup of the function analysis result fails
    'interp/InterpExpressions.ml:1189': 'float',     # binary operation on operands that are not integers/bools: every case in this corpus is f32/f64
    'interp/InterpExpressions.ml:120': 'float',      # constant that is not bool/char/integer: float literals
    'extract/Extract.ml:487': 'float',               # cast that is not integer/bool: integer <-> float
    'interp/InterpStatements.ml:1249': 'dyn_trait',  # "Function pointers are not supported yet": raised on the vtable call of a dyn method
}


def classify_msg(m):
    stage, msg, em = m.get('stage', ''), m.get('msg', ''), m.get('emitter') or ''
    if stage == 'lean' and m.get('aeneas_hole'):
        stage = 'aeneas'
    ekey = em.split(',')[0].strip() + ':' + (re.search(r'line (\d+)', em).group(1) if re.search(r'line (\d+)', em) else '')
    if ekey in EMITTER_FIRST:
        return EMITTER_FIRST[ekey]
    for cid, sre, mre, ere in RULES:
        if re.search(sre, stage) and re.search(mre, msg):
            if cid == 'aeneas_internal':
                key = em.split(',')[0].strip() + ':' + (re.search(r'line (\d+)', em).group(1) if re.search(r'line (\d+)', em) else '')
                return EMITTER_CLASS.get(key, cid)
            return cid
    return 'other'


def classes_of(f):
    """ordered list of distinct cause classes of a failed function (most specific first)"""
    cs = []
    for m in f['msgs']:
        c = classify_msg(m)
        if c not in cs:
            cs.append(c)
    # generic classes only count when nothing specific was found
    spec = [c for c in cs if c not in ('not_emitted', 'aeneas_internal', 'other', 'lean_missing', 'abort_trait_sig')]
    if spec:
        return spec
    return cs or ['other']


def load():
    out = {}
    for p in glob.glob(os.path.join(HERE, 'data', 'results', '*.json')):
        r = json.load(open(p))
        if 'surgery' not in r:
            print('skipping stale result file', p, file=sys.stderr)
            continue
        out[r['crate']] = r
    return out


def stage_of(f):
    if f['charon'] == 'absent':
        return 'absent'
    if f['charon'] != 'ok':
        return 'charon'
    if f['aeneas'] != 'ok':
        return 'aeneas'
    if f['lean'] != 'ok':
        return 'lean'
    return 'ok'


def pct(a, b):
    return '%.1f%%' % (100.0 * a / b) if b else 'n/a'


def main():
    R = load()
    crates = [c for c in ORDER if c in R]
    summ = {'crates': {}, 'overall': {}}
    allf = []
    for c in crates:
        r = R[c]
        for f in r['functions']:
            f['crate'] = c
            for k, v in (('ok', False), ('ok_closure', False), ('ok_closure_no_axiom', False), ('dep_lib', []), ('dep_axioms', []), ('dep_local', [])):
                f.setdefault(k, v)
            f['stage'] = stage_of(f)
            f['classes'] = classes_of(f) if f['stage'] not in ('ok', 'absent') else []
            allf.append(f)
    with open(os.path.join(HERE, 'data', 'functions.jsonl'), 'w') as o:
        for f in allf:
            o.write(json.dumps({k: f[k] for k in ('crate', 'id', 'file', 'name', 'path', 'kind', 'origin', 'line_start', 'line_end', 'loc', 'stage', 'ok',
                                                 'ok_closure', 'ok_closure_no_axiom', 'classes', 'msgs', 'dep_lib', 'dep_axioms', 'dep_local', 'feat', 'macros', 'methods', 'cfgs', 'lean_names')}) + '\n')

    def agg(fs):
        src = [f for f in fs if f['origin'] == 'source']
        comp = [f for f in src if f['stage'] != 'absent']
        d = {'source_fns': len(src), 'not_compiled': len(src) - len(comp), 'fns': len(comp), 'loc': sum(f['loc'] for f in comp)}
        for k, pred in (('charon_ok', lambda f: f['stage'] in ('aeneas', 'lean', 'ok')), ('aeneas_ok', lambda f: f['stage'] in ('lean', 'ok')),
                        ('lean_ok', lambda f: f['stage'] == 'ok'), ('closure_ok', lambda f: f['ok_closure']), ('closure_no_axiom', lambda f: f['ok_closure_no_axiom'])):
            d[k] = sum(1 for f in comp if pred(f))
            d[k + '_loc'] = sum(f['loc'] for f in comp if pred(f))
        gen = [f for f in fs if f['origin'] != 'source']
        d['generated_fns'] = len(gen)
        d['generated_ok'] = sum(1 for f in gen if f['stage'] == 'ok')
        return d
    for c in crates:
        fs = [f for f in allf if f['crate'] == c]
        d = agg(fs)
        r = R[c]
        d['as_is'] = r['as_is']
        d['as_is_ok'] = 0 if r['as_is'] else d['lean_ok']
        d['as_is_ok_loc'] = 0 if r['as_is'] else d['lean_ok_loc']
        d['peeled'] = r['peeled']
        d['surgery'] = r['surgery']
        d['opaque_marks'] = len(r['opaque_marks'])
        d['lean_lines'] = r.get('lean_lines')
        d['lake'] = r.get('lake')
        d['rounds'] = len(r['rounds'])
        d['version'] = r['version']
        d['axioms'] = len(r.get('axioms', []))
        d['secs'] = {'charon': sum(x['secs'] for x in r['rounds'] if x['stage'] == 'charon'), 'aeneas': sum(x['secs'] for x in r['rounds'] if x['stage'] == 'aeneas'),
                     'aeneas_final': [x['secs'] for x in r['rounds'] if x['stage'] == 'aeneas'][-1] if any(x['stage'] == 'aeneas' for x in r['rounds']) else None}
        summ['crates'][c] = d
    for g, sel in (('overall', crates), ('business', [c for c in crates if GROUP[c] == 'business']), ('popular', [c for c in crates if GROUP[c] == 'popular']),
                   ('overall_without_cedar', [c for c in crates if c != 'cedar-policy-core'])):
        d = agg([f for f in allf if f['crate'] in sel])
        d['as_is_ok'] = sum(summ['crates'][c]['as_is_ok'] for c in sel)
        d['as_is_ok_loc'] = sum(summ['crates'][c]['as_is_ok_loc'] for c in sel)
        summ[g] = d

    summ['aborts'] = {'aeneas': sum(1 for c in crates if (R[c]['as_is'] or {}).get('stage') == 'aeneas'),
                      'charon': sum(1 for c in crates if (R[c]['as_is'] or {}).get('stage') == 'charon'),
                      'none': sum(1 for c in crates if not R[c]['as_is'])}
    # ---- failure classes
    comp = [f for f in allf if f['origin'] == 'source' and f['stage'] not in ('absent',)]
    fail = [f for f in comp if f['stage'] != 'ok']
    cls = {}
    for cid in CLASSES:
        prim = [f for f in fail if f['classes'][0] == cid]
        sole = [f for f in fail if f['classes'] == [cid]]
        anyc = [f for f in fail if cid in f['classes']]
        if not anyc:
            continue
        cls[cid] = {'title': CLASSES[cid][0], 'family': CLASSES[cid][1],
                    'primary': len(prim), 'primary_loc': sum(f['loc'] for f in prim),
                    'sole': len(sole), 'sole_loc': sum(f['loc'] for f in sole),
                    'any': len(anyc), 'any_loc': sum(f['loc'] for f in anyc),
                    'by_crate': {c: sum(1 for f in anyc if f['crate'] == c) for c in crates if any(f['crate'] == c for f in anyc)},
                    'sole_by_crate': {c: sum(1 for f in sole if f['crate'] == c) for c in crates if any(f['crate'] == c for f in sole)},
                    'stages': dict(collections.Counter(f['stage'] for f in anyc)),
                    'examples': [{'crate': f['crate'], 'file': f['file'], 'line': f['line_start'], 'name': f['name'], 'msg': f['msgs'][0]['msg'][:160]} for f in sole[:4] or anyc[:4]]}
    summ['classes'] = cls
    fam = collections.OrderedDict()
    for cid, d in cls.items():
        x = fam.setdefault(d['family'], {'any': set(), 'sole': set(), 'loc': {}})
    for f in fail:
        fams = []
        for c in f['classes']:
            fm = CLASSES[c][1]
            if fm not in fams:
                fams.append(fm)
        for fm in fams:
            fam[fm]['any'].add((f['crate'], f['id']))
            fam[fm]['loc'][(f['crate'], f['id'])] = f['loc']
        if len(fams) == 1:
            fam[fams[0]]['sole'].add((f['crate'], f['id']))
    summ['families'] = {k: {'any': len(v['any']), 'any_loc': sum(v['loc'][x] for x in v['any']), 'sole': len(v['sole']), 'sole_loc': sum(v['loc'][x] for x in v['sole'])} for k, v in fam.items()}
    summ['failed_total'] = {'fns': len(fail), 'loc': sum(f['loc'] for f in fail)}

    # ---- candidate tool improvements: what each would unlock in this corpus
    #   lower bound = functions for which the classes it addresses are the only cause of failure
    #   upper bound = functions in which they appear at all
    IMPROVE = [
        ('abort', 'Aeneas: skip a trait method whose signature fails instead of aborting the crate', None),
        ('ice', 'Charon: do not let a failed user-type-annotation recovery turn into a rustc ICE', None),
        ('shadow', 'Aeneas (Lean output): qualify builtin type names and keep local names from capturing module names', ['lean_shadow']),
        ('loops', 'Aeneas: general early exit from loops (return / ? / labelled break)', ['loop_exit']),
        ('float', 'Aeneas + library: floating-point operations, constants and casts (as opaque operations)', ['float']),
        ('fnitem', 'Aeneas: function items passed as values when their signature has lifetimes', ['fn_ptr']),
        ('dyn', 'Charon + Aeneas: trait objects and calls through vtables / function pointers', ['dyn_trait', 'trait_removed']),
        ('pattern', 'Aeneas + library: `core::str::pattern::Pattern` (generic associated type) and the str search functions', ['str_pattern']),
        ('itersig', 'Aeneas: trait methods with trait-type constraints (`Iterator::copied`, `cloned`, `try_fold`) and iterator models', ['abort_trait_sig', 'iter_std']),
        ('borrow', 'Aeneas: borrow patterns outside the fragment (nested borrows, joins, non-endable abstractions)', ['borrow_shape', 'loop_join']),
        ('rawptr', 'Aeneas: raw pointers and pointer casts', ['raw_ptr']),
        ('match', 'Aeneas (+ Lean output): `match` on `char`; signed literal patterns; enum expansion', ['match_scrutinee', 'lean_match']),
        ('hrtb', 'Aeneas: higher-ranked lifetimes related to free lifetimes', ['hrtb']),
        ('leanmisc', 'Aeneas (Lean output): remaining elaboration failures (universe metavariables, structure fields, implicit arguments, unresolved names)', ['lean_universe', 'lean_struct', 'lean_type', 'lean_other', 'lean_syntax', 'lean_missing', 'name_clash']),
        ('mixed', 'Aeneas: go on after a declaration group that mixes functions with types or trait impls', ['mixed_group']),
        ('crash', 'Aeneas: catch every exception per function, not only its own error type', ['aeneas_crash']),
        ('internal', 'Aeneas: internal errors without a specific message', ['aeneas_internal', 'not_emitted', 'other']),
        ('const', 'Aeneas: constants and statics it cannot evaluate', ['const_static']),
        ('ext', 'Translate or model external crates', ['external_dep']),
    ]
    imp = []
    for iid, title, cl in IMPROVE:
        if iid in ('abort', 'ice'):
            st = 'aeneas' if iid == 'abort' else 'charon'
            cs = [c for c in crates if (R[c]['as_is'] or {}).get('stage') == st]
            fs = [f for f in comp if f['crate'] in cs and f['stage'] == 'ok']
            extra = [f for f in fail if f['crate'] in cs and f['classes'] == ['charon_ice']] if iid == 'ice' else []
            imp.append({'id': iid, 'title': title, 'classes': ['(whole-crate abort)'], 'lower': len(fs) + len(extra), 'lower_loc': sum(f['loc'] for f in fs + extra),
                        'upper': len(fs) + len(extra), 'upper_loc': sum(f['loc'] for f in fs + extra), 'crates': cs,
                        'note': 'functions that compile once the abort is worked around' + ('; plus %d functions hidden behind the ICE sites, if nothing else stops them' % len(extra) if extra else '')})
        else:
            lo = [f for f in fail if set(f['classes']) <= set(cl)]
            up = [f for f in fail if set(f['classes']) & set(cl)]
            if not up:
                continue
            imp.append({'id': iid, 'title': title, 'classes': cl, 'lower': len(lo), 'lower_loc': sum(f['loc'] for f in lo), 'upper': len(up), 'upper_loc': sum(f['loc'] for f in up),
                        'crates': sorted(set(f['crate'] for f in up), key=lambda c: -sum(1 for f in up if f['crate'] == c)),
                        'by_crate': {c: sum(1 for f in up if f['crate'] == c) for c in crates if any(f['crate'] == c for f in up)}})
    summ['improvements'] = sorted(imp, key=lambda d: -d['lower'])
    # strict metric: functions that compile with all local callees but sit on at least one axiom, by axiom
    axfam = collections.Counter()
    axfam_sole = collections.Counter()
    byid = {(f['crate'], str(f['id'])): f for f in allf}

    def closure_axioms(f, seen):
        out = set()
        key = (f['crate'], str(f['id']))
        if key in seen:
            return out
        seen.add(key)
        for a in f.get('dep_axioms', []):
            out.add(axname.get((f['crate'], a)) or a) if False else out.add((f['crate'], a))
        for j in f.get('dep_local', []):
            g = byid.get((f['crate'], str(j)))
            if g is not None:
                out |= closure_axioms(g, seen)
        return out
    summ['_axiom_closure_pending'] = True

    # ---- emitters (Aeneas source lines that raised the errors)
    em = collections.Counter()
    em_ex = {}
    em_fns = collections.defaultdict(set)
    for f in fail:
        seen = set()
        for m in f['msgs']:
            if m.get('emitter'):
                k = (m['emitter'], re.sub(r'\d+', 'N', m['msg'])[:90])
                if k in seen:
                    continue
                seen.add(k)
                em[k] += 1
                em_fns[m['emitter']].add((f['crate'], f['id']))
                em_ex.setdefault(k, '%s %s:%s %s' % (f['crate'], f['file'], f['line_start'], f['name']))
    summ['emitters'] = [{'emitter': k[0], 'msg': k[1], 'fns': v, 'example': em_ex[k], 'class': classify_msg({'stage': 'aeneas', 'msg': k[1], 'emitter': k[0]})} for k, v in em.most_common(80)]

    # ---- syntactic features vs outcome
    feats = collections.OrderedDict()
    FEATS = ['for_range', 'for_iter', 'while_loop', 'while_let', 'loop_loop', 'nested_loop', 'return_in_loop', 'try_in_loop', 'labeled_break', 'closure',
             'try_op', 'match', 'unsafe_block', 'unsafe_fn', 'ptr_cast', 'as_cast', 'index', 'index_range', 'float', 'sig_float', 'sig_dyn', 'dyn_in_body',
             'sig_impl_trait', 'sig_fn_trait', 'sig_iterator', 'trait_bounds', 'type_params', 'lifetime_params', 'const_fn', 'sig_mut_ref', 'sig_string',
             'sig_formatter', 'sig_box', 'sig_rc', 'sig_cell', 'interior_mut', 'sig_map', 'sig_vec', 'str_literal', 'macro_call', 'method_call', 'sig_hrtb', 'async_fn']
    # Idiom tables leave cedar-policy-core out: 88% of its functions fail for one cause that has nothing to do with what
    # they contain (they come after a mixed declaration group), which would swamp every idiom's rate.
    comp_all = comp
    comp = [f for f in comp_all if f['crate'] != 'cedar-policy-core']
    for k in FEATS:
        w = [f for f in comp if f['feat'].get(k)]
        if w:
            feats[k] = {'fns': len(w), 'ok': sum(1 for f in w if f['stage'] == 'ok'), 'loc': sum(f['loc'] for f in w), 'ok_loc': sum(f['loc'] for f in w if f['stage'] == 'ok')}
    plain = [f for f in comp if not any(f['feat'].get(k) for k in ('for_loop', 'while_loop', 'loop_loop', 'closure', 'unsafe_block', 'unsafe_fn', 'sig_dyn', 'dyn_in_body', 'sig_impl_trait', 'sig_fn_trait', 'trait_bounds', 'type_params', 'float', 'sig_float', 'sig_formatter'))]
    feats['(none of: loop, closure, unsafe, dyn, impl Trait, generics, float, Formatter)'] = {'fns': len(plain), 'ok': sum(1 for f in plain if f['stage'] == 'ok'), 'loc': sum(f['loc'] for f in plain), 'ok_loc': sum(f['loc'] for f in plain if f['stage'] == 'ok')}
    summ['features'] = feats
    # macros and methods
    mac = collections.defaultdict(lambda: [0, 0])
    met = collections.defaultdict(lambda: [0, 0])
    for f in comp:
        for k in f['macros']:
            mac[k][0] += 1
            mac[k][1] += f['stage'] == 'ok'
        for k in f['methods']:
            met[k][0] += 1
            met[k][1] += f['stage'] == 'ok'
    summ['macros'] = {k: v for k, v in sorted(mac.items(), key=lambda kv: -kv[1][0])[:40]}
    summ['methods'] = {k: v for k, v in sorted(met.items(), key=lambda kv: -kv[1][0])[:600]}
    comp = comp_all

    # ---- standard library reliance
    lib = collections.Counter()
    libc = collections.defaultdict(set)
    ax = collections.Counter()
    axc = collections.defaultdict(set)
    axname = {}
    for c in crates:
        for a in R[c].get('axioms', []):
            axname[(c, a['lean_name'])] = a['rust_name']
    for f in comp:
        if f['stage'] != 'ok':
            continue
        for x in f['dep_lib']:
            lib[x] += 1
            libc[x].add(f['crate'])
        for x in f['dep_axioms']:
            rn = axname.get((f['crate'], x)) or x
            rn = re.sub(r"<[^<>]*>", '<_>', rn)
            ax[rn] += 1
            axc[rn].add(f['crate'])
    def fam_of(rn):
        rn = re.sub(r'<[^<>]*>', '<_>', rn or '?')
        if 'try_trait' in rn and 'option' in rn:
            return '`?` on `Option` (`Try::branch`, `FromResidual::from_residual` for `Option`)'
        if 'try_trait' in rn:
            return '`?` through other `Try` impls'
        if rn.startswith(('core::fmt', 'alloc::fmt', 'alloc::string', 'core::str', 'alloc::str')) or '::fmt::' in rn or 'to_string' in rn:
            return 'strings and formatting (`core::fmt`, `str`, `String`)'
        if rn.startswith('core::iter') or 'Iterator' in rn or '::iter::' in rn or 'into_iter' in rn:
            return 'iterators (`core::iter`, slice/vec iterators)'
        if rn.startswith(('core::ptr', 'core::mem', 'core::alloc', 'alloc::alloc', 'core::intrinsics', 'core::hint', 'core::cell', 'alloc::rc', 'alloc::sync')) or 'as_ptr' in rn or 'as_mut_ptr' in rn or 'unchecked' in rn:
            return 'pointers, memory, cells, reference counting (`core::ptr`, `core::mem`, `Rc`, `Cell`)'
        if rn.startswith(('std::collections', 'alloc::collections', 'hashbrown')):
            return 'maps and sets (`HashMap`, `BTreeMap`, hashbrown)'
        if rn.startswith(('core::num', 'core::ops', 'core::cmp', 'core::convert')) or re.match(r'core::(u|i)\d', rn):
            return 'numeric and conversion functions without a model (`core::num`, `core::convert`, `core::cmp`, `core::ops`)'
        if rn.startswith(('core::option', 'core::result')):
            return '`Option`/`Result` methods without a model'
        if rn.startswith(('alloc::vec', 'core::slice', 'alloc::slice', 'core::array', 'alloc::boxed')):
            return '`Vec`/slice/array/`Box` methods without a model'
        if rn.startswith(('core::', 'alloc::', 'std::')):
            return 'other standard library (`' + '::'.join(rn.split('::')[:2]) + '`)'
        return 'external crate `' + rn.split('::')[0].split('#')[0] + '`'
    fam_any, fam_sole = collections.Counter(), collections.Counter()
    for f in comp:
        if f['stage'] == 'ok' and f['ok_closure'] and not f['ok_closure_no_axiom']:
            fams = set(fam_of(axname.get(k)) for k in closure_axioms(f, set()))
            for fm in fams:
                fam_any[fm] += 1
            if len(fams) == 1:
                fam_sole[list(fams)[0]] += 1
    summ['axiom_families'] = [{'family': k, 'any': v, 'sole': fam_sole.get(k, 0)} for k, v in fam_any.most_common()]
    del summ['_axiom_closure_pending']
    summ['lib_models'] = [{'name': k, 'fns': v, 'crates': len(libc[k])} for k, v in lib.most_common(400)]
    summ['axioms_used'] = [{'rust_name': k, 'fns': v, 'crates': len(axc[k])} for k, v in ax.most_common(400)]
    summ['axioms_declared'] = {c: len(R[c].get('axioms', [])) for c in crates}
    json.dump(summ, open(os.path.join(HERE, 'data', 'summary.json'), 'w'), indent=1)
    return summ, allf, R


if __name__ == '__main__':
    summ, allf, R = main()
    if '--unclassified' in sys.argv:
        cnt = collections.Counter()
        ex = {}
        for f in allf:
            if f['origin'] == 'source' and f['stage'] not in ('ok', 'absent') and f['classes'][0] in ('other', 'aeneas_internal', 'not_emitted', 'lean_other', 'lean_missing', 'abort_trait_sig'):
                m = f['msgs'][0]
                k = (f['classes'][0], m['stage'], re.sub(r'\d+', 'N', m['msg'])[:110], m.get('emitter'))
                cnt[k] += 1
                ex.setdefault(k, (f['crate'], f['file'], f['line_start'], f['name']))
        for k, v in cnt.most_common(80):
            print(v, k, ex[k])
    else:
        o = summ['overall']
        print('functions', o['fns'], 'loc', o['loc'], 'as-is ok', o['as_is_ok'], 'peeled: charon', o['charon_ok'], 'aeneas', o['aeneas_ok'], 'lean', o['lean_ok'], 'closure', o['closure_ok'], 'no-axiom', o['closure_no_axiom'])
        for c, d in summ['crates'].items():
            print('  %-18s fns %5d loc %6d | as-is %5d | charon %5d aeneas %5d lean %5d (%s) closure %5d noax %5d | gen %d/%d' % (c, d['fns'], d['loc'], d['as_is_ok'], d['charon_ok'], d['aeneas_ok'], d['lean_ok'], pct(d['lean_ok'], d['fns']), d['closure_ok'], d['closure_no_axiom'], d['generated_ok'], d['generated_fns']))
        for cid, d in sorted(summ['classes'].items(), key=lambda kv: -kv[1]['any']):
            print('  %-16s any %5d sole %5d loc %6d  %s' % (cid, d['any'], d['sole'], d['any_loc'], d['by_crate']))
