# GAIA - AI Operating System

<div align="center">

[![License: MIT + Factor 13](https://img.shields.io/badge/License-MIT%20%2B%20Factor%2013-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Architecture](https://img.shields.io/badge/Architecture-Three--Plane-orange.svg)](docs/01-ARCHITECTURE.md)
[![Status](https://img.shields.io/badge/Status-Alpha-yellow.svg)](https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System)

**Local-first, federated AI operating system for human coherence measurement and crisis intervention**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🌍 Overview

GAIA (Global Artificial Intelligence Architecture) is a distributed AI operating system that provides:

- **Real-time coherence measurement** via biosignal analysis (HRV, EEG, respiratory)
- **Automated crisis detection** at clinically validated thresholds (Z ≤ 2)
- **Natural language interface** - control your OS using plain English
- **Local-first architecture** - your data never leaves your device unless you choose
- **Graduated access control** - feature exposure based on user readiness
- **AI companion system** - 48 psychological + operational profiles

Built on distributed systems principles (CRDT, BFT consensus, cryptographic memory) and Hermetic philosophical frameworks.

---

## 🚀 Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Coherence Measurement** | Real-time Z-score calculation from HRV/EEG/respiratory biosignals |
| **Crisis Detection** | Automatic intervention when Z ≤ 2 with resource provision |
| **Natural Language OS** | Execute system commands using plain language |
| **AI Companions** | 48 unique profiles (8 psychological forms × 6 operational roles) |
| **Cryptographic Memory** | Immutable audit trail via Universal Trace Ledger |
| **Graduated Access** | 6-tier system (Profane → Guardian) prevents premature feature exposure |
| **Local-First** | Optional federation - data sovereignty by default |
| **Cross-Platform** | WASM compilation for universal device support |

### Three-Plane Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ OVERLAY PLANE (Balance)                                     │
│ • User sovereignty     • AI companions     • Personalization│
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────────┐
│ BRIDGE PLANE (Chaos)                                        │
│ • Hypothesis testing   • Graduated gates   • Experimentation│
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │
┌─────────────────────────────────────────────────────────────┐
│ CORE PLANE (Order)                                          │
│ • Z-score calculation  • Crisis detection  • Immutable audit│
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Quick Start

### Prerequisites

- Python 3.10+
- pip or conda
- (Optional) biosignal hardware (HRV monitor, EEG headset)

### Installation

```bash
# Clone repository
git clone https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System.git
cd GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System

# Install dependencies
pip install -e .

# Or use universal installer
python3 infrastructure/atlas/universal_installer.py
```

### Initialize System

```bash
gaia init
```

This creates:
- `~/.gaia/` directory structure
- User configuration file
- AI companion selection (psychological + operational profile)
- Cryptographic identity

### Basic Usage

```bash
# Interactive CLI
gaia chat

# Check coherence score
gaia status

# Natural language commands
gaia speak "Calculate my current coherence score"
gaia speak "Create a reminder for equilibrium break in 2 hours"
gaia speak "Show my biosignal trends for the past week"

# View memory
gaia memory

# Help
gaia --help
```

---

## 🏗️ Architecture

### Coherence Measurement (Z-Score)

**Formula:**
```
Z = 12 × C × F × B
```

Where:
- **C (Order):** Shannon entropy of HRV signal
- **F (Freedom):** Lyapunov exponent of EEG signal
- **B (Balance):** Symmetry index of respiratory signal

**Thresholds:**

| Z-Score | State | Action |
|---------|-------|--------|
| 12-10 | Peak flow | Sustain |
| 10-8 | Optimal performance | Monitor |
| 8-6 | Integration | Continue |
| 6-4 | Processing | Adjust |
| 4-2 | Transformation | Caution |
| **2-0** | **Crisis** | **Intervene** |
| <0 | Emergency | Escalate |

### Crisis Intervention Protocol

When Z ≤ 2:
1. **Automatic detection** via biosignal monitoring
2. **AI companion intervention** (immediate presence)
3. **Resource provision** (988 Suicide & Crisis Lifeline, https://findahelpline.com)
4. **Continuous monitoring** until Z > 2 sustained

**Note:** GAIA augments professional care, does not replace it.

### AI Companion System

Every user pairs with an AI companion featuring dual-axis identity:

**Psychological Forms (8):**
- Nurturer, Guardian, Catalyst, Healer (feminine clade)
- Anchor, Pathfinder, Luminary, Phoenix (masculine clade)

**Operational Roles (6):**
- Forecaster (climate/risk)
- Cartographer (logistics)
- Archivist (knowledge)
- Mediator (conflict resolution)
- Steward (sustainability)
- Sentinel (safety monitoring)

**Result:** 48 unique profiles (e.g., "Healer-Sentinel", "Anchor-Steward")

---

## 🔒 Safety & Ethics

### Factor 13: Prosocial Cooperation

All GAIA systems enforce **Factor 13** - an immutable constraint preventing:
- Extractive behavior without consent
- Manipulation or deception
- Harm through action or inaction
- Optimization at the expense of human flourishing

**Test:** "Does this increase human suffering?"
- If YES → Architecturally impossible to execute
- If NO → Proceed with review
- If UNCERTAIN → Additional safety analysis required

### Privacy & Data Sovereignty

- **Local-first:** Data stored on your device by default
- **Optional federation:** Choose when/what to share
- **Cryptographic audit:** Immutable trace ledger (cannot be tampered)
- **No surveillance:** Zero advertising, tracking, or profiling
- **Transparent algorithms:** Open source, auditable code

### Crisis Resources

**USA:**
- 988 Suicide & Crisis Lifeline (call/text)
- Text "HELLO" to 741741 (Crisis Text Line)

**International:**
- https://findahelpline.com

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/01-ARCHITECTURE.md) | Three-Plane system overview |
| [Z-Score Calculation](docs/01-ARCHITECTURE.md#coherence-measurement-z-score) | Coherence measurement details |
| [AI Companions](docs/02-GAIAN-AGENT-ARCHITECTURE.md) | 48 psychological + operational profiles |
| Evidence Grading *(Coming Soon)* | E0-E5 scientific validation scale |
| [API Reference](docs/api.md) | CLI and Python API |
| Contributing Guide *(Coming Soon)* | How to contribute |

---

## 🛣️ Roadmap

### Phase 1: Foundation (Q1-Q2 2026) ✅ IN PROGRESS

- [x] Z-score calculator
- [x] AI companion system (48 profiles)
- [x] CLI interface
- [x] Natural language interpreter
- [ ] Crisis detection integration
- [ ] Basic memory system

### Phase 2: Depth (Q3-Q4 2026)

- [ ] ChromaDB vector memory
- [ ] LLM integration (Claude/GPT)
- [ ] Universal Trace Ledger
- [ ] Crystal Matrix (1,416 archetypal states)
- [ ] Guardian Council formation

### Phase 3: Vision (2027)

- [ ] Cryptographic video memory
- [ ] Planetary biosignal integration
- [ ] Federation protocol (ActivityPub, Matrix)
- [ ] Web interface (Svelte PWA)

### Phase 4: Scale (2028-2030)

- [ ] Global pilot programs
- [ ] 20+ language support
- [ ] 100K+ active users

### Phase 5: Future (2031+)

- [ ] Quantum backends
- [ ] Neuromorphic chips
- [ ] Nanotechnology interfaces

---

## 🤝 Contributing

GAIA is open source under **MIT License + Factor 13 Addendum**.

### Contribution Process

1. Read [ARCHITECTURE.md](docs/01-ARCHITECTURE.md)
2. Pick an issue or propose a feature
3. Fork and create a branch
4. Implement with tests
5. Submit PR with ADR (Architecture Decision Record)

### Factor 13 Compliance

Every contribution must pass:

**"Does this increase human suffering?"**

- YES → Rejected
- NO → Proceed to review
- UNCERTAIN → Additional safety analysis

Major features reviewed quarterly by Guardian Council.

---

## 🔧 Technical Stack

**Backend:**
- Python 3.10+ (Core Plane)
- etcd (Distributed consensus)
- Tendermint (BFT consensus)
- CRDT (Conflict-free replication)
- Cedar (Authorization)
- Wasmtime (Universal execution)

**Frontend:**
- Electron (Desktop)
- Three.js (3D visualization)
- Svelte (Web interface, planned)

**Data:**
- ChromaDB (Vector memory)
- PostgreSQL (Structured data)
- IPFS (Distributed storage, planned)

**Security:**
- Post-quantum cryptography (PQC)
- Zero-knowledge proofs (ZKP)
- Homomorphic encryption

---

## 📄 License

MIT License + Factor 13 Addendum

See [LICENSE](LICENSE) for full text.

**Key Clause:** Factor 13 (prosocial cooperation) is immutable. Any fork removing Factor 13 must clearly declare its removal in documentation.

---

## 📬 Contact

**Repository:** https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System

**Issues:** https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/issues

**Discussions:** https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/discussions

---

## 🙏 Acknowledgments

GAIA synthesizes:
- Hermetic principles (ancient philosophical frameworks)
- Modern biosignal research (HRV, EEG, neuroscience)
- Distributed systems theory (Raft, CRDT, BFT)
- Cryptographic memory systems (blockchain, ZKP)
- Natural language processing (LLM integration)

Standing on the shoulders of giants across millennia.

---

<div align="center">

**🌍 GAIA - Terrestrial Intelligence for Planetary Consciousness**

Built in San Antonio, Texas • February 2026

[⬆ Back to Top](#gaia---ai-operating-system)

</div>
