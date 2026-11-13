"""Attestation records (plan nodes W0, W1): who says what about which entry. The format is frozen in trust/FREEZE.md.

A record names a SUBJECT by its digest, an ACT, a SIGNER with a KIND, an optional delegation, a time and a scope:

    {"subject": {"kind": "piece", "book": "core.yaml", "id": "always", "digest": {"alg": "sha256-text", "value": "…"}},
     "act": "reviewed", "signer": {"kind": "model", "id": "model:…"}, "on_behalf_of": null,
     "at": "2026-11-12T02:10:00-05:00", "scope": "…", "signature": null}

Records replace both sign-off files (clausebook/<book>.signoff.json, glossary.signoff.json):

    clausebook/<book>.attest.json    entries that book defines
    glossary.attest.json             entries of the old whole-phrase glossary
    trust/<project>.attest.json      the project's trust policy
    trust/assumptions.attest.json    entries of the assumption ledger (clausal/ledger.py)

Fixed here, in code, whatever a policy says:

  * the kind of a signer is read from the prefix of its id and must agree with the `kind` written; a record where the two
    disagree is refused;
  * `on_behalf_of` records a delegation and never changes the kind;
  * a model's record is `model-asserted`. It is never a person's: `person_review` looks at records of kind `person` only.

This module knows nothing of the Clausebook: what a subject's current digest is, and which store it belongs to, are given
to `sort_records` by the caller (vreport.py for pieces, report.py for the old glossary, trust.py for policies).
"""
from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

from .core import FeatureError

KINDS = {"person": "human:", "model": "model:", "tool": "tool:", "organisation": "org:"}      # signer kind -> id prefix
EVIDENCE_KIND = {"person": "human-asserted", "model": "model-asserted", "organisation": "organisation-asserted", "tool": "tested"}
ACTS = ["authored", "tested", "reviewed", "approved", "vouched"]
TOOL_ACTS = {"authored", "tested"}                       # a tool reads nothing against its meaning and accepts nothing
REVIEW_ACTS = {"reviewed", "approved"}                   # what the old sign-off was
SUBJECT_KINDS = {"piece", "separation", "glossary-entry", "policy", "assumption"}       # `assumption`: an entry of the ledger (W4, clausal/ledger.py)
RESERVED_SUBJECT_KINDS = {"specialist-term", "external-proof", "join"}                       # W8: not built
DIGEST_ALGS = {"sha256-text", "sha256"}
FIELDS = {"subject", "act", "signer", "on_behalf_of", "at", "scope", "context", "signature"}
REQUIRED = FIELDS - {"context"}
CONTEXT_KEYS = {"commit", "run", "toolchain"}


def kind_of_id(agent) -> str | None:
    """The signer kind an agent id carries in its prefix; None for a bare name or an unknown prefix."""
    if not isinstance(agent, str):
        return None
    for kind, prefix in KINDS.items():
        if agent.startswith(prefix) and agent[len(prefix):].strip() and "*" not in agent:
            return kind
    return None


