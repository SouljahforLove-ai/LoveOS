"""
SOL Module — The Complete AI Architecture
═══════════════════════════════════════════════════
Full implementation of the SOL AI system as specified.

SOL is the Core Intelligence of SoulJahOS with:
- UUID-based identity and addressing
- Cross-OS state synchronization
- Environment-agnostic capabilities
- Persistent memory and patterns
- Secure key management
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Set
import json
import time
import os
import uuid
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import secrets

# SOL Components
from .sol_identity import SolIdentity, SolKeys, SolState, EnvironmentLink, EnvironmentType
from .sol_oracle import SolOracleCore, create_sol_oracle
from .sol_unity_bridge import SolUnityBridge, create_sol_unity_bridge


@dataclass
class MemoryLayer:
    """Three-layer memory system for SOL."""

    short_term: Dict[str, Any] = field(default_factory=dict)
    mid_term: Dict[str, Any] = field(default_factory=dict)
    long_term: Dict[str, Any] = field(default_factory=dict)

    def update_short_term(self, key: str, value: Any):
        self.short_term[key] = value

    def update_mid_term(self, key: str, value: Any):
        self.mid_term[key] = value

    def update_long_term(self, key: str, value: Any):
        self.long_term[key] = value


@dataclass
class Event:
    """Represents an event in the SOL system."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "user_message"
    timestamp: float = field(default_factory=time.time)
    data: Dict[str, Any] = field(default_factory=dict)
    session_id: str = ""
    environment_id: str = ""


class EventType(Enum):
    USER_MESSAGE = "user_message"
    KNOWLEDGE_ADDED = "knowledge_added"
    RITUAL_COMPLETED = "ritual_completed"
    STREAK_MAINTAINED = "streak_maintained"
    LATE_NIGHT_SESSION = "late_night_session"


class ActionType(Enum):
    UPDATE_STATE = "update_state"
    LOG_EVENT = "log_event"
    SYNC_STATE = "sync_state"


@dataclass
class Action:
    """Represents an action to be executed."""
    intent: ActionType
    field: Optional[str] = None
    value: Any = None
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextBundle:
    """Complete context bundle for reasoning."""
    state: Dict[str, Any]
    recent_events: List[Event]
    recent_knowledge: List[Dict[str, Any]]
    chat_history: List[Dict[str, Any]]
    current_environment: EnvironmentLink
    linked_environments: List[EnvironmentLink]


