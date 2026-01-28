#!/usr/bin/env python3
import json
import re

# Check one failing case in detail
issue = "Near a village fair, the neighbor struck a passerby with a iron rod during a quarrel, causing injuries treated at a local clinic."
issue_lower = issue.lower()

# Current assault pattern
pattern = r'(assault|violence|hurt|injury|beating|attacked|struck.*with|struck.*rod|struck.*bottle)'

# Keywords for assault
keywords = ['assault', 'hurt', 'grievous hurt', 'causing injury', 'violence', 'intentional', 'struck', 'attacked']

print(f"Issue: {issue}")
print(f"\nPattern match: {bool(re.search(pattern, issue_lower))}")

# Check keyword matches
print(f"\nKeyword matches ({len(keywords)} total):")
matches = 0
for kw in keywords:
    if re.search(kw.replace('.', r'\.'), issue_lower):
        print(f"  ✓ '{kw}'")
        matches += 1
    else:
        print(f"  ✗ '{kw}'")

print(f"\nTotal matches: {matches}")
print(f"Min threshold for priority<100: 2")
print(f"Will pass? {matches >= 2}")
