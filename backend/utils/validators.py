
REQUIRED_FIELDS = ["sensor_id", "zone", "log_type"]


def validate_log(log):
    """Vérifie la structure et les valeurs d'un log."""

    if not isinstance(log, dict):
        return False, "Chaque log doit être un objet JSON."

    # Vérifier les champs obligatoires
    for field in REQUIRED_FIELDS:
        if field not in log or not str(log[field]).strip():
            return False, f"Le champ '{field}' est obligatoire."

    # Vérifier les mesures numériques
    numeric_fields = ["temperature", "humidity", "luminosity", "co2", "energy"]

    for field in numeric_fields:
        if field in log:
            try:
                value = float(log[field])
            except (ValueError, TypeError):
                return False, f"Le champ '{field}' doit être numérique."

            if value < 0 and field != "temperature":
                return False, f"Le champ '{field}' ne peut pas être négatif."

    return True, None


def validate_logs(logs):
    """Vérifie tous les logs d'un fichier."""

    if not isinstance(logs, list) or not logs:
        return False, "Le fichier ne contient aucun log."

    for index, log in enumerate(logs):
        is_valid, error = validate_log(log)

        if not is_valid:
            return False, f"Log {index + 1} : {error}"

    return True, None

