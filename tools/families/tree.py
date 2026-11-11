"""Typed trees exported by Export.lean: parsing, shape keys at each looseness level,
n-ary anti-unification (least general generalisation), and a pseudo-Lean printer.

Tree nodes (tuples):
  ('A', tag, head, *args)   head: str (constant, '$i', '#k') or a node
  ('C', tag, name) ('V', tag, i) ('B', tag, k) ('N', tag, n) ('S',) ('U',)
  ('L', T, B) ('Q', bi, T, B) ('I', A, B) ('K', *conj)       '*' erased
  ('?', id)                 hole (only in generalisations)
"""
import re
import hashlib

TOK = re.compile(r'\(|\)|[^\s()]+')


def parse(s):
    stack = [[]]
    for t in TOK.findall(s):
        if t == '(':
            stack.append([])
        elif t == ')':
            x = tuple(stack.pop())
            stack[-1].append(x)
        else:
            stack[-1].append(t)
    return stack[0][0]


def size(t):
    """number of nodes, erased arguments not counted"""
    if isinstance(t, str):
        return 0
    k = t[0]
    if k == 'A':
        return 1 + (size(t[2]) if not isinstance(t[2], str) else 0) + sum(size(a) for a in t[3:])
    if k in ('C', 'V', 'B', 'N', 'S', 'U', '?', 'BIG'):
        return 1
    if k == 'Q':
        return 1 + size(t[2]) + size(t[3])
    return 1 + sum(size(a) for a in t[1:])


def renumber_params(t, order=None):
    """parameters numbered by first occurrence (so two bodies that use their parameters in the same
    pattern agree whatever the telescope positions are).  Returns (tree, order) with order[new] = old."""
    if order is None:
        order = []
    idx = {o: i for i, o in enumerate(order)}

    def get(old):
        if old not in idx:
            idx[old] = len(order)
            order.append(old)
        return idx[old]

    def go(t):
        if isinstance(t, str):
            return t
        k = t[0]
        if k == 'V':
            return ('V', t[1], str(get(int(t[2]))))
        if k == 'A':
            h = t[2]
            if isinstance(h, str):
                if h.startswith('$'):
                    h = '$' + str(get(int(h[1:])))
            else:
                h = go(h)
            return ('A', t[1], h) + tuple(go(a) for a in t[3:])
        if k == 'Q':
            return ('Q', t[1], go(t[2]), go(t[3]))
        if k in ('L', 'I', 'K'):
            return (k,) + tuple(go(a) for a in t[1:])
        return t

    return go(t), order


def consts(t, out=None, heads_only=False):
    """constant names occurring (heads and leaves)"""
    if out is None:
        out = set()
    if isinstance(t, str):
        return out
    k = t[0]
    if k == 'A':
        h = t[2]
        if isinstance(h, str):
            if not (h.startswith('$') or h.startswith('#') or h == '*'):
                out.add(h)
        else:
            consts(h, out)
        for a in t[3:]:
            consts(a, out)
    elif k == 'C':
        out.add(t[2])
    elif k == 'Q':
        consts(t[2], out)
        consts(t[3], out)
    elif k in ('L', 'I', 'K', 'SIG', 'P'):
        for a in t[1:]:
            consts(a, out)
    return out


class Renderer:
    """Shape key at a looseness level.
       0  exact up to bound names and binder kinds
       1  + numeric literals abstracted (their type kept)
       2  + constants standing as arguments become typed holes
       3  + project constants in head position become holes, project type names in tags erased
    cmap: optional function name -> replacement (used for API profiles: the definition itself -> hole,
    other project constants -> numbered holes)."""

    def __init__(self, lvl, isproj=None, cmap=None):
        self.lvl = lvl
        self.isproj = isproj
        self.cmap = cmap

    def tag(self, tg):
        if self.cmap is not None:
            if tg.startswith('F>'):
                return 'F>' + self.cmap(tg[2:])
            return self.cmap(tg)
        if self.lvl >= 3 and self.isproj is not None:
            base = tg[2:] if tg.startswith('F>') else tg
            if self.isproj(base):
                return 'F>?P' if tg.startswith('F>') else '?P'
        return tg

    def r(self, t):
        if isinstance(t, str):
            return t
        k = t[0]
        if k == 'A':
            h = t[2]
            if isinstance(h, str):
                if h[0] not in '$#*':
                    if self.cmap is not None:
                        h = self.cmap(h)
                    elif self.lvl >= 3 and self.isproj(h):
                        h = '?P'
            else:
                h = self.r(h)
            return '(A ' + self.tag(t[1]) + ' ' + h + ''.join(' ' + self.r(a) for a in t[3:]) + ')'
        if k == 'C':
            if self.cmap is not None:
                nm = self.cmap(t[2])
                if self.lvl >= 2 and not nm.startswith('◊'):
                    return '(H ' + self.tag(t[1]) + ')'
                return '(C ' + self.tag(t[1]) + ' ' + nm + ')'
            if self.lvl >= 2:
                return '(H ' + self.tag(t[1]) + ')'
            return '(C ' + t[1] + ' ' + t[2] + ')'
        if k == 'N':
            if self.lvl >= 1:
                return '(N ' + self.tag(t[1]) + ')'
            return '(N ' + t[1] + ' ' + t[2] + ')'
        if k in ('V', 'B'):
            return '(' + k + ' ' + self.tag(t[1]) + ' ' + t[2] + ')'
        if k == 'Q':
            return '(Q ' + self.r(t[2]) + ' ' + self.r(t[3]) + ')'
        if k == 'P':  # signature parameter: kind, type
            return '(P ' + t[1] + ' ' + self.r(t[2]) + ')'
        if k in ('L', 'I', 'K', 'SIG'):
            return '(' + k + ''.join(' ' + self.r(a) for a in t[1:]) + ')'
        return '(' + k + ')'


