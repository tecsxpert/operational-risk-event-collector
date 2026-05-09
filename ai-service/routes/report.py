"""
POST /api/ai/generate-report — Generate a comprehensive risk event report.
Day 6 task: structured JSON with title, summary, overview, key items, recommendations.
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

report_bp = Blueprint("report", __name__)

# ---------------------------------------------------------------------------
# Fallback report — returned when Groq is unavailable
# ---------------------------------------------------------------------------
REPORT_FALLBACK = {
    "title": "Operational Risk Event Report — AI Unavailable",
    "executive_summary": (
        "AI report generation is temporarily unavailable. "
        "Manual review of the risk events is required."
    ),
    "overview": {
        "total_events": 0,
        "critical_count": 0,
        "high_count": 0,
        "medium_count": 0,
        "low_count": 0,
        "average_risk_score": 0.0,
        "reporting_period": "N/A",
    },
    "key_risk_themes": [],
    "top_events": [],
    "recommendations": [
        "Review all open risk events manually.",
        "Escalate critical events to the Risk Committee.",
        "Re-run AI report generation when service is restored.",
    ],
    "conclusion": "Report generation failed. The AI service will be restored shortly.",
    "is_fallback": True,
}


@report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    """
    Generate a comprehensive operational risk report from a list of events.

    Request body:
        events          (list, required) — array of risk event objects
        reporting_period (str, optional) — e.g. "April 2026"
        report_title    (str, optional) — custom report title

    Returns:
        200 — structured report JSON
        400 — validation error
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON", "code": 400}), 400

    events = data.get("events")
    if not events or not isinstance(events, list) or len(events) == 0:
        return (
            jsonify({"error": "Field 'events' must be a non-empty list", "code": 400}),
            400,
        )

    if len(events) > 100:
        return (
            jsonify({"error": "Maximum 100 events per report request", "code": 400}),
            400,
        )

    reporting_period = sanitise_string(
        data.get("reporting_period", "Current Period"), max_length=50
    )
    report_title = sanitise_string(
        data.get("report_title", f"Operational Risk Event Report — {reporting_period}"),
        max_length=200,
    )

    # Build concise event summary for the prompt (limit token usage)
    event_lines = []
    for i, evt in enumerate(events[:50], 1):  # Cap at 50 events for token budget
        if isinstance(evt, dict):
            event_lines.append(
                f"{i}. [{evt.get('severity', 'Unknown')}] "
                f"{evt.get('title', 'Untitled')} — "
                f"Risk Score: {evt.get('risk_score', 'N/A')} — "
                f"Type: {evt.get('event_type', 'Unknown')}"
            )

    user_message = (
        f"Report Title: {report_title}\n"
        f"Reporting Period: {reporting_period}\n"
        f"Total Events Submitted: {len(events)}\n\n"
        f"Event List:\n" + "\n".join(event_lines)
    )

    try:
        system_prompt = load_prompt("generate_report")
    except FileNotFoundError as exc:
        logger.error("Prompt template missing: %s", exc)
        return jsonify({"error": "Server configuration error", "code": 500}), 500

    logger.info(
        "Calling Groq /generate-report — %d events, period: %s",
        len(events),
        reporting_period,
    )
    raw_response = call_groq(
        system_prompt,
        user_message,
        temperature=0.3,
        max_tokens=2048,
    )

    if raw_response is None:
        logger.warning("/generate-report Groq call failed — returning fallback")
        fallback = {
            **REPORT_FALLBACK,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        return jsonify(fallback), 200

    try:
        result = json.loads(raw_response)
        if "generated_at" not in result or not result["generated_at"]:
            result["generated_at"] = datetime.now(timezone.utc).isoformat()
        result.setdefault("is_fallback", False)
        return jsonify(result), 200

    except json.JSONDecodeError:
        logger.error("Groq /generate-report returned non-JSON: %.200s", raw_response)
        return (
            jsonify({"error": "AI returned an invalid format", "raw": raw_response[:500], "code": 500}),
            500,
        )
