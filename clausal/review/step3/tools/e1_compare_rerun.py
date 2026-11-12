"""Compare the reviewer's rerun of a seeded sample of E1 mutants (scratch copy work2) with the stored raw results."""
import json, glob, os, sys
C = '/Users/will/dev/lean-rosette/clausal/compare/'
N = '/Users/will/dev/lean-rosette/clausal/review/step3/work2/compare/e1/results/raw/'
rules = json.load(open(C + 'rules.json'))['rules']
K2R = {f"Spec.{r['crate']}.{r['id']}" for r in rules}
CAND = {'Rule.ledger_rules.k2_whole_agrees_with_batch', 'Rule.ledger_rules.k2_batch_agrees_with_transfers'}
def flags(r):
    p = r['property']['status'] in ('fail', 'hang')
    rg = r['bounded'].get('rungs') or []
    k = any(g['status'] == 'failed' for g in rg) and r['bounded'].get('replay') not in ('holds', 'out-of-scope', 'mismatch')
    return p, k
tot = dict(same=0, diff=0)
for p in sorted(glob.glob(N + '*.json')):
    mid = os.path.basename(p)[:-5]
    new = json.load(open(p)); old = json.load(open(C + 'e1/results/raw/' + mid + '.json'))
    ne, oe = new['evidence']['readings'], old['evidence']['readings']
    diffs = []
    for rid in sorted(set(ne) | set(oe)):
        if rid not in ne or rid not in oe:
            diffs.append((rid, 'missing in one')); continue
        a, b = flags(oe[rid]), flags(ne[rid])
        if a != b:
            diffs.append((rid, 'old prop/kani', a, 'new', b, [g['status'] for g in oe[rid]['bounded'].get('rungs') or []], [g['status'] for g in ne[rid]['bounded'].get('rungs') or []]))
    # the unit of the E1 table: the 23 rules and the candidates
    det_old = sorted(r for r in oe if r in K2R | CAND and any(flags(oe[r])))
    det_new = sorted(r for r in ne if r in K2R | CAND and any(flags(ne[r])))
    same_det = det_old == det_new
    tot['same' if same_det else 'diff'] += 1
    print(f"{mid}: readings {len(ne)}; K2-rule/candidate detections old {len(det_old)} new {len(det_new)} {'SAME' if same_det else 'DIFFERENT'}; per-reading flag differences {len(diffs)}")
    for d in diffs[:8]: print('   ', d)
print(tot)
