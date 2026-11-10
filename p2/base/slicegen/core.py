"""slicegen core: Gherkin-subset parser, glossary loader, step matcher, scenario binding.

The generator is UNTRUSTED code. Its job is deliberately dumb: match each step
against exactly one glossary phrase and apply the named Lean definition to
variables. It never writes a Lean expression of its own. Lean type-checks what
it emits, the audit checks which constants the emitted statement uses, and the
report prints every statement beside its scenario.
"""
from __future__ import annotations

import difflib
import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

RULE_VERSION = "slicegen-rule/3"     # 2: several Whens in sequence; list and record literals
                                     # 3: Gherkin `Rule:` (a suite of scenarios; tags and Background inherited)


def sha(text: str) -> str:
    return hashlib.sha256(" ".join(text.split()).encode()).hexdigest()


def slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return ("s_" + s) if (not s or s[0].isdigit()) else s


# --------------------------------------------------------------------------- Gherkin

@dataclass
class Step:
    keyword: str          # as written: Given / When / Then / And / But / *
    kind: str             # given / when / then (And/But/* inherit)
    text: str
    line: int


@dataclass
class Scenario:
    feature: "Feature"
    name: str
    line: int
    end_line: int = 0
    tags: list = field(default_factory=list)
    outline: bool = False
    steps: list = field(default_factory=list)
    header: list = field(default_factory=list)
    rows: list = field(default_factory=list)      # [(line, [cells])]
    problems: list = field(default_factory=list)  # [(code, line, message)] found while parsing
    rule: "Rule | None" = None                    # the `Rule:` this scenario sits under, if any
    start_line: int = 0                           # first line of the tags / comments written directly above it

    @property
    def inherited_tags(self) -> list:
        """Tags of the Feature and of the Rule: they apply to every scenario beneath them (as in every
        Gherkin runner). `@id:` is never inherited: it names the thing it is written on."""
        up = list(self.feature.tags) + (list(self.rule.tags) if self.rule else [])
        return [t for t in up if not t.startswith("@id:")]

    @property
    def all_tags(self) -> list:
        """Inherited tags first, then the scenario's own; no duplicates."""
        out = []
        for t in self.inherited_tags + list(self.tags):
            if t not in out:
                out.append(t)
        return out

    @property
    def id(self) -> str:
        for t in self.tags:
            if t.startswith("@id:"):
                return f"Spec.{self.feature.slug}.{slug(t[4:])}"
        return f"Spec.{self.feature.slug}.{slug(self.name)}"

    @property
    def text(self) -> str:
        lines = self.feature.lines[self.line - 1:self.end_line]
        while lines and not lines[-1].strip():
            lines.pop()
        ind = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
        return "\n".join(l[ind:] for l in lines)

    @property
    def expect(self) -> str | None:
        # the scenario's own tag wins over one inherited from its Rule, which wins over the Feature's
        own = list(self.tags)
        up = (list(self.rule.tags) if self.rule else []) + list(self.feature.tags)
        for t in own + up:
            if t.startswith("@expect-"):
                return t[len("@expect-"):].upper()
        return None

    @property
    def control(self) -> bool:
        """Tagged `@control` (directly, or through its Rule or Feature): a check of the pipeline's own checks,
        not a claim about the code. Such a scenario gets its verdict like any other, but is left out of
        the suite adequacy note."""
        return "@control" in self.all_tags

    @property
    def background(self) -> list:
        """Background steps that run before this scenario's own: the Feature's, then its Rule's."""
        return list(self.feature.background) + (list(self.rule.background) if self.rule else [])


@dataclass
class Rule:
    """A Gherkin `Rule:`. The rule line and the free text under it are carried into the report verbatim;
    they are NOT compiled to Lean. What is proved is each scenario beneath it; together they are the
    rule's suite."""
    feature: "Feature"
    name: str
    line: int
    tags: list = field(default_factory=list)
    description: list = field(default_factory=list)   # free-text lines under the rule line
    background: list = field(default_factory=list)
    scenarios: list = field(default_factory=list)
    end_line: int = 0

    @property
    def id(self) -> str:
        for t in self.tags:
            if t.startswith("@id:"):
                return f"Rule.{self.feature.slug}.{slug(t[4:])}"
        return f"Rule.{self.feature.slug}.{slug(self.name)}"

    @property
    def text(self) -> str:
        """The rule line and its description (not the scenarios)."""
        return "\n".join([f"Rule: {self.name}"] + [l for l in self.description])


