"""
Spiritual Schema — Data types for the spiritual alignment layer.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import time


@dataclass
class SpiritualRecord:
    """A timestamped spiritual state record."""
    alignment: float = 0.5
    presence: float = 0.5
    gratitude: float = 0.5
    surrender: float = 0.0
    faith: float = 0.5
    service: float = 0.5
    integrity: float = 1.0
    sovereignty: float = 1.0
    context: str = ""
    timestamp: float = field(default_factory=time.time)


@dataclass
class RitualRecord:
    """Record of a completed ritual."""
    name: str = ""
    ritual_type: str = ""      # "boot", "grounding", "audit", "closure", "custom"
    intention: str = ""
    pre_alignment: float = 0.0
    post_alignment: float = 0.0
    duration_seconds: float = 0.0
    completed: bool = False
    notes: str = ""
    timestamp: float = field(default_factory=time.time)

    @property
    def delta(self) -> float:
        return self.post_alignment - self.pre_alignment


@dataclass
class PrayerRecord:
    """Record of a prayer/meditation session."""
    intention: str = ""
    tradition: str = "integrated"
    duration_seconds: float = 0.0
    grace_recognized: bool = False
    insights: list[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
