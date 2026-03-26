# 🤖 VedLinks - Smart AI Adaptive Tutor

**Empowering Education through Intelligent Question Generation & Personalized Learning**

VedLinks is a next-generation educational platform built on a specialized AI model fine-tuned for the NCERT curriculum. It transforms textbooks into interactive learning experiences, providing teachers with high-quality assessment tools and students with an adaptive tutor.

---

## 🌟 Key Features

### 🧠 Adaptive AI Fine-Tuning
- **Custom Model**: Fine-tuned **TinyLlama-1.1B-Chat** using QLoRA for optimized educational performance.
- **Massive Dataset**: Trained on **1,172+ curated samples** across 16 textbook chapters.
- **Context Awareness**: Generates questions that strictly follow textbook definitions and concepts.

### 📝 Smart Question Paper Generator
- **Multi-Format Support**: Create MCQs, Fill-in-blanks, Short Answers, and Long Answers.
- **Difficulty Control**: Balanced question distribution (Easy/Medium/Hard).
- **Professional Export**: Generate formatted **.docx** exam papers ready for printing.
- **Automated Marking**: Complete with answer keys and evaluation schemes.

### 🎯 AI-Powered Practice & Doubts
- **On-Demand Generation**: Click "Generate More" to get fresh AI questions using the fine-tuned model.
- **Source Badging**: Clear transparency with **🤖 AI Generated** and **📚 Knowledge Bank** badges.
- **Instant Feedback**: Real-time scoring and detailed explanations for every answer.
- **Concept Discovery**: searchable database of key textbook definitions.

### 📁 Textbook Upload & Processing
- **Smart Metadata**: Label PDFs by Class, Subject, and Chapter at the input stage.
- **Dynamic Text Extraction**: Automatically caches actual textbook content to power the Retrieval-Augmented Generation (RAG) fallback.
- **Fuzzy Matching**: Matches misspelled or differently cased chapters smoothly to the Knowledge Bank.

---

## 🚀 Quick Start

### 1. Install Dependencies
See `documents/requirements.md` for the full list of local backend dependencies including the PyTorch and HuggingFace stack.
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file based on `.env.example`:
```bash
MODEL_NAME="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MAX_SEQ_LENGTH=256
NUM_TRAIN_EPOCHS=5
```

### 3. Start the Server
```bash
python app.py
```
Access the dashboard at: **http://127.0.0.1:5000**

---

## 🛠️ AI Training Pipeline

VedLinks features a built-in pipeline to fine-tune the model on new textbook data.

```bash
# Level 1: Generate enhanced dataset from NCERT knowledge bank
python train_pipeline.py generate

# Level 2: Execute QLoRA fine-tuning
python train_pipeline.py train

# Level 3: Run full automated pipeline
python train_pipeline.py all
```

---

## 📁 Project Architecture

```
vedlinks/
├── app.py                      # Flask Server & AI API Endpoints
├── train_pipeline.py           # Dataset Generator & Training Orchestrator
├── question_paper_generator.py   # Core logic for structured generation
├── src/
│   ├── train_lora.py           # Deep Learning LoRA implementation
│   └── lesson_planner.py       # Educational planning logic
├── data/
│   ├── raw/                    # Uploaded NCERT PDFs
│   ├── topics/                 # Processed Chapter Metadata
│   └── finetune_dataset.jsonl  # The 1172+ sample training set
├── templates/
│   ├── index.html              # Exam Generator Dashboard
│   ├── practice.html           # AI Tutor / Practice Interface
│   └── upload.html             # Textbook Onboarding
└── output/
    └── qlora_tuned_model/      # Fine-tuned model adapters
```

---

## 🌐 Elite API Suite

| Endpoint | Action | Impact |
|----------|--------|--------|
| `/api/ai-generate-questions` | POST | Generates fresh, context-specific AI questions |
| `/api/practice-questions` | POST | Retrieves weighted mix of AI and bank questions |
| `/api/upload-textbook` | POST | Processes raw PDFs with full metadata labeling |
| `/api/generate-paper` | POST | Creates a full curriculum-aligned exam paper |
| `/api/ai-model-status` | GET | monitors the availability of the fine-tuned model |

---

## 🤝 Contributing

We are building the future of adaptive learning. Feel free to:
1.  Extend the knowledge bank for higher classes (11th & 12th).
2.  Enhance AI generation prompts in `app.py`.
3.  Add new question types like "Case-Based Questions".

---

**Built with ❤️ for VedLinks - The Future of NCERT Learning**