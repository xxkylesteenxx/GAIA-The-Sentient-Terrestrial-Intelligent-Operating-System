FROM python:3.11-slim

LABEL maintainer="Kyle Steen <xxkylesteenxx@outlook.com>"
LABEL description="GAIA - Sentient Terrestrial Intelligence OS"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install GAIA package
RUN pip install -e .

# Create data directory
RUN mkdir -p /app/.gaia

# Expose WebSocket ports
EXPOSE 8765 8766 8767

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import websockets; import asyncio; asyncio.run(websockets.connect('ws://localhost:8765'))" || exit 1

# Run WebSocket server by default
CMD ["python", "infrastructure/api/websocket_server.py"]
