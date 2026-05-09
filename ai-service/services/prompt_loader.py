"""
Prompt Loader Service — Tool-66 AI Microservice
Loads prompt templates from the prompts/ directory.
Author: AI Developer 1
"""

import os
import logging

logger = logging.getLogger(__name__)

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


def load_prompt(template_name: str) -> str:
    """
    Load a prompt template by filename (without .txt extension).
    Raises FileNotFoundError if the template does not exist.
    """
    path = os.path.join(PROMPTS_DIR, f"{template_name}.txt")
    if not os.path.exists(path):
        logger.error("Prompt template not found: %s", path)
        raise FileNotFoundError(f"Prompt template '{template_name}' not found")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    logger.debug("Loaded prompt template: %s (%d chars)", template_name, len(content))
    return content
