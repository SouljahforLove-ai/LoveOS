#!/usr/bin/env python3
"""
SOL Oracle Test Script
Demonstrates the knowledge synthesis and growth analysis capabilities.
"""

import os
import sys
import time

# Add modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

from sol import SolModule

def test_oracle_functionality():
    """Test the SOL Oracle knowledge synthesis."""
    print("🕉️  SOL Oracle Test")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Initialize SOL
    print("Initializing SOL...")
    sol = SolModule()

    # Test basic functionality
    print("Testing basic SOL functionality...")
    greeting = sol.greet()
    print(f"SOL Greeting: {greeting}")

    # Test oracle activation
    print("\nActivating Oracle...")
    oracle_started = sol.start_oracle_monitoring()
    if oracle_started:
        print("✅ Oracle monitoring started")

        # Perform knowledge scan
        print("Scanning knowledge base...")
        insights_found = sol.scan_knowledge_base()
        print(f"📚 Found {insights_found} insights")

        # Get recent insights
        print("\nRecent Oracle Insights:")
        insights = sol.get_oracle_insights(limit=3)
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight.get('core_lesson', 'No insight')}")
            print(f"   Next level: {insight.get('next_level_concept', 'Continue')}")
            print()

        # Get growth summary
        print("Growth Summary:")
        summary = sol.get_growth_summary()
        if "error" not in summary:
            print(f"Total insights: {summary.get('total_insights', 0)}")
            print(f"Files monitored: {summary.get('monitored_files', 0)}")
        else:
            print(f"Summary error: {summary['error']}")

        # Stop oracle
        sol.stop_oracle_monitoring()
        print("🔮 Oracle monitoring stopped")

    else:
        print("⚠️  Oracle monitoring not available")

    # Test message processing
    print("\nTesting SOL message processing...")
    test_messages = [
        "I've been working on understanding quantum computing",
        "How can I improve my development workflow?",
        "What patterns do you see in my growth?"
    ]

    for msg in test_messages:
        print(f"\n👤 You: {msg}")
        response, actions = sol.process_message(msg)
        print(f"🕉️  SOL: {response}")
        if actions:
            print(f"⚡ Actions: {len(actions)} triggered")

    print("\n✅ SOL Oracle test complete!")

def test_unity_bridge():
    """Test the Unity VR/AR bridge."""
    print("\n🌐 Testing Unity Bridge...")
    sol = SolModule()

    # Test Unity bridge activation
    bridge_started = sol.start_unity_bridge()
    if bridge_started:
        print("✅ Unity Bridge started on localhost:8888")

        # Test script generation
        scripts = sol.get_unity_scripts()
        print(f"📦 Generated {len(scripts)} Unity scripts")

        # Stop bridge
        sol.stop_unity_bridge()
        print("🌐 Unity Bridge stopped")
    else:
        print("⚠️  Unity Bridge not available")

def test_alchemist_logic():
    """Test the Alchemist logic for data transmutation."""
    print("\n🔮 Testing Alchemist Logic...")
    sol = SolModule()

    # Test data transmutation
    test_data = "I've been learning about neural networks and finding it challenging but rewarding."

    result = sol.transmute_data(test_data)
    if result.get("transmutation_complete"):
        legacy = result.get("legacy_gold", {})
        print("✅ Data transmutation successful!")
        print(f"Legacy Gold: {legacy.get('reflection', 'No reflection')}")
        print(f"Guidance: {legacy.get('guidance', 'No guidance')}")
    else:
        print("❌ Data transmutation failed")

if __name__ == "__main__":
    try:
        test_oracle_functionality()
        test_unity_bridge()
        test_alchemist_logic()

        print("\n🎉 All SOL tests completed!")
        print("\nTo start the full Quantum Dojo experience:")
        print("  python sol_dojo.py setup")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()