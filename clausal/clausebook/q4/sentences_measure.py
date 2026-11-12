import json, sys, os
sys.path.insert(0, os.getcwd())
authors = json.load(open("authors.json"))["authors"]
import rewordings
import try_compile
lines = [r["rule"] for a in authors for r in a["rules"]]
_, _, res = try_compile.compile_lines(lines, name="q4_measure")
ret = [x for x in res if not x["compiled"] and "no longer accepts" in x["message"]]
print(f"as written: {sum(x['compiled'] for x in res)} of {len(res)} compile; refused as written with a retired form or shape: {len(ret)}")
R = rewordings.R
texts = [(k, v) for k, v in R.items()]
def text_of(v):
    return v.get("text") if isinstance(v, dict) else (v[0] if isinstance(v, (list, tuple)) else v)
rew = [(k, text_of(v)) for k, v in texts if text_of(v)]
_, _, res2 = try_compile.compile_lines([t for _, t in rew], name="q4_rewordings")
ok = sum(x["compiled"] for x in res2)
ret2 = [x for x in res2 if not x["compiled"] and "no longer accepts" in x["message"]]
offered = [x for x in ret2 if "write the clause as" in (x["hint"] or "")]
other = [x for x in res2 if not x["compiled"] and x not in ret2]
print(f"expert rewordings (rewordings.py): {len(rew)} with a text; {ok} compile; {len(ret2)} refused for a retired form or shape ({len(offered)} with the clause to write); {len(other)} refused otherwise: {sorted(set(x['status'] for x in other))}")
