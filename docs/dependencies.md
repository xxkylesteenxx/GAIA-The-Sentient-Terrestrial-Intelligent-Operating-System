# GAIA Dependencies

Comprehensive documentation of all GAIA dependencies with rationale.

## Quick Start

```bash
# Production deployment
pip install -r requirements.txt

# Development environment
pip install -r requirements.txt -r requirements-dev.txt

# Verify installation
python -c "import core; import overlay; import bridge; print('GAIA dependencies OK')"
```

## Version Requirements

- **Python**: ≥ 3.11 (required for `|` type unions, `dataclass` improvements)
- **pip**: ≥ 23.0 (for modern dependency resolution)

---

## Core Plane Dependencies

### Scientific Computing

#### `numpy>=1.24.0`
**Purpose**: Array operations, biosignal processing, Z-score calculation  
**Used by**: `core/zscore/calculator.py`  
**Why this version**: 1.24.0+ required for NumPy 2.0 compatibility path

#### `scipy>=1.10.0`
**Purpose**: Shannon entropy, Lyapunov exponent, signal processing  
**Used by**: `core/zscore/calculator.py`, biosignal analyzers  
**Why this version**: 1.10.0+ includes performance improvements for entropy calculations

---

## Bridge Plane Dependencies

### Real-time Communication

#### `websockets>=12.0`
**Purpose**: Three-port WebSocket architecture (Core/Bridge/Overlay)  
**Used by**: `infrastructure/api/websocket_server.py`  
**Why this version**: 12.0+ modern API, security patches  
**Ports**:
- Core: 8765 (Z-score, crisis events)
- Bridge: 8766 (alchemical transitions)
- Overlay: 8767 (Avatar speech, UI updates)

#### `aiohttp>=3.9.0`
**Purpose**: Async HTTP client for external APIs  
**Used by**: Avatar LLM calls, future federation protocol  
**Why this version**: 3.9.0+ security patches, modern SSL

#### `fastapi>=0.100.0` (Phase 2)
**Purpose**: REST API framework (OpenAPI/Swagger auto-docs)  
**Used by**: Planned REST API alongside WebSocket  
**Why this version**: 0.100.0+ Pydantic 2.0 compatibility

#### `uvicorn>=0.22.0` (Phase 2)
**Purpose**: ASGI server for FastAPI  
**Used by**: Production REST API deployment  
**Why this version**: 0.22.0+ WebSocket support, graceful shutdown

---

## Overlay Plane Dependencies

### Avatar LLM Integration

#### `anthropic>=0.20.0`
**Purpose**: Claude API for Avatar personality  
**Used by**: `overlay/avatar/personality.py`  
**Why this version**: 0.20.0+ streaming API, modern SDK  
**Note**: **CORRECT package name** (was incorrectly `anthropicsdk` in audit)

#### `openai>=1.0.0` (Optional)
**Purpose**: GPT-4 API for Avatar personality (alternative to Claude)  
**Used by**: `overlay/avatar/personality.py`  
**Why this version**: 1.0.0+ modern SDK rewrite  
**Note**: Only ONE LLM provider is required (user choice)

### Semantic Memory

#### `chromadb>=0.4.22`
**Purpose**: Vector database for Avatar memory (episodic/semantic/emotional)  
**Used by**: `overlay/avatar/memory.py`  
**Why this version**: 0.4.22+ modern `PersistentClient` API (old API removed)  
**API change**: Use `chromadb.PersistentClient(path=...)` not deprecated `Client(Settings(...))`

#### `sentence-transformers>=2.2.0`
**Purpose**: Sentence embeddings for semantic memory recall  
**Used by**: ChromaDB automatic embedding generation  
**Why this version**: 2.2.0+ improved model compatibility

### Astrological Engine

#### `kerykeion>=4.0.0`
**Purpose**: High-level natal chart calculation API  
**Used by**: `overlay/astrology/` (archetypal mapping)  
**Why this version**: 4.0.0+ modern Pythonic API

