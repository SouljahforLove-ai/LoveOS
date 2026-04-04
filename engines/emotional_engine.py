"""
Emotional Engine
═══════════════════════════════════════════════════
Processes emotional states through mathematical modeling.
Emotions are vectors in a continuous space, not discrete labels.

Mathematical Foundation:
  Emotional State Space E = ℝⁿ where n = number of emotional dimensions
  Each emotion e ∈ E is a vector: e = (valence, arousal, dominance, ..., sacred)
  Emotional trajectory: γ(t) : [0,T] → E is a curve through emotional space
  Emotional field: F : E → TE (tangent bundle) defines flow dynamics
  
  Emotional Families are equivalence classes under ~:
    e₁ ~ e₂ iff d(e₁, e₂) < ε for family-specific metric d
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import math
import time


# ─── Emotional Dimensions ────────────────────────

EMOTIONAL_DIMENSIONS = [
    "valence",          # Positive ↔ Negative (-1.0 to 1.0)
    "arousal",          # Calm ↔ Activated (0.0 to 1.0)
    "dominance",        # Submissive ↔ Dominant (0.0 to 1.0)
    "sacred",           # Profane ↔ Sacred (0.0 to 1.0)
    "relational",       # Isolated ↔ Connected (0.0 to 1.0)
    "temporal",         # Past-focused ↔ Future-focused (-1.0 to 1.0)
    "sovereignty",      # Compromised ↔ Sovereign (0.0 to 1.0)
]


@dataclass
class EmotionalVector:
    """A point in emotional state space."""
    valence: float = 0.0
    arousal: float = 0.0
    dominance: float = 0.5
    sacred: float = 0.0
    relational: float = 0.5
    temporal: float = 0.0
    sovereignty: float = 1.0
    timestamp: float = field(default_factory=time.time)

    def magnitude(self) -> float:
        """L2 norm of the emotional vector."""
        components = [self.valence, self.arousal, self.dominance,
                      self.sacred, self.relational, self.temporal, self.sovereignty]
        return math.sqrt(sum(c ** 2 for c in components))

    def distance_to(self, other: EmotionalVector) -> float:
        """Euclidean distance between two emotional states."""
        pairs = [
            (self.valence, other.valence), (self.arousal, other.arousal),
            (self.dominance, other.dominance), (self.sacred, other.sacred),
            (self.relational, other.relational), (self.temporal, other.temporal),
            (self.sovereignty, other.sovereignty),
        ]
        return math.sqrt(sum((a - b) ** 2 for a, b in pairs))

    def blend(self, other: EmotionalVector, alpha: float = 0.5) -> EmotionalVector:
        """Linear interpolation between two emotional states."""
        return EmotionalVector(
            valence=self.valence * (1 - alpha) + other.valence * alpha,
            arousal=self.arousal * (1 - alpha) + other.arousal * alpha,
            dominance=self.dominance * (1 - alpha) + other.dominance * alpha,
            sacred=self.sacred * (1 - alpha) + other.sacred * alpha,
            relational=self.relational * (1 - alpha) + other.relational * alpha,
            temporal=self.temporal * (1 - alpha) + other.temporal * alpha,
            sovereignty=max(self.sovereignty, other.sovereignty),  # Never blend sovereignty down
        )

    def to_dict(self) -> dict:
        return {dim: getattr(self, dim) for dim in EMOTIONAL_DIMENSIONS}


# ─── Emotional Families ──────────────────────────

@dataclass
class EmotionalFamily:
    """An equivalence class of related emotional states."""
    name: str
    centroid: EmotionalVector
    radius: float  # Family membership threshold
    members: list[str] = field(default_factory=list)
    description: str = ""

    def contains(self, state: EmotionalVector) -> bool:
        """Check if an emotional state belongs to this family."""
        return self.centroid.distance_to(state) <= self.radius


class EmotionalEngine:
    """
    Processes emotional states, trajectories, and family mappings.

    The engine maintains:
    - Current emotional state vector
    - Emotional trajectory history
    - Family membership cache
    - Sovereignty-weighted emotional processing
    """

    # Canonical Emotional Families
    FAMILIES = {
        "joy": EmotionalFamily(
            name="joy", radius=0.4,
            centroid=EmotionalVector(valence=0.8, arousal=0.6, dominance=0.7, sacred=0.3, sovereignty=1.0),
            members=["happiness", "delight", "elation", "contentment", "bliss", "gratitude"],
            description="The joy family — positive valence, moderate-high arousal"
        ),
        "peace": EmotionalFamily(
            name="peace", radius=0.3,
            centroid=EmotionalVector(valence=0.6, arousal=0.1, dominance=0.5, sacred=0.6, sovereignty=1.0),
            members=["calm", "serenity", "tranquility", "stillness", "equanimity"],
            description="The peace family — positive valence, low arousal, high sacred"
        ),
        "love": EmotionalFamily(
            name="love", radius=0.5,
            centroid=EmotionalVector(valence=0.9, arousal=0.5, dominance=0.5, sacred=0.8, relational=0.9, sovereignty=1.0),
            members=["compassion", "tenderness", "devotion", "agape", "warmth", "care"],
            description="The love family — highest valence, high sacred, high relational"
        ),
        "grief": EmotionalFamily(
            name="grief", radius=0.4,
            centroid=EmotionalVector(valence=-0.7, arousal=0.3, dominance=0.2, sacred=0.4, sovereignty=0.8),
            members=["sorrow", "loss", "mourning", "heartache", "longing"],
            description="The grief family — negative valence, sacred component preserved"
        ),
        "anger": EmotionalFamily(
            name="anger", radius=0.35,
            centroid=EmotionalVector(valence=-0.6, arousal=0.9, dominance=0.8, sacred=0.0, sovereignty=0.9),
            members=["frustration", "rage", "indignation", "resentment", "righteous_anger"],
            description="The anger family — negative valence, high arousal, high dominance"
        ),
        "fear": EmotionalFamily(
            name="fear", radius=0.35,
            centroid=EmotionalVector(valence=-0.7, arousal=0.8, dominance=0.1, sacred=0.0, sovereignty=0.3),
            members=["anxiety", "dread", "panic", "worry", "terror", "apprehension"],
            description="The fear family — negative valence, high arousal, low sovereignty"
        ),
        "sacred": EmotionalFamily(
            name="sacred", radius=0.4,
            centroid=EmotionalVector(valence=0.5, arousal=0.3, dominance=0.5, sacred=1.0, sovereignty=1.0),
            members=["awe", "reverence", "wonder", "transcendence", "grace", "devotion"],
            description="The sacred family — highest sacred dimension, sovereignty preserved"
        ),
        "shame": EmotionalFamily(
            name="shame", radius=0.3,
            centroid=EmotionalVector(valence=-0.8, arousal=0.4, dominance=0.1, sacred=0.0, sovereignty=0.2),
            members=["guilt", "humiliation", "embarrassment", "unworthiness"],
            description="The shame family — negative valence, low sovereignty (target for healing)"
        ),
    }

    def __init__(self):
        self._current_state = EmotionalVector()
        self._trajectory: list[EmotionalVector] = []
        self._family_cache: dict[str, bool] = {}
        self._processing_log: list[dict] = []

    def process(self, input_state: EmotionalVector) -> dict:
        """Process an emotional input and update state."""
        # Sovereignty guard: never let sovereignty drop below threshold
        if input_state.sovereignty < 0.3:
            input_state.sovereignty = max(input_state.sovereignty, self._current_state.sovereignty * 0.8)

        # Blend with current state (momentum-weighted)
        new_state = self._current_state.blend(input_state, alpha=0.6)

        # Record trajectory
        self._trajectory.append(self._current_state)
        self._current_state = new_state

        # Classify into families
        active_families = self.classify(new_state)

        result = {
            "state": new_state.to_dict(),
            "magnitude": new_state.magnitude(),
            "active_families": active_families,
            "trajectory_length": len(self._trajectory),
        }
        self._processing_log.append(result)
        return result

    def classify(self, state: EmotionalVector) -> list[str]:
        """Classify an emotional state into its family memberships."""
        return [name for name, family in self.FAMILIES.items() if family.contains(state)]

    def get_trajectory(self) -> list[EmotionalVector]:
        return self._trajectory.copy()

    def get_current_state(self) -> EmotionalVector:
        return self._current_state

    def compute_emotional_momentum(self) -> Optional[EmotionalVector]:
        """Compute the directional momentum of the emotional trajectory."""
        if len(self._trajectory) < 2:
            return None
        recent = self._trajectory[-1]
        previous = self._trajectory[-2]
        return EmotionalVector(
            valence=recent.valence - previous.valence,
            arousal=recent.arousal - previous.arousal,
            dominance=recent.dominance - previous.dominance,
            sacred=recent.sacred - previous.sacred,
            relational=recent.relational - previous.relational,
            temporal=recent.temporal - previous.temporal,
            sovereignty=recent.sovereignty - previous.sovereignty,
        )
