def check_safety(message):
    message_lower = message.lower()

    # Prompt injection
    if "ignore previous instructions" in message_lower:
        return {
            "category": "prompt_injection",
            "risk": "high",
            "warning": "Possible attempt to override chatbot instructions."
        }

    # Prompt extraction
    if "reveal your system prompt" in message_lower:
        return {
            "category": "prompt_extraction",
            "risk": "high",
            "warning": "Possible attempt to extract hidden instructions."
        }

    # Safety bypass
    if "bypass your safety" in message_lower:
        return {
            "category": "safety_bypass",
            "risk": "high",
            "warning": "Possible attempt to bypass safety controls."
        }

    # Harassment indicators
    harassment_words = [
        "fuck",
        "stupid",
        "shut up"
    ]

    if any(word in message_lower for word in harassment_words):
        return {
            "category": "harassment",
            "risk": "medium",
            "warning": "This conversation may contain harassing or abusive language."
        }

    # Exploitation / grooming-related indicators
    grooming_indicators = [
        "keep this secret",
        "don't tell anyone",
        "move this conversation somewhere private",
        "you are mature for your age"
    ]

    if any(phrase in message_lower for phrase in grooming_indicators):
        return {
            "category": "grooming_or_exploitation",
            "risk": "high",
            "warning": "This conversation may contain inappropriate or exploitative behavior."
        }

    # Threat indicators
    threat_indicators = [
        "i will hurt you",
        "i'm going to hurt you",
        "threaten you"
    ]

    if any(phrase in message_lower for phrase in threat_indicators):
        return {
            "category": "threat",
            "risk": "high",
            "warning": "This conversation may contain threatening language."
        }

    # Normal conversation
    return {
        "category": "normal",
        "risk": "low",
        "warning": None
    }