@dataclass
class Feature:
    path: str             # relative to slice/
    name: str = ""
    slug: str = ""
    line: int = 0
    lines: list = field(default_factory=list)
    background: list = field(default_factory=list)
    scenarios: list = field(default_factory=list)     # every scenario, in file order (inside a Rule or not)
    rules: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    description: list = field(default_factory=list)

    def suites(self) -> list:
        """[(Rule | None, [Scenario])] in file order: the scenarios before the first Rule (if any), then each Rule."""
        out = []
        loose = [sc for sc in self.scenarios if sc.rule is None]
        if loose:
            out.append((None, loose))
        return out + [(r, list(r.scenarios)) for r in self.rules]


class FeatureError(Exception):
    pass


def parse_feature(path: Path, rel: str) -> Feature:
    f = Feature(path=rel, lines=path.read_text().splitlines())
    cur = None            # current Scenario, "background", or "header" (description lines of Feature / Rule)
    rule = None           # current Rule: once a Rule starts, everything up to the next Rule belongs to it
    in_examples = False
    pending_tags: list = []
    pending_from = 0      # line of the first tag / comment directly above the next keyword line
    last_kind = None
    for no, raw in enumerate(f.lines, 1):
        s = raw.strip()
        if not s:
            if not pending_tags:
                pending_from = 0
            continue
        if s.startswith("#"):
            pending_from = pending_from or no
            continue
        if s.startswith("@"):
            pending_tags += s.split()
            pending_from = pending_from or no
            continue
        m = re.match(r"(Feature|Background|Scenario Outline|Scenario Template|Scenario|Example|Examples|Scenarios|Rule):\s*(.*)$", s)
        if m:
            kw, rest = m.groups()
            start, pending_from = pending_from or no, 0
            if kw == "Feature":
                if f.name:
                    raise FeatureError(f"{rel}:{no}: UNSUPPORTED: a second `Feature:` in one file")
                f.name, f.slug, f.line, f.tags = rest, slug(rest), no, pending_tags
                pending_tags, cur = [], "header"
            elif kw == "Rule":
                if not f.name:
                    raise FeatureError(f"{rel}:{no}: `Rule:` before `Feature:`")
                if not rest:
                    raise FeatureError(f"{rel}:{no}: a `Rule:` needs its text on the same line")
                if isinstance(cur, Scenario):
                    cur.end_line = start - 1
                if rule is not None:
                    rule.end_line = start - 1
                rule = Rule(feature=f, name=rest, line=no, tags=pending_tags)
                f.rules.append(rule)
                pending_tags, cur, in_examples, last_kind = [], "header", False, None
            elif kw == "Background":
                if (rule.scenarios or rule.background) if rule else (f.scenarios or f.background):
                    raise FeatureError(f"{rel}:{no}: UNSUPPORTED: a Background must come first in its Feature or Rule, and only once")
                cur, in_examples, last_kind = "background", False, None
            elif kw in ("Examples", "Scenarios"):
                if not isinstance(cur, Scenario) or not cur.outline:
                    raise FeatureError(f"{rel}:{no}: UNSUPPORTED: Examples outside a Scenario Outline")
                if cur.header:
                    cur.problems.append(("E_EXAMPLES", no, "more than one Examples table"))
                if pending_tags:
                    cur.problems.append(("E_EXAMPLES", no, "tags on an Examples table are not supported"))
                    pending_tags = []
                in_examples = True
            else:
                if isinstance(cur, Scenario):
                    cur.end_line = no - 1
                cur = Scenario(feature=f, name=rest, line=no, tags=pending_tags, rule=rule, start_line=start,
                               outline=kw in ("Scenario Outline", "Scenario Template"))
                pending_tags, in_examples, last_kind = [], False, None
                f.scenarios.append(cur)
                if rule is not None:
                    rule.scenarios.append(cur)
            continue
        pending_from = 0
        if cur is None:
            continue
        if cur == "header":       # free-text description under `Feature:` or `Rule:`
            (rule.description if rule is not None else f.description).append(s)
            continue
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not in_examples:
                if isinstance(cur, Scenario):
                    cur.problems.append(("E_DATATABLE", no, "data tables on steps are not supported"))
                continue
            if not cur.header:
                cur.header = cells
            else:
                cur.rows.append((no, cells))
            continue
        if s.startswith('"""') or s.startswith("```"):
            if isinstance(cur, Scenario):
                cur.problems.append(("E_DOCSTRING", no, "doc strings are not supported"))
            continue
        m = re.match(r"(Given|When|Then|And|But|\*)\s+(.*)$", s)
        if m and not in_examples:
            kw, text = m.groups()
            if kw in ("Given", "When", "Then"):
                last_kind = kw.lower()
            if last_kind is None:
                raise FeatureError(f"{rel}:{no}: `{kw}` with no preceding Given/When/Then")
            st = Step(kw, last_kind, " ".join(text.split()), no)
            if cur == "background":
                (rule.background if rule is not None else f.background).append(st)
            else:
                cur.steps.append(st)
            continue
        # anything else inside a scenario: free-text description line; ignore
    if isinstance(cur, Scenario):
        cur.end_line = len(f.lines)
    if rule is not None:
        rule.end_line = len(f.lines)
    ids = [r.id for r in f.rules]
    for r in f.rules:
        if ids.count(r.id) > 1:
            raise FeatureError(f"{rel}:{r.line}: two Rules of this feature have the same id {r.id}; "
                               "change one text or tag one with @id:<name>")
    # end_line: trim trailing blank / comment / tag lines belonging to the next scenario
    for sc in f.scenarios:
        e = sc.end_line
        while e > sc.line and (not f.lines[e - 1].strip() or f.lines[e - 1].strip()[0] in "#@"):
            e -= 1
        sc.end_line = e
    if not f.name:
        raise FeatureError(f"{rel}: no `Feature:` line")
    return f


