"""The ORDINARY-ENGLISH TABLES of composer version 2, second part (plan node L1c): phrase cues, word cues for the pieces the
last wave added, the words of a comparison and their direction, function words. Version 1's table (compose.CUES) is
not changed; these are used beside it by clausal/compose2.py.

WHAT A CUE IS. A cue never adds a form and never changes what a sentence means: the sentence shown is a sentence of the
book and its reading is the compiler's. A cue only says that a word (or a phrase) of the author's is ACCOUNTED FOR by a
piece of a candidate. A wrong cue can therefore make a candidate look complete that is not what the author meant; that
is the risk of every line here, and why each line is tied to what the piece MEANS (its echo in the book).

WHERE THE LINES CAME FROM. Written while looking at the development set (clausal/compose_tests/dev/devset.json) and at
nothing of trials/sentences. They are ordinary English for the meaning of SHARED pieces (clausebook/core.yaml and the
packs); no line names an operation or a domain word of a project by id. Words for a project's own pieces come from the
book: a role's type ("the receiving wallet": a role of type wallet), a domain piece's echo (`echo_words`).
"""
from __future__ import annotations

import re

from . import compose as v1

# --------------------------------------------------------------------------------------------- senses: which pieces say what
# A sense is a meaning that several pieces of the book carry. `ids`: the shared pieces. `classes`: also every piece of
# category `class` whose form is that text (the acceptance class of each project: "it is accepted").
SENSES = {
    # the answer is an acceptance
    "ACCEPT": {"ids": ("successful", "always", "if_then", "only_if", "exactly_when", "accepted"), "class_form": "it is accepted"},
    # the answer is a rejection
    "REJECT": {"ids": ("rejected", "never", "rejected_unchanged"), "class_form": None},
    # the state (or a measure of it) after the call is what it was before
    "UNCHANGED": {"ids": ("never_changes", "rejected_unchanged"), "class_form": None},
    "UP": {"ids": ("increases_by",), "class_form": None},            # after = before + t
    "DOWN": {"ids": ("decreases_by",), "class_form": None},          # after + t = before
    "IFF": {"ids": ("exactly_when",), "class_form": None},           # accepted if and only if the condition
    "SAME": {"ids": ("equals", "same_input"), "class_form": None},
    "THEN": {"ids": ("and_then",), "class_form": None},              # a second call on the state the first leaves
}
# "ONLY IF" / "ONLY WHEN" says which of the three connectives is meant: these two words are accounted for only by the frame
# "is accepted only if" (as its form words, its cue, or the opener of its condition), never as a cue for "whenever" or
# "exactly when", and never as the opener of another piece's condition.
NECESSARY = r"\b(only) (if|when)\b"
NECESSARY_PIECE = "only_if"

# What a phrase of a sense adds to the tokens VERSION 1'S GENERATOR sees (compose2.hint_tokens): one of version 1's own cue
# words for the sense, so that it writes the narrowing or the frame. Coverage never sees these.
SENSE_HINT = {"ACCEPT": "accept", "REJECT": "reject", "UNCHANGED": "unchanged never changes", "UP": "increases", "DOWN": "decreases",
              "IFF": "exactly when", "SAME": "same equals", "THEN": "followed"}

# WORD CUES of version 2, beside version 1's (compose.CUES): {piece id: words}. Stemmed with version 1's stemmer.
CUES2 = {
    # the frames that say "accepted": the author's other words for an acceptance (version 1 has these on the narrowing only)
    "always": "succeed ok allow permit work",
    "if_then": "succeed ok allow permit work accept",
    "only_if": "succeed ok allow permit work accept",
    "exactly_when": "succeed ok allow permit work accept",
    # "is always rejected": the author's other words for a rejection
    "never": "reject refuse fail deny decline",
    # ---- the pieces of the last wave (L2)
    "equals": "equal same identical itself",                 # a is the same value as b
    "each_at_most": "each every all most exceed more above over hold",   # every one of the numbers after the call is at most t
    "same_input": "same again back",                         # the second call is given the first call's input
    # ---- version 1's frames, further words
    "never_changes": "untouched alone intact put restore",
    "increases_by": "raise",
    "decreases_by": "lower remove",
    "and_then": "then",
}
CUES2_NEG = {"equals": "different differ distinct other"}    # "differs from": the negated piece


def bag2(text: str) -> frozenset:
    """The stems of every word of a cue line (version 1's `bag` leaves out its stop words: "then", "it")."""
    return frozenset(v1.stem(w) for w in text.split())


