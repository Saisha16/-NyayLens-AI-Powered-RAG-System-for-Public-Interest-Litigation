#!/usr/bin/env python3
import json
import re

chunks = json.load(open("data/legal_chunks.json", "r", encoding="utf-8"))
bns_chunks = [c for c in chunks if "Bhartiya_Nyaya" in c.get("file", "") or "Bhartiya Nyaya Sanhita" in c.get("source", "")]

print(f"Total BNS chunks available: {len(bns_chunks)}\n")

for i, chunk in enumerate(bns_chunks[:5]):
    text = chunk.get('text', '')
    print(f"Chunk {i}:")
    print(f"  Text: {text[:150]}")
    print()