#### `pyswisseph>=2.10.3`
**Purpose**: Swiss Ephemeris low-level calculations  
**Used by**: kerykeion backend  
**Why this version**: 2.10.3+ bugfixes for edge-case charts  
**Note**: **CORRECT package name** (was incorrectly `swisseph` in audit)

---

## Security & Configuration

#### `cryptography>=41.0.0`
**Purpose**: Memory encryption, consent protocol signatures  
**Used by**: `overlay/avatar/memory.py` (Phase 2 encryption)  
**Why this version**: 41.0.0+ modern OpenSSL bindings

#### `pyyaml>=6.0.0`
**Purpose**: Configuration file parsing (config.yaml)  
**Used by**: System configuration, settings management  
**Why this version**: 6.0.0+ safer YAML loading

#### `python-dotenv>=1.0.0`
**Purpose**: Environment variable management (.env files)  
**Used by**: API keys, secrets, configuration  
**Why this version**: 1.0.0+ stable release

#### `pydantic>=2.0.0`
**Purpose**: Data validation, settings management, type safety  
**Used by**: FastAPI models, configuration validation  
**Why this version**: 2.0.0+ performance improvements, better error messages

---

## CLI & User Interface

#### `click>=8.1.0`
**Purpose**: CLI framework (command-line argument parsing)  
**Used by**: `overlay/cli.py`  
**Why this version**: 8.1.0+ modern parameter types  
**Note**: Was **MISSING** in original audit

#### `rich>=13.0.0`
**Purpose**: Terminal UI (colored output, tables, progress bars)  
**Used by**: CLI status display, formatted output  
**Why this version**: 13.0.0+ table improvements  
**Note**: Was **MISSING** in original audit

---

## Development Dependencies

Install via: `pip install -r requirements-dev.txt`

### Testing Framework

#### `pytest>=7.4.0`
**Purpose**: Test framework  
**Used by**: All unit tests, integration tests  
**Why this version**: 7.4.0+ modern fixture API

#### `pytest-asyncio>=0.21.0`
**Purpose**: Async test support  
**Used by**: WebSocket tests, async function tests  
**Why this version**: 0.21.0+ stable async scope

#### `pytest-cov>=4.1.0`
**Purpose**: Coverage reporting  
**Used by**: CI/CD codecov integration  
**Why this version**: 4.1.0+ branch coverage

### Code Quality Tools

#### `black~=23.0`
**Purpose**: Code formatter (PEP 8 compliant)  
**Used by**: CI/CD linting step  
**Why this version**: ~= pins major version for team consistency  
**Config**: `pyproject.toml` (line-length=100)

#### `flake8~=6.0`
**Purpose**: Linter, style checker  
**Used by**: CI/CD code quality checks  
**Why this version**: ~= pins major version for team consistency

#### `mypy~=1.5`
**Purpose**: Static type checker  
**Used by**: CI/CD type safety verification  
**Why this version**: ~= pins major version for team consistency

### Development Utilities

#### `ipython>=8.10.0`
**Purpose**: Enhanced Python REPL (interactive development)  
**Why this version**: 8.10.0+ modern completion

#### `ipdb>=0.13.0`
**Purpose**: IPython debugger (better than pdb)  
**Usage**: `breakpoint()` drops into ipdb REPL  
**Why this version**: 0.13.0+ stable release

---

## Version Constraint Rationale

### `>=` (Greater than or equal)
Used for: **Production libraries**  
Reason: Allow security patches and bugfixes  
Example: `numpy>=1.24.0`

### `~=` (Approximately equal / Compatible release)
Used for: **Development tools**  
Reason: Pin major version for team consistency  
Example: `black~=23.0` allows 23.x, blocks 24.0

### `==` (Exact version)
Used for: **Never** (prevents security updates)  
Reason: Too restrictive, blocks patches

---

## Common Installation Issues

