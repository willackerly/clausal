#!/usr/bin/env python3
"""Take a meaning trial in a terminal.

    python3 take_trial.py --reader NAME

Shows the brief, then one item at a time in an order shuffled for this reader
(the seed and the order are recorded). For each item it records a judgement,
a confidence, a free-text reason and the time taken. Progress is saved after
every item, so the trial can be stopped (q, Ctrl-C, closing the terminal) and
resumed by running the same command again.

This program reads exactly three kinds of file: items.json, the brief named in
it, and the reader's own answers file. It contains no code that reads the
answer key and gives no feedback on whether an answer is right.

Standard library only; Python 3.8 or later.
"""
import argparse
import datetime
import hashlib
import json
import os
import random
import re
import shutil
import sys
import textwrap
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RESPONSE_SCHEMA = "meaning-trial-response-v1"
ITEMS_SCHEMA = "meaning-trial-items-v1"
SHUFFLE = "python-random-shuffle-per-part-v1"
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


class Stop(Exception):
    """The reader stopped (q, Ctrl-C or end of input)."""


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_material(bank_dir):
    items_path = os.path.join(bank_dir, "items.json")
    with open(items_path, "rb") as f:
        items_bytes = f.read()
    material = json.loads(items_bytes.decode("utf-8"))
    if material.get("schema") != ITEMS_SCHEMA:
        sys.exit("items.json: unexpected schema %r" % material.get("schema"))
    brief_name = os.path.basename(material["brief_file"])
    with open(os.path.join(bank_dir, brief_name), "rb") as f:
        brief_bytes = f.read()
    sha = hashlib.sha256(items_bytes + b"\n" + brief_bytes).hexdigest()
    return material, brief_bytes.decode("utf-8"), sha


def make_order(material, seed):
    """Parts in the bank's order; items shuffled within each part."""
    rng = random.Random(seed)
    order = []
    for part in material["parts"]:
        ids = [i["id"] for i in material["items"] if i["kind"] == part["kind"]]
        rng.shuffle(ids)
        order.extend(ids)
    return order


def save(path, record):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def width():
    return max(40, min(100, shutil.get_terminal_size((88, 24)).columns - 2))


def wrap(text, indent=""):
    out = []
    for line in text.split("\n"):
        if not line.strip():
            out.append("")
            continue
        out.extend(textwrap.wrap(line, width=width(), initial_indent=indent,
                                 subsequent_indent=indent, break_long_words=False,
                                 break_on_hyphens=False) or [""])
    return "\n".join(out)


def rule(char="-"):
    return char * width()


