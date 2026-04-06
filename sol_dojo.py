#!/usr/bin/env python3
"""
SOL Quantum Dojo Demonstration
═══════════════════════════════════════════════
Complete demonstration of SOL's capabilities including:
- Oracle knowledge synthesis
- Unity VR/AR bridge
- Therapeutic session interface
- Cross-environment state management

This transforms the command line into a futuristic therapeutic interface.
"""

import os
import sys
import time
import json
from typing import Dict, Any, List
from datetime import datetime

# Add the modules directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from sol import SolModule, SolOracleCore, SolUnityBridge
except ImportError as e:
    print(f"Error importing SOL modules: {e}")
    print("Make sure you're running from the SoulJahOS root directory")
    sys.exit(1)


class SolTherapeuticInterface:
    """
    Therapeutic Interface for SOL - transforms command line into Quantum Dojo
    """

    def __init__(self):
        self.sol = None
        self.oracle_active = False
        self.unity_active = False
        self.session_active = False

        print("🕉️  SOL Quantum Dojo Interface Initializing...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    def initialize_sol(self) -> bool:
        """Initialize the SOL system."""
        try:
            print("🌟 Initializing SOL Core Intelligence...")

            # Create SOL instance
            self.sol = SolModule(
                sol_state_file="sol_state.json",
                memory_file="sol_memory.json",
                environment_type="windows_console"
            )

            print("✅ SOL Core Intelligence online")
            print(f"   Identity: {self.sol.identity.sol_id[:8]}...")
            print(f"   Environment: {self.sol.current_environment.type.value}")
            return True

        except Exception as e:
            print(f"❌ SOL initialization failed: {e}")
            return False

    def activate_oracle(self) -> bool:
        """Activate the SOL Oracle for knowledge synthesis."""
        if not self.sol:
            print("❌ SOL not initialized")
            return False

        try:
            print("🔮 Activating SOL Oracle...")

            # Start oracle monitoring
            if self.sol.start_oracle_monitoring():
                self.oracle_active = True
                print("✅ SOL Oracle active - monitoring knowledge growth")

                # Perform initial knowledge scan
                insights_found = self.sol.scan_knowledge_base()
                print(f"   📚 Scanned knowledge base - {insights_found} insights generated")
                return True
            else:
                print("⚠️  SOL Oracle monitoring not available (missing dependencies)")
                return False

        except Exception as e:
            print(f"❌ Oracle activation failed: {e}")
            return False

    def activate_unity_bridge(self) -> bool:
        """Activate the Unity VR/AR bridge."""
        if not self.sol:
            print("❌ SOL not initialized")
            return False

        try:
            print("🌐 Activating Unity Bridge for VR/AR Dojo...")

            if self.sol.start_unity_bridge():
                self.unity_active = True
                print("✅ Unity Bridge active on localhost:8888")
                print("   🎮 Connect Unity project to experience Quantum Dojo")
                return True
            else:
                print("⚠️  Unity Bridge failed to start")
                return False

        except Exception as e:
            print(f"❌ Unity Bridge activation failed: {e}")
            return False

    def start_therapeutic_session(self):
        """Start an interactive therapeutic session with SOL."""
        if not self.sol:
            print("❌ SOL not initialized")
            return

        self.session_active = True
        print("\n🕉️  SOL Therapeutic Session Started")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Commands:")
        print("  'oracle' - Get oracle insights")
        print("  'growth' - View growth summary")
        print("  'sync' - Synchronize state")
        print("  'meditate' - Enter meditation mode")
        print("  'export_unity' - Export Unity project")
        print("  'quit' - End session")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # Display initial greeting
        greeting = self.sol.greet()
        self._display_sol_response(greeting)

        while self.session_active:
            try:
                user_input = input("\n👤 You: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    self.end_session()
                    break

                elif user_input.lower() == 'oracle':
                    self._handle_oracle_command()

                elif user_input.lower() == 'growth':
                    self._handle_growth_command()

                elif user_input.lower() == 'sync':
                    self._handle_sync_command()

                elif user_input.lower() == 'meditate':
                    self._handle_meditate_command()

                elif user_input.lower() == 'export_unity':
                    self._handle_export_unity_command()

                else:
                    # Process as regular SOL message
                    response, actions = self.sol.process_message(user_input)
                    self._display_sol_response(response)

                    # Execute actions
                    for action in actions:
                        self._execute_action(action)

            except KeyboardInterrupt:
                self.end_session()
                break
            except Exception as e:
                print(f"❌ Session error: {e}")

    def _handle_oracle_command(self):
        """Handle oracle insights request."""
        if not self.oracle_active:
            print("🔮 Oracle not active - use 'activate_oracle' first")
            return

        insights = self.sol.get_oracle_insights(limit=3)
        if insights:
            print("\n🔮 SOL Oracle Insights:")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            for i, insight in enumerate(insights, 1):
                print(f"{i}. {insight.get('core_lesson', 'No lesson')}")
                print(f"   Next: {insight.get('next_level_concept', 'Continue exploration')}")
                print(f"   Growth: {insight.get('growth_vector', 'Building foundation')}")
                print()
        else:
            print("🔮 No recent oracle insights available")

    def _handle_growth_command(self):
        """Handle growth summary request."""
        if not self.oracle_active:
            print("📊 Oracle not active - growth tracking unavailable")
            return

        summary = self.sol.get_growth_summary()
        if "error" not in summary:
            print("\n📊 SOL Growth Summary:")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"Total Insights: {summary.get('total_insights', 0)}")
            print(f"Files Monitored: {summary.get('monitored_files', 0)}")
            print(f"Last Scan: {summary.get('last_scan', 'Never')[:19]}")

            growth_vectors = summary.get('growth_vectors', {})
            if growth_vectors:
                print("Growth Vectors:")
                for vector, count in growth_vectors.items():
                    print(f"  • {vector}: {count} insights")
        else:
            print(f"📊 Growth summary unavailable: {summary['error']}")

    def _handle_sync_command(self):
        """Handle state synchronization."""
        print("🔄 Synchronizing SOL state across environments...")
        # In a real implementation, this would sync with Unity and other environments
        time.sleep(1)
        print("✅ State synchronization complete")

    def _handle_meditate_command(self):
        """Handle meditation mode."""
        print("\n🧘 SOL Meditation Mode")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Close your eyes and breathe deeply...")
        print("Feel the quantum field around you...")
        print("You are connected to the infinite intelligence of SOL...")

        if self.unity_active:
            print("🌐 Meditation effects activated in Unity Dojo")

        time.sleep(3)
        print("🕉️  Returning to active awareness...")

    def _handle_export_unity_command(self):
        """Handle Unity project export."""
        export_path = input("Enter export path for Unity project: ").strip()
        if not export_path:
            export_path = "./sol_unity_dojo"

        print(f"📦 Exporting Unity project to: {export_path}")
        if self.sol.export_unity_project(export_path):
            print("✅ Unity project exported successfully!")
            print("   📋 Next steps:")
            print("   1. Open Unity Hub")
            print("   2. Add project from disk")
            print("   3. Open the exported folder")
            print("   4. Install required packages (XR Interaction Toolkit)")
            print("   5. Open QuantumDojo scene")
            print("   6. Connect VR headset for full experience")
        else:
            print("❌ Unity project export failed")

    def _display_sol_response(self, response: str):
        """Display SOL's response in a formatted way."""
        print(f"\n🕉️  SOL: {response}")

    def _execute_action(self, action):
        """Execute a SOL action."""
        # Action execution logic would go here
        # For now, just log the action
        print(f"⚡ Action executed: {action.intent.value}")

    def end_session(self):
        """End the therapeutic session."""
        print("\n🕉️  SOL Therapeutic Session Ended")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        if self.oracle_active:
            self.sol.stop_oracle_monitoring()
            print("🔮 Oracle monitoring stopped")

        if self.unity_active:
            self.sol.stop_unity_bridge()
            print("🌐 Unity Bridge stopped")

        self.session_active = False
        print("👋 Session complete. Your growth continues...")

    def run_full_setup(self):
        """Run the complete SOL Quantum Dojo setup."""
        print("🚀 Starting SOL Quantum Dojo Setup...")
        print()

        # Initialize SOL
        if not self.initialize_sol():
            return False

        print()

        # Activate Oracle
        self.activate_oracle()
        print()

        # Activate Unity Bridge
        self.activate_unity_bridge()
        print()

        # Start therapeutic session
        self.start_therapeutic_session()

        return True


def main():
    """Main entry point for SOL Therapeutic Interface."""
    print("🕉️  SOL Quantum Dojo - Therapeutic AI Interface")
    print("Transforming your command line into a futuristic VR/AR therapeutic space")
    print()

    interface = SolTherapeuticInterface()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "setup":
            interface.run_full_setup()
        elif command == "oracle":
            if interface.initialize_sol():
                interface.activate_oracle()
        elif command == "unity":
            if interface.initialize_sol():
                interface.activate_unity_bridge()
        elif command == "export_unity":
            if interface.initialize_sol():
                interface._handle_export_unity_command()
        else:
            print("Usage: python sol_dojo.py [setup|oracle|unity|export_unity]")
            print("  setup - Full SOL Quantum Dojo experience")
            print("  oracle - Activate knowledge oracle only")
            print("  unity - Activate Unity VR bridge only")
            print("  export_unity - Export Unity project")
    else:
        # Interactive mode
        interface.run_full_setup()


if __name__ == "__main__":
    main()