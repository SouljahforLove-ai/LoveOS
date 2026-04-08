"""
EXAMPLE: Real Therapy Session with Complete Emotion + Pattern Analytics
═══════════════════════════════════════════════════════════════════════════════

This example shows how to use sol_emotion_mathematics.py to track a real
therapeutic conversation, including emotion detection, pattern identification,
and generating team dashboards.
"""

from modules.sol.sol_emotion_mathematics import (
    ComprehensiveEmotionAnalytics,
    EmotionalVector,
    EMOTION_FAMILIES,
    MENTAL_PATTERNS
)
import json
import time


def example_therapy_session():
    """
    Simulate a therapy session tracking emotions and mental patterns.
    """
    
    # Initialize analytics engine for this session
    analytics = ComprehensiveEmotionAnalytics(data_dir="example_session_analytics")
    
    print("=" * 80)
    print("EXAMPLE: Real Therapy Session with Full Analytics")
    print("=" * 80)
    print()
    
    # ─────────────────────────────────────────────────────────────────
    # BEGINNING OF SESSION: Client enters in anxious state
    # ─────────────────────────────────────────────────────────────────
    
    print("📍 CLIENT ENTERS SESSION")
    print("-" * 80)
    
    # Client starts with high anxiety
    fear_vector = EmotionalVector(
        valence=-0.6,
        arousal=0.8,
        sovereignty=0.4,  # Reduced agency from anxiety
        relational=0.6,   # Hesitant about connection
        sacred=0.2,       # Disconnected from meaning
    )
    
    emotion1, vec1 = analytics.log_emotion(
        emotion_name="fear",
        vector=fear_vector,
        context="Just arrived for session, thinking about work presentation tomorrow"
    )
    
    print(f"Initial emotion: {emotion1}")
    print(f"Vector: {vec1.to_dict()}")
    print(f"  → Sovereignty is LOW (0.4) - client feels powerless")
    print(f"  → Arousal is HIGH (0.8) - nervous system activated")
    print()
    
    # Immediately logs rumination pattern
    pattern1 = analytics.log_mental_pattern(
        pattern_type="catastrophizing",
        emotion_context="fear",
        intensity=0.75,
        triggered_by="anticipatory worry about presentation"
    )
    
    print(f"Pattern detected: {pattern1.pattern_type}")
    print(f"  Pattern ID: {pattern1.pattern_id}")
    print(f"  Intensity: {pattern1.intensity}")
    print(f"  (Triggers reality_check_ritual intervention)")
    print()
    
    # ─────────────────────────────────────────────────────────────────
    # MIDDLE OF SESSION: Therapeutic work happening
    # ─────────────────────────────────────────────────────────────────
    
    print("📍 DURING SESSION - Grounding & Reality Work")
    print("-" * 80)
    
    # Simulate passage of time
    time.sleep(0.5)
    
    # Client transitions to peace after grounding exercise
    peace_vector = EmotionalVector(
        valence=0.5,
        arousal=0.3,
        sovereignty=0.7,  # Starting to reclaim agency
        relational=0.8,   # More connected
        sacred=0.4,
    )
    
    emotion2, vec2 = analytics.log_emotion(
        emotion_name="peace",
        vector=peace_vector,
        context="After grounding exercise - feeling more present"
    )
    
    distance = vec1.distance_to(vec2)
    
    print(f"Emotion transition: fear → peace")
    print(f"Emotional distance traveled: {distance:.3f}/2.45 (max)")
    print(f"  → Valence improved: {vec1.valence} → {vec2.valence}")
    print(f"  → Sovereignty improved: {vec1.sovereignty} → {vec2.sovereignty}")
    print(f"  → Arousal decreased: {vec1.arousal} → {vec2.arousal}")
    print()
    
    # Mark the catastrophizing pattern as resolved
    analytics.resolve_pattern(
        pattern1.pattern_id,
        intervention="reality_check_ritual + grounding_exercise"
    )
    
    print(f"✓ Pattern {pattern1.pattern_id} resolved")
    print(f"  Duration: {time.time() - pattern1.timestamp:.1f} seconds")
    print()
    
    # More conversation - client shifts to meaningful reflection
    time.sleep(0.3)
    
    sacred_vector = EmotionalVector(
        valence=0.6,
        arousal=0.2,
        sovereignty=1.0,  # Full agency restored
        relational=0.9,   # Deeply connected
        sacred=0.7,       # Connected to meaning
    )
    
    emotion3, vec3 = analytics.log_emotion(
        emotion_name="sacred",  # Awe/transcendence from meaningful conversation
        vector=sacred_vector,
        context="Realized this presentation is aligned with my values and purpose"
    )
    
    print(f"Deepening insight (final emotion): sacred/transcendence")
    print(f"Vector: {vec3.to_dict()}")
    print(f"  → Sovereignty: FULLY RESTORED (1.0)")
    print(f"  → Sacred alignment: HIGH (0.7) - meaning reconnected")
    print(f"  → Relational: STRONG (0.9) - feeling held in session")
    print()
    
    # ─────────────────────────────────────────────────────────────────
    # END OF SESSION: Generate analytics
    # ─────────────────────────────────────────────────────────────────
    
    print("📍 SESSION COMPLETE - Generating Analytics")
    print("-" * 80)
    print()
    
    # Get comprehensive reports
    emotion_report = analytics.get_emotion_report()
    pattern_report = analytics.get_pattern_report()
    
    print("EMOTION REPORT:")
    print(f"  Total emotions logged: {emotion_report['total_emotions_logged']}")
    print(f"  Emotion frequency: {emotion_report['emotion_frequency']}")
    print(f"  Distribution: {emotion_report['emotion_distribution']}")
    print()
    
    print("DIMENSIONAL PROFILE:")
    for dim, value in emotion_report['dimensional_profile'].items():
        print(f"  {dim}: {value:+.3f}")
    print()
    
    print("VOLATILITY & STABILITY:")
    volatility = emotion_report['volatility_score']
    stability = 1.0 - volatility
    print(f"  Volatility score: {volatility:.3f}")
    print(f"  Stability score: {stability:.3f}/1.0")
    print(f"  (Higher = more emotionally stable throughout session)")
    print()
    
    print("MENTAL PATTERNS:")
    print(f"  Total patterns: {pattern_report['total_patterns_logged']}")
    print(f"  Resolution rate: {pattern_report['resolution_rate']:.1%}")
    print()
    
    # ─────────────────────────────────────────────────────────────────
    # TEAM DASHBOARD EXPORT
    # ─────────────────────────────────────────────────────────────────
    
    print("📊 TEAM DASHBOARD EXPORT")
    print("-" * 80)
    
    export_files = analytics.export_team_analytics()
    
    print("Files created for team:")
    for file_type, filepath in export_files.items():
        print(f"  ✓ {file_type}: {filepath}")
    print()
    
    # Show what's in the dashboard
    print("DASHBOARD CONTENTS:")
    print()
    
    # Read dashboard to show sample
    import os
    import json
    dash_file = export_files.get("dashboard")
    
    if dash_file and os.path.exists(dash_file):
        with open(dash_file, 'r') as f:
            dashboard = json.load(f)
        
        print(json.dumps(dashboard, indent=2))
    
    print()
    print("=" * 80)
    print("INTERPRETATION FOR THERAPY TEAM:")
    print("=" * 80)
    print()
    print("✓ Session was successful")
    print("  - Client began in fear/anxiety (Sovereignty: 0.4)")
    print("  - Through therapeutic work, reached sacred/meaning state (Sovereignty: 1.0)")
    print("  - Catastrophizing pattern identified and resolved quickly")
    print("  - Emotional volatility LOW (stable despite transitions)")
    print("  - Final state: high agency, high connection, high meaning")
    print()
    print("→ Next session focus: Build on meaning-making momentum, prevent regression")
    print()


