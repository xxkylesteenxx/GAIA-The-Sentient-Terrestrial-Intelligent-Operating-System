# Developer Quickstart Guide

Get up and running with GAIA development in under 15 minutes.

## Prerequisites

- **Python**: >=3.11 (check: `python --version`)
- **Git**: Latest version (check: `git --version`)
- **Optional**: Docker (for integration tests), VS Code (recommended IDE)

## 1. Environment Setup

### Clone Repository

```bash
git clone https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System.git
cd GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System
```

### Create Virtual Environment

```bash
# Create venv
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

### Install Dependencies

```bash
# Install production + development dependencies
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

# Install GAIA in editable mode
pip install -e .
```

### Verify Installation

```bash
# Check imports work
python -c "import core; import overlay; import bridge; print('✅ GAIA dependencies OK')"

# Check tools installed
ruff --version
black --version
mypy --version
pytest --version
mkdocs --version
```

Expected output:
```
✅ GAIA dependencies OK
ruff 0.1.15
black, 23.12.1
mypy 1.8.0
pytest 7.4.3
mkdocs, version 1.5.3
```

## 2. Install Pre-commit Hooks

Pre-commit hooks automatically run code quality checks before each commit.

```bash
# Install hooks (one-time setup)
pre-commit install

# Test hooks manually
pre-commit run --all-files
```

What gets checked:
1. **Ruff** - Linting (errors, style, imports)
2. **Black** - Code formatting (auto-fix)
3. **Mypy** - Type checking (core modules)
4. **Pytest** - Fast unit tests
5. **Standard checks** - Trailing whitespace, YAML syntax, etc.

## 3. Development Workflow

### Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### Make Changes

Edit code, add tests, update docs.

### Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_zscore.py

# Run with coverage
pytest --cov=core --cov=overlay --cov-report=html

# Skip slow tests (integration)
pytest -m "not slow"
```

### Commit Changes

```bash
git add .
git commit -m "feat: add your feature"

# Pre-commit hooks run automatically!
# If checks fail, fix issues and commit again
```

### Push and Create PR

```bash
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# CI/CD will run automatically
```

## 4. Testing

### Test Structure

```
tests/
├── core/
│   ├── test_zscore.py
│   └── test_crisis_detector.py
├── overlay/
│   ├── test_avatar_personality.py
│   └── test_avatar_memory.py
└── integration/
    └── test_websocket_server.py
```

### Run Tests

```bash
# All tests
pytest

# Specific module
pytest tests/core/

# Specific test
pytest tests/core/test_zscore.py::TestZScoreCalculator::test_calculate

# With markers
pytest -m unit         # Fast unit tests only
pytest -m integration  # Integration tests only
pytest -m "not slow"   # Skip slow tests

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=core --cov=overlay --cov-report=html

# Open in browser
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## 5. Code Quality

### Linting (Ruff)

```bash
# Check for issues
ruff check core/ overlay/ bridge/

# Auto-fix simple issues
ruff check --fix core/ overlay/ bridge/

# Check specific file
ruff check core/zscore/calculator.py
```

### Formatting (Black)

```bash
# Format all code
black core/ overlay/ bridge/

# Check formatting (no changes)
black --check core/ overlay/ bridge/

# Format specific file
black core/zscore/calculator.py
```

### Type Checking (Mypy)

```bash
# Check types
mypy core/ overlay/ bridge/

# Check specific module
mypy core/zscore/

# Strict mode (core only)
mypy --strict core/
```

### Run All Quality Checks

```bash
pre-commit run --all-files
```

## 6. Documentation

### Serve Docs Locally

```bash
# Start local server (hot reload)
mkdocs serve

# Open browser to: http://127.0.0.1:8000/
```

### Build Docs

```bash
# Build static site
mkdocs build

# Output: site/ directory
```

### Deploy Docs

```bash
# Deploy to GitHub Pages (main branch only)
mkdocs gh-deploy

