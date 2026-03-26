# Project Requirements

This document outlines the dependencies required to run the full VedLinks application locally, including the AI model training and dynamic question generation pipelines.

## Automatic Installation

To install everything needed for the full backend, run:

```bash
pip install -r requirements.local.txt
```

*(If `requirements.local.txt` doesn't exist, manually install the packages below)*

## Core Dependencies

### Web Server & Backend

```text
flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
requests==2.31.0
```

### File Processing & Data

```text
PyPDF2==3.0.1
pdfplumber==0.10.3
numpy>=1.26.0
pandas>=2.1.0
python-docx==1.1.0
```

### AI & Machine Learning Pipeline

To run the local QLoRA fine-tuning and the `transformers` models, you need the following PyTorch/HF stack:

```text
torch>=2.0.0
transformers>=4.38.0
peft>=0.9.0
trl>=0.7.11
datasets>=2.18.0
accelerate>=0.27.2
```

### Optional (For CUDA/GPU Training)

If you have an NVIDIA GPU and want to use 4-bit quantization to speed up training, install:

```text
bitsandbytes>=0.41.0
```

*Note: The training pipeline is designed to gracefully fall back to standard `float16` and `adamw_torch` if `bitsandbytes` is not installed or not compatible with your OS (e.g., native Windows).*
