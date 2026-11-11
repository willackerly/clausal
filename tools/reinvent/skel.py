"""Skeleton terms exported by Export.lean: parser, matcher (second-order pattern matching with three
stated relaxations), signatures for indexing, and a printer back to Lean source.

Trees: atoms are strings ('$3' pattern variable, '§3' rigid parameter of the subject, '#1' bound variable,
'%5' literal, '*' erased, '@2' abstraction slot inside a binding, otherwise a constant name);
compound nodes are tuples (tag, ...): ('p'|'a', head, args...), ('\\', dom, body), ('!', dom, body),
('>', a, b), ('&', c1, c2, ...).
"""
import itertools
import re
import sys

sys.setrecursionlimit(10000)

TOK = re.compile(r'\(|\)|[^\s()]+')


def parse(s):
    toks = TOK.findall(s)
    pos = 0

    def rd():
        nonlocal pos
        t = toks[pos]
        pos += 1
        if t == '(':
            out = []
            while toks[pos] != ')':
                out.append(rd())
            pos += 1
            return tuple(out)
        return t
    t = rd()
    return t


def rigidify(t):
    """Subject side: its own parameters become rigid atoms."""
    if isinstance(t, str):
        return '§' + t[1:] if t[0] == '$' else t
    return tuple(rigidify(x) for x in t)


def is_var(t):
    return isinstance(t, str) and t[0] == '$'


def is_bv(t):
    return isinstance(t, str) and t[0] == '#'


def is_const(t):
    return isinstance(t, str) and t[0] not in '$§#%*@' and t != '?bad'


def consts(t, acc=None):
    if acc is None:
        acc = set()
    if isinstance(t, str):
        if is_const(t):
            acc.add(t)
    else:
        for x in t[1:]:
            consts(x, acc)
    return acc


def weight(t):
    """Rigid content of a pattern: constants, literals and binders (pattern variables count 0)."""
    if isinstance(t, str):
        return 1 if (is_const(t) or t[0] == '%') else 0
    tag = t[0]
    if tag in ('p', 'a'):
        return sum(weight(x) for x in t[1:])
    if tag in ('\\', '!'):
        return 1 + weight(t[2])
    if tag == '>':
        return 1 + weight(t[1]) + weight(t[2])
    return sum(weight(x) for x in t[1:])


def size(t):
    if isinstance(t, str):
        return 1
    return 1 + sum(size(x) for x in t[1:])


def is_prop(t):
    return isinstance(t, tuple) and t[0] in ('p', '&', '>')


# ---------------------------------------------------------------- shifting / substitution

def shift(t, k, cut=0):
    """Add k to loose bound variables >= cut."""
    if k == 0:
        return t
    if isinstance(t, str):
        if t[0] == '#':
            i = int(t[1:])
            return '#%d' % (i + k) if i >= cut else t
        return t
    tag = t[0]
    if tag in ('\\', '!'):
        return (tag, shift(t[1], k, cut), shift(t[2], k, cut + 1))
    return (tag,) + tuple(shift(x, k, cut) for x in t[1:])


def mk_app(tag, head, args):
    """Application with beta / app-merge."""
    if not args:
        return head
    if isinstance(head, tuple) and head[0] == '\\':
        body = subst_bv0(head[2], args[0])
        return mk_app(tag, body, args[1:])
    if isinstance(head, tuple) and head[0] in ('p', 'a'):
        return (tag, head[1]) + tuple(head[2:]) + tuple(args)
    return (tag, head) + tuple(args)


def subst_bv0(body, arg, depth=0):
    """body[#0 := arg] (body is under one binder being removed)."""
    if isinstance(body, str):
        if body[0] == '#':
            i = int(body[1:])
            if i == depth:
                return shift(arg, depth)
            if i > depth:
                return '#%d' % (i - 1)
        return body
    tag = body[0]
    if tag in ('\\', '!'):
        return (tag, subst_bv0(body[1], arg, depth), subst_bv0(body[2], arg, depth + 1))
    if tag in ('p', 'a'):
        h = subst_bv0(body[1], arg, depth)
        args = tuple(subst_bv0(x, arg, depth) for x in body[2:])
        if isinstance(h, tuple) and (h[0] == '\\' or (h[0] in ('p', 'a') and isinstance(body[1], str))):
            return mk_app(tag, h, args)
        return (tag, h) + args
    return (tag,) + tuple(subst_bv0(x, arg, depth) for x in body[1:])


