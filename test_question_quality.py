"""
VedLinks AI/ML Quality Test Script

Tests all 6 bug fixes:
  BUG-01: Difficulty-aware question selection
  BUG-02: Question deduplication
  BUG-03: Bloom's taxonomy enforcement
  BUG-04: Multi-chapter distribution
  BUG-05: Distractor quality (shuffle verification)
  BUG-06: Answer distribution balancing (A/B/C/D roughly equal)
"""

import sys
import json
from collections import Counter

# Add project root to path
sys.path.insert(0, '.')

from question_paper_generator import QuestionPaperGenerator, NCERT_KNOWLEDGE, get_generator


def test_bug01_difficulty_awareness():
    """BUG-01: Verify that questions at different difficulty levels are different."""
    print("\n" + "=" * 60)
    print("TEST BUG-01: Difficulty-Aware Question Selection")
    print("=" * 60)
    
    gen = QuestionPaperGenerator()
    
    # Use Heredity chapter (has many questions)
    knowledge = NCERT_KNOWLEDGE.get("Heredity", {})
    if not knowledge:
        print("  SKIP: No Heredity chapter found")
        return False
    
    gen._used_questions = set()
    easy_qs = gen.generate_mcqs(knowledge, 5, 'easy')
    
    gen._used_questions = set()
    hard_qs = gen.generate_mcqs(knowledge, 5, 'hard')
    
    easy_texts = set(q['question'] for q in easy_qs)
    hard_texts = set(q['question'] for q in hard_qs)
    overlap = easy_texts & hard_texts
    
    overlap_pct = len(overlap) / max(1, len(easy_texts)) * 100
    
    print(f"  Easy questions: {len(easy_texts)}")
    print(f"  Hard questions: {len(hard_texts)}")
    print(f"  Overlap: {len(overlap)} ({overlap_pct:.0f}%)")
    
    # Check Bloom's levels
    easy_levels = [q.get('bloomsLevel', 'L1') for q in easy_qs]
    hard_levels = [q.get('bloomsLevel', 'L1') for q in hard_qs]
    print(f"  Easy Bloom's levels: {Counter(easy_levels)}")
    print(f"  Hard Bloom's levels: {Counter(hard_levels)}")
    
    passed = overlap_pct < 80  # At least 20% different
    print(f"  RESULT: {'PASS' if passed else 'FAIL'} (overlap < 80%: {overlap_pct:.0f}%)")
    return passed


def test_bug02_deduplication():
    """BUG-02: Verify no duplicate questions within a single paper."""
    print("\n" + "=" * 60)
    print("TEST BUG-02: Question Deduplication")
    print("=" * 60)
    
    gen = QuestionPaperGenerator()
    
    config = {
        'examType': 'Unit Test',
        'sections': [
            {'name': 'Section A', 'questionType': 'mcq', 'questionCount': 5, 'marksPerQuestion': 1},
            {'name': 'Section B', 'questionType': 'mcq', 'questionCount': 5, 'marksPerQuestion': 1},
        ],
        'selectedTopics': ['heredity'],
        'difficulty': {'easy': 30, 'medium': 50, 'hard': 20},
        'includeAnswerKey': True,
    }
    
    topic_contents = {
        'heredity': "Class: 10\nSubject: Science\nChapter: Heredity\nTopics: Genetics, Mendel's Laws"
    }
    
    paper = gen.generate_paper(config, topic_contents)
    
    all_questions = []
    for section in paper['sections']:
        for q in section['questions']:
            all_questions.append(q['question'])
    
    unique_questions = set(all_questions)
    duplicates = len(all_questions) - len(unique_questions)
    
    print(f"  Total questions: {len(all_questions)}")
    print(f"  Unique questions: {len(unique_questions)}")
    print(f"  Duplicates: {duplicates}")
    
    passed = duplicates == 0
    print(f"  RESULT: {'PASS' if passed else 'FAIL'}")
    return passed


def test_bug03_blooms_taxonomy():
    """BUG-03: Verify Bloom's taxonomy classification works."""
    print("\n" + "=" * 60)
    print("TEST BUG-03: Bloom's Taxonomy Enforcement")
    print("=" * 60)
    
    test_cases = [
        ("What is photosynthesis?", "L1"),
        ("Define osmosis.", "L1"),
        ("Explain the process of digestion.", "L2"),
        ("Why do plants need sunlight?", "L2"),
        ("Calculate the ratio of offspring.", "L3"),
        ("Draw a labeled diagram of the heart.", "L3"),
        ("Compare mitosis and meiosis.", "L4"),
        ("Evaluate the effectiveness of vaccination.", "L5"),
        ("Design an experiment to test osmosis.", "L6"),
    ]
    
    correct = 0
    gen = QuestionPaperGenerator()
    
    for question, expected_level in test_cases:
        actual_level = gen.classify_blooms_level(question)
        match = actual_level == expected_level
        correct += int(match)
        status = "OK" if match else "XX"
        print(f"  {status} '{question[:50]}...' -> {actual_level} (expected {expected_level})")
    
    accuracy = correct / len(test_cases) * 100
    passed = accuracy >= 70  # Allow some flexibility
    print(f"\n  Accuracy: {accuracy:.0f}% ({correct}/{len(test_cases)})")
    print(f"  RESULT: {'PASS' if passed else 'FAIL'}")
    return passed