def h64(s):
    return hashlib.blake2b(s.encode(), digest_size=8).hexdigest()


# ---------------------------------------------------------------- anti-unification

def _shape(t):
    """what must agree for two nodes to be generalised node-by-node"""
    if isinstance(t, str):
        return ('*',)
    k = t[0]
    if k == 'A':
        return ('A', len(t))
    if k in ('C', 'V', 'B', 'N'):
        return (k, t[2])
    if k == 'K':
        return ('K', len(t))
    return (k,)


def lgg(trees, holes=None, head_holes=True):
    """Least general generalisation of a list of trees (first-order, plus a hole in head position when
    the heads differ but the argument counts agree).  `holes` maps a tuple of fillers (one per tree) to a
    hole id, so the same variation at two positions is ONE hole.  Tags are not compared (a hole in a
    sub-term may change the tag of its parents); a tag that differs is written '_'."""
    if holes is None:
        holes = {}

    def hole(ts):
        key = tuple(ts)
        if key not in holes:
            holes[key] = len(holes)
        return ('?', holes[key])

    def go(ts):
        t0 = ts[0]
        if all(t == t0 for t in ts[1:]):
            return t0
        sh = _shape(t0)
        if any(_shape(t) != sh for t in ts[1:]):
            # numerals of different value / constants of different name: a leaf hole
            return hole(ts)
        k = t0[0]
        if k == 'A':
            heads = [t[2] for t in ts]
            tg = t0[1] if all(t[1] == t0[1] for t in ts) else '_'
            if all(h == heads[0] for h in heads):
                h = heads[0]
            elif all(not isinstance(h, str) for h in heads):
                h = go(heads)
            elif head_holes and all(isinstance(h, str) for h in heads):
                h = hole([('HEAD', x) for x in heads])
            else:
                return hole(ts)
            return ('A', tg, h) + tuple(go([t[i] for t in ts]) for i in range(3, len(t0)))
        if k == 'Q':
            return ('Q', 'd', go([t[2] for t in ts]), go([t[3] for t in ts]))
        if k in ('L', 'I', 'K'):
            return (k,) + tuple(go([t[i] for t in ts]) for i in range(1, len(t0)))
        if k in ('C', 'V', 'B', 'N'):  # same name / index, tag differs
            return (k, '_', t0[2])
        return t0

    return go(list(trees)), holes


def pair_stats(a, b):
    """(shared skeleton nodes, number of distinct holes) of lgg(a, b)"""
    g, holes = lgg([a, b])
    return skel_size(g), len(holes)


def skel_size(g):
    """non-hole nodes of a generalisation"""
    if isinstance(g, str):
        return 0
    k = g[0]
    if k == '?':
        return 0
    if k == 'A':
        h = g[2]
        own = 1 if isinstance(h, str) else (0 if h[0] == '?' else skel_size(h) + 1)
        return own + sum(skel_size(a) for a in g[3:])
    if k in ('C', 'V', 'B', 'N', 'S', 'U', 'BIG'):
        return 1
    if k == 'Q':
        return 1 + skel_size(g[2]) + skel_size(g[3])
    return 1 + sum(skel_size(a) for a in g[1:])


def is_leaf_filler(f):
    return isinstance(f, str) or f[0] in ('C', 'V', 'B', 'N', 'S', 'U', 'HEAD')


def lost_mass(holes, j):
    """nodes of member j that sit inside COMPOUND holes (a hole whose fillers are all leaves or heads
    costs nothing: that is the variation levels 1-3 already allow)"""
    tot = 0
    for fill in holes:
        if all(is_leaf_filler(f) for f in fill):
            continue
        tot += size(fill[j]) if not is_leaf_filler(fill[j]) else 1
    return tot


