"""
SOL Emotion & Pattern Analytics — Frequency, Dimensions & Mental Patterns
═══════════════════════════════════════════════════════════════════════════════

Comprehensive tracking of:
- 💭 Mental Patterns (recurring thought sequences)
- 🎭 Emotion Frequency & Distribution
- 📊 Emotional Dimensions (Valence, Arousal, Sovereignty)
- 🔄 Pattern-to-Pattern Transitions
- 🌀 Dimensional Phase Space Analysis
- 💫 Emotion-Dimension Correlation

For team dashboards, research, and therapeutic insights.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from enum import Enum
from collections import Counter, defaultdict
import json
import csv
import time
import math


# ═══════════════════════════════════════════════════════════════════════════════
# CORE DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

class EmotionalDimension(Enum):
    """The 3D space of emotional experience."""
    VALENCE = "valence"      # Negative ↔ Positive
    AROUSAL = "arousal"      # Low ↔ High (energy/intensity)
    SOVEREIGNTY = "sovereignty"  # Low (overwhelmed) ↔ High (empowered)


class MentalPatternType(Enum):
    """Categories of recurring mental patterns."""
    REPETITION = "repetition"      # Same thought recurring
    AVOIDANCE = "avoidance"        # Avoiding something
    RUMINATION = "rumination"      # Going in circles
    ANALYSIS = "analysis"          # Deep thinking/problem-solving
    PLANNING = "planning"          # Future-focused
    REFLECTION = "reflection"      # Looking back
    EMOTIONAL_PROCESSING = "emotional_processing"  # Feeling work
    GROUNDING = "grounding"        # Present-moment anchoring
    BREAKTHROUGH = "breakthrough"  # Novel insight
    SPIRAL = "spiral"              # Descending pattern


@dataclass
class EmotionSnapshot:
    """A moment-in-time capture of emotional state."""
    timestamp: float
    emotion_name: str
    valence: float = 0.0      # -1.0 to 1.0
    arousal: float = 0.0      # 0.0 to 1.0
    sovereignty: float = 1.0  # 0.0 to 1.0
    intensity: float = 0.5    # 0.0 to 1.0
    context: str = ""         # What triggered this?
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
            "emotion": self.emotion_name,
            "valence": round(self.valence, 3),
            "arousal": round(self.arousal, 3),
            "sovereignty": round(self.sovereignty, 3),
            "intensity": round(self.intensity, 3),
            "context": self.context
        }


@dataclass
class MentalPattern:
    """A recurring pattern detected in thinking/behavior."""
    pattern_id: str
    pattern_type: MentalPatternType
    name: str
    description: str
    first_detected: float
    occurrences: int = 1
    last_occurrence: float = field(default_factory=time.time)
    average_duration_seconds: float = 0.0
    associated_emotions: List[str] = field(default_factory=list)
    locations_in_conversation: List[int] = field(default_factory=list)  # Turn indices
    keywords: List[str] = field(default_factory=list)
    severity: float = 0.5  # 0.0-1.0 for concerning patterns
    is_helpful: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "type": self.pattern_type.value,
            "name": self.name,
            "description": self.description,
            "first_detected": datetime.fromtimestamp(self.first_detected).isoformat(),
            "last_occurrence": datetime.fromtimestamp(self.last_occurrence).isoformat(),
            "occurrences": self.occurrences,
            "average_duration_sec": round(self.average_duration_seconds, 2),
            "associated_emotions": self.associated_emotions,
            "keywords": self.keywords,
            "severity": round(self.severity, 3),
            "is_helpful": self.is_helpful,
            "frequency_per_hour": self._calc_frequency()
        }
    
    def _calc_frequency(self) -> float:
        """Occurrences per hour since first detection."""
        elapsed = time.time() - self.first_detected
        if elapsed < 3600:
            return self.occurrences
        return self.occurrences / (elapsed / 3600)


@dataclass
class DimensionalSnapshot:
    """3D emotional state at a moment."""
    timestamp: float
    valence: float
    arousal: float
    sovereignty: float
    emotion_label: str = ""
    
    def distance_to(self, other: DimensionalSnapshot) -> float:
        """Euclidean distance in 3D emotional space."""
        dv = (self.valence - other.valence) ** 2
        da = (self.arousal - other.arousal) ** 2
        ds = (self.sovereignty - other.sovereignty) ** 2
        return math.sqrt(dv + da + ds)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
            "valence": round(self.valence, 3),
            "arousal": round(self.arousal, 3),
            "sovereignty": round(self.sovereignty, 3),
            "emotion_label": self.emotion_label
        }


@dataclass
class PatternTransition:
    """When one mental pattern transitions to another."""
    from_pattern: str
    to_pattern: str
    timestamp: float
    transition_type: str = "natural"  # natural, triggered, forced, breakthrough
    emotion_at_transition: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "from": self.from_pattern,
            "to": self.to_pattern,
            "timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
            "type": self.transition_type,
            "emotion": self.emotion_at_transition
        }


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class EmotionPatternAnalytics:
    """
    Deep analysis of emotional states, mental patterns, and dimensional dynamics.
    """
    
    def __init__(self, data_dir: str = "sol_emotion_analytics"):
        self.data_dir = data_dir
        import os
        os.makedirs(data_dir, exist_ok=True)
        
        self._emotions: List[EmotionSnapshot] = []
        self._dimensions: List[DimensionalSnapshot] = []
        self._patterns: Dict[str, MentalPattern] = {}
        self._transitions: List[PatternTransition] = []
        self._current_pattern: Optional[str] = None
        
        # Frequency tracking
        self._emotion_frequency: Counter = Counter()
        self._pattern_frequency: Counter = Counter()
        self._transition_frequency: Counter = Counter()
        
        # Correlations
        self._emotion_to_patterns: Dict[str, Set[str]] = defaultdict(set)
        self._pattern_to_dimensions: Dict[str, List[DimensionalSnapshot]] = defaultdict(list)

    # ───────────────────────────────────────────────────────────────────────────
    # EMOTION TRACKING
    # ───────────────────────────────────────────────────────────────────────────

    def log_emotion(self, emotion_name: str, valence: float = 0.0, arousal: float = 0.0,
                   sovereignty: float = 1.0, intensity: float = 0.5, context: str = "") -> EmotionSnapshot:
        """Log an emotional state."""
        snapshot = EmotionSnapshot(
            timestamp=time.time(),
            emotion_name=emotion_name,
            valence=max(-1.0, min(1.0, valence)),
            arousal=max(0.0, min(1.0, arousal)),
            sovereignty=max(0.0, min(1.0, sovereignty)),
            intensity=max(0.0, min(1.0, intensity)),
            context=context
        )
        
        self._emotions.append(snapshot)
        self._emotion_frequency[emotion_name] += 1
        
        # Log dimensional state
        dim_snap = DimensionalSnapshot(
            timestamp=snapshot.timestamp,
            valence=snapshot.valence,
            arousal=snapshot.arousal,
            sovereignty=snapshot.sovereignty,
            emotion_label=emotion_name
        )
        self._dimensions.append(dim_snap)
        
        return snapshot

    def get_current_emotion_state(self) -> Optional[EmotionSnapshot]:
        """Get most recent emotional state."""
        return self._emotions[-1] if self._emotions else None

    def get_emotion_frequency(self, limit: int = 10) -> Dict[str, int]:
        """Top N emotions by frequency."""
        return dict(self._emotion_frequency.most_common(limit))

    def get_emotion_distribution(self) -> Dict[str, float]:
        """Emotion distribution as percentages."""
        total = len(self._emotions)
        if total == 0:
            return {}
        
        return {
            emotion: round((count / total) * 100, 2)
            for emotion, count in self._emotion_frequency.items()
        }

    # ───────────────────────────────────────────────────────────────────────────
    # MENTAL PATTERN TRACKING
    # ───────────────────────────────────────────────────────────────────────────

    def detect_pattern(self, pattern_type: MentalPatternType, name: str, description: str,
                      keywords: List[str] = None, severity: float = 0.5, is_helpful: bool = True) -> MentalPattern:
        """Register detection of a mental pattern."""
        pattern_id = f"{pattern_type.value}_{len(self._patterns)}"
        
        pattern = MentalPattern(
            pattern_id=pattern_id,
            pattern_type=pattern_type,
            name=name,
            description=description,
            first_detected=time.time(),
            keywords=keywords or [],
            severity=severity,
            is_helpful=is_helpful
        )
        
        self._patterns[pattern_id] = pattern
        self._pattern_frequency[name] += 1
        
        # Link to current emotion if exists
        if self._emotions:
            current_emotion = self._emotions[-1].emotion_name
            pattern.associated_emotions.append(current_emotion)
            self._emotion_to_patterns[current_emotion].add(pattern_id)
        
        # Track current pattern
        if self._current_pattern:
            self._transitions.append(PatternTransition(
                from_pattern=self._current_pattern,
                to_pattern=pattern_id,
                timestamp=time.time(),
                emotion_at_transition=self._emotions[-1].emotion_name if self._emotions else ""
            ))
            self._transition_frequency[f"{self._current_pattern} → {pattern_id}"] += 1
        
        self._current_pattern = pattern_id
        return pattern

    def record_pattern_occurrence(self, pattern_id: str, duration_seconds: float = 0.0):
        """Record that a pattern occurred again."""
        if pattern_id in self._patterns:
            pattern = self._patterns[pattern_id]
            pattern.occurrences += 1
            pattern.last_occurrence = time.time()
            
            if duration_seconds > 0:
                # Update running average
                total_duration = pattern.average_duration_seconds * (pattern.occurrences - 1)
                pattern.average_duration_seconds = (total_duration + duration_seconds) / pattern.occurrences
            
            self._pattern_frequency[pattern.name] += 1

    def get_pattern_frequency(self, limit: int = 10) -> Dict[str, int]:
        """Top N patterns by frequency."""
        return dict(self._pattern_frequency.most_common(limit))

    def get_patterns_by_type(self, pattern_type: MentalPatternType) -> List[MentalPattern]:
        """Get all patterns of a specific type."""
        return [p for p in self._patterns.values() if p.pattern_type == pattern_type]

    def get_problematic_patterns(self, severity_threshold: float = 0.6) -> List[MentalPattern]:
        """Get patterns that are concerning (high severity or not helpful)."""
        return [
            p for p in self._patterns.values()
            if not p.is_helpful or p.severity >= severity_threshold
        ]

    # ───────────────────────────────────────────────────────────────────────────
    # DIMENSIONAL ANALYSIS (3D EMOTIONAL SPACE)
    # ───────────────────────────────────────────────────────────────────────────

    def get_dimensional_stats(self) -> Dict[str, Dict[str, float]]:
        """Statistics on each dimension."""
        if not self._dimensions:
            return {}
        
        stats = {}
        for dim in [EmotionalDimension.VALENCE, EmotionalDimension.AROUSAL, EmotionalDimension.SOVEREIGNTY]:
            values = [getattr(d, dim.value) for d in self._dimensions]
            stats[dim.value] = {
                "min": round(min(values), 3),
                "max": round(max(values), 3),
                "mean": round(sum(values) / len(values), 3),
                "stdev": round(self._stdev(values), 3) if len(values) > 1 else 0.0
            }
        
        return stats

    def get_dimensional_trajectory(self, window_size: int = 10) -> List[Dict[str, float]]:
        """Recent trajectory through 3D emotional space."""
        if not self._dimensions:
            return []
        
        recent = self._dimensions[-window_size:]
        return [d.to_dict() for d in recent]

    def get_dimensional_clusters(self) -> Dict[str, int]:
        """Identify regions of emotional space that recur."""
        if len(self._dimensions) < 3:
            return {}
        
        clusters = defaultdict(int)
        
        for dim in self._dimensions:
            # Quantize to nearest 0.1 for clustering
            v_bucket = round(dim.valence * 10) / 10
            a_bucket = round(dim.arousal * 10) / 10
            s_bucket = round(dim.sovereignty * 10) / 10
            
            key = f"V{v_bucket:.1f}_A{a_bucket:.1f}_S{s_bucket:.1f}"
            clusters[key] += 1
        
        # Return clusters with count > 1 (recurring states)
        return {k: v for k, v in sorted(clusters.items(), key=lambda x: x[1], reverse=True) if v > 1}

    def get_emotional_range(self) -> Dict[str, Tuple[float, float]]:
        """Range of movement in emotional space."""
        if not self._dimensions:
            return {}
        
        return {
            "valence": (min(d.valence for d in self._dimensions), max(d.valence for d in self._dimensions)),
            "arousal": (min(d.arousal for d in self._dimensions), max(d.arousal for d in self._dimensions)),
            "sovereignty": (min(d.sovereignty for d in self._dimensions), max(d.sovereignty for d in self._dimensions)),
        }

    # ───────────────────────────────────────────────────────────────────────────
    # CORRELATION ANALYSIS
    # ───────────────────────────────────────────────────────────────────────────

    def get_emotion_pattern_correlations(self) -> Dict[str, List[str]]:
        """Which patterns tend to appear with which emotions?"""
        return dict(self._emotion_to_patterns)

    def get_pattern_dimensional_profile(self, pattern_id: str) -> Dict[str, float]:
        """Average dimensional values when this pattern occurs."""
        if pattern_id not in self._pattern_to_dimensions:
            return {}
        
        dims = self._pattern_to_dimensions[pattern_id]
        if not dims:
            return {}
        
        return {
            "avg_valence": round(sum(d.valence for d in dims) / len(dims), 3),
            "avg_arousal": round(sum(d.arousal for d in dims) / len(dims), 3),
            "avg_sovereignty": round(sum(d.sovereignty for d in dims) / len(dims), 3),
            "count": len(dims)
        }

    def get_transition_network(self) -> Dict[str, Dict[str, int]]:
        """Pattern transition adjacency (frequency of A→B transitions)."""
        network = defaultdict(lambda: defaultdict(int))
        
        for trans in self._transitions:
            network[trans.from_pattern][trans.to_pattern] += 1
        
        return {k: dict(v) for k, v in network.items()}

    # ───────────────────────────────────────────────────────────────────────────
    # EXPORT FUNCTIONS
    # ───────────────────────────────────────────────────────────────────────────

    def export_emotion_log(self, filepath: str = None) -> str:
        """Export all emotion snapshots to CSV."""
        if not filepath:
            filepath = f"{self.data_dir}/emotion_log.csv"
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "timestamp", "emotion", "valence", "arousal", "sovereignty", "intensity", "context"
            ])
            writer.writeheader()
            for snapshot in self._emotions:
                writer.writerow(snapshot.to_dict())
        
        return filepath

    def export_pattern_analysis(self, filepath: str = None) -> str:
        """Export mental pattern analysis to CSV."""
        if not filepath:
            filepath = f"{self.data_dir}/pattern_analysis.csv"
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "pattern_id", "type", "name", "description", "first_detected", "occurrences",
                "average_duration_sec", "associated_emotions", "keywords", "severity",
                "is_helpful", "frequency_per_hour"
            ])
            writer.writeheader()
            for pattern in self._patterns.values():
                data = pattern.to_dict()
                data["associated_emotions"] = ",".join(data["associated_emotions"])
                data["keywords"] = ",".join(data["keywords"])
                writer.writerow(data)
        
        return filepath

    def export_dimensional_trajectory(self, filepath: str = None) -> str:
        """Export 3D emotional trajectory to CSV."""
        if not filepath:
            filepath = f"{self.data_dir}/dimensional_trajectory.csv"
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "timestamp", "valence", "arousal", "sovereignty", "emotion_label"
            ])
            writer.writeheader()
            for snapshot in self._dimensions:
                writer.writerow(snapshot.to_dict())
        
        return filepath

    def export_team_report(self) -> Dict[str, str]:
        """Export complete emotion + pattern + dimensional analysis."""
        files = {}
        
        files["emotions"] = self.export_emotion_log()
        files["patterns"] = self.export_pattern_analysis()
        files["dimensions"] = self.export_dimensional_trajectory()
        
        # Summary JSON
        summary_file = f"{self.data_dir}/emotion_pattern_summary.json"
        summary = {
            "generated_at": datetime.now().isoformat(),
            "emotion_stats": {
                "total_emotions_logged": len(self._emotions),
                "unique_emotions": len(self._emotion_frequency),
                "distribution": self.get_emotion_distribution(),
                "frequency": self.get_emotion_frequency(),
            },
            "pattern_stats": {
                "total_patterns_detected": len(self._patterns),
                "pattern_types": {
                    pt.value: len(self.get_patterns_by_type(pt))
                    for pt in MentalPatternType
                },
                "problematic_patterns": [
                    p.to_dict() for p in self.get_problematic_patterns()
                ],
                "transitions": len(self._transitions),
                "transition_network": self.get_transition_network(),
            },
            "dimensional_stats": self.get_dimensional_stats(),
            "dimensional_clusters": self.get_dimensional_clusters(),
            "correlations": {
                k: list(v) for k, v in self.get_emotion_pattern_correlations().items()
            }
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        files["summary"] = summary_file
        print(f"✅ Emotion & Pattern Analysis exported to {self.data_dir}/")
        return files

    # ───────────────────────────────────────────────────────────────────────────
    # UTILITIES
    # ───────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _stdev(values: List[float]) -> float:
        """Calculate standard deviation."""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)

    def get_team_dashboard_data(self) -> Dict[str, Any]:
        """All data formatted for team visualization."""
        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "session_duration_hours": (time.time() - self._emotions[0].timestamp) / 3600 if self._emotions else 0,
            },
            "emotions": {
                "frequency": self.get_emotion_frequency(),
                "distribution": self.get_emotion_distribution(),
                "current": self.get_current_emotion_state().to_dict() if self.get_current_emotion_state() else {},
            },
            "patterns": {
                "detected": len(self._patterns),
                "frequency": self.get_pattern_frequency(),
                "by_type": {
                    pt.value: len(self.get_patterns_by_type(pt))
                    for pt in MentalPatternType
                },
                "problematic": [
                    {k: v for k, v in p.to_dict().items() if k != "keywords"}
                    for p in self.get_problematic_patterns()
                ],
            },
            "dimensions": {
                "stats": self.get_dimensional_stats(),
                "range": {k: {"min": v[0], "max": v[1]} for k, v in self.get_emotional_range().items()},
                "trajectory": self.get_dimensional_trajectory(window_size=20),
                "clusters": self.get_dimensional_clusters(),
            },
            "transitional_dynamics": {
                "patterns_detected": len(self._transitions),
                "network": self.get_transition_network(),
            }
        }
