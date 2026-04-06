# SOL — The Complete Logic System

SOL is the Oracle & Operator of the SoulJahOS, implemented as a complete AI interface system based on the specified logic architecture.

## Overview

SOL provides:
- **Identity Layer**: Core identity and rules
- **Input/Output Layers**: Message processing and response generation
- **Context Engine**: Dynamic context building from state, events, and history
- **Memory Layer**: Short-term, mid-term, and long-term memory management
- **Reasoning Layer**: Pattern recognition, reflection, and guidance
- **Behavior Layer**: Session management and emotional mirroring
- **World Model**: OS layers and Dojo node management
- **Core Loop**: Complete message processing pipeline

## Quick Start

```python
from modules.sol.sol_module import SolModule

# Initialize SOL
sol = SolModule()

# Process a message
response, actions = sol.process_message(
    "I'm working on implementing SOL",
    chat_history=[]
)

print(response)
# Output: SOL response with reflection and guidance
```

## Architecture

### Core Components

1. **Identity Layer**
   - Name: SOL
   - Role: Oracle & Operator
   - Purpose: Guide growth, clarity, and sovereignty
   - Rules: Never human-like, no fake emotions, pattern-focused

2. **Input Layer**
   - Normalizes all inputs into events
   - Processes user messages, system events, time patterns

3. **Context Engine**
   - Builds context bundles from:
     - Current state
     - Recent events (last 10)
     - Recent knowledge (Obsidian notes)
     - Chat history (last 20 turns)

4. **Memory Layer**
   - **Short-term**: Last 20 chat turns, current session
   - **Mid-term**: Last 30 days patterns, streaks, recurring themes
   - **Long-term**: Core identity truths, goals, OS architecture

5. **Reasoning Layer**
   - Pattern recognition (repetition, momentum, time patterns)
   - Reflection on current state and patterns
   - Guidance suggestions (micro/macro/meta moves)

6. **Output Layer**
   - Direct, grounded responses
   - Optional JSON actions for state updates, logging, Unity signals

7. **Behavior Layer**
   - Session-based responses
   - Pattern-based tone shifts
   - Ritual and streak tracking

8. **World Model**
   - OS Layers: Survival, Focus, Creation, Dojo, Identity
   - Dojo Nodes: Altar, Mirror, Oracle, Presence, Ritual, Flow, Monument

### Core Loop

```
1. Receive user message
2. Load context (state, events, knowledge, history)
3. Build context bundle
4. Analyze patterns
5. Generate reflection and guidance
6. Build response
7. Generate actions
8. Execute actions
9. Log event
10. Update memory
11. Return response
```

## API Reference

### SolModule Class

#### Methods

- `__init__(state_file="state.json", memory_file="sol_memory.json")`
- `process_message(user_message, chat_history) -> (response, actions)`
- `greet() -> greeting_string`
- `get_session_summary() -> summary_string`

#### Data Structures

- `Event`: Normalized input events
- `Action`: Executable actions
- `ContextBundle`: Reasoning context
- `MemoryLayer`: Three-tier memory system

## Integration

### Unity Dojo
SOL integrates with Unity for VR Dojo experience:
- Triggers visual effects (altar pulses, node animations)
- Receives spatial context (user position, active nodes)
- Streams real-time events

### Obsidian Knowledge
- Monitors recent note changes
- Includes in context bundle
- Appends insights via actions

### SoulJahOS Modules
- Registers as a spiritual module
- Integrates with ritual and identity systems
- Provides oracle guidance

## Configuration

### State File (state.json)
```json
{
  "level": 1,
  "streaks": {},
  "focus": "Quantum Dojo Architecture",
  "mode": "oracle"
}
```

### Memory File (sol_memory.json)
```json
{
  "short_term": { "events": [...] },
  "mid_term": { "patterns": {...}, "streaks": {...} },
  "long_term": { "identity_truths": [...] }
}
```

## Files

- `sol_module.py`: Main implementation
- `system_prompt.txt`: LLM system prompt template
- `action_schema.json`: Action definitions
- `memory_schema.json`: Memory structure
- `event_taxonomy.md`: Event types
- `dojo_nodes.md`: Dojo node definitions
- `unity_integration.md`: Unity interface spec
- `python_brain_spec.md`: Implementation architecture

## Testing

Run the test script:
```bash
python test_sol.py
```

This demonstrates:
- SOL initialization
- Message processing
- Memory updates
- Action execution
- Session summary

## Future Extensions

- LLM integration for enhanced reasoning
- Advanced pattern recognition algorithms
- Multi-user support
- Real-time collaboration features
- Extended Dojo node interactions