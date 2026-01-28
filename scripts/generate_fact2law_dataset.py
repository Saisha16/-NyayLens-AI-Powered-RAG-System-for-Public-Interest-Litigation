#!/usr/bin/env python3
import json
import random
import os
from datetime import datetime

random.seed(42)

CRIME_FAMILIES = [
    {
        "name": "rape",
        "sections": ["64", "65", "66"],
        "title_map": {
            "64": "Rape",
            "65": "Aggravated rape",
            "66": "Related sexual offences"
        },
        "elements": [
            "sexual intercourse or penetration",
            "without consent / coercion",
            "aggravating circumstances (if any)"
        ],
        "signals": ["rape", "sexual assault", "without consent", "forced"],
        "keywords": ["rape", "sexual assault", "without consent", "coercion", "penetration"],
        "confounders": ["promise to marry", "Section 69", "consensual relations"],
        "near_miss": ["69", "351", "352"]
    },
    {
        "name": "sexual_deceit_69",
        "sections": ["69"],
        "title_map": {"69": "Sexual intercourse by employing deceitful means"},
        "elements": [
            "deceitful means or promise to marry",
            "sexual intercourse",
            "not amounting to rape"
        ],
        "signals": ["promise to marry", "deceit", "sexual intercourse", "no force"],
        "keywords": ["promise to marry", "deceitful means", "sexual intercourse", "not amounting to rape"],
        "confounders": ["false document", "cheating 318-320", "rape"],
        "near_miss": ["64", "318", "320"]
    },
    {
        "name": "murder",
        "sections": ["100", "101", "102", "103"],
        "title_map": {
            "100": "Murder",
            "101": "Punishment for murder",
            "102": "Culpable homicide not amounting to murder",
            "103": "Related homicide provisions"
        },
        "elements": [
            "act causing death",
            "intention or knowledge",
            "distinguish murder vs culpable homicide"
        ],
        "signals": ["murder", "killed", "fatal", "homicide"],
        "keywords": ["murder", "intent", "death", "fatal", "homicide"],
        "confounders": ["grievous hurt", "culpable homicide not amounting to murder"],
        "near_miss": ["351", "352", "102"]
    },
    {
        "name": "kidnapping",
        "sections": ["137", "138", "139"],
        "title_map": {
            "137": "Kidnapping",
            "138": "Abduction",
            "139": "Procurement/trafficking related"
        },
        "elements": [
            "taking or enticing",
            "minor or without consent",
            "wrongful confinement or specific purpose"
        ],
        "signals": ["kidnap", "abduct", "minor", "without consent", "confined"],
        "keywords": ["kidnapping", "abduction", "minor", "without consent", "wrongfully confining"],
        "confounders": ["consensual elopement", "custody disputes"],
        "near_miss": ["351", "370"]
    },
    {
        "name": "dowry_cruelty",
        "sections": ["85", "86"],
        "title_map": {
            "85": "Cruelty related to dowry",
            "86": "Dowry-related harassment"
        },
        "elements": [
            "harassment or cruelty",
            "dowry demand context",
            "marital relationship"
        ],
        "signals": ["dowry", "harassment", "cruelty", "wife"],
        "keywords": ["dowry", "harassment", "cruelty", "wife", "husband"],
        "confounders": ["property dispute", "domestic quarrel without dowry"],
        "near_miss": ["351", "318"]
    },
    {
        "name": "assault_hurt",
        "sections": ["351", "352", "353", "354", "355"],
        "title_map": {
            "351": "Assault",
            "352": "Causing hurt",
            "353": "Grievous hurt",
            "354": "Assault with specific intent",
            "355": "Other hurt provisions"
        },
        "elements": [
            "assault or use of force",
            "injury or hurt",
            "any aggravating intent (if any)"
        ],
        "signals": ["assault", "beating", "injury", "hurt"],
        "keywords": ["assault", "hurt", "grievous", "injury", "violence"],
        "confounders": ["self-defense", "verbal abuse only"],
        "near_miss": ["100", "370"]
    },
    {
        "name": "theft_robbery",
        "sections": ["370", "371", "372"],
        "title_map": {
            "370": "Theft",
            "371": "Robbery",
            "372": "Dacoity"
        },
        "elements": [
            "dishonest taking of property",
            "without consent",
            "robbery/dacoity if violence/group present"
        ],
        "signals": ["stolen", "robbery", "dacoity", "extortion"],
        "keywords": ["theft", "stolen", "robbery", "dacoity", "extortion"],
        "confounders": ["lost property", "civil debt"],
        "near_miss": ["318", "351"]
    },
    {
        "name": "cheating_forgery",
        "sections": ["318", "319", "320"],
        "title_map": {
            "318": "Cheating",
            "319": "Forgery",
            "320": "Using forged document"
        },
        "elements": [
            "deception or false representation",
            "inducement to deliver property/act",
            "making/using false document (forgery)"
        ],
        "signals": ["cheated", "forged", "false document", "impersonation"],
        "keywords": ["cheating", "fraud", "forgery", "false document", "dishonestly"],
        "confounders": ["promise to marry", "consumer dispute"],
        "near_miss": ["69", "370"]
    }
]

