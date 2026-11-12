"""In a private copy of trials/sentences: the expert rewordings (rewordings.py) that the batch refuses, rewritten by
following the refusals ("write the clause as: ..."), and their Lean compared with the Lean recorded from the copy
that holds the compiler before the batch. usage: sent_migrate.py dump|check FILE"""
import json, os, re, sys
sys.path.insert(0, os.getcwd())
import rewordings
mode, path = sys.argv[1], os.path.abspath(sys.argv[2])
import try_compile
text_of = lambda v: v.get("text")
rew = [(k, text_of(v)) for k, v in rewordings.R.items() if text_of(v)]
def comp(lines):
    return try_compile.compile_lines(lines, name="q4_migrate")[2]
if mode == "dump":
    res = comp([t for _, t in rew])
    json.dump({k: x.get("lean") for (k, _), x in zip(rew, res)}, open(path, "w"))
    print("dumped", sum(x["compiled"] for x in res), "of", len(res))
else:
    before = json.load(open(path))
    same = moved = stuck = 0
    for k, t in rew:
        line, steps = t, 0
        while True:
            x = comp([line])[0]
            if x["compiled"] or steps > 8:
                break
            m = re.search(r': "(.*?)" is written in a way', x["message"])
            h = re.search(r'write the clause as: "(.*?)"\n', x["hint"] + "\n")
            if not (m and h):
                break
            old, new = m.group(1), h.group(1)
            i = line.lower().find(old.lower())
            if i < 0:
                break
            new = new[0].upper() + new[1:] if line[i].isupper() else new
            line, steps = line[:i] + new + line[i + len(old):], steps + 1
        if steps == 0:
            continue
        moved += 1
        ok = x["compiled"] and x["lean"].split(":=", 1)[1] == before[k].split(":=", 1)[1]
        same += ok
        stuck += not x["compiled"]
        print(("SAME LEAN " if ok else "DIFFERENT " if x["compiled"] else "STUCK     ") + f"{k} ({steps} clauses rewritten): {line}")
    print(f"{moved} rewordings needed rewriting; {same} compile to the Lean they had before; {moved - same - stuck} compile to other Lean; {stuck} could not be rewritten by following the refusals")
