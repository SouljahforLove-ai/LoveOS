"""
Legacy Engine
═══════════════════════════════════════════════════
Manages intergenerational knowledge transmission,
legacy artifacts, and teaching workflows.

Design Philosophy:
  Legacy is not passive inheritance — it is active transmission.
  Every workflow, every ritual, every pattern is potentially
  a legacy artifact that can be taught, reproduced, and evolved.

Legacy Categories:
  - WORKFLOW:   Reproducible operational sequences
  - RITUAL:     Ceremonial and grounding practices
  - KNOWLEDGE:  Documented understanding and insight
  - ARTIFACT:   Created works (code, documents, designs)
  - PATTERN:    Behavioral and architectural patterns
  - TEACHING:   Structured educational content
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional
import time
import hashlib


class LegacyCategory(Enum):
    WORKFLOW = auto()
    RITUAL = auto()
    KNOWLEDGE = auto()
    ARTIFACT = auto()
    PATTERN = auto()
    TEACHING = auto()


class LegacyMaturity(Enum):
    SEED = auto()          # Initial capture
    GROWING = auto()       # Being developed
    MATURE = auto()        # Ready for transmission
    TRANSMITTED = auto()   # Successfully passed on
    EVOLVING = auto()      # Being adapted by next generation


@dataclass
class LegacyItem:
    """A single legacy artifact."""
    id: str = ""
    title: str = ""
    category: LegacyCategory = LegacyCategory.KNOWLEDGE
    maturity: LegacyMaturity = LegacyMaturity.SEED
    content: Any = None
    metadata: dict = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    transmitted_to: list[str] = field(default_factory=list)
    sovereignty_sealed: bool = True

    def compute_hash(self) -> str:
        return hashlib.sha256(f"{self.title}:{self.content}".encode()).hexdigest()[:16]


@dataclass
class TransmissionRecord:
    """Record of a legacy transmission event."""
    legacy_id: str
    recipient: str
    method: str  # "direct", "document", "ritual", "workflow"
    timestamp: float = field(default_factory=time.time)
    success: bool = False
    notes: str = ""


class LegacyEngine:
    """
    Manages the full lifecycle of legacy items — from seed to transmission.

    Core Operations:
    - Capture: Record new legacy items from workflows, rituals, insights
    - Develop: Mature legacy items through iteration and refinement
    - Transmit: Package and deliver legacy items to recipients
    - Track: Monitor transmission success and adaptation
    - Archive: Preserve legacy items with sovereignty seals
    """

    def __init__(self):
        self._items: dict[str, LegacyItem] = {}
        self._transmissions: list[TransmissionRecord] = []
        self._archive: dict[str, LegacyItem] = {}

    def capture(self, title: str, content: Any, category: LegacyCategory,
                tags: list[str] | None = None) -> LegacyItem:
        """Capture a new legacy item."""
        item = LegacyItem(
            id=hashlib.sha256(f"{title}:{time.time()}".encode()).hexdigest()[:12],
            title=title,
            category=category,
            content=content,
            tags=tags or [],
        )
        self._items[item.id] = item
        return item

    def develop(self, item_id: str, updates: dict) -> Optional[LegacyItem]:
        """Develop/refine a legacy item."""
        item = self._items.get(item_id)
        if not item:
            return None

        for key, value in updates.items():
            if hasattr(item, key):
                setattr(item, key, value)

        if item.maturity == LegacyMaturity.SEED:
            item.maturity = LegacyMaturity.GROWING
        elif item.maturity == LegacyMaturity.GROWING:
            item.maturity = LegacyMaturity.MATURE

        return item

    def transmit(self, item_id: str, recipient: str, method: str = "direct") -> TransmissionRecord:
        """Transmit a legacy item to a recipient."""
        item = self._items.get(item_id)
        record = TransmissionRecord(
            legacy_id=item_id,
            recipient=recipient,
            method=method,
            success=item is not None,
        )
        if item:
            item.transmitted_to.append(recipient)
            item.maturity = LegacyMaturity.TRANSMITTED
        self._transmissions.append(record)
        return record

    def archive(self, item_id: str) -> bool:
        """Archive a legacy item with sovereignty seal."""
        item = self._items.get(item_id)
        if not item:
            return False
        item.sovereignty_sealed = True
        self._archive[item_id] = item
        return True

    def query(self, category: Optional[LegacyCategory] = None,
              tags: Optional[list[str]] = None) -> list[LegacyItem]:
        """Query legacy items by category and/or tags."""
        results = list(self._items.values())
        if category:
            results = [i for i in results if i.category == category]
        if tags:
            results = [i for i in results if any(t in i.tags for t in tags)]
        return results

    def get_transmission_history(self) -> list[TransmissionRecord]:
        return self._transmissions.copy()

    def get_stats(self) -> dict:
        by_category = {}
        by_maturity = {}
        for item in self._items.values():
            cat = item.category.name
            mat = item.maturity.name
            by_category[cat] = by_category.get(cat, 0) + 1
            by_maturity[mat] = by_maturity.get(mat, 0) + 1
        return {
            "total_items": len(self._items),
            "by_category": by_category,
            "by_maturity": by_maturity,
            "total_transmissions": len(self._transmissions),
            "archived": len(self._archive),
        }
