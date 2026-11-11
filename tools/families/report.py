#!/usr/bin/env python3
"""M9 families, step 3: out/families/ns/CLUSTERS.md from clusters.jsonl / summary.json of the three projects,
the planted controls and the cloned-module control.  Every number is read from those files.
Hand-entered readings (labelled as readings) come from tools/families/reading.json, keyed by the
family's first member and size."""
import json, os, pickle, collections

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(H, '..', '..')
OUT = os.path.join(REPO, 'out', 'families')
TOP = 60
SIDE = 15


def load(p, sfx=''):
    R = [json.loads(l) for l in open(os.path.join(OUT, p, f'clusters{sfx}.jsonl'))]
    S = json.load(open(os.path.join(OUT, p, f'summary{sfx}.json')))
    return R, S


def sn(n, k=2):
    p = n.split('.')
    return '.'.join(p[-k:]) if len(p) > k else n


def esc(s):
    return s.replace('|', '\\|').replace('\n', ' ')


def select(R, top):
    """highest scores first; a family is skipped when it overlaps one already listed
    (|A ∩ B| / min(|A|, |B|) ≥ 0.6); the skipped ids are noted on the one that is kept"""
    chosen = []
    for r in R:
        ms = set(r['members'])
        hit = None
        for c in chosen:
            cs = c['_set']
            if len(ms & cs) / min(len(ms), len(cs)) >= 0.6:
                hit = c
                break
        if hit is not None:
            hit['_also'].append(r)
            continue
        if len(chosen) >= top:
            continue
        r['_set'] = ms
        r['_also'] = []
        chosen.append(r)
    return chosen


def hole_desc(h):
    kinds = ', '.join(f'{k} ×{v}' if len(h['kinds']) > 1 else k for k, v in sorted(h['kinds'].items(), key=lambda kv: -kv[1]))
    extra = []
    if h['dependsOnBound']:
        extra.append('depends on a bound variable, so the parameter must be a function')
    if h['compound']:
        extra.append('compound')
    return f"{kinds}; {h['distinct']} distinct values" + ('; ' + '; '.join(extra) if extra else '')


def channel_names(lvs):
    out = []
    for pre, nm in (('L', 'body'), ('AU@', 'anti-unification'), ('API@', 'lemma shapes'), ('APIL@', None), ('ROLE@', 'lemma roles'), ('WRAP', 'specialisation')):
        xs = [l for l in lvs if l.startswith(pre) and 'x' not in l and (pre != 'L' or l[1:].isdigit())]
        if xs and nm:
            out.append(nm + ' (' + ', '.join(xs) + ')')
    if any('xAPI' in l for l in lvs):
        out.append('body and lemma shapes')
    return '; '.join(out)


