# Use slim Python base image
FROM python:3.10-slim

# Install qpdf
RUN apt-get update && apt-get install -y qpdf

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (use same as in app.py if specified)
EXPOSE 10000

# Start Flask app
CMD ["python", "app.py"]
