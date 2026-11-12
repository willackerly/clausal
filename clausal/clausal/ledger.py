"""The assumption ledger (plan node W4). The format, the refusals and the flags are frozen in trust/FREEZE-w46.md, section 3.

An ENTRY of trust/assumptions.yaml states a fact that nothing in this pipeline checks and that a word of the Clausebook rests
on. The word points to it with `assumes: [<id>]` inside its own entry, so the pointer is under the word's digest. An entry
says what is assumed, whether the thing the word is bound to here is a stand-in, which Lean axioms a proof resting on it may
use, and its USAGE CONDITIONS: each an ordinary Rule of a feature file (named by id), or a sentence saying what cannot be
stated. Nothing about a condition's verdict is stored: `state` reads it from the verdicts of the run it is given.

    python3 -m clausal ledger            the entries, the words that rest on them, who has vouched (reads the tree only)
    python3 -m clausal ledger check      the same checks `clausal gen` and `clausal book check` make; exit 1 on a fault

WHO VOUCHES is an attestation record (clausal/attest.py) of act `vouched` in trust/assumptions.attest.json, whose subject is
the entry at its current digest. `vouch` returns a person's or an organisation's; whether a project ADMITS it is its trust
policy's business (clausal/trust.py). With none the entry is printed AWAITED.

This module reads no Lean and runs nothing.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

import yaml

from . import attest
from .core import FeatureError, sha

ROOT = Path(__file__).resolve().parent.parent
FILE = "trust/assumptions.yaml"
STORE = "trust/assumptions.attest.json"
KEYS = {"id", "statement", "class", "lean_axioms", "stand_in", "attached_to", "usage_conditions", "not_covered", "external_proof", "review_by"}
CLASSES = ("property", "opaque-function")
EXT_KEYS = {"pointer", "commit", "sha256", "theorem"}
STD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROVED = "PROVED-FOR-ALL"
UNSTATED = "CANNOT-BE-STATED"
# the flags of a Rule verdict that rests on an entry (trust/FREEZE-w46.md, section 3)
F_ASSUMES, F_AXIOM, F_NOT_MET, F_UNSTATED, F_NOT_VOUCHED = ("ASSUMES:", "ASSUMPTION-AXIOM-USED:", "ASSUMPTION-CONDITION-NOT-MET:",
                                                              "ASSUMPTION-CONDITION-UNSTATED:", "ASSUMPTION-NOT-VOUCHED:")


class Ledger:
    def __init__(self, entries: dict, rel: str = FILE):
        self.entries, self.rel = entries, rel

    def __contains__(self, id_):
        return id_ in self.entries

    def __iter__(self):
        return iter(self.entries.values())


def entry_problems(e, where: str) -> list:
    """Every reason one entry is not an entry of the frozen format. [] if it is one."""
    if not isinstance(e, dict):
        return [f"{where}: an entry is a mapping"]
    why = []
    if set(e) - KEYS:
        why.append(f"unknown key(s) {sorted(set(e) - KEYS)} (nothing is stored about who vouches or what a condition's verdict is)")
    if KEYS - set(e):
        why.append(f"missing key(s) {sorted(KEYS - set(e))}")
    if "id" in e and not (isinstance(e["id"], str) and re.fullmatch(r"[A-Za-z][\w.\-]*", e["id"])):
        why.append("`id` is a name (letters, digits, dots)")
    if "statement" in e and not (isinstance(e["statement"], str) and e["statement"].strip()):
        why.append("`statement` says what is assumed, in words: it may not be empty")
    if "class" in e and e["class"] not in CLASSES:
        why.append(f"`class` is one of {', '.join(CLASSES)}; got {e['class']!r}")
    ax = e.get("lean_axioms")
    if "lean_axioms" in e:
        if not (isinstance(ax, list) and all(isinstance(x, str) and x for x in ax)):
            why.append("`lean_axioms` is a list of Lean axiom names")
        elif set(ax) & STD_AXIOMS:
            why.append(f"`lean_axioms` lists {sorted(set(ax) & STD_AXIOMS)}: the standard three are always allowed and are no assumption of an entry")
    if "stand_in" in e and not isinstance(e["stand_in"], bool):
        why.append("`stand_in` is true or false")
    if "attached_to" in e and not (isinstance(e["attached_to"], list) and e["attached_to"] and all(isinstance(x, str) for x in e["attached_to"])):
        why.append("`attached_to` lists the Clausebook entries that say `assumes:` this id (at least one)")
    cs = e.get("usage_conditions")
    if "usage_conditions" in e:
        if not isinstance(cs, list):
            why.append("`usage_conditions` is a list")
        else:
            seen = set()
            for c in cs:
                if not isinstance(c, dict) or "id" not in c or "rule" not in c:
                    why.append(f"a usage condition has an `id` and a `rule` (a Rule id, or null with `unstated:`); got {c!r}")
                    continue
                if set(c) - {"id", "rule", "unstated"}:
                    why.append(f"usage condition {c['id']}: unknown key(s) {sorted(set(c) - {'id', 'rule', 'unstated'})} (a condition's verdict is read "
                               "from the run, never stored)")
                if c["id"] in seen:
                    why.append(f"usage condition {c['id']} is listed twice")
                seen.add(c["id"])
                if c["rule"] is None:
                    if not (isinstance(c.get("unstated"), str) and c["unstated"].strip()):
                        why.append(f"usage condition {c['id']}: `rule: null` needs `unstated:` saying what cannot be stated")
                elif not isinstance(c["rule"], str) or "unstated" in c:
                    why.append(f"usage condition {c['id']}: `rule` is a Rule id, or null with `unstated:` (not both)")
    if "not_covered" in e and not (isinstance(e["not_covered"], list) and all(isinstance(x, str) for x in e["not_covered"])):
        why.append("`not_covered` is a list of sentences")
    x = e.get("external_proof")
    if "external_proof" in e and x is not None:
        if not isinstance(x, dict) or set(x) != EXT_KEYS or not all(isinstance(v, str) and v for v in x.values()):
            why.append(f"`external_proof` is null or has exactly the fields {', '.join(sorted(EXT_KEYS))}, each a non-empty string")
        elif not re.fullmatch(r"[0-9a-f]{64}", x["sha256"]):
            why.append("`external_proof.sha256` is 64 lower-case hex digits")
    if "review_by" in e and not isinstance(e["review_by"], datetime.date):
        why.append(f"`review_by` is a date (YYYY-MM-DD); got {e['review_by']!r}")
    return [f"{where}: {w}" for w in why]


def parse(raw, rel: str = FILE) -> Ledger:
    if raw is None:
        return Ledger({}, rel)
    if not isinstance(raw, dict) or set(raw) != {"assumptions"} or not isinstance(raw["assumptions"], list):
        raise FeatureError(f"{rel}: the ledger is one key, `assumptions:`, with a list of entries")
    why, entries = [], {}
    for k, e in enumerate(raw["assumptions"]):
        where = f"{rel}, entry {k + 1}" + (f" ({e['id']})" if isinstance(e, dict) and isinstance(e.get("id"), str) else "")
        why += entry_problems(e, where)
        if isinstance(e, dict) and isinstance(e.get("id"), str):
            if e["id"] in entries:
                why.append(f"{where}: the id is used twice")
            entries[e["id"]] = e
    if why:
        raise FeatureError("the assumption ledger is refused:\n  " + "\n  ".join(why))
    return Ledger(entries, rel)


def load(root: Path = ROOT) -> Ledger:
    p = root / FILE
    if not p.exists():
        return Ledger({})
    try:
        return parse(yaml.safe_load(p.read_text()))
    except yaml.YAMLError as e:
        raise FeatureError(f"{FILE}: not YAML ({e})")


def assumes_of(voc, id_: str) -> list:
    e = voc.ops.get(id_) or voc.pieces.get(id_) or voc.idioms.get(id_) or {}
    a = e.get("assumes") or []
    if not (isinstance(a, list) and all(isinstance(x, str) for x in a)):
        raise FeatureError(f"{voc.book_of(id_).rel}: `{id_}`: `assumes:` is a list of ids of the assumption ledger ({FILE})")
    return a


def words(voc) -> dict:
    """Clausebook entry -> the ledger ids it names with `assumes:`."""
    out = {}
    for i in list(voc.ops) + list(voc.pieces) + list(voc.idioms):
        a = assumes_of(voc, i)
        if a:
            out[i] = a
    return out


def check(led: Ledger, voc, rule_ids) -> None:
    """The ledger against the Clausebook and the feature files: every `assumes:` names an entry the ledger holds, `attached_to`
    and `assumes:` say the same thing, every stated usage condition is a Rule that exists. FeatureError otherwise: `clausal gen`,
    `clausal book check` and `clausal report` stop."""
    why = []
    w = words(voc)
    for i, ids in w.items():
        for a in ids:
            if a not in led:
                why.append(f"{voc.book_of(i).rel}:{voc.line_of(i)}: `{i}` says `assumes: [{a}]`, and the ledger does not hold `{a}` ({led.rel}): "
                           "a word may not rest on an assumption that is written nowhere")
    for e in led:
        for i in e["attached_to"]:
            if e["id"] not in w.get(i, []):
                why.append(f"{led.rel}: `{e['id']}`: `attached_to` names `{i}`, "
                           + ("which is no operation, piece or idiom of the Clausebook" if i not in voc.home else "whose entry does not say `assumes: [" + e["id"] + "]`"))
        for i, ids in w.items():
            if e["id"] in ids and i not in e["attached_to"]:
                why.append(f"{led.rel}: `{e['id']}`: `{i}` says `assumes:` it, and `attached_to` does not list `{i}`")
        for c in e["usage_conditions"]:
            if c["rule"] is not None and rule_ids is not None and c["rule"] not in rule_ids:
                why.append(f"{led.rel}: `{e['id']}`, usage condition {c['id']}: `{c['rule']}` is not a Rule of any feature file")
    if why:
        raise FeatureError("the assumption ledger and the Clausebook disagree:\n  " + "\n  ".join(why))


def assumed_by(voc, used) -> list:
    """The ledger ids the entries of a reading rest on, in the order met."""
    return list(dict.fromkeys(a for i in used for a in assumes_of(voc, i)))


def word_of(voc, led_id: str, used) -> list:
    return [i for i in used if led_id in assumes_of(voc, i)]


def allowed_axioms(led: Ledger, ids) -> dict:
    """Lean axiom -> the entry that lists it, over the entries `ids`: what a proof resting on them may use beyond the standard three."""
    return {ax: i for i in ids if i in led for ax in led.entries[i]["lean_axioms"]}


def lock_terms(root: Path = ROOT) -> dict:
    p = root / "clausebook" / "terms.lock.json"
    return json.loads(p.read_text())["sentences"] if p.exists() else {}


def digest_text(e: dict, lock: dict) -> str:
    """What a vouch is a vouch OF: the statement, the class, the axioms, stand-in, the conditions (with what each stated one
    compiles to, from clausebook/terms.lock.json), what is not covered, the external proof and the review date."""
    conds = []
    for c in e["usage_conditions"]:
        if c["rule"] is None:
            conds.append(f"{c['id']} UNSTATED {c['unstated']}")
        else:
            t = lock.get(c["rule"], {})
            conds.append(f"{c['id']} {c['rule']} {t.get('lean_sha256') or t.get('status') or 'NOT-IN-LOCK'}")
    x = e["external_proof"]
    return "\n".join([e["id"], e["statement"], e["class"], "axioms " + " ".join(e["lean_axioms"]), f"stand_in {e['stand_in']}"] + conds
                     + ["not covered: " + n for n in e["not_covered"]]
                     + ["external " + (" ".join(f"{k}={x[k]}" for k in sorted(x)) if x else "none"), f"review_by {e['review_by']}"])


def digest(e: dict, lock: dict) -> dict:
    return {"alg": "sha256-text", "value": sha(digest_text(e, lock))}


def load_records(led: Ledger, root: Path = ROOT, today: datetime.date | None = None) -> attest.Records:
    """The records of trust/assumptions.attest.json, sorted. Void: the entry changed since; or a vouch made after, or read after,
    the entry's `review_by`."""
    lock = lock_terms(root)
    today = today or datetime.date.today()

    def current(r):
        s = r["subject"]
        if s["kind"] != "assumption":
            return None, f"a record about a {s['kind']} does not belong in the ledger's store"
        if s["id"] not in led:
            return None, f"`{s['id']}` is not an entry of {led.rel}"
        if s["book"] != led.rel:
            return None, f"the record says `{s['id']}` is an entry of {s['book']}, and it is in the store of {led.rel}"
        return digest(led.entries[s["id"]], lock), ""
    out = attest.sort_records(attest.read_store(root / STORE), STORE, current)
    live = []
    for r in out.valid:
        by = led.entries[r["subject"]["id"]]["review_by"]
        at = datetime.datetime.fromisoformat(r["at"]).date()
        if r["act"] == "vouched" and (today > by or at > by):
            out.void.append((r, f"{STORE}: the vouch of `{r['subject']['id']}` by {r['signer']['id']} ({r['at'][:10]}) is past the entry's review date {by}: the record is void"))
        else:
            live.append(r)
    out.valid = live
    return out


