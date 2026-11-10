#!/usr/bin/env python3
"""Robustness checks on the friction census (fixes after the adversarial review, 2026-11-10).

  friction_robust.py mkconfig                 write the variant configs (out/corpus/friction/robust/cfg_*.json)
  friction_robust.py auxtargets <corpus>      target list for the `aux` variant (from a.auxlist.tsv + decls.jsonl)
  friction_robust.py merge <corpus> <variant> merge shards of a variant run into robust/<variant>.jsonl (slim rows)
  friction_robust.py report [--B 1000]        write out/corpus/friction/robust.json and ROBUSTNESS.md

All inputs are files produced by the Expr-level exporters (Friction.lean, Census.lean, Bundles.lean)
and the corpus exports' decls.jsonl.  Standard library only.
"""
import glob, json, os, random, re, sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR = os.path.join(REPO, 'out/corpus/friction')
DERIVVAL = ['HasDerivAt', 'HasDerivWithinAt', 'HasStrictDerivAt', 'HasFDerivAt', 'HasFDerivWithinAt',
            'HasStrictFDerivAt', 'HasGradientAt', 'HasDerivAtFilter', 'HasFDerivAtFilter',
            'HasLineDerivAt', 'HasLineDerivWithinAt']
SIDE0 = ['finiteness', 'positivity', 'measurability', 'integrability', 'regularity', 'support']


def mkconfig():
    cfg = json.load(open(os.path.join(REPO, 'bench/friction_families.json')))
    os.makedirs(FR + '/robust', exist_ok=True)
    reg = [o for o in cfg['type_heads'] if o['class'] == 'regularity'][0]
    missing = [h for h in DERIVVAL if h not in reg['heads']]
    assert not missing, missing
    reg['heads'] = [h for h in reg['heads'] if h not in DERIVVAL]
    cfg['type_heads'].append({'class': 'derivval', 'heads': DERIVVAL})
    cfg['classes'].append('derivval')
    cfg['side_condition_classes'].append('derivval')
    cfg['_doc'] = ['VARIANT of bench/friction_families.json written by bench/friction_robust.py mkconfig; do not edit.']
    json.dump(cfg, open(FR + '/robust/cfg_split.json', 'w'), indent=1, ensure_ascii=False)
    cfg['inst_props_are_instances'] = True
    json.dump(cfg, open(FR + '/robust/cfg_splitinst.json', 'w'), indent=1, ensure_ascii=False)


def auxtargets(c):
    kind = {}
    for l in open(os.path.join(REPO, 'out/corpus', c, 'decls.jsonl')):
        d = json.loads(l)
        kind[d['name']] = (d['kind'], d.get('typeIsProp', False))
    o = os.path.join(FR, c, 'robust')
    n = Counter()
    with open(o + '/aux_targets.txt', 'w') as t, open(o + '/aux_parent.tsv', 'w') as pf:
        for l in open(o + '/a.auxlist.tsv'):
            a, p = l.rstrip('\n').split('\t')
            k = kind.get(p, ('?', False))[0]
            n['aux of ' + k] += 1
            if k != 'theorem':
                t.write(a + '\n'); pf.write(f'{a}\t{p}\t{k}\n')
        for name, (k, isp) in kind.items():
            if k != 'theorem' and isp:
                t.write(name + '\n'); pf.write(f'{name}\t{name}\t{k}:own\n'); n['Prop-typed ' + k] += 1
    json.dump(n, open(o + '/aux_counts.json', 'w'), indent=1)
    print(c, dict(n))


def merge(c, v):
    o = os.path.join(FR, c, 'robust'); sh = o + '/shards'
    rows = []
    for f in sorted(glob.glob(f'{sh}/{v}.hyps.*.jsonl')):
        for l in open(f):
            d = json.loads(l)
            m = d.get('mass') or {}
            rows.append({'name': d['name'], 'module': d['module'], 'proofSize': d.get('proofSize', 0),
                         'rootClass': d.get('rootClass'), 'chead': (d.get('concl') or {}).get('head'),
                         'nodes': m.get('nodes', 0), 'outer': m.get('outer', {}), 'inner': m.get('inner', {}),
                         'kind': m.get('kind', [0, 0, 0]), 'cast': m.get('castRegion', 0),
                         'err': d.get('massError') or d.get('stmtError')})
    rows.sort(key=lambda d: d['name'])
    with open(f'{o}/{v}.jsonl', 'w') as fh:
        for d in rows:
            fh.write(json.dumps(d, ensure_ascii=False, separators=(',', ':')) + '\n')
    heads = {}
    for f in glob.glob(f'{sh}/{v}.heads.*.jsonl'):
        for l in open(f):
            d = json.loads(l); k = (d['cls'], d['head'])
            if k in heads:
                heads[k]['mass'] += d['mass']; heads[k]['proofSubterms'] += d['proofSubterms']
            else:
                heads[k] = d
    with open(f'{o}/{v}.heads.jsonl', 'w') as fh:
        for d in sorted(heads.values(), key=lambda d: -d['mass']):
            fh.write(json.dumps(d, ensure_ascii=False, separators=(',', ':')) + '\n')
    metas = [json.load(open(f)) for f in glob.glob(f'{sh}/{v}.meta.*.json')]
    meta = {'variant': v, 'rows': len(rows), 'errors': sum(1 for r in rows if r['err']),
            'unresolved': sum(len(m['theoremsUnresolved']) for m in metas) // max(1, len(metas)),
            'listed': metas[0]['theoremsListed'] if metas else 0}
    json.dump(meta, open(f'{o}/{v}.meta.json', 'w'), indent=1)
    print(c, v, meta)


