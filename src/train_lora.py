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
MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
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
            
        bnb_config = None
        use_bnb = False
        if device == "cuda":
            try:
                from transformers import BitsAndBytesConfig
                import bitsandbytes as bnb_lib
                print("  Attempting to configure 4-bit quantization...")
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                )
                use_bnb = True
                print("  4-bit quantization configuration created.")
            except ImportError:
                print("  bitsandbytes not found. Falling back to float16 training.")
            except Exception as e:
                print(f"  bitsandbytes error: {e}. Falling back to float16 training.")
                bnb_config = None
                use_bnb = False
        
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
            
            # Prepare for k-bit training if using quantization
            if bnb_config:
                print("  Preparing model for k-bit training (QLoRA)...")
                model = prepare_model_for_kbit_training(model)
        else:
            # CPU mode - no quantization
            print("   Running on CPU - training will be slow")
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                trust_remote_code=True,
            )
        
        # Check for existing adapter for incremental training
        adapter_path = os.path.join(OUTPUT_DIR, "adapter_config.json")
        if os.path.exists(adapter_path):
            print(f"\n   Loading existing LoRA adapter from {OUTPUT_DIR} for incremental training...")
            from peft import PeftModel
            model = PeftModel.from_pretrained(model, OUTPUT_DIR, is_trainable=True)
            model.print_trainable_parameters()
        else:
            # Configure new LoRA
            print(f"\n   Configuring new LoRA (r={LORA_R}, alpha={LORA_ALPHA})...")
            lora_config = LoraConfig(
                r=LORA_R,
                lora_alpha=LORA_ALPHA,
                target_modules=["q_proj", "v_proj"],
                lora_dropout=0.05,
                bias="none",
                task_type="CAUSAL_LM",
            )
            
            # Get PEFT model
            model = get_peft_model(model, lora_config)
            model.print_trainable_parameters()
        
        # Choose optimizer based on bitsandbytes availability
        optim = "paged_adamw_32bit" if use_bnb else "adamw_torch"
        use_gradient_checkpointing = (device == "cuda")
        
        # Build SFTConfig args dynamically for version compatibility
        import inspect
        sft_params = set(inspect.signature(SFTConfig.__init__).parameters.keys())
        
        sft_kwargs = {
            "output_dir": OUTPUT_DIR,
            "num_train_epochs": NUM_TRAIN_EPOCHS,
            "per_device_train_batch_size": PER_DEVICE_TRAIN_BATCH_SIZE,
            "gradient_accumulation_steps": 4,
            "learning_rate": LEARNING_RATE,
            "logging_steps": 10,
            "save_steps": 100,
            "save_total_limit": 2,
            "fp16": (device == "cuda"),
            "bf16": False,  # Explicitly disable bf16 to prevent CPU crash
            "optim": optim,
            "warmup_steps": 20,
            "gradient_checkpointing": use_gradient_checkpointing,
            "logging_dir": f"{OUTPUT_DIR}/logs",
            "report_to": "none",
        }
        
        # CPU-specific: tell trainer to use CPU explicitly (version-safe)
        if device == "cpu":
            for cpu_key, cpu_val in {"use_cpu": True, "no_cuda": True}.items():
                if cpu_key in sft_params or 'kwargs' in sft_params:
                    sft_kwargs[cpu_key] = cpu_val
        
        # Add optional params only if SFTConfig supports them
        optional_params = {
            "dataset_text_field": "text",
            "max_seq_length": MAX_SEQ_LENGTH,
            "max_length": MAX_SEQ_LENGTH,
            "packing": False,
            "overwrite_output_dir": True,
            "remove_unused_columns": True,
            "dataloader_num_workers": 0 if sys.platform == 'win32' else 2,
        }
        
        for key, val in optional_params.items():
            if key in sft_params or 'kwargs' in sft_params:
                sft_kwargs[key] = val
        
        # Avoid duplicate max_length vs max_seq_length
        if "max_seq_length" in sft_kwargs and "max_length" in sft_kwargs:
            if "max_seq_length" in sft_params:
                del sft_kwargs["max_length"]
            else:
                del sft_kwargs["max_seq_length"]
        
        print(f"\n  SFTConfig params: {list(sft_kwargs.keys())}")
        training_args = SFTConfig(**sft_kwargs)
        
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
            tokenizer=tokenizer,
            callbacks=[ProgressPrinterCallback()],
        )
        
        # Train
        print(f"\n  Starting training...")
        print(f"Epochs: {NUM_TRAIN_EPOCHS}")
        print(f"Batch size: {PER_DEVICE_TRAIN_BATCH_SIZE}")
        print(f"Learning rate: {LEARNING_RATE}")
        print(f"Output: {OUTPUT_DIR}")
        print()
        
        # Train (Sequential fine-tuning means we treat it as a new run, not resuming trainer state)
        trainer.train()
        
        # Save final model
        print(f"\n  Saving final model to {OUTPUT_DIR}...")
        trainer.save_model()
        tokenizer.save_pretrained(OUTPUT_DIR)
        
        # Mark pending topics as trained
        pending_file = "data/pending_topics.json"
        if os.path.exists(pending_file):
            import json
            try:
                with open(pending_file, 'r', encoding='utf-8') as f:
                    new_topics = json.load(f)
                
                registry_file = "data/topic_registry.json"
                if os.path.exists(registry_file):
                    with open(registry_file, 'r', encoding='utf-8') as f:
                        registry = json.load(f)
                    
                    for topic in new_topics:
                        if topic in registry.get('files', {}):
                            registry['files'][topic]['is_trained'] = True
                            print(f"  Marked {topic} as trained.")
                    
                    with open(registry_file, 'w', encoding='utf-8') as f:
                        json.dump(registry, f, indent=2, ensure_ascii=False)
                
                os.remove(pending_file)
            except Exception as e:
                print(f"  Failed to update topic_registry.json: {e}")
        
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
