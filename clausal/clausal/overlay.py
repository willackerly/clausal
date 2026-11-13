"""clausal overlay: projects of the LOCAL OVERLAY (plan node T9.7a): clausal/projects.local.yaml, untracked.

A project whose crate is not in the tracked repository (the TDFLite decision core lives in a local, unpublished
repository) cannot be an entry of projects.yaml: `./run.sh` would not be reproducible from a clean checkout. Such a
project is declared in `projects.local.yaml`, which git ignores, and is run by this module and by nothing else:

    python3 -m clausal overlay                 the overlay as read, or "no overlay"
    python3 -m clausal overlay gen  [name]     compile the feature files; write the project's own Lean workspace
    python3 -m clausal overlay run  [name]     gen, then build, link, audit; print the verdict of every sentence;
                                               exit 1 if a verdict differs from the project's `expected` file
    python3 -m clausal overlay run [name] --record FILE    also write the verdict table to FILE (.json and .md)
    python3 -m clausal overlay lint [name]     the registration lint of `book check` over the project's own merged book

ISOLATION. Nothing here is read by `clausal gen`, `clausal report`, `clausal book check` or `projects check`, and
nothing here writes a tracked file (except with --record). An overlay project has

  * its own merged book: the books it lists (core, its packs, its local book) and no other project's;
  * its own actor and literal types (`types:`), in the format of glossary.yaml; the shared glossary.yaml is not read;
  * its own Lean workspace, build/overlay/<name>/lean (git-ignored): the frame library and lean/Bdd/{Ops,Audit,
    AuditLinks}.lean by symbolic link, the sources the overlay names by symbolic link, and the generated files
    `Local/Readings.lean`, `Local/Obligations.lean`, `Run/Links.lean`. Its lakefile and manifest are written here
    from lean/lakefile.toml and lean/lake-manifest.json (same pins, same package cache; `lake update` is never run).

So `./run.sh` with no overlay does exactly what it did, and with an overlay its eight steps and their outputs are
the same too: the overlay is one more step after the report (run.sh, step "overlay").

WHAT AN OVERLAY PROJECT GETS, AND DOES NOT. Per Rule line and per scenario:

  compiled      `vocab.Compiler` on its own book: a reading, or a refusal (UNBOUND, ...)
  obligation    the flat proof obligation `oblig.py` generates from the pieces
  linked        `<id>.reading_iff_obligation`, the generated script of `oblig.iff_theorem`, kernel-checked; the audit
                (lean/Bdd/AuditLinks.lean) checks its type and that it uses a proof of neither side
  proved        a hand-written theorem `<id>` of type exactly `<id>.obligation` in `<proofs>.<name of the item>`,
                standard axioms only; the constants of `through:` roots it reaches are listed (the theorems of another
                development the proof goes through)
  not vacuous   for a reading with a scope ("for which", Givens): a hand-written theorem `<id>.sat` of type exactly
                `<id>.in_scope` (some state and input are in scope)
  refuted       a hand-written theorem `<id>.refuted : ¬ <id>.obligation`; the script derives `¬ reading`
  linked to     (fix round of T9.7a; optional, the project's `links:` file, e.g. tdf/links.yaml) a LINK says that some sentences,
  another       together, say exactly what some statements of another development say:
  development       Link.<name>.claim := (obligation ∧ ...) ↔ (<statement>.stmt ∧ ...)        generated, Local/Links.lean
                a person proves it (`<links>.<name>`); it is counted only with the exact type, standard axioms, and a proof
                that reaches no proof of either side and no theorem of the `through:` roots outside the link's `given`.
                A sentence of a link is proved FROM the link and the statements' theorems (`<id>.from_link`, generated); if
                the link is not counted its verdict is UNLINKED. A sentence in no link is one-way: a hand-written proof of
                the obligation, counted only if it reaches every theorem its expected `through` lists.

  narrowing     the check of clausal/narrowing.py on its own readings (what its books declare narrowing settles is
                kernel-checked, what they do not declare is attempted and must fail; printed coverage against the
                Calls value); a failure stops the run

It does NOT get: translation by run.sh (the model is the file the overlay names), the crate's unit tests, the
reading search on a grid (no counterexample is searched for: a refutation is at an input a person named), the
Rust side (cucumber, generated property tests, bounded checks), the adequacy note, mutation, a place in
out/report.md or out/graph.json. Its verdict codes are the report's where the
evidence is the same (PROVED-FOR-ALL, PROVED-INSTANCE, REFUTED, UNBOUND, UNLINKED) and STATED-ONLY otherwise
(compiled and linked; no proof, no test).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml

from . import oblig, vocab
from .core import FeatureError, Problem, load_glossary, parse_feature

ROOT = Path(__file__).resolve().parent.parent
FILE = "projects.local.yaml"
KEYS = {"name", "crate", "books", "features", "types", "expected", "links", "lean"}
LEAN_KEYS = {"model", "sources", "proofs", "links", "through"}
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SHARED = ["Frames", "Bdd/Ops.lean", "Bdd/Audit.lean", "Bdd/AuditLinks.lean", "Bdd/NarrowingAudit.lean"]     # of clausal/lean, linked into every workspace
HEADER = "-- GENERATED by `clausal overlay` from the feature files and the books of an overlay project. Do not edit.\n"


def load(root: Path = ROOT) -> list:
    """The overlay projects, or [] if there is no overlay file."""
    # $CLAUSAL_OVERLAY names another overlay file (tdf/check_controls.py runs seeded copies of a project this way)
    path = Path(os.environ["CLAUSAL_OVERLAY"]) if os.environ.get("CLAUSAL_OVERLAY") else root / FILE
    if not path.exists():
        return []
    raw = yaml.safe_load(path.read_text()) or {}
    out, seen = [], set()
    for k, d in enumerate(raw.get("projects") or []):
        where = f"{FILE}: project {k + 1}"
        if not isinstance(d, dict) or not isinstance(d.get("name"), str):
            raise FeatureError(f"{where}: every project has a `name`")
        where = f"{FILE}: project `{d['name']}`"
        if set(d) - KEYS:
            raise FeatureError(f"{where}: unknown key(s) {sorted(set(d) - KEYS)}")
        for key in ("books", "features", "types", "lean"):
            if not d.get(key):
                raise FeatureError(f"{where}: `{key}` is missing")
        if set(d["lean"]) - LEAN_KEYS:
            raise FeatureError(f"{where}: unknown key(s) under `lean` {sorted(set(d['lean']) - LEAN_KEYS)}")
        if d["name"] in seen:
            raise FeatureError(f"{where}: named twice")
        seen.add(d["name"])
        out.append(d)
    return out


def check(root: Path, d: dict) -> list:
    """Problems of one overlay project against the files. Static."""
    bad = []
    tracked = set()
    try:
        from . import projects
        tracked = {p.name for p in projects.load(root)}
        for p in projects.load(root):
            for f in d["features"]:
                if f in p.features:
                    bad.append(f"{f} is a feature file of the tracked project `{p.name}`")
    except FeatureError:
        pass
    if d["name"] in tracked:
        bad.append(f"`{d['name']}` is the name of a project of projects.yaml")
    for f in d["features"]:
        if not (root / f).is_file():
            bad.append(f"{f} does not exist")
        elif (root / f).parent == root / "features":
            bad.append(f"{f} is under features/, which holds the feature files of the tracked projects (projects check would stop ./run.sh)")
    for b in d["books"]:
        if not (root / vocab.BOOK_DIR / b).is_file():
            bad.append(f"book {vocab.BOOK_DIR}/{b} does not exist")
    for key in ("types", "expected", "links"):
        if d.get(key) and not (root / d[key]).is_file():
            bad.append(f"`{key}`: {d[key]} does not exist")
    for name, src in (d["lean"].get("sources") or {}).items():
        if not source_path(root, src).exists():
            bad.append(f"lean.sources: `{name}`: {src} does not exist")
    return bad


def source_path(root: Path, src: str) -> Path:
    p = Path(os.path.expanduser(src))
    return p if p.is_absolute() else root / p


# --------------------------------------------------------------------------- compiling

class Item:
    def __init__(self, kind, id_, source, text, expect, result):
        self.kind, self.id, self.source, self.text, self.expect, self.result = kind, id_, source, text, expect, result

    @property
    def tail(self) -> str:
        return self.id.rsplit(".", 1)[1]


def compile_project(root: Path, d: dict) -> tuple:
    gl = load_glossary(root / d["types"], d["types"])
    voc = vocab.Vocabulary([(root / vocab.BOOK_DIR / b, f"{vocab.BOOK_DIR}/{b}") for b in d["books"]], gl)
    comp = vocab.Compiler(voc)
    books = {f"{vocab.BOOK_DIR}/{b}" for b in d["books"]}
    items, seen = [], {}
    for rel in d["features"]:
        f = parse_feature(root / rel, rel)
        under = set()
        for r in f.rules:
            sc_rds = {sc.id: comp.scenario(sc) for sc in r.scenarios}
            hint = next((x.info["ops"][0]["domain"] for x in sc_rds.values() if isinstance(x, vocab.Reading)), None)
            exp = next((t[len("@expect-"):].upper() for t in r.tags if t.startswith("@expect-")), None)
            items.append(Item("rule", r.id, f"{rel}:{r.line}", f"Rule: {r.name}", exp, comp.rule(r, hint, books)))
            for sc in r.scenarios:
                under.add(sc.id)
                items.append(Item("scenario", sc.id, f"{rel}:{sc.line}", sc.text, sc.expect, sc_rds[sc.id]))
        for sc in f.scenarios:
            if sc.id not in under:
                items.append(Item("scenario", sc.id, f"{rel}:{sc.line}", sc.text, sc.expect, comp.scenario(sc)))
    for x in items:
        if x.id in seen:
            raise FeatureError(f"{x.source}: duplicate id {x.id} (also {seen[x.id]})")
        seen[x.id] = x.source
    return voc, items


# --------------------------------------------------------------------------- links to the statements of another development

LINK_KEYS = {"name", "sentences", "statements", "given", "negated"}


def load_links(root: Path, d: dict) -> dict:
    """The project's `links:` file (tdf/links.yaml describes the format and what a link claims), or no links."""
    if not d.get("links"):
        return {"links": []}
    raw = yaml.safe_load((root / d["links"]).read_text()) or {}
    seen, used = set(), {}
    for l in raw.get("links") or []:
        where = f"{d['links']}: link `{l.get('name')}`"
        if set(l) - LINK_KEYS or not l.get("name") or not l.get("sentences") or not l.get("statements"):
            raise FeatureError(f"{where}: a link has `name`, `sentences`, `statements`, and may have `given`, `negated`")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", l["name"]) or l["name"] in seen:
            raise FeatureError(f"{where}: the name is not an identifier, or is used twice")
        seen.add(l["name"])
        l.setdefault("given", [])
        l.setdefault("negated", False)
        if l["negated"] and len(l["sentences"]) != 1:
            raise FeatureError(f"{where}: a negated link has one sentence")
        if set(l["given"]) & set(l["statements"]):
            raise FeatureError(f"{where}: a statement of the link is among its `given`")
        for sid in l["sentences"]:
            if sid in used:
                raise FeatureError(f"{where}: {sid} is also a sentence of the link `{used[sid]}` (one link per sentence)")
            used[sid] = l["name"]
    raw["links"] = raw.get("links") or []
    return raw


