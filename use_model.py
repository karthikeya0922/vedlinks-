"""
Demo script to use the fine-tuned model for generating educational content.
"""

import os
import sys
import warnings
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Suppress warnings
warnings.filterwarnings('ignore')

# Fix encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def load_model(model_path="output/qlora_tuned_model"):
    """Load the fine-tuned LoRA model."""
    print("="*60)
    print("Loading Fine-Tuned Model")
    print("="*60)
    
    print(f"\n📁 Model path: {model_path}")
    
    # Check device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🎮 Device: {device}")
    
    # Load tokenizer
    print("\n🔤 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    print("✅ Tokenizer loaded")
    
    # Load base model
    print("\n🤖 Loading base model...")
    base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Your base model
    
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )
    
    # Load LoRA adapter
    print("🔧 Loading LoRA adapter...")
    model = PeftModel.from_pretrained(base_model, model_path)
    
    # Move to device
    if device == "cuda":
        model = model.to(device)
    
    model.eval()  # Set to evaluation mode
    
    print("✅ Model ready!\n")
    
    return model, tokenizer, device


def generate_educational_content(model, tokenizer, device, topic_text, max_length=512):
    """
    Generate educational content for a given topic/passage.
    
    Args:
        model: The fine-tuned model
        tokenizer: Tokenizer
        device: Device (cuda/cpu)
        topic_text: The educational passage/topic
        max_length: Maximum tokens to generate
    
    Returns:
        Generated educational content
    """
    # Build prompt (same format as training)
    prompt = f"""Generate educational content based on NCERT-style learning materials.

Create:
1. Student Q&A pairs that help understand the topic
2. Multiple choice questions with explanations
3. Teacher summary of key concepts

### Teacher Summary:
{topic_text}

"""
    
    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt")
    
    if device == "cuda":
        inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Generate
    print("🔮 Generating content...")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_length,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    
    # Decode
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract just the completion (remove prompt)
    completion = generated_text[len(prompt):].strip()
    
    return completion


def main():
    """Main demo function."""
    print("\n" + "="*60)
    print("VedLinks Educational Content Generator - Demo")
    print("="*60)
    
    # Load model
    model, tokenizer, device = load_model()
    
    # Example 1: Generate content for a science topic
    print("\n" + "="*60)
    print("Example 1: Generating content about Water Cycle")
    print("="*60)
    
    topic1 = """The water cycle describes how water evaporates from the surface of the earth, 
rises into the atmosphere, cools and condenses into clouds, and falls back to the 
surface as precipitation. The water that falls to Earth as precipitation either 
evaporates, is taken up by plants, or becomes groundwater."""
    
    print(f"\n📖 Topic:\n{topic1}\n")
    
    result1 = generate_educational_content(model, tokenizer, device, topic1)
    
    print(f"\n📝 Generated Content:\n")
    print("="*60)
    print(result1)
    print("="*60)
    
    # Example 2: Interactive mode
    print("\n\n" + "="*60)
    print("Interactive Mode")
    print("="*60)
    print("\nEnter your own topic/passage (or press Enter to skip):")
    print("(Tip: Paste a paragraph from an NCERT textbook)")
    print()
    
    user_input = input("Your topic: ").strip()
    
    if user_input:
        print(f"\n🔮 Generating content for your topic...")
        result = generate_educational_content(model, tokenizer, device, user_input)
        
        print(f"\n📝 Generated Content:\n")
        print("="*60)
        print(result)
        print("="*60)
    else:
        print("Skipped interactive mode.")
    
    print("\n" + "="*60)
    print("✅ Demo Complete!")
    print("="*60)
    print("\n💡 To use this model in your own code:")
    print("   1. Load with: model, tokenizer, device = load_model()")
    print("   2. Generate with: generate_educational_content(model, tokenizer, device, topic)")
    print("   3. Model is at: output/qlora_tuned_model/")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
