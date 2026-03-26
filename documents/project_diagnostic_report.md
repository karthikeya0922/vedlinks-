# 🚨 VEDLINKS AI PROJECT MASTER DIAGNOSTIC & PROBLEM REPORT 🚨
**Date**: March 26, 2026
**Target**: VedLinks Local AI Pipeline & Flask Architecture

## 📉 EXECUTIVE SUMMARY OF THE CURRENT STATE
Right now, the application suffers from a total "Architectural Disconnect". The user interface gives the illusion of fine-tuning an AI model and generating Question Papers based on uploaded textbooks, but under the hood, the infrastructure is heavily fragmented into two entirely separate, isolated pipelines that do not communicate with each other.

1. **The Training Pipeline (The 20-minute Freeze):** The background QLoRA training pipeline using HuggingFace crashes or hangs indefinitely because running 4-bit quantization on a local Windows machine via `bitsandbytes` without natively optimized CUDA paths freezes the Python process.
2. **The Fake Question Generator (The "Concept 1" Bug):** The `question_paper_generator.py` script NEVER calls the trained AI model. It uses a hardcoded dictionary. If the textbook's chapter isn't in that dictionary, it spits out `(a) Concept 1` as a hardcoded fallback.

---

## 🛑 PROBLEM 1: THE "FAKE AI" FALLBACK (WHY MCQs DON'T DISPLAY ACTUAL DATA)

**The Symptom:**
In the Dashboard (Question Paper screen), after the user selects a loaded chapter (like Class 9 Science: Atoms and Molecules), the generated paper displays questions like: 
* "Which concept is most important in this chapter?" 
* Options: (a) Concept 1, (b) Concept 2, (c) Concept 3, (d) Concept 4.

**The Root Cause (Codebase Evidence):**
Inside `c:\internship2\vedlinks-\question_paper_generator.py`, the AI has been entirely bypassed. The code explicitly avoids loading `TinyLlama` or `Mistral` for text generation! 

Look at line 35 of the generator class:
```python
def __init__(self, model_path="output/qlora_tuned_model"):
    self.model = None
    self.is_loaded = True  # Using knowledge bank, no model needed! <-- THE SMOKING GUN
```
When you click "Generate Paper", the Python backend calls `def generate_questions()`. 
Instead of prompting an LLM (Large Language Model) with your loaded PDF contexts to generate an exam, the code does this:
1. It tries to search for the chapter name inside a hardcoded Python dictionary called `NCERT_KNOWLEDGE`.
2. Because `NCERT_KNOWLEDGE` only has 1 or 2 hardcoded sample chapters (like `Food – Where Does It Come From?`), it fails to match your newly uploaded PDFs.
3. It immediately triggers `self._generate_fallback_questions()`.
4. The fallback function explicitly hardcodes the garbage output you are seeing in the UI:
```python
fallback_mcqs = [
    ("What is the main topic of this chapter?", ["Option A", "Option B", "Option C", "Option D"]),
    ("Which concept is most important in this chapter?", ["Concept 1", "Concept 2", "Concept 3", "Concept 4"]),
]
```
**Why this is fatal:** As long as this file is structured this way, your model could train perfectly 100 times, and the UI would *still* only output "Concept 1, Concept 2". The generation script is visually disconnected from the `qlora_tuned_model`.

---

## 🛑 PROBLEM 2: QLoRA LOCAL TRAINING FAILURE SECRETS (THE 20-MIN FREEZE)

**The Symptom:** 
When pressing "Fine-Tune AI on Uploads", the UI progress bar hangs at 30% for over 20 minutes, and the background process eventually terminates with `exit code 1`.

**The Root Cause:**
The fine-tuning script (`src/train_lora.py`) relies on `bitsandbytes` to load a 1.1 Billion parameter model (`TinyLlama`) into 4-bit quantized memory so it doesn't blow up your computer's RAM. 
However, on native Windows installations:
1. `bitsandbytes` famously breaks or freezes unless the user has specially compiled `bitsandbytes-windows` DLL files natively linked to their system's NVIDIA CUDA Toolkit.
2. If `train_lora.py` tries to load PyTorch using "CUDA" (GPU) but the bitsandbytes library fails to compile the memory wrappers, the terminal hangs during `BitsAndBytesConfig` evaluation. It goes dead silent (which is why your UI receives absolutely no logs past 30%, which is the "Data generation complete" stage).
3. The underlying `train_pipeline.py` script waits for `train_lora.py` to finish by running it via `subprocess.Popen`. It waits until the process times out or violently aborts.

