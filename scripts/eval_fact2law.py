#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import re
from collections import defaultdict, Counter

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.rag_pipeline import _get_bns_sections

import argparse

DATA_PATH = "data/fact2law_dataset.json"
REPORT_PATH = "data/eval_fact2law_report.json"

sec_re = [
    re.compile(r"BNS Section\s+(\d+)"),
    re.compile(r"Section\s+(\d+)"),
    re.compile(r"^(\d+)\.")
]

def extract_section_num(item):
    # item is a predicted section dict from _get_bns_sections
    title = item.get("title", "") or ""
    excerpt = item.get("excerpt", "") or ""
    for r in sec_re:
        m = r.search(title)
        if m:
            return m.group(1)
    for r in sec_re:
        m = r.search(excerpt)
        if m:
            return m.group(1)
    return None


def family_from_example(ex):
    # generator stores first query variant like "<family> case in BNS"
    try:
        q0 = ex.get("retrieval", {}).get("query_variants", [""])[0]
        fam = q0.replace(" case in BNS", "").strip()
        return fam or "unknown"
    except Exception:
        return "unknown"


def eval_dataset(data_path=DATA_PATH, report_path=REPORT_PATH, topk_list=(1,3,5)):
    data = json.load(open(data_path, "r", encoding="utf-8"))
    results = {k: {"hits": 0, "count": 0, "prec": 0.0, "rec": 0.0, "avoid_neg": 0} for k in topk_list}
    fam_stats = defaultdict(lambda: {k: {"hits": 0, "count": 0, "avoid_neg": 0} for k in topk_list})

    detailed = []

    for ex in data:
        issue = ex["issue_summary"]
        true_secs = {s["section_id"] for s in ex.get("applicable_sections", [])}
        neg_secs = {s["section_id"] for s in ex.get("hard_negatives", [])}
        fam = family_from_example(ex)

        preds = _get_bns_sections(issue)
        pred_secs = [extract_section_num(p) for p in preds]
        pred_secs = [p for p in pred_secs if p is not None]

        for k in topk_list:
            topk = pred_secs[:k]
            hit = 1 if any(s in true_secs for s in topk) else 0
            avoid = 1 if all(s not in neg_secs for s in topk) else 0

            results[k]["hits"] += hit
            results[k]["count"] += 1
            results[k]["avoid_neg"] += avoid

            fam_stats[fam][k]["hits"] += hit
            fam_stats[fam][k]["count"] += 1
            fam_stats[fam][k]["avoid_neg"] += avoid

        detailed.append({
            "id": ex.get("id"),
            "family": fam,
            "true": sorted(list(true_secs)),
            "negatives": sorted(list(neg_secs)),
            "pred": pred_secs,
        })

    # finalize metrics
    summary = {}
    for k in topk_list:
        total = results[k]["count"] or 1
        hit_rate = results[k]["hits"] / total
        avoid_rate = results[k]["avoid_neg"] / total
        summary[str(k)] = {
            "hit@k": round(hit_rate, 4),
            "avoid_neg@k": round(avoid_rate, 4),
            "samples": total,
        }

    fam_summary = {}
    for fam, d in fam_stats.items():
        fam_summary[fam] = {}
        for k in topk_list:
            total = d[k]["count"] or 1
            fam_summary[fam][str(k)] = {
                "hit@k": round(d[k]["hits"] / total, 4),
                "avoid_neg@k": round(d[k]["avoid_neg"] / total, 4),
                "samples": total,
            }

    report = {
        "overall": summary,
        "by_family": fam_summary,
        "sampled_details": detailed[:30],
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default=DATA_PATH)
    parser.add_argument("--report", type=str, default=REPORT_PATH)
    args = parser.parse_args()

    rep = eval_dataset(data_path=args.data, report_path=args.report)
    print(json.dumps(rep["overall"], indent=2))
