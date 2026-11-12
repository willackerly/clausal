"""clausal book: checks on the Clausebook itself (plan nodes C1 and Q3).

    python3 -m clausal book check [--lean] [--update-expected] [--update-terms] [--json]
    python3 -m clausal book core [--lean]

`book core` (also the first part of `book check`): CORE STANDS ALONE.
  * clausebook/core.yaml loads by itself, with no other book and no glossary (no literal type, no actor type);
  * neither it nor the Lean files of the frame library (lean/Frames/*.lean) contains a FIXTURE NOUN: a word the other
    books and the glossary bring (actor and literal types, sorts, operation nouns, role names, Lean namespaces, crates);
  * with --lean: lean/Frames, copied alone into a scratch directory with a lakefile that has no dependency, builds.

`book check`: the REGISTRATION LINT (docs/studies/2026-11-12/readability.md, section 1), over EVERY accepted surface form
of the loaded books (the forms of the pieces in every position, the idioms, the `when` forms and nouns of the operations,
the grammar entries of core):

  1  holes      a form's holes are exactly the piece's holes: same names, same categories, none filled by a literal
  2  order      holes are in another order than in the piece's first form only where their categories all differ
  3  one form   at most one live form per piece per position (3a: per position; 3b: in a Rule line, where both a verb
                phrase and "for <subject>, <Then claim>" are read, and both an adjective on the subject and a prefix on the claim)
  4  skeleton   no two forms of DIFFERENT pieces share a literal skeleton (the form with its holes blanked), unless a
                separating pair is recorded (`separations:` in a book: one sentence for each piece, which the compiler
                must read as that piece and not the other) and SIGNED (`clausal review <id>`; void when either piece or
                either reading changes). A separation that is recorded and not in force is itself a violation.
  5  same term  every sentence of features/ and controls/ compiles to the term recorded in clausebook/terms.lock.json

The violations found are compared with clausebook/check.expected.json: exit 0 iff they are exactly the expected ones
(and core stands alone). The expected file is today's debt, cleared by plan node Q4; `--update-expected` rewrites it,
`--update-terms` rewrites the lock (after sentences were added, removed or deliberately changed).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from . import vocab
from .core import FeatureError, load_glossary
from .pipeline import LEAN, ROOT

CORE = "core.yaml"


def fixture_nouns(voc, gloss) -> dict:
    """word or phrase -> where it comes from: everything the non-core books and the glossary NAME."""
    out = {}
    def add(w, why):
        w = str(w).strip()
        if w:
            out.setdefault(w.lower(), why)
    for a in gloss.actors:
        add(a, "actor type (glossary.yaml)")
    for t in gloss.param_types:
        add(t, "literal type (glossary.yaml)")
    core = voc.books[0]
    for b in voc.books[1:]:
        for s in b.raw.get("sorts") or []:
            add(s, f"sort of {b.rel}")
        for ns in (b.raw.get("lean_files") or {}):
            out.setdefault(ns + ".", f"Lean namespace of {b.rel}")
        for o in b.raw.get("operations") or []:
            for n in o["nouns"]:
                add(n, f"operation noun ({o['id']}, {b.rel})")
            for r, _ in list(o["state"]) + list(o["input"]):
                add(r, f"role of {o['id']} ({b.rel})")
            add(o["model"].split(".")[0], f"crate of {o['id']} ({b.rel})")
    for w in list(out):                      # plain plurals
        if w.isalpha() and not w.endswith("s"):
            out.setdefault(w + "s", out[w] + ", plural")
    assert voc.home and core is voc.books[0]
    return out


def find_nouns(text: str, nouns: dict) -> list:
    """[(line number, noun, source)] for every occurrence of a fixture noun as a whole word."""
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for w, why in nouns.items():
            pat = (r"(?<![A-Za-z0-9_.])" + re.escape(w)) if w.endswith(".") else (r"(?<![A-Za-z0-9_])" + re.escape(w) + r"(?![A-Za-z0-9_])")
            if re.search(pat, line, 0 if w.endswith(".") else re.I):
                hits.append((n, w, why))
    return hits


def frames_alone(lean_dir: Path = LEAN) -> tuple:
    """Build lean/Frames in a scratch directory that holds nothing else. (ok, message)."""
    with tempfile.TemporaryDirectory(prefix="clausal-core-") as d:
        d = Path(d)
        shutil.copytree(lean_dir / "Frames", d / "Frames")
        shutil.copy(lean_dir / "lean-toolchain", d / "lean-toolchain")
        (d / "lakefile.toml").write_text('name = "frames"\ndefaultTargets = ["Frames"]\n\n[[lean_lib]]\nname = "Frames"\nglobs = ["Frames.+"]\n')
        import os
        env = dict(os.environ, PATH=str(Path.home() / ".elan" / "bin") + os.pathsep + os.environ.get("PATH", ""))
        try:
            r = subprocess.run(["lake", "build", "Frames"], cwd=d, capture_output=True, text=True, env=env)
        except FileNotFoundError:
            return False, "lean/Frames was NOT built alone: `lake` is not on the PATH"
        mods = sorted(p.stem for p in (d / "Frames").glob("*.lean"))
        built = sorted(p.stem for p in (d / ".lake" / "build" / "lib" / "lean" / "Frames").glob("*.olean")) if r.returncode == 0 else []
        if r.returncode or built != mods:
            return False, f"lean/Frames does NOT build alone (exit {r.returncode}; built {built} of {mods}):\n" + (r.stdout + r.stderr)[-2000:]
        return True, f"lean/Frames builds alone, with no dependency: {len(mods)} modules ({', '.join(mods)})"


def core_alone(lean: bool = False, root: Path = ROOT) -> dict:
    """{ok, lines, problems}: does core stand alone? (`root`: the project directory; another one only in the self-test,
    which seeds a fixture noun and a foreign import into a copy and expects this to say so.)"""
    ROOT, LEAN = root, root / "lean"                      # everything below reads the project at `root`
    lines, problems = [], []
    books = vocab.project_books(ROOT)
    core = next(((p, rel) for p, rel in books if p.name == CORE), None)
    if core is None or books[0] != core:
        return {"ok": False, "lines": [], "problems": [f"clausebook/project.yaml must list {CORE} first"]}
    try:
        alone = vocab.Vocabulary([core])                      # no other book, no glossary
        k = alone.kinds()
        lines.append(f"{core[1]} loads alone, with no glossary: {k['frame']} frames, {k['modifier']} modifiers, {len(alone.coverage)} coverage entries, "
                     f"{len(alone.raw['defaults'])} defaults; {k['domain']} domain words, {len(alone.ops)} operations, {len(alone.idioms)} idioms; "
                     f"sorts {alone.sorts}; Lean imports {alone.raw['lean_imports']}")
        if k["domain"] or alone.ops or alone.idioms or alone.books[0].raw.get("uses_types"):
            problems.append(f"{core[1]} holds a domain word, an operation, an idiom or a `uses_types` entry: core may have none")
    except FeatureError as e:
        problems.append(f"{core[1]} does not load alone: {e}")
        return {"ok": False, "lines": lines, "problems": problems}
    gloss = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    voc = vocab.load_project(ROOT, gloss)
    nouns = fixture_nouns(voc, gloss)
    files = [core[0]] + sorted((LEAN / "Frames").glob("*.lean"))
    for f in files:
        rel = str(f.relative_to(ROOT))
        hits = find_nouns(f.read_text(), nouns)
        problems += [f"{rel}:{n}: names `{w}`, a fixture noun ({why})" for n, w, why in hits]
    lines.append(f"no fixture noun in {', '.join(str(f.relative_to(ROOT)) for f in files)} "
                 f"({len(nouns)} words and phrases looked for, whole words, comments included)" if not any("fixture noun" in p for p in problems)
                 else "fixture nouns found in core (listed below)")
    for f in sorted((LEAN / "Frames").glob("*.lean")):
        for m in re.finditer(r"^import\s+(\S+)", f.read_text(), re.M):
            if not m.group(1).startswith("Frames."):
                problems.append(f"{f.relative_to(ROOT)}: imports {m.group(1)}, which is outside the frame library")
    if lean:
        ok, msg = frames_alone(LEAN)
        (lines if ok else problems).append(msg)
    else:
        lines.append("lean/Frames built alone: not run (pass --lean)")
    return {"ok": not problems, "lines": lines, "problems": problems, "nouns": len(nouns)}



RESERVED = {"op", "op2", "opbase", "item", "type", "claim", "subject", "vp", "clause", "role", "line"}   # structural holes: not a piece's own
FIELDS = (("forms", "any step"), ("not_forms", "any step, negated"), ("then_forms", "Then"), ("vp_forms", "Rule verb phrase"),
          ("subject_forms", "Rule subject"), ("claim_forms", "before the claim of a Then step"),
          ("first_call_forms", "of the first of two compared calls"), ("first_call_not_forms", "of the first of two compared calls, negated"))
EXPECTED = "check.expected.json"
LOCK = "terms.lock.json"


def skeleton(text: str) -> str:
    """The literal words of a form: every hole blanked."""
    return " ".join(vocab.HOLE.sub("{}", text).split())


def holes_of(text: str) -> list:
    return [(s[1], vocab.hole_voice(s[2])[0]) for s in vocab.segments(text) if s[0] == "hole" and s[1] not in RESERVED]


def surface(voc) -> list:
    """Every accepted surface form of the loaded books: [{owner, kind, domain, field, position, form, cat}]."""
    out = []
    def add(owner, kind, domain, field, position, form, cat):
        out.append({"owner": owner, "kind": kind, "domain": domain, "field": field, "position": position, "form": form, "cat": cat})
    for o in voc.ops.values():
        for f in o["when"]:
            add(o["id"], "operation", o["domain"], "when", "When", f, "op")
        for n in o["nouns"]:
            add(o["id"], "operation", o["domain"], "nouns", "Rule subject noun", n, "op")
    for p in voc.pieces.values():
        for field, position in FIELDS:
            for f in p.get(field) or []:
                add(p["id"], p["kind"], p.get("domain", "shared"), field, position, f, p["cat"])
        for f in (p.get("per_actor") or {}).get("forms", []):
            add(p["id"], p["kind"], p.get("domain", "shared"), "per_actor.forms", "plural", f, "per_actor")
    for i in voc.idioms.values():
        add(i["id"], "idiom", i.get("domain", "shared"), "form", "Then" if i["cat"] == "claim" else "any step", i["form"], i["cat"])
    for g in voc.grammar.values():
        for f in g.get("forms") or []:
            add(g["id"], "grammar", "shared", "forms", "Rule line", f, "grammar")
    return out


def piece_holes(p: dict) -> tuple:
    """(names of the piece's own holes, {name: category} where the book declares one, names written as a LIST hole)."""
    declared = p.get("_args_declared")
    if declared:
        names = list(p["args"])
    else:
        names = [m.group(1) for t in (p.get("lean", ""), p.get("item", "")) for m in vocab.HOLE.finditer(t)]
        names = [n for n in dict.fromkeys(names) if n not in RESERVED and n not in (p.get("from_operation") or [])]
    cats = {n: c for n, c in (p["args"] if declared else {}).items()}
    lists = {n: c[len("list<"):-1] for n, c in cats.items() if isinstance(c, str) and c.startswith("list<")}
    return names, cats, lists


def shared_skeletons(forms: list, a: str, b: str) -> list:
    """The literal skeletons that a form of `a` and a form of `b` both have."""
    sk = lambda o: {skeleton(f["form"]) for f in forms if f["owner"] == o and f["kind"] != "grammar"}
    return sorted(sk(a) & sk(b))


def skeleton_pattern(sk: str):
    """A skeleton as a pattern over text: each hole is one or more characters."""
    return re.compile(r"\s+".join(".+" if w == "{}" else re.escape(w).replace(r"\{\}", ".+") for w in sk.split()))


def head_collisions(forms: list) -> list:
    """[(general, specific)]: two Rule verb phrases of DIFFERENT frames, the second an instance of the first's skeleton
    (a hole of the first swallows the extra words of the second): "never changes {m}" and "never changes the answer when
    {v}". The second takes the first one's head with another meaning. (Readability synthesis, section 3, Q8 control 1.)"""
    vps = [(f, skeleton(f["form"])) for f in forms if f["field"] == "vp_forms"]
    out = []
    for a, ska in vps:
        for b, skb in vps:
            if a["owner"] != b["owner"] and ska != skb and "{}" in ska and skeleton_pattern(ska).fullmatch(skb.replace("{}", "X")):
                out.append((a, b))
    return out


def read_line(voc, line: str):
    """One Rule line, compiled against the loaded books: a Reading or a Problem."""
    from .core import parse_feature
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "separation.feature"
        p.write_text(f"Feature: Separation\n\n  Rule: {line}\n")
        f = parse_feature(p, "separation.feature")
    try:
        return vocab.Compiler(voc).rule(f.rules[0], None)
    except FeatureError as e:
        from .core import Problem
        return Problem("UNSUPPORTED", "UNSUPPORTED", 0, str(e), "")


def separation_state(voc, s: dict, forms: list | None = None) -> dict:
    """Does the separation `s` separate? {ok, why, terms}. Each of its two sentences is COMPILED now. It separates iff
      * the two pieces do share a literal skeleton (otherwise there is nothing to exempt),
      * each sentence is written with that skeleton (its literal words, in order),
      * each sentence compiles, to a reading that uses its own piece and does not use the other.
    Nothing here asks who signed: `lint` does, against the sign-off record of the entry."""
    forms = surface(voc) if forms is None else forms
    a, b = s["between"]
    why, terms = [], {}
    sks = shared_skeletons(forms, a, b)
    mine = {a: sks, b: sks}                      # the skeleton each sentence must be written with
    if not sks:                                  # ... or the two verb phrases of a head collision, each piece its own
        heads = [(g, sp) for g, sp in head_collisions(forms) if {g["owner"], sp["owner"]} == {a, b}]
        mine = {x: [skeleton(f["form"]) for pair in heads for f in pair if f["owner"] == x] for x in (a, b)}
        sks = sorted(set(mine[a]) | set(mine[b]))
    if not sks:
        why.append(f"no form of `{a}` shares a literal skeleton with a form of `{b}`, and no verb phrase of one takes the head of the other")
    for me, other in ((a, b), (b, a)):
        line = s["inputs"][me]
        pats = [re.compile(skeleton_pattern(sk).pattern, re.I) for sk in mine[me]]
        if sks and not any(p.search(line) for p in pats):
            why.append(f"the sentence for `{me}` (\"{line}\") is not written with the shared skeleton " + " / ".join(f'"{x}"' for x in mine[me]))
        rd = read_line(voc, line)
        if not isinstance(rd, vocab.Reading):
            terms[me] = f"REFUSED {rd.status}"
            why.append(f"the sentence for `{me}` (\"{line}\") does not compile ({rd.status})")
            continue
        terms[me] = rd.lean_def()
        if me not in rd.used:
            why.append(f"the sentence for `{me}` (\"{line}\") is not read with `{me}` (it is read with: {', '.join(rd.used)})")
        if other in rd.used:
            why.append(f"the sentence for `{me}` (\"{line}\") is read with `{other}` as well: it does not tell the two apart")
    return {"ok": not why, "why": why, "terms": terms}


def separation_parts(voc, s: dict) -> list:
    """What a sign-off of a separation is a sign-off OF, beside its own entry: the book text of the two pieces, and what
    each of its sentences compiles to."""
    from . import vreport
    st = separation_state(voc, s)
    return [vreport.entry_text(voc, x) for x in s["between"]] + [f"{k} := {st['terms'][k]}" for k in s["between"]]


def lint(voc, records=None) -> tuple:
    """(violations, notes). A violation: {check, key, owner(s), what}. `key` identifies it in the expected file.
    `records`: the attestation records (attest.Records; None: the ones stored beside the books)."""
    V, notes = [], {}
    forms = surface(voc)
    def v(check, key, what, **more):
        V.append({"check": check, "key": key, "what": what} | more)
    # ---- 1 holes, 2 order
    for p in voc.pieces.values():
        names, cats, lists = piece_holes(p)
        mine = [f for f in forms if f["owner"] == p["id"] and f["kind"] != "idiom" and f["field"] != "per_actor.forms"]
        seen_cat = dict((n, c) for n, c in cats.items() if n not in lists)
        ref_order = None
        for f in mine:
            hs = holes_of(f["form"])
            got = [n for n, _ in hs]
            item_cats = {c for c in lists.values()}
            as_list = [n for n, c in hs if n not in names and c in item_cats]          # a list hole written as several holes
            missing = [n for n in names if n not in got and not (n in lists and as_list)]
            extra = [n for n in got if n not in names and n not in as_list]
            if missing or extra:
                imp = p.get("implied") or {}
                why = []
                for n in missing:
                    why.append(f"`{n}` is not in the form" + (f": the words of the form stand for it (the book says `implied: {n} = {imp[n]}`)" if n in imp
                                                               else ": a literal fills it"))
                why += [f"`{n}` is no hole of the piece" for n in extra]
                v("1 holes", f"{p['id']}|{f['field']}|{f['form']}", f"`{p['id']}` ({f['position']}) \"{f['form']}\": " + "; ".join(why),
                  owner=p["id"], form=f["form"])
            for n, c in hs:
                if n in as_list or c is None:
                    continue
                if n in seen_cat and seen_cat[n] != c:
                    v("1 holes", f"{p['id']}|{f['field']}|{f['form']}|{n}", f"`{p['id']}` \"{f['form']}\": hole `{n}` is a {c} here and a {seen_cat[n]} elsewhere in the piece",
                      owner=p["id"], form=f["form"])
                seen_cat.setdefault(n, c)
            order = [n for n in got if n in names]
            if ref_order is None:
                ref_order = order
            else:
                common = [n for n in ref_order if n in order]
                now = [n for n in order if n in common]
                if now != common:
                    moved = [n for n, m in zip(common, now) if n != m]
                    cs = [seen_cat.get(n) for n in moved]
                    if len(set(cs)) != len(cs):
                        v("2 order", f"{p['id']}|{f['field']}|{f['form']}", f"`{p['id']}` \"{f['form']}\": the holes {', '.join(moved)} are in another order "
                          f"than in the piece's first form, and their categories ({', '.join(map(str, cs))}) do not all differ", owner=p["id"], form=f["form"])
    for i in voc.idioms.values():
        got = {n for n, _ in holes_of(i["form"])}
        used = set(re.findall(r"(?<![\w.])([A-Za-z_]\w*)(?![\w.(])", re.sub(r"[A-Za-z_][\w.]*\(", "(", i["means"])))
        if got != used:
            v("1 holes", f"{i['id']}|form|{i['form']}", f"idiom `{i['id']}`: the holes of its form ({sorted(got)}) are not the names its meaning uses ({sorted(used)})",
              owner=i["id"], form=i["form"])
    for o in voc.ops.values():
        roles = {r for r, _ in list(o["state"]) + list(o["input"])}
        for f in o["when"]:
            got = {n for n, _ in holes_of(f)}
            if got != roles:
                v("1 holes", f"{o['id']}|when|{f}", f"operation `{o['id']}` \"{f}\": its holes ({sorted(got)}) are not its roles ({sorted(roles)})", owner=o["id"], form=f)
    # ---- 3 one live form per piece per position
    by = {}
    for f in forms:
        by.setdefault((f["owner"], f["field"]), []).append(f)
    for (owner, field), fs in by.items():
        if len(fs) > 1:
            v("3a one form per position", f"{owner}|{field}", f"`{owner}` has {len(fs)} live forms in one position ({fs[0]['position']}): "
              + "; ".join(f"\"{f['form']}\"" for f in fs), owner=owner, forms=[f["form"] for f in fs])
    line = voc.grammar.get("g.line") or {}
    opt = [k for k in ("first_letter_either_case", "final_full_stop_optional") if line.get(k)]
    if opt:
        v("3a one form per position", "g.line|written", f"`g.line`: every Rule line is accepted in {2 ** len(opt)} written forms ({' and '.join(o.replace('_', ' ') for o in opt)})",
          owner="g.line", forms=opt)
    # 3b. Since plan node Q4 the book itself says how "for <subject>, <claim>" is read (`g.rule_for`): `reads: no_verb_phrase`
    # (a Then form is read there only if its frame has no verb phrase with the same holes) and `narrowing: on_subject` (no
    # prefix before the claim). The compiler obeys both (vocab.Compiler.clause_violations). What is still two ways in one
    # Rule line: a frame whose verb phrase has OTHER holes than its Then form (its words stand for a hole: `implied`).
    names = lambda f: {n for n, _ in holes_of(f)}
    if "g.rule_for" in voc.grammar and "g.rule_vp" in voc.grammar:
        for p in voc.pieces.values():
            one_voice = voc.for_reads == "no_verb_phrase" and all(any(names(x) == names(y) for y in p.get("vp_forms") or []) for x in p.get("then_forms") or [])
            if p.get("then_forms") and p.get("vp_forms") and not one_voice:
                v("3b one form in a Rule line", f"{p['id']}|rule voices", f"`{p['id']}` has two voices in a Rule line: the verb phrase "
                  + "; ".join(f"\"<subject> {x}\"" for x in p["vp_forms"]) + " and, through \"for <subject>, <claim>\", its Then form "
                  + "; ".join(f"\"{x}\"" for x in p["then_forms"]), owner=p["id"], forms=p["vp_forms"] + p["then_forms"])
            if p.get("subject_forms") and p.get("claim_forms") and voc.rule_prefixes:
                v("3b one form in a Rule line", f"{p['id']}|rule narrowing", f"`{p['id']}` can be written in two places of a Rule line: on the subject "
                  + "; ".join(f"\"{x}\"" for x in p["subject_forms"]) + " and, through \"for <subject>, <claim>\", before the claim "
                  + "; ".join(f"\"{x}\"" for x in p["claim_forms"]), owner=p["id"], forms=p["subject_forms"] + p["claim_forms"])
    # ---- 4 skeletons shared between different pieces
    groups = {}
    for f in forms:
        if f["kind"] != "grammar":
            groups.setdefault(skeleton(f["form"]), []).append(f)
    # A pair is exempt only if a separation of it is IN FORCE: its two sentences were compiled just now and each is read as
    # its own piece and not the other, and a sign-off of the entry is on record for exactly this text and these readings.
    signed = {}
    if voc.separations:
        from . import vreport
        from . import attest
        # (a separation names no Lean definition, so its digest needs none; records of other entries are not looked at here)
        recs = vreport.load_attestations(voc, {}) if records is None else records
    for s in voc.separations.values():
        st = separation_state(voc, s, forms)
        # IN FORCE needs a PERSON's review or approval of exactly this text and these readings (attest.person_review, fixed in
        # code): a model's record is kept and shown and exempts nothing.
        rec = attest.person_review(recs.of(s["id"], {"separation"}))
        why = list(st["why"])
        if st["ok"] and not rec:
            void = [r for r, _ in recs.void if r["subject"]["id"] == s["id"] and r["signer"]["kind"] == "person" and r["act"] in attest.REVIEW_ACTS]
            others = [r for r in recs.of(s["id"]) if r["signer"]["kind"] != "person"]
            if void:
                why.append(f"it was {void[0]['act']} by {void[0]['signer']['id']} on {void[0]['at'][:10]} and one of its two pieces, or what one of "
                           "its sentences compiles to, has changed since: that record is void")
            else:
                why.append(f"no person has reviewed or approved it (python3 -m clausal attest {s['id']} --act approved --as human:<id> --scope …)"
                           + (f"; on record, and not a person's: {'; '.join(attest.said(r) for r in others)}" if others else ""))
        if why:
            v("4 separation not in force", s["id"], f"separation `{s['id']}` of `{s['between'][0]}` and `{s['between'][1]}` ({voc.at(s['id'])}) "
              "exempts nothing: " + "; ".join(why), owner=s["id"])
        else:
            signed[frozenset(s["between"])] = {"id": s["id"], "signed_by": rec["signer"]["id"]}
    notes["cross_domain"], notes["signed"] = [], []
    # Two pieces of DIFFERENT systems are never both live in a scenario (its When names one system). In a Rule line with no
    # scenario beneath it they are, whenever the line's subject is a noun that names an operation of each system: the line is
    # then read in both. So a pair of two systems is left out only if the systems share no Rule subject noun.
    noun_of = {}
    for f in forms:
        if f["position"] == "Rule subject noun":
            noun_of.setdefault(f["form"], set()).add(f["domain"])
    def bridge(da, db):
        return sorted(n for n, ds in noun_of.items() if ds & da and ds & db)
    for sk, fs in sorted(groups.items()):
        owners = list(dict.fromkeys(f["owner"] for f in fs))
        if len(owners) < 2:
            continue
        meet, apart, across = [], [], {}
        for a in range(len(owners)):
            for b in range(a + 1, len(owners)):
                da = {f["domain"] for f in fs if f["owner"] == owners[a]}
                db = {f["domain"] for f in fs if f["owner"] == owners[b]}
                pair = (owners[a], owners[b])
                if "shared" in da | db or da & db:
                    meet.append(pair)
                elif bridge(da, db):
                    across[pair] = (sorted(da | db), bridge(da, db))
                else:
                    apart.append(pair)
        show = lambda pairs: [{"owner": f["owner"], "form": f["form"], "cat": f["cat"], "position": f["position"], "domain": f["domain"]}
                              for f in fs if any(f["owner"] in p for p in pairs)]
        unsigned = [p for p in meet if frozenset(p) not in signed]
        if len(unsigned) < len(meet):
            notes["signed"].append({"skeleton": sk, "pairs": [list(p) for p in meet if frozenset(p) in signed]})
        if unsigned:
            members = list(dict.fromkeys(o for p in unsigned for o in p))
            bare = sk == "{}"
            v("4 shared skeleton" + (" (no literal word: told apart by the type of the hole alone)" if bare else ""),
              f"{sk}|{','.join(sorted(members))}",
              f"{len(members)} pieces share the skeleton \"{sk}\" ({len(unsigned)} pairs, no separating pair signed): "
              + "; ".join(f"`{x['owner']}` \"{x['form']}\" ({x['cat']}, {x['position']})" for x in show(unsigned)),
              owners=members, pairs=len(unsigned), skeleton=sk)
        if across:
            members = list(dict.fromkeys(o for p in across for o in p))
            systems = sorted({d for ds, _ in across.values() for d in ds})
            nouns = sorted({n for _, ns in across.values() for n in ns})
            v("4 shared skeleton across systems", f"{sk}|{','.join(sorted(members))}",
              f"{len(members)} pieces of different systems ({', '.join(systems)}) share the skeleton \"{sk}\": "
              + "; ".join(f"`{x['owner']}` \"{x['form']}\" ({x['domain']}; {x['cat']}, {x['position']})" for x in show(list(across)))
              + (". A Rule line about it, with no scenario beneath it, is read in each system: whatever it claims, if each system can "
                 "make the claim the line is refused AMBIGUOUS, and every other skeleton the two systems share becomes live in one sentence. "
                 if all(x["position"] == "Rule subject noun" for x in show(list(across))) else
                 f". The systems share the Rule subject noun{'s' if len(nouns) > 1 else ''} {', '.join(chr(34) + n + chr(34) for n in nouns)}: a Rule line "
                 "about one, with no scenario beneath it, is read in each system, and no word of this form says which piece is meant. ")
              + "No separating pair can clear it (it is one sentence, not two); a noun only one system has would",
              owners=members, pairs=len(across), skeleton=sk, nouns=nouns)
        if apart:
            notes["cross_domain"].append({"skeleton": sk, "pairs": [list(p) for p in apart], "forms": show(apart)})
    # ---- 4, head collision: a Rule verb phrase that takes the head of another frame's verb phrase (Q8 control 1)
    for g, sp in head_collisions(forms):
        pair = frozenset((g["owner"], sp["owner"]))
        if pair in signed:
            notes["signed"].append({"skeleton": skeleton(sp["form"]), "pairs": [sorted(pair)]})
            continue
        v("4 head collision", f"{skeleton(sp['form'])}|{','.join(sorted(pair))}",
          f"the verb phrase \"{sp['form']}\" of `{sp['owner']}` takes the head of \"{g['form']}\" of `{g['owner']}` (it is an instance of that "
          "skeleton: a reader meets the same first words with another meaning), and no separating pair is signed",
          owners=sorted(pair), skeleton=skeleton(sp["form"]))
    # informational: a form that is an instance of another piece's skeleton ("takes another piece's head")
    sub = []
    pats = {}
    for f in forms:
        sk = skeleton(f["form"])
        if f["kind"] == "grammar" or not re.sub(r"[{}\s]", "", sk):
            continue
        pats[(f["owner"], f["form"])] = (f, sk, re.compile(r"\s+".join(".+" if w == "{}" else re.escape(w).replace(r"\{\}", ".+") for w in sk.split())))
    for (oa, fa), (a, ska, _) in pats.items():
        for (ob, fb), (b, skb, rb) in pats.items():
            if oa != ob and ska != skb and ("shared" in (a["domain"], b["domain"]) or a["domain"] == b["domain"]) \
                    and rb.fullmatch(ska.replace("{}", "X")):
                sub.append({"form": fa, "of": oa, "is_an_instance_of": fb, "of_piece": ob})
    notes["instance_of_another_skeleton"] = sub
    return V, notes


# ---------------------------------------------------------------------------------------------- 5: the same term

def compiled_terms(voc) -> dict:
    """Sentence id -> what it compiles to today, for every scenario and Rule line of features/ and controls/."""
    from .core import Problem, parse_feature
    comp = vocab.Compiler(voc)
    out = {}
    def rec(id_, source, r):
        if isinstance(r, Problem):
            out[id_] = {"source": source, "compiled": False, "status": r.status, "code": r.code}
        else:
            out[id_] = {"source": source, "compiled": True, "pieces": [i for i in r.used], "lean_sha256": __import__("hashlib").sha256(r.lean_def().encode()).hexdigest()}
    for d in ("features", "controls"):
        for path in sorted((ROOT / d).glob("*.feature")):
            f = parse_feature(path, f"{d}/{path.name}")
            rds = {sc.id: comp.scenario(sc) for sc in f.scenarios}
            for sc in f.scenarios:
                rec(sc.id, f"{d}/{path.name}:{sc.line}", rds[sc.id])
            for r in f.rules:
                hint = None if d == "controls" else next((rds[sc.id].info["ops"][0]["domain"] for sc in r.scenarios
                                                           if isinstance(rds.get(sc.id), vocab.Reading)), None)
                rec(r.id, f"{d}/{path.name}:{r.line}", comp.rule(r, hint))
    return out


def same_terms(voc) -> tuple:
    """(violations, {new, gone}, terms): today's terms against clausebook/terms.lock.json."""
    now = compiled_terms(voc)
    p = ROOT / vocab.BOOK_DIR / LOCK
    if not p.exists():
        return [{"check": "5 same term", "key": "no lock", "what": f"{vocab.BOOK_DIR}/{LOCK} does not exist (write it with --update-terms)"}], {"new": sorted(now), "gone": []}, now
    lock = json.loads(p.read_text())["sentences"]
    V = []
    for i, was in lock.items():
        same = lambda a, b: all(a.get(k) == b.get(k) for k in ("compiled", "status", "code", "lean_sha256"))     # `pieces` is for the message only
        if i in now and not same(now[i], was):
            what = (f"`{i}` ({now[i]['source']}) compiled, and is now refused ({now[i]['status']})" if was["compiled"] and not now[i]["compiled"] else
                    f"`{i}` ({now[i]['source']}) was refused ({was['status']}), and now compiles" if now[i]["compiled"] and not was["compiled"] else
                    f"`{i}` ({now[i]['source']}) compiles to another Lean term than the recorded one (pieces then: {was.get('pieces')}; now: {now[i].get('pieces')})"
                    if was["compiled"] else
                    f"`{i}` ({now[i]['source']}) was refused as {was['status']} ({was['code']}), and is now refused as {now[i]['status']} ({now[i]['code']})")
            V.append({"check": "5 same term", "key": i, "what": what})
    return V, {"new": sorted(set(now) - set(lock)), "gone": sorted(set(lock) - set(now))}, now


def cmd_check(argv) -> int:
    gloss = load_glossary(ROOT / "glossary.yaml", "glossary.yaml")
    voc = vocab.load_project(ROOT, gloss)
    core = core_alone(lean="--lean" in argv)
    V, notes = lint(voc)
    V5, drift, terms = same_terms(voc)
    # plan node W4: a word that rests on an assumption names an entry the ledger holds (and the ledger's conditions are Rules
    # that exist). A fault here is a fault of the book: FeatureError, the check fails.
    from . import ledger
    ledger.check(ledger.load(ROOT), voc, {i for i in terms if i.startswith("Rule.")})
    if "--update-terms" in argv:
        (ROOT / vocab.BOOK_DIR / LOCK).write_text(json.dumps({"what": "what every sentence of features/ and controls/ compiles to; written by `clausal book check --update-terms`",
                                                               "sentences": terms}, indent=1, sort_keys=True) + "\n")
        V5, drift = [], {"new": [], "gone": []}
    V += V5
    V.sort(key=lambda x: (x["check"], x["key"]))
    exp_path = ROOT / vocab.BOOK_DIR / EXPECTED
    if "--update-expected" in argv:
        by = {}
        for x in V:
            by[x["check"]] = by.get(x["check"], 0) + 1
        exp_path.write_text(json.dumps({"what": "the violations `python3 -m clausal book check` reports on the book as it stands, accepted as known debt "
                                                "(plan node Q3; cleared by Q4). The check passes iff it reports exactly these.",
                                        "counts": by, "violations": [{"check": x["check"], "key": x["key"], "what": x["what"]} for x in V]},
                                       indent=1, ensure_ascii=False) + "\n")
    expected = {(x["check"], x["key"]) for x in json.loads(exp_path.read_text())["violations"]} if exp_path.exists() else set()
    got = {(x["check"], x["key"]) for x in V}
    if "--json" in argv:
        print(json.dumps({"core": core, "violations": V, "notes": notes, "terms": drift,
                          "unexpected": sorted(got - expected), "cleared": sorted(expected - got)}, indent=1, ensure_ascii=False))
        return 0 if core["ok"] and got == expected else 1
    print("book check: core stands alone" if core["ok"] else "book check: CORE DOES NOT STAND ALONE")
    for l in core["lines"]:
        print("  " + l)
    for p in core["problems"]:
        print("  CORE IS NOT ALONE: " + p)
    n_forms = len(surface(voc))
    print(f"book check: registration lint over {n_forms} surface forms of {len(voc.books)} books: {len(V)} violations"
          + (" (listed below; --quiet for the counts only)" if V and "--quiet" not in argv else ""))
    counts = {}
    for x in V:
        counts[x["check"]] = counts.get(x["check"], 0) + 1
    for c in ("1 holes", "2 order", "3a one form per position", "3b one form in a Rule line", "4 shared skeleton",
              "4 shared skeleton (no literal word: told apart by the type of the hole alone)", "4 shared skeleton across systems", "4 head collision", "4 separation not in force", "5 same term"):
        print(f"  check {c}: {counts.get(c, 0)}")
        if "--quiet" not in argv:
            for x in V:
                if x["check"] == c:
                    print(f"    - {x['what']}" + ("" if (x["check"], x["key"]) in expected else "      <-- NOT EXPECTED"))
    print(f"  not counted: {len(notes['cross_domain'])} skeletons shared only between pieces of systems that share no Rule subject noun (no sentence is read in both): "
          + "; ".join(f"\"{n['skeleton']}\" ({', '.join(sorted({o for p in n['pairs'] for o in p}))})" for n in notes["cross_domain"]))
    print(f"  not counted: {len(notes['signed'])} skeletons with a signed separating pair; {len(notes['instance_of_another_skeleton'])} forms that are an "
          "instance of another piece's skeleton (informational, --json lists them)")
    print(f"  terms: {len(terms)} sentences of features/ and controls/ compiled or refused as recorded in {vocab.BOOK_DIR}/{LOCK}"
          + (f"; NOT in the lock (new): {len(drift['new'])}" if drift["new"] else "") + (f"; in the lock and gone: {len(drift['gone'])}" if drift["gone"] else "")
          if not V5 else f"  terms: {len(V5)} sentences do NOT compile to the recorded term")
    what = {(x["check"], x["key"]): x["what"] for x in V}
    for k in sorted(got - expected):
        print(f"  NOT EXPECTED: [{k[0]}] {what[k]}")
    for k in sorted(expected - got):
        print(f"  EXPECTED AND NO LONGER REPORTED (remove it from {vocab.BOOK_DIR}/{EXPECTED}): [{k[0]}] {k[1]}")
    ok = core["ok"] and got == expected
    print(f"book check: {'the violations are exactly the expected ones' if ok else 'FAILED'} ({len(expected)} expected, {vocab.BOOK_DIR}/{EXPECTED})")
    return 0 if ok else 1


def cmd_core(argv) -> int:
    r = core_alone(lean="--lean" in argv)
    for l in r["lines"]:
        print("  " + l)
    for p in r["problems"]:
        print("  CORE IS NOT ALONE: " + p)
    return 0 if r["ok"] else 1


def main(argv) -> int:
    if argv and argv[0] == "core":
        return cmd_core(argv[1:])
    if argv and argv[0] == "check":
        return cmd_check(argv[1:])
    print(__doc__)
    return 2
