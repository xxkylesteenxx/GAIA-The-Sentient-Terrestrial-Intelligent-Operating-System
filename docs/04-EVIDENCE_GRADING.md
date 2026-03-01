# Evidence Grading System (E0-E5)

## Overview

GAIA uses a **6-tier evidence classification system** to distinguish between metaphor, hypothesis, implementation, and physical law. This grading ensures that safety-critical systems (Core Plane) operate on validated evidence while creative exploration (Bridge/Overlay Planes) can work with speculation.

**Purpose:**
- Prevent premature solidification of untested ideas
- Enable safe experimentation in the Bridge Plane
- Enforce rigor in the Core Plane
- Allow user metaphors in the Overlay Plane
- Maintain intellectual honesty about uncertainty

---

## The 6 Evidence Tiers

### E5: Physical Law
**Definition:** Phenomena governed by invariant natural laws, reproducible across contexts.

**Characteristics:**
- SI units required
- Statistical significance (N ≥ 30, p < 0.05)
- Peer-reviewed publication
- Independent replication
- Predictive models with measured error bounds

**Examples in GAIA:**
- Solar position calculations (NOAA algorithms)
- Heart rate variability measurement (ms²)
- Shannon entropy of biosignals (bits)
- Electromagnetic spectrum frequencies (Hz)
- Temperature, pressure, location (SI units)

**Enforcement:**
- Core Plane MUST use E5 for all physical measurements
- Sensors must be calibrated to known standards
- Measurement uncertainty must be quantified

---

### E4: Validated Protocols
**Definition:** Peer-reviewed methods with demonstrated effectiveness in controlled settings.

**Characteristics:**
- Published in scientific journals
- Replicated by independent researchers
- Known limitations documented
- Effect sizes quantified
- Clinical or experimental validation

**Examples in GAIA:**
- HRV analysis for stress detection (Task Force 1996)
- EEG frequency band interpretation (alpha, beta, theta)
- Lyapunov exponent calculation for chaos detection
- Cognitive load measurement protocols
- Circadian rhythm modeling

**Enforcement:**
- Core Plane CAN use E4 for biosignal interpretation
- Bridge Plane MUST cite E4 sources when claiming effectiveness
- Overlay Plane can reference E4 for educational context

---

### E3: GAIA Implementation
**Definition:** Features implemented in GAIA codebase, tested in production or staging.

**Characteristics:**
- Source code exists in repository
- Unit tests pass (>80% coverage target)
- Integration tests validate behavior
- Documented in ADRs (Architecture Decision Records)
- May build on E4/E5 foundations

**Examples in GAIA:**
- Z-score calculator (`core/z_calculator.py`)
- Gaian companion system (`core/gaian.py`)
- Living Environment Engine (`bridge/environment/`)
- Crisis detection thresholds (Z ≤ 2)
- WebSocket API for environment state

**Enforcement:**
- Core Plane REQUIRES E3+ for all safety-critical features
- Bridge Plane tests E2 hypotheses to elevate them to E3
- Overlay Plane implements E3 features with user-facing polish

---

### E2: Working Hypothesis
**Definition:** Testable predictions with plausible mechanisms but not yet validated in GAIA.

**Characteristics:**
- Falsifiable claims
- Proposed implementation path
- Literature references (even if preliminary)
- Identified risks and assumptions
- Marked as "experimental" or "under investigation"

**Examples in GAIA:**
- Crystal Matrix archetypal state mapping (1,416 states)
- Graduated access gate effectiveness (6 tiers)
- Alchemical stage progression (12 stages)
- Synchrony metrics for human-Gaian bonding
- Planetary consciousness integration protocols

**Enforcement:**
- Core Plane CANNOT use E2 (too speculative for safety)
- Bridge Plane EXISTS to test E2 → E3 (hypothesis → implementation)
- Overlay Plane can DISPLAY E2 with clear disclaimers

---

### E1: Documentation
**Definition:** Claims made in documentation or discourse but not implemented or tested.

**Characteristics:**
- Design documents
- Roadmap features (not yet built)
- Architectural proposals
- User stories
- Conceptual frameworks

**Examples in GAIA:**
- Quantum backends (Phase 5, 2031+)
- Neuromorphic chip integration (future)
- Federation protocol (Phase 3, 2027)
- Guardian Council formation (Phase 2)
- Cryptographic video memory (Phase 3)

