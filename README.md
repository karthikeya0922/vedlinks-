# VedLinks AI - NCERT Question Paper Generator

**AI-Powered Educational Content Generation Platform for NCERT Curriculum**

Generate question papers, practice quizzes, and lesson plans from NCERT textbook content using AI.

---

## 🚀 Quick Start

### Start the Server
```powershell
python run.py
```
Access at: **http://127.0.0.1:5000**

### Training Pipeline
```powershell
python train_pipeline.py generate   # Generate training dataset
python train_pipeline.py train      # Train with LoRA
python train_pipeline.py all        # Complete pipeline
```

---

## ✨ Features

### 📝 Question Paper Generator
- **Multiple question types**: MCQ, Fill-in-blanks, Short Answer, Long Answer
- **Customizable sections**: Add/remove sections with different question types
- **Difficulty distribution**: Easy/Medium/Hard percentage sliders
- **Export to Word**: Download as .docx file
- **Answer key & Marking scheme**: Auto-generated

### 🎯 Practice & Doubts (Student Mode)
- **Interactive quiz**: MCQs and fill-in-blanks with instant feedback
- **Score tracking**: Real-time progress and final score
- **Key concepts**: Browse definitions and explanations
- **Search**: Find concepts quickly

### 📚 Supported Content
- **Class 10 Science** - All 13 NCERT chapters
- **Class 6 Science** - Food chapters
- **Class 8 Science** - Coal and Petroleum

---

## 📁 Project Structure

```
vedlinks/
├── app.py                    # Flask web server
├── run.py                    # Server startup script
├── train_pipeline.py         # Training pipeline
├── question_paper_generator.py # Question generation with knowledge bank
├── data/
│   ├── raw/                  # NCERT PDF files (jesc1XX.pdf)
│   ├── topics/               # Topic JSON files
│   └── topic_registry.json   # Master topic metadata
├── templates/
│   ├── index.html            # Question paper generator UI
│   └── practice.html         # Student practice page
├── static/
│   ├── style.css             # Styles
│   └── script.js             # Frontend logic
├── src/
│   ├── train_lora.py         # QLoRA training
│   └── lesson_planner.py     # Lesson plan generation
└── output/
    └── qlora_tuned_model/    # Trained model output
```

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/topics` | GET | List all available topics |
| `/api/topic/<id>` | GET | Get topic details |
| `/api/generate-paper` | POST | Generate question paper |
| `/api/export-docx` | POST | Export paper to Word |
| `/api/practice-questions` | POST | Get practice questions |
| `/api/concepts` | POST | Get key concepts |
| `/api/generate-lesson-plan` | POST | Generate lesson plan |

---

## 📖 Knowledge Bank

The system includes a comprehensive knowledge bank with real NCERT content:

| Chapter | MCQs | Fill Blanks | Short Answers | Long Answers |
|---------|------|-------------|---------------|--------------|
| Chemical Reactions & Equations | 10 | 8 | 5 | 2 |
| Acids, Bases & Salts | 8 | 6 | 4 | 1 |
| Metals & Non-metals | 5 | 4 | 2 | - |
| Carbon & Compounds | 5 | 4 | 2 | - |
| Life Processes | 7 | 6 | 3 | 1 |
| Light, Reflection & Refraction | 8 | 5 | 3 | 1 |
| Electricity | 7 | 6 | 4 | 1 |
| + 6 more chapters | ... | ... | ... | ... |

**Total: 74+ MCQs, 63+ Fill-blanks, 35+ Short Answers**

---

## 🔧 Installation

### Requirements
- Python 3.11+
- pip

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### For GPU Training (Optional)
```powershell
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install transformers accelerate peft trl datasets
```

---

## 📄 Adding New Topics

1. Add PDF to `data/raw/`
2. Update `data/topic_registry.json`:
```json
{
  "new_file.pdf": {
    "class": "10",
    "subject": "Science",
    "chapter_number": 14,
    "chapter": "Chapter Name",
    "topics": ["Topic 1", "Topic 2"]
  }
}
```
3. Add knowledge bank entry in `question_paper_generator.py`

---

## 🛠️ Configuration

### Environment Variables (.env)
```bash
LOCAL_MODEL_NAME=TinyLlama/TinyLlama-1.1B-Chat-v1.0
TEMPERATURE=0.1
MAX_NEW_TOKENS=1024
LORA_R=8
LORA_ALPHA=16
NUM_TRAIN_EPOCHS=3
```

---

## 📝 Usage Examples

### Generate a Question Paper
1. Open http://127.0.0.1:5000
2. Select topics from the list
3. Add sections (MCQ, Short Answer, etc.)
4. Set difficulty distribution
5. Click "Generate Question Paper"
6. Download as Word document

### Practice Mode
1. Open http://127.0.0.1:5000/practice
2. Select a chapter
3. Answer MCQs and fill-in-blanks
4. Get instant feedback and final score

---

## 🤝 Contributing

1. Add more chapters to the knowledge bank
2. Improve question quality
3. Add new question types
4. Create better UI/UX

---

## 📄 License

MIT License - Free for educational use.

---

**Built with ❤️ for VedLinks - NCERT Adaptive AI Tutor**
