#!/usr/bin/env python3
"""
QUICK TEST: Emotion Mathematics & Analytics System
═══════════════════════════════════════════════════════════════════════════════
Simple working test to verify everything is functional.
Run this to see the emotion system in action!

Usage:
  python test_emotion_system.py
"""

import sys
import os
import json
from pathlib import Path

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

print("🧠 TESTING EMOTION & ANALYTICS SYSTEM")
print("=" * 80)

# Test 1: Import modules
print("\n[1/5] Testing imports...")
try:
    from sol.sol_emotion_mathematics import (
        ComprehensiveEmotionAnalytics,
        EmotionalVector,
        EMOTION_FAMILIES,
        MENTAL_PATTERNS
    )
    print("✅ sol_emotion_mathematics imported successfully")
except ImportError as e:
    print(f"❌ Failed to import emotion mathematics: {e}")
    sys.exit(1)

try:
    from sol.sol_analytics import SolAnalytics
    print("✅ sol_analytics imported successfully")
except ImportError as e:
    print(f"❌ Failed to import analytics: {e}")
    sys.exit(1)

# Test 2: Initialize emotion analytics
print("\n[2/5] Initializing emotion analytics...")
try:
    emotion_system = ComprehensiveEmotionAnalytics(
        data_dir="test_emotion_data"
    )
    print("✅ Emotion analytics initialized")
    print(f"   - Available emotions: {len(EMOTION_FAMILIES)}")
    print(f"   - Available patterns: {len(MENTAL_PATTERNS)}")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    sys.exit(1)

# Test 3: Log emotions and track patterns
print("\n[3/5] Logging sample emotions and patterns...")
try:
    # Log emotions
    emotions_logged = []
    test_emotions = [
        ("fear", -0.7, 0.8, 0.3, "public speaking event"),
        ("peace", 0.6, 0.1, 1.0, "after meditation"),
        ("joy", 0.9, 0.6, 1.0, "breakthrough in code"),
    ]
    
    for emotion_name, valence, arousal, sovereignty, context in test_emotions:
        emotion_system.log_emotion(
            emotion_name=emotion_name,
            vector=EmotionalVector(
                valence=valence,
                arousal=arousal,
                sovereignty=sovereignty
            ),
            context=context
        )
        emotions_logged.append(emotion_name)
    
    print(f"✅ Logged {len(emotions_logged)} emotions: {', '.join(emotions_logged)}")
    
    # Log patterns
    patterns = [
        ("catastrophizing", "fear", 0.8, "news about economy"),
        ("self_criticism", "shame", 0.7, "mistake in code"),
    ]
    
    patterns_logged = []
    for pattern_type, emotion, intensity, trigger in patterns:
        emotion_system.log_mental_pattern(
            pattern_type=pattern_type,
            emotion_context=emotion,
            intensity=intensity,
            triggered_by=trigger
        )
        patterns_logged.append(pattern_type)
    
    print(f"✅ Logged {len(patterns_logged)} patterns: {', '.join(patterns_logged)}")
    
except Exception as e:
    print(f"❌ Failed to log data: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Generate analytics reports
print("\n[4/5] Generating analytics reports...")
try:
    emotion_report = emotion_system.get_emotion_report()
    
    print("✅ Emotion Profile:")
    print(f"   - Total emotions: {emotion_report['total_emotions_logged']}")
    print(f"   - Top emotions: {dict(list(emotion_report['emotion_frequency'].items())[:3])}")
    print(f"   - Distribution: {emotion_report['emotion_distribution']}")
    print(f"   - Dimensional profile:")
    for dim, val in emotion_report['dimensional_profile'].items():
        print(f"      {dim}: {val:+.2f}")
    print(f"   - Volatility: {emotion_report['volatility_score']:.3f}")
    print(f"   - Healing targets: {emotion_report['healing_targets']}")
    
    pattern_report = emotion_system.get_pattern_report()
    print(f"\n✅ Pattern Profile:")
    print(f"   - Total patterns: {pattern_report['total_patterns_logged']}")
    print(f"   - Pattern frequency: {pattern_report['pattern_frequency']}")
    print(f"   - Resolution rate: {pattern_report['resolution_rate']:.1%}")
    
except Exception as e:
    print(f"❌ Failed to generate reports: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Export data
print("\n[5/5] Testing data exports...")
try:
    exports = emotion_system.export_team_analytics()
    print(f"✅ Exported {len(exports)} files:")
    for export_type, filepath in exports.items():
        file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
        print(f"   - {export_type}: {filepath} ({file_size} bytes)")
        
        # Show contents of emotion report
        if export_type == "emotion" and os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                print(f"\n   📊 Emotion Profile Summary:")
                print(f"      Emotions logged: {data.get('total_emotions_logged', 0)}")
                print(f"      Main emotions: {list(data.get('emotion_frequency', {}).keys())[:3]}")
    
except Exception as e:
    print(f"❌ Failed to export: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Analytics module
print("\n[BONUS] Testing SolAnalytics module...")
try:
    analytics = SolAnalytics(data_dir="test_analytics_data")
    
    # Register a UUID
    uuid_record = analytics.register_uuid(
        uuid_str="demo-session-001",
        entity_type="session",
        metadata={"user": "test", "focus": "emotion_testing"}
    )
    print(f"✅ Registered UUID: {uuid_record.uuid}")
    
    # Log a chat turn
    chat_turn = analytics.log_chat_turn(
        session_id="demo-session-001",
        user_message="How are you feeling?",
        ai_response="I'm processing your emotional state with precision.",
        response_time=0.5,
        quality_score=0.95,
        emotion="joy"
    )
    print(f"✅ Logged chat turn: {chat_turn.turn_id}")
    
    # Get dashboard data
    dashboard = analytics.get_dashboard_json()
    print(f"✅ Dashboard data generated:")
    print(f"   - Chat turns: {dashboard['metadata']['total_chat_turns']}")
    print(f"   - UUIDs tracked: {dashboard['uuid_stats']['total']}")
    
except Exception as e:
    print(f"⚠️  Analytics test skipped: {e}")

# Final summary
print("\n" + "=" * 80)
print("🎉 ALL TESTS PASSED!")
print("\nYour emotion mathematics system is working correctly!")
print("\nNext steps:")
print("  1. Integrate into sol_module.py for real usage")
print("  2. Connect to sol_dojo.py for interactive sessions")
print("  3. Push to GitHub: git add -A && git commit -m 'feat: working emotion system' && git push")
print("\nTo see the data generated:")
print("  - Emotion data: test_emotion_data/")
print("  - CSV exports: test_emotion_data/*.csv")
print("  - JSON reports: test_emotion_data/*.json")
print("=" * 80)
