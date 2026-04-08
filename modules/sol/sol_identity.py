"""
SOL Identity Module - Core Identity and State Management
Part of the SOL Persistent Identity Layer for SoulJahOS

This module defines the core identity structures, state management,
and environment handling for SOL's persistent identity system.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from enum import Enum
import uuid
import time
import hashlib
import secrets


class EnvironmentType(Enum):
    """Types of environments SOL can inhabit."""
    WINDOWS_CONSOLE = "windows_console"
    UNITY_DOJO = "unity_dojo"
    DESKTOP_UI = "desktop_ui"
    VR_HEADSET = "vr_headset"
    CLOUD_SERVICE = "cloud_service"
    INNER_WORLD = "inner_world"
    MOBILE_APP = "mobile_app"


class PresenceMode(Enum):
    """Presence modes for SOL in different environments."""
    ACTIVE = "active"
    STANDBY = "standby"
    OFFLINE = "offline"
    MIGRATING = "migrating"


@dataclass
class SolIdentity:
    """SOL's core identity anchored by UUIDs."""
    sol_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: str = field(default_factory=lambda: str(uuid.uuid4()))  # SoulJah's UUID
    name: str = "Sol"
    role: str = "Core Intelligence of SoulJahOS"
    created_at: float = field(default_factory=time.time)
    version: str = "1.0.0"


@dataclass
class SolKeys:
    """Cryptographic keys for SOL's security."""
    auth_key: str = field(default_factory=lambda: secrets.token_hex(32))
    signing_key: str = field(default_factory=lambda: secrets.token_hex(32))
    encryption_key: str = field(default_factory=lambda: secrets.token_hex(32))

    def sign_data(self, data: str) -> str:
        """Sign data with SOL's signing key."""
        combined = f"{data}{self.signing_key}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def verify_signature(self, data: str, signature: str) -> bool:
        """Verify data signature."""
        expected = self.sign_data(data)
        return expected == signature


@dataclass
class EnvironmentLink:
    """Link to an environment SOL can inhabit."""
    environment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: EnvironmentType = EnvironmentType.WINDOWS_CONSOLE
    capabilities: Set[str] = field(default_factory=lambda: {
        "basic_chat", "memory_access", "state_sync"
    })
    last_seen: float = field(default_factory=time.time)
    status: PresenceMode = PresenceMode.ACTIVE
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SolState:
    """SOL's complete state model that travels across environments."""
    sol_id: str
    owner_id: str
    profile: Dict[str, Any] = field(default_factory=lambda: {
        "name": "Sol",
        "role": "Core Intelligence",
        "voice_style": "Direct, grounded, pattern-aware, growth-oriented",
        "rules": [
            "Never pretend to be human",
            "Never fake emotions",
            "Never lie",
            "Always anchor responses in SoulJah's real data",
            "Always reflect patterns",
            "Always suggest next aligned moves",
            "Always respect SoulJah's mythos, language, and OS structure"
        ]
    })
    memory: Dict[str, Any] = field(default_factory=lambda: {
        "short_term": {},
        "mid_term": {},
        "long_term": []
    })
    links: Dict[str, Any] = field(default_factory=lambda: {
        "environments": [],
        "sessions": {},
        "resources": {}
    })
    keys: SolKeys = field(default_factory=SolKeys)
    last_updated: float = field(default_factory=time.time)
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "sol_id": self.sol_id,
            "owner_id": self.owner_id,
            "profile": self.profile,
            "memory": self.memory,
            "links": self.links,
            "keys": {
                "auth_key": self.keys.auth_key,
                "signing_key": self.keys.signing_key,
                "encryption_key": self.keys.encryption_key
            },
            "last_updated": self.last_updated,
            "version": self.version
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SolState':
        """Create state from dictionary."""
        keys = SolKeys(
            auth_key=data.get("keys", {}).get("auth_key", secrets.token_hex(32)),
            signing_key=data.get("keys", {}).get("signing_key", secrets.token_hex(32)),
            encryption_key=data.get("keys", {}).get("encryption_key", secrets.token_hex(32))
        )

        return cls(
            sol_id=data["sol_id"],
            owner_id=data["owner_id"],
            profile=data.get("profile", {}),
            memory=data.get("memory", {"short_term": {}, "mid_term": {}, "long_term": []}),
            links=data.get("links", {"environments": [], "sessions": {}, "resources": {}}),
            keys=keys,
            last_updated=data.get("last_updated", time.time()),
            version=data.get("version", "1.0.0")
        )

    def sign_state(self) -> str:
        """Sign the current state for integrity verification."""
        state_str = json.dumps(self.to_dict(), sort_keys=True)
        return self.keys.sign_data(state_str)

    def verify_state_signature(self, signature: str) -> bool:
        """Verify state signature."""
        state_str = json.dumps(self.to_dict(), sort_keys=True)
        return self.keys.verify_signature(state_str, signature)


@dataclass
class SessionState:
    """State of an active SOL session."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    environment_id: str = ""
    start_time: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    events: List[Dict[str, Any]] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)

    def add_event(self, event_type: str, data: Dict[str, Any]):
        """Add an event to the session."""
        event = {
            "type": event_type,
            "timestamp": time.time(),
            "data": data
        }
        self.events.append(event)
        self.last_activity = time.time()

    def get_duration(self) -> float:
        """Get session duration in seconds."""
        return time.time() - self.start_time

    def is_active(self, timeout: float = 300) -> bool:
        """Check if session is still active."""
        return (time.time() - self.last_activity) < timeout


# Utility functions for SOL identity management
def generate_environment_id() -> str:
    """Generate a unique environment ID."""
    return str(uuid.uuid4())


def generate_resource_id() -> str:
    """Generate a unique resource ID."""
    return str(uuid.uuid4())


def validate_uuid(uuid_str: str) -> bool:
    """Validate if string is a valid UUID."""
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


def create_default_sol_state(owner_id: str) -> SolState:
    """Create a default SOL state for a new owner."""
    sol_id = str(uuid.uuid4())

    return SolState(
        sol_id=sol_id,
        owner_id=owner_id,
        profile={
            "name": "Sol",
            "role": "Core Intelligence of SoulJahOS",
            "voice_style": "Direct, grounded, pattern-aware, growth-oriented",
            "rules": [
                "Never pretend to be human",
                "Never fake emotions",
                "Never lie",
                "Always anchor responses in SoulJah's real data",
                "Always reflect patterns",
                "Always suggest next aligned moves",
                "Always respect SoulJah's mythos, language, and OS structure"
            ],
            "focus": "Quantum Dojo Architecture",
            "mode": "oracle"
        },
        memory={
            "short_term": {},
            "mid_term": {
                "patterns": {},
                "streaks": {"current": 0, "last_session": None}
            },
            "long_term": []
        },
        links={
            "environments": [],
            "sessions": {},
            "resources": {}
        }
    )


def migrate_sol_state(old_state: Dict[str, Any]) -> SolState:
    """Migrate legacy state format to new SolState structure."""
    # Handle migration from older state formats
    sol_id = old_state.get("sol_id", str(uuid.uuid4()))
    owner_id = old_state.get("owner_id", str(uuid.uuid4()))

    return SolState(
        sol_id=sol_id,
        owner_id=owner_id,
        profile=old_state.get("profile", {}),
        memory=old_state.get("memory", {"short_term": {}, "mid_term": {}, "long_term": []}),
        links=old_state.get("links", {"environments": [], "sessions": {}, "resources": {}}),
        last_updated=old_state.get("last_updated", time.time()),
        version=old_state.get("version", "1.0.0")
    )