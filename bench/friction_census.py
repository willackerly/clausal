#!/usr/bin/env python3
"""Friction census: tests claims A-D and the 'unfolding' claim on ns (machine) vs Carleson, PFR (human).

Inputs (all produced from the built Lean environments at Expr level):
  out/corpus/friction/<c>/hyps.jsonl          corpora/friction/Friction.lean  (run.sh)
  out/corpus/friction/<c>/census/c.*.jsonl    corpora/friction/Census.lean    (census_run.sh)
  out/corpus/<c>/decls.jsonl                  earlier export: valueDeps (propagation), statement text (display only)
Outputs:
  out/corpus/friction/census.json   every number, with intervals
  out/corpus/friction/CENSUS.md     verdict (bench/friction_census_verdict.md with placeholders filled) + tables + examples

Every statistic is a ratio of sums over theorems (share = sum numerator / sum denominator), so a
theorem bootstrap is a reweighting: B multinomial weight vectors, 95% percentile interval.
usage: python3 -I bench/friction_census.py [--B 1000]
"""
import json, glob, sys, os, re, hashlib, collections
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = REPO + '/out/corpus/friction'
CORPORA = ['ns', 'carleson', 'pfr']
B = int(sys.argv[sys.argv.index('--B') + 1]) if '--B' in sys.argv else 1000
SEED = 20261110

FAM = json.load(open(REPO + '/bench/friction_families.json'))
CLASSES = FAM['classes']
SIDE = FAM['side_condition_classes']
RT = set(FAM['real_types'])
SURG = ('indicator', 'restrict', 'support', 'cutoff')

# --- constant lists for the unfolding proxies (names are environment constants) ---
LIMIT_BUNDLED = {'Filter.Tendsto', 'Filter.Eventually', 'Filter.Frequently', 'Filter.EventuallyEq',
                 'Filter.EventuallyLE', 'Asymptotics.IsBigO', 'Asymptotics.IsLittleO',
                 'Asymptotics.IsBigOWith', 'Asymptotics.IsTheta', 'Asymptotics.IsEquivalent',
                 'TendstoUniformly', 'TendstoUniformlyOn', 'TendstoLocallyUniformly',
                 'TendstoLocallyUniformlyOn', 'TendstoUniformlyOnFilter', 'HasSum', 'Summable'}
LIN_BUNDLED = {'ContinuousLinearMap', 'LinearMap', 'ContinuousLinearEquiv', 'LinearEquiv',
               'ContinuousMultilinearMap', 'MultilinearMap', 'LinearIsometry', 'LinearIsometryEquiv',
               'ContinuousAlternatingMap', 'AlternatingMap', 'AddMonoidHom', 'MonoidHom', 'RingHom',
               'AlgHom', 'ContinuousAffineMap', 'AffineMap', 'LinearPMap'}
LIN_UNBUNDLED = {'IsLinearMap', 'IsBoundedLinearMap', 'IsBoundedBilinearMap', 'IsAddMonoidHom',
                 'IsAddGroupHom', 'IsMonoidHom', 'IsGroupHom', 'IsAddHom', 'IsMulHom'}
FUN_BUNDLED = {'ContinuousMap', 'BoundedContinuousFunction', 'SchwartzMap', 'MeasureTheory.Lp',
               'MeasureTheory.AEEqFun', 'ZeroAtInftyContinuousMap', 'CompactlySupportedContinuousMap',
               'MeasureTheory.SimpleFunc', 'ContDiffBump', 'TemperedDistribution'}
LP_BUNDLED = {'MeasureTheory.eLpNorm', "MeasureTheory.eLpNorm'", 'MeasureTheory.eLpNormEssSup',
              'MeasureTheory.MemLp', 'MeasureTheory.Lp', 'MeasureTheory.MemLorentz',
              'MeasureTheory.eLorentzNorm', 'MeasureTheory.wnorm', 'MeasureTheory.MemWLp'}
DERIV_PRED = {'ContDiff', 'ContDiffOn', 'ContDiffAt', 'ContDiffWithinAt', 'Differentiable',
              'DifferentiableOn', 'DifferentiableAt', 'DifferentiableWithinAt', 'HasDerivAt',
              'HasDerivWithinAt', 'HasFDerivAt', 'HasFDerivWithinAt', 'HasStrictDerivAt',
              'HasStrictFDerivAt'}

def tool_of(name, module):
    """decision / normalisation procedure a non-project proof constant belongs to (by declaring module / namespace)"""
    if module.startswith('Mathlib.Tactic.Linarith') or name.startswith('Linarith.') or module.startswith('Mathlib.Tactic.Polyrith'):
        return 'linarith'
    if module.startswith('Mathlib.Tactic.Ring') or module.startswith('Mathlib.Tactic.LinearCombination') \
            or module.startswith('Mathlib.Tactic.Abel') or module.startswith('Mathlib.Tactic.Module'):
        return 'ring'
    if module.startswith('Mathlib.Tactic.NormNum') or name.startswith('Mathlib.Meta.NormNum.'):
        return 'normnum'
    if module.startswith('Mathlib.Tactic.FieldSimp') or module.startswith('Mathlib.Tactic.CancelDenoms'):
        return 'fieldsimp'
    if module.startswith('Init.Omega') or name.startswith('Lean.Omega.') or module.startswith('Init.Data.Int.Linear') \
            or module.startswith('Init.Data.Nat.Linear') or module.startswith('Init.Grind') or name.startswith('Lean.Grind.'):
        return 'omega'
    return None
TOOLS = ['ring', 'normnum', 'linarith', 'fieldsimp', 'omega']
CNAME = re.compile(r'^(C|K|M|c)([^a-z].*)?$')     # binder NAME heuristic for "this real parameter is a constant"


def load_census(c):
    tab, thm = {}, {}
    imports = None
    for f in sorted(glob.glob(f'{OUT}/{c}/census/c.tab.*.jsonl')):
        loc = {}
        for l in open(f):
            d = json.loads(l)
            loc[d['id']] = d['name']
            tab.setdefault(d['name'], d)
        for l in open(f.replace('.tab.', '.thm.')):
            d = json.loads(l)
            d['sc'] = [loc[i] for i in d['sc']]
            d['pc'] = {loc[i]: n for i, n in d['pc']}
            d['pj'] = {loc[i]: n for i, n in d['pj']}
            thm[d['name']] = d
        m = json.load(open(f.replace('.tab.', '.meta.').replace('.jsonl', '.json')))
        if 'projectImports' in m:
            imports = m['projectImports']
    return tab, thm, imports


class Corpus:
    pass


