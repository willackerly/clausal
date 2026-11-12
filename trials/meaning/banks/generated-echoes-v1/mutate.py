"""Mechanical mutations of a rule's composition tree, applied BEFORE echoing (plan node V5).

The compiler of clausal/ (clausal/vocab.py, read through the scratch copy trials/sentences/work/clausal) turns a Rule line
into clauses: a scoped operation (its modifiers and Givens as trees) and claims (frames applied to trees). Each function
here changes that structure in one place and the tool's OWN echo generator (`Compiler.echo_rule`) is run again on the
changed structure. The rule sentence is left as written, so the item is the ORIGINAL sentence against the echo of a
neighbouring tree.

  drop_given        the first clause that has a condition ('for which ...', 'internal') loses it
  strictness        the first comparison found changes between strict and non-strict (at most <-> strictly less than, ...)
  successful_only   the first clause about every call becomes a clause about successful calls only
  other_party       the first party word found (sender / receiver) becomes the other party
  measure           the first quantity found becomes a neighbouring one (the sum of the balances <-> the balances account
                    by account; one account's balance -> the sum; the transfers of the batch <-> those it stopped at)
"""
import sys
from pathlib import Path

SENT = Path(__file__).resolve().parents[3] / "sentences"
sys.path.insert(0, str(SENT))
import try_compile as tc                      # noqa: E402  (chdirs into the scratch copy and imports its clausal)
from clausal import vocab                    # noqa: E402
from clausal.vocab import Leaf, Node, say, walk   # noqa: E402

STRICT = {      # piece id -> (words of its echo, words of the neighbour's)
    "more_than": ("is strictly more than", "is at least"),
    "exceeds": ("is strictly more than", "is at least"),
    "not_more_than": ("is at most", "is strictly less than"),
    "at_most_value": ("is at most", "is strictly less than"),
    "sum_within": ("is at most", "is strictly less than"),
    "sum_exceeds": ("is strictly more than", "is at least"),
    "result_at_most": ("is at most", "is strictly less than"),
    "result_at_least": ("is at least", "is strictly more than"),
    "at_most": ("is at most", "is strictly less than"),
    "at_least": ("is at least", "is strictly more than"),
    "l.smaller_amount": ("is at most", "is strictly less than"),
    "l.larger_amount": ("is at least", "is strictly more than"),
}


def compile_one(text):
    voc, items, res = tc.compile_lines([text], name="bank")
    rd = items[0]["result"]
    if not isinstance(rd, vocab.Reading):
        return None, None, None
    return voc, vocab.Compiler(voc), rd


def trees_of(g):
    """(kind, index, tree) for every tree of a clause: its conditions first, then its claims."""
    for i, t in enumerate(g["cond_trees"]):
        yield "cond", i, t
    for i, c in enumerate(g["claims"]):
        if c.node is not None:
            yield "claim", i, c.node


def refresh(g):
    """Recompute the English of every tree of a clause after a change (the tool's own `say`)."""
    ctx = g["ctx"]
    k = 0
    for c in g["conds"]:
        if c.get("lean") is not None:              # a 'for which' condition (the 'internal' one has fixed words)
            c["echo"] = say(g["cond_trees"][k], ctx)
            k += 1
    for c in g["claims"]:
        if c.node is not None:
            c.echo = say(c.node, ctx)


def replace_in(tree, pred, make):
    """Replace the first node or leaf of `tree` for which pred holds; returns (new tree, what was replaced) or (tree, None)."""
    if pred(tree):
        return make(tree), tree
    if isinstance(tree, list):
        for i, x in enumerate(tree):
            new, hit = replace_in(x, pred, make)
            if hit is not None:
                tree[i] = new
                return tree, hit
    if isinstance(tree, Node):
        for name, x in tree.args.items():
            new, hit = replace_in(x, pred, make)
            if hit is not None:
                tree.args[name] = new
                return tree, hit
    return tree, None


def change_first(clauses, pred, make, skip_frames=()):
    for k, g in enumerate(clauses):
        for kind, i, t in trees_of(g):
            if kind == "claim" and g["claims"][i].frame["id"] in skip_frames:
                continue
            new, hit = replace_in(t, pred, make)
            if hit is not None:
                if kind == "cond":
                    g["cond_trees"][i] = new
                else:
                    g["claims"][i].node = new
                refresh(g)
                return k, kind, hit
    return None


def drop_given(voc, clauses):
    for k, g in enumerate(clauses):
        if g["conds"]:
            was = "; ".join(c["echo"] for c in g["conds"])
            g["conds"], g["cond_trees"], g["internal"] = [], [], False
            return f"clause {k + 1}: the condition is dropped ({was})"
    return None


def successful_only(voc, clauses):
    for k, g in enumerate(clauses):
        if not g["mods"]:
            g["mods"] = ["successful"]
            for c in g["claims"]:                  # as the compiler does for 'a successful <operation>'
                c.mods = ["successful"] + [m for m in c.mods if m != "successful"]
            return f"clause {k + 1}: 'every such call, accepted or rejected' becomes 'ONLY successful calls'"
    return None


def strictness(voc, clauses):
    def make(n):
        a, b = STRICT[n.id]
        p = dict(n.piece)
        assert a in p["echo"], (n.id, p["echo"])
        p["echo"] = p["echo"].replace(a, b)
        return Node(p, n.args, n.cat, form=n.form)
    hit = change_first(clauses, lambda x: isinstance(x, Node) and x.id in STRICT, make)
    if hit:
        k, kind, n = hit
        a, b = STRICT[n.id]
        return f"clause {k + 1}, {'condition' if kind == 'cond' else 'claim'}: `{n.id}` reads '{b}' where it reads '{a}'"
    return None


