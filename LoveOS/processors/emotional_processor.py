"""
Emotional Processor
═══════════════════════════════════════════════════
Transforms raw emotional signals into EmotionalVectors
for the EmotionalEngine. Bridges natural language and
behavioral signals to mathematical emotional space.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
import re
import time


# Emotion keyword → vector component mappings
EMOTION_LEXICON = {
    # Positive valence
    "happy": {"valence": 0.8, "arousal": 0.5},
    "joyful": {"valence": 0.9, "arousal": 0.7},
    "peaceful": {"valence": 0.6, "arousal": 0.1},
    "grateful": {"valence": 0.7, "arousal": 0.3, "sacred": 0.5},
    "loved": {"valence": 0.9, "arousal": 0.4, "relational": 0.9},
    "confident": {"valence": 0.6, "arousal": 0.5, "dominance": 0.8, "sovereignty": 0.9},
    "inspired": {"valence": 0.7, "arousal": 0.7, "sacred": 0.4},
    # Negative valence
    "sad": {"valence": -0.6, "arousal": 0.2},
    "angry": {"valence": -0.5, "arousal": 0.9, "dominance": 0.8},
    "afraid": {"valence": -0.7, "arousal": 0.8, "dominance": 0.1, "sovereignty": 0.3},
    "ashamed": {"valence": -0.8, "arousal": 0.4, "dominance": 0.1, "sovereignty": 0.2},
    "lonely": {"valence": -0.5, "arousal": 0.2, "relational": 0.1},
    "overwhelmed": {"valence": -0.4, "arousal": 0.9, "dominance": 0.1},
    "anxious": {"valence": -0.5, "arousal": 0.7, "sovereignty": 0.4},
}


class EmotionalProcessor:
    """
    Transforms text and behavioral signals into emotional vectors.

    Processing stages:
    1. Lexical scan — match emotion keywords
    2. Contextual adjustment — modify based on modifiers
    3. Sovereignty guard — ensure sovereignty floor
    4. Vector assembly — produce EmotionalVector
    """

    SOVEREIGNTY_FLOOR = 0.3

    def __init__(self):
        self._processed_count = 0

    def process_text(self, text: str) -> dict:
        """Extract emotional vector components from text."""
        text_lower = text.lower()
        accumulated = {"valence": 0.0, "arousal": 0.0, "dominance": 0.5,
                        "sacred": 0.0, "relational": 0.5, "sovereignty": 1.0}
        matches = 0

        for keyword, components in EMOTION_LEXICON.items():
            if keyword in text_lower:
                matches += 1
                for dim, value in components.items():
                    accumulated[dim] = (accumulated[dim] + value) / 2

        # Sovereignty floor
        accumulated["sovereignty"] = max(accumulated["sovereignty"], self.SOVEREIGNTY_FLOOR)

        self._processed_count += 1
        return {
            "vector": accumulated,
            "matches": matches,
            "confidence": min(matches * 0.2, 1.0),
        }

    def get_stats(self) -> dict:
        return {"processed": self._processed_count}
