"""
SOL ANALYTICS QUICK-START GUIDE
═══════════════════════════════════════════════════════════════════════════════

Using sol_analytics.py and sol_emotion_patterns.py for your team dashboard.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 1. BASIC SETUP - Chat & Session Tracking
# ═══════════════════════════════════════════════════════════════════════════════

from modules.sol.sol_analytics import SolAnalytics, ChatTurn, SessionMetrics
from modules.sol.sol_emotion_patterns import EmotionPatternAnalytics, MentalPatternType
import json

# Initialize analytics engines
analytics = SolAnalytics(data_dir="team_dashboard")
emotions = EmotionPatternAnalytics(data_dir="team_dashboard/emotions")

# ═══════════════════════════════════════════════════════════════════════════════
# 2. EXAMPLE: Track a Chat Session
# ═══════════════════════════════════════════════════════════════════════════════

session_id = "session_001_deep_coding"

# Register UUIDs for this session
analytics.register_uuid(session_id, "session", metadata={"type": "work", "task": "system_design"})

# Start session metrics
analytics.start_session(session_id, user_id="souljah", session_type="analysis")

# Log emotional state
emotions.log_emotion(
    emotion_name="focused",
    valence=0.6,      # Positive
    arousal=0.8,      # High energy
    sovereignty=0.85, # Empowered
    intensity=0.7,
    context="Deep system architecture work"
)

# Detect a mental pattern
pattern = emotions.detect_pattern(
    pattern_type=MentalPatternType.ANALYSIS,
    name="Deep System Thinking",
    description="Engaged in complex architecture problem-solving",
    keywords=["kernel", "architecture", "module", "design"],
    severity=0.1,  # Not concerning
    is_helpful=True
)

# Log a chat turn with emotional context
chat_turn = analytics.log_chat_turn(
    session_id=session_id,
    user_message="How should I structure the microkernel for maximum sovereignty?",
    ai_response="Consider separating concerns: kernel manages boot/shutdown, modules handle specifics. Each module gets a sovereignty assertion point.",
    response_time=0.45,  # seconds
    quality_score=0.92,  # 0-1
    emotion="analytical",
    tags=["architecture", "design-pattern"]
)

# Record pattern occurrence (pattern happened again)
emotions.record_pattern_occurrence(pattern.pattern_id, duration_seconds=120)

# Emotional shift during conversation
emotions.log_emotion(
    emotion_name="clarity",
    valence=0.8,      # Even more positive
    arousal=0.7,      # Still engaged
    sovereignty=0.95, # Breakthrough!
    intensity=0.8,
    context="Solution emerged during thinking"
)

# Detect breakthrough pattern
breakthrough = emotions.detect_pattern(
    pattern_type=MentalPatternType.BREAKTHROUGH,
    name="Architectural Insight",
    description="Sudden clarity on system-wide pattern",
    keywords=["insight", "solution", "clarity"],
    severity=0.0,
    is_helpful=True
)

# More chat with the insight
analytics.log_chat_turn(
    session_id=session_id,
    user_message="I see - sovereignty should be the first-class object!",
    ai_response="Exactly. Make sovereignty a primitive. Every module inherits it. Guards check it. It's not bolted on—it's foundational.",
    response_time=0.38,
    quality_score=0.95,
    emotion="clear",
    tags=["breakthrough", "design-principle"]
)

# End the session
analytics.end_session(
    session_id=session_id,
    outcome="completed",
    notes="Major architectural breakthrough - microkernel design clarified"
)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. GENERATE CHARTS & REPORTS
# ═══════════════════════════════════════════════════════════════════════════════

# Export all data to CSV/JSON
dashboard_files = analytics.export_team_dashboard(output_dir="team_dashboard")
emotion_reports = emotions.export_team_report()

print("📊 Chat Analytics Files:")
for name, filepath in dashboard_files.items():
    print(f"  - {name}: {filepath}")

print("\n💭 Emotion & Pattern Files:")
for name, filepath in emotion_reports.items():
    print(f"  - {name}: {filepath}")

# Get visualization-ready data (for Tableau, Excel charts, web dashboards)
chat_data = analytics.get_dashboard_json()
emotion_data = emotions.get_team_dashboard_data()

print("\n✅ Dashboard Data Keys Available:")
print("Chat Analytics:")
for key in chat_data.keys():
    print(f"    - {key}")
print("\nEmotion & Patterns:")
for key in emotion_data.keys():
    print(f"    - {key}")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. EXAMPLE: MULTI-SESSION TEAM ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

"""
For a team dashboard, aggregate multiple sessions:
"""

sessions = [
    ("session_001", "souljah", "focus"),
    ("session_002", "souljah", "creative_breakthrough"),
    ("session_003", "ai_assistant", "support_role"),
]

for sess_id, user, session_type in sessions:
    analytics.register_uuid(sess_id, "session", metadata={"user": user, "type": session_type})
    analytics.start_session(sess_id, user_id=user, session_type=session_type)
    
    # Simulate different emotion profiles
    if session_type == "focus":
        emotions.log_emotion("focused", 0.6, 0.8, 0.85, context="Deep work")
    elif session_type == "creative_breakthrough":
        emotions.log_emotion("inspired", 0.9, 0.7, 0.9, context="Creative flow")
    else:
        emotions.log_emotion("supportive", 0.7, 0.5, 0.8, context="Helping others")
    
    analytics.log_chat_turn(sess_id, "test message", "test response", 0.3, 0.9)
    analytics.end_session(sess_id, outcome="completed")

# ═══════════════════════════════════════════════════════════════════════════════
# 5. EXAMPLE: DIMENSION & PATTERN DEEP DIVE
# ═══════════════════════════════════════════════════════════════════════════════

"""
Track emotional dimension space for a complete session:
"""

# Log emotions with specific dimensions
emotions.log_emotion("anxious", valence=-0.6, arousal=0.9, sovereignty=0.4, context="Before big decision")
emotions.log_emotion("resolved", valence=0.7, arousal=0.6, sovereignty=0.95, context="After decision made")
emotions.log_emotion("peaceful", valence=0.8, arousal=0.3, sovereignty=0.9, context="Rest after effort")

# Get dimensional stats
dimensional_info = emotions.get_dimensional_stats()
print("\n📊 DIMENSIONAL ANALYSIS")
print("─" * 50)
for dim, stats in dimensional_info.items():
    print(f"\n{dim.upper()}:")
    for stat_name, value in stats.items():
        print(f"  {stat_name}: {value}")

# Get emotional trajectory
trajectory = emotions.get_dimensional_trajectory(window_size=5)
print(f"\n📈 Recent Trajectory (last {len(trajectory)} snapshots):")
for i, point in enumerate(trajectory, 1):
    print(f"  {i}. {point['emotion_label']}: V={point['valence']:.2f}, A={point['arousal']:.2f}, S={point['sovereignty']:.2f}")

# Find recurring clusters in emotional space
clusters = emotions.get_dimensional_clusters()
print(f"\n🎯 Recurring Emotional States ({len(clusters)} clusters):")
for cluster_id, frequency in list(clusters.items())[:5]:
    print(f"  {cluster_id}: {frequency} occurrences")

# ═══════════════════════════════════════════════════════════════════════════════
# 6. PATTERN ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print("\n\n🧠 MENTAL PATTERN ANALYSIS")
print("─" * 50)

# What patterns are most common?
pattern_freq = emotions.get_pattern_frequency()
print("\nMost Frequent Patterns:")
for pattern_name, count in list(pattern_freq.items())[:5]:
    print(f"  {pattern_name}: {count} occurrences")

# What patterns are problematic?
problematic = emotions.get_problematic_patterns()
print(f"\n⚠️  Concerning Patterns ({len(problematic)} detected):")
for pattern in problematic:
    print(f"  • {pattern.name} (severity: {pattern.severity:.1%})")
    if pattern.keywords:
        print(f"    Keywords: {', '.join(pattern.keywords[:3])}")

# Pattern transitions (what follows what?)
transitions = emotions.get_transition_network()
print("\n🔄 Pattern Transitions (Common Sequences):")
for from_pattern, to_patterns in list(transitions.items())[:3]:
    print(f"  From: {from_pattern}")
    for to_pattern, count in list(to_patterns.items())[:2]:
        print(f"    → {to_pattern}: {count}x")

# ═══════════════════════════════════════════════════════════════════════════════
# 7. CORRELATION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print("\n\n🔗 CORRELATION ANALYSIS")
print("─" * 50)

# Which emotions go with which patterns?
correlations = emotions.get_emotion_pattern_correlations()
print("\nEmotion-Pattern Correlations:")
for emotion, patterns in list(correlations.items())[:3]:
    print(f"  {emotion}:")
    for pattern_id in list(patterns)[:3]:
        pattern = emotions._patterns.get(pattern_id)
        if pattern:
            print(f"    • {pattern.name}")

# ═══════════════════════════════════════════════════════════════════════════════
# 8. EXCEL/TABLEAU READY DATA
# ═══════════════════════════════════════════════════════════════════════════════

"""
Use this data with Excel, Google Sheets, Tableau, or any BI tool:
"""

# Get all data as JSON (ready for Excel import)
full_data = emotions.get_team_dashboard_data()

# Save as JSON for import
import json
with open("team_dashboard/full_dashboard.json", 'w') as f:
    json.dump(full_data, f, indent=2)

print("\n\n📈 TEAM DASHBOARD FILES CREATED:")
print("  ✅ team_dashboard/emotion_log.csv - All emotion snapshots")
print("  ✅ team_dashboard/pattern_analysis.csv - Mental patterns detected")  
print("  ✅ team_dashboard/dimensional_trajectory.csv - 3D emotional space")
print("  ✅ team_dashboard/emotions/emotion_pattern_summary.json - Complete analysis")
print("  ✅ team_dashboard/full_dashboard.json - All data combined")

print("\n💡 Import these CSVs into Excel or Tableau to create:")
print("  📊 Emotion frequency histogram")
print("  📈 Arousal vs Valence scatter plot")
print("  🔄 Pattern transition flow diagram")
print("  🎯 Dimensional space 3D visualization")
print("  📋 Pattern severity ranking")
print("  ⏱️  Session timeline with emotions")

# ═══════════════════════════════════════════════════════════════════════════════
# 9. QUICK STATS SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

print("\n\n📊 QUICK SUMMARY")
print("─" * 50)
print(f"Total emotions logged: {len(emotions._emotions)}")
print(f"Unique emotion types: {len(emotions._emotion_frequency)}")
print(f"Mental patterns detected: {len(emotions._patterns)}")
print(f"Pattern transitions recorded: {len(emotions._transitions)}")
print(f"Sessions tracked: {len(analytics._session_metrics)}")
print(f"Chat turns recorded: {len(analytics._chat_turns)}")
print(f"UUIDs registered: {len(analytics._uuid_records)}")

# ═══════════════════════════════════════════════════════════════════════════════
# 10. RE-USE IN SOL MODULES (Integration Example)
# ═══════════════════════════════════════════════════════════════════════════════

"""
Integrate into sol_module.py:

class SolModule:
    def __init__(self, ...):
        self.analytics = SolAnalytics()
        self.emotions = EmotionPatternAnalytics()
    
    def process_message(self, user_message, chat_history):
        # Detect emotion from message
        detected_emotion = self._detect_emotion(user_message)
        self.emotions.log_emotion(detected_emotion, ...)
        
        # Detect patterns
        patterns = self._analyze_patterns(user_message)
        for pattern_type, pattern_data in patterns.items():
            self.emotions.detect_pattern(pattern_type, ...)
        
        # Log chat turn with metadata
        self.analytics.log_chat_turn(
            self.current_session_id,
            user_message,
            response,
            response_time=elapsed,
            quality_score=confidence,
            emotion=detected_emotion
        )
        
        # Export on demand
        if should_report:
            files = self.analytics.export_team_dashboard()
            emotion_files = self.emotions.export_team_report()
"""

print("\n✅ SOL Analytics Ready for Your Team Dashboard!")