# URL: https://xxkylesteenxx.github.io/GAIA.../
```

### Add New Page

1. Create Markdown file in `docs/`
2. Add to `mkdocs.yml` navigation
3. Commit and push (auto-deploys)

## 7. Common Tasks

### Add New Dependency

```bash
# Production dependency
echo "new-package>=1.0.0" >> requirements.txt

# Development dependency
echo "new-dev-tool>=1.0.0" >> requirements-dev.txt

# Install
pip install -r requirements.txt -r requirements-dev.txt

# Document in docs/dependencies.md
```

### Add New Test

```python
# tests/core/test_new_feature.py
import pytest
from core import NewFeature

def test_new_feature():
    """Test new feature works correctly."""
    feature = NewFeature()
    result = feature.do_thing()
    assert result == expected_value

@pytest.mark.slow
def test_new_feature_integration():
    """Integration test (marked as slow)."""
    # Slow test code
    pass
```

### Update Documentation

```bash
# Edit Markdown file
vim docs/architecture/overview.md

# Preview changes
mkdocs serve

# Commit and push (auto-deploys)
git add docs/
git commit -m "docs: update architecture overview"
git push
```

### Fix Failing CI

```bash
# Check CI logs on GitHub
# Run same checks locally:

# 1. Quality checks
pre-commit run --all-files

# 2. Tests
pytest -v

# 3. Build
python -m build

# 4. Docs
mkdocs build --strict
```

## 8. Troubleshooting

### Import Errors

```bash
# Install in editable mode
pip install -e .

# Check PYTHONPATH
echo $PYTHONPATH

# Add to PYTHONPATH (temporary)
export PYTHONPATH="$PWD:$PYTHONPATH"
```

### Pre-commit Failures

```bash
# Run hooks manually to see details
pre-commit run --all-files

# Update hooks
pre-commit autoupdate

# Skip hooks (emergency only!)
git commit --no-verify
```

### Test Failures

```bash
# Run with verbose output
pytest -vv

# Show print statements
pytest -s

# Drop into debugger on failure
pytest --pdb

# Run specific failing test
pytest tests/core/test_zscore.py::test_failing_test -vv
```

### Documentation Build Errors

```bash
# Strict mode (shows warnings as errors)
mkdocs build --strict

# Validate YAML
python -c "import yaml; yaml.safe_load(open('mkdocs.yml'))"

# Check broken links
mkdocs build && python -m http.server --directory site
```

## 9. Best Practices

### Factor 13 (Universal Love)

- **NEVER** bypass crisis detection
- **ALWAYS** test emergency override
- **NEVER** create duplicate Z-score calculations
- **ALWAYS** use canonical imports from `core`

### Code Style

- **Type hints**: Use for all function signatures in `core/`
- **Docstrings**: Google style for all public functions
- **Line length**: 100 characters (enforced by Black)
- **Imports**: Sorted automatically by Ruff

### Testing

- **Coverage**: Aim for >80% in `core/`, >60% overall
- **Markers**: Use `@pytest.mark.slow` for integration tests
- **Fixtures**: Share test data via fixtures in `conftest.py`
- **Mocking**: Use `pytest-mock` for external dependencies

### Commits

- **Format**: `type: description` (e.g., `feat: add Z-score cache`)
- **Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`
- **Size**: Small, focused commits (easier to review)
- **Pre-commit**: Let it run! Catches issues early

## 10. Resources

- **Repository**: https://github.com/xxkylesteenxx/GAIA...
- **Documentation**: https://xxkylesteenxx.github.io/GAIA.../
- **Issues**: https://github.com/xxkylesteenxx/GAIA.../issues
- **Dependencies**: [docs/dependencies.md](../dependencies.md)
- **Audit**: [docs/AUDIT_REMEDIATION.md](../AUDIT_REMEDIATION.md)

## Next Steps

1. ✅ Environment set up
2. ✅ Pre-commit installed
3. ✅ Tests passing
4. 🚀 Read [Architecture Overview](../architecture/overview.md)
5. 🚀 Pick an issue and contribute!

---

**Welcome to GAIA development!** 🌿

*The greening force flows through all things.*
