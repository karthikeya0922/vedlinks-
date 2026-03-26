"""
Topic-Based Dataset Generator for VedLinks.

NEW APPROACH:
- No PDF parsing, no text chunking, no JSON output from model
- Uses structured topic metadata (class, subject, chapter, topics)
- Generates instruction-style training samples with plain text output
- Supports multiple task types: lesson plans, question papers, explanations, etc.
"""

import os
import json
import sys
import random
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Configuration
TOPICS_DIR = Path("data/topics")
OUTPUT_DIR = Path("data/datasets")
TASK_TYPES = ["lesson_plan", "question_paper", "explanation", "worksheet", "revision_plan"]


def load_topic_files() -> list:
    """Load all topic JSON files from data/topics directory."""
    topics = []
    
    if not TOPICS_DIR.exists():
        print(f"❌ Topics directory not found: {TOPICS_DIR}")
        print("Please create topic JSON files in data/topics/")
        return topics
    
    for file_path in TOPICS_DIR.glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                topic_data = json.load(f)
                topic_data['_source_file'] = file_path.name
                topics.append(topic_data)
        except Exception as e:
            print(f"⚠️  Error loading {file_path.name}: {e}")
    
    return topics


def format_topic_input(topic: dict, constraints: dict = None) -> str:
    """Format topic metadata as plain text input for the model."""
    lines = [
        f"Class: {topic.get('class', 'N/A')}",
        f"Subject: {topic.get('subject', 'N/A')}",
        f"Chapter: {topic.get('chapter', 'N/A')}",
        f"Topics: {', '.join(topic.get('topics', []))}",
    ]
    
    if constraints:
        for key, value in constraints.items():
            if isinstance(value, list):
                lines.append(f"{key.replace('_', ' ').title()}: {', '.join(value)}")
            else:
                lines.append(f"{key.replace('_', ' ').title()}: {value}")
    
    return "\n".join(lines)


# ============================================================================
# TASK GENERATORS - Each generates instruction/input/output training samples
# ============================================================================

def generate_lesson_plan_samples(topic: dict) -> list:
    """Generate lesson planning training samples."""
    samples = []
    
    # Variation 1: Standard 5-day plan
    samples.append({
        "instruction": "Create a detailed 5-day lesson plan for the following NCERT chapter. Include learning objectives, activities, and assessment strategies for each day.",
        "input": format_topic_input(topic, {
            "periods_per_day": 1,
            "holidays": ["Saturday", "Sunday"]
        }),
        "output": generate_lesson_plan_output(topic, days=5)
    })
    
    # Variation 2: 3-day intensive
    samples.append({
        "instruction": "Create a condensed 3-day lesson plan for quick revision of this chapter before exams.",
        "input": format_topic_input(topic, {
            "periods_per_day": 2,
            "focus": "exam preparation"
        }),
        "output": generate_lesson_plan_output(topic, days=3, intensive=True)
    })
    
    # Variation 3: Single topic deep dive
    if len(topic.get('topics', [])) > 0:
        single_topic = random.choice(topic.get('topics', ['General']))
        samples.append({
            "instruction": f"Create a detailed single-day lesson plan focusing on the topic: {single_topic}",
            "input": format_topic_input(topic, {
                "specific_topic": single_topic,
                "periods": 2
            }),
            "output": generate_single_topic_lesson(topic, single_topic)
        })
    
    return samples