def vouch(recs: list):
    """The record that makes an entry VOUCHED: act vouched, by a person or an organisation. Fixed in code, like
    attest.person_review: a model's or a tool's record is never returned."""
    return next((r for r in recs if r["act"] == "vouched" and r["signer"]["kind"] in ("person", "organisation")), None)


def state(e: dict, codes: dict) -> dict:
    """The usage conditions of an entry against the verdict codes of ONE run (`codes`: Rule id -> code). Computed, never stored."""
    conds = []
    for c in e["usage_conditions"]:
        if c["rule"] is None:
            conds.append({"id": c["id"], "rule": None, "code": UNSTATED, "unstated": c["unstated"]})
        else:
            conds.append({"id": c["id"], "rule": c["rule"], "code": codes.get(c["rule"], "NO-VERDICT")})
    return {"conditions": conds, "proved": sum(c["code"] == PROVED for c in conds), "unstated": sum(c["code"] == UNSTATED for c in conds),
            "not_met": [c["id"] for c in conds if c["code"] not in (PROVED, UNSTATED)], "n": len(conds)}


def flags(e: dict, st: dict, vouched: bool, axioms_used=()) -> list:
    """The flags a Rule verdict resting on `e` carries (trust/FREEZE-w46.md section 3). No verdict code changes."""
    out = [F_ASSUMES + e["id"]]
    if set(axioms_used) & set(e["lean_axioms"]):
        out.append(F_AXIOM + e["id"])
    if st["not_met"]:
        out.append(F_NOT_MET + e["id"])
    if st["unstated"]:
        out.append(F_UNSTATED + e["id"])
    if not vouched:
        out.append(F_NOT_VOUCHED + e["id"])
    return out