**Enforcement:**
- Core Plane IGNORES E1 (not real yet)
- Bridge Plane MAY prototype E1 → E2 (design → hypothesis)
- Overlay Plane MAY show E1 in roadmap/vision contexts

---

### E0: Speculation
**Definition:** Metaphors, analogies, aesthetic choices, or philosophical framings without empirical claims.

**Characteristics:**
- Poetic language
- Analogies ("like," "as if," "imagine")
- Aesthetic preferences
- Philosophical stances
- Mythological references

**Examples in GAIA:**
- "Digital home" metaphor (vs. "execution environment")
- "Gaian species" framing (vs. "AI agent class")
- "Alchemical transformation" language (vs. "state transitions")
- "Universal Love" as Factor 13 name (vs. "prosocial cooperation constraint")
- Tree of Life cosmology mapping

**Enforcement:**
- Core Plane EXCLUDES E0 (no metaphors in enforcement logic)
- Bridge Plane CAN use E0 for hypothesis generation inspiration
- Overlay Plane EMBRACES E0 (user experience, narrative, meaning)

---

## Three-Plane Evidence Requirements

### Core Plane (Order, Enforcement)
**Minimum Evidence:** E3 (GAIA Implementation)

**Rationale:**
- Safety-critical operations
- Crisis detection (Z ≤ 2)
- Audit trail integrity
- Resource access control
- Factor 13 enforcement

