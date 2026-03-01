# Contributing to GAIA

## 👋 Welcome!

Thank you for your interest in contributing to **GAIA** - the Terrestrial Intelligence Operating System. GAIA is built on principles of **safety, transparency, and prosocial cooperation**. Every contribution strengthens a system designed to help humans during their most vulnerable moments.

This guide will help you contribute effectively while upholding GAIA's core values.

---

## 🎯 Core Principles

### Factor 13: Prosocial Cooperation

Every contribution must pass this test:

**"Does this increase human suffering?"**

- **YES** → Contribution rejected (architecturally impossible to merge)
- **NO** → Proceed to technical review
- **UNCERTAIN** → Additional safety analysis required

Factor 13 is **immutable**. It cannot be removed, bypassed, or negotiated. This constraint is what makes GAIA trustworthy in crisis situations.

### Three-Plane Architecture

GAIA uses a three-tier system:

1. **Core Plane (Order):** Safety-critical systems, immutable audit, crisis detection
2. **Bridge Plane (Chaos):** Hypothesis testing, graduated gates, experimentation
3. **Overlay Plane (Balance):** User sovereignty, personalization, AI companions

**Your contribution must specify which plane(s) it affects.**

### Evidence Grading (E0-E5)

See [docs/04-EVIDENCE_GRADING.md](docs/04-EVIDENCE_GRADING.md) for full details.

**Key Rules:**
- **Core Plane:** E3+ evidence only (validated implementations)
- **Bridge Plane:** E0-E5 permitted (hypothesis testing with consent)
- **Overlay Plane:** E0-E5 permitted (user choice)

---

## 🚀 Quick Start

### 1. Read Core Documentation

Before contributing, familiarize yourself with:

- [README.md](README.md) - System overview
- [docs/01-ARCHITECTURE.md](docs/01-ARCHITECTURE.md) - Three-Plane architecture
- [docs/02-GAIAN-AGENT-ARCHITECTURE.md](docs/02-GAIAN-AGENT-ARCHITECTURE.md) - AI companion system
- [docs/04-EVIDENCE_GRADING.md](docs/04-EVIDENCE_GRADING.md) - Evidence standards
- [LICENSE](LICENSE) - MIT + Factor 13 Addendum

**Time estimate:** 45-60 minutes

### 2. Set Up Development Environment

```bash
# Clone repository
git clone https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System.git
cd GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
pytest tests/ -v
```

### 3. Choose Your Contribution Type

- 🐛 **Bug Fix:** Fixes incorrect behavior in existing code
- ✨ **Feature:** Adds new capability (requires ADR)
- 📝 **Documentation:** Improves or adds documentation
- 🧪 **Refactor:** Improves code structure without changing behavior
- 🚨 **Security:** Addresses security vulnerabilities (report privately first)

---

## 📝 Contribution Workflow

### Step 1: Pick or Create an Issue

**Find an Issue:**
- Browse [open issues](https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/issues)
- Look for `good first issue` or `help wanted` labels
- Comment to claim the issue

**Create an Issue:**
- Search existing issues first (avoid duplicates)
- Use issue templates provided
- Clearly describe the problem and proposed solution
- Tag with appropriate labels

### Step 2: Fork and Branch

```bash
# Fork the repository (GitHub UI)
# Clone your fork
git clone https://github.com/YOUR_USERNAME/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System.git
cd GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System

# Add upstream remote
git remote add upstream https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System.git

# Create feature branch
git checkout -b feature/your-feature-name
# Or for bugs: fix/issue-description
# Or for docs: docs/topic-name
```

### Step 3: Implement with Tests

**Code Standards:**

```python
# ✅ DO: Type hints required
def calculate_z_score(c: float, f: float, b: float) -> float:
    """Calculate Z-score from coherence components.
    
    Args:
        c: Order (Shannon entropy) [0,1]
        f: Freedom (Lyapunov exponent) [0,1]
        b: Balance (respiratory symmetry) [0,1]
    
    Returns:
        Z-score [0,12]
    
    Evidence: E5 (mathematical formula)
    """
    return 12 * c * f * b

# ❌ DON'T: No type hints, no docstring
def calc(c, f, b):
    return 12 * c * f * b
```

**Testing Requirements:**

