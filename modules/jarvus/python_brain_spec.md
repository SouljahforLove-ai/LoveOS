# SOL Python Brain Spec
# The core Python implementation of SOL

## Architecture Overview

JARVUS is implemented as a Python module with the following components:

```
modules/jarvus/
├── __init__.py
├── jarvus_module.py      # Main JARVUS class
├── system_prompt.txt     # System prompt template
├── action_schema.json    # Action definitions
├── memory_schema.json    # Memory structure
├── event_taxonomy.md     # Event types
├── dojo_nodes.md         # Dojo definitions
└── unity_integration.md  # Unity interface
```

## Core Classes

### SolModule
Main class implementing the SOL logic system.

#### Key Methods

##### __init__(state_file, memory_file)
- Initializes identity, memory, state, world model
- Loads persisted data

##### process_message(user_message, chat_history)
- Main entry point for message processing
- Returns (response_text, actions)

##### normalize_input(user_message, context)
- Converts input to Event object

##### build_context_bundle(user_message, chat_history)
- Creates ContextBundle for reasoning

##### reason_and_reflect(context, user_message)
- Core reasoning logic
- Returns (response, actions)

##### execute_actions(actions)
- Executes generated actions

##### log_event(event)
- Logs event to memory

##### update_memory(context, patterns)
- Updates memory layers

#### Helper Methods

##### _analyze_patterns(context, user_message)
- Pattern recognition logic

##### _generate_reflection(patterns, context)
- Creates reflection text

##### _generate_guidance(patterns, context)
- Creates guidance suggestions

##### _build_response(reflection, guidance, patterns)
- Combines into final response

##### _generate_actions(patterns, context)
- Creates action list

## Data Structures

### Event
```python
@dataclass
class Event:
    type: EventType
    timestamp: float
    data: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
```

### Action
```python
@dataclass
class Action:
    intent: ActionType
    field: Optional[str] = None
    value: Any = None
    data: Dict[str, Any] = field(default_factory=dict)
```

### ContextBundle
```python
@dataclass
class ContextBundle:
    state: Dict[str, Any]
    recent_events: List[Event]
    recent_knowledge: List[Dict[str, Any]]
    chat_history: List[Dict[str, Any]]
```

### MemoryLayer
```python
@dataclass
class MemoryLayer:
    short_term: Dict[str, Any] = field(default_factory=dict)
    mid_term: Dict[str, Any] = field(default_factory=dict)
    long_term: Dict[str, Any] = field(default_factory=dict)
```

## Core Loop Implementation

```python
def process_message(self, user_message, chat_history):
    # 1. Normalize input
    event = self.normalize_input(user_message, {})

    # 2-5. Build context
    context = self.build_context_bundle(user_message, chat_history)

    # 6-7. Reason and respond
    response, actions = self.reason_and_reflect(context, user_message)

    # 8-11. Execute and update
    self.execute_actions(actions)
    self.log_event(event)
    self.update_memory(context, patterns)

    return response, actions
```

## Integration Points

### File System
- state.json: Current state
- `sol_memory.json`: Memory persistence

### External Systems
- Obsidian: For recent knowledge
- Unity: Via API for VR Dojo
- OS Events: For Dojo growth, rituals

### Extensibility
- Modular reasoning components
- Pluggable action handlers
- Configurable memory backends

## Testing

Unit tests for:
- Event normalization
- Context building
- Pattern analysis
- Action execution
- Memory updates

Integration tests for:
- Full message processing loop
- File persistence
- External integrations

## Performance Considerations

- Memory limits on chat history (20 turns)
- Event pruning (last 10 events)
- Lazy loading of large data structures
- Async processing for heavy operations