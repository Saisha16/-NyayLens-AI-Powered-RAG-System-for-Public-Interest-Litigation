"""Generate comprehensive PIL draft with constitutional references."""

from datetime import datetime
import re


def _improve_text_formatting(text: str) -> str:
    """Fix broken words then add proper spacing."""
    import re
    # Step 1: Fix broken words from corrupted PDFs
    text = re.sub(r'\b([A-Z])\s+([A-Z]{2,})\b', r'\1\2', text)
    text = re.sub(r'\b([a-z]{1,3})\s+([a-z]{2,})\b', r'\1\2', text)
    text = text.replace(' IN ARY', 'INARY').replace('f or med', 'formed')
    text = text.replace('in tended', 'intended').replace('the reto', 'thereto')
    
    # Step 2: Add proper spacing
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([.!?;:,])([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([\)\]])([A-Za-z0-9])', r'\1 \2', text)
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
    
    # Step 3: Cleanup
    text = re.sub(r' +', ' ', text)
    return text.strip()


def generate_pil(issue: dict, legal_sections: list, topics: list = None, news_title: str = "", severity_score: float = 0.0) -> str:
    """Generate a PIL draft using the official concise template."""

    summary = issue.get("issue_summary", "") if isinstance(issue, dict) else str(issue)
    entities = issue.get("entities", []) if isinstance(issue, dict) else []

    # Classify legal sections by category for templating
    fundamental_rights = [s for s in legal_sections if s.get("category") == "Fundamental Right"]
    directive_principles = [s for s in legal_sections if s.get("category") == "Directive Principle"]
    case_laws = [s for s in legal_sections if s.get("category") == "Case Precedent"]
    other_provisions = [s for s in legal_sections if s.get("category") not in {
        "Fundamental Right",
        "Directive Principle",
        "Case Precedent",
    }]

    severity_label = (
        "HIGH" if severity_score > 0.7 else
        "MEDIUM" if severity_score > 0.4 else
        "MODERATE"
    )
    topics_display = ", ".join(topics) if topics else "General Public Interest"

    facts_section = f"""{news_title if news_title else "Public Interest Matter"}

Severity: {severity_label} (Score: {severity_score:.2f})
Topics: {topics_display}

{summary[:1500]}

{"Parties Involved: " + ", ".join(entities[:10]) if entities else ""}"""

    # Build legal grounds with detailed analysis
    legal_grounds = "The present Public Interest Litigation is filed on the following legal grounds:\n\n"

    legal_grounds += "FUNDAMENTAL RIGHTS VIOLATED:\n"
    if fundamental_rights:
        for i, fr in enumerate(fundamental_rights, 1):
            legal_grounds += f"{i}. {fr.get('source', 'Unknown')} - {fr.get('title', '')}\n"
            # Apply text formatting to excerpts
            excerpt = _improve_text_formatting(fr.get('excerpt', ''))
            legal_grounds += f"   {excerpt[:250]}...\n"
            # Add legal analysis
            legal_grounds += f"   Application: The facts reveal a clear violation of this constitutional guarantee, necessitating immediate judicial intervention.\n\n"
    else:
        legal_grounds += "Article 21 - Right to Life and Personal Liberty\n"
        legal_grounds += "   Application: The right to life is the most fundamental of all rights and encompasses the right to live with dignity, security, and protection from violence.\n\n"

    if directive_principles:
        legal_grounds += "DIRECTIVE PRINCIPLES OF STATE POLICY:\n"
        for i, dp in enumerate(directive_principles, 1):
            legal_grounds += f"{i}. {dp.get('source', 'Unknown')} - {dp.get('title', '')}\n"
            # Apply text formatting to excerpts
            excerpt = _improve_text_formatting(dp.get('excerpt', ''))
            legal_grounds += f"   {excerpt[:250]}...\n"
            legal_grounds += f"   Relevance: The State has failed in its constitutional obligation to ensure protection and welfare.\n\n"

    # Combine case laws and uploaded legal documents (BNS, BNSS, etc.) with analysis
    all_case_precedents = case_laws + other_provisions
    
    # Always show case precedents section (with defaults if none retrieved)
    legal_grounds += "APPLICABLE STATUTORY PROVISIONS AND PRECEDENTS:\n"
    
    if all_case_precedents:
        for i, case in enumerate(all_case_precedents, 1):
            # Show source for uploaded documents (BNS, BNSS, etc.)
            source_label = case.get('source', '')
            if case.get('category') == 'Uploaded Legal Document':
                legal_grounds += f"{i}. {source_label}\n"
                # Apply text formatting to legal documents
                excerpt = _improve_text_formatting(case.get('excerpt', ''))
                legal_grounds += f"   Provision: {excerpt[:350]}...\n"
                
                # Add specific legal analysis based on source
                if 'Bhartiya Nyaya' in source_label or 'BNS' in source_label:
                    legal_grounds += f"   Legal Analysis: The facts squarely attract the provisions of the Bhartiya Nyaya Sanhita, 2023. The accused's actions constitute cognizable offenses requiring strict prosecution and exemplary punishment to serve as a deterrent.\n\n"
                elif 'Nagarik Suraksha' in source_label or 'BNSS' in source_label:
                    legal_grounds += f"   Procedural Relevance: The investigative procedures and safeguards under this enactment must be strictly followed to ensure fair and expeditious justice.\n\n"
                else:
                    legal_grounds += f"   Applicability: This provision is directly relevant to the facts and circumstances of the present case.\n\n"
            else:
                # Apply text formatting to case laws
                excerpt = _improve_text_formatting(case.get('excerpt', ''))
                legal_grounds += f"{i}. {excerpt[:350]}...\n"
                legal_grounds += f"   Ratio: This precedent establishes binding legal principles applicable to the instant case.\n\n"
    else:
        # Show default case precedents when none retrieved
        default_precedents = [
            "1. S.P. Gupta v. Union of India – Expanded locus standi in Public Interest Litigation\n   Ratio: This landmark judgment expanded access to justice by recognizing the concept of public interest litigation.\n\n",
            "2. Bandhua Mukti Morcha v. Union of India – Epistolary jurisdiction and access to justice\n   Ratio: The Supreme Court recognized its power to entertain applications by letter for enforcement of fundamental rights.\n\n",
            "3. People's Union for Democratic Rights v. Union of India – PIL for enforcement of fundamental rights\n   Ratio: This case established that PIL is a powerful tool for protection of fundamental rights in matters of public importance.\n\n",
            "4. D.K. Basu v. State of West Bengal – Custodial Violence Guidelines\n   Ratio: Establishes binding guidelines to prevent custodial violence and safeguard fundamental rights of arrested persons.\n\n",
            "5. Nilabati Behera v. State of Orissa – Compensation for Custodial Death\n   Ratio: Recognizes the principle of constitutional compensation for violation of fundamental rights under public law.\n\n"
        ]
        legal_grounds += ''.join(default_precedents)

    prayer = (
        "It is most respectfully prayed that this Hon'ble Court may be pleased to:\n\n"
        "a) Take judicial notice of this matter of urgent public importance;\n"
        "b) Issue appropriate writs, orders, or directions in the nature of mandamus;\n"
        "c) Direct the Respondents to take immediate and effective action;\n"
        "d) Pass such other orders as deemed fit in the interest of justice;\n"
        "e) Award costs of this petition."
    )

    pil_text = f"""IN THE HON'BLE HIGH COURT OF __________

PUBLIC INTEREST LITIGATION

Petitioner:
A public-spirited citizen

Respondents:
State of __________ and relevant authorities

Facts of the Case:
{facts_section}

Legal Grounds:
{legal_grounds}

Prayer:
{prayer}

Filed in public interest.

Date: {datetime.now().strftime('%B %d, %Y')}
"""

    return pil_text.strip()
