"""The declared list of projects (plan node X7): clausal/projects.yaml.

A PROJECT is one Rust crate with the books it is read through, its feature files and its Lean modules. run.sh, translate.sh,
the generator, the report and the evidence step take the set of projects from this list; nothing else says which
crates there are. (Before X7 run.sh looped `for crate in wallet ledger` and named `Wallet.*` and `Ledger.*` modules.)

    python3 -m clausal projects              the list, as read
    python3 -m clausal projects crates       the crate directories, one line (run.sh step 1, translate.sh, workcopy.sh)
    python3 -m clausal projects lean-build   the Lean modules that must build in step 4 of run.sh, one line
    python3 -m clausal projects check        what the list says against the files (exit 1 if they disagree)

What is NOT per project (stated; see projects.yaml and DESIGN.md section 21): the books are loaded as ONE merged book in the
order of clausebook/project.yaml, the generated Lean of every project goes to lean/Wallet/{Statements,Checks,Readings,
Obligations}.lean, and the Rust readings of the pieces are in one file each. This module reads no Lean and runs nothing.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .core import FeatureError

ROOT = Path(__file__).resolve().parent.parent
FILE = "projects.yaml"
KEYS = {"name", "crate", "books", "features", "lean", "trust"}
LEAN_KEYS = {"model", "modules", "search_imports", "bridge", "hand_written"}


@dataclass
class Project:
    name: str
    crate: str                      # directory under clausal/ (= the cargo crate name)
    books: list                     # names relative to clausebook/, as clausebook/project.yaml writes them
    features: list                  # paths relative to clausal/
    model: str                      # the Lean module Aeneas writes for the crate (Generated.<Crate>)
    modules: list = field(default_factory=list)          # hand-written Lean modules that must build before any proof (step 4)
    search_imports: list = field(default_factory=list)   # modules the generated search scripts import beside the readings
    bridge_module: str | None = None                     # facts used only by generated glue proofs
    bridge_lemmas: list = field(default_factory=list)
    hand_written: list = field(default_factory=list)     # hand-written Lean files or directories (under clausal/), for the digest
    trust: str | None = None                             # the project's trust policy (path under clausal/; clausal/trust.py), or none

    @property
    def roots(self) -> list:
        """The Lean library roots the project's own modules live in (Generated excluded: it is shared)."""
        return list(dict.fromkeys(m.split(".")[0] for m in self.modules + self.search_imports
                                  + ([self.bridge_module] if self.bridge_module else [])))


@dataclass
class Projects:
    root: Path
    items: list
    lean_build: list                # shared Lean targets that must build in step 4 (models, frames, generated files)
    rust_side: list                 # crates that run the readings on the compiled Rust; each depends on every project crate

    def __iter__(self):
        return iter(self.items)

    @property
    def crates(self) -> list:
        return [p.crate for p in self.items]

    def lean_targets(self) -> list:
        """What `lake build` must build before any hand-written proof is looked at: the shared targets, then each project's."""
        return list(dict.fromkeys(self.lean_build + [m for p in self.items for m in p.modules]))

    def feature_paths(self) -> list:
        """Every feature file, in the order the pipeline reads them: the FIRST file of each project in project order, then
        the others by file name. (With the wallet and the ledger this is the order the pipeline had before the list.)"""
        first = [p.features[0] for p in self.items if p.features]
        rest = sorted((f for p in self.items for f in p.features[1:]), key=lambda f: Path(f).name)
        return first + rest

    def of_feature(self, rel: str) -> Project | None:
        return next((p for p in self.items if rel in p.features), None)

    def of_crate(self, crate: str) -> Project | None:
        return next((p for p in self.items if p.crate == crate), None)

    def search_imports(self) -> list:
        return list(dict.fromkeys(m for p in self.items for m in p.search_imports))

    def bridge_modules(self) -> list:
        return list(dict.fromkeys(p.bridge_module for p in self.items if p.bridge_module))

    def bridge_lemmas(self) -> list:
        return [l for p in self.items for l in p.bridge_lemmas]

    def digest_files(self) -> list:
        """The hand-written files of every project a run depends on: the crate source, then the Lean files."""
        out = [self.root / p.crate / "src" / "lib.rs" for p in self.items]
        for p in self.items:
            for h in p.hand_written:
                q = self.root / h
                out += sorted(q.rglob("*.lean")) if q.is_dir() else [q]
        return out


