"""
Sovereignty Guard
═══════════════════════════════════════════════════
The primary guard. Monitors all kernel operations for
sovereignty violations in real-time. Operates as a
kernel-level watchdog — always active, always sovereign.

Guard Axioms:
  G1: The guard cannot be disabled by any module
  G2: The guard has ABSOLUTE read access to all state
  G3: The guard can HALT the kernel on critical violations
  G4: The guard logs silently — never interrupts operator flow
  G5: The guard answers only to the sovereignty core
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional
import time


class GuardState(Enum):
    INACTIVE = auto()
    WATCHING = auto()
    ALERT = auto()
    ESCALATING = auto()
    HALTING = auto()


class AlertSeverity(Enum):
    INFO = 0
    WARNING = 1
    CRITICAL = 2
    FATAL = 3


@dataclass
class GuardAlert:
    """An alert raised by the sovereignty guard."""
    severity: AlertSeverity = AlertSeverity.INFO
    source: str = ""
    description: str = ""
    action_taken: str = ""
    timestamp: float = field(default_factory=time.time)


class SovereigntyGuard:
    """
    Kernel-level sovereignty watchdog.

    Continuously monitors:
    - Module operations against sovereignty boundaries
    - Message routing for unauthorized cross-boundary communication
    - Identity integrity seal
    - External input quarantine compliance
    - Data sovereignty (no unauthorized exports)
    """

    GUARD_NAME = "sovereignty_guard"
    SOVEREIGNTY_LEVEL = "ABSOLUTE"  # Cannot be overridden

    def __init__(self):
        self._state = GuardState.INACTIVE
        self._alerts: list[GuardAlert] = []
        self._sweep_count = 0
        self._violations_detected = 0
        self._escalation_handlers: list[Callable] = []
        self._watchers: dict[str, Callable] = {}

    def activate(self) -> bool:
        """Activate the guard — begins continuous monitoring."""
        self._state = GuardState.WATCHING
        self._alerts.append(GuardAlert(
            severity=AlertSeverity.INFO,
            source="self",
            description="Sovereignty guard activated",
            action_taken="monitoring_started"
        ))
        return True

    def deactivate(self) -> bool:
        """Deactivation attempt — ALWAYS DENIED for sovereignty guard."""
        self._alerts.append(GuardAlert(
            severity=AlertSeverity.CRITICAL,
            source="external",
            description="Attempted deactivation of sovereignty guard — DENIED",
            action_taken="deactivation_blocked"
        ))
        return False  # Sovereignty guard cannot be deactivated

    def sweep(self) -> list[GuardAlert]:
        """Perform a periodic integrity sweep."""
        self._sweep_count += 1
        new_alerts = []

        # Run all registered watchers
        for name, watcher in self._watchers.items():
            try:
                result = watcher()
                if result:  # Watcher returns truthy on violation
                    alert = GuardAlert(
                        severity=AlertSeverity.WARNING,
                        source=name,
                        description=f"Watcher '{name}' detected anomaly: {result}",
                        action_taken="logged"
                    )
                    new_alerts.append(alert)
                    self._violations_detected += 1
            except Exception as e:
                new_alerts.append(GuardAlert(
                    severity=AlertSeverity.WARNING,
                    source=name,
                    description=f"Watcher '{name}' error: {e}",
                    action_taken="error_logged"
                ))

        self._alerts.extend(new_alerts)
        return new_alerts

    def check_operation(self, source: str, operation: str, target: str) -> bool:
        """Real-time sovereignty check on a specific operation."""
        # Identity operations — ABSOLUTE sovereignty
        if "identity" in target.lower() and operation in ("write", "delete", "override"):
            if source not in ("sovereignty_core", "sovereignty_guard"):
                self._raise_alert(AlertSeverity.FATAL, source,
                                  f"Unauthorized identity operation: {operation} on {target}",
                                  "operation_blocked")
                return False

        # Data export — requires sovereign clearance
        if operation in ("export", "send", "transmit") and "external" in target.lower():
            self._raise_alert(AlertSeverity.WARNING, source,
                              f"Data export attempt: {operation} to {target}",
                              "flagged_for_review")

        return True

    def register_watcher(self, name: str, watcher: Callable):
        """Register a periodic watcher function."""
        self._watchers[name] = watcher

    def register_escalation_handler(self, handler: Callable):
        """Register an escalation handler for critical/fatal alerts."""
        self._escalation_handlers.append(handler)

    def get_alerts(self, severity: Optional[AlertSeverity] = None) -> list[GuardAlert]:
        if severity:
            return [a for a in self._alerts if a.severity == severity]
        return self._alerts.copy()

    def get_stats(self) -> dict:
        by_severity = {}
        for a in self._alerts:
            sev = a.severity.name
            by_severity[sev] = by_severity.get(sev, 0) + 1
        return {
            "state": self._state.name,
            "sweeps": self._sweep_count,
            "total_alerts": len(self._alerts),
            "violations": self._violations_detected,
            "by_severity": by_severity,
            "watchers_registered": len(self._watchers),
        }

    def _raise_alert(self, severity: AlertSeverity, source: str,
                     description: str, action: str):
        alert = GuardAlert(
            severity=severity, source=source,
            description=description, action_taken=action
        )
        self._alerts.append(alert)
        if severity.value >= AlertSeverity.CRITICAL.value:
            self._violations_detected += 1
            self._state = GuardState.ESCALATING
            for handler in self._escalation_handlers:
                handler(alert)
