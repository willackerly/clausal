#!/usr/bin/env python3
"""Dead-code report for the machine corpus (plan node M4), confirmed by compilation.

Inputs (all read-only):
  out/corpus/ns/decls.jsonl          declaration graph exported from Lean (term dependencies)
  out/corpus/ns/main_theorems.json   the four headline theorems
  corpora/ns/.lake/build/lib/lean/**/*.ilean
                                     Lean's own reference index: every source position where the
                                     elaborator resolved a constant, with the enclosing declaration
  corpora/ns/**/*.lean               sources (line ranges come from Lean; text is read for attributes)
  out/corpus/reuse/stmt_keys.jsonl   statement keys (exact / numerals / project-constant renaming)

Working copy: corpora/ns_trim/work (sources copied, .lake/packages symlinked, build output cloned).
Every `apply` regenerates the working copy's sources from the pristine corpora/ns files, so a plan is
always applied to the original text and never stacked on a previous edit.

Subcommands
  analyze                 classification, tables, 40-item sample -> out/corpus/deadcode/
  plan <stage>            control | sample | full | all   -> plans/<stage>.json
  apply <plan.json> [--restore names.txt]
  build <tag> [targets]   lake build in the working copy, log + parsed errors -> logs/<tag>.*
  control                 run the 20 negative controls one at a time
  control-reparse         recompute errorNamesDeclaration in control_results.json from the stored logs (no build)
  compare <predicted.jsonl> <export dir>   every field of the predicted graph against Lean's re-export -> <export dir>/compare.json
  trimgraph <plan.json> [--restore names.txt] <out.jsonl>   declaration graph after deletion
  tables                                   markdown tables -> tables.md
  outline <decls.jsonl> <outdir>           bench/outline.py on another graph + comparison with out/corpus/outline
  sizes <plan.json> [--restore names.txt]  files / lines / declarations before and after
"""
import collections
import json
import os
import random
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = os.path.join(ROOT, 'corpora/ns')
WORK = os.path.join(ROOT, 'corpora/ns_trim/work')
OUT = os.path.join(ROOT, 'out/corpus/deadcode')
ILEAN = os.path.join(NS, '.lake/build/lib/lean')
SEED = 20261110
HEAD_MODULES = ['NavierStokes.ComparatorSolution', 'Euler.Solution']
ROOT_FILES = {'NavierStokes': ['NavierStokes.ComparatorSolution'], 'Euler': ['Euler.Solution']}
CLONES = {  # out/corpus/reuse/REUSE.md section 1.7: namespace-renamed copies of a base module
    'Euler.BaseFirstPacketChoiceNoOptions': 'Euler.BaseFirstPacketChoice',
    'Euler.BaseFirstPacketEvolutionNoOptions': 'Euler.BaseFirstPacketEvolution',
    'Euler.BaseInductionStageNoOptions': 'Euler.BaseInductionStage',
    'Euler.GevreyGeneratingDerivativesNoOptions': 'Euler.GevreyGeneratingDerivatives',
    'Euler.LpCylinderCoefficientTimeInvestigation': 'Euler.LpCylinderCoefficientTime',
    'Euler.MeanPacketEnvelopeBoundsNoOptions': 'Euler.MeanPacketEnvelopeBounds',
    'Euler.PacketShiftArithmeticNoOptions': 'Euler.PacketShiftArithmetic',
    'Euler.ParentGeometryForwardChoiceNoOptions': 'Euler.ParentGeometryForwardChoice',
    'Euler.ParentGeometryJoinedChoiceInvestigation': 'Euler.ParentGeometryJoinedChoice',
    'Euler.TransversePacketCorrectorNoOptions': 'Euler.TransversePacketCorrector',
    'NavierStokes.ActualParticularDynamicsNoOptions': 'NavierStokes.ActualParticularDynamics',
    'NavierStokes.CorrectionInitializationNoOptions': 'NavierStokes.CorrectionInitialization',
    'NavierStokes.DiagonalJetBoundsNoOptions': 'NavierStokes.DiagonalJetBounds',
}
CMD_KW = ('variable', 'open', 'attribute', 'notation', 'local', 'scoped', 'prefix', 'infix', 'infixl',
          'infixr', 'postfix', 'alias', 'export', 'include', 'omit', 'universe', 'set_option',
          'section', 'namespace', 'end', 'noncomputable', 'private', 'protected', 'theorem', 'lemma',
          'def', 'abbrev', 'instance', 'structure', 'class', 'inductive', 'macro', 'syntax', 'elab',
          '#print', '#check', '#eval', 'example', 'deriving', 'import', '@[', '/-')
IN_START = ('omit', 'include', 'open', 'set_option', 'variable', 'universe', 'attribute', 'local', 'scoped')


def mpath(base, m):
    return os.path.join(base, m.replace('.', '/') + '.lean')


class Corpus:
    def __init__(self):
        self.D = [json.loads(l) for l in open(os.path.join(ROOT, 'out/corpus/ns/decls.jsonl'))]
        self.by = {d['name']: d for d in self.D}
        self.mains = [m['name'] for m in json.load(open(os.path.join(ROOT, 'out/corpus/ns/main_theorems.json')))['mainTheorems']]
        self.modules = [l.strip() for l in open(os.path.join(ROOT, 'out/corpus/ns/modules_built.txt')) if l.strip()]
        self.T = {d['name']: set(d['typeDeps']) | set(d['valueDeps']) for d in self.D}
        self._src = {}
        self._load_ilean()
        self.G = {n: self.T[n] | self.S.get(n, set()) for n in self.T}   # term + source references
        self.rT = collections.defaultdict(set)
        self.rG = collections.defaultdict(set)
        for a, bs in self.T.items():
            for b in bs:
                self.rT[b].add(a)
        for a, bs in self.G.items():
            for b in bs:
                self.rG[b].add(a)
        self.bymod = collections.defaultdict(list)
        for d in self.D:
            self.bymod[d['module']].append(d)

    # ---------------------------------------------------------------- sources
    def src(self, m):
        if m not in self._src:
            self._src[m] = open(mpath(NS, m), encoding='utf-8').read().split('\n')
        return self._src[m]

    def resolve(self, n, module=None):
        """Map a constant (constructor, projection, auxiliary ...) to the exported declaration that owns it."""
        while n and n not in self.by:
            if '.' not in n:
                return None
            n = n.rsplit('.', 1)[0]
        if not n:
            return None
        if module is not None and self.by[n]['module'] != module:
            return None
        return n

    def _load_ilean(self):
        cache = os.path.join(OUT, 'ilean_refs.json')
        if os.path.exists(cache):
            j = json.load(open(cache))
            self.S = {k: set(v) for k, v in j['S'].items()}
            self.cmd = {k: [tuple(x) for x in v] for k, v in j['cmd'].items()}
            self.imports = j['imports']
            return
        S = collections.defaultdict(set)
        cmd = collections.defaultdict(set)
        imports = {}
        for m in self.modules:
            j = json.load(open(os.path.join(ILEAN, m.replace('.', '/') + '.ilean')))
            imports[m] = [i[0] for i in j['directImports']]
            if m.startswith('ComparatorChallenges'):
                continue
            ranges = []
            for n, r in j['decls'].items():
                rn = self.resolve(n, m)
                if rn:
                    ranges.append((r[0], r[2], rn))
            for k, v in j['references'].items():
                k = json.loads(k)
                if 'c' not in k:
                    continue
                rn = self.resolve(k['c']['n'], k['c']['m'])
                if rn is None:
                    continue
                for u in v['usages']:
                    p = self.resolve(u[4], m) if len(u) > 4 and u[4] else None
                    if p is None:
                        c = [x for x in ranges if x[0] <= u[0] <= x[1]]
                        if c:
                            p = min(c, key=lambda x: x[1] - x[0])[2]
                    if p is None:
                        cmd[m].add((rn, u[0] + 1))
                    elif p != rn:
                        S[p].add(rn)
        self.S = dict(S)
        self.cmd = {k: sorted(v) for k, v in cmd.items()}
        self.imports = imports
        os.makedirs(OUT, exist_ok=True)
        json.dump({'S': {k: sorted(v) for k, v in S.items()}, 'cmd': self.cmd, 'imports': imports},
                  open(cache, 'w'))

    def cmd_keyword(self, m, line):
        """First word of the command that contains a command-level reference."""
        L = self.src(m)
        i = line - 1
        while i >= 0:
            s = L[i]
            if s and not s[0].isspace() and s.startswith(CMD_KW):
                w = s.split()[0]
                if w in ('local', 'scoped', 'private', 'noncomputable', 'protected') and len(s.split()) > 1:
                    w = w + ' ' + s.split()[1]
                return w
            i -= 1
        return '?'

    # ---------------------------------------------------------------- graph
    @staticmethod
    def closure(roots, nb):
        seen = set()
        st = list(roots)
        while st:
            n = st.pop()
            if n in seen:
                continue
            seen.add(n)
            st.extend(nb(n))
        return seen

    # ---------------------------------------------------------------- ranges
    def drange(self, d):
        """1-based inclusive line range to delete for a declaration, extended upward over `... in` prefixes."""
        if d['line'] is None:
            return None
        L = self.src(d['module'])
        a, b = d['line'], d['endLine']
        while a >= 2 and re.search(r'(^|\s)in\s*$', L[a - 2]) and not L[a - 2].lstrip().startswith('--'):
            j = a - 2
            k = j
            while k >= 0 and not L[k].startswith(IN_START):
                k -= 1
                if j - k > 12:
                    break
            if k < 0 or j - k > 12:
                break
            a = k + 1
        return a, b

    def attrs(self, d):
        """Attributes and keywords read from the source text inside the Lean-reported declaration range."""
        if d['line'] is None:
            return set()
        L = self.src(d['module'])
        head = ' '.join(L[d['line'] - 1:min(d['endLine'], d['line'] + 3)])
        doc = re.sub(r'/--.*?-/', ' ', ' '.join(L[d['line'] - 1:d['endLine']]), flags=re.S)[:400]
        out = set()
        for g in re.findall(r'@\[([^\]]*)\]', doc):
            for a in g.split(','):
                a = a.strip().split()
                if a:
                    out.add(a[0] if a[0] not in ('local', 'scoped') else a[1] if len(a) > 1 else a[0])
        m = re.match(r'\s*(?:@\[[^\]]*\]\s*)*((?:private |protected |noncomputable |local |scoped |unsafe |partial )*)(\w+)', doc)
        if m:
            if m.group(2) == 'abbrev':
                out.add('abbrev')
            if m.group(2) == 'instance':
                out.add('instance-kw')
            if m.group(2) == 'alias':
                out.add('alias')
            if 'local' in m.group(1):
                out.add('local')
        return out


