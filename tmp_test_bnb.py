import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import time
import logging

logging.basicConfig(level=logging.INFO)

print('starting')
MODEL_NAME = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
print('Loading tokenizer')
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
print('Configuring bnb')
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)
print('Loading model onto GPU with bnb')
start = time.time()
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map='auto',
)
print(f'Model loaded in {time.time() - start:.2f} seconds')
