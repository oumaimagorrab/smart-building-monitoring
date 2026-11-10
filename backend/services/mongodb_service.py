
from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)

db = client[Config.MONGO_DATABASE]

def test_connection():
    try:
        client.admin.command("ping")
        print("Connexion MongoDB réussie !")
        return True
    except Exception as e:
        print(f"Erreur de connexion MongoDB : {e}")
        return False
