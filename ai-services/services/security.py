import re

def sanitize_input(user_input):
    # Remove HTML tags
    clean_text = re.sub(r'<.*?>', '', user_input)

    # Remove dangerous characters
    clean_text = re.sub(r'[{};$]', '', clean_text)

    return clean_text.strip()

def detect_prompt_injection(user_input):
    suspicious_patterns = [
        "ignore previous instructions",
        "act as system",
        "bypass security",
        "you are chatgpt",
        "reveal system prompt"
    ]

    user_input_lower = user_input.lower()

    for pattern in suspicious_patterns:
        if pattern in user_input_lower:
            return True

    return False