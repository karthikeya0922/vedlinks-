import os
import sys
import time
import json
import urllib.request
from datetime import datetime

# URL of the VedLinks API
STATUS_URL = "http://127.0.0.1:5000/api/training-status"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_progress_bar(progress, width=40):
    filled = int(width * progress / 100)
    bar = "█" * filled + "▒" * (width - filled)
    return f"|{bar}| {progress:.1f}%"

def parse_training_stats(logs):
    """Extract latest stats from logs."""
    stats = {"epoch": "N/A", "step": "N/A", "loss": "N/A"}
    for line in reversed(logs):
        if "PROGRESS_UPDATE" in line:
            # Format: PROGRESS_UPDATE | Epoch: 1.23 | Step: 100 | Loss: 0.85
            try:
                parts = line.split('|')
                for part in parts:
                    if "Epoch:" in part:
                        stats["epoch"] = part.split(':')[1].strip()
                    elif "Step:" in part:
                        stats["step"] = part.split(':')[1].strip()
                    elif "Loss:" in part:
                        stats["loss"] = part.split(':')[1].strip()
                break # Found the latest update
            except:
                continue
    return stats

def monitor():
    print("Connecting to VedLinks AI Server...")
    
    last_processed_log_count = 0
    
    while True:
        try:
            with urllib.request.urlopen(STATUS_URL, timeout=5) as response:
                data = json.loads(response.read().decode())
            
            clear_screen()
            
            print("=" * 60)
            print(" 🤖 VedLinks AI Fine-Tuning Monitor")
            print("=" * 60)
            
            is_training = data.get("is_training", False)
            step = data.get("current_step", "unknown")
            progress = data.get("progress", 0)
            start_time = data.get("start_time", "N/A")
            logs = data.get("logs", [])
            
            # Status Header
            status_text = "🟢 ACTIVE" if is_training else "⚪ IDLE"
            if step == "completed": status_text = "✅ COMPLETED"
            if step == "failed": status_text = "❌ FAILED"
            
            print(f" Status:  {status_text}")
            print(f" Step:    {step.replace('_', ' ').title()}")
            print(f" Progress: {format_progress_bar(progress)}")
            print(f" Started:  {start_time}")
            print("-" * 60)
            
            # Training Specific Stats
            if step == "training_model" or step == "completed":
                stats = parse_training_stats(logs)
                print(f" Current Epoch: {stats['epoch']}")
                print(f" Current Step:  {stats['step']}")
                print(f" Current Loss:  {stats['loss']}")
                print("-" * 60)
            
            # Latest Logs
            print(" Recent Logs:")
            for log in logs[-8:]:
                # Clean up annoying repetitive markers for display
                display_log = log.split('|')[-1].strip() if "PROGRESS_UPDATE" in log else log
                print(f"  > {display_log}")
                
            if not is_training and step not in ["generating_data", "training_model"]:
                print("\n [!] No active training detected.")
                print("     Start training from the Web Dashboard or API.")
            
            print("-" * 60)
            print(f" (Auto-updating every 3 seconds - Press Ctrl+C to exit)")
            print(f" Last Sync: {datetime.now().strftime('%H:%M:%S')}")

        except Exception as e:
            clear_screen()
            print("=" * 60)
            print(" ⚠️ VedLinks Connection Error")
            print("=" * 60)
            print(f" Error: Could not connect to the local server at {STATUS_URL}")
            print(" Make sure 'python app.py' is running in another terminal.")
            print("-" * 60)
            print(f" Retrying in 5 seconds... (Press Ctrl+C to exit)")
            time.sleep(5)
            continue

        time.sleep(3)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\n\n Monitor stopped.")
        sys.exit(0)
