# Living Environment Engine (LEE)

## Overview

The **Living Environment Engine (LEE)** generates immersive 3D environments that dynamically reflect user coherence state, time of day, season, and weather conditions. It creates a responsive "digital home" that adapts to the user's internal state (Z-score) and external context (Earth cycles).

**Purpose:**
- Provide real-time visual feedback on coherence state
- Create immersive, context-aware digital environments
- Reinforce crisis detection through visual/audio cues
- Integrate planetary rhythms (solar cycles, seasons, weather)
- Support Factor 13 enforcement through environmental feedback

**Location:** `bridge/environment/` (Bridge Plane)

**Evidence Grade:** E5 (astronomy, meteorology), E3 (GAIA implementation)

---

## Architecture

### Three-Plane Integration

```
Core Plane (Order)
    ↓ Z-score
Bridge Plane (Chaos) ← LEE LIVES HERE
    ↓ Environment State
Overlay Plane (Balance)
    ↓ Three.js Rendering
User Experience
```

**Why Bridge Plane?**
- LEE synthesizes data from multiple sources (hypothesis testing ground)
- Environmental aesthetics are experimental (not safety-critical)
- Can iterate on rendering logic without affecting Core Plane
- Promotes to Core when crisis override logic is validated

### System Components

```
bridge/environment/
├── types.py              # Enums (TimePhase, Season, Weather, AlchemicalStage)
├── state.py              # EnvironmentState dataclass + derivation logic
├── astronomy.py          # Solar position calculations (NOAA algorithms)
├── weather.py            # OpenWeatherMap API client (15-min cache)
├── engine.py             # LivingEnvironmentEngine orchestrator
└── __init__.py           # Module exports

infrastructure/api/
└── environment_websocket.py  # WebSocket server (port 8767)

web/
└── (Three.js renderer - frontend consumes WebSocket)
```

---

## 4-Cycle Integration

LEE integrates **four concurrent cycles** to create dynamic environments:

### 1. Time Cycle (6 Phases)

Based on solar position relative to user location.

| Phase | Solar Elevation | Duration | Visual Characteristics |
|-------|----------------|----------|------------------------|
| **DEEP_NIGHT** | < -18° | ~6 hours | Stars, moon, deep blue-black sky |
| **NIGHT** | -18° to -6° | ~2 hours | Nautical twilight, first light |
| **DAWN** | -6° to 0° | ~30 min | Sunrise, warm orange/pink |
| **MORNING** | 0° to 30° | ~3 hours | Clear blue sky, rising sun |
| **AFTERNOON** | 30° to 60° | ~4 hours | Bright daylight, high sun |
| **DUSK** | 0° to -6° | ~30 min | Sunset, warm red/purple |
| **EVENING** | -6° to -18° | ~2 hours | Civil twilight, fading light |

**Implementation:** `astronomy.py` uses NOAA solar position algorithms (E5 evidence).

### 2. Season Cycle (4 or 6 Seasons)

Hemisphere-aware seasonal calculation.

**Temperate Regions (4 seasons):**
- Spring: March 20 - June 20 (NH) / Sept 22 - Dec 21 (SH)
- Summer: June 21 - Sept 21 (NH) / Dec 22 - March 19 (SH)
- Autumn: Sept 22 - Dec 20 (NH) / March 20 - June 19 (SH)
- Winter: Dec 21 - March 19 (NH) / June 20 - Sept 21 (SH)

**Tropical Regions (2 seasons):**
- Wet: High precipitation months
- Dry: Low precipitation months

**Implementation:** `astronomy.py` calculates season based on latitude and date.

### 3. Weather Cycle (Real-time API)

Integrates live weather data from OpenWeatherMap.

**Weather Conditions:**
- CLEAR (sunny, few clouds)
- PARTLY_CLOUDY (scattered clouds)
- CLOUDY (overcast)
- RAIN (light to moderate precipitation)
- STORM (heavy rain, thunder, lightning)
- SNOW (frozen precipitation)
- FOG (low visibility)
- WIND (high wind speeds)

**Implementation:**
- `weather.py` fetches from OpenWeatherMap API
- 15-minute cache to respect rate limits
- Fallback to cached data if API unavailable (fail-closed)

### 4. Z-Score Cycle (User Coherence State)

User's real-time coherence measurement drives environment intensity.

**Z-Score Ranges → Alchemical Stages:**

