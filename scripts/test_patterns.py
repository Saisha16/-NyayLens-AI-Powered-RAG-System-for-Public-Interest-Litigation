#!/usr/bin/env python3
import re

# Test issue from failing case
issue = "From a village fair, A 15-year-old was taken on a motorcycle by a neighbor without parental consent and kept overnight in a rented room."

patterns = {
    "kidnap": r'(kidnap|abduct|taken.*without|without.*consent.*taken|unlawful confinement|wrongfully|forcibly)',
    "rape": r'(rape|sexual.*assault|forced.*sex|non-consensual|without consent|forced himself|ignoring refusal)',
    "fraud": r'(fraud|cheating|forgery|impersonation|dishonestly|forged.*document)',
    "assault": r'(assault|violence|hurt|injury|beating|attacked|struck.*with|struck.*rod)',
}

issue_lower = issue.lower()

for name, pat in patterns.items():
    match = re.search(pat, issue_lower)
    if match:
        print(f"✓ {name}: MATCHED ('{match.group()}')")
    else:
        print(f"✗ {name}: NO MATCH")
