"""
VedLinks Server Runner
======================
Simple command to start the VedLinks server.

Usage:
    python run.py           - Start server on default port 5000
    python run.py --port 8080  - Start on custom port
"""

import sys
import os

# Fix encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    port = 5000
    
    # Parse arguments
    if '--port' in sys.argv:
        try:
            idx = sys.argv.index('--port')
            port = int(sys.argv[idx + 1])
        except (ValueError, IndexError):
            print("Invalid port. Using default 5000")
    
    print("=" * 60)
    print("       VedLinks AI Educational Content Generator")
    print("=" * 60)
    print(f"\n🚀 Starting server at http://127.0.0.1:{port}")
    print("\n📖 Available Pages:")
    print(f"   • Question Paper Generator: http://127.0.0.1:{port}/")
    print(f"   • Practice & Doubts:        http://127.0.0.1:{port}/practice")
    print("\n📡 API Endpoints:")
    print(f"   • GET  /api/topics          - List all topics")
    print(f"   • POST /api/generate-paper  - Generate question paper")
    print(f"   • POST /api/export-docx     - Export to Word document")
    print(f"   • POST /api/practice-questions - Get practice questions")
    print(f"   • POST /api/concepts        - Get key concepts")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    # Import and run Flask app
    from app import app
    app.run(debug=True, host='127.0.0.1', port=port)


if __name__ == "__main__":
    main()
