#!/usr/bin/env python3
"""End-to-end tests for the trial harness. Writes only to a temporary directory.

    python3 run_tests.py            # all tests; the browser test is skipped if Chrome is not found
    python3 run_tests.py --chrome /path/to/chrome

This is an organiser's tool: it reads key.json. Standard library only.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
CHROMES = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
           "/Applications/Chromium.app/Contents/MacOS/Chromium",
           "google-chrome", "chromium", "chromium-browser"]
results = []


def check(name, ok, detail=""):
    results.append((name, ok))
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (": " + detail) if detail and not ok else ""))


def run(cmd, stdin=None, cwd=None):
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, cwd=cwd)
    return p.returncode, p.stdout, p.stderr


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def answers_for(order, start, stop, judge):
    """Piped keystrokes for items order[start:stop]; exercises the re-prompts too."""
    lines = []
    for k in range(start, stop):
        j = judge(order[k])
        if k % 7 == 0:
            lines += ["b", "x"]                   # show the brief again, then an invalid key
        lines.append("n" if j == "not-faithful" else "f")
        if k % 5 == 0:
            lines.append("lots")                  # invalid confidence
        lines.append(str(50 + (k % 6) * 10))
        if j == "not-faithful":
            if k % 4 == 0:
                lines.append("")                  # empty reason is refused for not-faithful
            lines.append("differs %d" % k)
        else:
            lines.append("" if k % 2 else "same %d" % k)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--keep", action="store_true", help="keep the temporary directory")
    ap.add_argument("--bank", default=HERE, help="item bank to test (default: the bank next to this script)")
    args = ap.parse_args()
    BANK = os.path.abspath(args.bank)
    tmp = tempfile.mkdtemp(prefix="meaning-trial-test-")
    material = load(os.path.join(BANK, "items.json"))
    key = load(os.path.join(BANK, "key.json"))
    ids = [i["id"] for i in material["items"]]
    n = len(ids)

    # ---- 1. the key is not in anything a reader gets
    kit = os.path.join(tmp, "kit")
    rc, out, err = run([PY, os.path.join(HERE, "build_html.py"), "--bank", BANK, "--kit", kit])
    check("build_html.py builds trial.html and a reader kit", rc == 0, err)
    check("reader kit holds exactly the four reader files",
          sorted(os.listdir(kit)) == sorted(["take_trial.py", "items.json", os.path.basename(material["brief_file"]), "trial.html"]),
          str(os.listdir(kit)))
    leaks = []
    for name in os.listdir(kit):
        text = open(os.path.join(kit, name), encoding="utf-8").read()
        for item_id, k in key["items"].items():
            if k["explanation"][:60] in text:
                leaks.append((name, item_id))
        if name != "take_trial.py" and re.search(r'"(faithful|errorKind|error_kind|explanation|structure)"\s*:', text):
            leaks.append((name, "key field"))
    check("no key text or key field in any reader file", not leaks, str(leaks[:5]))
    for name in ("take_trial.py", "build_html.py", "trial.template.html"):
        src = open(os.path.join(HERE, name), encoding="utf-8").read()
        check("%s does not mention key.json" % name, "key.json" not in src)

    # ---- 2. terminal runner, piped, interrupted and resumed, in a kit with no key present
    log = os.path.join(tmp, "opened.log")
    wrapper = ("import sys, runpy\n"
               "log = open(%r, 'a')\n"
               "def hook(event, a):\n"
               "    if event == 'open':\n"
               "        log.write(str(a[0]) + '\\n'); log.flush()\n"
               "sys.addaudithook(hook)\n"
               "sys.argv = ['take_trial.py'] + sys.argv[1:]\n"
               "runpy.run_path(%r, run_name='__main__')\n" % (log, os.path.join(kit, "take_trial.py")))
    base = [PY, "-c", wrapper, "--reader", "test-human", "--seed", "12345"]
    truth = lambda i: "faithful" if key["items"][i]["faithful"] else "not-faithful"
    # first sitting: background line, Enter to begin, 20 items, then the input ends mid-item
    order = None
    rc, out, err = run(base, stdin="\n".join(["tester", ""]) + "\n", cwd=kit)   # stops before the first item
    check("end of input before the first item saves and exits with code 3", rc == 3, "rc=%s %s" % (rc, err[-300:]))
    resp = os.path.join(kit, "responses", "test-human.json")
    r = load(resp)
    order = r["order"]
    check("order is a seeded permutation, parts kept together",
          sorted(order) == sorted(ids) and r["seed"] == 12345 and order != ids
          and [material["items"][ids.index(i)]["kind"] for i in order] == [i["kind"] for i in material["items"]])
    lines = [""] + answers_for(order, 0, 20, truth) + ["f"]      # Enter to begin; 20 items; item 21 cut off after the judgement
    rc, out, err = run(base[:-2], stdin="\n".join(lines) + "\n", cwd=kit)
    r = load(resp)
    check("interrupted mid-item: 20 answers kept, half-answered item not recorded, exit code 3",
          rc == 3 and len(r["answers"]) == 20 and not r["complete"], "rc=%s n=%d" % (rc, len(r["answers"])))
    lines = [""] + answers_for(order, 20, 30, truth) + ["q"]
    rc, out, err = run(base[:-2], stdin="\n".join(lines) + "\n", cwd=kit)
    r = load(resp)
    check("q saves and stops", rc == 3 and len(r["answers"]) == 30)
    lines = [""] + answers_for(order, 30, n, truth)
    rc, out, err = run(base[:-2], stdin="\n".join(lines) + "\n", cwd=kit)
    r = load(resp)
    check("resumed run finishes with exit code 0", rc == 0, "rc=%s %s" % (rc, err[-300:]))
    a = r["answers"]
    check("answers file: human, complete, every item once, in the recorded order",
          r["reader_type"] == "human" and r["complete"] and r["model"] is None and r["resumed"] == 3
          and [x["id"] for x in a] == order and r["finished"] and r["background"] == "tester")
    check("each answer has judgement, confidence, reason and time",
          all(x["judgement"] in ("faithful", "not-faithful") and 0.5 <= x["confidence"] <= 1.0
              and isinstance(x["reason"], str) and x["seconds"] >= 0 and x["seconds_to_judgement"] >= 0 for x in a)
          and all(x["reason"] for x in a if x["judgement"] == "not-faithful")
          and [x["judgement"] for x in a] == [truth(i) for i in order])
    check("brief re-reads are counted", sum(x["brief_views"] for x in a) == len([k for k in range(n) if k % 7 == 0]))
    rc, out, err = run(base[:-2], stdin="\n", cwd=kit)
    check("a finished answers file is not overwritten", rc != 0 and "already complete" in err and load(resp) == r)
    shutil.copy(os.path.join(BANK, "responses", sorted(os.listdir(os.path.join(BANK, "responses")))[0]),
                os.path.join(kit, "responses", "some-proxy.json"))
    rc, out, err = run([PY, os.path.join(kit, "take_trial.py"), "--reader", "some-proxy"], stdin="\n", cwd=kit)
    check("a proxy reader's file is not overwritten", rc != 0 and "proxy" in err)
    os.remove(os.path.join(kit, "responses", "some-proxy.json"))
    rc, out, err = run([PY, os.path.join(kit, "take_trial.py"), "--reader", "../x"], stdin="\n", cwd=kit)
    check("reader names that are not plain file names are refused", rc != 0)
    opened = [l.strip() for l in open(log)]
    in_kit = sorted({os.path.relpath(p, kit) for p in opened if os.path.abspath(p).startswith(os.path.realpath(kit)) or os.path.abspath(p).startswith(kit)})
    allowed = {"take_trial.py", "items.json", os.path.basename(material["brief_file"]),
               os.path.join("responses", "test-human.json"), os.path.join("responses", "test-human.json.tmp")}
    check("the runner opened only its own script, items.json, the brief and the reader's answers file",
          set(in_kit) <= allowed and "items.json" in in_kit, str(set(in_kit) - allowed))
    check("the runner never opened a file named key.json", not any(os.path.basename(p) == "key.json" for p in opened))

    # ---- 3. browser version, driven through its own controls in headless Chrome
    chrome = args.chrome or next((c for c in CHROMES if os.path.exists(c) or shutil.which(c)), None)
    browser_file = None
    if chrome:
        url = "file://" + os.path.join(kit, "trial.html") + "#selftest"
        rc, out, err = run([chrome, "--headless=new", "--disable-gpu", "--no-first-run",
                            "--user-data-dir=" + os.path.join(tmp, "chrome-profile"),
                            "--virtual-time-budget=8000", "--dump-dom", url])
        title = re.search(r"<title>([^<]*)</title>", out)
        check("trial.html self-test (bad name refused, empty answer refused, stop, reload, resume, finish)",
              bool(title) and title.group(1) == "SELFTEST OK", title.group(1) if title else err[-300:])
        m = re.search(r'<textarea id="out"[^>]*>(.*?)</textarea>', out, re.S)
        if m:
            import html
            b = json.loads(html.unescape(m.group(1)))
            check("browser answers file: human, complete, every item once, seeded order, times recorded",
                  b["reader_type"] == "human" and b["complete"] and sorted(x["id"] for x in b["answers"]) == sorted(ids)
                  and [x["id"] for x in b["answers"]] == b["order"] and b["order"] != ids and isinstance(b["seed"], int)
                  and b["resumed"] == 1 and b["material_sha256"] == r["material_sha256"]
                  and all(x["seconds"] >= 0 and 0.5 <= x["confidence"] <= 1 for x in b["answers"]))
            browser_file = os.path.join(tmp, "selftest-browser.json")
            json.dump(b, open(browser_file, "w"))
        else:
            check("browser answers file found in the page", False)
    else:
        print("SKIP  trial.html self-test: no Chrome found (pass --chrome PATH)")

    # ---- 4. score.py end to end on a copy of the bank with the test readers added
    bank = os.path.join(tmp, "bank")
    os.makedirs(os.path.join(bank, "responses"))
    for name in ("items.json", os.path.basename(material["brief_file"]), "key.json", "item_flags.json", "analyst_notes.md"):
        if os.path.exists(os.path.join(BANK, name)):
            shutil.copy(os.path.join(BANK, name), bank)
    for p in glob.glob(os.path.join(BANK, "responses", "*.json")):
        shutil.copy(p, os.path.join(bank, "responses"))
    rc, out, err = run([PY, os.path.join(HERE, "score.py"), "--bank", bank])
    check("score.py runs on the stored responses", rc == 0, err[-400:])
    before = load(os.path.join(bank, "results.json"))
    check("with no human answers the human section says so",
          "No human readers have taken this trial yet." in open(os.path.join(bank, "REPORT.md")).read())
    shutil.copy(resp, os.path.join(bank, "responses"))
    if browser_file:
        shutil.copy(browser_file, os.path.join(bank, "responses"))
    flagger = dict(r, reader="test-flags-everything",
                   answers=[dict(x, judgement="not-faithful", reason="x") for x in r["answers"]])
    json.dump(flagger, open(os.path.join(bank, "responses", "test-flags-everything.json"), "w"))
    partial = dict(r, reader="test-partial", complete=False, answers=r["answers"][:10])
    json.dump(partial, open(os.path.join(bank, "responses", "test-partial.json"), "w"))
    rc, out, err = run([PY, os.path.join(HERE, "score.py"), "--bank", bank])
    check("score.py runs with human answers added", rc == 0, err[-400:])
    after = load(os.path.join(bank, "results.json"))
    check("proxy results are unchanged by adding human readers", before["proxy"] == after["proxy"])
    hum = {x["reader"]: x for x in after["human"]["readers"]}
    n_bad = sum(1 for k in key["items"].values() if not k["faithful"])
    check("a reader who answers exactly as the key scores all caught, no false alarms",
          hum["test-human"]["all"] == {"caught": n_bad, "unfaithful": n_bad, "false_alarms": 0, "faithful": n - n_bad})
    check("a reader who flags everything scores all caught, all false alarms",
          hum["test-flags-everything"]["all"] == {"caught": n_bad, "unfaithful": n_bad, "false_alarms": n - n_bad, "faithful": n - n_bad})
    check("a partial reader is scored on the items answered", hum["test-partial"]["answered"] == 10
          and hum["test-partial"]["all"]["unfaithful"] + hum["test-partial"]["all"]["faithful"] == 10)
    report = open(os.path.join(bank, "REPORT.md")).read()
    check("report keeps proxy and human readers in separate sections",
          report.index("## Proxy readers") < report.index("## Human readers") and "test-human" in report.split("## Human readers")[1]
          and "test-human" not in report.split("## Human readers")[0].split("## Proxy readers")[1])
    summary = open(os.path.join(bank, "SUMMARY.md")).read()
    known = sorted(ids, key=len, reverse=True)
    check("SUMMARY.md names no item and quotes no key text",
          not any(re.search(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(i), summary) for i in known)
          and not any(k["explanation"][:60] in summary for k in key["items"].values()))
    sys.path.insert(0, HERE)
    import score
    lo, hi = score.wilson(18, 18)
    lo2, hi2 = score.wilson(5, 10)
    check("Wilson interval matches known values", abs(lo - 0.8241) < 5e-4 and hi == 1.0 and abs(lo2 - 0.2366) < 5e-4 and abs(hi2 - 0.7634) < 5e-4)
    check("kappa: identical raters 1, independent-looking raters 0",
          abs(score.cohen_kappa([1, 0, 1, 0], [1, 0, 1, 0]) - 1) < 1e-9 and abs(score.cohen_kappa([1, 1, 0, 0], [1, 0, 1, 0])) < 1e-9
          and abs(score.fleiss_kappa([[1, 1], [0, 0], [1, 1], [0, 0]]) - 1) < 1e-9)
    bad = dict(r, reader="test-bad", answers=[dict(r["answers"][0], id="ZZ99")])
    json.dump(bad, open(os.path.join(bank, "responses", "test-bad.json"), "w"))
    rc, out, err = run([PY, os.path.join(HERE, "score.py"), "--bank", bank])
    check("score.py refuses an answers file that names an unknown item", rc != 0 and "ZZ99" in err)

    failed = [n_ for n_, ok in results if not ok]
    print("\n%d passed, %d failed%s" % (len(results) - len(failed), len(failed), "" if chrome else ", browser test skipped"))
    if args.keep:
        print("kept " + tmp)
    else:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
