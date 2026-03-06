"""
Flask Web Server for VedLinks AI Educational Content Generator

NEW APPROACH:
- Uses structured topic JSON files instead of raw PDFs
- Supports lesson plan generation and question paper generation
- Topic metadata (class, subject, chapter, topics) drives all content
"""

import os
import sys
import json
import re
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
from datetime import datetime
from io import BytesIO
import threading
import subprocess
import time

# Fix encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Import our modules
from question_paper_generator import get_generator

app = Flask(__name__)
CORS(app)

# Configuration - NEW: Use topics directory instead of raw PDFs
DATA_TOPICS_PATH = Path("data/topics")
REGISTRY_PATH = Path("data/topic_registry.json")
FINETUNED_MODEL_PATH = Path("output/qlora_tuned_model")

# Global state for the fine-tuned AI model
_ai_model = None
_ai_tokenizer = None
_ai_model_loaded = False

# Global state for training orchestration
_training_status = {
    "is_training": False,
    "current_step": "idle",
    "progress": 0,
    "last_error": None,
    "start_time": None,
    "logs": []
}


def get_ai_model():
    """Lazy-load the fine-tuned LoRA model for AI question generation."""
    global _ai_model, _ai_tokenizer, _ai_model_loaded
    
    if _ai_model_loaded:
        return _ai_model, _ai_tokenizer
    
    if not FINETUNED_MODEL_PATH.exists() or not (FINETUNED_MODEL_PATH / "adapter_config.json").exists():
        print("No fine-tuned model found. AI generation will use knowledge bank only.")
        _ai_model_loaded = True
        return None, None
    
    try:
        import torch
        from peft import PeftModel, PeftConfig
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading fine-tuned AI model on {device}...")
        
        # Load the LoRA config to find the base model
        config = PeftConfig.from_pretrained(str(FINETUNED_MODEL_PATH))
        base_model_name = config.base_model_name_or_path
        
        # Load tokenizer
        _ai_tokenizer = AutoTokenizer.from_pretrained(str(FINETUNED_MODEL_PATH))
        if _ai_tokenizer.pad_token is None:
            _ai_tokenizer.pad_token = _ai_tokenizer.eos_token
        
        # Load base model
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if device == "cuda":
            base_model = AutoModelForCausalLM.from_pretrained(
                base_model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
            )
        else:
            base_model = AutoModelForCausalLM.from_pretrained(
                base_model_name,
                trust_remote_code=True,
            )
        
        # Load LoRA adapter
        _ai_model = PeftModel.from_pretrained(base_model, str(FINETUNED_MODEL_PATH))
        _ai_model.eval()
        
        _ai_model_loaded = True
        print(f"AI model loaded on {device}")
        return _ai_model, _ai_tokenizer
        
    except Exception as e:
        print(f"Failed to load AI model: {e}")
        _ai_model_loaded = True
        return None, None


def generate_ai_text(prompt_text, max_new_tokens=200):
    """Generate text using the fine-tuned model."""
    import torch
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
        # Extract only the response part (after ### Response:)
        if "### Response:" in generated:
            response = generated.split("### Response:")[-1].strip()
        else:
            response = generated[len(prompt_text):].strip()
        
        return response if response else None
    except Exception as e:
        print(f"AI generation error: {e}")
        return None


def load_topic_registry() -> dict:
    """Load the topic registry for fallback topic data."""
    if REGISTRY_PATH.exists():
        try:
            with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading registry: {e}")
    return {"files": {}}


def get_available_topics():
    """Get list of available topics from data/topics directory and registry.
    
    Topics can come from:
    1. Individual JSON files in data/topics/
    2. Topic registry (data/topic_registry.json) for entries without JSON files
    """
    topics = []
    seen_chapters = set()
    
    # 1. Load from individual topic JSON files (primary source)
    if DATA_TOPICS_PATH.exists():
        for file_path in DATA_TOPICS_PATH.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    topic_data = json.load(f)
                    
                chapter = topic_data.get('chapter', file_path.stem)
                seen_chapters.add(chapter)
                
                topics.append({
                    'id': file_path.name,
                    'name': chapter,
                    'class': topic_data.get('class', 'N/A'),
                    'subject': topic_data.get('subject', 'N/A'),
                    'chapter': chapter,
                    'topics': topic_data.get('topics', []),
                    'topic_count': len(topic_data.get('topics', [])),
                    'source': 'topic_file'
                })
            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")
    
    # 2. Load from registry for any entries not already covered
    registry = load_topic_registry()
    for file_id, entry in registry.get('files', {}).items():
        chapter = entry.get('chapter', '')
        
        # Skip if we already have this chapter from a topic file
        if chapter in seen_chapters:
            continue
        
        # Skip empty/unknown chapters
        if not chapter or chapter.startswith('Unknown'):
            continue
        
        topics.append({
            'id': file_id,
            'name': chapter,
            'class': entry.get('class', 'N/A'),
            'subject': entry.get('subject', 'N/A'),
            'chapter': chapter,
            'topics': entry.get('topics', []),
            'topic_count': len(entry.get('topics', [])),
            'source': 'registry'
        })
        seen_chapters.add(chapter)
    
    return sorted(topics, key=lambda x: (x['class'], x['subject'], x['name']))


