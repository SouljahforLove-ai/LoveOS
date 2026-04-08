"""
Permission Matrix — Complete access control matrix for all SoulJahOS components.
═══════════════════════════════════════════════════
Maps every component to every operation with explicit
permission levels. The matrix is the single source of
truth for access control.

Permission Levels:
  DENY     → No access under any circumstance
  READ     → Observe state only
  WRITE    → Modify state
  EXECUTE  → Trigger behavior
  ADMIN    → Full control except sovereignty override
  SOVEREIGN → Full control including sovereignty operations
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional
import time


class AccessLevel(IntEnum):
    DENY = 0
    READ = 1
    WRITE = 2
    EXECUTE = 3
    ADMIN = 4
    SOVEREIGN = 5


@dataclass
class MatrixEntry:
    """Single cell in the permission matrix."""
    component: str
    operation: str
    required_level: AccessLevel
    override_allowed: bool = False
    audit_required: bool = True
    notes: str = ""


@dataclass
class AccessRequest:
    """A request for access to a component operation."""
    requestor: str
    component: str
    operation: str
    level: AccessLevel
    timestamp: float = field(default_factory=time.time)


@dataclass
class AccessDecision:
    """Result of an access control check."""
    granted: bool
    request: AccessRequest
    required_level: AccessLevel
    reason: str = ""
    timestamp: float = field(default_factory=time.time)


class PermissionMatrix:
    """
    The Permission Matrix — who can do what, where.
    
    Sovereignty axiom: No external entity can override
    SOVEREIGN-level permissions. The operator is the
    sole sovereign.
    """

    def __init__(self):
        self._matrix: dict[str, dict[str, MatrixEntry]] = {}
        self._grants: dict[str, AccessLevel] = {}  # entity → max level
        self._log: list[dict] = []
        self._build_default_matrix()

    def _build_default_matrix(self):
        """Build the canonical permission matrix."""
        components = {
            "kernel": {
                "boot":     MatrixEntry("kernel", "boot", AccessLevel.SOVEREIGN, False, True, "Only sovereign can boot"),
                "halt":     MatrixEntry("kernel", "halt", AccessLevel.SOVEREIGN, False, True, "Only sovereign can halt"),
                "status":   MatrixEntry("kernel", "status", AccessLevel.READ, False, False),
                "config":   MatrixEntry("kernel", "config", AccessLevel.ADMIN, False, True),
            },
            "identity": {
                "read":     MatrixEntry("identity", "read", AccessLevel.READ, False, False),
                "modify":   MatrixEntry("identity", "modify", AccessLevel.SOVEREIGN, False, True, "Identity is immutable without sovereignty"),
                "verify":   MatrixEntry("identity", "verify", AccessLevel.EXECUTE, False, True),
            },
            "emotional": {
                "read":     MatrixEntry("emotional", "read", AccessLevel.READ, False, False),
                "process":  MatrixEntry("emotional", "process", AccessLevel.EXECUTE, False, False),
                "override": MatrixEntry("emotional", "override", AccessLevel.DENY, False, True, "Emotions cannot be overridden"),
            },
            "spiritual": {
                "read":     MatrixEntry("spiritual", "read", AccessLevel.READ, False, False),
                "process":  MatrixEntry("spiritual", "process", AccessLevel.EXECUTE, False, False),
                "align":    MatrixEntry("spiritual", "align", AccessLevel.EXECUTE, False, True),
            },
            "security": {
                "read":     MatrixEntry("security", "read", AccessLevel.ADMIN, False, True),
                "configure": MatrixEntry("security", "configure", AccessLevel.SOVEREIGN, False, True),
                "disable":  MatrixEntry("security", "disable", AccessLevel.DENY, False, True, "Security cannot be disabled"),
            },
            "sovereignty": {
                "check":    MatrixEntry("sovereignty", "check", AccessLevel.READ, False, False),
                "declare":  MatrixEntry("sovereignty", "declare", AccessLevel.SOVEREIGN, False, True),
                "override": MatrixEntry("sovereignty", "override", AccessLevel.DENY, False, True, "Sovereignty cannot be overridden"),
            },
            "audit": {
                "read":     MatrixEntry("audit", "read", AccessLevel.ADMIN, False, True),
                "write":    MatrixEntry("audit", "write", AccessLevel.EXECUTE, False, False, "System writes; operator reads"),
                "delete":   MatrixEntry("audit", "delete", AccessLevel.DENY, False, True, "Audit is append-only"),
                "export":   MatrixEntry("audit", "export", AccessLevel.SOVEREIGN, False, True),
            },
            "legacy": {
                "read":     MatrixEntry("legacy", "read", AccessLevel.READ, False, False),
                "capture":  MatrixEntry("legacy", "capture", AccessLevel.EXECUTE, False, True),
                "transmit": MatrixEntry("legacy", "transmit", AccessLevel.SOVEREIGN, False, True, "Only sovereign transmits legacy"),
            },
            "faith": {
                "read":     MatrixEntry("faith", "read", AccessLevel.READ, False, False),
                "process":  MatrixEntry("faith", "process", AccessLevel.EXECUTE, False, False),
                "covenant": MatrixEntry("faith", "covenant", AccessLevel.SOVEREIGN, False, True),
            },
            "sorting": {
                "read":     MatrixEntry("sorting", "read", AccessLevel.READ, False, False),
                "process":  MatrixEntry("sorting", "process", AccessLevel.EXECUTE, False, False),
                "configure": MatrixEntry("sorting", "configure", AccessLevel.ADMIN, False, True),
            },
        }
        self._matrix = components

    def check_access(self, request: AccessRequest) -> AccessDecision:
        """Check whether an access request is granted."""
        comp = self._matrix.get(request.component)
        if not comp:
            return AccessDecision(False, request, AccessLevel.DENY, "Component not found")

        entry = comp.get(request.operation)
        if not entry:
            return AccessDecision(False, request, AccessLevel.DENY, "Operation not found")

        if entry.required_level == AccessLevel.DENY:
            decision = AccessDecision(False, request, entry.required_level, "Operation permanently denied")
        elif request.level >= entry.required_level:
            decision = AccessDecision(True, request, entry.required_level)
        else:
            decision = AccessDecision(False, request, entry.required_level,
                                       f"Requires {entry.required_level.name}, got {request.level.name}")

        if entry.audit_required:
            self._log.append({
                "action": "access_check",
                "requestor": request.requestor,
                "component": request.component,
                "operation": request.operation,
                "granted": decision.granted,
                "timestamp": time.time(),
            })
        return decision

    def grant_level(self, entity: str, level: AccessLevel):
        """Grant an access level to an entity."""
        self._grants[entity] = level

    def get_entity_level(self, entity: str) -> AccessLevel:
        return self._grants.get(entity, AccessLevel.DENY)

    def get_matrix_summary(self) -> dict:
        summary = {}
        for comp_name, ops in self._matrix.items():
            summary[comp_name] = {op: entry.required_level.name for op, entry in ops.items()}
        return summary

    def get_audit_log(self) -> list[dict]:
        return self._log.copy()