# ------------------------------------------------------------------ placeholders
def rget(R, path):
    x = R
    for k in path.split('/'):
        x = x[int(k)] if isinstance(x, list) else x[k]
    return x


def rfmt(x, mode=''):
    """{{r:path}} -> 'v [lo, hi]' for an interval triple, a rounded number otherwise; modes: p (point), d (signed)."""
    if isinstance(x, (list, tuple)) and len(x) == 3:
        v, lo, hi = x
        d = 2 if abs(v) < 10 else 1
        if mode == 'p': return f'{v:.{d}f}'
        if mode == 'd': return f'{v:+.{d}f} [{lo:+.{d}f}, {hi:+.{d}f}]'
        return f'{v:.{d}f} [{lo:.{d}f}, {hi:.{d}f}]'
    if isinstance(x, int): return f'{x:,}'
    if isinstance(x, float):
        d = 2 if abs(x) < 10 else 1
        return f'{x:+.{d}f}' if mode == 'd' else f'{x:.{d}f}'
    return str(x)


def rfill(txt, R):
    def sub(m):
        parts = [t.strip() for t in m.group(1).split('@')]
        return rfmt(rget(R, parts[0]), parts[1] if len(parts) > 1 else '')
    return re.sub(r'\{\{r:([^}]+)\}\}', sub, txt)


# ------------------------------------------------------------------ report
SEED = 20261110
LPN = {'MeasureTheory.eLpNorm', 'MeasureTheory.MemLp', 'MeasureTheory.Lp', "MeasureTheory.eLpNorm'"}
REGN = {'ContDiff', 'ContDiffOn', 'ContDiffAt', 'HasDerivAt', 'deriv', 'fderiv', 'iteratedFDeriv', 'HasFDerivAt',
        'DifferentiableAt', 'Differentiable', 'HasDerivWithinAt', 'iteratedDeriv', 'ContDiffWithinAt'}
OC = ['regularity', 'derivval', 'measurability', 'integrability', 'finiteness', 'positivity', 'support']


def load_variant(c, v):
    return {json.loads(l)['name']: json.loads(l) for l in open(f'{FR}/{c}/robust/{v}.jsonl')}


def load_stmt_sets(c):
    """per theorem: statement mentions Lp vocabulary / an integral / a derivative constant (Census.lean export)."""
    S = {}
    for f in sorted(glob.glob(f'{FR}/{c}/census/c.tab.*.jsonl')):
        tab = {}
        for l in open(f):
            r = json.loads(l); tab[r['id']] = r['name']
        for l in open(f.replace('c.tab', 'c.thm')):
            r = json.loads(l); names = {tab[i] for i in r['sc']}
            S[r['name']] = (bool(names & LPN), r['integ'] > 0, bool(names & REGN))
    return S


def load_hyps(c):
    """slim view of the baseline hyps.jsonl: Prop binders and conclusion (class, head, inst?, exRealPos)."""
    out = {}
    for l in open(f'{FR}/{c}/hyps.jsonl'):
        d = json.loads(l)
        hy = [(b['cls'], b['head'], b['kind'] == 'inst') for b in d.get('binders', []) if b.get('isProp')]
        cc = d.get('concl') or {}
        out[d['name']] = (hy, cc.get('cls'), cc.get('head'), cc.get('exRealPos', 0))
    return out


