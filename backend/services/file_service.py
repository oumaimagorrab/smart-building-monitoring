
import csv
import json
import os


def read_csv(file_path):
    """Lire un fichier CSV et retourner ses lignes."""
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def read_json(file_path):
    """Lire un fichier JSON et retourner ses données."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Accepter un objet JSON ou une liste d'objets
    if isinstance(data, dict):
        return [data]

    if isinstance(data, list):
        return data

    raise ValueError("Le fichier JSON doit contenir un objet ou une liste d'objets.")


def read_file(file_path):
    """Détecter le format et lire le fichier."""
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":
        return read_csv(file_path)

    if extension == ".json":
        return read_json(file_path)

    raise ValueError("Format non accepté. Utilisez CSV ou JSON.")
