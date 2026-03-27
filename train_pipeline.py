"""
VedLinks Training Pipeline
===========================
Complete pipeline for generating training data and fine-tuning the model.

Generates rich training data from the FULL NCERT_KNOWLEDGE bank covering
all chapters, main headings, and important topics. The fine-tuned model
learns NCERT-style question generation, concept explanation, and answering.

Usage:
    python train_pipeline.py generate   - Generate training dataset
    python train_pipeline.py train      - Train the model with LoRA
    python train_pipeline.py all        - Run complete pipeline
"""

import sys
import json
import random
import os
from pathlib import Path
from datetime import datetime
import re
from src.pdf_processor import get_chapter_text

# Fix encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Configuration
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output/qlora_tuned_model")
DATASET_FILE = DATA_DIR / "finetune_dataset.jsonl"


def generate_training_data():
    """Generate comprehensive training dataset from the full NCERT_KNOWLEDGE bank."""
    print("=" * 60)
    print("Step 1: Generating Enhanced Training Dataset")
    print("=" * 60)
    
    from question_paper_generator import NCERT_KNOWLEDGE
    
    training_samples = []
    
    is_incremental = (OUTPUT_DIR / "adapter_config.json").exists()
    if is_incremental:
        print("\n  Incremental training detected. Skipping static NCERT knowledge bank.")

    # Iterate over ALL chapters in the knowledge bank
    for chapter_name, knowledge in NCERT_KNOWLEDGE.items():
        if is_incremental:
            continue

        print(f"\n  Processing: {chapter_name}")
        chapter_samples = 0
        
        # --- 1. Key Concept Explanation Samples ---
        for const_item in knowledge.get('key_concepts', []):
            if len(const_item) >= 2:
                term, definition = const_item[:2]
            else:
                continue
            # "Explain concept" instruction
            training_samples.append({
                "prompt": f"### Instruction:\nExplain the concept of '{term}' from the chapter '{chapter_name}'.\n\n### Input:\n\n### Response:",
                "completion": definition
            })
            # "What is" question style
            training_samples.append({
                "prompt": f"### Instruction:\nWhat is {term}?\n\n### Input:\nThis is from the NCERT chapter '{chapter_name}'.\n\n### Response:",
                "completion": f"{term}: {definition}"
            })
            chapter_samples += 2
        
        # --- 2. MCQ Generation Samples ---
        for mcq_item in knowledge.get('mcq_pool', []):
            if len(mcq_item) >= 4:
                q, opts, ans, exp = mcq_item[:4]
            else:
                continue
            # "Generate MCQ" instruction
            response = f"Question: {q}\nOptions:\nA) {opts[0]}\nB) {opts[1]}\nC) {opts[2]}\nD) {opts[3]}\nAnswer: {ans}\nExplanation: {exp}"
            training_samples.append({
                "prompt": f"### Instruction:\nGenerate an MCQ question about '{chapter_name}'.\n\n### Input:\n\n### Response:",
                "completion": response
            })
            # "Answer MCQ" instruction
            options_text = "\n".join([f"{chr(65+i)}) {o}" for i, o in enumerate(opts)])
            training_samples.append({
                "prompt": f"### Instruction:\nAnswer the following MCQ from '{chapter_name}'.\n\n### Input:\n{q}\n{options_text}\n\n### Response:",
                "completion": f"The correct answer is: {ans}\nExplanation: {exp}"
            })
            chapter_samples += 2
        
        # --- 3. Fill in the Blank Samples ---
        for fb_item in knowledge.get('fill_blanks', []):
            if len(fb_item) >= 2:
                q, ans = fb_item[:2]
            else:
                continue
            training_samples.append({
                "prompt": f"### Instruction:\nFill in the blank for the following statement from '{chapter_name}'.\n\n### Input:\n{q}\n\n### Response:",
                "completion": f"The answer is: {ans}"
            })
            # Also generate as a question
            training_samples.append({
                "prompt": f"### Instruction:\nGenerate a fill-in-the-blank question about '{chapter_name}'.\n\n### Input:\n\n### Response:",
                "completion": f"{q}\nAnswer: {ans}"
            })
            chapter_samples += 2
        
        # --- 4. Short Answer Samples ---
        for sa_item in knowledge.get('short_answers', []):
            if len(sa_item) >= 2:
                q, ans = sa_item[:2]
            else:
                continue
            training_samples.append({
                "prompt": f"### Instruction:\nAnswer the following short question from '{chapter_name}'.\n\n### Input:\n{q}\n\n### Response:",
                "completion": ans
            })
            # "Generate short answer question" instruction
            training_samples.append({
                "prompt": f"### Instruction:\nGenerate a short answer question about '{chapter_name}'.\n\n### Input:\n\n### Response:",
                "completion": f"Question: {q}\nAnswer: {ans}"
            })
            chapter_samples += 2
        
        # --- 5. Long Answer / Comprehensive Explanation Samples ---
        for la_item in knowledge.get('long_answers', []):
            if len(la_item) >= 2:
                q, ans = la_item[:2]
            else:
                continue
            training_samples.append({
                "prompt": f"### Instruction:\nProvide a detailed answer for the following question from '{chapter_name}'.\n\n### Input:\n{q}\n\n### Response:",
                "completion": ans
            })
            chapter_samples += 1
        
        # --- 6. Chapter Summary Sample ---
        concepts = knowledge.get('key_concepts', [])
        if concepts:
            concept_list = "\n".join([f"- {term}: {defn}" for term, defn in concepts])
            training_samples.append({
                "prompt": f"### Instruction:\nList the key concepts and main topics covered in the chapter '{chapter_name}'.\n\n### Input:\n\n### Response:",
                "completion": f"Key concepts in '{chapter_name}':\n\n{concept_list}"
            })
            chapter_samples += 1
        
        print(f"      Generated {chapter_samples} samples")
    
    # --- 7. Dynamic Text-to-Sample Generation from Uploaded PDFs ---
    print("\n  Processing Dynamic Uploads from topic_registry.json...")
    REGISTRY_FILE = DATA_DIR / "topic_registry.json"
    
    new_topics = []
    
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            registry = json.load(f)
            
        pdf_samples = 0
        for topic_file, meta in registry.get('files', {}).items():
            if meta.get('is_trained', False):
                print(f"    Skipping already trained file: {topic_file}")
                continue
                
            new_topics.append(topic_file)
            class_val = meta.get('class', 'N/A')
            subject = meta.get('subject', 'N/A')
            chapter_num = meta.get('chapter_number', 'N/A')
            chapter_name = meta.get('chapter', 'N/A')
            
            # Context string for labeling
            context_label = f"Class {class_val} {subject} Chapter {chapter_num}: {chapter_name}"
            
            for pdf_name in meta.get('source_pdfs', []):
                pdf_path = DATA_DIR / "raw" / pdf_name
                if pdf_path.exists():
                    print(f"    Extracting from: {pdf_name} ({context_label})")
                    text_content = get_chapter_text(str(pdf_path))
                    
                    if not text_content:
                        continue
                    
                    # ── Split into clean sentences for rich sample generation ──
                    all_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text_content) 
                                     if len(s.strip()) > 30 and not re.match(r'^(Figure|Activity|Table|##|#|\d+\.)', s.strip(), re.I)]
                    
                    # Split text into chunks for paragraph-level samples
                    chunks = re.split(r'\n\n+', text_content)
                    
                    for chunk in chunks:
                        chunk = chunk.strip()
                        if len(chunk) < 80: continue
                        
                        sentences = [s.strip() for s in chunk.split('.') if len(s.strip()) > 15]
                        if not sentences: continue
                        
                        # ── Type 1: Summarize section ──
                        training_samples.append({
                            "prompt": f"### Instruction:\nSummarize this section from {context_label}.\n\n### Input:\n{chunk[:400]}\n\n### Response:",
                            "completion": f"This section explains that {sentences[0]}." + (f" Additionally, {sentences[1]}." if len(sentences) > 1 else "")
                        })
                        
                        # ── Type 2: Key insight ──
                        if len(sentences) > 1:
                            training_samples.append({
                                "prompt": f"### Instruction:\nWhat is a key insight from this text about {chapter_name}?\n\n### Input:\n{chunk[:200]}\n\n### Response:",
                                "completion": f"An important point is that {sentences[-1]}."
                            })
                        
                        # ── Type 3: Generate MCQ from text ──
                        for sent in sentences[:3]:
                            words = [w for w in re.findall(r'[A-Za-z]{5,}', sent) if w.lower() not in {'these', 'those', 'which', 'where', 'their', 'there', 'about', 'other', 'would', 'could', 'should'}]
                            if words:
                                keyword = random.choice(words[:3])
                                blanked = sent.replace(keyword, '_______', 1)
                                training_samples.append({
                                    "prompt": f"### Instruction:\nGenerate an MCQ question from {context_label}.\n\n### Input:\n{sent}\n\n### Response:",
                                    "completion": f"Question: {blanked}\nA) {keyword}\nB) process\nC) element\nD) compound\nAnswer: A) {keyword}"
                                })
                        
                        # ── Type 4: Fill in the blank ──
                        for sent in sentences[:2]:
                            words = [w for w in re.findall(r'[A-Za-z]{5,}', sent) if w.lower() not in {'these', 'those', 'which', 'where', 'their', 'there', 'about'}]
                            if words:
                                keyword = random.choice(words[:3])
                                blanked = sent.replace(keyword, '_______', 1)
                                training_samples.append({
                                    "prompt": f"### Instruction:\nCreate a fill-in-the-blank question from {context_label}.\n\n### Input:\n{sent}\n\n### Response:",
                                    "completion": f"Fill in the blank: {blanked}\nAnswer: {keyword}"
                                })
                        
                        # ── Type 5: Short answer question ──
                        if len(sentences) >= 2:
                            training_samples.append({
                                "prompt": f"### Instruction:\nCreate a short answer question from {context_label}.\n\n### Input:\n{'. '.join(sentences[:2])}\n\n### Response:",
                                "completion": f"Question: Explain briefly: {sentences[0].split(',')[0]}.\nAnswer: {'. '.join(sentences[:2])}."
                            })
                        
                        # ── Type 6: Long answer / detailed explanation ──
                        if len(chunk) > 200:
                            training_samples.append({
                                "prompt": f"### Instruction:\nWrite a detailed answer about the following topic from {context_label}.\n\n### Input:\n{sentences[0][:100]}\n\n### Response:",
                                "completion": chunk[:600]
                            })
                        
                        # ── Type 7: Define / What is ──
                        for sent in sentences:
                            m = re.match(r'^(.*?)\s+(?:is|are|is called|is known as|refers to|is defined as)\s+(.*)', sent, re.I)
                            if m and 2 <= len(m.group(1).split()) <= 6:
                                term = m.group(1).strip()
                                defn = m.group(2).strip()
                                training_samples.append({
                                    "prompt": f"### Instruction:\nWhat is {term}?\n\n### Input:\nFrom {context_label}\n\n### Response:",
                                    "completion": f"{term} {sent[sent.lower().find(' is'):]}."
                                })
                                break  # One definition per chunk
                        
                        # ── Type 8: Concept explanation ──
                        if len(sentences) >= 3:
                            training_samples.append({
                                "prompt": f"### Instruction:\nExplain the concept discussed in the following text from {context_label}.\n\n### Input:\n{'. '.join(sentences[:3])}.\n\n### Response:",
                                "completion": f"The text discusses {sentences[0].lower()}. {'. '.join(sentences[1:3])}."
                            })
                        
                        pdf_samples += 8  # approximate count per chunk
                        
        print(f"      Generated {pdf_samples} samples from uploaded PDFs")
    
    if not training_samples:
        print("\n  No new data to train on. All files are already trained.")
        return []
        
    # Write pending topics to a file so train_lora.py can mark them as trained
    pending_file = DATA_DIR / "pending_topics.json"
    with open(pending_file, 'w', encoding='utf-8') as f:
        json.dump(new_topics, f)
        
    # Shuffle and save
    random.shuffle(training_samples)
    
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATASET_FILE, 'w', encoding='utf-8') as f:
        for sample in training_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    total_chapters = len(NCERT_KNOWLEDGE)
    print(f"\n{'=' * 60}")
    print(f"  Generated {len(training_samples)} training samples")
    print(f"  Saved to: {DATASET_FILE}")
    print(f"{'=' * 60}")
    return new_topics


