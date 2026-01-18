"""
Topic File Generator for VedLinks

Generates individual topic JSON files from the topic registry.
Creates properly named files like 'class_6_science_ch01_food.json'
"""

import os
import re
import json
from pathlib import Path


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "topic_registry.json"
TOPICS_PATH = PROJECT_ROOT / "data" / "topics"


def slugify(text: str) -> str:
    """Convert text to a URL/filename-safe slug."""
    # Convert to lowercase
    text = text.lower()
    # Replace special characters
    text = text.replace('–', '-').replace('—', '-').replace("'", '')
    # Remove anything that's not alphanumeric or hyphen
    text = re.sub(r'[^a-z0-9\-\s]', '', text)
    # Replace spaces with underscores
    text = re.sub(r'\s+', '_', text)
    # Remove multiple underscores
    text = re.sub(r'_+', '_', text)
    # Limit length
    text = text[:30]
    # Remove trailing underscores
    text = text.strip('_')
    return text


def generate_filename(entry: dict) -> str:
    """Generate a proper filename from metadata."""
    class_num = entry.get('class', '0')
    subject = entry.get('subject', 'unknown').lower()
    chapter_num = entry.get('chapter_number', 0)
    chapter_title = entry.get('chapter', 'unknown')
    
    # Create slug from title
    title_slug = slugify(chapter_title)
    
    # Format: class_6_science_ch01_food_where_does_it_come
    filename = f"class_{class_num}_{subject}_ch{chapter_num:02d}_{title_slug}.json"
    
    return filename


def generate_topic_files():
    """Main function to generate topic files from registry."""
    print("=" * 60)
    print("VedLinks Topic File Generator")
    print("=" * 60)
    
    # Check registry exists
    if not REGISTRY_PATH.exists():
        print(f"❌ ERROR: Registry not found: {REGISTRY_PATH}")
        print("\nPlease run extract_pdf_metadata.py first:")
        print("  python scripts/extract_pdf_metadata.py")
        return
    
    # Load registry
    print(f"\n📖 Loading registry from {REGISTRY_PATH}")
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    files_data = registry.get('files', {})
    print(f"   Found {len(files_data)} entries in registry\n")
    
    # Ensure topics directory exists
    TOPICS_PATH.mkdir(parents=True, exist_ok=True)
    
    created_count = 0
    skipped_count = 0
    
    for source_file, entry in files_data.items():
        chapter_title = entry.get('chapter', 'Unknown')
        
        # Skip unknown/empty entries
        if not chapter_title or chapter_title.startswith('Unknown'):
            print(f"⚠️  Skipping {source_file}: No chapter title")
            skipped_count += 1
            continue
        
        # Generate proper filename
        new_filename = generate_filename(entry)
        target_path = TOPICS_PATH / new_filename
        
        # Create the topic JSON file
        topic_data = {
            "class": entry.get('class', '6'),
            "subject": entry.get('subject', 'Science'),
            "chapter": chapter_title,
            "chapter_number": entry.get('chapter_number', 0),
            "topics": entry.get('topics', []),
            "source_pdf": source_file
        }
        
        # Check if file already exists
        if target_path.exists():
            print(f"📄 {new_filename}")
            print(f"   ⚠️  File exists, skipping (delete to regenerate)")
            skipped_count += 1
            continue
        
        # Write the file
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(topic_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created: {new_filename}")
        print(f"   → {chapter_title}")
        created_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 SUMMARY:")
    print(f"   Created: {created_count} new topic files")
    print(f"   Skipped: {skipped_count} files")
    print(f"   Location: {TOPICS_PATH}")
    print("=" * 60)
    
    if created_count > 0:
        print("\n✅ Topic files generated successfully!")
        print("You can now run 'python app.py' to see all chapters in the UI.")


if __name__ == "__main__":
    generate_topic_files()
