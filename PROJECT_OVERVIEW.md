# 🎯 VedLinks Project Overview

VedLinks is a specialized AI-powered educational platform designed to transform traditional textbooks into interactive, adaptive learning experiences. It leverages a fine-tuned LLM (Small Language Model) optimized for the NCERT curriculum to provide teachers with high-quality assessment tools and students with a personalized tutor.

---

## 📂 Detailed Project Structure

```text
vedlinks/
├── app.py                      # Flask Main Entry Point (API Suite & Training Orchestrator)
├── train_pipeline.py           # Dataset Generator & High-level Training Orchestrator
├── question_paper_generator.py   # Large-scale structured question paper logic
├── GPU_SETUP.md                # Specialized instructions for model training on Windows GPUs
├── src/                        # Core Logic Layer
│   ├── dataset_generator.py    # Logic for extracting knowledge from PDFs to datasets
│   ├── lesson_planner.py       # School-format lesson plan generation logic
│   ├── pdf_processor.py        # PDF text and metadata extraction
│   ├── train_lora.py           # Deep Learning LoRA/QLoRA training implementation
│   └── utils/                  # Helper utilities (text cleaning, file management)
├── data/                       # Storage Layer
│   ├── raw/                    # User-uploaded textbook PDFs
│   ├── topics/                 # Processed Chapter Knowledge (JSON)
│   ├── finetune_dataset.jsonl  # Generated training set for LLM fine-tuning
│   └── topic_registry.json     # Master index of all available chapters
├── templates/                  # Web Frontend (HTML)
└── static/                     # Web Assets (JS/CSS)
```

---

## 🚀 Key Features & Capabilities

### 1. Smart Question Generation
- **Automated Exams**: Generate full-length question papers (MCQs, Short/Long answers) in seconds.
- **Difficulty Mapping**: Control the balance of Easy, Medium, and Hard questions.
- **Professional Export**: Download papers as ready-to-print **.docx** files using `api_export_docx`.

### 2. Adaptive AI Practice
- **Contextual Learning**: The AI model (`TinyLlama-1.1B`) is trained strictly on NCERT content.
- **Source Badging**: Differentiates between **🤖 AI Generated** and **📚 Knowledge Bank** questions.
- **Concept Discovery**: Users can discover key concepts extracted via `api_concepts`.

### 3. Educator Tools
- **Lesson Planner**: Generates detailed, curriculum-aligned lesson plans via `api_generate_lesson_plan`.
- **Textbook Onboarding**: Instantly turn any PDF into a structured knowledge source.

---

## 🔄 Project Technical Flow

### Phase 1: Content Onboarding 📁
- **Input**: User uploads PDF via `/api/upload-textbook`.
- **Logic**: `src/pdf_processor.py` extracts text; metadata is saved to `data/topic_registry.json`.

### Phase 2: Knowledge Bank Creation ⚙️
- **Processing**: Content is converted to structured JSON in `data/topics/`.
- **Outcome**: A searchable, structured index that the AI uses for context.

### Phase 3: AI Training Pipeline 🧠
- **Dataset Generation**: `src/dataset_generator.py` (via `train_pipeline.py`) creates `data/finetune_dataset.jsonl`.
- **Fine-Tuning**: `src/train_lora.py` executes QLoRA training in a background thread triggered by `/api/start-finetuning`.
- **Monitoring**: Training logs and progress are exposed via `/api/training-status`.

### Phase 4: Application Layer 🌐
- **Inference**: `app.py` loads the fine-tuned model from `output/qlora_tuned_model/`.
- **Serving**: Content is delivered via Flask endpoints to the `templates` frontend.

---

## 🗺️ Roadmap & Future Tasks

### 1. 🌏 Multi-Language Support
- **Interface Localization**: Multi-language dashboard support.
- **Multilingual AI**: Fine-tuning for Marathi, Hindi, and other regional languages.

### 2. ⚡ Fine-Tuning & Model Tasking
- **Task-Specific Tuning**: Specialize the model for 11th-12th grade complex problem solving.
- **Automated Verification**: Implement a testing suite to validate model accuracy against textbook facts after every training cycle.

---

**VedLinks - Empowering the next generation of learners with Smart AI.**