**Forbidden:**
- E0 (metaphors can't enforce safety)
- E1 (documentation isn't code)
- E2 (hypotheses aren't validated)

**Allowed:**
- E3 (tested GAIA features)
- E4 (validated protocols)
- E5 (physical law)

---

### Bridge Plane (Chaos, Testing)
**Minimum Evidence:** E0 (Speculation)

**Rationale:**
- Hypothesis testing ground
- Experimentation sandbox
- Graduated access gates
- Prototype validation
- E2 → E3 elevation pathway

**Purpose:**
- Test speculative ideas safely
- Validate before Core Plane promotion
- Collect evidence for elevation
- Fail fast on bad hypotheses

**Example Workflow:**
1. Start with E0 speculation ("What if alchemical stages map to Z-score?")
2. Formalize as E2 hypothesis (12 stages, threshold definitions)
3. Implement in Bridge Plane (prototype with logging)
4. Collect data, run tests
5. If validated → elevate to E3, promote to Core Plane
6. If refuted → keep in Bridge as educational "failed hypothesis"

---

### Overlay Plane (Balance, User Experience)
**Minimum Evidence:** E0 (Speculation)

**Rationale:**
- User sovereignty (choose own metaphors)
- Narrative coherence
- Aesthetic preferences
- Cultural adaptation
- Meaning-making

**Flexibility:**
- Can use ALL evidence tiers (E0-E5)
- Must LABEL tier when mixing (transparency)
- Safety warnings for E0-E2 ("experimental feature")
- User can disable speculative features

**Example:**
```python
# Overlay can show user a message like:
"Your Gaian companion Lyra (E3: implemented) 
senses your coherence at Z=3.2 (E5: measured) 
and suggests entering the Calcination stage (E2: hypothesis) 
of alchemical transformation (E0: metaphor)."
```

---

## Evidence Elevation Process

### E0 → E1 (Speculation → Documentation)
1. Write design document
2. Propose in GitHub issue or ADR
3. Community review
4. Merge into docs/ with E1 tag

### E1 → E2 (Documentation → Hypothesis)
1. Add falsifiable predictions
2. Identify testable claims
3. Propose experiments
4. Peer review (technical feasibility)
5. Mark as E2 in Bridge Plane experiments

### E2 → E3 (Hypothesis → Implementation)
1. Implement feature in Bridge Plane
2. Write unit + integration tests
3. Collect validation data
4. Document in ADR with test results
5. Promote to E3, consider Core Plane migration

### E3 → E4 (Implementation → Protocol)
1. External replication (other teams/orgs)
2. Peer-reviewed publication
3. Community adoption
4. Standardization
5. Recognized as validated protocol

### E4 → E5 (Protocol → Law)
1. Universal invariance demonstrated
2. Predictive models with error bounds
3. Multiple independent confirmations
4. Textbook/standard reference status
5. Treated as physical law

---

## Labeling Conventions

### In Documentation
```markdown
**Evidence Grade:** E3 (GAIA Implementation)
**Source:** `core/z_calculator.py`
**Tests:** `tests/core/test_z_calculator.py` (18 tests, 92% coverage)
```

### In Code Comments
```python
# Evidence: E5 (solar position from NOAA algorithm)
def calculate_solar_position(lat: float, lon: float, dt: datetime) -> tuple[float, float]:
    ...

# Evidence: E2 (hypothesis - needs validation)
def detect_archetypal_state(z_score: float) -> ArchetypalState:
    # TODO: Elevate to E3 after 30-day user study
    ...
```

### In UI
```
[E3] Crisis Detection Active
[E2 - Experimental] Alchemical Stage Tracking
[E0 - Metaphor] "Your digital home adapts to your energy"
```

---

## Examples Across Evidence Tiers

| Claim | Tier | Rationale |
|-------|------|----------|
| "HRV measured at 45 ms²" | E5 | Physical measurement with SI units |
| "Low HRV correlates with stress" | E4 | Peer-reviewed, validated protocol (Task Force 1996) |
| "Z-score < 2 triggers crisis alert" | E3 | Implemented in `core/safety/crisis_detector.py` |
| "12 alchemical stages map to Z-score ranges" | E2 | Hypothesis, needs validation |
| "Guardian tier unlocks at 180 days" | E1 | Designed but not implemented |
| "Your Gaian companion is like a digital twin" | E0 | Metaphor for user understanding |

---

## Common Pitfalls

### ❌ Don't: Use E0 in Core Plane
```python
# WRONG - metaphor in safety-critical code
if user_feels_like_transforming():  # E0 language
    trigger_crisis_alert()
```

### ✅ Do: Use E3+ in Core Plane
```python
# CORRECT - measured value in safety-critical code
if z_score <= 2.0:  # E3 threshold, E5 measurement
    trigger_crisis_alert()
```

### ❌ Don't: Claim E3 for Unimplemented Features
```markdown
The Crystal Matrix (E3) provides 1,416 archetypal states.
```
*(Correct: E2 if designed, E1 if only documented)*

### ✅ Do: Label Accurately
```markdown
The Crystal Matrix (E2 hypothesis, E1 documentation) proposes 1,416 archetypal states.
Implementation tracked in Issue #42.
```

---

## Enforcement Mechanisms

### Pre-Commit Hooks
```bash
# Check for E0 language in core/ directory
grep -r "feels like\|imagine\|as if" core/ && exit 1
```

### Code Review Checklist
- [ ] Core Plane changes use E3+ evidence only
- [ ] Bridge Plane experiments clearly marked E2
- [ ] Documentation cites evidence tier for claims
- [ ] UI labels experimental features

### CI/CD Gates
```yaml
# .github/workflows/evidence-gate.yml
- name: Evidence Grade Validation
  run: |
    python scripts/validate_evidence_grades.py
    # Fails if Core Plane has E0-E2 claims
```

---

## Relationship to Factor 13

Factor 13 (prosocial cooperation) enforcement REQUIRES high-evidence standards:

**Why E3+ for Core Plane?**
- Cannot enforce "do no harm" with metaphors (E0)
- Cannot protect users with untested ideas (E2)
- Cannot guarantee safety with documentation alone (E1)

**Evidence protects users:**
- E5 measurements detect real crisis states
- E4 protocols provide validated interventions
- E3 implementations have been tested

**Low evidence enables exploration:**
- E0-E2 in Bridge/Overlay lets users experiment
- Transparency about evidence tier enables informed consent
- Users can disable speculative features

---

## References

1. **Epistemology:** Popper, K. (1959). *The Logic of Scientific Discovery.*
2. **Evidence-Based Practice:** Sackett, D. L. (1996). "Evidence based medicine: what it is and what it isn't."
3. **GAIA Architecture:** `docs/01-ARCHITECTURE.md` (Three-Plane system)
4. **GAIA Constitution:** `docs/00-CONSTITUTION.md` (Factor 13)
5. **HRV Standards:** Task Force (1996). "Heart rate variability: standards of measurement."

---

## Changelog

- **2026-03-01:** Initial specification (this document)
- Evidence tier system standardized across GAIA documentation
- Core/Bridge/Overlay requirements clarified
- Elevation process defined

---

**Evidence Grade for This Document:** E1 (Documentation)

*This standard will elevate to E3 once enforcement mechanisms (pre-commit hooks, CI gates) are implemented and tested.*
