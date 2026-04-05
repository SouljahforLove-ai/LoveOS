"""
LoveOS Microkernel — Sovereign Runtime Core
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any
import uuid
import time

# Breathing + Emotion syscalls
from kernel.syscalls import syscall_breathe, syscall_emotion_tag


class KernelState(Enum):
    DORMANT = auto()
    BOOTING = auto()
    RITUAL_INIT = auto()
    RUNNING = auto()
    GROUNDING = auto()
    AUDITING = auto()
    CLOSING = auto()
    SOVEREIGN_HALT = auto()


class MessagePriority(Enum):
    CRITICAL = 0
    HIGH = 1
    STANDARD = 2
    LOW = 3
    BACKGROUND = 4


@dataclass
class KernelMessage:
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

    # ───────────────────────────────────────────────
    # BREATHING + EMOTIONS
    # ───────────────────────────────────────────────
    def breathe(self):
        return syscall_breathe()

    def tag_emotion(self, text: str):
        return syscall_emotion_tag(text)

    def emotional_state(self):
        return syscall_emotion_get_state()

    # ───────────────────────────────────────────────
    # BOOT SEQUENCE
    # ───────────────────────────────────────────────
    def boot(self, config: dict | None = None) -> bool:
        self.state = KernelState.BOOTING
        self._boot_log.append(f"[BOOT] LoveOS v{self.VERSION} initializing...")
        self._boot_log.append(f"[BOOT] Sigil: {self.SIGIL}")

        # Sovereignty engine
        from engines.sovereignty_engine import SovereigntyEngine
        self._sovereignty_engine = SovereigntyEngine()

        # Ritual init
        self.state = KernelState.RITUAL_INIT
        self._boot_log.append("[BOOT] Executing boot ritual...")
        self._execute_boot_ritual()

        # Mount core modules
        self._boot_log.append("[BOOT] Mounting core modules...")
        self._mount_core_modules()

        # Activate guards
        self._boot_log.append("[BOOT] Activating sovereignty guards...")
        self._activate_guards()

        # Running
        self.state = KernelState.RUNNING
        self._boot_log.append("[BOOT] ✅ LoveOS is SOVEREIGN and RUNNING.")
        return True

    # ───────────────────────────────────────────────
    # MESSAGE PASSING
    # ───────────────────────────────────────────────
    def send_message(self, message: KernelMessage) -> bool:
        if not self._sovereignty_engine:
            raise RuntimeError("Cannot send messages: sovereignty engine not mounted")

        message.sovereignty_cleared = self._sovereignty_engine.clear_message(message)
        if not message.validate():
            self._boot_log.append(
                f"[KERNEL] ⛔ Message {message.id} REJECTED — sovereignty violation"
            )
            return False

        self._message_queue.append(message)
        self._dispatch_next()
        return True

    # ───────────────────────────────────────────────
    # MODULE MANAGEMENT
    # ───────────────────────────────────────────────
    def mount_module(self, name: str, module: Any) -> bool:
        if name in self._mounted_modules:
            return False

        if self._sovereignty_engine and not self._sovereignty_engine.authorize_mount(name):
            return False

        self._mounted_modules[name] = module
        return True

    def unmount_module(self, name: str) -> bool:
        if name not in self._mounted_modules:
            return False
        del self._mounted_modules[name]
        return True

    # ───────────────────────────────────────────────
    # GUARDS
    # ───────────────────────────────────────────────
    def register_guard(self, name: str, guard: Any) -> None:
        self._registered_guards[name] = guard

    def _activate_guards(self):
        for name, guard in self._registered_guards.items():
            if hasattr(guard, 'activate'):
                guard.activate()

    # ───────────────────────────────────────────────
    # RITUALS
    # ───────────────────────────────────────────────
    def ground(self) -> None:
        prev_state = self.state
        self.state = KernelState.GROUNDING
        self.state = prev_state

    def audit(self) -> dict:
        self.state = KernelState.AUDITING
        report = {
            "version": self.VERSION,
            "state": self.state.name,
            "mounted_modules": list(self._mounted_modules.keys()),
            "registered_guards": list(self._registered_guards.keys()),
            "message_queue_depth": len(self._message_queue),
            "cycle_count": self._cycle_count,
            "boot_log": self._boot_log[-20:],
        }
        self.state = KernelState.RUNNING
        return report

    def shutdown(self) -> None:
        self.state = KernelState.CLOSING
        self._execute_closure_ritual()
        for name in list(reversed(list(self._mounted_modules.keys()))):
            self.unmount_module(name)
        self.state = KernelState.SOVEREIGN_HALT

    # ───────────────────────────────────────────────
    # INTERNALS
    # ───────────────────────────────────────────────
    def _execute_boot_ritual(self):
        pass

    def _execute_closure_ritual(self):
        pass

    def _mount_core_modules(self):
        core_modules = [
            "identity", "emotional", "spiritual",
            "security", "sorting", "faith",
            "legacy", "audit"
        ]
        for mod_name in core_modules:
            self._boot_log.append(f"[BOOT] Mounting module: {mod_name}")

    def _dispatch_next(self):
        if not self._message_queue:
            return
        self._message_queue.sort(key=lambda m: m.priority.value)
        msg = self._message_queue.pop(0)
        target = msg.target
        if target in self._dispatchers:
            self._dispatchers[target].dispatch(msg)


# Entry point
if __name__ == "__main__":
    kernel = Microkernel()
    kernel.boot()
    print("\n".join(kernel._boot_log))
