from rituals.grounding.breathe import ground_breathing
from kernel.ritual_dispatcher import RitualDispatcher
from engines.emotional.tagger import score_emotions
from engines.emotional.state import EmotionalState

_emotional_state = EmotionalState()

def syscall_breathe():
    dispatcher = RitualDispatcher()
    return dispatcher.dispatch(ground_breathing)

def syscall_emotion_tag(text: str):
    snapshot = score_emotions(text)
    _emotional_state.update(snapshot)
    return snapshot

def syscall_emotion_get_state():
    return _emotional_state.get_state()
