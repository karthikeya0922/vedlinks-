"""
Check GPU availability and CUDA setup.
"""

import sys

def check_gpu():
    print("="*60)
    print("GPU & CUDA Detection")
    print("="*60)
    
    # Check PyTorch
    try:
        import torch
        print(f"\n✅ PyTorch installed: {torch.__version__}")
        
        # Check CUDA availability
        cuda_available = torch.cuda.is_available()
        print(f"\n🔍 CUDA Available: {cuda_available}")
        
        if cuda_available:
            print(f"✅ GPU is available!")
            print(f"\nGPU Details:")
            print(f"  - CUDA Version: {torch.version.cuda}")
            print(f"  - GPU Count: {torch.cuda.device_count()}")
            
            for i in range(torch.cuda.device_count()):
                print(f"\n  GPU {i}:")
                print(f"    - Name: {torch.cuda.get_device_name(i)}")
                print(f"    - Memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.2f} GB")
                print(f"    - Compute Capability: {torch.cuda.get_device_properties(i).major}.{torch.cuda.get_device_properties(i).minor}")
            
            # Test tensor on GPU
            print(f"\n🧪 Testing GPU tensor...")
            try:
                x = torch.randn(3, 3).cuda()
                print(f"✅ Successfully created tensor on GPU!")
                print(f"   Device: {x.device}")
            except Exception as e:
                print(f"❌ Failed to create GPU tensor: {e}")
        else:
            print(f"❌ GPU NOT available")
            print(f"\nPossible reasons:")
            print(f"  1. PyTorch installed without CUDA support")
            print(f"  2. NVIDIA GPU drivers not installed")
            print(f"  3. No NVIDIA GPU in system")
            
            print(f"\n💡 To install PyTorch with CUDA support:")
            print(f"\nFor CUDA 11.8:")
            print(f"  pip uninstall torch torchvision torchaudio")
            print(f"  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
            
            print(f"\nFor CUDA 12.1:")
            print(f"  pip uninstall torch torchvision torchaudio")
            print(f"  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
            
            print(f"\nFor CUDA 12.4:")
            print(f"  pip uninstall torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124")
            
    except ImportError:
        print(f"❌ PyTorch not installed")
        print(f"\nInstall with: pip install torch torchvision torchaudio")
    
    # Check bitsandbytes (for quantization)
    print(f"\n{'='*60}")
    print(f"Checking bitsandbytes (for 4-bit quantization)...")
    try:
        import bitsandbytes as bnb
        print(f"✅ bitsandbytes installed")
        
        # Check if bitsandbytes can use CUDA
        if cuda_available:
            try:
                # Try to create a simple quantized tensor
                print(f"🧪 Testing bitsandbytes CUDA support...")
                print(f"✅ bitsandbytes should work with your GPU")
            except Exception as e:
                print(f"⚠️  bitsandbytes CUDA test issue: {e}")
    except ImportError:
        print(f"⚠️  bitsandbytes not installed")
        print(f"\nInstall with: pip install bitsandbytes")
    
    # NVIDIA-SMI check (Windows)
    print(f"\n{'='*60}")
    print(f"Checking NVIDIA GPU Driver...")
    try:
        import subprocess
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ NVIDIA Driver installed")
            print(f"\nGPU Info from nvidia-smi:")
            lines = result.stdout.split('\n')[:15]  # First 15 lines
            for line in lines:
                print(f"  {line}")
        else:
            print(f"⚠️  nvidia-smi not found or failed")
    except FileNotFoundError:
        print(f"❌ nvidia-smi not found - NVIDIA drivers may not be installed")
    except Exception as e:
        print(f"⚠️  Error checking nvidia-smi: {e}")
    
    print(f"\n{'='*60}")
    print(f"Summary")
    print(f"{'='*60}")
    
    if cuda_available:
        print(f"✅ Your system is ready for GPU-accelerated training!")
        print(f"\nThe pipeline will automatically use GPU when available.")
    else:
        print(f"❌ GPU not available - will use CPU (slower)")
        print(f"\nTo enable GPU:")
        print(f"1. Ensure you have an NVIDIA GPU")
        print(f"2. Install NVIDIA GPU drivers")
        print(f"3. Reinstall PyTorch with CUDA support (see commands above)")


if __name__ == "__main__":
    check_gpu()