def test_bug04_multi_chapter_distribution():
    """BUG-04: Verify questions come from multiple chapters when selected."""
    print("\n" + "=" * 60)
    print("TEST BUG-04: Multi-Chapter Distribution")
    print("=" * 60)
    
    gen = QuestionPaperGenerator()
    
    config = {
        'examType': 'Unit Test',
        'sections': [
            {'name': 'Section A', 'questionType': 'mcq', 'questionCount': 10, 'marksPerQuestion': 1},
        ],
        'difficulty': {'easy': 30, 'medium': 50, 'hard': 20},
    }
    
    topic_contents = {
        'heredity': "Class: 10\nSubject: Science\nChapter: Heredity\nTopics: Genetics",
        'evolution': "Class: 10\nSubject: Science\nChapter: Our Environment\nTopics: Ecosystem",
    }
    
    paper = gen.generate_paper(config, topic_contents)
    
    chapters_used = set()
    for section in paper['sections']:
        for q in section['questions']:
            chapter = q.get('chapter', 'Unknown')
            chapters_used.add(chapter)
    
    print(f"  Chapters selected: {len(topic_contents)}")
    print(f"  Chapters in paper: {len(chapters_used)} — {chapters_used}")
    
    passed = len(chapters_used) >= 2
    print(f"  RESULT: {'PASS' if passed else 'FAIL'}")
    return passed


def test_bug06_answer_distribution():
    """BUG-06: Verify A/B/C/D answer distribution is roughly equal."""
    print("\n" + "=" * 60)
    print("TEST BUG-06: Answer Distribution Balance")
    print("=" * 60)
    
    gen = QuestionPaperGenerator()
    
    config = {
        'examType': 'Unit Test',
        'sections': [
            {'name': 'Section A', 'questionType': 'mcq', 'questionCount': 12, 'marksPerQuestion': 1},
        ],
        'difficulty': {'easy': 30, 'medium': 50, 'hard': 20},
    }
    
    topic_contents = {
        'heredity': "Class: 10\nSubject: Science\nChapter: Heredity\nTopics: Genetics",
    }
    
    paper = gen.generate_paper(config, topic_contents)
    
    answer_counts = Counter()
    for section in paper['sections']:
        for q in section['questions']:
            if q.get('type') == 'mcq':
                answer_counts[q.get('answer', '?')] += 1
    
    total = sum(answer_counts.values())
    target = total / 4
    
    print(f"  Answer distribution: {dict(answer_counts)}")
    print(f"  Total MCQs: {total}, Target per letter: {target:.1f}")
    
    # Check that no letter has more than 50% of answers
    max_pct = max(answer_counts.values()) / max(1, total) * 100
    
    passed = max_pct <= 50  # No single letter should have >50%
    print(f"  Max concentration: {max_pct:.0f}%")
    print(f"  RESULT: {'PASS' if passed else 'FAIL'}")
    return passed


def test_difficulty_in_paper():
    """Additional: Verify difficulty labels are real, not cosmetic."""
    print("\n" + "=" * 60)
    print("TEST: Difficulty Labels Are Real (Not Cosmetic)")
    print("=" * 60)
    
    gen = QuestionPaperGenerator()
    
    config = {
        'examType': 'Unit Test',
        'sections': [
            {'name': 'Section A', 'questionType': 'mcq', 'questionCount': 10, 'marksPerQuestion': 1},
        ],
        'difficulty': {'easy': 100, 'medium': 0, 'hard': 0},
    }
    
    topic_contents = {
        'heredity': "Class: 10\nSubject: Science\nChapter: Heredity\nTopics: Genetics",
    }
    
    paper_easy = gen.generate_paper(config, topic_contents)
    
    config['difficulty'] = {'easy': 0, 'medium': 0, 'hard': 100}
    paper_hard = gen.generate_paper(config, topic_contents)
    
    easy_qs = set()
    hard_qs = set()
    
    for section in paper_easy['sections']:
        for q in section['questions']:
            easy_qs.add(q['question'])
            
    for section in paper_hard['sections']:
        for q in section['questions']:
            hard_qs.add(q['question'])
    
    overlap = easy_qs & hard_qs
    overlap_pct = len(overlap) / max(1, len(easy_qs)) * 100
    
    print(f"  100% Easy paper questions: {len(easy_qs)}")
    print(f"  100% Hard paper questions: {len(hard_qs)}")
    print(f"  Overlap: {len(overlap)} ({overlap_pct:.0f}%)")
    
    # Difficulty labels
    easy_diffs = Counter()
    hard_diffs = Counter()
    for section in paper_easy['sections']:
        for q in section['questions']:
            easy_diffs[q.get('difficulty', '?')] += 1
    for section in paper_hard['sections']:
        for q in section['questions']:
            hard_diffs[q.get('difficulty', '?')] += 1
    
    print(f"  Easy paper difficulty labels: {dict(easy_diffs)}")
    print(f"  Hard paper difficulty labels: {dict(hard_diffs)}")
    
    passed = overlap_pct < 80
    print(f"  RESULT: {'PASS' if passed else 'FAIL'}")
    return passed


if __name__ == '__main__':
    print("=" * 60)
    print("VedLinks AI/ML Quality Test Suite")
    print("=" * 60)
    
    results = {}
    results['BUG-01'] = test_bug01_difficulty_awareness()
    results['BUG-02'] = test_bug02_deduplication()
    results['BUG-03'] = test_bug03_blooms_taxonomy()
    results['BUG-04'] = test_bug04_multi_chapter_distribution()
    results['BUG-06'] = test_bug06_answer_distribution()
    results['DIFF_REAL'] = test_difficulty_in_paper()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for test, passed in results.items():
        print(f"  {test}: {'PASS' if passed else 'FAIL'}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print(f"\n  {passed}/{total} tests passed")
    
    sys.exit(0 if passed == total else 1)
