"""
Universal Sorting Intelligence Engine
═══════════════════════════════════════════════════
Routes, tags, classifies, and prioritizes ALL inputs
entering the LoveOS system. Nothing bypasses the sorter.

Design Pattern: Pipeline → Classify → Route → Audit

Input Categories:
  - SIGNAL:   Emotional/spiritual input requiring processing
  - COMMAND:  Operator directive requiring execution
  - DATA:     Information requiring storage/retrieval
  - THREAT:   Security-relevant input requiring guard escalation
  - RITUAL:   Ritual trigger requiring sequencing
  - NOISE:    Non-actionable input requiring filtering
  - LEGACY:   Legacy-relevant content requiring preservation
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional
import time
import re
import hashlib


class InputCategory(Enum):
    SIGNAL = auto()
    COMMAND = auto()
    DATA = auto()
    THREAT = auto()
    RITUAL = auto()
    NOISE = auto()
    LEGACY = auto()
    UNKNOWN = auto()


class RoutePriority(Enum):
    IMMEDIATE = 0
    HIGH = 1
    STANDARD = 2
    LOW = 3
    DEFERRED = 4


@dataclass
class SortedInput:
    """An input that has been classified and routed."""
    raw: Any
    category: InputCategory = InputCategory.UNKNOWN
    priority: RoutePriority = RoutePriority.STANDARD
    route_target: str = ""
    tags: list[str] = field(default_factory=list)
    confidence: float = 0.0
    sovereignty_cleared: bool = False
    fingerprint: str = ""
    timestamp: float = field(default_factory=time.time)


class SortingEngine:
    """
    Universal Sorting Intelligence — classify, route, and audit all inputs.

    Pipeline Stages:
    1. INTAKE     — Receive raw input
    2. FINGERPRINT — Compute content fingerprint for dedup/audit
    3. CLASSIFY   — Determine input category and confidence
    4. TAG        — Apply semantic tags
    5. PRIORITIZE — Assign route priority
    6. ROUTE      — Determine target module/engine
    7. AUDIT      — Log the sorting decision
    """

    def __init__(self):
        self._classifiers: list[Callable] = []
        self._routing_table: dict[InputCategory, str] = {
            InputCategory.SIGNAL: "emotional_engine",
            InputCategory.COMMAND: "kernel",
            InputCategory.DATA: "registry",
            InputCategory.THREAT: "security_module",
            InputCategory.RITUAL: "ritual_dispatcher",
            InputCategory.NOISE: "dev_null",
            InputCategory.LEGACY: "legacy_engine",
            InputCategory.UNKNOWN: "sorting_queue",
        }
        self._sort_log: list[SortedInput] = []
        self._tag_registry: dict[str, list[str]] = {}
        self._duplicate_cache: set[str] = set()

    def sort(self, raw_input: Any) -> SortedInput:
        """Full sorting pipeline: intake → classify → tag → route → audit."""
        result = SortedInput(raw=raw_input)

        # Stage 1: Fingerprint
        result.fingerprint = self._fingerprint(raw_input)

        # Dedup check
        if result.fingerprint in self._duplicate_cache:
            result.category = InputCategory.NOISE
            result.tags.append("duplicate")
            result.priority = RoutePriority.DEFERRED
        else:
            self._duplicate_cache.add(result.fingerprint)

            # Stage 2: Classify
            result.category, result.confidence = self._classify(raw_input)

            # Stage 3: Tag
            result.tags = self._tag(raw_input, result.category)

            # Stage 4: Prioritize
            result.priority = self._prioritize(result)

        # Stage 5: Route
        result.route_target = self._routing_table.get(
            result.category, "sorting_queue"
        )

        # Stage 6: Audit
        self._sort_log.append(result)

        return result

    def register_classifier(self, classifier: Callable):
        """Add a custom classifier to the pipeline."""
        self._classifiers.append(classifier)

    def update_routing(self, category: InputCategory, target: str):
        """Update the routing table for a category."""
        self._routing_table[category] = target

    def get_sort_log(self) -> list[SortedInput]:
        return self._sort_log.copy()

    def get_category_stats(self) -> dict[str, int]:
        """Return counts by category."""
        stats: dict[str, int] = {}
        for entry in self._sort_log:
            key = entry.category.name
            stats[key] = stats.get(key, 0) + 1
        return stats

    def _fingerprint(self, raw: Any) -> str:
        return hashlib.sha256(str(raw).encode()).hexdigest()[:16]

    def _classify(self, raw: Any) -> tuple[InputCategory, float]:
        """Classify input into a category with confidence."""
        text = str(raw).lower()

        # Threat detection (highest priority)
        threat_signals = ["attack", "inject", "override", "bypass", "exploit"]
        if any(sig in text for sig in threat_signals):
            return InputCategory.THREAT, 0.9

        # Command detection
        command_patterns = [r"^(mount|unmount|boot|shutdown|audit|ground)", r"^!"]
        if any(re.search(p, text) for p in command_patterns):
            return InputCategory.COMMAND, 0.85

        # Ritual detection
        ritual_signals = ["ritual", "ground", "presence", "ceremony", "meditation"]
        if any(sig in text for sig in ritual_signals):
            return InputCategory.RITUAL, 0.8

        # Legacy detection
        legacy_signals = ["legacy", "teach", "zen", "transmit", "generation"]
        if any(sig in text for sig in legacy_signals):
            return InputCategory.LEGACY, 0.75

        # Signal detection (emotional/spiritual)
        signal_signals = ["feel", "emotion", "spirit", "soul", "heart", "love"]
        if any(sig in text for sig in signal_signals):
            return InputCategory.SIGNAL, 0.7

        # Custom classifiers
        for classifier in self._classifiers:
            result = classifier(raw)
            if result:
                return result

        return InputCategory.DATA, 0.5

    def _tag(self, raw: Any, category: InputCategory) -> list[str]:
        """Apply semantic tags to the input."""
        tags = [category.name.lower()]
        text = str(raw).lower()

        tag_keywords = {
            "sovereignty": ["sovereign", "boundary", "dignity", "consent"],
            "emotional": ["feel", "emotion", "mood", "heart"],
            "spiritual": ["spirit", "soul", "faith", "sacred", "prayer"],
            "security": ["threat", "danger", "alert", "warning"],
            "legacy": ["legacy", "teach", "child", "generation", "zen"],
            "love": ["love", "compassion", "care", "agape"],
        }

        for tag, keywords in tag_keywords.items():
            if any(kw in text for kw in keywords):
                tags.append(tag)

        return list(set(tags))

    def _prioritize(self, result: SortedInput) -> RoutePriority:
        """Assign priority based on category and tags."""
        priority_map = {
            InputCategory.THREAT: RoutePriority.IMMEDIATE,
            InputCategory.COMMAND: RoutePriority.HIGH,
            InputCategory.RITUAL: RoutePriority.HIGH,
            InputCategory.SIGNAL: RoutePriority.STANDARD,
            InputCategory.LEGACY: RoutePriority.STANDARD,
            InputCategory.DATA: RoutePriority.LOW,
            InputCategory.NOISE: RoutePriority.DEFERRED,
        }
        return priority_map.get(result.category, RoutePriority.STANDARD)