def build(c):
    tab, cthm, imports = load_census(c)
    decl = {}
    for l in open(f'{REPO}/out/corpus/{c}/decls.jsonl'):
        d = json.loads(l)
        if d['kind'] == 'theorem':
            decl[d['name']] = (d['statement'], d.get('statementTruncated', False), d['valueDeps'])
    # tab-derived sets
    def T(n):
        return tab.get(n, {})
    def is_packet(n):
        t = T(n)
        return t.get('isProject') and t.get('isStruct') and not t.get('isClass') and not t.get('resProp') \
            and t.get('nPropFields', 0) > 0 and t.get('nFields', 0) > t.get('nPropFields', 0)
    def is_propstruct(n):
        t = T(n)
        return t.get('isProject') and t.get('isStruct') and not t.get('isClass') and t.get('resProp')
    def named_const(n, tier):
        t = T(n)
        if not (t.get('isProject') and t.get('kind') == 'def' and t.get('resHead') in RT and not t.get('isProjFn')):
            return False
        ah = t.get('argHeads', [])
        if t.get('nBinders', 0) > len(ah):
            return False
        ok = {'Nat', 'Int'} if tier == 1 else {'Nat', 'Int', 'Real', 'NNReal', 'ENNReal'}
        return all(a in ok for a in ah)
    rows, names, modules, extra = [], [], [], []
    cols = None
    for l in open(f'{OUT}/{c}/hyps.jsonl'):
        d = json.loads(l)
        t = cthm[d['name']]
        f = collections.OrderedDict()
        f['n'] = 1
        bs = d['binders']
        P = [b for b in bs if b['isProp']]
        cl = d['concl']
        # ---- (1) statement hypotheses
        f['B_all'] = len(bs)
        for k in ('type', 'term', 'inst', 'hyp'):
            f['B_' + k] = sum(1 for b in bs if b['kind'] == k)
        f['H'] = len(P)
        for k in CLASSES:
            f['H_' + k] = 0
        f['H_side'] = 0
        f['H_cast'] = f['H_ennTop'] = f['H_surg'] = f['H_fin_shape'] = f['H_projHead'] = f['H_projStruct'] = 0
        f['H_D'] = f['H_B'] = f['H_C'] = 0
        for b in P:
            f['H_' + b['cls']] += 1
            fl = b['flags']
            cast = 'cast' in fl
            surg = any(x in fl for x in SURG)
            f['H_cast'] += cast
            f['H_ennTop'] += 'ennrealTop' in fl
            f['H_surg'] += surg
            f['H_fin_shape'] += b['fin'] != ''
            f['H_side'] += b['cls'] in SIDE
            f['H_B'] += (b['cls'] == 'finiteness' or cast)
            f['H_C'] += (b['cls'] == 'support' or surg)
            f['H_D'] += b['cls'] in ('measurability', 'integrability', 'regularity')
            hd = T(b['head'])
            if hd.get('isProject'):
                f['H_projHead'] += 1
                f['H_projStruct'] += bool(hd.get('isStruct'))
        f['T_hasD'] = f['H_D'] > 0
        f['T_hasSide'] = f['H_side'] > 0
        allfl = set(cl['flags'])
        for b in P:
            allfl.update(b['flags'])
        f['S_cast'] = 'cast' in allfl
        f['S_ennTop'] = 'ennrealTop' in allfl
        f['S_surg'] = any(x in allfl for x in SURG)
        f['S_B'] = f['S_cast'] or f['H_finiteness'] > 0 or cl['cls'] == 'finiteness'
        f['S_C'] = f['S_surg'] or f['H_support'] > 0 or cl['cls'] == 'support'
        for k in CLASSES:
            f['C_' + k] = cl['cls'] == k
        f['C_side'] = cl['cls'] in SIDE
        # ---- (3) constants
        f['A_conclEC'] = cl['exRealPos'] > 0
        f['A_conclEReal'] = cl['exReal'] > 0
        f['A_ecBound'] = t['ec'][2] > 0
        f['A_ecBoth'] = t['ec'][3] > 0
        f['A_hypEC'] = any(b.get('exRealPos', 0) > 0 for b in P)
        pp, ppge = set(), set()
        for b in P:
            if b['cls'] == 'positivity' and b['peel'] in ('', 'F') and b.get('subjVar') is not None:
                tb = bs[b['subjVar']]
                if tb.get('head') in RT and tb['kind'] == 'term' and not tb.get('isFun'):
                    if b['pos'] == 'lt':
                        pp.add(tb['i'])
                    if b['pos'] in ('lt', 'le'):
                        ppge.add(tb['i'])
        f['A_posParam'] = len(pp) > 0
        f['A_posParamN'] = len(pp)
        f['A_posParam2'] = len(pp) >= 2
        f['A_nonnegParam'] = len(ppge) > 0
        est = [i for i in pp if cl['cls'] == 'order' and i in cl['mentions']]
        f['A_posParamEst'] = len(est) > 0
        f['A_posParamCname'] = any(CNAME.match(bs[i]['name']) for i in pp)
        f['A_realParam'] = any(b.get('head') in RT and b['kind'] == 'term' and not b.get('isFun') for b in bs)
        lit = t['lit']
        f['A_litReal'] = lit['nReal'] > 0
        f['A_litReal3'] = any(x >= 3 for x in lit['real'])
        f['A_litReal100'] = any(x >= 100 for x in lit['real'])
        f['A_litRealN'] = lit['nReal']
        f['A_litNat'] = lit['nNat'] > 0
        f['A_litAny3'] = any(x >= 3 for x in lit['real'] + lit['nat'] + lit['other'])
        sc = t['sc']
        f['A_named1'] = any(named_const(x, 1) for x in sc)
        f['A_named2'] = any(named_const(x, 2) for x in sc)
        f['A_any'] = f['A_conclEC'] or f['A_posParamCname'] or f['A_named1']
        # ---- (4) unfolding proxies
        scs = set(sc)
        f['U_limB'] = bool(scs & LIMIT_BUNDLED)
        f['U_tendsto'] = 'Filter.Tendsto' in scs
        f['U_epsAny'] = t['eps'][0] > 0
        f['U_epsEx'] = t['eps'][1] > 0
        f['U_epsStrict'] = t['eps'][2] > 0
        f['U_linB'] = bool(scs & LIN_BUNDLED)
        f['U_linU'] = bool(scs & LIN_UNBUNDLED)
        f['U_funB'] = bool(scs & FUN_BUNDLED)
        f['U_lpB'] = bool(scs & LP_BUNDLED)
        f['U_rawLp'] = t['rawLp'] > 0
        f['U_integ'] = t['integ'] > 0
        f['U_derivPred'] = bool(scs & DERIV_PRED)
        tb = [b for b in bs if b['kind'] == 'term']
        f['BT'] = len(tb)
        f['BT_fun'] = sum(1 for b in tb if b.get('isFun'))
        f['BT_scalar'] = sum(1 for b in tb if not b.get('isFun') and b.get('head') in (RT | {'Nat', 'Int', 'Complex'}))
        st = [b for b in tb if not b.get('isFun') and T(b.get('head')).get('isStruct') and not T(b.get('head')).get('isClass')]
        f['BT_struct'] = len(st)
        f['BT_structProj'] = sum(1 for b in st if T(b['head']).get('isProject'))
        f['BT_packet'] = sum(1 for b in st if is_packet(b['head']))
        f['S_packet'] = any(is_packet(x) for x in sc)
        f['S_propStruct'] = any(is_propstruct(x) for x in sc)
        f['S_bundle'] = f['S_packet'] or f['S_propStruct']
        f['SC'] = len(sc)
        projc = [x for x in sc if T(x).get('isProject')]
        f['SC_proj'] = len(projc)
        f['S_anyProj'] = len(projc) > 0
        f['S_MT'] = any(T(x).get('module', '').startswith('Mathlib.MeasureTheory.') for x in sc)
        eq = [(k, n) for k, n in t['pc'].items() if T(k).get('eqnOf')]
        f['U_eqnAny'] = len(eq) > 0
        f['U_eqnProj'] = any(T(k).get('eqnOfProject') for k, _ in eq)
        f['U_eqnProjN'] = sum(n for k, n in eq if T(k).get('eqnOfProject'))
        pf = [(k, n) for k, n in t['pc'].items() if T(k).get('isProjFn') and T(k).get('isProject')]
        f['U_projFn'] = len(pf) > 0
        # ---- tools (non-project proof constants by declaring module)
        tt = 0
        tools = dict.fromkeys(TOOLS, 0)
        for k, n in t['pc'].items():
            tk = T(k)
            if tk.get('isProject'):
                continue
            tt += n
            tl = tool_of(k, tk.get('module', ''))
            if tl:
                tools[tl] += n
        f['T_tot'] = tt
        for k in TOOLS:
            f['T_' + k] = tools[k]
            f['T_uses_' + k] = tools[k] > 0
        f['T_uses_anycert'] = any(tools[k] > 0 for k in TOOLS)
        # ---- (2) proof mass
        m = d.get('mass') or {'nodes': 0, 'outer': {}, 'inner': {}, 'castRegion': 0, 'surgRegion': 0, 'kind': [0, 0, 0]}
        f['M'] = m['nodes']
        f['Mo_main'] = m['outer'].get('main', 0)
        for k in SIDE:
            f['Mo_' + k] = m['outer'].get(k, 0)
        f['Mo_side'] = sum(m['outer'].get(k, 0) for k in SIDE)
        f['Mo_D'] = sum(m['outer'].get(k, 0) for k in ('measurability', 'integrability', 'regularity'))
        f['Mo_meas_int'] = sum(m['outer'].get(k, 0) for k in ('measurability', 'integrability'))
        rs = d.get('rootClass') in SIDE
        f['M_standalone'] = m['nodes'] if rs else 0
        f['M_inline_side'] = 0 if rs else f['Mo_side']
        for k in SIDE:
            f['Mstand_' + k] = m['nodes'] if d.get('rootClass') == k else 0
        for k in CLASSES:
            f['Mi_' + k] = m['inner'].get(k, 0)
        for k in SIDE:
            f['Minl_' + k] = 0 if rs else m['outer'].get(k, 0)
        f['M_EC'] = m['nodes'] if f['A_conclEC'] else 0
        f['M_posParam'] = m['nodes'] if f['A_posParam'] else 0
        f['Mi_ordeq'] = m['inner'].get('order', 0) + m['inner'].get('eq', 0)
        f['M_cast'] = m['castRegion']
        f['M_surg'] = m['surgRegion']
        f['Mk_spine'], f['Mk_data'], f['Mk_inst'] = m['kind']
        ce = d.get('constsExt', {})
        f['E'] = sum(v[0] for v in ce.values())
        for k in ('certificate', 'rewrite', 'order_plumbing', 'positivity', 'cast', 'ennreal_ns', 'enorm_fn', 'indicator',
                  'measurability', 'integrability', 'regularity', 'finiteness', 'support', 'data', 'data_instance',
                  'tc_lemma', 'eq_lemma', 'order_lemma'):
            f['E_' + k] = ce.get(k, [0, 0])[0]
        f['E_arith'] = f['E_certificate'] + f['E_rewrite'] + f['E_order_plumbing'] + f['E_positivity']
        f['E_B'] = f['E_cast'] + f['E_ennreal_ns'] + f['E_finiteness'] + f['E_enorm_fn']
        f['E_C'] = f['E_indicator'] + f['E_support']
        f['E_D'] = f['E_measurability'] + f['E_integrability'] + f['E_regularity']
        f['Pc'] = sum(v[0] for v in d.get('constsProj', {}).values())
        f['size_stmt'] = d['statementSize']
        f['size_stmt_dag'] = d['statementDagSize']
        f['size_both_dag'] = d['statementDagSize'] + d['proofSize']
        f['size_proof'] = d['proofSize']
        if cols is None:
            cols = list(f.keys())
        rows.append([float(f[k]) for k in cols])
        names.append(d['name'])
        modules.append(d['module'])
        st_, tr_, deps = decl.get(d['name'], ('', True, []))
        extra.append({'statement': st_, 'trunc': tr_, 'deps': deps,
                      'hypcls': collections.Counter(b['cls'] for b in P), 'concl': cl['cls']})
    X = np.array(rows)
    # ---- propagation columns (need the producer set first)
    ci = {k: i for i, k in enumerate(cols)}
    prod = {names[i] for i in range(len(names)) if X[i, ci['A_conclEC']] > 0}
    idx = {n: i for i, n in enumerate(names)}
    uses = np.zeros(len(names)); consumed = np.zeros(len(names)); consumedByProd = np.zeros(len(names))
    for i, e in enumerate(extra):
        ps = {x for x in e['deps'] if x in prod and x != names[i]}
        if ps:
            uses[i] = 1
            for p in ps:
                consumed[idx[p]] = 1
                if names[i] in prod:
                    consumedByProd[idx[p]] = 1
    isprod = X[:, ci['A_conclEC']]
    add = {'Pr_uses': uses, 'Pr_uses_isprod': uses * isprod, 'Pr_consumed': consumed, 'Pr_consumedByProd': consumedByProd,
           'Pr_notuses': 1 - uses, 'Pr_notuses_isprod': (1 - uses) * isprod}
    for k, v in add.items():
        cols.append(k)
        X = np.column_stack([X, v])
    # longest producer -> producer chain
    sys.setrecursionlimit(1000000)
    depth = {}
    def dep(n, stack=()):
        if n in depth:
            return depth[n]
        depth[n] = 1
        best = 0
        for x in extra[idx[n]]['deps']:
            if x in prod and x != n:
                best = max(best, dep(x))
        depth[n] = 1 + best
        return depth[n]
    for p in prod:
        dep(p)
    C = Corpus()
    C.name, C.X, C.cols, C.names, C.modules, C.extra, C.tab = c, X, cols, names, modules, extra, tab
    C.imports = imports
    C.chain = collections.Counter(depth.values())
    C.maxchain = max(depth.values()) if depth else 0
    return C


