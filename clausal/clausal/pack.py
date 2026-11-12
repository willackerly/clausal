"""clausal pack: RULE PACKS (plan node K1; packs/README.md).

A rule pack (packs/<name>/pack.yaml) is a parameterised suite of ordinary Clausal sentences. This module is TEXT
EXPANSION AT AUTHORING TIME and nothing else: it fills the {slot} holes of the pack's template sentences with words the
caller gives, writes the resulting plain Rule lines into a project's feature file under tags that name the pack, its
version and the member, and records the bindings in a small file beside the feature. The pipeline never imports this
module and never reads a pack or a bindings file: the lines are compiled like any hand-written line, and the tags are
inert (deleting the pack and stripping the tags changes no verdict; packs/validated-input/strip_test.sh).

    python3 -m clausal pack instantiate <pack> --project P --slots name="words" ... [--variants axis=choice ...]
                 [--waive MEMBER="reason" ...] [--expect MEMBER=unproved|refuted ...] [--feature F] [--prefix X] [--dry-run]
                 [--bindings FILE]      (FILE: a bindings file written by an earlier run; flags given beside it win)
    python3 -m clausal pack check       every bindings file beside a feature file: re-expand and compare with the tagged lines
                                        (DRIFT), compile each line, print the completeness line. Exit 1 on drift.
    python3 -m clausal pack strip <file.feature> [--out FILE]    the feature file without the pack's tags and marker comments
                                        (every line keeps its number: the term lock of the book records lines)

What it reports per member: stated | stated (workaround) | waived | not applicable | cannot be stated, the last with the
compiler's refusal or the piece the pack says is missing. THE COMPLETENESS LINE ALWAYS COUNTS THE MEMBERS THAT ARE NOT
STATED. It is informational: no verdict, no exit status of run.sh, depends on it.
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

import yaml

from .core import FeatureError, Problem, load_glossary, parse_feature

ROOT = Path(__file__).resolve().parent.parent
PACK_DIR = "packs"
HOLE = re.compile(r"\{([a-z_]+)\}")
NO_SENTENCE = ("none", "not-applicable")


def load_pack(name: str, root: Path = ROOT) -> dict:
    path = root / PACK_DIR / name / "pack.yaml"
    if not path.exists():
        raise FeatureError(f"no rule pack `{name}` ({PACK_DIR}/{name}/pack.yaml)")
    raw = yaml.safe_load(path.read_text())
    for k in ("pack", "version", "slots", "members"):
        if k not in raw:
            raise FeatureError(f"{PACK_DIR}/{name}/pack.yaml: no `{k}:`")
    ids = [m["id"] for m in raw["members"]]
    if len(set(ids)) != len(ids):
        raise FeatureError(f"{PACK_DIR}/{name}/pack.yaml: a member id is given twice")
    for m in raw["members"]:
        if isinstance(m.get("stated"), bool):          # YAML reads a bare `no` / `yes` as a boolean
            m["stated"] = "yes" if m["stated"] else "no"
        texts = [m.get("sentence"), m.get("draft")] + [v for v in (m.get("variants") or {}).values() if v not in NO_SENTENCE]
        for t in texts:
            for h in HOLE.findall(t or ""):
                if h not in raw["slots"]:
                    raise FeatureError(f"{PACK_DIR}/{name}/pack.yaml: member {m['id']} uses the slot {{{h}}}, which `slots:` does not define")
        if "axis" in m and m["axis"] not in (raw.get("axes") or {}):
            raise FeatureError(f"{PACK_DIR}/{name}/pack.yaml: member {m['id']} names the axis `{m['axis']}`, which `axes:` does not define")
    return raw


def tag(pack: dict) -> str:
    return f"@pack:{pack['pack']}@{pack['version']}"


def slug(member_id: str, prefix: str = "") -> str:
    return prefix + re.sub(r"\W", "_", member_id).lower()


def expand(template: str, slots: dict) -> tuple:
    """(text, [slots the template uses that were not filled])."""
    missing = [h for h in HOLE.findall(template) if h not in slots]
    return HOLE.sub(lambda m: slots.get(m.group(1), m.group(0)), template), missing


def chosen(pack: dict, m: dict, variants: dict):
    """(template | None, why there is none, 'workaround' | 'yes' | 'no')."""
    if m.get("stated") == "no":
        return None, f"the pack has no sentence for it: needs {m['needs']}", "no"
    how = m.get("stated", "yes")
    if "variants" not in m:
        return m["sentence"], "", how
    axis = m["axis"]
    if axis not in variants:
        raise FeatureError(f"member {m['id']} depends on the axis `{axis}`: give --variants {axis}=<{' | '.join(pack['axes'][axis]['choices'])}>")
    v = m["variants"].get(variants[axis])
    how = (m.get("stated_by_variant") or {}).get(variants[axis], how)
    if v == "not-applicable":
        return None, f"not applicable: {axis} is {variants[axis]}", "n/a"
    if v == "none" or v is None:
        return None, f"the pack has no sentence for {axis}: {variants[axis]}" + (f"; needs {m['needs_if_none']}" if m.get("needs_if_none") else ""), "no"
    return v, "", how


def compiler(root: Path):
    from . import vocab
    gl = load_glossary(root / "glossary.yaml", "glossary.yaml")
    return vocab.Compiler(vocab.load_project(root, gl))


def compile_lines(comp, lines: list, books, rel: str = "pack.feature") -> list:
    """[(status, message)] of each Rule line read by the ordinary compiler (status COMPILED, or the refusal's)."""
    if not lines:
        return []
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "probe.feature"
        p.write_text("Feature: Pack probe\n\n" + "".join(f"  @id:probe_{k}\n  Rule: {x}\n\n" for k, x in enumerate(lines)))
        f = parse_feature(p, rel)
    out = []
    for r in f.rules:
        g = comp.rule(r, None, books=books)
        if isinstance(g, Problem):
            out.append((g.code or g.status, " ".join(g.message.split())))
        else:
            out.append(("COMPILED", ""))
    return out


def slot_notes(comp, pack: dict, slots: dict, books) -> list:
    """Informational: is each filled slot, on its own, a piece of the category the pack names, in the project's books?
    The authoritative check is the compilation of each whole sentence."""
    from . import vocab
    voc = comp.voc
    mine = lambda e: books is None or (voc.home.get(e["id"]) is not None and voc.home[e["id"]].rel in books)
    ops = [o for o in voc.ops.values() if mine(o)]
    notes = []
    parse_op = next((o for o in ops if slots.get("parse") in o["nouns"]), None)
    for name, spec in pack["slots"].items():
        if name not in slots:
            continue
        cat, text = spec["category"], slots[name]
        if cat == "operation":
            ok = any(text in o["nouns"] for o in ops)
            notes.append((name, text, cat, "an operation noun of the project's books" if ok else "NOT an operation noun of the project's books"))
            continue
        if parse_op is None:
            notes.append((name, text, cat, "not looked at: the slot `parse` names no operation"))
            continue
        ps = vocab.Parser(voc, parse_op["domain"], "rule", roles=vocab.op_roles(parse_op, voc))
        cats = [cat.replace("<T>", f"<{s}>") for s in voc.sorts] if "<T>" in cat else [cat]
        got = []
        for c in cats:
            try:
                got += [(c, t) for t in ps.parse(c, text)]
            except Exception:           # a category the parser has no forms for
                pass
        if got:
            c, t = got[0]
            notes.append((name, text, cat, f"reads as {c}: {vocab.describe(t)}" + (" (negated)" if getattr(t, "neg", False) else "")))
        else:
            notes.append((name, text, cat, "does not read as that category on its own (it may still read inside a sentence: a form with words between its holes)"))
    return notes


class Result:
    def __init__(self):
        self.members = []      # {id, state, how, sentence, why, expect, rule_id}

    def count(self, state):
        return [m for m in self.members if m["state"] == state]

    def line(self, pack, project) -> str:
        n = len(self.members)
        st, wa, na, no = self.count("stated"), self.count("waived"), self.count("not applicable"), self.count("cannot be stated")
        work = [m for m in st if m["how"] == "workaround"]
        parts = [f"{len(st)} stated" + (f" ({len(work)} of them through a workaround word: {', '.join(m['id'] for m in work)})" if work else "")]
        parts.append(f"{len(wa)} waived" + (" (" + "; ".join(f"{m['id']}: {m['why']}" for m in wa) + ")" if wa else ""))
        parts.append(f"{len(na)} not applicable" + (" (" + ", ".join(m["id"] for m in na) + ")" if na else ""))
        parts.append(f"{len(no)} CANNOT BE STATED" + (" (" + "; ".join(f"{m['id']}: {m['why']}" for m in no) + ")" if no else ""))
        head = "COMPLETE" if len(st) == n else "INCOMPLETE"
        return f"pack {pack['pack']}@{pack['version']} on {project}: {head}: {n} members: " + ", ".join(parts)


def instantiate(pack: dict, slots: dict, variants: dict, waive: dict, expect: dict, comp, books, prefix="") -> Result:
    res = Result()
    todo = []
    for m in pack["members"]:
        row = {"id": m["id"], "says": m.get("says", ""), "how": "", "sentence": None, "why": "", "expect": expect.get(m["id"]),
               "rule_id": slug(m["id"], prefix)}
        if m["id"] in waive:
            row.update(state="waived", why=waive[m["id"]])
            res.members.append(row)
            continue
        tmpl, why, how = chosen(pack, m, variants)
        row["how"] = how
        if tmpl is None:
            row.update(state="not applicable" if how == "n/a" else "cannot be stated", why=why)
            if m.get("draft"):
                row["draft"], _ = expand(m["draft"], slots)
                todo.append((row, row["draft"], True))
            res.members.append(row)
            continue
        text, missing = expand(tmpl, slots)
        if missing:
            row.update(state="cannot be stated", why="the project gave no word for the slot(s) " + ", ".join(missing), sentence=text)
        else:
            row.update(state="stated", sentence=text)
            todo.append((row, text, False))
        res.members.append(row)
    got = compile_lines(comp, [t for _, t, _ in todo], books)
    for (row, text, draft), (status, msg) in zip(todo, got):
        if draft:
            row["draft_status"] = status
            row["why"] += f"; the draft \"{text}\" is " + ("refused by the compiler: " + status if status != "COMPILED" else "COMPILED (the pack says it cannot be stated: check the pack)")
        elif status != "COMPILED":
            row.update(state="cannot be stated", why=f"refused by the compiler ({status}): {msg[:400]}")
    return res


MARK_OPEN = "# >>> pack {t}"
MARK_CLOSE = "# <<< pack {t}"


def block(pack: dict, res: Result, bindings_rel: str) -> list:
    t = tag(pack)[len("@pack:"):]
    L = [f"  {MARK_OPEN.format(t=t)}: written by `python3 -m clausal pack instantiate` from {PACK_DIR}/{pack['pack']}/pack.yaml with the",
         f"  # bindings of {bindings_rel}. Plain Rule lines, compiled like any other; the @pack tags are read by nothing in the pipeline.",
         "  # Members of the pack that are NOT stated here are listed in the bindings file and by `python3 -m clausal pack check`.", ""]
    for m in res.count("stated"):
        tags = [f"@id:{m['rule_id']}", tag(pack), f"@pack-rule:{m['id']}"] + ([f"@expect-{m['expect']}"] if m["expect"] else [])
        L += [f"  # {m['id']}: {m['says']}", "  " + " ".join(tags), f"  Rule: {m['sentence']}", ""]
    L.append(f"  {MARK_CLOSE.format(t=t)}")
    return L


def write_feature(path: Path, pack: dict, res: Result, project: str, bindings_rel: str):
    t = tag(pack)[len("@pack:"):]
    new = block(pack, res, bindings_rel)
    if not path.exists():
        head = [f"Feature: {project.capitalize()} rules",
                f"  Rule lines of the project `{project}` (projects.yaml).", ""]
        path.write_text("\n".join(head + new) + "\n")
        return
    lines = path.read_text().splitlines()
    a = next((k for k, l in enumerate(lines) if l.strip().startswith(MARK_OPEN.format(t=t))), None)
    b = next((k for k, l in enumerate(lines) if l.strip() == MARK_CLOSE.format(t=t)), None)
    if a is not None and b is not None and a < b:
        lines[a:b + 1] = new
    else:
        lines += ([""] if lines and lines[-1].strip() else []) + new
    path.write_text("\n".join(lines) + "\n")


def bindings_path(feature: Path, pack: dict) -> Path:
    return feature.with_name(f"{feature.stem}.pack.{pack['pack']}.yaml")


def write_bindings(path: Path, pack: dict, project, feature_rel, slots, variants, waive, expect, prefix, res: Result):
    doc = {"pack": pack["pack"], "version": pack["version"], "project": project, "feature": feature_rel, "prefix": prefix,
           "slots": slots, "variants": variants, "waive": waive, "expect": expect,
           "members": [{k: m[k] for k in ("id", "state", "how", "rule_id", "sentence", "why", "draft") if m.get(k)} for m in res.members]}
    head = (f"# BINDINGS of the rule pack {pack['pack']}@{pack['version']} on the project `{project}` (written by `python3 -m clausal pack\n"
            f"# instantiate`; read by `python3 -m clausal pack check` and by nothing in the pipeline). `slots`, `variants`, `waive` and\n"
            f"# `expect` are what the project chose; `members` is what came of it (rewritten on every instantiate).\n")
    path.write_text(head + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=200))


