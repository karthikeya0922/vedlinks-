import fitz  # PyMuPDF
import re
import json
import os
import sys

def parse_pdf_to_json(pdf_path, output_json_path):
    print(f"Reading PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    
    # Extract text from all pages
    full_text = ""
    for page in doc:
        # get_text("text", sort=True) preserves logical layout (top-to-bottom, left-to-right)
        full_text += page.get_text("text", sort=True) + "\n"
        
    print("PDF loaded. Starting parsing...")

    # Sections to look for
    sections = [
        "Multiple Choice Questions",
        "ASSERTION AND REASON TYPE QUESTIONS",
        "SHORT ANSWER TYPE QUESTIONS",
        "LONG ANSWER TYPE QUESTIONS",
        "CASE BASED QUESTIONS",
        "Answers"
    ]
    
    # Store questions and answers
    qbank_data = {
        "mcq": [],
        "assertion_reason": [],
        "short_answer": [],
        "long_answer": [],
        "case_based": []
    }
    
    answers_data = {
        "mcq": {},
        "assertion_reason": {},
        "short_answer": {},
        "long_answer": {},
        "case_based": {}
    }

    current_section = None
    
    # Clean up massive spaces to help regex
    lines = full_text.split('\n')
    
    buffer = []
    
    # Regex to catch "1.", "2." at the start of lines
    question_pattern = re.compile(r'^\s*(\d+)\.\s+(.*)')
    
    # State tracking
    current_q_num = None
    current_q_text = []

    def commit_question(section, q_num, text_lines):
        if not q_num or not text_lines: return
        raw_text = " ".join(text_lines).strip()
        
        if section == "mcq":
            # Try to split out options (A) (B) (C) (D)
            parts = re.split(r'\(([A-D])\)', raw_text)
            if len(parts) >= 9: # Has question + 4 options
                q_text = parts[0].strip()
                opts = [
                    f"(A) {parts[2].strip()}",
                    f"(B) {parts[4].strip()}",
                    f"(C) {parts[6].strip()}",
                    f"(D) {parts[8].strip()}"
                ]
                qbank_data["mcq"].append({"id": q_num, "type": "mcq", "question": q_text, "options": opts})
            else:
                qbank_data["mcq"].append({"id": q_num, "type": "mcq", "question": raw_text, "options": []})
        
        elif section == "assertion_reason":
            # Extract Assertion and Reason text
            a_match = re.search(r'Assertion\s*\(A\):\s*(.*?)(Reason\s*\(R\):|$)', raw_text, re.IGNORECASE | re.DOTALL)
            r_match = re.search(r'Reason\s*\(R\):\s*(.*)', raw_text, re.IGNORECASE | re.DOTALL)
            
            a_text = a_match.group(1).strip() if a_match else raw_text
            r_text = r_match.group(1).strip() if r_match else ""
            
            qbank_data["assertion_reason"].append({
                "id": q_num,
                "type": "assertion_reason",
                "assertion": a_text,
                "reason": r_text
            })
            
        elif section == "short_answer":
            qbank_data["short_answer"].append({"id": q_num, "type": "short_answer", "question": raw_text})
        elif section == "long_answer":
            qbank_data["long_answer"].append({"id": q_num, "type": "long_answer", "question": raw_text})
        elif section == "case_based":
            qbank_data["case_based"].append({"id": q_num, "type": "case_based", "question": raw_text})

    print("Parsing questions...")
    ans_section_phase = False
    ans_sub_section = None
    
    for line in lines:
        stripped = line.strip()
        if not stripped: continue
        
        # Check if we hit a main header
        found_header = False
        for sec in sections:
            if stripped.upper() == sec.upper() or stripped.upper().startswith(sec.upper()):
                if current_q_num: 
                    commit_question(current_section, current_q_num, current_q_text)
                    current_q_num = None
                    current_q_text = []

                if "ANSWERS" in stripped.upper():
                    ans_section_phase = True
                else:
                    if "MULTIPLE CHOICE" in stripped.upper(): current_section = "mcq"
                    elif "ASSERTION" in stripped.upper(): current_section = "assertion_reason"
                    elif "SHORT" in stripped.upper(): current_section = "short_answer"
                    elif "LONG" in stripped.upper(): current_section = "long_answer"
                    elif "CASE" in stripped.upper(): current_section = "case_based"
                
                found_header = True
                break
                
        if found_header: continue

        # ANWERS Parsing logic
        if ans_section_phase:
            if "Multiple choice" in line: ans_sub_section = "mcq"
            elif "A-R" in line or "Assertion" in line: ans_sub_section = "assertion_reason"
            elif "SHORT" in line: ans_sub_section = "short_answer"
            elif "LONG" in line: ans_sub_section = "long_answer"
            elif "CASE" in line: ans_sub_section = "case_based"
            else:
                ans_match = re.match(r'^\s*(\d+)\.\s*(.*)', stripped)
                if ans_match and ans_sub_section:
                    answers_data[ans_sub_section][ans_match.group(1)] = ans_match.group(2).strip()
            continue

        # QUESTION Parsing Logic
        q_match = question_pattern.match(stripped)
        if q_match:
            # We found a new question starting like "1. Choose the..."
            # Commit the PREVIOUS question first
            if current_q_num and current_section:
                commit_question(current_section, current_q_num, current_q_text)
            
            # Start new question
            current_q_num = q_match.group(1)
            current_q_text = [q_match.group(2)]
        else:
            if current_q_num:
                current_q_text.append(stripped)

    # Commit last question
    if current_q_num and current_section:
        commit_question(current_section, current_q_num, current_q_text)

    # Merge Answers into Questions
    print("Merging Answers into Questions...")
    for q_type, questions in qbank_data.items():
        for q in questions:
            q_id = str(q['id'])
            if q_id in answers_data[q_type]:
                q['answer'] = answers_data[q_type][q_id]

    # Save to JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(qbank_data, f, indent=4, ensure_ascii=False)
        
    print(f"✅ Success! Parsed Question Bank saved to {output_json_path}")
    
    # Print a tiny summary
    for key, val in qbank_data.items():
        count = len(val)
        print(f" - Found {count} {key} questions.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parse Question Bank PDF.")
    parser.add_argument("pdf_input", help="Path to input PDF")
    parser.add_argument("--out", default="data/topics/structured_qbank.json", help="Path to output JSON")
    args = parser.parse_args()
    
    parse_pdf_to_json(args.pdf_input, args.out)