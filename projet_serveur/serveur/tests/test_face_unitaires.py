import unittest
import grpc
import numpy as np
import os
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../serveur/serveur_grpc/')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../serveur_grpc')))

from serveur.serveur_grpc import face_pb2_grpc, face_pb2
from serveur.serveur_grpc.recognition_service import FaceRecognitionServicer


class TestFaceRecognition(unittest.TestCase):

    def setUp(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = face_pb2_grpc.FaceRecognitionStub(self.channel)
        self.servicer = FaceRecognitionServicer()

    def test_recognize_face(self):
        img_path = "media/test.jpg"

        if not os.path.exists(img_path):
            raise FileNotFoundError(f"L'image {img_path} n'a pas été trouvée.")
        
        with open(img_path, "rb") as f:
            img_data = f.read()
        
        request = face_pb2.ImageRequest(image_data=img_data)
        
        response = self.stub.RecognizeFace(request)

        print(f"Nom détecté: {response.name}")
        print(f"Confiance: {response.confidence}%")

        self.assertNotEqual(response.name, "No Face Detected")
        self.assertGreater(response.confidence, 0)

if __name__ == "__main__":
    unittest.main()