**What we already fixed here:**
Originally, this pipeline was failing instantly because `trl`, `peft`, and `accelerate` were missing. I successfully installed those into the `.venv`. I also forced `app.py` to explicitly use `.venv/Scripts/python.exe` so the dependencies wouldn't be lost. But the underlying hardware limits of local QLoRA execution on Windows still trigger the 20-minute freeze.

---

## 🛑 PROBLEM 3: DATASET CORRUPTION (WHAT WE FIXED)

**The Symptom:**
The models, even if they could finish training, would generate horrible outputs, echoing back instructions instead of answering them.

**The Root Cause:**
In `src/dataset_generator.py`, the AI's training data was being built using hardcoded bracket templates. The Python loop was literally writing strings like:
`[simplified definition that a Class {class_num} student can understand]` directly into the `finetune_dataset.jsonl` file. 

**The Solution Applied:**
I wrote a Python injection script that gutted out all `[concept A]`, `[concept B]`, `[Example 1]`, and `Option A - correct concept` placeholders. I replaced them with dynamic logical inserts so the training JSONL file (which generated 1321 lines successfully) now contains *actual english words* that an AI can use to identify patterns, rather than literally trying to learn brackets.

---

## 🛑 PROBLEM 4: FLASK ENVIRONMENT DESYNC (WHAT WE FIXED)

**The Symptom:**
Python modules like 'trl' and 'transformers' were installed, but Flask kept insisting they didn't exist.

**The Root Cause:**
The `app.py` was being run by Windows PowerShell's global `python.exe`. But the `pip install` commands were installing packages into the isolated Virtual Environment directory (`c:\internship2\.venv\`). 

**The Solution Applied:**
I modified `subprocess.Popen` in `app.py` line 1943. Instead of using `sys.executable` (which changes based on how the user opened VS Code), I forcibly hardcoded it to resolve `os.path.join('.venv', 'Scripts', 'python.exe')`. Now, every single time the "Fine-Tune" button is clicked, it perfectly aligns with the required memory environment.

---

## 🛠️ THE MASTER SOLUTION PLAN: HOW TO MAKE IT 100% READY

To fix everything permanently and get the UI displaying *real* questions, the project needs the following architectural rewrites:

### PHASE 1: Hook `question_paper_generator.py` to an LLM
We must completely abolish the `NCERT_KNOWLEDGE` fake dictionary.
1. Rewrite `def generate_questions()` inside `question_paper_generator.py`.
2. Instead of matching a dictionary, it needs to invoke the AI inference loop. Ideally, you import `transformers` and map it to `output/qlora_tuned_model`.
3. Give the model a System Prompt: `"Create a 4-option multiple choice question based on the following text: {pdf_extracted_text}"`.
4. Parse the generated output into a JSON dictionary and pass it to the UI.

*(Alternative: If local LLMs are too heavy/crashing, replace `question_paper_generator.py` with standard API calls to OpenAI, Gemini, or Claude. This will solve the generation problem instantly without requiring a $2000 GPU).*

### PHASE 2: Fix the Windows QLoRA Hang 
To stop the 20-minute UI freeze during data training:
1. In `src/train_lora.py`, replace `BitsAndBytesConfig` initialization. If the user is on Windows without flawless CUDA SDK integration, we must force `load_in_8bit=False` and `load_in_4bit=False` and just use standard float16 training (if adequate GPU VRAM is available) or CPU/MPS fallback.
2. Alternatively, migrate the model fine-tuning logic to an external provider (like Azure AI, Replicate, or HuggingFace endpoints).

### PHASE 3: Connect Frontend to Real Document Context
When a user uploads a PDF on the upload screen:
1. Extract the text using `pdfplumber` (which is already happening inside `train_pipeline.py`).
2. Save that raw extracted text inside a `data/raw/{chapter_id}_text.txt` file.
3. When the user requests a question paper in `api_generate_paper`, read that text file and inject it directly into the AI's prompt as context (Retrieval-Augmented Generation / RAG).

*Current Status*: Phase 3 is partially there, but it writes to `finetune_dataset.jsonl` rather than queryable text blocks. 
