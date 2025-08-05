# Use small Python base image
FROM python:3.10-slim

# Prevents Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies and clean up
RUN apt-get update && \
    apt-get install -y qpdf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python packages first (leverage Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . .

# Expose port (Render will set $PORT, no need to expose manually)
# EXPOSE is not needed on Render, but harmless if you want:
# EXPOSE 5000  

# Run the Flask app
CMD ["python", "app.py"]
