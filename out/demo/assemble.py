#!/usr/bin/env python3
"""Assemble out/demo/<theorem>.md from the hand-written template in templates/ and the
Lean-generated blocks in generated/ (written by `lake env lean Rosette/Demo.lean`).

    python3 out/demo/assemble.py

Markers in a template (each on its own line), where <cfg> is lifted | filtered | wide:
    @@STATEMENT <cfg>@@   original signature and proof sizes
    @@RESULT <cfg>@@      the config / result / kernel-check lines
    @@SKELETON <cfg>@@    mermaid graph and nested list of lifted statements
    @@HAVES@@             the author's `have` boundaries with their hidingRatio rank
Nothing in the generated blocks is edited: they are copied verbatim.
"""
import os, re, sys

here = os.path.dirname(os.path.abspath(__file__))

def gen(name, cfg):
    with open(os.path.join(here, "generated", f"{name}.{cfg}.md"), encoding="utf-8") as f:
        return f.read()

def section(text, start, end=None):
    i = text.index(start) + len(start)
    j = text.index(end, i) if end and end in text[i:] else len(text)
    return text[i:j].strip("\n")

def expand(name, line):
    m = re.fullmatch(r"@@(STATEMENT|RESULT|SKELETON|HAVES)(?: (\w+))?@@", line.strip())
    if not m:
        return line
    kind, cfg = m.group(1), m.group(2) or "lifted"
    t = gen(name, cfg)
    if kind == "STATEMENT":
        head = section(t, "### Original statement", "### Recovered skeleton")
        return "\n".join(l for l in head.split("\n")
                         if not l.startswith(("- config", "- result", "- kernel check"))).rstrip()
    if kind == "RESULT":
        head = section(t, "### Original statement", "### Recovered skeleton")
        return "\n".join(l for l in head.split("\n")
                         if l.startswith(("- config", "- result", "- kernel check")))
    if kind == "SKELETON":
        return section(t, "### Recovered skeleton", "### The `have` boundaries")
    return section(t, "### The `have` boundaries in the original proof term")

def main():
    tdir = os.path.join(here, "templates")
    for fn in sorted(os.listdir(tdir)):
        if not fn.endswith(".md"):
            continue
        name = fn[:-3]
        with open(os.path.join(tdir, fn), encoding="utf-8") as f:
            lines = f.read().split("\n")
        out = "\n".join(expand(name, l) for l in lines)
        with open(os.path.join(here, fn), "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", os.path.join(here, fn))

if __name__ == "__main__":
    sys.exit(main())
