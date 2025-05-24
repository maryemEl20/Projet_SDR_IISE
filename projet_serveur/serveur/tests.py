

def test_recognize_face(self):
    # Charger une image de test
    img_path = "media/visages/test.jpg"  # Vérifier le chemin d'image
    
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"L'image {img_path} n'a pas été trouvée.")
    
    with open(img_path, "rb") as f:
        img_data = f.read()
    
    # Créer une requête gRPC avec l'image
    request = face_pb2.RecognitionRequest(image_data=img_data)
    
    # Appeler la méthode de reconnaissance faciale
    response = self.stub.RecognizeFace(request)

    # Vérifier que la réponse contient un nom et une confiance
    print(f"Nom détecté: {response.name}")
    print(f"Confiance: {response.confidence}%")
    print(f"Coordonnées: x={response.x}, y={response.y}, w={response.w}, h={response.h}")

    # Vérifiez que la réponse n'est pas un échec
    self.assertNotEqual(response.name, "No Face Detected")
    self.assertGreater(response.confidence, 0)
