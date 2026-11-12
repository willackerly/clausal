"""Reviewer's own encoding of the cases of five V4 rules (picked with random.Random(20261111).sample over the 30
compiled keys), evaluated with the reviewer's own transcription of ledger/src/lib.rs and of each compiled reading.
Written BEFORE reading the stored encodings; the comparison with them is printed after."""
import json
M = 2**64 - 1
def apply(l, t):
    l = list(l); f, to, a = t; n = len(l)
    if f >= n or to >= n or f == to: return False, l
    if l[f] < a: return False, l
    if l[to] + a > M: return False, l
    l[f] -= a; l[to] += a; return True, l
def apply_batch(l, b):
    i = 0
    for t in b:
        ok, l2 = apply(l, t)
        if not ok: break
        l = l2; i += 1
    return i, l
def apply_all(l, b):
    n, l2 = apply_batch(l, b)
    return (True, l2) if n == len(b) else (False, list(l))
def ref_whole(l, b):
    n, l2 = apply_batch(l, b)
    return (True, l2) if n == len(b) else (False, list(l))
def valid(l, t):
    f, to, a = t; n = len(l)
    return f < n and to < n and f != to and a <= l[f] and l[to] + a <= M
def lookup(l, i): return l[i] if i < len(l) else None
def bal(l, i): return l[i] if i < len(l) else 0
# readings: return 'out' (not in scope), True (claim holds), False (claim false)
def R8(l, b):      # successful apply_all agrees with ref_whole
    ok, l2 = apply_all(l, b)
    if not ok: return 'out'
    return (ok, l2) == ref_whole(l, b)
def R05(l, b):     # apply_all agrees with ref_whole (every call)
    return apply_all(l, b) == ref_whole(l, b)
def R12(l, i):     # lookup with bal(l,i)=0 never found
    if bal(l, i) != 0: return 'out'
    return lookup(l, i) is None
def R09(l, t):     # accepted exactly when valid
    ok, _ = apply(l, t); return ok == valid(l, t)
mine = {
 'sonnet-1/R8': (R8, [([10, 0], [(0,1,3),(0,1,3)], True), ([10, 0], [(0,1,5)], True), ([10, 0], [], True),
                      ([10, 0, 0], [(0,1,5),(1,2,5)], True), ([10, 0], [(0,1,4)]*3, 'out')]),
 'haiku-1/R05': (R05, [([10,0],[(0,1,4),(0,1,4)],True), ([10,0],[(0,1,4),(0,1,7)],True), ([5,5],[],True),
                      ([3,3],[(0,1,1),(1,2,1)],True), ([6,0],[(0,1,6),(1,0,6)],True)]),
 'haiku-1/R08': (R8, [([10,0],[(0,1,3),(1,0,1)],True), ([5,5],[(0,1,5),(1,0,5)],True), ([4,0,0],[(0,1,2),(1,2,2)],True),
                     ([2,8],[(1,0,3)],True), ([7,1],[(0,1,7)],True)]),
 'haiku-1/R12': (R12, [([0],0,False), ([5,0],1,False), ([5,0],2,True), ([5],0,'out'), ([3,0],1,False)]),
 'default-1/R09': (R09, [([100,50],(0,1,100),True), ([100,50],(0,1,101),True), ([100,M-50],(0,1,50),True),
                        ([100,M-50],(0,1,51),True), ([100,50],(0,2,10),True)]),
}
R = json.load(open('/Users/will/dev/lean-rosette/trials/sentences/results.json'))
byk = {r['key']: r for r in R['rules']}
for k, (f, cs) in mine.items():
    print('==', k)
    stored = byk[k]['cases']
    for n, (l, x, expect_author) in enumerate(cs):
        got = f(l, x)
        s = stored[n] if n < len(stored) else {}
        print(f'  mine: {l} {x} -> reading {got}; author expects {expect_author}; '
              f'{"agrees" if got == expect_author else "CONTRADICTS"}')
        print(f'  stored: values={s.get("values")} expect={s.get("expect")} status={s.get("status")} judgement={s.get("judgement")} code_does={s.get("code_does")}')
