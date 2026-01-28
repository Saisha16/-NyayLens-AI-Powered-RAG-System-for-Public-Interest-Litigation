#!/usr/bin/env python3
import json
import re

chunks = json.load(open("data/legal_chunks.json", "r", encoding="utf-8"))
bns_chunks = [c for c in chunks if "Bhartiya_Nyaya" in c.get("file", "") or "Bhartiya Nyaya Sanhita" in c.get("source", "")]

sections_found = set()

for chunk in bns_chunks:
    text = chunk.get('text', '')
    # Extract section numbers
    for m in re.finditer(r'Section\s+(\d+)|^(\d+)\.', text):
        sec = m.group(1) or m.group(2)
        if sec:
            sections_found.add(sec)

print(f"Sections found in BNS chunks: {sorted([int(s) for s in sections_found if s.isdigit()])}")
