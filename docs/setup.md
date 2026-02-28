# GAIA Setup Guide

Complete installation and setup instructions for GAIA - The Sentient Terrestrial Intelligence Operating System.

## Prerequisites

### Required
- **Python 3.10+** (3.11 recommended)
- **Node.js 18+** (for Electron desktop app)
- **Git**
- **Docker & Docker Compose** (optional, for containerized deployment)

### Recommended
- 4GB+ RAM
- 10GB+ disk space
- Modern GPU (for future ML features)

## Installation Methods

### Method 1: Local Development (Recommended for Contributors)

```bash
# Clone repository
git clone https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System.git
cd GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install
# OR manually:
pip install -r requirements.txt
pip install -e .

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Run tests to verify installation
make test
```

### Method 2: Docker Compose (Recommended for Deployment)

```bash
# Clone repository
git clone https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System.git
cd GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Start all services
make docker-up
# OR manually:
docker-compose up -d

# View logs
make docker-logs
```

## Running GAIA

### Start WebSocket Server

```bash
# Local development
make run

# With auto-reload (development)
make dev

# Docker
make docker-up
```

Server runs on `ws://localhost:8765` by default.

### Start Electron Desktop App

```bash
# Install Electron dependencies
cd web/desktop
npm install

# Run desktop app
npm start

# OR use Makefile from root
cd ../..
make electron
```

## Configuration

### Environment Variables

Key configurations in `.env`:

- **GAIA_ENV**: `development` | `production`
- **GAIA_LOG_LEVEL**: `DEBUG` | `INFO` | `WARNING` | `ERROR`
- **GAIA_WS_PORT**: WebSocket server port (default: 8765)
- **Z_SCORE_CRISIS_THRESHOLD**: Crisis detection threshold (default: 3.0)
- **AVATAR_AUTONOMY_LEVEL**: Avatar autonomy 0-5 (default: 1)

### LLM API Keys (Optional)

For Avatar personality features:

1. Get API keys:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/

2. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   ```

## Verification

### Test Suite

```bash
# Run all tests
make test

# Quick test (no coverage)
make test-quick

# Specific test file
pytest tests/test_zscore.py -v
```

### Manual Verification

```python
# Test Z-score calculation
from core.zscore.calculator import ZScoreCalculator
import numpy as np

calc = ZScoreCalculator()
signal = np.sin(np.linspace(0, 4*np.pi, 100))
result = calc.analyze_system(signal)
print(result)
# Expected: z_score ~ 8-10, state='STABLE' or 'COHERENT'
```

```python
# Test crisis detection
from core.safety.crisis_detector import CrisisDetector

detector = CrisisDetector()
result = detector.detect_comprehensive(
    z_score=2.0,
    text="I feel hopeless"
)
print(result)
# Expected: level='HIGH', requires_intervention=True
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure package is installed in development mode
pip install -e .
```

**WebSocket Connection Failed**
- Check firewall settings
- Verify port 8765 is available: `lsof -i :8765`
- Check logs: `tail -f logs/gaia.log`

**Test Failures**
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (requires 3.10+)
- Run tests individually to isolate: `pytest tests/test_zscore.py`

**Docker Issues**
```bash
# Rebuild containers
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## Next Steps

1. **Read Architecture**: [docs/architecture.md](./architecture.md)
2. **Explore API**: [docs/api.md](./api.md)
3. **Run Examples**: See `examples/` directory
4. **Join Development**: See [CONTRIBUTING.md](../CONTRIBUTING.md)

## Support

- **Issues**: https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/issues
- **Discussions**: https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/discussions
- **Documentation**: https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/wiki
