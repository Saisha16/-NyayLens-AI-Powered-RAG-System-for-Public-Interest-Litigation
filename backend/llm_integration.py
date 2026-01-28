"""LLM integration for enhanced issue summarization and legal analysis using OpenAI/Claude.

Provides AI-powered summarization and legal reasoning as an alternative to rule-based methods.
Falls back gracefully if API keys are not configured.
"""

from __future__ import annotations

import os
import json
from typing import Optional, Dict, List, Any
from backend.config import config
from backend.logger import logger

# Try to import OpenAI (optional dependency)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None


def summarize_with_llm(text: str, max_length: int = 200, model: str = "gpt-3.5-turbo") -> Optional[str]:
    """
    Generate AI-powered summary using OpenAI.
    
    Args:
        text: Article text to summarize
        max_length: Maximum summary length in words
        model: OpenAI model to use
    
    Returns:
        Summary string or None if LLM unavailable
    """
    if not OPENAI_AVAILABLE:
        logger.warning("OpenAI not available; install with: pip install openai")
        return None
    
    api_key = os.getenv("OPENAI_API_KEY") or config.OPENAI_API_KEY
    if not api_key:
        logger.info("No OpenAI API key configured; skipping LLM summarization")
        return None
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        prompt = f"""Summarize the following news article in {max_length} words or less, focusing on:
1. The main issue or violation
2. Who is affected
3. Key legal/constitutional concerns

Article:
{text[:2000]}  # Limit input to avoid token limits

Summary:"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a legal analyst summarizing news for PIL generation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_length * 2,  # Rough token estimate
            temperature=0.3,  # Lower temperature for factual summaries
        )
        
        summary = response.choices[0].message.content.strip()
        logger.info(f"LLM summary generated ({len(summary)} chars)")
        return summary
    
    except Exception as e:
        logger.error(f"LLM summarization failed: {e}")
        return None


def extract_legal_issues_llm(text: str) -> Optional[dict]:
    """
    Extract legal issues and entities using LLM for better accuracy.
    
    Args:
        text: Article text
    
    Returns:
        Dict with issue_summary, entities, and topics or None
    """
    if not OPENAI_AVAILABLE:
        return None
    
    api_key = os.getenv("OPENAI_API_KEY") or config.OPENAI_API_KEY
    if not api_key:
        return None
    
    try:
        # Support OpenRouter (sk-or-...) keys by switching base_url
        if api_key.startswith("sk-or-"):
            client = openai.OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            model_name = "openai/gpt-4o-mini"
        else:
            client = openai.OpenAI(api_key=api_key)
            model_name = "gpt-4o-mini"
        
        prompt = f"""Analyze this news article for Public Interest Litigation:

Article:
{text[:1500]}

Extract:
1. Issue Summary (2-3 sentences)
2. Named Entities (people, organizations, locations)
3. Topics (from: crime, corruption, health, education, environment, women_children, human_trafficking, public_health)

Format as JSON:
{
  "issue_summary": "...",
  "entities": ["...", "..."],
  "topics": ["...", "..."]
}"""
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a legal analyst. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        logger.info(f"LLM extracted issues for {len(result.get('topics', []))} topics")
        return result
    
    except Exception as e:
        logger.error(f"LLM issue extraction failed: {e}")
        return None


def analyze_severity_with_llm(text: str, severity_score: float) -> Optional[Dict[str, Any]]:
    """
    Generate AI-powered explanation for severity score with legal reasoning.
    
    Args:
        text: Article text
        severity_score: Calculated severity score (0-1)
    
    Returns:
        Dict with reasoning, priority, confidence, and legal_concerns
    """
    if not OPENAI_AVAILABLE:
        return None
    
    api_key = os.getenv("OPENAI_API_KEY") or config.OPENAI_API_KEY
    if not api_key:
        return None
    
    try:
        # Support OpenRouter API (sk-or-v1-*) 
        if api_key.startswith("sk-or-"):
            client = openai.OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            client = openai.OpenAI(api_key=api_key)
        
        priority_label = "CRITICAL" if severity_score > 0.7 else "HIGH" if severity_score > 0.4 else "MEDIUM"
        
        prompt = f"""As a legal expert, analyze this news article for Public Interest Litigation severity.

Article:
{text[:1200]}

Current Severity Score: {severity_score:.2f}/1.0 (Priority: {priority_label})

Provide a detailed reasoning explaining:
1. Why this score was assigned (what legal violations/concerns justify it)
2. What constitutional or fundamental rights are at stake
3. The urgency level and why immediate PIL is needed (or not)
4. Any vulnerable populations affected that increase severity