def kv(args: list, what: str) -> dict:
    out = {}
    for a in args:
        if "=" not in a:
            raise FeatureError(f"{what}: `{a}` is not name=value")
        k, v = a.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def take(argv: list, flag: str) -> list:
    """The values after `flag` up to the next --flag (the flag may be given several times)."""
    out, k = [], 0
    while k < len(argv):
        if argv[k] == flag:
            k += 1
            while k < len(argv) and not argv[k].startswith("--"):
                out.append(argv[k])
                k += 1
        else:
            k += 1
    return out


def cmd_instantiate(argv: list, root: Path = ROOT) -> int:
    from . import projects
    if not argv or argv[0].startswith("--"):
        raise FeatureError("usage: clausal pack instantiate <pack> --project P --slots name=\"words\" ...")
    pack = load_pack(argv[0], root)
    base = {}
    for b in take(argv, "--bindings"):
        base = yaml.safe_load(Path(b).read_text())
        if (base.get("pack"), base.get("version")) != (pack["pack"], pack["version"]):
            raise FeatureError(f"{b}: bindings of {base.get('pack')}@{base.get('version')}, not of {pack['pack']}@{pack['version']}")
    project = (take(argv, "--project") or [base.get("project")])[0]
    if not project:
        raise FeatureError("give --project <name> (a project of projects.yaml)")
    pr = projects.load(root)
    p = next((x for x in pr if x.name == project), None)
    if p is None:
        raise FeatureError(f"projects.yaml declares no project `{project}` (it declares {', '.join(x.name for x in pr)})")
    slots = {**(base.get("slots") or {}), **kv(take(argv, "--slots"), "--slots")}
    variants = {**(base.get("variants") or {}), **kv(take(argv, "--variants"), "--variants")}
    waive = {**(base.get("waive") or {}), **kv(take(argv, "--waive"), "--waive")}
    expect = {**(base.get("expect") or {}), **kv(take(argv, "--expect"), "--expect")}
    prefix = (take(argv, "--prefix") or [base.get("prefix") or ""])[0]
    for s in slots:
        if s not in pack["slots"]:
            raise FeatureError(f"the pack has no slot `{s}` (its slots: {', '.join(pack['slots'])})")
    for a, c in variants.items():
        if a not in (pack.get("axes") or {}) or c not in pack["axes"][a]["choices"]:
            raise FeatureError(f"--variants {a}={c}: the pack's axes are " + "; ".join(f"{k}: {' | '.join(v['choices'])}" for k, v in pack["axes"].items()))
    ids = {m["id"] for m in pack["members"]}
    for m in list(waive) + list(expect):
        if m not in ids:
            raise FeatureError(f"the pack has no member `{m}`")
    for m, e in expect.items():
        if e not in ("unproved", "refuted", "unbound", "vacuous"):
            raise FeatureError(f"--expect {m}={e}: one of unproved, refuted, unbound, vacuous")
    feature_rel = (take(argv, "--feature") or [base.get("feature") or (p.features[0] if p.features else None)])[0]
    if not feature_rel:
        raise FeatureError(f"project `{project}` lists no feature file: give --feature")
    if feature_rel not in p.features:
        raise FeatureError(f"{feature_rel} is not a feature file of project `{project}` (projects.yaml lists {', '.join(p.features)})")
    books = projects.books_of(pr, feature_rel)
    comp = compiler(root)
    res = instantiate(pack, slots, variants, waive, expect, comp, books, prefix)
    feature = root / feature_rel
    bpath = bindings_path(feature, pack)
    print(f"pack {pack['pack']}@{pack['version']} -> project {project}, {feature_rel}")
    print("slots (informational; the compiler reads each whole sentence):")
    for name, text, cat, note in slot_notes(comp, pack, slots, books):
        print(f"  {{{name}}} = \"{text}\"   [{cat}]  {note}")
    unfilled = [s for s in pack["slots"] if s not in slots]
    if unfilled:
        print(f"  not filled: {', '.join(unfilled)}")
    print("members:")
    for m in res.members:
        s = m["state"] + (" (workaround)" if m["state"] == "stated" and m["how"] == "workaround" else "")
        print(f"  {m['id']:6} {s:26} " + (f"Rule: {m['sentence']}" if m["state"] == "stated" else m["why"]))
    print(res.line(pack, project))
    if "--dry-run" in argv:
        print("(--dry-run: nothing written)")
        return 0
    write_feature(feature, pack, res, project, str(bpath.relative_to(root)))
    write_bindings(bpath, pack, project, feature_rel, slots, variants, waive, expect, prefix, res)
    print(f"wrote {feature_rel} ({len(res.count('stated'))} Rule lines under {tag(pack)}) and {bpath.relative_to(root)}")
    return 0


