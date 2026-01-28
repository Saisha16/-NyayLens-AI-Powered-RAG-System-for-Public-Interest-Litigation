"""
Simple Explainable AI module for NyayLens
Provides human-readable explanations for model decisions without heavy dependencies

This module implements lightweight explainability for:
1. Severity scoring decisions
2. Entity extraction confidence
3. Legal reference relevance
4. Topic classification reasoning

With optional LLM-powered analysis for enhanced legal reasoning.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from backend.severity_scoring import CRITICAL_KEYWORDS, HIGH_KEYWORDS, MEDIUM_KEYWORDS

# Optional LLM integration
try:
    from backend.llm_integration import (
        analyze_severity_with_llm,
        explain_legal_grounds_with_llm,
        assess_pil_viability_with_llm
    )
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


@dataclass
class SeverityExplanation:
    """Explanation for severity score decision"""
    score: float
    priority_level: str
    keywords_found: List[Dict[str, Any]]
    population_multipliers: List[str]
    reasoning: str
    confidence: float


@dataclass
class EntityExplanation:
    """Explanation for entity extraction"""
    entity_text: str
    entity_type: str
    confidence: float
    importance_to_case: str


@dataclass
class LegalReferenceExplanation:
    """Explanation for legal reference selection"""
    reference: str
    reference_type: str  # "article", "case_law", "provision"
    relevance_score: float
    matching_phrases: List[str]
    why_selected: str


class SimpleExplainer:
    """Lightweight explainability without additional ML libraries"""
    
    @staticmethod
    def explain_severity(article_text: str, severity_score: float, 
                        keyword_matches: Dict = None) -> SeverityExplanation:
        """
        Generate human-readable explanation for severity score
        
        Args:
            article_text: Original article text
            severity_score: Final normalized score (0-1)
            keyword_matches: Pre-computed keyword matches (optional)
        
        Returns:
            SeverityExplanation with detailed reasoning
        """
        text_lower = article_text.lower()
        keywords_found = []
        
        # Check for critical keywords
        for keyword, score_val in CRITICAL_KEYWORDS.items():
            if keyword.lower() in text_lower:
                keywords_found.append({
                    "keyword": keyword,
                    "category": "CRITICAL",
                    "base_score": score_val
                })
        
        # Check for high keywords
        for keyword, score_val in HIGH_KEYWORDS.items():
            if keyword.lower() in text_lower:
                keywords_found.append({
                    "keyword": keyword,
                    "category": "HIGH",
                    "base_score": score_val
                })
        
        # Check for medium keywords
        for keyword, score_val in MEDIUM_KEYWORDS.items():
            if keyword.lower() in text_lower:
                keywords_found.append({
                    "keyword": keyword,
                    "category": "MEDIUM",
                    "base_score": score_val
                })
        
        # Check for population multipliers
        multipliers = []
        if "minor" in text_lower or "child" in text_lower:
            multipliers.append("Involves minors (1.3x boost)")
        if "mass" in text_lower or "multiple" in text_lower or "thousands" in text_lower:
            multipliers.append("Mass incident (1.25x boost)")
        if "elderly" in text_lower or "senior" in text_lower:
            multipliers.append("Involves elderly (1.2x boost)")
        
        # Determine priority level
        if severity_score >= 0.8:
            priority = "CRITICAL"
        elif severity_score >= 0.6:
            priority = "HIGH"
        elif severity_score >= 0.4:
            priority = "MEDIUM"
        else:
            priority = "LOW"
        
        # Generate reasoning
        reasoning = SimpleExplainer._generate_severity_narrative(
            priority, keywords_found, multipliers, severity_score
        )
        
        # Calculate confidence (based on number of keyword matches)
        confidence = min(1.0, len(keywords_found) * 0.15 + 0.5)
        
        return SeverityExplanation(
            score=severity_score,
            priority_level=priority,
            keywords_found=keywords_found,
            population_multipliers=multipliers,
            reasoning=reasoning,
            confidence=confidence
        )
    
    @staticmethod
    def _generate_severity_narrative(priority: str, keywords_found: List[Dict],
                                     multipliers: List[str], score: float) -> str:
        """Generate human-readable narrative for severity"""
        
        base_msg = f"Priority Level: {priority} (Score: {score:.2f})"
        
        if not keywords_found:
            return f"{base_msg}\n\nNo critical keywords detected. Score based on general context."
        
        # Aggregate keywords by category
        critical = [kw for kw in keywords_found if kw['category'] == 'CRITICAL']
        high = [kw for kw in keywords_found if kw['category'] == 'HIGH']
        medium = [kw for kw in keywords_found if kw['category'] == 'MEDIUM']
        
        narrative = base_msg + "\n\n**Keywords Found:**\n"
        
        if critical:
            kw_list = ", ".join([f"'{kw['keyword']}'" for kw in critical])
            narrative += f"⚠️  CRITICAL: {kw_list}\n"
        
        if high:
            kw_list = ", ".join([f"'{kw['keyword']}'" for kw in high])
            narrative += f"🔴 HIGH: {kw_list}\n"
        
        if medium:
            kw_list = ", ".join([f"'{kw['keyword']}'" for kw in medium])
            narrative += f"🟡 MEDIUM: {kw_list}\n"
        
        if multipliers:
            narrative += f"\n**Multipliers Applied:**\n"
            for mult in multipliers:
                narrative += f"• {mult}\n"
        
        narrative += f"\n**Assessment:**\n"
        
        if priority == "CRITICAL":
            narrative += (
                f"This article contains critical legal violations requiring immediate PIL. "
                f"The presence of severe keywords ({len(critical)} CRITICAL, {len(high)} HIGH) "
                f"combined with {len(multipliers)} vulnerability factors elevates this to top priority."
            )
        elif priority == "HIGH":
            narrative += (
                f"This article describes significant legal issues suitable for PIL filing. "
                f"Keywords include {len(critical)} critical and {len(high)} high-severity terms. "
                f"Recommended for detailed legal analysis."
            )
        elif priority == "MEDIUM":
            narrative += (
                f"This article may warrant PIL consideration subject to deeper investigation. "
                f"While it contains relevant keywords, additional fact-checking is recommended "
                f"before formal filing."
            )
        else:
            narrative += (
                f"This article has lower probability of PIL qualification. "
                f"No critical keywords detected. May be suitable for monitoring."
            )
        
        return narrative
    
    @staticmethod
    def explain_entity_extraction(entity_text: str, entity_type: str, 
                                 confidence: float, context: str = "") -> EntityExplanation:
        """
        Explain why an entity was extracted and its importance
        
        Args:
            entity_text: Extracted entity (e.g., "John Doe", "Mumbai Police")
            entity_type: spaCy NER type (PERSON, ORG, GPE, LAW)
            confidence: spaCy confidence score
            context: Surrounding text context
        
        Returns:
            EntityExplanation with importance assessment
        """
        
        # Assess importance based on type
        importance_mapping = {
            "PERSON": "High - Key party in case",
            "ORG": "High - Potential respondent/defendant",
            "GPE": "Medium - Jurisdiction context",
            "LAW": "Critical - Direct legal reference",
            "PRODUCT": "Low - Product/organization reference",
            "EVENT": "Medium - Relevant incident"
        }
        
        importance = importance_mapping.get(entity_type, "Medium")
        
        return EntityExplanation(
            entity_text=entity_text,
            entity_type=entity_type,
            confidence=confidence,
            importance_to_case=importance
        )
    
    @staticmethod
    def explain_legal_reference(reference: str, relevance_score: float, 
                               matching_phrases: List[str],
                               article_topic: str = "") -> LegalReferenceExplanation:
        """
        Explain why a legal reference was selected
        
        Args:
            reference: Constitutional article, case law, or provision
            relevance_score: Semantic or keyword similarity (0-1)
            matching_phrases: Phrases in article that matched reference
            article_topic: Article's classified topic
        
        Returns:
            LegalReferenceExplanation with matching details
        """
        
        # Determine reference type
        if "Article" in reference:
            ref_type = "article"
        elif "Case" in reference or any(x in reference for x in ["vs", "v."]):
            ref_type = "case_law"
        else:
            ref_type = "provision"
        
        # Generate explanation
        if relevance_score >= 0.7:
            why_selected = f"Strong semantic match ({relevance_score:.0%} similarity)"
        elif relevance_score >= 0.5:
            why_selected = f"Moderate relevance ({relevance_score:.0%} similarity)"
        else:
            why_selected = f"Weak match ({relevance_score:.0%} similarity) - topic-based association"
        
        if matching_phrases:
            why_selected += f". Matching phrases: {', '.join(matching_phrases[:3])}"
        
        return LegalReferenceExplanation(
            reference=reference,
            reference_type=ref_type,
            relevance_score=relevance_score,
            matching_phrases=matching_phrases,
            why_selected=why_selected
        )
    
    @staticmethod
    def generate_pil_explanation_report(article_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive explanation report for PIL generation
        Uses LLM when available for enhanced reasoning, falls back to rule-based
        
        Args:
            article_data: Full article dict with all analysis results
        
        Returns:
            Structured explanation report with AI-powered insights
        """
        article_text = article_data.get('text', '')
        severity_score = article_data.get('severity_score', 0.0)
        legal_sources = article_data.get('legal_sources_used', [])
        
        # Get rule-based severity explanation (always available as fallback)
        severity_exp = SimpleExplainer.explain_severity(
            article_text,
            severity_score
        )

        # Try to enhance with LLM analysis
        llm_severity = None
        llm_legal_grounds = None
        llm_viability = None
        
        if LLM_AVAILABLE:
            try:
                # Run LLM calls in parallel using ThreadPoolExecutor for speed
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    future_severity = executor.submit(analyze_severity_with_llm, article_text, severity_score)
                    future_legal = executor.submit(explain_legal_grounds_with_llm, article_text, legal_sources)
                    future_viability = executor.submit(assess_pil_viability_with_llm, article_text, severity_score, legal_sources)
                    
                    # Wait for all with timeout
                    llm_severity = future_severity.result(timeout=15)
                    llm_legal_grounds = future_legal.result(timeout=15)
                    llm_viability = future_viability.result(timeout=15)
            except Exception as e:
                import traceback
                print(f"LLM enhancement failed: {e}")
                traceback.print_exc()

        # Normalize entities to a list of strings for downstream display
        raw_entities = article_data.get('entities', []) or []
        entity_names = []
        for ent in raw_entities:
            if isinstance(ent, dict):
                name = ent.get('text') or ent.get('name') or ent.get('entity')
                if name:
                    entity_names.append(name)
            elif isinstance(ent, str):
                entity_names.append(ent)
        
        # Build report with LLM enhancements if available
        report = {
            "article_title": article_data.get('title', ''),
            "severity_analysis": {
                "score": severity_exp.score,
                "priority": severity_exp.priority_level,
                "confidence": f"{severity_exp.confidence:.0%}",
                "keywords_found": severity_exp.keywords_found,
                "multipliers": severity_exp.population_multipliers,
                "reasoning": llm_severity.get('reasoning') if llm_severity else severity_exp.reasoning,
                # Add LLM-specific fields if available
                "ai_powered": bool(llm_severity),
                **({"key_violations": llm_severity.get('key_violations', []),
                    "constitutional_concerns": llm_severity.get('constitutional_concerns', []),
                    "vulnerable_groups": llm_severity.get('vulnerable_groups', []),
                    "urgency_assessment": llm_severity.get('urgency_assessment', '')} if llm_severity else {})
            },
            "entity_extraction": {
                "entities_found": len(entity_names),
                "key_parties": entity_names[:5],
                "explanation": "Identified key people, organizations, and locations mentioned in article"
            },
            "legal_references": {
                "total_selected": len(legal_sources),
                "primary_articles": legal_sources[:3],
                "explanation": (llm_legal_grounds.get('overall_reasoning', '') if isinstance(llm_legal_grounds, dict) else "") or "Selected constitutional provisions based on semantic similarity to article content",
                "ai_powered": isinstance(llm_legal_grounds, dict),
                **({"primary_grounds": llm_legal_grounds.get('primary_grounds', []),
                    "filing_strategy": llm_legal_grounds.get('filing_strategy', '')} if isinstance(llm_legal_grounds, dict) else {})
            },
            "pil_viability": {
                "suitable_for_pil": llm_viability.get('suitable_for_pil', severity_exp.priority_level in ["CRITICAL", "HIGH"]) if llm_viability else severity_exp.priority_level in ["CRITICAL", "HIGH"],
                "recommendation": llm_viability.get('recommendation') if llm_viability else (
                    "Recommended for PIL filing" 
                    if severity_exp.priority_level in ["CRITICAL", "HIGH"]
                    else "Consider further investigation before filing"
                ),
                "next_steps": llm_viability.get('next_steps', [
                    "Verify facts with primary sources",
                    "Consult with legal expert",
                    "Draft detailed statement of facts",
                    "Finalize constitutional grounds"
                ]) if llm_viability else [
                    "Verify facts with primary sources",
                    "Consult with legal expert",
                    "Draft detailed statement of facts",
                    "Finalize constitutional grounds"
                ],
                "ai_powered": bool(llm_viability),
                **({"viability_rating": llm_viability.get('viability_rating', ''),
                    "strengths": llm_viability.get('strengths', []),
                    "challenges": llm_viability.get('challenges', []),
                    "timeline_urgency": llm_viability.get('timeline_urgency', '')} if llm_viability else {})
            }
        }
        
        return report


# FastAPI integration (add to backend/main.py)
"""
@app.get("/explain-severity")
async def explain_severity(article_id: int):
    article = get_article(article_id)
    explainer = SimpleExplainer()
    explanation = explainer.explain_severity(article.text, article.severity_score)
    return explanation.__dict__

@app.get("/explain-pil/{article_id}")
async def explain_pil(article_id: int):
    article = get_article(article_id)
    article_data = {
        'title': article.title,
        'text': article.text,
        'severity_score': article.severity_score,
        'entities': article.entities,
        'legal_sources_used': article.legal_sources
    }
    explainer = SimpleExplainer()
    report = explainer.generate_pil_explanation_report(article_data)
    return report
"""
