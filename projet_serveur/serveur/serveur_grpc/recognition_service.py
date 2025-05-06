import cv2
import numpy as np
import grpc
from concurrent import futures
import face_pb2_grpc
import face_pb2
import os
import sys
import django
import pickle
import face_recognition
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Configuration de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projet_serveur.settings")
django.setup()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../serveur')))

from serveur.models import Employe, AccesLog

# Chargement des encodages connus
with open("known_faces.pickle", "rb") as f:
    data = pickle.load(f)
    known_encodings = data["encodings"]
    known_names = data["names"]

class FaceRecognitionServicer(face_pb2_grpc.FaceRecognitionServicer):
    def RecognizeFace(self, request, context):
        img_data = np.frombuffer(request.image_data, dtype=np.uint8)
        img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_img)
        face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

        if not face_encodings:
            return face_pb2.RecognitionResponse(name="No Face Detected", confidence=0.0, x=0, y=0, w=0, h=0)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            name = "Unknown"
            confidence = 1 - face_distances[best_match_index]
            

            if matches[best_match_index]:
                name = known_names[best_match_index]
                enregistrer_acces(name)

            if name == "Unknown":
                enregistrer_acces(name)

            return face_pb2.RecognitionResponse(
                name=name,
                confidence=float(confidence * 100),
                x=int(left),
                y=int(top),
                w=int(right - left),
                h=int(bottom - top)
            )


        return face_pb2.RecognitionResponse(name="Unknown", confidence=0.0, x=0, y=0, w=0, h=0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    face_pb2_grpc.add_FaceRecognitionServicer_to_server(FaceRecognitionServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Serveur gRPC (face_recognition) en cours d'exécution sur le port 50051...")
    server.wait_for_termination()



# def enregistrer_acces(request,nom_employe):
#     try:
#         employe = Employe.objects.get(nom=nom_employe)

#         dernier_acces = AccesLog.objects.filter(employe=employe).order_by('-date_entree').first()

#         maintenant = timezone.now()
#         if not dernier_acces or (maintenant - dernier_acces.date_entree) > timedelta(minutes=5):
#             AccesLog.objects.create(employe=employe, date_entree=maintenant)
#             #messages.success(request, f"Accès ENREGISTRÉ pour {nom_employe} à {maintenant}")
#             log_event(nom_employe, "Succès", image_path=f"{nom_employe}.jpg")  
#             #print(f"Accès ENREGISTRÉ pour {nom_employe} à {maintenant}")
#         else:
#             #messages.info(request, f"Accès DÉJÀ enregistré récemment pour {nom_employe}")
#             log_event(nom_employe, "Déjà enregistré récemment")
#             #print(f"Accès DÉJÀ enregistré récemment pour {nom_employe}")
#     except Employe.DoesNotExist:
#         #messages.error(request, f"Employé introuvable : {nom_employe}")
#         log_event(nom_employe, "Échec (Employé introuvable)")

#     return redirect('historique_acces')


from utils.logging_utils import log_event

def enregistrer_acces(nom_employe):
    try:
        employe = Employe.objects.filter(nom=nom_employe)
        if not employe:
            log_event(nom_employe, "Échec (Employé introuvable)")
            print(f"Employé introuvable")
            return
        
        employe = Employe.objects.get(nom=nom_employe)
        dernier_acces = AccesLog.objects.filter(employe=employe).order_by('-date_entree').first()
        maintenant = timezone.now()

        if not dernier_acces or (maintenant - dernier_acces.date_entree) > timedelta(minutes=5):
            AccesLog.objects.create(employe=employe, date_entree=maintenant)
            log_event(nom_employe, "Succès")
            print(f"Accès ENREGISTRÉ pour {nom_employe}")
        else:
            log_event(nom_employe, "Déjà enregistré récemment")
            print(f"Accès DÉJÀ enregistré récemment pour {nom_employe}")
    except Exception as e:
        print(f"Erreur inconnue: {e}")


if __name__ == '__main__':
    serve()
