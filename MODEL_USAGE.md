# How to Use Your Fine-Tuned Model

## 🎯 Quick Start

Run the demo script:
```powershell
python use_model.py
```

This will:
1. Load your trained model from `output/qlora_tuned_model/`
2. Show example generations
3. Let you try it interactively

---

## 📝 Usage in Your Own Code

### Option 1: Using the Demo Functions

```python
from use_model import load_model, generate_educational_content

# Load the model once
model, tokenizer, device = load_model()

# Generate content for any topic
topic = "Photosynthesis is the process..."
content = generate_educational_content(model, tokenizer, device, topic)
print(content)
```

### Option 2: Direct Usage

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load model
base_model = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    trust_remote_code=True
)
model = PeftModel.from_pretrained(base_model, "output/qlora_tuned_model")
tokenizer = AutoTokenizer.from_pretrained("output/qlora_tuned_model")

# Move to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()

# Create prompt
prompt = """Generate educational content based on NCERT-style learning materials.

Create:
1. Student Q&A pairs that help understand the topic
2. Multiple choice questions with explanations
3. Teacher summary of key concepts

### Teacher Summary:
Your topic text here...

"""

# Generate
inputs = tokenizer(prompt, return_tensors="pt").to(device)
outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.7)
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
```

---

## 🔧 Model Details

**Location**: `output/qlora_tuned_model/`

**Files**:
- `adapter_config.json` - LoRA configuration
- `adapter_model.safetensors` - Trained LoRA weights (~1.1MB)
- `tokenizer.json` - Tokenizer files
- `special_tokens_map.json` - Special tokens

**Architecture**:
- Base model: TinyLlama-1.1B-Chat-v1.0
- Fine-tuning method: LoRA (Low-Rank Adaptation)
- Trainable parameters: 1.1M (0.1% of total)
- Training data: 9 examples from your PDFs

---

## 💡 Generation Parameters

Adjust these for different outputs:

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=512,     # Maximum length of generation
    temperature=0.7,         # Higher = more creative (0.0-1.0)
    do_sample=True,          # Enable sampling
    top_p=0.9,              # Nucleus sampling threshold
    top_k=50,               # Top-k sampling
    repetition_penalty=1.2,  # Penalize repetition
)
```

**For educational content**:
- `temperature=0.7` - balanced creativity
- `temperature=0.3` - more focused/factual
- `temperature=1.0` - more diverse/creative

---

## 🚀 Use Cases

### 1. Batch Processing PDFs

```python
from use_model import load_model, generate_educational_content
from src.utils import load_documents

# Load model once
model, tokenizer, device = load_model()

# Load PDFs
documents = load_documents("data/raw")

# Generate for each
for filename, text in documents:
    content = generate_educational_content(model, tokenizer, device, text[:500])
    print(f"\n{filename}:\n{content}\n")
```

### 2. REST API Server

```python
from fastapi import FastAPI
from use_model import load_model, generate_educational_content

app = FastAPI()

# Load model at startup
model, tokenizer, device = load_model()

@app.post("/generate")
def generate(topic: str):
    content = generate_educational_content(model, tokenizer, device, topic)
    return {"content": content}

# Run with: uvicorn api:app --reload
```

### 3. Streamlit Web App

```python
import streamlit as st
from use_model import load_model, generate_educational_content

st.title("Educational Content Generator")

# Load model (cached)
@st.cache_resource
def get_model():
    return load_model()

model, tokenizer, device = get_model()

# Input
topic = st.text_area("Enter your topic/passage:")

if st.button("Generate"):
    with st.spinner("Generating..."):
        content = generate_educational_content(model, tokenizer, device, topic)
        st.markdown(content)

# Run with: streamlit run app.py
```

---

## 📊 Model Performance

**Training Results**:
- Final loss: 2.065
- Training time: ~4 minutes on RTX 2050
- Epochs: 3
- Dataset: 9 examples

**Expected Quality**:
- ✅ Good for generating Q&A pairs
- ✅ Good for simple explanations
- ⚠️ May need more training data for complex topics
- ⚠️ Consider using larger base model (phi-2) for better results

---

## 🔄 Updating the Model

To retrain with more data:

1. Add more PDFs to `data/raw/`
2. Regenerate dataset: `python -m src.dataset_generator`
3. Retrain: `python train_simple.py`

Your model will be updated in `output/qlora_tuned_model/`

---

## 📦 Sharing the Model

Your model is **very small** (~1.1MB LoRA weights):

```powershell
# Zip for sharing
Compress-Archive -Path output/qlora_tuned_model -DestinationPath vedlinks_model.zip

# Upload to Hugging Face Hub (optional)
python -c "from huggingface_hub import HfApi; HfApi().upload_folder(folder_path='output/qlora_tuned_model', repo_id='your-username/vedlinks-tuned')"
```

---

## 🎯 Next Steps

1. **Test the model**: `python use_model.py`
2. **Add more training data**: Get higher success rate
3. **Try bigger base model**: Switch to `microsoft/phi-2` in `.env`
4. **Build an app**: Use FastAPI or Streamlit
5. **Deploy**: Host on Hugging Face Spaces or your server

---

## ❓ Troubleshooting

**"CUDA out of memory"**:
- Model is on GPU, reduce `max_new_tokens`
- Or move to CPU: `model = model.to("cpu")`

**"Slow generation"**:
- Normal on CPU (~30s per generation)
- On GPU should be ~2-3s

**"Poor quality outputs"**:
- Need more training data (currently only 9 examples)
- Try better base model (phi-2)
- Adjust temperature (0.3-0.7 range)

---

**Your model is ready to use! 🎉**