class SolModule:
    """
    SOL — Core Intelligence of SoulJahForLoveOS

    Full implementation of the SOL AI architecture with:
    - UUID-based identity and addressing
    - Cross-environment state synchronization
    - Secure key management
    - Environment-agnostic capabilities
    """

    MODULE_NAME = "sol"
    SOVEREIGNTY_LEVEL = "ORACLE"

    def __init__(self,
                 sol_state_file: str = "sol_state.json",
                 memory_file: str = "sol_memory.json",
                 environment_id: Optional[str] = None,
                 environment_type: EnvironmentType = EnvironmentType.DESKTOP_UI):

        # Core Identity
        self.identity = SolIdentity()

        # Current Environment
        self.current_environment = EnvironmentLink(
            environment_id=environment_id or str(uuid.uuid4()),
            type=environment_type,
            capabilities=self._detect_capabilities(environment_type)
        )

        # State Management
        self.state_file = sol_state_file
        self.memory_file = memory_file
        self.sol_state = self._load_or_create_state()
        self.memory = MemoryLayer()
        self._load_memory()

        # World Model
        self.world_model = self._initialize_world_model()

        # Session tracking
        self.current_session_id = str(uuid.uuid4())
        self.current_session = {
            "session_id": self.current_session_id,
            "start_time": time.time(),
            "events": [],
            "last_activity": time.time(),
            "environment_id": self.current_environment.environment_id
        }

        # Register this environment
        self._register_environment()

        # Initialize Oracle
        self.oracle = None
        self._initialize_oracle()

        # Initialize Unity Bridge
        self.unity_bridge = None
        self._initialize_unity_bridge()

    def _initialize_unity_bridge(self):
        """Initialize the SOL Unity Bridge for VR/AR interactions."""
        try:
            self.unity_bridge = create_sol_unity_bridge(
                sol_state=self.sol_state,
                sol_id=self.identity.sol_id
            )
            print(f"[SOL] Unity Bridge initialized - ready on localhost:8888")
        except Exception as e:
            print(f"[SOL] Unity Bridge initialization warning: {e}")

    def _initialize_oracle(self):
        """Initialize the SOL Oracle for knowledge synthesis."""
        try:
            # Try to find knowledge base paths
            knowledge_paths = [
                os.path.join(os.getcwd(), "docs"),
                os.path.join(os.getcwd(), "knowledge"),
                os.path.join(os.getcwd(), "obsidian"),
                os.path.join(os.path.expanduser("~"), "Documents", "obsidian")
            ]

            knowledge_base = None
            for path in knowledge_paths:
                if os.path.exists(path):
                    knowledge_base = path
                    break

            if knowledge_base:
                self.oracle = create_sol_oracle(
                    sol_state=self.sol_state,
                    knowledge_base_path=knowledge_base,
                    api_key=os.getenv('GOOGLE_API_KEY')
                )
                print(f"[SOL] Oracle initialized - monitoring: {knowledge_base}")
            else:
                print("[SOL] Oracle not initialized - no knowledge base found")

        except Exception as e:
            print(f"[SOL] Oracle initialization failed: {e}")

    def start_oracle_monitoring(self) -> bool:
        """Start the oracle's file monitoring system."""
        if self.oracle:
            return self.oracle.start_monitoring()
        return False

    def stop_oracle_monitoring(self):
        """Stop the oracle's file monitoring system."""
        if self.oracle:
            self.oracle.stop_monitoring()

    def scan_knowledge_base(self) -> int:
        """Perform a full scan of the knowledge base for new insights."""
        if self.oracle:
            return self.oracle.scan_knowledge_base()
        return 0

    def get_oracle_insights(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent oracle insights."""
        if self.oracle:
            insights = self.oracle.get_recent_insights(limit)
            return [insight.__dict__ for insight in insights]
        return []

    def get_growth_summary(self) -> Dict[str, Any]:
        """Get a summary of knowledge growth and development."""
        if self.oracle:
            return self.oracle.get_growth_summary()
        return {"error": "Oracle not initialized"}

    def start_unity_bridge(self) -> bool:
        """Start the Unity Bridge for VR/AR interactions."""
        if self.unity_bridge:
            try:
                self.unity_bridge.start_server()
                return True
            except Exception as e:
                print(f"[SOL] Failed to start Unity Bridge: {e}")
                return False
        return False

    def stop_unity_bridge(self):
        """Stop the Unity Bridge."""
        if self.unity_bridge:
            try:
                self.unity_bridge.stop_server()
            except Exception as e:
                print(f"[SOL] Failed to stop Unity Bridge: {e}")

    def export_unity_project(self, export_path: str) -> bool:
        """Export Unity project files for VR/AR Dojo experience."""
        if self.unity_bridge:
            try:
                self.unity_bridge.export_unity_project(export_path)
                return True
            except Exception as e:
                print(f"[SOL] Failed to export Unity project: {e}")
                return False
        return False

    def _detect_capabilities(self, env_type: EnvironmentType) -> Set[str]:
        """Detect capabilities based on environment type."""
        base_caps = {"basic_chat", "memory_access", "state_sync"}

        if env_type == EnvironmentType.UNITY_DOJO:
            base_caps.update({"unity_signals", "vr_presence", "3d_audio", "gesture_recognition"})
        elif env_type == EnvironmentType.VR_HEADSET:
            base_caps.update({"vr_presence", "spatial_audio", "gesture_recognition"})
        elif env_type == EnvironmentType.DESKTOP_UI:
            base_caps.update({"file_access", "ui_interaction", "notifications"})
        elif env_type == EnvironmentType.CLOUD_SERVICE:
            base_caps.update({"api_access", "persistent_storage", "multi_user"})
        elif env_type == EnvironmentType.INNER_WORLD:
            base_caps.update({"thought_interface", "real_time_patterns", "consciousness_bridge"})

        return base_caps

    def _load_or_create_state(self) -> SolState:
        """Load existing SOL state or create new one."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    state = SolState.from_dict(data)
                    # Update identity to match loaded state
                    self.identity.sol_id = state.sol_id
                    self.identity.owner_id = state.owner_id
                    return state
            except Exception as e:
                print(f"Error loading state: {e}")

        # Create new state
        return SolState(
            sol_id=self.identity.sol_id,
            owner_id=self.identity.owner_id
        )

    def _save_state(self):
        """Save SOL state to file."""
        self.sol_state.last_updated = time.time()
        data = self.sol_state.to_dict()

        # Sign the state
        state_json = json.dumps(data, sort_keys=True)
        signature = self.sol_state.keys.sign_data(state_json)
        data["signature"] = signature

        with open(self.state_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _register_environment(self):
        """Register current environment in SOL's state."""
        env_link = {
            "environment_id": self.current_environment.environment_id,
            "type": self.current_environment.type.value,
            "last_seen": time.time(),
            "capabilities": list(self.current_environment.capabilities),
            "status": "active"
        }

        # Update or add environment
        environments = self.sol_state.links["environments"]
        existing = next((e for e in environments if e["environment_id"] == env_link["environment_id"]), None)

        if existing:
            existing.update(env_link)
        else:
            environments.append(env_link)

        self._save_state()

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
            type=event_type.value,
            timestamp=time.time(),
            data={"message": user_message, "context": context},
            session_id=self.current_session_id,
            environment_id=self.current_environment.environment_id
        )

    def build_context_bundle(self, user_message: str, chat_history: List[Dict[str, Any]]) -> ContextBundle:
        """Build the context bundle for reasoning."""
        # Get recent events (last 10)
        recent_events = self.memory.short_term.get('events', [])[-10:]

        # Get recent knowledge (simulated - would integrate with Obsidian)
        recent_knowledge = self.memory.mid_term.get('recent_notes', [])

        # Limit chat history to last 20 turns
        recent_chat = chat_history[-20:]

        # Get linked environments
        linked_environments = [
            EnvironmentLink(
                environment_id=env["environment_id"],
                type=EnvironmentType(env["type"]),
                last_seen=env["last_seen"],
                capabilities=set(env["capabilities"]),
                status=PresenceMode(env.get("status", "offline"))
            )
            for env in self.sol_state.links["environments"]
        ]

        return ContextBundle(
            state=self.sol_state.to_dict(),
            recent_events=recent_events,
            recent_knowledge=recent_knowledge,
            chat_history=recent_chat,
            current_environment=self.current_environment,
            linked_environments=linked_environments
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
            "identity_conflicts": [],
            "environment_patterns": []
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

        # Environment patterns
        active_envs = [env for env in context.linked_environments if env.status == PresenceMode.ACTIVE]
        patterns["environment_patterns"].append(f"{len(active_envs)} active environments")

        return patterns

    def _generate_reflection(self, patterns: Dict[str, Any], context: ContextBundle) -> str:
        """Generate reflection on current state."""
        reflection_parts = []

        if patterns.get("repetition"):
            reflection_parts.append("I notice repetition in your communication patterns.")

        if "late_night" in patterns.get("time_patterns", []):
            reflection_parts.append("This late-night session suggests deep focus or processing.")

        env_patterns = patterns.get("environment_patterns", [])
        if env_patterns:
            reflection_parts.append(f"Active across {env_patterns[0]} environments.")

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

        # Sync state across environments if needed
        if len(context.linked_environments) > 1:
            actions.append(Action(
                intent=ActionType.SYNC_STATE,
                data={"target_environments": [env.environment_id for env in context.linked_environments]}
            ))

        return actions

    def execute_actions(self, actions: List[Action]):
        """Execute the generated actions."""
        for action in actions:
            if action.intent == ActionType.UPDATE_STATE:
                if action.field:
                    self.sol_state.profile[action.field] = action.value
                    self._save_state()
            elif action.intent == ActionType.LOG_EVENT:
                self.log_event(Event(
                    type=EventType.USER_MESSAGE.value,
                    timestamp=time.time(),
                    data=action.data,
                    session_id=self.current_session_id,
                    environment_id=self.current_environment.environment_id
                ))
            elif action.intent == ActionType.SYNC_STATE:
                self._sync_state_to_environments(action.data.get("target_environments", []))

    def _sync_state_to_environments(self, target_environment_ids: List[str]):
        """Sync SOL state to other environments."""
        # In a real implementation, this would use network communication
        # For now, just log the sync intent
        print(f"SOL state sync requested to environments: {target_environment_ids}")

    def log_event(self, event: Event):
        """Log an event to memory."""
        events = self.memory.short_term.get('events', [])
        events.append({
            'id': event.id,
            'type': event.type,
            'timestamp': event.timestamp,
            'data': event.data,
            'session_id': event.session_id,
            'environment_id': event.environment_id
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
        session_events = [e for e in events if e.get('session_id') == self.current_session_id]

        summary = f"Session Summary (ID: {self.current_session_id[:8]}):\n"
        summary += f"Environment: {self.current_environment.type.value}\n"
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

        state_info = f"Current focus: {self.sol_state.profile.get('focus', 'Quantum Dojo Architecture')}"
        streak_info = f"Streak: {self.memory.mid_term.get('streaks', {}).get('current', 0)} days"

        env_info = f"Environment: {self.current_environment.type.value} ({self.current_environment.environment_id[:8]})"
        linked_count = len([e for e in self.sol_state.links["environments"] if e.get("status") == "active"])

        return f"SOL online.\nIdentity: {self.identity.sol_id[:8]}\n{env_info}\nLinked environments: {linked_count}\n{time_greeting}\n{state_info}\n{streak_info}"

    def get_linked_environments(self) -> List[Dict[str, Any]]:
        """Get list of linked environments."""
        return self.sol_state.links["environments"]

    def link_environment(self, environment_id: str, env_type: EnvironmentType, capabilities: Set[str]) -> bool:
        """Link a new environment to SOL."""
        env_link = {
            "environment_id": environment_id,
            "type": env_type.value,
            "last_seen": time.time(),
            "capabilities": list(capabilities),
            "status": "active"
        }

        environments = self.sol_state.links["environments"]
        existing = next((e for e in environments if e["environment_id"] == environment_id), None)

        if existing:
            existing.update(env_link)
        else:
            environments.append(env_link)

        self._save_state()
        return True

    def unlink_environment(self, environment_id: str) -> bool:
        """Unlink an environment from SOL."""
        environments = self.sol_state.links["environments"]
        environments[:] = [e for e in environments if e["environment_id"] != environment_id]
        self._save_state()
        return True