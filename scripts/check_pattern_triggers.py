#!/usr/bin/env python3
import re
import json

data = json.load(open("data/fact2law_dataset.json", "r", encoding="utf-8"))

patterns_test = {
    "assault": r'(assault|violence|hurt|injury|beating|attacked|struck.*with|struck.*rod|struck.*bottle)',
    "rape": r'(rape|sexual.*assault|forced.*sex|non-consensual|without consent|forced himself|ignoring refusal)',
    "dowry": r'(dowry|cruelty.*wife|harassment.*marriage|bride.*burning|in-laws|sustained harassment)',
    "theft": r'(theft|robbery|dacoity|burglary|stolen|extortion|snatched)',
    "cheating": r'(fraud|cheating|forgery|impersonation|dishonestly|forged.*document|impersonate)',
}

for pname, pat in patterns_test.items():
    matches = 0
    for ex in data:
        fam = ex.get("retrieval", {}).get("query_variants", [""])[0].split(" case in BNS")[0]
        if pname.replace('_', ' ') in fam.lower():
            issue = ex["issue_summary"].lower()
            if re.search(pat, issue):
                matches += 1
    
    print(f"{pname}: {matches} / 18-19 pattern matches")