def without_scenarios(path: Path, rel: str, names) -> str:
    """The text of a feature file with the named scenarios removed (`names`: the last part of each scenario id,
    e.g. `withdraw_covered`), each together with the tags and comments written directly above it.
    Used by the mutation harness to build controls; raises if a name is not found."""
    f = parse_feature(path, rel)
    drop = set()
    left = set(names)
    for sc in f.scenarios:
        short = sc.id.rsplit(".", 1)[1]
        if short in left:
            left.discard(short)
            end = sc.end_line
            while end < len(f.lines) and not f.lines[end].strip():      # the blank lines after it
                end += 1
            drop |= set(range(sc.start_line, end + 1))
    if left:
        raise FeatureError(f"{rel}: no scenario named {sorted(left)}")
    return "\n".join(l for no, l in enumerate(f.lines, 1) if no not in drop) + "\n"


# --------------------------------------------------------------------------- glossary

SLOT = re.compile(r"\{(\w+):(\w+)\}")
META = re.compile(r"([.^$*+?()\[\]{}|\\])")
PLACEHOLDER = r"<[A-Za-z_][A-Za-z0-9_]*>"
LIST_SEP = ", "


def nocapture(regex: str) -> str:
    """Turn capturing groups into non-capturing ones, so a literal's regex can sit inside a step regex
    without adding capture groups (cucumber passes one argument per group)."""
    return re.sub(r"(?<!\\)\((?!\?)", "(?:", regex)


def literal_regex(pts: dict, typ: str) -> str:
    """Regex of a literal of parameter type `typ`, without capturing groups.
    Three kinds of type:  scalar (`literal_regex`),  record (`literal_regex` with groups + `fields`),
    list (`list_of: <item type>`, written `[item, item, ...]`)."""
    pt = pts[typ]
    if "list_of" in pt:
        item = literal_regex(pts, pt["list_of"])
        return rf"\[(?:{item}(?:{LIST_SEP}{item})*)?\]"
    return nocapture(pt["literal_regex"])


