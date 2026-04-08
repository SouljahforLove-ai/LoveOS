#!/usr/bin/env python3
"""
SOL Test Script
Demonstrates the SOL system in action
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.jarvus.jarvus_module import SolModule

def main():
    print("Initializing SOL...")
    sol = SolModule()

    print("\n" + "="*50)
    print("SOL Oracle & Operator")
    print("="*50)

    # Greeting
    greeting = sol.greet()
    print(f"\n{greeting}")

    # Simulate conversation
    chat_history = []

    test_messages = [
        "I'm working on the SOL implementation",
        "This is taking longer than expected",
        "I need to focus on the core logic",
        "Late night coding session here"
    ]

    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Message {i} ---")
        print(f"User: {message}")

        response, actions = sol.process_message(message, chat_history)

        # Add to chat history
        chat_history.append({"message": message, "response": response})

        print(f"SOL: {response}")

        if actions:
            print("Actions:")
            for action in actions:
                print(f"  - {action.intent.value}: {getattr(action, 'field', '')} = {getattr(action, 'value', '')}")

    print(f"\n--- Session Summary ---")
    print(sol.get_session_summary())

    print("\nSOL session complete.")

if __name__ == "__main__":
    main()