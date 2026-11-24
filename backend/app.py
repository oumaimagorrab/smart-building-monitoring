
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

from routes.upload_routes import upload_bp
from routes.log_routes import log_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(upload_bp)
app.register_blueprint(log_bp)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Smart Building Monitoring API",
        "status": "running"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "OK",
        "service": "backend"
    })


@app.route("/docs", methods=["GET"])
def swagger_ui():
    return send_from_directory(
        os.path.join(app.root_path, "docs"),
        "index.html"
    )


@app.route("/openapi.yaml", methods=["GET"])
def openapi_spec():
    return send_from_directory(
        os.path.join(app.root_path, "docs"),
        "openapi.yaml"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