def fill_slots(body, args, depth=0):
    """Instantiate '@k' slots of a binding body with args (given at depth 0)."""
    if isinstance(body, str):
        if body[0] == '@':
            return shift(args[int(body[1:])], depth)
        return body
    tag = body[0]
    if tag in ('\\', '!'):
        return (tag, fill_slots(body[1], args, depth), fill_slots(body[2], args, depth + 1))
    if tag in ('p', 'a'):
        h = fill_slots(body[1], args, depth)
        rest = tuple(fill_slots(x, args, depth) for x in body[2:])
        if isinstance(h, tuple) and isinstance(body[1], str) and body[1][0] == '@':
            return mk_app(tag, h, rest)
        return (tag, h) + rest
    return (tag,) + tuple(fill_slots(x, args, depth) for x in body[1:])


def abstract(s, d, argidx):
    """Abstract the local bound variables `argidx` (de Bruijn indices at depth d) out of s.
    Returns the binding body with '@k' slots, or None if s mentions another local variable."""
    pos = {a: k for k, a in enumerate(argidx)}

    def go(t, j):
        if isinstance(t, str):
            if t[0] == '#':
                m = int(t[1:])
                if m >= j:
                    loc = m - j
                    if loc in pos:
                        return '@%d' % pos[loc]
                    if loc < d:
                        raise KeyError
                return t
            return t
        tag = t[0]
        if tag in ('\\', '!'):
            return (tag, go(t[1], j), go(t[2], j + 1))
        return (tag,) + tuple(go(x, j) for x in t[1:])
    try:
        return go(s, 0)
    except KeyError:
        return None


def apply_binding(b, args):
    """b = (arity, body); args given at the current depth."""
    n, body = b
    if len(args) < n:
        return None
    t = fill_slots(body, args[:n]) if n else body
    if len(args) > n:
        t = mk_app('a', t, tuple(args[n:]))
    return t


def instantiate(p, bind):
    """Instantiate a pattern with bindings; None if some variable is unbound."""
    if isinstance(p, str):
        if p[0] == '$':
            b = bind.get(p)
            if b is None:
                return None
            if b[0] == 0:
                return b[1]
            # eta-expand
            n, body = b
            t = fill_slots(body, ['#%d' % (n - 1 - k) for k in range(n)])
            for _ in range(n):
                t = ('\\', '*', t)
            return t
        return p
    tag = p[0]
    if tag in ('p', 'a'):
        args = []
        for x in p[2:]:
            y = instantiate(x, bind)
            if y is None:
                return None
            args.append(y)
        if is_var(p[1]):
            b = bind.get(p[1])
            if b is None:
                return None
            t = apply_binding(b, args)
            if t is None:
                return None
            if isinstance(t, tuple) and t[0] in ('p', 'a'):
                t = (tag,) + t[1:]
            return t
        h = instantiate(p[1], bind)
        if h is None:
            return None
        return (tag, h) + tuple(args)
    out = []
    for x in p[1:]:
        y = instantiate(x, bind)
        if y is None:
            return None
        out.append(y)
    return (tag,) + tuple(out)


def eq_mod(a, b):
    """Equality up to erased slots, binder domains and the p/a tag."""
    if a == b:
        return True
    if a == '*' or b == '*':
        return True
    if isinstance(a, str) or isinstance(b, str):
        return False
    if a[0] in ('p', 'a') and b[0] in ('p', 'a'):
        return len(a) == len(b) and all(eq_mod(x, y) for x, y in zip(a[1:], b[1:]))
    if a[0] != b[0] or len(a) != len(b):
        return False
    if a[0] in ('\\', '!'):
        return eq_mod(a[2], b[2])
    return all(eq_mod(x, y) for x, y in zip(a[1:], b[1:]))


# ---------------------------------------------------------------- matcher

class State:
    __slots__ = ('bind', 'extras', 'absorbed', 'post')

    def __init__(self, bind=None, extras=(), absorbed=(), post=()):
        self.bind = bind or {}
        self.extras = extras
        self.absorbed = absorbed
        self.post = post

    def with_bind(self, v, b):
        nb = dict(self.bind)
        nb[v] = b
        return State(nb, self.extras, self.absorbed, self.post)


def bind_var(st, v, b):
    old = st.bind.get(v)
    if old is None:
        return st.with_bind(v, b)
    n = max(old[0], b[0])
    slots = ['@%d' % k for k in range(n)]
    x = apply_binding(old, slots) if old[0] or n else old[1]
    y = apply_binding(b, slots) if b[0] or n else b[1]
    if x is None or y is None:
        return None
    return st if eq_mod(x, y) else None


