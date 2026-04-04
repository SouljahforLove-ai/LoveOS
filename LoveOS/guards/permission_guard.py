"""
Permission Guard — Enforces the permission matrix across all operations.
"""

from __future__ import annotations
from typing import Any, Optional
import time


class PermissionGuard:
    GUARD_NAME = "permission_guard"
    SOVEREIGNTY_LEVEL = "PROTECTED"

    def __init__(self):
        self._active = False
        self._grants: dict[str, dict] = {}  # entity → {permission → level}
        self._denials: list[dict] = []

    def activate(self) -> bool:
        self._active = True
        return True

    def deactivate(self) -> bool:
        self._active = False
        return True

    def grant(self, entity: str, permission: str, level: int):
        """Grant a permission to an entity."""
        if entity not in self._grants:
            self._grants[entity] = {}
        self._grants[entity][permission] = level

    def check(self, entity: str, permission: str, required_level: int) -> bool:
        """Check if an entity has sufficient permission."""
        if not self._active:
            return True  # Guard inactive, passthrough

        granted = self._grants.get(entity, {}).get(permission, 0)
        if granted >= required_level:
            return True

        self._denials.append({
            "entity": entity, "permission": permission,
            "required": required_level, "granted": granted,
            "timestamp": time.time(),
        })
        return False

    def sweep(self):
        """Periodic permission audit."""
        pass

    def get_denials(self) -> list[dict]:
        return self._denials.copy()

    def get_stats(self) -> dict:
        return {
            "active": self._active,
            "entities": len(self._grants),
            "total_grants": sum(len(v) for v in self._grants.values()),
            "denials": len(self._denials),
        }
