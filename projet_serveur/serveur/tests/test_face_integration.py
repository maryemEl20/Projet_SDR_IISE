import unittest
import grpc
import os
import sys
import time

# Ajouter le chemin vers le dossier du service gRPC
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../serveur/serveur_grpc/')))

from serveur.serveur_grpc import face_pb2_grpc, face_pb2
from serveur.serveur_grpc.recognition_service import FaceRecognitionServicer

class TestFaceRecognitionIntegration(unittest.TestCase):

    def setUp(self):
        # Connexion au serveur gRPC (doit être en cours d'exécution)
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = face_pb2_grpc.FaceRecognitionStub(self.channel)

        # Vérification que le serveur est en ligne
        # Pour des raisons d'intégration, on attend un peu que le serveur soit prêt à recevoir des requêtes.
        time.sleep(2)  # Attendez 2 secondes si le serveur démarre lentement

    def test_integration_face_recognition(self):
        # Chemin vers une image de test existante
        img_path = "media/test.jpg"
        # img_path = "../../media/img.png"

        # Vérification de l'existence du fichier image
        self.assertTrue(os.path.exists(img_path), f"L'image {img_path} n'existe pas")

        # Lecture du fichier image
        with open(img_path, "rb") as f:
            img_data = f.read()

        # Envoi de la requête gRPC avec l'image
        request = face_pb2.ImageRequest(image_data=img_data)
        response = self.stub.RecognizeFace(request)

        # Vérifications de la réponse
        print(f"Nom détecté : {response.name}")
        print(f"Confiance : {response.confidence}%")

        # Assertions sur les réponses
        self.assertIsInstance(response.name, str)
        self.assertGreaterEqual(response.confidence, 0)
        self.assertLessEqual(response.confidence, 100)

    def tearDown(self):
        # Fermer le canal après le test
        self.channel.close()

if __name__ == "__main__":
    unittest.main()