def groups_of(C):
    n = len(C.names)
    allidx = np.arange(n)
    g = collections.OrderedDict()
    mods = np.array(C.modules)
    col = {k: i for i, k in enumerate(C.cols)}
    if C.name == 'ns':
        leaf = {m for m, ds in C.imports.items() if not ds}
        sup = np.array([m in leaf for m in C.modules])
        root = np.array([m.split('.')[0] for m in C.modules])
        g['ns'] = allidx
        g['ns/NavierStokes'] = allidx[(root == 'NavierStokes') & ~sup]
        g['ns/Euler'] = allidx[(root == 'Euler') & ~sup]
        g['ns/support'] = allidx[sup]
    elif C.name == 'carleson':
        tm = np.array([m.startswith('Carleson.ToMathlib') for m in C.modules])
        g['carleson'] = allidx
        g['carleson/main'] = allidx[~tm]
        g['carleson/ToMathlib'] = allidx[tm]
    else:
        g['pfr'] = allidx
    mt = C.X[:, col['S_MT']] > 0
    if C.name != 'pfr':
        g[C.name + '|MT'] = allidx[mt]
        g[C.name + '|D-hyp'] = allidx[C.X[:, col['T_hasD']] > 0]
    return g


def boot_sums(X, rng, B):
    n = X.shape[0]
    out = np.empty((B, X.shape[1]))
    p = np.full(n, 1.0 / n)
    for s in range(0, B, 50):
        W = rng.multinomial(n, p, size=min(50, B - s)).astype(np.float64)
        out[s:s + W.shape[0]] = W @ X
    return out


