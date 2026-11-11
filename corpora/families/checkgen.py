#!/usr/bin/env python3
"""Post-review checks (M9 final).  usage: checkgen.py gen | collect
gen     writes lean/Circ.lean (for every re-derived lemma: which replaced corpus originals and which new-library
        declarations its proof depends on, transitively) and lean/LibHB_<fam>.lean (each family file with
        `#count_heartbeats in` on every declaration outside its `Re` section).
collect reads build/Circ.log and build/LibHB_*.log and writes out/families/gen/circular.json and libhb.json."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); G = os.path.join(HERE, '..', '..', 'out/families/gen')
FAMS = [('F00015', 'F15'), ('F00019', 'F19'), ('F00042', 'F42'), ('F00046', 'F46'), ('F00079', 'F79'), ('F00073', 'F73'), ('F02076', 'F2076')]
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|nonrec)\s+)*(theorem|lemma|def|abbrev|instance|structure)\s+([\w.'«»]+)")
def pairs():
    out = []
    for fid, fam in FAMS:
        p = f'{HERE}/subst/{fid}.re.json'
        if os.path.exists(p): out += [(fid, n, n + '_R') for n in json.load(open(p))]
    out += [('F00042m', n, n + '_M') for n in json.load(open(f'{HERE}/subst/F00042_mathlib.re.json'))]
    return out
def libhb(fam):
    L = open(f'{HERE}/lean/{fam}.lean').read().split('\n')
    ins = {}; inre = False; incomment = False
    for i, l in enumerate(L):
        s = l.strip()
        if incomment:
            if '-/' in s: incomment = False
            continue
        if s.startswith('/-') and '-/' not in s: incomment = True; continue
        if s.startswith('namespace Re') or s.startswith('namespace Fam.F2076.Re'): inre = True
        if s.startswith('end Re') or s.startswith('end Fam.F2076.Re'): inre = False
        m = DECL.match(l)
        if not m or inre: continue
        k = i
        while k > 0 and (L[k - 1].startswith('@[') or L[k - 1].rstrip().endswith('-/') or (L[k - 1].rstrip().endswith(' in') and L[k - 1][:1] not in (' ', '\t', '#'))):
            k -= 1
            while not L[k].lstrip().startswith('/-') and not L[k].startswith('@[') and not L[k].rstrip().endswith(' in'): k -= 1
        ins[k] = m.group(2)
    out = []
    lastimp = max(i for i, l in enumerate(L) if l.startswith('import '))
    for i, l in enumerate(L):
        if i in ins:
            if out and out[-1].strip() == '#count_heartbeats in': out.pop()
            out += [f'run_cmd IO.println "LIBDECL {ins[i]}"', '#count_heartbeats in']
        out.append(l)
        if i == lastimp:
            if 'Mathlib.Util.CountHeartbeats' not in '\n'.join(L): out.append('import Mathlib.Util.CountHeartbeats')
            out.append('set_option Elab.async false')
    # the measuring block at the end is not library
    txt = '\n'.join(out)
    txt = re.sub(r'\n(open [\w.]+ in\n)?run_cmd (do\n  )?Fam\.report .*', '\n', txt, flags=re.S)
    open(f'{HERE}/lean/LibHB_{fam}.lean', 'w').write(txt)
    return len(ins)
if sys.argv[1] == 'gen':
    P = pairs()
    imps = [f'{fid}_re' for fid, fam in FAMS if os.path.exists(f'{HERE}/subst/{fid}.re.json')] + ['F00042_mathlib'] + [fam for _, fam in FAMS]
    fams = ', '.join(f'"{fam}"' for _, fam in FAMS)
    lean = '\n'.join('import ' + m for m in imps) + '''
open Lean Meta Elab Command

/-- constants reachable from `start` through types and values, following only corpus and families modules -/
partial def famClosure (env : Environment) (start : Name) : Std.HashSet Name := Id.run do
  let mut seen : Std.HashSet Name := {}
  let mut stack : Array Name := #[start]
  while h : stack.size > 0 do
    let c := stack.back
    stack := stack.pop
    if seen.contains c then continue
    seen := seen.insert c
    let some ci := env.find? c | continue
    let follow := match env.getModuleIdxFor? c with
      | some i => let m := env.header.moduleNames[i.toNat]!; (`NavierStokes).isPrefixOf m || (`Euler).isPrefixOf m || m.toString.startsWith "F"
      | none => true
    if !follow then continue
    let mut used := ci.type.getUsedConstants
    if let some v := ci.value? (allowOpaque := true) then used := used ++ v.getUsedConstants
    for u in used do
      if !seen.contains u then stack := stack.push u
  return seen

run_cmd do
  let env ← getEnv
  let famFiles : List String := [%s]
  let pairs : List (Name × Name) := [
%s]
  let origs := pairs.map (·.1)
  for (o, r) in pairs do
    unless env.contains r do IO.println s!"MISSING {r}"
    let cl := famClosure env r
    IO.println s!"PAIR {o} {r}"
    for o' in origs.eraseDups do
      if cl.contains o' then IO.println s!"DEP {r} {o'}"
    for c in cl.toList do
      match env.getModuleIdxFor? c with
      | some i =>
        let m := env.header.moduleNames[i.toNat]!
        if famFiles.contains m.toString && c != r && !c.isInternal then IO.println s!"LIB {r} {c}"
      | none => pure ()
''' % (fams, ',\n'.join(f'  (`{n}, `{r})' for _, n, r in P))
    open(f'{HERE}/lean/Circ.lean', 'w').write(lean)
    print('Circ.lean:', len(P), 'pairs;', {fam: libhb(fam) for _, fam in FAMS})
else:
    P = pairs(); fam_of = {r: fid for fid, n, r in P}; orig_of = {r: n for fid, n, r in P}
    dep = {}; lib = {}; missing = []
    for l in open(f'{HERE}/build/Circ.log'):
        p = l.split()
        if l.startswith('MISSING'): missing.append(p[1])
        if l.startswith('DEP '): dep.setdefault(p[1], []).append(p[2])
        if l.startswith('LIB '): lib.setdefault(p[1], []).append(p[2])
    # replacement graph on originals: o -> o' when the re-derivation of o depends on the corpus original o'
    edges = {orig_of[r]: set(v) for r, v in dep.items() if r.endswith('_R')}
    def reach(a):
        seen = set(); st = list(edges.get(a, []))
        while st:
            x = st.pop()
            if x in seen: continue
            seen.add(x); st += list(edges.get(x, []))
        return seen
    circ = sorted(o for o in edges if o in reach(o))
    out = dict(pairs=len(P), missing=missing, circular=circ,
               dependsOnReplacedOriginal={orig_of[r]: sorted(v) for r, v in dep.items()},
               libraryUsed={orig_of[r] + ('' if r.endswith('_R') else ' (Mathlib-only)'): sorted(v) for r, v in lib.items()})
    json.dump(out, open(f'{G}/circular.json', 'w'), indent=1, ensure_ascii=False)
    print('pairs', len(P), 'missing', missing, 'circular', circ)
    H = {}
    for fid, fam in FAMS:
        rows = []; cur = None; errs = 0
        for l in open(f'{HERE}/build/LibHB_{fam}.log'):
            m = re.match(r'LIBDECL (\S+)', l)
            if m: cur = [m.group(1), None]; rows.append(cur); continue
            if ': error' in l: errs += 1
            hb = re.search(r'Used (\d+) heartbeats', l)
            if hb and cur is not None and cur[1] is None: cur[1] = int(hb.group(1))
        used = {c for r, v in lib.items() if fam_of[r] == fid for c in v}
        def isused(short): return any(c == short or c.endswith('.' + short) for c in used)
        H[fid] = dict(file=fam, errors=errs, decls=[dict(name=n, heartbeats=h, usedByRederivations=isused(n)) for n, h in rows],
                      all=sum(h or 0 for n, h in rows), used=sum(h or 0 for n, h in rows if isused(n)), unmeasured=[n for n, h in rows if h is None],
                      usedNotMatched=sorted(c for c in used if not any(c == n or c.endswith('.' + n) for n, h in rows)))
        print(fid, 'decls', len(rows), 'all', H[fid]['all'], 'used', H[fid]['used'], 'errors', errs, 'unmeasured', H[fid]['unmeasured'], 'unmatched', H[fid]['usedNotMatched'])
    json.dump(H, open(f'{G}/libhb.json', 'w'), indent=1, ensure_ascii=False)
