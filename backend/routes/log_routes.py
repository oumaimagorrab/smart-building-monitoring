from flask import Blueprint, request, jsonify
from services.elasticsearch_service import get_logs

log_bp = Blueprint("logs", __name__)


@log_bp.route("/api/logs", methods=["GET"])
def get_all_logs():
    try:
        sensor_id = request.args.get("sensor_id")
        zone = request.args.get("zone")
        log_type = request.args.get("log_type")

        limit = request.args.get("limit", default=50, type=int)

        if limit is None or limit < 1 or limit > 100:
            return jsonify({
                "error": "La limite doit être comprise entre 1 et 100"
            }), 400

        result = get_logs(
            sensor_id=sensor_id,
            zone=zone,
            log_type=log_type,
            limit=limit
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
