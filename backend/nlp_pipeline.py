import spacy
from backend.config import config


nlp = spacy.load("en_core_web_sm")


def extract_issue(article_text: str):
    """Extract entities and issue summary with optional LLM enhancement."""
    # Try LLM extraction if enabled
    if config.ENABLE_LLM_CLASSIFICATION:
        try:
            from backend.llm_integration import extract_legal_issues_llm
            llm_result = extract_legal_issues_llm(article_text)
            if llm_result:
                return llm_result
        except Exception:
            pass  # Fall back to spaCy
    
    # Fallback: spaCy-based extraction
    doc = nlp(article_text)

    entities = []
    for ent in doc.ents:
        if ent.label_ in ["GPE", "ORG", "PERSON", "LAW"]:
            entities.append(ent.text)

    issue_summary = article_text[:600]

    return {
        "issue_summary": issue_summary,
        "entities": list(set(entities))
    }
