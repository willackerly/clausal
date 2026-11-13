#!/usr/bin/env python3
"""Write clausebook/REVIEW-SHEET.md: every entry of the core book in a form a person can read and
attest. Generated; rerun after the book changes:  python3 clausebook/review_sheet.py"""
import yaml
from pathlib import Path
HERE = Path(__file__).parent
d = yaml.safe_load((HERE / "core.yaml").read_text())
def cell(x):
    if x is None: return ""
    if isinstance(x, list): x = "<br>".join(str(i) for i in x)
    return str(x).replace("|", "\\|").replace("\n", " ")
out = ["# Review sheet: the core Clausebook", "",
       "Generated from `clausebook/core.yaml` by `clausebook/review_sheet.py`. One row per entry.", "",
       "**What reviewing an entry means.** Read \"How it is written\" as an ordinary reader would, read \"What the tool takes it to mean\", and decide whether they are the same claim. The Lean column is what is actually proved; the definitions are in `lean/Frames/Core.lean` and `lean/Frames/Frames.lean`. `python3 -m clausal show \"<a sentence using the entry>\"` prints which calls a sentence covers and an allowed and a forbidden case.", "",
       "**To record your review of one entry** (run from `clausal/`; the id is in the first column):", "",
       "    python3 -m clausal attest <id> --act reviewed --as human:<your-id> --name \"<Your Name>\" --scope \"read the form, the echo and the Lean definition\"", "",
       "A record is tied to the entry's text as it is now; if the entry changes, the record is void. A model's record never counts as a person's. Entries you doubt: do not attest; note the id and why.", ""]
pieces = d.get("pieces", [])
for kind, title, note in (("frame", "Frames", "The logical shapes a rule can have. Start here: these carry the most meaning."),
                          ("modifier", "Modifiers", "Words that narrow, combine or compare.")):
    rows = [p for p in pieces if p.get("kind") == kind]
    out += [f"## {title} ({len(rows)})", "", note, "", "| id | How it is written | What the tool takes it to mean | Lean |", "|---|---|---|---|"]
    for p in rows:
        forms = []
        for key, label in (("vp_forms", "in a Rule"), ("then_forms", "in a Then step"), ("claim_forms", "as a claim"), ("subject_forms", "on the subject"), ("forms", ""), ("not_forms", "negated")):
            for f in p.get(key) or []: forms.append(f"{f}" + (f" *({label})*" if label else ""))
        dflt = ("<br>*defaults: " + ", ".join(p["defaults"]) + "*") if p.get("defaults") else ""
        out.append(f"| `{p['id']}` | {cell(forms)} | {cell(p.get('echo'))}{dflt} | `{cell(p.get('lean'))}` |")
    out.append("")
other = [p for p in pieces if p.get("kind") not in ("frame", "modifier")]
if other:
    out += [f"## Other pieces ({len(other)})", "", "| id | kind | How it is written | Meaning | Lean |", "|---|---|---|---|---|"]
    for p in other: out.append(f"| `{p['id']}` | {p.get('kind')} | {cell(p.get('forms'))} | {cell(p.get('echo'))} | `{cell(p.get('lean'))}` |")
    out.append("")
out += [f"## Defaults ({len(d.get('defaults', []))})", "", "What every sentence means unless it says otherwise. These are the fail-closed choices.", "", "| id | Text |", "|---|---|"]
dfl = d.get("defaults", [])
items = dfl.items() if isinstance(dfl, dict) else [(e.get("id"), e.get("text") or e.get("echo") or {k: v for k, v in e.items() if k != "id"}) if isinstance(e, dict) else (e, "") for e in dfl]
for k, v in items:
    out.append(f"| `{k}` | {cell(v if not isinstance(v, dict) else (v.get('text') or v.get('echo') or v))} |")
out += ["", f"## Coverage ({len(d.get('coverage', []))})", "", "Which calls a claim is about.", "", "| id | Covers | Lean |", "|---|---|---|"]
for e in d.get("coverage", []): out.append(f"| `{e['id']}` | {cell(e.get('covers'))} | `{cell(e.get('lean'))}` |")
out += ["", f"## Grammar ({len(d.get('grammar', []))})", "", "| id | How it is written | Meaning |", "|---|---|---|"]
for e in d.get("grammar", []): out.append(f"| `{e['id']}` | {cell(e.get('forms'))} | {cell(e.get('echo'))} |")
n = len(pieces) + len(d.get("defaults", [])) + len(d.get("coverage", [])) + len(d.get("grammar", []))
out += ["", f"Entries on this sheet: {n}. The other books (`ledger.yaml` and the `local/` books) hold project words and are reviewed by whoever owns that project."]
(HERE / "REVIEW-SHEET.md").write_text("\n".join(out) + "\n")
print("entries:", n)
