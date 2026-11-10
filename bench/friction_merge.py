#!/usr/bin/env python3
"""Merge the shards of a friction export and write the coverage report.

usage: friction_merge.py <ns|carleson|pfr>
reads  out/corpus/friction/<corpus>/shards/f.{hyps,consts,heads}.<k>.jsonl, f.meta.<k>.json
writes out/corpus/friction/<corpus>/{hyps.jsonl,consts.jsonl,heads.jsonl,export_meta.json,coverage.json,COVERAGE.md}
"""
import glob, json, os, sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pct(a, b):
    return 0.0 if not b else round(100.0 * a / b, 2)


def r0(x):
    return int(round(x))


def main(corpus):
    o = os.path.join(REPO, 'out/corpus/friction', corpus)
    sh = os.path.join(o, 'shards')
    cfg = json.load(open(os.path.join(REPO, 'bench/friction_families.json')))
    side = cfg['side_condition_classes']
    primary = set(l.rstrip('\n') for l in open(o + '/primary.txt'))

    # ---- hyps
    rows = []
    for f in sorted(glob.glob(sh + '/f.hyps.*.jsonl')):
        with open(f) as fh:
            rows += [json.loads(l) for l in fh if l.strip()]
    rows.sort(key=lambda d: d['name'])
    with open(o + '/hyps.jsonl', 'w') as fh:
        for d in rows:
            fh.write(json.dumps(d, ensure_ascii=False, separators=(',', ':')) + '\n')

    # ---- consts (sum over shards)
    consts = {}
    for f in glob.glob(sh + '/f.consts.*.jsonl'):
        for l in open(f):
            d = json.loads(l)
            c = consts.get(d['name'])
            if c is None:
                consts[d['name']] = d
            else:
                for k in ('dag', 'tree', 'theorems'):
                    c[k] += d[k]
    clist = sorted(consts.values(), key=lambda d: -d['dag'])
    with open(o + '/consts.jsonl', 'w') as fh:
        for d in clist:
            fh.write(json.dumps(d, ensure_ascii=False, separators=(',', ':')) + '\n')

    # ---- heads
    heads = {}
    for f in glob.glob(sh + '/f.heads.*.jsonl'):
        for l in open(f):
            d = json.loads(l)
            k = (d['cls'], d['head'])
            h = heads.get(k)
            if h is None:
                heads[k] = d
            else:
                h['mass'] += d['mass']
                h['proofSubterms'] += d['proofSubterms']
    hlist = sorted(heads.values(), key=lambda d: -d['mass'])
    with open(o + '/heads.jsonl', 'w') as fh:
        for d in hlist:
            fh.write(json.dumps(d, ensure_ascii=False, separators=(',', ':')) + '\n')

    # ---- meta
    metas = [json.load(open(f)) for f in sorted(glob.glob(sh + '/f.meta.*.json'))]
    start = int(open(o + '/export_start.txt').read()) if os.path.exists(o + '/export_start.txt') else None
    end = int(open(o + '/export_end.txt').read()) if os.path.exists(o + '/export_end.txt') else None
    slow = sorted((s for m in metas for s in m['slow']), key=lambda s: -s['ms'])
    meta = {
        'corpus': corpus,
        'leanVersion': metas[0]['leanVersion'] if metas else None,
        'shards': len(metas),
        'modulesImported': metas[0]['modulesImported'] if metas else None,
        'projectConstants': metas[0]['projectConstants'] if metas else None,
        'primaryResolved': metas[0]['primaryResolved'] if metas else None,
        'primaryUnresolved': metas[0]['primaryUnresolved'] if metas else None,
        'theoremsListed': metas[0]['theoremsListed'] if metas else None,
        'theoremsUnresolved': metas[0]['theoremsUnresolved'] if metas else None,
        'written': sum(m['written'] for m in metas),
        'noValue': sum(m['noValue'] for m in metas),
        'stmtFail': sum(m['stmtFail'] for m in metas),
        'massFail': sum(m['massFail'] for m in metas),
        'failures': [f for m in metas for f in m['failures']],
        'wallSeconds': (end - start) if start and end else None,
        'cpuSecondsSumOfShards': round(sum(m['totalMs'] for m in metas) / 1000, 1),
        'importMsPerShard': [m['importMs'] for m in metas],
        'theoremsOver2s': len(slow),
        'slowest': slow[:15],
        'sumTheoremMs': sum(d.get('ms', 0) for d in rows),
    }
    json.dump(meta, open(o + '/export_meta.json', 'w'), indent=1, ensure_ascii=False)

    # ---- coverage
    cov = {}
    # (1) hypothesis / conclusion head constants
    hyp_cls, hyp_head = Counter(), Counter()
    con_cls, con_head = Counter(), Counter()
    bk = Counter()
    for d in rows:
        for b in d.get('binders', []):
            bk[b['kind']] += 1
            if b['isProp']:
                hyp_cls[b['cls']] += 1
                hyp_head[(b['cls'], b['head'])] += 1
        c = d.get('concl')
        if c:
            con_cls[c['cls']] += 1
            con_head[(c['cls'], c['head'])] += 1
    nh, nc = sum(hyp_cls.values()), sum(con_cls.values())
    cov['binderKinds'] = dict(bk)
    cov['hypotheses'] = {'n': nh, 'byClass': {k: [v, pct(v, nh)] for k, v in hyp_cls.most_common()},
                         'otherPct': pct(hyp_cls['other'], nh),
                         'otherProjectDefinedPct': pct(sum(v for (c, h), v in hyp_head.items() if c == 'other' and h in primary), nh),
                         'distinctHeads': len({h for (_, h) in hyp_head}),
                         'distinctHeadsOther': len({h for (c, h) in hyp_head if c == 'other'}),
                         'topOtherHeads': [[h, v] for (c, h), v in hyp_head.most_common() if c == 'other'][:40]}
    cov['conclusions'] = {'n': nc, 'byClass': {k: [v, pct(v, nc)] for k, v in con_cls.most_common()},
                          'otherPct': pct(con_cls['other'], nc),
                          'otherProjectDefinedPct': pct(sum(v for (c, h), v in con_head.items() if c == 'other' and h in primary), nc),
                          'topOtherHeads': [[h, v] for (c, h), v in con_head.most_common() if c == 'other'][:40]}
    # (2) proof mass
    outer, inner = Counter(), Counter()
    nodes = cast = surg = 0
    kind = [0, 0, 0]
    psub = 0
    for d in rows:
        m = d.get('mass')
        if not m:
            continue
        nodes += m['nodes']; cast += m['castRegion']; surg += m['surgRegion']; psub += m['proofSubterms']
        for k, v in m['outer'].items():
            outer[k] += v
        for k, v in m['inner'].items():
            inner[k] += v
        for i in range(3):
            kind[i] += m['kind'][i]
    so, si = sum(outer.values()), sum(inner.values())
    cov['proofMass'] = {
        'theoremsWithMass': sum(1 for d in rows if d.get('mass')),
        'distinctNodes': nodes,
        'outerTotal': so, 'outerInflationOverDistinct': round(so / nodes, 4) if nodes else None,
        'outer': {k: [r0(v), pct(v, so)] for k, v in outer.most_common()},
        'innerTotal': si, 'innerInflationOverDistinct': round(si / nodes, 4) if nodes else None,
        'inner': {k: [r0(v), pct(v, si)] for k, v in inner.most_common()},
        'innerOtherPct': pct(inner['other'], si),
        'castRegionPct': pct(cast, nodes), 'surgeryRegionPct': pct(surg, nodes),
        'kindPct': {'proofSpine': pct(kind[0], sum(kind)), 'dataArgument': pct(kind[1], sum(kind)),
                    'instanceArgument': pct(kind[2], sum(kind))},
        'proofSubterms': psub,
        'topOtherTypeHeads': [[h['head'], h['mass'], h['isProject']] for h in hlist if h['cls'] == 'other'][:40],
    }
    hm = sum(h['mass'] for h in hlist)
    cov['proofMass']['otherHeadMassFromProjectPredicatesPct'] = pct(
        sum(h['mass'] for h in hlist if h['cls'] == 'other' and h['isProject']), hm)
    # (3) constants in proofs
    fam_dag = defaultdict(lambda: [0, 0])  # family -> [ext, proj]
    for c in clist:
        fam_dag[c['family']][1 if c['isProject'] else 0] += c['dag']
    ext = sum(v[0] for v in fam_dag.values()); prj = sum(v[1] for v in fam_dag.values())
    unclassified = ('other_lemma', 'data')
    cov['proofConstants'] = {
        'distinctConstants': len(clist), 'distinctProject': sum(1 for c in clist if c['isProject']),
        'usesExt': ext, 'usesProj': prj,
        'extByFamily': {k: [v[0], pct(v[0], ext)] for k, v in sorted(fam_dag.items(), key=lambda kv: -kv[1][0]) if v[0]},
        'projByFamily': {k: [v[1], pct(v[1], prj)] for k, v in sorted(fam_dag.items(), key=lambda kv: -kv[1][1]) if v[1]},
        'extOtherLemmaPct': pct(fam_dag['other_lemma'][0], ext),
        'extDataPct': pct(fam_dag['data'][0], ext),
        'extLemmaUses': sum(c['dag'] for c in clist if not c['isProject'] and c['isProp']),
        'extOtherLemmaPctOfLemmaUses': pct(fam_dag['other_lemma'][0], sum(c['dag'] for c in clist if not c['isProject'] and c['isProp'])),
        'topExtOtherLemma': [[c['name'], c['dag']] for c in clist if c['family'] == 'other_lemma' and not c['isProject']][:40],
        'topExtData': [[c['name'], c['dag']] for c in clist if c['family'] == 'data' and not c['isProject']][:25],
    }

    # ---- markdown
    L = []
    L.append(f'# Friction export coverage: {corpus}\n')
    L.append(f"Generated by `bench/friction_merge.py {corpus}` from `hyps.jsonl`, `consts.jsonl`, `heads.jsonl`. "
             f"Lean {meta['leanVersion']}.\n")
    L.append('## Export\n')
    L.append(f"- theorems listed (kind == theorem in `out/corpus/{corpus}/decls.jsonl`): {meta['theoremsListed']}; "
             f"not found in the environment: {len(meta['theoremsUnresolved'] or [])}; written: {meta['written']}")
    L.append(f"- statement failures: {meta['stmtFail']}; proof-mass failures: {meta['massFail']}; theorems without a value: {meta['noValue']}")
    L.append(f"- wall time {meta['wallSeconds']} s on {meta['shards']} shards (sum of shard times {meta['cpuSecondsSumOfShards']} s, "
             f"import {min(meta['importMsPerShard'])}-{max(meta['importMsPerShard'])} ms per shard); {meta['theoremsOver2s']} theorems took over 2 s")
    if meta['slowest']:
        s = meta['slowest'][0]
        L.append(f"- slowest theorem: `{s['name']}` {s['ms']} ms")
    L.append('')
    L.append('## Hypotheses and conclusions by class\n')
    L.append(f"Binders: {dict(bk)}. Prop-valued binders (hypotheses and Prop-class instances): {nh}.\n")
    L.append('| class | hypotheses | % | conclusions | % |')
    L.append('|---|---|---|---|---|')
    for k in cfg['classes']:
        L.append(f"| {k}{' (side)' if k in side else ''} | {hyp_cls[k]} | {pct(hyp_cls[k], nh)} | {con_cls[k]} | {pct(con_cls[k], nc)} |")
    L.append('')
    L.append(f"**Coverage:** {pct(hyp_cls['other'], nh)}% of hypotheses and {pct(con_cls['other'], nc)}% of conclusions have a head outside every configured class "
             f"({cov['hypotheses']['distinctHeadsOther']} of {cov['hypotheses']['distinctHeads']} distinct hypothesis heads). "
             f"Predicates defined by the project itself account for {cov['hypotheses']['otherProjectDefinedPct']} points of the hypothesis figure "
             f"and {cov['conclusions']['otherProjectDefinedPct']} points of the conclusion figure.\n")
    L.append('Largest unclassified hypothesis heads: ' + ', '.join(f'`{h}` {v}' for h, v in cov['hypotheses']['topOtherHeads'][:20]) + '\n')
    L.append('Largest unclassified conclusion heads: ' + ', '.join(f'`{h}` {v}' for h, v in cov['conclusions']['topOtherHeads'][:20]) + '\n')
    pm = cov['proofMass']
    L.append('## Proof mass by the type being proved\n')
    L.append(f"{pm['theoremsWithMass']} theorems, {nodes} distinct proof-term nodes, {psub} proof subterms.\n")
    L.append('| class | outermost side-condition region | % | nearest enclosing proof subterm | % |')
    L.append('|---|---|---|---|---|')
    L.append(f"| main (not inside any side-condition proof) | {r0(outer['main'])} | {pct(outer['main'], so)} | | |")
    for k in cfg['classes']:
        a = f"{r0(outer[k])} | {pct(outer[k], so)}" if k in side else ' | '
        L.append(f"| {k} | {a} | {r0(inner[k])} | {pct(inner[k], si)} |")
    L.append('')
    L.append(f"Shares are fractional: a subterm reached under k different labels gives 1/k to each, so each column sums to the number of distinct nodes "
             f"(check: {pm['outerInflationOverDistinct']}, {pm['innerInflationOverDistinct']}).\n")
    whole = Counter(d.get('rootClass') for d in rows if d.get('mass'))
    wm = Counter()
    for d in rows:
        if d.get('mass'):
            wm[d['rootClass']] += d['mass']['nodes']
    cov['proofMass']['rootClassTheorems'] = dict(whole)
    cov['proofMass']['rootClassNodes'] = dict(wm)
    side_whole = sum(wm[k] for k in side)
    cov['proofMass']['sideMassInTheoremsWhoseConclusionIsSidePct'] = pct(side_whole, nodes)
    L.append(f"Of the side-condition mass, {pct(side_whole, nodes)}% of all nodes belongs to theorems whose own conclusion is a side-condition class "
             f"({sum(whole[k] for k in side)} theorems: stand-alone side-condition lemmas); the rest is side conditions discharged inline.\n")
    L.append(f"Inside a proof subterm whose type mentions a cast function: {pm['castRegionPct']}% of distinct nodes; "
             f"mentions indicator/restrict/support/cutoff: {pm['surgeryRegionPct']}%.\n")
    L.append(f"Node kind: {pm['kindPct']}.\n")
    L.append(f"**Coverage:** {pm['innerOtherPct']}% of proof mass sits under a proof subterm of class `other` "
             f"(of all mass, {pm['otherHeadMassFromProjectPredicatesPct']}% is `other` with a project-defined predicate as head).\n")
    L.append('Largest `other` type heads by mass: ' + ', '.join(f"`{h}` {m}{' (project)' if p else ''}" for h, m, p in pm['topOtherTypeHeads'][:25]) + '\n')
    pc = cov['proofConstants']
    L.append('## Constants used in proofs, by family\n')
    L.append(f"Unit: distinct applications (DAG-unique uses) summed over theorems. Non-project uses: {ext}; project uses: {prj}.\n")
    L.append('| family | non-project uses | % | project uses | % |')
    L.append('|---|---|---|---|---|')
    for k, v in sorted(fam_dag.items(), key=lambda kv: -(kv[1][0] + kv[1][1])):
        L.append(f"| {k} | {v[0]} | {pct(v[0], ext)} | {v[1]} | {pct(v[1], prj)} |")
    L.append('')
    L.append(f"**Coverage:** `other_lemma` is {pc['extOtherLemmaPct']}% of non-project uses ({pc['extOtherLemmaPctOfLemmaUses']}% of non-project lemma uses); "
             f"`data` (functions, types, constructors not in any list) is {pc['extDataPct']}%.\n")
    L.append('Largest non-project `other_lemma` constants: ' + ', '.join(f'`{n}` {v}' for n, v in pc['topExtOtherLemma'][:25]) + '\n')
    open(o + '/COVERAGE.md', 'w').write('\n'.join(L) + '\n')
    json.dump(cov, open(o + '/coverage.json', 'w'), indent=1, ensure_ascii=False)
    print(f"{corpus}: {len(rows)} theorems, stmtFail {meta['stmtFail']}, massFail {meta['massFail']}, wall {meta['wallSeconds']} s")


if __name__ == '__main__':
    main(sys.argv[1])