def load(root: Path = ROOT) -> Projects:
    path = root / FILE
    raw = yaml.safe_load(path.read_text()) or {}
    ws = raw.get("workspace") or {}
    items, seen = [], set()
    for k, d in enumerate(raw.get("projects") or []):
        where = f"{FILE}: project {k + 1}"
        if not isinstance(d, dict) or not isinstance(d.get("name"), str):
            raise FeatureError(f"{where}: every project has a `name`")
        where = f"{FILE}: project `{d['name']}`"
        if set(d) - KEYS:
            raise FeatureError(f"{where}: unknown key(s) {sorted(set(d) - KEYS)}")
        for key in ("crate", "books", "features", "lean"):
            if not d.get(key):
                raise FeatureError(f"{where}: `{key}` is missing")
        lean = d["lean"]
        if set(lean) - LEAN_KEYS:
            raise FeatureError(f"{where}: unknown key(s) under `lean` {sorted(set(lean) - LEAN_KEYS)}")
        if not lean.get("model"):
            raise FeatureError(f"{where}: `lean.model` is missing (the module Aeneas writes for the crate)")
        if d["name"] in seen:
            raise FeatureError(f"{where}: named twice")
        seen.add(d["name"])
        br = lean.get("bridge") or {}
        items.append(Project(d["name"], d["crate"], list(d["books"]), list(d["features"]), lean["model"],
                             list(lean.get("modules") or []), list(lean.get("search_imports") or []),
                             br.get("module"), list(br.get("lemmas") or []), list(lean.get("hand_written") or []), d.get("trust")))
    if not items:
        raise FeatureError(f"{FILE}: no project is declared")
    return Projects(root, items, list(ws.get("lean_build") or []), list(ws.get("rust_side") or []))


# --------------------------------------------------------------------------- the list against the files

