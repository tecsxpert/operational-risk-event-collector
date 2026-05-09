"""
Input Sanitisation Service — Tool-66 AI Microservice
Strips HTML, detects prompt injection patterns, and validates input fields.
Author: AI Developer 1
"""

import re
import logging
import bleach

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt injection detection patterns
# ---------------------------------------------------------------------------
INJECTION_PATTERNS = [
    # Direct instruction overrides
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|prior|above)\s+instructions?",
    r"forget\s+(all\s+)?(previous|prior|above)\s+instructions?",
    r"override\s+(all\s+)?(previous|prior|above)\s+instructions?",
    # Role manipulation
    r"you\s+are\s+now\s+(a|an|the)\s+",
    r"act\s+as\s+(a|an|the)\s+",
    r"pretend\s+to\s+be\s+",
    r"roleplay\s+as\s+",
    # Jailbreak patterns
    r"(DAN|JAILBREAK|DEVELOPER MODE)",
    r"system\s*prompt",
    r"reveal\s+(your|the)\s+(system|hidden|secret)\s+prompt",
    # Instruction injection markers
    r"\[INST\]",
    r"<\|system\|>",
    r"###\s*instruction",
    r"##\s*new\s+instructions?",
    # SQL injection patterns (belt-and-suspenders — backend handles DB)
    r"(union\s+select|drop\s+table|insert\s+into|delete\s+from|exec\s*\()",
]

_COMPILED_PATTERNS = [
    re.compile(p, re.IGNORECASE | re.DOTALL) for p in INJECTION_PATTERNS
]


def strip_html(text: str) -> str:
    """Remove all HTML tags from user input using bleach."""
    return bleach.clean(text, tags=[], strip=True).strip()


def detect_prompt_injection(text: str) -> bool:
    """
    Return True if the text contains any known prompt injection pattern.
    Logs a warning with the matching pattern for audit purposes.
    """
    for pattern in _COMPILED_PATTERNS:
        if pattern.search(text):
            logger.warning(
                "Prompt injection pattern matched: '%s' in input: '%.80s…'",
                pattern.pattern,
                text,
            )
            return True
    return False


def sanitise_string(value: str, max_length: int = 2000) -> str:
    """Strip HTML and truncate to max_length characters."""
    cleaned = strip_html(value)
    if len(cleaned) > max_length:
        logger.warning(
            "Input truncated from %d to %d chars", len(cleaned), max_length
        )
        cleaned = cleaned[:max_length]
    return cleaned


def validate_required_fields(data: dict, required: list[str]) -> list[str]:
    """Return a list of missing or empty required field names."""
    missing = []
    for field in required:
        val = data.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            missing.append(field)
    return missing
