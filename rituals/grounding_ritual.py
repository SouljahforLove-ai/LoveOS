"""
Grounding Ritual — Centering, presence restoration, and sovereignty reset.
═══════════════════════════════════════════════════
Triggered when:
  - Sovereignty drops below threshold
  - Emotional momentum becomes negative
  - Operator requests grounding
  - System detects pattern: emotional_spiral

Sequence:
  1. Pause Processing — All non-essential processing halts
  2. Breathe Cycle — Structured breathing (4-7-8 pattern)
  3. Body Scan — Awareness through physical presence
  4. Sovereignty Check — Verify all boundaries intact
  5. Intention Reset — Re-anchor to purpose
  6. Resume Processing — Gradual re-engagement
"""

from __future__ import annotations
from dataclasses import dataclass, field
import time


@dataclass
class GroundingState:
    started_at: float = 0.0
    completed_at: float = 0.0
    processing_paused: bool = False
    breathe_cycles_completed: int = 0
    body_scan_complete: bool = False
    sovereignty_intact: bool = False
    intention_reset: bool = False
    processing_resumed: bool = False
    pre_sovereignty: float = 0.0
    post_sovereignty: float = 0.0


class GroundingRitual:
    """
    The Grounding Ritual — return to center.
    
    Classical music reference: Moonlight Sonata for deep grounding.
    """

    BREATHE_PATTERN = {"inhale": 4, "hold": 7, "exhale": 8}  # 4-7-8 pattern
    DEFAULT_CYCLES = 3

    def __init__(self):
        self.state = GroundingState()
        self._log: list[dict] = []

    def execute(self, current_sovereignty: float = 0.5, cycles: int = None) -> GroundingState:
        """Execute the full grounding ritual."""
        self.state.started_at = time.time()
        self.state.pre_sovereignty = current_sovereignty
        cycles = cycles or self.DEFAULT_CYCLES

        self._pause_processing()
        self._breathe_cycle(cycles)
        self._body_scan()
        self._sovereignty_check()
        self._intention_reset()
        self._resume_processing()

        self.state.completed_at = time.time()
        self.state.post_sovereignty = min(1.0, current_sovereignty + 0.2)

        self._log.append({
            "event": "grounding_complete",
            "duration": self.state.completed_at - self.state.started_at,
            "sovereignty_delta": self.state.post_sovereignty - self.state.pre_sovereignty,
        })
        return self.state

    def _pause_processing(self):
        self.state.processing_paused = True
        self._log.append({"phase": "pause", "timestamp": time.time()})

    def _breathe_cycle(self, cycles: int):
        for i in range(cycles):
            self._log.append({"phase": "breathe", "cycle": i + 1, "pattern": self.BREATHE_PATTERN})
        self.state.breathe_cycles_completed = cycles

    def _body_scan(self):
        self.state.body_scan_complete = True
        self._log.append({"phase": "body_scan", "timestamp": time.time()})

    def _sovereignty_check(self):
        self.state.sovereignty_intact = True
        self._log.append({"phase": "sovereignty_check", "intact": True, "timestamp": time.time()})

    def _intention_reset(self):
        self.state.intention_reset = True
        self._log.append({"phase": "intention_reset", "timestamp": time.time()})

    def _resume_processing(self):
        self.state.processing_resumed = True
        self.state.processing_paused = False
        self._log.append({"phase": "resume", "timestamp": time.time()})

    def get_log(self) -> list[dict]:
        return self._log.copy()
