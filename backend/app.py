from routes.upload_routes import upload_bp
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
app.register_blueprint(upload_bp)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