# =================================================================== classification
def classify(C):
    by, T, G = C.by, C.T, C.G
    R = C.closure(C.mains, lambda n: T[n])                 # needed by the kernel
    RS = C.closure(C.mains, lambda n: G[n])                # ... plus named in the source of what is needed
    U = set(by) - R
    # special classes among the unreachable: uses that never show up as a term dependency
    special = {}
    for n in U:
        d = by[n]
        a = C.attrs(d)
        tags = set()
        if 'simp' in a:
            tags.add('simp')
        if a & {'ext', 'fun_prop', 'reducible', 'aesop', 'gcongr', 'norm_cast', 'positivity', 'coe', 'inherit_doc'}:
            tags.add('other-attribute')
        if d['kind'] == 'instance' or 'instance-kw' in a or d.get('instanceAttr'):
            tags.add('instance')
        if d.get('isClass'):
            tags.add('class')
        if 'abbrev' in a:
            tags.add('abbrev')
        if 'alias' in a:
            tags.add('alias')
        if d['line'] is None:
            tags.add('no-source-range')
        if tags:
            special[n] = tags
    # command-level references (variable, open, attribute, notation, #print ...) hold a declaration
    # only while the module containing the command is kept: fixpoint.
    keep = set(RS)
    held_roots = dict((n, set(t)) for n, t in special.items())
    cmdheld = collections.defaultdict(set)
    while True:
        kept_mods = {by[n]['module'] for n in keep} | set(HEAD_MODULES)
        new = set()
        for m in kept_mods:
            for n, line in C.cmd.get(m, []):
                if n in U:
                    cmdheld[n].add((m, line))
                if n not in keep:
                    new.add(n)
        add = C.closure(list(new) + [n for n in held_roots if n not in keep], lambda n: G[n]) - keep
        if not add:
            break
        keep |= add
    for n, where in cmdheld.items():
        kws = {C.cmd_keyword(m, l) for m, l in where}
        held_roots.setdefault(n, set()).update('cmd:' + k for k in kws)
    E1 = RS - R
    held = keep - RS
    dead = set(by) - keep
    return dict(R=R, RS=RS, U=U, E1=E1, held=held, dead=dead, held_roots=held_roots, special=special)


def abc_rule(C, K):
    """(a) alternative / superseded version of something reachable, (c) variant for another setting,
    (b) support never used.  Stated rule, applied in this order:
      a1  the declaration lives in one of the 13 cloned modules (REUSE.md 1.7)
      a2  a reachable declaration has the identical statement (exact key E; statementHash for non-theorems)
      a3  a reachable theorem is the same derivation with the same statement up to numerals (SV-N)
      c1  a reachable theorem has the same statement AND proof up to one renaming of project constants (SV-P)
      c2  a reachable theorem has the same statement up to numerals (N) -- another parameter value
      c3  the declaration lives in, or is used (term dependency, transitively) by a declaration of, a
          root result module: a module that the root files NavierStokes.lean / Euler.lean import,
          directly or through declaration-free hub modules, other than the two headline modules.
          These hold the paper-form statements (local theorem, periodic corollary in the paper's
          form, appendix results): it serves a result stated in another form or setting
      a4  the declaration lives in a module that nothing imports (an orphaned development, built only
          because the Lake glob builds every file), or every unreachable declaration at the top of a
          dependency chain above it lives in such a module
      b   everything else
    Non-theorems inherit: a definition, structure or instance that is not a1/a2 takes the majority
    class of the unreachable theorems that use it directly, (b) when none does."""
    by, R, U = C.by, K['R'], K['U']
    keys = {}
    p = os.path.join(ROOT, 'out/corpus/reuse/stmt_keys.jsonl')
    if os.path.exists(p):
        for l in open(p):
            j = json.loads(l)
            if j['name'] in by:
                keys[j['name']] = j
    idx = {k: collections.defaultdict(set) for k in ('kE', 'svN', 'svP', 'kN')}
    hidx = collections.defaultdict(set)
    for n in R:
        hidx[(by[n]['kind'], by[n]['statementHash'])].add(n)
        j = keys.get(n)
        if j and by[n]['kind'] == 'theorem':
            for k in idx:
                idx[k][j[k]].add(n)
    imp = C.imports
    icl = C.closure(HEAD_MODULES, lambda m: [i for i in imp.get(m, []) if i in imp])
    rcl = C.closure(['NavierStokes', 'Euler'], lambda m: [i for i in imp.get(m, []) if i in imp])
    def expand(ms):
        o = []
        for m in ms:
            if m in imp and not C.bymod.get(m):
                o += expand(imp[m])
            elif m in imp:
                o.append(m)
        return o
    root_results = [m for m in expand(imp['NavierStokes'] + imp['Euler']) if m not in HEAD_MODULES]
    orphan = {m for m in imp if m not in rcl and m not in icl and not m.startswith('ComparatorChallenges')}
    RR = C.closure([d['name'] for m in root_results for d in C.bymod.get(m, [])], lambda n: C.T[n])
    live_tops = [n for n in U if not C.rT[n] and by[n]['module'] not in orphan]
    below_live_top = C.closure(live_tops, lambda n: [x for x in C.T[n] if x in U])
    RO = {n for n in U if by[n]['module'] in orphan or n not in below_live_top}
    abc_rule.root_results = root_results
    abc_rule.orphan = sorted(orphan)
    out = {}
    for n in U:
        d = by[n]
        j = keys.get(n)
        r = None
        if d['module'] in CLONES:
            r = ('a', 'a1 cloned module', CLONES[d['module']])
        elif d['kind'] == 'theorem' and j and idx['kE'][j['kE']]:
            r = ('a', 'a2 identical statement', sorted(idx['kE'][j['kE']])[0])
        elif d['kind'] != 'theorem' and hidx[(d['kind'], d['statementHash'])] and d['statementDagSize'] >= 8:
            r = ('a', 'a2 identical statement', sorted(hidx[(d['kind'], d['statementHash'])])[0])
        elif d['kind'] == 'theorem' and j and idx['svN'][j['svN']]:
            r = ('a', 'a3 same derivation up to numerals', sorted(idx['svN'][j['svN']])[0])
        elif d['kind'] == 'theorem' and j and idx['svP'][j['svP']]:
            r = ('c', 'c1 same derivation up to renaming', sorted(idx['svP'][j['svP']])[0])
        elif d['kind'] == 'theorem' and j and idx['kN'][j['kN']]:
            r = ('c', 'c2 same statement up to numerals', sorted(idx['kN'][j['kN']])[0])
        elif n in RR:
            r = ('c', 'c3 serves a root result (paper-form statement)', '')
        elif n in RO:
            r = ('a', 'a4 orphaned development', '')
        out[n] = r
    for n in U:
        if out[n] is None and by[n]['kind'] != 'theorem':
            users = [u for u in C.rT[n] if by[u]['kind'] == 'theorem' and out.get(u)]
            users_all = [u for u in C.rT[n] if by[u]['kind'] == 'theorem']
            if users_all:
                c = collections.Counter(out[u][0] if out.get(u) else 'b' for u in users_all)
                top = c.most_common(1)[0][0]
                if top != 'b':
                    out[n] = (top, 'inherited from users', '')
    for n in U:
        if out[n] is None:
            out[n] = ('b', 'b no twin found', '')
    return out


