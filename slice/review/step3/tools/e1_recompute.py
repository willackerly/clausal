"""Reviewer's recomputation of the E1 detection table from compare/e1/results/raw and compare/results/results.json.
Written from the raw field names, not from analyse.py's aggregation code. Also gives a strict variant that counts only
a concrete failing input (no hang, no Kani failure without a reproduced input)."""
import json, glob, os, collections
C = '/Users/will/dev/lean-rosette/slice/compare/'
k2 = json.load(open(C + 'results/results.json'))
rules = json.load(open(C + 'rules.json'))['rules']
raw = {os.path.basename(p)[:-5]: json.load(open(p)) for p in glob.glob(C + 'e1/results/raw/*.json')}
print('raw files', len(raw), 'k2 mutants', len(k2['mutants']))
def gen(ev, reading, strict=False):
    r = ev['readings'].get(reading)
    if r is None: return None
    ps = r['property']['status']
    prop = ps == 'fail' or (ps == 'hang' and not strict)
    rungs = r['bounded'].get('rungs') or []
    failed = any(g['status'] == 'failed' for g in rungs)
    rep = r['bounded'].get('replay')
    if strict:
        kani = failed and rep == 'fails'
    else:
        kani = failed and rep not in ('holds', 'out-of-scope', 'mismatch')
    return prop, kani, ps, rep, [g['status'] for g in rungs]
reps = collections.Counter(); pstat = collections.Counter()
rows = collections.defaultdict(lambda: collections.Counter())
pairs = collections.defaultdict(lambda: collections.Counter())
lost = []
for strict in (False, True):
    rows = collections.defaultdict(collections.Counter); pairs = collections.defaultdict(collections.Counter)
    for m in k2['mutants']:
        if m['id'] not in raw: print('MISSING', m['id']); continue
        ev = raw[m['id']]['evidence']
        sets = []
        s = 'tool' if m['set'] == 'cargo-mutants' else 'hand'
        any_k2 = any_gp = any_gk = any_hand = False
        for r in rules:
            if r['crate'] != m['crate']: continue
            det = m['rules'][r['id']]
            k2arms = {a: bool(det[a]['detected']) for a in ('a', 'b_plain', 'b_edge', 'c', 'd') if a in det}
            g = gen(ev, f"Spec.{r['crate']}.{r['id']}", strict)
            if not strict:
                reps[g[3]] += 1; pstat[g[2]] += 1
            gp, gk = g[0], g[1]
            if any(k2arms.values()):
                pairs[s]['k2any'] += 1
                pairs[s]['edge'] += k2arms.get('b_edge', False)
                pairs[s]['kani'] += k2arms.get('c', False)
                pairs[s]['gp'] += gp; pairs[s]['gk'] += gk; pairs[s]['ge'] += gp or gk
                if (k2arms.get('b_edge') or k2arms.get('b_plain') or k2arms.get('c')) and not (gp or gk):
                    lost.append((strict, m['id'], r['id']))
            elif gp or gk:
                pairs[s]['gen_only'] += 1
            any_k2 |= any(k2arms.values()); any_gp |= gp; any_gk |= gk
        rows[(s, m['crate'])]['n'] += 1
        rows[(s, m['crate'])]['k2'] += any_k2
        rows[(s, m['crate'])]['gp'] += any_gp; rows[(s, m['crate'])]['gk'] += any_gk; rows[(s, m['crate'])]['ge'] += any_gp or any_gk
    print('\nSTRICT' if strict else '\nAS DEFINED IN E1')
    for k in sorted(rows): print(' mutants', k, dict(rows[k]))
    for k in pairs: print(' pairs', k, dict(pairs[k]))
print('lost pairs (k2 hand arm found, generated did not):', lost)
print('replay values', reps); print('property statuses', pstat)