# ---------------- statistic registry: (section, id, label, numerator cols, denominator cols, scale) ----------------
S = []
def stat(sec, sid, label, num, den='n', scale=100.0):
    S.append((sec, sid, label, num if isinstance(num, list) else [num], den if isinstance(den, list) else [den], scale))

# (1) hypotheses
stat('hyp', 'hyp.perthm', 'Prop-valued binders per theorem (mean)', 'H', 'n', 1)
stat('hyp', 'hyp.explicit.perthm', 'explicit hypotheses per theorem (mean)', 'B_hyp', 'n', 1)
stat('hyp', 'hyp.binders.perthm', 'all binders per theorem (mean)', 'B_all', 'n', 1)
stat('hyp', 'hyp.side.perthm', 'side-condition hypotheses per theorem (mean)', 'H_side', 'n', 1)
for k in CLASSES:
    stat('hyp', 'hyp.cls.' + k, f'% of Prop binders: {k}' + (' (side)' if k in SIDE else ''), 'H_' + k, 'H')
stat('hyp', 'hyp.side', '% of Prop binders: any side-condition class', 'H_side', 'H')
stat('hyp', 'hyp.A', 'claim A: % positivity', 'H_positivity', 'H')
stat('hyp', 'hyp.B', 'claim B: % finiteness class or mentioning a cast', 'H_B', 'H')
stat('hyp', 'hyp.B.cast', '... % mentioning a cast function', 'H_cast', 'H')
stat('hyp', 'hyp.B.fin', '... % of shape `x ≠ ⊤` / `x < ⊤`', 'H_fin_shape', 'H')
stat('hyp', 'hyp.C', 'claim C: % support class or mentioning indicator/restrict/support/cutoff', 'H_C', 'H')
stat('hyp', 'hyp.D', 'claim D: % measurability + integrability + regularity', 'H_D', 'H')
stat('hyp', 'hyp.D.mi', '... % measurability + integrability', ['H_measurability', 'H_integrability'], 'H')
stat('hyp', 'hyp.projHead', '% of Prop binders whose head is a project-defined predicate', 'H_projHead', 'H')
stat('hyp', 'thm.hasD', '% of theorems with at least one claim-D hypothesis', 'T_hasD')
stat('hyp', 'thm.hasSide', '% of theorems with at least one side-condition hypothesis', 'T_hasSide')
stat('hyp', 'thm.S_B', '% of theorems whose statement has a cast or a finiteness-class fact', 'S_B')
stat('hyp', 'thm.S_C', '% of theorems whose statement has domain surgery', 'S_C')
stat('hyp', 'thm.C_side', '% of theorems whose conclusion is a side-condition class', 'C_side')
# (2) proof mass
stat('mass', 'mass.side', 'inside a side-condition proof (any class)', 'Mo_side', 'M')
for k in SIDE:
    stat('mass', 'mass.outer.' + k, f'... {k}', 'Mo_' + k, 'M')
stat('mass', 'mass.B', 'claim B: finiteness side-conditions', 'Mo_finiteness', 'M')
stat('mass', 'mass.B.region', 'claim B upper bound: inside a proof whose type mentions a cast', 'M_cast', 'M')
stat('mass', 'mass.C', 'claim C: support side-conditions', 'Mo_support', 'M')
stat('mass', 'mass.C.region', 'claim C upper bound: inside a proof whose type mentions indicator/restrict/support/cutoff', 'M_surg', 'M')
stat('mass', 'mass.D', 'claim D: measurability + integrability + regularity', 'Mo_D', 'M')
stat('mass', 'mass.D.mi', '... measurability + integrability only', 'Mo_meas_int', 'M')
stat('mass', 'mass.standalone', 'in theorems whose own conclusion is a side condition', 'M_standalone', 'M')
stat('mass', 'mass.inline', 'side conditions discharged inline (other theorems)', 'M_inline_side', 'M')
for k in SIDE:
    stat('mass', 'mass.inline.' + k, f'... inline {k}', 'Minl_' + k, 'M')
stat('mass', 'mass.EC', 'proof mass of theorems concluding `∃ C, 0 < C ∧ …` (claim A)', 'M_EC', 'M')
stat('mass', 'mass.posParam', 'proof mass of theorems taking a positive real parameter (claim A, upper bound)', 'M_posParam', 'M')
stat('mass', 'mass.inner.eq', 'nearest goal is an equation', 'Mi_eq', 'M')
stat('mass', 'mass.inner.order', 'nearest goal is an inequality (not 0-positivity)', 'Mi_order', 'M')
stat('mass', 'mass.inner.ordeq', 'arithmetic/order plumbing: nearest goal is an equation or inequality', 'Mi_ordeq', 'M')
stat('mass', 'mass.inner.positivity', 'nearest goal is positivity', 'Mi_positivity', 'M')
stat('mass', 'mass.inner.cert', 'nearest goal is a certificate predicate (ring/norm_num/linarith internals)', 'Mi_cert', 'M')
stat('mass', 'mass.inner.tc', 'nearest goal is a Prop-valued type-class fact', 'Mi_tc', 'M')
stat('mass', 'mass.inner.other', 'nearest goal is unclassified (mostly project predicates)', 'Mi_other', 'M')
stat('mass', 'mass.inner.logic', 'nearest goal is logic', 'Mi_logic', 'M')
stat('mass', 'mass.inner.mem', 'nearest goal is membership / inclusion', 'Mi_mem', 'M')
stat('mass', 'mass.kind.inst', 'nodes inside an instance argument', 'Mk_inst', 'M')
stat('mass', 'mass.kind.data', 'nodes inside a non-proof (term) argument', 'Mk_data', 'M')
stat('mass', 'mass.kind.spine', 'nodes on the proof spine', 'Mk_spine', 'M')
stat('mass', 'size.stmtshare', 'statement DAG nodes as % of statement + proof DAG nodes', 'size_stmt_dag', 'size_both_dag')
stat('mass', 'size.stmt.mean', 'statement DAG nodes per theorem (mean)', 'size_stmt_dag', 'n', 1)
stat('mass', 'size.proof.mean', 'proof DAG nodes per theorem (mean, `proofSize`)', 'size_proof', 'n', 1)
stat('mass', 'mass.perthm', 'distinct proof nodes per theorem (mean)', 'M', 'n', 1)
stat('part', 'part.outer.main', 'outer: main argument (not inside any side-condition proof)', 'Mo_main', 'M')
for k in SIDE:
    stat('part', 'part.outer.' + k, f'outer: {k}', 'Mo_' + k, 'M')