# relaxation 2 is limited to operations whose side condition `0 <= t` can hold
ABSORBABLE = ('Norm.norm', 'abs')


class Budget(Exception):
    pass


STEPS = [0]
MAXSTEPS = 20000


def match(p, s, d, st, ctx, relax):
    """Yield states in which pattern p matches subject s at binder depth d.
    ctx: tuple of subject binder domains (for side conditions).  relax: allow the two approximate rules."""
    STEPS[0] += 1
    if STEPS[0] > MAXSTEPS:
        raise Budget()
    if p == '*' or s == '*':
        yield st
        return
    if isinstance(p, str):
        if p[0] == '$':
            b = abstract(s, d, ())
            if b is None:
                return
            st2 = bind_var(st, p, (0, b))
            if st2 is not None:
                yield st2
            return
        if p == s:
            yield st
        return
    tag = p[0]
    if tag in ('p', 'a'):
        head = p[1]
        if is_var(head):
            args = p[2:]
            if all(is_bv(a) and int(a[1:]) < d for a in args) and len(set(args)) == len(args):
                if tag == 'p' and not (is_prop(s) or (isinstance(s, tuple) and s[0] == '!')):
                    return
                if tag == 'a' and is_prop(s):
                    return
                b = abstract(s, d, [int(a[1:]) for a in args])
                if b is None:
                    return
                st2 = bind_var(st, head, (len(args), b))
                if st2 is not None:
                    yield st2
                return
            # not a Miller pattern: postpone
            yield State(st.bind, st.extras, st.absorbed, st.post + ((p, s, d),))
            return
        if tag == 'p' and isinstance(s, tuple) and s[0] == '&':
            # relaxation 1: the subject carries extra conjuncts
            for i, c in enumerate(s[1:]):
                for st2 in match(p, c, d, st, ctx, relax):
                    rest = tuple(x for j, x in enumerate(s[1:]) if j != i)
                    yield State(st2.bind, st2.extras + tuple((ctx, r) for r in rest), st2.absorbed, st2.post)
            return
        ok = False
        if isinstance(s, tuple) and s[0] in ('p', 'a') and len(s) == len(p) and \
                (s[1] == head or (isinstance(head, tuple) and isinstance(s[1], tuple))):
            def args_iter(i, st1):
                if i == len(p):
                    yield st1
                    return
                for st2 in match(p[i], s[i], d, st1, ctx, relax):
                    yield from args_iter(i + 1, st2)
            start = 2 if isinstance(head, str) else 1
            for st2 in args_iter(start, st):
                ok = True
                yield st2
        if not ok and relax and tag == 'a' and isinstance(head, str) and is_const(head) and not is_prop(s):
            # relaxation 2: a unary library operation around the pattern is absorbed
            kept = [x for x in p[2:] if x != '*']
            if head in ABSORBABLE and len(kept) == 1 and not (isinstance(s, tuple) and s[0] in ('p', 'a') and s[1] == head):
                for st2 in match(kept[0], s, d, st, ctx, False):
                    wrapped = (tag, head) + tuple(x if x == '*' else s for x in p[2:])
                    yield State(st2.bind, st2.extras, st2.absorbed + ((ctx, wrapped, s),), st2.post)
        return
    if not isinstance(s, tuple):
        return
    if tag == '&':
        if s[0] != '&' or len(s) < len(p) or len(s) > 9:
            return
        ps, ss = p[1:], s[1:]

        def inj(i, used, st1):
            if i == len(ps):
                rest = tuple(x for j, x in enumerate(ss) if j not in used)
                yield State(st1.bind, st1.extras + tuple((ctx, r) for r in rest), st1.absorbed, st1.post)
                return
            for j in range(len(ss)):
                if j in used:
                    continue
                for st2 in match(ps[i], ss[j], d, st1, ctx, relax):
                    yield from inj(i + 1, used | {j}, st2)
        yield from inj(0, frozenset(), st)
        return
    if s[0] == '&' and tag in ('>', '!'):
        for i, c in enumerate(s[1:]):
            for st2 in match(p, c, d, st, ctx, relax):
                rest = tuple(x for j, x in enumerate(s[1:]) if j != i)
                yield State(st2.bind, st2.extras + tuple((ctx, r) for r in rest), st2.absorbed, st2.post)
        return
    if s[0] != tag:
        return
    if tag in ('\\', '!'):
        for st2 in match(p[1], s[1], d, st, ctx, False):
            yield from match(p[2], s[2], d + 1, st2, ctx + (s[1],), relax)
        return
    if tag == '>':
        for st2 in match(p[1], s[1], d, st, ctx, relax):
            yield from match(p[2], s[2], d, st2, ctx, relax)
        return


