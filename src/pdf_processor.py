
import pdfplumber
from pathlib import Path

def extract_structured_text(pdf_path: str):
    """
    Extracts text from a PDF, attempting to preserve some structure 
    (headings and paragraphs) for better training data generation.
    """
    structured_content = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract words with their layout information
                words = page.extract_words(
                    use_text_flow=True,
                    extra_attrs=["fontname", "size"]
                )
                
                if not words:
                    continue
                
                # Simple heuristic: Group words into lines and identify potential headings
                current_line = []
                last_top = -1
                
                for word in words:
                    # If this word is significantly lower than the last, it's a new line
                    if last_top != -1 and abs(word['top'] - last_top) > 5:
                        line_text = " ".join([w['text'] for w in current_line]).strip()
                        if line_text:
                            # Heuristic for headings: Large font size or all caps
                            is_heading = any(w['size'] > 12 for w in current_line) or line_text.isupper()
                            structured_content.append({
                                'text': line_text,
                                'is_heading': is_heading,
                                'page': page.page_number
                            })
                        current_line = []
                    
                    current_line.append(word)
                    last_top = word['top']
                
                # Add the last line
                if current_line:
                    line_text = " ".join([w['text'] for w in current_line]).strip()
                    if line_text:
                        structured_content.append({
                            'text': line_text,
                            'is_heading': any(w['size'] > 12 for w in current_line) or line_text.isupper(),
                            'page': page.page_number
                        })
                        
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
        
    return structured_content

def get_chapter_text(pdf_path: str):
    """Returns the raw text of a chapter optimized for LLM processing."""
    content = extract_structured_text(pdf_path)
    
    # Format the content into a single string with semantic markers
    formatted_text = ""
    for item in content:
        if item['is_heading']:
            formatted_text += f"\n\n## {item['text']}\n"
        else:
            formatted_text += f"{item['text']} "
            
    return formatted_text.strip()