def free_bvars(t, depth=0):
    """does the sub-term mention a variable bound outside it? (then a hole here must be a function of it)"""
    if isinstance(t, str):
        return False
    k = t[0]
    if k == 'B':
        return int(t[2]) >= depth
    if k == 'A':
        h = t[2]
        if isinstance(h, str):
            if h.startswith('#') and int(h[1:]) >= depth:
                return True
        elif free_bvars(h, depth):
            return True
        return any(free_bvars(a, depth) for a in t[3:])
    if k == 'L':
        return free_bvars(t[1], depth) or free_bvars(t[2], depth + 1)
    if k == 'Q':
        return free_bvars(t[2], depth) or free_bvars(t[3], depth + 1)
    if k in ('I', 'K'):
        return any(free_bvars(a, depth) for a in t[1:])
    return False


def filler_kind(f):
    """kind of one filler: numeral, constant, type, set, function, head, term"""
    if isinstance(f, str):
        return 'erased'
    k = f[0]
    if k == 'HEAD':
        return 'head'
    if k == 'N':
        return 'numeral'
    if k == 'U':
        return 'type'
    if k in ('I', 'K', 'Q'):
        return 'prop' if k != 'Q' else 'prop-or-type'
    if k == 'L':
        return 'function'
    if k == 'S':
        return 'string'
    tag = f[1] if len(f) > 1 and isinstance(f[1], str) else ''
    if k == 'V':
        return 'parameter'
    if k == 'B':
        return 'boundvar'
    if tag == 'U':
        return 'type'
    if tag == 'Prop':
        return 'prop'
    if tag == 'Set' or tag == 'Finset':
        return 'set'
    if tag.startswith('F>'):
        return 'function'
    if k == 'C':
        return 'constant'
    return 'term'


# ---------------------------------------------------------------- pseudo-Lean printer

INFIX = {'LE.le': '≤', 'LT.lt': '<', 'HMul.hMul': '*', 'HAdd.hAdd': '+', 'HSub.hSub': '-', 'HDiv.hDiv': '/',
         'HPow.hPow': '^', 'Eq': '=', 'HSMul.hSMul': '•', 'Iff': '↔', 'Or': '∨', 'HasSubset.Subset': '⊆',
         'Inter.inter': '∩', 'Union.union': '∪', 'Function.comp': '∘', 'SDiff.sdiff': '\\', 'Dvd.dvd': '∣',
         'Max.max': '⊔', 'Min.min': '⊓', 'HEq': '≍', 'HMod.hMod': '%', 'Monoid.npow': '^'}


def short(n):
    p = n.split('.')
    return '.'.join(p[-2:]) if len(p) > 2 else n


def pretty(t, pnames=None, hole_names=None, limit=1200):
    """readable rendering; bound variables are x0, x1, .. by binding depth; parameters by name when known
    (else p0, p1, ..); holes ⟨h1⟩; erased arguments dropped"""
    def pn(i):
        i = int(i)
        if pnames is not None and i < len(pnames):
            return pnames[i]
        return f'p{i}'

    def hn(i):
        return hole_names[i] if hole_names and i in hole_names else f'⟨h{i + 1}⟩'

    def go(t, d, top=False):
        if isinstance(t, str):
            return '_'
        k = t[0]
        if k == '?':
            return hn(t[1])
        if k == 'HEAD':
            return short(t[1])
        if k == 'C':
            return short(t[2])
        if k == 'V':
            return pn(t[2])
        if k == 'B':
            lv = d - 1 - int(t[2])
            return f'x{lv}' if lv >= 0 else f'⟨bound↑{-lv}⟩'
        if k == 'N':
            return t[2] if len(t) > 2 else 'N'
        if k == 'S':
            return '"…"'
        if k == 'U':
            return 'Sort'
        if k == 'BIG':
            return '…'
        if k == 'L':
            return f'(fun x{d} : {go(t[1], d)} ↦ {go(t[2], d + 1)})'
        if k == 'Q':
            return f'(∀ x{d} : {go(t[2], d)}, {go(t[3], d + 1)})'
        if k == 'I':
            return f'({go(t[1], d)} → {go(t[2], d)})'
        if k == 'K':
            return '(' + ' ∧ '.join(go(a, d) for a in t[1:]) + ')'
        if k == 'A':
            h = t[2]
            args = [a for a in t[3:] if a != '*']
            if isinstance(h, str):
                if h.startswith('$'):
                    hs = pn(h[1:])
                elif h.startswith('#'):
                    lv = d - 1 - int(h[1:])
                    hs = f'x{lv}' if lv >= 0 else f'⟨bound↑{-lv}⟩'
                else:
                    if h in INFIX and len(args) == 2:
                        return f'({go(args[0], d)} {INFIX[h]} {go(args[1], d)})'
                    if h == 'Membership.mem' and len(args) == 2:
                        return f'({go(args[1], d)} ∈ {go(args[0], d)})'
                    if h == 'Exists' and len(args) == 1 and not isinstance(args[0], str) and args[0][0] == 'L':
                        l = args[0]
                        return f'(∃ x{d} : {go(l[1], d)}, {go(l[2], d + 1)})'
                    if h == 'Norm.norm' and len(args) == 1:
                        return f'‖{go(args[0], d)}‖'
                    if h == 'abs' and len(args) == 1:
                        return f'|{go(args[0], d)}|'
                    if h == 'Not' and len(args) == 1:
                        return f'¬{go(args[0], d)}'
                    if h == 'Neg.neg' and len(args) == 1:
                        return f'-{go(args[0], d)}'
                    hs = short(h)
            elif h[0] == '?':
                hs = hn(h[1])
            else:
                hs = go(h, d)
            if not args:
                return hs
            return '(' + hs + ' ' + ' '.join(go(a, d) for a in args) + ')'
        return '(' + str(k) + ')'

    s = go(t, 0, True)
    if s.startswith('(') and s.endswith(')'):
        # strip one outer pair when it is balanced
        depth = 0
        ok = True
        for i, ch in enumerate(s):
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0 and i != len(s) - 1:
                    ok = False
                    break
        if ok:
            s = s[1:-1]
    if len(s) > limit:
        s = s[:limit] + ' …'
    return s


