from rituals.grounding.breathe import ground_breathing
from kernel.ritual_dispatcher import RitualDispatcher

def syscall_breathe():
    dispatcher = RitualDispatcher()
    return dispatcher.dispatch(ground_breathing)
from engines.emotional.tagger import tag_emotion

def syscall_emotion_tag(text: str):
    return tag_emotion(text)
