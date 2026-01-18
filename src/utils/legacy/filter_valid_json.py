"""
Filter and validate JSONL files to extract only valid entries.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

from src.utils.parsers import safe_parse_json, validate_generated_output


def filter_valid_entries(input_jsonl: str, output_jsonl: str = None) -> tuple[int, int]:
    """
    Filter JSONL file to keep only valid, parseable entries.
    
    Args:
        input_jsonl: Path to input JSONL file
        output_jsonl: Path to output filtered JSONL (default: input_filtered.jsonl)
    
    Returns:
        (valid_count, total_count)
    """
    if output_jsonl is None:
        output_jsonl = input_jsonl.replace('.jsonl', '_filtered.jsonl')
    
    valid_entries = []
    total = 0
    
    with open(input_jsonl, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total += 1
            line = line.strip()
            if not line:
                continue
            
            try:
                # Try to parse the line as JSON
                entry = json.loads(line)
                
                # Validate structure
                is_valid, error = validate_generated_output(entry)
                if is_valid:
                    valid_entries.append(entry)
                else:
                    print(f"Line {line_num}: Invalid structure - {error}")
            except json.JSONDecodeError as e:
                # Try to recover using safe_parse_json
                recovered = safe_parse_json(line)
                if recovered:
                    is_valid, error = validate_generated_output(recovered)
                    if is_valid:
                        valid_entries.append(recovered)
                        print(f"Line {line_num}: Recovered from parse error")
                    else:
                        print(f"Line {line_num}: Recovered but invalid - {error}")
                else:
                    print(f"Line {line_num}: Parse error - {e}")
    
    # Write valid entries
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for entry in valid_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"\n✅ Filtered: {len(valid_entries)}/{total} valid entries")
    print(f"📁 Output: {output_jsonl}")
    
    return len(valid_entries), total


def main():
    """Command-line interface for filtering."""
    if len(sys.argv) < 2:
        print("Usage: python -m src.utils.filter_valid_json <input.jsonl> [output.jsonl]")
        print("\nLooking for latest adaptive_*.jsonl in data/datasets/...")
        
        # Auto-find latest adaptive file
        dataset_dir = Path("data/datasets")
        if dataset_dir.exists():
            adaptive_files = sorted(dataset_dir.glob("adaptive_*.jsonl"))
            adaptive_files = [f for f in adaptive_files if '_filtered' not in f.name]
            
            if adaptive_files:
                latest = adaptive_files[-1]
                print(f"Found: {latest}")
                filter_valid_entries(str(latest))
                return
        
        print("No files found. Please specify input file.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    filter_valid_entries(input_file, output_file)


if __name__ == "__main__":
    main()
