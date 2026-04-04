"""
Identity Schema
═══════════════════════════════════════════════════
Defines the operator identity data model.
Identity is ABSOLUTE sovereignty — it cannot be
overridden, redefined, or tampered with externally.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional, FrozenSet
import time
import hashlib


@dataclass(frozen=False)
class IdentityCore:
    """The immutable core of operator identity."""
    sovereign_name: str = ""
    aliases: tuple[str, ...] = ()
    sigil: str = "N2 m(THYSELF)e | 👁️ ."
    purpose_declaration: str = ""
    sovereignty_level: str = "ABSOLUTE"
    created_at: float = field(default_factory=time.time)

    def seal(self) -> str:
        raw = f"{self.sovereign_name}:{self.sigil}:{self.purpose_declaration}"
        return hashlib.sha256(raw.encode()).hexdigest()[:24]


@dataclass
class IdentityProfile:
    """Extended operator identity profile."""
    core: IdentityCore = field(default_factory=IdentityCore)
    roles: list[str] = field(default_factory=list)
    skills: dict[str, str] = field(default_factory=dict)  # skill -> level
    values: list[str] = field(default_factory=list)
    boundaries: list[str] = field(default_factory=list)
    relationships: dict[str, dict] = field(default_factory=dict)
    goals: list[str] = field(default_factory=list)
    legacy_targets: list[str] = field(default_factory=list)
    sovereignty_sealed: bool = True

    def validate(self) -> bool:
        return bool(self.core.sovereign_name and self.core.sigil)


@dataclass
class IdentityEvent:
    """A change event on the identity profile."""
    field_changed: str
    old_value: Any = None
    new_value: Any = None
    authorized_by: str = ""
    timestamp: float = field(default_factory=time.time)
    sovereignty_check: bool = True


# ─── Default Operator Identity ────────────────────

DEFAULT_IDENTITY = IdentityProfile(
    core=IdentityCore(
        sovereign_name="Jorge",
        aliases=("Jeremiah", "Junebug", "Vision"),
        sigil="N2 m(THYSELF)e | 👁️ .",
        purpose_declaration="Love is the operating system. Everything else is an app.",
    ),
    roles=["architect", "operator", "visionary", "builder", "father"],
    values=["love", "sovereignty", "legacy", "dignity", "presence", "faith"],
    boundaries=[
        "Identity cannot be overridden externally",
        "Consent is required for all actions",
        "Dignity is computationally sacred",
        "Data never leaves without explicit authorization",
    ],
    legacy_targets=["Zen"],
)