def main():
    R, S = load('ns')
    Rc, Sc = load('carleson')
    Rp, Sp = load('pfr')
    Ra, Sa = load('ns', '_all')
    funnel = {p: json.load(open(os.path.join(OUT, p, 'funnel.json'))) for p in ('ns', 'carleson', 'pfr')}
    planted = json.load(open(os.path.join(OUT, 'ns', 'planted_result.json')))
    stmts = {}
    for l in open(os.path.join(REPO, 'out', 'corpus', 'ns', 'decls.jsonl')):
        d = json.loads(l)
        if d['kind'] == 'theorem':
            stmts[d['name']] = d.get('statement', '')
    try:
        reading = json.load(open(os.path.join(H, 'reading.json')))
    except FileNotFoundError:
        reading = {}
    N = S['definitions clustered']
    L = S['levels']
    o = []
    w = o.append

    w('# M9 families: wide-aperture clustering of definitions (ns, with Carleson and PFR beside it)\n')
    w(open(os.path.join(H, 'report_head.md')).read().format(**head_numbers(R, S, Sc, Sp, Sa, funnel, planted)))

    # ------------------------------------------------------------ funnel
    w('\n## 1. What was clustered\n')
    w('| | ns (machine) | Carleson | PFR |\n|---|---:|---:|---:|')
    rows = ['definitions and structures exported', 'dropped: syntax / metaprogramming', 'dropped: body over 4000 nodes',
            'definitions and structures kept (all)', '… not in the dead-code export (auxiliary definitions Lean generated)',
            '… reachable from the headline theorems', 'theorems with a statement tree', '… reachable',
            'theorem statements over the node limit (not profiled)',
            'definitions with ≥ 1 reachable theorem stated about them']
    for k in rows:
        w(f"| {k} | " + ' | '.join(f"{funnel[p].get(k, 0):,}" for p in ('ns', 'carleson', 'pfr')) + ' |')
    w('')
    w('Reachable definitions by result: ' + '; '.join(
        f"{p}: " + ', '.join(f'{v:,} {k}' for k, v in s['definitions by result class'].items())
        for p, s in (('ns', S), ('Carleson', Sc), ('PFR', Sp))) + '.')
    w('"Not in the dead-code export" are `ctorIdx`, `noConfusionType` and similar definitions Lean generates for each structure; they are not declarations a reader meets and are counted as unreachable. Instances (25 in ns) and definitions whose result is a type class (143) are not exported.')

    # ------------------------------------------------------------ aperture
    w('\n## 2. The aperture: how many definitions fall in families as the matching loosens\n')
    w('Each cell is the number of reachable definitions in a family of at least that size (share of all reachable definitions in brackets for "≥ 2"). "removable" = members − 1 summed over families: the definitions that would disappear if each family became one definition. A row marked *skeleton ≥ 4* counts only families whose shared body has at least four nodes; the rest of a row is families like "a product of two types" or "one function applied to one argument".\n')

    def table(S_, n_, keys):
        t = ['| level | families | defs in ≥ 2 | ≥ 3 | ≥ 5 | ≥ 10 | largest | removable |', '|---|---:|---:|---:|---:|---:|---:|---:|']
        for k, label in keys:
            d = S_['levels'].get(k)
            if d is None:
                continue
            t.append(f"| {label} | {d['clusters']:,} | {d['>=2']:,} ({100 * d['>=2'] / n_:.1f}%) | {d['>=3']:,} | {d['>=5']:,} | {d['>=10']:,} | {d['largest']} | {d['>=2'] - d['clusters']:,} ({100 * (d['>=2'] - d['clusters']) / n_:.1f}%) |")
        return '\n'.join(t)
    keys = [('L0', 'L0 body, exact up to bound names'), ('L0 (body ≥ 4 nodes)', '… *body ≥ 4 nodes*'),
            ('L0+sig', '… and equal signature'),
            ('L1', 'L1 + numerals abstracted'), ('L2', 'L2 + leaf constants → typed holes'),
            ('L3', 'L3 + project heads → holes'), ('L3 (body ≥ 4 nodes)', '… *body ≥ 4 nodes*'), ('L3+sig', '… and equal signature at L3'),
            ('AU@1.0', 'AU@1.0 anti-unification, leaf and head holes only'), ('AU@1.0 (shared skeleton ≥ 4 nodes)', '… *skeleton ≥ 4*'),
            ('AU@0.9', 'AU@0.9'), ('AU@0.8', 'AU@0.8'), ('AU@0.7', 'AU@0.7 (≤ 30% of a member inside compound holes)'),
            ('AU@0.7 (shared skeleton ≥ 4 nodes)', '… *skeleton ≥ 4*'), ('AU@0.6', 'AU@0.6'), ('AU@0.5', 'AU@0.5'),
            ('AU@0.5 (shared skeleton ≥ 4 nodes)', '… *skeleton ≥ 4*'),
            ('API@8', 'API@8 ≥ 8 identical lemma shapes'), ('API@5', 'API@5'), ('API@3', 'API@3'), ('API@2', 'API@2'),
            ('APIL@2', 'APIL@2 the same with leaf constants abstracted'),
            ('ROLE@0.5', 'ROLE@0.5 lemma roles, weighted overlap ≥ 0.5'), ('ROLE@0.35', 'ROLE@0.35'), ('ROLE@0.25', 'ROLE@0.25'), ('ROLE@0.15', 'ROLE@0.15'),
            ('AU@0.7 x API@2', 'AU@0.7 and ≥ 2 identical lemma shapes'),
            ('WRAP (a definition and ≥ 2 specialisations of it)', 'WRAP a definition and ≥ 2 named specialisations')]
    w(f'### ns: {N:,} reachable definitions\n')
    w(table(S, N, keys))
    w('')
    d = S['exact duplicates removable (members − 1), by kind']
    pl = {'type': 'types', 'value or function': 'values or functions', 'proposition': 'propositions'}
    w(f"Of the {L['L0']['>=2'] - L['L0']['clusters']:,} exact duplicates (L0 removable), " + ', '.join(f'{v:,} are {pl[k]}' for k, v in sorted(d.items(), key=lambda kv: -kv[1])) + '.')
    a = S['api']
    w(f"\nLemma side. {a['exact statement shape: distinct shapes']:,} distinct (statement, definition-holed) shapes; {a['exact statement shape: shapes held by ≥ 2 definitions']:,} are held by two or more definitions, by {a['exact statement shape: definitions with ≥ 1 shape shared with another definition']:,} definitions in all. "
      f"{S['theorems with a statement shape (some definition holed) also proved about another definition']:,} of {S['reachable theorems profiled']:,} reachable theorems that mention a definition ({100 * S['theorems with a statement shape (some definition holed) also proved about another definition'] / S['reachable theorems profiled']:.1f}%) have a statement that is also proved, hole for hole, about a different definition. Abstracting leaf constants as well adds {a['leaf-abstracted statement shape: shapes held by ≥ 2 definitions'] - a['exact statement shape: shapes held by ≥ 2 definitions']} shapes: nothing. "
      f"Roles are much coarser: {a['roles: distinct']:,} distinct, {a['roles: held by ≥ 2 definitions']:,} held by two or more definitions, the commonest by {a['roles: most widely held, definitions']:,}.")
    w(f'\n### ns, every definition (dead code included): {Sa["definitions clustered"]:,} definitions\n')
    w(table(Sa, Sa['definitions clustered'], [k for k in keys if k[0] in ('L0', 'L3', 'AU@0.7', 'API@2', 'ROLE@0.25')]))
    for nm, S_ in (('Carleson', Sc), ('PFR', Sp)):
        n_ = S_['definitions clustered']
        w(f'\n### {nm}: {n_:,} reachable definitions\n')
        w(table(S_, n_, [k for k in keys if k[0] in ('L0', 'L1', 'L2', 'L3', 'L3 (body ≥ 4 nodes)', 'AU@1.0', 'AU@0.7', 'AU@0.7 (shared skeleton ≥ 4 nodes)', 'AU@0.5', 'API@3', 'API@2', 'ROLE@0.5', 'ROLE@0.25', 'ROLE@0.15', 'AU@0.7 x API@2', 'WRAP (a definition and ≥ 2 specialisations of it)')]))
        a = S_['api']
        w(f"\n{S_['theorems with a statement shape (some definition holed) also proved about another definition']:,} of {S_['reachable theorems profiled']:,} theorems ({100 * S_['theorems with a statement shape (some definition holed) also proved about another definition'] / max(1, S_['reachable theorems profiled']):.1f}%) have a statement shape also proved about another definition.")
    w('\nThe largest families in the human projects, for scale:\n')
    for nm, R_ in (('Carleson', Rc), ('PFR', Rp)):
        for r in select(R_, 4):
            w(f"- {nm}: {r['m']} members, {channel_names(r['levels'])}; skeleton `{(r['skeleton'] or 'no common body')[:150]}`; members {', '.join('`' + sn(x) + '`' for x in r['members'][:6])}{' …' if r['m'] > 6 else ''}; {r['sharedShapes']} identical lemma shapes, {r['sharedRoles']} shared roles.")

    # ------------------------------------------------------------ controls
    w('\n## 3. Controls\n')
    w('### 3.1 Known cases in ns (no names were given to the tool)\n')
    w(open(os.path.join(H, 'report_controls.md')).read())
    w('\nWhere each known definition sits (every family record that contains it; rank is by triage score among ' + f'{len(R):,} family records):\n')
    w('| definition | rank | channel | members | identical lemma shapes | shared roles | others in the family |\n|---|---:|---|---:|---:|---:|---|')
    for c in ('NavierStokes.WeightedClasses.MemClass', 'NavierStokes.LabelSumBounds.UniformClass', 'NavierStokes.WeightedClasses.WaveClass', 'NavierStokes.DiagonalResidual.JetRate'):
        for i, r in enumerate(R):
            if c in r['members']:
                w(f"| `{sn(c)}` | {i + 1:,} | {', '.join(r['levels'][:4])} | {r['m']} | {r['sharedShapes']} | {r['sharedRoles']} | {', '.join('`' + sn(x, 1) + '`' for x in r['members'] if x != c)[:160]} |")
    w('\n### 3.2 Cloned modules\n')
    w(clone_section(Ra))
    w('\n### 3.3 Planted families\n')
    w('`tools/families/planted/FamiliesPlanted.lean` (compiled against the corpus\'s Mathlib, never part of it) is mixed into the ns export and the whole pipeline rerun; expectations were written in `planted/expected.json` before the planted run. The families were written by the builder of the matcher, after the ns runs, so they test that the pipeline does what it is described to do and not how it fares on families someone else would write (plan rule 2 is not met).\n')
    w('| control | expectation | result | where it landed |\n|---|---|---|---|')
    for k, v in planted.items():
        where = '; '.join(f"rank {h['rank']:,}: {', '.join(h['levels'][:3])}, {h['m']} members" + (f" (with {', '.join(sn(x, 1) for x in h['others'][:3])}{'…' if len(h['others']) > 3 else ''})" if h['others'] else '') + (f", holes: {', '.join(h['holeKinds'])}" if h['holeKinds'] and h['skeleton'] else '') for h in v['families'][:3]) or 'no family'
        w(f"| {k}: {', '.join('`' + sn(m, 1) + '`' for m in v['members'])} | {v['expect']} | **{'as expected' if v['pass'] else 'NOT as expected'}** | {where} |")
    w('\nThe two planted families also merge with each other in the lemma-shape channel: `zero`, `neg`, `add` and `const_mul` have the identical statement for all six predicates. That is correct behaviour (all six are sets of functions closed under the same operations) and it shows what the lemma channel finds: a shared algebra, whatever the bodies are.')

    # ------------------------------------------------------------ score
    w('\n## 4. Triage score\n')
    w(open(os.path.join(H, 'report_score.md')).read())

    # ------------------------------------------------------------ top families
    chosen = select(R, TOP)
    w(f'\n## 5. The {TOP} highest-scoring families\n')
    w('A family that overlaps a higher-scoring one (60% of the smaller) is folded into it and its id is listed under "also". Columns: m members; tight = tightest level at which the members are already together; sk = nodes of the shared skeleton (– = no common body); holes = distinct holes / effective parameters (holes that always change together count once); users = declarations that use a member; stmt = theorems whose statement mentions a member; shapes = identical lemma shapes held by ≥ 2 members; roles = shared lemma roles; low–high = estimated concept-count reduction (definitions + lemma statements).\n')
    w('| # | id | m | tight | channels | sk | holes | users | stmt | shapes | roles | low–high | pen | score | skeleton / first members |\n|---:|---|---:|---|---|---:|---|---:|---:|---:|---:|---|---:|---:|---|')
    for i, r in enumerate(chosen):
        lab = r['skeleton'][:70] if r['skeleton'] else 'no common body'
        w(f"| {i + 1} | {r['id']} | {r['m']} | {r['tightest']} | {esc(short_channels(r['levels']))} | {r['skeletonNodes'] if r['skeleton'] else '–'} | {r['nHoles'] if r['skeleton'] else '–'}/{r['effectiveParams'] if r['skeleton'] else '–'} | {r['users']:,} | {r['stmtMentions']:,} | {r['sharedShapes']} | {r['sharedRoles']} | {r['conceptReductionLow']}–{r['conceptReductionHigh']} | {r['penalty']:g} | {r['score']:g} | `{esc(lab)}` · {', '.join(sn(x, 1) for x in r['members'][:3])} |")
    kinds = collections.Counter()
    for r in chosen:
        kinds[max(r['resultClass'], key=r['resultClass'].get)] += 1
    w(f"\nBy what the members are: {kinds.get('U', 0)} families of types, {kinds.get('Prop', 0)} of propositions (predicates and Prop-valued structures), {kinds.get('val', 0)} of values or functions.")
    if reading:
        w('\n### Reading of the list (a model\'s reading, not evidence)\n')
        w(reading.get('_summary', ''))
    w('\n### Details\n')
    for i, r in enumerate(chosen):
        w(f"\n#### {i + 1}. {r['id']}: {r['m']} members, score {r['score']:g}\n")
        key = f"{r['members'][0]}|{r['m']}"
        if key in reading:
            w(f"*Reading (model, not evidence):* {reading[key]}\n")
        w(f"- found by: {channel_names(r['levels'])}" + (f"; also {', '.join(x['id'] for x in r['_also'][:8])}{' …' if len(r['_also']) > 8 else ''} ({len(r['_also'])} overlapping records folded in)" if r['_also'] else ''))
        w(f"- kinds: {', '.join(f'{v} {k}' for k, v in r['kinds'].items())}; {r['modules']} modules; instance arguments per member {r['instanceParams'][0]}–{r['instanceParams'][1]}, type arguments {r['typeParams'][0]}–{r['typeParams'][1]}")
        w(f"- usage: {r['users']:,} declarations use a member; {r['stmtMentions']:,} theorem statements mention one; {r['cooccurInStatements'] if r['cooccurInStatements'] is not None else 'n/a'} member pairs occur together in a statement")
        w(f"- lemma family: {r['sharedShapes']} identical shapes ({r['lemmasInSharedShapes']} theorems; {r['coreShapes']} shapes held by every member), {r['sharedRoles']} shared roles ({r['lemmasInSharedRoles']} theorems; {r['coreRoles']} roles held by every member), out of {r['lemmasAboutMembers']:,} statements about the members")
        w(f"- concept-count estimate: {r['m'] - 1} definitions + {r['lemmaReduction']} lemma statements by identical shape (low), or + {r['roleReduction']} by role (high); penalty {r['penalty']:g}; score {r['score']:g}")
        if r['wrapBase']:
            w(f"- the general form already exists: `{r['wrapBase']}`; the skeleton below is over its named specialisations")
        if r['skeleton']:
            w(f"- similarity {r['similarity']} (smallest share of a member outside compound holes), skeleton of {r['skeletonNodes']} nodes over {r['lggOver']} distinct bodies:\n\n  ```\n  {r['skeleton']}\n  ```")
            if r['holes']:
                ind = {True: 'the holes vary independently (more joint combinations than any one hole has values)',
                       False: 'the holes do not vary independently (no more joint combinations than the most varied hole has values)',
                       None: ''}[r['independent']]
                w(f"- holes: {r['nHoles']}, effective parameters {r['effectiveParams']}" + (f'; {ind}' if ind else ''))
                for h in r['holes'][:8]:
                    w(f"  - ⟨h{h['id']}⟩ {hole_desc(h)}")
                if len(r['holes']) > 8:
                    w(f"  - … {len(r['holes']) - 8} more holes")
            else:
                w('- no holes: the bodies are identical up to bound names')
        elif r['similarity'] == 1.0:
            w('- each body is a single constant or parameter (the generalisation is one leaf hole): a family of aliases')
        else:
            w('- no common body (the generalisation is a single hole): a shared interface would have to be a structure or class, not a parameter')
        # members with fillers
        fill = {}
        if r['skeleton'] and r['holes']:
            for j, nme in enumerate(r['repNames']):
                fill[nme] = [h['fill'][j] for h in r['holes'][:6]]
        w('')
        if fill:
            hdr = ' | '.join(f'⟨h{h["id"]}⟩' for h in r['holes'][:6])
            w(f'| member | stmt | users | {hdr} |\n|---|---:|---:|' + '---|' * len(r['holes'][:6]))
            for mi in r['memberInfo'][:14]:
                fs = fill.get(mi['name'])
                cells = ' | '.join(f'`{esc(x[:60])}`' for x in fs) if fs else ' | '.join('(same body as another member)' if k == 0 else '' for k in range(len(r['holes'][:6])))
                if r['wrapBase'] == mi['name']:
                    cells = ' | '.join('(the general form)' if k == 0 else '' for k in range(len(r['holes'][:6])))
                w(f"| `{esc(sn(mi['name'], 3))}` | {mi['nstmt']} | {mi['users']} | {cells} |")
        else:
            w('| member | stmt | users | body |\n|---|---:|---:|---|')
            for mi in r['memberInfo'][:14]:
                w(f"| `{esc(sn(mi['name'], 3))}` | {mi['nstmt']} | {mi['users']} | `{esc(mi['body'][:110])}` |")
        if r['m'] > 14:
            w(f"\n… and {r['m'] - 14} more members (all in `clusters.jsonl`).")
        if i < SIDE:
            exact = {t for p in r['parallel'] for v in p['thms'].values() for t in v}
            rows = r['parallelRoles'][:6]
            if rows or r['parallel']:
                w('\nParallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):\n')
            shown = set()
            for p in rows:
                w(f"- role `{p['role']}` (held by {p['heldByDefinitionsOverall']} definitions in the corpus)")
                for mname, ts in list(p['thms'].items())[:5]:
                    t = ts[0]
                    shown.add(t)
                    w(f"  - `{sn(mname, 1)}`: {'= ' if t in exact else ''}`{sn(t, 2)}` : `{esc(stmts.get(t, '')[:210])}`")
            if not rows:
                for p in r['parallel'][:4]:
                    w(f"- identical shape (held by {p['heldByDefinitionsOverall']} definitions in the corpus)")
                    for mname, ts in list(p['thms'].items())[:5]:
                        w(f"  - `{sn(mname, 1)}`: = `{sn(ts[0], 2)}` : `{esc(stmts.get(ts[0], '')[:210])}`")
    w('\n## 6. Files\n')
    w(open(os.path.join(H, 'report_files.md')).read())
    # ---- added after the independent review of M9 (2026-11-11); fixed text, the reviewer's readings
    o += ['', '## 7. After review (2026-11-11)', '',
          'An independent agent checked this step together with the Lean step (`out/families/FAMILIES.md`, section 10). Its findings about the clustering are readings, not kernel-checked, and were not rerun:', '',
          '- No control name appears in `cluster.py`, `features.py`, `tree.py` or `Export.lean`; only this report looks names up, to print ranks.',
          '- **15 random family records outside the top 60** (seed 9090, spread over the looseness levels): 4 real families, 6 parallel by construction with different mathematics, 5 accidental. The real ones were at the exact level, the project-heads level and the loosest anti-unification level; none were in the samples from the middle levels, the named-specialisation channel or the lemma channels.',
          '- **Families no channel sees.** Of 30 random reachable definitions (types left out; seed 31337) read with their 5 nearest neighbours by name and signature, 7 (95% interval 12% to 41%) have a neighbour the reviewer would call the same notion that nothing here joins to them. Three have the shape of the one family that paid in Lean: the same structure or module repeated with one inserted argument or a different record (`GradeGuards` in 4 parallel modules; the `PressureStream` module redone in `VariableGaugeMean` with an extra gauge argument; `MeanVector` / `LocalMeanVector` / `WaveVector`). The list is in `out/families/review/nn30.txt`.',
          '- **Consequence for the numbers above.** The "in families" percentages are upper bounds on paper at every level (most loose families are not one idea), and at the same time the method misses the kind of family worth most. Of the top 60 read in the Lean step, 8 were read as one idea with several instances and 20 as one type under many names; measured, the type names are removable as they stand (389 of 389 by `rfl`), and one of the 7 families taken through Lean supplies 99% of the net proof saving, the other six together being break-even.', '']
    open(os.path.join(OUT, 'ns', 'CLUSTERS.md'), 'w').write('\n'.join(o) + '\n')
    print('written', os.path.join(OUT, 'ns', 'CLUSTERS.md'), len('\n'.join(o)), 'chars;', len(chosen), 'families')


