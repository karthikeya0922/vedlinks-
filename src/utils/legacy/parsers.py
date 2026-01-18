"""
Robust JSON parser with recovery heuristics for LLM-generated outputs.
Handles common issues like markdown fences, trailing commas, and extra text.
"""

import json
import re


def extract_first_json_object(text: str):
    """
    Find first top-level JSON object by scanning for matching braces.
    Returns substring or None.
    """
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    return None


def extract_first_json_array(text: str):
    """
    Find first top-level JSON array by scanning for matching brackets.
    Returns substring or None.
    """
    start = text.find("[")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    return None


def pretty_fix_common_issues(s: str) -> str:
    """
    Apply common fixes to JSON-like strings.
    - Remove markdown fences
    - Strip whitespace
    - Replace smart quotes
    """
    # Remove markdown code fences
    s = re.sub(r"```json\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"```\s*", "", s)
    s = s.strip()
    
    # Replace smart quotes with regular quotes
    s = s.replace(""", '"').replace(""", '"')
    s = s.replace("'", "'").replace("'", "'")
    
    return s


def safe_parse_json(raw_text: str):
    """
    Attempt to extract and parse first JSON object or array from raw_text.
    Returns python object or None.
    
    Strategy:
    1. Try to extract first JSON object {...}
    2. If not found, try to extract first JSON array [...]
    3. Apply common fixes (remove markdown, fix quotes)
    4. Attempt parsing with progressive repairs
    """
    if not raw_text:
        return None
    
    # Try to extract object first
    cand = extract_first_json_object(raw_text)
    
    # Fallback: try to find array
    if cand is None:
        cand = extract_first_json_array(raw_text)
    
    if cand is None:
        return None

    cand = pretty_fix_common_issues(cand)
    
    # Attempt 1: Parse as-is
    try:
        return json.loads(cand)
    except Exception:
        pass
    
    # Attempt 2: Fix trailing commas
    cand2 = re.sub(r",\s*([}\]])", r"\1", cand)
    try:
        return json.loads(cand2)
    except Exception:
        pass
    
    # Attempt 3: Additional quote fixes
    cand3 = cand2.replace("'", '"')  # Convert single to double quotes (risky but worth trying)
    try:
        return json.loads(cand3)
    except Exception:
        pass
    
    # All attempts failed
    return None


def validate_generated_output(data: dict) -> tuple[bool, str]:
    """
    Validate that generated output has the expected structure.
    Returns (is_valid, error_message).
    
    Expected structure:
    {
        "student_qa": [{"q": "...", "a": "..."}, ...],
        "teacher_summary": "...",
        "mcqs": [{"q": "...", "options": [...], "answer": "...", "explanation": "..."}, ...]
    }
    """
    if not isinstance(data, dict):
        return False, "Output is not a dictionary"
    
    # Check for required keys
    required_keys = ["student_qa", "teacher_summary", "mcqs"]
    for key in required_keys:
        if key not in data:
            return False, f"Missing required key: {key}"
    
    # Validate student_qa
    if not isinstance(data["student_qa"], list):
        return False, "student_qa must be a list"
    if len(data["student_qa"]) == 0:
        return False, "student_qa is empty"
    for i, qa in enumerate(data["student_qa"]):
        if not isinstance(qa, dict):
            return False, f"student_qa[{i}] is not a dict"
        if "q" not in qa or "a" not in qa:
            return False, f"student_qa[{i}] missing 'q' or 'a'"
        if not qa["q"] or not qa["a"]:
            return False, f"student_qa[{i}] has empty 'q' or 'a'"
    
    # Validate teacher_summary
    if not isinstance(data["teacher_summary"], str):
        return False, "teacher_summary must be a string"
    if not data["teacher_summary"].strip():
        return False, "teacher_summary is empty"
    
    # Validate mcqs
    if not isinstance(data["mcqs"], list):
        return False, "mcqs must be a list"
    if len(data["mcqs"]) == 0:
        return False, "mcqs is empty"
    for i, mcq in enumerate(data["mcqs"]):
        if not isinstance(mcq, dict):
            return False, f"mcqs[{i}] is not a dict"
        required_mcq_keys = ["q", "options", "answer", "explanation"]
        for key in required_mcq_keys:
            if key not in mcq:
                return False, f"mcqs[{i}] missing key: {key}"
        if not isinstance(mcq["options"], list):
            return False, f"mcqs[{i}] options must be a list"
        if len(mcq["options"]) < 2:
            return False, f"mcqs[{i}] must have at least 2 options"
        if not mcq["q"] or not mcq["answer"] or not mcq["explanation"]:
            return False, f"mcqs[{i}] has empty required field"
    
    return True, ""
