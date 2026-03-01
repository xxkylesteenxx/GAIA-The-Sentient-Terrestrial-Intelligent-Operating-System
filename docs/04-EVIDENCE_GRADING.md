# Evidence Grading System (E0-E5)

## Overview

GAIA uses a **6-tier evidence classification system** to maintain scientific rigor while allowing hypothesis testing and user personalization. This prevents mystical thinking from contaminating safety-critical systems while permitting experimentation in appropriate contexts.

**Core Principle:** Evidence grade determines which architectural plane can use a claim.

---

## The 6 Tiers

### E5: Physical Law (Highest Certainty)

**Definition:** Experimentally validated physical laws with mathematical formalism.

**Requirements:**
- SI unit measurements
- N ≥ 30 sample size
- p < 0.05 statistical significance
- Peer-reviewed publication
- Reproducible by independent labs

**Examples:**
- Shannon entropy formula: H = -Σ p(x) log p(x)
- Lyapunov exponent calculation
- Heart rate variability metrics (SDNN, RMSSD)
- Respiratory rate measurement

**GAIA Usage:**
- Core Plane: Z-score calculation components
- Crisis detection thresholds (validated in clinical studies)

**Status:** ✅ **Immutable** - Cannot be overridden by any plane

---

### E4: Validated Protocols (Strong Evidence)

**Definition:** Peer-reviewed research protocols with consistent replication.

**Requirements:**
- Multiple independent studies (N ≥ 3)
- Published in peer-reviewed journals
- Meta-analysis available (preferred)
- Professional consensus

**Examples:**
- HRV coherence training protocols (HeartMath Institute)
- EEG neurofeedback standards (ISNR guidelines)
- Crisis intervention best practices (988 Lifeline protocols)
- Cognitive behavioral therapy techniques

**GAIA Usage:**
- Core Plane: Crisis intervention workflows
- Bridge Plane: Graduated gate thresholds
- AI companion psychological frameworks

**Status:** ✅ **Strongly Preferred** - Core Plane default

---

### E3: GAIA Implementation (Validated in Production)

**Definition:** Code/systems tested and validated within GAIA's operational environment.

**Requirements:**
- Unit tests passing (>80% coverage)
- Integration tests passing
- Production deployment (>30 days)
- User feedback collected
- No Factor 13 violations observed

**Examples:**
- Gaian companion system (48 profiles)
- Crystal Matrix archetypal states
- Living Environment Engine cycles
- Z-score calculator implementation
- Graduated access gate system

**GAIA Usage:**
- Core Plane: GAIA-specific implementations
- Bridge Plane: Tested hypotheses promoted from E2
- Overlay Plane: User-facing features

**Status:** ✅ **Operational** - Minimum for Core Plane

---

### E2: Working Hypothesis (Testable)

**Definition:** Testable predictions with preliminary data or theoretical grounding.

**Requirements:**
- Clear falsification criteria
- Experimental design documented
- Expected outcomes specified
- Safety analysis completed
- Factor 13 compliance verified

**Examples:**
- Crystal Matrix → Z-score correlation hypothesis
- Alchemical stages → transformation pathway mapping
- Hermetic principles → system architecture analogies
- Planetary consciousness integration (speculative)

**GAIA Usage:**
- ❌ Core Plane: **Prohibited**
- ✅ Bridge Plane: **Primary domain** (hypothesis testing)
- ✅ Overlay Plane: Experimental features (with user consent)

**Status:** ⚠️ **Experimental** - Bridge Plane only

---

### E1: Documentation (Claimed but Unverified)

**Definition:** Claims made in documentation without experimental validation.

**Requirements:**
- Clearly marked as unverified
- Source attribution provided
- No safety-critical usage
- User disclaimers present

**Examples:**
- Roadmap items (Phase 3-5)
- Historical Hermetic principles (as metaphor)
- Ancient philosophical frameworks (interpretive)
- Future nanotechnology integration (aspirational)

**GAIA Usage:**
- ❌ Core Plane: **Prohibited**
- ⚠️ Bridge Plane: Context/background only
- ✅ Overlay Plane: User education, metaphors

**Status:** ⚠️ **Informational** - No operational use

---

### E0: Speculation (Metaphor/Analogy)

