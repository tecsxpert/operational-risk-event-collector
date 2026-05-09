"""
Tool-66 — Operational Risk Event Collector
AI Microservice — Entry Point
Author: AI Developer 1
"""

import os
import time
import logging
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.api import api_bp

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

# Record service start time for /health uptime calculation
SERVICE_START_TIME = time.time()

def create_app():
    """Application factory — creates and configures the Flask app."""
    app = Flask(__name__)

    # ── Rate Limiter ────────────────────────────────────────────────────────
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["30 per minute"],
        storage_uri=redis_url,
    )

    # ── Security headers middleware ──────────────────────────────────────────
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Content-Security-Policy"] = "default-src 'none'"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    # ── Input sanitisation middleware ────────────────────────────────────────
    @app.before_request
    def sanitise_request():
        """Strip malicious payloads before they reach any route handler."""
        from flask import request
        from services.sanitiser import detect_prompt_injection

        if request.is_json and request.content_length and request.content_length > 0:
            data = request.get_json(silent=True) or {}
            for value in data.values():
                if isinstance(value, str) and detect_prompt_injection(value):
                    logger.warning("Prompt injection attempt detected — blocked")
                    return jsonify({"error": "Invalid input detected", "code": 400}), 400

    # ── Register blueprints ──────────────────────────────────────────────────
    from routes.describe import describe_bp
    from routes.recommend import recommend_bp
    from routes.report import report_bp
    from routes.health import health_bp

    app.register_blueprint(describe_bp, url_prefix="/api/ai")
    app.register_blueprint(recommend_bp, url_prefix="/api/ai")
    app.register_blueprint(report_bp, url_prefix="/api/ai")
    app.register_blueprint(health_bp)

    # Apply rate limiter to all blueprints
    limiter.limit("30 per minute")(describe_bp)
    limiter.limit("30 per minute")(recommend_bp)
    limiter.limit("30 per minute")(report_bp)

    # ── Global error handlers ────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Endpoint not found", "code": 404}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed", "code": 405}), 405

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return (
            jsonify({"error": "Rate limit exceeded — max 30 requests/min", "code": 429}),
            429,
        )

    @app.errorhandler(500)
    def internal_error(e):
        logger.error("Unhandled internal error: %s", e)
        return jsonify({"error": "Internal server error", "code": 500}), 500

    # ── Pre-load and seed knowledge base (Day 11/12) ─────────────────────────
    from services.knowledge_base import seed_knowledge_base
    seed_knowledge_base()

    logger.info("AI service started — Flask app configured successfully")
    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("AI_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
def create_app():
    app = Flask(__name__)
    CORS(app) # Allow all origins for development
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'ai-service'}
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