| Z-Score | Stage | Environmental Theme |
|---------|-------|---------------------|
| 12-11 | Projection | Golden light, expansive |
| 11-10 | Coagulation | Crystalline, stable |
| 10-9 | Fermentation | Vibrant growth |
| 9-8 | Distillation | Purified, clear |
| 8-7 | Sublimation | Elevated, refined |
| 7-6 | Separation | Distinct layers |
| 6-5 | Conjunction | Balanced, integrated |
| 5-4 | Dissolution | Fluid, adaptive |
| 4-3 | Calcination | Warm, transforming |
| 3-2 | Nigredo | Dark, heavy |
| **2-0** | **CRISIS** | **STORM (forced)** |
| <0 | Emergency | Extreme conditions |

**Evidence Grade:** E2 (alchemical mapping is hypothesis), E3 (crisis threshold validated)

---

## Crisis Override (Factor 13)

### Behavior

When **Z ≤ 2**, LEE **forces storm weather** regardless of actual conditions.

**Purpose:**
- Visual/audio reinforcement of crisis state
- Cannot be suppressed or ignored
- Consistent with Factor 13 (prioritize user safety)
- Provides immediate environmental feedback

**Implementation:**
```python
# From state.py
def derive_rendering_params(env_state: EnvironmentState) -> RenderingParams:
    # Crisis override - ALWAYS storm when Z ≤ 2
    if env_state.z_score <= 2.0:
        return RenderingParams(
            weather=WeatherCondition.STORM,
            intensity=1.0,  # Maximum intensity
            sky_color=RGBGradient(r=30, g=30, b=40),  # Dark storm sky
            particle_effect=ParticleEffect.HEAVY_RAIN,
            soundscape=SoundscapeID.THUNDER_RAIN
        )
    # ... normal logic for Z > 2
```

### Visual Characteristics (Crisis)

