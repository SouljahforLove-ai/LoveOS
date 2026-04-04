"""
Pattern Registry — Central store of all known behavioral and architectural patterns.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
import time


@dataclass
class PatternDef:
    """A registered pattern definition."""
    name: str
    pattern_type: str       # "behavioral", "architectural", "emotional", "ritual"
    description: str = ""
    trigger_conditions: list[str] = field(default_factory=list)
    response_actions: list[str] = field(default_factory=list)
    frequency: int = 0
    confidence: float = 0.0
    registered_at: float = field(default_factory=time.time)


class PatternRegistry:
    def __init__(self):
        self._patterns: dict[str, PatternDef] = {}
        self._initialize_core_patterns()

    def _initialize_core_patterns(self):
        core = [
            PatternDef("operator_grounding", "behavioral",
                        "Operator needs grounding when sovereignty drops",
                        ["sovereignty < 0.5", "arousal > 0.7"],
                        ["trigger_grounding_ritual", "notify_operator"]),
            PatternDef("emotional_spiral", "emotional",
                        "Negative emotional momentum exceeding threshold",
                        ["valence_trend < -0.3", "duration > 300s"],
                        ["inject_grounding", "offer_ritual"]),
            PatternDef("legacy_capture", "architectural",
                        "Workflow completion triggers legacy capture",
                        ["workflow_complete", "quality_score > 0.7"],
                        ["capture_legacy_item", "tag_for_transmission"]),
            PatternDef("threat_escalation", "behavioral",
                        "Security threat requires guard escalation",
                        ["threat_level >= HIGH", "source == external"],
                        ["quarantine_input", "notify_sovereignty_guard"]),
            PatternDef("faith_alignment", "ritual",
                        "Spiritual alignment triggers faith integration",
                        ["spiritual_alignment > 0.7", "faith_active"],
                        ["sync_faith_engine", "update_covenant_status"]),
        ]
        for p in core:
            self._patterns[p.name] = p

    def register(self, pattern: PatternDef):
        self._patterns[pattern.name] = pattern

    def lookup(self, name: str) -> Optional[PatternDef]:
        return self._patterns.get(name)

    def match_conditions(self, conditions: dict) -> list[PatternDef]:
        """Find patterns whose trigger conditions match current state."""
        # Simplified matching — in full implementation, would parse conditions
        return list(self._patterns.values())

    def get_all(self) -> list[PatternDef]:
        return list(self._patterns.values())

    def get_stats(self) -> dict:
        by_type = {}
        for p in self._patterns.values():
            by_type[p.pattern_type] = by_type.get(p.pattern_type, 0) + 1
        return {"total": len(self._patterns), "by_type": by_type}
