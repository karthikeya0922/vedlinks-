#!/usr/bin/env python3
"""
Script to push the fine-tuned VedLinks model to Hugging Face Hub.
This script merges the LoRA adapter with the base model and pushes the full model to HF Hub.

Requires:
- A Hugging Face account
- pip install huggingface_hub torch peft transformers
- Run `huggingface-cli login` in your terminal first, or set HF_API_TOKEN in your .env file
"""

import os
import sys
from pathlib import Path

# Add parent directory to path so we can import from src if needed
sys.path.append(str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

def push_to_hub():
    # Attempt to load token from .env
    load_dotenv()
    
    hf_token = os.environ.get("HF_API_TOKEN")
    if not hf_token:
        print("WARNING: HF_API_TOKEN not found in .env file.")
        print("Ensure you have run `huggingface-cli login` in your terminal.")
        choice = input("Continue anyway? (y/n): ")
        if choice.lower() != 'y':
            return

    model_dir = Path("output/qlora_tuned_model")
    
    if not model_dir.exists() or not (model_dir / "adapter_config.json").exists():
        print(f"Error: {model_dir} not found or no adapter_config.json.")
        print("Please ensure you have completed the model fine-tuning process first.")
        return
        
    print("\n--- Hugging Face Model Publisher ---")
    hf_repo = input("Enter your Hugging Face model repository name (format: 'your-username/vedlinks-model'): ").strip()
    
    if not hf_repo or '/' not in hf_repo:
        print("Error: Invalid repository name format. It must be 'username/model-name'.")
        return

    print("\nLoading heavy ML libraries... (This may take a moment)")
    import torch
    from peft import PeftModel, PeftConfig
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print("\n1/5 Reading LoRA configuration...")
    try:
        config = PeftConfig.from_pretrained(str(model_dir))
        base_model_name = config.base_model_name_or_path
    except Exception as e:
        print(f"Error reading configuration: {e}")
        return
        
    print(f"\n2/5 Loading tokenizer from {model_dir}...")
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
    
    print(f"\n3/5 Loading base model '{base_model_name}'...")
    print("This requires sufficient RAM and may take several minutes.")
    try:
        # Load the base model
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
    except Exception as e:
        print(f"Error loading base model: {e}")
        return
        
    print(f"\n4/5 Loading LoRA adapter and merging with base model...")
    try:
        model = PeftModel.from_pretrained(base_model, str(model_dir))
        # Merge the LoRA weights with the base model weights
        # This is necessary because HF Inference API prefers a single merged model
        print("Merging weights... (this may take a while to process)")
        model = model.merge_and_unload()
    except Exception as e:
        print(f"Error merging model: {e}")
        return
        
    print(f"\n5/5 Pushing full model to Hugging Face Hub: {hf_repo}...")
    try:
        kwargs = {}
        if hf_token:
            kwargs['token'] = hf_token
            
        # Push to hub
        tokenizer.push_to_hub(hf_repo, **kwargs)
        model.push_to_hub(hf_repo, **kwargs)
        
        print("\n✅ SUCCESS!")
        print(f"Your model is now available at: https://huggingface.co/{hf_repo}")
        print("\n--- NEXT STEPS FOR VERCEL DEPLOYMENT ---")
        print("1. Update your Vercel Environment Variables:")
        print(f"   USE_HF_API = True")
        print(f"   HF_MODEL_ID = {hf_repo}")
        print(f"   HF_API_TOKEN = <your_hugging_face_access_token>")
        
    except Exception as e:
        print(f"\n❌ Error pushing to Hugging Face Hub: {e}")
        print("Check your internet connection and verify that your token has 'write' permissions.")

if __name__ == "__main__":
    push_to_hub()
