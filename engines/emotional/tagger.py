"""
Emotion Tagger — SoulJahOS
Multi-emotion scoring + dominant label.
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

def score_emotions(text: str) -> dict:
    text = text.lower()
    scores = {e: 0.0 for e in EMOTION_KEYWORDS.keys()}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for k in keywords:
            if k in text:
                scores[emotion] += 1.0
    total = sum(scores.values()) or 1.0
    for k in scores:
        scores[k] /= total
    dominant = max(scores, key=scores.get)
    return {
        "dominant": dominant,
        "scores": scores,
        "confidence": scores[dominant],
    }
