"""
PDF Metadata Extraction Script for VedLinks

Automatically extracts chapter metadata from NCERT PDFs:
- Reads the first page of each PDF
- Extracts chapter title using common patterns
- Detects class level from filename or content
- Generates topic_registry.json with all metadata
"""

import os
import re
import json
from pathlib import Path

# Try to import PDF libraries
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"
REGISTRY_PATH = PROJECT_ROOT / "data" / "topic_registry.json"


# NCERT filename patterns - decode common naming conventions
NCERT_PATTERNS = {
    # Format: aemr1XX where XX is chapter number, 1 might be class indicator
    r'^aemr(\d)(\d{2})\.pdf$': lambda m: {'class_hint': m.group(1), 'chapter': int(m.group(2))},
    r'^(\w+)(\d{2})\.pdf$': lambda m: {'chapter': int(m.group(2))},
}

# Common chapter title patterns in NCERT books
CHAPTER_TITLE_PATTERNS = [
    # "Chapter 1: Food – Where Does It Come From?"
    r'Chapter\s*(\d+)\s*[:\-–—]\s*(.+?)(?:\n|$)',
    # "1. Food – Where Does It Come From?"
    r'^(\d+)\.\s+(.+?)(?:\n|$)',
    # "CHAPTER 1 FOOD – WHERE DOES IT COME FROM"
    r'CHAPTER\s*(\d+)\s+(.+?)(?:\n|$)',
    # Just a title at the start
    r'^([A-Z][a-zA-Z\s\-–—\']+)(?:\n|$)',
]

# Known NCERT books mapping (for files we can identify)
KNOWN_NCERT_BOOKS = {
    'aemr1': {'class': '6', 'subject': 'Science'},  # Class 6 Science chapters
    'aemr2': {'class': '7', 'subject': 'Science'},
    'aemr3': {'class': '8', 'subject': 'Science'},
}


def extract_text_from_pdf(pdf_path: Path, max_pages: int = 2) -> str:
    """Extract text from first few pages of PDF."""
    text = ""
    
    if HAS_PDFPLUMBER:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages[:max_pages]):
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
            return text
        except Exception as e:
            print(f"  ⚠️  pdfplumber failed: {e}")
    
    if HAS_PYPDF2:
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for i in range(min(max_pages, len(reader.pages))):
                    page_text = reader.pages[i].extract_text() or ""
                    text += page_text + "\n"
            return text
        except Exception as e:
            print(f"  ⚠️  PyPDF2 failed: {e}")
    
    return text


def extract_chapter_title(text: str) -> tuple:
    """Extract chapter number and title from text."""
    # Clean up text
    text = text.strip()
    
    for pattern in CHAPTER_TITLE_PATTERNS:
        match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) == 2:
                chapter_num = groups[0]
                title = groups[1].strip()
                # Clean up title
                title = re.sub(r'\s+', ' ', title)
                title = title.strip('.')
                return chapter_num, title
            elif len(groups) == 1:
                title = groups[0].strip()
                title = re.sub(r'\s+', ' ', title)
                return None, title
    
    # Fallback: use first line as title
    first_line = text.split('\n')[0].strip() if text else "Unknown Chapter"
    first_line = first_line[:100]  # Limit length
    return None, first_line


def decode_filename(filename: str) -> dict:
    """Decode NCERT filename to extract metadata hints."""
    info = {'chapter': None, 'class_hint': None, 'subject_hint': None}
    
    for pattern, decoder in NCERT_PATTERNS.items():
        match = re.match(pattern, filename, re.IGNORECASE)
        if match:
            extracted = decoder(match)
            info.update(extracted)
            break
    
    # Check against known book prefixes
    name_lower = filename.lower()
    for prefix, book_info in KNOWN_NCERT_BOOKS.items():
        if name_lower.startswith(prefix):
            info['class_hint'] = book_info.get('class')
            info['subject_hint'] = book_info.get('subject')
            break
    
    return info


def generate_topic_list(chapter_title: str, subject: str = "Science") -> list:
    """Generate a basic topic list for a chapter."""
    # This is a placeholder - ideally we'd extract topics from PDF content
    # For now, return a generic list that can be edited
    return [
        f"Introduction to {chapter_title}",
        f"Key concepts in {chapter_title}",
        f"Important definitions",
        f"Applications and examples",
        f"Summary and review"
    ]


def extract_metadata_from_pdfs():
    """Main function to extract metadata from all PDFs."""
    print("=" * 60)
    print("VedLinks PDF Metadata Extractor")
    print("=" * 60)
    
    if not HAS_PDFPLUMBER and not HAS_PYPDF2:
        print("❌ ERROR: No PDF library available!")
        print("Please install: pip install pdfplumber PyPDF2")
        return
    
    if not RAW_DATA_PATH.exists():
        print(f"❌ ERROR: Raw data path not found: {RAW_DATA_PATH}")
        return
    
    # Get all PDFs
    pdf_files = list(RAW_DATA_PATH.glob("*.pdf"))
    print(f"\n📁 Found {len(pdf_files)} PDF files in {RAW_DATA_PATH}\n")
    
    if not pdf_files:
        print("No PDF files found!")
        return
    
    # Load existing registry if present
    registry = {"version": "1.0", "files": {}}
    if REGISTRY_PATH.exists():
        try:
            with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            print(f"📖 Loaded existing registry with {len(registry.get('files', {}))} entries\n")
        except Exception as e:
            print(f"⚠️  Could not load existing registry: {e}\n")
    
    # Process each PDF
    for pdf_path in sorted(pdf_files):
        filename = pdf_path.name
        print(f"📄 Processing: {filename}")
        
        # Skip if already in registry and has proper title
        if filename in registry.get('files', {}):
            existing = registry['files'][filename]
            if existing.get('chapter') and existing['chapter'] != "Unknown Chapter":
                print(f"   ✓ Already in registry: {existing['chapter']}")
                continue
        
        # Decode filename
        file_info = decode_filename(filename)
        
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        
        if not text:
            print(f"   ⚠️  Could not extract text from PDF")
            chapter_num, chapter_title = None, f"Unknown - {filename}"
        else:
            chapter_num, chapter_title = extract_chapter_title(text)
        
        # Build metadata entry
        entry = {
            "class": file_info.get('class_hint') or "6",  # Default to class 6
            "subject": file_info.get('subject_hint') or "Science",
            "chapter_number": file_info.get('chapter') or (int(chapter_num) if chapter_num else 0),
            "chapter": chapter_title,
            "topics": generate_topic_list(chapter_title),
            "source_file": filename,
            "auto_extracted": True
        }
        
        registry['files'][filename] = entry
        print(f"   → Chapter: {chapter_title}")
        print(f"   → Class: {entry['class']}, Subject: {entry['subject']}")
    
    # Save registry
    print(f"\n💾 Saving registry to {REGISTRY_PATH}")
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Registry saved with {len(registry['files'])} entries")
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("1. Review and edit 'data/topic_registry.json' to correct any errors")
    print("2. Run 'python scripts/generate_topic_files.py' to create topic JSON files")
    print("=" * 60)


if __name__ == "__main__":
    extract_metadata_from_pdfs()
