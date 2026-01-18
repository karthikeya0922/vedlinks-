"""
Convert filtered dataset to finetune format for SFTTrainer.
"""

import json
import sys
from pathlib import Path


def format_for_finetune(entry: dict) -> dict:
    """
    Convert a validated entry into finetune format.
    
    Format for instruction tuning:
    {
        "prompt": "...",
        "completion": "..."
    }
    """
    # Create a structured prompt
    prompt_parts = []
    
    # Add student Q&A
    if entry.get("student_qa"):
        prompt_parts.append("### Student Questions and Answers:")
        for qa in entry["student_qa"]:
            prompt_parts.append(f"Q: {qa['q']}")
            prompt_parts.append(f"A: {qa['a']}")
            prompt_parts.append("")
    
    # Add MCQs
    if entry.get("mcqs"):
        prompt_parts.append("### Multiple Choice Questions:")
        for mcq in entry["mcqs"]:
            prompt_parts.append(f"Q: {mcq['q']}")
            for opt in mcq["options"]:
                prompt_parts.append(f"  - {opt}")
            prompt_parts.append(f"Answer: {mcq['answer']}")
            prompt_parts.append(f"Explanation: {mcq['explanation']}")
            prompt_parts.append("")
    
    completion = "\n".join(prompt_parts)
    
    # The prompt will be the instruction to generate this content
    prompt = f"""Generate educational content based on NCERT-style learning materials.

Create:
1. Student Q&A pairs that help understand the topic
2. Multiple choice questions with explanations
3. Teacher summary of key concepts

### Teacher Summary:
{entry.get('teacher_summary', '')}

"""
    
    return {
        "prompt": prompt.strip(),
        "completion": completion.strip()
    }


def prepare_finetune_dataset(input_jsonl: str, output_jsonl: str = "data/finetune_dataset.jsonl"):
    """
    Convert filtered JSONL to finetune format.
    
    Args:
        input_jsonl: Path to filtered JSONL
        output_jsonl: Path to output finetune JSONL
    """
    entries = []
    
    with open(input_jsonl, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            finetune_entry = format_for_finetune(entry)
            entries.append(finetune_entry)
    
    # Write finetune dataset
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"✅ Created finetune dataset: {output_jsonl}")
    print(f"📊 {len(entries)} training examples")
    
    return len(entries)


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print("Usage: python -m src.utils.prepare_for_finetune <filtered.jsonl> [output.jsonl]")
        print("\nLooking for latest *_filtered.jsonl in data/datasets/...")
        
        # Auto-find latest filtered file
        dataset_dir = Path("data/datasets")
        if dataset_dir.exists():
            filtered_files = sorted(dataset_dir.glob("*_filtered.jsonl"))
            
            if filtered_files:
                latest = filtered_files[-1]
                print(f"Found: {latest}")
                prepare_finetune_dataset(str(latest))
                return
        
        print("No filtered files found. Please run filter_valid_json first.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "data/finetune_dataset.jsonl"
    
    prepare_finetune_dataset(input_file, output_file)


if __name__ == "__main__":
    main()
