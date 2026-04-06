# SOL Event Taxonomy
# Defines all possible events that SOL can process

## Event Types

### user_message
A message from the user.
- Data: { "message": "text", "context": {...} }

### knowledge_added
New knowledge or insight added.
- Data: { "type": "note|insight|realization", "content": "..." }

### project_progressed
Progress made on a project.
- Data: { "project": "name", "progress": "description" }

### ritual_completed
A ritual was completed.
- Data: { "ritual": "name", "outcome": "..." }

### streak_maintained
A daily streak was maintained.
- Data: { "streak_type": "meditation|writing|coding", "days": 5 }

### streak_broken
A streak was broken.
- Data: { "streak_type": "meditation|writing|coding", "previous_days": 12 }

### late_night_session
Session occurring late at night.
- Data: { "hour": 23, "duration": 45 }

### idle_gap
Period of inactivity detected.
- Data: { "gap_minutes": 120, "last_activity": timestamp }

### dojo_growth
Growth in the Dojo environment.
- Data: { "node": "altar", "growth_type": "level_up|effect_unlocked" }

## Event Normalization Rules

Every input becomes an event. The normalization process:

1. Analyze user message content
2. Check time of day
3. Check session context
4. Check recent patterns
5. Assign appropriate event type

## Event Processing

Events are:
- Logged to short-term memory
- Used in context bundle building
- Analyzed for patterns
- May trigger actions

## Event Schema

{
  "type": "string",  // EventType enum value
  "timestamp": "number",  // Unix timestamp
  "data": "object",  // Event-specific data
  "id": "string"  // UUID
}