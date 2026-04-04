"""
Legacy Module — Wraps the LegacyEngine for module lifecycle.
"""
from __future__ import annotations
from typing import Any, Optional


class LegacyModule:
    MODULE_NAME = "legacy"
    SOVEREIGNTY_LEVEL = "PROTECTED"

    def __init__(self):
        self._active = False
        self._engine = None

    def mount(self) -> bool:
        from engines.legacy_engine import LegacyEngine
        self._engine = LegacyEngine()
        self._active = True
        return True

    def unmount(self) -> bool:
        self._active = False
        return True

    def capture(self, title: str, content: Any, category: str, tags: list[str] = None) -> dict:
        if not self._engine:
            return {}
        from engines.legacy_engine import LegacyCategory
        cat = getattr(LegacyCategory, category.upper(), LegacyCategory.KNOWLEDGE)
        item = self._engine.capture(title, content, cat, tags)
        return {"id": item.id, "title": item.title, "category": cat.name}

    def transmit(self, item_id: str, recipient: str) -> dict:
        if not self._engine:
            return {}
        record = self._engine.transmit(item_id, recipient)
        return {"success": record.success, "recipient": record.recipient}

    def get_stats(self) -> dict:
        return self._engine.get_stats() if self._engine else {}
