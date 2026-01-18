"""
Test script to verify the trained model can be loaded and used for inference.
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig

def test_trained_model():
    """Load and test the fine-tuned model."""
    model_path = "output/qlora_tuned_model"
    
    print("="*60)
    print("Testing Trained VedLinks Model")
    print("="*60)
    
    # Load tokenizer
    print(f"\n🔤 Loading tokenizer from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    print("✅ Tokenizer loaded")
    
    # Load base model and adapter
    print(f"\n🤖 Loading model...")
    try:
        # First, load the PEFT config to get the base model name
        config = PeftConfig.from_pretrained(model_path)
        base_model_name = config.base_model_name_or_path
        
        print(f"   Base model: {base_model_name}")
        
        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        
        # Load PEFT adapter
        model = PeftModel.from_pretrained(base_model, model_path)
        print("✅ Model loaded with LoRA adapter")
        
    except Exception as e:
        print(f"⚠️  PEFT loading failed: {e}")
        print("   Trying direct load...")
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        print("✅ Model loaded")
    
    # Test prompt
    test_prompt = """Generate educational content based on NCERT-style learning materials.

Create:
1. Student Q&A pairs that help understand the topic
2. Multiple choice questions with explanations
3. Teacher summary of key concepts

### Teacher Summary:
Water is essential for all living organisms and exists in three states: solid, liquid, and gas.

"""
    
    print(f"\n🧪 Testing inference...")
    print(f"\nPrompt:\n{test_prompt[:100]}...\n")
    
    # Tokenize
    inputs = tokenizer(test_prompt, return_tensors="pt")
    
    # Generate
    print("Generating response...")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract just the completion (remove prompt)
    completion = generated_text[len(test_prompt):].strip()
    
    print(f"\n📝 Generated Output:\n")
    print("="*60)
    print(completion)
    print("="*60)
    
    print("\n✅ Model test complete!")
    print(f"\nModel is ready to use. Load it with:")
    print(f"  from peft import PeftModel, PeftConfig")
    print(f"  config = PeftConfig.from_pretrained('{model_path}')")
    print(f"  base_model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path)")
    print(f"  model = PeftModel.from_pretrained(base_model, '{model_path}')")


if __name__ == "__main__":
    try:
        test_trained_model()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
