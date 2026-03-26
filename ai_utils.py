"""
Shared AI Text Generation Utility for VedLinks.

This module provides AI text generation via the HF Space API or local model.
Extracted from app.py to avoid circular imports with question_paper_generator.py.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

FINETUNED_MODEL_PATH = Path(os.environ.get('OUTPUT_DIR', 'output/qlora_tuned_model'))

# Global state for local model (lazy loaded)
_ai_model = None
_ai_tokenizer = None
_ai_model_loaded = False


def is_ai_available() -> bool:
    """Check if AI generation is available (either HF API or local model)."""
    use_hf_api = os.environ.get('USE_HF_API', 'False').lower() == 'true'
    if use_hf_api:
        hf_space_url = os.environ.get('HF_SPACE_URL', '')
        hf_model = os.environ.get('HF_MODEL_ID', '')
        return bool(hf_space_url or hf_model)
    return FINETUNED_MODEL_PATH.exists() and (FINETUNED_MODEL_PATH / "adapter_config.json").exists()


def get_ai_model():
    """Lazy-load the fine-tuned LoRA model for AI question generation."""
    global _ai_model, _ai_tokenizer, _ai_model_loaded

    if _ai_model_loaded:
        return _ai_model, _ai_tokenizer

    if not FINETUNED_MODEL_PATH.exists() or not (FINETUNED_MODEL_PATH / "adapter_config.json").exists():
        print("No fine-tuned model found. AI generation will use HF API or knowledge bank.")
        _ai_model_loaded = True
        return None, None

    try:
        import torch
        from peft import PeftModel, PeftConfig
        from transformers import AutoModelForCausalLM, AutoTokenizer

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading fine-tuned AI model on {device}...")

        config = PeftConfig.from_pretrained(str(FINETUNED_MODEL_PATH))
        base_model_name = config.base_model_name_or_path

        _ai_tokenizer = AutoTokenizer.from_pretrained(str(FINETUNED_MODEL_PATH))
        if _ai_tokenizer.pad_token is None:
            _ai_tokenizer.pad_token = _ai_tokenizer.eos_token

        if device == "cuda":
            base_model = AutoModelForCausalLM.from_pretrained(
                base_model_name, torch_dtype=torch.float16,
                device_map="auto", trust_remote_code=True,
            )
        else:
            base_model = AutoModelForCausalLM.from_pretrained(
                base_model_name, trust_remote_code=True,
            )

        _ai_model = PeftModel.from_pretrained(base_model, str(FINETUNED_MODEL_PATH))
        _ai_model.eval()

        _ai_model_loaded = True
        print(f"AI model loaded on {device}")
        return _ai_model, _ai_tokenizer

    except Exception as e:
        print(f"Failed to load AI model: {e}")
        _ai_model_loaded = True
        return None, None


def generate_ai_text(prompt_text: str, max_new_tokens: int = 200) -> str:
    """Generate text using the HF Space API or local fine-tuned model.
    
    Returns the generated text string, or None on failure.
    """
    use_hf_api = os.environ.get('USE_HF_API', 'False').lower() == 'true'

    if use_hf_api:
        return _generate_via_hf_api(prompt_text, max_new_tokens)

    return _generate_via_local_model(prompt_text, max_new_tokens)


def _generate_via_hf_api(prompt_text: str, max_new_tokens: int) -> str:
    """Generate text using the Hugging Face Inference API or Space."""
    import requests

    hf_token = os.environ.get('HF_API_TOKEN', '')
    hf_model = os.environ.get('HF_MODEL_ID', '')
    hf_space_url = os.environ.get('HF_SPACE_URL', '')

    if not hf_token and not hf_space_url:
        print("HF_API_TOKEN or HF_SPACE_URL is required.")
        return None

    headers = {}
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"

    payload = {
        "inputs": prompt_text,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.2,
            "return_full_text": False
        }
    }

    if hf_space_url:
        API_URL = hf_space_url
    elif hf_model:
        API_URL = f"https://api-inference.huggingface.co/models/{hf_model}"
    else:
        print("Neither HF_SPACE_URL nor HF_MODEL_ID were provided.")
        return None

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                generated = result[0]['generated_text']
                if "### Response:" in generated:
                    response_text = generated.split("### Response:")[-1].strip()
                else:
                    response_text = generated.strip()
                return response_text if response_text else None
        print(f"HF API Error: {response.status_code} - {response.text[:200]}")
        return None
    except Exception as e:
        print(f"HF API Exception: {e}")
        return None


def _generate_via_local_model(prompt_text: str, max_new_tokens: int) -> str:
    """Generate text using the locally loaded fine-tuned model."""
    try:
        import torch
    except ImportError:
        return None

    model, tokenizer = get_ai_model()
    if model is None or tokenizer is None:
        return None

    try:
        inputs = tokenizer(prompt_text, return_tensors="pt", truncation=True, max_length=256)
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                repetition_penalty=1.2,
            )

        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        if "### Response:" in generated:
            response = generated.split("### Response:")[-1].strip()
        else:
            response = generated[len(prompt_text):].strip()

        return response if response else None
    except Exception as e:
        print(f"AI generation error: {e}")
        return None