def report(B):
    import numpy as np
    rng = np.random.default_rng(SEED)
    R = {'B': B, 'seed': SEED}
    L = []
    CS = ['ns', 'carleson', 'pfr']
    cols = (['nodes'] + ['o_' + k for k in OC] + ['i_' + k for k in OC] + ['i_eq', 'i_tc', 'i_order', 'k_spine', 'k_data', 'k_inst', 'cast',
            'root_dv', 'root_reg', 'root_reg_inst', 'root_reg_i_reg', 'root_reg_i_eq', 'root_reg_i_tc', 'root_reg_k0', 'root_reg_k1'])
    ci = {k: i for i, k in enumerate(cols)}

    def matrix(rows, names):
        X = np.zeros((len(names), len(cols)))
        for r, n in enumerate(names):
            d = rows[n]
            X[r, 0] = d['nodes']
            for k in OC:
                X[r, ci['o_' + k]] = d['outer'].get(k, 0); X[r, ci['i_' + k]] = d['inner'].get(k, 0)
            for k in ('eq', 'tc', 'order'):
                X[r, ci['i_' + k]] = d['inner'].get(k, 0)
            X[r, ci['k_spine']], X[r, ci['k_data']], X[r, ci['k_inst']] = d['kind']
            X[r, ci['cast']] = d['cast']
            if d['rootClass'] == 'derivval': X[r, ci['root_dv']] = d['nodes']
            if d['rootClass'] in ('derivval', 'regularity'):
                X[r, ci['root_reg']] = d['nodes']; X[r, ci['root_reg_inst']] = d['kind'][2]
                X[r, ci['root_reg_i_reg']] = d['inner'].get('regularity', 0) + d['inner'].get('derivval', 0)
                X[r, ci['root_reg_i_eq']] = d['inner'].get('eq', 0); X[r, ci['root_reg_i_tc']] = d['inner'].get('tc', 0)
                X[r, ci['root_reg_k0']] = d['kind'][0]; X[r, ci['root_reg_k1']] = d['kind'][1]
        return X

    def boots(X):
        n = len(X)
        out = np.zeros((B, X.shape[1]))
        for b in range(B):
            out[b] = X[rng.integers(0, n, n)].sum(axis=0)
        return out

    def val(s, num, den=('nodes',)):
        a = sum(s[..., ci[k]] for k in num); b = sum(s[..., ci[k]] for k in den)
        return 100 * a / np.where(b > 0, b, 1)

    def cell(G, g, num, den=('nodes',)):
        v = float(val(G[g][0], num, den)); d = val(G[g][1], num, den)
        return v, float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))

    def dcell(G, a, b, num, den=('nodes',)):
        v = float(val(G[a][0], num, den) - val(G[b][0], num, den)); d = val(G[a][1], num, den) - val(G[b][1], num, den)
        return v, float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))

    def f(t, sign=False):
        v, lo, hi = t
        d = 2 if abs(v) < 10 else 1
        return (f'{v:+.{d}f} [{lo:+.{d}f}, {hi:+.{d}f}]' if sign else f'{v:.{d}f} [{lo:.{d}f}, {hi:.{d}f}]')

    V = {c: {v: load_variant(c, v) for v in ('split', 'splitinst')} for c in CS}
    names = {c: sorted(V[c]['split']) for c in CS}
    Xs = {c: matrix(V[c]['split'], names[c]) for c in CS}
    Xi = {c: matrix(V[c]['splitinst'], names[c]) for c in CS}
    G = {c: (Xs[c].sum(axis=0), boots(Xs[c])) for c in CS}
    Gi = {c: (Xi[c].sum(axis=0), boots(Xi[c])) for c in CS}

    # consistency with the baseline export: regularity + derivval (split) == regularity (baseline), nodes equal
    base = {}
    chk = {}
    for c in CS:
        o = Counter(); n = 0; hy = 0
        for l in open(f'{FR}/{c}/hyps.jsonl'):
            d = json.loads(l); m = d.get('mass') or {}
            n += m.get('nodes', 0)
            for k, v in m.get('outer', {}).items(): o[k] += v
        base[c] = (n, o)
        s = G[c][0]
        chk[c] = {'nodes_baseline': n, 'nodes_split': float(s[0]),
                  'side_total_baseline': round(sum(o[k] for k in SIDE0), 1),
                  'side_total_split': round(float(sum(s[ci['o_' + k]] for k in OC)), 1),
                  'regularity_baseline': round(o['regularity'], 1),
                  'regularity_plus_derivval_split': round(float(s[ci['o_regularity']] + s[ci['o_derivval']]), 1)}
    R['consistency'] = chk

    def table(title, rows, GG=G, note=None):
        L.append(f'### {title}'); L.append('')
        if note: L.append(note); L.append('')
        L.append('| % of proof-term nodes | ns (machine) | Carleson (human) | ns − Carleson | PFR (human) |'); L.append('|---|---|---|---|---|')
        for key, label, num, den in rows:
            cs = {c: cell(GG, c, num, den) for c in CS}; dd = dcell(GG, 'ns', 'carleson', num, den)
            R.setdefault('rows', {})[key] = {**{c: cs[c] for c in CS}, 'ns-carleson': dd}
            L.append(f'| {label} | {f(cs["ns"])} | {f(cs["carleson"])} | {f(dd, True)} | {f(cs["pfr"])} |')
        L.append('')

    N = ('nodes',)
    Dall = ['o_regularity', 'o_derivval', 'o_measurability', 'o_integrability']
    Iall = ['i_regularity', 'i_derivval', 'i_measurability', 'i_integrability']
    L.append('## 1. Claim D under four defensible rules (review findings 1 and 2)'); L.append('')
    L.append('Two choices were made silently in the first census: (a) facts that state *what a derivative is* (`HasDerivAt f f\' x`, `HasFDerivAt`, … — list in `bench/friction_robust.py`) were counted as regularity side conditions; (b) mass was charged with the `outer` label, under which everything below a side goal, including the rewriting and instance terms used to prove it, belongs to that side condition. The `inner` label charges a node to the nearest enclosing goal only. Both labels were always in the export; the split of (a) is a rerun of the exporter with one extra class (`robust_run.sh <corpus> split`). Regularity + derivative-value under the split equals baseline regularity to within 0.15% in every corpus, and node counts are identical (`robust.json: consistency`; the residue is the fractional-share rule applied to one more label).'); L.append('')
    table('outer label (everything below a side goal)', [
        ('o.reg_all', 'regularity incl. derivative-value facts (the census headline)', ['o_regularity', 'o_derivval'], N),
        ('o.dv', '… derivative-value facts (`HasDerivAt` family)', ['o_derivval'], N),
        ('o.reg', '… smoothness / continuity proper', ['o_regularity'], N),
        ('o.mi', 'measurability + integrability', ['o_measurability', 'o_integrability'], N),
        ('o.D_all', 'claim D, derivative-value facts counted', Dall, N),
        ('o.D', 'claim D, derivative-value facts not counted', ['o_regularity', 'o_measurability', 'o_integrability'], N),
        ('root.dv', 'stand-alone lemmas whose conclusion is a derivative-value fact (whole proof)', ['root_dv'], N)])
    table('inner label (nearest enclosing goal only)', [
        ('i.reg_all', 'regularity incl. derivative-value facts', ['i_regularity', 'i_derivval'], N),
        ('i.dv', '… derivative-value facts', ['i_derivval'], N),
        ('i.reg', '… smoothness / continuity proper', ['i_regularity'], N),
        ('i.mi', 'measurability + integrability', ['i_measurability', 'i_integrability'], N),
        ('i.D_all', 'claim D, derivative-value facts counted', Iall, N),
        ('i.D', 'claim D, derivative-value facts not counted', ['i_regularity', 'i_measurability', 'i_integrability'], N)])
    table('what is inside the stand-alone regularity / derivative-value lemmas', [
        ('rr.share', 'their share of all nodes', ['root_reg'], N),
        ('rr.i_reg', 'of their nodes: directly under a regularity / derivative goal', ['root_reg_i_reg'], ('root_reg',)),
        ('rr.i_eq', 'of their nodes: under an equation goal', ['root_reg_i_eq'], ('root_reg',)),
        ('rr.i_tc', 'of their nodes: under a type-class goal', ['root_reg_i_tc'], ('root_reg',)),
        ('rr.k0', 'of their nodes: proof spine', ['root_reg_k0'], ('root_reg',)),
        ('rr.k1', 'of their nodes: data terms', ['root_reg_k1'], ('root_reg',)),
        ('rr.k2', 'of their nodes: instance arguments', ['root_reg_inst'], ('root_reg',))])

    L.append('## 2. Side-condition classes without instance synthesis (review finding 8)'); L.append('')
    L.append('Variant `splitinst`: a Prop-valued instance-implicit argument (`NeZero`, `Nat.AtLeastTwo` on numerals, `BorelSpace`, `IsFiniteMeasure` found by instance search, …) is treated as an instance argument, not as a side-condition proof. Outer label. "with" is the `split` variant (same rule as the census), "without" is `splitinst`.'); L.append('')
    L.append('| % of proof-term nodes | ns with | ns without | Carleson with | Carleson without | PFR with | PFR without |'); L.append('|---|---|---|---|---|---|---|')
    for k in ('positivity', 'measurability', 'integrability', 'finiteness', 'regularity', 'derivval'):
        cells = []
        for c in CS:
            a = cell(G, c, ['o_' + k], N); b = cell(Gi, c, ['o_' + k], N)
            R.setdefault('inst', {}).setdefault(k, {})[c] = {'with': a, 'without': b}
            cells += [f(a), f(b)]
        L.append(f'| {k} | ' + ' | '.join(cells) + ' |')
    dpos = dcell(Gi, 'ns', 'carleson', ['o_positivity'], N); R['inst']['positivity']['ns-carleson without'] = dpos
    L.append(''); L.append(f'Positivity without instance arguments, ns − Carleson: {f(dpos, True)}.'); L.append('')
    table('claim D without instance synthesis', [
        ('ni.D_all', 'claim D outer, derivative-value facts counted', Dall, N),
        ('ni.D', 'claim D outer, derivative-value facts not counted', ['o_regularity', 'o_measurability', 'o_integrability'], N),
        ('ni.mi', 'measurability + integrability, outer', ['o_measurability', 'o_integrability'], N),
        ('ni.fin', 'finiteness, outer', ['o_finiteness'], N)], GG=Gi)

    # ---- matched stratum
    L.append('## 3. Matched subject stratum (review finding 3)'); L.append('')
    L.append('The first census\'s subject control ("statement mentions any `Mathlib.MeasureTheory` constant") was too loose. Stratum here, from the statement\'s constant set (`Census.lean`): the statement mentions `eLpNorm` / `MemLp` / `Lp` or contains an integral, and mentions no derivative or `ContDiff` constant. Outer label, baseline rule (derivative-value facts inside regularity).'); L.append('')
    strata = {}
    for c in ('ns', 'carleson'):
        S = load_stmt_sets(c)
        nm = names[c]
        fl = np.array([S.get(n, (False, False, False)) for n in nm])
        strata[c] = {'matched': (fl[:, 0] | fl[:, 1]) & ~fl[:, 2], 'lp': fl[:, 0], 'lp_or_int': fl[:, 0] | fl[:, 1]}
        strata[c]['mods'] = {k: len({V[c]['split'][n]['module'] for n, m in zip(nm, strata[c][k]) if m}) for k in ('matched', 'lp', 'lp_or_int')}
    for key, title in (('matched', 'Lp or integral in the statement, no derivative constant'), ('lp', 'Lp vocabulary in the statement'), ('lp_or_int', 'Lp or integral in the statement (derivatives allowed)')):
        GM = {c: (Xs[c][strata[c][key]].sum(axis=0), boots(Xs[c][strata[c][key]])) for c in ('ns', 'carleson')}
        ns_n, ca_n = int(strata['ns'][key].sum()), int(strata['carleson'][key].sum())
        tot_share = float(Xs['ns'][strata['ns'][key], 0].sum() / Xs['ns'][:, 0].sum() * 100)
        L.append(f'### {title}'); L.append('')
        L.append(f'ns {ns_n:,} theorems in {strata["ns"]["mods"][key]:,} modules ({ns_n / len(names["ns"]) * 100:.1f}% of theorems, {tot_share:.1f}% of proof nodes); Carleson {ca_n:,} in {strata["carleson"]["mods"][key]}.'); L.append('')
        L.append('| % of proof-term nodes in the stratum | ns | Carleson | ns − Carleson |'); L.append('|---|---|---|---|')
        R.setdefault('matched', {})[key] = {'n': {'ns': ns_n, 'carleson': ca_n}, 'ns_share_of_nodes': tot_share}
        for sk, label, num in (('reg_all', 'regularity (incl. derivative-value facts)', ['o_regularity', 'o_derivval']),
                               ('mi', 'measurability + integrability', ['o_measurability', 'o_integrability']),
                               ('mif', 'measurability + integrability + finiteness (the chat\'s packet)', ['o_measurability', 'o_integrability', 'o_finiteness']),
                               ('fin', 'finiteness', ['o_finiteness']), ('pos', 'positivity', ['o_positivity']),
                               ('cast', 'cast region (upper bound)', ['cast']), ('inst', 'instance arguments', ['k_inst'])):
            a, b, d = cell(GM, 'ns', num, N), cell(GM, 'carleson', num, N), dcell(GM, 'ns', 'carleson', num, N)
            R['matched'][key][sk] = {'ns': a, 'carleson': b, 'ns-carleson': d}
            L.append(f'| {label} | {f(a)} | {f(b)} | {f(d, True)} |')
        L.append('')
        if key == 'matched':
            GMi = {c: (Xi[c][strata[c][key]].sum(axis=0), boots(Xi[c][strata[c][key]])) for c in ('ns', 'carleson')}
            num = ['o_measurability', 'o_integrability', 'o_finiteness']
            a, b, d = cell(GMi, 'ns', num, N), cell(GMi, 'carleson', num, N), dcell(GMi, 'ns', 'carleson', num, N)
            R['matched'][key]['mif_noinst'] = {'ns': a, 'carleson': b, 'ns-carleson': d}
            L.append(f'Same stratum with Prop instance arguments not counted (variant `splitinst`): measurability + integrability + finiteness {f(a)} in ns, {f(b)} in Carleson, difference {f(d, True)}.'); L.append('')

    # ---- size standardisation of the instance share
    L.append('## 4. Instance-argument share, standardised for proof size (review finding 7)'); L.append('')
    edges = [0, 100, 300, 1000, 3000, 10000, 10 ** 12]
    lab = ['under 100', '100–300', '300–1k', '1k–3k', '3k–10k', 'over 10k']
    bins = {}
    for c in ('ns', 'carleson'):
        X = Xs[c]; b = np.digitize(X[:, 0], edges[1:-1])
        bins[c] = [(X[b == k, 0].sum(), X[b == k, ci['k_inst']].sum()) for k in range(6)]
    tot = {c: sum(m for m, _ in bins[c]) for c in bins}
    raw = {c: 100 * sum(i for _, i in bins[c]) / tot[c] for c in bins}
    std = sum((bins['carleson'][k][0] / tot['carleson']) * (bins['ns'][k][1] / bins['ns'][k][0]) for k in range(6) if bins['ns'][k][0] > 0) * 100
    std_rev = sum((bins['ns'][k][0] / tot['ns']) * (bins['carleson'][k][1] / bins['carleson'][k][0]) for k in range(6) if bins['carleson'][k][0] > 0) * 100
    L.append('| proof size (nodes) | ns: share of mass in bin | ns: instance % | Carleson: share of mass in bin | Carleson: instance % |'); L.append('|---|---|---|---|---|')
    for k in range(6):
        L.append(f'| {lab[k]} | {100 * bins["ns"][k][0] / tot["ns"]:.1f} | {100 * bins["ns"][k][1] / max(1, bins["ns"][k][0]):.1f} | {100 * bins["carleson"][k][0] / tot["carleson"]:.1f} | {100 * bins["carleson"][k][1] / max(1, bins["carleson"][k][0]):.1f} |')
    ov = cell(G, 'ns', ['root_reg_inst'], N)
    R['inst_size'] = {'raw': raw, 'ns_at_carleson_size_mix': std, 'carleson_at_ns_size_mix': std_rev,
                      'excess_raw': raw['ns'] - raw['carleson'], 'excess_std': std - raw['carleson'], 'excess_std_rev': raw['ns'] - std_rev,
                      'overlap_inst_in_standalone_regularity': ov}
    L.append('')
    L.append(f'- Raw: ns {raw["ns"]:.1f}%, Carleson {raw["carleson"]:.1f}%, excess {raw["ns"] - raw["carleson"]:+.1f} points.')
    L.append(f'- ns reweighted to Carleson\'s distribution of proof mass over size bins: {std:.1f}%, excess {std - raw["carleson"]:+.1f} points. Carleson reweighted to ns\'s: {std_rev:.1f}%, excess {raw["ns"] - std_rev:+.1f} points.')
    L.append(f'- Measured overlap with the regularity excess: instance arguments inside stand-alone regularity / derivative-value lemmas are {f(ov)}% of all ns nodes.')
    L.append('- Not controlled: Lean 4.34 against 4.36 and the Mathlib versions, which change how instances elaborate.'); L.append('')

    # ---- project predicates
    L.append('## 5. What the project-defined predicates contain (review finding 4)'); L.append('')
    L.append('The census classed every project-defined predicate as `other`. `robust_run.sh <corpus> preds` opens each one at Expr level: definitions are δ-unfolded with their arguments, structures are replaced by their field types, recursively (depth 8), through ∧ / ∀ / ∃; each atom reached is classified by the usual rule. "Contains" below means at least one atom of that class is reached.'); L.append('')
    SIDE = set(SIDE0) | {'derivval'}
    for c in ('ns', 'carleson'):
        P = {}; P2 = {}
        for l in open(f'{FR}/{c}/robust/p.preds8.jsonl'):
            d = json.loads(l); P[d['name']] = d
        for l in open(f'{FR}/{c}/robust/p.preds2.jsonl'):
            d = json.loads(l); P2[d['name']] = d
        H = load_hyps(c)
        def flags(h):
            d = P.get(h)
            if d is None: return None
            cl = d['classes']
            return {'reg': bool(cl.get('regularity') or cl.get('derivval')), 'mi': bool(cl.get('measurability') or cl.get('integrability')),
                    'exC': d['exRealPos'] > 0, 'exC2': P2[h]['exRealPos'] > 0, 'side': any(k in SIDE for k in cl), 'unres': bool(d['unresolved']),
                    'regexC': bool(cl.get('regularity') or cl.get('derivval')) and d['exRealPos'] > 0,
                    'D': bool(cl.get('regularity') or cl.get('derivval') or cl.get('measurability') or cl.get('integrability'))}
        nH = 0; hc = Counter(); heads = Counter()
        for n, (hy, _, _, _) in H.items():
            for cls, head, inst in hy:
                nH += 1
                if cls != 'other': continue
                hc['other'] += 1
                fl = flags(head)
                if fl is None: hc['not_in_table'] += 1; continue
                hc['in_table'] += 1
                for k, v in fl.items():
                    if v: hc[k] += 1
                if fl['D'] or fl['exC']: heads[head] += 1
        # conclusions / mass
        X = Xs[c]; idx = {n: i for i, n in enumerate(names[c])}
        mc = Counter(); tc = Counter(); totn = X[:, 0].sum(); extraD = 0.0; hidden_exC = 0; hidden_exC2 = 0; base_exC = 0; mA = Counter()
        for n, (_, ccls, chead, cex) in H.items():
            i = idx[n]
            if cex > 0: base_exC += 1; mA['direct'] += X[i, 0]
            if ccls != 'other': continue
            mc['other'] += X[i, 0]; tc['other'] += 1
            fl = flags(chead)
            if fl is None: mc['not_in_table'] += X[i, 0]; tc['not_in_table'] += 1; continue
            for k, v in fl.items():
                if v: mc[k] += X[i, 0]; tc[k] += 1
            if fl['D']:
                extraD += X[i, 0] - sum(X[i, ci[k]] for k in Dall)
            if fl['exC'] and cex == 0: hidden_exC += 1; mA['deep'] += X[i, 0]
            if fl['exC2'] and cex == 0: hidden_exC2 += 1; mA['shallow'] += X[i, 0]
        pct = lambda a, b: round(100 * a / b, 2) if b else 0.0
        Dall_now = float(sum(X[:, ci[k]].sum() for k in Dall) / totn * 100)
        res = {'predicates': len(P), 'structures': sum(1 for d in P.values() if d['kind'] == 'structure'),
               'pred_with_D_atom': sum(1 for h in P if flags(h)['D']), 'pred_with_exC': sum(1 for h in P if flags(h)['exC']),
               'pred_with_reg_and_exC': sum(1 for h in P if flags(h)['regexC']),
               'hyps': nH, 'hyp_pct': {k: pct(v, nH) for k, v in hc.items()},
               'concl_theorems': dict(tc), 'concl_mass_pct': {k: pct(v, totn) for k, v in mc.items()},
               'D_outer_all': round(Dall_now, 2), 'D_upper_bound': round(Dall_now + 100 * extraD / totn, 2),
               'exC_producers_direct': base_exC, 'exC_producers_hidden': hidden_exC, 'exC_producers_hidden_shallow': hidden_exC2,
               'exC_mass_pct': {k: pct(v, totn) for k, v in mA.items()},
               'top_heads': heads.most_common(12)}
        R.setdefault('preds', {})[c] = res
        L.append(f'### {c}'); L.append('')
        L.append(f'- {res["predicates"]:,} project-defined predicates (non-class, Prop-valued definitions and structures); {res["pred_with_D_atom"]:,} contain a regularity, measurability or integrability atom, {res["pred_with_exC"]:,} hide a real `∃ C` with a sign conjunct, {res["pred_with_reg_and_exC"]:,} both.')
        hp = res['hyp_pct']
        L.append(f'- Hypotheses ({nH:,} Prop binders): `other` is {hp.get("other", 0)}%; in the predicate table {hp.get("in_table", 0)}%. Of all Prop binders: {hp.get("reg", 0)}% are a project predicate containing a regularity fact, {hp.get("mi", 0)}% one containing measurability / integrability, {hp.get("exC", 0)}% one hiding an `∃ C` with sign, {hp.get("regexC", 0)}% both smoothness and a hidden constant; {hp.get("side", 0)}% contain any side-condition atom. {hp.get("unres", 0)}% bottom out in something the scan could not open; {hp.get("not_in_table", 0)}% have a head that is not a project predicate (a variable, a library predicate without a class).')
        cm = res['concl_mass_pct']
        L.append(f'- Theorems whose conclusion is `other`: {cm.get("other", 0)}% of proof nodes. Concluding a predicate that contains a regularity fact: {cm.get("reg", 0)}% of nodes ({tc.get("reg", 0):,} theorems); measurability / integrability: {cm.get("mi", 0)}% ({tc.get("mi", 0):,}); a hidden `∃ C`: {cm.get("exC", 0)}% ({tc.get("exC", 0):,}).')
        L.append(f'- Claim D (outer, derivative-value facts counted) is {res["D_outer_all"]}% by the census rule. If every theorem concluding a predicate with a regularity / measurability / integrability atom were charged whole to D, it would be {res["D_upper_bound"]}%. That is an upper bound, not an estimate: such a predicate usually also contains bounds and equations.')
        ma = res['exC_mass_pct']
        L.append(f'- `∃ C` producers: {base_exC:,} theorems state `∃ C, 0 < C ∧ …` (or `0 ≤ C`) directly ({ma.get("direct", 0)}% of proof nodes). A further {hidden_exC2:,} conclude a predicate that hides one within two levels of unfolding ({ma.get("shallow", 0)}% of nodes), and {hidden_exC:,} one that hides it at any depth ({ma.get("deep", 0)}%). Hypotheses that are a predicate hiding an `∃ C` within two levels: {hp.get("exC2", 0)}% of Prop binders.')
        if res['top_heads']:
            L.append('- Commonest such predicates among hypotheses: ' + ', '.join(f'`{h}` ({n:,})' for h, n in res['top_heads'][:8]) + '.')
        L.append('')

    # ---- proofs outside theorems
    L.append('## 6. Proofs outside `kind == theorem` (review finding 5)'); L.append('')
    L.append('The census exported theorems only. Proofs also sit in the auxiliary theorem constants Lean generates for definitions, instances and structures (`foo._proof_3`: the proof obligations of a bundled object or of a definition that takes proof arguments) and in Prop-typed non-theorem declarations. `robust_run.sh <corpus> aux` runs the same exporter (split rule) on those constants. The 18.5% the review gave for ns used the size fields of the corpus export, which also count the data terms of definitions and compiler-generated lemmas; on the node measure used everywhere else in the census, and counting author-written proof obligations only, the figure is below.'); L.append('')
    L.append('| | ns | Carleson | PFR |'); L.append('|---|---|---|---|')
    A = {}
    for c in CS:
        rows_all = load_variant(c, 'aux')
        par = {}
        for l in open(f'{FR}/{c}/robust/aux_parent.tsv'):
            a, p, k = l.rstrip('\n').split('\t'); par[a] = k
        # author-written proof obligations only: `_proof_N` auxiliaries and Prop-typed declarations.
        # Compiler-generated lemmas (eq_N, eq_def, injEq, inj, sizeOf_spec, congr_simp, ...) are left out.
        keep = lambda n: par.get(n, '').endswith(':own') or re.search(r'(^|\.)_?proof_\d+$', n) is not None
        rows = {n: d for n, d in rows_all.items() if keep(n)}
        gen_nodes = sum(d['nodes'] for n, d in rows_all.items() if not keep(n))
        gen_n = len(rows_all) - len(rows)
        nm = sorted(rows); Xa = matrix(rows, nm)
        s = Xa.sum(axis=0); t = Xs[c].sum(axis=0)
        bk = Counter()
        for n, x in zip(nm, Xa[:, 0]): bk[par.get(n, '?').split(':')[0]] += x
        comb = s + t
        A[c] = {'generated_excluded': gen_n, 'generated_nodes': gen_nodes, 'proofSize_units': sum(d['proofSize'] for d in rows.values()), 'targets': len(nm), 'errors': sum(1 for r in rows.values() if r['err']), 'aux_nodes': float(s[0]), 'theorem_nodes': float(t[0]),
                'aux_share_of_all_proof_nodes': float(100 * s[0] / (s[0] + t[0])),
                'by_parent_kind_pct': {k: round(100 * v / s[0], 1) for k, v in bk.most_common()},
                'outer': {k: round(float(100 * s[ci['o_' + k]] / s[0]), 2) for k in OC},
                'inner': {k: round(float(100 * s[ci['i_' + k]] / s[0]), 2) for k in OC + ['eq', 'tc', 'order']},
                'kind_inst': round(float(100 * s[ci['k_inst']] / s[0]), 2),
                'D_all_aux': round(float(100 * sum(s[ci[k]] for k in Dall) / s[0]), 2),
                'D_all_theorems': round(float(100 * sum(t[ci[k]] for k in Dall) / t[0]), 2),
                'D_all_combined': round(float(100 * sum(comb[ci[k]] for k in Dall) / comb[0]), 2),
                'D_inner_aux': round(float(100 * sum(s[ci[k]] for k in Iall) / s[0]), 2),
                'D_inner_combined': round(float(100 * sum(comb[ci[k]] for k in Iall) / comb[0]), 2),
                'reg_all_combined': round(float(100 * (comb[ci['o_regularity']] + comb[ci['o_derivval']]) / comb[0]), 2),
                'inst_combined': round(float(100 * comb[ci['k_inst']] / comb[0]), 2),
                'pos_aux': round(float(100 * s[ci['o_positivity']] / s[0]), 2)}
    R['aux'] = A
    row = lambda label, fn: L.append(f'| {label} | ' + ' | '.join(fn(A[c]) for c in CS) + ' |')
    row('proof constants counted (failures)', lambda a: f'{a["targets"]:,} ({a["errors"]})')
    row('compiler-generated lemmas exported but left out (`eq_N`, `injEq`, `sizeOf_spec`, `congr_simp`, …): constants, nodes', lambda a: f'{a["generated_excluded"]:,}, {a["generated_nodes"]:,}')
    row('their proof nodes as % of all proof nodes (theorems + these)', lambda a: f'{a["aux_share_of_all_proof_nodes"]:.1f}')
    row('… by kind of parent declaration (%)', lambda a: ', '.join(f'{k} {v}' for k, v in a['by_parent_kind_pct'].items()))
    row('claim D outer in these proofs / in theorems / combined', lambda a: f'{a["D_all_aux"]} / {a["D_all_theorems"]} / {a["D_all_combined"]}')
    row('claim D inner in these proofs / combined', lambda a: f'{a["D_inner_aux"]} / {a["D_inner_combined"]}')
    row('regularity outer (incl. derivative-value) in these proofs', lambda a: f'{a["outer"]["regularity"] + a["outer"]["derivval"]:.2f}')
    row('measurability + integrability outer in these proofs', lambda a: f'{a["outer"]["measurability"] + a["outer"]["integrability"]:.2f}')
    row('positivity outer in these proofs', lambda a: f'{a["pos_aux"]}')
    row('finiteness outer in these proofs', lambda a: f'{a["outer"]["finiteness"]}')
    row('nearest goal is an equation, in these proofs', lambda a: f'{a["inner"]["eq"]}')
    row('instance arguments in these proofs / combined', lambda a: f'{a["kind_inst"]} / {a["inst_combined"]}')
    L.append('')

    json.dump(R, open(FR + '/robust.json', 'w'), indent=1, ensure_ascii=False)
    head = open(os.path.join(REPO, 'bench/friction_robust_head.md')).read() if os.path.exists(os.path.join(REPO, 'bench/friction_robust_head.md')) else '# Friction census: robustness\n'
    head = rfill(head, json.load(open(FR + '/robust.json')))
    open(FR + '/ROBUSTNESS.md', 'w').write(head.rstrip() + '\n\n---\n\n# Tables\n\nGenerated by `bench/friction_robust.py report` (B = %d theorem bootstraps, seed %d). Cells are `value [2.5%%, 97.5%%]`.\n\n' % (B, SEED) + '\n'.join(L) + '\n')
    print(json.dumps(R['consistency'], indent=1))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'mkconfig': mkconfig()
    elif cmd == 'auxtargets': auxtargets(sys.argv[2])
    elif cmd == 'merge': merge(sys.argv[2], sys.argv[3])
    elif cmd == 'report': report(int(sys.argv[sys.argv.index('--B') + 1]) if '--B' in sys.argv else 1000)
