"""
Sorting Module — Wraps the SortingEngine for module lifecycle.
"""
from __future__ import annotations
from typing import Any


class SortingModule:
    MODULE_NAME = "sorting"
    SOVEREIGNTY_LEVEL = "GUARDED"

    def __init__(self):
        self._active = False
        self._engine = None

    def mount(self) -> bool:
        from engines.sorting_engine import SortingEngine
        self._engine = SortingEngine()
        self._active = True
        return True

    def unmount(self) -> bool:
        self._active = False
        return True

    def sort(self, raw_input: Any) -> dict:
        if not self._engine:
            return {}
        result = self._engine.sort(raw_input)
        return {
            "category": result.category.name,
            "priority": result.priority.name,
            "route_target": result.route_target,
            "tags": result.tags,
            "confidence": result.confidence,
        }

    def get_stats(self) -> dict:
        return self._engine.get_category_stats() if self._engine else {}
