#!/usr/bin/env python3
"""Read a replay compile log; one JSON line per theorem: ok, heartbeats, first error.
usage: replay_log.py FILE.log"""
import json, re, sys
blocks = []; cur = None
for l in open(sys.argv[1]):
    m = re.match(r'BLOCK (\S+)', l)
    if m:
        cur = dict(name=m.group(1), ok=True, heartbeats=None, error=None); blocks.append(cur); continue
    if cur is None: continue
    if re.match(r'[^:]+\.lean:\d+:\d+: error', l):
        cur['ok'] = False
        if cur['error'] is None: cur['error'] = l.split('error', 1)[1].lstrip(':(').strip()[:300]
    elif cur['error'] is not None and len(cur['error']) < 400 and not l.startswith('Used'):
        cur['error'] += ' ' + l.strip()[:200]
    hb = re.search(r'Used (\d+) heartbeats', l)
    if hb: cur['heartbeats'] = int(hb.group(1))
for b in blocks:
    b['ok'] = b['ok'] and b['heartbeats'] is not None
    print(json.dumps(b, ensure_ascii=False))
