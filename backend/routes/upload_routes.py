
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from services.file_service import read_file
from services.logstash_service import send_log

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv", "json"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload_bp.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Aucun fichier sélectionné"}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Format non accepté. Utilisez CSV ou JSON"
        }), 400

    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(file_path)

        logs = read_file(file_path)

        if not logs:
            return jsonify({
                "error": "Le fichier ne contient aucun log"
            }), 400

        if not all(isinstance(log, dict) for log in logs):
            return jsonify({"error": "Format des données invalide"}), 400

        for log in logs:
            if not send_log(log):
                return jsonify({
                    "error": "Erreur lors de l'envoi des logs à Logstash"
                }), 502

        return jsonify({
            "message": "Fichier importé avec succès",
            "filename": filename,
            "logs_count": len(logs)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
