"""
Emotional Family Map
═══════════════════════════════════════════════════
Maps all emotional families, their centroids, members,
inter-family distances, and transition probabilities.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FamilyMapEntry:
    """An emotional family with relational data."""
    name: str
    members: list[str] = field(default_factory=list)
    centroid: dict = field(default_factory=dict)
    radius: float = 0.4
    adjacent_families: list[str] = field(default_factory=list)
    transition_probabilities: dict[str, float] = field(default_factory=dict)
    healing_target: bool = False  # True if this family is a target for healing work


class EmotionalFamilyMap:
    def __init__(self):
        self._families: dict[str, FamilyMapEntry] = {}
        self._initialize()

    def _initialize(self):
        families = [
            FamilyMapEntry("joy",
                members=["happiness", "delight", "elation", "contentment", "bliss", "gratitude"],
                centroid={"valence": 0.8, "arousal": 0.6, "sovereignty": 1.0},
                adjacent_families=["love", "peace", "sacred"],
                transition_probabilities={"peace": 0.3, "love": 0.25, "grief": 0.05}),
            FamilyMapEntry("peace",
                members=["calm", "serenity", "tranquility", "stillness", "equanimity"],
                centroid={"valence": 0.6, "arousal": 0.1, "sovereignty": 1.0},
                adjacent_families=["joy", "sacred", "love"],
                transition_probabilities={"joy": 0.2, "sacred": 0.3, "fear": 0.05}),
            FamilyMapEntry("love",
                members=["compassion", "tenderness", "devotion", "agape", "warmth", "care"],
                centroid={"valence": 0.9, "arousal": 0.5, "sovereignty": 1.0},
                adjacent_families=["joy", "sacred", "peace", "grief"],
                transition_probabilities={"joy": 0.3, "grief": 0.1, "sacred": 0.2}),
            FamilyMapEntry("grief",
                members=["sorrow", "loss", "mourning", "heartache", "longing"],
                centroid={"valence": -0.7, "arousal": 0.3, "sovereignty": 0.8},
                adjacent_families=["love", "shame", "anger"],
                transition_probabilities={"love": 0.15, "anger": 0.1, "peace": 0.1}),
            FamilyMapEntry("anger",
                members=["frustration", "rage", "indignation", "resentment", "righteous_anger"],
                centroid={"valence": -0.6, "arousal": 0.9, "sovereignty": 0.9},
                adjacent_families=["grief", "fear"],
                transition_probabilities={"grief": 0.15, "peace": 0.05, "shame": 0.1}),
            FamilyMapEntry("fear",
                members=["anxiety", "dread", "panic", "worry", "terror", "apprehension"],
                centroid={"valence": -0.7, "arousal": 0.8, "sovereignty": 0.3},
                adjacent_families=["anger", "shame"],
                transition_probabilities={"anger": 0.2, "peace": 0.1, "shame": 0.15},
                healing_target=True),
            FamilyMapEntry("sacred",
                members=["awe", "reverence", "wonder", "transcendence", "grace", "devotion"],
                centroid={"valence": 0.5, "arousal": 0.3, "sovereignty": 1.0},
                adjacent_families=["love", "peace", "joy"],
                transition_probabilities={"peace": 0.3, "love": 0.25, "joy": 0.2}),
            FamilyMapEntry("shame",
                members=["guilt", "humiliation", "embarrassment", "unworthiness"],
                centroid={"valence": -0.8, "arousal": 0.4, "sovereignty": 0.2},
                adjacent_families=["fear", "grief"],
                transition_probabilities={"grief": 0.2, "fear": 0.15, "love": 0.05},
                healing_target=True),
        ]
        for f in families:
            self._families[f.name] = f

    def get_family(self, name: str) -> Optional[FamilyMapEntry]:
        return self._families.get(name)

    def get_adjacent(self, name: str) -> list[str]:
        f = self._families.get(name)
        return f.adjacent_families if f else []

    def get_healing_targets(self) -> list[FamilyMapEntry]:
        return [f for f in self._families.values() if f.healing_target]

    def get_transition_probability(self, from_family: str, to_family: str) -> float:
        f = self._families.get(from_family)
        if not f:
            return 0.0
        return f.transition_probabilities.get(to_family, 0.0)

    def get_all(self) -> list[FamilyMapEntry]:
        return list(self._families.values())