def finish(st):
    """Resolve postponed non-Miller applications."""
    for (p, s, d) in st.post:
        t = instantiate(p, st.bind)
        if t is None or not eq_mod(t, s):
            return None
    return st


def first_match(p, s, relax, limit=200):
    best = None
    n = 0
    STEPS[0] = 0
    try:
        for st in match(p, s, 0, State(), (), relax):
            n += 1
            st = finish(st)
            if st is not None:
                key = (len(st.absorbed), len(st.extras))
                if best is None or key < best[0]:
                    best = (key, st)
                    if key == (0, 0):
                        break
            if n >= limit:
                break
    except Budget:
        BUDGET_HITS[0] += 1
    return best[1] if best else None


BUDGET_HITS = [0]


def prune_forall(doms, body):
    """Close `body` (under binders with domains `doms`, outermost first) keeping only binders it uses."""
    def occurs(t, k):
        if isinstance(t, str):
            return t == '#%d' % k
        if t[0] in ('\\', '!'):
            return occurs(t[1], k) or occurs(t[2], k + 1)
        return any(occurs(x, k) for x in t[1:])
    c = body
    for dom in reversed(doms):
        if occurs(c, 0):
            c = ('!', dom, c)
        else:
            c = subst_bv0(c, '*')
    return c


# ---------------------------------------------------------------- signatures

def sig(t, pat):
    """Prop-level skeleton used as a hash key.  pat=True: pattern side."""
    if isinstance(t, str):
        return ''
    tag = t[0]
    if tag == 'p':
        h = t[1]
        if isinstance(h, str):
            if h[0] == '$':
                return '?' if pat else '§'
            if h[0] in '§#':
                return '§'
            sub = [sig(x, pat) for x in t[2:] if isinstance(x, tuple) and (x[0] in ('\\', '&', '>', '!', 'p'))]
            return h + '[' + ','.join(x for x in sub if x) + ']'
        return 'app'
    if tag == '&':
        return '&[' + ','.join(sorted(sig(x, pat) for x in t[1:])) + ']'
    if tag == '>':
        return '>[' + sig(t[1], pat) + ',' + sig(t[2], pat) + ']'
    if tag == '!':
        return '![' + sig(t[2], pat) + ']'
    if tag == '\\':
        inner = sig(t[2], pat)
        return '\\[' + inner + ']' if inner else ''
    return ''


def sig_variants(t, cap=400):
    """Subject side: signatures with up to 2 conjuncts dropped and up to 2 Prop subtrees wildcarded."""
    def go(t):
        # returns list of (sig, drops, wilds)
        if isinstance(t, str):
            return [('', 0, 0)]
        tag = t[0]
        if tag == 'p':
            h = t[1]
            out = [('?', 0, 1)]
            if isinstance(h, str):
                if h[0] in '§#$':
                    out.append(('§', 0, 0))
                    return out
                subs = [go(x) for x in t[2:] if isinstance(x, tuple) and (x[0] in ('\\', '&', '>', '!', 'p'))]
                for combo in itertools.product(*subs) if subs else [()]:
                    dr = sum(c[1] for c in combo)
                    wi = sum(c[2] for c in combo)
                    if dr <= 2 and wi <= 2:
                        out.append((h + '[' + ','.join(c[0] for c in combo if c[0]) + ']', dr, wi))
            else:
                out.append(('app', 0, 0))
            return out[:cap]
        if tag == '&':
            kids = [go(x) for x in t[1:]]
            out = [('?', 0, 1)]
            n = len(kids)
            for ndrop in range(0, min(2, n - 1) + 1):
                for dropped in itertools.combinations(range(n), ndrop):
                    keep = [kids[i] for i in range(n) if i not in dropped]
                    for combo in itertools.product(*keep):
                        dr = ndrop + sum(c[1] for c in combo)
                        wi = sum(c[2] for c in combo)
                        if dr <= 2 and wi <= 2:
                            if len(combo) == 1:
                                out.append((combo[0][0], dr, wi))
                            else:
                                out.append(('&[' + ','.join(sorted(c[0] for c in combo)) + ']', dr, wi))
                        if len(out) > cap:
                            return out
            return out
        if tag == '>':
            out = [('?', 0, 1)]
            for a in go(t[1]):
                for b in go(t[2]):
                    if a[1] + b[1] <= 2 and a[2] + b[2] <= 2:
                        out.append(('>[' + a[0] + ',' + b[0] + ']', a[1] + b[1], a[2] + b[2]))
            return out[:cap]
        if tag in ('\\', '!'):
            inner = go(t[2])
            if tag == '!':
                out = [('![' + x[0] + ']', x[1], x[2]) for x in inner]
                out.append(('?', 0, 1))
            else:
                out = [('\\[' + x[0] + ']', x[1], x[2]) for x in inner if x[0]]
                out.append(('', 0, 1 if out else 0))
            return out[:cap]
        return [('', 0, 0)]
    res = {x[0] for x in go(t) if x[0] not in ('?', '')}
    return res