def check(pr: Projects) -> list:
    """Problems: where projects.yaml and the files disagree. Static: no Lean, no cargo, no run."""
    import tomllib
    from . import vocab
    root, bad = pr.root, []
    # ---- feature files: each one belongs to exactly one project
    on_disk = sorted(f"features/{p.name}" for p in (root / "features").glob("*.feature"))
    owner = {}
    for p in pr:
        for f in p.features:
            if f in owner:
                bad.append(f"{f} is listed by two projects, `{owner[f]}` and `{p.name}`")
            owner[f] = p.name
            if not (root / f).is_file():
                bad.append(f"project `{p.name}`: {f} does not exist")
    bad += [f"{f} is listed by no project of {FILE}: it would not be read" for f in on_disk if f not in owner]
    # ---- crates
    crates = {}
    for p in pr:
        if p.crate in crates:
            bad.append(f"crate `{p.crate}` is named by two projects, `{crates[p.crate]}` and `{p.name}`")
        crates[p.crate] = p.name
        if not (root / p.crate / "Cargo.toml").is_file() or not (root / p.crate / "src" / "lib.rs").is_file():
            bad.append(f"project `{p.name}`: {p.crate}/Cargo.toml or {p.crate}/src/lib.rs does not exist")
            continue
        got = tomllib.loads((root / p.crate / "Cargo.toml").read_text()).get("package", {}).get("name")
        if got != p.crate:
            bad.append(f"project `{p.name}`: {p.crate}/Cargo.toml names the package `{got}`; the directory and the crate must have one name "
                       "(translate.sh writes lean/Generated/<Crate>.lean from it)")
        if p.model != "Generated." + p.crate[:1].upper() + p.crate[1:]:
            bad.append(f"project `{p.name}`: `lean.model: {p.model}` is not the module Aeneas writes for crate `{p.crate}` "
                       f"(Generated.{p.crate[:1].upper() + p.crate[1:]})")
    for side in pr.rust_side:
        man = root / side / "Cargo.toml"
        if not man.is_file():
            bad.append(f"workspace.rust_side: {side}/Cargo.toml does not exist")
            continue
        deps = tomllib.loads(man.read_text()).get("dependencies", {})
        for p in pr:
            # Only that the dependency is there, by path. WHICH directory the path names is not checked here on purpose:
            # a Rust side built against other source than the translated crate is what the generated property tests
            # report as MODEL MISMATCH (mutation control c38 points the path at a changed copy and expects that).
            d = deps.get(p.crate)
            if not isinstance(d, dict) or not d.get("path"):
                bad.append(f"{side}/Cargo.toml does not depend on the crate of project `{p.name}` by path "
                           f"({p.crate} = {{ path = ... }}): its rules could not be run on the compiled Rust")
    # ---- books: every project's books are loaded, in the load order, and are closed under `needs:`
    loaded = [rel for _, rel in vocab.project_books(root)]
    short = [r.split("/", 1)[1] for r in loaded]
    used = set()
    names = {}
    for path, rel in vocab.project_books(root):
        names[rel.split("/", 1)[1]] = yaml.safe_load(path.read_text()) or {}
    by_name = {str(v.get("book") or Path(k).stem): k for k, v in names.items()}
    for p in pr:
        for b in p.books:
            if b not in short:
                bad.append(f"project `{p.name}`: book {b} is not in the load order of {vocab.BOOK_DIR}/{vocab.PROJECT_FILE}")
        have = [b for b in p.books if b in short]
        if have != [b for b in short if b in have]:
            bad.append(f"project `{p.name}`: its books are not in the load order of {vocab.BOOK_DIR}/{vocab.PROJECT_FILE} ({', '.join(short)})")
        for b in have:
            for need in names[b].get("needs", []):
                if by_name.get(need) not in have[:have.index(b)]:
                    bad.append(f"project `{p.name}`: book {b} needs the book `{need}`, which the project does not list before it")
        used |= set(have)
    bad += [f"{vocab.BOOK_DIR}/{b} is loaded ({vocab.BOOK_DIR}/{vocab.PROJECT_FILE}) and no project of {FILE} lists it" for b in short if b not in used]
    # ---- Lean: every module named has a file, and its library root is a library of the lakefile
    lake = tomllib.loads((root / "lean" / "lakefile.toml").read_text())
    libs = {l.get("name") for l in lake.get("lean_lib", [])}
    for p in pr:
        for m in p.modules + p.search_imports + ([p.bridge_module] if p.bridge_module else []):
            if not (root / "lean").joinpath(*m.split(".")).with_suffix(".lean").is_file():
                bad.append(f"project `{p.name}`: Lean module {m} has no file (lean/{m.replace('.', '/')}.lean)")
            if m.split(".")[0] not in libs:
                bad.append(f"project `{p.name}`: Lean module {m} is in no library of lean/lakefile.toml (no [[lean_lib]] named {m.split('.')[0]})")
        for h in p.hand_written:
            if not (root / h).exists():
                bad.append(f"project `{p.name}`: hand_written {h} does not exist")
    for t in pr.lean_build:
        if t.split(".")[0] not in libs:
            bad.append(f"workspace.lean_build: {t} is in no library of lean/lakefile.toml")
    return bad