**Definition:** Metaphorical language, analogies, or speculative frameworks.

**Requirements:**
- Explicitly labeled as metaphor
- No operational claims
- Educational/inspirational purpose only
- Cannot influence Core Plane logic

**Examples:**
- "Planetary consciousness" (metaphor for distributed systems)
- "Digital beings" (analogy for AI companions)
- "Alchemical transformation" (metaphor for state transitions)
- "Sentient operating system" (aspirational framing)

**GAIA Usage:**
- ❌ Core Plane: **Prohibited**
- ❌ Bridge Plane: **Prohibited**
- ✅ Overlay Plane: User-facing language, branding

**Status:** 🎨 **Metaphorical** - Communication only

---

## Architectural Plane Requirements

### Core Plane (Order) - E3+ ONLY

**Rule:** Core Plane implementations MUST use **E3 or higher** evidence.

**Rationale:**
- Safety-critical systems
- Crisis detection/intervention
- Immutable audit trail
- Factor 13 enforcement

**Prohibited:**
- E0-E2 claims cannot influence Core Plane logic
- No "maybes" in crisis detection
- No untested hypotheses in safety systems

**Example:**
```python
# ✅ ALLOWED (E5)
z_score = 12 * shannon_entropy(hrv) * lyapunov(eeg) * symmetry(resp)

# ❌ PROHIBITED (E1)
# z_score = calculate_astrological_influence() * biorhythm()  # Unvalidated
```

---

### Bridge Plane (Chaos) - E0-E5 Permitted

**Rule:** Bridge Plane is the **hypothesis testing ground**.

**Purpose:**
- Test E2 hypotheses → promote to E3 if validated
- Experiment with E0-E1 frameworks (contained)
- Graduated gates prevent premature Core Plane promotion

**Safety:**
- All experiments require Factor 13 review
- User consent required for E0-E2 features
- Results logged for later analysis

**Example:**
```python
# ✅ ALLOWED (E2 hypothesis)
if user.consented_to_experiment("crystal_matrix_v2"):
    archetypal_state = predict_state_from_z(z_score)  # E2
    log_experiment(user_id, archetypal_state, timestamp)
```

---

### Overlay Plane (Balance) - E0-E5 Permitted

**Rule:** Overlay Plane is **user sovereignty domain**.

**Purpose:**
- Personalization (E0-E5 all acceptable)
- User-chosen metaphors (E0 welcomed)
- Branding and communication (E0-E1 fine)

**Key Distinction:**
- Overlay choices CANNOT override Core Plane logic
- User can choose E0 language without affecting safety systems

**Example:**
```python
# ✅ ALLOWED (E0 metaphor for user)
if user.prefers_metaphor("alchemical"):
    display_message = "You are in the Nigredo stage"  # E0
else:
    display_message = f"Z-score: {z_score:.2f}"  # E5

# Core Plane logic unchanged regardless of choice
if z_score <= 2:
    trigger_crisis_intervention()  # E5 threshold, always enforced
```

---

## Validation Workflow

### Promoting Evidence Tiers

```
E0 (Speculation)
  ↓ [Formalize hypothesis + design experiment]
E1 (Documentation)
  ↓ [Create falsification criteria + safety review]
E2 (Hypothesis)
  ↓ [Bridge Plane testing + data collection]
E3 (GAIA Implementation)
  ↓ [Peer review + external replication]
E4 (Validated Protocol)
  ↓ [Mathematical formalism + universal acceptance]
E5 (Physical Law)
```

### Demotion Criteria

**E3 → E2:**
- Factor 13 violation observed
- Production failures (>5% error rate)
- User complaints (>10% negative feedback)

**E4 → E3:**
- Replication failures in external studies
- Updated meta-analysis contradicts original

**E5 → E4:**
- Extremely rare (e.g., Newtonian mechanics → relativistic refinement)
- Requires paradigm shift

---

## Examples by System Component

