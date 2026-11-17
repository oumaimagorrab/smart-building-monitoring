from datetime import datetime, timezone

from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)

db = client[Config.MONGO_DATABASE]

# Collection qui stocke l'historique des imports
uploads_collection = db["uploads"]


def test_connection():
    try:
        client.admin.command("ping")
        print("Connexion MongoDB réussie !")
        return True
    except Exception as e:
        print(f"Erreur de connexion MongoDB : {e}")
        return False


def save_upload_history(filename, logs_count, status="success", error=None):
    try:
        upload = {
            "filename": filename,
            "date": datetime.now(timezone.utc),
            "logs_count": logs_count,
            "status": status,
            "error": error
        }

        result = uploads_collection.insert_one(upload)

        print("Historique de l'import enregistré !")
        return str(result.inserted_id)

    except Exception as e:
        print(f"Erreur lors de l'enregistrement de l'historique : {e}")
        return None


def get_upload_history(limit=50):
    try:
        uploads = uploads_collection.find().sort("date", -1).limit(limit)

        history = []

        for upload in uploads:
            upload["_id"] = str(upload["_id"])
            upload["date"] = upload["date"].isoformat()
            history.append(upload)

        return history

    except Exception as e:
        print(f"Erreur lors de la récupération de l'historique : {e}")
        return []
