"""
Permission Schema — Sovereignty-grounded permission definitions.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import FrozenSet
import time


class PermissionLevel(Enum):
    DENY = 0
    READ = 1
    WRITE = 2
    EXECUTE = 3
    ADMIN = 4
    SOVEREIGN = 5     # Only the operator, only via sovereignty check


class PermissionScope(Enum):
    MODULE = auto()
    ENGINE = auto()
    GUARD = auto()
    RITUAL = auto()
    DATA = auto()
    IDENTITY = auto()
    EXTERNAL = auto()


@dataclass(frozen=True)
class Permission:
    """An immutable permission declaration."""
    name: str
    level: PermissionLevel
    scope: PermissionScope
    granted_to: str = ""
    granted_by: str = "sovereignty_core"
    conditions: tuple[str, ...] = ()
    expires_at: float = 0.0  # 0 = never expires

    @property
    def is_sovereign(self) -> bool:
        return self.level == PermissionLevel.SOVEREIGN


@dataclass
class PermissionGrant:
    """A record of a permission being granted."""
    permission: Permission
    timestamp: float = field(default_factory=time.time)
    sovereignty_verified: bool = True
    audit_id: str = ""


# ─── Default Permission Matrix ───────────────────

CORE_PERMISSIONS = {
    "identity.read": Permission("identity.read", PermissionLevel.READ, PermissionScope.IDENTITY),
    "identity.write": Permission("identity.write", PermissionLevel.SOVEREIGN, PermissionScope.IDENTITY),
    "module.mount": Permission("module.mount", PermissionLevel.ADMIN, PermissionScope.MODULE),
    "module.unmount": Permission("module.unmount", PermissionLevel.ADMIN, PermissionScope.MODULE),
    "guard.activate": Permission("guard.activate", PermissionLevel.ADMIN, PermissionScope.GUARD),
    "ritual.trigger": Permission("ritual.trigger", PermissionLevel.EXECUTE, PermissionScope.RITUAL),
    "data.read": Permission("data.read", PermissionLevel.READ, PermissionScope.DATA),
    "data.write": Permission("data.write", PermissionLevel.WRITE, PermissionScope.DATA),
    "data.export": Permission("data.export", PermissionLevel.SOVEREIGN, PermissionScope.DATA),
    "external.connect": Permission("external.connect", PermissionLevel.ADMIN, PermissionScope.EXTERNAL),
    "external.send": Permission("external.send", PermissionLevel.SOVEREIGN, PermissionScope.EXTERNAL),
}
