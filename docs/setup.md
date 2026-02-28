# GAIA Setup Guide

## Quick Start

### Prerequisites
- Python 3.11 or higher
- Node.js 18+ (for Electron desktop)
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System.git
cd GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System

# Install Python dependencies
make install

# Or manually:
pip install -r requirements.txt
pip install -e .
```

### Running Tests

```bash
# Run full test suite
make test

# Or with pytest directly:
pytest tests/ -v
```

### Starting the Server

```bash
# Start WebSocket server
make run-server

# Or manually:
python infrastructure/api/websocket_server.py
```

The server will start three WebSocket endpoints:
- **Core Plane**: `ws://localhost:8765` - Z-score, crisis detection
- **Bridge Plane**: `ws://localhost:8766` - Hypothesis testing
- **Overlay Plane**: `ws://localhost:8767` - Avatar, meaning-making

### Desktop Application

```bash
# Install Electron dependencies
cd web/desktop
npm install

# Start desktop app
npm start
```

## Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key settings:
- `GAIA_USER_ID`: Your username
- `GAIA_CRISIS_THRESHOLD`: Z-score crisis threshold (default: 2.0)
- `GAIA_MEMORY_DIR`: Where to store memories

## Docker Deployment

```bash
# Build and run with Docker Compose
make docker-build
make docker-run

# Or manually:
docker-compose up -d
```

## Development Mode

```bash
# Install dev dependencies
make install-dev

# Run in development mode (server + desktop)
make dev
```

## Testing Components

### Z-Score Calculator
```bash
python core/zscore/calculator.py
```

### Crisis Detector
```bash
python core/safety/crisis_detector.py
```

### Equilibrium Tracker
```bash
python overlay/equilibrium/tracker.py
```

### Avatar Memory
```bash
python overlay/avatar/memory.py
```

## Troubleshooting

### WebSocket Connection Fails
- Check if ports 8765-8767 are available
- Verify firewall settings
- Ensure server is running: `ps aux | grep websocket_server`

### Import Errors
- Reinstall: `pip install -e .`
- Check Python version: `python --version` (needs 3.11+)

### ChromaDB Issues
- Install manually: `pip install chromadb`
- Falls back to simple storage if unavailable

### Tests Failing
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Clear cache: `make clean`

## Next Steps

- Read [Architecture Documentation](architecture.md)
- Explore [API Specification](api.md)
- Review [Phase 1 Roadmap](../README.md#roadmap)

## Support

- Issues: https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/issues
- Discussions: https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/discussions
