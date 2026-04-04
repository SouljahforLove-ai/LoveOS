"""
Event Schema — Canonical event definitions for the kernel event system.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any
import uuid
import time


class EventType(Enum):
    # Kernel events
    BOOT = auto()
    SHUTDOWN = auto()
    MODULE_MOUNT = auto()
    MODULE_UNMOUNT = auto()

    # Sovereignty events
    SOVEREIGNTY_CHECK = auto()
    SOVEREIGNTY_VIOLATION = auto()
    BOUNDARY_DECLARED = auto()

    # Processing events
    EMOTIONAL_UPDATE = auto()
    SPIRITUAL_UPDATE = auto()
    FAITH_UPDATE = auto()

    # Ritual events
    RITUAL_START = auto()
    RITUAL_COMPLETE = auto()
    RITUAL_FAILED = auto()

    # Security events
    THREAT_DETECTED = auto()
    THREAT_RESOLVED = auto()
    FILE_QUARANTINED = auto()

    # Legacy events
    LEGACY_CAPTURED = auto()
    LEGACY_TRANSMITTED = auto()
    LEGACY_ARCHIVED = auto()

    # Sorting events
    INPUT_SORTED = auto()
    INPUT_ROUTED = auto()

    # Audit events
    AUDIT_START = auto()
    AUDIT_COMPLETE = auto()


@dataclass
class SystemEvent:
    """A canonical LoveOS system event."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = EventType.BOOT
    source: str = ""
    target: str = ""
    payload: Any = None
    priority: int = 2          # 0=critical, 4=background
    sovereignty_cleared: bool = False
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.event_type.name,
            "source": self.source,
            "target": self.target,
            "priority": self.priority,
            "sovereignty_cleared": self.sovereignty_cleared,
            "timestamp": self.timestamp,
        }
