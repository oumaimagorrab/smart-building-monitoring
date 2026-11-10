
import requests
from config import Config

def send_log(log_data):
    try:
        response = requests.post(
            Config.LOGSTASH_URL,
            json=log_data,
            timeout=5
        )

        response.raise_for_status()
        print("Log envoyé à Logstash avec succès !")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi à Logstash : {e}")
        return False
