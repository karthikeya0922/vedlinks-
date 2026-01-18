---
description: How to run and train VedLinks
---

# VedLinks Commands

## Start the Server
```powershell
// turbo
python run.py
```
Access at: http://127.0.0.1:5000

## Training Pipeline

### Generate Training Dataset
```powershell
python train_pipeline.py generate
```
Creates training samples from knowledge bank → `data/finetune_dataset.jsonl`

### Train Model with LoRA
```powershell
python train_pipeline.py train
```
Requires dataset to exist. Outputs to `output/qlora_tuned_model/`

### Run Complete Pipeline
```powershell
python train_pipeline.py all
```
Generates dataset + trains model in one command.

## Custom Port
```powershell
python run.py --port 8080
```