for k in CLASSES:
    stat('part', 'part.inner.' + k, f'inner: {k}', 'Mi_' + k, 'M')
stat('part', 'part.kind.spine', 'kind: proof spine', 'Mk_spine', 'M')
stat('part', 'part.kind.data', 'kind: inside a term argument', 'Mk_data', 'M')
stat('part', 'part.kind.inst', 'kind: inside an instance argument', 'Mk_inst', 'M')
stat('const', 'const.cert', 'automation certificates (ring, norm_num, linarith, omega, decide, ...)', 'E_certificate', 'E')
for k in TOOLS:
    stat('const', 'const.tool.' + k, f'... {k}', 'T_' + k, 'T_tot')
stat('const', 'const.rewrite', 'rewrite glue (Eq.mpr, congrArg, simp lemmas of core)', 'E_rewrite', 'E')
stat('const', 'const.order_plumbing', 'order/arithmetic library lemmas', 'E_order_plumbing', 'E')
stat('const', 'const.positivity', 'positivity lemmas', 'E_positivity', 'E')
stat('const', 'const.arith', 'arithmetic total: certificates + rewrite + order + positivity', 'E_arith', 'E')
stat('const', 'const.B', 'claim B: cast functions, cast lemmas, ENNReal/NNReal lemmas, finiteness lemmas, ℝ≥0∞ norms', 'E_B', 'E')
stat('const', 'const.C', 'claim C: indicator/restrict/support/cutoff lemmas and functions', 'E_C', 'E')
stat('const', 'const.D', 'claim D: measurability + integrability + regularity lemmas', 'E_D', 'E')
stat('const', 'const.D.reg', '... regularity lemmas', 'E_regularity', 'E')
stat('const', 'const.inst', 'instances (data_instance)', 'E_data_instance', 'E')
stat('const', 'const.data', 'functions and types (data)', 'E_data', 'E')
for k in TOOLS + ['anycert']:
    stat('const', 'thm.uses.' + k, f'% of theorems whose proof contains {k} output' if k != 'anycert' else '% of theorems whose proof contains any of these', 'T_uses_' + k)
# (3) constants
stat('A', 'A.conclEC', 'conclusion is `∃ C, 0 < C ∧ …` (real-typed ∃ with a `0 < C` or `0 ≤ C` conjunct)', 'A_conclEC')
stat('A', 'A.ecBoth', '... and that C is used as an upper bound (`… ≤ … C …`)', 'A_ecBoth')
stat('A', 'A.ecBound', 'conclusion has a real ∃ used as an upper bound, with or without a sign conjunct', 'A_ecBound')
stat('A', 'A.conclEReal', 'conclusion has any real-typed ∃', 'A_conclEReal')
stat('A', 'A.hypEC', 'a hypothesis has the `∃ C, 0 < C ∧ …` shape', 'A_hypEC')
stat('A', 'A.posParam', 'takes a real parameter x together with `0 < x`', 'A_posParam')
stat('A', 'A.posParam2', '... two or more such parameters', 'A_posParam2')
stat('A', 'A.posParamN', '... mean number of such parameters per theorem', 'A_posParamN', 'n', 1)
stat('A', 'A.posParamEst', '... and the conclusion is an inequality mentioning it', 'A_posParamEst')
stat('A', 'A.posParamCname', '... and the binder is named like a constant (C*, K*, M*, c*)', 'A_posParamCname')
stat('A', 'A.named1', 'statement mentions a project-defined real constant (closed or ℕ/ℤ-indexed)', 'A_named1')
stat('A', 'A.named2', '... allowing real parameters too (includes ordinary real functions)', 'A_named2')
stat('A', 'A.litReal', 'statement has a real literal ≥ 2', 'A_litReal')
stat('A', 'A.litReal3', 'statement has a real literal ≥ 3', 'A_litReal3')
stat('A', 'A.litReal100', 'statement has a real literal ≥ 100', 'A_litReal100')
stat('A', 'A.litRealN', 'distinct real literals ≥ 2 per theorem (mean)', 'A_litRealN', 'n', 1)
stat('A', 'A.litAny3', 'statement has any numeric literal ≥ 3', 'A_litAny3')
stat('A', 'A.prop.cond', 'P(conclusion is ∃C>0 | proof uses a lemma concluding ∃C>0)', 'Pr_uses_isprod', 'Pr_uses')
stat('A', 'A.prop.base', 'P(conclusion is ∃C>0 | proof uses no such lemma)', 'Pr_notuses_isprod', 'Pr_notuses')
stat('A', 'A.prop.uses', '% of theorems whose proof uses a lemma concluding ∃C>0', 'Pr_uses')
stat('A', 'A.prop.consumed', '% of ∃C>0 lemmas used by another project theorem', 'Pr_consumed', 'A_conclEC')
stat('A', 'A.prop.consumedByProd', '% of ∃C>0 lemmas used by another ∃C>0 lemma', 'Pr_consumedByProd', 'A_conclEC')
# (4) unfolding
stat('U', 'U.lim.bundled', 'P1 statement uses a filter/asymptotic notion (Tendsto, ∀ᶠ, IsBigO, HasSum, …)', 'U_limB')
stat('U', 'U.lim.tendsto', 'P1 ... Filter.Tendsto', 'U_tendsto')
stat('U', 'U.lim.epsStrict', 'P1 statement has an explicit ε-shape `∀ ε>0, … ∃ …, … < ε`', 'U_epsStrict')
stat('U', 'U.lim.epsEx', 'P1 statement has `∀ x>0, … ∃ …` (looser)', 'U_epsEx')
stat('U', 'U.lim.ratio', 'P1 bundled share = bundled / (bundled + strict ε-shape)', 'U_limB', ['U_limB', 'U_epsStrict'])
stat('U', 'U.lin.bundled', 'P2 statement uses a bundled morphism type (ContinuousLinearMap, LinearMap, …)', 'U_linB')
stat('U', 'U.lin.unbundled', 'P2 statement uses IsLinearMap / IsBoundedLinearMap-style predicates', 'U_linU')
stat('U', 'U.fun.bundled', 'P2 statement uses a bundled function space (C(X,Y), Lp, 𝓢, a.e.-classes)', 'U_funB')
stat('U', 'U.bt.fun', 'P2 % of term binders that are bare functions', 'BT_fun', 'BT')
stat('U', 'U.bt.struct', 'P2 % of term binders whose type is a structure', 'BT_struct', 'BT')
stat('U', 'U.bt.structProj', 'P2 ... a project-defined structure', 'BT_structProj', 'BT')
stat('U', 'U.lp.bundled', 'P3 statement uses eLpNorm / MemLp / Lp', 'U_lpB')
stat('U', 'U.lp.raw', 'P3 statement has an integral of a power of a norm', 'U_rawLp')
stat('U', 'U.lp.integ', 'P3 statement has any integral', 'U_integ')
stat('U', 'U.lp.ratio', 'P3 bundled share = bundled / (bundled + raw)', 'U_lpB', ['U_lpB', 'U_rawLp'])
stat('U', 'U.cert.mass', 'P4 proof mass whose nearest goal is a certificate predicate', 'Mi_cert', 'M')
stat('U', 'U.cert.const', 'P4 certificate constants as share of non-project constant uses', 'E_certificate', 'E')
stat('U', 'U.cert.linarith', 'P4 % of theorems with linarith/nlinarith output in the proof', 'T_uses_linarith')
stat('U', 'U.eqn.proj', 'P5 % of theorems whose proof rewrites with an equation lemma of a project definition', 'U_eqnProj')
stat('U', 'U.proj.any', 'P5 % of theorems whose statement mentions a project-defined constant', 'S_anyProj')
stat('U', 'U.proj.vocab', 'P5 project-defined share of the distinct constants in a statement', 'SC_proj', 'SC')
stat('U', 'U.packet', 'P5 statement mentions a project structure bundling data with proofs ("packet")', 'S_packet')
stat('U', 'U.propStruct', 'P5 statement mentions a project Prop-valued structure', 'S_propStruct')
stat('U', 'U.bundle', 'P5 either', 'S_bundle')
stat('U', 'U.bt.packet', 'P5 % of term binders whose type is a project packet', 'BT_packet', 'BT')
stat('U', 'U.hyp.projStruct', 'P5 % of Prop binders whose head is a project structure', 'H_projStruct', 'H')