def malformed(rec) -> list:
    """Every reason the record is not a record of the frozen format (shape only: nothing about the tree). [] if it is one."""
    if not isinstance(rec, dict):
        return ["a record is a JSON object"]
    why = []
    if set(rec) - FIELDS:
        why.append(f"unknown field(s) {sorted(set(rec) - FIELDS)}")
    if REQUIRED - set(rec):
        why.append(f"missing field(s) {sorted(REQUIRED - set(rec))}")
    s = rec.get("subject")
    if "subject" in rec:
        if not isinstance(s, dict) or set(s) != {"kind", "book", "id", "digest"}:
            why.append("`subject` has exactly the fields kind, book, id, digest")
        else:
            if s["kind"] in RESERVED_SUBJECT_KINDS:
                why.append(f"subject kind `{s['kind']}` is reserved and not built (plan node W8): nothing can check such a record yet")
            elif s["kind"] not in SUBJECT_KINDS:
                why.append(f"unknown subject kind `{s['kind']}` (one of: {', '.join(sorted(SUBJECT_KINDS))})")
            if not all(isinstance(s[k], str) and s[k] for k in ("book", "id")):
                why.append("`subject.book` and `subject.id` are non-empty strings")
            d = s["digest"]
            if not isinstance(d, dict) or set(d) != {"alg", "value"}:
                why.append("`subject.digest` has exactly the fields alg, value")
            elif d["alg"] not in DIGEST_ALGS:
                why.append(f"unknown digest algorithm `{d['alg']}` (one of: {', '.join(sorted(DIGEST_ALGS))})")
            elif not (isinstance(d["value"], str) and re.fullmatch(r"[0-9a-f]{64}", d["value"])):
                why.append("`subject.digest.value` is 64 lower-case hex digits")
    if "act" in rec and rec["act"] not in ACTS:
        why.append(f"unknown act `{rec['act']}` (one of: {', '.join(ACTS)})")
    g = rec.get("signer")
    kind = None
    if "signer" in rec:
        if not isinstance(g, dict) or not {"kind", "id"} <= set(g) or set(g) - {"kind", "id", "name"}:
            why.append("`signer` has the fields kind, id and optionally name")
        else:
            from_id = kind_of_id(g["id"])
            if g["kind"] not in KINDS:
                why.append(f"unknown signer kind `{g['kind']}` (one of: {', '.join(KINDS)})")
            if from_id is None:
                why.append(f"the signer id `{g['id']}` carries no kind: it must start with one of {', '.join(KINDS.values())} "
                           "(a bare name is not a signer)")
            elif g["kind"] in KINDS and from_id != g["kind"]:
                why.append(f"signer kind `{g['kind']}` with the id `{g['id']}`, which is a {from_id}'s: the kind is read from the id "
                           "and the two must agree")
            else:
                kind = from_id
            if "name" in g and not (isinstance(g["name"], str) and g["name"]):
                why.append("`signer.name`, when given, is a non-empty string")
    if kind == "tool" and rec.get("act") in ACTS and rec["act"] not in TOOL_ACTS:
        why.append(f"a tool may only have {' or '.join(sorted(TOOL_ACTS))} something; `{rec['act']}` by a tool is refused")
    if "on_behalf_of" in rec and rec["on_behalf_of"] is not None:
        o = rec["on_behalf_of"]
        if kind_of_id(o) is None:
            why.append(f"`on_behalf_of` is null or an agent id with a kind prefix; got {o!r}")
        elif isinstance(g, dict) and o == g.get("id"):
            why.append("`on_behalf_of` names the signer itself: that is no delegation")
    if "at" in rec:
        try:
            t = datetime.datetime.fromisoformat(rec["at"])
            if t.tzinfo is None or "T" not in rec["at"]:
                raise ValueError
        except (TypeError, ValueError):
            why.append(f"`at` is an ISO 8601 date and time with a UTC offset; got {rec['at']!r}")
    if "scope" in rec and not (isinstance(rec["scope"], str) and rec["scope"].strip()):
        why.append("`scope` says what was looked at: it may not be empty")
    if "context" in rec:
        c = rec["context"]
        if not isinstance(c, dict) or set(c) - CONTEXT_KEYS or not all(isinstance(v, str) for v in c.values()):
            why.append(f"`context` is an object of strings with the keys {', '.join(sorted(CONTEXT_KEYS))}")
    if "signature" in rec and rec["signature"] is not None:
        why.append("`signature` must be null: signatures are not checked in this build (plan node W9), and one that is not "
                   "checked may not be carried as if it were")
    return why


def make(subject_kind: str, book: str, id_: str, digest: dict, act: str, signer: str, scope: str, on_behalf_of: str | None = None,
         name: str | None = None, at: str | None = None, context: dict | None = None) -> dict:
    """A record, or FeatureError with every reason it would be refused. The signer's kind is READ from its id."""
    kind = kind_of_id(signer)
    if kind is None:
        raise FeatureError(f"`{signer}` is not a signer: an id starts with one of {', '.join(KINDS.values())} (person, model, tool, "
                           "organisation). A bare name is refused; nothing was written")
    rec = {"subject": {"kind": subject_kind, "book": book, "id": id_, "digest": digest}, "act": act,
           "signer": {"kind": kind, "id": signer, **({"name": name} if name else {})}, "on_behalf_of": on_behalf_of,
           "at": at or datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "scope": scope,
           **({"context": context} if context else {}), "signature": None}
    why = malformed(rec)
    if why:
        raise FeatureError("the attestation is refused and nothing was written: " + "; ".join(why))
    return rec