def load_topic_data(topic_id: str) -> dict:
    """Load complete topic data from a JSON file or registry.
    
    First checks for individual topic file in data/topics/,
    then falls back to the topic registry.
    """
    # 1. Try loading from individual topic file
    file_path = DATA_TOPICS_PATH / topic_id
    
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {topic_id}: {e}")
    
    # 2. Try loading from registry
    registry = load_topic_registry()
    if topic_id in registry.get('files', {}):
        entry = registry['files'][topic_id]
        return {
            'class': entry.get('class', 'N/A'),
            'subject': entry.get('subject', 'N/A'),
            'chapter': entry.get('chapter', 'Unknown'),
            'chapter_number': entry.get('chapter_number', 0),
            'topics': entry.get('topics', [])
        }
    
    return {}


@app.route('/')
def index():
    """Serve the main question paper generator page."""
    return render_template('index.html')


@app.route('/practice')
def practice():
    """Serve the practice and doubts page for students."""
    return render_template('practice.html')


@app.route('/lesson-planner')
def lesson_planner():
    """Serve the lesson plan generator page."""
    return render_template('lesson_planner.html')


@app.route('/upload')
def upload_page():
    """Serve the textbook upload page."""
    return render_template('upload.html')


@app.route('/api/upload-textbook', methods=['POST'])
def api_upload_textbook():
    """Upload one or more textbook PDFs with manual metadata."""
    try:
        # Get the uploaded files (supports multiple)
        files = request.files.getlist('files')
        
        # Fallback: also check for single 'file' key (backward compatibility)
        if not files:
            if 'file' in request.files:
                files = [request.files['file']]
            else:
                return jsonify({'success': False, 'error': 'No files uploaded'}), 400
        
        # Filter out empty filenames
        files = [f for f in files if f.filename and f.filename != '']
        if not files:
            return jsonify({'success': False, 'error': 'No files selected'}), 400
        
        # Validate all files are PDFs
        for f in files:
            if not f.filename.lower().endswith('.pdf'):
                return jsonify({'success': False, 'error': f'Only PDF files are allowed. "{f.filename}" is not a PDF.'}), 400
        
        # Get manual metadata from form
        class_num = request.form.get('class', '').strip()
        subject = request.form.get('subject', '').strip()
        chapter_number = request.form.get('chapter_number', '').strip()
        chapter_name = request.form.get('chapter_name', '').strip()
        topics_raw = request.form.get('topics', '').strip()
        
        # Validate required fields
        if not class_num:
            return jsonify({'success': False, 'error': 'Class is required'}), 400
        if not subject:
            return jsonify({'success': False, 'error': 'Subject is required'}), 400
        if not chapter_number:
            return jsonify({'success': False, 'error': 'Chapter number is required'}), 400
        if not chapter_name:
            return jsonify({'success': False, 'error': 'Chapter name is required'}), 400
        
        chapter_number = int(chapter_number)
        
        # Parse topics (comma-separated)
        topics = [t.strip() for t in topics_raw.split(',') if t.strip()] if topics_raw else []
        
        # Save each PDF and create topic entries
        raw_dir = Path('data/raw')
        raw_dir.mkdir(parents=True, exist_ok=True)
        topics_dir = Path('data/topics')
        topics_dir.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        registry = load_topic_registry()
        
        for file in files:
            safe_name = secure_filename(file.filename)
            pdf_path = raw_dir / safe_name
            file.save(str(pdf_path))
            saved_files.append(safe_name)
        
        # Create topic JSON filename
        subject_slug = re.sub(r'[^a-z0-9]', '_', subject.lower()).strip('_')
        topic_filename = f"class_{class_num}_{subject_slug}_ch{chapter_number}.json"
        
        # Create topic data
        topic_data = {
            'class': str(class_num),
            'subject': subject,
            'chapter': chapter_name,
            'chapter_number': chapter_number,
            'topics': topics,
            'source_pdfs': saved_files
        }
        
        # Save to data/topics/
        topic_path = topics_dir / topic_filename
        
        with open(topic_path, 'w', encoding='utf-8') as f:
            json.dump(topic_data, f, indent=2, ensure_ascii=False)
        
        # Update registry
        registry['files'][topic_filename] = {
            'class': str(class_num),
            'subject': subject,
            'chapter_number': chapter_number,
            'chapter': chapter_name,
            'topics': topics,
            'has_knowledge_bank': False,
            'source_pdfs': saved_files
        }
        
        with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        
        file_count = len(saved_files)
        return jsonify({
            'success': True,
            'message': f'Uploaded {file_count} file{"s" if file_count > 1 else ""} successfully! Class {class_num} {subject} - Ch {chapter_number}: {chapter_name}',
            'topic_file': topic_filename,
            'pdf_files': saved_files
        })
        
    except ValueError:
        return jsonify({'success': False, 'error': 'Chapter number must be a valid number'}), 400
    except Exception as e:
        print(f'Error uploading textbook: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/topics', methods=['GET'])
def api_get_topics():
    """Get list of available topics."""
    topics = get_available_topics()
    return jsonify({
        'success': True,
        'topics': topics,
        'count': len(topics)
    })


@app.route('/api/topics-grouped', methods=['GET'])
def api_get_topics_grouped():
    """Get topics grouped hierarchically: Class -> Subject -> Chapters."""
    topics = get_available_topics()
    
    grouped = {}
    for t in topics:
        cls = t.get('class', 'N/A')
        subject = t.get('subject', 'N/A')
        
        if cls not in grouped:
            grouped[cls] = {}
        if subject not in grouped[cls]:
            grouped[cls][subject] = []
        
        grouped[cls][subject].append({
            'id': t['id'],
            'chapter': t.get('chapter', t.get('name', '')),
            'chapter_number': t.get('chapter_number', 0),
            'topic_count': t.get('topic_count', 0),
            'topics': t.get('topics', []),
            'source': t.get('source', 'unknown')
        })
    
    # Sort chapters by chapter_number within each subject
    for cls in grouped:
        for subject in grouped[cls]:
            grouped[cls][subject].sort(key=lambda x: x.get('chapter_number', 0))
    
    # Sort classes numerically
    sorted_grouped = {}
    for cls in sorted(grouped.keys(), key=lambda x: int(x) if x.isdigit() else 999):
        sorted_grouped[cls] = grouped[cls]
    
    return jsonify({
        'success': True,
        'grouped': sorted_grouped
    })


