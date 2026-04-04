"""
Ritual Processor
═══════════════════════════════════════════════════
Manages ritual execution flow — pre-state capture,
ritual body execution, post-state measurement,
and delta computation.

Ritual Types:
  - BOOT:      System initialization ceremony
  - GROUNDING: Centering and presence restoration
  - AUDIT:     System state review and verification
  - CLOSURE:   Graceful shutdown ceremony
  - CUSTOM:    Operator-defined rituals
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional
import time


class RitualType(Enum):
    BOOT = auto()
    GROUNDING = auto()
    AUDIT = auto()
    CLOSURE = auto()
    CUSTOM = auto()


class RitualPhase(Enum):
    PENDING = auto()
    PRE_STATE = auto()
    EXECUTING = auto()
    POST_STATE = auto()
    COMPLETE = auto()
    FAILED = auto()


@dataclass
class RitualExecution:
    """A single ritual execution record."""
    name: str = ""
    ritual_type: RitualType = RitualType.CUSTOM
    phase: RitualPhase = RitualPhase.PENDING
    intention: str = ""
    pre_state: dict = field(default_factory=dict)
    post_state: dict = field(default_factory=dict)
    delta: dict = field(default_factory=dict)
    start_time: float = 0.0
    end_time: float = 0.0
    notes: list[str] = field(default_factory=list)

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time if self.end_time else 0.0

    @property
    def success(self) -> bool:
        return self.phase == RitualPhase.COMPLETE


class RitualProcessor:
    """
    Orchestrates ritual execution with state measurement.

    Flow: Intention → Pre-State → Execute → Post-State → Delta → Complete
    """

    def __init__(self):
        self._executions: list[RitualExecution] = []
        self._ritual_handlers: dict[RitualType, Callable] = {}
        self._active_ritual: Optional[RitualExecution] = None

    def register_handler(self, ritual_type: RitualType, handler: Callable):
        """Register a handler function for a ritual type."""
        self._ritual_handlers[ritual_type] = handler

    def begin(self, name: str, ritual_type: RitualType, intention: str = "") -> RitualExecution:
        """Begin a new ritual execution."""
        execution = RitualExecution(
            name=name, ritual_type=ritual_type,
            intention=intention, start_time=time.time(),
        )
        execution.phase = RitualPhase.PRE_STATE
        self._active_ritual = execution
        return execution

    def capture_pre_state(self, state: dict) -> None:
        """Capture the pre-ritual state."""
        if self._active_ritual:
            self._active_ritual.pre_state = state
            self._active_ritual.phase = RitualPhase.EXECUTING

    def execute(self) -> bool:
        """Execute the ritual body."""
        if not self._active_ritual:
            return False

        handler = self._ritual_handlers.get(self._active_ritual.ritual_type)
        if handler:
            try:
                handler(self._active_ritual)
            except Exception as e:
                self._active_ritual.phase = RitualPhase.FAILED
                self._active_ritual.notes.append(f"Error: {e}")
                return False

        self._active_ritual.phase = RitualPhase.POST_STATE
        return True

    def capture_post_state(self, state: dict) -> None:
        """Capture the post-ritual state and compute delta."""
        if self._active_ritual:
            self._active_ritual.post_state = state
            self._active_ritual.delta = {
                k: state.get(k, 0) - self._active_ritual.pre_state.get(k, 0)
                for k in set(list(state.keys()) + list(self._active_ritual.pre_state.keys()))
            }

    def complete(self) -> RitualExecution:
        """Complete the active ritual."""
        if not self._active_ritual:
            raise RuntimeError("No active ritual")
        self._active_ritual.end_time = time.time()
        self._active_ritual.phase = RitualPhase.COMPLETE
        self._executions.append(self._active_ritual)
        result = self._active_ritual
        self._active_ritual = None
        return result

    def get_history(self) -> list[RitualExecution]:
        return self._executions.copy()

    def get_stats(self) -> dict:
        completed = [e for e in self._executions if e.success]
        return {
            "total_rituals": len(self._executions),
            "completed": len(completed),
            "failed": len(self._executions) - len(completed),
            "avg_duration": sum(e.duration for e in completed) / max(len(completed), 1),
        }