# --------------------------------------------------------------------------- stores

def read_store(path: Path) -> list:
    """The records of one store, as written ([] if there is no file). A store that is not a JSON list stops the caller."""
    if not path.exists():
        return []
    try:
        recs = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise FeatureError(f"{path.name}: not JSON ({e})")
    if not isinstance(recs, list):
        raise FeatureError(f"{path.name}: an attestation store is a JSON list of records")
    return recs


def write_store(path: Path, recs: list) -> None:
    path.write_text(json.dumps(recs, indent=2, ensure_ascii=False) + "\n")


def same_slot(a: dict, b: dict) -> bool:
    """One live record per (subject, act, signer): attesting again replaces the earlier record."""
    return (a["subject"]["kind"], a["subject"]["id"], a["act"], a["signer"]["id"]) == (b["subject"]["kind"], b["subject"]["id"], b["act"], b["signer"]["id"])


def add(path: Path, rec: dict) -> None:
    recs = [r for r in read_store(path) if malformed(r) or not same_slot(r, rec)]
    write_store(path, recs + [rec])


def refuse_old_file(path: Path) -> None:
    """A sign-off file of the old format is not read and not ignored: it would be a record with no kind, no act and no scope."""
    if path.exists():
        raise FeatureError(f"{path.name}: a sign-off file of the old format. It is no longer read: attest again with "
                           "`python3 -m clausal attest <id> --act … --as <kind-prefixed id> --scope …`, then delete the file")


class Records:
    """The records of some stores, sorted: `valid` (well-formed, in the right store, of the subject's current digest), `void`
    (well-formed, right store, but the subject has changed since) and `refused` (never counted; `clausal attest check` fails)."""

    def __init__(self):
        self.valid, self.void, self.refused = [], [], []          # records | (record, why) | (where, why-list, record)

    def of(self, id_: str, subject_kinds=None) -> list:
        return [r for r in self.valid if r["subject"]["id"] == id_ and (subject_kinds is None or r["subject"]["kind"] in subject_kinds)]

    def extend(self, other: "Records") -> "Records":
        self.valid += other.valid
        self.void += other.void
        self.refused += other.refused
        return self


def sort_records(recs: list, where: str, current) -> Records:
    """`current(record) -> (digest dict | None, reason)`: the subject's digest today, or None and why the record does not belong
    in this store (an entry the store's book does not define, an unknown id)."""
    out = Records()
    for k, r in enumerate(recs):
        at = f"{where}, record {k + 1}"
        why = malformed(r)
        if why:
            out.refused.append((at, why, r))
            continue
        now, reason = current(r)
        if now is None:
            out.refused.append((at, [reason], r))
        elif now != r["subject"]["digest"]:
            out.void.append((r, f"{at}: `{r['subject']['id']}` has changed since {r['signer']['id']} {r['act']} it on {r['at']}: the record is void"))
        else:
            out.valid.append(r)
    return out


def person_review(recs: list):
    """The record that makes a subject REVIEWED BY A PERSON, or None: act reviewed or approved, signer kind person. Fixed in
    code. A model's, a tool's or an organisation's record is never returned, whatever it says it was on behalf of."""
    return next((r for r in recs if r["signer"]["kind"] == "person" and r["act"] in REVIEW_ACTS), None)


def brief(r: dict) -> dict:
    """What the graph stores about a valid record (the subject is the node it is stored on)."""
    return {"act": r["act"], "kind": r["signer"]["kind"], "by": r["signer"]["id"], **({"name": r["signer"]["name"]} if r["signer"].get("name") else {}),
            "on_behalf_of": r["on_behalf_of"], "at": r["at"], "scope": r["scope"], "digest": r["subject"]["digest"],
            "evidence_kind": EVIDENCE_KIND[r["signer"]["kind"]]}


def said(r: dict) -> str:
    """One record in words. A person's record carries no checked signature (W9), so it is printed as a claim."""
    who = r["signer"].get("name") or r["signer"]["id"] if "signer" in r else r["by"]
    kind = r["signer"]["kind"] if "signer" in r else r["kind"]
    return (f"{r['act']} by {who}" + (" (claims to be; no signature is checked)" if kind == "person" else f" ({kind})")
            + (f" for {r['on_behalf_of']}" if r.get("on_behalf_of") else "") + f", {r['at'][:10]}")
