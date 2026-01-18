"""
Quick test script to verify installation and model loading.
"""

import os
import sys
import warnings
from pathlib import Path

# Suppress bitsandbytes warnings (cosmetic only, doesn't affect functionality)
warnings.filterwarnings('ignore', category=UserWarning, module='bitsandbytes')


def check_dependencies():
    """Check if all required packages are installed."""
    required = [
        "torch",
        "transformers",
        "accelerate",
        "datasets",
        "peft",
        "trl",
        "bitsandbytes",
        "PyPDF2",
        "pdfplumber",
        "dotenv",
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package if package != "dotenv" else "dotenv")
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def check_directories():
    """Check if required directories exist."""
    required_dirs = [
        "data/raw",
        "data/datasets",
        "data/failed_generations",
        "src/utils",
        "output",
    ]
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}")
        else:
            print(f"⚠️  Creating {dir_path}")
            path.mkdir(parents=True, exist_ok=True)
    
    print("\n✅ All directories ready!")
    return True


def check_env():
    """Check if .env file exists."""
    if Path(".env").exists():
        print("✅ .env file found")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        model = os.getenv("LOCAL_MODEL_NAME")
        print(f"   Model: {model}")
        return True
    else:
        print("⚠️  .env not found")
        print("   Copy .env.example to .env and configure it")
        return False


def test_model_loading():
    """Test loading the model specified in .env."""
    try:
        import torch
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check GPU first
        if torch.cuda.is_available():
            print(f"\n🎮 GPU Status:")
            print(f"   ✅ CUDA Available: True")
            print(f"   ✅ GPU: {torch.cuda.get_device_name(0)}")
            print(f"   ✅ VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        
        model_name = os.getenv("LOCAL_MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        print(f"\n🔍 Testing model load: {model_name}")
        
        from transformers import AutoTokenizer
        
        print("   Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print(f"   ✅ Tokenizer loaded ({len(tokenizer)} tokens)")
        
        print("\n✅ Model components can be loaded!")
        print("   (Full model loading skipped to save time)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Model loading failed: {e}")
        return False


def main():
    """Run all checks."""
    print("="*60)
    print("VedLinks AI-Backend Setup Check")
    print("="*60)
    
    print("\n📦 Checking dependencies...")
    deps_ok = check_dependencies()
    
    print("\n📁 Checking directories...")
    dirs_ok = check_directories()
    
    print("\n⚙️  Checking configuration...")
    env_ok = check_env()
    
    if deps_ok and env_ok:
        print("\n🤖 Testing model...")
        model_ok = test_model_loading()
    else:
        model_ok = False
    
    print("\n" + "="*60)
    if deps_ok and dirs_ok and env_ok and model_ok:
        print("✅ SETUP COMPLETE - Ready to generate dataset!")
        print("="*60)
        print("\nNext steps:")
        print("1. Add PDF/TXT files to data/raw/")
        print("2. Run: python -m src.dataset_generator")
        return 0
    else:
        print("⚠️  SETUP INCOMPLETE - Fix issues above")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
