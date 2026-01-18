"""
VedLinks Training Pipeline
===========================
Complete pipeline for generating training data and fine-tuning the model.

Usage:
    python train_pipeline.py generate   - Generate training dataset
    python train_pipeline.py train      - Train the model with LoRA
    python train_pipeline.py all        - Run complete pipeline
"""

import sys
import json
import random
from pathlib import Path
from datetime import datetime

# Configuration
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output/qlora_tuned_model")
DATASET_FILE = DATA_DIR / "finetune_dataset.jsonl"


def generate_training_data():
    """Generate training dataset from topic registry and knowledge bank."""
    print("=" * 60)
    print("Step 1: Generating Training Dataset")
    print("=" * 60)
    
    from question_paper_generator import NCERT_KNOWLEDGE
    
    # Load topic registry
    registry_path = DATA_DIR / "topic_registry.json"
    if not registry_path.exists():
        print("❌ Topic registry not found!")
        return False
    
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    training_samples = []
    
    # Generate instruction samples from each chapter
    for file_key, topic_data in registry.get('files', {}).items():
        chapter = topic_data.get('chapter', '')
        class_num = topic_data.get('class', '')
        subject = topic_data.get('subject', '')
        topics = topic_data.get('topics', [])
        
        knowledge = NCERT_KNOWLEDGE.get(chapter, {})
        
        # Generate question generation samples
        if knowledge.get('mcq_pool'):
            for q, opts, ans, exp in knowledge['mcq_pool'][:5]:  # Limit per chapter
                instruction = f"Generate an MCQ question for Class {class_num} {subject} - {chapter}"
                response = f"Question: {q}\nOptions:\nA) {opts[0]}\nB) {opts[1]}\nC) {opts[2]}\nD) {opts[3]}\nAnswer: {ans}\nExplanation: {exp}"
                training_samples.append({
                    "prompt": f"### Instruction:\n{instruction}\n\n### Input:\n{', '.join(topics[:3])}\n\n### Response:",
                    "completion": response
                })
        
        # Generate explanation samples
        if knowledge.get('key_concepts'):
            for term, definition in knowledge['key_concepts'][:3]:
                instruction = f"Explain the concept of {term} for Class {class_num} {subject}"
                training_samples.append({
                    "prompt": f"### Instruction:\n{instruction}\n\n### Input:\n\n### Response:",
                    "completion": definition
                })
        
        # Generate short answer samples
        if knowledge.get('short_answers'):
            for q, ans in knowledge['short_answers'][:3]:
                instruction = f"Answer this question for Class {class_num} {subject}"
                training_samples.append({
                    "prompt": f"### Instruction:\n{instruction}\n\n### Input:\n{q}\n\n### Response:",
                    "completion": ans
                })
    
    # Shuffle and save
    random.shuffle(training_samples)
    
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATASET_FILE, 'w', encoding='utf-8') as f:
        for sample in training_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    print(f"✅ Generated {len(training_samples)} training samples")
    print(f"📁 Saved to: {DATASET_FILE}")
    return True


def train_model():
    """Train model with QLoRA."""
    print("\n" + "=" * 60)
    print("Step 2: Training Model with QLoRA")
    print("=" * 60)
    
    if not DATASET_FILE.exists():
        print("❌ Training dataset not found! Run 'generate' first.")
        return False
    
    try:
        from src.train_lora import train_lora
        train_lora()
        print("✅ Training complete!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: pip install transformers accelerate peft trl datasets")
        return False
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False


def run_pipeline():
    """Run complete training pipeline."""
    print("\n" + "=" * 60)
    print("VedLinks Complete Training Pipeline")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    if not generate_training_data():
        return
    
    if not train_model():
        return
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETE")
    print("=" * 60)
    print(f"\nModel saved to: {OUTPUT_DIR}")
    print("\nTo start the server: python run.py")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nCommands:")
        print("  generate  - Generate training dataset from knowledge bank")
        print("  train     - Train model with QLoRA (requires dataset)")
        print("  all       - Run complete pipeline")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'generate':
        generate_training_data()
    elif command == 'train':
        train_model()
    elif command == 'all':
        run_pipeline()
    else:
        print(f"Unknown command: {command}")
        print("Use: generate | train | all")


if __name__ == "__main__":
    main()
