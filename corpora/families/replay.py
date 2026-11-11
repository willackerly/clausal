#!/usr/bin/env python3
"""Replay corpus theorems in a scratch file, optionally with member names replaced by a primitive.

usage: replay.py OUT.lean SUFFIX IMPORTS(comma) SUBST.json NAME [NAME ...]
  SUBST.json: {"Full.Member.Name": "replacement text", ...}  ({} = verbatim replay)
Each theorem is re-elaborated in its original namespace/open/variable context (copied from the corpus
source, which is only read), renamed NAME ++ SUFFIX, under `count_heartbeats in`.  A marker line
`-- REPLAY <name> <first line> <last line>` lets `replay_log.py` attribute errors.
"""
import json, os, re, sys
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
out, suffix, imports, substf = sys.argv[1:5]
names = sys.argv[5:]
subst = json.load(open(substf)) if substf != '-' else {}
# optional: REPLAY_PROOFS=file.json {theorem name: proof term}: keep the corpus STATEMENT verbatim, replace the proof
proofs = json.load(open(os.environ['REPLAY_PROOFS'])) if os.environ.get('REPLAY_PROOFS') else {}
def cut_statement(src):
    """text up to the top-level `:=` that starts the proof"""
    depth = 0; i = 0
    while i < len(src):
        c = src[i]
        if c in '([{⟨': depth += 1
        elif c in ')]}⟩': depth -= 1
        elif src.startswith(':=', i) and depth == 0: return src[:i]
        elif src.startswith('--', i):
            j = src.find('\n', i); i = j if j >= 0 else len(src); continue
        i += 1
    return None
decl = {}
for l in open(os.path.join(REPO, 'out/corpus/ns/decls.jsonl')):
    d = json.loads(l)
    if d['name'] in names: decl[d['name']] = d
CTX = ('open ', 'universe ', 'variable ', 'variable\n', 'namespace ', 'section', 'end ', 'end\n', 'noncomputable section',
       'local ', 'include ', 'omit ', 'set_option ', 'attribute [local', 'export ', 'scoped ', 'open\n')
def chunks(lines):
    """top-level chunks before a line: a chunk starts at a column-0 code line and runs over indented lines"""
    res, cur, start, incomment = [], [], 0, False
    for i, l in enumerate(lines):
        if incomment:
            if '-/' in l: incomment = False
            continue
        if l.startswith('/-'):
            if cur: res.append((start, cur)); cur = []
            if '-/' not in l: incomment = True
            continue
        if l.strip() == '' or l.startswith('--'):
            if cur: res.append((start, cur)); cur = []
            continue
        if l[:1] in (' ', '\t'):
            if cur: cur.append(l)
            continue
        if cur: res.append((start, cur))
        cur = [l]; start = i
    if cur: res.append((start, cur))
    return res
def tokens_sub(text, subst, ownname):
    # longest qualified suffix first; a token is an identifier path
    table = {}
    for full, rep in subst.items():
        parts = full.split('.')
        for k in range(len(parts)):
            table.setdefault('.'.join(parts[k:]), rep)
    def f(m):
        tok = m.group(0)
        if tok in table: return table[tok]
        # member used as a namespace prefix:  Member.lemma  ->  Rep.lemma  (only for plain-identifier replacements)
        for k in sorted(table, key=len, reverse=True):
            if tok.startswith(k + '.') and re.fullmatch(r"[\w.']+", table[k]):
                return table[k] + tok[len(k):]
        return tok
    return re.sub(r"(?<![\w.'])[A-Za-z_][\w']*(?:\.[A-Za-z_][\w']*)*", f, text)
o = ['import Tool'] + ['import ' + m for m in imports.split(',') if m]
mods = sorted({decl[n]['module'] for n in names if n in decl})
o += ['import ' + m for m in mods] + ['import Mathlib.Util.CountHeartbeats', 'set_option Elab.async false  -- so that #count_heartbeats includes the proof', '']
body = []
for n in names:
    if n not in decl: print('MISSING', n, file=sys.stderr); continue
    d = decl[n]
    path = os.path.join(REPO, 'corpora/ns', d['module'].replace('.', '/') + '.lean')
    lines = open(path).read().split('\n')
    stack, ctx = [], []
    for start, ch in chunks(lines[:d['line'] - 1]):
        head = '\n'.join(ch)
        if head.rstrip().endswith(' in') or head.split('\n')[0].rstrip().endswith(' in'): continue
        if head.startswith(CTX) or head in ('section', 'end', 'variable'):
            first = head.split('\n')[0].split()
            if first[0] == 'namespace': stack.append(first[1])
            elif head.startswith('noncomputable section'): stack.append(first[2] if len(first) > 2 else '')
            elif first[0] == 'section': stack.append(first[1] if len(first) > 1 else '')
            elif first[0] == 'end':
                if stack: stack.pop()
            ctx.append(head)
    target = lines[d['line'] - 1:d['endLine']]
    src = '\n'.join(target)
    # drop doc comment and attributes, rename
    src = re.sub(r'^/--.*?-/\s*', '', src, flags=re.S)
    src = re.sub(r'^(@\[[^\]]*\]\s*)+', '', src)
    m = re.match(r"((?:private |protected |noncomputable |nonrec )*)(theorem|lemma)\s+([\w.'«»]+)", src)
    if not m: print('UNPARSED', n, file=sys.stderr); continue
    own = m.group(3)
    rest = src[m.end():]
    if subst: rest = tokens_sub(rest, subst, own)
    if n in proofs:
        st = cut_statement(rest)
        if st is None: print('NOCUT', n, file=sys.stderr); continue
        rest = st + ':=\n  ' + proofs[n]
    src = f"{m.group(1).replace('private ', '')}theorem {own}{suffix}" + rest
    prev = lines[d['line'] - 2].strip() if d['line'] >= 2 else ''
    # a doc comment may sit between `omit … in` and the theorem
    k = d['line'] - 2
    while k >= 0 and not (lines[k].startswith('omit ') or lines[k].startswith('theorem') or lines[k].strip() == '' or lines[k].startswith('end') or lines[k].startswith('variable')): k -= 1
    omit = [lines[k].strip()] if k >= 0 and lines[k].startswith('omit ') and lines[k].rstrip().endswith(' in') else []
    blk = ['section', 'set_option linter.all false'] + ctx + omit + ['#count_heartbeats in', src]
    for s in reversed(stack): blk.append('end ' + s if s else 'end')
    blk.append('end')
    body.append((n, d, own, '\n'.join(blk)))
text = '\n'.join(o) + '\n'
for n, d, own, blk in body:
    a = text.count('\n') + 2
    b = a + blk.count('\n')
    text += f"-- REPLAY {n} {a} {b}\nrun_cmd IO.println \"BLOCK {n}\"\n" + blk + '\n\n'
if os.environ.get('REPLAY_FAM'):
    text += 'run_cmd Fam.reportPairs "%s" "re" [%s]\n' % (os.environ['REPLAY_FAM'], ', '.join(f'(`{n}, `{n}{suffix})' for n, d, own, blk in body))
open(out, 'w').write(text)
print(f"wrote {out}: {len(body)} theorems")
