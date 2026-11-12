#!/usr/bin/env python3
"""WHERE THE CUES OF clausal/cues2.py HAVE SUPPORT: for every entry of its ordinary-English tables, the development
sentences (compose_tests/dev/devset.json) and the frozen trial sentences (trials/sentences/authors.json) it matches.

    python3 clausal/compose_tests/cue_audit.py            # prints the table; writes compose_tests/cue_audit.json
    python3 clausal/compose_tests/cue_audit.py --check    # exit 1 if cue_audit.json is not what the tables give now

WHY (fix round of plan node L1c). The composer was to be developed against the development set only. The study the
builder followed (docs/studies/2026-11-12/composer-v2.md) quotes words of the frozen sentences ("rejected when amount is
larger", "no larger than the number of transfers", "goes down / goes up"), and version 1's report on the 48
(compose_tests/l4b_a0/) was written earlier in the same stream of work. So a cue can fit a frozen sentence without any development sentence asking for it. This script lists those
entries. It was first written by the reviewer of L1c (cuecheck.py); this is that method, committed.

It READS trials/sentences/authors.json and changes nothing there. No composer is run: a sentence is lexed
(compose2.lex), and an entry MATCHES a sentence when
  a pattern table (PHRASES, OP_SYNONYMS, LIGHT with each operation noun of the book, DIRECTIONS, NECESSARY): the pattern
      is found in the lexed words joined by one space. The entry is the words of the pattern's groups that took part
      ("leaves unchanged"), so one pattern gives several entries. Each DIRECTIONS pattern is tried on its own (the
      composer does not let a later pattern match inside an earlier match; here "larger than" is also counted inside "no
      larger than").
  a stemmed word table (CUES2, CUES2_NEG, INPUT_ROLE_WORDS, ROLE_WORDS): a word of the sentence has the entry's stem.
  an exact word table (PREPOSITIONS, PARTICLES, COORDINATORS, PRONOUNS, DETERMINERS, REFLEXIVES, NEGATION_WORDS): the
      word is in the sentence.

FROZEN-ONLY: an entry that matches at least one frozen sentence and no development sentence. That is all it means. It
does not show that the entry was written FOR a frozen sentence (it may be plain English the builder would have written
anyway), and an entry that also matches a development sentence may still have been written with a frozen one in mind.
An entry that matches neither set is listed as `unsupported` (it was written from general English, tested on nothing).

NOT AUDITED: the tables of version 1 (compose.CUES, older than the development set), and the patterns inside
clausal/compose2.py itself (OPENERS, the role patterns, MISSING_KINDS, the clause splitter).

The list `frozen_only` of cue_audit.json is what compose_tests/ablate.py removes for the sensitivity run
(compose_tests/l4r_sens.py); it is committed before that run.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLAUSAL = HERE.parent
REPO = CLAUSAL.parent
OUT = HERE / "cue_audit.json"

WORD_TABLES = ("PREPOSITIONS", "PARTICLES", "COORDINATORS", "PRONOUNS", "DETERMINERS", "REFLEXIVES", "NEGATION_WORDS")


def norm_match(m) -> str:
    """The words of the groups of a match that took part, in order, joined by one space."""
    gs = [m.group(k) for k in range(1, (m.re.groups or 0) + 1) if m.group(k) is not None]
    return " ".join(g.strip() for g in gs) if gs else m.group(0)


def pattern_tables(cues2, nouns) -> list:
    """[(table, label, pattern)] for every pattern the composer applies to the author's words."""
    out = [("PHRASES", f"{n}:{sense}", pat) for n, (sense, pat) in enumerate(cues2.PHRASES)]
    out += [("OP_SYNONYMS", noun, pat) for noun, pat in cues2.OP_SYNONYMS.items()]
    out += [("LIGHT", noun, cues2.LIGHT.replace("%NOUN%", re.escape(noun) + "s?")) for noun in nouns]
    out += [("DIRECTIONS", f"{n}:{rel}", pat) for n, (rel, pat) in enumerate(cues2.DIRECTIONS)]
    out += [("NECESSARY", "only_if", cues2.NECESSARY)]
    return out