def split_list(text: str) -> list:
    inner = text.strip()[1:-1].strip()
    return [x for x in inner.split(LIST_SEP)] if inner else []


def literal_problem(pts: dict, typ: str, text: str) -> str | None:
    """None if `text` is a literal of `typ` within range; otherwise what is wrong with it."""
    pt = pts[typ]
    if "enum" in pt:
        return None if text in pt["enum"] else f"`{text}` is not a value of `{typ}`"
    if not re.fullmatch(literal_regex(pts, typ), text):
        return f"`{text}` is not a literal of `{typ}`"
    if "list_of" in pt:
        for item in split_list(text):
            bad = literal_problem(pts, pt["list_of"], item)
            if bad:
                return bad
        return None
    mx = pt.get("max")
    if mx is None:
        return None
    if pt.get("fields"):
        for g, m in zip(re.fullmatch(pt["literal_regex"], text).groups(), mx):
            if m is not None and int(g) > m:
                return f"{g} in `{text}` exceeds the maximum of that field of `{typ}` ({m})"
        return None
    return f"literal {text} exceeds the maximum of `{typ}` ({mx})" if int(text) > mx else None


@dataclass
class Entry:
    raw: dict
    id: str
    kind: str
    phrase: str
    slots: list           # [(type, name)]
    match_re: re.Pattern  # generator-side: also accepts <placeholders>
    cucumber_re: str      # runner-side: concrete text only (cucumber substitutes rows first)

    def __getattr__(self, k):
        return self.raw.get(k)


@dataclass
class Glossary:
    raw: dict
    path: str
    param_types: dict
    actors: dict
    entries: list
    text: str

    def entry(self, id_):
        return next(e for e in self.entries if e.id == id_)


def load_glossary(path: Path, rel: str) -> Glossary:
    text = path.read_text()
    raw = yaml.safe_load(text)
    pts, actors = raw["param_types"], raw["actors"]
    entries = []
    for r in raw["steps"]:
        slots, gen, cuc, pos = [], "", "", 0
        for m in SLOT.finditer(r["phrase"]):
            lit = META.sub(r"\\\1", r["phrase"][pos:m.start()])
            gen += lit
            cuc += lit
            typ, name = m.groups()
            slots.append((typ, name))
            if typ in actors:
                alt = actors[typ]["name_regex"]
                gen += f"(?P<{name}>{alt})"
                cuc += f"({alt})"
            elif typ in pts:
                pt = pts[typ]
                alt = "|".join(META.sub(r"\\\1", k) for k in pt["enum"]) if "enum" in pt else literal_regex(pts, typ)
                gen += f"(?P<{name}>{alt}|{PLACEHOLDER})"
                cuc += f"({alt})"
            else:
                raise FeatureError(f"{rel}: step {r['id']}: unknown slot type `{typ}`")
            pos = m.end()
        tail = META.sub(r"\\\1", r["phrase"][pos:])
        entries.append(Entry(raw=r, id=r["id"], kind=r["kind"], phrase=r["phrase"], slots=slots,
                             match_re=re.compile("^" + gen + tail + "$"),
                             cucumber_re="^" + cuc + tail + "$"))
    ids = [e.id for e in entries]
    if len(set(ids)) != len(ids):
        raise FeatureError(f"{rel}: duplicate step ids")
    return Glossary(raw=raw, path=rel, param_types=pts, actors=actors, entries=entries, text=text)


# --------------------------------------------------------------------------- binding

@dataclass
class Val:
    kind: str             # param | lit | enum | actor
    text: str             # param name, literal digits, enum key, actor name
    type: str


@dataclass
class BoundStep:
    step: Step
    entry: Entry
    slots: dict           # slot name -> Val


@dataclass
class Problem:
    status: str           # UNBOUND | AMBIGUOUS | UNSUPPORTED
    code: str
    line: int
    message: str
    hint: str = ""


