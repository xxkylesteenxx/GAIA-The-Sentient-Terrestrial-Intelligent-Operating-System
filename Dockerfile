FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install GAIA package
RUN pip install -e .

# Create data and log directories
RUN mkdir -p /app/data /app/logs

# Expose ports
EXPOSE 8765 8766

# Run WebSocket server
CMD ["python", "-m", "infrastructure.api.websocket_server"]
