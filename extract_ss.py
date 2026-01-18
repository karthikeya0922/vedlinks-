"""Extract chapter info from Social Science Geography PDFs."""
import pdfplumber
from pathlib import Path

raw_path = Path("data/raw")
pdfs = [
    "jess101.pdf", "jess102.pdf", "jess103.pdf", "jess104.pdf",
    "jess105.pdf", "jess106.pdf", "jess107.pdf"
]

for filename in pdfs:
    pdf_file = raw_path / filename
    if not pdf_file.exists():
        continue
    print(f"\n{filename}:")
    try:
        with pdfplumber.open(pdf_file) as pdf:
            # Try page 0 and 1 for chapter title
            for page_num in [0, 1]:
                if page_num < len(pdf.pages):
                    text = pdf.pages[page_num].extract_text() or ""
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    # Look for chapter pattern
                    for i, line in enumerate(lines[:15]):
                        if 'chapter' in line.lower() or line.isupper():
                            print(f"  [{page_num}] {line}")
    except Exception as e:
        print(f"  Error: {e}")
