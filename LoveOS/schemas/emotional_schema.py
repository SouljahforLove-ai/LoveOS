"""
Emotional Schema — Data types for the emotional processing layer.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import time


@dataclass
class EmotionRecord:
    """A timestamped emotional state record."""
    valence: float = 0.0
    arousal: float = 0.0
    dominance: float = 0.5
    sacred: float = 0.0
    relational: float = 0.5
    temporal: float = 0.0
    sovereignty: float = 1.0
    family: str = ""
    source: str = ""
    context: str = ""
    timestamp: float = field(default_factory=time.time)


@dataclass
class EmotionalTrajectory:
    """A sequence of emotional records forming a trajectory."""
    records: list[EmotionRecord] = field(default_factory=list)
    label: str = ""
    start_time: float = 0.0
    end_time: float = 0.0

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time if self.end_time else 0.0

    @property
    def trend(self) -> float:
        if len(self.records) < 2:
            return 0.0
        return self.records[-1].valence - self.records[0].valence


@dataclass
class EmotionalFamilyDef:
    """Schema definition for an emotional family."""
    name: str
    centroid_valence: float = 0.0
    centroid_arousal: float = 0.0
    centroid_dominance: float = 0.5
    centroid_sacred: float = 0.0
    centroid_sovereignty: float = 1.0
    radius: float = 0.4
    members: list[str] = field(default_factory=list)
    description: str = ""