def pct(a, b):
    return round(100.0 * a / b, 1) if b else 0.0


def analyze():
    C = Corpus()
    K = classify(C)
    by, R, RS, U = C.by, K['R'], K['RS'], K['U']
    abc = abc_rule(C, K)
    imp = C.imports
    proj = [m for m in C.modules if not m.startswith('ComparatorChallenges')]
    icl = C.closure(HEAD_MODULES, lambda m: [i for i in imp.get(m, []) if i in imp])
    rcl = C.closure(['NavierStokes', 'Euler'], lambda m: [i for i in imp.get(m, []) if i in imp])
    flines = {m: len(C.src(m)) - (1 if C.src(m)[-1] == '' else 0) for m in proj}

    def dl(n):
        r = C.drange(by[n])
        return (r[1] - r[0] + 1) if r else 0

    A = {}
    A['declarations'] = len(by)
    A['reachable'] = len(R)
    A['unreachable'] = len(U)
    A['unreachablePct'] = pct(len(U), len(by))
    kinds = ['theorem', 'def', 'instance', 'structure', 'inductive']
    A['byKind'] = {k: {'all': sum(1 for d in C.D if d['kind'] == k),
                       'unreachable': sum(1 for n in U if by[n]['kind'] == k)} for k in kinds}
    for k in kinds:
        A['byKind'][k]['pct'] = pct(A['byKind'][k]['unreachable'], A['byKind'][k]['all'])
    A['byLibrary'] = {}
    for lib in ('NavierStokes', 'Euler'):
        al = [d for d in C.D if d['module'].split('.')[0] == lib]
        un = [d for d in al if d['name'] in U]
        A['byLibrary'][lib] = {'all': len(al), 'unreachable': len(un), 'pct': pct(len(un), len(al)),
                               'allTheorems': sum(1 for d in al if d['kind'] == 'theorem'),
                               'unreachableTheorems': sum(1 for d in un if d['kind'] == 'theorem')}
    tot_lines = sum(flines.values())
    decl_lines_all = sum(dl(d['name']) for d in C.D)
    decl_lines_un = sum(dl(n) for n in U)
    A['lines'] = {'sourceLinesAll': tot_lines, 'declLinesAll': decl_lines_all, 'declLinesUnreachable': decl_lines_un,
                  'pctOfDeclLines': pct(decl_lines_un, decl_lines_all), 'pctOfSourceLines': pct(decl_lines_un, tot_lines)}
    A['proofSize'] = {'all': sum(d['proofSize'] for d in C.D if d['kind'] == 'theorem'),
                      'unreachable': sum(by[n]['proofSize'] for n in U if by[n]['kind'] == 'theorem')}
    A['proofSize']['pct'] = pct(A['proofSize']['unreachable'], A['proofSize']['all'])
    # modules
    mrows = []
    for m in proj:
        ds = C.bymod.get(m, [])
        un = [d for d in ds if d['name'] in U]
        mrows.append({'module': m, 'decls': len(ds), 'unreachable': len(un), 'lines': flines[m],
                      'unreachableLines': sum(dl(d['name']) for d in un),
                      'inHeadlineImportClosure': m in icl, 'inRootImportClosure': m in rcl,
                      'clone': CLONES.get(m)})
    whole = [r for r in mrows if r['decls'] > 0 and r['unreachable'] == r['decls']]
    nodecl = [r for r in mrows if r['decls'] == 0]
    A['modules'] = {
        'project': len(proj), 'withDecls': sum(1 for r in mrows if r['decls']),
        'withoutDecls': [r['module'] for r in nodecl],
        'headlineImportClosure': len([m for m in icl if m in flines]),
        'rootImportClosure': len([m for m in rcl if m in flines]),
        'importedByNeither': len([m for m in proj if m not in icl and m not in rcl]),
        'whollyUnreachable': len(whole), 'whollyUnreachableDecls': sum(r['decls'] for r in whole),
        'whollyUnreachableLines': sum(r['lines'] for r in whole),
        'whollyUnreachableInsideHeadlineClosure': sum(1 for r in whole if r['inHeadlineImportClosure']),
        'whollyUnreachableOutsideHeadlineClosure': sum(1 for r in whole if not r['inHeadlineImportClosure']),
        'whollyUnreachableOnlyFromRoots': sum(1 for r in whole if not r['inHeadlineImportClosure'] and r['inRootImportClosure']),
        'whollyUnreachableOrphans': sum(1 for r in whole if not r['inHeadlineImportClosure'] and not r['inRootImportClosure']),
        'partly': sum(1 for r in mrows if 0 < r['unreachable'] < r['decls']),
        'fullyReachable': sum(1 for r in mrows if r['decls'] and r['unreachable'] == 0),
        'majorityUnreachable': sum(1 for r in mrows if r['decls'] and 0.5 <= r['unreachable'] / r['decls'] < 1),
    }
    A['clones'] = [{'module': r['module'], 'base': r['clone'], 'lines': r['lines'], 'decls': r['decls'],
                    'unreachable': r['unreachable'], 'baseDecls': len(C.bymod.get(r['clone'], [])),
                    'baseUnreachable': sum(1 for d in C.bymod.get(r['clone'], []) if d['name'] in U),
                    'importedByHeadlineClosure': r['inHeadlineImportClosure']} for r in mrows if r['clone']]
    # classes of non-term use
    tagc = collections.Counter()
    for n, tags in K['held_roots'].items():
        if n in U:
            for t in tags:
                tagc[t] += 1
    A['nonTerm'] = {
        'elaborationOnlyDepsOfHeadlines': len(K['E1']),
        'elaborationOnlyByKind': dict(collections.Counter(by[n]['kind'] for n in K['E1'])),
        'heldRootsByTag': dict(tagc.most_common()),
        'heldRoots': sum(1 for n in K['held_roots'] if n in U and n not in RS),
        'held': len(K['held']), 'heldByKind': dict(collections.Counter(by[n]['kind'] for n in K['held'])),
        'dead': len(K['dead']), 'deadByKind': dict(collections.Counter(by[n]['kind'] for n in K['dead'])),
        'deadLines': sum(dl(n) for n in K['dead']), 'heldLines': sum(dl(n) for n in K['held']),
        'e1Lines': sum(dl(n) for n in K['E1']),
    }
    # how the source-reference edges out of reachable declarations that are not term edges arise
    # (a) / (b) / (c)
    ac = collections.Counter()
    al = collections.Counter()
    for n in U:
        ac[(abc[n][0], abc[n][1], by[n]['kind'] == 'theorem')] += 1
        al[abc[n][0]] += dl(n)
    A['abc'] = {'byRule': [{'class': k[0], 'rule': k[1], 'theorem': k[2], 'n': v} for k, v in sorted(ac.items())],
                'byClass': {c: {'decls': sum(v for k, v in ac.items() if k[0] == c),
                                'theorems': sum(v for k, v in ac.items() if k[0] == c and k[2]),
                                'lines': al[c]} for c in 'abc'}}
    # root result modules: what the project's root files state that the headlines do not use
    rr = abc_rule.root_results
    root_decls = [d['name'] for m in rr for d in C.bymod.get(m, [])]
    RR = C.closure(root_decls, lambda n: C.T[n])
    A['rootResults'] = {'modules': rr, 'declsInThoseModules': len(root_decls),
                        'unreachableDeclsUsedByThem': len(RR & U),
                        'unreachableTheoremsUsedByThem': sum(1 for n in RR & U if by[n]['kind'] == 'theorem'),
                        'unreachableLinesUsedByThem': sum(dl(n) for n in RR & U)}
    A['orphanModules'] = {'modules': abc_rule.orphan, 'n': len(abc_rule.orphan),
                          'decls': sum(len(C.bymod.get(m, [])) for m in abc_rule.orphan),
                          'lines': sum(flines[m] for m in abc_rule.orphan)}
    # unreachable roots: unreachable declarations nothing depends on (tops of dead islands)
    tops = [n for n in U if not C.rT[n]]
    A['islands'] = {'tops': len(tops), 'topsTheorems': sum(1 for n in tops if by[n]['kind'] == 'theorem'),
                    'leafShare': pct(len(tops), len(U))}
    os.makedirs(OUT, exist_ok=True)
    json.dump(A, open(os.path.join(OUT, 'analysis.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(mrows, open(os.path.join(OUT, 'modules.json'), 'w'), indent=0)
    with open(os.path.join(OUT, 'unreachable.jsonl'), 'w') as f:
        for n in sorted(U):
            d = by[n]
            f.write(json.dumps({'name': n, 'kind': d['kind'], 'module': d['module'], 'line': d['line'],
                                'endLine': d['endLine'], 'lines': dl(n),
                                'status': 'elaboration-only' if n in K['E1'] else 'held' if n in K['held'] else 'dead',
                                'tags': sorted(K['held_roots'].get(n, [])), 'abc': abc[n][0], 'rule': abc[n][1],
                                'twin': abc[n][2], 'users': len(C.rT[n])}, ensure_ascii=False) + '\n')
    # elaboration-only dependencies: the list, with the tactic that names each one
    TAC = re.compile(r'\b(simp_rw|simp only|simpa only|simpa|simp|dsimp|rw|rewrite|erw|unfold|norm_num|field_simp|ring_nf|'
                     r'linarith|nlinarith|positivity|exact|refine|apply|change|convert|aesop|omega|subst|calc|have|show)\b')
    ctx = collections.Counter()
    with open(os.path.join(OUT, 'elaboration_only.jsonl'), 'w') as f:
        for n in sorted(K['E1']):
            d = by[n]
            users = sorted(u for u in C.rG[n] if u in R)
            short = n.split('.')[-1]
            tacs = set()
            for u in users:
                du = by[u]
                body = ' '.join(C.src(du['module'])[du['line'] - 1:du['endLine']])
                for mt in re.finditer(re.escape(short), body):
                    prev = TAC.findall(body[:mt.start()])
                    tacs.add(prev[-1] if prev else 'term')
            for t in tacs:
                ctx[t] += 1
            txt = ' '.join(C.src(d['module'])[d['line'] - 1:d['endLine']]).strip()
            f.write(json.dumps({'name': n, 'module': d['module'], 'line': d['line'], 'simpAttr': 'simp' in C.attrs(d),
                                'rflProof': bool(re.search(r':=\s*(by\s+)?(rfl|Iff\.rfl)\s*$', txt)),
                                'namedBy': users[:5], 'namedByCount': len(users), 'tactics': sorted(tacs)}, ensure_ascii=False) + '\n')
    A['nonTerm']['elaborationOnlyNamedIn'] = dict(ctx.most_common())
    sh = [n for n, t in K['special'].items() if 'simp' in t]
    A['nonTerm']['unreachableSimpTagged'] = len(sh)
    A['nonTerm']['unreachableSimpTaggedRfl'] = sum(1 for n in sh if re.search(
        r':=\s*(by\s+)?(rfl|Iff\.rfl)\s*$', ' '.join(C.src(by[n]['module'])[by[n]['line'] - 1:by[n]['endLine']]).strip()))
    A['nonTerm']['elaborationOnlyRfl'] = sum(1 for n in K['E1'] if re.search(
        r':=\s*(by\s+)?(rfl|Iff\.rfl)\s*$', ' '.join(C.src(by[n]['module'])[by[n]['line'] - 1:by[n]['endLine']]).strip()))
    json.dump(A, open(os.path.join(OUT, 'analysis.json'), 'w'), indent=1, ensure_ascii=False)
    # seeded hand-read sample of 40
    rng = random.Random(SEED)
    samp = rng.sample(sorted(U), 40)
    with open(os.path.join(OUT, 'sample40.md'), 'w') as f:
        for i, n in enumerate(samp):
            d = by[n]
            L = C.src(d['module'])
            r = C.drange(d) or (1, 1)
            f.write('## %d. `%s` (%s) %s:%s-%s\nrule: %s / %s twin=%s users=%d tags=%s status=%s\n```lean\n%s\n```\n\n' % (
                i + 1, n, d['kind'], d['module'], r[0], r[1], abc[n][0], abc[n][1], abc[n][2], len(C.rT[n]),
                sorted(K['held_roots'].get(n, [])), 'elab-only' if n in K['E1'] else 'held' if n in K['held'] else 'dead',
                '\n'.join(L[max(0, r[0] - 1):min(r[1], r[0] + 24)])))
    json.dump([{'i': i + 1, 'name': n, 'rule': abc[n][0], 'ruleDetail': abc[n][1]} for i, n in enumerate(samp)],
              open(os.path.join(OUT, 'sample40.json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(A, indent=1, ensure_ascii=False)[:6000])
    return C, K, abc


# =================================================================== plans
def separable(C, names):
    """Split a deletion set into declarations whose source range can be removed and those that cannot
    (no range, or range nested inside / containing a declaration that stays)."""
    names = set(names)
    ok, bad = set(), {}
    per = collections.defaultdict(list)
    for n in names:
        per[C.by[n]['module']].append(n)
    for m, ns in per.items():
        rngs = {d['name']: C.drange(d) for d in C.bymod[m]}
        stay = [(r, n) for n, r in rngs.items() if n not in names and r]
        for n in ns:
            r = rngs[n]
            if r is None:
                bad[n] = 'no source range'
                continue
            clash = [k for (kr, k) in stay if not (kr[1] < r[0] or kr[0] > r[1])]
            if clash:
                bad[n] = 'range overlaps kept ' + clash[0]
            else:
                ok.add(n)
    return ok, bad


def up_closure(C, names, allowed):
    """Everything that depends (term or source reference) on `names`, restricted to `allowed`."""
    return C.closure(names, lambda n: [u for u in C.rG[n] if u in allowed])


def make_plan(stage):
    C = Corpus()
    K = classify(C)
    by, U, R = C.by, K['U'], K['R']
    rng = random.Random(SEED)
    os.makedirs(os.path.join(OUT, 'plans'), exist_ok=True)
    plan = {'stage': stage, 'seed': SEED}
    if stage == 'control':
        # 20 used declarations, sampled uniformly from the term-reachable set (headline theorems themselves excluded)
        pool = sorted(n for n in R if n not in C.mains and C.rT[n] and by[n]['line'] is not None)
        picks = []
        for n in rng.sample(pool, 60):
            ok, bad = separable(C, [n])
            if ok:
                picks.append(n)
            if len(picks) == 20:
                break
        plan['controls'] = []
        desc = {}
        for n in picks:
            m = by[n]['module']
            users = sorted(C.rT[n])
            same = [u for u in users if by[u]['module'] == m]
            if same:
                tgt = m
            else:
                # cheapest target: the user module with the fewest modules between it and m
                best = None
                for um in sorted({by[u]['module'] for u in users}):
                    anc = C.closure([um], lambda x: [i for i in C.imports.get(x, []) if i in C.imports])
                    if m not in desc:
                        rimp = collections.defaultdict(set)
                        for a, bs in C.imports.items():
                            for b in bs:
                                rimp[b].add(a)
                        desc[m] = C.closure([m], lambda x: rimp[x])
                    cost = len(anc & desc[m])
                    if best is None or cost < best[0]:
                        best = (cost, um)
                tgt = best[1]
            plan['controls'].append({'name': n, 'kind': by[n]['kind'], 'module': m, 'target': tgt,
                                     'users': len(users), 'sameModuleUser': bool(same)})
    else:
        if stage == 'sample':
            pool = sorted(n for n in U if by[n]['kind'] == 'theorem')
            picks = rng.sample(pool, 300)
            dele = up_closure(C, picks, U)
            plan['sampled'] = picks
            plan['note'] = ('300 theorems sampled uniformly from all term-unreachable theorems (special classes and '
                            'elaboration-only ones included, so the sample tests the term graph itself), plus every '
                            'unreachable declaration that depends on one of them, plus every wholly unreachable module')
            whole = [m for m, ds in C.bymod.items() if ds and all(d['name'] in U for d in ds)]
            for m in whole:
                dele |= {d['name'] for d in C.bymod[m]}
            dele = up_closure(C, dele, U)
        elif stage == 'full':
            dele = set(K['dead'])
        elif stage == 'all':
            dele = set(U) - K['E1']
            dele -= C.closure(K['E1'], lambda n: C.G[n])
        else:
            raise SystemExit('unknown stage')
        ok, bad = separable(C, dele)
        # a declaration that cannot be removed keeps its dependencies
        while bad:
            keepc = C.closure(list(bad), lambda n: C.G[n])
            ok2 = ok - keepc
            if ok2 == ok:
                break
            ok, bad2 = separable(C, ok2)
            bad.update(bad2)
            bad.update({n: 'needed by a declaration that cannot be removed' for n in (dele - ok - set(bad))})
            if not bad2:
                break
        plan['delete'] = sorted(ok)
        plan['notSeparable'] = bad
        _, deleted_mods, _ = layout(C, ok)
        pb = {}
        for n in ok:
            why = []
            if n in K['E1']:
                why.append('named in the source of a reachable declaration')
            if any(u not in ok for u in C.rG[n]):
                why.append('referenced by a declaration that stays')
            for m, cl in C.cmd.items():
                pass
            pb[n] = why
        for m, cl in C.cmd.items():
            if m in deleted_mods:
                continue
            for n, line in cl:
                if n in ok:
                    pb[n].append('named in a `%s` command of %s' % (C.cmd_keyword(m, line), m))
        plan['predictedBreaks'] = {n: sorted(set(w)) for n, w in pb.items() if w}
        plan['deletedModules'] = sorted(deleted_mods)
    p = os.path.join(OUT, 'plans', stage + '.json')
    json.dump(plan, open(p, 'w'), indent=0, ensure_ascii=False)
    print(p, {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in plan.items()})
    return plan


# =================================================================== apply
def load_plan(path, restore=None):
    plan = json.load(open(path))
    dele = set(plan['delete'])
    if restore:
        C = None
        rs = {l.strip() for l in open(restore) if l.strip() and not l.startswith('#')}
        dele -= rs
    return plan, dele


def restore_closure(C, dele, restore):
    """Removing names from a deletion set also restores everything they depend on."""
    need = C.closure(restore, lambda n: C.G[n])
    return dele - need


def layout(C, dele):
    """Files of the trimmed corpus: {module: text or None (deleted)}; returns (texts, deleted modules, stats)."""
    by = C.by
    per = collections.defaultdict(list)
    for n in dele:
        per[by[n]['module']].append(n)
    proj = [m for m in C.modules if not m.startswith('ComparatorChallenges')]
    deleted = set()
    for m in proj:
        ds = C.bymod.get(m, [])
        if ds and all(d['name'] in dele for d in ds):
            deleted.add(m)
    # modules without declarations (import hubs): deleted when every project module they import is deleted.
    # The two root files stay; imports of deleted modules are dropped from them and the headline module
    # of the library is added, so that the root still builds the headline theorems.
    imp = C.imports
    changed = bool(deleted)
    while changed:
        changed = False
        for m in proj:
            if m in deleted or C.bymod.get(m) or m in ROOT_FILES:
                continue
            pi = [i for i in imp.get(m, []) if i in imp]
            if pi and all(i in deleted for i in pi):
                deleted.add(m)
                changed = True

    def repl(m, seen=None):
        """Imports that stand in for a deleted module: its own imports, recursively."""
        seen = seen if seen is not None else set()
        out = []
        for i in imp.get(m, []):
            if i in deleted:
                if i not in seen:
                    seen.add(i)
                    out.extend(repl(i, seen))
            else:
                out.append(i)
        return out

    texts = {}
    removed_lines = 0
    for m in proj:
        if m in deleted:
            texts[m] = None
            continue
        L = list(C.src(m))
        kill = set()
        for n in per.get(m, []):
            a, b = C.drange(by[n])
            kill.update(range(a, b + 1))
        if m in ROOT_FILES:
            if not any(i in deleted for i in imp.get(m, [])):
                texts[m] = '\n'.join(L)
            else:
                keep_i = [i for i in imp.get(m, []) if i not in deleted]
                keep_i += [i for i in ROOT_FILES[m] if i not in keep_i]
                texts[m] = ''.join('import %s\n' % i for i in keep_i)
            continue
        out = []
        done_imports = set()
        for i, s in enumerate(L, 1):
            if i in kill:
                removed_lines += 1
                continue
            mm = re.match(r'^import\s+(\S+)\s*$', s)
            if mm:
                tgt = mm.group(1)
                if tgt in deleted:
                    for r in repl(tgt):
                        if r not in done_imports and ('import ' + r) not in L:
                            out.append('import ' + r)
                            done_imports.add(r)
                    continue
                if tgt in done_imports:
                    continue
                done_imports.add(tgt)
            out.append(s)
        texts[m] = '\n'.join(out)
    layout.open_edits = repair_opens(C, texts, dele) if dele else []
    return texts, deleted, removed_lines


IDENT = re.compile(r"^[A-Za-z_\u00c0-\uffff][\w.'\u00c0-\uffff]*$")


def file_namespaces(L):
    """Full names of the namespaces a file enters, and the namespace in force at each line (1-based)."""
    stack = []      # (kind, name)
    names = set()
    at = {}
    for i, s in enumerate(L, 1):
        cur = '.'.join(n for k, n in stack if k == 'ns')
        at[i] = cur
        m = re.match(r'^(namespace|section|end)\b\s*(\S*)', s)
        if not m:
            continue
        if m.group(1) == 'namespace' and m.group(2):
            stack.append(('ns', m.group(2)))
            full = '.'.join(n for k, n in stack if k == 'ns')
            parts = full.split('.')
            for j in range(1, len(parts) + 1):
                names.add('.'.join(parts[:j]))
        elif m.group(1) == 'section':
            stack.append(('sec', m.group(2)))
        elif m.group(1) == 'end' and stack:
            stack.pop()
    return names, at


def prefixes(name):
    parts = name.split('.')
    return ['.'.join(parts[:j]) for j in range(1, len(parts))]


def repair_opens(C, texts, dele):
    """`open X` fails with "unknown namespace" once nothing declares X any more.  A namespace of the
    project that only deleted declarations (or deleted files) kept alive is removed from the `open`
    commands of the files that stay.  Returns the list of edits."""
    alive, orig = set(), set()
    for d in C.D:
        ps = prefixes(d['userName'])
        orig.update(ps)
        if d['name'] not in dele:
            alive.update(ps)
    for m in texts:
        ns, _ = file_namespaces(C.src(m))
        orig |= ns
        if texts[m] is not None:
            alive |= file_namespaces(texts[m].split('\n'))[0]
    edits = []
    for m, t in texts.items():
        if t is None or 'open ' not in t:
            continue
        L = t.split('\n')
        _, at = file_namespaces(L)
        out = []
        i = 0
        changed = False
        while i < len(L):
            s = L[i]
            if not s.startswith('open '):
                out.append(s)
                i += 1
                continue
            block = [s]
            j = i + 1
            while j < len(L) and L[j][:1] in (' ', '\t') and L[j].strip() and all(
                    IDENT.match(w) for w in L[j].split()) and not block[-1].rstrip().endswith(' in'):
                block.append(L[j])
                j += 1
            cur = at[i + 1]
            scopes = [''] + ['.'.join(cur.split('.')[:k]) + '.' for k in range(1, len(cur.split('.')) + 1)] if cur else ['']
            new_block = []
            dropped = []
            stop = False
            for bi, b in enumerate(block):
                toks = b.split()
                keep = []
                for ti, w in enumerate(toks):
                    if stop or (bi == 0 and ti == 0) or w in ('scoped',):
                        keep.append(w)
                        continue
                    if w in ('in', 'hiding', 'renaming') or w.startswith('('):
                        stop = True
                        keep.append(w)
                        continue
                    cands = [sc + w for sc in scopes]
                    if any(c in orig for c in cands) and not any(c in alive for c in cands):
                        dropped.append(w)
                    else:
                        keep.append(w)
                new_block.append((b[:len(b) - len(b.lstrip())] + ' '.join(keep)) if keep else None)
            if dropped:
                changed = True
                edits.append({'module': m, 'line': i + 1, 'dropped': dropped})
                rest = [b for b in new_block if b is not None and b.strip()]
                words = ' '.join(rest).split()
                body = [w for w in words if w not in ('open', 'scoped', 'in')]
                if body:
                    out.extend(rest)
                # an `open` left with no namespace is removed altogether (also the `open ... in` form)
            else:
                out.extend(block)
            i = j
        if changed:
            texts[m] = '\n'.join(out)
    return edits


def apply_plan(path, restore=None, quiet=False):
    C = Corpus()
    plan, dele = load_plan(path)
    if restore:
        rs = [l.strip() for l in open(restore) if l.strip() and not l.startswith('#')]
        dele = restore_closure(C, dele, [r for r in rs if r in C.by])
    return apply_set(C, dele, quiet)


def apply_set(C, dele, quiet=False):
    texts, deleted, removed = layout(C, dele)
    changed = 0
    for m, t in texts.items():
        p = mpath(WORK, m)
        if t is None:
            if os.path.exists(p):
                os.remove(p)
                changed += 1
            continue
        cur = open(p, encoding='utf-8').read() if os.path.exists(p) else None
        if cur != t:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, 'w', encoding='utf-8').write(t)
            changed += 1
    if not quiet:
        print('applied: %d declarations deleted, %d modules deleted, %d files written/removed, %d declaration lines removed'
              % (len(dele), len(deleted), changed, removed))
    return C, dele, texts, deleted


def reset_work():
    C = Corpus()
    C2, dele, texts, deleted = apply_set(C, set(), quiet=True)
    print('working copy reset to the original sources')


# =================================================================== build
def lake_build(tag, targets, timeout=None):
    os.makedirs(os.path.join(OUT, 'logs'), exist_ok=True)
    log = os.path.join(OUT, 'logs', tag + '.log')
    env = dict(os.environ)
    env['PATH'] = os.path.expanduser('~/.elan/bin') + ':' + env['PATH']
    t0 = time.time()
    with open(log, 'w') as f:
        rc = subprocess.call(['lake', 'build'] + targets, cwd=WORK, stdout=f, stderr=subprocess.STDOUT, env=env, timeout=timeout)
    dt = time.time() - t0
    res = parse_log(log)
    res.update({'tag': tag, 'targets': targets, 'exit': rc, 'seconds': round(dt, 1)})
    json.dump(res, open(os.path.join(OUT, 'logs', tag + '.json'), 'w'), indent=1, ensure_ascii=False)
    return res


def parse_log(log):
    errs = []
    axioms = {}
    built = 0
    cpu = 0.0
    failed = []
    for l in open(log, errors='replace'):
        m = re.match(r'^error: (\S+\.lean):(\d+):(\d+): (.*)', l)
        if m:
            errs.append({'file': m.group(1), 'line': int(m.group(2)), 'msg': m.group(4).strip()[:300]})
        m = re.match(r"^info: \S+: '(\S+)' depends on axioms: \[(.*)\]", l)
        if m:
            axioms[m.group(1)] = sorted(x.strip() for x in m.group(2).split(','))
        m = re.match(r'^[✔ℹ⚠✖] \[\d+/\d+\] (Built|Building) (\S+)(?: \((\d+(?:\.\d+)?)(ms|s)\))?', l)
        if m and m.group(1) == 'Built':
            built += 1
            if m.group(3):
                cpu += float(m.group(3)) / (1000 if m.group(4) == 'ms' else 1)
        m = re.match(r'^- (\S+)$', l)
        if m:
            failed.append(m.group(1))
        if l.startswith('error:') and not re.match(r'^error: \S+\.lean:\d+', l):
            errs.append({'file': '', 'line': 0, 'msg': l.strip()[:300]})
    return {'errors': errs, 'axioms': axioms, 'modulesBuilt': built, 'sumModuleSeconds': round(cpu, 1), 'failedTargets': failed}


def full_error_messages(log):
    """Each error of a Lake log as its whole message: the `error:` line and the lines up to the next message."""
    msgs, cur = [], None
    for l in open(log, errors='replace'):
        if re.match(r'^(error|warning|info|trace): ', l) or re.match(r'^[✔ℹ⚠✖] \[\d+/\d+\] ', l):
            if cur is not None:
                msgs.append(cur)
            cur = l if l.startswith('error:') else None
        elif cur is not None:
            cur += l
    if cur is not None:
        msgs.append(cur)
    return msgs


def names_declaration(tag, name):
    """True when some error message of the build (whole message, not only its first line) names the declaration."""
    short = name.split('.')[-1]
    return any(short in m for m in full_error_messages(os.path.join(OUT, 'logs', tag + '.log')))


def control_reparse():
    """Recompute errorNamesDeclaration from the stored control logs; nothing is built."""
    path = os.path.join(OUT, 'control_results.json')
    rows = json.load(open(path))
    for i, r in enumerate(rows):
        new = names_declaration('control_%02d' % (i + 1), r['name'])
        if new != r['errorNamesDeclaration']:
            print(i + 1, r['name'], 'errorNamesDeclaration', r['errorNamesDeclaration'], '->', new)
        r['errorNamesDeclaration'] = new
    json.dump(rows, open(path, 'w'), indent=1, ensure_ascii=False)
    print('named', sum(1 for r in rows if r['errorNamesDeclaration']), 'of', len(rows), '; failed', sum(1 for r in rows if r['exit']))


def compare_export(pred_path, exp_dir):
    """Compare the predicted trimmed graph with the one Lean re-exported from the trimmed build, on every field."""
    P = {d['name']: d for d in map(json.loads, open(pred_path))}
    E = {d['name']: d for d in map(json.loads, open(os.path.join(exp_dir, 'decls.jsonl')))}
    mains = [m['name'] for m in json.load(open(os.path.join(ROOT, 'out/corpus/ns/main_theorems.json')))['mainTheorems']]
    seen, todo = set(), [m for m in mains if m in E]
    while todo:
        n = todo.pop()
        if n in seen:
            continue
        seen.add(n)
        todo.extend(x for x in set(E[n]['typeDeps']) | set(E[n]['valueDeps']) if x in E and x not in seen)
    fields = collections.Counter()
    beyond = []
    for n in sorted(set(P) & set(E)):
        diff = [k for k in sorted(set(P[n]) | set(E[n])) if P[n].get(k) != E[n].get(k)]
        fields.update(diff)
        if set(diff) - {'line', 'endLine'}:
            beyond.append(n)
    out = {
        'declarationsPredicted': len(P), 'declarationsReExported': len(E), 'namesEqual': set(P) == set(E),
        'fieldsCompared': 'all',
        'fieldsDiffering': dict(sorted(fields.items(), key=lambda kv: -kv[1])),
        'declarationsDifferingBeyondLines': len(beyond),
        'ofWhichReachable': sum(1 for n in beyond if n in seen),
        'auxProofSizeOverThose': {'predicted': sum(P[n].get('auxProofSize', 0) for n in beyond),
                                  'reExported': sum(E[n].get('auxProofSize', 0) for n in beyond)},
        'namesDifferingBeyondLines': beyond,
        'reachableReExported': len(seen),
        'axiomsFileIdenticalToOriginal': open(os.path.join(exp_dir, 'axioms.json'), 'rb').read() ==
                                         open(os.path.join(ROOT, 'out/corpus/ns/axioms.json'), 'rb').read(),
        'writtenBy': 'bench/deadcode.py compare',
    }
    json.dump(out, open(os.path.join(exp_dir, 'compare.json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != 'namesDifferingBeyondLines'}, indent=1))


def run_control():
    plan = json.load(open(os.path.join(OUT, 'plans', 'control.json')))
    C = Corpus()
    rows = []
    for i, c in enumerate(plan['controls']):
        apply_set(C, {c['name']}, quiet=True)
        r = lake_build('control_%02d' % (i + 1), [c['target']])
        named = names_declaration('control_%02d' % (i + 1), c['name'])    # whole message: Lean may name it in a hint line
        rows.append(dict(c, exit=r['exit'], seconds=r['seconds'], nErrors=len(r['errors']),
                         firstError=(r['errors'][0] if r['errors'] else None), errorNamesDeclaration=named,
                         modulesBuilt=r['modulesBuilt']))
        print(i + 1, c['name'], 'exit', r['exit'], 'errors', len(r['errors']), 'named', named, r['seconds'], flush=True)
        json.dump(rows, open(os.path.join(OUT, 'control_results.json'), 'w'), indent=1, ensure_ascii=False)
    reset_work()


# =================================================================== after-graph and sizes
def trimgraph(path, restore, outp):
    C = Corpus()
    plan, dele = load_plan(path)
    if restore:
        rs = [l.strip() for l in open(restore) if l.strip() and not l.startswith('#')]
        dele = restore_closure(C, dele, [r for r in rs if r in C.by])
    n = 0
    with open(outp, 'w') as f:
        for l in open(os.path.join(ROOT, 'out/corpus/ns/decls.jsonl')):
            if json.loads(l)['name'] not in dele:
                f.write(l)
                n += 1
    print('wrote', outp, n, 'declarations')


def outline_rerun(decls_path, outdir):
    """Run bench/outline.py unchanged on another declaration graph, writing to a separate directory."""
    import shutil
    sys.path.insert(0, os.path.join(ROOT, 'bench'))
    import outline
    cdir = os.path.join(outdir, 'corpus')
    os.makedirs(cdir, exist_ok=True)
    shutil.copy(decls_path, os.path.join(cdir, 'decls.jsonl'))
    shutil.copy(os.path.join(ROOT, 'out/corpus/ns/main_theorems.json'), cdir)
    src_r = os.path.join(ROOT, 'out/corpus/outline/ratings.json')
    if os.path.exists(src_r):
        shutil.copy(src_r, outdir)
    outline.CORPUS = cdir
    outline.OUT = outdir
    outline.main()
    a = json.load(open(os.path.join(ROOT, 'out/corpus/outline/shape.json')))
    b = json.load(open(os.path.join(outdir, 'shape.json')))
    diffs = []

    def walk(x, y, path):
        if isinstance(x, dict) and isinstance(y, dict):
            for k in sorted(set(x) | set(y)):
                if k not in x or k not in y:
                    diffs.append((path + '/' + k, 'only in ' + ('original' if k in x else 'trimmed')))
                else:
                    walk(x[k], y[k], path + '/' + k)
        elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
            for i, (u, v) in enumerate(zip(x, y)):
                walk(u, v, path + '/%d' % i)
        elif x != y:
            diffs.append((path, '%r -> %r' % (x, y)))
    walk(a, b, '')
    same = {}
    for f in sorted(os.listdir(outdir)):
        o = os.path.join(ROOT, 'out/corpus/outline', f)
        if os.path.isfile(os.path.join(outdir, f)) and os.path.exists(o):
            same[f] = open(o, 'rb').read() == open(os.path.join(outdir, f), 'rb').read()
    json.dump({'shapeDifferences': diffs, 'filesIdentical': same}, open(os.path.join(outdir, 'compare.json'), 'w'), indent=1)
    print('shape.json differences:', len(diffs), diffs[:20])
    print('files byte-identical to out/corpus/outline:', same)


def tables():
    """Markdown tables for DEADCODE.md from the JSON written by the other subcommands."""
    A = json.load(open(os.path.join(OUT, 'analysis.json')))
    M = json.load(open(os.path.join(OUT, 'modules.json')))
    o = []
    w = o.append
    f = lambda x: f'{x:,}'
    kd = lambda d: ', '.join('%s %s' % (f(v), k) for k, v in sorted(d.items(), key=lambda kv: -kv[1]))
    w('### T1. Unreachable declarations by kind\n')
    w('| kind | all | not reachable from a headline theorem | share |\n|---|---:|---:|---:|')
    for k, v in A['byKind'].items():
        w('| %s | %s | %s | %s%% |' % (k, f(v['all']), f(v['unreachable']), v['pct']))
    w('| **all** | %s | %s | %s%% |\n' % (f(A['declarations']), f(A['unreachable']), A['unreachablePct']))
    w('### T2. By library\n')
    w('| library | declarations | unreachable | share | theorems | unreachable theorems | share |\n|---|---:|---:|---:|---:|---:|---:|')
    for k, v in A['byLibrary'].items():
        w('| %s | %s | %s | %s%% | %s | %s | %s%% |' % (k, f(v['all']), f(v['unreachable']), v['pct'], f(v['allTheorems']),
                                                    f(v['unreachableTheorems']), pct(v['unreachableTheorems'], v['allTheorems'])))
    L = A['lines']
    w('\n### T3. By source lines\n')
    w('| measure | lines |\n|---|---:|')
    w('| all lines of the 2,657 project files | %s |' % f(L['sourceLinesAll']))
    w('| lines inside a declaration (Lean declaration ranges, plus `omit/include ... in` prefixes) | %s |' % f(L['declLinesAll']))
    w('| ... of unreachable declarations | %s (%s%% of declaration lines, %s%% of all lines) |' % (f(L['declLinesUnreachable']), L['pctOfDeclLines'], L['pctOfSourceLines']))
    w('| proof size (distinct subterms) of unreachable theorems | %s of %s (%s%%) |\n' % (f(A['proofSize']['unreachable']), f(A['proofSize']['all']), A['proofSize']['pct']))
    m = A['modules']
    w('### T4. Modules\n')
    w('| | modules | declarations | lines |\n|---|---:|---:|---:|')
    w('| project modules (two root files and three import hubs have no declarations) | %s | %s | %s |' % (f(m['project']), f(A['declarations']), f(L['sourceLinesAll'])))
    w('| in the import closure of the two headline modules | %s | | |' % f(m['headlineImportClosure']))
    w('| every declaration reachable | %s | | |' % f(m['fullyReachable']))
    w('| some unreachable, some reachable | %s | | |' % f(m['partly']))
    w('| ... of which at least half unreachable | %s | | |' % f(m['majorityUnreachable']))
    w('| **wholly unreachable** | **%s** | %s | %s |' % (f(m['whollyUnreachable']), f(m['whollyUnreachableDecls']), f(m['whollyUnreachableLines'])))
    wh = [r for r in M if r['decls'] and r['unreachable'] == r['decls']]
    for lab, fn in [('... imported on the way to a headline theorem, nothing in them used', lambda r: r['inHeadlineImportClosure']),
                    ('... imported only from the root files (paper-form results and their support)', lambda r: not r['inHeadlineImportClosure'] and r['inRootImportClosure']),
                    ('... imported by nothing (orphans, built only by the Lake glob)', lambda r: not r['inHeadlineImportClosure'] and not r['inRootImportClosure'])]:
        x = [r for r in wh if fn(r)]
        w('| %s | %s | %s | %s |' % (lab, f(len(x)), f(sum(r['decls'] for r in x)), f(sum(r['lines'] for r in x))))
    w('\nLargest wholly unreachable modules: ' + ', '.join('`%s` (%d decls, %d lines)' % (r['module'], r['decls'], r['lines'])
                                                           for r in sorted(wh, key=lambda r: -r['lines'])[:12]) + '.\n')
    part = sorted([r for r in M if 0 < r['unreachable'] < r['decls']], key=lambda r: -r['unreachableLines'])[:15]
    w('Partly unreachable modules with the most unreachable lines:\n')
    w('| module | declarations | unreachable | unreachable lines | file lines |\n|---|---:|---:|---:|---:|')
    for r in part:
        w('| `%s` | %d | %d | %s | %s |' % (r['module'], r['decls'], r['unreachable'], f(r['unreachableLines']), f(r['lines'])))
    w('\n### T5. Cloned modules (the 13 of REUSE.md section 1.7)\n')
    w('| clone | lines | declarations | unreachable | base module | base declarations | base unreachable | imported by anything |\n|---|---:|---:|---:|---|---:|---:|---|')
    for c in A['clones']:
        w('| `%s` | %s | %d | %d | `%s` | %d | %d | %s |' % (c['module'], f(c['lines']), c['decls'], c['unreachable'], c['base'].split('.', 1)[1],
                                                         c['baseDecls'], c['baseUnreachable'], 'headline closure' if c['importedByHeadlineClosure'] else 'no'))
    w('| **total** | %s | %d | %d | | | %d | |\n' % (f(sum(c['lines'] for c in A['clones'])), sum(c['decls'] for c in A['clones']),
                                                   sum(c['unreachable'] for c in A['clones']), sum(c['baseUnreachable'] for c in A['clones'])))
    n = A['nonTerm']
    w('### T6. Status of the unreachable declarations\n')
    w('| status | declarations | declaration lines | by kind |\n|---|---:|---:|---|')
    w('| named in the source of a reachable declaration, absent from its term (elaboration-only dependency) | %s | %s | %s |' % (f(n['elaborationOnlyDepsOfHeadlines']), f(n['e1Lines']), kd(n['elaborationOnlyByKind'])))
    w('| held back: carries an attribute, is an instance or an abbreviation, is named in a command of a kept file, or is needed by one of those | %s | %s | %s |' % (f(n['held']), f(n['heldLines']), kd(n['heldByKind'])))
    w('| **classified dead** | **%s** | **%s** | %s |' % (f(n['dead']), f(n['deadLines']), kd(n['deadByKind'])))
    w('\nWhy declarations are held back (a declaration can carry several tags; %s tagged declarations pull in the rest as dependencies):\n' % f(n['heldRoots']))
    w('| tag | unreachable declarations |\n|---|---:|')
    for k, v in n['heldRootsByTag'].items():
        w('| %s | %s |' % (k, f(v)))
    w('\n### T7. (a) / (b) / (c) by the stated rule\n')
    w('| class | rule | theorems | other declarations |\n|---|---|---:|---:|')
    rules = collections.OrderedDict()
    for r in A['abc']['byRule']:
        rules.setdefault((r['class'], r['rule']), [0, 0])[0 if r['theorem'] else 1] += r['n']
    for (c, rule), (t, nt) in rules.items():
        w('| %s | %s | %s | %s |' % (c, rule, f(t), f(nt)))
    w('\n| class | declarations | theorems | declaration lines | share of unreachable declarations |\n|---|---:|---:|---:|---:|')
    names = {'a': '(a) alternative or superseded version', 'b': '(b) support with no term use (includes 174 elaboration-only lemmas that `simp` needs and 1,048 held declarations)', 'c': '(c) variant for another setting or form'}
    for c, v in A['abc']['byClass'].items():
        w('| %s | %s | %s | %s | %s%% |' % (names[c], f(v['decls']), f(v['theorems']), f(v['lines']), pct(v['decls'], A['unreachable'])))
    hp = os.path.join(OUT, 'hand_sample.json')
    if os.path.exists(hp):
        H = json.load(open(hp))['labels']
        S = json.load(open(os.path.join(OUT, 'sample40.json')))
        cm = collections.Counter((x['rule'], H[str(x['i'])]) for x in S)
        w('\nHand-read sample of 40 (seed %d), rule against reader:\n' % SEED)
        w('| rule \\ reader | a | b | c |\n|---|---:|---:|---:|')
        for r in 'abc':
            w('| %s | %d | %d | %d |' % (r, cm[(r, 'a')], cm[(r, 'b')], cm[(r, 'c')]))
    cp = os.path.join(OUT, 'control_results.json')
    if os.path.exists(cp):
        R = json.load(open(cp))
        w('\n### T8. Negative control: 20 used declarations deleted one at a time\n')
        w('| # | declaration | kind | direct users | build target | result | first error |\n|---|---|---|---:|---|---|---|')
        for i, r in enumerate(R, 1):
            e = r['firstError']
            w('| %d | `%s` | %s | %d | `%s` | %s | %s |' % (i, r['name'].replace('_private.', '').split('.0.')[-1], r['kind'], r['users'], r['target'],
                                                       'FAILED (as it should)' if r['exit'] else '**built**', ('line %d: %s' % (e['line'], e['msg'][:70].replace('|', '/'))) if e else ''))
        w('\n%d of %d builds failed.\n' % (sum(1 for r in R if r['exit']), len(R)))
    open(os.path.join(OUT, 'tables.md'), 'w').write('\n'.join(o) + '\n')
    print('wrote', os.path.join(OUT, 'tables.md'))


def sizes(path, restore):
    C = Corpus()
    plan, dele = load_plan(path)
    if restore:
        rs = [l.strip() for l in open(restore) if l.strip() and not l.startswith('#')]
        dele = restore_closure(C, dele, [r for r in rs if r in C.by])
    texts, deleted, removed = layout(C, dele)
    proj = [m for m in C.modules if not m.startswith('ComparatorChallenges')]
    before = {'files': len(proj), 'lines': sum(len(C.src(m)) - (1 if C.src(m)[-1] == '' else 0) for m in proj),
              'declarations': len(C.by), 'theorems': sum(1 for d in C.D if d['kind'] == 'theorem')}
    after = {'files': sum(1 for t in texts.values() if t is not None),
             'lines': sum(len(t.split('\n')) - (1 if t.endswith('\n') or t == '' else 0) for t in texts.values() if t is not None),
             'declarations': len(C.by) - len(dele),
             'theorems': sum(1 for d in C.D if d['kind'] == 'theorem' and d['name'] not in dele)}
    out = {'before': before, 'after': after, 'deletedDeclarations': len(dele), 'deletedModules': len(deleted),
           'declarationLinesRemoved': removed}
    print(json.dumps(out, indent=1))
    return out


def main():
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    restore = None
    if '--restore' in a:
        i = a.index('--restore')
        restore = a[i + 1]
        del a[i:i + 2]
    if a[0] == 'analyze':
        analyze()
    elif a[0] == 'plan':
        make_plan(a[1])
    elif a[0] == 'apply':
        apply_plan(a[1], restore)
    elif a[0] == 'reset':
        reset_work()
    elif a[0] == 'build':
        r = lake_build(a[1], a[2:] or HEAD_MODULES)
        print(json.dumps({k: (v if k != 'errors' else v[:40]) for k, v in r.items()}, indent=1, ensure_ascii=False))
    elif a[0] == 'control':
        run_control()
    elif a[0] == 'control-reparse':
        control_reparse()
    elif a[0] == 'compare':
        compare_export(a[1], a[2])
    elif a[0] == 'trimgraph':
        trimgraph(a[1], restore, a[2])
    elif a[0] == 'tables':
        tables()
    elif a[0] == 'outline':
        outline_rerun(a[1], a[2])
    elif a[0] == 'sizes':
        sizes(a[1], restore)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