def term_key(t, pat):
    """Key for non-Prop bodies: root head and the heads of its arguments."""
    if not (isinstance(t, tuple) and t[0] == 'a' and isinstance(t[1], str) and is_const(t[1])):
        return None

    def h(x):
        if isinstance(x, str):
            if x[0] == '$':
                return '?' if pat else '§'
            if x[0] in '§#':
                return '§'
            if x[0] == '%':
                return x
            return x
        if x[0] in ('p', 'a'):
            if isinstance(x[1], str):
                if x[1][0] == '$':
                    return '?' if pat else '§'
                if x[1][0] in '§#':
                    return '§'
                return x[1]
            return 'app'
        return x[0]
    return (t[1], tuple(h(x) for x in t[2:]))


def term_key_variants(t):
    k = term_key(t, False)
    if k is None:
        return []
    head, hs = k
    idx = [i for i, x in enumerate(hs) if x != '*']
    out = []
    if len(idx) > 7:
        idx = idx[:7]
    for r in range(len(idx) + 1):
        for comb in itertools.combinations(idx, r):
            out.append('a:' + head + '(' + ','.join('?' if i in comb else x for i, x in enumerate(hs)) + ')')
    return out


# ---------------------------------------------------------------- printer

OKNAME = re.compile(r"^[^\s()«»]+$")


class Unprintable(Exception):
    pass


def lean_name(n):
    if n.startswith('_private') or n == '?bad' or not OKNAME.match(n):
        raise Unprintable(n)
    parts = n.split('.')
    for q in parts:
        if q == '' or q[0].isdigit() or '✝' in q or '@' in q:
            raise Unprintable(n)
    return n


def to_lean(t, binders=(), slots=None):
    """binders: names of enclosing bound variables, innermost last."""
    if isinstance(t, str):
        c = t[0]
        if c == '*':
            return '_'
        if c == '§':
            return 'p%s' % t[1:]
        if c == '#':
            i = int(t[1:])
            if i >= len(binders):
                raise Unprintable(t)
            return binders[len(binders) - 1 - i]
        if c == '%':
            if t == '%s':
                raise Unprintable(t)
            return '(nat_lit %s)' % t[1:]
        if c == '@':
            return slots[int(t[1:])]
        if c == '$':
            raise Unprintable(t)
        return '@' + lean_name(t)
    tag = t[0]
    if tag in ('p', 'a'):
        h = t[1]
        if isinstance(h, str) and is_const(h):
            hs = '@' + lean_name(h)
        else:
            hs = to_lean(h, binders, slots)
        if len(t) == 2:
            return hs
        return '(' + hs + ' ' + ' '.join(to_lean(x, binders, slots) for x in t[2:]) + ')'
    if tag in ('\\', '!'):
        nm = 'x%d' % len(binders)
        dom = t[1]
        try:
            ds = '' if dom == '*' else ' : ' + to_lean(dom, binders, slots)
        except Unprintable:
            ds = ''
        body = to_lean(t[2], binders + (nm,), slots)
        if tag == '\\':
            return '(fun (%s%s) => %s)' % (nm, ds, body)
        return '(∀ (%s%s), %s)' % (nm, ds, body)
    if tag == '>':
        return '(%s → %s)' % (to_lean(t[1], binders, slots), to_lean(t[2], binders, slots))
    if tag == '&':
        return '(' + ' ∧ '.join(to_lean(x, binders, slots) for x in t[1:]) + ')'
    raise Unprintable(str(t))


def binding_to_lean(b):
    n, body = b
    if n == 0:
        return to_lean(body)
    names = ['y%d' % k for k in range(n)]
    return '(fun %s => %s)' % (' '.join(names), to_lean(body, (), names))


def show(t):
    """Inverse of parse."""
    if isinstance(t, str):
        return t
    return '(' + ' '.join(show(x) for x in t) + ')'