@app.route('/api/topic/<topic_id>', methods=['GET'])
def api_get_topic_details(topic_id):
    """Get detailed information about a specific topic."""
    topic_data = load_topic_data(topic_id)
    
    if not topic_data:
        return jsonify({
            'success': False,
            'error': f'Topic not found: {topic_id}'
        }), 404
    
    return jsonify({
        'success': True,
        'topic': topic_data
    })


@app.route('/api/practice-questions', methods=['POST'])
def api_practice_questions():
    """Get practice questions for a topic, mixing knowledge bank and AI-generated."""
    import random
    from question_paper_generator import NCERT_KNOWLEDGE
    
    data = request.get_json()
    topic_id = data.get('topicId', '')
    
    # Load topic data
    topic_data = load_topic_data(topic_id)
    if not topic_data:
        return jsonify({'success': False, 'error': 'Topic not found'}), 404
    
    chapter = topic_data.get('chapter', '')
    
    # Get questions from knowledge bank
    questions = []
    knowledge = NCERT_KNOWLEDGE.get(chapter, {})
    
    # Add MCQs
    for q, opts, ans, exp in knowledge.get('mcq_pool', []):
        questions.append({
            'type': 'mcq',
            'question': q,
            'options': opts,
            'answer': ans,
            'explanation': exp,
            'source': 'knowledge_bank'
        })
    
    # Add fill in blanks
    for q, ans in knowledge.get('fill_blanks', []):
        questions.append({
            'type': 'fill_blank',
            'question': q.replace('_______', '________'),
            'answer': ans,
            'source': 'knowledge_bank'
        })
    
    # Add short answer questions
    for q, ans in knowledge.get('short_answers', []):
        questions.append({
            'type': 'short_answer',
            'question': q,
            'answer': ans,
            'source': 'knowledge_bank'
        })
    
    # Check if AI model is available
    has_ai = FINETUNED_MODEL_PATH.exists() and (FINETUNED_MODEL_PATH / "adapter_config.json").exists()
    
    # Shuffle and limit
    random.shuffle(questions)
    questions = questions[:15]  # Max 15 questions per session
    
    return jsonify({
        'success': True,
        'questions': questions,
        'count': len(questions),
        'ai_available': has_ai,
        'chapter': chapter
    })


@app.route('/api/concepts', methods=['POST'])
def api_concepts():
    """Get key concepts for a topic."""
    from question_paper_generator import NCERT_KNOWLEDGE
    
    data = request.get_json()
    topic_id = data.get('topicId', '')
    
    # Load topic data
    topic_data = load_topic_data(topic_id)
    if not topic_data:
        return jsonify({'success': False, 'error': 'Topic not found'}), 404
    
    chapter = topic_data.get('chapter', '')
    
    # Get concepts from knowledge bank
    concepts = []
    knowledge = NCERT_KNOWLEDGE.get(chapter, {})
    
    # Add key concepts
    for term, definition in knowledge.get('key_concepts', []):
        concepts.append({
            'term': term,
            'definition': definition,
            'source': 'knowledge_bank'
        })
    
    # Also add short answers as additional Q&A concepts
    for q, ans in knowledge.get('short_answers', []):
        concepts.append({
            'term': q,
            'definition': ans,
            'source': 'knowledge_bank'
        })
    
    # Add from topics list if still empty
    if not concepts and topic_data.get('topics'):
        for topic in topic_data['topics']:
            concepts.append({
                'term': topic,
                'definition': f'Key topic in {chapter}. Review your textbook for detailed explanation.',
                'source': 'topic_list'
            })
    
    return jsonify({
        'success': True,
        'concepts': concepts,
        'count': len(concepts)
    })


