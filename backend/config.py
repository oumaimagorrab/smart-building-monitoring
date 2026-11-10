
import os

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/"
    )
    MONGO_DATABASE = "smart_building_db"

    ELASTICSEARCH_URL = "http://localhost:9200"

    LOGSTASH_URL = "http://localhost:8081"
