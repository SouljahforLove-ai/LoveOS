"""
Project Registry — Tracks all LoveOS projects, builds, and public-facing outputs.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import time


class ProjectStatus(Enum):
    CONCEPT = auto()
    DESIGN = auto()
    BUILDING = auto()
    TESTING = auto()
    DEPLOYED = auto()
    ARCHIVED = auto()


@dataclass
class ProjectEntry:
    """A registered project."""
    name: str
    description: str = ""
    status: ProjectStatus = ProjectStatus.CONCEPT
    tags: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    legacy_relevant: bool = False
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


class ProjectRegistry:
    def __init__(self):
        self._projects: dict[str, ProjectEntry] = {}
        self._initialize_core_projects()

    def _initialize_core_projects(self):
        core = [
            ProjectEntry("LoveOS", "Sovereign Microkernel Runtime",
                          ProjectStatus.BUILDING,
                          tags=["core", "kernel", "sovereign"],
                          legacy_relevant=True),
            ProjectEntry("FaithOS", "Christian + Universal faith integration layer",
                          ProjectStatus.BUILDING,
                          tags=["faith", "spiritual", "integration"],
                          dependencies=["LoveOS"],
                          legacy_relevant=True),
            ProjectEntry("SoulJahForLove", "Universe and brand ecosystem",
                          ProjectStatus.BUILDING,
                          tags=["brand", "universe", "creative"],
                          legacy_relevant=True),
            ProjectEntry("LegacyEngine", "Intergenerational knowledge transmission system",
                          ProjectStatus.DESIGN,
                          tags=["legacy", "teaching", "transmission"],
                          dependencies=["LoveOS"],
                          legacy_relevant=True),
            ProjectEntry("MasterBinder", "Canonical reference document for all OS layers",
                          ProjectStatus.BUILDING,
                          tags=["documentation", "reference", "canonical"],
                          dependencies=["LoveOS"],
                          legacy_relevant=True),
        ]
        for p in core:
            self._projects[p.name] = p

    def register(self, project: ProjectEntry):
        self._projects[project.name] = project

    def update_status(self, name: str, status: ProjectStatus) -> bool:
        proj = self._projects.get(name)
        if not proj:
            return False
        proj.status = status
        proj.updated_at = time.time()
        return True

    def get(self, name: str) -> Optional[ProjectEntry]:
        return self._projects.get(name)

    def get_by_status(self, status: ProjectStatus) -> list[ProjectEntry]:
        return [p for p in self._projects.values() if p.status == status]

    def get_legacy_projects(self) -> list[ProjectEntry]:
        return [p for p in self._projects.values() if p.legacy_relevant]

    def get_manifest(self) -> list[dict]:
        return [
            {"name": p.name, "description": p.description,
             "status": p.status.name, "tags": p.tags}
            for p in self._projects.values()
        ]
