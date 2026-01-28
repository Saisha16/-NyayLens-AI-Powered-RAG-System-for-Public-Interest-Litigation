"""Constitutional and Legal Reference Database for PIL Generation

Maps topics and issues to relevant Constitutional Articles, Fundamental Rights,
DPSPs, and landmark case laws for proper legal grounding of PILs.
"""

# Fundamental Rights (Part III: Articles 14-32)
FUNDAMENTAL_RIGHTS = {
    "equality": {
        "article": "Article 14",
        "title": "Equality before law",
        "text": "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India."
    },
    "discrimination": {
        "article": "Article 15",
        "title": "Prohibition of discrimination",
        "text": "The State shall not discriminate against any citizen on grounds only of religion, race, caste, sex, place of birth or any of them."
    },
    "equal_opportunity": {
        "article": "Article 16",
        "title": "Equality of opportunity in public employment",
        "text": "There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State."
    },
    "life_liberty": {
        "article": "Article 21",
        "title": "Protection of life and personal liberty",
        "text": "No person shall be deprived of his life or personal liberty except according to procedure established by law. This includes right to clean environment, health, education, and dignified life."
    },
    "education": {
        "article": "Article 21A",
        "title": "Right to Education",
        "text": "The State shall provide free and compulsory education to all children of the age of six to fourteen years in such manner as the State may, by law, determine."
    },
    "exploitation": {
        "article": "Article 23",
        "title": "Prohibition of traffic in human beings and forced labour",
        "text": "Traffic in human beings and begar and other similar forms of forced labour are prohibited and any contravention of this provision shall be an offence punishable in accordance with law."
    },
    "child_labour": {
        "article": "Article 24",
        "title": "Prohibition of employment of children in factories",
        "text": "No child below the age of fourteen years shall be employed to work in any factory or mine or engaged in any other hazardous employment."
    },
    "constitutional_remedies": {
        "article": "Article 32",
        "title": "Right to Constitutional Remedies",
        "text": "The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed."
    }
}

# Directive Principles of State Policy (Part IV: Articles 36-51)
DIRECTIVE_PRINCIPLES = {
    "health": {
        "article": "Article 39(e) & (f)",
        "title": "Protection of workers and children",
        "text": "The State shall direct its policy towards securing that the health and strength of workers, men and women, and the tender age of children are not abused and that citizens are not forced by economic necessity to enter avocations unsuited to their age or strength; and that children are given opportunities and facilities to develop in a healthy manner."
    },
    "nutrition": {
        "article": "Article 47",
        "title": "Duty to raise nutrition and standard of living",
        "text": "The State shall regard the raising of the level of nutrition and the standard of living of its people and the improvement of public health as among its primary duties."
    },
    "environment": {
        "article": "Article 48A",
        "title": "Protection and improvement of environment",
        "text": "The State shall endeavour to protect and improve the environment and to safeguard the forests and wild life of the country."
    },
    "justice": {
        "article": "Article 39A",
        "title": "Equal justice and free legal aid",
        "text": "The State shall secure that the operation of the legal system promotes justice, on a basis of equal opportunity, and shall, in particular, provide free legal aid, by suitable legislation or schemes."
    },
    "early_childhood": {
        "article": "Article 45",
        "title": "Provision for early childhood care and education",
        "text": "The State shall endeavour to provide early childhood care and education for all children until they complete the age of six years."
    }
}