def example_multi_session_analysis():
    """
    Analyze patterns across multiple therapy sessions.
    """
    
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Multi-Session Analysis (Pattern Across Time)")
    print("=" * 80)
    print()
    
    analytics = ComprehensiveEmotionAnalytics(data_dir="multi_session_analytics")
    
    # Simulate 5 sessions worth of emotion data
    sessions = [
        # Session 1: Anxious, catastrophizing
        [("fear", 0.75), ("fear", 0.70), ("peace", 0.50)],
        # Session 2: Still anxious, less catastrophizing
        [("fear", 0.60), ("peace", 0.55), ("peace", 0.60)],
        # Session 3: Mixed emotions, some joy emerging
        [("peace", 0.55), ("joy", 0.50), ("peace", 0.65)],
        # Session 4: More stable, mostly peace/joy
        [("joy", 0.65), ("peace", 0.70), ("love", 0.60)],
        # Session 5: Resilient, accessing sacred
        [("joy", 0.70), ("sacred", 0.65), ("peace", 0.75)],
    ]
    
    patterns_logged = []
    
    for session_num, emotions in enumerate(sessions, 1):
        print(f"Session {session_num}:")
        
        for emotion_name, intensity in emotions:
            vector = EmotionalVector(
                valence=EMOTION_FAMILIES[emotion_name]["valence"],
                arousal=EMOTION_FAMILIES[emotion_name]["arousal"],
                sovereignty=EMOTION_FAMILIES[emotion_name]["sovereignty"],
            )
            
            analytics.log_emotion(emotion_name, vector)
            print(f"  {emotion_name} (intensity: {intensity})")
        
        # Log a pattern every other session
        if session_num % 2 == 1:
            pattern = analytics.log_mental_pattern(
                pattern_type="catastrophizing" if session_num < 3 else "flow_state",
                emotion_context=emotions[0][0],
                intensity=0.5
            )
            patterns_logged.append(pattern)
        
        print()
    
    # Analyze patterns across sessions
    print("MULTI-SESSION ANALYSIS:")
    print("-" * 80)
    
    freq = analytics.frequency
    
    print("Emotion frequency across all sessions:")
    for emotion, count in freq.get_emotion_frequency().items():
        percent = (count / analytics.frequency.emotion_counts.total()) * 100
        print(f"  {emotion}: {count} times ({percent:.1f}%)")
    
    print()
    print("Emotional trajectory:")
    centroid = analytics.get_emotional_centroid()
    print(f"  Average state: {centroid.to_dict()}")
    
    print()
    print("Client progress:")
    print("  ✓ Session 1-2: High anxiety (fear dominant)")
    print("  ✓ Session 3: Breakthrough (joy emerging)")
    print("  ✓ Session 4-5: Stable positive state")
    print()
    print("→ Recommend: Begin deeper work on meaning/purpose")
    print("→ Watch for: Potential relapse to fear if triggered")
    print("→ Celebrate: Consistent upward trajectory in sovereignty")
    print()


