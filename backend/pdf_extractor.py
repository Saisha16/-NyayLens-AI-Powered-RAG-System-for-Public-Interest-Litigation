"""Extract and chunk text from legal PDF documents.

Processes PDFs from data/legal_docs/ and creates structured chunks
for semantic search and RAG retrieval.
"""

from pathlib import Path
import json
from typing import List, Dict
import re

try:
    from pdfminer.high_level import extract_text
except ImportError:
    extract_text = None


def clean_text(text: str) -> str:
    """Clean extracted PDF text - remove bad spacing then add good spacing."""
    
    # Step 1: Remove embedded spaces that break words (common in corrupted PDFs)
    # Fix things like "S ANHITA" -> "SANHITA", "Decem be r" -> "December"
    # Look for single letter followed by space then letters (likely broken word)
    text = re.sub(r'\b([A-Z])\s+([A-Z]{2,})\b', r'\1\2', text)  # "S ANHITA" -> "SANHITA"
    text = re.sub(r'\b([a-z]{1,3})\s+([a-z]{2,})\b', r'\1\2', text)  # "be r" -> "ber"
    
    # Fix common broken words in legal docs
    text = text.replace(' IN ARY', 'INARY')  # "PRELIM IN ARY" -> "PRELIMINARY"
    text = text.replace(' IN ', 'IN')  # "EXTRAORD IN ARY" -> "EXTRAORDINARY"
    text = text.replace('f or med', 'formed')
    text = text.replace('in tended', 'intended')
    text = text.replace('the reto', 'thereto')
    text = text.replace('the re', 'there')
    
    # Step 2: Normalize all whitespace to single spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Step 3: Add spaces where clearly missing (dense text)
    # Add space between lowercase and uppercase ONLY if not already there
    # But be careful not to break acronyms
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Add space after punctuation if missing
    text = re.sub(r'([.!?;:,])([A-Za-z])', r'\1 \2', text)
    
    # Add space after closing brackets/parens
    text = re.sub(r'([\)\]])([A-Za-z0-9])', r'\1 \2', text)
    
    # Add space between number and letter
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
    
    # Step 4: Clean up artifacts
    text = re.sub(r'\b\d+\s*\|\s*Page\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bPage\s+\d+\b', '', text, flags=re.IGNORECASE)
    
    # Step 5: Final whitespace cleanup
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks by sentences."""
    # Split by sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Filter out very short sentences (likely artifacts)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    if not sentences:
        # Fallback: if no good sentence boundaries, split by word count
        words = text.split()
        sentences = []
        for i in range(0, len(words), chunk_size):
            sentences.append(' '.join(words[i:i + chunk_size]))
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_len = len(sentence.split())
        
        if current_length + sentence_len > chunk_size and current_chunk:
            # Save current chunk
            chunks.append(' '.join(current_chunk))
            # Keep overlap sentences
            overlap_sentences = []
            overlap_len = 0
            for s in reversed(current_chunk):
                s_len = len(s.split())
                if overlap_len + s_len <= overlap:
                    overlap_sentences.insert(0, s)
                    overlap_len += s_len
                else:
                    break
            current_chunk = overlap_sentences
            current_length = overlap_len
        
        current_chunk.append(sentence)
        current_length += sentence_len
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
def _extract_bns_sections(cleaned_text: str, pdf_path: Path) -> List[Dict]:
    """Specialized extractor for Bhartiya Nyaya Sanhita: split by section numbers."""
    sections: List[Dict] = []
    # Pattern: captures "137. Kidnapping" style headings; title may include spaces/commas/brackets
    heading_re = re.compile(r"(\d{1,4})\.\s+([A-Z][A-Za-z0-9\s,\-\(\)/]{2,80})")
    matches = list(heading_re.finditer(cleaned_text))
    if not matches:
        return sections

    source_name = "Bhartiya Nyaya Sanhita 2023"
    seen_ids = set()
    for idx, match in enumerate(matches):
        sec_num = match.group(1)
        # Keep only valid BNS sections 1–358 and dedupe
        if not sec_num.isdigit():
            continue
        if not (1 <= int(sec_num) <= 358):
            continue
        if sec_num in seen_ids:
            continue
        seen_ids.add(sec_num)

        title = match.group(2).strip()
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(cleaned_text)
        content = cleaned_text[start:end].strip()
        if len(content) < 5:
            continue
        sections.append({
            "id": f"{pdf_path.stem}_sec_{sec_num}",
            "section_id": sec_num,
            "title": title,
            "text": content,
            "source": source_name,
            "file": pdf_path.name,
            "chunk_index": idx
        })
    return sections


def extract_pdf_chunks(pdf_path: Path) -> List[Dict]:
    """Extract and chunk a single PDF file."""
    if not extract_text:
        print(f"Warning: pdfminer.six not available, skipping {pdf_path.name}")
        return []

    try:
        raw_text = extract_text(str(pdf_path))
        cleaned = clean_text(raw_text)

        # Specialized path: if this is the BNS PDF, split by section headings
        if "bhartiya_nyaya_sanhita" in pdf_path.stem.lower():
            sections = _extract_bns_sections(cleaned, pdf_path)
            if sections:
                print(f"  → Extracted {len(sections)} BNS sections from {pdf_path.name}")
                return sections
            # Fall back to generic chunking if headings were not detected

        # Generic chunking for all other PDFs
        chunks = chunk_text(cleaned, chunk_size=400, overlap=80)

        source_name = pdf_path.stem.replace('_', ' ').title()
        result = []
        for idx, text_chunk in enumerate(chunks):
            if len(text_chunk.strip()) < 50:
                continue
            result.append({
                "id": f"{pdf_path.stem}_chunk_{idx}",
                "text": text_chunk,
                "source": source_name,
                "file": pdf_path.name,
                "chunk_index": idx
            })
        return result

    except Exception as e:
        print(f"Error extracting {pdf_path.name}: {e}")
        return []


def build_legal_chunks_db(legal_docs_dir: str = "data/legal_docs", output_file: str = "data/legal_chunks.json"):
    """Process all PDFs in legal_docs directory and create chunks JSON."""
    legal_dir = Path(legal_docs_dir)
    
    if not legal_dir.exists():
        print(f"Legal docs directory not found: {legal_docs_dir}")
        return
    
    all_chunks = []
    pdf_files = list(legal_dir.glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files")
    
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        chunks = extract_pdf_chunks(pdf_file)
        all_chunks.extend(chunks)
        print(f"  → Extracted {len(chunks)} chunks")
    
    # Write to JSON
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Created {output_file} with {len(all_chunks)} total chunks")
    return all_chunks


if __name__ == "__main__":
    build_legal_chunks_db()