def ask(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        raise Stop()


def clear(enabled):
    if enabled:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def show_brief(brief, material):
    print(rule("="))
    print(material.get("title", "Meaning trial"))
    print(rule("="))
    print()
    print(wrap(brief))
    print()
    print(rule())
    print(wrap(material["instructions"]))
    print(rule())


def parse_confidence(text):
    """Accepts 50..100 (percent, '%' allowed) or a fraction such as 0.8."""
    t = text.rstrip("%").strip()
    try:
        v = float(t)
    except ValueError:
        return None
    if "." in t and 0.0 <= v <= 1.0 and not text.endswith("%"):
        return round(v, 4)
    if 0.0 <= v <= 100.0:
        return round(v / 100.0, 4)
    return None


def run_item(item, part, n, total, brief, material, use_clear):
    clear(use_clear)
    print(rule("="))
    print("%s, item %d of %d" % (part["title"], n, total))
    print(wrap(part["question"]))
    print(rule("="))
    print()
    print(part["first_label"] + ":")
    print(wrap(item["first"], "  "))
    print()
    print(part["second_label"] + ":")
    print(wrap(item["second"], "  "))
    print()
    t0 = time.monotonic()
    brief_views = 0
    while True:
        a = ask("Faithful? [f = faithful, n = not faithful, b = show the brief again, q = save and stop] ").lower()
        if a in ("f", "faithful"):
            judgement = "faithful"
            break
        if a in ("n", "not-faithful", "not faithful"):
            judgement = "not-faithful"
            break
        if a == "b":
            brief_views += 1
            print()
            show_brief(brief, material)
            print()
            continue
        if a in ("q", "quit"):
            raise Stop()
        print("  Please type f, n, b or q.")
    t1 = time.monotonic()
    while True:
        a = ask("How sure are you? [50 = coin flip ... 100 = certain] ")
        if a.lower() in ("q", "quit"):
            raise Stop()
        confidence = parse_confidence(a)
        if confidence is not None:
            break
        print("  Please type a number from 50 to 100.")
    while True:
        if judgement == "not-faithful":
            a = ask("What differs? (one or two sentences) ")
        else:
            a = ask("Reason (one or two sentences; Enter to skip) ")
        if a or judgement == "faithful":
            reason = a
            break
        print("  Please say briefly what differs.")
    t2 = time.monotonic()
    return {"id": item["id"], "judgement": judgement, "confidence": confidence, "reason": reason,
            "seconds": round(t2 - t0, 1), "seconds_to_judgement": round(t1 - t0, 1),
            "brief_views": brief_views}


def main():
    ap = argparse.ArgumentParser(description="Take a meaning trial. Stop at any time; run the same command to resume.")
    ap.add_argument("--reader", required=True, help="your name or a pseudonym (letters, digits, - _ .)")
    ap.add_argument("--bank", default=HERE, help="directory holding items.json and the brief (default: next to this script)")
    ap.add_argument("--responses-dir", default=None, help="where to write the answers file (default: BANK/responses)")
    ap.add_argument("--seed", type=int, default=None, help="shuffle seed (default: chosen at random and recorded)")
    ap.add_argument("--background", default=None, help="one line about your background (asked if omitted)")
    ap.add_argument("--no-clear", action="store_true", help="do not clear the screen between items")
    args = ap.parse_args()

    if not NAME_RE.match(args.reader):
        sys.exit("--reader must be 1-64 characters: letters, digits, '-', '_' or '.', starting with a letter or digit")
    material, brief, sha = load_material(args.bank)
    items = {i["id"]: i for i in material["items"]}
    parts = {p["kind"]: p for p in material["parts"]}
    out_dir = args.responses_dir or os.path.join(args.bank, "responses")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, args.reader + ".json")
    use_clear = sys.stdout.isatty() and sys.stdin.isatty() and not args.no_clear

    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            record = json.load(f)
        if record.get("reader_type") != "human":
            sys.exit("%s belongs to a %s reader; choose another --reader name" % (path, record.get("reader_type")))
        if record.get("complete"):
            sys.exit("%s is already complete. To take the trial again, use a different --reader name." % path)
        if record.get("material_sha256") != sha:
            sys.exit("%s was started on a different version of the items; use a different --reader name." % path)
        if args.seed is not None and args.seed != record.get("seed"):
            sys.exit("%s was started with seed %s; omit --seed to resume." % (path, record.get("seed")))
        record["resumed"] = record.get("resumed", 0) + 1
        resumed = True
    else:
        seed = args.seed if args.seed is not None else int.from_bytes(os.urandom(4), "big")
        record = {
            "schema": RESPONSE_SCHEMA,
            "bank": material["bank"],
            "material_sha256": sha,
            "reader": args.reader,
            "reader_type": "human",
            "model": None,
            "background": args.background,
            "presentation": "terminal (take_trial.py), one item at a time",
            "shuffle": SHUFFLE,
            "seed": seed,
            "order": make_order(material, seed),
            "started": now(),
            "finished": None,
            "complete": False,
            "resumed": 0,
            "answers": [],
        }
        resumed = False

    order = record["order"]
    done = {a["id"] for a in record["answers"]}
    try:
        clear(use_clear)
        show_brief(brief, material)
        print()
        print(wrap("There are %d items. You can stop at any time with q or Ctrl-C and resume later by running "
                   "the same command. You will not be told whether your answers are right. Please do not look "
                   "anything up or discuss the items with other readers." % len(order)))
        print()
        if resumed:
            print("Resuming: %d of %d items already answered." % (len(done), len(order)))
        if record.get("background") is None:
            record["background"] = ask("In one line, your background (for example 'backend engineer', 'product manager'; Enter to skip): ")
        save(path, record)
        ask("Press Enter to begin. ")
        for n, item_id in enumerate(order, 1):
            if item_id in done:
                continue
            item = items[item_id]
            answer = run_item(item, parts[item["kind"]], n, len(order), brief, material, use_clear)
            record["answers"].append(answer)
            done.add(item_id)
            save(path, record)
            print()
    except Stop:
        save(path, record)
        print(wrap("Stopped with %d of %d items answered. Your answers so far are saved in %s. "
                   "Run the same command to carry on." % (len(done), len(order), path)))
        return 3

    record["finished"] = now()
    record["complete"] = True
    save(path, record)
    clear(use_clear)
    print(rule("="))
    print(wrap("Finished: %d items answered. Thank you. Your answers file is:" % len(order)))
    print("  " + path)
    print(wrap("Please send that file to the person running the trial."))
    print(rule("="))
    return 0


if __name__ == "__main__":
    sys.exit(main())
