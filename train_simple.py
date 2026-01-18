"""
Simplified LoRA training without bitsandbytes dependency.
"""

import os
import sys
import warnings
from pathlib import Path

# Fix encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Suppress warnings
warnings.filterwarnings('ignore')

# Set environment to avoid bitsandbytes
os.environ['BITSANDBYTES_NOWELCOME'] = '1'

from dotenv import load_dotenv
load_dotenv()

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset

# Configuration
MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/qlora_tuned_model")
LORA_R = int(os.getenv("LORA_R", "8"))
LORA_ALPHA = int(os.getenv("LORA_ALPHA", "16"))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", "2e-4"))
NUM_TRAIN_EPOCHS = int(os.getenv("NUM_TRAIN_EPOCHS", "3"))
MAX_SEQ_LENGTH = 256  # Reduced for 4GB VRAM
PER_DEVICE_TRAIN_BATCH_SIZE = 1  # Small batch for limited VRAM

def main():
    print("="*60)
    print("VedLinks LoRA Training (No Quantization)")
    print("="*60)
    
    # Check dataset
    finetune_file = "data/finetune_dataset.jsonl"
    if not Path(finetune_file).exists():
        print(f"❌ Dataset not found: {finetune_file}")
        return 1
    
    # Load dataset
    print(f"\n📚 Loading dataset...")
    dataset = load_dataset("json", data_files=finetune_file, split="train")
    print(f"✅ {len(dataset)} examples")
    
    # Preprocess - add 'text' field
    def add_text_field(example):
        example['text'] = f"{example['prompt']}\n\n{example['completion']}"
        return example
    
    dataset = dataset.map(add_text_field)
    
    #Load tokenizer
    print(f"\n🔤 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    print("✅ Tokenizer loaded")
    
    # Load model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n🤖 Loading model on {device}...")
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )
    
    # Move to device
    if device == "cuda":
        model = model.to(device)
    
    # Enable gradient checkpointing to save VRAM
    model.gradient_checkpointing_enable()
    
    print("✅ Model loaded")
    
    # Configure LoRA
    print(f"\n⚙️  Configuring LoRA...")
    lora_config = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Tokenize dataset
    print(f"\n📝 Tokenizing dataset...")
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=MAX_SEQ_LENGTH,
        )
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)
    tokenized_dataset = tokenized_dataset.add_column("labels", tokenized_dataset["input_ids"])
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=NUM_TRAIN_EPOCHS,
        per_device_train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        logging_steps=1,
        save_steps=100,
        save_total_limit=2,
        fp16=False,  # Disabled FP16 for compatibility
        optim="adamw_torch",
        warmup_steps=10,
        logging_dir=f"{OUTPUT_DIR}/logs",
        report_to="none",
    )
    
    # Trainer
    print(f"\n🏋️  Creating trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )
    
    # Train
    print(f"\n🚀 Training...")
    print(f"Epochs: {NUM_TRAIN_EPOCHS}, Batch: {PER_DEVICE_TRAIN_BATCH_SIZE}, LR: {LEARNING_RATE}")
    print()
    
    trainer.train()
    
    # Save
    print(f"\n💾 Saving model...")
    trainer.save_model()
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE")
    print("="*60)
    print(f"Model: {OUTPUT_DIR}")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
