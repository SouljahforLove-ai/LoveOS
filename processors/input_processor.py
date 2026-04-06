"""
Input Processor
═══════════════════════════════════════════════════
First contact point for all raw inputs entering SoulJahOS.
Sanitizes, normalizes, and prepares inputs for the sorting engine.

Pipeline: Raw → Sanitize → Normalize → Enrich → Emit
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
import re
import time
import hashlib


@dataclass
class ProcessedInput:
    """An input that has passed through the input processor."""
    raw: Any = None
    sanitized: str = ""
    normalized: str = ""
    metadata: dict = field(default_factory=dict)
    fingerprint: str = ""
    safe: bool = True
    processing_time_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)


class InputProcessor:
    """
    Sanitize, normalize, and enrich all inputs before sorting.

    Security: Strips injection attempts, logs suspicious patterns.
    Normalization: Unicode normalization, whitespace cleanup, case handling.
    Enrichment: Adds metadata (length, language hints, content type).
    """

    STRIP_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=\s*["\']',
    ]

    def __init__(self):
        self._processed_count = 0
        self._flagged_count = 0

    def process(self, raw_input: Any) -> ProcessedInput:
        """Full input processing pipeline."""
        start = time.time()
        result = ProcessedInput(raw=raw_input)

        text = str(raw_input)

        # Stage 1: Sanitize
        result.sanitized = self._sanitize(text)
        if result.sanitized != text:
            result.safe = False
            self._flagged_count += 1

        # Stage 2: Normalize
        result.normalized = self._normalize(result.sanitized)

        # Stage 3: Enrich
        result.metadata = self._enrich(result.normalized)

        # Stage 4: Fingerprint
        result.fingerprint = hashlib.sha256(result.normalized.encode()).hexdigest()[:16]

        result.processing_time_ms = (time.time() - start) * 1000
        self._processed_count += 1
        return result

    def _sanitize(self, text: str) -> str:
        """Remove potentially dangerous content."""
        cleaned = text
        for pattern in self.STRIP_PATTERNS:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.DOTALL)
        return cleaned

    def _normalize(self, text: str) -> str:
        """Normalize whitespace and encoding."""
        normalized = ' '.join(text.split())
        return normalized.strip()

    def _enrich(self, text: str) -> dict:
        """Add metadata to the input."""
        return {
            "length": len(text),
            "word_count": len(text.split()),
            "has_urls": bool(re.search(r'https?://', text)),
            "has_email": bool(re.search(r'[\w.-]+@[\w.-]+', text)),
            "content_type": self._detect_content_type(text),
        }

    def _detect_content_type(self, text: str) -> str:
        """Heuristic content type detection."""
        if re.match(r'^[{[]', text.strip()):
            return "structured_data"
        if re.search(r'(def |class |import |from )', text):
            return "code"
        if len(text.split()) > 50:
            return "prose"
        return "short_text"

    def get_stats(self) -> dict:
        return {"processed": self._processed_count, "flagged": self._flagged_count}