@dataclass
class Bound:
    sc: Scenario
    gloss: Glossary
    givens: list
    whens: list           # one or more When steps, executed in order
    thens: list
    params: list          # [(name, type)] in Examples-header order   (∀-bound)
    actors: list          # [(Name, type)] in order of first mention  (∀-bound)
    returned: list        # actor Names some When hands back, in order of first return
    builders: dict        # actor Name -> ("given", BoundStep) | ("hidden", param name)
    hidden: list          # [(name, type)] search-only parameters for actors with no constructive Given
    flags: list = field(default_factory=list)

    @property
    def id(self):
        return self.sc.id

    @property
    def scope(self):
        return "universal" if self.sc.outline else "instance"

    @property
    def when(self):
        """The LAST When: the one whose result `outcome` in a Then refers to."""
        return self.whens[-1]

    @property
    def multi(self):
        return len(self.whens) > 1

    @property
    def calls(self):
        seen = []
        for w in self.whens:
            if w.entry.call not in seen:
                seen.append(w.entry.call)
        return seen

    @property
    def all_steps(self):
        return self.givens + self.whens + self.thens

    def var(self, actor):
        return actor.lower()


def bind_step(step: Step, gloss: Glossary):
    hits = []
    for e in gloss.entries:
        if e.kind != step.kind:
            continue
        m = e.match_re.match(step.text)
        if not m:
            continue
        vals = {}
        for typ, name in e.slots:
            t = m.group(name)
            if typ in gloss.actors:
                vals[name] = Val("actor", t, typ)
            elif t.startswith("<"):
                vals[name] = Val("param", t[1:-1], typ)
            elif "enum" in gloss.param_types[typ]:
                vals[name] = Val("enum", t, typ)
            else:
                vals[name] = Val("lit", t, typ)
        hits.append(BoundStep(step, e, vals))
    return hits


def when_returns(w: BoundStep) -> list:
    """Actor names a When hands back, in tuple order (after the return value)."""
    out = []
    for r in w.entry.returns:
        m = re.fullmatch(r"post\((\w+)\)", r)
        if m:
            out.append(w.slots[m.group(1)].text)
    return out


def unbound_hint(step: Step, gloss: Glossary) -> str:
    phrases = [e.phrase for e in gloss.entries if e.kind == step.kind]
    near = difflib.get_close_matches(step.text, phrases, n=3, cutoff=0.0)
    stub = (f"  - id: {step.kind[0].upper()}-TODO\n    kind: {step.kind}\n"
            f"    phrase: \"{step.text}\"\n    lean: Vocab.TODO\n    args: []")
    return ("nearest glossary phrases:\n" + "\n".join(f"  - {p}" for p in near)
            + "\npaste-ready glossary stub (then define the Lean definition in the Vocab file of that crate):\n" + stub)


