"""
Quick start script - runs the complete pipeline from raw data to trained model.
"""

import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Run a command and show progress."""
    print(f"\n{'='*60}")
    print(f"📍 {description}")
    print(f"{'='*60}")
    print(f"$ {cmd}")
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode != 0:
        print(f"\n❌ Failed: {description}")
        return False
    
    return True


def main():
    """Run the complete pipeline."""
    print("="*60)
    print("VedLinks AI-Backend - Quick Start")
    print("="*60)
    
    # Check setup
    if not run_command("python setup_check.py", "Verifying setup"):
        print("\n⚠️  Setup check failed. Please fix issues first.")
        return 1
    
    # Check for data files
    raw_dir = Path("data/raw")
    data_files = list(raw_dir.glob("*.pdf")) + list(raw_dir.glob("*.txt"))
    
    if not data_files:
        print("\n⚠️  No PDF or TXT files found in data/raw/")
        print("Please add your files to data/raw/ and run again.")
        return 1
    
    print(f"\n✅ Found {len(data_files)} files to process:")
    for f in data_files:
        print(f"   - {f.name}")
    
    # Confirm
    response = input("\n▶️  Start pipeline? [y/N]: ")
    if response.lower() != 'y':
        print("Cancelled.")
        return 0
    
    # Step 1: Generate dataset
    if not run_command("python -m src.dataset_generator", "Step 1: Generate dataset"):
        return 1
    
    # Step 2: Prepare for finetune
    if not run_command("python -m src.utils.prepare_for_finetune", "Step 2: Prepare finetune dataset"):
        return 1
    
    # Step 3: Ask about training
    print("\n" + "="*60)
    print("📊 Dataset preparation complete!")
    print("="*60)
    
    response = input("\n▶️  Start QLoRA training? (This may take a while) [y/N]: ")
    if response.lower() == 'y':
        if not run_command("python -m src.train_lora", "Step 3: Train QLoRA model"):
            return 1
        
        print("\n" + "="*60)
        print("🎉 COMPLETE! Model trained and saved to output/qlora_tuned_model/")
        print("="*60)
    else:
        print("\nSkipping training. You can run it later with:")
        print("  python -m src.train_lora")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
