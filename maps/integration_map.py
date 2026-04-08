"""
Integration Map — Maps connections between all engines, modules, and layers.
Defines how data flows through the LoveOS system.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class IntegrationLink:
    """A directional link between two system components."""
    source: str
    target: str
    link_type: str  # "data_flow", "event", "dependency", "sovereignty"
    description: str = ""
    bidirectional: bool = False


class IntegrationMap:
    """
    Maps all inter-component connections in LoveOS.
    """

    def __init__(self):
        self._links: list[IntegrationLink] = []
        self._initialize()

    def _initialize(self):
        self._links = [
            # Kernel → Engines
            IntegrationLink("kernel", "sovereignty_engine", "dependency",
                            "Kernel depends on sovereignty engine for all clearances"),
            IntegrationLink("kernel", "sorting_engine", "data_flow",
                            "All inputs route through sorting before module dispatch"),

            # Sovereignty flows
            IntegrationLink("sovereignty_engine", "sovereignty_guard", "event",
                            "Engine feeds violations to guard", bidirectional=True),
            IntegrationLink("sovereignty_engine", "all_modules", "sovereignty",
                            "Every module mount requires sovereignty clearance"),

            # Sorting → Engine routing
            IntegrationLink("sorting_engine", "emotional_engine", "data_flow",
                            "SIGNAL category inputs route to emotional engine"),
            IntegrationLink("sorting_engine", "spiritual_engine", "data_flow",
                            "Spiritual inputs route to spiritual engine"),
            IntegrationLink("sorting_engine", "security_module", "data_flow",
                            "THREAT category inputs route to security"),
            IntegrationLink("sorting_engine", "legacy_engine", "data_flow",
                            "LEGACY category inputs route to legacy engine"),
            IntegrationLink("sorting_engine", "faith_engine", "data_flow",
                            "Faith-related inputs route to faith engine"),

            # Emotional ↔ Spiritual
            IntegrationLink("emotional_engine", "spiritual_engine", "data_flow",
                            "Emotional state feeds spiritual alignment", bidirectional=True),

            # Faith ↔ Spiritual
            IntegrationLink("faith_engine", "spiritual_engine", "data_flow",
                            "Faith processing feeds spiritual alignment", bidirectional=True),

            # Legacy capture points
            IntegrationLink("all_modules", "legacy_engine", "event",
                            "Completed workflows emit legacy capture events"),

            # Audit capture points
            IntegrationLink("all_modules", "audit_module", "event",
                            "All module operations emit audit events"),
            IntegrationLink("all_guards", "audit_module", "event",
                            "All guard actions emit audit events"),

            # Processor chains
            IntegrationLink("input_processor", "sorting_engine", "data_flow",
                            "Sanitized inputs flow to sorting"),
            IntegrationLink("emotional_processor", "emotional_engine", "data_flow",
                            "Processed emotional signals flow to engine"),
            IntegrationLink("ritual_processor", "ritual_dispatcher", "data_flow",
                            "Ritual execution flows through dispatcher"),
            IntegrationLink("pattern_processor", "pattern_registry", "data_flow",
                            "Discovered patterns register in the registry"),

            # Dispatcher routing
            IntegrationLink("event_dispatcher", "all_modules", "event",
                            "Events dispatched to subscribed modules"),
            IntegrationLink("module_dispatcher", "all_modules", "data_flow",
                            "Inter-module communication routing"),
            IntegrationLink("ritual_dispatcher", "ritual_processor", "data_flow",
                            "Ritual dispatch triggers ritual processing"),
        ]

    def get_links_from(self, source: str) -> list[IntegrationLink]:
        return [l for l in self._links if l.source == source]

    def get_links_to(self, target: str) -> list[IntegrationLink]:
        return [l for l in self._links if l.target == target]

    def get_all(self) -> list[IntegrationLink]:
        return self._links.copy()

    def get_data_flows(self) -> list[IntegrationLink]:
        return [l for l in self._links if l.link_type == "data_flow"]

    def get_sovereignty_links(self) -> list[IntegrationLink]:
        return [l for l in self._links if l.link_type == "sovereignty"]