LOCALITIES = [
    "a busy market", "a village fair", "a suburban lane", "near the bus stand",
    "outside a school", "at a rented room", "in a park", "near the railway station"
]

WEAPONS = ["knife", "stick", "bottle", "iron rod", "firearm"]

NAMES_M = ["the accused", "a 28-year-old man", "the neighbor", "a shopkeeper", "the driver"]
NAMES_F = ["the woman", "a 22-year-old woman", "the wife", "a student", "the complainant"]


def pick(lst, k=1):
    return random.sample(lst, k)


def gen_entities():
    ents = []
    if random.random() < 0.6:
        ents.append(random.choice(["minor", "woman", "man", "neighbor", "husband", "wife"]))
    if random.random() < 0.4:
        ents.append(random.choice(["police", "witness", "shopkeeper", "driver"]))
    return ents


def ex_id(i):
    return f"ex-{i:03d}"


def build_issue_summary(family):
    loc = random.choice(LOCALITIES)
    if family["name"] == "sexual_deceit_69":
        subj = random.choice(NAMES_M) + " allegedly promised marriage to " + random.choice(NAMES_F)
        detail = ", and they engaged in sexual relations without force."
        tail = "Messages later suggested he never intended to marry."
        return f"{subj} at {loc}{detail} {tail}"
    if family["name"] == "rape":
        subj = random.choice(NAMES_M) + " allegedly forced himself on " + random.choice(NAMES_F)
        detail = ", ignoring repeated refusals."
        tail = "Medical report noted injuries consistent with assault."
        return f"At {loc}, {subj}{detail} {tail}"
    if family["name"] == "murder":
        weapon = random.choice(WEAPONS)
        subj = random.choice(NAMES_M) + f" allegedly attacked a victim with a {weapon}"
        tail = "The victim succumbed to injuries on the spot."
        return f"At {loc}, {subj}. {tail}"
    if family["name"] == "kidnapping":
        subj = "A 15-year-old was taken on a motorcycle by a neighbor"
        tail = "without parental consent and kept overnight in a rented room."
        return f"From {loc}, {subj} {tail}"
    if family["name"] == "dowry_cruelty":
        subj = "The wife reported sustained harassment over demands for cash and gold"
        tail = "by her husband and in-laws, escalating to threats."
        return f"At {loc}, {subj} {tail}"
    if family["name"] == "assault_hurt":
        weapon = random.choice(WEAPONS)
        subj = random.choice(NAMES_M) + f" struck a passerby with a {weapon} during a quarrel"
        tail = "causing injuries treated at a local clinic."
        return f"Near {loc}, {subj}, {tail}"
    if family["name"] == "theft_robbery":
        subj = "Two individuals snatched a phone from a commuter"
        tail = "and fled on a motorcycle after issuing threats."
        return f"At {loc}, {subj} {tail}"
    if family["name"] == "cheating_forgery":
        subj = "The complainant alleges the agent used a forged document to secure payment"
        tail = "and later impersonated an official to obtain more."
        return f"From {loc}, {subj} {tail}"
    return f"Incident reported at {loc}."


def applicable_for_family(family):
    secs = []
    # Choose 1-2 applicable sections per family with rationale
    if family["name"] == "sexual_deceit_69":
        secs = ["69"]
    elif family["name"] == "murder":
        secs = ["100"] + (["101"] if random.random() < 0.5 else [])
    elif family["name"] == "rape":
        secs = ["64"] + (["65"] if random.random() < 0.3 else [])
    elif family["name"] == "kidnapping":
        secs = ["137"]
    elif family["name"] == "dowry_cruelty":
        secs = [random.choice(["85", "86"])]
    elif family["name"] == "assault_hurt":
        secs = [random.choice(["351", "352", "353"])]
    elif family["name"] == "theft_robbery":
        secs = [random.choice(["370", "371"]) ]
    elif family["name"] == "cheating_forgery":
        secs = [random.choice(["318", "319", "320"]) ]
    out = []
    for s in secs:
        title = family["title_map"].get(s)
        rationale = {
            "69": "Intercourse induced by promise to marry without intent; no force alleged.",
            "100": "Fatal attack indicating intention/knowledge to cause death.",
            "101": "Sentencing provision linked to murder conviction.",
            "64": "Non-consensual sexual act reported; force/refusal indicated.",
            "65": "Aggravating factors present (e.g., injury/weapon/minor).",
            "137": "Minor taken without guardian consent; overnight confinement.",
            "85": "Sustained harassment connected to dowry demands in marriage.",
            "86": "Cruelty linked with dowry pressure by spouse/relatives.",
            "351": "Assault by use of force during quarrel.",
            "352": "Voluntarily caused hurt; medical treatment taken.",
            "353": "Injuries suggesting grievous hurt.",
            "370": "Dishonest taking of movable property without consent.",
            "371": "Robbery: theft with threat/violence.",
            "372": "Dacoity: group robbery (rare in these facts).",
            "318": "Deception causing delivery of money/act (cheating).",
            "319": "Making a false document (forgery).",
            "320": "Using a forged document as genuine."
        }.get(s, "Applies to the core conduct described.")
        support = {
            "69": "Deceit via promise to marry; intercourse not amounting to rape.",
            "100": "Whoever commits murder shall be punished… (paraphrase)",
            "101": "Punishment prescribed for murder… (paraphrase)",
            "64": "Sexual act without consent/against will… (paraphrase)",
            "65": "Aggravated circumstances for sexual assault… (paraphrase)",
            "137": "Whoever kidnaps by taking from lawful guardianship… (paraphrase)",
            "85": "Cruelty related to dowry demands… (paraphrase)",
            "86": "Harassment for dowry by husband/relatives… (paraphrase)",
            "351": "Assault/force causing apprehension of hurt… (paraphrase)",
            "352": "Voluntarily causing hurt… (paraphrase)",
            "353": "Grievous hurt defined… (paraphrase)",
            "370": "Theft: dishonest taking of property… (paraphrase)",
            "371": "Robbery: theft with threat/instant fear… (paraphrase)",
            "372": "Dacoity: robbery by five or more… (paraphrase)",
            "318": "Cheating by deception inducing delivery… (paraphrase)",
            "319": "Forgery: making a false document… (paraphrase)",
            "320": "Using forged document as genuine… (paraphrase)"
        }.get(s, "Statutory text paraphrase")
        out.append({
            "section_id": s,
            "title": title,
            "support_quote": support[:200],
            "paraphrase": True,
            "rationale": rationale
        })
    return out


