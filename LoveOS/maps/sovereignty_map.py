"""
Sovereignty Map — Maps sovereignty levels across all components.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SovereigntyMapping:
    component: str
    component_type: str  # "kernel", "engine", "module", "guard", "dispatcher", "processor"
    sovereignty_level: str  # "ABSOLUTE", "PROTECTED", "GUARDED", "OPEN"
    can_be_disabled: bool
    can_be_overridden: bool
    requires_consent: bool


class SovereigntyMap:
    """Maps sovereignty levels across the entire system."""

    def __init__(self):
        self._mappings: list[SovereigntyMapping] = [
            # Kernel — ABSOLUTE
            SovereigntyMapping("microkernel", "kernel", "ABSOLUTE", False, False, True),
            SovereigntyMapping("sovereignty_core", "kernel", "ABSOLUTE", False, False, True),

            # Engines
            SovereigntyMapping("sovereignty_engine", "engine", "ABSOLUTE", False, False, True),
            SovereigntyMapping("emotional_engine", "engine", "PROTECTED", True, False, True),
            SovereigntyMapping("spiritual_engine", "engine", "PROTECTED", True, False, True),
            SovereigntyMapping("sorting_engine", "engine", "GUARDED", True, True, False),
            SovereigntyMapping("legacy_engine", "engine", "PROTECTED", True, False, True),
            SovereigntyMapping("faith_engine", "engine", "PROTECTED", True, False, True),

            # Modules
            SovereigntyMapping("identity_module", "module", "ABSOLUTE", False, False, True),
            SovereigntyMapping("emotional_module", "module", "PROTECTED", True, False, True),
            SovereigntyMapping("spiritual_module", "module", "PROTECTED", True, False, True),
            SovereigntyMapping("security_module", "module", "PROTECTED", False, False, True),
            SovereigntyMapping("sorting_module", "module", "GUARDED", True, True, False),
            SovereigntyMapping("faith_module", "module", "PROTECTED", True, False, True),
            SovereigntyMapping("legacy_module", "module", "PROTECTED", True, False, True),
            SovereigntyMapping("audit_module", "module", "PROTECTED", False, False, True),

            # Guards
            SovereigntyMapping("sovereignty_guard", "guard", "ABSOLUTE", False, False, True),
            SovereigntyMapping("integrity_guard", "guard", "PROTECTED", False, False, True),
            SovereigntyMapping("permission_guard", "guard", "PROTECTED", True, False, True),
            SovereigntyMapping("boundary_guard", "guard", "ABSOLUTE", False, False, True),

            # Dispatchers
            SovereigntyMapping("event_dispatcher", "dispatcher", "GUARDED", True, True, False),
            SovereigntyMapping("module_dispatcher", "dispatcher", "GUARDED", True, True, False),
            SovereigntyMapping("ritual_dispatcher", "dispatcher", "PROTECTED", True, False, True),

            # Processors
            SovereigntyMapping("input_processor", "processor", "GUARDED", True, True, False),
            SovereigntyMapping("emotional_processor", "processor", "GUARDED", True, True, False),
            SovereigntyMapping("ritual_processor", "processor", "PROTECTED", True, False, True),
            SovereigntyMapping("pattern_processor", "processor", "GUARDED", True, True, False),
        ]

    def get_by_level(self, level: str) -> list[SovereigntyMapping]:
        return [m for m in self._mappings if m.sovereignty_level == level]

    def get_by_type(self, component_type: str) -> list[SovereigntyMapping]:
        return [m for m in self._mappings if m.component_type == component_type]

    def get_immutable(self) -> list[SovereigntyMapping]:
        """Return components that cannot be disabled or overridden."""
        return [m for m in self._mappings if not m.can_be_disabled and not m.can_be_overridden]

    def get_all(self) -> list[SovereigntyMapping]:
        return self._mappings.copy()

    def get_summary(self) -> dict:
        by_level = {}
        for m in self._mappings:
            by_level[m.sovereignty_level] = by_level.get(m.sovereignty_level, 0) + 1
        return {
            "total_components": len(self._mappings),
            "by_level": by_level,
            "immutable_count": len(self.get_immutable()),
        }
