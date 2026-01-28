#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.rag_pipeline import _get_bns_sections

# Pick a few failing cases to debug
failing = []
data = json.load(open("data/fact2law_dataset.json", "r", encoding="utf-8"))

for ex in data[:20]:  # Check first 20 examples
    issue = ex["issue_summary"]
    true_secs = {s["section_id"] for s in ex.get("applicable_sections", [])}
    
    preds = _get_bns_sections(issue)
    pred_nums = []
    for p in preds:
        title = p.get("title", "")
        # Extract number from "BNS Section XXX"
        import re
        m = re.search(r'(\d+)', title)
        if m:
            pred_nums.append(m.group(1))
    
    pred_set = set(pred_nums)
    
    if not any(s in pred_set for s in true_secs):
        failing.append({
            "id": ex["id"],
            "issue": issue[:100],
            "true": sorted(list(true_secs)),
            "pred": sorted(list(pred_set)),
        })

print(f"Failing cases (first 20 checked): {len(failing)}")
for case in failing[:5]:
    print(json.dumps(case, indent=2))