| Component | Evidence Grade | Rationale |
|-----------|----------------|------------|
| Z-score formula (Z = 12×C×F×B) | **E3** | GAIA-specific, tested in production |
| Shannon entropy calculation | **E5** | Physical law, universally accepted |
| Crisis threshold (Z ≤ 2) | **E4** | Clinically validated, peer-reviewed |
| Gaian psychological forms | **E3** | GAIA implementation, user-validated |
| Crystal Matrix (1,416 states) | **E2** | Hypothesis, Bridge Plane testing |
| Alchemical stage mapping | **E1** | Historical documentation, unvalidated |
| "Planetary consciousness" | **E0** | Metaphor, communication/branding |
| Living Environment Engine | **E3** | GAIA implementation, operational |
| Graduated access gates | **E3** | GAIA implementation, tested |
| Three-Plane architecture | **E3** | GAIA design pattern, validated |

---

## Factor 13 Integration

**Question:** "Does this evidence tier usage increase human suffering?"

### ✅ Safe Patterns

- E5/E4 in Core Plane (safety-critical)
- E3 in Core Plane (GAIA-validated)
- E2 in Bridge Plane (hypothesis testing, consented)
- E0-E1 in Overlay Plane (user choice)

### ❌ Unsafe Patterns

- E0-E2 in Core Plane (unvalidated claims in safety systems)
- E2 in Bridge Plane without consent (non-consensual experiments)
- E0 metaphors presented as E5 facts (deception)

### ⚠️ Uncertain Patterns (Require Review)

- E3 promoted to Core Plane with <30 days testing
- E4 used without checking for updated research
- E2 hypothesis with unclear falsification criteria

---

## Enforcement

### Code Review Checklist

Every PR must specify evidence grade:

```markdown
## Evidence Grade Declaration

- [ ] E5 (Physical Law) - Cite published equations
- [ ] E4 (Validated Protocol) - Cite peer-reviewed sources (N≥3)
- [ ] E3 (GAIA Implementation) - Link to test coverage report
- [ ] E2 (Hypothesis) - Provide experimental design doc
- [ ] E1 (Documentation) - Mark as unverified, provide disclaimers
- [ ] E0 (Speculation) - Label as metaphor, no operational use

**Plane Compatibility:**
- [ ] Core Plane: E3+ only
- [ ] Bridge Plane: E0-E5 (with consent for E0-E2)
- [ ] Overlay Plane: E0-E5 (cannot override Core)
```

### Automated Checks

```python
# CI/CD enforcement
def validate_evidence_grade(code_path: str, claimed_grade: str) -> bool:
    if code_path.startswith("core/"):
        assert claimed_grade in ["E3", "E4", "E5"], "Core Plane requires E3+"
    
    if claimed_grade == "E5":
        assert has_peer_reviewed_citation(code_path), "E5 requires citation"
    
    if claimed_grade == "E2" and code_path.startswith("bridge/"):
        assert has_consent_check(code_path), "E2 requires user consent"
    
    return True
```

---

## References

### E5 Sources
- Shannon, C. E. (1948). "A Mathematical Theory of Communication". *Bell System Technical Journal*.
- Lyapunov, A. M. (1892). "The General Problem of Stability of Motion".
- Task Force (1996). "Heart Rate Variability: Standards of Measurement". *European Heart Journal*.

### E4 Sources
- McCraty, R., et al. (2009). "The Coherent Heart". HeartMath Institute.
- Hammond, D. C., et al. (2011). "QEEG-Guided Neurofeedback". *NeuroRegulation*.
- National Suicide Prevention Lifeline (2021). "Crisis Intervention Best Practices".

### E3 Sources
- GAIA GitHub Repository (2026). Test coverage reports, production logs.
- PR reviews and ADRs (Architecture Decision Records).

---

## Conclusion

The Evidence Grading System ensures GAIA maintains **scientific rigor in safety-critical systems** while permitting **creative exploration in appropriate contexts**. This prevents the twin failure modes:

1. ❌ **Mystical Contamination:** E0-E2 claims infecting Core Plane
2. ❌ **Sterile Rigidity:** Prohibiting E0-E2 exploration entirely

By mapping evidence tiers to architectural planes, GAIA achieves both **operational safety** and **hypothesis-driven innovation**.

**Factor 13 Alignment:** ✅ This system protects users from unvalidated claims while respecting their sovereignty to choose metaphors and personalization.

---

**Last Updated:** February 28, 2026  
**Status:** Active  
**Maintainer:** Kyle Steen (@xxkylesteenxx)