MED = [('hyp.med', 'Prop-valued binders per theorem (median)', 'H'), ('stmt.med', 'statement size, tree nodes (median)', 'size_stmt'),
       ('proof.med', 'proof size, distinct subterms (median)', 'size_proof')]


def fmt(v, lo, hi, d=None):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return '–'
    if d is None:
        a = abs(v)
        d = 3 if 0 < a < 0.1 else (2 if a < 10 else 1)
    return f'{v:.{d}f} [{lo:.{d}f}, {hi:.{d}f}]'


def main():
    rng = np.random.default_rng(SEED)
    Cs = {c: build(c) for c in CORPORA}
    G, sums, bsums, res, modG = collections.OrderedDict(), {}, {}, collections.OrderedDict(), {}
    for c in CORPORA:
        C = Cs[c]
        for g, idx in groups_of(C).items():
            G[g] = (C, idx)
            Xg = C.X[idx]
            sums[g] = Xg.sum(axis=0)
            bsums[g] = boot_sums(Xg, rng, B)
            # module-cluster sums
            mods = sorted({C.modules[i] for i in idx})
            mi = {m: k for k, m in enumerate(mods)}
            Xm = np.zeros((len(mods), Xg.shape[1]))
            for r, i in enumerate(idx):
                Xm[mi[C.modules[i]]] += Xg[r]
            modG[g] = boot_sums(Xm, rng, B)
    def ratio(s, C, num, den):
        ci = {k: i for i, k in enumerate(C.cols)}
        a = s[..., [ci[k] for k in num]].sum(axis=-1)
        b = s[..., [ci[k] for k in den]].sum(axis=-1)
        with np.errstate(divide='ignore', invalid='ignore'):
            return np.where(b > 0, a / np.where(b > 0, b, 1), np.nan)
    draws = {}
    for g, (C, idx) in G.items():
        res[g] = {'n': int(len(idx)), 'modules': len({C.modules[i] for i in idx})}
        for sec, sid, label, num, den, sc in S:
            v = float(ratio(sums[g], C, num, den)) * sc
            dr = ratio(bsums[g], C, num, den) * sc
            dm = ratio(modG[g], C, num, den) * sc
            draws[(g, sid)] = dr
            if np.isnan(v) or np.all(np.isnan(dr)):
                res[g][sid] = {'v': None}
                continue
            lo, hi = np.nanpercentile(dr, [2.5, 97.5])
            mlo, mhi = np.nanpercentile(dm, [2.5, 97.5])
            res[g][sid] = {'v': v, 'lo': float(lo), 'hi': float(hi), 'mlo': float(mlo), 'mhi': float(mhi)}
        ci = {k: i for i, k in enumerate(C.cols)}
        for sid, label, colname in MED:
            x = C.X[idx, ci[colname]]
            ds = [np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(200)]
            res[g][sid] = {'v': float(np.median(x)), 'lo': float(np.percentile(ds, 2.5)), 'hi': float(np.percentile(ds, 97.5))}
    # differences (independent bootstraps)
    def diff(a, b, key):
        out = {}
        for sec, sid, label, num, den, sc in S:
            ra, rb = res[a][sid], res[b][sid]
            if ra.get('v') is None or rb.get('v') is None:
                out[sid] = {'v': None}
                continue
            d = draws[(a, sid)] - draws[(b, sid)]
            lo, hi = np.nanpercentile(d, [2.5, 97.5])
            out[sid] = {'v': ra['v'] - rb['v'], 'lo': float(lo), 'hi': float(hi)}
        res[key] = out
    diff('ns', 'carleson', 'ns-carleson')
    diff('ns|MT', 'carleson|MT', 'ns-carleson|MT')
    diff('ns|D-hyp', 'carleson|D-hyp', 'ns-carleson|D-hyp')
    diff('ns/support', 'carleson/ToMathlib', 'support-ToMathlib')

    # ---------- propagation detail ----------
    prop = {}
    for c in CORPORA:
        C = Cs[c]
        ci = {k: i for i, k in enumerate(C.cols)}
        prop[c] = {'producers': int(C.X[:, ci['A_conclEC']].sum()), 'consumers': int(C.X[:, ci['Pr_uses']].sum()),
                   'consumers_that_produce': int(C.X[:, ci['Pr_uses_isprod']].sum()),
                   'producers_consumed': int(C.X[:, ci['Pr_consumed']].sum()),
                   'producers_consumed_by_producer': int(C.X[:, ci['Pr_consumedByProd']].sum()),
                   'longest_chain': C.maxchain, 'chain_depth_hist': {str(k): v for k, v in sorted(C.chain.items())}}

    # ---------- examples ----------
    def key(n):
        return hashlib.sha1(n.encode()).hexdigest()
    EX = [
        ('A1', 'A: conclusion `∃ C, 0 < C ∧ …`', lambda C, i, ci: C.X[i, ci['A_conclEC']] > 0),
        ('A2', 'A: positive real parameter in an inequality', lambda C, i, ci: C.X[i, ci['A_posParamEst']] > 0),
        ('B', 'B: statement with a cast or a finiteness fact', lambda C, i, ci: C.X[i, ci['S_B']] > 0),
        ('C', 'C: statement with indicator / restrict / support / cutoff', lambda C, i, ci: C.X[i, ci['S_C']] > 0),
        ('D-mi', 'D: measurability or integrability hypothesis', lambda C, i, ci: C.X[i, ci['H_measurability']] + C.X[i, ci['H_integrability']] > 0),
        ('D-reg', 'D: regularity hypothesis (ContDiff, Continuous, HasDerivAt, …)', lambda C, i, ci: C.X[i, ci['H_regularity']] > 0),
    ]
    MAXLEN = 420
    examples = collections.OrderedDict()
    for eid, title, pred in EX:
        examples[eid] = {'title': title}
        for c, k in (('ns', 5), ('carleson', 5)):
            C = Cs[c]
            ci = {x: i for i, x in enumerate(C.cols)}
            match = [i for i in range(len(C.names)) if pred(C, i, ci)]
            elig = [i for i in match if not C.extra[i]['trunc'] and 0 < len(C.extra[i]['statement']) <= MAXLEN]
            elig.sort(key=lambda i: key(C.names[i]))
            examples[eid][c] = {'matching': len(match), 'eligible': len(elig),
                                'items': [{'name': C.names[i], 'module': C.modules[i], 'statement': C.extra[i]['statement']} for i in elig[:k]]}

    out = {'B': B, 'seed': SEED, 'groups': {g: res[g] for g in res}, 'propagation': prop,
           'examples': examples,
           'stats': [{'section': s[0], 'id': s[1], 'label': s[2], 'num': s[3], 'den': s[4], 'scale': s[5]} for s in S]}
    json.dump(out, open(OUT + '/census.json', 'w'), indent=1, ensure_ascii=False)

    # ---------------- CENSUS.md ----------------
    L = []
    def cell(g, sid, cluster=False):
        r = res[g].get(sid, {'v': None})
        if r.get('v') is None:
            return '–'
        return fmt(r['v'], r['mlo'], r['mhi']) if cluster else fmt(r['v'], r['lo'], r['hi'])
    def table(sec, gs, heads=None, ids=None, cluster=False):
        heads = heads or gs
        L.append('| | ' + ' | '.join(heads) + ' |')
        L.append('|---|' + '---|' * len(gs))
        for s in S:
            if (ids is None and s[0] == sec) or (ids is not None and s[1] in ids):
                L.append(f'| {s[2]} | ' + ' | '.join(cell(g, s[1], cluster) for g in gs) + ' |')
        L.append('')
    MAIN = ['ns', 'carleson', 'ns-carleson', 'pfr']
    MAINH = ['ns (machine)', 'Carleson (human)', 'ns − Carleson', 'PFR (human)']
    AREA = ['ns/NavierStokes', 'ns/Euler', 'ns/support', 'carleson/main', 'carleson/ToMathlib']
    AREAH = ['ns: Navier–Stokes', 'ns: Euler', 'ns: support', 'Carleson: main', 'Carleson: ToMathlib']

    vp = REPO + '/bench/friction_census_verdict.md'
    if os.path.exists(vp):
        txt = open(vp).read()
        # {{r:path}} placeholders come from robust.json (bench/friction_robust.py report), filled first
        rj = REPO + '/out/corpus/friction/robust.json'
        if os.path.exists(rj):
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import friction_robust
            txt = friction_robust.rfill(txt, json.load(open(rj)))
        def sub(m):
            parts = [x.strip() for x in m.group(1).split('@')]
            sid, g = parts[0], parts[1]
            mode = parts[2] if len(parts) > 2 else ''
            if sid.startswith('prop.'):
                return f"{prop[g][sid[5:]]:,}"
            if sid == 'n':
                return f"{res[g]['n']:,}"
            r = res[g][sid]
            if r.get('v') is None:
                return 'n/a'
            a = abs(r['v'])
            d = 3 if 0 < a < 0.1 else (2 if a < 10 else 1)
            if mode == 'p':
                return f"{r['v']:.{d}f}"
            if mode == 'd':
                return f"{r['v']:+.{d}f} [{r['lo']:+.{d}f}, {r['hi']:+.{d}f}]"
            return f"{r['v']:.{d}f} [{r['lo']:.{d}f}, {r['hi']:.{d}f}]"
        txt = re.sub(r'\{\{([^}]+)\}\}', sub, txt)
        L.append(txt.rstrip())
        L.append('')
    L.append('---')
    L.append('')
    L.append('# Tables')
    L.append('')
    L.append(f'Generated by `bench/friction_census.py` (B = {B} bootstrap resamples of theorems, seed {SEED}). '
             'Cells are `value [2.5%, 97.5%]`. Every share is a ratio of sums over theorems, so large theorems weigh more in mass shares. '
             'The `ns − Carleson` column is the difference with its own interval (independent resamples); an interval that excludes 0 is a difference not explained by theorem sampling.')
    L.append('')
    L.append('## Groups')
    L.append('')
    L.append('| group | theorems | modules | rule |')
    L.append('|---|---|---|---|')
    rule = {'ns': 'all exported theorems', 'ns/NavierStokes': 'module root `NavierStokes`, not support',
            'ns/Euler': 'module root `Euler`, not support',
            'ns/support': 'modules that import no project module (import graph read from the environment header)',
            'carleson': 'all', 'carleson/main': 'not under `Carleson.ToMathlib`', 'carleson/ToMathlib': 'under `Carleson.ToMathlib`',
            'pfr': 'all', 'ns|MT': 'statement mentions a constant declared under `Mathlib.MeasureTheory.`', 'carleson|MT': 'same',
            'ns|D-hyp': 'theorem has at least one measurability / integrability / regularity hypothesis', 'carleson|D-hyp': 'same'}
    for g in G:
        L.append(f"| {g.replace('|', ', ')} | {res[g]['n']:,} | {res[g]['modules']:,} | {rule.get(g, '')} |")
    L.append('')
    L.append('## 1. Statement hypotheses')
    L.append('')
    L.append('Denominator for the class shares: Prop-valued binders of the statement telescope (explicit hypotheses plus Prop-valued instance arguments).')
    L.append('')
    table('hyp', MAIN, MAINH)
    L.append('| | ' + ' | '.join(MAINH[:2] + MAINH[3:]) + ' |')
    L.append('|---|---|---|---|')
    for sid, label, _ in MED:
        L.append(f'| {label} | ' + ' | '.join(fmt(res[g][sid]['v'], res[g][sid]['lo'], res[g][sid]['hi'], 0) for g in ('ns', 'carleson', 'pfr')) + ' |')
    L.append('')
    L.append('By area:')
    L.append('')
    table('hyp', AREA, AREAH)
    L.append('## 2. Proof mass')
    L.append('')
    L.append('Share (%) of distinct proof-term nodes (`mass.nodes`, definition in `README.md`). '
             '"Inside a side-condition proof" uses the outermost-attribution label; "nearest goal" uses the inner label; they are two marginals of the same nodes and are not additive with each other.')
    L.append('')
    table('mass', MAIN, MAINH)
    L.append('By area:')
    L.append('')
    table('mass', AREA, AREAH)
    L.append('### Constants used in proofs')
    L.append('')
    L.append('Share (%) of non-project constant uses (distinct applications). The per-tool rows use the declaring module of each constant.')
    L.append('')
    table('const', MAIN, MAINH)
    L.append('By area:')
    L.append('')
    table('const', AREA, AREAH)
    L.append('## 3. Explicit constants (claim A)')
    L.append('')
    L.append('Percent of theorems unless the row says otherwise.')
    L.append('')
    table('A', MAIN, MAINH)
    L.append('By area:')
    L.append('')
    table('A', AREA, AREAH)
    L.append('Propagation of `∃ C > 0` through the dependency graph (project theorems, `valueDeps` of the earlier export):')
    L.append('')
    L.append('| | ns | Carleson | PFR |')
    L.append('|---|---|---|---|')
    for k, lab in (('producers', 'theorems concluding `∃ C, 0 < C ∧ …`'), ('producers_consumed', '... used by another project theorem'),
                   ('producers_consumed_by_producer', '... used by another theorem that also concludes `∃ C > 0`'),
                   ('consumers', 'theorems whose proof uses such a lemma'), ('consumers_that_produce', '... and conclude `∃ C > 0` themselves'),
                   ('longest_chain', 'longest chain of `∃ C` lemmas feeding `∃ C` lemmas')):
        L.append(f'| {lab} | ' + ' | '.join(str(prop[c][k]) for c in CORPORA) + ' |')
    L.append('')
    L.append('Chain depth of ns `∃ C` lemmas (1 = uses no other `∃ C` lemma): ' +
             ', '.join(f'{k}: {v}' for k, v in prop['ns']['chain_depth_hist'].items()) + '.')
    L.append('')
    L.append('## 4. Unfolding proxies')
    L.append('')
    L.append('Percent of theorems unless the row says otherwise. P1–P5 are defined and justified in the verdict section.')
    L.append('')
    table('U', MAIN, MAINH)
    L.append('By area:')
    L.append('')
    table('U', AREA, AREAH)
    L.append('## 5. Subject-matter control')
    L.append('')
    L.append('The same shares restricted to theorems of comparable content in both corpora. '
             '`MT`: the statement mentions a constant from `Mathlib.MeasureTheory`. `D-hyp`: the theorem has a measurability, integrability or regularity hypothesis.')
    L.append('')
    CTRL = ['hyp.perthm', 'hyp.cls.positivity', 'hyp.cls.measurability', 'hyp.cls.integrability', 'hyp.cls.regularity', 'hyp.cls.finiteness',
            'hyp.B.cast', 'hyp.C', 'mass.side', 'mass.outer.positivity', 'mass.outer.measurability', 'mass.outer.integrability',
            'mass.outer.regularity', 'mass.outer.finiteness', 'mass.B.region', 'mass.C.region', 'mass.inner.ordeq', 'mass.inner.cert',
            'mass.kind.inst', 'const.cert', 'A.conclEC', 'A.posParam', 'A.litReal3', 'U.lp.bundled', 'U.lp.raw', 'U.lin.bundled', 'U.bundle']
    table(None, ['ns|MT', 'carleson|MT', 'ns-carleson|MT'], ['ns, MT', 'Carleson, MT', 'difference'], ids=CTRL)
    table(None, ['ns|D-hyp', 'carleson|D-hyp', 'ns-carleson|D-hyp'], ['ns, D-hyp', 'Carleson, D-hyp', 'difference'], ids=CTRL)
    L.append('Support libraries against each other (ns modules importing no project module vs `Carleson.ToMathlib`):')
    L.append('')
    table(None, ['ns/support', 'carleson/ToMathlib', 'support-ToMathlib'], ['ns: support', 'Carleson: ToMathlib', 'difference'], ids=CTRL)
    L.append('## 6. Sensitivity: resampling modules instead of theorems')
    L.append('')
    L.append('Theorems in one file are not independent. The same point estimates with intervals from resampling whole modules:')
    L.append('')
    KEY = ['hyp.cls.positivity', 'hyp.cls.regularity', 'hyp.cls.measurability', 'mass.side', 'mass.outer.regularity', 'mass.outer.positivity',
           'mass.D.mi', 'mass.B', 'mass.B.region', 'mass.C.region', 'mass.inner.ordeq', 'mass.inner.cert', 'mass.kind.inst', 'const.cert',
           'A.conclEC', 'A.posParam', 'U.bundle', 'U.eqn.proj']
    table(None, ['ns', 'ns/NavierStokes', 'ns/Euler', 'carleson'], ['ns', 'ns: Navier–Stokes', 'ns: Euler', 'Carleson'], ids=KEY, cluster=True)
    L.append('## 7. Where the proof mass is: three partitions')
    L.append('')
    L.append('Each block is an exclusive partition of the same proof nodes (shares sum to 100 within a block), sorted by the ns share. '
             'outer = outermost enclosing side-condition proof; inner = class of the nearest enclosing goal; kind = syntactic position.')
    L.append('')
    for pre in ('part.outer.', 'part.inner.', 'part.kind.'):
        ids = sorted([x[1] for x in S if x[1].startswith(pre)], key=lambda i: -(res['ns'][i]['v'] or 0))
        L.append('| | ' + ' | '.join(MAINH) + ' |')
        L.append('|---|---|---|---|---|')
        lab = {x[1]: x[2] for x in S}
        for i in ids:
            if all((res[g][i].get('v') or 0) < 0.005 for g in ('ns', 'carleson', 'pfr')):
                continue
            L.append(f'| {lab[i]} | ' + ' | '.join(cell(g, i) for g in MAIN) + ' |')
        L.append('')
    L.append('## 8. Examples')
    L.append('')
    L.append(f'Selection rule (no hand-picking): among theorems matching the stated predicate whose stored statement is complete and at most {MAXLEN} characters, '
             'sort by the SHA-1 of the theorem name and take the first five. Statements are the pretty-printed text stored by the earlier export, shown for reading only; '
             'the predicates were evaluated on the `Expr`. The length cap biases the examples towards short statements; the share that passes it is given.')
    L.append('')
    for eid, e in examples.items():
        L.append(f"### {e['title']}")
        L.append('')
        for c in ('ns', 'carleson'):
            x = e[c]
            L.append(f"**{c}**: {x['matching']:,} theorems match, {x['eligible']:,} within the length cap.")
            L.append('')
            for it in x['items']:
                L.append(f"- `{it['module']}`")
                L.append('  ```lean')
                for ln in it['statement'].split('\n'):
                    L.append('  ' + ln)
                L.append('  ```')
            L.append('')
    open(OUT + '/CENSUS.md', 'w').write('\n'.join(L) + '\n')
    print('wrote', OUT + '/CENSUS.md', 'and census.json')
    for g in G:
        print(g, res[g]['n'])


if __name__ == '__main__':
    main()
