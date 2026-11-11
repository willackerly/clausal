"""The sentences of the bank: every Rule line the tool compiles, from the V4 trial and from the fixtures."""
import json, re, sys
from pathlib import Path
import mutate
SENT = mutate.SENT
sys.path.insert(0, str(SENT))
import units

def pool():
    out, seen = [], set()
    for u, t in units.UNITS.items():
        if t not in seen:
            seen.add(t); out.append({"source": "v4:" + u, "text": t})
    for f in sorted((SENT / "work" / "slice" / "features").glob("*.feature")):
        if f.name == "v4_authored.feature":
            continue
        for line in f.read_text().splitlines():
            m = re.match(r"\s*Rule: (.+)", line)
            if m and m.group(1).strip() not in seen:
                seen.add(m.group(1).strip()); out.append({"source": "fixture:" + f.name, "text": m.group(1).strip()})
    return out

if __name__ == "__main__":
    rows = []
    for n, s in enumerate(pool()):
        e = mutate.faithful_echo(s["text"])
        ks = {}
        if e:
            for k in mutate.KINDS:
                m, what = mutate.mutated_echo(s["text"], k)
                if m: ks[k] = what
        rows.append((n, s, e is not None, ks))
        print(f"{n:>2} {'ok ' if e else 'NO '} {s['source']:<28} {s['text'][:110]}\n      " + "; ".join(f"{k}" for k in ks))
    print(len(rows), sum(r[2] for r in rows))