def attest_entry(led: Ledger, which: str, act: str, signer: str, scope: str, on_behalf_of=None, name=None, at=None, context=None, root: Path = ROOT) -> int:
    """`clausal attest assumption:<id>`: one record about a ledger entry at its current digest."""
    if which not in led:
        raise FeatureError(f"`assumption:{which}`: the ledger ({led.rel}) holds no such entry")
    rec = attest.make("assumption", led.rel, which, digest(led.entries[which], lock_terms(root)), act, signer, scope, on_behalf_of, name, at, context)
    attest.add(root / STORE, rec)
    print(f"attested assumption {which} ({led.rel}): {attest.said(rec)}")
    return 0


def main(argv) -> int:
    from . import vocab
    from .core import load_glossary
    led = load()
    voc = vocab.load_project(ROOT, load_glossary(ROOT / "glossary.yaml", "glossary.yaml"))
    lock = lock_terms()
    check(led, voc, {i for i in lock if i.startswith("Rule.")} if lock else None)
    recs = load_records(led)
    w = words(voc)
    for e in led:
        v = vouch(recs.of(e["id"]))
        print(f"{e['id']}  [{e['class']}{'; STAND-IN' if e['stand_in'] else ''}]  {e['statement']}")
        print(f"    rests on it: {', '.join(i for i, ids in w.items() if e['id'] in ids)}")
        print(f"    vouched by: {attest.said(v) if v else 'nobody (AWAITED)'}")
        for r in recs.of(e["id"]):
            if r is not v:
                print(f"    on record, not a vouch by a person or an organisation: {attest.said(r)}")
        for c in e["usage_conditions"]:
            print(f"    {c['id']}  " + (f"{c['rule']} (verdict: read from a run, `clausal report`)" if c["rule"] else f"CANNOT BE STATED: {c['unstated']}"))
        print(f"    lean axioms a proof may use: {', '.join(e['lean_axioms']) or 'none'}; external proof: "
              + (f"{e['external_proof']['pointer']} (sha256 {e['external_proof']['sha256'][:12]}, not checked here)" if e["external_proof"] else "none")
              + f"; review by {e['review_by']}")
    for r, why in recs.void:
        print(f"VOID     {why}")
    for where, why, _ in recs.refused:
        print(f"REFUSED  {where}: " + "; ".join(why))
    print(f"assumption ledger: {len(led.entries)} entries, {sum(1 for e in led if vouch(recs.of(e['id'])))} vouched by a person or an organisation; "
          f"records: {len(recs.valid)} valid, {len(recs.void)} void, {len(recs.refused)} refused")
    return 1 if recs.refused else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
