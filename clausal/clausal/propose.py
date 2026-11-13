"""clausal propose: THE INTERFACE OF A PROPOSER (the hook for plan node L1f). NOTHING HERE CALLS A LANGUAGE MODEL, and
no proposer is shipped: L1f (a model proposer, the neighbour comparison, the adversarial tests, the evidence-graph kind)
is not built. What is here is the contract and the checker, so that whatever proposes is held to it:

    python3 -m clausal propose --request "<rough English>" [--domain D]     what a proposer is GIVEN, as JSON
    python3 -m clausal propose --check PROPOSAL.json                        what the tool makes of what a proposer RETURNS

A PROPOSER IS GIVEN (`request`):
    { "schema": "clausal-proposal-request-v1",
      "rough": "<the author's sentence, verbatim>", "rough_sha256": "...",
      "system": "<a system of the book>" | null,                 null: the author gave none
      "books": [ { "book": "<file>", "sha256": "..." } ],        the books its trees are checked against
      "tree_schema": "python3 -m clausal tree --schema",         how to get the JSON schema of the trees, GENERATED FROM THE BOOK
                                                                 (about 1 MB: piece ids, the holes of each, the roles of each
                                                                 operation, the literal types; not inlined, never stored)
      "tree_format": "clausal-tree-v1" }

A PROPOSER MUST RETURN (`PROPOSAL`), and nothing else is read:
    { "schema": "clausal-proposal-v1",
      "rough_sha256": "<of the request>",
      "proposed_by": { "kind": "model" | "person" | "rule-based",
                       "id": "<for a model: the `model` field OF THE API RESPONSE, not of the request>",
                       "provider": "...", "date": "YYYY-MM-DD", "prompt_sha256": "...", "parameters": { ... },
                       "on_behalf_of": "<the person who ran it>" },
      "trees": [ TREE, ... ],                at most MAX_TREES; each a `clausal-tree-v1` tree (clausal/ctree.py: piece ids and
                                             role phrases, NO TEXT OF A SENTENCE)
      "alignment": [ { "tree": 0, "word": 3, "piece": "<piece id of that tree>" }, ... ] | null,
                                             optional: which word of the rough sentence (index among its words) the proposer
                                             reads as which piece. ADVISORY (see below)
      "no_tree": null | { "missing": "<the kind of piece the book lacks>" } }      optional; ADVISORY: declining is the tool's rule

    A field of free text that would reach a feature file does not exist: the sentence is written from the tree by the
    compiler's own writer. `additionalProperties` are refused.

HOW IT IS CHECKED (`check`; every step is the tool's, none is the proposer's):
  1. shape       the proposal has exactly the fields above; `rough_sha256` is the request's.
  2. schema      each tree is validated against the schema generated from the book NOW (`ctree.validate`): an unknown piece,
                 a role of another operation, a missing hole, prose in a field -> the tree is DROPPED (reason kept).
  3. written     the sentence is written from the tree with the live form of each piece (`ctree.sentence`), compiled by the
                 ordinary compiler, and kept only if the composition the compiler finds IS the tree proposed (a tree that
                 spells another composition is DROPPED). A refusal of the compiler (Q1, a retired form, a sentence two
                 systems read) DROPS the tree; its text is kept for a repair round (at most two; a caller's loop, not here).
  4. filters     the filters of compose2 (other-book, opposite-narrowing, by-zero, same-sides, constants).
  5. coverage    compose2's accounting of the ROUGH sentence against the compiled reading: DROPPED words, ADDED pieces,
                 CONDITION DROPPED, argument order. Computed from the form words and the cue tables only. The proposer's
                 `alignment` is NOT used for it in this version: it is carried into the record as `alignment_claimed` and
                 shown, so that a false alignment cannot hide a dropped word. (Whether a model alignment may ever count is
                 the seeded-drop test of node L1b with an adversarial aligner; not run.)
  6. outcome     the candidates that pass go where rule-based candidates go: ANSWER only with full coverage and one reading;
                 otherwise the author is asked (clausal/dialogue.py). A proposal never chooses.
  The echo shown beside a candidate is the compiler's, never the proposer's words.

HOW IT IS ATTESTED (`record`): one record per composed rule, in the sidecar `<FILE>.compose.json` that
`clausal compose2 --write` already keeps, keyed by the digest of the Lean term:
    proposed_by     as returned, with `kind`; a model's `id` must come from the API response
    rough, rough_sha256, books (digests)
    checks          schema_valid, written_and_read_back, filters, coverage (dropped, added, conditions, full),
                    alignment_claimed, each question asked with its input and who answered
    chosen_by       "human:<name>" | "rule (the one surviving reading)"       never the proposer
    what            "the harness's record of what was run; not a signature"
  In the evidence graph such a rule is to be its own kind (`model-proposed`, agent `model:<id>`), never `human-asserted`,
  and a model attestation must not satisfy strict mode (the sign-off record gains `kind` and `on_behalf_of`). THAT PART IS
  NOT BUILT: nothing reads the sidecar yet (clausal/report.py, clausal/vreport.py are unchanged).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from . import compose2, ctree, projects
from .pipeline import ROOT

REQUEST, PROPOSAL = "clausal-proposal-request-v1", "clausal-proposal-v1"
MAX_TREES = 8
FIELDS = {"schema", "rough_sha256", "proposed_by", "trees", "alignment", "no_tree"}
BY_FIELDS = {"kind", "id", "provider", "date", "prompt_sha256", "parameters", "on_behalf_of"}
KINDS = ("model", "person", "rule-based")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def request(rough: str, system: str | None = None) -> dict:
    voc, _ = compose2.load()
    return {"schema": REQUEST, "rough": rough, "rough_sha256": sha(rough), "system": system,
            "books": [{"book": b.rel, "sha256": sha(b.text)} for b in voc.books],
            "tree_schema": "python3 -m clausal tree --schema", "tree_format": ctree.SCHEMA}


def check(req: dict, proposal) -> dict:
    """What the tool makes of a proposal: {ok, errors, proposed_by, candidates: [...], dropped: [...]}. See the module text."""
    out = {"schema": "clausal-proposal-check-v1", "ok": False, "errors": [], "proposed_by": None, "candidates": [], "dropped": [],
           "no_tree": None, "language_model_called_here": False}
    if not isinstance(proposal, dict) or proposal.get("schema") != PROPOSAL:
        out["errors"].append(f"not a `{PROPOSAL}` object")
        return out
    extra = set(proposal) - FIELDS
    if extra:
        out["errors"].append("fields that are not part of a proposal (nothing else is read): " + ", ".join(sorted(extra)))
    if proposal.get("rough_sha256") != req["rough_sha256"]:
        out["errors"].append("`rough_sha256` is not the request's")
    by = proposal.get("proposed_by")
    if not isinstance(by, dict) or by.get("kind") not in KINDS or not isinstance(by.get("id"), str) or set(by) - BY_FIELDS:
        out["errors"].append(f"`proposed_by` needs `kind` (one of {', '.join(KINDS)}) and `id`, and only the fields {', '.join(sorted(BY_FIELDS))}")
    trees = proposal.get("trees")
    if not isinstance(trees, list) or len(trees) > MAX_TREES:
        out["errors"].append(f"`trees` is a list of at most {MAX_TREES} trees")
    if out["errors"]:
        return out
    out["proposed_by"], out["no_tree"] = by, proposal.get("no_tree")
    voc, comp = compose2.load()
    sch = ctree.schema(voc)
    projs = list(projects.load(ROOT))
    align = proposal.get("alignment") or []
    for k, tree in enumerate(trees):
        errs = ctree.validate(tree, sch)
        if errs:
            out["dropped"].append({"tree": k, "step": "schema", "why": errs[:5]})
            continue
        try:
            got = ctree.sentence(tree, voc, comp)
        except ctree.TreeError as e:
            out["dropped"].append({"tree": k, "step": "written", "why": str(e)})
            continue
        rd = got["reading"]
        f = compose2.filtered(voc, rd, projs)
        if f:
            out["dropped"].append({"tree": k, "step": "filters", "why": f, "sentence": got["sentence"]})
            continue
        cov = compose2.coverage(voc, req["rough"], rd)
        out["candidates"].append({"tree": k, "sentence": got["sentence"], "system": rd.info["domain"], "compiles_as_written": got["compiles_as_written"],
                                  "term_sha256": ctree.body_sha(rd), "echo": [list(e) for e in rd.echo],
                                  "coverage": {x: cov[x] for x in ("dropped", "added", "condition_dropped", "order_refused", "full", "askable")},
                                  "alignment_claimed": [a for a in align if isinstance(a, dict) and a.get("tree") == k],
                                  "alignment_used_for_coverage": False})
    out["ok"] = True
    return out


def record(req: dict, checked: dict, cand: dict, chosen_by: str) -> dict:
    """The attestation record of one rule composed from a proposal (the sidecar format of `clausal compose2 --write`)."""
    assert not chosen_by.startswith("model"), "a proposer never chooses"
    return {"sentence": cand["sentence"], "term_sha256": cand["term_sha256"], "system": cand["system"], "proposed_by": checked["proposed_by"],
            "rough": req["rough"], "rough_sha256": req["rough_sha256"], "books": req["books"],
            "checks": {"schema_valid": True, "written_and_read_back": True, "filters": "passed", "coverage": cand["coverage"],
                       "alignment_claimed": cand["alignment_claimed"], "alignment_used_for_coverage": False, "questions": None},
            "chosen_by": chosen_by, "what": "the harness's record of what was run; not a signature"}


def main(argv) -> int:
    argv = list(argv)
    domain = None
    if "--domain" in argv:
        i = argv.index("--domain")
        domain = argv[i + 1]
        del argv[i:i + 2]
    if "--request" in argv:
        i = argv.index("--request")
        print(json.dumps(request(argv[i + 1], domain), indent=1, ensure_ascii=False))
        return 0
    if "--check" in argv:
        i = argv.index("--check")
        p = json.loads(Path(argv[i + 1]).read_text() if argv[i + 1] != "-" else sys.stdin.read())
        rough = p.pop("rough", None)             # a test file may carry the rough sentence beside the proposal
        if rough is None:
            print("clausal propose --check: the file needs `rough` (the request's sentence) beside the proposal", file=sys.stderr)
            return 2
        res = check(request(rough, domain), p)
        print(json.dumps(res, indent=1, ensure_ascii=False))
        return 0 if res["ok"] and res["candidates"] else 1
    print(__doc__)
    return 2
