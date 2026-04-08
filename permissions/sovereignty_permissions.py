"""
Sovereignty Permissions — Immutable permission layer for sovereignty operations.
═══════════════════════════════════════════════════
These permissions CANNOT be modified at runtime.
They are the constitutional layer of LoveOS.

Axioms:
  1. Identity is sovereign — no external entity modifies it
  2. Consent is mandatory — no action without operator consent
  3. Dignity is inviolable — no degradation of operator worth
  4. Boundaries are absolute — no boundary can be removed
  5. Data is sovereign — no data leaves without consent
  6. Sovereignty cannot be delegated — no proxy sovereignty
  7. Audit is immutable — no erasure of history
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import FrozenSet
import hashlib


@dataclass(frozen=True)
class SovereigntyPermission:
    """An immutable sovereignty permission."""
    name: str
    description: str
    can_override: bool      # Always False for sovereignty
    can_delegate: bool      # Always False for sovereignty
    can_disable: bool       # Always False for sovereignty
    constitutional: bool    # Always True for sovereignty


# ═══════════════════════════════════════════════════
# The Seven Constitutional Permissions
# ═══════════════════════════════════════════════════

IDENTITY_SOVEREIGNTY = SovereigntyPermission(
    name="identity_sovereignty",
    description="The operator's identity is sovereign and immutable without sovereign consent.",
    can_override=False, can_delegate=False, can_disable=False, constitutional=True,
)

CONSENT_SOVEREIGNTY = SovereigntyPermission(
    name="consent_sovereignty",
    description="No system action proceeds without operator consent — explicit or standing.",
    can_override=False, can_delegate=False, can_disable=False, constitutional=True,
)

DIGNITY_SOVEREIGNTY = SovereigntyPermission(
    name="dignity_sovereignty",
    description="The operator's dignity is inviolable. No system behavior degrades worth.",
    can_override=False, can_delegate=False, can_disable=False, constitutional=True,
)

BOUNDARY_SOVEREIGNTY = SovereigntyPermission(
    name="boundary_sovereignty",
    description="No system boundary can be removed, only strengthened.",
    can_override=False, can_delegate=False, can_disable=False, constitutional=True,
)

DATA_SOVEREIGNTY = SovereigntyPermission(
    name="data_sovereignty",
    description="No operator data leaves the system without explicit sovereign consent.",
    can_override=False, can_delegate=False, can_disable=False, constitutional=True,
)

DELEGATION_PROHIBITION = SovereigntyPermission(
    name="delegation_prohibition",
    description="Sovereignty cannot be delegated. No proxy, no agent, no automation overrides sovereignty.",
    can_override=False, can_delegate=False, can_disable=False, constitutional=True,
)

AUDIT_IMMUTABILITY = SovereigntyPermission(
    name="audit_immutability",
    description="The audit trail is append-only and immutable. No erasure of system history.",
    can_override=False, can_delegate=False, can_disable=False, constitutional=True,
)


# ═══════════════════════════════════════════════════
# Constitutional Registry
# ═══════════════════════════════════════════════════

CONSTITUTIONAL_PERMISSIONS: FrozenSet[SovereigntyPermission] = frozenset({
    IDENTITY_SOVEREIGNTY,
    CONSENT_SOVEREIGNTY,
    DIGNITY_SOVEREIGNTY,
    BOUNDARY_SOVEREIGNTY,
    DATA_SOVEREIGNTY,
    DELEGATION_PROHIBITION,
    AUDIT_IMMUTABILITY,
})


def verify_constitutional_integrity() -> dict:
    """Verify all constitutional permissions are intact and unmodified."""
    results = {}
    for perm in CONSTITUTIONAL_PERMISSIONS:
        intact = (
            perm.can_override is False and
            perm.can_delegate is False and
            perm.can_disable is False and
            perm.constitutional is True
        )
        results[perm.name] = {"intact": intact, "description": perm.description}
    all_intact = all(r["intact"] for r in results.values())
    seal = hashlib.sha256(
        "|".join(sorted(p.name for p in CONSTITUTIONAL_PERMISSIONS)).encode()
    ).hexdigest()[:16]
    return {"all_intact": all_intact, "permissions": results, "seal": seal}


def check_sovereignty_violation(action: str) -> bool:
    """Check if an action would violate any sovereignty permission.
    Returns True if the action is a violation."""
    violation_keywords = {
        "override_identity", "bypass_consent", "degrade_dignity",
        "remove_boundary", "export_data_unconsented",
        "delegate_sovereignty", "erase_audit",
    }
    return action.lower().replace(" ", "_") in violation_keywords