# ---------------------------------------------------------------- lemma roles

def role(st, d, isproj):
    """A coarse, name-free description of what a theorem says about definition `d`:
       (number of hypotheses that mention d, capped at 3;
        head of the conclusion: ◊ if it is d itself, P for another project constant, else the library head;
        if the conclusion is d applied to arguments: the library operations inside those arguments
        (a closure law under those operations); otherwise the library heads on the way from the
        conclusion's root to the first occurrence of d, then the operations inside d's arguments)."""
    pre = d + '.'

    def is_d(n):
        return n == d or n.startswith(pre)

    def mentions(t):
        return any(is_d(c) for c in consts(t))

    def lab(h):
        if h[0] in '$#*':
            return 'v'
        if is_d(h):
            return '◊'
        if isproj(h):
            return 'P'
        return h

    def ops(t, depth, out):
        if isinstance(t, str) or depth > 4:
            return
        k = t[0]
        if k == 'A':
            h = t[2]
            if isinstance(h, str):
                l = lab(h)
                if l not in ('v', '◊', 'P'):
                    out.add(l)
            else:
                ops(h, depth + 1, out)
            for a in t[3:]:
                ops(a, depth + 1, out)
        elif k == 'Q':
            ops(t[2], depth + 1, out); ops(t[3], depth + 1, out)
        elif k in ('L', 'I', 'K'):
            for a in t[1:]:
                ops(a, depth + 1, out)

    def path(t, acc):
        """heads from the root to the first occurrence of d; returns the d-application or None"""
        if isinstance(t, str):
            return None
        k = t[0]
        if k == 'C':
            return t if is_d(t[2]) else None
        if k == 'A':
            h = t[2]
            if isinstance(h, str):
                l = lab(h)
                if l == '◊':
                    return t
                acc.append(l)
            else:
                r = path(h, acc)
                if r is not None:
                    return r
            n = len(acc)
            for a in t[3:]:
                r = path(a, acc)
                if r is not None:
                    return r
                del acc[n:]
            if isinstance(h, str):
                acc.pop()
            return None
        kids = (t[2], t[3]) if k == 'Q' else t[1:] if k in ('L', 'I', 'K') else ()
        if not kids:
            return None
        acc.append(k)
        n = len(acc)
        for a in kids:
            r = path(a, acc)
            if r is not None:
                return r
            del acc[n:]
        acc.pop()
        return None

    t = st
    nh = 0
    while not isinstance(t, str):
        if t[0] == 'Q':
            if mentions(t[2]):
                nh += 1
            t = t[3]
        elif t[0] == 'I':
            if mentions(t[1]):
                nh += 1
            t = t[2]
        else:
            break
    nh = min(nh, 3)
    acc = []
    hit = path(t, acc)
    o = set()
    if hit is not None and hit[0] == 'A':
        for a in hit[3:]:
            ops(a, 0, o)
    o = sorted(o)[:6]
    if hit is None:
        head = lab(t[2]) if (not isinstance(t, str) and t[0] == 'A' and isinstance(t[2], str)) else (t[0] if not isinstance(t, str) else '*')
        return f'{nh}|uses>{head}|'
    if not acc:
        return f'{nh}|◊|' + ','.join(o)
    return f'{nh}|' + '>'.join(acc[:5]) + '>◊|' + ','.join(o)
