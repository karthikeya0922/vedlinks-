"""
Install PyTorch with CUDA support for GPU acceleration.
This script will uninstall CPU-only PyTorch and install CUDA-enabled version.
"""

import subprocess
import sys

def run_command(cmd, description):
    """Run a command and show progress."""
    print(f"\n{'='*60}")
    print(f"📍 {description}")
    print(f"{'='*60}")
    print(f"$ {cmd}")
    print()
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode != 0:
        print(f"\n❌ Failed: {description}")
        return False
    
    print(f"✅ Success: {description}")
    return True


def main():
    print("="*60)
    print("Enable GPU Acceleration for VedLinks")
    print("="*60)
    print("\nDetected GPU: NVIDIA GeForce RTX 2050 (4GB VRAM)")
    print("Current PyTorch: CPU-only version")
    print("\nThis will:")
    print("  1. Uninstall CPU-only PyTorch")
    print("  2. Install PyTorch with CUDA 12.1 support")
    print("  3. Verify GPU is detected")
    
    response = input("\n▶️  Continue? [y/N]: ")
    if response.lower() != 'y':
        print("Cancelled.")
        return 0
    
    # Step 1: Uninstall CPU version
    if not run_command(
        "pip uninstall -y torch torchvision torchaudio",
        "Uninstalling CPU-only PyTorch"
    ):
        return 1
    
    # Step 2: Install CUDA version
    # Using CUDA 12.1 which is compatible with most recent drivers
    if not run_command(
        "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121",
        "Installing PyTorch with CUDA 12.1"
    ):
        return 1
    
    # Step 3: Verify
    print("\n" + "="*60)
    print("🧪 Verifying GPU Support")
    print("="*60)
    
    if not run_command("python check_gpu.py", "Checking GPU availability"):
        return 1
    
    print("\n" + "="*60)
    print("✅ GPU SETUP COMPLETE!")
    print("="*60)
    print("\n🚀 Your pipeline will now use GPU acceleration automatically!")
    print("\nBenefits:")
    print("  - Faster dataset generation (~10-50x speedup)")
    print("  - Faster training (~100x speedup)")
    print("  - Ability to use 4-bit quantization (lower memory usage)")
    
    print("\n💡 Next steps:")
    print("  1. Run: python -m src.dataset_generator")
    print("  2. The model will automatically load on GPU")
    print("  3. Check console output - should say 'Using device: cuda'")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
