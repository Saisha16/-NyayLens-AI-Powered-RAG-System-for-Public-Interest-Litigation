"""
LaTeX-based PDF generator for PIL documents
Generates professional LaTeX-formatted PDFs with proper formatting and typography
"""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


class LatexPDFGenerator:
    """Generate professional PDFs using LaTeX template"""
    
    def __init__(self):
        """Initialize LaTeX PDF generator"""
        self.latex_template = r"""
\documentclass[12pt]{article}

% Packages
\usepackage[a4paper,margin=1in]{geometry}
\usepackage{setspace}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{ragged2e}

% Settings
\setstretch{1.5}
\setlength{\parindent}{0pt}
\titleformat{\section}{\bfseries\uppercase}{\thesection.}{1em}{}

% Custom commands for better formatting
\newcommand{\vs}{\vspace{1em}}
\newcommand{\vss}{\vspace{0.5em}}

\begin{document}

%(content)s

\end{document}
"""

    def escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters in text"""
        if not text:
            return text
        
        latex_special_chars = {
            '\\': r'\textbackslash{}',
            '#': r'\#',
            '$': r'\$',
            '%': r'\%',
            '&': r'\&',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
        }
        
        result = text
        # Must process backslash first
        for char, replacement in sorted(latex_special_chars.items(), 
                                       key=lambda x: len(x[0]), 
                                       reverse=True):
            if char != '\\':
                result = result.replace(char, replacement)
        
        return result

    def build_pil_latex(self, pil_dict: Dict[str, Any]) -> str:
        """Build LaTeX content from PIL dictionary"""
        
        content_parts = []
        
        # Header
        content_parts.append(r"""
