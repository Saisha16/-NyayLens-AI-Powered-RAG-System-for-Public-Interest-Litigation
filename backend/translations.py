"""
Multi-language support for constitutional provisions and legal terms
Currently supports: English (default), Hindi
"""

# Fundamental Rights translations
FUNDAMENTAL_RIGHTS_HI = {
    "Article 14": {
        "en": "Equality before law",
        "hi": "विधि के समक्ष समता"
    },
    "Article 15": {
        "en": "Prohibition of discrimination on grounds of religion, race, caste, sex or place of birth",
        "hi": "धर्म, मूलवंश, जाति, लिंग या जन्म स्थान के आधार पर भेदभाव का निषेध"
    },
    "Article 16": {
        "en": "Equality of opportunity in matters of public employment",
        "hi": "लोक नियोजन के विषय में अवसर की समता"
    },
    "Article 19": {
        "en": "Protection of certain rights regarding freedom of speech etc.",
        "hi": "वाक्-स्वातंत्र्य आदि विषयक कुछ अधिकारों का संरक्षण"
    },
    "Article 21": {
        "en": "Protection of life and personal liberty",
        "hi": "प्राण और दैहिक स्वतंत्रता का संरक्षण"
    },
    "Article 21A": {
        "en": "Right to education",
        "hi": "शिक्षा का अधिकार"
    },
    "Article 23": {
        "en": "Prohibition of traffic in human beings and forced labour",
        "hi": "मानव के दुर्व्यापार और बलात्‌ श्रम का प्रतिषेध"
    },
    "Article 24": {
        "en": "Prohibition of employment of children in factories, etc.",
        "hi": "कारखानों आदि में बालकों के नियोजन का प्रतिषेध"
    }
}

DIRECTIVE_PRINCIPLES_HI = {
    "Article 38": {
        "en": "State to secure a social order for the promotion of welfare of the people",
        "hi": "राज्य लोक कल्याण की अभिवृद्धि के लिए सामाजिक व्यवस्था बनाएगा"
    },
    "Article 39": {
        "en": "Certain principles of policy to be followed by the State",
        "hi": "राज्य द्वारा अनुसरणीय कुछ नीति तत्व"
    },
    "Article 39A": {
        "en": "Equal justice and free legal aid",
        "hi": "समान न्याय और निःशुल्क विधिक सहायता"
    },
    "Article 41": {
        "en": "Right to work, to education and to public assistance in certain cases",
        "hi": "काम, शिक्षा और सार्वजनिक सहायता पाने का अधिकार"
    },
    "Article 48A": {
        "en": "Protection and improvement of environment and safeguarding of forests and wild life",
        "hi": "पर्यावरण का संरक्षण और संवर्धन तथा वन एवं वन्य जीवों की रक्षा"
    }
}

# Legal terms
LEGAL_TERMS_HI = {
    "petition": {
        "en": "Petition",
        "hi": "याचिका"
    },
    "petitioner": {
        "en": "Petitioner",
        "hi": "याचिकाकर्ता"
    },
    "respondent": {
        "en": "Respondent",
        "hi": "प्रतिवादी"
    },
    "fundamental_right": {
        "en": "Fundamental Right",
        "hi": "मौलिक अधिकार"
    },
    "supreme_court": {
        "en": "Supreme Court of India",
        "hi": "भारत का सर्वोच्च न्यायालय"
    },
    "high_court": {
        "en": "High Court",
        "hi": "उच्च न्यायालय"
    },
    "public_interest": {
        "en": "Public Interest Litigation",
        "hi": "जनहित याचिका"
    },
    "constitution": {
        "en": "Constitution of India",
        "hi": "भारत का संविधान"
    },
    "violation": {
        "en": "Violation",
        "hi": "उल्लंघन"
    },
    "relief": {
        "en": "Relief",
        "hi": "राहत"
    },
    "writ": {
        "en": "Writ",
        "hi": "रिट"
    },
    "habeas_corpus": {
        "en": "Habeas Corpus",
        "hi": "बंदी प्रत्यक्षीकरण"
    },
    "mandamus": {
        "en": "Mandamus",
        "hi": "परमादेश"
    },
    "certiorari": {
        "en": "Certiorari",
        "hi": "उत्प्रेषण"
    },
    "prohibition": {
        "en": "Prohibition",
        "hi": "प्रतिषेध"
    },
    "quo_warranto": {
        "en": "Quo Warranto",
        "hi": "अधिकार-पृच्छा"
    }
}

