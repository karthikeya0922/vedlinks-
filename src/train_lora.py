"""
QLoRA fine-tuning script using trl SFTTrainer.
"""

import os
import sys
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Fix encoding issues on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Suppress bitsandbytes warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

load_dotenv()

# Configuration from environment
MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output/qlora_tuned_model")
LORA_R = int(os.getenv("LORA_R", "8"))
LORA_ALPHA = int(os.getenv("LORA_ALPHA", "16"))
LEARNING_RATE = float(os.getenv("LEARNING_RATE", "2e-4"))
NUM_TRAIN_EPOCHS = int(os.getenv("NUM_TRAIN_EPOCHS", "3"))
MAX_SEQ_LENGTH = int(os.getenv("MAX_SEQ_LENGTH", "512"))
PER_DEVICE_TRAIN_BATCH_SIZE = int(os.getenv("PER_DEVICE_TRAIN_BATCH_SIZE", "4"))


def train_lora():
    """Train model with QLoRA using trl SFTTrainer."""
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, TrainerCallback
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from datasets import load_dataset
        from trl import SFTTrainer, SFTConfig

        class ProgressPrinterCallback(TrainerCallback):
            """Custom callback to print training progress clearly for the wrapper."""
            def on_log(self, args, state, control, logs=None, **kwargs):
                if logs:
                    loss = logs.get("loss", "N/A")
                    epoch = state.epoch if state.epoch is not None else 0
                    step = state.global_step
                    # Clearly marked for app.py to parse
                    print(f"PROGRESS_UPDATE | Epoch: {epoch:.2f} | Step: {step} | Loss: {loss}")

            def on_epoch_begin(self, args, state, control, **kwargs):
                print(f"\n=== EPOCH {int(state.epoch) + 1} BEGUN ===")

            def on_epoch_end(self, args, state, control, **kwargs):
                print(f"=== EPOCH {int(state.epoch)} FINISHED ===")
        
        print("="*60)
        print("VedLinks QLoRA Training")
        print("="*60)
        
        # Check for finetune dataset
        finetune_file = "data/finetune_dataset.jsonl"
        if not Path(finetune_file).exists():
            print(f"  Finetune dataset not found: {finetune_file}")
            print("Please run: python -m src.utils.prepare_for_finetune")
            sys.exit(1)
        
        # Load dataset
        print(f"\n  Loading dataset from {finetune_file}...")
        dataset = load_dataset("json", data_files=finetune_file, split="train")
        print(f"  Loaded {len(dataset)} training examples")
        
        # Load tokenizer
        print(f"\n  Loading tokenizer: {MODEL_NAME}")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        
        # Set padding token if not present
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load model
        print(f"\n  Loading model: {MODEL_NAME}")
        
        # Check for GPU and CUDA availability
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        # Clear VRAM cache
        if device == "cuda":
            torch.cuda.empty_cache()
            
        # Configure Quantization
        bnb_config = None
        if device == "cuda":
            try:
                from transformers import BitsAndBytesConfig
                print("  Attempting to configure 4-bit quantization...")
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                )
                print("  4-bit quantization configuration created.")
            except ImportError:
                print("  bitsandbytes not found or incompatible. Falling back to float16 training.")
        
        # Load model
        print(f"\n  Loading model: {MODEL_NAME}")
        
        if device == "cuda":
            if bnb_config:
                print("  Loading model with 4-bit quantization on GPU (CUDA)...")
                model = AutoModelForCausalLM.from_pretrained(
                    MODEL_NAME,
                    quantization_config=bnb_config,
                    device_map="auto",
                    trust_remote_code=True,
                )
            else:
                print("  Loading model with float16 on GPU (CUDA)...")
                model = AutoModelForCausalLM.from_pretrained(
                    MODEL_NAME,
                    torch_dtype=torch.float16,
                    device_map="auto",
                    trust_remote_code=True,
                )
            print("  Loaded model successfully onto GPU (CUDA)")
        else:
            # CPU mode - no quantization
            print("   Running on CPU - training will be slow")
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                trust_remote_code=True,
            )
        
        # Configure LoRA
        print(f"\n   Configuring LoRA (r={LORA_R}, alpha={LORA_ALPHA})...")
        lora_config = LoraConfig(
            r=LORA_R,
            lora_alpha=LORA_ALPHA,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # Expanded target modules
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        )
        
        # Enable gradient checkpointing to save VRAM
        model.gradient_checkpointing_enable()
        
        # Get PEFT model
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()
        
        # Training arguments (using SFTConfig for trl v0.29+)
        print(f"\n  Setting up training arguments...")
        training_args = SFTConfig(
            output_dir=OUTPUT_DIR,
            num_train_epochs=NUM_TRAIN_EPOCHS,
            per_device_train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
            gradient_accumulation_steps=4,
            learning_rate=LEARNING_RATE,
            logging_steps=10,
            save_steps=100,
            save_total_limit=2,
            fp16=device == "cuda",
            optim="adamw_torch",  # Use standard optimizer (no bitsandbytes required)
            warmup_steps=20,
            gradient_checkpointing=True,
            logging_dir=f"{OUTPUT_DIR}/logs",
            report_to="none",  # Change to "wandb" if you want W&B logging
            dataset_text_field="text",
            max_length=MAX_SEQ_LENGTH,
            packing=False,
        )
        
        # Preprocess dataset to add 'text' field
        def add_text_field(example):
            """Combine prompt and completion into a single text field."""
            example['text'] = f"{example['prompt']}\n{example['completion']}"
            return example
        
        print(f"\n  Preprocessing dataset...")
        dataset = dataset.map(add_text_field)
        
        # Create trainer
        print(f"\n   Creating SFTTrainer...")
        trainer = SFTTrainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
            processing_class=tokenizer,
            callbacks=[ProgressPrinterCallback()],
        )
        
        # Train
        print(f"\n  Starting training...")
        print(f"Epochs: {NUM_TRAIN_EPOCHS}")
        print(f"Batch size: {PER_DEVICE_TRAIN_BATCH_SIZE}")
        print(f"Learning rate: {LEARNING_RATE}")
        print(f"Output: {OUTPUT_DIR}")
        print()
        
        trainer.train()
        
        # Save final model
        print(f"\n  Saving final model to {OUTPUT_DIR}...")
        trainer.save_model()
        tokenizer.save_pretrained(OUTPUT_DIR)
        
        print("\n" + "="*60)
        print("  TRAINING COMPLETE")
        print("="*60)
        print(f"Model saved to: {OUTPUT_DIR}")
        print("\nTo use the model:")
        print(f"  from transformers import AutoModelForCausalLM, AutoTokenizer")
        print(f"  model = AutoModelForCausalLM.from_pretrained('{OUTPUT_DIR}')")
        print(f"  tokenizer = AutoTokenizer.from_pretrained('{OUTPUT_DIR}')")
        
    except ImportError as e:
        print(f"  Missing dependency: {e}")
        print("\nPlease install required packages:")
        print("  pip install transformers accelerate peft trl bitsandbytes datasets")
        sys.exit(1)
    except Exception as e:
        print(f"\n  Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        train_lora()
    except KeyboardInterrupt:
        print("\n\n   Training interrupted by user")
        sys.exit(0)
