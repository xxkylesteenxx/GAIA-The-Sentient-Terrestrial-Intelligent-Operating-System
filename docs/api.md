# GAIA WebSocket API Specification

## Overview

GAIA uses WebSocket connections for real-time communication between the backend and desktop client. The API follows the Three-Plane Architecture:

- **Core Plane** (`ws://localhost:8765`): Deterministic, fail-closed operations
- **Bridge Plane** (`ws://localhost:8766`): Hypothesis testing, simulations
- **Overlay Plane** (`ws://localhost:8767`): Avatar, meaning-making

## Message Format

All messages use JSON with this structure:

```json
{
  "type": "zscore",
  "plane": "core",
  "timestamp": "2026-02-28T21:00:00.000Z",
  "data": {
    "value": 7.5,
    "trend": "stable"
  },
  "reality_label": "E2"
}
```

### Message Types

#### Core Plane Messages

**`zscore`** - Current Z-score
```json
{
  "type": "zscore",
  "plane": "core",
  "data": {
    "value": 7.5,
    "c_order": 0.85,
    "f_freedom": 0.78,
    "b_balance": 0.92,
    "level": "Rubedo",
    "color": "Gold"
  }
}
```

**`crisis`** - Crisis alert (HIGHEST PRIORITY)
```json
{
  "type": "crisis",
  "plane": "core",
  "data": {
    "severity": 3,
    "zscore": 1.2,
    "message": "Emergency message...",
    "resources": {
      "suicide_lifeline": "988",
      "crisis_text": "741741"
    }
  }
}
```

**`equilibrium`** - Capacity state
```json
{
  "type": "equilibrium",
  "plane": "core",
  "data": {
    "capacity_percent": 65.0,
    "state": "good",
    "emoji": "👍",
    "rest_mandatory": false
  }
}
```

#### Overlay Plane Messages

**`avatar_response`** - Avatar message
```json
{
  "type": "avatar_response",
  "plane": "overlay",
  "data": {
    "message": "I see you, Kyle.",
    "emotion": "attentive",
    "autonomy_level": 0.6
  }
}
```

**`avatar_state`** - Avatar status
```json
{
  "type": "avatar_state",
  "plane": "overlay",
  "data": {
    "emotion": "attentive",
    "autonomy": 0.6,
    "mood": "supportive",
    "trust_level": 0.85
  }
}
```

#### Client → Server Messages

**`user_input`** - User message
```json
{
  "type": "user_input",
  "content": "I'm feeling stressed today."
}
```

**`request_zscore`** - Request current Z-score
```json
{
  "type": "request_zscore"
}
```

**`crisis_alert`** - Trigger crisis protocol
```json
{
  "type": "crisis_alert",
  "data": {
    "reason": "User triggered emergency"
  }
}
```

## Reality Labels (Evidence Grading)

- **E0**: Axiom (self-evident)
- **E1**: Model/Theory (untested)
- **E2**: Experimental/Observational
- **E3**: Peer-reviewed
- **E4**: Replicated
- **E5**: Consensus
- **NONFICTION**: Life-critical (crisis resources)

## Connection Lifecycle

1. **Connect** to plane-specific endpoint
2. **Receive** initial state snapshot
3. **Subscribe** to updates (automatic)
4. **Send** messages as needed
5. **Handle** crisis broadcasts (all planes)
6. **Disconnect** gracefully

## Error Handling

```json
{
  "type": "error",
  "data": {
    "code": "INVALID_MESSAGE",
    "message": "Message format invalid"
  }
}
```

## Rate Limits

- No rate limits on crisis messages (Factor 13)
- User input: 10 messages/second
- Z-score requests: 1/second

## Example Client

```python
import asyncio
import websockets
import json

async def connect_to_gaia():
    uri = "ws://localhost:8767"  # Overlay Plane
    
    async with websockets.connect(uri) as websocket:
        # Receive initial state
        initial_state = await websocket.recv()
        print(f"Initial state: {initial_state}")
        
        # Send user message
        await websocket.send(json.dumps({
            "type": "user_input",
            "content": "Hello, Avatar!"
        }))
        
        # Listen for responses
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data['type']}")
            
            if data['type'] == 'crisis':
                # Handle crisis with highest priority
                print(f"CRISIS: {data['data']['message']}")

asyncio.run(connect_to_gaia())
```

## JavaScript Client

```javascript
const ws = new WebSocket('ws://localhost:8767');

ws.onopen = () => {
  console.log('Connected to GAIA Overlay Plane');
  
  // Send message
  ws.send(JSON.stringify({
    type: 'user_input',
    content: 'Hello, Avatar!'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'crisis') {
    // Handle crisis
    alert(`CRISIS: ${data.data.message}`);
  } else if (data.type === 'avatar_response') {
    // Display Avatar message
    console.log(`Avatar: ${data.data.message}`);
  }
};
```

## Security

- Local-first: Runs on `localhost` by default
- Encryption: TLS/SSL for remote connections (future)
- Authentication: Required for federation (future)
- Authorization: User owns all data

## Federation Protocol (Future)

When connecting to Neighbor instances:
- Mutual consent required
- End-to-end encryption
- Selective data sharing
- Revocable access

See [Federation Documentation](federation.md) for details.
