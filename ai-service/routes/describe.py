"""
POST /api/ai/describe — Analyse and describe an operational risk event.
Day 3 task: validate input, load prompt, call Groq, return structured JSON.
Author: AI Developer 1
"""

import json
import logging
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify

from services.groq_client import call_groq
from services.prompt_loader import load_prompt
from services.sanitiser import sanitise_string, validate_required_fields

logger = logging.getLogger(__name__)

describe_bp = Blueprint("describe", __name__)

# ---------------------------------------------------------------------------
# Fallback template — returned when Groq is unavailable (Day 9 requirement)
# ---------------------------------------------------------------------------
DESCRIBE_FALLBACK = {
    "event_type": "Unknown",
    "severity": "Unknown",
    "impact_score": 0,
    "likelihood_score": 0,
    "risk_score": 0,
    "description": "AI analysis is temporarily unavailable. Please review manually.",
    "root_cause": "Unable to determine — AI service unavailable",
    "affected_areas": [],
    "regulatory_flags": [],
    "is_fallback": True,
}


@describe_bp.route("/describe", methods=["POST"])
def describe():
    """
    Analyse an operational risk event and return a structured JSON description.

    Request body:
        title       (str, required) — short title of the event
        description (str, required) — detailed description of what happened
        event_date  (str, optional) — date the event occurred (ISO 8601)
        department  (str, optional) — affected department

    Returns:
        200 — structured risk event analysis
        400 — validation error
        500 — unexpected error
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON", "code": 400}), 400

    # Validate required fields
    missing = validate_required_fields(data, ["title", "description"])
    if missing:
        return (
            jsonify(
                {
                    "error": f"Missing required fields: {', '.join(missing)}",
                    "code": 400,
                }
            ),
            400,
        )

    # Sanitise inputs
    title = sanitise_string(data["title"], max_length=200)
    description = sanitise_string(data["description"], max_length=2000)
    event_date = sanitise_string(data.get("event_date", "Not specified"), max_length=50)
    department = sanitise_string(data.get("department", "Not specified"), max_length=100)

    if not title or not description:
        return jsonify({"error": "title and description must not be empty", "code": 400}), 400

    # Build user message from sanitised inputs
    user_message = (
        f"Risk Event Title: {title}\n"
        f"Description: {description}\n"
        f"Event Date: {event_date}\n"
        f"Affected Department: {department}"
    )

    try:
        system_prompt = load_prompt("describe")
    except FileNotFoundError as exc:
        logger.error("Prompt template missing: %s", exc)
        return jsonify({"error": "Server configuration error", "code": 500}), 500

    logger.info("Calling Groq /describe for event: '%s'", title[:60])
    raw_response = call_groq(system_prompt, user_message, temperature=0.3)

    if raw_response is None:
        logger.warning("/describe Groq call failed — returning fallback")
        fallback = {
            **DESCRIBE_FALLBACK,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        return jsonify(fallback), 200

    # Parse the JSON response from Groq
    try:
        result = json.loads(raw_response)
        # Ensure generated_at is always set
        if "generated_at" not in result or not result["generated_at"]:
            result["generated_at"] = datetime.now(timezone.utc).isoformat()
        result.setdefault("is_fallback", False)
        return jsonify(result), 200
    except json.JSONDecodeError:
        logger.error("Groq /describe returned non-JSON: %.200s", raw_response)
        # Try to return a structured error with the raw text
        return (
            jsonify(
                {
                    "error": "AI returned an invalid format",
                    "raw": raw_response[:500],
                    "code": 500,
                }
            ),
            500,
        )
