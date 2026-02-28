# GAIA WebSocket API Specification

Complete API reference for GAIA WebSocket server.

## Connection

### Endpoint

```
ws://localhost:8765
```

### Connection Protocol

1. Client initiates WebSocket connection
2. Server sends welcome message
3. Client can send requests
4. Server responds with JSON messages

### Example (JavaScript)

```javascript
const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => {
    console.log('Connected to GAIA');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};
```

## Message Format

All messages are JSON objects with a `type` field:

```json
{
    "type": "message_type",
    "data": { ... },
    "timestamp": "2026-02-28T21:00:00Z"
}
```

## API Methods

### 1. Health Check

**Request:**
```json
{
    "type": "ping"
}
```

**Response:**
```json
{
    "type": "pong",
    "timestamp": "2026-02-28T21:00:00Z"
}
```

### 2. Calculate Z-Score

**Request:**
```json
{
    "type": "calculate_z_score",
    "time_series": [0.1, 0.2, 0.3, ...],
    "positive": 5.0,
    "negative": 1.0
}
```

**Parameters:**
- `time_series`: Array of floats (normalized [0,1])
- `positive`: Positive event count/intensity
- `negative`: Negative event count/intensity

**Response:**
```json
{
    "type": "z_score_result",
    "z_score": 8.456,
    "coherence": 0.789,
    "fidelity": 0.654,
    "balance": 1.0,
    "lyapunov": -0.123,
    "state": "STABLE",
    "timestamp": "2026-02-28T21:00:00Z"
}
```

**States:**
- `CRISIS`: Z < 3.0
- `TRANSITIONAL`: 3.0 ≤ Z < 6.0
- `STABLE`: 6.0 ≤ Z < 9.0
- `COHERENT`: Z ≥ 9.0

### 3. Crisis Detection

**Request:**
```json
{
    "type": "check_crisis",
    "z_score": 2.5,
    "text": "I feel hopeless and lost",
    "history": [5.0, 4.0, 3.0, 2.5]
}
```

**Parameters:**
- `z_score`: Current Z-score
- `text`: User text input
- `history`: (Optional) Recent Z-score history

**Response:**
```json
{
    "type": "crisis_alert",
    "level": "HIGH",
    "severity": 3,
    "z_threshold_breach": true,
    "keyword_matches": ["hopeless"],
    "trend": "degrading",
    "requires_intervention": true,
    "requires_emergency": false,
    "protocol": {
        "action": "urgent_support",
        "avatar_mode": "crisis_counselor",
        "access_level": "minimal",
        "resources": ["hotline", "emergency_contacts", "safety_plan"]
    },
    "timestamp": "2026-02-28T21:00:00Z"
}
```

**Crisis Levels:**
- `NONE` (0): No intervention needed
- `LOW` (1): Monitor
- `MODERATE` (2): Intervention recommended
- `HIGH` (3): Urgent support
- `CRITICAL` (4): Emergency protocol

### 4. Update Equilibrium

**Request:**
```json
{
    "type": "update_equilibrium",
    "cognitive": 0.7,
    "emotional": 0.5,
    "physical": 0.3,
    "z_score": 7.8
}
```

**Parameters:**
- `cognitive`: Cognitive load [0,1]
- `emotional`: Emotional load [0,1]
- `physical`: Physical load [0,1]
- `z_score`: Current Z-score

**Response:**
```json
{
    "type": "equilibrium_state",
    "capacity_level": "MODERATE",
    "available_capacity": 0.42,
    "recommendations": [
        "Take a cognitive break - reduce information intake",
        "Practice emotional regulation - breathing, grounding"
    ],
    "recovery_estimate_hours": 3.5,
    "timestamp": "2026-02-28T21:00:00Z"
}
```

**Capacity Levels:**
- `CRITICAL`: < 10%
- `LOW`: 10-30%
- `MODERATE`: 30-60%
- `ADEQUATE`: 60-80%
- `OPTIMAL`: > 80%

### 5. Check Equilibrium Budget

**Request:**
```json
{
    "type": "check_budget",
    "requested_load": 0.3
}
```

**Response:**
```json
{
    "type": "budget_result",
    "approved": true,
    "remaining_capacity": 0.35,
    "timestamp": "2026-02-28T21:00:00Z"
}
```

**OR (if insufficient):**
```json
{
    "type": "budget_result",
    "approved": false,
    "reason": "Insufficient capacity",
    "deficit": 0.15,
    "recommendation": "Schedule for later or reduce scope",
    "timestamp": "2026-02-28T21:00:00Z"
}
```

### 6. Avatar Message (Phase 1 Partial)

**Request:**
```json
{
    "type": "avatar_message",
    "message": "How should I approach this difficult conversation?",
    "context": {
        "z_score": 6.5,
        "equilibrium": 0.55,
        "crisis_level": "LOW"
    }
}
```

**Response:**
```json
{
    "type": "avatar_response",
    "message": "From my perspective as your complement, I see your strength in direct communication. Consider approaching with curiosity rather than defensiveness. What outcome would bring you both peace?",
    "autonomy_level": 1,
    "emotional_tone": "supportive",
    "timestamp": "2026-02-28T21:00:00Z"
}
```

### 7. Store Memory (Avatar)

**Request:**
```json
{
    "type": "store_memory",
    "memory_type": "emotional",
    "emotion": "joy",
    "context": "Completed a challenging project successfully",
    "intensity": 0.85,
    "z_score": 9.2
}
```

**Memory Types:**
- `episodic`: User interactions
- `semantic`: Concepts and knowledge
- `emotional`: Affective experiences

**Response:**
```json
{
    "type": "memory_stored",
    "memory_id": "emotion_2026-02-28T21:00:00",
    "timestamp": "2026-02-28T21:00:00Z"
}
```

### 8. Recall Memory

**Request:**
```json
{
    "type": "recall_memory",
    "memory_type": "emotional",
    "query": "times I felt accomplished",
    "n_results": 5
}
```

**Response:**
```json
{
    "type": "memory_results",
    "memories": [
        {
            "emotion": "joy",
            "context": "Completed a challenging project successfully",
            "intensity": 0.85,
            "z_score": 9.2,
            "timestamp": "2026-02-28T21:00:00Z",
            "relevance": 0.92
        }
    ],
    "timestamp": "2026-02-28T21:00:00Z"
}
```

## Error Handling

**Error Response:**
```json
{
    "type": "error",
    "code": "INVALID_REQUEST",
    "message": "Missing required field: time_series",
    "timestamp": "2026-02-28T21:00:00Z"
}
```

**Error Codes:**
- `INVALID_REQUEST`: Malformed request
- `MISSING_FIELD`: Required field missing
- `INVALID_DATA`: Data validation failed
- `SERVER_ERROR`: Internal server error
- `CRISIS_OVERRIDE`: Request blocked due to crisis state

## Rate Limiting

- **Default**: 100 requests per minute
- **Crisis Detection**: 10 requests per minute
- **Memory Operations**: 50 requests per minute

## Security

### Phase 1 (Current)

- **Local Only**: Binds to `localhost`
- **No Authentication**: Trust local processes

### Phase 2 (Future)

- **TLS**: Encrypted WebSocket (wss://)
- **Authentication**: Token-based
- **Authorization**: Role-based access control

## Examples

See `examples/` directory for complete client implementations:

- `examples/python_client.py`: Python WebSocket client
- `examples/js_client.html`: Browser JavaScript client
- `web/desktop/`: Electron desktop app

## Testing

```bash
# Run WebSocket API tests
pytest tests/test_websocket_api.py -v
```

## Support

For API issues, open an issue on GitHub:
https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/issues
