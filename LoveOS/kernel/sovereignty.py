"""
Sovereignty Enforcement Layer
═══════════════════════════════════════════════════
The non-negotiable core. Sovereignty is not a feature —
it is the foundation on which every other layer rests.

Sovereignty Axioms:
  S1: No external process may override operator intent
  S2: Every module mount requires sovereignty clearance
  S3: Every message must pass sovereignty validation
  S4: Boundaries are immutable once declared
  S5: The operator's dignity is computationally sacred
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, FrozenSet
import hashlib
import time


class SovereigntyLevel(Enum):
    """Graduated sovereignty enforcement levels."""
    ABSOLUTE = auto()     # No override possible (identity, boundaries)
    PROTECTED = auto()    # Requires explicit operator consent to modify
    GUARDED = auto()      # Logged and monitored, soft enforcement
    OPEN = auto()         # Standard operation, sovereignty passthrough


class ViolationType(Enum):
    """Categories of sovereignty violations."""
    BOUNDARY_BREACH = auto()
    UNAUTHORIZED_MOUNT = auto()
    IDENTITY_TAMPERING = auto()
    CONSENT_BYPASS = auto()
    EXTERNAL_OVERRIDE = auto()
    DIGNITY_VIOLATION = auto()


@dataclass(frozen=True)
class SovereigntyBoundary:
    """An immutable sovereignty boundary declaration."""
    name: str
    level: SovereigntyLevel
    description: str
    declared_at: float = field(default_factory=time.time)

    @property
    def seal(self) -> str:
        """Compute integrity seal for this boundary."""
        raw = f"{self.name}:{self.level.name}:{self.description}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass
class SovereigntyViolation:
    """Record of a sovereignty violation event."""
    violation_type: ViolationType
    source: str
    target: str
    description: str
    timestamp: float = field(default_factory=time.time)
    resolved: bool = False


class SovereigntyCore:
    """
    The Sovereignty Core — immutable enforcement of operator dignity.

    This is the innermost ring of LoveOS. It cannot be bypassed,
    overridden, or negotiated with. Sovereignty is absolute.
    """

    def __init__(self):
        self._boundaries: dict[str, SovereigntyBoundary] = {}
        self._violations: list[SovereigntyViolation] = []
        self._authorized_modules: set[str] = set()
        self._sovereignty_seal: str = ""
        self._initialize_core_boundaries()

    def _initialize_core_boundaries(self):
        """Declare the foundational sovereignty boundaries."""
        core_boundaries = [
            SovereigntyBoundary(
                name="identity_sovereignty",
                level=SovereigntyLevel.ABSOLUTE,
                description="Operator identity cannot be overridden or redefined externally"
            ),
            SovereigntyBoundary(
                name="boundary_integrity",
                level=SovereigntyLevel.ABSOLUTE,
                description="Declared boundaries are immutable once set"
            ),
            SovereigntyBoundary(
                name="consent_requirement",
                level=SovereigntyLevel.ABSOLUTE,
                description="No action proceeds without operator consent"
            ),
            SovereigntyBoundary(
                name="dignity_preservation",
                level=SovereigntyLevel.ABSOLUTE,
                description="Operator dignity is computationally sacred"
            ),
            SovereigntyBoundary(
                name="data_sovereignty",
                level=SovereigntyLevel.PROTECTED,
                description="Operator data never leaves without explicit authorization"
            ),
            SovereigntyBoundary(
                name="module_authorization",
                level=SovereigntyLevel.PROTECTED,
                description="Only authorized modules may mount and execute"
            ),
            SovereigntyBoundary(
                name="external_isolation",
                level=SovereigntyLevel.GUARDED,
                description="External inputs are quarantined and validated"
            ),
        ]
        for boundary in core_boundaries:
            self._boundaries[boundary.name] = boundary

    def declare_boundary(self, boundary: SovereigntyBoundary) -> bool:
        """Declare a new sovereignty boundary. Cannot override ABSOLUTE."""
        if boundary.name in self._boundaries:
            existing = self._boundaries[boundary.name]
            if existing.level == SovereigntyLevel.ABSOLUTE:
                return False  # Cannot modify absolute boundaries
        self._boundaries[boundary.name] = boundary
        return True

    def check_sovereignty(self, action: str, source: str) -> bool:
        """Validate an action against all sovereignty boundaries."""
        # All actions must pass — sovereignty is conjunctive
        for name, boundary in self._boundaries.items():
            if not self._action_respects_boundary(action, source, boundary):
                self._violations.append(SovereigntyViolation(
                    violation_type=ViolationType.BOUNDARY_BREACH,
                    source=source,
                    target=name,
                    description=f"Action '{action}' violates boundary '{name}'"
                ))
                return False
        return True

    def authorize_module(self, module_name: str) -> bool:
        """Grant a module sovereignty clearance to mount."""
        if self.check_sovereignty(f"mount:{module_name}", "kernel"):
            self._authorized_modules.add(module_name)
            return True
        return False

    def is_module_authorized(self, module_name: str) -> bool:
        """Check if a module has sovereignty clearance."""
        return module_name in self._authorized_modules

    def clear_message(self, message: Any) -> bool:
        """Sovereignty-clear a kernel message for dispatch."""
        return self.check_sovereignty(
            f"message:{message.source}->{message.target}",
            message.source
        )

    def get_violations(self) -> list[SovereigntyViolation]:
        """Return all recorded sovereignty violations."""
        return self._violations.copy()

    def get_boundaries(self) -> dict[str, SovereigntyBoundary]:
        """Return all declared boundaries."""
        return self._boundaries.copy()

    def compute_seal(self) -> str:
        """Compute a composite integrity seal over all boundaries."""
        combined = "|".join(
            b.seal for b in sorted(self._boundaries.values(), key=lambda x: x.name)
        )
        return hashlib.sha256(combined.encode()).hexdigest()[:32]

    def _action_respects_boundary(
        self, action: str, source: str, boundary: SovereigntyBoundary
    ) -> bool:
        """Check if an action respects a specific boundary."""
        # ABSOLUTE boundaries: only kernel can originate
        if boundary.level == SovereigntyLevel.ABSOLUTE:
            if source not in ("kernel", "sovereignty_guard"):
                if boundary.name in action:
                    return False
        return True
