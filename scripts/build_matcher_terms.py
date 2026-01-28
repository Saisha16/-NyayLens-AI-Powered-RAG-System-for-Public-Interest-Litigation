#!/usr/bin/env python3
import json
import os
import re
from collections import Counter, defaultdict

import argparse

DATA_PATH = "data/fact2law_dataset.json"
OUT_PATH = "data/matcher_terms.json"

# Map dataset family label -> matcher key used in rag pipeline
FAMILY_TO_KEY = {
    "rape": "64-66",
    "sexual deceit 69": "69",
    "murder": "100-103",
    "kidnapping": "137-139",
    "dowry cruelty": "85-86",
    "assault hurt": "351-355",
    "theft robbery": "303-310",
    "cheating forgery": "318-320",
}

STOP = set("""
  a an the and or to of for by in on with at from into during including until unless
  without within against among between through over under again further then once here
  there when where why how all any both each few more most other some such no nor not
  only own same so than too very can will just don don t should now
""".split())

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z\-]+")


def tokenize(text):
    return [t.lower() for t in TOKEN_RE.findall(text or "") if t]


def family_from_example(ex):
    try:
        q0 = ex.get("retrieval", {}).get("query_variants", [""])[0]
        fam = q0.replace(" case in BNS", "").strip()
        return fam or "unknown"
    except Exception:
        return "unknown"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default=DATA_PATH)
    parser.add_argument("--out", type=str, default=OUT_PATH)
    args = parser.parse_args()

    data = json.load(open(args.data, "r", encoding="utf-8"))

    buckets = defaultdict(list)
    for ex in data:
        fam = family_from_example(ex)
        buckets[fam].append(ex)

    out = {}
    for fam, items in buckets.items():
        key = FAMILY_TO_KEY.get(fam)
        if not key:
            continue
        kw_counter = Counter()
        # collect keywords and query phrases
        for ex in items:
            retr = ex.get("retrieval", {})
            kws = retr.get("keywords", [])
            qvs = retr.get("query_variants", [])
            for w in kws:
                for tok in tokenize(w):
                    if tok not in STOP and len(tok) > 2:
                        kw_counter[tok] += 1
            for q in qvs:
                for tok in tokenize(q):
                    if tok not in STOP and len(tok) > 2:
                        kw_counter[tok] += 1
        # keep top 15 tokens as extra terms
        extra = [w for w, _ in kw_counter.most_common(15)]
        out[key] = {
            "extra_keywords": extra
        }

    os.makedirs(os.path.dirname(args.out) or "data", exist_ok=True)
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote matcher terms to {args.out}")

if __name__ == "__main__":
    main()