# Topic to Constitutional Provisions Mapping
TOPIC_CONSTITUTIONAL_MAPPING = {
    "environment": {
        "fundamental_rights": ["life_liberty"],
        "directive_principles": ["environment"],
        "relevant_articles": [
            {"article": "Article 51A(g)", "text": "It shall be the duty of every citizen of India to protect and improve the natural environment including forests, lakes, rivers and wild life."}
        ],
        "key_case_laws": [
            "MC Mehta v. Union of India (Oleum Gas Leak Case) - Right to clean environment is part of Article 21",
            "Subhash Kumar v. State of Bihar - Right to pollution-free water and air",
            "Indian Council for Enviro-Legal Action v. Union of India - Polluter pays principle"
        ]
    },
    "health": {
        "fundamental_rights": ["life_liberty"],
        "directive_principles": ["health", "nutrition"],
        "relevant_articles": [],
        "key_case_laws": [
            "Paschim Banga Khet Mazdoor Samity v. State of West Bengal - Right to health care",
            "Consumer Education & Research Centre v. Union of India - Health of workers is fundamental right",
            "Pt. Parmanand Katara v. Union of India - Right to emergency medical aid"
        ]
    },
    "education": {
        "fundamental_rights": ["education", "life_liberty"],
        "directive_principles": ["early_childhood"],
        "relevant_articles": [],
        "key_case_laws": [
            "Mohini Jain v. State of Karnataka - Right to education is a fundamental right",
            "Unni Krishnan v. State of Andhra Pradesh - Right to free education up to 14 years",
            "Society for Unaided Private Schools v. Union of India - RTE Act validation"
        ]
    },
    "women_children": {
        "fundamental_rights": ["equality", "discrimination", "life_liberty", "exploitation", "child_labour"],
        "directive_principles": ["health", "early_childhood"],
        "relevant_articles": [
            {"article": "Article 15(3)", "text": "Nothing in this article shall prevent the State from making any special provision for women and children."}
        ],
        "key_case_laws": [
            "Vishaka v. State of Rajasthan - Sexual harassment at workplace",
            "MC Mehta v. State of Tamil Nadu - Child labour in hazardous industries",
            "Gaurav Jain v. Union of India - Rehabilitation of children of prostitutes"
        ]
    },
    "child_labour": {
        "fundamental_rights": ["child_labour", "exploitation", "life_liberty"],
        "directive_principles": ["health"],
        "relevant_articles": [],
        "key_case_laws": [
            "MC Mehta v. State of Tamil Nadu - Prohibition of child labour in hazardous industries",
            "Bandhua Mukti Morcha v. Union of India - Bonded child labour",
            "People's Union for Democratic Rights v. Union of India - Asiad workers case"
        ]
    },
    "human_trafficking": {
        "fundamental_rights": ["exploitation", "life_liberty"],
        "directive_principles": ["health", "justice"],
        "relevant_articles": [],
        "key_case_laws": [
            "Vishal Jeet v. Union of India - Trafficking of women and children",
            "Gaurav Jain v. Union of India - Prostitution and trafficking",
            "Bachpan Bachao Andolan v. Union of India - Child trafficking and rescue"
        ]
    },
    "corruption": {
        "fundamental_rights": ["equality", "equal_opportunity"],
        "directive_principles": ["justice"],
        "relevant_articles": [],
        "key_case_laws": [
            "Vineet Narain v. Union of India - Jain Hawala Case - CBI autonomy",
            "Common Cause v. Union of India - Appointment of Lokpal",
            "Centre for PIL v. Union of India - 2G Spectrum case - Public trust doctrine"
        ]
    },
    "crime": {
        "fundamental_rights": ["life_liberty", "equality"],
        "directive_principles": ["justice"],
        "relevant_articles": [],
        "key_case_laws": [
            "DK Basu v. State of West Bengal - Custodial violence and arrest guidelines",
            "Nilabati Behera v. State of Orissa - Compensation for custodial death",
            "State of Maharashtra v. Ravikant S. Patil - Fast track courts"
        ]
    },
    "public_health": {
        "fundamental_rights": ["life_liberty"],
        "directive_principles": ["health", "nutrition"],
        "relevant_articles": [],
        "key_case_laws": [
            "CERC v. Union of India - Public health hazards in industries",
            "Bandhua Mukti Morcha v. Union of India - Health and sanitation in work places",
            "Vincent Panikurlangara v. Union of India - Public health and tobacco"
        ]
    },
    "general": {
        "fundamental_rights": ["constitutional_remedies", "life_liberty"],
        "directive_principles": ["justice"],
        "relevant_articles": [],
        "key_case_laws": [
            "SP Gupta v. Union of India - Public Interest Litigation locus standi",
            "Bandhua Mukti Morcha v. Union of India - Epistolary jurisdiction",
            "PUDR v. Union of India - PIL by organization for public cause"
        ]
    }
}

# Additional Constitutional Provisions
ADDITIONAL_PROVISIONS = {
    "article_226": {
        "article": "Article 226",
        "title": "Power of High Courts to issue writs",
        "text": "Every High Court shall have power to issue to any person or authority directions, orders or writs including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari for enforcement of fundamental rights and for any other purpose."
    },
    "article_32": {
        "article": "Article 32",
        "title": "Remedies for enforcement of rights",
        "text": "The Supreme Court shall have power to issue directions or orders or writs for the enforcement of any of the rights conferred by Part III."
    }
}


def retrieve_constitutional_provisions(topics: list, issue_summary: str) -> dict:
    """
    Retrieve relevant constitutional provisions based on topics and issue.
    
    Args:
        topics: List of classified topics for the news article
        issue_summary: Brief summary of the issue
        
    Returns:
        Dictionary containing relevant constitutional references
    """
    provisions = {
        "fundamental_rights": [],
        "directive_principles": [],
        "additional_articles": [],
        "case_laws": [],
        "primary_articles": []
    }
    
    # Collect provisions from all matched topics
    for topic in topics:
        if topic in TOPIC_CONSTITUTIONAL_MAPPING:
            mapping = TOPIC_CONSTITUTIONAL_MAPPING[topic]
            
            # Add fundamental rights
            for fr_key in mapping.get("fundamental_rights", []):
                if fr_key in FUNDAMENTAL_RIGHTS:
                    fr = FUNDAMENTAL_RIGHTS[fr_key]
                    if fr not in provisions["fundamental_rights"]:
                        provisions["fundamental_rights"].append(fr)
                        provisions["primary_articles"].append(fr["article"])
            
            # Add directive principles
            for dp_key in mapping.get("directive_principles", []):
                if dp_key in DIRECTIVE_PRINCIPLES:
                    dp = DIRECTIVE_PRINCIPLES[dp_key]
                    if dp not in provisions["directive_principles"]:
                        provisions["directive_principles"].append(dp)
            
            # Add additional articles
            for article in mapping.get("relevant_articles", []):
                if article not in provisions["additional_articles"]:
                    provisions["additional_articles"].append(article)
            
            # Add case laws
            for case in mapping.get("key_case_laws", []):
                if case not in provisions["case_laws"]:
                    provisions["case_laws"].append(case)
    
    # Always add Article 32 for PIL jurisdiction
    provisions["additional_articles"].append({
        "article": "Article 32",
        "text": "Right to move Supreme Court for enforcement of Fundamental Rights"
    })
    
    return provisions


def get_legal_grounds(topics: list) -> str:
    """
    Generate legal grounds statement for PIL based on topics.
    
    Args:
        topics: List of classified topics
        
    Returns:
        String describing the legal grounds for the PIL
    """
    provisions = retrieve_constitutional_provisions(topics, "")
    
    grounds = []
    
    if provisions["fundamental_rights"]:
        articles = [fr["article"] for fr in provisions["fundamental_rights"]]
        grounds.append(f"Fundamental Rights under {', '.join(articles)}")
    
    if provisions["directive_principles"]:
        articles = [dp["article"] for dp in provisions["directive_principles"]]
        grounds.append(f"Directive Principles under {', '.join(articles)}")
    
    return " and ".join(grounds) if grounds else "Fundamental Rights under Part III"