def other_party(voc, clauses):
    swap = {"l.sender": "l.receiver", "l.receiver": "l.sender"}
    names = {"the sender": "the receiver", "the receiver": "the sender"}

    def pred(x):
        return (isinstance(x, Node) and x.id in swap) or (isinstance(x, Leaf) and x.kind == "actor" and x.text in names)

    def make(x):
        if isinstance(x, Node):
            return Node(voc.pieces[swap[x.id]], x.args, x.cat, form=x.form)
        return Leaf(x.kind, x.type, names[x.text], x.how)
    hit = change_first(clauses, pred, make, skip_frames=("changes_only",))
    if hit:
        k, kind, x = hit
        was = x.id if isinstance(x, Node) else x.text
        return f"clause {k + 1}, {'condition' if kind == 'cond' else 'claim'}: {was} becomes {swap.get(was) or names[was]}"
    return None


def measure(voc, clauses):
    P = voc.pieces

    def ledger_of(n):
        return next(x for x in walk(n) if isinstance(x, Leaf) and x.kind == "actor")

    def pred(x):
        if not isinstance(x, Node):
            return False
        if x.id == "aggregate":
            return any(isinstance(y, Node) and y.id == "l.balances_of" for y in walk(x))
        return x.id in ("l.ledger", "l.bal_of", "l.transfers", "l.stopped_at")

    def make(x):
        if x.id == "aggregate":
            return Node(P["l.ledger"], {"l": ledger_of(x)}, "measure<balances>")
        if x.id in ("l.ledger", "l.bal_of"):
            return Node(P["aggregate"], {"ns": Node(P["l.balances_of"], {"l": ledger_of(x)}, "nums")}, "measure<num>")
        other = "l.stopped_at" if x.id == "l.transfers" else "l.transfers"
        return Node(P[other], x.args, x.cat)
    hit = change_first(clauses, pred, make)
    if hit:
        k, kind, x = hit
        to = {"aggregate": "the balances account by account", "l.ledger": "the sum of the balances", "l.bal_of": "the sum of the balances",
              "l.transfers": "the transfers at which the batch stopped", "l.stopped_at": "the transfers of the batch"}[x.id]
        return f"clause {k + 1}, {'condition' if kind == 'cond' else 'claim'}: `{x.id}` becomes {to}"
    return None


KINDS = {"drop_given": drop_given, "strictness": strictness, "successful_only": successful_only, "other_party": other_party, "measure": measure}


def render(echo):
    """The echo as the reader sees it: one line per slot line, the slot label at the start of its first line."""
    out = []
    for label, text in echo:
        out.append((label.capitalize() + ": " if label else "    ") + text)
    return "\n".join(out)


def faithful_echo(text):
    voc, comp, rd = compile_one(text)
    return None if rd is None else render(rd.echo)


def mutated_echo(text, kind):
    """(echo of the mutated tree, what was changed), or (None, None) when the mutation does not apply to this sentence."""
    voc, comp, rd = compile_one(text)
    if rd is None:
        return None, None
    before = render(rd.echo)
    clauses = rd.info["clauses"]
    what = KINDS[kind](voc, clauses)
    if what is None:
        return None, None
    comp.echo_rule(rd, clauses)
    after = render(rd.echo)
    return (after, what) if after != before else (None, None)


def selftest():
    """Where the mutated tree is one a sentence can spell, the mutated echo must be the tool's echo of that sentence."""
    pairs = [
        ("successful_only", "A transfer never changes the total of all balances of the ledger", "A successful transfer never changes the total of all balances of the ledger"),
        ("successful_only", "A computation of the total is always accepted", None),
        ("drop_given", "An internal transfer never changes the total of all balances of the ledger", "A transfer never changes the total of all balances of the ledger"),
        ("drop_given", "For a lookup for which the account is not an account of the ledger, there is no result", "For a lookup, there is no result"),
        ("measure", "A rejected transfer never changes the ledger", "A rejected transfer never changes the total of all balances of the ledger"),
        ("measure", "A batch never changes the total of all balances of the ledger", "A batch never changes the ledger"),
        ("other_party", "A transfer for which the amount is not more than the sender's balance is always accepted",
         "A transfer for which the amount is not more than the receiver's balance is always accepted"),
        ("other_party", "A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger",
         "A transfer is accepted only if the amount of the transfer is not more than the balance of account the receiver of the transfer of the ledger"),
    ]
    bad = 0
    for kind, text, same_as in pairs:
        got, what = mutated_echo(text, kind)
        if same_as is None:
            print(f"ok    {kind}: applies ({what})" if got else f"FAIL  {kind}: does not apply to {text!r}")
            bad += not got
            continue
        want = faithful_echo(same_as)
        ok = got == want
        bad += not ok
        print(f"{'ok   ' if ok else 'FAIL '} {kind}: echo of the mutated tree of {text!r} {'==' if ok else '!='} the tool's echo of {same_as!r}")
        if not ok:
            import difflib
            print("\n".join(difflib.unified_diff((want or "").splitlines(), (got or "").splitlines(), "tool", "mutated", lineterm="")))
    return bad


if __name__ == "__main__":
    sys.exit(1 if selftest() else 0)
