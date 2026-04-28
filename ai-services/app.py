from flask import Flask
from routes.ai_routes import ai_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Rate limiter
limiter = Limiter(
    get_remote_address,
    default_limits=["30 per minute"]
)
limiter.init_app(app)

# Register routes
app.register_blueprint(ai_bp)

@app.route("/health")
def health():
    return {"status": "AI service running"}

if __name__ == "__main__":
    app.run(debug=True)