def short_channels(lvs):
    out = []
    if any(l in ('L0', 'L1', 'L2', 'L3') for l in lvs):
        out.append('body')
    if any(l.startswith('AU@') and 'x' not in l for l in lvs):
        out.append('AU')
    if any(l.startswith('API@') for l in lvs):
        out.append('shapes')
    if any(l.startswith('ROLE@') for l in lvs):
        out.append('roles')
    if 'WRAP' in lvs:
        out.append('wrap')
    return '+'.join(out)


def clone_section(Ra):
    P = pickle.load(open(os.path.join(OUT, 'ns', 'features.pkl'), 'rb'))
    F = P['feats']
    clones = json.load(open(os.path.join(REPO, 'out', 'deadcode', 'ns', 'clones.json')))
    bymod = collections.defaultdict(list)
    for f in F.values():
        bymod[f['module']].append(f['name'])
    lv = collections.defaultdict(lambda: collections.defaultdict(set))
    for r in Ra:
        for l in r['levels']:
            for m in r['members']:
                lv[m][l] |= set(r['members'])
    rows = []
    tot = collections.Counter()
    seen = set()
    for c in clones:
        if c['label'] != 'near-identical' or (c['clone'], c['base']) in seen:
            continue
        seen.add((c['clone'], c['base']))
        cd = bymod.get(c['clone'], [])
        bd = set(bymod.get(c['base'], []))
        row = {l: sum(1 for d in cd if lv[d][l] & bd) for l in ('L0', 'L3', 'AU@0.7', 'API@2', 'ROLE@0.25')}
        reach = sum(1 for d in cd if F[d]['reach'])
        tot['modules'] += 1
        tot['defs'] += len(cd)
        tot['reach'] += reach
        for l, v in row.items():
            tot[l] += v
        if not cd:
            tot['empty'] += 1
        if cd:
            rows.append(f"| `{c['clone']}` | {len(cd)} | {row['L0']} | {row['L3']} | {row['AU@0.7']} | {row['API@2']} | {row['ROLE@0.25']} | {reach} |")
    s = (f"The dead-code tool lists {tot['modules']} near-identical module clones. They hold {tot['defs']} definitions, of which {tot['reach']} is reachable from the headline theorems, "
         f"so the clones are invisible to the main run and were checked in the run over every definition. A clone definition counts as found when it is in one family with a definition of the module it was copied from.\n\n"
         f"- by exact body (L0): {tot['L0']} of {tot['defs']}. The rest mention other cloned definitions, so their bodies differ in names.\n"
         f"- with project heads abstracted (L3): {tot['L3']} of {tot['defs']}.\n"
         f"- by identical lemma shapes (API@2): {tot['API@2']} of {tot['defs']}; by roles (ROLE@0.25): {tot['ROLE@0.25']}.\n\n"
         f"{tot['empty']} of the {tot['modules']} clone modules contain theorems only and are not in the table.\n\n"
         "| clone module | definitions | L0 | L3 | AU@0.7 | API@2 | ROLE@0.25 | reachable |\n|---|---:|---:|---:|---:|---:|---:|---:|\n" + '\n'.join(rows))
    return s


