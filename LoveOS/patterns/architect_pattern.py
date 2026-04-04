"""
Architect Pattern
═══════════════════════════════════════════════════
Defines the system-building behavioral pattern.
Active when the operator is in creation/building mode.

The Architect Pattern governs:
  - How system components are designed and connected
  - Module composition and dependency resolution
  - Blueprint validation before build
  - Legacy-aware design decisions
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import time


class DesignPhase(Enum):
    BLUEPRINT = auto()      # Planning and sketching
    PROTOTYPE = auto()      # First implementation
    ITERATION = auto()      # Refinement cycle
    VALIDATION = auto()     # Testing and verification
    INTEGRATION = auto()    # Connecting to existing system
    DEPLOYMENT = auto()     # Live in the system


@dataclass
class DesignDecision:
    """A recorded design decision."""
    component: str
    decision: str
    rationale: str
    sovereignty_impact: str     # "positive", "neutral", "negative"
    legacy_relevant: bool = False
    timestamp: float = field(default_factory=time.time)


@dataclass
class Blueprint:
    """A system component blueprint."""
    name: str
    component_type: str     # "engine", "module", "guard", "processor", etc.
    dependencies: list[str] = field(default_factory=list)
    interfaces: list[str] = field(default_factory=list)
    sovereignty_level: str = "GUARDED"
    design_decisions: list[DesignDecision] = field(default_factory=list)
    phase: DesignPhase = DesignPhase.BLUEPRINT
    validated: bool = False


class ArchitectPattern:
    """
    Behavioral pattern for system architecture work.
    
    Principles:
    1. Sovereignty First — Every component must pass sovereignty check
    2. Modular Independence — Components are self-contained
    3. Legacy Awareness — Design for intergenerational transmission
    4. Silent Security — No pop-ups, no interruptions
    5. Ritual Integration — Every lifecycle has ceremony
    """

    def __init__(self):
        self._blueprints: dict[str, Blueprint] = {}
        self._decisions: list[DesignDecision] = []
        self._log: list[dict] = []

    def create_blueprint(self, name: str, component_type: str,
                          dependencies: list[str] = None,
                          sovereignty_level: str = "GUARDED") -> Blueprint:
        """Create a new component blueprint."""
        bp = Blueprint(
            name=name, component_type=component_type,
            dependencies=dependencies or [],
            sovereignty_level=sovereignty_level,
        )
        self._blueprints[name] = bp
        self._log.append({"action": "create_blueprint", "name": name, "timestamp": time.time()})
        return bp

    def record_decision(self, component: str, decision: str, rationale: str,
                         sovereignty_impact: str = "neutral",
                         legacy_relevant: bool = False) -> DesignDecision:
        """Record an architectural design decision."""
        dd = DesignDecision(component, decision, rationale, sovereignty_impact, legacy_relevant)
        self._decisions.append(dd)
        bp = self._blueprints.get(component)
        if bp:
            bp.design_decisions.append(dd)
        return dd

    def validate_blueprint(self, name: str) -> dict:
        """Validate a blueprint for sovereignty and dependency issues."""
        bp = self._blueprints.get(name)
        if not bp:
            return {"valid": False, "errors": ["Blueprint not found"]}
        errors = []
        # Check dependencies exist
        for dep in bp.dependencies:
            if dep not in self._blueprints:
                errors.append(f"Missing dependency: {dep}")
        # Check sovereignty
        if bp.sovereignty_level not in ("ABSOLUTE", "PROTECTED", "GUARDED", "OPEN"):
            errors.append(f"Invalid sovereignty level: {bp.sovereignty_level}")
        # Check negative sovereignty impact decisions
        neg_decisions = [d for d in bp.design_decisions if d.sovereignty_impact == "negative"]
        if neg_decisions:
            errors.append(f"{len(neg_decisions)} decisions with negative sovereignty impact")
        bp.validated = len(errors) == 0
        return {"valid": bp.validated, "errors": errors}

    def get_all_blueprints(self) -> list[Blueprint]:
        return list(self._blueprints.values())

    def get_legacy_decisions(self) -> list[DesignDecision]:
        return [d for d in self._decisions if d.legacy_relevant]
