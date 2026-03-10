FROM python:3.10-slim

# Set working dir
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements_hf.txt .
RUN pip install --no-cache-dir -r requirements_hf.txt

# Copy the full application
COPY app.py .
COPY question_paper_generator.py .
COPY src/ src/
COPY data/ data/
COPY output/ output/
COPY templates/ templates/
COPY static/ static/

# HF Spaces expects port 7860
EXPOSE 7860

# Start the Flask app
CMD ["python", "app.py"]