def tagged_rules(feature: Path, rel: str, pack: dict) -> dict:
    """{member id: Rule line text} of the lines of a feature file tagged with this pack."""
    f = parse_feature(feature, rel)
    out = {}
    for r in f.rules:
        if tag(pack) in r.tags:
            mid = next((t[len("@pack-rule:"):] for t in r.tags if t.startswith("@pack-rule:")), None)
            out[mid] = r.name.strip()
    return out


def cmd_check(argv: list, root: Path = ROOT) -> int:
    from . import projects
    pr = projects.load(root)
    files = sorted(p for f in pr.feature_paths() for p in (root / f).parent.glob(f"{Path(f).stem}.pack.*.yaml"))
    if not files:
        print("pack check: no bindings file beside any feature file (no rule pack is instantiated)")
        return 0
    comp, bad = compiler(root), 0
    for b in dict.fromkeys(files):
        doc = yaml.safe_load(b.read_text())
        rel = str(b.relative_to(root))
        try:
            pack = load_pack(doc["pack"], root)
        except FeatureError as e:
            print(f"pack check: {rel}: {e} (the feature's lines stand as plain lines; nothing to compare)")
            continue
        if pack["version"] != doc["version"]:
            print(f"pack check: {rel}: DRIFT: instantiated from version {doc['version']}, the pack is now version {pack['version']}")
            bad += 1
            continue
        books = projects.books_of(pr, doc["feature"])
        res = instantiate(pack, doc["slots"], doc["variants"], doc.get("waive") or {}, doc.get("expect") or {}, comp, books, doc.get("prefix") or "")
        have = tagged_rules(root / doc["feature"], doc["feature"], pack)
        want = {m["id"]: m["sentence"] for m in res.count("stated")}
        drift = [f"{k}: the feature has \"{have[k]}\", the pack gives \"{want[k]}\"" for k in want if k in have and have[k] != want[k]]
        drift += [f"{k}: stated by the pack, no tagged line in the feature" for k in want if k not in have]
        drift += [f"{k}: a tagged line in the feature, not stated by the pack" for k in have if k not in want]
        print(res.line(pack, doc["project"]))
        for m in res.members:
            if m["state"] != "stated":
                print(f"  {m['id']}: {m['state'].upper()}: {m['why']}")
        if drift:
            bad += 1
            print(f"  DRIFT ({rel} against {doc['feature']}): " + "; ".join(drift))
        else:
            print(f"  no drift: the {len(want)} tagged lines of {doc['feature']} are the pack's sentences with the bindings of {rel}")
    return 1 if bad else 0


