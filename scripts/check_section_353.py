#!/usr/bin/env python3
import json
import re

chunks = json.load(open("data/legal_chunks.json", "r", encoding="utf-8"))
bns_chunks = [c for c in chunks if "Bhartiya_Nyaya" in c.get("file", "") or "Bhartiya Nyaya Sanhita" in c.get("source", "")]

print(f"Total BNS chunks: {len(bns_chunks)}")

# Search for section 353
found = 0
for chunk in bns_chunks:
    text = chunk.get('text', '')
    if re.search(r'Section\s+353|^353\.', text):
        found += 1
        print(f"Found Section 353:")
        print(f"  Text: {text[:200]}")
        break

if found == 0:
    print("Section 353 NOT FOUND in BNS chunks")
    
    # Try to find related hurt sections
    for num in [351, 352, 353, 354, 355]:
        for chunk in bns_chunks:
            text = chunk.get('text', '')
            if re.search(rf'Section\s+{num}|^{num}\.', text):
                print(f"Found Section {num}: {text[:80]}")
                break
