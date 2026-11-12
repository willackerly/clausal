"""clausal displaytext: the WORDS of the computed display (plan node Q6) and how a stored display is printed.

Pure: it imports nothing of clausal, so `clausal rules` can print the display of a Rule line from out/graph.json alone
(clausal/rules.py). The display itself is computed in clausal/display.py; every line below is chosen by a computed value
(a Calls value read off probes, a cell label, a case), never by the words of the sentence or its echo.
This text is display only: it is no sentence of the language and the compiler never reads it.
"""
from __future__ import annotations

import re
import textwrap

KINDS = ["accepted", "rejected", "no answer"]
LETTER = "arn"

# ------------------------------------------------------------------------------------------ the words of the display
# Display text only: no sentence of the language, never read by the compiler. Each line is chosen by a COMPUTED value.
HEAD = ("computed from the rule's Lean statement and its executable reading on generated inputs; "
        "not part of the rule, never read by the compiler")
COVERS = {
    "every": "every call in scope, accepted or rejected. A call that gives no answer BREAKS the rule.",
    "accepted": "ONLY calls that are accepted. A call that is rejected, or that gives no answer, is outside the rule: nothing is claimed about it.",
    "rejected": "ONLY calls that are rejected. A call that is accepted, or that gives no answer, is outside the rule: nothing is claimed about it.",
}
COVERS2 = {
    "every": "every pair of calls in scope where the second is related to the first as the rule says, whatever the two answers. "
             "If either call gives no answer the rule is BROKEN.",
    "accepted": "ONLY pairs of calls in which BOTH are accepted. Any other pair, and any pair in which a call gives no answer, is "
                "outside the rule: nothing is claimed about it.",
    "rejected": "ONLY pairs of calls in which BOTH are rejected. Any other pair, and any pair in which a call gives no answer, is "
                "outside the rule: nothing is claimed about it.",
}
LABEL = {
    "allowed": "allowed",
    "forbidden": "FORBIDDEN",
    "same": "allowed only if both calls give the same answer, otherwise FORBIDDEN",
    "mixed": "depends on the two answers ({true} of {n} sampled pairs of outcomes allowed)",
    "empty": "(no such outcome among the samples)",
}


# ------------------------------------------------------------------------------------------ printing

def say_values(v: dict) -> str:
    return ", ".join(f"{n.replace('_', ' ')} = {x}" for n, x in v.items())


def say_outcome(o: dict) -> str:
    if o["kind"] == "no answer":
        return "gives no answer"
    return f"answers {o['answer']} ({o['kind']}) and leaves {o['after']}"


HOW = {"model": "what the model of the code does", "substituted": "NOT what the model does here: an outcome it gives at another input, substituted",
       "silent": "NOT what the model does here: the call made to give no answer"}


def say_case(x: dict) -> list:
    how = HOW[x["how"]] + (": the code BREAKS the rule here" if x["how"] == "model" and x["which"] == "forbidden" else "")
    if "values2" in x:
        return [f"first call:  {say_values(x['values'])}: {say_outcome(x['outcome'])}",
                f"second call: {say_values(x['values2'])}: {say_outcome(x['outcome2'])}", f"[{how}]"]
    return [f"{say_values(x['values'])}: the call {say_outcome(x['outcome'])}", f"[{how}]"]


def render(d: dict, width: int = 104) -> list:
    """The display of one Rule line as text lines (label column of 10, as the rule block of the report)."""
    o = []

    def row(lab, text):
        text = re.sub(r"\[[^\]]*\]", lambda m: m.group(0).replace(" ", "\u00a0"), text)      # a list of values is not broken across lines
        w = [x.replace("\u00a0", " ") for x in textwrap.wrap(text, width, break_on_hyphens=False, break_long_words=False)] or [""]
        return [f"  {lab:<10}{w[0]}"] + [f"  {'':<10}{x}" for x in w[1:]]
    o += row("Display", f"({HEAD})")
    many = len(d["claims"]) > 1
    for k, c in enumerate(d["claims"]):
        if many:
            o += row("", f"-- claim {k + 1} of {len(d['claims'])} (frame `{c['frame']}`)")
        if "error" in c:
            o += row("covers", f"NOT COMPUTED: {c['error'].splitlines()[0][:400]}")
            continue
        cv, two = c["covers"], c["runs"] == 2
        what = " followed by ".join(c["nouns"])
        if not two and cv["in_scope"] == 0:
            o += row("covers", f"NOT COMPUTED: none of the {cv['points']} generated inputs is in scope of the rule, so nothing could be evaluated: "
                     "no covers line, no allowed case and no forbidden case. (The rule is not thereby empty: the samples do not reach it.)")
            continue
        if cv["calls"] is None:
            o += row("covers", f"NOT SETTLED: the claim's Calls value is `{c['calls']}` and the executable reading does not behave so ({cv['seen']})")
        elif two:
            o += row("covers", COVERS2[cv["calls"]] + f" (The call: {what}. {cv['pairs_in_scope']} of {cv['points'] ** 2} generated pairs of calls are in scope "
                     f"and related; {cv['pairs_of_different_calls']} of them are two different calls.)")
        else:
            o += row("covers", COVERS[cv["calls"]] + f" (The call: {what}. {cv['in_scope']} of {cv['points']} generated calls are in scope.)")
        if two and c["table"]:
            o.append(f"  {'outcomes':<10}{'first call':<13}{'second call':<13}the rule")
            for key, cell in c["table"]["cells"].items():
                lab = LABEL[cell["label"]].format(true=cell["allowed"], n=cell["outcome_pairs"])
                o += [f"  {'':<10}{KINDS[LETTER.index(key[0])]:<13}{KINDS[LETTER.index(key[1])]:<13}{x}" if i == 0 else f"  {'':<36}{x}"
                      for i, x in enumerate(textwrap.wrap(lab + f"   [the model, on the grid: {cell['model_pairs_on_grid']} pairs]", width - 26))]
        elif two:
            o += row("outcomes", "NOT COMPUTED: the grid has no pair of two different calls that is in scope and related")
        for lab, x in (("allowed", c["allowed"]), ("forbidden", c["forbidden"])):
            if x is None:
                o += row(lab, "no forbidden case exists among the generated inputs and substituted outcomes: on them the rule forbids NOTHING"
                         if lab == "forbidden" else "no case found in which the rule is about the call and holds")
            else:
                lines = say_case(x)
                o += row(lab, lines[0])
                for t in lines[1:]:
                    o += row("", t)
        nb = c.get("neighbour")
        if nb:
            o += row("neighbour", f"\"{nb['sentence']}\" ALLOWS the forbidden case ({nb['how']}; {nb['distance']} word(s) away)")
            sp = nb.get("separate")
            if sp:
                o += row("", sp)
        elif c.get("forbidden") and "neighbours_tried" in c:
            o += row("neighbour", f"none of the {c['neighbours_tried']} neighbouring sentences that compile allows the forbidden case"
                     if c["neighbours_tried"] else "no neighbouring sentence compiles")
    return o