def generate_lesson_plan_output(topic: dict, days: int = 5, intensive: bool = False) -> str:
    """Generate a lesson plan output (plain text, not JSON)."""
    topics_list = topic.get('topics', ['General topic'])
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    subject = topic.get('subject', '')
    
    output_lines = [
        f"LESSON PLAN: {chapter_name}",
        f"Class {class_num} {subject}",
        f"Duration: {days} days",
        "=" * 50,
        ""
    ]
    
    topics_per_day = max(1, len(topics_list) // days)
    
    for day in range(1, days + 1):
        start_idx = (day - 1) * topics_per_day
        end_idx = min(start_idx + topics_per_day, len(topics_list))
        day_topics = topics_list[start_idx:end_idx] if start_idx < len(topics_list) else [topics_list[-1]]
        
        output_lines.extend([
            f"DAY {day}: {', '.join(day_topics)}",
            "-" * 40,
            "",
            "Learning Objectives:",
            f"- Students will understand the concept of {day_topics[0].lower()}",
            f"- Students will be able to explain key aspects of {day_topics[0].lower()}",
            "",
            "Teaching Activities:",
            "1. Warm-up (5 min): Quick recap of previous concepts",
            f"2. Introduction (10 min): Introduce {day_topics[0]} with real-life examples",
            "3. Explanation (15 min): Detailed explanation with diagrams on board",
            "4. Discussion (10 min): Interactive Q&A session with students",
            "5. Practice (10 min): Worksheet or textbook exercises",
            "",
            "Assessment:",
            "- Oral questions during the lesson",
            "- Check classwork completion",
            f"- Quick quiz on {day_topics[0]}",
            "",
            "Homework:",
            f"- Read the textbook section on {day_topics[0]}",
            "- Complete exercise questions from NCERT",
            "",
        ])
        
        if intensive:
            output_lines.append("Additional Revision Notes:")
            output_lines.append(f"- Key formulas/definitions for {day_topics[0]}")
            output_lines.append("")
    
    output_lines.extend([
        "=" * 50,
        "End of Lesson Plan",
    ])
    
    return "\n".join(output_lines)


def generate_single_topic_lesson(topic: dict, specific_topic: str) -> str:
    """Generate a single-topic focused lesson plan."""
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    subject = topic.get('subject', '')
    
    return f"""FOCUSED LESSON PLAN: {specific_topic}
Chapter: {chapter_name}
Class {class_num} {subject}
Duration: 2 periods (80 minutes)
{'=' * 50}

LEARNING OBJECTIVES:
By the end of this lesson, students will be able to:
1. Define and explain {specific_topic}
2. Identify real-world examples of {specific_topic}
3. Apply concepts of {specific_topic} to solve problems
4. Connect {specific_topic} to related topics in the chapter

PERIOD 1 (40 minutes):
-----------------------
0-5 min: Warm-up
- Quick brainstorming: What do students already know about {specific_topic}?
- Write student responses on the board

5-20 min: Concept Introduction
- Define {specific_topic} clearly
- Explain with 2-3 real-life examples
- Draw diagrams on the board
- Highlight key terms and definitions

20-35 min: Detailed Explanation
- Break down {specific_topic} into sub-components
- Explain each part with examples
- Address common misconceptions

35-40 min: Quick Check
- 3 oral questions to check understanding

PERIOD 2 (40 minutes):
-----------------------
0-10 min: Recap
- Students summarize what they learned in Period 1
- Address any remaining doubts

10-25 min: Application
- Solve 2-3 example problems on board
- Relate to NCERT textbook examples
- Show step-by-step problem-solving

25-35 min: Practice
- Students work on worksheet individually
- Teacher moves around to help struggling students

35-40 min: Wrap-up
- Key takeaways summary
- Assign homework

MATERIALS NEEDED:
- NCERT textbook
- Whiteboard and markers
- Worksheets (prepared beforehand)
- Visual aids/charts if available

HOMEWORK:
- Complete NCERT exercises related to {specific_topic}
- Write 5 key points about {specific_topic} in notebook

{'=' * 50}
End of Lesson Plan
"""


def generate_question_paper_samples(topic: dict) -> list:
    """Generate question paper training samples."""
    samples = []
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    subject = topic.get('subject', '')
    topics_list = topic.get('topics', ['General'])
    
    # Variation 1: Standard 40-mark paper
    samples.append({
        "instruction": "Generate a 40-mark CBSE-style question paper for the following chapter. Include a mix of MCQs, short answers, and long answers.",
        "input": format_topic_input(topic, {
            "total_marks": 40,
            "section_a": "10 MCQs (1 mark each)",
            "section_b": "5 Short answers (2 marks each)",
            "section_c": "4 Long answers (5 marks each)"
        }),
        "output": generate_question_paper_output(topic, total_marks=40)
    })
    
    # Variation 2: Quick 20-mark test
    samples.append({
        "instruction": "Generate a quick 20-mark class test for formative assessment on this chapter.",
        "input": format_topic_input(topic, {
            "total_marks": 20,
            "section_a": "5 MCQs (1 mark each)",
            "section_b": "5 Fill in the blanks (1 mark each)",
            "section_c": "5 Short answers (2 marks each)"
        }),
        "output": generate_quick_test_output(topic)
    })
    
    # Variation 3: MCQ-only paper
    samples.append({
        "instruction": "Generate a 25-mark MCQ-only question paper for objective assessment.",
        "input": format_topic_input(topic, {
            "total_marks": 25,
            "format": "25 MCQs (1 mark each)",
            "difficulty": "Easy: 10, Medium: 10, Hard: 5"
        }),
        "output": generate_mcq_paper_output(topic)
    })
    
    return samples


def generate_question_paper_output(topic: dict, total_marks: int = 40) -> str:
    """Generate a full question paper (plain text)."""
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    subject = topic.get('subject', '')
    topics_list = topic.get('topics', ['General'])
    
    paper = f"""
{'=' * 60}
{subject.upper()} QUESTION PAPER
Class {class_num} | Chapter: {chapter_name}
Total Marks: {total_marks} | Time: 1.5 hours
{'=' * 60}

General Instructions:
1. All questions are compulsory.
2. Read all questions carefully before answering.
3. Write neat and legible answers.

{'=' * 60}

SECTION A - MULTIPLE CHOICE QUESTIONS (10 × 1 = 10 marks)
Answer the following questions by choosing the correct option:

1. Which of the following is related to {topics_list[0]}?
   a) A correct phenomenon related to {topics_list[0] if len(topics_list)>0 else chapter_name}
   b) Option B - related but incorrect
   c) Option C - common misconception
   d) Option D - completely unrelated
   
   Answer: a) A correct phenomenon related to {topics_list[0] if len(topics_list)>0 else chapter_name}

2. The main characteristic of {topics_list[0] if len(topics_list) > 0 else 'this chapter'} is:
   a) Characteristic 1
   b) The primary property defining {topics_list[0] if len(topics_list)>0 else chapter_name}
   c) Characteristic 3
   d) Characteristic 4
   
   Answer: b) The primary property defining {topics_list[0] if len(topics_list)>0 else chapter_name}

3. In the context of {chapter_name}, which statement is TRUE?
   a) A verified factual statement regarding {chapter_name}
   b) Incorrect statement
   c) Partially correct statement  
   d) Misleading statement
   
   Answer: a) A verified factual statement regarding {chapter_name}

[Questions 4-10 follow similar pattern covering all topics: {', '.join(topics_list)}]

{'=' * 60}

SECTION B - SHORT ANSWER QUESTIONS (5 × 2 = 10 marks)
Answer the following questions in 2-3 sentences:

11. Define {topics_list[0]} and give one example. (2 marks)
    
    Expected Answer: {topics_list[0]} refers to the standard explanation found in {subject} textbooks. 
    An example of this is a practical demonstration of this concept. This is important because it forms the foundation of {chapter_name}.

12. What is the difference between {topics_list[0]} and {topics_list[1] if len(topics_list) > 1 else topics_list[0]} in {chapter_name}? (2 marks)
    
    Expected Answer: {topics_list[0] if len(topics_list)>0 else "The first concept"} is characterized by specific identifiable traits, while 
    {topics_list[1] if len(topics_list)>1 else "the second concept"} is characterized by contrasting recognizable properties. The main 
    difference lies in their fundamental nature.

13. List any four examples of {topics_list[1] if len(topics_list) > 1 else topics_list[0]}. (2 marks)
    
    Expected Answer: Four examples are:
    1. Example 1
    2. Example 2
    3. Example 3
    4. Example 4

14. Explain the importance of {topics_list[-1]} in daily life. (2 marks)
    
    Expected Answer: {topics_list[-1]} is important because its numerous applications 
    and theoretical importance. In daily life, we see this in common household items or natural events.

15. What happens when processes related to {chapter_name} occur? Explain briefly. (2 marks)
    
    Expected Answer: When these processes occur, observable changes and measured outcomes 
    happen. This is because the underlying laws of {subject}.

{'=' * 60}

SECTION C - LONG ANSWER QUESTIONS (4 × 5 = 20 marks)
Answer the following questions in detail:

16. Explain {topics_list[0]} in detail. Include:
    - Definition
    - Characteristics
    - Examples
    - Importance (5 marks)
    
    Expected Answer: 
    Definition: {topics_list[0]} is defined as a thorough explanation detailing the mechanism of {topics_list[0] if len(topics_list)>0 else chapter_name}.
    
    Characteristics:
    - Characteristic 1: a key attribute contributing to its behavior
    - Characteristic 2: a key attribute contributing to its behavior
    - Characteristic 3: a key attribute contributing to its behavior
    
    Examples: Common examples include Natural occurrence, Industrial application, and Laboratory demonstration.
    
    Importance: This concept is important because its numerous applications, theoretical importance, 
    and helps us understand [larger concept].

17. Draw a labeled diagram showing [relevant concept from {chapter_name}]. 
    Explain each labeled part. (5 marks)
    
    Expected Answer: [Diagram description with labels]
    Part 1: Function and purpose of this specific component within the system
    Part 2: Function and purpose of this specific component within the system
    Part 3: Function and purpose of this specific component within the system
    Part 4: Function and purpose of this specific component within the system
    Part 5: Function and purpose of this specific component within the system

18. Compare and contrast {topics_list[0]} and {topics_list[1] if len(topics_list) > 1 else 'related concept'}.
    Present your answer in tabular form. (5 marks)
    
    Expected Answer:
    | Aspect | {topics_list[0]} | {topics_list[1] if len(topics_list) > 1 else 'Related Concept'} |
    |--------|------------------|------------------|
    | Definition | Primary definition of first concept | Primary definition of second concept |
    | Examples | First practical example | Second practical example |
    | Features | Core feature of the first | Core feature of the second |
    | Importance | Significance of the first | Significance of the second |

19. Write a short note on any TWO of the following: (5 marks)
    a) {topics_list[0]}
    b) {topics_list[1] if len(topics_list) > 1 else 'topic B'}
    c) {topics_list[2] if len(topics_list) > 2 else 'topic C'}
    
    Expected Answer:
    [Topic selected 1]: [Detailed explanation in 5-6 sentences covering 
    definition, examples, and importance]
    
    [Topic selected 2]: [Detailed explanation in 5-6 sentences covering 
    definition, examples, and importance]

{'=' * 60}
END OF QUESTION PAPER
{'=' * 60}

ANSWER KEY SUMMARY:
Section A: 1-a, 2-b, 3-a, [4-10 answers...]
Section B: Detailed answers provided above
Section C: Detailed answers provided above

MARKING SCHEME:
- Section A: 1 mark each, no partial marking
- Section B: Half marks for partially correct answers
- Section C: Award marks for content (3), presentation (1), examples (1)
"""
    return paper.strip()


def generate_quick_test_output(topic: dict) -> str:
    """Generate a quick 20-mark class test."""
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    subject = topic.get('subject', '')
    topics_list = topic.get('topics', ['General'])
    
    return f"""
{'=' * 50}
CLASS TEST - {subject.upper()}
Class {class_num} | Chapter: {chapter_name}
Total Marks: 20 | Time: 30 minutes
{'=' * 50}

SECTION A - MCQs (5 × 1 = 5 marks)

1. What is {topics_list[0]}?
   a) The textbook definition of {topics_list[0]}
   b) An incorrect assumption often made
   c) A property of an entirely different topic
   d) An unrelated {subject} concept

2. Which of the following is an example of {topics_list[0]}?
   a) An example from a different chapter
   b) A valid practical example of {topics_list[0]}
   c) A completely theoretical non-example
   d) An incorrect application

3. The main purpose of {topics_list[1] if len(topics_list) > 1 else topics_list[0]} is:
   a) A secondary minor effect
   b) The main objective of this process in {subject}
   c) An unrelated {subject} mechanism
   d) An opposite outcome

4. In {chapter_name}, we learn that:
   a) A verified principle from {chapter_name}
   b) A statement that contradicts the laws of {subject}
   c) A fact from Class {class_num} Math instead
   d) A common misconception about {chapter_name}

5. Which statement is FALSE about {chapter_name}?
   a) A factual observation about {chapter_name}
   b) Another correct principle
   c) An intentionally false statement to test comprehension
   d) A valid concluding statement

SECTION B - FILL IN THE BLANKS (5 × 1 = 5 marks)

6. {topics_list[0]} is defined as __________.
7. The main types of {topics_list[0]} are varied and distinct.
8. __________ is an example of {topics_list[-1]}.
9. The process of __________ helps in producing predictable results.
10. In Class {class_num} {subject}, we study __________ in this chapter.

SECTION C - SHORT ANSWERS (5 × 2 = 10 marks)

11. Define {topics_list[0]}. (2 marks)
12. Give two examples of {topics_list[1] if len(topics_list) > 1 else topics_list[0]}. (2 marks)
13. Why is {chapter_name} important? (2 marks)
14. What is the difference between {topics_list[0]} and {topics_list[1] if len(topics_list) > 1 else topics_list[0]}? (2 marks)
15. Explain any one topic from this chapter in brief. (2 marks)

{'=' * 50}
ANSWER KEY:
Section A: 1-a, 2-b, 3-b, 4-a, 5-c
Section B: 6-[answer], 7-[answer], 8-[answer], 9-[answer], 10-[answer]
Section C: Detailed answers as per textbook
{'=' * 50}
""".strip()


def generate_mcq_paper_output(topic: dict) -> str:
    """Generate MCQ-only paper."""
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    subject = topic.get('subject', '')
    topics_list = topic.get('topics', ['General'])
    
    lines = [
        "=" * 50,
        f"MCQ QUESTION PAPER - {subject.upper()}",
        f"Class {class_num} | Chapter: {chapter_name}",
        f"Total Marks: 25 | Time: 25 minutes",
        "=" * 50,
        "",
        "Instructions: Choose the correct option for each question.",
        "Each question carries 1 mark.",
        "",
    ]
    
    # Generate 25 MCQs
    for i in range(1, 26):
        topic_idx = (i - 1) % len(topics_list)
        current_topic = topics_list[topic_idx]
        
        if i <= 10:
            difficulty = "Easy"
        elif i <= 20:
            difficulty = "Medium"
        else:
            difficulty = "Hard"
        
        lines.extend([
            f"{i}. [{difficulty}] Question about {current_topic}?",
            f"   a) Option A",
            f"   b) Option B (correct)",
            f"   c) Option C",
            f"   d) Option D",
            "",
        ])
    
    lines.extend([
        "=" * 50,
        "ANSWER KEY:",
        "1-b, 2-b, 3-b, 4-b, 5-b, 6-b, 7-b, 8-b, 9-b, 10-b,",
        "11-b, 12-b, 13-b, 14-b, 15-b, 16-b, 17-b, 18-b, 19-b, 20-b,",
        "21-b, 22-b, 23-b, 24-b, 25-b",
        "=" * 50,
    ])
    
    return "\n".join(lines)


def generate_explanation_samples(topic: dict) -> list:
    """Generate topic explanation training samples."""
    samples = []
    topics_list = topic.get('topics', ['General topic'])
    
    for specific_topic in topics_list[:3]:  # Generate for first 3 topics
        samples.append({
            "instruction": f"Explain the concept of '{specific_topic}' in simple terms suitable for a Class {topic.get('class', '')} student.",
            "input": format_topic_input(topic, {"specific_topic": specific_topic}),
            "output": generate_explanation_output(topic, specific_topic)
        })
    
    # Full chapter explanation
    samples.append({
        "instruction": "Provide a comprehensive summary of this entire chapter suitable for quick revision.",
        "input": format_topic_input(topic),
        "output": generate_chapter_summary(topic)
    })
    
    return samples


def generate_explanation_output(topic: dict, specific_topic: str) -> str:
    """Generate a topic explanation."""
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    subject = topic.get('subject', '')
    
    return f"""TOPIC EXPLANATION: {specific_topic}
{'=' * 50}
Chapter: {chapter_name}
Class: {class_num} | Subject: {subject}

WHAT IS {specific_topic.upper()}?
{'-' * 40}
{specific_topic} is an important concept that we study in this chapter. 
In simple words, it refers to [simplified definition that a Class {class_num} 
student can understand].

Think of it like this: [Simple analogy or real-life example that students 
can relate to].

KEY POINTS TO REMEMBER:
{'-' * 40}
1. {specific_topic} is a core component of {chapter_name}.
2. It interacts with other elements in {subject} to produce predictable results.
3. You must remember the specific rules associated with {specific_topic}.
4. How it connects to other topics in the chapter
5. Why it is important to learn

EXAMPLES FROM DAILY LIFE:
{'-' * 40}
- {specific_topic} in natural environments.
- Practical applications of {specific_topic} in modern technology.
- Basic experiments demonstrating {specific_topic} in a school lab.

HOW TO REMEMBER THIS:
{'-' * 40}
A simple trick to remember {specific_topic}:
Always relate {specific_topic} directly to {chapter_name} to remember its role.

COMMON MISTAKES TO AVOID:
{'-' * 40}
- Don't confuse {specific_topic} with other advanced topics in {subject}
- Remember that the idea that {specific_topic} works in isolation is actually wrong
- Always verify your steps when applying {specific_topic} concepts

PRACTICE QUESTIONS:
{'-' * 40}
Try answering these to test your understanding:
1. What is {specific_topic}?
2. Give two examples of {specific_topic}.
3. Why is {specific_topic} important?

{'=' * 50}
Remember: Understanding {specific_topic} will help you in understanding 
the rest of the chapter better!
"""


def generate_chapter_summary(topic: dict) -> str:
    """Generate a full chapter summary."""
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    subject = topic.get('subject', '')
    topics_list = topic.get('topics', ['General topic'])
    
    summary_lines = [
        f"CHAPTER SUMMARY: {chapter_name}",
        "=" * 50,
        f"Class: {class_num} | Subject: {subject}",
        "",
        "OVERVIEW:",
        "-" * 40,
        f"This chapter covers {len(topics_list)} main topics that help us understand",
        f"{chapter_name.lower()}. Let's go through each topic briefly.",
        "",
    ]
    
    for i, topic_name in enumerate(topics_list, 1):
        summary_lines.extend([
            f"TOPIC {i}: {topic_name}",
            "-" * 40,
            f"• Definition: [What {topic_name} means]",
            f"• Key Facts: [Important points about {topic_name}]",
            f"• Examples: [Real-life examples of {topic_name}]",
            "",
        ])
    
    summary_lines.extend([
        "KEY TAKEAWAYS:",
        "-" * 40,
        "1. [Most important point from the chapter]",
        "2. [Second most important point]",
        "3. [Third important point]",
        "4. [Connection between topics]",
        "5. [Practical application of chapter concepts]",
        "",
        "IMPORTANT TERMS:",
        "-" * 40,
    ])
    
    for topic_name in topics_list[:5]:
        summary_lines.append(f"• {topic_name}: [Brief definition]")
    
    summary_lines.extend([
        "",
        "REVISION TIPS:",
        "-" * 40,
        "• Read the chapter summary in NCERT first",
        "• Make notes of key terms and definitions",
        "• Practice the exercises at the end of the chapter",
        "• Try explaining concepts to a friend or family member",
        "",
        "=" * 50,
        "Good luck with your studies!",
    ])
    
    return "\n".join(summary_lines)


def generate_worksheet_samples(topic: dict) -> list:
    """Generate worksheet training samples."""
    samples = []
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    
    # Practice worksheet
    samples.append({
        "instruction": "Create a practice worksheet for this chapter with a variety of question types.",
        "input": format_topic_input(topic, {"purpose": "practice", "difficulty": "mixed"}),
        "output": generate_worksheet_output(topic, "practice")
    })
    
    # Homework worksheet
    samples.append({
        "instruction": "Create a homework assignment worksheet for this chapter.",
        "input": format_topic_input(topic, {"purpose": "homework", "time": "30 minutes"}),
        "output": generate_worksheet_output(topic, "homework")
    })
    
    return samples


def generate_worksheet_output(topic: dict, worksheet_type: str) -> str:
    """Generate a worksheet."""
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    subject = topic.get('subject', '')
    topics_list = topic.get('topics', ['General topic'])
    
    title = "PRACTICE WORKSHEET" if worksheet_type == "practice" else "HOMEWORK WORKSHEET"
    
    return f"""
{'=' * 50}
{title}
{subject} - Class {class_num}
Chapter: {chapter_name}
{'=' * 50}

Name: _________________ Date: ___________ Roll No: _____

SECTION A: TRUE OR FALSE (5 marks)
Write T for True and F for False:

1. [Statement about {topics_list[0]}] _____
2. [Statement about {topics_list[1] if len(topics_list) > 1 else topics_list[0]}] _____
3. [Statement about the chapter] _____
4. [Statement testing misconception] _____
5. [Statement about application] _____

SECTION B: MATCH THE FOLLOWING (5 marks)
Match Column A with Column B:

Column A                    Column B
1. {topics_list[0]}         a. [Related concept]
2. {topics_list[1] if len(topics_list) > 1 else 'Concept 2'}         b. [Related concept]
3. {topics_list[2] if len(topics_list) > 2 else 'Concept 3'}         c. [Related concept]
4. Concept 4                d. [Related concept]
5. Concept 5                e. [Related concept]

SECTION C: FILL IN THE BLANKS (5 marks)

1. {topics_list[0]} is defined as ____________.
2. The main types of ____________ are Type A and Type B.
3. An example of {topics_list[-1]} is ____________.
4. The process of ____________ results in [outcome].
5. In this chapter, we learned that ____________.

SECTION D: SHORT ANSWER QUESTIONS (10 marks)
Answer in 2-3 sentences:

1. What is {topics_list[0]}? (2 marks)
_______________________________________________
_______________________________________________

2. Give two examples of {topics_list[1] if len(topics_list) > 1 else topics_list[0]}. (2 marks)
_______________________________________________
_______________________________________________

3. Why is {chapter_name} important to study? (2 marks)
_______________________________________________
_______________________________________________

4. Explain one real-life application of concepts from this chapter. (2 marks)
_______________________________________________
_______________________________________________

5. What is the difference between {topics_list[0]} and {topics_list[1] if len(topics_list) > 1 else topics_list[0]}? (2 marks)
_______________________________________________
_______________________________________________

SECTION E: DIAGRAM (5 marks)
Draw a neat labeled diagram of [relevant concept from {chapter_name}].

[Space for diagram]

{'=' * 50}
TEACHER'S REMARKS:

Marks Obtained: _____ / 30

{'=' * 50}
""".strip()


def generate_revision_samples(topic: dict) -> list:
    """Generate revision plan training samples."""
    samples = []
    
    # One-day revision
    samples.append({
        "instruction": "Create a quick 1-day revision plan for this chapter before an exam.",
        "input": format_topic_input(topic, {"time_available": "1 day", "purpose": "exam preparation"}),
        "output": generate_revision_plan_output(topic, days=1)
    })
    
    # Week-long revision
    samples.append({
        "instruction": "Create a comprehensive week-long revision schedule for this chapter.",
        "input": format_topic_input(topic, {"time_available": "1 week", "purpose": "thorough revision"}),
        "output": generate_revision_plan_output(topic, days=7)
    })
    
    return samples


def generate_revision_plan_output(topic: dict, days: int) -> str:
    """Generate a revision plan."""
    chapter_name = topic.get('chapter', 'Chapter')
    class_num = topic.get('class', '')
    subject = topic.get('subject', '')
    topics_list = topic.get('topics', ['General topic'])
    
    if days == 1:
        return f"""
ONE-DAY REVISION PLAN
{'=' * 50}
Chapter: {chapter_name}
Class {class_num} {subject}
{'=' * 50}

MORNING SESSION (2 hours):
{'-' * 40}
Hour 1: Quick Read-Through
- Skim through the entire chapter in NCERT (30 min)
- Highlight key terms and definitions (15 min)
- Note down formulas/important points (15 min)

Hour 2: Topic-Wise Revision
- {topics_list[0]}: Read and make quick notes (20 min)
- {topics_list[1] if len(topics_list) > 1 else 'Topic 2'}: Focus on examples (20 min)
- {topics_list[2] if len(topics_list) > 2 else 'Remaining topics'}: Quick overview (20 min)

AFTERNOON SESSION (2 hours):
{'-' * 40}
Hour 3: Practice Questions
- Solve NCERT exercise questions (30 min)
- Practice previous year questions (30 min)

Hour 4: Self-Assessment
- Take a quick self-test (20 min)
- Review wrong answers (20 min)
- Final doubt clearance (20 min)

EVENING SESSION (1 hour):
{'-' * 40}
- Quick flashcard review of key terms (20 min)
- Recite main points aloud (20 min)
- Relax and get good sleep! (20 min)

KEY POINTS TO MEMORIZE:
{'-' * 40}
1. [Key point 1 about {topics_list[0]}]
2. [Key point 2 about {topics_list[1] if len(topics_list) > 1 else 'chapter'}]
3. [Key point 3 about {topics_list[2] if len(topics_list) > 2 else 'chapter'}]
4. [Important formula/definition]
5. [Common exam question area]

LAST-MINUTE TIPS:
{'-' * 40}
- Don't try to learn new things at this point
- Focus on what you already know
- Stay calm and confident
- Get proper sleep before exam

{'=' * 50}
Good luck with your exam!
""".strip()
    else:
        plan_lines = [
            f"WEEK-LONG REVISION PLAN",
            "=" * 50,
            f"Chapter: {chapter_name}",
            f"Class {class_num} {subject}",
            "=" * 50,
            "",
        ]
        
        day_activities = [
            ("Overview & Planning", "Read entire chapter, identify weak areas"),
            ("Core Concepts", f"Deep study of {topics_list[0]}"),
            ("Practice Day 1", "Solve NCERT exercises"),
            ("Additional Topics", f"Study {', '.join(topics_list[1:3]) if len(topics_list) > 1 else 'remaining topics'}"),
            ("Practice Day 2", "Previous year questions"),
            ("Revision & Gaps", "Fill knowledge gaps, revisit weak areas"),
            ("Final Review", "Quick revision, mock test, rest"),
        ]
        
        for day_num, (activity, description) in enumerate(day_activities, 1):
            plan_lines.extend([
                f"DAY {day_num}: {activity}",
                "-" * 40,
                f"Morning: {description}",
                f"Afternoon: Practice related questions",
                f"Evening: Review and note-making",
                "",
            ])
        
        plan_lines.extend([
            "STUDY TIPS:",
            "-" * 40,
            "• Study in 45-minute blocks with 10-minute breaks",
            "• Make flashcards for key terms",
            "• Teach concepts to someone else",
            "• Solve at least 5 questions daily",
            "",
            "=" * 50,
        ])
        
        return "\n".join(plan_lines)


def generate_dataset():
    """Main function to generate the instruction-style dataset."""
    print("=" * 60)
    print("VedLinks Topic-Based Dataset Generator")
    print("=" * 60)
    
    # Load topic files
    print("\n📚 Loading topic files from data/topics/...")
    topics = load_topic_files()
    
    if not topics:
        print("❌ No topic files found!")
        print("Please add JSON files to data/topics/ directory")
        print("\nExample file format:")
        print(json.dumps({
            "class": "6",
            "subject": "Science",
            "chapter": "Food – Where Does It Come From?",
            "topics": ["Sources of food", "Plant products", "Animal products"]
        }, indent=2))
        return
    
    print(f"✅ Loaded {len(topics)} topic files")
    
    # Generate samples for each topic
    print("\n🔮 Generating training samples...")
    all_samples = []
    
    for topic in tqdm(topics, desc="Processing topics"):
        # Generate all task types
        all_samples.extend(generate_lesson_plan_samples(topic))
        all_samples.extend(generate_question_paper_samples(topic))
        all_samples.extend(generate_explanation_samples(topic))
        all_samples.extend(generate_worksheet_samples(topic))
        all_samples.extend(generate_revision_samples(topic))
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save dataset
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"instruction_{timestamp}.jsonl"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for sample in all_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    # Also update the main finetune dataset
    main_dataset = Path("data/finetune_dataset.jsonl")
    with open(main_dataset, 'w', encoding='utf-8') as f:
        for sample in all_samples:
            # Format for training: instruction + input -> output
            training_sample = {
                "prompt": f"### Instruction:\n{sample['instruction']}\n\n### Input:\n{sample['input']}\n\n### Response:",
                "completion": sample['output']
            }
            f.write(json.dumps(training_sample, ensure_ascii=False) + '\n')
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ DATASET GENERATION COMPLETE")
    print("=" * 60)
    print(f"📊 Total samples generated: {len(all_samples)}")
    print(f"📊 Topics processed: {len(topics)}")
    print(f"📁 Raw output: {output_file}")
    print(f"📁 Training file: {main_dataset}")
    
    # Sample breakdown
    print("\n📈 Sample breakdown by type:")
    sample_types = {}
    for sample in all_samples:
        instruction_start = sample['instruction'].split()[0:3]
        sample_type = ' '.join(instruction_start)
        sample_types[sample_type] = sample_types.get(sample_type, 0) + 1
    
    for sample_type, count in sorted(sample_types.items()):
        print(f"   • {sample_type}...: {count}")


if __name__ == "__main__":
    try:
        generate_dataset()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
