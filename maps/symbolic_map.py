"""
Symbolic Map
═══════════════════════════════════════════════════
Maps symbolic meanings to computational constructs.
Symbols bridge the human-spiritual layer to the
mathematical-computational layer.

Every symbol in SoulJahOS has:
  - A name (human-readable identifier)
  - A glyph (visual representation)
  - A vector (mathematical embedding)
  - A domain (which engine/module uses it)
  - A sovereignty weight (how sovereign-critical it is)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Symbol:
    """A mapped symbol with computational meaning."""
    name: str
    glyph: str
    description: str
    domain: str                    # "identity", "emotional", "spiritual", "faith", "legacy"
    vector: list[float] = field(default_factory=list)  # Mathematical embedding
    sovereignty_weight: float = 0.5  # 0→1, how sovereignty-critical
    associations: list[str] = field(default_factory=list)


class SymbolicMap:
    """
    Central symbolic mapping — bridges meaning and computation.
    """

    def __init__(self):
        self._symbols: dict[str, Symbol] = {}
        self._initialize_core_symbols()

    def _initialize_core_symbols(self):
        core = [
            Symbol("sigil", "N2 m(THYSELF)e | 👁️ .", "The sovereign sigil — identity seal",
                   "identity", [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0], 1.0,
                   ["identity", "sovereignty", "presence"]),
            Symbol("eye", "👁️", "The all-seeing eye — awareness and presence",
                   "spiritual", [0.0, 0.3, 0.5, 0.9, 0.7, 0.0, 0.8], 0.8,
                   ["presence", "awareness", "vision"]),
            Symbol("heart", "🖤", "The sovereign heart — love as foundation",
                   "emotional", [0.9, 0.5, 0.5, 0.8, 0.9, 0.0, 1.0], 0.9,
                   ["love", "compassion", "sovereignty"]),
            Symbol("cross", "✝️", "The cross — faith integration",
                   "faith", [0.5, 0.3, 0.5, 1.0, 0.5, 0.0, 0.8], 0.7,
                   ["faith", "sacrifice", "grace", "redemption"]),
            Symbol("shield", "🛡️", "The sovereignty shield — boundary protection",
                   "identity", [0.3, 0.4, 0.9, 0.3, 0.2, 0.0, 1.0], 1.0,
                   ["protection", "boundary", "sovereignty"]),
            Symbol("seed", "🌱", "The legacy seed — intergenerational transmission",
                   "legacy", [0.6, 0.2, 0.3, 0.5, 0.7, 0.8, 0.7], 0.6,
                   ["legacy", "growth", "transmission", "zen"]),
            Symbol("flame", "🔥", "The sacred flame — spiritual intensity",
                   "spiritual", [0.4, 0.9, 0.6, 0.8, 0.3, 0.0, 0.7], 0.5,
                   ["intensity", "passion", "sacred"]),
            Symbol("anchor", "⚓", "The grounding anchor — presence and stability",
                   "spiritual", [0.5, 0.1, 0.6, 0.4, 0.5, 0.0, 0.9], 0.7,
                   ["grounding", "stability", "presence"]),
            Symbol("key", "🗝️", "The sovereignty key — access and authorization",
                   "identity", [0.3, 0.3, 0.8, 0.2, 0.2, 0.0, 1.0], 0.9,
                   ["access", "permission", "sovereignty"]),
            Symbol("crown", "👑", "The operator crown — sovereign authority",
                   "identity", [0.5, 0.4, 1.0, 0.6, 0.3, 0.0, 1.0], 1.0,
                   ["authority", "sovereignty", "dignity"]),
        ]
        for s in core:
            self._symbols[s.name] = s

    def lookup(self, name: str) -> Optional[Symbol]:
        return self._symbols.get(name)

    def get_by_domain(self, domain: str) -> list[Symbol]:
        return [s for s in self._symbols.values() if s.domain == domain]

    def get_sovereign_symbols(self, threshold: float = 0.8) -> list[Symbol]:
        return [s for s in self._symbols.values() if s.sovereignty_weight >= threshold]

    def register(self, symbol: Symbol):
        self._symbols[symbol.name] = symbol

    def get_all(self) -> list[Symbol]:
        return list(self._symbols.values())

    def compute_resonance(self, symbol_a: str, symbol_b: str) -> float:
        """Compute resonance (cosine similarity) between two symbols."""
        a = self._symbols.get(symbol_a)
        b = self._symbols.get(symbol_b)
        if not a or not b or not a.vector or not b.vector:
            return 0.0
        import math
        dot = sum(x * y for x, y in zip(a.vector, b.vector))
        mag_a = math.sqrt(sum(x ** 2 for x in a.vector))
        mag_b = math.sqrt(sum(x ** 2 for x in b.vector))
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)