# Issue categories
ISSUE_CATEGORIES_HI = {
    "environmental": {
        "en": "Environmental pollution and destruction",
        "hi": "पर्यावरण प्रदूषण और विनाश"
    },
    "child_rights": {
        "en": "Child rights violation",
        "hi": "बाल अधिकार उल्लंघन"
    },
    "labor": {
        "en": "Labour rights and exploitation",
        "hi": "श्रम अधिकार और शोषण"
    },
    "corruption": {
        "en": "Corruption and transparency",
        "hi": "भ्रष्टाचार और पारदर्शिता"
    },
    "police": {
        "en": "Police misconduct and brutality",
        "hi": "पुलिस दुर्व्यवहार और क्रूरता"
    },
    "discrimination": {
        "en": "Discrimination and inequality",
        "hi": "भेदभाव और असमानता"
    },
    "healthcare": {
        "en": "Right to health and medical negligence",
        "hi": "स्वास्थ्य का अधिकार और चिकित्सा लापरवाही"
    },
    "education": {
        "en": "Right to education",
        "hi": "शिक्षा का अधिकार"
    }
}


def get_translation(text: str, category: str = "legal_terms", lang: str = "hi") -> str:
    """
    Get translation for legal terms, articles, or categories
    
    Args:
        text: English text to translate
        category: One of "legal_terms", "fundamental_rights", "directive_principles", "issue_categories"
        lang: Target language code (currently only "hi" supported)
    
    Returns:
        Translated text if available, otherwise original text
    """
    if lang != "hi":
        return text  # Only Hindi supported for now
    
    lookup = {
        "legal_terms": LEGAL_TERMS_HI,
        "fundamental_rights": FUNDAMENTAL_RIGHTS_HI,
        "directive_principles": DIRECTIVE_PRINCIPLES_HI,
        "issue_categories": ISSUE_CATEGORIES_HI
    }
    
    if category not in lookup:
        return text
    
    # Check if text is a key (e.g., "petition")
    if text.lower() in lookup[category]:
        return lookup[category][text.lower()][lang]
    
    # Check if text is an article reference (e.g., "Article 21")
    if category in ["fundamental_rights", "directive_principles"]:
        if text in lookup[category]:
            return lookup[category][text][lang]
    
    return text  # Return original if not found


def translate_pil_section(section_text: str, lang: str = "hi") -> str:
    """
    Translate key terms in a PIL section to target language
    Useful for bilingual PIL generation
    
    Args:
        section_text: English text from PIL
        lang: Target language code
    
    Returns:
        Text with key legal terms translated (preserves structure)
    """
    if lang != "hi":
        return section_text
    
    translated = section_text
    
    # Replace legal terms
    for key, translations in LEGAL_TERMS_HI.items():
        en_term = translations["en"]
        hi_term = translations["hi"]
        # Case-insensitive replacement
        import re
        translated = re.sub(
            re.escape(en_term), 
            f"{en_term} ({hi_term})", 
            translated, 
            flags=re.IGNORECASE
        )
    
    return translated


def get_bilingual_article_reference(article: str) -> str:
    """
    Returns bilingual reference for constitutional articles
    Example: "Article 21 (अनुच्छेद 21: प्राण और दैहिक स्वतंत्रता का संरक्षण)"
    
    Args:
        article: Article reference like "Article 21"
    
    Returns:
        Bilingual string with Hindi translation
    """
    # Check Fundamental Rights
    if article in FUNDAMENTAL_RIGHTS_HI:
        hi_desc = FUNDAMENTAL_RIGHTS_HI[article]["hi"]
        return f"{article} (अनुच्छेद {article.split()[1]}: {hi_desc})"
    
    # Check Directive Principles
    if article in DIRECTIVE_PRINCIPLES_HI:
        hi_desc = DIRECTIVE_PRINCIPLES_HI[article]["hi"]
        return f"{article} (अनुच्छेद {article.split()[1]}: {hi_desc})"
    
    return article


# Example usage
if __name__ == "__main__":
    print("=== Translation Examples ===\n")
    
    # Legal term translation
    print("1. Legal Terms:")
    print(f"   petition → {get_translation('petition', 'legal_terms')}")
    print(f"   supreme_court → {get_translation('supreme_court', 'legal_terms')}\n")
    
    # Article translation
    print("2. Constitutional Articles:")
    print(f"   Article 21 → {get_translation('Article 21', 'fundamental_rights')}")
    print(f"   Article 48A → {get_translation('Article 48A', 'directive_principles')}\n")
    
    # Bilingual reference
    print("3. Bilingual References:")
    print(f"   {get_bilingual_article_reference('Article 21')}")
    print(f"   {get_bilingual_article_reference('Article 48A')}\n")
    
    # Section translation
    print("4. PIL Section Translation:")
    sample = "The Petitioner approaches this Hon'ble Supreme Court under Article 32 seeking Writ of Mandamus"
    print(f"   Original: {sample}")
    print(f"   Translated: {translate_pil_section(sample)}")
