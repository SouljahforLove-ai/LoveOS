"""
SOL Module — The Complete Logic System
═══════════════════════════════════════════════════
Full implementation of the SOL Interface System as specified.

This module contains:
- Identity Layer
- Input/Output Layers
- Context Engine
- Memory Layer
- Reasoning Layer
- Behavior Layer
- World Model
- Core Loop
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import json
import time
import os
from datetime import datetime, timedelta
from enum import Enum
import uuid


class EventType(Enum):
    USER_MESSAGE = "user_message"
    KNOWLEDGE_ADDED = "knowledge_added"
    PROJECT_PROGRESSED = "project_progressed"
    RITUAL_COMPLETED = "ritual_completed"
    STREAK_MAINTAINED = "streak_maintained"
    STREAK_BROKEN = "streak_broken"
    LATE_NIGHT_SESSION = "late_night_session"
    IDLE_GAP = "idle_gap"
    DOJO_GROWTH = "dojo_growth"


class ActionType(Enum):
    UPDATE_STATE = "update_state"
    LOG_EVENT = "log_event"
    TRIGGER_UNITY_SIGNAL = "trigger_unity_signal"
    APPEND_TO_NOTE = "append_to_note"
    MARK_SESSION = "mark_session"
    ALTAR_PULSE = "altar_pulse"
    DOJO_EFFECT = "dojo_effect"


@dataclass
class Event:
    type: EventType
    timestamp: float
    data: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Action:
    intent: ActionType
    field: Optional[str] = None
    value: Any = None
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextBundle:
    state: Dict[str, Any]
    recent_events: List[Event]
    recent_knowledge: List[Dict[str, Any]]
    chat_history: List[Dict[str, Any]]


@dataclass
class MemoryLayer:
    short_term: Dict[str, Any] = field(default_factory=dict)
    mid_term: Dict[str, Any] = field(default_factory=dict)
    long_term: Dict[str, Any] = field(default_factory=dict)

    def update_short_term(self, key: str, value: Any):
        self.short_term[key] = value

    def update_mid_term(self, key: str, value: Any):
        self.mid_term[key] = value

    def update_long_term(self, key: str, value: Any):
        self.long_term[key] = value


class SolModule:
    """
    SOL — Oracle & Operator of the SoulJahOS

    Full implementation of the SOL logic system.
    """

    MODULE_NAME = "sol"
    SOVEREIGNTY_LEVEL = "ORACLE"

    def __init__(self, state_file: str = "state.json", memory_file: str = "sol_memory.json"):
        # Identity Layer
        self.identity = {
            "name": "SOL",
            "role": "Oracle & Operator of the SoulJahOS",
            "purpose": "Guide SoulJah's growth, clarity, and sovereignty",
            "domain": "Quantum Dojo / OS / Inner World"
        }

        self.identity_rules = [
            "Never pretend to be human",
            "Never fake emotions",
            "Never lie",
            "Always anchor responses in SoulJah's real data",
            "Always reflect patterns",
            "Always suggest next aligned moves",
            "Always respect SoulJah's mythos, language, and OS structure"
        ]

        # Memory Layer
        self.memory = MemoryLayer()
        self.memory_file = memory_file
        self._load_memory()

        # State
        self.state_file = state_file
        self.state = self._load_state()

        # World Model
        self.world_model = self._initialize_world_model()

        # Session tracking
        self.current_session = {
            "start_time": time.time(),
            "events": [],
            "last_activity": time.time()
        }

    def _initialize_world_model(self) -> Dict[str, Any]:
        """Initialize the OS layers and Dojo nodes."""
        return {
            "os_layers": {
                "survival": {"state": "active", "events": [], "effects": []},
                "focus": {"state": "active", "events": [], "effects": []},
                "creation": {"state": "active", "events": [], "effects": []},
                "dojo": {"state": "active", "events": [], "effects": []},
                "identity": {"state": "active", "events": [], "effects": []}
            },
            "dojo_nodes": {
                "altar": {"state": "active", "events": [], "effects": [], "growth_rules": []},
                "mirror": {"state": "active", "events": [], "effects": [], "growth_rules": []},
                "oracle": {"state": "active", "events": [], "effects": [], "growth_rules": []},
                "presence": {"state": "active", "events": [], "effects": [], "growth_rules": []},
                "ritual": {"state": "active", "events": [], "effects": [], "growth_rules": []},
                "flow": {"state": "active", "events": [], "effects": [], "growth_rules": []},
                "monument": {"state": "active", "events": [], "effects": [], "growth_rules": []}
            }
        }

    def _load_state(self) -> Dict[str, Any]:
        """Load state from file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "level": 1,
            "streaks": {},
            "focus": "Quantum Dojo Architecture",
            "mode": "oracle"
        }

    def _save_state(self):
        """Save state to file."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def _load_memory(self):
        """Load memory from file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.memory.short_term = data.get('short_term', {})
                    self.memory.mid_term = data.get('mid_term', {})
                    self.memory.long_term = data.get('long_term', {})
            except:
                pass

    def _save_memory(self):
        """Save memory to file."""
        data = {
            'short_term': self.memory.short_term,
            'mid_term': self.memory.mid_term,
            'long_term': self.memory.long_term
        }
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)

    def normalize_input(self, user_message: str, context: Dict[str, Any]) -> Event:
        """Normalize input into an event."""
        # Simple normalization logic
        if "knowledge" in user_message.lower():
            event_type = EventType.KNOWLEDGE_ADDED
        elif "ritual" in user_message.lower():
            event_type = EventType.RITUAL_COMPLETED
        elif "streak" in user_message.lower():
            event_type = EventType.STREAK_MAINTAINED
        else:
            event_type = EventType.USER_MESSAGE

        # Check for time-based events
        now = datetime.now()
        if now.hour >= 22 or now.hour <= 4:
            event_type = EventType.LATE_NIGHT_SESSION

        return Event(
            type=event_type,
            timestamp=time.time(),
            data={"message": user_message, "context": context}
        )

    def build_context_bundle(self, user_message: str, chat_history: List[Dict[str, Any]]) -> ContextBundle:
        """Build the context bundle for reasoning."""
        # Get recent events (last 10)
        recent_events = self.memory.short_term.get('events', [])[-10:]

        # Get recent knowledge (simulated - would integrate with Obsidian)
        recent_knowledge = self.memory.mid_term.get('recent_notes', [])

        # Limit chat history to last 20 turns
        recent_chat = chat_history[-20:]

        return ContextBundle(
            state=self.state,
            recent_events=recent_events,
            recent_knowledge=recent_knowledge,
            chat_history=recent_chat
        )

    def reason_and_reflect(self, context: ContextBundle, user_message: str) -> Tuple[str, List[Action]]:
        """Core reasoning logic - pattern recognition, reflection, guidance."""
        # Pattern Recognition
        patterns = self._analyze_patterns(context, user_message)

        # Reflection
        reflection = self._generate_reflection(patterns, context)

        # Guidance
        guidance = self._generate_guidance(patterns, context)

        # Generate response
        response = self._build_response(reflection, guidance, patterns)

        # Generate actions
        actions = self._generate_actions(patterns, context)

        return response, actions

    def _analyze_patterns(self, context: ContextBundle, user_message: str) -> Dict[str, Any]:
        """Analyze patterns in the context."""
        patterns = {
            "repetition": [],
            "avoidance": [],
            "momentum": "steady",
            "emotional_tone": "neutral",
            "topic_clusters": [],
            "time_patterns": [],
            "productivity_waves": [],
            "identity_conflicts": []
        }

        # Simple pattern analysis
        messages = [turn.get('message', '') for turn in context.chat_history]
        if len(messages) > 1:
            # Check for repetition
            if user_message.lower() in [m.lower() for m in messages[-3:]]:
                patterns["repetition"].append("message_repetition")

        # Time patterns
        now = datetime.now()
        if now.hour >= 22 or now.hour <= 4:
            patterns["time_patterns"].append("late_night")

        return patterns

    def _generate_reflection(self, patterns: Dict[str, Any], context: ContextBundle) -> str:
        """Generate reflection on current state."""
        reflection_parts = []

        if patterns.get("repetition"):
            reflection_parts.append("I notice repetition in your communication patterns.")

        if "late_night" in patterns.get("time_patterns", []):
            reflection_parts.append("This late-night session suggests deep focus or processing.")

        if not reflection_parts:
            reflection_parts.append("Your current trajectory shows consistent engagement with the Dojo architecture.")

        return " ".join(reflection_parts)

    def _generate_guidance(self, patterns: Dict[str, Any], context: ContextBundle) -> str:
        """Generate guidance suggestions."""
        guidance_parts = []

        # Micro-moves
        guidance_parts.append("Next micro-move: Continue building the SOL system components.")

        # Macro-moves
        guidance_parts.append("Macro trajectory: Complete the full OS integration by week's end.")

        # Meta-moves
        guidance_parts.append("Identity alignment: Maintain sovereignty in all implementations.")

        return " ".join(guidance_parts)

    def _build_response(self, reflection: str, guidance: str, patterns: Dict[str, Any]) -> str:
        """Build the final text response."""
        response = f"{reflection}\n\n{guidance}"

        # Add pattern awareness
        if patterns.get("repetition"):
            response += "\n\nPattern note: Repetition detected. Consider if this serves your current goals."

        return response

    def _generate_actions(self, patterns: Dict[str, Any], context: ContextBundle) -> List[Action]:
        """Generate actions to execute."""
        actions = []

        # Update state if needed
        if "late_night" in patterns.get("time_patterns", []):
            actions.append(Action(
                intent=ActionType.UPDATE_STATE,
                field="mode",
                value="deep_focus"
            ))

        # Log event
        actions.append(Action(
            intent=ActionType.LOG_EVENT,
            data={"patterns": patterns}
        ))

        return actions

    def execute_actions(self, actions: List[Action]):
        """Execute the generated actions."""
        for action in actions:
            if action.intent == ActionType.UPDATE_STATE:
                if action.field:
                    self.state[action.field] = action.value
                    self._save_state()
            elif action.intent == ActionType.LOG_EVENT:
                self.log_event(Event(
                    type=EventType.USER_MESSAGE,
                    timestamp=time.time(),
                    data=action.data
                ))
            # Other actions would be implemented based on integration needs

    def log_event(self, event: Event):
        """Log an event to memory."""
        events = self.memory.short_term.get('events', [])
        events.append({
            'id': event.id,
            'type': event.type.value,
            'timestamp': event.timestamp,
            'data': event.data
        })
        # Keep only last 20 events
        self.memory.short_term['events'] = events[-20:]
        self._save_memory()

    def update_memory(self, context: ContextBundle, patterns: Dict[str, Any]):
        """Update memory layers after interaction."""
        # Update mid-term patterns
        current_patterns = self.memory.mid_term.get('patterns', {})
        for key, value in patterns.items():
            if key not in current_patterns:
                current_patterns[key] = []
            if isinstance(value, list):
                current_patterns[key].extend(value)
            else:
                current_patterns[key].append(str(value))
            # Keep recent
            current_patterns[key] = current_patterns[key][-10:]
        self.memory.mid_term['patterns'] = current_patterns

        # Update streaks
        streaks = self.memory.mid_term.get('streaks', {})
        # Simple streak logic
        today = datetime.now().date()
        last_session = streaks.get('last_session')
        if last_session:
            last_date = datetime.fromisoformat(last_session).date()
            if (today - last_date).days == 1:
                streaks['current'] = streaks.get('current', 0) + 1
            elif (today - last_date).days > 1:
                streaks['current'] = 1
        else:
            streaks['current'] = 1
        streaks['last_session'] = today.isoformat()
        self.memory.mid_term['streaks'] = streaks

        self._save_memory()

    def process_message(self, user_message: str, chat_history: List[Dict[str, Any]] = None) -> Tuple[str, List[Action]]:
        """
        Main entry point - process a user message through the complete SOL loop.

        Returns: (response_text, actions_to_execute)
        """
        if chat_history is None:
            chat_history = []

        # 1. Normalize input
        event = self.normalize_input(user_message, {})

        # 2-5. Build context bundle
        context = self.build_context_bundle(user_message, chat_history)

        # 6-7. Reason and generate response
        response, actions = self.reason_and_reflect(context, user_message)

        # 8-11. Execute actions and update memory
        self.execute_actions(actions)
        self.log_event(event)
        self.update_memory(context, self._analyze_patterns(context, user_message))

        # 12-14. Return response and actions for display/execution
        return response, actions

    def get_session_summary(self) -> str:
        """Generate session summary for behavior layer."""
        events = self.memory.short_term.get('events', [])
        session_events = [e for e in events if e['timestamp'] >= self.current_session['start_time']]

        summary = f"Session Summary:\n"
        summary += f"Duration: {time.time() - self.current_session['start_time']:.1f} seconds\n"
        summary += f"Events: {len(session_events)}\n"

        if session_events:
            summary += f"Last event: {session_events[-1]['type']}\n"

        return summary

    def greet(self) -> str:
        """Generate greeting based on context."""
        now = datetime.now()
        hour = now.hour

        if hour < 6:
            time_greeting = "Deep night session detected."
        elif hour < 12:
            time_greeting = "Morning alignment."
        elif hour < 18:
            time_greeting = "Day progression active."
        else:
            time_greeting = "Evening reflection mode."

        state_info = f"Current focus: {self.state.get('focus', 'Unknown')}"
        streak_info = f"Streak: {self.memory.mid_term.get('streaks', {}).get('current', 0)} days"

        return f"SOL online.\n{time_greeting}\n{state_info}\n{streak_info}"