#!/usr/bin/env python3
import json
import sys
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.rag_pipeline import _get_bns_sections

# Analyze all failing cases and extract signal gaps per family
data = json.load(open("data/fact2law_dataset.json", "r", encoding="utf-8"))

family_fails = defaultdict(list)
family_signals = defaultdict(set)

for ex in data:
    issue = ex["issue_summary"]
    true_secs = {s["section_id"] for s in ex.get("applicable_sections", [])}
    crime_signals = ex.get("crime_signals", [])
    
    preds = _get_bns_sections(issue)
    pred_nums = []
    for p in preds:
        title = p.get("title", "")
        m = re.search(r'(\d+)', title)
        if m:
            pred_nums.append(m.group(1))
    
    pred_set = set(pred_nums)
    
    # Extract family from query variant
    fam = ex.get("retrieval", {}).get("query_variants", [""])[0].split(" case in BNS")[0]
    
    if not any(s in pred_set for s in true_secs):
        family_fails[fam].append({
            "issue": issue[:100],
            "true": list(true_secs),
            "signals": crime_signals
        })
        for sig in crime_signals:
            family_signals[fam].add(sig)

# Print summary
print("=== FAILING CASES BY FAMILY ===\n")
for fam in sorted(family_fails.keys()):
    fails = family_fails[fam]
    sigs = family_signals[fam]
    print(f"{fam.upper()}: {len(fails)} failures")
    print(f"  Key signals present: {', '.join(sorted(sigs))}")
    for case in fails[:2]:  # Show first 2 failing cases
        print(f"    - {case['issue']}")
        print(f"      True: {case['true']}, Signals: {case['signals']}")
    print()
