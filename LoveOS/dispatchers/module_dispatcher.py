"""
Module Dispatcher — Routes operations to specific mounted modules.
"""

from __future__ import annotations
from typing import Any, Optional


class ModuleDispatcher:
    """
    Routes inter-module communication and operation requests.

    Maintains a live registry of mounted modules and their
    interfaces. Provides the IPC layer between modules.
    """

    DISPATCHER_NAME = "module_dispatcher"

    def __init__(self):
        self._modules: dict[str, Any] = {}
        self._route_log: list[dict] = []
        self._active = False

    def activate(self) -> bool:
        self._active = True
        return True

    def register_module(self, name: str, module: Any):
        """Register a module for dispatch routing."""
        self._modules[name] = module

    def unregister_module(self, name: str):
        """Remove a module from dispatch routing."""
        self._modules.pop(name, None)

    def dispatch(self, target_module: str, operation: str, payload: Any = None) -> Any:
        """Dispatch an operation to a specific module."""
        module = self._modules.get(target_module)
        if not module:
            self._route_log.append({
                "target": target_module, "operation": operation,
                "result": "module_not_found",
            })
            return None

        handler = getattr(module, operation, None)
        if not handler or not callable(handler):
            self._route_log.append({
                "target": target_module, "operation": operation,
                "result": "operation_not_found",
            })
            return None

        result = handler(payload) if payload else handler()
        self._route_log.append({
            "target": target_module, "operation": operation,
            "result": "success",
        })
        return result

    def broadcast(self, operation: str, payload: Any = None) -> dict:
        """Broadcast an operation to all mounted modules."""
        results = {}
        for name, module in self._modules.items():
            handler = getattr(module, operation, None)
            if handler and callable(handler):
                try:
                    results[name] = handler(payload) if payload else handler()
                except Exception as e:
                    results[name] = {"error": str(e)}
        return results

    def list_modules(self) -> list[str]:
        return list(self._modules.keys())

    def get_stats(self) -> dict:
        return {
            "active": self._active,
            "modules_registered": len(self._modules),
            "module_list": list(self._modules.keys()),
            "operations_routed": len(self._route_log),
        }
