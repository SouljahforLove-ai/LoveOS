"""
Pattern Processor
═══════════════════════════════════════════════════
Detects, records, and learns from behavioral patterns.
Patterns are the system's long-term memory of recurring
sequences — operator habits, emotional cycles, ritual
effectiveness, and sovereignty maintenance patterns.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
import time
import hashlib


@dataclass
class Pattern:
    """A detected behavioral pattern."""
    id: str = ""
    name: str = ""
    pattern_type: str = ""     # "emotional", "behavioral", "ritual", "sovereignty"
    sequence: list[str] = field(default_factory=list)
    frequency: int = 0
    confidence: float = 0.0
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)

    @property
    def is_established(self) -> bool:
        return self.frequency >= 3 and self.confidence >= 0.6


class PatternProcessor:
    """
    Detect and learn from recurring behavioral patterns.

    The processor maintains a pattern library and matches
    incoming sequences against known patterns. New patterns
    are discovered through frequency analysis.
    """

    def __init__(self):
        self._patterns: dict[str, Pattern] = {}
        self._sequence_buffer: list[str] = []
        self._buffer_max = 100

    def observe(self, event: str) -> Optional[Pattern]:
        """Observe an event and check for pattern matches."""
        self._sequence_buffer.append(event)
        if len(self._sequence_buffer) > self._buffer_max:
            self._sequence_buffer = self._sequence_buffer[-self._buffer_max:]

        # Check for known patterns
        matched = self._match_patterns()
        if matched:
            return matched

        # Try to discover new patterns
        discovered = self._discover_patterns()
        if discovered:
            return discovered

        return None

    def register_pattern(self, name: str, sequence: list[str],
                          pattern_type: str = "behavioral") -> Pattern:
        """Manually register a known pattern."""
        pid = hashlib.sha256(f"{name}:{','.join(sequence)}".encode()).hexdigest()[:12]
        pattern = Pattern(
            id=pid, name=name, sequence=sequence,
            pattern_type=pattern_type, confidence=0.8,
        )
        self._patterns[pid] = pattern
        return pattern

    def get_established_patterns(self) -> list[Pattern]:
        """Return all established (high-confidence, recurring) patterns."""
        return [p for p in self._patterns.values() if p.is_established]

    def get_all_patterns(self) -> list[Pattern]:
        return list(self._patterns.values())

    def _match_patterns(self) -> Optional[Pattern]:
        """Match the current sequence buffer against known patterns."""
        for pattern in self._patterns.values():
            seq_len = len(pattern.sequence)
            if len(self._sequence_buffer) >= seq_len:
                recent = self._sequence_buffer[-seq_len:]
                if recent == pattern.sequence:
                    pattern.frequency += 1
                    pattern.last_seen = time.time()
                    pattern.confidence = min(pattern.confidence + 0.05, 1.0)
                    return pattern
        return None

    def _discover_patterns(self) -> Optional[Pattern]:
        """Attempt to discover new patterns from the buffer."""
        if len(self._sequence_buffer) < 4:
            return None

        # Simple bigram frequency analysis
        bigrams: dict[tuple, int] = {}
        for i in range(len(self._sequence_buffer) - 1):
            bg = (self._sequence_buffer[i], self._sequence_buffer[i + 1])
            bigrams[bg] = bigrams.get(bg, 0) + 1

        for bg, count in bigrams.items():
            if count >= 3:
                pid = hashlib.sha256(f"discovered:{bg}".encode()).hexdigest()[:12]
                if pid not in self._patterns:
                    pattern = Pattern(
                        id=pid, name=f"auto:{bg[0]}->{bg[1]}",
                        sequence=list(bg), pattern_type="discovered",
                        frequency=count, confidence=0.4,
                    )
                    self._patterns[pid] = pattern
                    return pattern
        return None
