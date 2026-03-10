import os
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify

app = Flask(__name__)

# Basic authentication (set HF_SECRET_TOKEN in Space Secrets)
SECRET_TOKEN = os.environ.get("HF_SECRET_TOKEN", "")

# Load model path (assuming the merged model or adapter is here)
MODEL_PATH = "./model"

print("Loading model and tokenizer...")
try:
    # First try loading as a bare model (if merged)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH, 
        device_map="auto", 
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    )
    print("Bare model loaded.")
except Exception as e:
    print(f"Failed to load as bare model, trying to load as base+adapter: {e}")
    # If it fails, maybe it's just the adapter.
    # We must look at adapter_config.json to find the base model
    config = PeftConfig.from_pretrained(MODEL_PATH)
    base_model_name = config.base_model_name_or_path
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    )
    model = PeftModel.from_pretrained(base_model, MODEL_PATH)
    print("Base model + Adapter loaded.")

model.eval()
print("Setup complete.")

@app.route("/")
def index():
    return jsonify({"status": "VedLinks Inference Space is running!"})

@app.route("/api/generate", methods=["POST"])
def generate():
    # Authentication check
    auth_header = request.headers.get("Authorization")
    if SECRET_TOKEN:
        if not auth_header or auth_header != f"Bearer {SECRET_TOKEN}":
            return jsonify({"error": "Unauthorized"}), 401
            
    data = request.json
    if not data or "inputs" not in data:
        return jsonify({"error": "Missing 'inputs' field"}), 400
        
    prompt_text = data["inputs"]
    parameters = data.get("parameters", {})
    
    max_new_tokens = parameters.get("max_new_tokens", 250)
    temperature = parameters.get("temperature", 0.7)
    top_p = parameters.get("top_p", 0.9)
    repetition_penalty = parameters.get("repetition_penalty", 1.2)
    
    try:
        inputs = tokenizer(prompt_text, return_tensors="pt", truncation=True, max_length=256)
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                repetition_penalty=repetition_penalty,
            )
            
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return jsonify([{"generated_text": generated_text}])
        
    except Exception as e:
        print(f"Error during generation: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
