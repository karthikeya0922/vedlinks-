"""Quick test to isolate the training error."""
import sys
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

try:
    print("Testing imports...")
    from src.train_lora import train_lora
    print("✅ Import successful")
    
    print("\nStarting training...")
    train_lora()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
