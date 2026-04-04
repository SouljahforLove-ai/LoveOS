"""
Guardian Pattern
═══════════════════════════════════════════════════
Defines the protective behavioral pattern.
Active at all times — guards never sleep.

The Guardian Pattern governs:
  - How threats are detected and handled
  - Boundary enforcement protocols
  - Escalation procedures
  - Silent operation (no pop-ups)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable
import time


class ThreatResponse(Enum):
    OBSERVE = auto()        # Log and watch
    QUARANTINE = auto()     # Isolate the input
    BLOCK = auto()          # Deny the action
    ESCALATE = auto()       # Raise to sovereignty guard
    HALT = auto()           # Emergency system halt


class GuardianState(Enum):
    VIGILANT = auto()       # Normal watchful state
    ALERT = auto()          # Elevated awareness
    DEFENSIVE = auto()      # Active threat response
    LOCKDOWN = auto()       # Full defensive posture


@dataclass
class ThreatRecord:
    source: str
    threat_type: str
    severity: float         # 0→1
    response: ThreatResponse
    resolved: bool = False
    timestamp: float = field(default_factory=time.time)


class GuardianPattern:
    """
    Behavioral pattern for system protection.
    
    Principles:
    1. Always On — Guards cannot be fully deactivated
    2. Silent Operation — No pop-ups, no interruptions to operator
    3. Proportional Response — Match response to threat level
    4. Sovereignty Priority — Identity and consent are inviolable
    5. Audit Everything — Every action is logged
    """

    SEVERITY_THRESHOLDS = {
        ThreatResponse.OBSERVE: 0.2,
        ThreatResponse.QUARANTINE: 0.4,
        ThreatResponse.BLOCK: 0.6,
        ThreatResponse.ESCALATE: 0.8,
        ThreatResponse.HALT: 0.95,
    }

    def __init__(self):
        self.state = GuardianState.VIGILANT
        self._threats: list[ThreatRecord] = []
        self._escalation_handlers: list[Callable] = []
        self._log: list[dict] = []

    def assess_threat(self, source: str, threat_type: str, severity: float) -> ThreatResponse:
        """Assess a threat and determine the appropriate response."""
        response = ThreatResponse.OBSERVE
        for resp, threshold in sorted(self.SEVERITY_THRESHOLDS.items(), key=lambda x: x[1]):
            if severity >= threshold:
                response = resp

        record = ThreatRecord(source, threat_type, severity, response)
        self._threats.append(record)
        self._log.append({
            "action": "threat_assessed", "source": source,
            "type": threat_type, "severity": severity,
            "response": response.name, "timestamp": time.time(),
        })

        # Update guardian state
        if response in (ThreatResponse.ESCALATE, ThreatResponse.HALT):
            self.state = GuardianState.LOCKDOWN
        elif response in (ThreatResponse.BLOCK, ThreatResponse.QUARANTINE):
            self.state = GuardianState.DEFENSIVE
        elif response == ThreatResponse.OBSERVE and self.state == GuardianState.VIGILANT:
            pass  # Stay vigilant
        else:
            self.state = GuardianState.ALERT

        # Fire escalation
        if response == ThreatResponse.ESCALATE:
            for handler in self._escalation_handlers:
                try:
                    handler(record)
                except Exception:
                    pass

        return response

    def register_escalation_handler(self, handler: Callable):
        self._escalation_handlers.append(handler)

    def get_active_threats(self) -> list[ThreatRecord]:
        return [t for t in self._threats if not t.resolved]

    def resolve_threat(self, index: int) -> bool:
        if 0 <= index < len(self._threats):
            self._threats[index].resolved = True
            # Check if we can de-escalate
            if not self.get_active_threats():
                self.state = GuardianState.VIGILANT
            return True
        return False

    def get_summary(self) -> dict:
        return {
            "state": self.state.name,
            "total_threats": len(self._threats),
            "active_threats": len(self.get_active_threats()),
            "threats_by_response": {
                r.name: sum(1 for t in self._threats if t.response == r)
                for r in ThreatResponse
            },
        }
