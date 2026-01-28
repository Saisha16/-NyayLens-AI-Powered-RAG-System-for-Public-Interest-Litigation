"""Generate a PDF file for the PIL draft text."""

import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime


def generate_pil_pdf(pil_text: str, output_path: str = "data/generated_pil.pdf") -> str:
    """Generate PIL PDF with improved text spacing."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=LETTER)
    width, height = LETTER

    # Add formatted date to PDF header
    today = datetime.now().strftime("%B %d, %Y")

    # Text object for better wrapping and baseline control
    text = c.beginText()
    text.setTextOrigin(0.75 * inch, height - 0.75 * inch)
    text.setLeading(14)
    text.setFont("Helvetica", 11)

    def wrap_line(raw: str, max_chars: int = 95):
        """Wrap a single line by characters while preserving word boundaries when possible."""
        if not raw:
            return [""]
        out = []
        line = raw
        while len(line) > max_chars:
            # Try to wrap at space if possible
            split_point = max_chars
            last_space = line.rfind(' ', 0, max_chars)
            if last_space > max_chars * 0.6:  # Only use space if it's reasonably close
                split_point = last_space
            
            out.append(line[:split_point].strip())
            line = line[split_point:].strip()
        
        if line.strip():
            out.append(line.strip())
        return out if out else [""]

    # Build wrapped lines with better spacing preservation
    wrapped_lines = []
    for raw_line in pil_text.split("\n"):
        # Preserve empty lines for section breaks
        if not raw_line.strip():
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(wrap_line(raw_line))

    # Footer date
    wrapped_lines.append("")
    wrapped_lines.append(f"Date of Generation: {today}")

    for line in wrapped_lines:
        text.textLine(line)
        # New page if we overflow
        if text.getY() < 0.75 * inch:
            c.drawText(text)
            c.showPage()
            text = c.beginText()
            text.setTextOrigin(0.75 * inch, height - 0.75 * inch)
            text.setLeading(14)
            text.setFont("Helvetica", 11)

    c.drawText(text)
    c.save()
    return output_path