@app.route('/api/generate-paper', methods=['POST'])
def api_generate_paper():
    """Generate a complete question paper."""
    try:
        config = request.get_json()
        
        if not config:
            return jsonify({
                'success': False,
                'error': 'No configuration provided'
            }), 400
        
        # Validate required fields
        if 'sections' not in config or not config['sections']:
            return jsonify({
                'success': False,
                'error': 'At least one section is required'
            }), 400
        
        if 'selectedTopics' not in config or not config['selectedTopics']:
            return jsonify({
                'success': False,
                'error': 'At least one topic must be selected'
            }), 400
        
        # Load topic data (NEW: Uses structured topic data)
        topic_contents = {}
        topic_metadata = []
        
        for topic_id in config['selectedTopics']:
            topic_data = load_topic_data(topic_id)
            if topic_data:
                # Create content from topic metadata for the generator
                content = f"Class: {topic_data.get('class', '')}\n"
                content += f"Subject: {topic_data.get('subject', '')}\n"
                content += f"Chapter: {topic_data.get('chapter', '')}\n"
                content += f"Topics: {', '.join(topic_data.get('topics', []))}"
                
                topic_contents[topic_id] = content
                topic_metadata.append(topic_data)
        
        if not topic_contents:
            return jsonify({
                'success': False,
                'error': 'Could not load any topic data'
            }), 400
        
        # Get generator and generate paper
        generator = get_generator()
        paper = generator.generate_paper(config, topic_contents)
        
        # Add metadata about topics used
        paper['topicMetadata'] = topic_metadata
        
        return jsonify({
            'success': True,
            'paper': paper
        })
        
    except Exception as e:
        print(f"Error generating paper: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate-lesson-plan', methods=['POST'])
def api_generate_lesson_plan():
    """Generate a detailed school-format lesson plan."""
    try:
        from question_paper_generator import NCERT_KNOWLEDGE
        
        config = request.get_json()
        
        if not config:
            return jsonify({
                'success': False,
                'error': 'No configuration provided'
            }), 400
        
        # Get chapter info
        chapter_id = config.get('chapterId')
        chapter_name = config.get('chapterName', 'Chapter')
        
        # Load topic data
        topic_data = load_topic_data(chapter_id) if chapter_id else {}
        
        # Get knowledge from NCERT bank
        knowledge = NCERT_KNOWLEDGE.get(chapter_name, {})
        key_concepts = knowledge.get('key_concepts', [])
        
        # Calculate timing based on periods
        periods = int(config.get('periodsCount', 1))
        duration = int(config.get('periodDuration', 40))
        total_time = periods * duration
        
        # Distribute time: 15% opening, 70% main, 15% closure
        opening_time = max(5, int(total_time * 0.15))
        main_time = int(total_time * 0.70)
        closure_time = max(5, int(total_time * 0.15))
        
        # Build prerequisite knowledge from key concepts
        prereq = []
        if key_concepts:
            for i, (term, defn) in enumerate(key_concepts[:4]):
                prereq.append(f"{term}: {defn[:80]}..." if len(defn) > 80 else f"{term}: {defn}")
        else:
            prereq = [
                "Basic understanding of the subject",
                "Previous chapter concepts",
                "Fundamental terminology"
            ]
        
        # Build teaching phases
        phases = [
            {
                "name": "Opening / Activating Prior Knowledge",
                "duration": f"{opening_time} min",
                "learningOutcome": f"Students will recall previous knowledge related to {config.get('topic', chapter_name)}",
                "methodology": ["Lecture", "Discussion", "Q&A", "Brainstorming"],
                "teachingAids": ["Blackboard", "Previous notes"],
                "teacherActivities": [
                    "Recap previous lesson",
                    "Ask probing questions to assess prior knowledge",
                    "Introduce today's topic with real-life example"
                ],
                "learnerActivities": [
                    "Answer pre-requisite questions",
                    "Share previous knowledge",
                    "Listen to introduction"
                ],
                "assessment": "Oral questioning to check prerequisite knowledge",
                "homeAssignment": ""
            },
            {
                "name": "Teaching & Conducting Activities",
                "duration": f"{main_time} min",
                "learningOutcome": f"Students will understand and apply concepts of {config.get('topic', chapter_name)}",
                "methodology": [
                    "Active Collaborative Learning",
                    "Inquiry-Based Learning",
                    "Experiential Learning",
                    "Concept Mapping"
                ],
                "teachingAids": ["PPT", "Videos", "Charts", "Models", "Diagrams"],
                "teacherActivities": [
                    "Explain key concepts with examples",
                    "Show PPT/Video demonstration",
                    "Conduct hands-on activity",
                    "Facilitate group discussion",
                    "Address misconceptions"
                ],
                "learnerActivities": [
                    "Take notes and draw diagrams",
                    "Observe demonstrations",
                    "Participate in activities",
                    "Ask questions and clarify doubts",
                    "Work in groups on assigned tasks"
                ],
                "assessment": "Formative assessment through observation and questioning",
                "homeAssignment": ""
            },
            {
                "name": "Closure, Feedback & Doubt Clarification",
                "duration": f"{closure_time} min",
                "learningOutcome": "Students will consolidate learning and clarify any remaining doubts",
                "methodology": ["Summarization", "Peer Teaching", "Reflection"],
                "teachingAids": ["Worksheet", "Blackboard"],
                "teacherActivities": [
                    "Summarize key points",
                    "Conduct quick assessment",
                    "Address remaining doubts",
                    "Assign homework"
                ],
                "learnerActivities": [
                    "Participate in recap discussion",
                    "Complete quick assessment",
                    "Ask clarifying questions",
                    "Note down homework"
                ],
                "assessment": "Quick quiz or exit ticket",
                "homeAssignment": f"Read textbook pages on {config.get('topic', chapter_name)}. Complete worksheet questions 1-5."
            }
        ]
        
        # Build values based on chapter
        values_map = {
            "Chemical Reactions": "Scientific inquiry, Environmental awareness, Safety consciousness",
            "Acids": "Curiosity, Analytical thinking, Application of knowledge",
            "Metals": "Resource conservation, Sustainable development, Scientific temperament",
            "Carbon": "Environmental responsibility, Organic awareness, Practical application",
            "Life Processes": "Respect for life, Health consciousness, Scientific observation",
            "Control": "Self-discipline, Mind-body awareness, Coordination",
            "Reproduction": "Respect for life, Responsibility, Scientific understanding",
            "Heredity": "Appreciation of diversity, Scientific reasoning, Family values",
            "Light": "Scientific curiosity, Observation skills, Optical awareness",
            "Human Eye": "Health awareness, Vision care, Scientific appreciation",
            "Electricity": "Energy conservation, Safety awareness, Practical application",
            "Magnetic": "Scientific inquiry, Technological appreciation, Practical skills",
            "Environment": "Environmental stewardship, Conservation, Sustainable living"
        }
        
        # Find matching value
        values = "Scientific inquiry, Critical thinking, Curiosity"
        for key, val in values_map.items():
            if key.lower() in chapter_name.lower():
                values = val
                break
        
        # Build real-life applications
        applications_map = {
            "Chemical Reactions": "Cooking, rusting prevention, fire extinguishers, photography",
            "Acids": "Antacids for digestion, cleaning agents, food preservation, batteries",
            "Metals": "Construction, jewelry, electrical wiring, utensils, coins",
            "Carbon": "Fuels, plastics, medicines, soaps, cosmetics",
            "Life Processes": "Nutrition, breathing exercises, blood donation awareness",
            "Control": "Stress management, reflex actions, hormonal health",
            "Reproduction": "Agriculture, animal husbandry, family planning awareness",
            "Heredity": "Genetic counseling, crop improvement, disease prediction",
            "Light": "Photography, fiber optics, rainbows, mirrors",
            "Human Eye": "Spectacles, cameras, telescopes, corrective surgery",
            "Electricity": "Home appliances, lighting, electronic devices, power generation",
            "Magnetic": "Motors, generators, MRI scans, magnetic storage",
            "Environment": "Waste management, conservation, sustainable practices"
        }
        
        real_life = "Everyday science applications and practical demonstrations"
        for key, val in applications_map.items():
            if key.lower() in chapter_name.lower():
                real_life = val
                break
        
        # Build cross-curricular connections
        cross_curricular = "Mathematics (calculations), Geography (resources), History (scientific discoveries)"
        
        # Build lesson plan response
        lesson_plan = {
            "teacherName": config.get('teacherName', 'Teacher'),
            "schoolName": config.get('schoolName', 'School Name'),
            "designation": config.get('designation', ''),
            "grade": config.get('grade', '10'),
            "subject": config.get('subject', 'Science'),
            "chapterName": chapter_name,
            "topic": config.get('topic', chapter_name),
            "date": config.get('date', ''),
            "planNumber": config.get('planNumber', '1'),
            "periodsCount": periods,
            "periodDuration": duration,
            "totalDuration": total_time,
            "prerequisiteKnowledge": prereq,
            "phases": phases,
            "values": values,
            "realLifeApplication": real_life,
            "crossCurricular": cross_curricular,
            "extendedTask": f"Research project: Explore real-world applications of {config.get('topic', chapter_name)} and prepare a short presentation."
        }
        
        return jsonify({
            'success': True,
            'lessonPlan': lesson_plan
        })
        
    except Exception as e:
        print(f"Error generating lesson plan: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/model-status', methods=['GET'])
def api_model_status():
    """Check if model is loaded."""
    generator = get_generator()
    return jsonify({
        'success': True,
        'loaded': generator.is_loaded,
        'device': generator.device or 'not loaded',
        'mode': 'template' if generator.use_template_mode else 'model'
    })


@app.route('/api/load-model', methods=['POST'])
def api_load_model():
    """Preload the model."""
    try:
        generator = get_generator()
        success = generator.load_model()
        return jsonify({
            'success': success,
            'device': generator.device,
            'mode': 'template' if generator.use_template_mode else 'model'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai-generate-questions', methods=['POST'])
def api_ai_generate_questions():
    """Generate fresh practice questions using the fine-tuned AI model."""
    import random
    from question_paper_generator import NCERT_KNOWLEDGE
    
    data = request.get_json()
    chapter = data.get('chapter', '')
    question_type = data.get('type', 'mcq')  # mcq, short_answer, concept
    count = min(int(data.get('count', 3)), 5)  # Max 5 at a time
    
    if not chapter:
        return jsonify({'success': False, 'error': 'Chapter name is required'}), 400
    
    results = []
    
    # Try AI model first
    model, tokenizer = get_ai_model()
    if model is not None:
        for i in range(count):
            if question_type == 'mcq':
                prompt = f"### Instruction:\nGenerate an MCQ question about '{chapter}'.\n\n### Input:\n\n### Response:"
            elif question_type == 'short_answer':
                prompt = f"### Instruction:\nGenerate a short answer question about '{chapter}'.\n\n### Input:\n\n### Response:"
            else:  # concept
                prompt = f"### Instruction:\nExplain a key concept from the chapter '{chapter}'.\n\n### Input:\n\n### Response:"
            
            response = generate_ai_text(prompt, max_new_tokens=200)
            if response:
                if question_type == 'mcq' and 'Question:' in response:
                    # Parse MCQ format
                    try:
                        lines = response.strip().split('\n')
                        q_text = ''
                        options = []
                        answer = ''
                        explanation = ''
                        for line in lines:
                            line = line.strip()
                            if line.startswith('Question:'):
                                q_text = line.replace('Question:', '').strip()
                            elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                                options.append(line[2:].strip())
                            elif line.startswith('Answer:'):
                                answer = line.replace('Answer:', '').strip()
                            elif line.startswith('Explanation:'):
                                explanation = line.replace('Explanation:', '').strip()
                        
                        if q_text and len(options) >= 4 and answer:
                            results.append({
                                'type': 'mcq',
                                'question': q_text,
                                'options': options[:4],
                                'answer': answer,
                                'explanation': explanation,
                                'source': 'ai_generated'
                            })
                    except:
                        pass
                elif question_type == 'short_answer' and 'Question:' in response:
                    try:
                        parts = response.split('Answer:')
                        q_text = parts[0].replace('Question:', '').strip()
                        ans_text = parts[1].strip() if len(parts) > 1 else ''
                        if q_text and ans_text:
                            results.append({
                                'type': 'short_answer',
                                'question': q_text,
                                'answer': ans_text,
                                'source': 'ai_generated'
                            })
                    except:
                        pass
                else:
                    results.append({
                        'type': 'concept',
                        'question': f'AI explanation about {chapter}',
                        'answer': response,
                        'source': 'ai_generated'
                    })
    
    # If AI didn't produce enough, supplement from knowledge bank
    knowledge = NCERT_KNOWLEDGE.get(chapter, {})
    if len(results) < count and knowledge:
        if question_type == 'mcq':
            pool = list(knowledge.get('mcq_pool', []))
            random.shuffle(pool)
            for q, opts, ans, exp in pool[:count - len(results)]:
                results.append({
                    'type': 'mcq',
                    'question': q,
                    'options': opts,
                    'answer': ans,
                    'explanation': exp,
                    'source': 'knowledge_bank'
                })
        elif question_type == 'short_answer':
            pool = list(knowledge.get('short_answers', []))
            random.shuffle(pool)
            for q, ans in pool[:count - len(results)]:
                results.append({
                    'type': 'short_answer',
                    'question': q,
                    'answer': ans,
                    'source': 'knowledge_bank'
                })
        else:
            pool = list(knowledge.get('key_concepts', []))
            random.shuffle(pool)
            for term, defn in pool[:count - len(results)]:
                results.append({
                    'type': 'concept',
                    'question': f'Explain: {term}',
                    'answer': defn,
                    'source': 'knowledge_bank'
                })
    
    return jsonify({
        'success': True,
        'questions': results,
        'count': len(results),
        'ai_used': model is not None
    })


@app.route('/api/ai-model-status', methods=['GET'])
def api_ai_model_status():
    """Check if the fine-tuned AI model is available."""
    model_exists = FINETUNED_MODEL_PATH.exists() and (FINETUNED_MODEL_PATH / "adapter_config.json").exists()
    return jsonify({
        'success': True,
        'model_available': model_exists,
        'model_loaded': _ai_model is not None,
        'model_path': str(FINETUNED_MODEL_PATH)
    })


@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'topics_available': len(get_available_topics())
    })


@app.route('/api/export-docx', methods=['POST'])
def api_export_docx():
    """Export question paper as Word document."""
    try:
        from docx import Document
        from docx.shared import Inches, Pt
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.style import WD_STYLE_TYPE
        
        data = request.get_json()
        if not data or 'paper' not in data:
            return jsonify({'success': False, 'error': 'No paper data provided'}), 400
        
        paper = data['paper']
        
        # Create Word document
        doc = Document()
        
        # Set up styles
        style = doc.styles['Normal']
        style.font.name = 'Times New Roman'
        style.font.size = Pt(12)
        
        # Add header
        header = doc.add_paragraph()
        header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = header.add_run(paper.get('schoolName', 'School Name'))
        run.bold = True
        run.font.size = Pt(16)
        
        # Add exam title
        title = doc.add_paragraph()
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = title.add_run(paper.get('examTitle', 'Question Paper'))
        run.bold = True
        run.font.size = Pt(14)
        
        # Add metadata
        meta = doc.add_paragraph()
        meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
        meta.add_run(f"Class: {paper.get('class', 'X')} | Subject: {paper.get('subject', 'Science')} | ")
        meta.add_run(f"Max Marks: {paper.get('totalMarks', 80)} | Time: {paper.get('duration', '3 hours')}")
        
        doc.add_paragraph()  # Spacing
        
        # Add instructions
        instructions = doc.add_paragraph()
        instructions.add_run('General Instructions:').bold = True
        doc.add_paragraph('1. All questions are compulsory.')
        doc.add_paragraph('2. Write neat and legible answers.')
        doc.add_paragraph('3. Marks are indicated against each question.')
        
        doc.add_paragraph()  # Spacing
        
        # Add sections
        for section in paper.get('sections', []):
            # Section header
            sec_header = doc.add_paragraph()
            sec_header.add_run(f"Section {section.get('name', 'A')}: {section.get('title', '')}").bold = True
            
            # Questions in section
            for q in section.get('questions', []):
                q_para = doc.add_paragraph()
                q_num = q.get('number', '')
                q_text = q.get('question', q.get('text', ''))
                marks = q.get('marks', 1)
                
                q_para.add_run(f"Q{q_num}. ").bold = True
                q_para.add_run(f"{q_text} ")
                q_para.add_run(f"[{marks} mark{'s' if marks > 1 else ''}]")
                
                # Add options for MCQ
                if 'options' in q:
                    for i, opt in enumerate(q['options']):
                        doc.add_paragraph(f"    {opt}")
            
            doc.add_paragraph()  # Spacing between sections
        
        # Save to BytesIO
        file_stream = BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        
        filename = f"question_paper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        
        return send_file(
            file_stream,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=filename
        )
        
    except ImportError:
        return jsonify({'success': False, 'error': 'python-docx not installed. Run: pip install python-docx'}), 500
    except Exception as e:
        print(f"Error exporting to Word: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/export-lesson-plan-docx', methods=['POST'])
def api_export_lesson_plan_docx():
    """Export lesson plan as Word document in school format."""
    try:
        from docx import Document
        from docx.shared import Inches, Pt, Cm
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.table import WD_TABLE_ALIGNMENT
        from docx.oxml.ns import nsdecls
        from docx.oxml import parse_xml
        
        data = request.get_json()
        if not data or 'lessonPlan' not in data:
            return jsonify({'success': False, 'error': 'No lesson plan data provided'}), 400
        
        plan = data['lessonPlan']
        
        # Create Word document
        doc = Document()
        
        # Set up styles
        style = doc.styles['Normal']
        style.font.name = 'Arial'
        style.font.size = Pt(11)
        
        # Set margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Cm(1.5)
            section.bottom_margin = Cm(1.5)
            section.left_margin = Cm(1.5)
            section.right_margin = Cm(1.5)
        
        # ===== HEADER =====
        header = doc.add_paragraph()
        header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = header.add_run(plan.get('schoolName', 'School Name'))
        run.bold = True
        run.font.size = Pt(16)
        
        subtitle = doc.add_paragraph()
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = subtitle.add_run('LESSON PLAN')
        run.bold = True
        run.font.size = Pt(14)
        
        # ===== INFO TABLE =====
        info_table = doc.add_table(rows=4, cols=4)
        info_table.style = 'Table Grid'
        
        # Row 1
        info_table.cell(0, 0).text = 'Teacher:'
        info_table.cell(0, 1).text = plan.get('teacherName', '')
        info_table.cell(0, 2).text = 'Date:'
        info_table.cell(0, 3).text = plan.get('date', '')
        
        # Row 2
        info_table.cell(1, 0).text = 'Subject:'
        info_table.cell(1, 1).text = plan.get('subject', '')
        info_table.cell(1, 2).text = 'Grade:'
        info_table.cell(1, 3).text = f"Class {plan.get('grade', '')}"
        
        # Row 3
        info_table.cell(2, 0).text = 'Chapter:'
        info_table.cell(2, 1).text = plan.get('chapterName', '')
        info_table.cell(2, 2).text = 'Periods:'
        info_table.cell(2, 3).text = f"{plan.get('periodsCount', 1)} ({plan.get('periodDuration', 40)} min each)"
        
        # Row 4
        info_table.cell(3, 0).text = 'Topic:'
        info_table.cell(3, 1).merge(info_table.cell(3, 3))
        info_table.cell(3, 1).text = plan.get('topic', '')
        
        # Bold the labels
        for row in info_table.rows:
            for i in [0, 2]:
                if i < len(row.cells):
                    for para in row.cells[i].paragraphs:
                        for run in para.runs:
                            run.bold = True
        
        doc.add_paragraph()  # Spacing
        
        # ===== PRE-REQUISITE KNOWLEDGE =====
        prereq_header = doc.add_paragraph()
        run = prereq_header.add_run('PRE-REQUISITE KNOWLEDGE:')
        run.bold = True
        run.font.size = Pt(11)
        
        for item in plan.get('prerequisiteKnowledge', []):
            doc.add_paragraph(f"• {item}", style='List Bullet')
        
        doc.add_paragraph()  # Spacing
        
        # ===== MAIN LESSON PLAN TABLE =====
        main_header = doc.add_paragraph()
        run = main_header.add_run('LESSON PLAN DETAILS:')
        run.bold = True
        run.font.size = Pt(11)
        
        # Create table with 8 columns
        phases = plan.get('phases', [])
        table = doc.add_table(rows=len(phases) + 1, cols=8)
        table.style = 'Table Grid'
        
        # Header row
        headers = ['Duration', 'Learning Outcome', 'Methodology', 'Teaching Aids', 
                   'Teacher Activities', 'Learner Activities', 'Assessment', 'Home Assignment']
        for i, header_text in enumerate(headers):
            cell = table.cell(0, i)
            cell.text = header_text
            # Make header bold
            for para in cell.paragraphs:
                for run in para.runs:
                    run.bold = True
                    run.font.size = Pt(9)
        
        # Data rows
        for row_idx, phase in enumerate(phases, 1):
            table.cell(row_idx, 0).text = f"{phase.get('name', '')}\n({phase.get('duration', '')})"
            table.cell(row_idx, 1).text = phase.get('learningOutcome', '')
            table.cell(row_idx, 2).text = ', '.join(phase.get('methodology', []))
            table.cell(row_idx, 3).text = ', '.join(phase.get('teachingAids', []))
            table.cell(row_idx, 4).text = '\n'.join([f"• {a}" for a in phase.get('teacherActivities', [])])
            table.cell(row_idx, 5).text = '\n'.join([f"• {a}" for a in phase.get('learnerActivities', [])])
            table.cell(row_idx, 6).text = phase.get('assessment', '')
            table.cell(row_idx, 7).text = phase.get('homeAssignment', '-')
        
        # Set font size for all cells
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    para.paragraph_format.space_after = Pt(2)
                    for run in para.runs:
                        run.font.size = Pt(8)
        
        doc.add_paragraph()  # Spacing
        
        # ===== FOOTER SECTIONS =====
        # Values
        values_para = doc.add_paragraph()
        run = values_para.add_run('VALUES DEALT IN THE LESSON (VD): ')
        run.bold = True
        values_para.add_run(plan.get('values', ''))
        
        # Real Life Application
        rl_para = doc.add_paragraph()
        run = rl_para.add_run('REAL LIFE APPLICATION (RL): ')
        run.bold = True
        rl_para.add_run(plan.get('realLifeApplication', ''))
        
        # Cross Curricular
        cc_para = doc.add_paragraph()
        run = cc_para.add_run('CROSS CURRICULAR CONNECTION (CC): ')
        run.bold = True
        cc_para.add_run(plan.get('crossCurricular', ''))
        
        # Extended Task
        if plan.get('extendedTask'):
            ext_para = doc.add_paragraph()
            run = ext_para.add_run('EXTENDED TASK: ')
            run.bold = True
            ext_para.add_run(plan.get('extendedTask', ''))
        
        doc.add_paragraph()  # Spacing
        doc.add_paragraph()  # More spacing
        
        # ===== SIGNATURES =====
        sig_table = doc.add_table(rows=2, cols=3)
        sig_table.cell(0, 0).text = ''
        sig_table.cell(0, 1).text = ''
        sig_table.cell(0, 2).text = ''
        
        sig_table.cell(1, 0).text = '________________________\nSignature of Subject Teacher'
        sig_table.cell(1, 1).text = '________________________\nSignature of HOD'
        sig_table.cell(1, 2).text = '________________________\nSignature of Principal'
        
        for cell in sig_table.rows[1].cells:
            for para in cell.paragraphs:
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Save to BytesIO
        file_stream = BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        
        # Generate filename
        chapter_safe = ''.join(c if c.isalnum() else '_' for c in plan.get('chapterName', 'lesson'))
        filename = f"lesson_plan_{chapter_safe}_{datetime.now().strftime('%Y%m%d')}.docx"
        
        return send_file(
            file_stream,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=filename
        )
        
    except ImportError:
        return jsonify({'success': False, 'error': 'python-docx not installed. Run: pip install python-docx'}), 500
    except Exception as e:
        print(f"Error exporting lesson plan to Word: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/start-finetuning', methods=['POST'])
def api_start_finetuning():
    """Trigger the fine-tuning process in the background."""
    global _training_status
    
    if _training_status["is_training"]:
        return jsonify({"success": False, "error": "Training is already in progress."})
        
    def run_training():
        global _training_status, _ai_model_loaded
        _training_status.update({
            "is_training": True,
            "current_step": "generating_data",
            "progress": 10,
            "last_error": None,
            "start_time": datetime.now().isoformat(),
            "logs": ["Starting data generation..."]
        })
        
        try:
            # 1. Generate new training data (includes dynamic uploads)
            from train_pipeline import generate_training_data
            generate_training_data()
            _training_status["logs"].append("Data generation complete.")
            _training_status["current_step"] = "training_model"
            _training_status["progress"] = 30
            
            # 2. Run training via subprocess to avoid blocking/memory issues
            process = subprocess.Popen(
                [sys.executable, "train_pipeline.py", "train"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',  # Explicitly use utf-8 for Windows compatibility
                errors='replace',  # Replace undecodable characters instead of crashing
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            _training_status["logs"].append("Model training started...")
            
            # Use safe iterator for stdout to catch potential pipe errors
            try:
                for line in iter(process.stdout.readline, ""):
                    line = line.strip()
                    if line:
                        _training_status["logs"].append(line)
                        
                        # Special parsing for our custom ProgressPrinterCallback
                        if "PROGRESS_UPDATE" in line:
                            # Format: PROGRESS_UPDATE | Epoch: 1.23 | Step: 100 | Loss: 0.85
                            try:
                                # Echo to terminal as per user request
                                print(f"[FINE-TUNE] {line}")
                                
                                # Estimate progress (approx 2000 steps for 5 epochs)
                                parts = line.split('|')
                                step_str = [p for p in parts if "Step:" in p][0]
                                current_step = int(step_str.split(':')[1].strip())
                                # Total steps estimation: 5 epochs * (1600 samples / 4 grad_acc) = 2000
                                _training_status["progress"] = min(99, (current_step / 2000) * 100)
                            except:
                                pass
                        else:
                            # Standard output echo
                            print(f"[TRAINING] {line}")
                            
                            # Fallback progress estimation
                            if "%" in line:
                                _training_status["progress"] = min(95, _training_status["progress"] + 0.1)
            except Exception as pipe_err:
                _training_status["logs"].append(f"Pipe log error (non-fatal): {str(pipe_err)}")
                
            process.wait()
            
            if process.returncode == 0:
                _training_status["logs"].append("Training successfully finished!")
                _training_status["progress"] = 100
                _training_status["current_step"] = "completed"
                # Flag to reload model on next inference
                _ai_model_loaded = False
            else:
                _training_status["logs"].append(f"Training failed with exit code {process.returncode}")
                _training_status["current_step"] = "failed"
                _training_status["last_error"] = f"Subprocess exit code: {process.returncode}"
                
        except Exception as e:
            _training_status["last_error"] = str(e)
            _training_status["current_step"] = "failed"
            _training_status["logs"].append(f"CRITICAL ERROR: {str(e)}")
        finally:
            _training_status["is_training"] = False

    thread = threading.Thread(target=run_training)
    thread.daemon = True
    thread.start()
    
    return jsonify({"success": True, "message": "Training started in background."})

@app.route('/api/training-status')
def api_training_status():
    """Get the current training status and latest logs."""
    status_copy = _training_status.copy()
    # Only send latest logs to keep response small
    status_copy["logs"] = _training_status["logs"][-20:]
    return jsonify(status_copy)


if __name__ == '__main__':
    print("=" * 60)
    print("VedLinks AI Educational Content Generator")
    print("=" * 60)
    print(f"\n📁 Topics directory: {DATA_TOPICS_PATH.absolute()}")
    
    topics = get_available_topics()
    print(f"📚 Available topics: {len(topics)}")
    
    for topic in topics[:5]:  # Show first 5
        print(f"   • Class {topic['class']} {topic['subject']}: {topic['chapter']}")
    
    if len(topics) > 5:
        print(f"   ... and {len(topics) - 5} more")
    
    import torch
    cuda_status = "✅ CUDA Available" if torch.cuda.is_available() else "❌ CUDA Not Found (Using CPU)"
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A"
    
    print(f"\n🚀 Hardware Status: {cuda_status}")
    if torch.cuda.is_available():
        print(f"🎸 GPU: {gpu_name}")
        
    print("\n🌐 Starting server at http://127.0.0.1:5000")
    print("\n📖 API Endpoints:")
    print("   GET  /api/topics          - List all topics")
    print("   GET  /api/topic/<id>      - Get topic details")
    print("   POST /api/generate-paper  - Generate question paper")
    print("   POST /api/generate-lesson-plan - Generate lesson plan")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
