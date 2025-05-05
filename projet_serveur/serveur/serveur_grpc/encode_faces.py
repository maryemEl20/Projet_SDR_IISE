import face_recognition
import os
import pickle

BASE_DIR = "../../media/visages/"  
known_encodings = []
known_names = []

print("🔍 Génération des encodages...")

for person_name in os.listdir(BASE_DIR):
    person_dir = os.path.join(BASE_DIR, person_name)
    if not os.path.isdir(person_dir):
        continue

    for filename in os.listdir(person_dir):
        if filename.lower().endswith(('.jpg', '.png')):
            path = os.path.join(person_dir, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person_name)
                print(f"[✓] Encodage ajouté pour {person_name} ({filename})")
            else:
                print(f"[x] Aucun visage trouvé dans {filename}")

# Sauvegarde des encodages
with open("known_faces.pickle", "wb") as f:
    pickle.dump({"encodings": known_encodings, "names": known_names}, f)

print("Tous les encodages ont été générés avec succès.")
