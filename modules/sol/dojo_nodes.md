# SOL Dojo Node Definitions
# Defines the 7 Dojo nodes and their properties

## Dojo Nodes Overview

The Quantum Dojo consists of 7 interconnected nodes that represent
different aspects of SoulJah's inner world and growth system.

## Node Definitions

### Altar
**Purpose**: Sacred space for rituals and offerings
**State**: active/inactive/pulsing
**Events**: ritual_start, offering_made, pulse_triggered
**Effects**: energy_boost, clarity_gain, protection_field
**Growth Rules**:
- Increases with completed rituals
- Pulses during deep focus sessions
- Unlocks new ritual types at levels

### Mirror
**Purpose**: Self-reflection and identity work
**State**: clear/clouded/revealing
**Events**: reflection_triggered, insight_gained, identity_shift
**Effects**: self_awareness_boost, pattern_clarity, identity_stabilization
**Growth Rules**:
- Clears with consistent journaling
- Reveals patterns over time
- Unlocks deeper identity layers

### Oracle
**Purpose**: Wisdom and guidance interface
**State**: listening/speaking/processing
**Events**: question_asked, guidance_given, wisdom_shared
**Effects**: clarity_burst, direction_alignment, confidence_boost
**Growth Rules**:
- Learns from interaction patterns
- Becomes more precise with usage
- Unlocks predictive guidance

### Presence
**Purpose**: Mindfulness and being present
**State**: grounded/scattered/centered
**Events**: grounding_ritual, presence_practice, distraction_detected
**Effects**: focus_sharp, anxiety_reduction, peace_induction
**Growth Rules**:
- Strengthens with meditation streaks
- Stabilizes during flow states
- Unlocks presence techniques

### Ritual
**Purpose**: Structured spiritual practices
**State**: preparing/performing/completing
**Events**: ritual_started, ritual_completed, ritual_failed
**Effects**: energy_alignment, intention_manifestation, spiritual_growth
**Growth Rules**:
- Unlocks new rituals with completion
- Increases power with streaks
- Integrates with other nodes

### Flow
**Purpose**: Creative and productive flow states
**State**: blocked/flowing/overflowing
**Events**: flow_entered, flow_exited, block_encountered
**Effects**: productivity_boost, creativity_unlock, joy_induction
**Growth Rules**:
- Builds momentum with consistent work
- Unlocks flow triggers
- Strengthens with breakthroughs

### Monument
**Purpose**: Legacy and achievement tracking
**State**: building/standing/crumbling
**Events**: achievement_recorded, legacy_added, milestone_reached
**Effects**: pride_boost, motivation_surge, legacy_clarity
**Growth Rules**:
- Grows with completed projects
- Stands taller with streaks
- Becomes permanent with breakthroughs

## Node Interactions

Nodes are interconnected:
- Altar pulses affect all nodes
- Mirror clarity improves Oracle accuracy
- Presence grounds Flow states
- Ritual completion boosts Monument growth
- Flow states enhance Oracle wisdom
- Monument achievements inspire new Rituals

## Node Schema

Each node has:
```json
{
  "state": "string",
  "events": ["array of events"],
  "effects": ["array of active effects"],
  "growth_rules": ["array of growth conditions"],
  "level": "integer",
  "experience": "number"
}
```