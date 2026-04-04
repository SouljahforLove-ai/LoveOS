"""
Module Registry
═══════════════════════════════════════════════════
Central registry of all mountable modules. Tracks module
metadata, dependencies, mount state, and version info.

The registry is the kernel's source of truth for what
modules exist and their operational status.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional
import time


class ModuleState(Enum):
    REGISTERED = auto()
    MOUNTING = auto()
    MOUNTED = auto()
    SUSPENDED = auto()
    UNMOUNTING = auto()
    UNMOUNTED = auto()
    FAILED = auto()


@dataclass
class ModuleEntry:
    """Registry entry for a module."""
    name: str
    version: str = "1.0.0"
    sovereignty_level: str = "GUARDED"
    state: ModuleState = ModuleState.REGISTERED
    dependencies: list[str] = field(default_factory=list)
    mount_order: int = 0
    instance: Any = None
    mounted_at: float = 0.0
    metadata: dict = field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        return self.state == ModuleState.MOUNTED


class ModuleRegistry:
    """
    Central module registry — tracks all modules in the LoveOS ecosystem.

    Operations:
    - Register: Add a module definition to the registry
    - Mount: Instantiate and activate a module
    - Unmount: Deactivate and clean up a module
    - Query: Look up module state and metadata
    - Validate: Check dependency chains
    """

    # Canonical module manifest — all modules in mount order
    CANONICAL_MODULES = [
        ModuleEntry(name="identity", sovereignty_level="ABSOLUTE", mount_order=0,
                    dependencies=[], metadata={"description": "Operator identity resolution"}),
        ModuleEntry(name="emotional", sovereignty_level="PROTECTED", mount_order=1,
                    dependencies=["identity"], metadata={"description": "Emotional state processing"}),
        ModuleEntry(name="spiritual", sovereignty_level="PROTECTED", mount_order=2,
                    dependencies=["identity", "emotional"],
                    metadata={"description": "Spiritual alignment engine"}),
        ModuleEntry(name="security", sovereignty_level="PROTECTED", mount_order=3,
                    dependencies=["identity"],
                    metadata={"description": "Threat detection and boundary enforcement"}),
        ModuleEntry(name="sorting", sovereignty_level="GUARDED", mount_order=4,
                    dependencies=["identity", "security"],
                    metadata={"description": "Universal sorting intelligence"}),
        ModuleEntry(name="faith", sovereignty_level="PROTECTED", mount_order=5,
                    dependencies=["identity", "spiritual"],
                    metadata={"description": "Faith OS integration layer"}),
        ModuleEntry(name="legacy", sovereignty_level="PROTECTED", mount_order=6,
                    dependencies=["identity"],
                    metadata={"description": "Legacy engine and transmission"}),
        ModuleEntry(name="audit", sovereignty_level="PROTECTED", mount_order=7,
                    dependencies=["identity", "security"],
                    metadata={"description": "Audit trail and compliance"}),
    ]

    def __init__(self):
        self._registry: dict[str, ModuleEntry] = {}
        self._mount_history: list[dict] = []
        self._initialize_canonical()

    def _initialize_canonical(self):
        """Load the canonical module manifest."""
        for entry in self.CANONICAL_MODULES:
            self._registry[entry.name] = ModuleEntry(
                name=entry.name,
                sovereignty_level=entry.sovereignty_level,
                mount_order=entry.mount_order,
                dependencies=entry.dependencies.copy(),
                metadata=entry.metadata.copy(),
            )

    def register(self, name: str, sovereignty_level: str = "GUARDED",
                 dependencies: list[str] = None, metadata: dict = None) -> ModuleEntry:
        """Register a new module."""
        entry = ModuleEntry(
            name=name, sovereignty_level=sovereignty_level,
            dependencies=dependencies or [], metadata=metadata or {},
            mount_order=len(self._registry),
        )
        self._registry[name] = entry
        return entry

    def get(self, name: str) -> Optional[ModuleEntry]:
        """Get a module entry by name."""
        return self._registry.get(name)

    def mount(self, name: str, instance: Any) -> bool:
        """Record a module as mounted."""
        entry = self._registry.get(name)
        if not entry:
            return False

        # Validate dependencies are mounted
        for dep in entry.dependencies:
            dep_entry = self._registry.get(dep)
            if not dep_entry or not dep_entry.is_active:
                return False  # Dependency not mounted

        entry.state = ModuleState.MOUNTED
        entry.instance = instance
        entry.mounted_at = time.time()
        self._mount_history.append({"name": name, "action": "mount", "timestamp": time.time()})
        return True

    def unmount(self, name: str) -> bool:
        """Record a module as unmounted."""
        entry = self._registry.get(name)
        if not entry:
            return False
        entry.state = ModuleState.UNMOUNTED
        entry.instance = None
        self._mount_history.append({"name": name, "action": "unmount", "timestamp": time.time()})
        return True

    def get_mount_order(self) -> list[str]:
        """Return modules in correct mount order."""
        entries = sorted(self._registry.values(), key=lambda e: e.mount_order)
        return [e.name for e in entries]

    def get_mounted(self) -> list[str]:
        """Return names of all currently mounted modules."""
        return [name for name, entry in self._registry.items() if entry.is_active]

    def validate_dependencies(self) -> dict[str, list[str]]:
        """Validate all dependency chains. Returns {module: [missing_deps]}."""
        issues = {}
        for name, entry in self._registry.items():
            missing = [d for d in entry.dependencies if d not in self._registry]
            if missing:
                issues[name] = missing
        return issues

    def get_manifest(self) -> list[dict]:
        """Export the full module manifest."""
        return [
            {
                "name": e.name, "version": e.version,
                "sovereignty_level": e.sovereignty_level,
                "state": e.state.name, "mount_order": e.mount_order,
                "dependencies": e.dependencies, "metadata": e.metadata,
            }
            for e in sorted(self._registry.values(), key=lambda x: x.mount_order)
        ]