def train_model():
    """Train model with QLoRA."""
    print("\n" + "=" * 60)
    print("Step 2: Training Model with QLoRA")
    print("=" * 60)
    
    if not DATASET_FILE.exists():
        print("  Training dataset not found! Run 'generate' first.")
        return False
    
    # Show dataset stats
    with open(DATASET_FILE, 'r', encoding='utf-8') as f:
        sample_count = sum(1 for _ in f)
    print(f"  Dataset size: {sample_count} samples")
    
    try:
        from src.train_lora import train_lora
        train_lora()
        print("  Training complete!")
        return True
    except ImportError as e:
        print(f"  Missing dependency: {e}")
        print("Install with: pip install transformers accelerate peft trl datasets")
        return False
    except Exception as e:
        print(f"  Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_pipeline():
    """Run complete training pipeline."""
    print("\n" + "=" * 60)
    print("VedLinks Complete Training Pipeline")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    new_topics = generate_training_data()
    if new_topics is False:
        return
    if isinstance(new_topics, list) and len(new_topics) == 0 and (OUTPUT_DIR / "adapter_config.json").exists():
        print("\n" + "=" * 60)
        print("  NO NEW DATA. PIPELINE COMPLETE")
        print("=" * 60)
        return
    
    if not train_model():
        return
    
    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)
    print(f"\nModel saved to: {OUTPUT_DIR}")
    print("\nTo start the server: python app.py")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nCommands:")
        print("  generate  - Generate training dataset from full NCERT knowledge bank")
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
