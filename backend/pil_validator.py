"""PIL citation format validator and SC/HC filing requirements checker.

Ensures generated PILs meet Supreme Court and High Court standards.
"""

from typing import List, Dict, Tuple
import re


class PILValidator:
    """Validate PIL document format and citations."""
    
    # Required sections for SC/HC PIL
    REQUIRED_SECTIONS = [
        "In the Supreme Court of India",
        "Public Interest Litigation",
        "The Petitioner",
        "The Respondent",
        "Constitutional Provisions",
        "Prayer",
    ]
    
    # Valid citation formats
    CITATION_PATTERNS = {
        "article": r"Article\s+\d+[A-Z]?(?:\s*\([a-z0-9]+\))?",  # Article 21, Article 14(1)
        "case": r"[A-Z][a-zA-Z\s&]+v\.?\s+[A-Z][a-zA-Z\s&]+\s*\(\d{4}\)",  # Vishaka v. State (1997)
        "statute": r"[A-Z][a-zA-Z\s,]+Act,?\s+\d{4}",  # Environment Protection Act, 1986
    }
    
    # SC/HC filing requirements
    FILING_REQUIREMENTS = {
        "sc_article_32": {
            "jurisdiction": "Supreme Court",
            "article": "Article 32",
            "grounds": "Fundamental Rights violation",
            "required_elements": ["FR violation", "Constitutional provision", "Public interest"],
        },
        "hc_article_226": {
            "jurisdiction": "High Court",
            "article": "Article 226",
            "grounds": "FR violation or other legal rights",
            "required_elements": ["Legal rights violation", "Constitutional/statutory provision"],
        }
    }
    
    def validate_structure(self, pil_text: str) -> Tuple[bool, List[str]]:
        """Check if PIL contains all required sections."""
        errors = []
        
        for section in self.REQUIRED_SECTIONS:
            if section not in pil_text:
                errors.append(f"Missing section: {section}")
        
        return len(errors) == 0, errors
    
    def validate_citations(self, pil_text: str) -> Tuple[bool, List[str]]:
        """Validate citation formats."""
        errors = []
        
        # Check for at least one constitutional article
        article_matches = re.findall(self.CITATION_PATTERNS["article"], pil_text, re.IGNORECASE)
        if not article_matches:
            errors.append("No constitutional articles cited")
        
        # Check citation format consistency
        for match in article_matches:
            if not re.match(r"Article\s+\d+", match):
                errors.append(f"Malformed article citation: {match}")
        
        # Check for case law citations (optional but recommended)
        case_matches = re.findall(self.CITATION_PATTERNS["case"], pil_text)
        if len(case_matches) == 0:
            errors.append("Warning: No case law precedents cited (recommended)")
        
        return len(errors) == 0, errors
    
    def check_filing_requirements(self, pil_text: str, jurisdiction: str = "sc") -> Dict:
        """Check if PIL meets SC/HC filing requirements."""
        req_key = "sc_article_32" if jurisdiction.lower() == "sc" else "hc_article_226"
        requirements = self.FILING_REQUIREMENTS[req_key]
        
        met_requirements = []
        missing_requirements = []
        
        for req in requirements["required_elements"]:
            # Simple keyword check (can be enhanced with NLP)
            if any(keyword in pil_text.lower() for keyword in req.lower().split()):
                met_requirements.append(req)
            else:
                missing_requirements.append(req)
        
        return {
            "jurisdiction": requirements["jurisdiction"],
            "article": requirements["article"],
            "grounds": requirements["grounds"],
            "met_requirements": met_requirements,
            "missing_requirements": missing_requirements,
            "compliant": len(missing_requirements) == 0,
        }
    
    def format_citation(self, citation_type: str, citation_text: str) -> str:
        """Format citations according to legal standards."""
        if citation_type == "article":
            # Ensure "Article" is capitalized and properly spaced
            match = re.match(r"article\s*(\d+[a-z]?)", citation_text.lower())
            if match:
                return f"Article {match.group(1)}"
        
        elif citation_type == "case":
            # Format case name properly
            parts = citation_text.split("v.")
            if len(parts) == 2:
                petitioner = parts[0].strip().title()
                respondent = parts[1].strip().title()
                return f"{petitioner} v. {respondent}"
        
        return citation_text
    
    def generate_compliance_report(self, pil_text: str, jurisdiction: str = "sc") -> str:
        """Generate full compliance report for PIL."""
        report = ["=== PIL Compliance Report ===\n"]
        
        # Structure validation
        struct_valid, struct_errors = self.validate_structure(pil_text)
        report.append(f"Structure: {'✓ Valid' if struct_valid else '✗ Invalid'}")
        for error in struct_errors:
            report.append(f"  - {error}")
        
        # Citation validation
        cite_valid, cite_errors = self.validate_citations(pil_text)
        report.append(f"\nCitations: {'✓ Valid' if cite_valid else '⚠ Issues'}")
        for error in cite_errors:
            report.append(f"  - {error}")
        
        # Filing requirements
        filing_check = self.check_filing_requirements(pil_text, jurisdiction)
        report.append(f"\nFiling Requirements ({filing_check['jurisdiction']}):")
        report.append(f"  Jurisdiction: {filing_check['article']}")
        report.append(f"  Grounds: {filing_check['grounds']}")
        report.append(f"  Status: {'✓ Compliant' if filing_check['compliant'] else '✗ Non-compliant'}")
        
        if filing_check["missing_requirements"]:
            report.append("  Missing:")
            for req in filing_check["missing_requirements"]:
                report.append(f"    - {req}")
        
        return "\n".join(report)


# Singleton instance
pil_validator = PILValidator()