def head_numbers(R, S, Sc, Sp, Sa, funnel, planted):
    L = S['levels']
    N = S['definitions clustered']

    def rem(S_, k):
        d = S_['levels'][k]
        return d['>=2'] - d['clusters']

    def pct(S_, k):
        return 100 * rem(S_, k) / S_['definitions clustered']
    d = dict(
        N=N, Nall=funnel['ns']['definitions and structures kept (all)'],
        Nexp=funnel['ns']['definitions and structures exported'],
        thm=S['reachable theorems profiled'],
        twin=S['theorems with a statement shape (some definition holed) also proved about another definition'],
        twinpct=100 * S['theorems with a statement shape (some definition holed) also proved about another definition'] / S['reachable theorems profiled'],
        nrec=len(R),
        dupType=S['exact duplicates removable (members − 1), by kind'].get('type', 0),
        dupVal=S['exact duplicates removable (members − 1), by kind'].get('value or function', 0),
        dupProp=S['exact duplicates removable (members − 1), by kind'].get('proposition', 0),
        planted_pass=sum(1 for v in planted.values() if v['pass']), planted_n=len(planted),
    )
    for k, nm in (('L0', 'L0'), ('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3'), ('AU@1.0', 'AU10'), ('AU@0.7', 'AU07'), ('AU@0.5', 'AU05'),
                  ('AU@0.7 (shared skeleton ≥ 4 nodes)', 'AU07s'), ('L3 (body ≥ 4 nodes)', 'L3s'), ('L0 (body ≥ 4 nodes)', 'L0s'),
                  ('API@2', 'API2'), ('API@3', 'API3'), ('ROLE@0.25', 'ROLE25'), ('ROLE@0.5', 'ROLE5'), ('ROLE@0.15', 'ROLE15'),
                  ('AU@0.7 x API@2', 'AUAPI'), ('WRAP (a definition and ≥ 2 specialisations of it)', 'WRAP')):
        d[nm + '_in'] = L[k]['>=2']
        d[nm + '_rem'] = rem(S, k)
        d[nm + '_pct'] = pct(S, k)
        d[nm + '_n'] = L[k]['clusters']
        d[nm + '_max'] = L[k]['largest']
        d[nm + '_10'] = L[k]['>=10']
        for tag, S_ in (('c', Sc), ('p', Sp)):
            d[f'{nm}_{tag}pct'] = pct(S_, k)
            d[f'{nm}_{tag}rem'] = rem(S_, k)
    d['Nc'] = Sc['definitions clustered']
    d['Np'] = Sp['definitions clustered']
    d['twin_c'] = 100 * Sc['theorems with a statement shape (some definition holed) also proved about another definition'] / Sc['reachable theorems profiled']
    d['twin_p'] = 100 * Sp['theorems with a statement shape (some definition holed) also proved about another definition'] / Sp['reachable theorems profiled']
    def allc(r, c):
        return r['resultClass'].get(c, 0) == r['m']
    ax = [r for r in R if 'AU@0.7xAPI@2' in r['levels']]
    a7 = [r for r in R if 'AU@0.7' in r['levels']]
    r25 = [r for r in R if 'ROLE@0.25' in r['levels']]
    rl = [r for r in R if any(l.startswith('ROLE@') for l in r['levels'])]
    wr = [r for r in R if 'WRAP' in r['levels']]
    d.update(
        ax_n=len(ax), ax_defs=sum(r['m'] for r in ax), ax_lem=sum(r['lemmaReduction'] for r in ax),
        ax_eff01=sum(1 for r in ax if r['effectiveParams'] <= 1), ax_max=max((r['m'] for r in ax), default=0),
        ax_val=sum(1 for r in ax if max(r['resultClass'], key=r['resultClass'].get) == 'val'),
        a7_n=len(a7), a7_eff0=sum(1 for r in a7 if r['effectiveParams'] == 0),
        a7_eff1=sum(1 for r in a7 if r['effectiveParams'] == 1),
        a7_eff2=sum(1 for r in a7 if r['effectiveParams'] >= 2),
        a7_multi=sum(1 for r in a7 if r['nHoles'] >= 2), a7_indep=sum(1 for r in a7 if r['independent'] is True),
        a7_ho=sum(1 for r in a7 if r['higherOrderHoles']), a7_comp=sum(1 for r in a7 if r['compoundHoles']),
        a7_shapes=sum(1 for r in a7 if r['sharedShapes']), a7_inst=sum(1 for r in a7 if r['instanceParams'][1] > 0),
        a7_kinds=', '.join(f'{k} {v:,}' for k, v in collections.Counter(h['kind'] for r in a7 for h in r['holes']).most_common()),
        r25_n=len(r25), r25_nobody=sum(1 for r in r25 if r['similarity'] < 0.5),
        r25_nobody_defs=sum(r['m'] for r in r25 if r['similarity'] < 0.5),
        role_prop3=sum(1 for r in rl if allc(r, 'Prop') and r['m'] >= 3),
        wrap_n=len(wr), wrap_spec=sum(r['m'] - 1 for r in wr),
    )

    def rank(name, pre):
        for i, r in enumerate(R):
            if name in r['members'] and any(l.startswith(pre) for l in r['levels']):
                return i + 1
        return 0
    d['rk_mem_wrap'] = rank('NavierStokes.WeightedClasses.MemClass', 'WRAP')
    d['rk_mem_role'] = rank('NavierStokes.WeightedClasses.MemClass', 'ROLE')
    d['rk_uni_wrap'] = rank('NavierStokes.LabelSumBounds.UniformClass', 'WRAP')
    d['rk_jet_role'] = rank('NavierStokes.DiagonalResidual.JetRate', 'ROLE')
    d['rk_jet_api'] = rank('NavierStokes.DiagonalResidual.JetRate', 'API')
    d['L1_minus_L0'] = d['L1_rem'] - d['L0_rem']
    ch = select(R, TOP)
    d['fam_role_big'], d['role_big_m'], d['fam_mem'] = '?', 0, '?'
    for i, r in enumerate(ch):
        if r['skeleton'] is None and r['resultClass'].get('Prop', 0) == r['m'] and r['m'] > d['role_big_m'] and 'WRAP' not in r['levels']:
            d['fam_role_big'], d['role_big_m'] = i + 1, r['m']
        if 'NavierStokes.LabelSumBounds.UniformClass' in r['members'] and any(l.startswith('ROLE') for l in r['levels']):
            d['fam_mem'] = i + 1
    for r in ch:
        r.pop('_set', None); r.pop('_also', None)
    d['wrapdefs'] = L['WRAP (a definition and ≥ 2 specialisations of it)']['>=2'] - L['WRAP (a definition and ≥ 2 specialisations of it)']['clusters']
    return d


if __name__ == '__main__':
    main()