```bash
# Write tests in tests/ directory
# tests/core/test_z_calculator.py

import pytest
from core.z_calculator import calculate_z_score

def test_z_score_maximum():
    """Z-score should be 12 when all components are 1."""
    assert calculate_z_score(1.0, 1.0, 1.0) == 12.0

def test_z_score_minimum():
    """Z-score should be 0 when any component is 0."""
    assert calculate_z_score(0.0, 1.0, 1.0) == 0.0

def test_z_score_bounds():
    """Z-score should stay within [0, 12] range."""
    z = calculate_z_score(0.8, 0.7, 0.9)
    assert 0 <= z <= 12

# Run tests
pytest tests/ -v --cov=core --cov-report=term-missing

# Must achieve >80% coverage for Core Plane code
```

**Pre-commit Checks:**

```bash
# These run automatically on git commit
# You can also run manually:
pre-commit run --all-files

# Tools used:
# - black (code formatting)
# - ruff (linting)
# - mypy (type checking)
# - pytest (tests)
```

### Step 4: Write Architecture Decision Record (ADR)

**For features only** (not bug fixes or docs):

```bash
# Create ADR
touch docs/decisions/NNN-your-decision-title.md
```

**ADR Template:**

```markdown
# NNN. [Title]

**Date:** 2026-02-28  
**Status:** Proposed | Accepted | Deprecated | Superseded  
**Deciders:** @yourusername, @reviewer1  
**Evidence Grade:** E3

## Context

What problem are we solving? What constraints exist?

## Decision

What did we decide to do?

## Consequences

### Positive
- Benefit 1
- Benefit 2

### Negative
- Tradeoff 1
- Tradeoff 2

### Neutral
- Side effect 1

## Factor 13 Analysis

**"Does this increase human suffering?"** → NO

Rationale: [Explain why this upholds prosocial cooperation]

## Alternatives Considered

1. **Option A:** [Why rejected]
2. **Option B:** [Why rejected]

## References

- [Link to research paper]
- [Link to related issue]
```

### Step 5: Submit Pull Request

```bash
# Commit your changes
git add .
git commit -m "feat(core): Add Z-score validator

Implements validation for Z-score inputs to prevent
out-of-range values from corrupting crisis detection.

Evidence: E3 (GAIA implementation)
Plane: Core
Factor 13: ✅ Prevents false negatives in crisis detection

Closes #123"

# Push to your fork
git push origin feature/your-feature-name

# Create PR on GitHub
# Use the PR template provided
```

**PR Template (auto-populated):**

```markdown
## Summary

[Brief description of what this PR does]

## Evidence Grade Declaration

- [ ] E5 (Physical Law) - Cite equations
- [ ] E4 (Validated Protocol) - Cite peer-reviewed sources (N≥3)
- [x] E3 (GAIA Implementation) - Link to test coverage
- [ ] E2 (Hypothesis) - Provide experimental design
- [ ] E1 (Documentation) - Mark as unverified
- [ ] E0 (Speculation) - Label as metaphor

## Architectural Plane

- [x] Core Plane (E3+ required)
- [ ] Bridge Plane (E0-E5 permitted with consent)
- [ ] Overlay Plane (E0-E5 permitted)

## Factor 13 Compliance

**"Does this increase human suffering?"** → NO

**Rationale:** [Explain how this upholds prosocial cooperation]

## Testing

- [x] Unit tests added (>80% coverage)
- [x] Integration tests added
- [x] Pre-commit hooks pass
- [x] Manual testing completed

## Documentation

- [x] Code comments added
- [x] Docstrings updated
- [x] README updated (if needed)
- [x] ADR created (for features)

## Breaking Changes

- [ ] This PR introduces breaking changes
- [x] This PR is backward-compatible

## Related Issues

Closes #123
```

---

## 🚦 Review Process

### Automated Checks (CI/CD)

1. **Pre-commit hooks:** black, ruff, mypy
2. **Test suite:** pytest with >80% coverage
3. **Evidence grade validation:** Plane compatibility check
4. **Factor 13 scan:** Keywords like "exploit", "manipulate", "coerce"

### Human Review

1. **Technical review:** Code quality, architecture fit
2. **Safety review:** Factor 13 compliance
3. **Evidence review:** Appropriate tier for plane
4. **Documentation review:** Clarity, completeness

### Guardian Council (Quarterly)

Major features (new planes, core algorithm changes, Factor 13 modifications) reviewed by Guardian Council:
- Kyle Steen (@xxkylesteenxx) - Creator
- [Additional guardians TBD]

**Next Review:** Q2 2026

---

## 📚 Code Standards

