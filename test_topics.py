"""Quick test to verify topics are loading from registry."""
import sys
sys.path.insert(0, '.')
from app import get_available_topics

topics = get_available_topics()
print(f"Total topics: {len(topics)}")
print()
for t in topics:
    source = t.get('source', 'unknown')
    print(f"  - Class {t['class']} {t['subject']}: {t['chapter']} [{source}]")
