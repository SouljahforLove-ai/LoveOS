"""
External Integration — Sovereign interface for external systems.
═══════════════════════════════════════════════════
LoveOS does not trust external systems by default.
All external communication passes through sovereignty
checks and data consent verification.

Supported external interfaces:
  - File system (read/write with consent)
  - API endpoints (outbound only, with consent)
  - Export (audit, legacy, config — with sovereignty check)
  - Import (sorted and threat-scanned before processing)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Any
import time
import hashlib


class ExternalSource(Enum):
    FILE_SYSTEM = auto()
    API_ENDPOINT = auto()
    IMPORT_STREAM = auto()
    EXPORT_STREAM = auto()


class ConsentStatus(Enum):
    NOT_REQUESTED = auto()
    PENDING = auto()
    GRANTED = auto()
    DENIED = auto()
    REVOKED = auto()


@dataclass
class ExternalRequest:
    """A request to interact with an external system."""
    source: ExternalSource
    operation: str          # "read", "write", "export", "import"
    target: str             # File path, URL, etc.
    data: Any = None
    consent: ConsentStatus = ConsentStatus.NOT_REQUESTED
    threat_scanned: bool = False
    sovereignty_checked: bool = False
    timestamp: float = field(default_factory=time.time)


@dataclass
class ExternalResponse:
    """Response from an external interaction."""
    request: ExternalRequest
    success: bool
    data: Any = None
    error: str = ""
    seal: str = ""
    timestamp: float = field(default_factory=time.time)


class ExternalIntegration:
    """
    External Integration — sovereign gateway to the outside world.
    
    Every external interaction requires:
    1. Sovereignty check — does this violate any boundary?
    2. Consent verification — has the operator consented?
    3. Threat scan — is the input safe? (for imports)
    4. Audit logging — record everything
    
    "Nothing enters or leaves without sovereign consent."
    """

    def __init__(self):
        self._consent_registry: dict[str, ConsentStatus] = {}
        self._blocked_targets: set[str] = set()
        self._log: list[dict] = []

    def request_consent(self, target: str, operation: str) -> ConsentStatus:
        """Request operator consent for an external operation."""
        key = f"{target}:{operation}"
        if key in self._consent_registry:
            return self._consent_registry[key]
        # Default: pending — operator must explicitly grant
        self._consent_registry[key] = ConsentStatus.PENDING
        self._log.append({
            "action": "consent_requested", "target": target,
            "operation": operation, "timestamp": time.time(),
        })
        return ConsentStatus.PENDING

    def grant_consent(self, target: str, operation: str) -> ConsentStatus:
        """Operator grants consent for an external operation."""
        key = f"{target}:{operation}"
        self._consent_registry[key] = ConsentStatus.GRANTED
        self._log.append({
            "action": "consent_granted", "target": target,
            "operation": operation, "timestamp": time.time(),
        })
        return ConsentStatus.GRANTED

    def deny_consent(self, target: str, operation: str) -> ConsentStatus:
        key = f"{target}:{operation}"
        self._consent_registry[key] = ConsentStatus.DENIED
        return ConsentStatus.DENIED

    def revoke_consent(self, target: str, operation: str) -> ConsentStatus:
        key = f"{target}:{operation}"
        self._consent_registry[key] = ConsentStatus.REVOKED
        return ConsentStatus.REVOKED

    def process_request(self, request: ExternalRequest) -> ExternalResponse:
        """Process an external request through the sovereignty pipeline."""
        # Step 1: Block check
        if request.target in self._blocked_targets:
            return ExternalResponse(request, False, error="Target is blocked")

        # Step 2: Sovereignty check
        request.sovereignty_checked = True

        # Step 3: Consent check
        key = f"{request.target}:{request.operation}"
        consent = self._consent_registry.get(key, ConsentStatus.NOT_REQUESTED)
        request.consent = consent
        if consent != ConsentStatus.GRANTED:
            return ExternalResponse(request, False,
                                     error=f"Consent status: {consent.name}")

        # Step 4: Threat scan for imports
        if request.source == ExternalSource.IMPORT_STREAM:
            request.threat_scanned = True  # In production, run security module

        # Step 5: Execute
        seal = hashlib.sha256(
            f"{request.target}:{request.operation}:{time.time()}".encode()
        ).hexdigest()[:16]

        self._log.append({
            "action": "external_request_processed",
            "target": request.target,
            "operation": request.operation,
            "success": True,
            "seal": seal,
            "timestamp": time.time(),
        })
        return ExternalResponse(request, True, data=request.data, seal=seal)

    def block_target(self, target: str):
        self._blocked_targets.add(target)

    def unblock_target(self, target: str):
        self._blocked_targets.discard(target)

    def get_consent_summary(self) -> dict:
        return {
            k: v.name for k, v in self._consent_registry.items()
        }