\begin{center}
    \textbf{IN THE HON'BLE SUPREME COURT OF INDIA}\\
    \textbf{(ORIGINAL JURISDICTION)}\\[1em]
    \textbf{PUBLIC INTEREST LITIGATION}\\
    \textbf{UNDER ARTICLE 32 OF THE CONSTITUTION OF INDIA}
\end{center}

\vs

\textbf{Date of Filing:} """ + self.escape_latex(pil_dict.get('date_of_filing', 'January 26, 2026')) + r"""

\vs

\textbf{IN THE MATTER OF:}

\vss

A Public-Spirited Citizen,\\
Acting bona fide in public interest\\
\textbf{...Petitioner}

\vs

\begin{center}
    \textbf{VERSUS}
\end{center}

\vss

\begin{enumerate}[label=\arabic*.]
    \item Union of India, Through the Secretary
    \item State Government, Through the Chief Secretary
    \item Other concerned authorities\\
    \textbf{...Respondents}
\end{enumerate}

\vs

\section*{Subject Matter}
""")
        
        # Subject matter
        issue = pil_dict.get('issue', '')
        severity = pil_dict.get('severity_score', '')
        nature = pil_dict.get('nature_of_issue', '')
        
        if issue:
            content_parts.append(r"\textbf{Issue:} " + self.escape_latex(issue) + r" \\ ")
        if severity:
            content_parts.append(r"\textbf{Severity Assessment:} " + self.escape_latex(str(severity)) + r" \\ ")
        if nature:
            content_parts.append(r"\textbf{Nature of Issue:} " + self.escape_latex(nature) + r" \\ ")
        
        content_parts.append(r"""
\vs

\section{Facts of the Case}

\begin{enumerate}
""")
        
        # Facts
        facts = pil_dict.get('facts', [])
        if facts:
            if isinstance(facts, str):
                facts = [facts]
            for fact in facts:
                if fact.strip():
                    content_parts.append(r"    \item " + self.escape_latex(fact.strip()) + "\n")
        else:
            content_parts.append(r"    \item Reports indicate a matter of significant public interest.")
        
        content_parts.append(r"""
\end{enumerate}

\vs

\section{Grounds for Filing the Petition}

\subsection*{A. Violation of Fundamental Rights}

\textbf{Article 21 – Right to Life and Personal Liberty}

No person shall be deprived of his life or personal liberty except according to procedure 
established by law. The arbitrary or unjust state action violates the core essence of 
Article 21, which includes the right to dignity and due process.

\textbf{Article 32 – Right to Constitutional Remedies}

Article 32 guarantees the right to approach this Hon'ble Court for enforcement of 
fundamental rights. The present petition is maintainable as it raises serious 
constitutional concerns of public importance.

\subsection*{B. Directive Principles of State Policy}

\textbf{Article 39A – Equal Justice and Free Legal Aid}

The State is constitutionally obligated to ensure access to justice and protection 
of vulnerable persons against arbitrary state action.

\section*{C. Relevant Case Precedents and Statutory Provisions}

\setlength{\parskip}{6pt}
""")
        
        # Add case precedents
        precedents = pil_dict.get('relevant_case_precedents', [])
        if precedents and isinstance(precedents, list):
            for i, precedent in enumerate(precedents, 1):
                if precedent.strip() and not precedent.startswith('[Case precedents'):
                    # Try to parse structured precedent if available
                    if isinstance(precedent, dict):
                        case_name = precedent.get('case_name', f'Case {i}')
                        subject = precedent.get('subject', 'Constitutional Law')
                        ratio = precedent.get('ratio_decidendi', precedent.get('ratio', ''))
                        content_parts.append(r"\subsection*{" + str(i) + r". \textit{" + self.escape_latex(case_name) + r"}}" + "\n")
                        content_parts.append(r"\textbf{Subject:} " + self.escape_latex(subject) + r"\\" + "\n\n")
                        content_parts.append(r"\textbf{Ratio Decidendi:} " + self.escape_latex(ratio) + r"\\" + "\n\n")
                        content_parts.append(r"\vspace{0.3cm}" + "\n\n")
                    else:
                        content_parts.append(r"\subsection*{" + str(i) + r". \textit{" + self.escape_latex(precedent.strip()) + r"}}" + "\n")
                        content_parts.append(r"\vspace{0.3cm}" + "\n\n")
        else:
            # Default precedents with structured format
            default_cases = [
                ('S.P. Gupta v. Union of India, 1981', 'Public Interest Litigation – Locus Standi', 'Any public-spirited citizen can approach the Court for enforcement of public duties and fundamental rights.'),
                ('Bandhua Mukti Morcha v. Union of India, 1984', 'Epistolary Jurisdiction and Access to Justice', 'Letters and informal petitions can be treated as writ petitions in appropriate cases.'),
                ("People's Union for Democratic Rights v. Union of India, 1982", 'PIL for Enforcement of Fundamental Rights', 'The Court has the constitutional duty to protect and enforce fundamental rights of citizens.')
            ]
            for i, (case_name, subject, ratio) in enumerate(default_cases, 1):
                content_parts.append(r"\subsection*{" + str(i) + r". \textit{" + self.escape_latex(case_name) + r"}}" + "\n")
                content_parts.append(r"\textbf{Subject:} " + self.escape_latex(subject) + r"\\" + "\n\n")
                content_parts.append(r"\textbf{Ratio Decidendi:} " + self.escape_latex(ratio) + r"\\" + "\n\n")
                content_parts.append(r"\vspace{0.3cm}" + "\n\n")
        
        # Constitutional provisions
        content_parts.append(r"""
\subsection*{Constitutional Provision — Article 32}
\textbf{Provision:}  
``The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed.''

\textbf{Legal Significance:}  
Article 32 is the cornerstone of the Indian constitutional framework, empowering citizens to directly approach the Supreme Court for violation of fundamental rights. This provision is itself a fundamental right and cannot be suspended except as provided by the Constitution.

\vspace{0.3cm}
""")
        
        # Statutory provisions section
        statutory_provisions = pil_dict.get('statutory_provisions', [])
        if statutory_provisions:
            if isinstance(statutory_provisions, str):
                statutory_provisions = [statutory_provisions]
            
            content_parts.append(r"\subsection*{Applicable Statutory Provisions}" + "\n")
            content_parts.append(r"\textbf{Relevant Provisions:}" + "\n")
            content_parts.append(r"\begin{itemize}" + "\n")
            for provision in statutory_provisions:
                if provision.strip():
                    content_parts.append(r"    \item " + self.escape_latex(provision.strip()) + "\n")
            content_parts.append(r"\end{itemize}" + "\n\n")
            content_parts.append(r"\textbf{Legal Analysis:} The above provisions are directly applicable to the present case and provide the statutory framework for addressing the grievances of the petitioner." + "\n\n")
            content_parts.append(r"\vspace{0.3cm}" + "\n")

        content_parts.append(r"""
\subsection*{D. Other Legal Provisions}

Relevant provisions relating to lawful use of force, executive accountability, 
and protection of fundamental rights under applicable criminal and procedural laws.

\vs

\section{Prayer for Relief}

In view of the facts and circumstances stated above, it is most respectfully prayed 
that this Hon'ble Court may be pleased to:

\begin{enumerate}[label=\alph*.]
    \item Take judicial notice of this matter of urgent public importance;
    \item Issue appropriate writs, orders or directions in the nature of mandamus;
    \item Direct the Respondents to take immediate and effective remedial measures;
    \item Pass such other order(s) as this Hon'ble Court may deem fit in the interest of justice;
    \item Award costs of the present petition.
\end{enumerate}

\vspace{2em}

\textbf{AND FOR THIS ACT OF KINDNESS, THE PETITIONER SHALL EVER PRAY.}

\vspace{2em}

\textbf{Filed in Public Interest}\\
\textbf{Date:} """ + self.escape_latex(pil_dict.get('date_of_filing', 'January 26, 2026')) + r"""

\vs

\textbf{Petitioner (In Person)}\\
\textbf{OR}\\
\textbf{Through Counsel}

\end{document}
""")
        
        return ''.join(content_parts)

    def generate_pdf_with_pylatexenc(self, pil_dict: Dict[str, Any]) -> Optional[bytes]:
        """
        Generate PDF using pylatexenc (pure Python, no external LaTeX needed)
        Falls back to reportlab if pylatexenc not available
        """
        try:
            import pylatexenc
            from pylatexenc.latex2text import LatexNodes2Text
        except ImportError:
            # Fallback to reportlab-based generation
            return self._generate_pdf_fallback(pil_dict)
        
        # Generate LaTeX content
        latex_content = self.build_pil_latex(pil_dict)
        
        # For now, generate using reportlab as LaTeX compilation isn't available
        return self._generate_pdf_fallback(pil_dict)

    def _generate_pdf_fallback(self, pil_dict: Dict[str, Any]) -> Optional[bytes]:
        """Fallback to reportlab-based PDF generation with professional formatting"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
            from io import BytesIO
            
            # Create PDF in memory
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                  topMargin=0.85*inch,
                                  bottomMargin=0.85*inch,
                                  leftMargin=0.85*inch,
                                  rightMargin=0.85*inch)
            
            # Define styles
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.black,
                spaceAfter=8,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.black,
                spaceAfter=13,
                alignment=TA_JUSTIFY,
                leading=19,
                fontName='Helvetica'
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.black,
                spaceAfter=11,
                spaceBefore=11,
                fontName='Helvetica-Bold'
            )
            
            story = []
            
            # Title section
            story.append(Paragraph("IN THE HON'BLE SUPREME COURT OF INDIA", title_style))
            story.append(Paragraph("(ORIGINAL JURISDICTION)", title_style))
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("PUBLIC INTEREST LITIGATION", title_style))
            story.append(Paragraph("UNDER ARTICLE 32 OF THE CONSTITUTION OF INDIA", title_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Filing date
            filing_date = pil_dict.get('date_of_filing', 'January 26, 2026')
            story.append(Paragraph(f"<b>Date of Filing:</b> {filing_date}", body_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Parties
            story.append(Paragraph("<b>IN THE MATTER OF:</b>", body_style))
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("A Public-Spirited Citizen,<br/>Acting bona fide in public interest<br/><b>...Petitioner</b>", body_style))
            story.append(Spacer(1, 0.15*inch))
            story.append(Paragraph("<b>VERSUS</b>", title_style))
            story.append(Spacer(1, 0.15*inch))
            
            respondents = "1. Union of India, Through the Secretary<br/>2. State Government, Through the Chief Secretary<br/>3. Other concerned authorities<br/><b>...Respondents</b>"
            story.append(Paragraph(respondents, body_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Subject matter
            story.append(Paragraph("<b>Subject Matter</b>", heading_style))
            
            issue = pil_dict.get('issue', '')
            if issue:
                story.append(Paragraph(f"<b>Issue:</b> {issue}", body_style))
            
            severity = pil_dict.get('severity_score', '')
            if severity:
                story.append(Paragraph(f"<b>Severity Assessment:</b> {severity}", body_style))
            
            nature = pil_dict.get('nature_of_issue', '')
            if nature:
                story.append(Paragraph(f"<b>Nature of Issue:</b> {nature}", body_style))
            
            story.append(Spacer(1, 0.2*inch))
            
            # Facts
            story.append(Paragraph("<b>Facts of the Case</b>", heading_style))
            facts = pil_dict.get('facts', [])
            if facts:
                if isinstance(facts, str):
                    facts = [facts]
                for i, fact in enumerate(facts, 1):
                    if fact.strip():
                        story.append(Paragraph(f"{i}. {fact.strip()}", body_style))
            
            story.append(Spacer(1, 0.2*inch))
            
            # Grounds
            story.append(Paragraph("<b>Grounds for Filing the Petition</b>", heading_style))
            story.append(Paragraph("<b>A. Violation of Fundamental Rights</b>", heading_style))
            story.append(Paragraph(
                "<b>Article 21 – Right to Life and Personal Liberty:</b> No person shall be deprived of his life or personal liberty except according to procedure established by law. The arbitrary use of force or unjust action violates the core essence of Article 21.",
                body_style
            ))
            
            story.append(Paragraph(
                "<b>Article 32 – Right to Constitutional Remedies:</b> The present petition is maintainable as it raises serious constitutional concerns of public importance.",
                body_style
            ))
            
            # Directive Principles
            story.append(Spacer(1, 0.15*inch))
            story.append(Paragraph("<b>B. Directive Principles of State Policy</b>", heading_style))
            
            # Article 39A section
            story.append(Paragraph("<b>Article 39A — Equal Justice and Free Legal Aid</b>", heading_style))
            story.append(Paragraph(
                "<b>Constitutional Provision:</b><br/>" +
                "Article 39A of the Constitution of India mandates that: 'The State shall secure that the operation of the legal system promotes justice, on a basis of equal opportunity, and shall, in particular, provide free legal aid, by suitable legislation or schemes, so as to ensure that opportunities for securing justice are not denied to any citizen by reason of economic or other disabilities.'",
                body_style
            ))
            story.append(Paragraph(
                "<b>Relevance:</b> The failure of the State to ensure protection, welfare, and access to justice constitutes a clear violation of its constitutional obligation under Article 39A.",
                body_style
            ))
            
            # Custom directive principles if provided
            directive_principles = pil_dict.get('directive_principles', [])
            if directive_principles:
                if isinstance(directive_principles, str):
                    directive_principles = [directive_principles]
                for principle in directive_principles:
                    if principle.strip():
                        story.append(Paragraph(f"• {principle.strip()}", body_style))
            
            # Section C: Case Precedents and Statutory Provisions
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("<b>C. Relevant Case Precedents and Statutory Provisions</b>", heading_style))
            
            # Style with extra bottom spacing to replace Spacer elements
            case_para_style = ParagraphStyle(
                'CaseParagraph',
                parent=body_style,
                spaceAfter=18,  # Add space after each paragraph instead of using Spacer
                leading=16
            )
            
            # Helper function to strip leading numbers from strings
            def strip_leading_number(text):
                """Remove leading number patterns like '1. ' or '1) ' from text"""
                import re
                return re.sub(r'^\d+[\.\)]\s*', '', text.strip())
            
            # Helper function to parse case precedent string into components
            def parse_case_precedent(case_str):
                """Parse a case precedent string that may contain embedded Ratio/Provision/etc."""
                import re
                
                case_str = case_str.strip()
                lines = case_str.split('\n')
                case_name = strip_leading_number(lines[0].strip()) if lines else case_str
                full_text = ' '.join(lines)
                
                ratio = ''
                provision = ''
                legal_analysis = ''
                procedural_relevance = ''
                
                # Extract Ratio
                ratio_match = re.search(r'Ratio(?:\s*Decidendi)?:\s*(.+?)(?=(?:Provision:|Legal Analysis:|Procedural Relevance:|$))', full_text, re.IGNORECASE)
                if ratio_match:
                    ratio = ratio_match.group(1).strip()
                
                # Extract Provision
                provision_match = re.search(r'Provision:\s*(.+?)(?=(?:Legal Analysis:|Procedural Relevance:|$))', full_text, re.IGNORECASE)
                if provision_match:
                    provision = provision_match.group(1).strip()
                
                # Extract Legal Analysis
                legal_match = re.search(r'Legal Analysis:\s*(.+?)(?=(?:Procedural Relevance:|$))', full_text, re.IGNORECASE)
                if legal_match:
                    legal_analysis = legal_match.group(1).strip()
                
                # Extract Procedural Relevance
                proc_match = re.search(r'Procedural Relevance:\s*(.+?)$', full_text, re.IGNORECASE)
                if proc_match:
                    procedural_relevance = proc_match.group(1).strip()
                
                # Clean case name
                case_name = re.sub(r'\s*(?:Ratio|Provision|Legal Analysis|Procedural Relevance):.*$', '', case_name, flags=re.IGNORECASE)
                
                return {
                    'case_name': case_name.strip(),
                    'ratio': ratio,
                    'provision': provision,
                    'legal_analysis': legal_analysis,
                    'procedural_relevance': procedural_relevance
                }
            
            case_precedents = pil_dict.get('relevant_case_precedents', [])
            item_count = 0  # Unified counter for all items
            
            if case_precedents:
                if isinstance(case_precedents, str):
                    case_precedents = [case_precedents]
                
                # Pre-process: merge separate Ratio/Provision/Legal Analysis/Procedural Relevance lines
                # with their preceding case/statute entry
                merged_precedents = []
                for item in case_precedents:
                    item_stripped = item.strip() if isinstance(item, str) else ""
                    # Check if this line starts with a sub-section marker (not a new numbered entry)
                    if item_stripped.startswith(('Ratio:', 'Provision:', 'Legal Analysis:', 'Procedural Relevance:')):
                        # Merge with previous entry if exists
                        if merged_precedents:
                            merged_precedents[-1] = merged_precedents[-1] + '\n' + item_stripped
                        else:
                            merged_precedents.append(item_stripped)
                    else:
                        merged_precedents.append(item_stripped if item_stripped else item)
                
                case_precedents = merged_precedents
                
                for case in case_precedents:
                    if isinstance(case, dict):
                        # Structured case data - combine into single paragraph
                        item_count += 1
                        case_name = case.get('case_name', f'Case {item_count}')
                        subject = case.get('subject', '')
                        ratio = case.get('ratio_decidendi', case.get('ratio', ''))
                        
                        # Build single combined paragraph
                        para_text = f"<b>{item_count}. <i>{case_name}</i></b>"
                        if subject:
                            para_text += f"<br/><br/><b>Subject:</b> {subject}"
                        if ratio:
                            para_text += f"<br/><br/><b>Ratio Decidendi:</b><br/>{ratio}"
                        story.append(Paragraph(para_text, case_para_style))
                        
                    elif case.strip():
                        parsed = parse_case_precedent(case)
                        case_name = parsed['case_name']
                        
                        # Check if this is a statutory provision
                        is_statute = any(kw in case_name for kw in ['Sanhita', 'Act,', 'Code,', 'Rules,', 'Regulation'])
                        
                        item_count += 1
                        
                        if is_statute:
                            # Statutory provision - single combined paragraph
                            para_text = f"<b>{item_count}. {case_name}</b>"
                            if parsed['provision']:
                                para_text += f"<br/><br/><b>Relevant Provision:</b><br/>{parsed['provision']}"
                            if parsed['legal_analysis']:
                                para_text += f"<br/><br/><b>Legal Analysis:</b><br/>{parsed['legal_analysis']}"
                            if parsed['procedural_relevance']:
                                para_text += f"<br/><br/><b>Procedural Relevance:</b><br/>{parsed['procedural_relevance']}"
                            story.append(Paragraph(para_text, case_para_style))
                        else:
                            # Case precedent - single combined paragraph
                            para_text = f"<b>{item_count}. <i>{case_name}</i></b>"
                            if parsed['ratio']:
                                para_text += f"<br/><br/><b>Ratio Decidendi:</b><br/>{parsed['ratio']}"
                            story.append(Paragraph(para_text, case_para_style))
            else:
                # Default precedents - each as single combined paragraph
                default_cases = [
                    {
                        'name': 'D.K. Basu v. State of West Bengal',
                        'subject': 'Custodial violence and arrest guidelines',
                        'ratio': 'This judgment lays down binding guidelines to prevent abuse of power and protect fundamental rights under Articles 21 and 22 of the Constitution.'
                    },
                    {
                        'name': 'Nilabati Behera v. State of Orissa',
                        'subject': 'Compensation for custodial death',
                        'ratio': 'The State is liable to compensate for violations of fundamental rights caused by acts of its officials.'
                    },
                    {
                        'name': 'Bachpan Bachao Andolan v. Union of India',
                        'subject': 'Child trafficking and rescue',
                        'ratio': 'The State has a constitutional obligation to protect children from exploitation and abuse.'
                    }
                ]
                for i, case_data in enumerate(default_cases, 1):
                    para_text = f"<b>{i}. <i>{case_data['name']}</i></b>"
                    para_text += f"<br/><br/><b>Subject:</b> {case_data['subject']}"
                    para_text += f"<br/><br/><b>Ratio Decidendi:</b><br/>{case_data['ratio']}"
                    story.append(Paragraph(para_text, case_para_style))
                item_count = len(default_cases)
            
            # Constitutional Provision Section - single combined paragraph
            item_count += 1
            const_text = f"<b>{item_count}. Constitutional Provision — Article 32</b>"
            const_text += '<br/><br/><b>Provision:</b><br/>"The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed."'
            const_text += "<br/><br/><b>Legal Significance:</b><br/>Article 32 is itself a fundamental right and empowers this Hon'ble Court to issue writs for enforcement of constitutional guarantees."
            story.append(Paragraph(const_text, case_para_style))
            
            # Applicable Statutory Provisions (from pil_dict, if any separate ones exist)
            statutory_provisions = pil_dict.get('statutory_provisions', [])
            if statutory_provisions:
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph("<b>Applicable Statutory Provisions</b>", heading_style))
                story.append(Spacer(1, 0.05*inch))
                story.append(Paragraph("<b>Relevant Provisions:</b>", label_style))
                if isinstance(statutory_provisions, str):
                    statutory_provisions = [statutory_provisions]
                provisions_text = ""
                for provision in statutory_provisions:
                    if provision.strip():
                        provisions_text += f"• {strip_leading_number(provision.strip())}<br/>"
                if provisions_text:
                    story.append(Paragraph(provisions_text, body_style))
                legal_analysis_text = "<b>Legal Analysis:</b><br/>The above provisions are directly applicable to the present case and provide the statutory framework for addressing the grievances of the petitioner. These provisions establish the legal basis for the reliefs sought herein."
                story.append(Paragraph(legal_analysis_text, body_style))
                story.append(Spacer(1, 0.15*inch))
            
            # Prayer - combined into single paragraph
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("<b>Prayer for Relief</b>", heading_style))
            story.append(Spacer(1, 0.1*inch))
            
            prayer_text = "It is most respectfully prayed that this Hon'ble Court may be pleased to:"
            prayer_text += "<br/><br/>a) Take judicial notice of the matter of urgent public importance;"
            prayer_text += "<br/><br/>b) Issue appropriate writs, orders, or directions in the nature of mandamus;"
            prayer_text += "<br/><br/>c) Direct the Respondents to take immediate and effective remedial measures;"
            prayer_text += "<br/><br/>d) Pass such other order(s) as this Hon'ble Court may deem fit in the interest of justice;"
            prayer_text += "<br/><br/>e) Award costs of the present petition."
            story.append(Paragraph(prayer_text, body_style))
            
            story.append(Spacer(1, 0.4*inch))
            story.append(Paragraph("<b>AND FOR THIS ACT OF KINDNESS, THE PETITIONER SHALL EVER PRAY.</b>", title_style))
            story.append(Spacer(1, 0.4*inch))
            
            closing_text = f"<b>Date:</b> {filing_date}<br/><b>Petitioner (In Person)</b><br/><b>OR Through Counsel</b>"
            story.append(Paragraph(closing_text, body_style))
            
            # Build PDF
            doc.build(story)
            
            # Get PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            return pdf_bytes
            
        except Exception as e:
            import traceback
            error_msg = f"Error generating PDF: {e}\n{traceback.format_exc()}"
            print(error_msg)
            return None

    def generate(self, pil_dict: Dict[str, Any]) -> Optional[bytes]:
        """Generate professional PIL PDF with LaTeX-inspired formatting"""
        return self.generate_pdf_with_pylatexenc(pil_dict)


if __name__ == "__main__":
    # Test the generator
    generator = LatexPDFGenerator()
    
    test_pil = {
        'date_of_filing': 'January 26, 2026',
        'issue': 'Man Shot Dead by U.S. Immigration Agents in Minneapolis — Second Killing',
        'severity_score': '0.96 (High)',
        'nature_of_issue': 'Violation of right to life, abuse of executive power, lack of accountability',
        'facts': [
            'Reports indicate a man was shot dead by enforcement agents in Minneapolis.',
            'This marks the second such killing in the same month.',
            'The incident raises concerns regarding excessive force and absence of accountability.',
            'The matter has attracted widespread public attention.'
        ],
        'relevant_case_precedents': [
            'S.P. Gupta v. Union of India – Expanded locus standi in PIL',
            'Bandhua Mukti Morcha v. Union of India – Epistolary jurisdiction',
            'People\'s Union for Democratic Rights v. Union of India – PIL for enforcement'
        ]
    }
    
    pdf_bytes = generator.generate(test_pil)
    if pdf_bytes:
        with open('test_output.pdf', 'wb') as f:
            f.write(pdf_bytes)
        print("PDF generated successfully: test_output.pdf")
    else:
        print("PDF generation failed")
