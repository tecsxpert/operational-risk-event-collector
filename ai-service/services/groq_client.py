"""
Groq API Client — Tool-66 AI Service
Wraps the Groq SDK with retry logic, error handling, and response caching.
Author: AI Developer 1 / AI Developer 2 (shared)
"""

import os
import time
import logging
import hashlib
import json
from typing import Optional

from groq import Groq, RateLimitError, APIStatusError, APIConnectionError

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2  # seconds — exponential: 2, 4, 8
DEFAULT_TEMPERATURE_FACTUAL = 0.3
DEFAULT_TEMPERATURE_CREATIVE = 0.7
DEFAULT_MAX_TOKENS = 1024

# ---------------------------------------------------------------------------
# Redis cache (optional — degrades gracefully if Redis is unavailable)
# ---------------------------------------------------------------------------
_redis_client = None


def _get_redis():
    """Return a Redis client, or None if unavailable."""
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    try:
        import redis

        url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        _redis_client = redis.from_url(url, socket_connect_timeout=2)
        _redis_client.ping()
        logger.info("Redis cache connected: %s", url)
    except Exception as exc:
        logger.warning("Redis unavailable — AI responses will not be cached: %s", exc)
        _redis_client = None
    return _redis_client


def _cache_key(prompt: str, temperature: float) -> str:
    """SHA-256 cache key derived from the prompt and temperature."""
    raw = f"{prompt}|{temperature}|{MODEL_NAME}"
    return "ai_cache:" + hashlib.sha256(raw.encode()).hexdigest()


def _cache_get(key: str) -> Optional[str]:
    r = _get_redis()
    if r is None:
        return None
    try:
        value = r.get(key)
        return value.decode() if value else None
    except Exception:
        return None


def _cache_set(key: str, value: str, ttl_seconds: int = 900) -> None:
    """Store a value with 15-min TTL (900 s)."""
    r = _get_redis()
    if r is None:
        return
    try:
        r.setex(key, ttl_seconds, value)
    except Exception as exc:
        logger.warning("Redis set failed: %s", exc)


# ---------------------------------------------------------------------------
# Response time tracking (for /health endpoint)
# ---------------------------------------------------------------------------
_response_times: list[float] = []


def get_avg_response_time() -> float:
    """Return the rolling average Groq response time in milliseconds."""
    if not _response_times:
        return 0.0
    recent = _response_times[-50:]  # Keep last 50 readings
    return round(sum(recent) / len(recent), 2)


# ---------------------------------------------------------------------------
# Core Groq call
# ---------------------------------------------------------------------------

def call_groq(
    system_prompt: str,
    user_message: str,
    temperature: float = DEFAULT_TEMPERATURE_FACTUAL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    use_cache: bool = True,
) -> Optional[str]:
    """
    Call the Groq API with retry logic, caching, and comprehensive error handling.

    Returns the model's text response, or None on permanent failure.
    Never raises — callers receive None and should return a fallback response.
    """
    full_prompt = system_prompt + "\n\n" + user_message
    cache_key = _cache_key(full_prompt, temperature)

    # Check cache first
    if use_cache:
        cached = _cache_get(cache_key)
        if cached:
            logger.info("Cache HIT for key %s…", cache_key[-8:])
            return cached

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY environment variable is not set")
        return None

    client = Groq(api_key=api_key)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            start = time.time()
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            elapsed_ms = (time.time() - start) * 1000
            _response_times.append(elapsed_ms)

            result = completion.choices[0].message.content.strip()
            logger.info(
                "Groq call success (attempt %d) — %.0f ms", attempt, elapsed_ms
            )

            # Store in cache
            if use_cache:
                _cache_set(cache_key, result)

            return result

        except RateLimitError:
            wait = RETRY_BACKOFF_BASE ** attempt
            logger.warning(
                "Groq rate limit hit (attempt %d/%d) — retrying in %ds",
                attempt,
                MAX_RETRIES,
                wait,
            )
            if attempt < MAX_RETRIES:
                time.sleep(wait)

        except APIConnectionError as exc:
            logger.error("Groq connection error (attempt %d): %s", attempt, exc)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF_BASE ** attempt)

        except APIStatusError as exc:
            logger.error(
                "Groq API status error (attempt %d): %s %s",
                attempt,
                exc.status_code,
                exc.message,
            )
            # Do not retry on 4xx client errors
            if exc.status_code < 500:
                break
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF_BASE ** attempt)

        except Exception as exc:
            logger.error("Unexpected Groq error (attempt %d): %s", attempt, exc)
            break

    logger.error("All %d Groq attempts failed — returning None", MAX_RETRIES)
    return None
