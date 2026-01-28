#!/usr/bin/env python3
import json
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.rag_pipeline import _get_bns_sections

# Test assault case
issue = "Near a village fair, the neighbor struck a passerby with a iron rod during a quarrel, causing injuries treated at a local clinic."

preds = _get_bns_sections(issue)
print(f"Issue: {issue[:80]}\n")
print(f"Returned {len(preds)} sections:")
for p in preds:
    print(f"  - {p['title']} (from: {p['source']})")
    print(f"    Excerpt: {p['excerpt'][:100]}")

print("\nExpected: Section 353 (Grievous Hurt)")
