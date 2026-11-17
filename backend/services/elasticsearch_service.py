import requests
from config import Config


def get_logs(sensor_id=None, zone=None, log_type=None, limit=50):
    try:
        filters = []

        if sensor_id:
            filters.append({"term": {"sensor_id.keyword": sensor_id}})

        if zone:
            filters.append({"term": {"zone.keyword": zone}})

        if log_type:
            filters.append({"term": {"log_type.keyword": log_type}})

        query = {
            "query": {
                "bool": {
                    "filter": filters
                }
            },
            "sort": [
                {
                    "@timestamp": {
                        "order": "desc",
                        "unmapped_type": "date"
                    }
                }
            ],
            "size": limit
        }

        response = requests.get(
            f"{Config.ELASTICSEARCH_URL}/iot-logs-test/_search",
            json=query,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        hits = data["hits"]["hits"]

        logs = []

        for hit in hits:
            log = hit["_source"]
            log["id"] = hit["_id"]
            logs.append(log)

        return {
            "total": data["hits"]["total"]["value"],
            "logs": logs
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"Erreur Elasticsearch : {e}")
