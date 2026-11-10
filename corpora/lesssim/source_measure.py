#!/usr/bin/env python3
"""Source-text measures for original and native family theorems, the library and the equivalence file.
Statement = lines up to and including the first line whose code ends in ':=' or ':= by'; proof = the rest
(up to the next blank line).  Docstrings and comment-only lines are not counted.  Tokens are
whitespace-separated."""
import json, re, sys
REPO = sys.argv[1]
fam = json.load(open(REPO + '/out/corpus/lesssim/family.json'))

def split(lines):
    lines = [l for l in lines if l.strip() and not l.strip().startswith('--')]
    k = next(i for i, l in enumerate(lines) if re.search(r':=\s*(by)?\s*$', l))
    st, pr = lines[:k + 1], lines[k + 1:]
    # a ':= by' or ':=' tail belongs to the statement line; tokens after ':=' on that line go to the proof
    head, _, tail = st[-1].rpartition(':=')
    stoks = sum(len(l.split()) for l in st[:-1]) + len(head.split())
    ptoks = sum(len(l.split()) for l in pr) + len(tail.split())
    return {'stmtLines': len(st), 'proofLines': len(pr), 'stmtTokens': stoks, 'proofTokens': ptoks,
            'stmtChars': sum(len(l.strip()) for l in st), 'proofChars': sum(len(l.strip()) for l in pr)}

def block(lines, start):
    """lines of the declaration starting at index start (0-based), to the next blank line"""
    out = []
    for l in lines[start:]:
        if not l.strip(): break
        out.append(l)
    return out

def decls(path):
    L = open(path).read().split('\n')
    res = []
    i = 0
    while i < len(L):
        m = re.match(r'(?:private )?theorem (\S+)', L[i])
        if m:
            b = block(L, i)
            res.append((m.group(1), split(b)))
            i += len(b)
        else:
            i += 1
    return res

nat = dict(decls(REPO + '/corpora/lesssim/lean/Native.lean'))
lib = dict(decls(REPO + '/corpora/lesssim/lean/Lib.lean'))
eqv_l = decls(REPO + '/corpora/lesssim/lean/Equiv.lean')
eqv = {f'{i}:{n}': v for i, (n, v) in enumerate(eqv_l)}
# the sample: the first occurrence of each name in Sample.lean is the native restatement
smp_l = decls(REPO + '/corpora/lesssim/lean/Sample.lean') + decls(REPO + '/corpora/lesssim/lean/SampleS8.lean')
smp = {}
for n, v in smp_l: smp.setdefault(n, v)
sample = json.load(open(REPO + '/out/corpus/lesssim/sample.json'))['sample']
srows = []
for f in sample:
    src = open(REPO + '/corpora/ns/' + f['module'].replace('.', '/') + '.lean').read().split('\n')
    short = f['name'].split('.')[-1]
    srows.append({'name': f['name'], 'orig': split(src[f['line'] - 1:f['endLine']]), 'native': smp.get(short)})
rows = []
for f in fam:
    src = open(REPO + '/corpora/ns/' + f['module'].replace('.', '/') + '.lean').read().split('\n')
    o = split(src[f['line'] - 1:f['endLine']])
    short = f['name'].split('.', 2)[2]
    n = nat[short]
    rows.append({'name': f['name'], 'short': short, 'depth': f['depth'], 'orig': o, 'native': n})
json.dump({'family': rows, 'lib': lib, 'equiv': eqv, 'sample': srows}, open(REPO + '/out/corpus/lesssim/source_measure.json', 'w'), indent=1)
tot = lambda k, g: sum(r[g][k] for r in rows)
for r in sorted(rows, key=lambda r: r['depth']):
    print(r['depth'], r['short'][:50].ljust(50), r['orig']['stmtLines'], r['native']['stmtLines'], '|', r['orig']['proofLines'], r['native']['proofLines'], '|', r['orig']['proofTokens'], r['native']['proofTokens'])
for k in ['stmtLines', 'proofLines', 'stmtTokens', 'proofTokens', 'stmtChars', 'proofChars']:
    print(k, tot(k, 'orig'), tot(k, 'native'))
for k in ['stmtLines', 'proofLines', 'stmtTokens', 'proofTokens']:
    print('lib', k, sum(v[k] for v in lib.values()), 'equiv', k, sum(v[k] for v in eqv.values()))
print(len(lib), len(eqv))

for r in srows:
    print(r['name'].split('.')[-1][:45].ljust(45), r['orig']['stmtLines'], r['orig']['proofLines'], r['orig']['proofTokens'], '->', r['native'] and (r['native']['stmtLines'], r['native']['proofLines'], r['native']['proofTokens']))
