from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
from services.security import sanitize_input, detect_prompt_injection

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/describe", methods=["POST"])
def describe():
    data = request.json
    user_input = data.get("text", "")

    # Injection check
    if detect_prompt_injection(user_input):
        return jsonify({"error": "Invalid input"}), 400

    # Clean input
    clean_input = sanitize_input(user_input)

    prompt = f"Explain this operational risk clearly: {clean_input}"

    result = generate_response(prompt)

    return jsonify({
        "description": result,
        "generated_at": "now"
    })


@ai_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    user_input = data.get("text", "")

    if detect_prompt_injection(user_input):
        return jsonify({"error": "Invalid input"}), 400

    clean_input = sanitize_input(user_input)

    prompt = f"Give 3 risk mitigation recommendations for: {clean_input}"

    result = generate_response(prompt)

    return jsonify({
        "recommendations": result
    })