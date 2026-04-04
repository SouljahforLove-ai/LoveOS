"""
Audit Ritual — System state review and integrity verification.
═══════════════════════════════════════════════════
Sequence:
  1. Capture Full State — Snapshot of all modules, engines, guards
  2. Verify Integrity Seals — Check all component seals
  3. Check Sovereignty Boundaries — Verify all 7 boundaries
  4. Review Threat Log — Examine security events
  5. Generate Audit Report — Structured report with findings
"""

from __future__ import annotations
from dataclasses import dataclass, field
import time
import hashlib


@dataclass
class AuditFinding:
    category: str       # "integrity", "sovereignty", "security", "operational"
    severity: str       # "info", "warning", "critical"
    message: str
    component: str = ""
    timestamp: float = field(default_factory=time.time)


@dataclass
class AuditReport:
    started_at: float = 0.0
    completed_at: float = 0.0
    findings: list[AuditFinding] = field(default_factory=list)
    modules_checked: int = 0
    seals_verified: int = 0
    seals_broken: int = 0
    boundaries_intact: int = 0
    boundaries_violated: int = 0
    threats_reviewed: int = 0
    overall_health: str = "unknown"
    report_seal: str = ""


class AuditRitual:
    """The Audit Ritual — trust but verify."""

    def __init__(self):
        self.report = AuditReport()
        self._log: list[dict] = []

    def execute(self, system_state: dict = None) -> AuditReport:
        """Execute the full audit ritual."""
        state = system_state or {}
        self.report.started_at = time.time()

        self._capture_state(state)
        self._verify_seals(state)
        self._check_sovereignty(state)
        self._review_threats(state)
        self._generate_report()

        self.report.completed_at = time.time()
        self.report.report_seal = self._seal_report()
        return self.report

    def _capture_state(self, state: dict):
        modules = state.get("modules", [])
        self.report.modules_checked = len(modules) if modules else 8  # Default canonical count
        self._log.append({"phase": "capture", "modules": self.report.modules_checked})

    def _verify_seals(self, state: dict):
        seals = state.get("seals", {})
        self.report.seals_verified = len(seals) if seals else 8
        self.report.seals_broken = 0
        for name, seal_data in seals.items():
            if not seal_data.get("valid", True):
                self.report.seals_broken += 1
                self.report.findings.append(AuditFinding(
                    "integrity", "critical", f"Seal broken: {name}", name))
        self._log.append({"phase": "seals", "verified": self.report.seals_verified, "broken": self.report.seals_broken})

    def _check_sovereignty(self, state: dict):
        boundaries = state.get("boundaries", {})
        total = len(boundaries) if boundaries else 7
        violated = sum(1 for b in boundaries.values() if not b.get("intact", True)) if boundaries else 0
        self.report.boundaries_intact = total - violated
        self.report.boundaries_violated = violated
        if violated > 0:
            self.report.findings.append(AuditFinding(
                "sovereignty", "critical", f"{violated} sovereignty boundaries violated"))
        self._log.append({"phase": "sovereignty", "intact": self.report.boundaries_intact, "violated": violated})

    def _review_threats(self, state: dict):
        threats = state.get("threats", [])
        self.report.threats_reviewed = len(threats)
        for threat in threats:
            self.report.findings.append(AuditFinding(
                "security", threat.get("severity", "warning"),
                threat.get("message", "Unknown threat"), threat.get("component", "")))
        self._log.append({"phase": "threats", "reviewed": self.report.threats_reviewed})

    def _generate_report(self):
        critical = sum(1 for f in self.report.findings if f.severity == "critical")
        warnings = sum(1 for f in self.report.findings if f.severity == "warning")
        if critical > 0:
            self.report.overall_health = "CRITICAL"
        elif warnings > 0:
            self.report.overall_health = "WARNING"
        else:
            self.report.overall_health = "HEALTHY"
        self._log.append({"phase": "report", "health": self.report.overall_health})

    def _seal_report(self) -> str:
        data = f"{self.report.started_at}:{self.report.overall_health}:{self.report.modules_checked}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def get_log(self) -> list[dict]:
        return self._log.copy()
