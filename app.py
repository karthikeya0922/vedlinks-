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
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime
from io import BytesIO

# Fix encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Import our modules
from question_paper_generator import get_generator
from src.lesson_planner import LessonPlanner

app = Flask(__name__)
CORS(app)

# Configuration - NEW: Use topics directory instead of raw PDFs
DATA_TOPICS_PATH = Path("data/topics")
REGISTRY_PATH = Path("data/topic_registry.json")


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


@app.route('/api/topics', methods=['GET'])
def api_get_topics():
    """Get list of available topics."""
    topics = get_available_topics()
    return jsonify({
        'success': True,
        'topics': topics,
        'count': len(topics)
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
    """Get practice questions for a topic."""
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
            'explanation': exp
        })
    
    # Add fill in blanks
    for q, ans in knowledge.get('fill_blanks', []):
        questions.append({
            'type': 'fill_blank',
            'question': q.replace('_______', '________'),
            'answer': ans
        })
    
    # Shuffle and limit
    random.shuffle(questions)
    questions = questions[:15]  # Max 15 questions per session
    
    return jsonify({
        'success': True,
        'questions': questions,
        'count': len(questions)
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
            'definition': definition
        })
    
    # If no key_concepts, use short answers as explanations
    if not concepts:
        for q, ans in knowledge.get('short_answers', []):
            concepts.append({
                'term': q,
                'definition': ans
            })
    
    # Add from topics list if still empty
    if not concepts and topic_data.get('topics'):
        for topic in topic_data['topics']:
            concepts.append({
                'term': topic,
                'definition': f'Key topic in {chapter}. Review your textbook for detailed explanation.'
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
    """Generate a lesson plan for selected topics."""
    try:
        config = request.get_json()
        
        if not config:
            return jsonify({
                'success': False,
                'error': 'No configuration provided'
            }), 400
        
        # Get topic ID
        topic_id = config.get('topicId')
        if not topic_id:
            return jsonify({
                'success': False,
                'error': 'Topic ID is required'
            }), 400
        
        # Load topic data
        topic_data = load_topic_data(topic_id)
        if not topic_data:
            return jsonify({
                'success': False,
                'error': f'Topic not found: {topic_id}'
            }), 404
        
        # Get constraints from config
        constraints = {
            'days': config.get('days', 5),
            'periods_per_day': config.get('periodsPerDay', 1),
            'holidays': config.get('holidays', ['Saturday', 'Sunday']),
            'start_date': datetime.now(),
        }
        
        # Add topic difficulties if provided
        if 'topicDifficulties' in config:
            constraints['topic_difficulties'] = config['topicDifficulties']
        
        # Generate lesson plan
        planner = LessonPlanner()
        lesson_plan = planner.generate_lesson_plan(topic_data, constraints)
        
        return jsonify({
            'success': True,
            'lessonPlan': lesson_plan,
            'topic': topic_data,
            'constraints': {
                'days': constraints['days'],
                'periodsPerDay': constraints['periods_per_day'],
                'holidays': constraints['holidays']
            }
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
                        opt_label = chr(65 + i)  # A, B, C, D
                        doc.add_paragraph(f"    {opt_label}) {opt}")
            
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
    
    print("\n🌐 Starting server at http://127.0.0.1:5000")
    print("\n📖 API Endpoints:")
    print("   GET  /api/topics          - List all topics")
    print("   GET  /api/topic/<id>      - Get topic details")
    print("   POST /api/generate-paper  - Generate question paper")
    print("   POST /api/generate-lesson-plan - Generate lesson plan")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
