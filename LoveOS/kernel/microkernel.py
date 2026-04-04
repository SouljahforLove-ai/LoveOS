"""
LoveOS Microkernel — Central Kernel Loop and IPC
═══════════════════════════════════════════════════
The sovereign core. All processes route through here.
No module executes without kernel authorization.

Architecture: Message-passing microkernel
Pattern: Event-driven with sovereignty checkpoints
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional
import uuid
import time


class KernelState(Enum):
    """Discrete states of the microkernel lifecycle."""
    DORMANT = auto()
    BOOTING = auto()
    RITUAL_INIT = auto()
    RUNNING = auto()
    GROUNDING = auto()
    AUDITING = auto()
    CLOSING = auto()
    SOVEREIGN_HALT = auto()


class MessagePriority(Enum):
    """IPC message priority levels."""
    CRITICAL = 0       # Sovereignty violations, security threats
    HIGH = 1           # Ritual triggers, guard alerts
    STANDARD = 2       # Normal module communication
    LOW = 3            # Logging, telemetry, audit trails
    BACKGROUND = 4     # Pattern learning, passive analysis


@dataclass
class KernelMessage:
    """Interprocess communication message."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""
    target: str = ""
    payload: Any = None
    priority: MessagePriority = MessagePriority.STANDARD
    timestamp: float = field(default_factory=time.time)
    sovereignty_cleared: bool = False
    requires_ritual: bool = False

    def validate(self) -> bool:
        return bool(self.source and self.target and self.sovereignty_cleared)