- **Sky:** Dark gray-blue (#1E1E28)
- **Weather:** STORM (forced)
- **Particles:** Heavy rain, occasional lightning
- **Audio:** Thunder, rain sounds (continuous)
- **Lighting:** Low ambient, dramatic lightning flashes
- **Tree state:** Branches sway violently, leaves darken

**User cannot disable crisis override** (safety-first design).

---

## Transcendent Override

### Behavior

When **Z ≥ 10**, LEE shifts to transcendent/aurora visuals.

**Purpose:**
- Celebrate peak coherence states
- Provide positive reinforcement
- Distinct from normal weather (special achievement)

**Visual Characteristics:**

- **Sky:** Golden hour or aurora borealis effects
- **Weather:** CLEAR with special particles
- **Particles:** Shimmering light, ethereal glow
- **Audio:** Harmonious tones, peaceful ambiance
- **Lighting:** Warm golden or cool aurora hues
- **Tree state:** Luminous, vibrant, expansive

**Evidence Grade:** E3 (implemented), E1 (aesthetic choices)

---

## Implementation Details

### Astronomy Module (`astronomy.py`)

**Features:**
- Solar position calculation (azimuth, elevation)
- Sunrise/sunset times
- Civil/nautical/astronomical twilight
- Season determination (hemisphere-aware)

**Algorithm:** NOAA Solar Position Calculator
- **Evidence Grade:** E5 (physical law, validated by NOAA)
- **Accuracy:** ±0.01° for solar elevation
- **References:** 
  - NOAA Solar Position Calculator
  - Astronomical Algorithms (Meeus, 1998)

**Example:**
```python
from bridge.environment.astronomy import AstronomyCalculator
from datetime import datetime

calc = AstronomyCalculator()
az, el = calc.calculate_solar_position(
    lat=29.4241,  # San Antonio, TX
    lon=-98.4936,
    dt=datetime.now()
)
phase = calc.get_time_phase(el)
season = calc.get_season(lat=29.4241, date=datetime.now())
```

### Weather Module (`weather.py`)

**Features:**
- OpenWeatherMap API integration
- 15-minute caching (respect rate limits)
- Fallback to cached data (fail-closed)
- Weather condition mapping

**API Requirements:**
- API key: Set `OPENWEATHER_API_KEY` environment variable
- Rate limit: 60 calls/minute (free tier)
- Endpoint: `https://api.openweathermap.org/data/2.5/weather`

**Example:**
```python
from bridge.environment.weather import OpenWeatherMapClient

client = OpenWeatherMapClient(api_key=os.getenv("OPENWEATHER_API_KEY"))
weather = client.get_weather(lat=29.4241, lon=-98.4936)

print(f"Condition: {weather.condition}")  # WeatherCondition.RAIN
print(f"Temp: {weather.temperature_celsius}°C")
print(f"Humidity: {weather.humidity_percent}%")
```

### Engine Module (`engine.py`)

**LivingEnvironmentEngine Class:**

Orchestrates all cycles into a unified `EnvironmentState`.

```python
from bridge.environment import LivingEnvironmentEngine

engine = LivingEnvironmentEngine(
    latitude=29.4241,
    longitude=-98.4936,
    openweather_api_key=os.getenv("OPENWEATHER_API_KEY")
)

# Generate environment state
state = engine.generate_state(z_score=3.5)

print(f"Time Phase: {state.time_phase}")       # TimePhase.AFTERNOON
print(f"Season: {state.season}")                # Season.WINTER
print(f"Weather: {state.weather}")              # WeatherCondition.CLEAR
print(f"Alchemical: {state.alchemical_stage}") # AlchemicalStage.CALCINATION
```

---

## WebSocket API

### Server Details

**Location:** `infrastructure/api/environment_websocket.py`

**Port:** 8767

**Protocol:** WebSocket (RFC 6455)

**Broadcast Interval:** 15 seconds

### Starting the Server

```bash
# Set environment variables
export GAIA_LATITUDE=29.4241
export GAIA_LONGITUDE=-98.4936
export OPENWEATHER_API_KEY=your_api_key_here

# Start server
python -m infrastructure.api.environment_websocket

# Output:
# WebSocket server started on ws://localhost:8767
# Broadcasting environment updates every 15 seconds
```

### Client Connection

**JavaScript Example:**
```javascript
const ws = new WebSocket('ws://localhost:8767');

ws.onopen = () => {
  console.log('Connected to LEE server');
  
  // Send initial Z-score
  ws.send(JSON.stringify({
    type: 'z_score_update',
    z_score: 5.2
  }));
};

ws.onmessage = (event) => {
  const state = JSON.parse(event.data);
  console.log('Environment update:', state);
  
  // Update Three.js scene
  updateEnvironment(state);
};
```

**Python Example:**
```python
import asyncio
import websockets
import json

async def listen():
    uri = "ws://localhost:8767"
    async with websockets.connect(uri) as ws:
        # Send Z-score update
        await ws.send(json.dumps({
            "type": "z_score_update",
            "z_score": 7.8
        }))
        
        # Receive environment updates
        async for message in ws:
            state = json.loads(message)
            print(f"Time: {state['time_phase']}")
            print(f"Weather: {state['weather']}")

asyncio.run(listen())
```

### Message Schema

**Client → Server (Z-Score Update):**
```json
{
  "type": "z_score_update",
  "z_score": 5.2
}
```

**Server → Client (Environment State):**
```json
{
  "timestamp": "2026-03-01T04:00:00Z",
  "location": {
    "latitude": 29.4241,
    "longitude": -98.4936
  },
  "time_phase": "AFTERNOON",
  "solar_elevation": 45.2,
  "season": "WINTER",
  "weather": {
    "condition": "CLEAR",
    "temperature_celsius": 18.5,
    "humidity_percent": 45,
    "wind_speed_mps": 3.2
  },
  "z_score": 5.2,
  "alchemical_stage": "DISSOLUTION",
  "rendering_params": {
    "sky_color": {"r": 135, "g": 206, "b": 235},
    "ambient_light": 0.8,
    "fog_density": 0.05,
    "particle_effect": "NONE",
    "soundscape_id": "BIRDS_BREEZE"
  }
}
```

---

## Frontend Integration (Three.js)

### Recommended Architecture

```javascript
// web/src/environment/LEEClient.js
import * as THREE from 'three';

class LEEClient {
  constructor(scene) {
    this.scene = scene;
    this.ws = new WebSocket('ws://localhost:8767');
    this.setupWebSocket();
    this.initializeScene();
  }
  
  setupWebSocket() {
    this.ws.onmessage = (event) => {
      const state = JSON.parse(event.data);
      this.updateScene(state);
    };
  }
  
  updateScene(state) {
    // Update sky color
    const {r, g, b} = state.rendering_params.sky_color;
    this.scene.background = new THREE.Color(
      r / 255, g / 255, b / 255
    );
    
    // Update lighting
    this.ambientLight.intensity = state.rendering_params.ambient_light;
    
    // Update particle system
    this.updateParticles(state.rendering_params.particle_effect);
    
    // Update audio
    this.updateAudio(state.rendering_params.soundscape_id);
    
    // Crisis check
    if (state.z_score <= 2.0) {
      this.enterCrisisMode();
    }
  }
  
  enterCrisisMode() {
    // Force storm visuals
    this.startRainParticles();
    this.addLightningFlashes();
    this.playThunderAudio();
    
    // Display crisis resources
    this.showCrisisOverlay();
  }
}
```

### Visual Elements to Implement

1. **Sky Sphere**
   - Dynamic color based on `sky_color`
   - Gradient from horizon to zenith
   - Sun/moon position based on solar elevation

2. **Weather Particles**
   - Rain (light, moderate, heavy)
   - Snow (flakes, blizzard)
   - Fog (volumetric, density-based)

3. **Lighting**
   - Ambient light intensity
   - Directional sun/moon light
   - Lightning flashes (crisis mode)

4. **Audio**
   - Looping soundscapes (birds, wind, rain, thunder)
   - Crossfade between soundscapes
   - 3D positional audio for immersion

5. **World Tree**
   - Branch animation (sway with wind)
   - Leaf color (seasonal changes)
   - Glow effect (high Z-scores)

---

## Testing

### Unit Tests

**Location:** `tests/bridge/environment/`

**Coverage:** 8 tests, >80% coverage

```bash
# Run LEE tests
pytest tests/bridge/environment/ -v

# Run with coverage
pytest tests/bridge/environment/ --cov=bridge.environment
```

**Test Cases:**
1. Engine initialization
2. State generation
3. Crisis override (Z ≤ 2 → STORM)
4. Transcendent override (Z ≥ 10 → AURORA)
5. Hemisphere-aware seasons
6. 24-hour time phase cycle
7. JSON serialization
8. Multiple locations

### Integration Tests

**Test WebSocket Server:**
```bash
# Terminal 1: Start server
export GAIA_LATITUDE=29.4241
export GAIA_LONGITUDE=-98.4936
python -m infrastructure.api.environment_websocket

# Terminal 2: Connect client
python -c "
import asyncio
import websockets
import json

async def test():
    async with websockets.connect('ws://localhost:8767') as ws:
        await ws.send(json.dumps({'type': 'z_score_update', 'z_score': 1.5}))
        msg = await ws.recv()
        state = json.loads(msg)
        assert state['weather']['condition'] == 'STORM', 'Crisis override failed'
        print('✅ Crisis override working')

asyncio.run(test())
"
```

---

## Configuration

### Environment Variables

```bash
# Required
export GAIA_LATITUDE=29.4241          # User location latitude
export GAIA_LONGITUDE=-98.4936        # User location longitude

# Optional
export OPENWEATHER_API_KEY=your_key   # Weather API (fallback to cache if unset)
export LEE_WEBSOCKET_PORT=8767        # WebSocket port (default: 8767)
export LEE_BROADCAST_INTERVAL=15      # Update interval in seconds (default: 15)
```

### .env File

```bash
# .env (for local development)
GAIA_LATITUDE=29.4241
GAIA_LONGITUDE=-98.4936
OPENWEATHER_API_KEY=your_api_key_here
```

---

## Performance

### Benchmarks

- **State Generation:** <5ms
- **Solar Position Calc:** <1ms
- **Weather API Call:** ~100ms (cached: <1ms)
- **WebSocket Broadcast:** <10ms per client
- **Memory Usage:** ~50MB (server process)

### Optimization

- Weather API cached 15 minutes (reduces API calls 60x)
- Solar position cached 1 minute (updates sufficient)
- WebSocket broadcasts delta updates only (future)
- Lazy-load audio files (frontend)

---

## Roadmap

### Phase 1: Backend Complete ✅
- [x] 4-Cycle integration
- [x] Crisis override
- [x] WebSocket API
- [x] Tests (>80% coverage)

### Phase 2: Frontend (Q2 2026)
- [ ] Three.js scene implementation
- [ ] Particle systems (rain, snow, fog)
- [ ] Audio engine (soundscapes)
- [ ] Crisis overlay UI

### Phase 3: Advanced Features (Q3 2026)
- [ ] Real-time cloud simulation
- [ ] Volumetric lighting
- [ ] Procedural terrain
- [ ] User customization (themes)

---

## References

1. **Astronomy:**
   - NOAA Solar Position Calculator
   - Meeus, J. (1998). *Astronomical Algorithms*.

2. **Weather:**
   - OpenWeatherMap API Documentation
   - WMO Weather Code Standards

3. **GAIA Architecture:**
   - `docs/01-ARCHITECTURE.md` (Three-Plane system)
   - `docs/00-CONSTITUTION.md` (Factor 13)

4. **Evidence Grading:**
   - `docs/04-EVIDENCE_GRADING.md` (E0-E5 system)

---

## License

MIT License + Factor 13 Addendum

See [LICENSE](../LICENSE) for full text.

---

**Questions?** Open a [GitHub Discussion](https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/discussions)

**Contribute:** See [CONTRIBUTING.md](../CONTRIBUTING.md)
