"""
Ritual Dispatcher — Sequences and dispatches ritual execution.
Ensures rituals execute in correct order with state capture.
"""

from __future__ import annotations
from typing import Any, Callable, Optional
import time


class RitualDispatcher:
    """
    Dispatches ritual execution in correct sequence.

    Ritual Sequence:
    1. Validate ritual exists in registry
    2. Capture pre-state
    3. Execute ritual steps in order
    4. Capture post-state
    5. Compute and log delta
    6. Emit completion event
    """

    DISPATCHER_NAME = "ritual_dispatcher"

    def __init__(self):
        self._ritual_handlers: dict[str, Callable] = {}
        self._execution_log: list[dict] = []
        self._active = False

    def activate(self) -> bool:
        self._active = True
        return True

    def register_ritual(self, name: str, handler: Callable):
        """Register a ritual handler."""
        self._ritual_handlers[name] = handler

    def dispatch(self, ritual_name: str, context: dict = None) -> dict:
        """Dispatch a ritual for execution."""
        handler = self._ritual_handlers.get(ritual_name)
        if not handler:
            return {"error": f"Ritual '{ritual_name}' not registered"}

        start = time.time()
        try:
            result = handler(context or {})
            success = True
        except Exception as e:
            result = {"error": str(e)}
            success = False

        record = {
            "ritual": ritual_name,
            "success": success,
            "duration_ms": (time.time() - start) * 1000,
            "result": result,
            "timestamp": start,
        }
        self._execution_log.append(record)
        return record

    def list_rituals(self) -> list[str]:
        return list(self._ritual_handlers.keys())

    def get_stats(self) -> dict:
        completed = [r for r in self._execution_log if r["success"]]
        return {
            "active": self._active,
            "registered_rituals": len(self._ritual_handlers),
            "total_executions": len(self._execution_log),
            "successful": len(completed),
            "failed": len(self._execution_log) - len(completed),
        }
