"""
GET /health — AI service health check endpoint.
Day 7 task: returns model name, avg response time, uptime.
Author: AI Developer 1
"""

import time
import logging
import os
from flask import Blueprint, jsonify

from services.groq_client import get_avg_response_time, MODEL_NAME

logger = logging.getLogger(__name__)

health_bp = Blueprint("health", __name__)

# Imported from app.py — set at startup
try:
    from app import SERVICE_START_TIME
except ImportError:
    SERVICE_START_TIME = time.time()


@health_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint for the AI microservice.

    Returns:
        200 — service status, model name, avg response time, uptime
    """
    uptime_seconds = int(time.time() - SERVICE_START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

    # Check Redis connectivity
    redis_status = "unavailable"
    try:
        import redis
        r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"),
                           socket_connect_timeout=1)
        r.ping()
        redis_status = "connected"
    except Exception:
        pass

    avg_rt = get_avg_response_time()
    performance_status = (
        "optimal" if avg_rt < 2000 else
        "degraded" if avg_rt < 5000 else
        "slow"
    )

    return jsonify({
        "status": "healthy",
        "service": "Tool-66 AI Microservice",
        "model": MODEL_NAME,
        "avg_response_time_ms": avg_rt,
        "performance_status": performance_status,
        "uptime": uptime_str,
        "uptime_seconds": uptime_seconds,
        "redis_cache": redis_status,
        "endpoints": [
            {"method": "POST", "path": "/api/ai/describe"},
            {"method": "POST", "path": "/api/ai/recommend"},
            {"method": "POST", "path": "/api/ai/generate-report"},
            {"method": "GET",  "path": "/health"},
        ],
        "rate_limit": "30 requests/minute per IP",
    }), 200
