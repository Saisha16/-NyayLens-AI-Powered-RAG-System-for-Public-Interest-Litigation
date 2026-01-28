#!/usr/bin/env python3
import re

tests = [
    ("Near a village fair, the neighbor struck a passerby with a iron rod during a quarrel, causing injuri", "assault"),
    ("At a suburban lane, a shopkeeper allegedly forced himself on the wife, ignoring repeated refusals.", "rape"),
    ("At at a rented room, Two individuals snatched a phone from a commuter and fled on a motorcycle after", "theft"),
]

patterns = {
    "assault": r'(assault|violence|hurt|injury|beating|attacked|struck.*with|struck.*rod)',
    "rape": r'(rape|sexual.*assault|forced.*sex|non-consensual|without consent|forced himself|ignoring refusal)',
    "theft": r'(theft|robbery|dacoity|burglary|stolen|extortion)',
}

for issue, expected_match in tests:
    issue_lower = issue.lower()
    pat = patterns[expected_match]
    m = re.search(pat, issue_lower)
    status = "✓" if m else "✗"
    matched_text = f"('{m.group()}')" if m else "(NO MATCH)"
    print(f"{status} {expected_match}: {matched_text}")
    if not m:
        print(f"   Pattern: {pat}")
        print(f"   Text: {issue_lower}")
