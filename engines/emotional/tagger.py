"""
Emotion Tagger — LoveOS
Automatically classifies emotional state from signals.
"""

EMOTION_KEYWORDS = {
    "anger": ["mad", "angry", "irritated", "pissed", "frustrated"],
    "fear": ["scared", "afraid", "worried", "anxious"],
    "sadness": ["sad", "down", "hurt", "cry"],
    "love": ["love", "warm", "grateful", "connected"],
    "hope": ["hope", "faith", "believe"],
    "overwhelm": ["overwhelmed", "too much", "can't"],
    "numbness": ["numb", "empty", "nothing"],
}

def tag_emotion(text: str) -> dict:
    text = text.lower()
    for emotion, keywords in EMOTION_KEYWORDS.items():
        if any(k in text for k in keywords):
            return {"emotion": emotion, "confidence": 0.8}
    return {"emotion": "neutral", "confidence": 0.5}
