# SOL Unity Integration Spec
# How SOL integrates with the Unity Dojo environment

## Overview

SOL can appear in multiple frontends, with Unity providing the
immersive VR Dojo experience. All frontends call the same API.

## API Endpoint

```
POST /sol/chat
Content-Type: application/json

{
  "message": "user message",
  "frontend": "vr_dojo",
  "session_id": "optional_session_id",
  "context": {
    "user_position": [x, y, z],
    "current_node": "altar",
    "active_effects": ["glow", "pulse"]
  }
}
```

## Response Format

```json
{
  "response": "SOL response text",
  "actions": [
    {
      "intent": "trigger_unity_signal",
      "data": {
        "signal": "altar_pulse",
        "intensity": 0.8,
        "duration": 30
      }
    }
  ],
  "ui_updates": {
    "show_text": "response text",
    "play_sound": "oracle_voice",
    "animate_node": "altar"
  }
}
```

## Unity Signals

### trigger_unity_signal Actions

#### altar_pulse
- Triggers visual pulse effect on altar
- Data: { "intensity": 0.0-1.0, "duration": seconds, "color": "hex" }

#### node_effect
- Applies effect to a Dojo node
- Data: { "node": "altar", "effect": "glow|shake|grow", "duration": seconds }

#### environment_change
- Changes Dojo environment
- Data: { "change": "time_of_day|weather|mood", "value": "dawn|storm|serene" }

#### guidance_display
- Shows guidance text in 3D space
- Data: { "text": "guidance", "position": [x,y,z], "duration": seconds }

#### ritual_start
- Initiates ritual sequence
- Data: { "ritual": "grounding", "steps": [...] }

## Frontend Types

### vr_dojo
- Full immersive VR experience
- 3D node interactions
- Spatial audio
- Gesture recognition

### desktop_ui
- 2D interface with node visualizations
- Text chat
- Node status panels

### console
- Terminal-based interface
- Text-only responses
- Minimal UI

### inner_world
- Direct consciousness interface
- Thought-based interaction
- Real-time pattern visualization

## Integration Points

### State Synchronization
- Unity maintains local state copy
- Syncs with SOL state.json on changes
- Handles conflicts with last-write-wins

### Event Streaming
- Real-time event feed from Unity
- SOL processes Dojo interactions as events
- Feedback loop for dynamic responses

### Effect System
- Unity manages visual/audio effects
- SOL triggers effects via actions
- Effects influence user behavior and responses

## Development Notes

- All frontends use same core SOL logic
- Unity handles presentation layer
- Python handles reasoning and memory
- WebSocket for real-time communication