Format as JSON:
{{
  "reasoning": "2-3 sentence explanation of severity score based on legal violations and rights at stake",
  "priority_level": "{priority_label}",
  "confidence_percent": 75,
  "key_violations": ["violation 1", "violation 2"],
  "constitutional_concerns": ["Article 21 violation", "etc"],
  "vulnerable_groups": ["minors", "women", "etc"] or [],
  "urgency_assessment": "immediate/high/moderate",
  "pil_viability": "strong/moderate/weak"
}}"""
        
        # Use appropriate model based on API provider
        model = "openai/gpt-4o-mini" if api_key.startswith("sk-or-") else "gpt-4o-mini"
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert Indian constitutional lawyer analyzing cases for PIL filing. Be concise and legally precise."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        logger.info(f"LLM severity analysis generated with {result.get('confidence_percent')}% confidence")
        return result
    
    except Exception as e:
        logger.error(f"LLM severity analysis failed: {e}")
        return None


def explain_legal_grounds_with_llm(text: str, legal_sections: List[Dict]) -> Optional[Dict[str, Any]]:
    """
    Generate AI explanation for why specific constitutional articles/laws were selected.
    
    Args:
        text: Article text
        legal_sections: List of selected legal references
    
    Returns:
        Dict with selection reasoning and relevance scores
    """
    if not OPENAI_AVAILABLE:
        return None
    
    api_key = os.getenv("OPENAI_API_KEY") or config.OPENAI_API_KEY
    if not api_key:
        return None
    
    try:
        # Support OpenRouter API
        if api_key.startswith("sk-or-"):
            client = openai.OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            model = "openai/gpt-4o-mini"
        else:
            client = openai.OpenAI(api_key=api_key)
            model = "gpt-4o-mini"
        
        # Extract article numbers
        articles = []
        for section in legal_sections[:5]:
            # Handle both dict and string formats
            source = section.get('source', '') if isinstance(section, dict) else str(section)
            if 'Article' in source:
                articles.append(source)
        
        prompt = f"""As a constitutional law expert, explain why these legal provisions were selected for this case.

Case Summary:
{text[:1000]}

Selected Legal Provisions:
{chr(10).join(articles[:5])}

For each provision, briefly explain:
1. Why it's relevant to this specific case
2. What right/principle it protects that's violated here
3. How strong the connection is (relevance score 0-100)

Format as JSON:
{{
  "overall_reasoning": "1-2 sentences on overall legal strategy",
  "provisions": [
    {{
      "article": "Article 21",
      "why_relevant": "brief explanation",
      "relevance_score": 95
    }}
  ],
  "primary_grounds": ["main constitutional ground 1", "ground 2"],
  "filing_strategy": "brief tactical note on PIL approach"
}}"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert Indian constitutional lawyer. Be precise and legally accurate."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        logger.info(f"LLM legal grounds explanation generated for {len(articles)} provisions")
        return result
        
    except Exception as e:
        logger.error(f"LLM legal grounds explanation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def assess_pil_viability_with_llm(text: str, severity_score: float, legal_sections: List[Dict]) -> Optional[Dict[str, Any]]:
    """
    Use LLM to assess whether this case is suitable for PIL filing.
    
    Args:
        text: Article text
        severity_score: Calculated severity
        legal_sections: Selected legal references
    
    Returns:
        Dict with viability assessment, recommendations, and next steps
    """
    if not OPENAI_AVAILABLE:
        return None
    
    api_key = os.getenv("OPENAI_API_KEY") or config.OPENAI_API_KEY
    if not api_key:
        return None
    
    try:
        # Support OpenRouter API
        if api_key.startswith("sk-or-"):
            client = openai.OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            model = "openai/gpt-4o-mini"
        else:
            client = openai.OpenAI(api_key=api_key)
            model = "gpt-4o-mini"
        
        prompt = f"""As a senior advocate, assess if this case is suitable for Public Interest Litigation (PIL).

Case Summary:
{text[:1000]}

Severity Score: {severity_score:.2f}/1.0

PIL Requirements:
- Must involve public interest (not private grievance)
- Must show constitutional/fundamental rights violation
- Must demonstrate state/authority failure
- Should have broader societal impact

Assess:
1. Is this suitable for PIL? (Yes/No/Marginal)
2. What are the strengths of this case?
3. What are potential challenges/weaknesses?
4. Recommended next steps for filing

Format as JSON:
{{
  "suitable_for_pil": true/false,
  "viability_rating": "strong/moderate/weak",
  "recommendation": "Recommended for PIL filing" or reason why not,
  "strengths": ["strength 1", "strength 2"],
  "challenges": ["challenge 1", "challenge 2"],
  "next_steps": ["step 1", "step 2", "step 3"],
  "timeline_urgency": "immediate/within 1 week/within 1 month",
  "additional_evidence_needed": ["evidence type 1", "etc"] or []
}}"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a senior advocate experienced in PIL matters before High Courts and Supreme Court of India."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        logger.info(f"LLM PIL viability assessment: {result.get('viability_rating')}")
        return result
    
    except Exception as e:
        logger.error(f"LLM PIL viability assessment failed: {e}")
        return None