CUE2_BAGS = {k: bag2(v) for k, v in CUES2.items()}
CUE2_NEG_BAGS = {k: bag2(v) for k, v in CUES2_NEG.items()}

# PHRASE CUES: (sense, pattern over the lower-cased words of the rough sentence joined by one space). The words in the
# pattern's GROUPS are the phrase; words matched outside a group (the gap between "leaves" and "untouched") stay free.
G = r"(?:[a-z0-9']+ ){0,6}?"       # a gap of up to six words
PHRASES = [
    ("ACCEPT", r"\b(go|goes|went|gone|going) (through|ahead)\b"),
    ("REJECT", r"\b(turn|turns|turned) (down)\b"),
    ("UNCHANGED", r"\b(leave|leaves|left|leaving|keep|keeps|kept) " + G + r"(untouched|unchanged|alone|intact|the same)\b"),
    ("UNCHANGED", r"\b(leave|leaves|left|leaving|keep|keeps|kept) " + G + r"(exactly )?(as|where) (it|they) (was|were|started|found it|found them|is|are)\b"),
    ("UNCHANGED", r"\b(stay|stays|stayed|remain|remains|remained) (put|the same|unchanged|untouched)\b"),
    ("UNCHANGED", r"\b(stay|stays|stayed|remain|remains|remained) (exactly )?(as|where) (it|they) (was|were|started|is|are)\b"),
    ("UNCHANGED", r"\b(does|do|did) (not) (move|change|budge)\b"),
    ("UNCHANGED", r"\b(is|are|goes|go|put|puts) " + G + r"(back) (to )?(what|where) (it|they) (was|were|started)\b"),
    ("UP", r"\b(add|adds|added|adding) " + G + r"(to)\b"),
    ("UP", r"\b(credit|credits|credited) " + G + r"(with)\b"),
    ("UP", r"\b(go|goes|went) (up)\b"),
    ("DOWN", r"\b(take|takes|took|taking) " + G + r"(out) (of)\b"),
    ("DOWN", r"\b(go|goes|went) (down)\b"),
    ("IFF", r"\b(and) (?:is |be |it is |are )?(refused|rejected|turned down|fails|fail|denied) (otherwise)\b"),
    ("IFF", r"\b(and) (?:is |be |it is |are )?(refused|rejected|turned down|fails|fail|denied) (when|if) (it|they) (?:does |do |is |are |has |have )(not)\b"),
    ("SAME", r"\b(the) (same)\b"),
]

# OPERATIONS NAMED BY A VERB PHRASE, keyed by the operation's NOUN in the book (not by its id): ordinary English for what
# the noun names. An operation anchored this way is `anchored by: a synonym of its noun`, and the words are mapped to it.
OP_SYNONYMS = {
    "deposit": r"\b(put|puts|putting|pay|pays|paying) (?:money |funds |an amount |cash )?(in|into)\b",
    "withdrawal": r"\b(take|takes|taking) (?:money |funds |an amount |cash )?(out)\b",
    "transfer": r"\b(send|sends|sending|move|moves|moving) (?:money|funds)\b|\b(send|sends|sending)\b",
    "lookup": r"\b(look|looks|looking) (up)\b|\b(ask|asks|asking) (for)\b",
    "batch applied as a whole": r"\b(all) (or) (nothing)\b|\b(atomic|atomically)\b",
}
# A LIGHT VERB before an operation's noun says nothing of its own ("applying a transfer", "running a batch").
LIGHT = r"\b(apply|applies|applying|run|runs|running|make|makes|making|perform|performs|performing|execute|executes|executing|do|does|doing|try|tries|trying|attempt|attempts|attempting)\b(?= (?:to )?(?:a |an |the |one |each |every |any )?%NOUN%\b)"

# AN INPUT ROLE said with a participle: "the requested amount", "the amount given".
INPUT_ROLE_WORDS = bag2("requested given asked supplied")
# A ROLE said by another word for it: {role name: words}. Ordinary English for the role's NAME, not for a project.
ROLE_WORDS = {"receiver": bag2("receiving recipient payee destination"), "sender": bag2("sending payer source")}

