"""
SoulJahOS Configuration — Runtime configuration management.
═══════════════════════════════════════════════════
Loads configuration from YAML, validates against sovereignty
axioms, and provides typed access to all config values.

Configuration is hierarchical:
  defaults → config file → runtime overrides

Sovereignty axioms cannot be overridden by config.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import hashlib
import time


@dataclass
class KernelConfig:
    boot_timeout: float = 30.0
    max_modules: int = 64
    ipc_queue_size: int = 1024
    sovereignty_enforcement: bool = True      # Cannot be disabled
    audit_enabled: bool = True                 # Cannot be disabled


@dataclass
class EngineConfig:
    emotional_dimensions: int = 7
    spiritual_dimensions: int = 8
    sovereignty_floor: float = 0.5
    emotional_sovereignty_floor: float = 0.3
    sorting_pipeline_stages: int = 7
    legacy_significance_threshold: float = 0.3
    faith_tradition: str = "INTEGRATED"


@dataclass
class SecurityConfig:
    silent_mode: bool = True                   # No pop-ups
    threat_log_enabled: bool = True
    quarantine_enabled: bool = True
    dangerous_extensions: list[str] = field(default_factory=lambda: [
        ".exe", ".bat", ".cmd", ".scr", ".pif", ".com",
        ".vbs", ".js", ".wsh", ".wsf", ".ps1",
    ])
    injection_detection: bool = True


@dataclass
class RitualConfig:
    boot_ritual_enabled: bool = True
    grounding_breathe_pattern: dict = field(default_factory=lambda: {"inhale": 4, "hold": 7, "exhale": 8})
    grounding_cycles: int = 3
    closure_gratitude: bool = True
    audit_interval_seconds: float = 3600.0
    moonlight_sonata_grounding: bool = True


@dataclass
class OperatorConfig:
    sovereign_name: str = "Jorge"
    aliases: list[str] = field(default_factory=lambda: ["Jeremiah", "Junebug", "Vision"])
    sigil: str = "N2 m(THYSELF)e | 👁️ ."
    purpose: str = "To build, protect, and transmit sovereign love across generations."
    legacy_target: str = "Zen"


@dataclass
class SoulJahOSConfig:
    """Master configuration for SoulJahOS."""
    version: str = "1.0.0"
    codename: str = "Sovereign Genesis"
    motto: str = "Love is the operating system. Everything else is an app."
    proprietary_owner: str = "SoulJahForLove"

    kernel: KernelConfig = field(default_factory=KernelConfig)
    engines: EngineConfig = field(default_factory=EngineConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    rituals: RitualConfig = field(default_factory=RitualConfig)
    operator: OperatorConfig = field(default_factory=OperatorConfig)

    def validate(self) -> dict:
        """Validate configuration against sovereignty axioms."""
        errors = []
        # Sovereignty enforcement CANNOT be disabled
        if not self.kernel.sovereignty_enforcement:
            errors.append("VIOLATION: sovereignty_enforcement cannot be False")
            self.kernel.sovereignty_enforcement = True
        # Audit CANNOT be disabled
        if not self.kernel.audit_enabled:
            errors.append("VIOLATION: audit_enabled cannot be False")
            self.kernel.audit_enabled = True
        # Security silent mode is mandatory
        if not self.security.silent_mode:
            errors.append("WARNING: silent_mode should be True (no pop-ups)")
        # Sovereignty floor must be positive
        if self.engines.sovereignty_floor <= 0:
            errors.append("VIOLATION: sovereignty_floor must be > 0")
            self.engines.sovereignty_floor = 0.5
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "config_seal": self._compute_seal(),
        }

    def _compute_seal(self) -> str:
        data = f"{self.version}:{self.operator.sovereign_name}:{self.operator.sigil}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    @classmethod
    def load_defaults(cls) -> SoulJahOSConfig:
        """Load the default canonical configuration."""
        config = cls()
        config.validate()
        return config
