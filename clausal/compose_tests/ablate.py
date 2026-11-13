"""REMOVE THE FROZEN-ONLY CUE ENTRIES from a loaded composer, in the running process only (fix round of plan node L1c).

    import ablate; ablate.install(compose2, cues2, json.load(open("cue_audit.json"))["frozen_only"])

Nothing on disk changes: clausal/cues2.py and clausal/compose2.py stay as frozen at 3147bb4. This is for the sensitivity
run (compose_tests/l4r_sens.py) and its control on the development set (compose_tests/dev_sens.py).

WHAT REMOVING AN ENTRY MEANS, per table (the entries are those of compose_tests/cue_audit.py):
  PHRASES, OP_SYNONYMS, LIGHT, NECESSARY   a match of the entry's pattern whose group words are the entry ("leaves
      unchanged") is not seen by the composer: `re.finditer` and `re.search` as compose2 calls them skip it. Other matches
      of the same pattern ("leaves ... untouched") are seen as before.
  DIRECTIONS   the same, inside cues2.directions, and ONLY ON THE AUTHOR'S WORDS: the table also reads the direction of
      the book's own forms ("{t} is at most {m}"), and that reading is left whole. A text is the author's when it is the
      joined words of a lexed sentence (compose2.lexed_text returned it); every call of the composer on the author's words
      passes exactly that text. A removed match takes no place, so a later pattern can still match there if it is not
      removed too.
  CUES2, CUES2_NEG, INPUT_ROLE_WORDS, ROLE_WORDS   the entry's stem is taken out of that piece's (role's) bag.
  PREPOSITIONS, PARTICLES, COORDINATORS, PRONOUNS, DETERMINERS, REFLEXIVES, NEGATION_WORDS   the word is taken out of the
      set (and out of FUNCTION if no other of its sets still has it).
Version 1's own cue table (compose.CUES) is not touched: a word removed here that version 1 also has as a cue for the same
piece is still a cue through version 1's table.

`install` returns a record of what was removed; `hits` counts, per removed pattern entry, how often a match was skipped.
"""
from __future__ import annotations

import re as _re

hits: dict = {}

WORD_SETS = ("PREPOSITIONS", "PARTICLES", "COORDINATORS", "PRONOUNS", "DETERMINERS", "REFLEXIVES", "NEGATION_WORDS")
FUNCTION_SETS = ("PREPOSITIONS", "PARTICLES", "COORDINATORS", "PRONOUNS", "DETERMINERS")


def norm_match(m) -> str:
    gs = [m.group(k) for k in range(1, (m.re.groups or 0) + 1) if m.group(k) is not None]
    return " ".join(g.strip() for g in gs) if gs else m.group(0)


class FilteredRe:
    """The module `re` as compose2 sees it, with the removed matches skipped. Everything else is `re`."""

    def __init__(self, banned: dict):
        self.banned = banned                         # {pattern string: {entry}}

    def __getattr__(self, name):
        return getattr(_re, name)

    def finditer(self, pat, text, *a, **k):
        ban = self.banned.get(pat) if isinstance(pat, str) else None
        for m in _re.finditer(pat, text, *a, **k):
            if ban and norm_match(m) in ban:
                hits[(pat, norm_match(m))] = hits.get((pat, norm_match(m)), 0) + 1
                continue
            yield m

    def search(self, pat, text, *a, **k):
        if isinstance(pat, str) and pat in self.banned:
            return next(self.finditer(pat, text, *a, **k), None)
        return _re.search(pat, text, *a, **k)


def install(compose2, cues2, frozen_only: list) -> dict:
    banned, dir_banned, removed = {}, {}, []
    for e in frozen_only:
        t = e["table"]
        if t in ("PHRASES", "OP_SYNONYMS", "LIGHT", "NECESSARY"):
            banned.setdefault(e["pattern"], set()).add(e["entry"])
        elif t == "DIRECTIONS":
            dir_banned.setdefault(e["pattern"], set()).add(e["entry"])
        elif t == "CUES2":
            cues2.CUE2_BAGS[e["label"]] = cues2.CUE2_BAGS[e["label"]] - {e["stem"]}
        elif t == "CUES2_NEG":
            cues2.CUE2_NEG_BAGS[e["label"]] = cues2.CUE2_NEG_BAGS[e["label"]] - {e["stem"]}
        elif t == "INPUT_ROLE_WORDS":
            cues2.INPUT_ROLE_WORDS = cues2.INPUT_ROLE_WORDS - {e["stem"]}
        elif t == "ROLE_WORDS":
            cues2.ROLE_WORDS[e["label"]] = cues2.ROLE_WORDS[e["label"]] - {e["stem"]}
        elif t in WORD_SETS:
            setattr(cues2, t, getattr(cues2, t) - {e["entry"]})
        else:
            raise ValueError(f"no rule to remove an entry of {t}")
        removed.append(f"{t} {e['label']} {e['entry']!r}")
    cues2.FUNCTION = frozenset().union(*(getattr(cues2, s) for s in FUNCTION_SETS))
    compose2.re = FilteredRe(banned)

    author_texts = set()
    lexed_text = compose2.lexed_text

    def lexed_text_recording(lx):
        out = lexed_text(lx)
        author_texts.add(out[0])
        return out

    compose2.lexed_text = lexed_text_recording

    def directions(text: str) -> list:
        """cues2.directions, with the removed entries skipped on the author's words."""
        mine = text in author_texts
        taken, out = [], []
        for rel, pat in cues2.DIRECTIONS:
            ban = dir_banned.get(pat) if mine else None
            for m in _re.finditer(pat, text):
                if any(m.start() < e and s < m.end() for s, e in taken):
                    continue
                if ban and norm_match(m) in ban:
                    hits[(pat, norm_match(m))] = hits.get((pat, norm_match(m)), 0) + 1
                    continue
                taken.append(m.span(0))
                out.append((rel, cues2.groups(m), m.start()))
        return sorted(out, key=lambda x: x[2])

    cues2.directions = directions
    return {"removed": removed, "patterns": len(banned), "direction_patterns": len(dir_banned)}
