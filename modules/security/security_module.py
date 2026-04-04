"""
Security Module
═══════════════════════════════════════════════════
Threat detection, dangerous file logging, boundary enforcement,
and external input quarantine. Operates silently — no pop-ups,
no interruptions. Threats are logged and escalated, never blocked
without sovereignty authorization.

Threat Categories:
  - FILE_THREAT:      Dangerous file detected
  - INPUT_INJECTION:  Attempted prompt/input injection
  - BOUNDARY_PROBE:   External entity testing boundaries
  - DATA_EXFIL:       Unauthorized data movement
  - IDENTITY_SPOOF:   Identity tampering attempt
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional
import hashlib
import time
import re


class ThreatLevel(Enum):
    INFO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class ThreatCategory(Enum):
    FILE_THREAT = auto()
    INPUT_INJECTION = auto()
    BOUNDARY_PROBE = auto()
    DATA_EXFIL = auto()
    IDENTITY_SPOOF = auto()
    UNKNOWN = auto()


@dataclass
class ThreatRecord:
    """Record of a detected threat."""
    id: str = ""
    category: ThreatCategory = ThreatCategory.UNKNOWN
    level: ThreatLevel = ThreatLevel.INFO
    source: str = ""
    description: str = ""
    payload_hash: str = ""
    quarantined: bool = False
    resolved: bool = False
    timestamp: float = field(default_factory=time.time)


class SecurityModule:
    """
    Silent security processing — detect, log, escalate.
    Never interrupts operator flow. Dangerous files are
    quarantined and logged, not deleted or blocked without consent.
    """

    MODULE_NAME = "security"
    SOVEREIGNTY_LEVEL = "PROTECTED"

    # Dangerous file extensions
    DANGEROUS_EXTENSIONS = {
        ".exe", ".bat", ".cmd", ".vbs", ".js", ".ps1", ".scr",
        ".pif", ".msi", ".dll", ".sys", ".drv", ".com",
    }

    # Injection patterns
    INJECTION_PATTERNS = [
        r"(?i)(drop\s+table|delete\s+from|insert\s+into)",
        r"(?i)(eval\s*\(|exec\s*\(|system\s*\()",
        r"(?i)(<script|javascript:|on\w+\s*=)",
        r"(?i)(override|bypass|ignore\s+previous)",
    ]

    def __init__(self):
        self._active = False
        self._threat_log: list[ThreatRecord] = []
        self._quarantine: dict[str, Any] = {}
        self._scan_count = 0

    def mount(self) -> bool:
        self._active = True
        return True

    def unmount(self) -> bool:
        self._active = False
        return True

    def scan_file(self, filename: str, content_hash: str = "") -> ThreatRecord:
        """Scan a file for threats. Silent logging."""
        self._scan_count += 1
        record = ThreatRecord(
            id=f"threat-{self._scan_count:06d}",
            source=filename,
        )

        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext in self.DANGEROUS_EXTENSIONS:
            record.category = ThreatCategory.FILE_THREAT
            record.level = ThreatLevel.HIGH
            record.description = f"Dangerous file extension: {ext}"
            record.quarantined = True
            self._quarantine[record.id] = {"filename": filename, "hash": content_hash}

        self._threat_log.append(record)
        return record

    def scan_input(self, text: str) -> ThreatRecord:
        """Scan text input for injection attempts."""
        self._scan_count += 1
        record = ThreatRecord(
            id=f"threat-{self._scan_count:06d}",
            source="input_scan",
            payload_hash=hashlib.sha256(text.encode()).hexdigest()[:16],
        )

        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, text):
                record.category = ThreatCategory.INPUT_INJECTION
                record.level = ThreatLevel.HIGH
                record.description = f"Injection pattern detected"
                record.quarantined = True
                break

        self._threat_log.append(record)
        return record

    def get_threat_log(self) -> list[ThreatRecord]:
        return self._threat_log.copy()

    def get_quarantine(self) -> dict:
        return self._quarantine.copy()

    def get_stats(self) -> dict:
        by_level = {}
        for t in self._threat_log:
            lvl = t.level.name
            by_level[lvl] = by_level.get(lvl, 0) + 1
        return {
            "total_scans": self._scan_count,
            "threats_detected": len([t for t in self._threat_log if t.level.value > 0]),
            "quarantined": len(self._quarantine),
            "by_level": by_level,
        }