def example_healing_targets():
    """
    Identify which emotions need the most therapeutic work.
    """
    
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Healing Priority Matrix")
    print("=" * 80)
    print()
    
    analytics = ComprehensiveEmotionAnalytics(data_dir="healing_targets_analytics")
    
    # Simulate emotional data over a week
    week_data = {
        "fear": 28,
        "shame": 12,
        "grief": 8,
        "peace": 45,
        "joy": 35,
        "love": 18,
    }
    
    for emotion, count in week_data.items():
        for _ in range(count):
            analytics.log_emotion(emotion)
    
    print("HEALING PRIORITY ANALYSIS")
    print("-" * 80)
    print()
    
    healing_targets = analytics.get_healing_targets()
    
    if healing_targets:
        print("🎯 PRIMARY HEALING TARGETS (Emotions that reduce sovereignty):")
        print()
        
        for emotion, count in healing_targets.items():
            family = EMOTION_FAMILIES.get(emotion, {})
            severity = family.get("severity", "medium")
            
            print(f"  {emotion.upper()}: {count} occurrences (severity: {severity})")
            print(f"    → Reduces sovereignty to: {family.get('sovereignty', 0)}")
            
            if emotion in MENTAL_PATTERNS:
                print(f"    → Associated patterns: {MENTAL_PATTERNS[emotion]}")
            
            print()
    else:
        print("✨ No primary healing targets! Client in positive emotional space.")
        print()
    
    print("DISTRIBUTION:")
    dist = analytics.frequency.get_emotion_distribution()
    
    positive = ["joy", "peace", "love", "sacred"]
    negative = ["fear", "shame", "grief", "anger"]
    
    positive_percent = sum(dist.get(e, 0) for e in positive)
    negative_percent = sum(dist.get(e, 0) for e in negative)
    
    print(f"  Positive emotions: {positive_percent:.1f}%")
    print(f"  Negative emotions: {negative_percent:.1f}%")
    print()
    
    if negative_percent > 25:
        print("→ RECOMMENDATION: Increase frequency/intensity of interventions")
    else:
        print("→ RECOMMENDATION: Maintain current therapeutic approach")
    print()


if __name__ == "__main__":
    # Run all examples
    example_therapy_session()
    example_multi_session_analysis()
    example_healing_targets()
    
    print("\n" + "=" * 80)
    print("END OF EXAMPLES")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Integrate EmotionPatternAnalytics into sol_module.py")
    print("  2. Wire emotion detection into process_message()")
    print("  3. Add commands to sol_dojo.py for analytics access")
    print("  4. Use exported JSON data to create team dashboards")
    print()
