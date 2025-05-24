import csv
import os
from datetime import datetime

# Utilise le chemin absolu du dossier courant de recognition_service.py
LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs.csv')

def log_event(user_name, status):
    timestamp = datetime.now().isoformat()
    file_exists = os.path.isfile(LOG_FILE)

    last_user_name = None
    last_status = None

    # Lire la dernière ligne si le fichier n’est pas vide
    if file_exists:
        with open(LOG_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:  # il y a au moins une ligne de données
                last_entry = reader[-1]
                if len(last_entry) >= 3:
                    last_user_name = last_entry[1]
                    last_status = last_entry[2]

    # Éviter la duplication
    if user_name == last_user_name and status == last_status:
        return

    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists or os.stat(LOG_FILE).st_size == 0:
            writer.writerow(['timestamp', 'user_name', 'status'])

        writer.writerow([timestamp, user_name, status])
