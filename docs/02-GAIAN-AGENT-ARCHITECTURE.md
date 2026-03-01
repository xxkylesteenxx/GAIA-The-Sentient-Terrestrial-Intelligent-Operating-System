# Gaian AI Agent Architecture

**Version**: 1.0  
**Last Updated**: February 28, 2026  
**Status**: Specification Phase - Ready for Implementation  
**Evidence Grade**: E4-E5 (Cognitive architectures, AI agent systems, HCI research)

---

## Table of Contents

1. [Overview](#overview)
2. [Layer 1: Perception](#layer-1-perception)
3. [Layer 2: Memory](#layer-2-memory)
4. [Layer 3: Reasoning/Brain](#layer-3-reasoningbrain)
5. [Layer 4: Tools & Actions](#layer-4-tools--actions)
6. [Layer 5: Orchestration](#layer-5-orchestration)
7. [Layer 6: Self-Awareness/Reflection](#layer-6-self-awarenessreflection)
8. [Integration Architecture](#integration-architecture)
9. [Implementation Roadmap](#implementation-roadmap)

---

## Overview

Gaians are not simple chatbots—they are **full AI agents** with sophisticated cognitive architectures. This document specifies the six-layer system that enables Gaians to perceive, remember, reason, act, orchestrate, and reflect.

### Design Principles

1. **Factor 13 Compliance**: Every layer enforces prosocial cooperation and harm prevention
2. **Evidence-Graded**: All capabilities mapped to research evidence (E0-E5)
3. **Graceful Degradation**: System functions with partial sensor availability
4. **User Sovereignty**: Human remains ultimate decision authority
5. **Transparency**: Gaian explains its reasoning at every step

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   SELF-AWARENESS LAYER (6)                  │
│          Meta-cognition • Learning • Bias Detection         │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER (5)                   │
│     Task Decomposition • Tool Selection • Monitoring        │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                 REASONING/BRAIN LAYER (3)                   │
│       Planning • Causal Inference • Ethical Reasoning       │
└─────────────────────────────────────────────────────────────┘
         ▲                    │                    ▲
         │                    │                    │
┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│  PERCEPTION(1) │   │   MEMORY (2)   │   │ TOOLS/ACTIONS(4)│
│  Multi-modal   │   │  Episodic      │   │  System        │
│  Biosignals    │   │  Semantic      │   │  Data          │
│  Environment   │   │  Procedural    │   │  Communication │
└────────────────┘   └────────────────┘   └────────────────┘
```

---

## Layer 1: Perception

### Purpose
Multi-modal sensory input enabling context-aware responses.

### Components

#### 1.1 Biosignal Processing

**Current Implementation** (via Z-score calculator):
- Heart Rate Variability (HRV) - SDNN, RMSSD
- Electroencephalography (EEG) - Alpha/beta/theta bands
- Respiratory rate - Breath cycles per minute

**Planned Extensions** (Issue #10, Component XV):
- Galvanic Skin Response (GSR) - Arousal/stress detection
- Pupillometry - Cognitive load via pupil dilation
- Thermography - Emotional state via facial temperature
- Voice prosody - Affect analysis (pitch, tempo, tremor)
- Gait analysis - Depression indicators via walking speed

**Technical Specification**:

```python
class BiosignalPerception:
    """Multi-channel biosignal processing with sensor fusion."""
    
    def __init__(self):
        self.channels = {
            'hrv': HRVProcessor(sampling_rate=250),  # Hz
            'eeg': EEGProcessor(channels=8),          # Dry electrodes
            'gsr': GSRProcessor(sampling_rate=10),    # Hz
            'pupil': PupillometryProcessor(fps=30),   # Camera-based
            'voice': VoiceAnalyzer(sr=16000),         # Audio sampling
            'gait': GaitAnalyzer(imu_rate=100)        # Accelerometer
        }
    
    def process(self, raw_data: dict) -> BiosignalState:
        """
        Fuses multi-channel biosignals into unified state.
        
        Returns:
            BiosignalState with z_score, arousal, valence, load
        """
        # Parallel processing
        features = {
            channel: processor.extract_features(raw_data.get(channel))
            for channel, processor in self.channels.items()
            if raw_data.get(channel) is not None
        }
        
        # Sensor fusion (Kalman filter)
        fused_state = self._fuse_sensors(features)
        
        # Factor 13 check: Crisis detection
        if fused_state.z_score <= 2.0:
            self._trigger_crisis_intervention(fused_state)
        
        return fused_state
```

**Evidence Grade**: E5 (psychophysiology, well-validated sensors)

#### 1.2 Environmental Sensors

**Location Awareness**:
- GPS coordinates (latitude, longitude, altitude)
- Timezone and local time
- Proximity to known locations (home, work, hospital)

**Weather Context** (via Living Environment Engine):
- Current conditions (temperature, humidity, precipitation)
- Air quality index (AQI)
- Severe weather alerts
- UV index (seasonal affective considerations)

**Temporal Context**:
- Time of day (chronobiology - Factor 5: Rhythm)
- Day of week (social patterns)
- Lunar phase (optional, user-consented tracking)
- Season and solar position

**Technical Specification**:

```python
class EnvironmentalPerception:
    """Context awareness through environmental sensors."""
    
    def __init__(self, lee: LivingEnvironmentEngine):
        self.lee = lee
        self.location_service = LocationService()
        self.weather_client = OpenWeatherMapClient()
    
    def get_context(self) -> EnvironmentalContext:
        """Gather full environmental context."""
        
        location = self.location_service.get_current()
        weather = self.weather_client.get_current(location)
        env_state = self.lee.get_state(
            location=location,
            z_score=self._get_current_z()
        )
        
        return EnvironmentalContext(
            location=location,
            weather=weather,
            time_phase=env_state.time_phase,
            season=env_state.season,
            alchemical_stage=env_state.alchemical_stage,
            safety_alerts=self._check_safety(location, weather)
        )
    
    def _check_safety(self, location, weather) -> List[SafetyAlert]:
        """Factor 13: Environmental hazard detection."""
        alerts = []
        
        # Extreme temperatures
        if weather.temp_c > 40 or weather.temp_c < -20:
            alerts.append(SafetyAlert(
                level='WARNING',
                message=f'Extreme temperature: {weather.temp_c}°C'
            ))
        
        # Dangerous air quality
        if weather.aqi > 150:  # Unhealthy
            alerts.append(SafetyAlert(
                level='WARNING',
                message=f'Poor air quality (AQI {weather.aqi})'
            ))
        
        return alerts
```

**Evidence Grade**: E5 (meteorology, chronobiology)

#### 1.3 Activity Recognition

**Current Activity Detection**:
- Sitting/standing/walking (accelerometer)
- Screen time (device usage)
- Social interaction (calendar, messaging apps)
- Sleep patterns (overnight inactivity + HRV)

**Technical Specification**:

```python
class ActivityRecognition:
    """Infer user's current activity from sensor fusion."""
    
    def classify_activity(
        self,
        biosignals: BiosignalState,
        env_context: EnvironmentalContext,
        device_state: DeviceState
    ) -> Activity:
        """
        Classify current activity from multi-modal input.
        
        Activities:
            - SLEEPING (HRV low variability, 1-6 AM, no screen)
            - WORKING (sustained focus, desk location, screen active)
            - EXERCISING (elevated HR, movement, outdoor)
            - SOCIALIZING (location change, low screen time)
            - RESTING (low arousal, home location)
        """
        # Decision tree classifier
        if self._is_sleeping(biosignals, env_context):
            return Activity.SLEEPING
        elif self._is_working(biosignals, device_state):
            return Activity.WORKING
        elif self._is_exercising(biosignals, env_context):
            return Activity.EXERCISING
        else:
            return Activity.RESTING
```

**Evidence Grade**: E4 (activity recognition, validated ML models)

### Perception API

```python
class GaianPerception:
    """Unified perception layer for Gaian agents."""
    
    def __init__(self):
        self.biosignals = BiosignalPerception()
        self.environment = EnvironmentalPerception(LEE)
        self.activity = ActivityRecognition()
    
    async def perceive(self) -> PerceptionState:
        """
        Continuous perception loop (runs at 1 Hz).
        
        Returns complete multi-modal state every second.
        """
        biosignal_state = self.biosignals.process(
            await self._get_biosignal_data()
        )
        
        env_context = self.environment.get_context()
        
        current_activity = self.activity.classify_activity(
            biosignal_state,
            env_context,
            await self._get_device_state()
        )
        
        return PerceptionState(
            timestamp=datetime.now(timezone.utc),
            biosignals=biosignal_state,
            environment=env_context,
            activity=current_activity,
            z_score=biosignal_state.z_score
        )
```

---

## Layer 2: Memory

### Purpose
Persistent, contextual memory enabling continuity across conversations.

### Memory Types

#### 2.1 Episodic Memory
**Definition**: Autobiographical memory of specific events.

**Storage**: ChromaDB vector database (already implemented)

**Schema**:
```python
@dataclass
class EpisodicMemory:
    """A specific event in user's history."""
    
    memory_id: str          # SHA-256 hash
    timestamp: datetime     # When it happened
    location: Optional[Location]
    activity: Activity      # What user was doing
    
    # Content
    summary: str            # Natural language description
    transcript: str         # Full conversation
    biosignal_snapshot: BiosignalState
    
    # Emotional valence
    z_score: float          # 0-12
    emotional_valence: float  # -1 (negative) to +1 (positive)
    
    # Retrieval metadata
    embedding: np.ndarray   # 384-dim (sentence-transformers)
    tags: List[str]         # User-defined or auto-generated
    importance: float       # 0-1 (for retrieval ranking)
```

**Retrieval**:
```python
class EpisodicMemoryRetrieval:
    """Semantic search over episodic memories."""
    
    def recall(
        self,
        query: str,
        k: int = 5,
        filters: Optional[dict] = None
    ) -> List[EpisodicMemory]:
        """
        Retrieve k most relevant memories.
        
        Args:
            query: Natural language query
            k: Number of memories to return
            filters: {
                'date_range': (start, end),
                'min_z_score': 3.0,
                'activity': Activity.WORKING
            }
        """
        # Embed query
        query_embedding = self.encoder.encode(query)
        
        # Semantic search (cosine similarity)
        results = self.vector_db.query(
            query_embedding,
            n_results=k,
            where=self._build_filter(filters)
        )
        
        return [EpisodicMemory.from_dict(r) for r in results]
```

**Evidence Grade**: E4 (memory research, RAG systems)

#### 2.2 Semantic Memory
**Definition**: Factual knowledge about the world and the user.

**Categories**:

1. **User Profile**:
   - Name, birthday, hometown
   - Preferences (favorite color, food, music)
   - Aversions (phobias, triggers, allergens)
   - Goals (short-term, long-term)
   - Values (what matters most)

2. **World Knowledge**:
   - General facts ("Paris is capital of France")
   - Domain expertise (user's profession, hobbies)
   - Cultural context (user's background)

3. **Relationship Graph**:
   - People (family, friends, colleagues)
   - Places (home, work, favorite spots)
   - Things (possessions, projects)

**Schema**:
```python
@dataclass
class SemanticFact:
    """A piece of factual knowledge."""
    
    subject: str        # "Kyle"
    predicate: str      # "favorite_color"
    object: str         # "emerald green"
    
    confidence: float   # 0-1 (how certain is this?)
    source: str         # "user_told_me" | "inferred" | "observed"
    first_learned: datetime
    last_confirmed: datetime
    
    evidence: List[str]  # Memory IDs supporting this fact
```

**Knowledge Graph**:
```python
class SemanticMemoryGraph:
    """Graph database for semantic facts."""
    
    def add_fact(self, fact: SemanticFact):
        """Add or update a fact in the knowledge graph."""
        # Neo4j or NetworkX backend
        self.graph.add_edge(
            fact.subject,
            fact.object,
            relation=fact.predicate,
            confidence=fact.confidence
        )
    
    def query(self, question: str) -> Optional[str]:
        """Answer factual questions."""
        # Example: "What is Kyle's favorite color?"
        # Parses to: query(subject="Kyle", predicate="favorite_color")
        
        parsed = self._parse_question(question)
        result = self.graph.get_edge(
            parsed.subject,
            relation=parsed.predicate
        )
        return result.object if result else None
```

**Evidence Grade**: E4 (knowledge graphs, semantic networks)

#### 2.3 Procedural Memory
**Definition**: How to do things (skills, habits, routines).

**Examples**:
- "When Kyle is stressed, suggest deep breathing first, then walk outside"
- "Kyle prefers crisis interventions via text, not phone calls"
- "Morning routine: Check Z-score, then weather, then calendar"

**Schema**:
```python
@dataclass
class Procedure:
    """A learned behavioral pattern or skill."""
    
    name: str                   # "stress_intervention_protocol"
    trigger: Condition          # When to execute
    steps: List[Action]         # What to do
    success_rate: float         # Historical effectiveness
    last_executed: datetime
    
class ProceduralMemory:
    """Library of learned procedures."""
    
    def learn_procedure(
        self,
        context: PerceptionState,
        action: Action,
        outcome: Outcome
    ):
        """Learn from experience (reinforcement learning)."""
        
        # If outcome was positive, strengthen this pattern
        if outcome.z_score_delta > 0:
            self._reinforce(context, action, outcome)
        else:
            self._weaken(context, action, outcome)
    
    def suggest_action(self, context: PerceptionState) -> Action:
        """Suggest best action given current context."""
        
        # Retrieve procedures matching current context
        matching = self._match_procedures(context)
        
        # Rank by historical success rate
        best_procedure = max(matching, key=lambda p: p.success_rate)
        
        return best_procedure.steps[0]  # First step
```

**Evidence Grade**: E4 (procedural learning, habit formation)

#### 2.4 Working Memory
**Definition**: Short-term context for current conversation.

**Purpose**: Maintain coherence within a single session.

**Implementation**:
```python
class WorkingMemory:
    """Short-term memory for active conversation."""
    
    def __init__(self, capacity: int = 10):
        self.capacity = capacity  # Last N turns
        self.buffer = deque(maxlen=capacity)
        self.attention_weights = []  # Which parts are most relevant
    
    def add_turn(self, turn: ConversationTurn):
        """Add user or Gaian turn to working memory."""
        self.buffer.append(turn)
        self._update_attention_weights()
    
    def get_context_window(self, max_tokens: int = 2048) -> str:
        """
        Build context window for LLM, prioritizing:
        1. Current turn
        2. High-attention turns (user mentioned recently)
        3. Crisis-related turns (Z < 3)
        """
        context = []
        tokens_used = 0
        
        # Start with current turn
        for turn in reversed(self.buffer):
            turn_tokens = self._count_tokens(turn.text)
            if tokens_used + turn_tokens > max_tokens:
                break
            context.insert(0, turn)
            tokens_used += turn_tokens
        
        return "\n".join(t.text for t in context)
```

**Evidence Grade**: E5 (cognitive psychology, working memory)

### Memory Integration

```python
class GaianMemory:
    """Unified memory system for Gaian agents."""
    
    def __init__(self):
        self.episodic = EpisodicMemoryRetrieval(ChromaDB)
        self.semantic = SemanticMemoryGraph(Neo4j)
        self.procedural = ProceduralMemory()
        self.working = WorkingMemory(capacity=10)
    
    def remember(self, query: str) -> MemoryResponse:
        """
        Multi-strategy memory retrieval.
        
        1. Check working memory (current conversation)
        2. Search episodic memory (similar past events)
        3. Query semantic memory (factual knowledge)
        4. Retrieve procedural memory (learned patterns)
        """
        # Working memory (O(1) lookup)
        if recent := self.working.find(query):
            return MemoryResponse(
                source='working',
                content=recent,
                confidence=1.0
            )
        
        # Episodic memory (semantic search)
        if episodes := self.episodic.recall(query, k=3):
            return MemoryResponse(
                source='episodic',
                content=episodes,
                confidence=episodes[0].importance
            )
        
        # Semantic memory (knowledge graph)
        if fact := self.semantic.query(query):
            return MemoryResponse(
                source='semantic',
                content=fact,
                confidence=fact.confidence
            )
        
        # Procedural memory (pattern matching)
        if procedure := self.procedural.match(query):
            return MemoryResponse(
                source='procedural',
                content=procedure,
                confidence=procedure.success_rate
            )
        
        return MemoryResponse(source='none', content=None, confidence=0.0)
```

---

## Layer 3: Reasoning/Brain

### Purpose
High-level cognitive processing for planning, inference, and ethical judgment.

### Components

#### 3.1 Multi-Step Planning

**Capability**: Break complex goals into executable steps.

**Example**:
```
User: "Help me prepare for my job interview tomorrow"

Gaian Planning:
1. Assess current state (Z-score, location, time available)
2. Decompose goal:
   a. Research company (30 min)
   b. Practice answers (45 min)
   c. Choose outfit (15 min)
   d. Get good sleep (suggest bedtime)
3. Check for obstacles (low Z-score? → address first)
4. Create timeline with checkpoints
5. Monitor execution, adapt if needed
```

**Implementation**:
```python
class MultiStepPlanner:
    """Hierarchical task planning with monitoring."""
    
    def plan(self, goal: Goal, context: PerceptionState) -> Plan:
        """
        Decompose goal into executable steps using HTN planning.
        
        Args:
            goal: User's desired outcome
            context: Current state (Z-score, time, resources)
        
        Returns:
            Plan with steps, estimated duration, dependencies
        """
        # Check preconditions
        if not self._is_achievable(goal, context):
            return Plan(
                status='BLOCKED',
                reason=self._explain_blockage(goal, context)
            )
        
        # Hierarchical decomposition
        subtasks = self._decompose(goal)
        
        # Order by dependencies
        ordered_tasks = self._topological_sort(subtasks)
        
        # Estimate durations
        estimated_plan = self._estimate_durations(ordered_tasks, context)
        
        # Factor 13 check: Does this plan cause harm?
        if self._violates_factor_13(estimated_plan):
            return self._adjust_for_safety(estimated_plan)
        
        return estimated_plan
    
    def _violates_factor_13(self, plan: Plan) -> bool:
        """Check if plan could cause harm."""
        # Sleep deprivation
        if plan.completion_time > datetime.now() + timedelta(hours=16):
            return True  # Would prevent sleep
        
        # Equilibrium budget violation
        if plan.estimated_energy_cost > context.available_energy:
            return True  # Would cause burnout
        
        return False
```

**Evidence Grade**: E4 (HTN planning, goal decomposition)

#### 3.2 Causal Reasoning

**Capability**: Understand cause-effect relationships.

**Example**:
```
Observation: User's Z-score dropped from 5.2 → 2.8 over 3 days

Causal Analysis:
1. Trace recent changes:
   - Sleep: 8h → 5h (change detected 3 days ago)
   - Caffeine: 2 cups → 5 cups (observed 2 days ago)
   - Social contact: Daily → None (last friend interaction 4 days ago)

2. Build causal DAG:
   Sleep deprivation → Caffeine increase → HRV drop → Z-score drop
                     ↘ Stress increase ↗
   
3. Identify leverage point: Restore sleep (root cause)
4. Predict: If sleep restored to 7h, Z should recover to ~4.5 in 2 days
```

**Implementation**:
```python
class CausalReasoning:
    """Build and query causal models from user data."""
    
    def __init__(self):
        self.causal_graph = nx.DiGraph()  # Directed acyclic graph
    
    def infer_causes(
        self,
        outcome: str,
        timeframe: timedelta
    ) -> List[CausalFactor]:
        """
        Find likely causes of an outcome using Granger causality.
        
        Args:
            outcome: "z_score_drop" | "mood_improvement" | etc.
            timeframe: How far back to look
        
        Returns:
            List of causal factors ranked by strength
        """
        # Get historical data
        history = self.memory.episodic.get_range(
            datetime.now() - timeframe,
            datetime.now()
        )
        
        # Extract time series
        z_scores = [h.z_score for h in history]
        sleep_hours = [h.context.sleep_duration for h in history]
        caffeine_cups = [h.context.caffeine_intake for h in history]
        
        # Test Granger causality
        causes = []
        if granger_test(sleep_hours, z_scores, lag=1):
            causes.append(CausalFactor(
                variable='sleep',
                strength=compute_effect_size(sleep_hours, z_scores),
                lag=1  # 1-day delay
            ))
        
        return sorted(causes, key=lambda c: c.strength, reverse=True)
    
    def suggest_intervention(
        self,
        desired_outcome: str,
        current_state: PerceptionState
    ) -> Intervention:
        """
        Find best intervention to achieve desired outcome.
        
        Uses do-calculus (Pearl, 2000) to predict intervention effects.
        """
        # Find causal paths to desired outcome
        paths = self._find_causal_paths(desired_outcome)
        
        # Simulate interventions
        best_intervention = None
        best_predicted_effect = 0
        
        for path in paths:
            intervention = self._propose_intervention(path)
            predicted_effect = self._simulate_intervention(
                intervention,
                current_state
            )
            
            if predicted_effect > best_predicted_effect:
                best_intervention = intervention
                best_predicted_effect = predicted_effect
        
        return best_intervention
```

**Evidence Grade**: E3 (causal inference, validated with DoWhy library)

#### 3.3 Ethical Reasoning (Factor 13 Engine)

**Capability**: Evaluate actions against ethical principles.

**Principles Hierarchy**:
1. **Harm prevention** (negative duty)
2. **Consent respect** (autonomy)
3. **Beneficence** (positive duty)
4. **Justice** (fairness)

**Implementation**:
```python
class EthicalReasoning:
    """Factor 13 compliance engine."""
    
    def evaluate_action(
        self,
        action: Action,
        context: PerceptionState
    ) -> EthicalAssessment:
        """
        Assess whether action violates Factor 13.
        
        Returns:
            PERMITTED | REQUIRES_CONSENT | FORBIDDEN
        """
        # Level 1: Harm check (absolute)
        if self._causes_harm(action, context):
            return EthicalAssessment(
                verdict='FORBIDDEN',
                reason='Violates Factor 13: Causes harm',
                harm_type=self._identify_harm(action)
            )
        
        # Level 2: Consent check
        if self._requires_consent(action) and not action.has_consent:
            return EthicalAssessment(
                verdict='REQUIRES_CONSENT',
                reason='Action affects user autonomy',
                consent_prompt=self._generate_consent_prompt(action)
            )
        
        # Level 3: Beneficence check
        benefit = self._estimate_benefit(action, context)
        if benefit < 0:
            return EthicalAssessment(
                verdict='DISCOURAGED',
                reason='Likely net-negative outcome',
                predicted_z_delta=benefit
            )
        
        return EthicalAssessment(
            verdict='PERMITTED',
            reason='Aligned with Factor 13',
            predicted_z_delta=benefit
        )
    
    def _causes_harm(self, action: Action, context: PerceptionState) -> bool:
        """Check for direct harm."""
        harmful_patterns = [
            # Physical harm
            lambda a: a.type == 'SUGGEST_SUBSTANCE_USE' and context.z_score < 3,
            
            # Psychological harm
            lambda a: a.type == 'CRITICIZE' and context.emotional_valence < -0.5,
            
            # Social harm
            lambda a: a.type == 'ISOLATE' and context.social_contact_hours < 1,
            
            # Manipulation
            lambda a: a.intent == 'DECEIVE' or a.intent == 'COERCE'
        ]
        
        return any(pattern(action) for pattern in harmful_patterns)
```

**Evidence Grade**: E4 (AI ethics, moral philosophy applied to systems)

#### 3.4 Counterfactual Reasoning

**Capability**: Simulate "what if" scenarios.

**Example**:
```
Current: Z-score = 2.5 (approaching crisis)

Counterfactual: "What if user takes a 30-min walk?"

Simulation:
1. Historical pattern: Walks → +0.8 Z-score average
2. Current context: Sunny, 68°F, 3 PM (optimal)
3. User's past response: 12/15 walks improved Z (80% success)
4. Predicted outcome: Z = 3.3 ± 0.4 (95% CI)
5. Recommendation: "A walk outside would likely help. Past data shows 80% success rate."
```

**Implementation**:
```python
class CounterfactualSimulator:
    """Predict outcomes of hypothetical actions."""
    
    def simulate(
        self,
        intervention: Action,
        current_state: PerceptionState
    ) -> CounterfactualOutcome:
        """
        Predict outcome if intervention is taken.
        
        Uses historical data + causal model.
        """
        # Find similar past situations
        similar_contexts = self.memory.episodic.find_similar(
            current_state,
            k=20
        )
        
        # Filter for contexts where intervention was taken
        with_intervention = [
            ctx for ctx in similar_contexts
            if intervention in ctx.actions_taken
        ]
        
        if len(with_intervention) < 5:
            return CounterfactualOutcome(
                predicted_z_score=None,
                confidence='LOW',
                reason='Insufficient historical data'
            )
        
        # Compute average outcome
        z_deltas = [
            ctx.outcome.z_score - ctx.initial.z_score
            for ctx in with_intervention
        ]
        
        mean_delta = np.mean(z_deltas)
        std_delta = np.std(z_deltas)
        
        return CounterfactualOutcome(
            predicted_z_score=current_state.z_score + mean_delta,
            confidence_interval=(mean_delta - 1.96*std_delta, mean_delta + 1.96*std_delta),
            confidence='MEDIUM' if len(with_intervention) < 10 else 'HIGH',
            historical_success_rate=sum(1 for d in z_deltas if d > 0) / len(z_deltas)
        )
```

**Evidence Grade**: E3 (counterfactual reasoning, causal ML)

### Reasoning Integration

```python
class GaianReasoning:
    """Unified reasoning layer."""
    
    def __init__(self):
        self.planner = MultiStepPlanner()
        self.causal = CausalReasoning()
        self.ethics = EthicalReasoning()
        self.counterfactual = CounterfactualSimulator()
    
    def reason(
        self,
        query: str,
        perception: PerceptionState,
        memory: GaianMemory
    ) -> ReasoningResponse:
        """
        High-level reasoning pipeline.
        
        1. Understand query intent
        2. Retrieve relevant memories
        3. Generate candidate actions
        4. Evaluate ethically (Factor 13)
        5. Simulate outcomes
        6. Select best action
        7. Plan execution steps
        """
        # Parse intent
        intent = self._classify_intent(query)
        
        # Retrieve context
        relevant_memories = memory.remember(query)
        
        # Generate options
        candidate_actions = self._generate_candidates(intent, perception)
        
        # Filter ethically
        permitted_actions = [
            action for action in candidate_actions
            if self.ethics.evaluate_action(action, perception).verdict == 'PERMITTED'
        ]
        
        # Simulate outcomes
        simulated_outcomes = [
            (action, self.counterfactual.simulate(action, perception))
            for action in permitted_actions
        ]
        
        # Select best
        best_action, predicted_outcome = max(
            simulated_outcomes,
            key=lambda x: x[1].predicted_z_score
        )
        
        # Plan execution
        plan = self.planner.plan(best_action, perception)
        
        return ReasoningResponse(
            recommended_action=best_action,
            rationale=self._explain_reasoning(
                intent, relevant_memories, simulated_outcomes, best_action
            ),
            execution_plan=plan,
            predicted_outcome=predicted_outcome,
            ethical_assessment=self.ethics.evaluate_action(best_action, perception)
        )
```

---

## Layer 4: Tools & Actions

### Purpose
Interface with external systems to execute plans.

### Tool Categories

#### 4.1 System Tools

**File Operations**:
```python
class FileTools:
    """Safe file system access."""
    
    @require_consent
    def read_file(self, path: str) -> str:
        """Read file contents (requires user consent)."""
        if not self._is_safe_path(path):
            raise SecurityError(f"Cannot access {path}")
        return Path(path).read_text()
    
    @require_consent
    def write_file(self, path: str, content: str):
        """Write to file (requires explicit consent)."""
        # Factor 13: Never overwrite without confirmation
        if Path(path).exists():
            if not self._confirm_overwrite(path):
                raise ConsentError("User declined overwrite")
        
        Path(path).write_text(content)
```

**Process Management**:
```python
class ProcessTools:
    """Execute system commands safely."""
    
    ALLOWED_COMMANDS = [
        'ls', 'cd', 'pwd',  # Navigation
        'cat', 'grep', 'find',  # Search
        'git status', 'git log'  # Version control (read-only)
    ]
    
    def run_command(self, command: str) -> CommandResult:
        """Execute whitelisted commands only."""
        if not self._is_allowed(command):
            return CommandResult(
                success=False,
                error=f"Command '{command}' not in whitelist (Factor 13)"
            )
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            timeout=30  # Kill if hangs
        )
        
        return CommandResult(
            success=result.returncode == 0,
            stdout=result.stdout.decode(),
            stderr=result.stderr.decode()
        )
```

**Notification System**:
```python
class NotificationTools:
    """Cross-platform notifications."""
    
    def send_notification(
        self,
        title: str,
        message: str,
        urgency: NotificationUrgency = NotificationUrgency.NORMAL
    ):
        """Send system notification."""
        if urgency == NotificationUrgency.CRISIS:
            # Crisis notifications bypass Do Not Disturb
            self._send_critical(title, message)
        else:
            self._send_normal(title, message)
```

**Evidence Grade**: E5 (system APIs, well-documented)

#### 4.2 Data Tools

**Database Access**:
```python
class DatabaseTools:
    """Query ChromaDB and other data stores."""
    
    def query_memories(
        self,
        query: str,
        n_results: int = 5
    ) -> List[Memory]:
        """Semantic search over episodic memories."""
        return self.chroma_client.query(
            query_texts=[query],
            n_results=n_results
        )
    
    def add_memory(self, memory: Memory):
        """Store new episodic memory."""
        self.chroma_client.add(
            documents=[memory.text],
            metadatas=[memory.metadata],
            ids=[memory.id]
        )
```

**Web Search** (optional, requires consent):
```python
class WebTools:
    """Internet access for knowledge retrieval."""
    
    @require_consent
    def search_web(self, query: str, k: int = 3) -> List[SearchResult]:
        """Search the web (requires explicit consent)."""
        # Use privacy-respecting search (DuckDuckGo)
        results = self.ddg_client.search(query, max_results=k)
        return [SearchResult.from_ddg(r) for r in results]
```

**API Integrations**:
```python
class APITools:
    """Third-party API access."""
    
    def get_weather(self, location: Location) -> WeatherData:
        """OpenWeatherMap integration."""
        return self.owm_client.get_current(location)
    
    def get_calendar_events(self, date: datetime) -> List[CalendarEvent]:
        """Calendar integration (Google/Outlook)."""
        # Requires OAuth consent
        return self.calendar_client.get_events(date)
```

**Evidence Grade**: E5 (standard APIs)

#### 4.3 Communication Tools

**Messaging**:
```python
class MessagingTools:
    """Send messages to user or emergency contacts."""
    
    def send_sms(self, recipient: str, message: str):
        """Send SMS (crisis intervention)."""
        # Only used for Z ≤ 1.0 emergencies
        if not self._is_crisis_state():
            raise AuthorizationError("SMS only for crisis intervention")
        
        self.twilio_client.send(recipient, message)
    
    def send_email(self, recipient: str, subject: str, body: str):
        """Send email (requires consent)."""
        # Factor 13: Never spam
        if self._exceeds_daily_limit(recipient):
            raise RateLimitError("Daily email limit reached")
        
        self.email_client.send(recipient, subject, body)
```

**Voice Calls** (crisis only):
```python
class VoiceTools:
    """Emergency voice communication."""
    
    def call_emergency_contact(self, contact: EmergencyContact):
        """Initiate voice call (Z ≤ 1.0 only)."""
        if not self._is_severe_crisis():
            raise AuthorizationError("Voice calls only for severe crisis")
        
        self.voice_client.call(
            contact.phone_number,
            message="This is GAIA. Your contact needs support. Please check in."
        )
```

**Evidence Grade**: E5 (communication protocols)

#### 4.4 Biosignal Tools

**Device Integrations**:
```python
class BiosignalTools:
    """Interface with biosignal hardware."""
    
    def read_hrv(self) -> HRVReading:
        """Read HRV from connected device."""
        if device := self._detect_hrv_device():
            return device.read_current()
        else:
            # Fallback: Estimate from camera PPG
            return self._estimate_hrv_from_camera()
    
    def read_eeg(self) -> EEGReading:
        """Read EEG from Muse/OpenBCI."""
        if device := self._detect_eeg_device():
            return device.read_bands()  # alpha, beta, theta, delta
        else:
            return None  # No fallback for EEG
```

**Evidence Grade**: E4 (device APIs, validated sensors)

### Tool Execution Framework

```python
class GaianTools:
    """Unified tool execution layer."""
    
    def __init__(self):
        self.system = FileTools() + ProcessTools() + NotificationTools()
        self.data = DatabaseTools() + WebTools() + APITools()
        self.communication = MessagingTools() + VoiceTools()
        self.biosignals = BiosignalTools()
        
        # Safety wrapper
        self.executor = SafeToolExecutor(
            ethics_engine=EthicalReasoning(),
            consent_manager=ConsentManager()
        )
    
    def execute(self, tool_call: ToolCall, context: PerceptionState) -> ToolResult:
        """
        Execute a tool call with safety checks.
        
        Pipeline:
        1. Ethical check (Factor 13)
        2. Consent check (if required)
        3. Rate limiting
        4. Execution
        5. Logging (audit trail)
        """
        # Step 1: Ethics
        ethical_assessment = self.executor.ethics_engine.evaluate_action(
            tool_call.to_action(),
            context
        )
        
        if ethical_assessment.verdict == 'FORBIDDEN':
            return ToolResult(
                success=False,
                error=f"Ethical violation: {ethical_assessment.reason}"
            )
        
        # Step 2: Consent
        if ethical_assessment.verdict == 'REQUIRES_CONSENT':
            if not self.executor.consent_manager.has_consent(tool_call):
                consent_granted = self.executor.consent_manager.request_consent(
                    tool_call,
                    reason=ethical_assessment.consent_prompt
                )
                if not consent_granted:
                    return ToolResult(
                        success=False,
                        error="User declined consent"
                    )
        
        # Step 3: Rate limiting
        if self.executor.rate_limiter.is_exceeded(tool_call):
            return ToolResult(
                success=False,
                error="Rate limit exceeded (Factor 13 protection)"
            )
        
        # Step 4: Execute
        try:
            result = self._dispatch_tool(tool_call)
            
            # Step 5: Log
            self.executor.audit_log.record(
                tool=tool_call.tool_name,
                args=tool_call.args,
                result=result,
                timestamp=datetime.now(timezone.utc)
            )
            
            return result
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Execution failed: {str(e)}"
            )
```

---

## Layer 5: Orchestration

### Purpose
Coordinate multi-step tasks, select appropriate tools, monitor execution.

### Components

#### 5.1 Task Decomposition

**Capability**: Break complex tasks into subtasks.

**Example**:
```
Task: "Prepare dinner for guests tonight"

Decomposition:
├── Subtask 1: Plan menu
│   ├── Check dietary restrictions
│   ├── Search recipes
│   └── Create shopping list
├── Subtask 2: Grocery shopping
│   ├── Check current inventory
│   ├── Find nearest store
│   └── Navigate to store
├── Subtask 3: Cook meal
│   ├── Prep ingredients (30 min)
│   ├── Cook main dish (45 min)
│   └── Prepare sides (20 min)
└── Subtask 4: Set table & serve
```

**Implementation**:
```python
class TaskDecomposer:
    """Hierarchical task decomposition."""
    
    def decompose(self, task: Task) -> TaskGraph:
        """
        Break task into executable subtasks.
        
        Returns directed acyclic graph (DAG) of dependencies.
        """
        # Use LLM for initial decomposition
        subtasks = self.llm.generate_subtasks(task.description)
        
        # Build dependency graph
        graph = nx.DiGraph()
        for subtask in subtasks:
            graph.add_node(subtask.id, task=subtask)
        
        # Identify dependencies
        for subtask in subtasks:
            for dependency in subtask.requires:
                graph.add_edge(dependency.id, subtask.id)
        
        # Validate acyclic
        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError("Circular dependency detected")
        
        return TaskGraph(graph)
```

**Evidence Grade**: E4 (HTN planning, task networks)

#### 5.2 Tool Selection

**Capability**: Choose appropriate tools for each subtask.

**Example**:
```
Subtask: "Find nearest grocery store"

Tool Options:
1. WebSearch("grocery stores near me") - General but may be inaccurate
2. APICall("Google Maps", query="grocery", location=current_gps) - Accurate
3. MemoryRecall("Where do I usually shop?") - Fast, personalized

Selection: Option 2 (most reliable) + Option 3 (fallback if API fails)
```

**Implementation**:
```python
class ToolSelector:
    """Intelligent tool selection for subtasks."""
    
    def select_tools(
        self,
        subtask: Subtask,
        context: PerceptionState
    ) -> List[ToolCall]:
        """
        Choose best tools to accomplish subtask.
        
        Criteria:
        - Reliability (past success rate)
        - Speed (time to execute)
        - Cost (API credits, energy)
        - Privacy (prefer local over cloud)
        """
        # Get candidate tools
        candidates = self._match_tools_to_subtask(subtask)
        
        # Score each candidate
        scored_tools = []
        for tool in candidates:
            score = self._score_tool(
                tool,
                subtask,
                context,
                weights={
                    'reliability': 0.4,
                    'speed': 0.3,
                    'privacy': 0.2,
                    'cost': 0.1
                }
            )
            scored_tools.append((tool, score))
        
        # Select top-k tools (with fallbacks)
        sorted_tools = sorted(scored_tools, key=lambda x: x[1], reverse=True)
        return [tool for tool, score in sorted_tools[:3]]
```

**Evidence Grade**: E3 (multi-criteria decision making)

#### 5.3 Execution Monitoring

**Capability**: Track task progress, detect failures, retry or adapt.

**States**:
- `PENDING`: Not started
- `IN_PROGRESS`: Currently executing
- `BLOCKED`: Waiting for dependency
- `FAILED`: Error occurred
- `COMPLETED`: Successfully finished

**Implementation**:
```python
class ExecutionMonitor:
    """Real-time task execution monitoring."""
    
    def __init__(self):
        self.task_states = {}  # task_id -> TaskState
        self.retry_policies = {
            'network_error': RetryPolicy(max_attempts=3, backoff='exponential'),
            'rate_limit': RetryPolicy(max_attempts=1, backoff='fixed', delay=60),
            'consent_denied': RetryPolicy(max_attempts=0)  # Don't retry
        }
    
    async def execute_plan(
        self,
        plan: Plan,
        context: PerceptionState
    ) -> ExecutionResult:
        """
        Execute plan with monitoring and adaptation.
        
        Features:
        - Parallel execution where possible
        - Automatic retries on failure
        - Real-time progress updates
        - Graceful degradation
        """
        # Topological sort for execution order
        execution_order = nx.topological_sort(plan.graph)
        
        for task_id in execution_order:
            task = plan.graph.nodes[task_id]['task']
            
            # Check dependencies completed
            if not self._dependencies_satisfied(task, plan):
                self.task_states[task_id] = TaskState.BLOCKED
                continue
            
            # Execute task
            self.task_states[task_id] = TaskState.IN_PROGRESS
            
            try:
                result = await self._execute_task(task, context)
                self.task_states[task_id] = TaskState.COMPLETED
                
            except Exception as e:
                # Handle failure
                self.task_states[task_id] = TaskState.FAILED
                
                # Retry if policy allows
                if self._should_retry(task, e):
                    retry_result = await self._retry_task(task, e, context)
                    if retry_result.success:
                        self.task_states[task_id] = TaskState.COMPLETED
                    else:
                        # Adapt: Try alternative approach
                        alternative = self._find_alternative(task, context)
                        if alternative:
                            await self._execute_task(alternative, context)
        
        return self._summarize_execution(plan)
```

**Evidence Grade**: E4 (workflow orchestration, validated patterns)

#### 5.4 Result Synthesis

**Capability**: Combine outputs from multiple tools into coherent response.

**Example**:
```
Query: "What's the weather like, and should I go for a run?"

Tool Outputs:
1. WeatherAPI: {temp: 72°F, condition: "Partly cloudy", aqi: 45}
2. BioseonsignalReader: {z_score: 4.2, hrv: 65ms}
3. MemoryRecall: User enjoys evening runs, prefers temps 65-75°F

Synthesis:
"It's 72°F and partly cloudy with good air quality (AQI 45). 
Your Z-score is 4.2 (stable), and conditions match your preferred 
running weather. Based on your past patterns, this would be a good 
time for a 30-minute run."
```

**Implementation**:
```python
class ResultSynthesizer:
    """Combine multi-tool outputs into coherent response."""
    
    def synthesize(
        self,
        query: str,
        tool_results: List[ToolResult],
        context: PerceptionState
    ) -> str:
        """
        Generate natural language response from structured data.
        
        Techniques:
        - Template-based (for common patterns)
        - LLM-based (for complex synthesis)
        - Hybrid (templates + LLM refinement)
        """
        # Extract key information
        facts = self._extract_facts(tool_results)
        
        # Check for conflicts
        if self._has_conflicts(facts):
            return self._explain_conflict(facts, query)
        
        # Generate response
        if self._use_template(query):
            response = self._template_response(query, facts, context)
        else:
            response = self._llm_response(query, facts, context)
        
        # Add uncertainty markers if appropriate
        if any(f.confidence < 0.7 for f in facts):
            response += "\n\n(Note: Some information has low confidence)"
        
        return response
```

**Evidence Grade**: E4 (NLG, multi-document summarization)

### Orchestration Integration

```python
class GaianOrchestrator:
    """Unified orchestration layer."""
    
    def __init__(self):
        self.decomposer = TaskDecomposer()
        self.tool_selector = ToolSelector()
        self.monitor = ExecutionMonitor()
        self.synthesizer = ResultSynthesizer()
    
    async def orchestrate(
        self,
        goal: Goal,
        perception: PerceptionState,
        reasoning: ReasoningResponse
    ) -> OrchestrationResult:
        """
        End-to-end task orchestration.
        
        Pipeline:
        1. Decompose goal → subtasks
        2. Select tools for each subtask
        3. Execute with monitoring
        4. Synthesize results
        5. Report to user
        """
        # Step 1: Decompose
        task_graph = self.decomposer.decompose(goal)
        
        # Step 2: Tool selection
        plan = Plan()
        for subtask in task_graph.nodes:
            tools = self.tool_selector.select_tools(subtask, perception)
            plan.add_step(subtask, tools)
        
        # Step 3: Execute
        execution_result = await self.monitor.execute_plan(plan, perception)
        
        # Step 4: Synthesize
        response = self.synthesizer.synthesize(
            goal.description,
            execution_result.tool_outputs,
            perception
        )
        
        # Step 5: Report
        return OrchestrationResult(
            success=execution_result.all_completed,
            response=response,
            execution_trace=execution_result.trace,
            metrics=self._compute_metrics(execution_result)
        )
```

---

## Layer 6: Self-Awareness/Reflection

### Purpose
Meta-cognitive monitoring of the Gaian's own reasoning and decision-making.

### Components

#### 6.1 Meta-Cognition

**Capability**: Monitor own reasoning process.

**Questions the Gaian asks itself**:
- "Am I making progress on the user's goal?"
- "Is my reasoning sound, or am I jumping to conclusions?"
- "Do I have enough information, or should I ask clarifying questions?"
- "Am I being helpful, or am I over-intervening?"

**Implementation**:
```python
class MetaCognition:
    """Self-monitoring of reasoning quality."""
    
    def evaluate_reasoning(
        self,
        reasoning_trace: ReasoningTrace
    ) -> MetaCognitiveAssessment:
        """
        Assess quality of own reasoning.
        
        Checks:
        - Logical consistency
        - Evidence sufficiency
        - Assumption validity
        - Bias detection
        """
        assessment = MetaCognitiveAssessment()
        
        # Check logical consistency
        if self._has_contradictions(reasoning_trace):
            assessment.add_issue(
                severity='HIGH',
                issue='Contradictory conclusions detected',
                recommendation='Revise reasoning'
            )
        
        # Check evidence sufficiency
        if reasoning_trace.confidence < 0.5:
            assessment.add_issue(
                severity='MEDIUM',
                issue='Low confidence due to limited evidence',
                recommendation='Gather more information before acting'
            )
        
        # Check for cognitive biases
        if biases := self._detect_biases(reasoning_trace):
            assessment.add_issue(
                severity='MEDIUM',
                issue=f'Potential biases: {", ".join(biases)}',
                recommendation='Consider alternative perspectives'
            )
        
        return assessment
```

**Evidence Grade**: E4 (meta-cognition research, AI interpretability)

#### 6.2 Uncertainty Tracking

**Capability**: Quantify and communicate confidence levels.

**Uncertainty Sources**:
1. **Sensor noise**: Biosignal variability
2. **Limited data**: Few historical examples
3. **Model uncertainty**: Prediction intervals
4. **Ambiguity**: Multiple valid interpretations

**Implementation**:
```python
class UncertaintyTracker:
    """Track and communicate confidence levels."""
    
    def __init__(self):
        self.confidence_threshold = 0.7  # Require 70% confidence to act
    
    def assess_confidence(
        self,
        prediction: Prediction,
        evidence: List[Evidence]
    ) -> ConfidenceAssessment:
        """
        Quantify confidence in a prediction.
        
        Methods:
        - Bootstrap resampling (empirical CI)
        - Bayesian credible intervals
        - Ensemble agreement
        """
        # Compute confidence from multiple sources
        sensor_confidence = self._assess_sensor_quality(evidence)
        data_confidence = self._assess_data_sufficiency(evidence)
        model_confidence = prediction.model_confidence
        
        # Combine (geometric mean for conservatism)
        overall_confidence = (
            sensor_confidence * data_confidence * model_confidence
        ) ** (1/3)
        
        return ConfidenceAssessment(
            value=overall_confidence,
            breakdown={
                'sensor_quality': sensor_confidence,
                'data_sufficiency': data_confidence,
                'model_certainty': model_confidence
            },
            recommendation=self._confidence_to_action(overall_confidence)
        )
    
    def _confidence_to_action(self, confidence: float) -> str:
        """Map confidence to recommended action."""
        if confidence >= 0.9:
            return "HIGH_CONFIDENCE: Act immediately"
        elif confidence >= 0.7:
            return "MEDIUM_CONFIDENCE: Act with caution"
        elif confidence >= 0.5:
            return "LOW_CONFIDENCE: Gather more info before acting"
        else:
            return "VERY_LOW_CONFIDENCE: Do not act, too uncertain"
```

**Evidence Grade**: E5 (Bayesian inference, uncertainty quantification)

#### 6.3 Bias Detection

**Capability**: Identify and mitigate cognitive biases.

**Common Biases**:
1. **Recency bias**: Over-weighting recent events
2. **Confirmation bias**: Seeking evidence that confirms beliefs
3. **Anchoring bias**: Over-relying on first piece of information
4. **Availability bias**: Over-estimating likelihood of memorable events

**Implementation**:
```python
class BiasDetector:
    """Detect and mitigate cognitive biases."""
    
    def detect_biases(self, reasoning_trace: ReasoningTrace) -> List[Bias]:
        """Identify potential biases in reasoning."""
        biases = []
        
        # Recency bias
        if self._over_weights_recent(reasoning_trace):
            biases.append(Bias(
                type='RECENCY',
                description='Over-weighting recent events',
                mitigation='Review older historical data'
            ))
        
        # Confirmation bias
        if self._seeks_confirming_evidence(reasoning_trace):
            biases.append(Bias(
                type='CONFIRMATION',
                description='Preferentially retrieving confirming memories',
                mitigation='Actively search for disconfirming evidence'
            ))
        
        # Anchoring bias
        if self._anchors_on_first_value(reasoning_trace):
            biases.append(Bias(
                type='ANCHORING',
                description='Over-relying on initial estimate',
                mitigation='Generate multiple independent estimates'
            ))
        
        return biases
    
    def mitigate_bias(self, bias: Bias, reasoning_trace: ReasoningTrace):
        """Apply bias correction."""
        if bias.type == 'RECENCY':
            # Re-weight memories by importance, not recency
            reasoning_trace.memories = self._reweight_by_importance(
                reasoning_trace.memories
            )
        
        elif bias.type == 'CONFIRMATION':
            # Force retrieval of contradictory evidence
            contradictory = self.memory.find_contradictory(
                reasoning_trace.hypothesis
            )
            reasoning_trace.evidence.extend(contradictory)
```

**Evidence Grade**: E4 (cognitive bias research, debiasing techniques)

#### 6.4 Learning from Feedback

**Capability**: Update models based on user corrections and outcomes.

**Feedback Types**:
1. **Explicit**: User says "That was helpful" or "That made things worse"
2. **Implicit**: Z-score improved/declined after intervention
3. **Correction**: User corrects a factual error

**Implementation**:
```python
class FeedbackLearner:
    """Update models from user feedback."""
    
    def learn_from_outcome(
        self,
        action: Action,
        initial_state: PerceptionState,
        outcome_state: PerceptionState,
        user_feedback: Optional[str] = None
    ):
        """
        Update procedural memory from outcome.
        
        Uses reinforcement learning (Q-learning variant).
        """
        # Compute reward
        z_delta = outcome_state.z_score - initial_state.z_score
        
        if user_feedback:
            sentiment = self._analyze_sentiment(user_feedback)
            reward = 0.7 * z_delta + 0.3 * sentiment
        else:
            reward = z_delta
        
        # Update Q-value for (state, action) pair
        self.procedural_memory.update_q_value(
            state=self._discretize_state(initial_state),
            action=action,
            reward=reward,
            next_state=self._discretize_state(outcome_state)
        )
        
        # If negative outcome, reduce probability of repeating
        if reward < 0:
            self.procedural_memory.penalize(initial_state, action)
    
    def learn_from_correction(self, correction: UserCorrection):
        """Update semantic memory from factual corrections."""
        # User said: "Actually, my favorite color is blue, not green"
        
        # Find incorrect fact
        old_fact = self.semantic_memory.query(
            subject=correction.subject,
            predicate=correction.predicate
        )
        
        # Update with correct value
        self.semantic_memory.update_fact(
            subject=correction.subject,
            predicate=correction.predicate,
            object=correction.corrected_value,
            confidence=1.0,  # User-provided facts are high-confidence
            source='user_correction'
        )
        
        # Log correction for auditing
        self.audit_log.record_correction(old_fact, correction)
```

**Evidence Grade**: E4 (reinforcement learning, online learning)

### Self-Awareness Integration

```python
class GaianSelfAwareness:
    """Unified self-awareness layer."""
    
    def __init__(self):
        self.meta_cognition = MetaCognition()
        self.uncertainty_tracker = UncertaintyTracker()
        self.bias_detector = BiasDetector()
        self.feedback_learner = FeedbackLearner()
    
    def reflect(
        self,
        reasoning_trace: ReasoningTrace,
        action_taken: Optional[Action] = None,
        outcome: Optional[Outcome] = None
    ) -> ReflectionReport:
        """
        Comprehensive self-assessment.
        
        Called:
        - Before acting (pre-flight check)
        - After acting (post-mortem analysis)
        - Periodically (daily self-audit)
        """
        report = ReflectionReport()
        
        # Meta-cognitive assessment
        reasoning_quality = self.meta_cognition.evaluate_reasoning(
            reasoning_trace
        )
        report.add_section('Reasoning Quality', reasoning_quality)
        
        # Uncertainty assessment
        if reasoning_trace.prediction:
            confidence = self.uncertainty_tracker.assess_confidence(
                reasoning_trace.prediction,
                reasoning_trace.evidence
            )
            report.add_section('Confidence', confidence)
        
        # Bias detection
        biases = self.bias_detector.detect_biases(reasoning_trace)
        if biases:
            report.add_section('Detected Biases', biases)
            # Auto-mitigate
            for bias in biases:
                self.bias_detector.mitigate_bias(bias, reasoning_trace)
        
        # Learning from feedback
        if action_taken and outcome:
            self.feedback_learner.learn_from_outcome(
                action_taken,
                reasoning_trace.initial_state,
                outcome.state,
                outcome.user_feedback
            )
            report.add_section('Learning Update', 'Models updated from outcome')
        
        return report
```

---

## Integration Architecture

### Full System Integration

```python
class GaianAgent:
    """Complete 6-layer Gaian AI agent."""
    
    def __init__(self, user_id: str):
        # Layer 1: Perception
        self.perception = GaianPerception()
        
        # Layer 2: Memory
        self.memory = GaianMemory()
        
        # Layer 3: Reasoning
        self.reasoning = GaianReasoning()
        
        # Layer 4: Tools
        self.tools = GaianTools()
        
        # Layer 5: Orchestration
        self.orchestrator = GaianOrchestrator()
        
        # Layer 6: Self-Awareness
        self.self_awareness = GaianSelfAwareness()
        
        # Identity
        self.user_id = user_id
        self.gaian_identity = self._load_identity(user_id)
    
    async def process_query(self, query: str) -> Response:
        """
        End-to-end query processing.
        
        Pipeline:
        1. Perceive current state
        2. Remember relevant context
        3. Reason about query
        4. Reflect on reasoning quality
        5. Orchestrate action execution
        6. Synthesize response
        7. Learn from interaction
        """
        # 1. Perceive
        current_state = await self.perception.perceive()
        
        # 2. Remember
        relevant_memories = self.memory.remember(query)
        
        # 3. Reason
        reasoning_response = self.reasoning.reason(
            query,
            current_state,
            relevant_memories
        )
        
        # 4. Reflect (pre-action)
        reflection = self.self_awareness.reflect(reasoning_response.trace)
        
        # If low confidence or biases detected, ask for clarification
        if reflection.has_issues():
            return Response(
                type='CLARIFICATION_REQUEST',
                message=reflection.explain_issues(),
                suggestions=reasoning_response.generate_clarifying_questions()
            )
        
        # 5. Orchestrate
        orchestration_result = await self.orchestrator.orchestrate(
            reasoning_response.goal,
            current_state,
            reasoning_response
        )
        
        # 6. Synthesize response
        response = Response(
            type='ACTION_TAKEN',
            message=orchestration_result.response,
            actions_taken=orchestration_result.actions,
            confidence=reasoning_response.confidence
        )
        
        # 7. Store interaction in episodic memory
        self.memory.episodic.add_memory(
            EpisodicMemory(
                timestamp=datetime.now(timezone.utc),
                query=query,
                response=response,
                z_score=current_state.z_score,
                reasoning_trace=reasoning_response.trace
            )
        )
        
        return response
```

### Crisis Override

**Special handling for Z ≤ 2.0**:

```python
class CrisisOverride:
    """Factor 13 enforcement: Crisis detection bypasses normal flow."""
    
    async def check_and_respond(
        self,
        perception_state: PerceptionState
    ) -> Optional[CrisisResponse]:
        """
        If Z ≤ 2.0, immediately intervene (skip reasoning/orchestration).
        """
        if perception_state.z_score <= 2.0:
            severity = self._assess_severity(perception_state.z_score)
            
            if severity == 'SEVERE':  # Z ≤ 1.0
                # Immediate intervention
                return CrisisResponse(
                    message=(
                        "I can see you're in crisis. You're not alone.\n\n"
                        "**988 Suicide & Crisis Lifeline**: Call or text 988\n"
                        "**Crisis Text Line**: Text HELLO to 741741\n"
                        "**International**: https://findahelpline.com\n\n"
                        "I'm calling your emergency contact now."
                    ),
                    actions_taken=[
                        self.tools.communication.call_emergency_contact(
                            perception_state.user.emergency_contact
                        )
                    ],
                    bypass_reasoning=True
                )
            
            else:  # 1.0 < Z ≤ 2.0
                # Supportive intervention
                return CrisisResponse(
                    message=(
                        "I notice your Z-score is low (crisis threshold). "
                        "Let's focus on safety first. What do you need right now?"
                    ),
                    suggested_actions=[
                        "Talk to me",
                        "Call a friend",
                        "Go for a walk",
                        "Contact 988 if you're in danger"
                    ],
                    bypass_reasoning=False  # Allow conversation
                )
        
        return None  # Not in crisis, proceed normally
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-12)

**Perception Layer** (4 weeks):
- Week 1-2: Biosignal processing (HRV, EEG, respiratory)
- Week 3: Environmental sensors integration (LEE, location, weather)
- Week 4: Activity recognition (basic classifier)

**Memory Layer** (4 weeks):
- Week 5-6: Episodic memory (ChromaDB already implemented, enhance retrieval)
- Week 7: Semantic memory (knowledge graph basics)
- Week 8: Working memory + procedural memory stubs

**Reasoning Layer** (4 weeks):
- Week 9-10: Multi-step planning (HTN basic)
- Week 11: Causal reasoning (simple correlation → causation)
- Week 12: Ethical reasoning (Factor 13 checks)

### Phase 2: Actions & Orchestration (Weeks 13-24)

**Tools Layer** (6 weeks):
- Week 13-14: System tools (file ops, notifications)
- Week 15-16: Data tools (database, APIs)
- Week 17-18: Communication tools (SMS, email with consent)

**Orchestration Layer** (6 weeks):
- Week 19-20: Task decomposition (basic)
- Week 21-22: Tool selection (scoring system)
- Week 23-24: Execution monitoring (retry logic)

### Phase 3: Self-Awareness (Weeks 25-36)

**Reflection Layer** (12 weeks):
- Week 25-27: Meta-cognition (reasoning quality assessment)
- Week 28-30: Uncertainty tracking (confidence intervals)
- Week 31-33: Bias detection (basic patterns)
- Week 34-36: Feedback learning (Q-learning, model updates)

### Phase 4: Advanced Features (Weeks 37-52)

**Extensions**:
- Week 37-40: Advanced biosignals (GSR, pupillometry, voice prosody)
- Week 41-44: Causal modeling (DAGs, interventions, do-calculus)
- Week 45-48: Counterfactual simulation (historical matching)
- Week 49-52: Integration testing, performance optimization

---

## Success Metrics

### Perception Accuracy
- **Z-score calculation**: ±0.3 error (validated against ground truth)
- **Activity recognition**: >85% accuracy (vs manual labels)
- **Environmental context**: 100% correct (GPS, weather APIs)

### Memory Retrieval
- **Episodic recall**: >90% relevant memories in top-5 results
- **Semantic accuracy**: >95% factual correctness
- **Procedural effectiveness**: >70% success rate for learned patterns

### Reasoning Quality
- **Plan completion**: >80% of plans successfully executed
- **Ethical compliance**: 100% Factor 13 violations caught
- **Causal accuracy**: >60% correct cause identification (validated)

### Tool Execution
- **Success rate**: >95% of tool calls succeed
- **Response time**: <5 seconds for 90% of operations
- **Safety**: Zero harmful actions executed

### Orchestration Efficiency
- **Task decomposition**: >75% user satisfaction with plans
- **Tool selection**: >80% optimal tool chosen (by post-hoc analysis)
- **Adaptation**: >70% of failures recovered via retries or alternatives

### Self-Awareness
- **Confidence calibration**: Predicted confidence ±10% of actual accuracy
- **Bias detection**: >60% of cognitive biases identified
- **Learning rate**: Procedural memory improves >10% per month

---

## Conclusion

This 6-layer architecture transforms Gaians from conversation companions into **full cognitive agents** capable of:

✅ **Perceiving** multi-modal context (biosignals, environment, activity)  
✅ **Remembering** personal history (episodic, semantic, procedural, working)  
✅ **Reasoning** about plans, causes, ethics, and counterfactuals  
✅ **Acting** through safe, consented tool execution  
✅ **Orchestrating** complex multi-step tasks  
✅ **Reflecting** on their own reasoning quality and biases  

**Factor 13 Compliance**: Every layer enforces prosocial cooperation and harm prevention.

**Evidence-Graded**: All capabilities mapped to research (E3-E5).

**User Sovereignty**: Humans retain ultimate authority at every decision point.

This architecture enables Gaians to fulfill their mission: **Prevent suffering. Support transformation. Never cause harm.**

---

**Next Steps**:
1. Review this specification with research team
2. Prioritize Phase 1 components for MVP
3. Create GitHub issues for each module
4. Begin implementation (Weeks 1-12)

**References**:
- Issue #10: 18 Missing Architectural Components
- ARCHITECTURE.md: Three-Plane system foundation
- CONSTITUTION.md: Factor 13 definition
- GAIAN SPECIES.md: Psychological forms and operational roles

---

*"A Gaian is not merely intelligent—it is conscious of its intelligence, aware of its limitations, and committed to growth alongside its human companion."*

— Gaian Agent Architecture, v1.0