"""
Emotional Module — Emotional state management and family classification.
Wraps the EmotionalEngine for module-level lifecycle and IPC.
"""
from __future__ import annotations
from typing import Any, Optional


class EmotionalModule:
    MODULE_NAME = "emotional"
    SOVEREIGNTY_LEVEL = "PROTECTED"

    def __init__(self):
        self._active = False
        self._engine = None
        self._event_buffer: list[dict] = []

    def mount(self) -> bool:
        from engines.emotional_engine import EmotionalEngine
        self._engine = EmotionalEngine()
        self._active = True
        return True

    def unmount(self) -> bool:
        self._active = False
        return True

    def process_input(self, emotional_data: dict) -> dict:
        if not self._active or not self._engine:
            return {"error": "module not mounted"}
        from engines.emotional_engine import EmotionalVector
        vec = EmotionalVector(**{k: v for k, v in emotional_data.items()
                                 if hasattr(EmotionalVector, k)})
        result = self._engine.process(vec)
        self._event_buffer.append(result)
        return result

    def get_current_state(self) -> dict:
        if self._engine:
            return self._engine.get_current_state().to_dict()
        return {}

    def classify_state(self, emotional_data: dict) -> list[str]:
        if not self._engine:
            return []
        from engines.emotional_engine import EmotionalVector
        vec = EmotionalVector(**{k: v for k, v in emotional_data.items()
                                 if hasattr(EmotionalVector, k)})
        return self._engine.classify(vec)

    def get_families(self) -> dict:
        if not self._engine:
            return {}
        return {name: {"members": fam.members, "description": fam.description}
                for name, fam in self._engine.FAMILIES.items()}