def conj(parts: list) -> str:
    return " ∧ ".join(f"({p})" if " " in p else p for p in parts)


def proj(k: int, n: int) -> str:
    """The k-th of n conjuncts of a right-nested conjunction, as projections."""
    if n == 1:
        return ""
    return ".2" * k + (".1" if k < n - 1 else "")


def links_file(links: dict, items: list) -> tuple:
    """Local/Links.lean: the CLAIM of every link, over the flat obligations and over the compiled readings. (text, usable):
    a link one of whose sentences does not compile has no claim."""
    by_id = {x.id: x.result for x in items}
    L, usable = [], {}
    for l in links["links"]:
        rds = [by_id.get(sid) for sid in l["sentences"]]
        if not all(isinstance(r, vocab.Reading) for r in rds):
            usable[l["name"]] = "a sentence of the link does not compile: " + ", ".join(s for s, r in zip(l["sentences"], rds) if not isinstance(r, vocab.Reading))
            continue
        rhs = conj([s + ".stmt" for s in l["statements"]])
        neg = "¬ " if l["negated"] else ""
        for suffix, names in (("claim", [r.id + ".obligation" for r in rds]), ("readings_claim", [r.name for r in rds])):
            L.append(f"/-- Link `{l['name']}`: " + ("the sentence is false exactly when the statement holds" if l["negated"] else "the sentences together say exactly what the statements say")
                     + (" (over the flat obligations; proved by hand)" if suffix == "claim" else " (over the compiled readings; derived by the run)") + ". -/\n"
                     f"def Link.{l['name']}.{suffix} : Prop :=\n  ({neg}({conj(names)})) ↔ ({rhs})\n")
        usable[l["name"]] = None
    text = (HEADER + "-- THE CLAIM of every link of the project's `links:` file. A person proves `theorem Link.<name> : Link.<name>.claim`.\n"
            + "import Local.Obligations\nimport Local.Readings\n" + (f"import {links['statements_import']}\n" if links["links"] else "")
            + "open Aeneas Aeneas.Std Result\nset_option linter.unusedVariables false\n\n" + "\n".join(L))
    return text, usable


