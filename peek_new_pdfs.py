"""Quick script to extract first page content from new jess PDFs."""
import pdfplumber
from pathlib import Path

raw_path = Path("data/raw")
for pdf_file in sorted(raw_path.glob("jess*.pdf")):
    print(f"\n{'='*60}")
    print(f"FILE: {pdf_file.name}")
    print('='*60)
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = pdf.pages[0].extract_text() or ""
            # Show first 400 chars
            print(text[:400])
    except Exception as e:
        print(f"Error: {e}")
