"""
Audit Module
═══════════════════════════════════════════════════
Captures, indexes, and manages the complete audit trail
for all LoveOS operations. The audit module mounts LAST
so it can capture the full boot sequence.

Audit Categories:
  - KERNEL:     Kernel lifecycle events
  - SOVEREIGNTY: Sovereignty checks and violations
  - MODULE:     Module mount/unmount/operations
  - RITUAL:     Ritual execution and outcomes
  - SECURITY:   Threat detection and resolution
  - LEGACY:     Legacy capture and transmission
  - SORTING:    Input classification and routing
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional
import time
import json
import hashlib


class AuditCategory(Enum):
    KERNEL = auto()
    SOVEREIGNTY = auto()
    MODULE = auto()
    RITUAL = auto()
    SECURITY = auto()
    LEGACY = auto()
    SORTING = auto()
    GENERAL = auto()


@dataclass
class AuditEntry:
    """A single audit log entry."""
    id: str = ""
    category: AuditCategory = AuditCategory.GENERAL
    action: str = ""
    source: str = ""
    details: dict = field(default_factory=dict)
    sovereignty_relevant: bool = False
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "id": self.id, "category": self.category.name,
            "action": self.action, "source": self.source,
            "details": self.details, "sovereignty_relevant": self.sovereignty_relevant,
            "timestamp": self.timestamp,
        }


class AuditModule:
    """
    Complete audit trail management.
    Immutable append-only log with sovereignty-sealed entries.
    """

    MODULE_NAME = "audit"
    SOVEREIGNTY_LEVEL = "PROTECTED"

    def __init__(self):
        self._active = False
        self._log: list[AuditEntry] = []
        self._entry_count = 0
        self._sealed_hashes: list[str] = []

    def mount(self) -> bool:
        self._active = True
        self.log(AuditCategory.MODULE, "audit_module_mounted", "kernel")
        return True

    def unmount(self) -> bool:
        self.log(AuditCategory.MODULE, "audit_module_unmounting", "kernel")
        self._active = False
        return True

    def log(self, category: AuditCategory, action: str, source: str,
            details: dict = None, sovereignty_relevant: bool = False) -> str:
        """Append an immutable audit entry. Returns entry ID."""
        self._entry_count += 1
        entry_id = f"audit-{self._entry_count:08d}"
        entry = AuditEntry(
            id=entry_id, category=category, action=action,
            source=source, details=details or {},
            sovereignty_relevant=sovereignty_relevant,
        )
        self._log.append(entry)

        # Compute and store hash for immutability verification
        entry_hash = hashlib.sha256(json.dumps(entry.to_dict(), default=str).encode()).hexdigest()[:16]
        self._sealed_hashes.append(entry_hash)

        return entry_id

    def query(self, category: Optional[AuditCategory] = None,
              source: Optional[str] = None, limit: int = 50) -> list[dict]:
        """Query audit entries by category and/or source."""
        results = self._log
        if category:
            results = [e for e in results if e.category == category]
        if source:
            results = [e for e in results if e.source == source]
        return [e.to_dict() for e in results[-limit:]]

    def verify_integrity(self) -> bool:
        """Verify the audit log has not been tampered with."""
        for i, entry in enumerate(self._log):
            expected = hashlib.sha256(
                json.dumps(entry.to_dict(), default=str).encode()
            ).hexdigest()[:16]
            if i < len(self._sealed_hashes) and self._sealed_hashes[i] != expected:
                return False
        return True

    def export(self) -> list[dict]:
        """Export the full audit log."""
        return [e.to_dict() for e in self._log]

    def get_stats(self) -> dict:
        by_category = {}
        for e in self._log:
            cat = e.category.name
            by_category[cat] = by_category.get(cat, 0) + 1
        return {
            "total_entries": len(self._log),
            "by_category": by_category,
            "integrity_verified": self.verify_integrity(),
            "sovereignty_entries": len([e for e in self._log if e.sovereignty_relevant]),
        }