def link_module(d: dict, name: str) -> str | None:
    root = d["lean"].get("links")
    return f"{root}.{name}" if root else None


# --------------------------------------------------------------------------- the workspace

def workspace(root: Path, d: dict) -> Path:
    return root / "build" / "overlay" / d["name"] / "lean"


def link(dst: Path, src: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_symlink() or dst.exists():
        if dst.is_symlink() and Path(os.readlink(dst)) == src:
            return
        if dst.is_symlink() or dst.is_file():
            dst.unlink()
        else:
            raise FeatureError(f"{dst} exists and is not a symbolic link: remove it")
    dst.symlink_to(src)


def lib_of(name: str) -> tuple:
    """`Generated/TdfCore.lean` -> (Generated, glob); `IdSpec.lean` -> (IdSpec, single module); `T93` -> (T93, glob)."""
    head = name.split("/")[0]
    if head.endswith(".lean"):
        return head[:-5], False
    return head, True


def write_workspace(root: Path, d: dict, voc, items) -> Path:
    ws = workspace(root, d)
    (ws / "Local").mkdir(parents=True, exist_ok=True)
    (ws / "Run").mkdir(exist_ok=True)
    lean = root / "lean"
    for s in SHARED:
        link(ws / s, (lean / s).resolve())
    libs = {"Frames": True, "Bdd": True, "Local": True}
    for name, src in (d["lean"].get("sources") or {}).items():
        link(ws / name, source_path(root, src).resolve())
        lib, glob = lib_of(name)
        libs[lib] = libs.get(lib, False) or glob
    # the same pins as clausal/lean: its toolchain file, its manifest with the project name and the path of the Aeneas
    # library changed, its package cache by symbolic link. `lake update` is never run.
    (ws / "lean-toolchain").write_text((lean / "lean-toolchain").read_text())
    base = tomllib.loads((lean / "lakefile.toml").read_text())
    aeneas = next(r for r in base["require"] if r["name"] == "aeneas")
    apath = (lean / aeneas["path"]).resolve()
    L = [f"# GENERATED by `clausal overlay` (clausal/clausal/overlay.py) for the overlay project `{d['name']}`. Do not edit.",
         f'name = "overlay_{d["name"]}"', 'defaultTargets = ["Local"]', "", "[[require]]", 'name = "aeneas"', f'path = "{apath}"']
    for lib, glob in libs.items():
        L += ["", "[[lean_lib]]", f'name = "{lib}"'] + ([f'globs = ["{lib}.+"]'] if glob else [])
    (ws / "lakefile.toml").write_text("\n".join(L) + "\n")
    man = json.loads((lean / "lake-manifest.json").read_text())
    man["name"] = f"overlay_{d['name']}"
    for p in man["packages"]:
        if p.get("name") == "aeneas":
            p["dir"] = str(apath)
    (ws / "lake-manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    link(ws / ".lake" / "packages", (lean / ".lake" / "packages").resolve())
    rds = [x.result for x in items if isinstance(x.result, vocab.Reading)]
    (ws / "Local" / "Readings.lean").write_text(vocab.readings_file(voc, rds).replace(vocab.HEADER, HEADER))
    scopes = []
    for rd in rds:
        u = oblig.units(rd)[0]
        if u.hyps:
            binders = rd.outer + [("st", rd.state_type), ("inp", rd.input_type)]
            scopes.append(f"/-- The reading of {rd.id} is not vacuous: some state and input are in its scope. -/\n"
                          f"def {rd.id}.in_scope : Prop :=\n  ∃ {vocab.group(binders)}, ({u.op}).scope st inp\n")
    (ws / "Local" / "Obligations.lean").write_text(
        oblig.obligations_file(voc, rds).replace(oblig.emit.HEADER, HEADER)
        + "\n-- NON-VACUITY: the statement that the scope of a reading with a scope is met somewhere (proved by hand, `<id>.sat`).\n"
        + "\n".join(scopes))
    text, usable = links_file(load_links(root, d), items)
    (ws / "Local" / "Links.lean").write_text(text)
    return ws


def proof_module(d: dict, x: Item) -> str | None:
    root = d["lean"].get("proofs")
    return f"{root}.{x.tail}" if root else None


def proof_file(ws: Path, d: dict, x: Item) -> Path | None:
    m = proof_module(d, x)
    return ws.joinpath(*m.split(".")).with_suffix(".lean") if m else None


def has(path: Path, pattern: str) -> bool:
    return bool(re.search(pattern, path.read_text()))


def links_script(ws: Path, d: dict, voc, items, built: set, links: dict | None = None, usable: dict | None = None) -> tuple:
    """Run/Links.lean of the workspace: reading ↔ obligation for every compiled sentence; the reading itself from a
    supplied proof; ¬ reading from a supplied refutation; the audit. (text, meta)"""
    meta = {"oiffs": [], "holds": [], "oproofs": [], "nots": [], "sats": [], "ofail": {}, "through": {}, "links": {}, "stmts": []}
    body, imports = [], []
    roots = list(d["lean"].get("through") or [])
    links, usable = links or {"links": []}, usable or {}
    of_link = {sid: (l, k) for l in links["links"] for k, sid in enumerate(l["sentences"])}
    have_link = set()         # links whose hand-written theorem is there to be audited
    for l in links["links"]:
        mod = link_module(d, l["name"])
        if usable.get(l["name"]) is None and mod in built:
            imports.append(mod)
            have_link.add(l["name"])
    if links["links"]:
        imports.append(links["proofs_import"])
    for x in items:
        rd = x.result
        if not isinstance(rd, vocab.Reading):
            continue
        body.append(f"-- ===== {rd.id}")
        try:
            body.append(oblig.iff_theorem(rd))
        except KeyError as e:
            meta["ofail"][rd.id] = str(e)
            body.append(f"-- no obligation: {e}\n")
            continue
        meta["oiffs"].append([rd.id + ".reading_iff_obligation", rd.name, rd.id + ".obligation"])
        pf, mod = proof_file(ws, d, x), proof_module(d, x)
        l, k = of_link.get(rd.id, (None, 0))
        if l and not l["negated"] and l["name"] in have_link:
            # A SENTENCE OF A LINK: its obligation is what the link gives from the theorems of the linked statements
            n = l["name"]
            body.append(f"/-- The obligation, from the link `{n}` and the theorems of its statements. -/\n"
                        f"theorem {rd.id}.from_link : {rd.id}.obligation := by\n  have h : Link.{n}.claim := Link.{n}\n  unfold Link.{n}.claim at h\n"
                        f"  exact (h.mpr {l['statements'][0] if len(l['statements']) == 1 else '⟨' + ', '.join(l['statements']) + '⟩'}){proj(k, len(l['sentences']))}\n"
                        f"/-- The reading holds: through the link `{n}`. -/\n"
                        f"theorem {rd.id}.proved : {rd.name} := {rd.id}.reading_iff_obligation.mpr {rd.id}.from_link\n")
            meta["holds"].append([rd.id + ".proved", rd.name])
            meta["oproofs"].append([rd.id + ".from_link", rd.id + ".obligation"])
        if pf is None or not pf.exists() or mod not in built:
            continue
        imports.append(mod)
        e = re.escape(rd.id)
        if has(pf, rf"theorem\s+{e}\s*:\s*{e}\.obligation\b") and not (l and not l["negated"]):
            body.append(f"/-- The reading holds: the supplied proof of its flat obligation ({mod}), through the equivalence. -/\n"
                        f"theorem {rd.id}.proved : {rd.name} := {rd.id}.reading_iff_obligation.mpr {rd.id}\n")
            meta["holds"].append([rd.id + ".proved", rd.name])
            meta["oproofs"].append([rd.id, rd.id + ".obligation"])
        if has(pf, rf"theorem\s+{e}\.refuted\s*:\s*¬\s*{e}\.obligation\b"):
            body.append(f"/-- The reading is FALSE: the supplied refutation of its flat obligation ({mod}), through the equivalence. -/\n"
                        f"theorem {rd.id}.reading_refuted : ¬ {rd.name} := fun h => {rd.id}.refuted ({rd.id}.reading_iff_obligation.mp h)\n")
            meta["nots"].append([rd.id + ".reading_refuted", rd.name])
        if has(pf, rf"theorem\s+{e}\.sat\s*:\s*{e}\.in_scope\b"):
            meta["sats"].append([rd.id + ".sat", rd.id + ".in_scope"])
    # THE LINKS: the claim over the readings, from the hand-written claim over the obligations and the generated
    # equivalences reading ↔ obligation; the statements' theorems, each of type exactly its statement
    ok_iffs = {a for a, _, _ in meta["oiffs"]}
    for l in links["links"]:
        n = l["name"]
        if n not in have_link:
            continue
        ids = l["sentences"]
        if not all(i + ".reading_iff_obligation" in ok_iffs for i in ids):
            continue
        cong = ids[-1] + ".reading_iff_obligation"
        for i in reversed(ids[:-1]):
            cong = f"and_congr {i}.reading_iff_obligation ({cong})"
        if l["negated"]:
            cong = f"not_congr ({cong})"
        body.append(f"-- ===== link {n}\n/-- The link `{n}`, over the compiled readings. -/\n"
                    f"theorem Link.{n}.readings : Link.{n}.readings_claim := by\n  have h : Link.{n}.claim := Link.{n}\n"
                    f"  unfold Link.{n}.claim at h\n  unfold Link.{n}.readings_claim\n  exact Iff.trans ({cong}) h\n")
        meta["links"][n] = {"claim": [f"Link.{n}", f"Link.{n}.claim"], "readings": [f"Link.{n}.readings", f"Link.{n}.readings_claim"]}
    meta["stmts"] = [[s, s + ".stmt"] for s in dict.fromkeys(s for l in links["links"] for s in l["statements"])]
    names = lambda xs: "#[" + ", ".join("`" + n for n in xs) + "]"
    watched = [a for a, _ in meta["oproofs"]] + [a for a, _ in meta["nots"]] + [f"Link.{n}" for n in meta["links"]]
    lproofs = [p for v in meta["links"].values() for p in (v["claim"], v["readings"])] + meta["stmts"]
    # per link: the constants its hand-written proof may not reach (a proof of one of its sentences)
    sides = {n: [x for i in next(l for l in links["links"] if l["name"] == n)["sentences"] for x in (i, i + ".from_link", i + ".proved", i + ".refuted", i + ".reading_refuted")]
             for n in meta["links"]}
    side_types = {n: [i + ".obligation" for i in next(l for l in links["links"] if l["name"] == n)["sentences"]]
                     + [nm for i in next(l for l in links["links"] if l["name"] == n)["sentences"] for nm in [next(x.result.name for x in items if x.id == i)]]
                     + [s + ".stmt" for s in next(l for l in links["links"] if l["name"] == n)["statements"]]
                  for n in meta["links"]}
    text = (HEADER + "-- Run with `lake env lean Run/Links.lean` in this workspace.\n"
            + "".join(f"import {m}\n" for m in dict.fromkeys(imports))
            + "import Local.Obligations\nimport Local.Readings\nimport Bdd.AuditLinks\n"
            "open Aeneas Aeneas.Std Result Lean\n"
            "set_option linter.unusedTactic false\nset_option linter.unreachableTactic false\n"
            "set_option linter.unusedSimpArgs false\nset_option linter.unusedVariables false\n"
            "set_option maxHeartbeats 200000\n\n"
            + "\n".join(body)
            + "\n#eval Bdd.Audit.reportLinks\n"
            "  (iffs := #[" + ", ".join(f"(`{a}, `{b}, `{c})" for a, b, c in meta["oiffs"]) + "])\n"
            "  (imps := #[])\n"
            "  (nots := #[" + ", ".join(f"(`{a}, `{b})" for a, b in meta["nots"]) + "])\n"
            "  (proofs := #[" + ", ".join(f"(`{a}, `{b})" for a, b in meta["holds"] + meta["oproofs"] + meta["sats"] + lproofs) + "])\n"
            "  (locals := #[])\n  (consts := #[])\n\n"
            # which theorems of the `through:` roots each supplied proof reaches: everything the proof term uses, entered
            # through every constant that is not of Lean's core, Mathlib or the Aeneas library
            "def throughRoots : Array Name := " + names(roots) + "\n"
            "def ownRoots : Array Name := " + names(sorted({m.split(".")[0] for m in imports} | {"Local"})) + "\n"
            "partial def reachThrough (env : Environment) (root : Name) : NameSet := Id.run do\n"
            "  let mut seen : NameSet := {}\n  let mut hit : NameSet := {}\n  let mut todo : Array Name := #[root]\n"
            "  while !todo.isEmpty do\n    let n := todo.back!\n    todo := todo.pop\n    if seen.contains n then continue\n"
            "    seen := seen.insert n\n"
            "    let m := Bdd.Audit.moduleOf env n\n"
            "    let r := match m with | some m => m.getRoot | none => `_script\n"
            "    if throughRoots.contains r then\n"
            "      match env.find? n with\n      | some (.thmInfo _) => hit := hit.insert n\n      | _ => pure ()\n"
            "    else if m.isNone || ownRoots.contains r then\n"
            "      if let some ci := env.find? n then\n        for u in Bdd.Audit.usedBy ci do\n          if !seen.contains u then todo := todo.push u\n"
            "  return hit\n"
            "#eval show CoreM Unit from do\n  let env ← getEnv\n"
            "  let mut out : Array (String × Json) := #[]\n"
            "  for t in " + names(watched) + " do\n"
            "    out := out.push (t.toString, Bdd.Audit.names ((reachThrough env t).toArray.qsort (fun a b => a.toString < b.toString)))\n"
            "  IO.println s!\"THROUGH\\t{(Json.mkObj out.toList).compress}\"\n"
            # DOES THE PROOF OF A LINK USE A PROOF OF ONE OF ITS SIDES? Everything the proof term reaches through constants that
            # are not of Lean's core, Mathlib or the Aeneas library (the values of theorems entered; a theorem of a `through`
            # root is recorded and not entered): a constant that is a proof of a sentence of the link by name, or any theorem
            # whose type is exactly an obligation or a reading of the link, a statement of the link, or the conjunction side.
            "partial def reachAll (env : Environment) (root : Name) : NameSet := Id.run do\n"
            "  let mut seen : NameSet := {}\n  let mut todo : Array Name := #[root]\n"
            "  while !todo.isEmpty do\n    let n := todo.back!\n    todo := todo.pop\n    if seen.contains n then continue\n"
            "    seen := seen.insert n\n"
            "    let m := Bdd.Audit.moduleOf env n\n"
            "    let r := match m with | some m => m.getRoot | none => `_script\n"
            "    if !throughRoots.contains r && (m.isNone || ownRoots.contains r) then\n"
            "      if let some ci := env.find? n then\n        for u in Bdd.Audit.usedBy ci do\n          if !seen.contains u then todo := todo.push u\n"
            "  return seen\n"
            "def usesSide (env : Environment) (t : Name) (byName byType : Array Name) : Array Name :=\n"
            "  ((reachAll env t).erase t).toArray.filter fun n =>\n"
            "    byName.contains n || match env.find? n with\n"
            "      | some (.thmInfo ci) => byType.any fun a => ci.type == mkConst a\n      | _ => false\n"
            "#eval show CoreM Unit from do\n  let env ← getEnv\n"
            "  let mut out : Array (String × Json) := #[]\n"
            + "".join(f"  out := out.push (\"{n}\", Bdd.Audit.names (usesSide env `Link.{n} {names(sides[n])} {names(side_types[n])}))\n" for n in meta["links"])
            + "  IO.println s!\"LINKUSE\\t{(Json.mkObj out.toList).compress}\"\n")
    return text, meta


# --------------------------------------------------------------------------- running

def lake(ws: Path, args: list, log: Path) -> int:
    env = dict(os.environ, PATH=f"{Path.home()}/.elan/bin:{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""))
    with log.open("w") as f:
        return subprocess.run(["lake"] + args, cwd=ws, stdout=f, stderr=subprocess.STDOUT, env=env).returncode


def failed_modules(log: str) -> set:
    return set(re.findall(r"^- (\S+)$", log, re.M)) | set(re.findall(r"^✖ \[\d+/\d+\] \w+ (\S+)", log, re.M))


def run_project(root: Path, d: dict, quiet: bool = False) -> dict:
    voc, items = compile_project(root, d)
    ws = write_workspace(root, d, voc, items)
    out = ws.parent / "out"
    out.mkdir(exist_ok=True)
    say = (lambda *a: None) if quiet else print
    say(f"overlay `{d['name']}`: {sum(isinstance(x.result, vocab.Reading) for x in items)} of {len(items)} sentences compiled; workspace {ws.relative_to(root)}")
    links = load_links(root, d)
    _, usable = links_file(links, items)
    rc = lake(ws, ["build", "Local.Readings", "Local.Obligations", "Local.Links", "Bdd.AuditLinks", "Bdd.NarrowingAudit"], out / "build.log")
    if rc != 0:
        raise FeatureError(f"overlay `{d['name']}`: the compiled readings or their obligations do not build (a fault of the books or of the "
                           f"generator, never a verdict): {out / 'build.log'}\n" + (out / "build.log").read_text()[-3000:])
    mods = {proof_module(d, x): x for x in items
            if isinstance(x.result, vocab.Reading) and proof_file(ws, d, x) is not None and proof_file(ws, d, x).exists()}
    for l in links["links"]:          # the hand-written proof of each link's claim
        m = link_module(d, l["name"])
        if m and usable.get(l["name"]) is None and ws.joinpath(*m.split(".")).with_suffix(".lean").exists():
            mods[m] = l
    built, errors = set(mods), {}
    if mods:
        rc = lake(ws, ["build"] + sorted(mods), out / "proofs.log")
        log = (out / "proofs.log").read_text()
        if rc != 0:
            named = failed_modules(log)
            bad = {m for m in mods if m in named} or set(mods)       # cannot say where: count no proof at all
            for m in mods:           # a proof module that imports a broken one is lost with it
                src = ws.joinpath(*m.split(".")).with_suffix(".lean")
                if m not in bad and any(dep in named for dep in re.findall(r"^import (\S+)$", src.read_text(), re.M)):
                    bad.add(m)
            built -= bad
            for m in bad:
                hit = re.search(rf"^error: {re.escape('/'.join(m.split('.')) + '.lean')}:(\d+):\d+: (.*)$", log, re.M)
                errors[m] = f"line {hit.group(1)}: {hit.group(2)[:200]}" if hit else "see proofs.log"
        nsorry = len(re.findall(r"declaration uses .sorry.", log))
        say(f"  proof modules: {len(built)} compiled, {len(mods) - len(built)} FAILED; declarations using sorry: {nsorry}")
    # NARROWED CLAIMS (plan nodes Q1, Q2; clausal/narrowing.py, the generator and the reader of the tracked run): Lean is
    # asked to prove what the project's books declare narrowing settles for each operation and to fail on what they do not
    # declare, and which calls each claim of each reading is about. A wrong answer is a fault of the book: the run stops.
    from . import narrowing
    rds = [x.result for x in items if isinstance(x.result, vocab.Reading)]
    ntext, nside = narrowing.script(voc, rds, [])
    (ws / "Run" / "Narrowing.lean").write_text(ntext.replace(vocab.HEADER, HEADER))
    lake(ws, ["env", "lean", "Run/Narrowing.lean"], out / "narrowing.log")          # failing scripts are expected in it
    nres = narrowing.collect(nside, (out / "narrowing.log").read_text())
    (out / "narrowing.json").write_text(json.dumps(nres, indent=1, ensure_ascii=False))
    c = nres["counts"]
    say(f"  narrowing: {c['facts_declared']} declared facts about what narrowing settles kernel-checked, {c['facts_not_declared']} undeclared ones "
        f"attempted and not provable; Calls value reported for {c['calls_reported']} of {c['claims']} claims, printed coverage differs in "
        f"{c['coverage_mismatches']}" if nres["ok"] else f"  narrowing: {len(nres['problems'])} PROBLEM(S)")
    if not nres["ok"]:
        raise FeatureError(f"overlay `{d['name']}`: the narrowing check failed ({out / 'narrowing.json'}):\n  " + "\n  ".join(nres["problems"]))
    text, meta = links_script(ws, d, voc, items, built, links, usable)
    (ws / "Run" / "Links.lean").write_text(text)
    lake(ws, ["env", "lean", "Run/Links.lean"], out / "links.log")
    log = (out / "links.log").read_text()
    m1, m2 = re.search(r"^LINKS\t(.*)$", log, re.M), re.search(r"^THROUGH\t(.*)$", log, re.M)
    if not m1:
        raise FeatureError(f"overlay `{d['name']}`: the link audit produced no result: {out / 'links.log'}\n" + log[-3000:])
    th = json.loads(m1.group(1))["theorems"]
    through = json.loads(m2.group(1)) if m2 else {}
    m3 = re.search(r"^LINKUSE\t(.*)$", log, re.M)
    linkuse = json.loads(m3.group(1)) if m3 else {}

    def good(name, iff=False) -> tuple:
        t = th.get(name)
        if not t or not t["exists"]:
            return False, "no such theorem"
        if not t["type_ok"]:
            return False, "its type is not exactly the expected one"
        extra = sorted(set(t["axioms"]) - STANDARD_AXIOMS)
        if extra:
            return False, f"axioms beyond the standard three: {', '.join(extra)}"
        if iff and t.get("uses_proof"):
            return False, "the equivalence uses a proof of one of its sides"
        return True, ""

    # THE LINKS: is each counted? (name -> {"ok", "why", "through"})
    lres = {}
    for l in links["links"]:
        n, mod = l["name"], link_module(d, l["name"])
        r = {"name": n, "sentences": l["sentences"], "statements": l["statements"], "negated": l["negated"], "given_allowed": l["given"], "module": mod}
        why = usable.get(n)
        if why is None and n not in meta["links"]:
            why = (errors.get(mod) and f"{mod} does not compile ({errors[mod]})") or \
                  (mod not in built and f"no proof of the claim (`theorem Link.{n} : Link.{n}.claim` in {mod})") or \
                  "a sentence of the link is not kernel-linked to its obligation"
        if why is None:
            for name, what in ([(f"Link.{n}", "the claim")] + [(s, f"the theorem of the statement {s}.stmt") for s in l["statements"]] + [(f"Link.{n}.readings", "the claim over the readings")]):
                ok, w = good(name)
                if not ok:
                    why = f"{what}: {w}"
                    break
        if why is None:
            r["through"] = through.get(f"Link.{n}", [])
            if n not in linkuse:
                why = "the audit of what the proof uses produced no result"
            elif linkuse[n]:
                why = "the proof of the equivalence uses a proof of one of its sides: " + ", ".join(linkuse[n])
            elif set(r["through"]) & set(l["statements"]):
                why = "the proof of the equivalence uses the theorem of one of its statements: " + ", ".join(sorted(set(r["through"]) & set(l["statements"])))
            elif set(r["through"]) - set(l["given"]):
                why = "the proof of the equivalence uses a theorem that is not among the link's `given`: " + ", ".join(sorted(set(r["through"]) - set(l["given"])))
        r.update({"ok": why is None, "why": why})
        lres[n] = r
    of_link = {sid: l["name"] for l in links["links"] for sid in l["sentences"]}

    expected = json.loads((root / d["expected"]).read_text())["items"] if d.get("expected") else {}
    rows = []
    for x in items:
        rd = x.result
        row = {"id": x.id, "kind": x.kind, "source": x.source, "text": x.text.splitlines()[0].strip() if x.kind == "rule" else x.text,
               "expected": (expected.get(x.id) or {}).get("code")}
        if isinstance(rd, Problem):
            row.update({"code": rd.status, "compiled": False, "why": rd.message, "missing": (expected.get(x.id) or {}).get("missing")})
            rows.append(row)
            continue
        row.update({"compiled": True, "reading": rd.lean_def(), "pieces": rd.used, "echo": [list(e) for e in rd.echo]})
        mod = proof_module(d, x)
        scoped = bool(oblig.units(rd)[0].hyps)
        ok_iff, why_iff = good(rd.id + ".reading_iff_obligation", iff=True)
        ok_not, _ = good(rd.id + ".reading_refuted")
        ok_pf, why_pf = good(rd.id + ".proved")
        ln = of_link.get(rd.id)
        lk = lres.get(ln)
        ok_ob, why_ob = good(rd.id + ".from_link" if lk and not lk["negated"] else rd.id)
        row["link"] = ln
        row["t93"] = ({"relation": "false exactly when" if lk["negated"] else "equivalent", "link": ln, "with": [s for s in lk["sentences"] if s != rd.id],
                       "statements": lk["statements"], "given": lk.get("through", []), "counted": lk["ok"]} if lk else
                      {"relation": "one-way"})
        ok_sat, why_sat = good(rd.id + ".sat") if scoped else (True, "")
        row["linked"] = ok_iff
        row["scope"] = "narrowed by a condition" if scoped else "every call"
        if not ok_iff:
            row.update({"code": "UNLINKED", "why": f"reading ↔ obligation: {meta['ofail'].get(rd.id) or why_iff}"})
        elif lk and not lk["ok"]:
            row.update({"code": "UNLINKED", "why": f"the link `{ln}` to {', '.join(s + '.stmt' for s in lk['statements'])} is not counted: {lk['why']}"})
        elif ok_not:
            row.update({"code": "REFUTED", "theorem": rd.id + ".reading_refuted", "module": mod, "axioms": th[rd.id + ".reading_refuted"]["axioms"],
                        "through": through.get(rd.id + ".reading_refuted", []), "at": (expected.get(x.id) or {}).get("at")})
        elif ok_pf and ok_ob and ok_sat:
            universal = x.kind == "rule" or "Scenario Outline" in x.text
            row.update({"code": "PROVED-FOR-ALL" if universal else "PROVED-INSTANCE", "theorem": rd.id + ".proved", "module": lk["module"] if lk else mod,
                        "axioms": th[rd.id + ".proved"]["axioms"], "through": through.get(rd.id + ".from_link" if lk else rd.id, []),
                        "sat": (rd.id + ".sat") if scoped else None})
        else:
            why = (errors.get(mod) and f"{mod} does not compile ({errors[mod]})") or \
                  (not (ok_pf and ok_ob) and f"no counted proof of the obligation ({why_ob or why_pf})") or \
                  f"proved, but its scope is not shown to be met (`{rd.id}.sat`: {why_sat})"
            row.update({"code": "STATED-ONLY", "why": why})
        want = (expected.get(x.id) or {}).get("through")
        if want is not None and "through" in row:
            row["through_expected_not_reached"] = sorted(set(want) - set(row["through"]))
            if row["through_expected_not_reached"] and row["code"] in ("PROVED-FOR-ALL", "PROVED-INSTANCE"):
                # a PROVED verdict is "from the theorems of T9.3" (the codes of the expected file): a proof that does not reach
                # them is not that verdict. A refutation is at a named input whatever it rests on: there the list is reported.
                row.update({"was": row["code"], "code": "STATED-ONLY",
                            "why": f"there is a counted proof, but it does not reach "
                                   f"{', '.join(row['through_expected_not_reached'])} (expected `through`); it reaches {', '.join(row['through']) or 'no theorem of the named roots'}"})
        rows.append(row)
    res = {"project": d["name"], "books": d["books"], "features": d["features"], "rows": rows, "narrowing": nres["counts"],
           "links": list(lres.values()),
           "counts": {c: sum(r["code"] == c for r in rows) for c in dict.fromkeys(r["code"] for r in rows)},
           "differ": [r["id"] for r in rows if r["expected"] != r["code"] or (r.get("compiled") and (expected.get(r["id"]) or {}).get("link") != r.get("link"))],
           "not_expected": sorted(set(expected) - {r["id"] for r in rows})}
    (out / "verdicts.json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    return res


def table(res: dict) -> str:
    L = [f"# Verdicts of the overlay project `{res['project']}`", "",
         f"Written by `python3 -m clausal overlay run {res['project']} --record <file>` (clausal/clausal/overlay.py). "
         f"Books: {', '.join(res['books'])}. Feature files: {', '.join(res['features'])}.", "",
         "| Id | Sentence | Verdict | Expected | Relation to the linked statements | Evidence |", "|---|---|---|---|---|---|"]
    for r in res["rows"]:
        if r["code"] in ("PROVED-FOR-ALL", "PROVED-INSTANCE"):
            ev = f"`{r['theorem']}`, in `{r['module']}`; through {', '.join('`' + t + '`' for t in r['through']) or 'nothing of the named roots'}" \
                 + (f"; scope met: `{r['sat']}`" if r.get("sat") else "")
        elif r["code"] == "REFUTED":
            ev = f"`{r['theorem']}`, from `{r['module']}`" + (f"; at {', '.join('`' + a + '`' for a in r['at'])}" if r.get("at") else "") \
                 + f"; through {', '.join('`' + t + '`' for t in r['through']) or 'nothing of the named roots'}" \
                 + (f"; listed as expected and NOT reached: {', '.join('`' + t + '`' for t in r['through_expected_not_reached'])}" if r.get("through_expected_not_reached") else "")
        elif not r["compiled"]:
            ev = "not a composition of today's pieces" + (f". Missing: {r['missing']}" if r.get("missing") else "")
        else:
            ev = r.get("why", "")
        text = r["text"] if r["kind"] == "rule" else "Scenario: " + " / ".join(l.strip() for l in r["text"].splitlines()[1:])
        t = r.get("t93")
        if not r["compiled"]:
            rel = "–"
        elif t and t.get("link"):
            rel = (f"{'FALSE EXACTLY WHEN' if t['relation'] != 'equivalent' else 'EQUIVALENT'}"
                   + (f", with {', '.join('`' + s.rsplit('.', 1)[1] + '`' for s in t['with'])}," if t["with"] else "")
                   + f" {'' if t['relation'] != 'equivalent' else 'to '}{' ∧ '.join('`' + s + '.stmt`' for s in t['statements'])} (link `{t['link']}`"
                   + (f"; given {', '.join('`' + g + '`' for g in t['given'])}" if t["given"] else "; given nothing") + ")"
                   + ("" if t["counted"] else " NOT COUNTED"))
        elif r["code"] in ("PROVED-FOR-ALL", "STATED-ONLY"):
            rel = "one-way: follows from the theorems under Evidence; not shown to say as much as any statement"
        else:
            rel = "at the named input only"
        L.append(f"| `{r['id'].split('.', 1)[1]}` | {text.replace('|', '/')} | {r['code']} | {r['expected'] or '(none)'} | {rel} | {ev.replace('|', '/')} |")
    if res.get("links"):
        L += ["", "## Links", "", "| Link | Claim | Counted | Its proof leans on (`given`) | Allowed |", "|---|---|---|---|---|"]
        for l in res["links"]:
            lhs = " ∧ ".join("`" + s.rsplit(".", 1)[1] + "`" for s in l["sentences"])
            L.append(f"| `{l['name']}` | {'¬ ' if l['negated'] else ''}({lhs}) ↔ {' ∧ '.join('`' + s + '.stmt`' for s in l['statements'])} | "
                     f"{'yes: `Link.' + l['name'] + '` in `' + str(l['module']) + '`' if l['ok'] else 'NO: ' + str(l['why']).replace('|', '/')} | "
                     f"{', '.join('`' + g + '`' for g in l.get('through', [])) or 'nothing'} | {', '.join('`' + g + '`' for g in l['given_allowed']) or 'nothing'} |")
    L += ["", "Counts: " + ", ".join(f"{n} {c}" for c, n in res["counts"].items()) + f"; {len(res['differ'])} differ from the expected verdict."]
    return "\n".join(L) + "\n"


def lint_project(root: Path, d: dict) -> dict:
    """The registration lint of `clausal book check` (clausal/book.py) over THIS project's merged book. The violations
    that name an entry of a book other than core are the project's own; the rest are core's recorded debt."""
    from . import book
    voc, _ = compile_project(root, d)
    vs, _ = book.lint(voc)
    own_ids = [i for i in list(voc.ops) + list(voc.pieces) + [x["id"] for x in voc.raw["idioms"]]
               if voc.book_of(i).rel != f"{vocab.BOOK_DIR}/core.yaml"]
    own = [v for v in vs if any(re.search(rf"`{re.escape(i)}`", v["what"]) for i in own_ids)]
    return {"forms": len(book.surface(voc)), "violations": len(vs), "own": own, "own_entries": len(own_ids)}


def main(argv) -> int:
    root = ROOT
    ds = load(root)
    cmd = argv[0] if argv else "show"
    rest = [a for a in argv[1:] if not a.startswith("--")]
    record = argv[argv.index("--record") + 1] if "--record" in argv else None
    if record in rest:
        rest.remove(record)
    if not ds:
        print(f"overlay: no {FILE}; nothing to do")
        return 0
    if rest:
        ds = [d for d in ds if d["name"] in rest]
        if not ds:
            print(f"overlay: no project named {rest} in {FILE}", file=sys.stderr)
            return 2
    status = 0
    for d in ds:
        bad = check(root, d)
        if bad:
            for b in bad:
                print(f"overlay `{d['name']}`: {b}", file=sys.stderr)
            status = 1
            continue
        if cmd == "show":
            print(f"overlay `{d['name']}`: books {', '.join(d['books'])}; features {', '.join(d['features'])}; "
                  f"model {d['lean'].get('model')}; crate {d.get('crate', '(not named)')}")
        elif cmd == "gen":
            voc, items = compile_project(root, d)
            ws = write_workspace(root, d, voc, items)
            for x in items:
                r = x.result
                print(f"  {'compiled' if isinstance(r, vocab.Reading) else r.status:<10}{x.id}" + ("" if isinstance(r, vocab.Reading) else f"\n            {r.message[:300]}"))
            print(f"overlay `{d['name']}`: workspace written to {ws.relative_to(root)}")
        elif cmd == "run":
            res = run_project(root, d)
            for r in res["rows"]:
                mark = " " if r["expected"] == r["code"] else "!"
                print(f" {mark} {r['code']:<16}{r['id']}" + (f"   [expected {r['expected']}]" if mark == "!" else "")
                      + (f"\n                    {r['why'][:260]}" if r.get("why") and r["code"] in ("STATED-ONLY", "UNLINKED") else "")
                      + (f"\n                    note: `through` lists {', '.join(r['through_expected_not_reached'])}, which the refutation does not reach"
                         if r["code"] == "REFUTED" and r.get("through_expected_not_reached") else ""))
            for l in res.get("links", []):
                print(f"   link {l['name']:<11}" + ("counted" if l["ok"] else f"NOT COUNTED: {l['why']}")
                      + f"   ({'¬ ' if l['negated'] else ''}{len(l['sentences'])} sentence(s) ↔ {', '.join(l['statements'])}; leans on {', '.join(l.get('through', [])) or 'nothing'})")
            print(f"overlay `{d['name']}`: " + ", ".join(f"{n} {c}" for c, n in res["counts"].items())
                  + f"; {len(res['differ'])} differ from {d.get('expected', 'no expected file')}"
                  + (f"; expected and not in the feature files: {res['not_expected']}" if res["not_expected"] else ""))
            if res["differ"] or res["not_expected"]:
                status = 1
            if record:
                base = root / record
                base.with_suffix(".json").write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
                base.with_suffix(".md").write_text(table(res))
                print(f"  recorded: {base.with_suffix('.json').relative_to(root)}, {base.with_suffix('.md').relative_to(root)}")
        elif cmd == "lint":
            r = lint_project(root, d)
            print(f"overlay `{d['name']}`: {r['forms']} surface forms in its merged book; the registration lint reports {r['violations']} violations, "
                  f"{len(r['own'])} of which name one of the {r['own_entries']} entries of its own books (the others are core's)")
            for v in r["own"]:
                print(f"  {v['check']}: {v['what']}")
        else:
            print("usage: python3 -m clausal overlay [show|gen|run|lint] [name] [--record FILE]", file=sys.stderr)
            return 2
    return status
