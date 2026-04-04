"""
Sovereignty Engine
═══════════════════════════════════════════════════
The prime engine. Enforces operator sovereignty across
every kernel interaction. Wraps the SovereigntyCore
with runtime processing, escalation, and audit hooks.

Mathematical Foundation:
  Let S = {s₁, s₂, ..., sₙ} be the set of sovereignty boundaries.
  For any action a ∈ A, sovereignty holds iff:
    ∀sᵢ ∈ S : respects(a, sᵢ) = True
  Sovereignty is conjunctive — one failure rejects the action.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional
import time
import hashlib


class EscalationLevel(Enum):
    SILENT = auto()       # Log only
    NOTIFY = auto()       # Log + notify operator
    BLOCK = auto()        # Log + block action
    HALT = auto()         # Log + halt system


@dataclass
class SovereigntyEvent:
    """An event processed by the sovereignty engine."""
    source: str
    action: str
    target: str
    timestamp: float = field(default_factory=time.time)
    cleared: bool = False
    escalation: EscalationLevel = EscalationLevel.SILENT


class SovereigntyEngine:
    """
    Runtime sovereignty enforcement engine.

    Processes all sovereignty checks, maintains violation history,
    and coordinates with guards for escalation.
    """

    def __init__(self):
        self._event_log: list[SovereigntyEvent] = []
        self._active_boundaries: dict[str, dict] = {}
        self._violation_count: int = 0
        self._escalation_handlers: dict[EscalationLevel, list] = {
            level: [] for level in EscalationLevel
        }
        self._initialize_boundaries()

    def _initialize_boundaries(self):
        """Load core sovereignty boundaries."""
        self._active_boundaries = {
            "identity": {"level": "ABSOLUTE", "mutable": False},
            "consent": {"level": "ABSOLUTE", "mutable": False},
            "dignity": {"level": "ABSOLUTE", "mutable": False},
            "boundaries": {"level": "ABSOLUTE", "mutable": False},
            "data": {"level": "PROTECTED", "mutable": True},
            "modules": {"level": "PROTECTED", "mutable": True},
            "external": {"level": "GUARDED", "mutable": True},
        }

    def clear_message(self, message: Any) -> bool:
        """Sovereignty-clear a kernel message."""
        event = SovereigntyEvent(
            source=getattr(message, 'source', 'unknown'),
            action='message_pass',
            target=getattr(message, 'target', 'unknown'),
        )
        return self._process_event(event)

    def authorize_mount(self, module_name: str) -> bool:
        """Authorize a module to mount in the kernel."""
        event = SovereigntyEvent(
            source="kernel",
            action="mount",
            target=module_name,
        )
        return self._process_event(event)

    def check_action(self, source: str, action: str, target: str) -> bool:
        """General sovereignty check for any action."""
        event = SovereigntyEvent(source=source, action=action, target=target)
        return self._process_event(event)

    def register_escalation_handler(self, level: EscalationLevel, handler):
        """Register a handler for sovereignty escalations."""
        self._escalation_handlers[level].append(handler)

    def get_violation_count(self) -> int:
        return self._violation_count

    def get_event_log(self) -> list[SovereigntyEvent]:
        return self._event_log.copy()

    def compute_integrity_hash(self) -> str:
        """Compute hash of current sovereignty state."""
        state = str(sorted(self._active_boundaries.items()))
        return hashlib.sha256(state.encode()).hexdigest()[:24]

    def _process_event(self, event: SovereigntyEvent) -> bool:
        """Process a sovereignty event through all boundaries."""
        cleared = True
        for name, boundary in self._active_boundaries.items():
            if not self._check_boundary(event, name, boundary):
                cleared = False
                self._violation_count += 1
                event.escalation = self._determine_escalation(boundary)
                self._escalate(event)
                break

        event.cleared = cleared
        self._event_log.append(event)
        return cleared

    def _check_boundary(self, event: SovereigntyEvent, name: str, boundary: dict) -> bool:
        """Check if an event respects a specific boundary."""
        if boundary["level"] == "ABSOLUTE":
            # Only kernel and guards can touch absolute boundaries
            if event.source not in ("kernel", "sovereignty_guard", "integrity_guard"):
                if name in event.target.lower():
                    return False
        return True

    def _determine_escalation(self, boundary: dict) -> EscalationLevel:
        if boundary["level"] == "ABSOLUTE":
            return EscalationLevel.HALT
        elif boundary["level"] == "PROTECTED":
            return EscalationLevel.BLOCK
        return EscalationLevel.NOTIFY

    def _escalate(self, event: SovereigntyEvent):
        for handler in self._escalation_handlers.get(event.escalation, []):
            handler(event)
