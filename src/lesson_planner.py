"""
Lesson Planner Module for VedLinks.

Provides functionality to generate teacher-friendly lesson plans based on:
- Chapter and topic metadata
- Scheduling constraints (holidays, periods per day)
- Topic difficulty weighting
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class LessonPlanner:
    """Generate lesson plans based on topic metadata and constraints."""
    
    # Day names for scheduling
    DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Default topic difficulty levels (can be overridden)
    DEFAULT_DIFFICULTY = {
        'easy': 1,      # 1 period needed
        'medium': 2,    # 2 periods needed
        'hard': 3       # 3 periods needed
    }
    
    def __init__(self):
        """Initialize the lesson planner."""
        pass
    
    def load_topic(self, topic_file: str) -> dict:
        """Load topic from a JSON file."""
        file_path = Path(topic_file)
        if not file_path.exists():
            raise FileNotFoundError(f"Topic file not found: {topic_file}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def calculate_teaching_days(self, start_date: datetime, num_days: int, 
                                 holidays: list = None) -> list:
        """Calculate actual teaching days excluding holidays."""
        holidays = holidays or ['Saturday', 'Sunday']
        holidays_lower = [h.lower() for h in holidays]
        
        teaching_days = []
        current_date = start_date
        
        while len(teaching_days) < num_days:
            day_name = self.DAY_NAMES[current_date.weekday()]
            if day_name.lower() not in holidays_lower:
                teaching_days.append({
                    'date': current_date,
                    'day_name': day_name,
                    'day_number': len(teaching_days) + 1
                })
            current_date += timedelta(days=1)
        
        return teaching_days
    
    def distribute_topics(self, topics: list, num_days: int, 
                          topic_difficulties: dict = None) -> list:
        """Distribute topics across teaching days based on difficulty."""
        if not topics:
            return []
        
        topic_difficulties = topic_difficulties or {}
        
        # Calculate total periods needed
        topic_periods = []
        for topic in topics:
            difficulty = topic_difficulties.get(topic, 'medium')
            periods = self.DEFAULT_DIFFICULTY.get(difficulty, 2)
            topic_periods.append({'topic': topic, 'periods': periods, 'difficulty': difficulty})
        
        total_periods = sum(t['periods'] for t in topic_periods)
        periods_per_day = max(1, total_periods // num_days)
        
        # Distribute topics to days
        days_plan = []
        current_day = []
        current_periods = 0
        
        for topic_info in topic_periods:
            if current_periods + topic_info['periods'] > periods_per_day and current_day:
                days_plan.append(current_day)
                current_day = []
                current_periods = 0
            
            current_day.append(topic_info)
            current_periods += topic_info['periods']
        
        if current_day:
            days_plan.append(current_day)
        
        # Ensure we have exactly num_days (pad or merge)
        while len(days_plan) < num_days and days_plan:
            # Split the day with most topics
            max_idx = max(range(len(days_plan)), key=lambda i: len(days_plan[i]))
            if len(days_plan[max_idx]) > 1:
                split_point = len(days_plan[max_idx]) // 2
                days_plan.insert(max_idx + 1, days_plan[max_idx][split_point:])
                days_plan[max_idx] = days_plan[max_idx][:split_point]
            else:
                break
        
        while len(days_plan) > num_days:
            # Merge last two days
            days_plan[-2].extend(days_plan[-1])
            days_plan.pop()
        
        return days_plan
    
    def generate_lesson_plan(self, topic: dict, constraints: dict = None) -> str:
        """
        Generate a complete lesson plan.
        
        Args:
            topic: Topic dictionary with class, subject, chapter, topics
            constraints: Dictionary with:
                - days: Number of teaching days (default: 5)
                - periods_per_day: Periods per day (default: 1)
                - holidays: List of holiday days (default: ['Saturday', 'Sunday'])
                - start_date: Optional start date
                - topic_difficulties: Optional {topic: difficulty} mapping
        
        Returns:
            Formatted lesson plan as string
        """
        constraints = constraints or {}
        
        # Extract parameters
        num_days = constraints.get('days', 5)
        periods_per_day = constraints.get('periods_per_day', 1)
        holidays = constraints.get('holidays', ['Saturday', 'Sunday'])
        start_date = constraints.get('start_date', datetime.now())
        topic_difficulties = constraints.get('topic_difficulties', {})
        
        # Get topic info
        class_num = topic.get('class', 'N/A')
        subject = topic.get('subject', 'N/A')
        chapter = topic.get('chapter', 'Chapter')
        topics_list = topic.get('topics', [])
        
        # Calculate teaching days
        teaching_days = self.calculate_teaching_days(start_date, num_days, holidays)
        
        # Distribute topics
        days_plan = self.distribute_topics(topics_list, num_days, topic_difficulties)
        
        # Generate the plan
        lines = [
            "=" * 60,
            f"LESSON PLAN",
            "=" * 60,
            "",
            f"Chapter: {chapter}",
            f"Class: {class_num} | Subject: {subject}",
            f"Duration: {num_days} teaching days",
            f"Periods per day: {periods_per_day}",
            f"Holidays: {', '.join(holidays)}",
            "",
            "-" * 60,
        ]
        
        for i, day_info in enumerate(teaching_days):
            day_topics = days_plan[i] if i < len(days_plan) else []
            topic_names = [t['topic'] for t in day_topics]
            
            lines.extend([
                "",
                f"DAY {day_info['day_number']} ({day_info['day_name']}, {day_info['date'].strftime('%d %b %Y')})",
                f"Topics: {', '.join(topic_names) if topic_names else 'Revision/Assessment'}",
                "-" * 40,
            ])
            
            # Generate activities for each topic
            for topic_info in day_topics:
                topic_name = topic_info['topic']
                difficulty = topic_info['difficulty']
                
                lines.extend([
                    "",
                    f"📚 {topic_name} [{difficulty.upper()}]",
                    "",
                    "Learning Objectives:",
                    f"  • Students will understand the concept of {topic_name.lower()}",
                    f"  • Students will be able to explain and apply {topic_name.lower()}",
                    "",
                    "Teaching Strategy:",
                    f"  1. Introduction (5 min): Connect to previous knowledge",
                    f"  2. Explanation (15 min): Explain {topic_name} with examples",
                    f"  3. Discussion (10 min): Interactive Q&A",
                    f"  4. Practice (10 min): Guided exercises",
                    "",
                    "Resources Needed:",
                    f"  • NCERT Textbook - Class {class_num} {subject}",
                    "  • Whiteboard/Blackboard",
                    "  • Visual aids (if available)",
                    "",
                    "Assessment:",
                    f"  • Oral questions during lesson",
                    f"  • Quick 5-question quiz at end of topic",
                ])
            
            # Add homework section
            if topic_names:
                lines.extend([
                    "",
                    "📝 Homework:",
                    f"  • Read NCERT section on: {', '.join(topic_names)}",
                    f"  • Complete exercises from textbook",
                    f"  • Write 3 key points about each topic in notebook",
                ])
        
        # Add summary and tips
        lines.extend([
            "",
            "=" * 60,
            "TEACHING TIPS",
            "=" * 60,
            "",
            "• Use real-life examples that students can relate to",
            "• Encourage questions and discussions",
            "• Connect new topics to previously learned concepts",
            "• Use visual aids and diagrams wherever possible",
            "• Assign peer-learning activities for difficult topics",
            "",
            "ASSESSMENT SUGGESTIONS:",
            "• Conduct a short quiz after every 2-3 topics",
            "• Assign a chapter-end project or presentation",
            "• Review homework regularly",
            "",
            "=" * 60,
            f"Generated on: {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
            "=" * 60,
        ])
        
        return "\n".join(lines)
    
    def generate_quick_plan(self, topic: dict, days: int = 3) -> str:
        """Generate a condensed lesson plan for quick revision."""
        class_num = topic.get('class', 'N/A')
        subject = topic.get('subject', 'N/A')
        chapter = topic.get('chapter', 'Chapter')
        topics_list = topic.get('topics', [])
        
        topics_per_day = max(1, len(topics_list) // days)
        
        lines = [
            "=" * 50,
            f"QUICK REVISION PLAN: {chapter}",
            f"Class {class_num} {subject}",
            f"Duration: {days} days (intensive)",
            "=" * 50,
        ]
        
        for day in range(1, days + 1):
            start_idx = (day - 1) * topics_per_day
            end_idx = min(start_idx + topics_per_day + 1, len(topics_list))
            day_topics = topics_list[start_idx:end_idx]
            
            lines.extend([
                "",
                f"DAY {day}: {', '.join(day_topics)}",
                "-" * 40,
                "• Quick concept review (15 min per topic)",
                "• Key definitions and formulas",
                "• Solve 2-3 important questions",
                "• Make flashcards for revision",
            ])
        
        lines.extend([
            "",
            "=" * 50,
            "Focus on understanding concepts, not memorizing!",
            "=" * 50,
        ])
        
        return "\n".join(lines)


# Module functions for easy access

def generate_lesson_plan(topic_file: str, constraints: dict = None) -> str:
    """
    Generate a lesson plan from a topic file.
    
    Args:
        topic_file: Path to topic JSON file
        constraints: Optional scheduling constraints
    
    Returns:
        Formatted lesson plan string
    """
    planner = LessonPlanner()
    topic = planner.load_topic(topic_file)
    return planner.generate_lesson_plan(topic, constraints)


def generate_lesson_plan_from_dict(topic: dict, constraints: dict = None) -> str:
    """
    Generate a lesson plan from a topic dictionary.
    
    Args:
        topic: Topic dictionary with class, subject, chapter, topics
        constraints: Optional scheduling constraints
    
    Returns:
        Formatted lesson plan string
    """
    planner = LessonPlanner()
    return planner.generate_lesson_plan(topic, constraints)


if __name__ == "__main__":
    # Demo usage
    sample_topic = {
        "class": "6",
        "subject": "Science",
        "chapter": "Food – Where Does It Come From?",
        "topics": [
            "Sources of food",
            "Plant products as food",
            "Animal products as food",
            "Edible parts of plants",
            "Herbivores, carnivores, and omnivores"
        ]
    }
    
    planner = LessonPlanner()
    
    print("Generating lesson plan...")
    print()
    
    plan = planner.generate_lesson_plan(sample_topic, {
        'days': 5,
        'periods_per_day': 1,
        'holidays': ['Saturday', 'Sunday'],
        'topic_difficulties': {
            'Sources of food': 'easy',
            'Plant products as food': 'easy',
            'Animal products as food': 'medium',
            'Edible parts of plants': 'medium',
            'Herbivores, carnivores, and omnivores': 'hard'
        }
    })
    
    print(plan)