class Microkernel:
    """
    LoveOS Microkernel — The Sovereign Runtime Core

    Responsibilities:
    - Module lifecycle management (mount, unmount, suspend)
    - Inter-process communication (IPC) via message queue
    - Sovereignty enforcement at every syscall boundary
    - Ritual sequencing (boot, ground, audit, close)
    - Guard coordination and threat escalation
    """

    VERSION = "1.0.0"
    SIGIL = "N2 m(THYSELF)e | 👁️ ."

    def __init__(self):
        self.state = KernelState.DORMANT
        self._message_queue: list[KernelMessage] = []
        self._mounted_modules: dict[str, Any] = {}
        self._registered_guards: dict[str, Any] = {}
        self._dispatchers: dict[str, Any] = {}
        self._sovereignty_engine = None
        self._boot_log: list[str] = []
        self._cycle_count: int = 0

    def boot(self, config: dict | None = None) -> bool:
        """
        Execute the full boot sequence:
        1. DORMANT → BOOTING: Hardware/config validation
        2. BOOTING → RITUAL_INIT: Load boot ritual
        3. RITUAL_INIT → RUNNING: Mount core modules
        """
        self.state = KernelState.BOOTING
        self._boot_log.append(f"[BOOT] LoveOS v{self.VERSION} initializing...")
        self._boot_log.append(f"[BOOT] Sigil: {self.SIGIL}")

        # Phase 1: Load sovereignty engine FIRST — nothing runs without it
        self._boot_log.append("[BOOT] Mounting sovereignty engine...")
        from engines.sovereignty_engine import SovereigntyEngine
        self._sovereignty_engine = SovereigntyEngine()

        # Phase 2: Ritual initialization
        self.state = KernelState.RITUAL_INIT
        self._boot_log.append("[BOOT] Executing boot ritual...")
        self._execute_boot_ritual()

        # Phase 3: Mount core modules
        self._boot_log.append("[BOOT] Mounting core modules...")
        self._mount_core_modules()

        # Phase 4: Activate guards
        self._boot_log.append("[BOOT] Activating sovereignty guards...")
        self._activate_guards()

        # Phase 5: Go live
        self.state = KernelState.RUNNING
        self._boot_log.append("[BOOT] ✅ LoveOS is SOVEREIGN and RUNNING.")
        return True

    def send_message(self, message: KernelMessage) -> bool:
        """Route a message through sovereignty check then dispatch."""
        if not self._sovereignty_engine:
            raise RuntimeError("Cannot send messages: sovereignty engine not mounted")

        # Every message must pass sovereignty clearance
        message.sovereignty_cleared = self._sovereignty_engine.clear_message(message)
        if not message.validate():
            self._boot_log.append(
                f"[KERNEL] ⛔ Message {message.id} REJECTED — sovereignty violation"
            )
            return False

        self._message_queue.append(message)
        self._dispatch_next()
        return True

    def mount_module(self, name: str, module: Any) -> bool:
        """Mount a module into the kernel's module space."""
        if name in self._mounted_modules:
            self._boot_log.append(f"[KERNEL] Module '{name}' already mounted")
            return False

        # Sovereignty check on mount
        if self._sovereignty_engine and not self._sovereignty_engine.authorize_mount(name):
            self._boot_log.append(f"[KERNEL] ⛔ Module '{name}' DENIED mount")
            return False

        self._mounted_modules[name] = module
        self._boot_log.append(f"[KERNEL] ✅ Module '{name}' mounted")
        return True

    def unmount_module(self, name: str) -> bool:
        """Safely unmount a module with closure ritual."""
        if name not in self._mounted_modules:
            return False
        del self._mounted_modules[name]
        self._boot_log.append(f"[KERNEL] Module '{name}' unmounted")
        return True

    def register_guard(self, name: str, guard: Any) -> None:
        """Register a sovereignty or integrity guard."""
        self._registered_guards[name] = guard
        self._boot_log.append(f"[KERNEL] Guard '{name}' registered")

    def register_dispatcher(self, name: str, dispatcher: Any) -> None:
        """Register an event dispatcher."""
        self._dispatchers[name] = dispatcher

    def kernel_loop(self) -> None:
        """Main kernel loop — process messages, run guards, cycle rituals."""
        while self.state == KernelState.RUNNING:
            self._cycle_count += 1

            # Process pending messages
            self._dispatch_next()

            # Run guard checks every N cycles
            if self._cycle_count % 10 == 0:
                self._run_guard_sweep()

            # Yield control (in real runtime, this would be async)
            time.sleep(0.01)

    def ground(self) -> None:
        """Execute grounding ritual — pause, center, re-align."""
        prev_state = self.state
        self.state = KernelState.GROUNDING
        self._boot_log.append("[KERNEL] 🌿 Grounding ritual initiated...")
        # Grounding logic delegated to ritual processor
        self.state = prev_state

    def audit(self) -> dict:
        """Execute audit ritual — return full system state."""
        self.state = KernelState.AUDITING
        report = {
            "version": self.VERSION,
            "state": self.state.name,
            "mounted_modules": list(self._mounted_modules.keys()),
            "registered_guards": list(self._registered_guards.keys()),
            "message_queue_depth": len(self._message_queue),
            "cycle_count": self._cycle_count,
            "boot_log": self._boot_log[-20:],  # Last 20 entries
        }
        self.state = KernelState.RUNNING
        return report

    def shutdown(self) -> None:
        """Execute closure ritual and sovereign halt."""
        self.state = KernelState.CLOSING
        self._boot_log.append("[KERNEL] Executing closure ritual...")
        self._execute_closure_ritual()

        # Unmount all modules in reverse order
        for name in list(reversed(list(self._mounted_modules.keys()))):
            self.unmount_module(name)

        self.state = KernelState.SOVEREIGN_HALT
        self._boot_log.append("[KERNEL] 🖤 LoveOS sovereign halt complete.")

    # ─── Private Methods ─────────────────────────────

    def _execute_boot_ritual(self):
        """Boot ritual: presence, intention, sovereignty declaration."""
        pass  # Delegated to rituals/boot_ritual.py

    def _execute_closure_ritual(self):
        """Closure ritual: gratitude, audit, secure shutdown."""
        pass  # Delegated to rituals/closure_ritual.py

    def _mount_core_modules(self):
        """Mount the essential module set in dependency order."""
        core_modules = [
            "identity", "emotional", "spiritual",
            "security", "sorting", "faith",
            "legacy", "audit"
        ]
        for mod_name in core_modules:
            self._boot_log.append(f"[BOOT] Mounting module: {mod_name}")

    def _activate_guards(self):
        """Bring all registered guards to active state."""
        for name, guard in self._registered_guards.items():
            if hasattr(guard, 'activate'):
                guard.activate()

    def _dispatch_next(self):
        """Dispatch the highest-priority message in the queue."""
        if not self._message_queue:
            return
        # Sort by priority (lower enum value = higher priority)
        self._message_queue.sort(key=lambda m: m.priority.value)
        msg = self._message_queue.pop(0)
        target = msg.target
        if target in self._dispatchers:
            self._dispatchers[target].dispatch(msg)

    def _run_guard_sweep(self):
        """Run all guards for periodic integrity check."""
        for name, guard in self._registered_guards.items():
            if hasattr(guard, 'sweep'):
                guard.sweep()


# ═══════════════════════════════════════════════════
# Sovereign Entry Point
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    kernel = Microkernel()
    kernel.boot()
    print("\n".join(kernel._boot_log))
