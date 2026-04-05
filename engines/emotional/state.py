"""
Emotional State — LoveOS
Tracks current emotion + history.
"""

from collections import deque

class EmotionalState:
    def __init__(self, history_size: int = 20):
        self.current = None
        self.history = deque(maxlen=history_size)

    def update(self, snapshot: dict):
        self.current = snapshot
        self.history.append(snapshot)

    def get_state(self) -> dict:
        return {
            "current": self.current,
            "history": list(self.history),
        }