def audit() -> dict:
    sys.path.insert(0, str(CLAUSAL))
    import os
    os.chdir(CLAUSAL)
    from clausal import compose as v1
    from clausal import compose2, cues2
    authors = json.loads((REPO / "trials" / "sentences" / "authors.json").read_text())["authors"]
    frozen = {f"{a['author']}/{r['id']}": r["rule"] for a in authors for r in a["rules"]}
    dev = {d["id"]: d["sentence"] for d in json.loads((HERE / "dev" / "devset.json").read_text())}
    assert len(frozen) == 48 and len(dev) == 60, (len(frozen), len(dev))

    def lexed(sents):
        out = {}
        for k, s in sents.items():
            lx = compose2.lex(s)
            out[k] = (" ".join(w for w, _ in lx), [w for w, _ in lx])
        return out

    F, D = lexed(frozen), lexed(dev)
    voc, _ = compose2.load()
    nouns = sorted({n for o in voc.ops.values() for n in o["nouns"]})
    entries = []

    def add(table, label, entry, f, d, **more):
        entries.append({"table": table, "label": label, "entry": entry, "frozen": sorted(f), "dev": sorted(d), **more})

    for table, label, pat in pattern_tables(cues2, nouns):
        hits = {}
        for which, T in (("f", F), ("d", D)):
            for k, (text, _) in T.items():
                for m in re.finditer(pat, text):
                    hits.setdefault(norm_match(m), {"f": set(), "d": set()})[which].add(k)
        for e in sorted(hits):
            add(table, label, e, hits[e]["f"], hits[e]["d"], pattern=pat)
        if not hits:
            add(table, label, None, (), (), pattern=pat)

    def stem_table(table, label, words):
        for w in words:
            st = v1.stem(w)
            add(table, label, w, [k for k, (_, ws) in F.items() if st in {v1.stem(x) for x in ws}],
                [k for k, (_, ws) in D.items() if st in {v1.stem(x) for x in ws}], stem=st)

    for pid, words in cues2.CUES2.items():
        stem_table("CUES2", pid, words.split())
    for pid, words in cues2.CUES2_NEG.items():
        stem_table("CUES2_NEG", pid, words.split())
    # the two role tables are kept as bags of stems; the words are listed here as cues2.py writes them
    stem_table("INPUT_ROLE_WORDS", "input role", "requested given asked supplied".split())
    assert cues2.INPUT_ROLE_WORDS == cues2.bag2("requested given asked supplied")
    role_src = {"receiver": "receiving recipient payee destination", "sender": "sending payer source"}
    assert {k: cues2.bag2(v) for k, v in role_src.items()} == cues2.ROLE_WORDS
    for role, words in role_src.items():
        stem_table("ROLE_WORDS", role, words.split())
    for table in WORD_TABLES:
        for w in sorted(getattr(cues2, table)):
            add(table, table.lower(), w, [k for k, (_, ws) in F.items() if w in ws], [k for k, (_, ws) in D.items() if w in ws])

    real = [e for e in entries if e["entry"] is not None]
    fo = [e for e in real if e["frozen"] and not e["dev"]]
    return {"schema": "cue-audit-v1",
            "what": "every entry of the tables of clausal/cues2.py with the frozen trial sentences and the development sentences it matches; "
                    "frozen_only = at least one frozen sentence and no development sentence (see compose_tests/cue_audit.py)",
            "sentences": {"frozen": len(frozen), "dev": len(dev)},
            "counts": {"entries": len(real), "frozen_only": len(fo), "one_frozen_sentence_only": sum(len(e["frozen"]) == 1 for e in fo),
                       "dev_supported": sum(bool(e["dev"]) for e in real), "unsupported": sum(not e["frozen"] and not e["dev"] for e in real),
                       "patterns_matching_nothing": sum(e["entry"] is None for e in entries)},
            "frozen_only": fo, "entries": entries}


def say(d: dict) -> str:
    c = d["counts"]
    o = [f"entries {c['entries']}: matched by a development sentence {c['dev_supported']}, FROZEN-ONLY {c['frozen_only']} "
         f"({c['one_frozen_sentence_only']} of them in exactly one frozen sentence), in neither set {c['unsupported']}; "
         f"patterns that match no sentence of either set {c['patterns_matching_nothing']}", "", "FROZEN-ONLY:"]
    for e in d["frozen_only"]:
        o.append(f"  {e['table']:16s} {e['label']:26s} {e['entry']!r:24s} frozen {len(e['frozen']):2d}: {', '.join(e['frozen'])}")
    return "\n".join(o)


if __name__ == "__main__":
    d = audit()
    text = json.dumps(d, indent=1, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        same = OUT.exists() and OUT.read_text() == text
        print("cue_audit.json is what the tables give now" if same else "cue_audit.json DIFFERS from what the tables give now")
        sys.exit(0 if same else 1)
    OUT.write_text(text)
    print(say(d))
