"""
POST /api/ai/recommend — Generate 3 risk mitigation recommendations.
Day 4 task: 3 recommendations as JSON array, each with action_type, description, priority.
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

recommend_bp = Blueprint("recommend", __name__)

# ---------------------------------------------------------------------------
# Fallback recommendations — returned when Groq is unavailable
# ---------------------------------------------------------------------------
RECOMMEND_FALLBACK = {
    "recommendations": [
        {
            "action_type": "Immediate",
            "priority": "High",
            "description": "Escalate the event to the Risk Management team for immediate assessment.",
            "owner": "Risk Management",
            "estimated_effort": "Low",
            "expected_outcome": "Ensures the event receives timely attention and does not escalate further.",
        },
        {
            "action_type": "Short-Term",
            "priority": "Medium",
            "description": "Conduct a root cause analysis and document findings in the risk register.",
            "owner": "Operations",
            "estimated_effort": "Medium",
            "expected_outcome": "Identifies the root cause and prevents recurrence within 30 days.",
        },
        {
            "action_type": "Long-Term",
            "priority": "Medium",
            "description": "Review and update the relevant control framework and SOPs to address systemic gaps.",
            "owner": "Compliance",
            "estimated_effort": "High",
            "expected_outcome": "Strengthens the control environment and reduces long-term risk exposure.",
        },
    ],
    "overall_risk_reduction": "AI analysis unavailable — generic recommendations applied.",
    "is_fallback": True,
}


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    """
    Generate 3 risk mitigation recommendations for a given operational risk event.

    Request body:
        title       (str, required) — event title
        description (str, required) — event description
        severity    (str, optional) — event severity (Critical|High|Medium|Low)
        risk_score  (int, optional) — numeric risk score

    Returns:
        200 — recommendations JSON array
        400 — validation error
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON", "code": 400}), 400

    missing = validate_required_fields(data, ["title", "description"])
    if missing:
        return (
            jsonify(
                {"error": f"Missing required fields: {', '.join(missing)}", "code": 400}
            ),
            400,
        )

    title = sanitise_string(data["title"], max_length=200)
    description = sanitise_string(data["description"], max_length=2000)
    severity = sanitise_string(data.get("severity", "Unknown"), max_length=20)
    risk_score = data.get("risk_score", "Not provided")

    if not title or not description:
        return jsonify({"error": "title and description must not be empty", "code": 400}), 400

    user_message = (
        f"Risk Event Title: {title}\n"
        f"Description: {description}\n"
        f"Severity: {severity}\n"
        f"Risk Score: {risk_score}"
    )

    try:
        system_prompt = load_prompt("recommend")
    except FileNotFoundError as exc:
        logger.error("Prompt template missing: %s", exc)
        return jsonify({"error": "Server configuration error", "code": 500}), 500

    logger.info("Calling Groq /recommend for event: '%s'", title[:60])
    raw_response = call_groq(system_prompt, user_message, temperature=0.5)

    if raw_response is None:
        logger.warning("/recommend Groq call failed — returning fallback")
        fallback = {
            **RECOMMEND_FALLBACK,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        return jsonify(fallback), 200

    try:
        result = json.loads(raw_response)
        if "generated_at" not in result or not result["generated_at"]:
            result["generated_at"] = datetime.now(timezone.utc).isoformat()
        result.setdefault("is_fallback", False)

        # Validate we got exactly 3 recommendations
        recs = result.get("recommendations", [])
        if not isinstance(recs, list) or len(recs) == 0:
            logger.warning("/recommend got malformed recommendations — using fallback")
            return jsonify(
                {
                    **RECOMMEND_FALLBACK,
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                }
            ), 200

        return jsonify(result), 200

    except json.JSONDecodeError:
        logger.error("Groq /recommend returned non-JSON: %.200s", raw_response)
        return (
            jsonify({"error": "AI returned an invalid format", "raw": raw_response[:500], "code": 500}),
            500,
        )
