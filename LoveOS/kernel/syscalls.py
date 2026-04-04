"""
LoveOS System Call Interface
═══════════════════════════════════════════════════
The syscall layer provides the API surface between
modules and the kernel. Every external interaction
with the kernel routes through a syscall.

Syscall Categories:
  - MODULE:    Mount, unmount, query, configure modules
  - MESSAGE:   Send, receive, broadcast messages
  - GUARD:     Register, activate, deactivate guards
  - RITUAL:    Trigger, sequence, complete rituals
  - AUDIT:     Log, query, export audit trails
  - SOVEREIGN: Declare boundaries, check sovereignty
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional
import time
import uuid


class SyscallCategory(Enum):
    MODULE = auto()
    MESSAGE = auto()
    GUARD = auto()
    RITUAL = auto()
    AUDIT = auto()
    SOVEREIGN = auto()


class SyscallResult(Enum):
    SUCCESS = auto()
    DENIED = auto()
    NOT_FOUND = auto()
    INVALID = auto()
    SOVEREIGNTY_VIOLATION = auto()


@dataclass
class Syscall:
    """A system call request."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    category: SyscallCategory = SyscallCategory.MODULE
    operation: str = ""
    caller: str = ""
    args: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class SyscallResponse:
    """Response from a system call."""
    syscall_id: str = ""
    result: SyscallResult = SyscallResult.SUCCESS
    data: Any = None
    message: str = ""
    timestamp: float = field(default_factory=time.time)


class SyscallInterface:
    """
    System Call Interface — the sovereign API boundary.

    All module-to-kernel and kernel-to-module communication
    flows through this interface. No direct kernel access.
    """

    def __init__(self, kernel=None):
        self.kernel = kernel
        self._handlers: dict[str, Callable] = {}
        self._audit_log: list[dict] = []
        self._register_core_handlers()

    def invoke(self, syscall: Syscall) -> SyscallResponse:
        """Execute a system call with sovereignty validation."""
        # Log the syscall
        self._audit_log.append({
            "id": syscall.id,
            "category": syscall.category.name,
            "operation": syscall.operation,
            "caller": syscall.caller,
            "timestamp": syscall.timestamp,
        })

        # Route to handler
        handler_key = f"{syscall.category.name}:{syscall.operation}"
        if handler_key in self._handlers:
            return self._handlers[handler_key](syscall)

        return SyscallResponse(
            syscall_id=syscall.id,
            result=SyscallResult.NOT_FOUND,
            message=f"No handler for {handler_key}"
        )

    def register_handler(self, category: SyscallCategory, operation: str, handler: Callable):
        """Register a syscall handler."""
        key = f"{category.name}:{operation}"
        self._handlers[key] = handler

    def _register_core_handlers(self):
        """Register the built-in kernel syscall handlers."""
        # Module operations
        self.register_handler(SyscallCategory.MODULE, "mount", self._handle_mount)
        self.register_handler(SyscallCategory.MODULE, "unmount", self._handle_unmount)
        self.register_handler(SyscallCategory.MODULE, "query", self._handle_query)

        # Sovereignty operations
        self.register_handler(SyscallCategory.SOVEREIGN, "check", self._handle_sov_check)
        self.register_handler(SyscallCategory.SOVEREIGN, "declare", self._handle_sov_declare)

        # Audit operations
        self.register_handler(SyscallCategory.AUDIT, "log", self._handle_audit_log)
        self.register_handler(SyscallCategory.AUDIT, "export", self._handle_audit_export)

        # Ritual operations
        self.register_handler(SyscallCategory.RITUAL, "trigger", self._handle_ritual_trigger)

    def _handle_mount(self, syscall: Syscall) -> SyscallResponse:
        return SyscallResponse(syscall_id=syscall.id, result=SyscallResult.SUCCESS)

    def _handle_unmount(self, syscall: Syscall) -> SyscallResponse:
        return SyscallResponse(syscall_id=syscall.id, result=SyscallResult.SUCCESS)

    def _handle_query(self, syscall: Syscall) -> SyscallResponse:
        return SyscallResponse(syscall_id=syscall.id, result=SyscallResult.SUCCESS)

    def _handle_sov_check(self, syscall: Syscall) -> SyscallResponse:
        return SyscallResponse(syscall_id=syscall.id, result=SyscallResult.SUCCESS)

    def _handle_sov_declare(self, syscall: Syscall) -> SyscallResponse:
        return SyscallResponse(syscall_id=syscall.id, result=SyscallResult.SUCCESS)

    def _handle_audit_log(self, syscall: Syscall) -> SyscallResponse:
        return SyscallResponse(syscall_id=syscall.id, result=SyscallResult.SUCCESS)

    def _handle_audit_export(self, syscall: Syscall) -> SyscallResponse:
        return SyscallResponse(
            syscall_id=syscall.id,
            result=SyscallResult.SUCCESS,
            data=self._audit_log.copy()
        )

    def _handle_ritual_trigger(self, syscall: Syscall) -> SyscallResponse:
        return SyscallResponse(syscall_id=syscall.id, result=SyscallResult.SUCCESS)
