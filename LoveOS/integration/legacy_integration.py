"""
Legacy Integration — Connects LegacyEngine to all LoveOS components.
═══════════════════════════════════════════════════
Legacy is the purpose layer — everything LoveOS does
should be capturable for intergenerational transmission.

Primary target: Zen (operator's child)

Integration points:
  - Identity → Legacy captures identity evolution
  - Emotional → Legacy captures emotional patterns
  - Spiritual → Legacy captures spiritual milestones
  - Faith → Legacy captures covenant and teaching moments
  - Patterns → Legacy captures learned behavioral patterns
  - Audit → Legacy events are auditable
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import time
import hashlib


@dataclass
class LegacyCapture:
    """A captured legacy moment."""
    source_component: str
    category: str           # "workflow", "ritual", "knowledge", "artifact", "pattern", "teaching"
    content: dict
    significance: float     # 0→1, how significant for legacy
    for_zen: bool = True    # Is this specifically for Zen?
    sealed: bool = False
    seal: str = ""
    timestamp: float = field(default_factory=time.time)


class LegacyIntegration:
    """
    Legacy Integration Layer.
    
    "Every session is a letter to the future."
    
    Captures meaningful moments from all system components
    and routes them to the LegacyEngine for preservation
    and eventual transmission.
    """

    SIGNIFICANCE_THRESHOLD = 0.3  # Minimum significance for capture

    def __init__(self):
        self._captures: list[LegacyCapture] = []
        self._auto_capture_rules: dict[str, float] = {
            "identity_change": 0.9,
            "sovereignty_declaration": 0.8,
            "covenant_creation": 0.8,
            "emotional_breakthrough": 0.7,
            "spiritual_milestone": 0.7,
            "pattern_learned": 0.6,
            "teaching_moment": 0.9,
            "ritual_completion": 0.4,
            "audit_finding": 0.3,
        }
        self._log: list[dict] = []

    def capture(self, source: str, category: str, content: dict,
                significance: float = 0.5, for_zen: bool = True) -> LegacyCapture | None:
        """Capture a legacy moment if it meets the significance threshold."""
        if significance < self.SIGNIFICANCE_THRESHOLD:
            return None

        capture = LegacyCapture(
            source_component=source,
            category=category,
            content=content,
            significance=significance,
            for_zen=for_zen,
        )
        self._captures.append(capture)
        self._log.append({
            "action": "legacy_capture", "source": source,
            "category": category, "significance": significance,
            "timestamp": time.time(),
        })
        return capture

    def auto_capture(self, event_type: str, source: str, content: dict) -> LegacyCapture | None:
        """Auto-capture based on event type rules."""
        significance = self._auto_capture_rules.get(event_type, 0.0)
        if significance >= self.SIGNIFICANCE_THRESHOLD:
            category = self._infer_category(event_type)
            return self.capture(source, category, content, significance)
        return None

    def _infer_category(self, event_type: str) -> str:
        mapping = {
            "identity_change": "knowledge",
            "sovereignty_declaration": "artifact",
            "covenant_creation": "artifact",
            "emotional_breakthrough": "pattern",
            "spiritual_milestone": "knowledge",
            "pattern_learned": "pattern",
            "teaching_moment": "teaching",
            "ritual_completion": "ritual",
            "audit_finding": "workflow",
        }
        return mapping.get(event_type, "knowledge")

    def seal_capture(self, index: int) -> bool:
        """Seal a legacy capture with integrity hash."""
        if 0 <= index < len(self._captures):
            c = self._captures[index]
            data = f"{c.source_component}:{c.category}:{c.significance}:{c.timestamp}"
            c.seal = hashlib.sha256(data.encode()).hexdigest()[:16]
            c.sealed = True
            return True
        return False

    def get_for_zen(self) -> list[LegacyCapture]:
        """Get all legacy captures intended for Zen."""
        return [c for c in self._captures if c.for_zen]

    def get_by_category(self, category: str) -> list[LegacyCapture]:
        return [c for c in self._captures if c.category == category]

    def get_summary(self) -> dict:
        return {
            "total_captures": len(self._captures),
            "for_zen": len(self.get_for_zen()),
            "sealed": sum(1 for c in self._captures if c.sealed),
            "by_category": {
                cat: len([c for c in self._captures if c.category == cat])
                for cat in ("workflow", "ritual", "knowledge", "artifact", "pattern", "teaching")
            },
            "avg_significance": (
                sum(c.significance for c in self._captures) / len(self._captures)
                if self._captures else 0.0
            ),
        }