def strip_text(text: str) -> str:
    out = []
    for l in text.splitlines():
        s = l.strip()
        if s.startswith("# >>> pack ") or s.startswith("# <<< pack "):
            out.append(l[:len(l) - len(l.lstrip())] + "#")       # the line stays (as an empty comment): no line number moves
            continue
        if s.startswith("@"):
            keep = [t for t in s.split() if not t.startswith("@pack:") and not t.startswith("@pack-rule:")]
            l = l[:len(l) - len(l.lstrip())] + " ".join(keep)
        out.append(l)
    return "\n".join(out) + "\n"


def cmd_strip(argv: list) -> int:
    if not argv:
        raise FeatureError("usage: clausal pack strip <file.feature> [--out FILE]")
    src = Path(argv[0])
    out = (take(argv, "--out") or [argv[0]])[0]
    Path(out).write_text(strip_text(src.read_text()))
    print(f"pack strip: {src} -> {out} (pack tags removed, marker comments emptied; every line keeps its number; Rule lines, @id and @expect tags kept)")
    return 0


def main(argv: list) -> int:
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "instantiate":
        return cmd_instantiate(argv[1:])
    if argv[0] == "check":
        return cmd_check(argv[1:])
    if argv[0] == "strip":
        return cmd_strip(argv[1:])
    print(f"clausal pack: unknown subcommand {argv[0]} (instantiate | check | strip)", file=sys.stderr)
    return 2