def hard_negatives_for_family(family):
    negs = []
    pool = list(set(family["near_miss"]))
    random.shuffle(pool)
    for s in pool[: random.randint(2, 4) ]:
        reason = {
            "64": "No force/lack of consent alleged in facts.",
            "69": "This is not deceit/promise to marry; consent obtained by force instead.",
            "101": "Sentencing section without murder conviction context.",
            "102": "Intent unclear here; differentiated from murder.",
            "351": "Simple assault does not cover fatal outcomes.",
            "370": "No dishonest taking; civil/ownership dispute instead.",
            "318": "No property/inducement deception; it's relational deceit.",
            "320": "No forged document used/made."
        }.get(s, "Element(s) not satisfied by the described facts.")
        negs.append({"section_id": s, "reason_not_applicable": reason})
    return negs


def element_coverage(family, summary):
    snippets = []
    for el in family["elements"][: random.randint(2, len(family["elements"])) ]:
        # pick a short snippet from summary heuristically
        part = random.choice(summary.split(", "))[:120]
        snippets.append({
            "statutory_element": el,
            "fact_snippet": part.strip(" ."),
            "confidence": round(random.uniform(0.7, 0.98), 2)
        })
    return snippets


def retrieval_block(family, summary):
    qv = []
    base = family["keywords"]
    qv.append(f"{family['name'].replace('_', ' ')} case in BNS")
    qv.append(summary.split(".")[0][:80].lower())
    qv.extend(random.sample(base, k=min(3, len(base))))
    qv = [x for x in qv if x]
    return {
        "query_variants": qv[:5],
        "keywords": base[:6],
        "confounders": family["confounders"][:4]
    }


def crime_signals(family):
    return random.sample(family["signals"], k=min(3, len(family["signals"])) )


def build_example(i, family):
    summary = build_issue_summary(family)
    return {
        "id": ex_id(i),
        "issue_summary": summary,
        "entities": gen_entities(),
        "crime_signals": crime_signals(family),
        "applicable_sections": applicable_for_family(family),
        "hard_negatives": hard_negatives_for_family(family),
        "element_coverage": element_coverage(family, summary),
        "retrieval": retrieval_block(family, summary),
        "difficulty": random.choice(["easy", "medium", "hard"]) if random.random() < 0.35 else random.choice(["easy", "medium"])
    }


def allocate_counts(total=150, families=CRIME_FAMILIES):
    n = len(families)
    base = total // n
    rem = total % n
    counts = [base] * n
    # give the remainder to first few families to keep balance
    for idx in range(rem):
        counts[idx] += 1
    return counts


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--total", type=int, default=150, help="Total examples to generate")
    parser.add_argument("--out", type=str, default="data/fact2law_dataset.json", help="Output JSON path")
    args = parser.parse_args()

    total = args.total
    counts = allocate_counts(total)
    out = []
    i = 1
    for fam, cnt in zip(CRIME_FAMILIES, counts):
        for _ in range(cnt):
            out.append(build_example(i, fam))
            i += 1
    # shuffle slightly to mix families
    random.shuffle(out)

    os.makedirs(os.path.dirname(args.out) or "data", exist_ok=True)
    path = args.out
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(out)} examples to {path}")

    # quick validation
    assert len(out) == total, f"Expected {total} examples"
    fam_counts = {}
    for e in out:
        fam = e["retrieval"]["query_variants"][0].split(" case in BNS")[0]
        fam_counts[fam] = fam_counts.get(fam, 0) + 1
    print("By family:", fam_counts)

if __name__ == "__main__":
    main()
