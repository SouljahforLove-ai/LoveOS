#!/usr/bin/env python3
"""
INTEGRATION EXAMPLE: Using Emotion Analytics in SOL
═══════════════════════════════════════════════════════════════════════════════
Shows how to integrate emotion tracking into the SOL module.

This is a minimal example of how to wire emotion analytics into your system.
"""

import sys
import os

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from sol.sol_emotion_mathematics import ComprehensiveEmotionAnalytics, EMOTION_FAMILIES

def simple_emotion_tracker():
    """Simple example: Track a conversation with emotion awareness."""
    
    print("🧠 SOL Emotion Tracking Example")
    print("=" * 80)
    
    # Initialize emotion analytics
    emotion_system = ComprehensiveEmotionAnalytics(data_dir="demo_session")
    
    # Simulate a therapeutic conversation
    conversation_flow = [
        {
            "user": "I'm feeling overwhelmed with my project",
            "detected_emotion": "fear",
            "detected_pattern": "catastrophizing",
            "ai_response": "I notice you're in fear (arousal: 0.8). Let's break this down into smaller steps."
        },
        {
            "user": "That helps. I actually made good progress yesterday",
            "detected_emotion": "peace",
            "detected_pattern": None,
            "ai_response": "Good. You're moving toward peace (sovereignty: 1.0). Build on that momentum."
        },
        {
            "user": "I realize this aligns with my growth goals",
            "detected_emotion": "joy",
            "detected_pattern": "meaning_making",
            "ai_response": "Exactly. You've found the meaning. That's joy + sacred awareness."
        }
    ]
    
    print("\n📝 Simulating therapeutic conversation:\n")
    
    for i, turn in enumerate(conversation_flow, 1):
        print(f"Turn {i}:")
        print(f"  User: {turn['user']}")
        
        # Log the detected emotion
        emotion_system.log_emotion(
            emotion_name=turn['detected_emotion'],
            context=turn['user']
        )
        print(f"  ✓ Emotion detected: {turn['detected_emotion']}")
        
        # Log pattern if detected
        if turn['detected_pattern']:
            emotion_system.log_mental_pattern(
                pattern_type=turn['detected_pattern'],
                emotion_context=turn['detected_emotion'],
                triggered_by=turn['user']
            )
            print(f"  ✓ Pattern detected: {turn['detected_pattern']}")
        
        print(f"  SOL: {turn['ai_response']}")
        print()
    
    # Generate insights
    print("=" * 80)
    print("\n📊 Session Analysis:\n")
    
    emotion_report = emotion_system.get_emotion_report()
    
    print("Emotion Frequency:")
    for emotion, count in emotion_report['emotion_frequency'].items():
        family = EMOTION_FAMILIES.get(emotion, {})
        healing = "⚠️ HEALING TARGET" if family.get('healing_target') else ""
        print(f"  • {emotion}: {count} {healing}")
    
    print(f"\nDimensional Profile (Session Average):")
    for dim, val in emotion_report['dimensional_profile'].items():
        bar = "█" * int(max(abs(val), 0) * 20)
        print(f"  {dim:15s}: {val:+.2f} {bar}")
    
    print(f"\nVolatility Score: {emotion_report['volatility_score']:.3f}")
    if emotion_report['volatility_score'] < 0.3:
        print("  → Client is emotionally stable ✓")
    elif emotion_report['volatility_score'] < 0.7:
        print("  → Client has moderate emotional fluctuation")
    else:
        print("  → Client experiencing high emotional volatility")
    
    if emotion_report['healing_targets']:
        print(f"\nHealing Targets (Emotions needing work):")
        for emotion, freq in emotion_report['healing_targets'].items():
            print(f"  • {emotion}: {freq} occurrences → Recommend intervention")
    
    # Export for team
    print("\n🎯 Exporting for team dashboard:")
    exports = emotion_system.export_team_analytics()
    for export_type, path in exports.items():
        print(f"  ✓ {export_type}: {path}")
    
    return emotion_system


def usage_in_sol_module():
    """
    Show how to integrate this into sol_module.py
    """
    print("\n" + "=" * 80)
    print("\n💡 HOW TO INTEGRATE INTO sol_module.py:\n")
    
    example_code = '''
# In sol_module.py __init__:
from .sol_emotion_mathematics import ComprehensiveEmotionAnalytics

class SolModule:
    def __init__(self, ...):
        # ... existing code ...
        
        # Initialize emotion analytics
        self.emotion_analytics = ComprehensiveEmotionAnalytics(
            data_dir=f"sessions/{self.current_session_id}/emotions"
        )
    
    def process_message(self, user_message: str) -> str:
        """Process with emotion awareness."""
        
        # 1. Detect emotion in user message
        emotion = self._detect_emotion(user_message)
        if emotion:
            self.emotion_analytics.log_emotion(emotion, context=user_message)
        
        # 2. Process message normally
        response = self.reason_and_reflect(user_message)
        
        # 3. Detect patterns
        patterns = self._detect_patterns(user_message)
        for pattern_type in patterns:
            self.emotion_analytics.log_mental_pattern(
                pattern_type=pattern_type,
                emotion_context=emotion
            )
        
        return response
    
    def _detect_emotion(self, text: str) -> str:
        """Simple keyword-based emotion detection."""
        keywords = {
            "fear": ["worried", "anxious", "afraid", "scared"],
            "joy": ["happy", "excited", "delighted", "great"],
            "peace": ["calm", "peaceful", "serene"],
            # ... etc
        }
        for emotion, words in keywords.items():
            if any(w in text.lower() for w in words):
                return emotion
        return "neutral"
    
    # Commands for dojo
    def emotion_status(self):
        report = self.emotion_analytics.get_emotion_report()
        return json.dumps(report, indent=2)
    
    def export_emotion_analytics(self):
        return self.emotion_analytics.export_team_analytics()
'''
    
    print(example_code)


if __name__ == "__main__":
    try:
        # Run the example
        emotion_system = simple_emotion_tracker()
        
        # Show integration example
        usage_in_sol_module()
        
        print("\n" + "=" * 80)
        print("✅ Integration example complete!")
        print("\nYou now have:")
        print("  ✓ Working emotion tracking system")
        print("  ✓ Analytics exports for your team")
        print("  ✓ Clear integration pattern to add to your code")
        print("\nNext steps:")
        print("  1. Add emotion detection to sol_module.py")
        print("  2. Test with real conversations")
        print("  3. Create team dashboards from exports")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