### Issue: `anthropicsdk` not found
**Error**: `ERROR: Could not find a version that satisfies the requirement anthropicsdk`  
**Fix**: The correct package name is `anthropic` (no "sdk" suffix)  
**Resolution**: Use `anthropic>=0.20.0` in requirements.txt

### Issue: `swisseph` not found
**Error**: `ERROR: Could not find a version that satisfies the requirement swisseph`  
**Fix**: The correct package name is `pyswisseph` ("py" prefix)  
**Resolution**: Use `pyswisseph>=2.10.3` in requirements.txt

### Issue: ChromaDB TypeError on import
**Error**: `TypeError: Client() got an unexpected keyword argument 'chroma_db_impl'`  
**Fix**: The old API was removed in ChromaDB 0.4.0  
**Resolution**: Use modern API:
```python
# OLD (deprecated)
import chromadb
from chromadb.config import Settings
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", ...))

# NEW (correct)
import chromadb
client = chromadb.PersistentClient(path="./data/chroma")
```

### Issue: NumPy compatibility warnings
**Warning**: `numpy.dtype size changed, may indicate binary incompatibility`  
**Fix**: Upgrade NumPy to 1.24.0+  
**Resolution**: `pip install --upgrade numpy>=1.24.0`

### Issue: M1 Mac installation failures
**Error**: `ERROR: Failed building wheel for pyswisseph`  
**Fix**: Install Rosetta 2 or use conda  
**Resolution**:
```bash
# Option 1: Rosetta 2
softwareupdate --install-rosetta

# Option 2: Conda (native ARM64)
conda create -n gaia python=3.11
conda activate gaia
conda install numpy scipy
pip install -r requirements.txt
```

### Issue: Windows cryptography build failures
**Error**: `error: Microsoft Visual C++ 14.0 or greater is required`  
**Fix**: Install Visual C++ Build Tools  
**Resolution**: Download from https://visualstudio.microsoft.com/visual-cpp-build-tools/

---

## CI/CD Integration

GitHub Actions (`.github/workflows/ci.yml`) automatically:
1. Installs both `requirements.txt` and `requirements-dev.txt`
2. Runs pytest with coverage reporting
3. Uploads coverage to Codecov
4. Runs flake8 linting
5. Runs mypy type checking

All actions updated to `@v4` (Node.js 20) as of Issue #9 resolution.

---

## Dependency Audit History

### 2026-02-28 (Issue #8 Resolution)
**Fixed**:
- `anthropicsdk` → `anthropic` (correct PyPI name)
- `swisseph` → `pyswisseph` (correct PyPI name)
- Added missing: `click>=8.1.0`, `rich>=13.0.0`

**Added**:
- `sentence-transformers>=2.2.0` (semantic memory)
- `fastapi>=0.100.0` (Phase 2 REST API)
- `uvicorn>=0.22.0` (ASGI server)
- `pydantic>=2.0.0` (data validation)

**Updated**:
- `websockets` 11.0 → 12.0 (security)
- `aiohttp` 3.8.0 → 3.9.0 (security)
- `anthropic` 0.18.0 → 0.20.0 (latest API)
- `pyswisseph` 2.10.0 → 2.10.3 (bugfixes)

---

## Maintenance

### Updating Dependencies
```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Regenerate lockfile (if using pip-tools)
pip-compile requirements.in
```

### Security Audits
```bash
# Check for known vulnerabilities
pip-audit

# Or use safety
safety check -r requirements.txt
```

### Testing Dependency Changes
```bash
# Create clean test environment
python -m venv test-env
source test-env/bin/activate
pip install -r requirements.txt
pytest tests/
```

---

## References

- **PyPI Package Index**: https://pypi.org/
- **Python Packaging Guide**: https://packaging.python.org/
- **Semantic Versioning**: https://semver.org/
- **PEP 440 (Version Specifiers)**: https://peps.python.org/pep-0440/

---

**Last updated**: 2026-02-28  
**Audit status**: ✅ All dependencies verified and documented  
**Next review**: Phase 2 kickoff (Q2 2026)
