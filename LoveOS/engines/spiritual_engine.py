"""
Spiritual Engine
═══════════════════════════════════════════════════
Processes spiritual alignment through discrete dynamical systems.
The spiritual dimension is orthogonal to emotional processing —
it represents alignment with purpose, meaning, and the sacred.

Mathematical Foundation:
  Spiritual State: σ ∈ S where S is a compact manifold
  Alignment Function: A(σ, p) → [0,1] measuring alignment between
    state σ and purpose vector p
  Spiritual Dynamics: σₜ₊₁ = T(σₜ, input, ritual_state)
    where T is a sovereignty-preserving transformation

  Key Invariant: sovereignty(σₜ₊₁) ≥ sovereignty(σₜ) · decay_floor
    (Spiritual processing never degrades sovereignty)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import math
import time


@dataclass
class SpiritualVector:
    """A point in spiritual state space."""
    alignment: float = 0.5       # Alignment with declared purpose (0→1)
    presence: float = 0.5        # Present-moment awareness (0→1)
    gratitude: float = 0.5       # Gratitude quotient (0→1)
    surrender: float = 0.0       # Release of control (0→1)
    faith: float = 0.5           # Trust in process/higher order (0→1)
    service: float = 0.5         # Orientation toward service (0→1)
    integrity: float = 1.0       # Internal consistency (0→1)
    sovereignty: float = 1.0     # Spiritual sovereignty (0→1, never forced down)
    timestamp: float = field(default_factory=time.time)

    def alignment_score(self) -> float:
        """Composite alignment score — weighted geometric mean."""
        weights = [0.20, 0.15, 0.10, 0.10, 0.15, 0.10, 0.10, 0.10]
        components = [self.alignment, self.presence, self.gratitude,
                      self.surrender, self.faith, self.service,
                      self.integrity, self.sovereignty]
        log_sum = sum(w * math.log(max(c, 0.001)) for w, c in zip(weights, components))
        return math.exp(log_sum)

    def to_dict(self) -> dict:
        return {
            "alignment": self.alignment, "presence": self.presence,
            "gratitude": self.gratitude, "surrender": self.surrender,
            "faith": self.faith, "service": self.service,
            "integrity": self.integrity, "sovereignty": self.sovereignty,
        }


@dataclass
class SpiritualRitual:
    """A spiritual ritual with measurable pre/post states."""
    name: str
    intention: str
    pre_state: Optional[SpiritualVector] = None
    post_state: Optional[SpiritualVector] = None
    duration_seconds: float = 0.0
    completed: bool = False


class SpiritualEngine:
    """
    Processes spiritual alignment, ritual integration, and purpose tracking.

    Core Operations:
    - Compute alignment with declared life purpose
    - Track spiritual trajectory over time
    - Process ritual pre/post state transitions
    - Maintain spiritual sovereignty invariant
    """

    PURPOSE_VECTOR = {
        "love": 1.0,
        "sovereignty": 1.0,
        "legacy": 0.9,
        "service": 0.8,
        "presence": 0.8,
        "faith": 0.7,
    }

    def __init__(self):
        self._current_state = SpiritualVector()
        self._trajectory: list[SpiritualVector] = []
        self._rituals_completed: list[SpiritualRitual] = []
        self._alignment_history: list[float] = []
        self._sovereignty_floor = 0.5  # Sovereignty never drops below this

    def process(self, input_state: SpiritualVector) -> dict:
        """Process a spiritual state update."""
        # Sovereignty invariant: never degrade
        input_state.sovereignty = max(
            input_state.sovereignty,
            self._current_state.sovereignty * 0.95,
            self._sovereignty_floor
        )

        # Update state with momentum
        alpha = 0.5
        new_state = SpiritualVector(
            alignment=self._current_state.alignment * (1 - alpha) + input_state.alignment * alpha,
            presence=input_state.presence,  # Presence is instantaneous
            gratitude=self._current_state.gratitude * (1 - alpha) + input_state.gratitude * alpha,
            surrender=self._current_state.surrender * (1 - alpha) + input_state.surrender * alpha,
            faith=self._current_state.faith * (1 - alpha) + input_state.faith * alpha,
            service=self._current_state.service * (1 - alpha) + input_state.service * alpha,
            integrity=min(self._current_state.integrity, input_state.integrity),
            sovereignty=input_state.sovereignty,
        )

        self._trajectory.append(self._current_state)
        self._current_state = new_state

        score = new_state.alignment_score()
        self._alignment_history.append(score)

        return {
            "state": new_state.to_dict(),
            "alignment_score": score,
            "trajectory_length": len(self._trajectory),
            "purpose_alignment": self._compute_purpose_alignment(new_state),
        }

    def process_ritual(self, ritual: SpiritualRitual) -> dict:
        """Process a completed spiritual ritual."""
        ritual.completed = True
        self._rituals_completed.append(ritual)

        delta = {}
        if ritual.pre_state and ritual.post_state:
            pre = ritual.pre_state.to_dict()
            post = ritual.post_state.to_dict()
            delta = {k: post[k] - pre[k] for k in pre}

        return {
            "ritual": ritual.name,
            "delta": delta,
            "rituals_completed": len(self._rituals_completed),
        }

    def _compute_purpose_alignment(self, state: SpiritualVector) -> float:
        """Compute alignment between current state and life purpose."""
        state_dict = state.to_dict()
        alignment_sum = 0.0
        weight_sum = 0.0
        for purpose_dim, purpose_weight in self.PURPOSE_VECTOR.items():
            if purpose_dim in state_dict:
                alignment_sum += purpose_weight * state_dict[purpose_dim]
                weight_sum += purpose_weight
        return alignment_sum / weight_sum if weight_sum > 0 else 0.0

    def get_current_state(self) -> SpiritualVector:
        return self._current_state

    def get_alignment_trend(self, window: int = 10) -> float:
        """Compute trend of alignment over recent window."""
        if len(self._alignment_history) < 2:
            return 0.0
        recent = self._alignment_history[-window:]
        if len(recent) < 2:
            return 0.0
        return (recent[-1] - recent[0]) / len(recent)
