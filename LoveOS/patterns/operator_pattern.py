"""
Operator Pattern
═══════════════════════════════════════════════════
Defines the behavioral patterns of the Operator — the
sovereign user at the center of LoveOS.

The Operator Pattern governs:
  - How the operator interacts with the system
  - Default response behaviors to operator state changes
  - Sovereignty maintenance during operator workflows
  - Ritual triggers based on operator behavior
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Optional
import time


class OperatorMode(Enum):
    """Current operational mode of the operator."""
    ACTIVE = auto()         # Engaged and processing
    REFLECTIVE = auto()     # Contemplative / journaling
    BUILDING = auto()       # Architecture / creation mode
    GROUNDING = auto()      # In grounding ritual
    TEACHING = auto()       # Legacy transmission to Zen
    RESTING = auto()        # Low-energy / recovery
    SOVEREIGN = auto()      # Full sovereignty assertion


@dataclass
class OperatorState:
    """Current state of the operator."""
    mode: OperatorMode = OperatorMode.ACTIVE
    sovereignty_level: float = 1.0
    energy_level: float = 0.8
    focus_target: str = ""
    session_duration: float = 0.0
    interactions_count: int = 0
    last_grounding: float = 0.0
    last_ritual: str = ""


class OperatorPattern:
    """
    Behavioral pattern engine for the Operator.
    
    Monitors operator state and triggers appropriate responses:
    - Sovereignty drop → Grounding ritual
    - Extended session → Rest suggestion
    - Teaching mode → Legacy capture activation
    - Building mode → Minimize interruptions, silent security
    """

    # Thresholds
    SOVEREIGNTY_FLOOR = 0.4          # Below this triggers grounding
    ENERGY_WARNING = 0.3             # Below this suggests rest
    SESSION_LONG_THRESHOLD = 7200    # 2 hours → suggest break
    GROUNDING_COOLDOWN = 1800        # 30 min between groundings

    def __init__(self):
        self.state = OperatorState()
        self._handlers: dict[str, list[Callable]] = {
            "sovereignty_drop": [],
            "energy_low": [],
            "session_long": [],
            "mode_change": [],
            "teaching_start": [],
        }
        self._log: list[dict] = []

    def update_state(self, **kwargs) -> list[str]:
        """Update operator state and return triggered events."""
        triggered = []
        old_mode = self.state.mode

        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)

        # Check sovereignty
        if self.state.sovereignty_level < self.SOVEREIGNTY_FLOOR:
            triggered.append("sovereignty_drop")
            self._fire("sovereignty_drop")

        # Check energy
        if self.state.energy_level < self.ENERGY_WARNING:
            triggered.append("energy_low")
            self._fire("energy_low")

        # Check session duration
        if self.state.session_duration > self.SESSION_LONG_THRESHOLD:
            triggered.append("session_long")
            self._fire("session_long")

        # Check mode transition
        if self.state.mode != old_mode:
            triggered.append("mode_change")
            self._fire("mode_change")
            if self.state.mode == OperatorMode.TEACHING:
                triggered.append("teaching_start")
                self._fire("teaching_start")

        self._log.append({"state_update": kwargs, "triggered": triggered, "timestamp": time.time()})
        return triggered

    def register_handler(self, event: str, handler: Callable):
        """Register a handler for an operator event."""
        if event in self._handlers:
            self._handlers[event].append(handler)

    def _fire(self, event: str):
        for handler in self._handlers.get(event, []):
            try:
                handler(self.state)
            except Exception:
                pass  # Silent — no pop-ups

    def needs_grounding(self) -> bool:
        """Check if operator needs grounding."""
        if self.state.sovereignty_level < self.SOVEREIGNTY_FLOOR:
            cooldown_elapsed = (time.time() - self.state.last_grounding) > self.GROUNDING_COOLDOWN
            return cooldown_elapsed
        return False

    def get_recommended_action(self) -> Optional[str]:
        """Get the most appropriate action for current state."""
        if self.needs_grounding():
            return "grounding_ritual"
        if self.state.energy_level < self.ENERGY_WARNING:
            return "rest_suggestion"
        if self.state.session_duration > self.SESSION_LONG_THRESHOLD:
            return "break_suggestion"
        if self.state.mode == OperatorMode.TEACHING:
            return "legacy_capture"
        return None

    def get_summary(self) -> dict:
        return {
            "mode": self.state.mode.name,
            "sovereignty": self.state.sovereignty_level,
            "energy": self.state.energy_level,
            "focus": self.state.focus_target,
            "session_minutes": round(self.state.session_duration / 60, 1),
            "recommended_action": self.get_recommended_action(),
        }