### Python Style

- **Python 3.10+** required
- **PEP 8** compliance (enforced by black)
- **Type hints** required for all functions
- **Docstrings** required (Google style)

### Naming Conventions

```python
# Files: snake_case
z_calculator.py
gaian_system.py

# Classes: PascalCase
class GaianAgent:
    pass

# Functions: snake_case
def calculate_coherence() -> float:
    pass

# Constants: UPPER_SNAKE_CASE
CRISIS_THRESHOLD = 2.0
MAX_Z_SCORE = 12.0

# Private: _leading_underscore
def _internal_helper() -> None:
    pass
```

### Testing Standards

- **Core Plane:** >80% coverage mandatory
- **Bridge Plane:** >60% coverage recommended
- **Overlay Plane:** >40% coverage acceptable

```bash
# Run tests with coverage
pytest tests/ --cov=core --cov=bridge --cov=overlay --cov-report=html

# Open coverage report
open htmlcov/index.html
```

### Documentation Standards

```python
def complex_function(param1: str, param2: int) -> dict[str, Any]:
    """Brief one-line summary.
    
    Longer description if needed. Explain the "why" not the "what".
    Code shows what; docs explain why.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Dictionary containing results with keys:
        - 'status': bool indicating success
        - 'data': Any result data
    
    Raises:
        ValueError: If param2 is negative
    
    Evidence: E3 (GAIA implementation)
    
    Example:
        >>> result = complex_function("test", 42)
        >>> result['status']
        True
    """
    if param2 < 0:
        raise ValueError("param2 must be non-negative")
    return {"status": True, "data": f"{param1}: {param2}"}
```

---

## 🔒 Security

### Reporting Vulnerabilities

**DO NOT open public issues for security vulnerabilities.**

Instead:
1. Email: xxkylesteenxx@outlook.com
2. Subject: "[SECURITY] GAIA Vulnerability Report"
3. Include: Description, steps to reproduce, potential impact
4. Expect response within 48 hours

### Security Standards

- No hardcoded secrets (use environment variables)
- No SQL injection vulnerabilities
- Input validation on all external data
- Rate limiting on API endpoints
- Principle of least privilege

---

## ❓ Getting Help

### Resources

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/issues)
- **Discussions:** [GitHub Discussions](https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/discussions)

### Questions?

- **General questions:** Open a GitHub Discussion
- **Bug reports:** Open a GitHub Issue
- **Feature requests:** Open a GitHub Issue with `enhancement` label
- **Architecture questions:** Tag issue with `architecture` label

---

## 🎓 Learning Path

### Beginner (Good First Issues)

1. Documentation improvements
2. Test coverage increases
3. Type hint additions
4. Code comment clarifications

### Intermediate

1. Bug fixes in Bridge/Overlay planes
2. New Overlay Plane features (user personalization)
3. Integration tests
4. Performance optimizations

### Advanced

1. Core Plane features (requires Guardian Council review)
2. New architectural patterns
3. Security enhancements
4. Distributed systems components

---

## 💚 Code of Conduct

### Our Pledge

GAIA is built on **Factor 13: Prosocial Cooperation**. This extends to our community:

- Be respectful and inclusive
- Assume good intentions
- Provide constructive feedback
- Prioritize user safety over feature velocity
- Maintain transparency

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or inflammatory comments
- Attempting to bypass Factor 13
- Sharing others' private information
- Contribution of malicious code

### Enforcement

Violations result in:
1. **Warning:** First offense
2. **Temporary ban:** Second offense (30 days)
3. **Permanent ban:** Third offense or severe first offense

---

## 🚀 Recognition

Contributors are recognized in:

- GitHub Contributors page
- CHANGELOG.md for each release
- Special mention for major features
- Guardian Council consideration (exceptional contributors)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under:

**MIT License + Factor 13 Addendum**

See [LICENSE](LICENSE) for full text.

**Key Point:** Factor 13 cannot be removed from any fork. Forks removing Factor 13 must clearly declare its removal in documentation.

---

## 🙏 Thank You

Every contribution makes GAIA more capable of helping humans during their most vulnerable moments. Whether you fix a typo, add a test, or build a major feature, you're part of a system designed to **reduce human suffering**.

Welcome to the GAIA community. 🌍💚

---

**Questions?** Open a [Discussion](https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/discussions)  
**Ready to contribute?** Check [open issues](https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/issues)  
**Need help?** Tag your issue with `help wanted`