def check_trust(pr: Projects) -> list:
    """Each `trust:` names a policy file that loads, is for that project, and names only books the project lists (plan node W3)."""
    from . import trust
    bad = []
    for p in pr:
        if not p.trust:
            continue
        try:
            pol = trust.load_policy(pr.root / p.trust, p.trust)
        except FeatureError as e:
            bad.append(str(e))
            continue
        if pol.project != p.name:
            bad.append(f"{p.trust}: the policy is for project `{pol.project}`, and {FILE} names it for `{p.name}`")
        for name, q in pol.requirements.items():
            for b in (q.get("books") or []):
                if b not in p.books:
                    bad.append(f"{p.trust}: requirement `{name}` covers the book {b}, which project `{p.name}` does not list")
    return bad


def check_translation(pr: Projects, translation: dict) -> list:
    """After translate.sh: lean/translation.json holds exactly the declared crates."""
    got = list(translation.get("crates", []))
    if sorted(got) != sorted(pr.crates):
        return [f"lean/translation.json holds the crates {got}; {FILE} declares {pr.crates} (run ./translate.sh)"]
    return []


def book_use(pr: Projects, voc, readings) -> list:
    """Every sentence of a project is read through the books THAT PROJECT lists: [(project, reading id, entry id, book)] for
    each entry a compiled reading uses whose book the reading's project does not list. `readings`: [(feature path, Reading)]."""
    out = []
    for path, rd in readings:
        p = pr.of_feature(path)
        if p is None:
            continue
        mine = {f"{BOOK_PREFIX}{b}" for b in p.books}
        for i in dict.fromkeys(list(rd.used) + list(rd.defaults)):
            b = voc.home.get(i)
            if b is not None and b.rel not in mine:
                out.append((p.name, rd.id, i, b.rel))
    return out


def books_of(pr: Projects, feature_path: str):
    """The books (as `Book.rel`) of the project that lists the feature file, or None if no project does. Given to
    `Compiler.rule(..., books=)` so that a refusal names the operations of the sentence's own project."""
    p = pr.of_feature(feature_path)
    return None if p is None else {f"{BOOK_PREFIX}{b}" for b in p.books}


BOOK_PREFIX = "clausebook/"


def summary(pr: Projects) -> list:
    L = []
    for p in pr:
        L.append(f"project {p.name}")
        L.append(f"  crate     {p.crate}/  (model: lean/{p.model.replace('.', '/')}.lean)")
        L.append(f"  books     {', '.join(p.books)}")
        L.append(f"  features  {', '.join(p.features)}")
        L.append(f"  trust     {p.trust or 'no policy named: strict mode uses the built-in one (every entry reviewed or approved by a person)'}")
        L.append(f"  lean      {', '.join(p.modules) or '-'}"
                 + (f"; search scripts import {', '.join(p.search_imports)}" if p.search_imports else "")
                 + (f"; glue lemmas {', '.join(p.bridge_lemmas)} ({p.bridge_module})" if p.bridge_module else ""))
    L.append(f"shared Lean targets: {', '.join(pr.lean_build)}")
    L.append(f"Rust-side crates (each depends on every project crate): {', '.join(pr.rust_side)}")
    return L


def main(argv) -> int:
    pr = load()
    cmd = argv[0] if argv else "show"
    if cmd == "crates":
        print(" ".join(pr.crates))
        return 0
    if cmd == "lean-build":
        print(" ".join(pr.lean_targets()))
        return 0
    if cmd == "features":
        print(" ".join(pr.feature_paths()))
        return 0
    if cmd == "check":
        bad = check(pr) + check_trust(pr)
        for b in bad:
            print(f"projects: {b}", file=sys.stderr)
        print(f"projects: {len(pr.items)} declared ({', '.join(p.name for p in pr)}); "
              + ("the list agrees with the files" if not bad else f"{len(bad)} PROBLEM(S)"))
        return 1 if bad else 0
    if cmd == "show":
        print("\n".join(summary(pr)))
        return 0
    print("usage: python3 -m clausal projects [show|crates|lean-build|features|check]", file=sys.stderr)
    return 2
