"""
Ritual Registry — Central store of all ritual definitions.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import time


@dataclass
class RitualDef:
    """A registered ritual definition."""
    name: str
    ritual_type: str        # "boot", "grounding", "audit", "closure", "custom"
    description: str = ""
    steps: list[str] = field(default_factory=list)
    duration_estimate_seconds: float = 0.0
    sovereignty_required: bool = True
    registered_at: float = field(default_factory=time.time)


class RitualRegistry:
    def __init__(self):
        self._rituals: dict[str, RitualDef] = {}
        self._initialize_core_rituals()

    def _initialize_core_rituals(self):
        core = [
            RitualDef("boot_ritual", "boot", "System boot ceremony",
                      ["declare_presence", "set_intention", "affirm_sovereignty",
                       "verify_identity_seal", "acknowledge_purpose"],
                      duration_estimate_seconds=30),
            RitualDef("grounding_ritual", "grounding", "Centering and presence restoration",
                      ["pause_processing", "breathe_cycle", "body_scan",
                       "sovereignty_check", "intention_reset", "resume_processing"],
                      duration_estimate_seconds=120),
            RitualDef("audit_ritual", "audit", "System state review",
                      ["capture_full_state", "verify_integrity_seals",
                       "check_sovereignty_boundaries", "review_threat_log",
                       "generate_audit_report"],
                      duration_estimate_seconds=60),
            RitualDef("closure_ritual", "closure", "Graceful shutdown ceremony",
                      ["express_gratitude", "archive_session_state",
                       "seal_audit_trail", "declare_closure", "sovereign_halt"],
                      duration_estimate_seconds=30),
            RitualDef("moonlight_reset", "custom", "Classical music emotional reset (Moonlight Sonata)",
                      ["pause_all_processing", "engage_moonlight_sonata",
                       "open_emotional_channel", "process_release",
                       "restore_sovereignty", "resume_processing"],
                      duration_estimate_seconds=300),
        ]
        for r in core:
            self._rituals[r.name] = r

    def register(self, ritual: RitualDef):
        self._rituals[ritual.name] = ritual

    def lookup(self, name: str) -> Optional[RitualDef]:
        return self._rituals.get(name)

    def get_by_type(self, ritual_type: str) -> list[RitualDef]:
        return [r for r in self._rituals.values() if r.ritual_type == ritual_type]

    def get_all(self) -> list[RitualDef]:
        return list(self._rituals.values())

    def get_stats(self) -> dict:
        by_type = {}
        for r in self._rituals.values():
            by_type[r.ritual_type] = by_type.get(r.ritual_type, 0) + 1
        return {"total": len(self._rituals), "by_type": by_type}
