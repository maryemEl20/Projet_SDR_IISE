import grpc
import cv2
import face_pb2
import face_pb2_grpc
import time

# Connexion au serveur
channel = grpc.insecure_channel('localhost:50051')
stub = face_pb2_grpc.FaceRecognitionStub(channel)

# Ouverture de la caméra (avec CAP_DSHOW pour accélérer sur Windows)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

last_sent = 0
response = None  # Pour éviter une erreur si aucune image n'est encore envoyée

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Correction : inverser l'image horizontalement (effet miroir)
    frame = cv2.flip(frame, 1)

    #Affichage immédiat
    display_frame = frame.copy()

    # Envoi toutes les secondes
    current_time = time.time()
    if current_time - last_sent > 1:
        # Redimensionner (optionnel pour accélérer)
        resized_frame = cv2.resize(frame, (320, 240))

        # Encodage et envoi
        _, img_encoded = cv2.imencode('.jpg', resized_frame)
        img_bytes = img_encoded.tobytes()

        request = face_pb2.ImageRequest(image_data=img_bytes)
        response = stub.RecognizeFace(request)
        last_sent = current_time

    # Affichage des résultats SÉPARÉ (ne bloque pas la caméra)
    if response and response.name != "No Face Detected":
        x, y, w, h = response.x, response.y, response.w, response.h
        # Mise à l’échelle des coordonnées si on a redimensionné
        scale_x = frame.shape[1] / 320
        scale_y = frame.shape[0] / 240
        x, y, w, h = int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)

        cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(display_frame, f"Nom : {response.name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(display_frame, f"Confiance : {response.confidence:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Visage Capturé", display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
