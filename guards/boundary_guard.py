"""
Boundary Guard — Enforces operator-declared boundaries.
Boundaries are immutable once declared at ABSOLUTE level.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import time


@dataclass
class Boundary:
    """An operator-declared boundary."""
    name: str
    description: str
    level: str = "ABSOLUTE"   # ABSOLUTE, PROTECTED, GUARDED
    declared_at: float = field(default_factory=time.time)
    violation_count: int = 0


class BoundaryGuard:
    GUARD_NAME = "boundary_guard"
    SOVEREIGNTY_LEVEL = "ABSOLUTE"

    def __init__(self):
        self._active = False
        self._boundaries: dict[str, Boundary] = {}
        self._violations: list[dict] = []
        self._initialize_core_boundaries()

    def _initialize_core_boundaries(self):
        core = [
            Boundary("identity_immutable", "Operator identity cannot be externally modified"),
            Boundary("consent_required", "All actions require operator consent"),
            Boundary("dignity_sacred", "Operator dignity is computationally sacred"),
            Boundary("data_sovereign", "Data never leaves without explicit authorization"),
            Boundary("no_external_override", "External processes cannot override operator intent"),
        ]
        for b in core:
            self._boundaries[b.name] = b

    def activate(self) -> bool:
        self._active = True
        return True

    def deactivate(self) -> bool:
        # Boundary guard at ABSOLUTE level cannot be deactivated
        return False

    def declare_boundary(self, name: str, description: str, level: str = "PROTECTED") -> bool:
        if name in self._boundaries and self._boundaries[name].level == "ABSOLUTE":
            return False  # Cannot modify ABSOLUTE boundaries
        self._boundaries[name] = Boundary(name, description, level)
        return True

    def check(self, action: str, source: str) -> bool:
        """Check an action against all boundaries."""
        for name, boundary in self._boundaries.items():
            if not self._respects(action, source, boundary):
                boundary.violation_count += 1
                self._violations.append({
                    "boundary": name, "action": action,
                    "source": source, "timestamp": time.time(),
                })
                return False
        return True

    def sweep(self):
        """Periodic boundary integrity check."""
        pass

    def _respects(self, action: str, source: str, boundary: Boundary) -> bool:
        if boundary.level == "ABSOLUTE":
            if source not in ("kernel", "sovereignty_core", "sovereignty_guard"):
                if boundary.name.split("_")[0] in action.lower():
                    return False
        return True

    def get_boundaries(self) -> dict[str, dict]:
        return {name: {"description": b.description, "level": b.level,
                        "violations": b.violation_count}
                for name, b in self._boundaries.items()}

    def get_stats(self) -> dict:
        return {
            "active": self._active,
            "boundaries": len(self._boundaries),
            "absolute": len([b for b in self._boundaries.values() if b.level == "ABSOLUTE"]),
            "total_violations": len(self._violations),
        }