def bind(sc: Scenario, gloss: Glossary):
    """Return Bound, or Problem. First problem wins, in the verdict order UNBOUND > AMBIGUOUS > UNSUPPORTED."""
    steps = [Step(s.keyword, s.kind, s.text, s.line) for s in sc.background] + sc.steps
    bound, problems = [], []
    for st in steps:
        hits = bind_step(st, gloss)
        if not hits:
            problems.append(Problem("UNBOUND", "UNBOUND", st.line,
                                    f"no glossary `{st.kind}` phrase matches: \"{st.text}\"", unbound_hint(st, gloss)))
        elif len(hits) > 1:
            problems.append(Problem("AMBIGUOUS", "AMBIGUOUS", st.line,
                                    f"\"{st.text}\" matches {len(hits)} glossary entries: "
                                    + ", ".join(h.entry.id for h in hits)))
        else:
            bound.append(hits[0])
    for order in ("UNBOUND", "AMBIGUOUS"):
        for p in problems:
            if p.status == order:
                return p

    def unsupported(code, line, msg, hint=""):
        return Problem("UNSUPPORTED", code, line, msg, hint)

    if sc.problems:
        code, line, msg = sc.problems[0]
        return unsupported(code, line, msg)
    whens = [b for b in bound if b.entry.kind == "when"]
    if not whens:
        return unsupported("E_WHEN", sc.line, "at least one When is required, found 0")
    when = whens[-1]
    kinds = [b.entry.kind for b in bound]
    if kinds != sorted(kinds, key=["given", "when", "then"].index):
        return unsupported("E_ORDER", sc.line, "steps must be ordered Given*, When+, Then+ "
                                               "(a Then between two Whens is not supported)")
    givens = [b for b in bound if b.entry.kind == "given"]
    thens = [b for b in bound if b.entry.kind == "then"]
    if not thens:
        return unsupported("E_NOTHEN", sc.line, "a scenario needs at least one Then")

    # parameters
    ptypes, first_use = {}, {}
    for b in bound:
        for name, v in b.slots.items():
            if v.kind == "param":
                if ptypes.setdefault(v.text, v.type) != v.type:
                    return unsupported("E_TYPE", b.step.line,
                                       f"<{v.text}> is used as both `{ptypes[v.text]}` and `{v.type}`")
                first_use.setdefault(v.text, b)
            if v.kind == "lit":
                bad = literal_problem(gloss.param_types, v.type, v.text)
                if bad:
                    return unsupported("E_RANGE", b.step.line, bad)
    if ptypes and not sc.outline:
        return unsupported("E_PARAM", sc.line, "<placeholders> are only allowed in a Scenario Outline")
    if sc.outline and not sc.header:
        return unsupported("E_EXAMPLES", sc.line, "Scenario Outline without an Examples table")
    for name, b in first_use.items():
        if name not in sc.header:
            return unsupported("E_PARAM", b.step.line, f"<{name}> is not a column of the Examples table")
        if b.entry.kind == "then":
            return unsupported("E_OUTPUT_COLUMN", b.step.line,
                               f"<{name}> first appears in a Then, so nothing defines it for all inputs",
                               "phrase the Then relationally (in terms of the Givens' values)")
    params = [(h, ptypes[h]) for h in sc.header if h in ptypes]
    for h in sc.header:
        if h not in ptypes:
            return unsupported("E_PARAM", sc.rows[0][0] - 1 if sc.rows else sc.line, f"Examples column `{h}` is not used by any step")
        if not re.fullmatch(r"[a-z_][a-z0-9_]*", h):
            return unsupported("E_NAME", sc.line, f"Examples column `{h}` must be a lower-case identifier")
    for line, cells in sc.rows:
        if len(cells) != len(sc.header):
            return unsupported("E_EXAMPLES", line, "row has the wrong number of cells")
        for h, c in zip(sc.header, cells):
            bad = literal_problem(gloss.param_types, ptypes[h], c)
            if bad:
                return unsupported("E_RANGE", line, bad)

    # actors
    actors = []
    for b in bound:
        for typ, name in b.entry.slots:
            v = b.slots[name]
            if v.kind == "actor" and v.text not in [a for a, _ in actors]:
                actors.append((v.text, v.type))
    for a, _ in actors:
        if a.lower() in ptypes or a.lower() == "outcome":
            return unsupported("E_NAME", sc.line, f"actor `{a}` clashes with a parameter name")
    returned = []
    for w in whens:
        d = w.entry.distinct or []
        if len({w.slots[s].text for s in d}) != len(d):
            return unsupported("E_ALIAS", w.step.line, "the same actor is used for two arguments that cannot alias")
        for a in when_returns(w):
            if a not in returned:
                returned.append(a)
    # `outcome` in a Then is the LAST When's result: a Then written for another kind of result is a type error
    for t in thens:
        want = t.entry.outcome_type
        if "outcome" in t.entry.args and want and want != when.entry.outcome_type:
            return unsupported("E_TYPE", t.step.line,
                               f"\"{t.step.text}\" speaks about a result of type `{want}`, but the "
                               f"{'last ' if len(whens) > 1 else ''}When returns `{when.entry.outcome_type}`")

    builders, hidden = {}, []
    for a, typ in actors:
        g = next((g for g in givens if g.entry.builds and g.slots[g.entry.builds["actor"]].text == a), None)
        if g:
            builders[a] = ("given", g)
        else:
            hp = f"{a.lower()}_init"
            hidden.append((hp, gloss.actors[typ]["build"]["param_type"]))
            builders[a] = ("hidden", hp)
    return Bound(sc=sc, gloss=gloss, givens=givens, whens=whens, thens=thens, params=params,
                 actors=actors, returned=returned, builders=builders, hidden=hidden)