# FUNCTION WORDS. Not on the stop list: each gets a status. A preposition is accounted for WITH ITS OBJECT (the next
# content word, else the word before it); a particle with the word before it (else after); a coordinator when the words on
# both sides of it are accounted for; a pronoun stands for the subject of the sentence (the operation).
PREPOSITIONS = frozenset("to of in by from with into onto on at for than as per".split())
PARTICLES = frozenset("up down out back through off away over".split())
COORDINATORS = frozenset("and or nor but".split())
PRONOUNS = frozenset("it its they their them".split())
# A universal determiner before a word that is accounted for ("every balance", "the whole ledger") says nothing more, UNLESS
# the candidate has a quantifier piece of its own (then "every" against "some" is a difference, and the word must be said).
DETERMINERS = frozenset("every each all any both whole entire".split())
QUANTIFIER_PIECES = frozenset("every some_of no_such the_first every_of none_of each_at_most within covers all_of".split())
FUNCTION = PREPOSITIONS | PARTICLES | COORDINATORS | PRONOUNS | DETERMINERS

# THE WORDS OF A COMPARISON AND THEIR DIRECTION (argument order). "A <words> B" says A REL B. Longest patterns first: "no
# more than" is tried before "more than". The same table reads the direction of a candidate's own form ("{t} is at most
# {m}", "never leaves {m} above {t}"), so nothing here names a piece.
DIRECTIONS = [
    ("LE", r"\b(no|not) (more|larger|greater|bigger|higher) (than)\b"),
    ("GE", r"\b(no|not) (less|fewer|smaller|lower) (than)\b"),
    ("LE", r"\b(at) (or) (under|below)\b"),
    ("GE", r"\b(at) (or) (over|above)\b"),
    ("LE", r"\b(at) (most)\b"),
    ("GE", r"\b(at) (least)\b"),
    ("GT", r"\b(more|larger|greater|bigger|higher) (?:[a-z]+ ){0,2}?(than)\b"),
    ("LT", r"\b(less|fewer|smaller|lower) (?:[a-z]+ ){0,2}?(than)\b"),
    ("GT", r"\b(exceed|exceeds|exceeded|exceeding)\b"),
    ("GT", r"\b(above|over|past|beyond)\b"),
    ("LT", r"\b(below|under)\b"),
    ("GE", r"\b(enough) (?:[a-z]+ )?(to) (cover)\b"),
    ("GE", r"\b(cover|covers|covered)\b"),
    ("GE", r"\b(enough)\b"),
    ("LE", r"\b(within)\b"),
    ("LT", r"\b(too) (little|few)\b"),
    ("NE", r"\b(differ|differs|differed|different) (from)\b"),
    ("NE", r"\b(not) (equal|equals)\b"),
    ("EQ", r"\b(equal|equals|equalled|equalling)\b"),
    ("EQ", r"\b(itself|themselves)\b"),              # "from an account to itself": the two are the same
]
REFLEXIVES = frozenset("itself themselves".split())
NEGATE = {"LE": "GT", "GT": "LE", "GE": "LT", "LT": "GE", "EQ": "NE", "NE": "EQ"}
CONVERSE = {"LE": "GE", "GE": "LE", "GT": "LT", "LT": "GT", "EQ": "EQ", "NE": "NE"}
NEGATION_WORDS = frozenset("not no never none nothing neither nor".split())


def groups(m) -> list:
    """The (start, end) character spans of the groups of a match that took part."""
    return [m.span(k) for k in range(1, (m.re.groups or 0) + 1) if m.span(k) != (-1, -1)] or [m.span(0)]


def directions(text: str) -> list:
    """The comparison words of a text, left to right, each once: [(REL, [(start, end) of its words], start of the match)].
    A later pattern never matches inside an earlier match."""
    taken, out = [], []
    for rel, pat in DIRECTIONS:
        for m in re.finditer(pat, text):
            if any(m.start() < e and s < m.end() for s, e in taken):
                continue
            taken.append(m.span(0))
            out.append((rel, groups(m), m.start()))
    return sorted(out, key=lambda x: x[2])


def form_direction(form_literal_before: str, form_literal: str):
    """The relation a form says between the holes written before its comparison words and those after, or None.
    A negation word of the form before the comparison flips it ("never leaves {m} above {t}": m is at most t)."""
    ds = directions(form_literal)
    if not ds and " ".join(form_literal.split()) in ("is", "is now"):
        return "EQ", form_literal.find("is")      # "{m} is {t}", "{a} is {t}", "{m} is now {t}": an equation said with "is"
    if len(ds) != 1:
        return None
    rel, spans, start = ds[0]
    if set(re.findall(r"[a-z]+", form_literal[:start])) & NEGATION_WORDS:
        rel = NEGATE[rel]
    return rel, start


def echo_words(piece: dict) -> frozenset:
    """The words of a DOMAIN piece's echo, outside its parentheses: the book's own plain words for the piece."""
    if piece.get("kind") != "domain":
        return frozenset()
    return v1.bag(re.sub(r"\([^)]*\)", " ", piece.get("echo") or ""))
