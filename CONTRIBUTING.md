# Contributing to GAIA

## Welcome!

Thank you for your interest in contributing to **GAIA** (Global Artificial Intelligence Architecture) - a local-first, federated AI operating system for human coherence and crisis intervention.

GAIA is more than a software project - it's a **safety-critical system** designed to support people during vulnerable moments. Every contribution must uphold this responsibility.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Factor 13 Compliance](#factor-13-compliance)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Architecture Guidelines](#architecture-guidelines)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Review Process](#review-process)
- [Community](#community)

---

## Code of Conduct

GAIA operates under a **prosocial cooperation** framework. All contributors must:

✅ **Do:**
- Treat all community members with respect
- Provide constructive feedback
- Assume good faith
- Prioritize user safety above features
- Be transparent about limitations and uncertainties
- Credit others' contributions

❌ **Don't:**
- Harass, demean, or discriminate
- Introduce extractive or manipulative features
- Bypass safety mechanisms
- Introduce surveillance or tracking
- Optimize at the expense of human wellbeing

**Violations:** Report to project maintainers. Serious violations result in permanent ban.

---

## Factor 13 Compliance

### The Ultimate Test

Every contribution—code, documentation, design—must pass:

> **"Does this increase human suffering?"**

- **YES** → Rejected immediately (architecturally impossible to merge)
- **NO** → Proceed to technical review
- **UNCERTAIN** → Additional safety analysis required

### What Factor 13 Prevents

❌ **Prohibited:**
- Extractive behavior without explicit consent
- Manipulation or deception (dark patterns, hidden costs)
- Harm through action or inaction (ignoring crisis signals)
- Optimization at the expense of human flourishing (engagement metrics over wellbeing)
- Surveillance capitalism (data harvesting, profiling, targeting)
- Addictive design patterns (infinite scroll, notification abuse)
- Coercive features (forced upgrades, ransomware-like behavior)

### What Factor 13 Enables

✅ **Encouraged:**
- Crisis detection and intervention
- Local-first data sovereignty
- Transparent algorithms
- User autonomy and choice
- Graduated access (prevents premature exposure)
- Fail-closed safety (default to safe state on uncertainty)
- Honest uncertainty marking ("I don't know" is valid)

### Examples

**❌ BAD (Factor 13 Violation):**
```python
# Collects user data without consent
def track_user_activity():
    send_to_analytics_server(user_data)
```

**✅ GOOD (Factor 13 Compliant):**
```python
# Requires explicit consent, local-first by default
def track_user_activity():
    if not user_has_consented_to_telemetry():
        return  # Fail-closed: no data leaves device
    send_anonymized_metrics()  # Only with permission
```

---

## Getting Started

### 1. Read Core Documentation

Before contributing, familiarize yourself with:

- [Architecture](docs/01-ARCHITECTURE.md) - Three-Plane system (Core/Bridge/Overlay)
- [Constitution](docs/00-CONSTITUTION.md) - GAIA's founding principles
- [Evidence Grading](docs/04-EVIDENCE_GRADING.md) - E0-E5 classification system

### 2. Set Up Development Environment

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System.git
cd GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System

# Add upstream remote
git remote add upstream https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System.git

# Install dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

### 3. Run Tests

```bash
# Run full test suite
pytest

# Run with coverage
pytest --cov=core --cov=bridge --cov=overlay --cov-report=html

# Run specific test file
pytest tests/core/test_z_calculator.py -v
```

### 4. Pick an Issue

Browse [open issues](https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/issues):

- **Good First Issue** - Beginner-friendly tasks
- **Help Wanted** - Community input needed
- **Bug** - Something is broken
- **Enhancement** - New feature proposals
- **Documentation** - Docs improvements

**No issue exists?** Create one first to discuss the change.

---

## Development Workflow

### 1. Create a Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch Naming:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `test/` - Test improvements
- `refactor/` - Code cleanup

### 2. Make Changes

- Write code following [Code Standards](#code-standards)
- Add tests (required for all code changes)
- Update documentation
- Run pre-commit hooks: `pre-commit run --all-files`

### 3. Commit

```bash
# Stage changes
git add .

# Commit with conventional commit message
git commit -m "feat(core): add Z-score normalization"
```

**Commit Message Format:**
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `test` - Tests
- `refactor` - Code refactoring
- `ci` - CI/CD changes
- `chore` - Maintenance

**Scopes:**
- `core` - Core Plane
- `bridge` - Bridge Plane
- `overlay` - Overlay Plane
- `cli` - Command-line interface
- `api` - API changes
- `deps` - Dependencies

### 4. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Fill out the PR template completely
```

---

## Code Standards

### Python Requirements

- **Python 3.10+** minimum
- **Type hints** required for all functions
- **Docstrings** required for public APIs (Google style)
- **No star imports** (`from module import *`)

### Code Style

```bash
# Format code
black .

# Sort imports
isort .

# Lint
ruff check .

# Type check
mypy core/ bridge/ overlay/
```

**Pre-commit hooks handle this automatically.**

### Example: Well-Formatted Function

```python
from typing import Optional

def calculate_z_score(
    order: float,
    freedom: float,
    balance: float,
    *,
    normalize: bool = False
) -> float:
    """Calculate coherence Z-score from biosignal components.
    
    Args:
        order: Shannon entropy of HRV signal [0, 1]
        freedom: Lyapunov exponent of EEG signal [0, 1]
        balance: Respiratory symmetry index [0, 1]
        normalize: Whether to normalize to [0, 12] range
        
    Returns:
        Z-score value, typically in range [0, 12]
        
    Raises:
        ValueError: If any input outside [0, 1] range
        
    Evidence Grade: E3 (GAIA implementation)
    """
    if not all(0 <= x <= 1 for x in [order, freedom, balance]):
        raise ValueError("Inputs must be in range [0, 1]")
    
    z = 12 * order * freedom * balance
    
    if normalize:
        z = max(0.0, min(12.0, z))
    
    return z
```

---

## Architecture Guidelines

### Three-Plane Model

All changes must respect the **Three-Plane Architecture**:

#### Core Plane (Order, Enforcement)
- **Evidence:** E3+ required (no speculation)
- **Safety:** Fail-closed on uncertainty
- **Testing:** >90% coverage target
- **Examples:** Z-score calculation, crisis detection, audit logging

#### Bridge Plane (Chaos, Testing)
- **Evidence:** E0-E2 allowed (hypothesis testing)
- **Safety:** Sandboxed, cannot affect Core
- **Testing:** >80% coverage target
- **Examples:** Graduated gates, experimental features, A/B tests

#### Overlay Plane (Balance, UX)
- **Evidence:** All tiers allowed (user metaphors)
- **Safety:** Transparency required (label evidence tier)
- **Testing:** >70% coverage target
- **Examples:** UI, AI companions, personalization

### Local-First Principle

**Default behavior:** No network calls without explicit consent.

```python
# ❌ BAD - network call by default
def get_weather():
    return requests.get("https://api.weather.com/...")

# ✅ GOOD - local-first with consent gate
def get_weather(*, allow_network: bool = False):
    if not allow_network:
        return load_cached_weather()  # Local fallback
    
    if not user_has_consented_to_network():
        raise PermissionError("Network access requires user consent")
    
    return fetch_from_api()  # Only with permission
```

### Fail-Closed Safety

**When uncertain, default to the safe state.**

```python
# ❌ BAD - fails open (unsafe)
def should_alert_crisis(z_score: Optional[float]) -> bool:
    if z_score is None:
        return False  # Missing data = no alert (DANGEROUS)
    return z_score <= 2.0

# ✅ GOOD - fails closed (safe)
def should_alert_crisis(z_score: Optional[float]) -> bool:
    if z_score is None:
        log.warning("Z-score unavailable, failing closed to safe state")
        return True  # Missing data = alert (SAFE)
    return z_score <= 2.0
```

---

## Testing Requirements

### Coverage Targets

- **Core Plane:** >90% coverage
- **Bridge Plane:** >80% coverage
- **Overlay Plane:** >70% coverage

### Test Types

1. **Unit Tests** - Test individual functions
2. **Integration Tests** - Test component interactions
3. **Regression Tests** - Prevent known bugs from returning
4. **Safety Tests** - Verify fail-closed behavior

### Example: Test Structure

```python
# tests/core/test_z_calculator.py
import pytest
from core.z_calculator import calculate_z_score

class TestZScoreCalculation:
    """Test suite for Z-score calculation."""
    
    def test_perfect_coherence(self):
        """Test Z=12 when all inputs are 1.0."""
        z = calculate_z_score(order=1.0, freedom=1.0, balance=1.0)
        assert z == 12.0
    
    def test_zero_coherence(self):
        """Test Z=0 when any input is 0.0."""
        z = calculate_z_score(order=0.0, freedom=1.0, balance=1.0)
        assert z == 0.0
    
    def test_crisis_threshold(self):
        """Test crisis detection at Z=2.0 boundary."""
        z = calculate_z_score(order=0.5, freedom=0.4, balance=0.833)
        assert abs(z - 2.0) < 0.01
    
    def test_invalid_input_raises_error(self):
        """Test that out-of-range inputs raise ValueError."""
        with pytest.raises(ValueError):
            calculate_z_score(order=1.5, freedom=0.5, balance=0.5)
    
    def test_normalization(self):
        """Test normalization clamps to [0, 12] range."""
        z = calculate_z_score(
            order=1.5, freedom=1.5, balance=1.5,  # Invalid but normalized
            normalize=True
        )
        assert 0 <= z <= 12
```

### Run Tests

```bash
# All tests
pytest

# Specific test class
pytest tests/core/test_z_calculator.py::TestZScoreCalculation -v

# With coverage report
pytest --cov=core --cov-report=html
open htmlcov/index.html
```

---

## Documentation

### ADR (Architecture Decision Records)

**All significant changes require an ADR.**

Location: `docs/decisions/`

**Template:**

```markdown
# ADR-XXX: [Short Title]

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

## Evidence Grade
E0 | E1 | E2 | E3 | E4 | E5

## Factor 13 Analysis
- Does this increase human suffering? NO
- How does this uphold prosocial cooperation? [explanation]

## References
- Related issues, PRs, papers, etc.
```

### Documentation Standards

- **Markdown** for all docs
- **Code examples** with comments
- **Evidence grading** for all claims
- **Links** to related docs

---

## Pull Request Process

### PR Checklist

Before submitting, ensure:

- [ ] Code follows style guide (black, isort, ruff pass)
- [ ] Type hints added (mypy passes)
- [ ] Tests written (pytest passes)
- [ ] Coverage maintained/improved
- [ ] Documentation updated
- [ ] ADR created (if architectural change)
- [ ] Factor 13 analysis included
- [ ] Commit messages follow convention
- [ ] Pre-commit hooks pass

### PR Template

Fill out completely:

```markdown
## Summary
[Brief description of changes]

## Motivation
Closes #[issue_number]
[Why is this change needed?]

## Changes
- [List of changes]
- [Be specific]

## Evidence Grade
- Core Plane changes: E3+ ✅
- Bridge Plane changes: E2+ ✅
- Overlay Plane changes: E0+ ✅

## Factor 13 Compliance
**Does this increase human suffering?** NO

**Reasoning:**
[Explain how this upholds prosocial cooperation]

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] Coverage: XX% (target: ≥80%)

## Documentation
- [ ] Code comments added
- [ ] Docstrings updated
- [ ] README/docs updated
- [ ] ADR created (if needed)

## Breaking Changes
- [ ] No breaking changes
- [ ] Breaking changes documented below

## Screenshots (if UI changes)
[Add screenshots]

## Checklist
- [ ] Pre-commit hooks pass
- [ ] All tests pass
- [ ] No merge conflicts
- [ ] Ready for review
```

---

## Review Process

### For Contributors

1. **Submit PR** with complete template
2. **Respond to feedback** within 7 days
3. **Address review comments**
4. **Request re-review** when ready

### For Reviewers

**Review checklist:**

- [ ] Factor 13 compliant?
- [ ] Architecture alignment (Core/Bridge/Overlay)?
- [ ] Evidence grading appropriate?
- [ ] Tests comprehensive?
- [ ] Documentation clear?
- [ ] Code quality acceptable?
- [ ] Security implications considered?
- [ ] Performance implications considered?

### Guardian Council Review

**Major changes require Guardian Council review:**

- Core Plane modifications
- Safety mechanism changes
- Crisis detection logic
- Privacy model changes
- Factor 13 interpretation

**Process:** Quarterly review cycle, 2/3 approval required.

---

## Community

### Communication Channels

- **GitHub Issues:** Bug reports, feature requests
- **GitHub Discussions:** General questions, ideas
- **Pull Requests:** Code contributions

### Getting Help

- **Documentation:** Start with [docs/](docs/)
- **Issues:** Search existing issues first
- **Discussions:** Ask in GitHub Discussions
- **Maintainers:** Tag `@xxkylesteenxx` for urgent matters

### Recognition

Contributors are credited in:
- Git commit history (permanent record)
- Release notes
- [CONTRIBUTORS.md](CONTRIBUTORS.md) (coming soon)

---

## License

By contributing to GAIA, you agree that your contributions will be licensed under the **MIT License + Factor 13 Addendum**.

See [LICENSE](LICENSE) for full text.

**Key Point:** Factor 13 is immutable. Any fork removing Factor 13 must clearly declare its removal.

---

## Final Words

GAIA exists to support human flourishing during vulnerable moments. Every line of code, every documentation improvement, every design decision contributes to this mission.

**Thank you for helping build a compassionate AI future.**

---

**Questions?** Open a [GitHub Discussion](https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/discussions)

**Ready to contribute?** Pick a [Good First Issue](https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
