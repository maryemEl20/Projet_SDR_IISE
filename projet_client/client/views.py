import sys
import base64
import numpy as np
import cv2
import grpc
from . import face_pb2
from . import face_pb2_grpc
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render


def home(request):
    return render(request, 'client/home.html')

def camera_view(request):
    return render(request, "client/camera.html")

@csrf_exempt
def recognize_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        header, encoded = data["image"].split(",", 1)
        img_data = base64.b64decode(encoded)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Send to gRPC server
        channel = grpc.insecure_channel('localhost:50051')
        stub = face_pb2_grpc.FaceRecognitionStub(channel)

        _, img_encoded = cv2.imencode('.jpg', img)
        request_pb = face_pb2.ImageRequest(image_data=img_encoded.tobytes())
        response_pb = stub.RecognizeFace(request_pb)

        return JsonResponse({
            "name": response_pb.name,
            "confidence": float(response_pb.confidence),
        })

    return JsonResponse({"error": "Invalid request"}, status=400)