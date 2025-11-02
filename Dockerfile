FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (no cache to reduce size)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for models (will be mounted as volume)
RUN mkdir -p /app/models

# Make startup script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 5000

# Use startup script that handles model installation
CMD ["./start.sh"]

