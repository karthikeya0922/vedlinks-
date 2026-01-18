"""
Text loader for reading PDFs and text files.
"""

import os
from typing import List
from pathlib import Path

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False


def read_pdf_pypdf2(file_path: str) -> str:
    """Read PDF using PyPDF2."""
    if not HAS_PYPDF2:
        raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
    
    text = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    
    return "\n".join(text)


def read_pdf_pdfplumber(file_path: str) -> str:
    """Read PDF using pdfplumber (better for tables and complex layouts)."""
    if not HAS_PDFPLUMBER:
        raise ImportError("pdfplumber not installed. Run: pip install pdfplumber")
    
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    
    return "\n".join(text)


def read_text_file(file_path: str) -> str:
    """Read plain text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def clean_text(text: str) -> str:
    """
    Clean extracted text:
    - Join broken lines (lines ending mid-word)
    - Remove excessive whitespace
    - Strip page numbers and headers/footers (basic heuristic)
    """
    lines = text.split('\n')
    cleaned = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip likely page numbers (single number on a line)
        if line.isdigit() and len(line) < 4:
            i += 1
            continue
        
        # Join broken lines (if line doesn't end with punctuation and next line exists)
        if i < len(lines) - 1 and line and not line[-1] in '.!?;:':
            next_line = lines[i + 1].strip()
            if next_line and next_line[0].islower():
                line = line + " " + next_line
                i += 2
                cleaned.append(line)
                continue
        
        if line:
            cleaned.append(line)
        i += 1
    
    # Join into paragraphs (double newline separation)
    text = '\n'.join(cleaned)
    
    # Remove excessive whitespace
    text = '\n'.join(line.strip() for line in text.split('\n'))
    
    return text


def load_documents(raw_dir: str = "data/raw") -> List[tuple[str, str]]:
    """
    Load all PDF and text files from raw_dir.
    Returns list of (filename, text_content) tuples.
    """
    documents = []
    raw_path = Path(raw_dir)
    
    if not raw_path.exists():
        print(f"Warning: {raw_dir} does not exist. Creating it...")
        raw_path.mkdir(parents=True, exist_ok=True)
        return documents
    
    # Process PDFs
    pdf_files = list(raw_path.glob("*.pdf"))
    for pdf_file in pdf_files:
        print(f"Loading PDF: {pdf_file.name}")
        try:
            # Try pdfplumber first (better extraction), fallback to PyPDF2
            if HAS_PDFPLUMBER:
                text = read_pdf_pdfplumber(str(pdf_file))
            elif HAS_PYPDF2:
                text = read_pdf_pypdf2(str(pdf_file))
            else:
                print(f"  Skipping {pdf_file.name}: No PDF library installed")
                continue
            
            text = clean_text(text)
            documents.append((pdf_file.name, text))
            print(f"  Loaded {len(text)} characters")
        except Exception as e:
            print(f"  Error loading {pdf_file.name}: {e}")
    
    # Process text files
    txt_files = list(raw_path.glob("*.txt"))
    for txt_file in txt_files:
        print(f"Loading text file: {txt_file.name}")
        try:
            text = read_text_file(str(txt_file))
            text = clean_text(text)
            documents.append((txt_file.name, text))
            print(f"  Loaded {len(text)} characters")
        except Exception as e:
            print(f"  Error loading {txt_file.name}: {e}")
    
    return documents
