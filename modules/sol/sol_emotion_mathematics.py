"""
SOL EMOTION & MENTAL PATTERN MATHEMATICS
═══════════════════════════════════════════════════════════════════════════════
Complete Emotional Algebra, Mental Pattern Tracking, Dimensional Analysis
with Frequency Distribution, Transitions, and Therapeutic Scaling

Author: SoulJahOS Architecture
Based on: VAD model (Valence-Arousal-Dominance) + Sovereignty Extensions
Mathematical Foundation: Vector Spaces, Set Theory, Dynamical Systems
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from collections import Counter, defaultdict
import math
import json
import time


# ═══════════════════════════════════════════════════════════════════════════════
# EMOTIONAL TAXONOMY — COMPLETE EMOTION FAMILIES
# ═══════════════════════════════════════════════════════════════════════════════

EMOTION_FAMILIES = {
    "joy": {
        "members": ["happiness", "delight", "elation", "contentment", "bliss", "gratitude"],
        "valence": 0.9,      # -1.0 to 1.0 (negative ↔ positive)
        "arousal": 0.6,      # 0.0 to 1.0 (low energy ↔ high energy)
        "sovereignty": 1.0,  # 0.0 to 1.0 (powerless ↔ empowered)
        "category": "positive",
        "healing_target": False,
    },
    "peace": {
        "members": ["calm", "serenity", "tranquility", "stillness", "equanimity"],
        "valence": 0.6,
        "arousal": 0.1,
        "sovereignty": 1.0,
        "category": "positive",
        "healing_target": False,
    },
    "love": {
        "members": ["compassion", "tenderness", "devotion", "agape", "warmth", "care"],
        "valence": 0.9,
        "arousal": 0.5,
        "sovereignty": 1.0,
        "category": "positive",
        "healing_target": False,
    },
    "sacred": {
        "members": ["awe", "reverence", "wonder", "transcendence", "grace"],
        "valence": 0.5,
        "arousal": 0.3,
        "sovereignty": 1.0,
        "category": "positive",
        "healing_target": False,
    },
    "grief": {
        "members": ["sorrow", "loss", "mourning", "heartache", "longing"],
        "valence": -0.7,
        "arousal": 0.3,
        "sovereignty": 0.8,
        "category": "negative",
        "healing_target": False,  # Process, don't eliminate
    },
    "anger": {
        "members": ["frustration", "rage", "indignation", "resentment"],
        "valence": -0.5,
        "arousal": 0.9,
        "sovereignty": 0.9,  # Anger has agency
        "category": "negative",
        "healing_target": False,
    },
    "fear": {
        "members": ["anxiety", "dread", "panic", "worry", "terror", "apprehension"],
        "valence": -0.7,
        "arousal": 0.8,
        "sovereignty": 0.3,  # Fear REDUCES agency
        "category": "negative",
        "healing_target": True,  # Primary healing target
    },
    "shame": {
        "members": ["guilt", "humiliation", "embarrassment", "unworthiness"],
        "valence": -0.8,
        "arousal": 0.4,
        "sovereignty": 0.2,  # Shame DESTROYS sovereignty
        "category": "negative",
        "healing_target": True,  # Primary healing target
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# EMOTIONAL DIMENSIONS — AXIS DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

class EmotionalDimension(Enum):
    """The mathematical space of emotional experience."""
    VALENCE = "valence"            # -1.0 to 1.0 | Negative ↔ Positive
    AROUSAL = "arousal"            # 0.0 to 1.0  | Low Energy ↔ High Energy
    DOMINANCE = "dominance"        # 0.0 to 1.0  | Passive ↔ Assertive
    SOVEREIGNTY = "sovereignty"    # 0.0 to 1.0  | Powerless ↔ Empowered (SoulJahOS extension)
    RELATIONAL = "relational"      # 0.0 to 1.0  | Isolated ↔ Connected (SoulJahOS extension)
    SACRED = "sacred"              # 0.0 to 1.0  | Mundane ↔ Transcendent (SoulJahOS extension)


# ═══════════════════════════════════════════════════════════════════════════════
# MENTAL PATTERN TAXONOMY
# ═══════════════════════════════════════════════════════════════════════════════

MENTAL_PATTERNS = {
    "rumination": {
        "description": "Repetitive negative thinking loop",
        "associated_emotions": ["fear", "shame", "grief"],
        "frequency_indicator": "circular_thoughts",
        "intervention": "grounding_ritual",
        "severity": "medium",
    },
    "catastrophizing": {
        "description": "Imagining worst-case scenarios",
        "associated_emotions": ["fear", "anxiety"],
        "frequency_indicator": "worst_case_language",
        "intervention": "reality_check_ritual",
        "severity": "high",
    },
    "self_criticism": {
        "description": "Harsh self-judgment pattern",
        "associated_emotions": ["shame", "guilt"],
        "frequency_indicator": "negative_self_talk",
        "intervention": "self_compassion_ritual",
        "severity": "high",
    },
    "people_pleasing": {
        "description": "Suppressing own needs for others",
        "associated_emotions": ["fear", "anxiety"],
        "frequency_indicator": "over_accommodation",
        "intervention": "boundary_setting_ritual",
        "severity": "medium",
    },
    "avoidance": {
        "description": "Withdrawal from challenges or feelings",
        "associated_emotions": ["fear", "shame"],
        "frequency_indicator": "procrastination",
        "intervention": "approach_gradient_ritual",
        "severity": "medium",
    },
    "hypervigilance": {
        "description": "Hyper-alert threat detection",
        "associated_emotions": ["fear", "anger"],
        "frequency_indicator": "scanning_behavior",
        "intervention": "safety_affirmation_ritual",
        "severity": "high",
    },
    "flow_state": {
        "description": "Complete absorption in meaningful activity",
        "associated_emotions": ["joy", "peace", "sacred"],
        "frequency_indicator": "time_distortion",
        "intervention": "extend_flow_ritual",
        "severity": "low",  # Positive pattern
    },
    "meaning_making": {
        "description": "Finding purpose in difficulty",
        "associated_emotions": ["grief", "love", "sacred"],
        "frequency_indicator": "narrative_construction",
        "intervention": "legacy_capture_ritual",
        "severity": "low",  # Positive pattern
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# MATHEMATICAL MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class EmotionalVector:
    """3-6D vector in emotional space."""
    valence: float = 0.0        # -1.0 to 1.0
    arousal: float = 0.0        # 0.0 to 1.0
    dominance: float = 0.5      # 0.0 to 1.0
    sovereignty: float = 1.0    # 0.0 to 1.0
    relational: float = 0.5     # 0.0 to 1.0
    sacred: float = 0.0         # 0.0 to 1.0

    def magnitude(self) -> float:
        """Euclidean length in 6D space."""
        return math.sqrt(
            self.valence**2 + self.arousal**2 + self.dominance**2 +
            self.sovereignty**2 + self.relational**2 + self.sacred**2
        )

    def distance_to(self, other: EmotionalVector) -> float:
        """Distance between two emotional states."""
        dv = (self.valence - other.valence) ** 2
        da = (self.arousal - other.arousal) ** 2
        dd = (self.dominance - other.dominance) ** 2
        ds = (self.sovereignty - other.sovereignty) ** 2
        dr = (self.relational - other.relational) ** 2
        dsac = (self.sacred - other.sacred) ** 2
        return math.sqrt(dv + da + dd + ds + dr + dsac)

    def dot_product(self, other: EmotionalVector) -> float:
        """Cosine similarity in emotional space."""
        return (self.valence * other.valence +
                self.arousal * other.arousal +
                self.dominance * other.dominance +
                self.sovereignty * other.sovereignty +
                self.relational * other.relational +
                self.sacred * other.sacred)

    def normalize(self) -> EmotionalVector:
        """Unit vector in emotional space."""
        mag = self.magnitude()
        if mag == 0:
            return EmotionalVector()
        return EmotionalVector(
            valence=self.valence / mag,
            arousal=self.arousal / mag,
            dominance=self.dominance / mag,
            sovereignty=self.sovereignty / mag,
            relational=self.relational / mag,
            sacred=self.sacred / mag
        )

    def to_dict(self) -> Dict[str, float]:
        return {
            "valence": round(self.valence, 3),
            "arousal": round(self.arousal, 3),
            "dominance": round(self.dominance, 3),
            "sovereignty": round(self.sovereignty, 3),
            "relational": round(self.relational, 3),
            "sacred": round(self.sacred, 3),
        }


@dataclass
class MentalPatternInstance:
    """An occurrence of a mental pattern."""
    pattern_id: str
    pattern_type: str  # From MENTAL_PATTERNS keys
    timestamp: float = field(default_factory=time.time)
    emotion_context: str = ""
    intensity: float = 0.5  # 0.0 to 1.0
    duration_seconds: float = 0.0
    triggered_by: str = ""  # Event or thought that triggered it
    intervention_applied: str = ""
    resolved: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timestamp)),
            "emotion_context": self.emotion_context,
            "intensity": round(self.intensity, 2),
            "duration_seconds": round(self.duration_seconds, 1),
            "triggered_by": self.triggered_by,
            "intervention": self.intervention_applied,
            "resolved": self.resolved,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# FREQUENCY & TRANSITION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

class EmotionTransitionMatrix:
    """Track how emotions transition to other emotions."""
    
    def __init__(self):
        self.transitions: Dict[str, Counter] = defaultdict(Counter)
        self.transition_times: Dict[str, List[float]] = defaultdict(list)
        self.last_emotion: Optional[str] = None
        self.last_transition_time: float = time.time()

    def record_transition(self, from_emotion: str, to_emotion: str, duration: float = 0.0):
        """Record an emotional transition."""
        self.transitions[from_emotion][to_emotion] += 1
        self.transition_times[f"{from_emotion}->{to_emotion}"].append(duration)

    def get_transition_probabilities(self, from_emotion: str) -> Dict[str, float]:
        """Probability of transitioning to each emotion."""
        if from_emotion not in self.transitions:
            return {}
        
        total = sum(self.transitions[from_emotion].values())
        return {
            to_e: count / total
            for to_e, count in self.transitions[from_emotion].items()
        }

    def avg_transition_time(self, from_e: str, to_e: str) -> float:
        """Average time to transition between emotions."""
        key = f"{from_e}->{to_e}"
        if key not in self.transition_times or not self.transition_times[key]:
            return 0.0
        return sum(self.transition_times[key]) / len(self.transition_times[key])

    def get_stuck_emotions(self, threshold_seconds: float = 300.0) -> List[str]:
        """Emotions that user gets stuck in (> threshold duration)."""
        stuck = []
        for key, times in self.transition_times.items():
            if any(t > threshold_seconds for t in times):
                from_e = key.split("->")[0]
                stuck.append(from_e)
        return list(set(stuck))


class FrequencyAnalyzer:
    """Analyze occurrence frequency of emotions and patterns."""
    
    def __init__(self):
        self.emotion_counts: Counter = Counter()
        self.pattern_counts: Counter = Counter()
        self.emotion_by_hour: Dict[int, Counter] = defaultdict(Counter)
        self.emotion_by_day: Dict[str, Counter] = defaultdict(Counter)
        self.pattern_by_emotion: Dict[str, Counter] = defaultdict(Counter)

    def record_emotion(self, emotion: str, timestamp: float = None):
        """Record an emotion occurrence."""
        if timestamp is None:
            timestamp = time.time()
        
        self.emotion_counts[emotion] += 1
        
        # Time-based bucketing
        hour = time.localtime(timestamp).tm_hour
        self.emotion_by_hour[hour][emotion] += 1
        
        date = time.strftime('%Y-%m-%d', time.localtime(timestamp))
        self.emotion_by_day[date][emotion] += 1

    def record_pattern(self, pattern: str, emotion: str = ""):
        """Record a mental pattern occurrence."""
        self.pattern_counts[pattern] += 1
        if emotion:
            self.pattern_by_emotion[emotion][pattern] += 1

    def get_emotion_frequency(self, limit: int = 10) -> Dict[str, int]:
        """Top N emotions by frequency."""
        return dict(self.emotion_counts.most_common(limit))

    def get_emotion_distribution(self) -> Dict[str, float]:
        """Emotion distribution as percentages."""
        total = sum(self.emotion_counts.values())
        if total == 0:
            return {}
        return {
            e: round((c / total) * 100, 1)
            for e, c in self.emotion_counts.items()
        }

    def get_daily_frequency(self, date: str) -> Dict[str, int]:
        """Emotion frequency for a specific day."""
        return dict(self.emotion_by_day.get(date, Counter()))

    def get_hourly_frequency(self, hour: int) -> Dict[str, int]:
        """Emotion frequency for a specific hour."""
        return dict(self.emotion_by_hour.get(hour, Counter()))

    def get_pattern_frequency(self, limit: int = 10) -> Dict[str, int]:
        """Top N patterns by frequency."""
        return dict(self.pattern_counts.most_common(limit))

    def get_patterns_by_emotion(self, emotion: str) -> Dict[str, int]:
        """Which patterns occur with which emotions."""
        return dict(self.pattern_by_emotion.get(emotion, Counter()))


# ═══════════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE EMOTION ANALYZER
# ═══════════════════════════════════════════════════════════════════════════════

class ComprehensiveEmotionAnalytics:
    """
    Complete emotion and mental pattern analysis system.
    
    Capabilities:
    - Track all emotions with mathematical precision
    - Identify recurring mental patterns
    - Analyze dimensional dynamics (6D emotional space)
    - Generate therapeutic insights
    - Export for team dashboards
    """

    def __init__(self, data_dir: str = "sol_emotion_analytics"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.emotions: List[Tuple[float, str, EmotionalVector]] = []
        self.patterns: List[MentalPatternInstance] = []
        self.transitions = EmotionTransitionMatrix()
        self.frequency = FrequencyAnalyzer()
        
        self._last_emotion: Optional[str] = None
        self._last_emotion_time: float = time.time()

    def log_emotion(self, emotion_name: str, vector: Optional[EmotionalVector] = None,
                   context: str = "") -> Tuple[str, EmotionalVector]:
        """Log an emotional state."""
        timestamp = time.time()
        
        # Infer vector from EMOTION_FAMILIES if not provided
        if vector is None:
            if emotion_name in EMOTION_FAMILIES:
                family = EMOTION_FAMILIES[emotion_name]
                vector = EmotionalVector(
                    valence=family["valence"],
                    arousal=family["arousal"],
                    sovereignty=family["sovereignty"]
                )
            else:
                vector = EmotionalVector()
        
        self.emotions.append((timestamp, emotion_name, vector))
        self.frequency.record_emotion(emotion_name, timestamp)
        
        # Record transition if there was a previous emotion
        if self._last_emotion and self._last_emotion != emotion_name:
            duration = timestamp - self._last_emotion_time
            self.transitions.record_transition(self._last_emotion, emotion_name, duration)
        
        self._last_emotion = emotion_name
        self._last_emotion_time = timestamp
        
        return emotion_name, vector

    def log_mental_pattern(self, pattern_type: str, emotion_context: str = "",
                          intensity: float = 0.5, triggered_by: str = "") -> MentalPatternInstance:
        """Log a mental pattern occurrence."""
        import uuid
        pattern_id = str(uuid.uuid4())[:8]
        
        instance = MentalPatternInstance(
            pattern_id=pattern_id,
            pattern_type=pattern_type,
            emotion_context=emotion_context,
            intensity=max(0.0, min(1.0, intensity)),
            triggered_by=triggered_by
        )
        
        self.patterns.append(instance)
        self.frequency.record_pattern(pattern_type, emotion_context)
        
        return instance

    def resolve_pattern(self, pattern_id: str, intervention: str = "",
                       resolved: bool = True):
        """Mark a pattern as resolved."""
        for pattern in self.patterns:
            if pattern.pattern_id == pattern_id:
                pattern.resolved = resolved
                pattern.intervention_applied = intervention
                pattern.duration_seconds = time.time() - pattern.timestamp
                break

    # ─────────────────────────────────────────────────────
    # ANALYSIS & INSIGHTS
    # ─────────────────────────────────────────────────────

    def get_emotional_centroid(self) -> Optional[EmotionalVector]:
        """Average emotional state across all logged emotions."""
        if not self.emotions:
            return None
        
        vectors = [v for _, _, v in self.emotions]
        avg = EmotionalVector(
            valence=sum(v.valence for v in vectors) / len(vectors),
            arousal=sum(v.arousal for v in vectors) / len(vectors),
            dominance=sum(v.dominance for v in vectors) / len(vectors),
            sovereignty=sum(v.sovereignty for v in vectors) / len(vectors),
            relational=sum(v.relational for v in vectors) / len(vectors),
            sacred=sum(v.sacred for v in vectors) / len(vectors),
        )
        return avg

    def get_emotional_volatility(self) -> float:
        """How much emotions vary (standard deviation in space)."""
        if len(self.emotions) < 2:
            return 0.0
        
        centroid = self.get_emotional_centroid()
        if not centroid:
            return 0.0
        
        distances = [centroid.distance_to(v) for _, _, v in self.emotions]
        mean_dist = sum(distances) / len(distances)
        variance = sum((d - mean_dist) ** 2 for d in distances) / len(distances)
        return math.sqrt(variance)

    def get_healing_targets(self) -> Dict[str, float]:
        """Emotions that need healing work + frequency."""
        healing_emotions = {e: d["healing_target"] for e, d in EMOTION_FAMILIES.items() if d["healing_target"]}
        freq = self.frequency.get_emotion_frequency(100)
        
        targets = {}
        for emotion, is_target in healing_emotions.items():
            if is_target and emotion in freq:
                targets[emotion] = freq[emotion]
        
        return dict(sorted(targets.items(), key=lambda x: x[1], reverse=True))

    def get_dimensional_profile(self) -> Dict[str, float]:
        """Average value on each dimension."""
        centroid = self.get_emotional_centroid()
        return centroid.to_dict() if centroid else {}

    def get_stuck_cycles(self) -> List[str]:
        """Emotions that repeat without transitioning."""
        return self.transitions.get_stuck_emotions()

    def get_unresolved_patterns(self) -> List[MentalPatternInstance]:
        """Mental patterns that haven't been addressed."""
        return [p for p in self.patterns if not p.resolved]

    # ─────────────────────────────────────────────────────
    # EXPORTS FOR DASHBOARDS
    # ─────────────────────────────────────────────────────

    def get_emotion_report(self) -> Dict[str, Any]:
        """Complete emotional profile for team dashboard."""
        return {
            "total_emotions_logged": len(self.emotions),
            "emotion_frequency": self.frequency.get_emotion_frequency(),
            "emotion_distribution": self.frequency.get_emotion_distribution(),
            "dimensional_profile": self.get_dimensional_profile(),
            "volatility_score": round(self.get_emotional_volatility(), 3),
            "healing_targets": self.get_healing_targets(),
            "stuck_emotions": self.transitions.get_stuck_emotions(),
            "transition_matrix": {
                e: self.transitions.get_transition_probabilities(e)
                for e in self.frequency.emotion_counts.keys()
            }
        }

    def get_pattern_report(self) -> Dict[str, Any]:
        """Complete mental pattern profile."""
        return {
            "total_patterns_logged": len(self.patterns),
            "pattern_frequency": self.frequency.get_pattern_frequency(),
            "unresolved_patterns": [p.to_dict() for p in self.get_unresolved_patterns()],
            "patterns_by_emotion": {
                e: self.frequency.get_patterns_by_emotion(e)
                for e in self.frequency.emotion_counts.keys()
            },
            "resolution_rate": round(
                len([p for p in self.patterns if p.resolved]) / max(1, len(self.patterns)),
                3
            )
        }

    def export_team_analytics(self) -> Dict[str, str]:
        """Export all analytics for team visualization."""
        import os as os_module
        
        files = {}
        
        # Emotion report
        emotion_data = self.get_emotion_report()
        emotion_file = os_module.path.join(self.data_dir, "emotion_profile.json")
        with open(emotion_file, 'w') as f:
            json.dump(emotion_data, f, indent=2)
        files["emotion"] = emotion_file
        
        # Pattern report
        pattern_data = self.get_pattern_report()
        pattern_file = os_module.path.join(self.data_dir, "pattern_profile.json")
        with open(pattern_file, 'w') as f:
            json.dump(pattern_data, f, indent=2)
        files["patterns"] = pattern_file
        
        # Combined dashboard
        dashboard = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "emotions": emotion_data,
            "patterns": pattern_data,
        }
        
        dash_file = os_module.path.join(self.data_dir, "complete_dashboard.json")
        with open(dash_file, 'w') as f:
            json.dump(dashboard, f, indent=2)
        files["dashboard"] = dash_file
        
        return files


# Utility imports
import os
