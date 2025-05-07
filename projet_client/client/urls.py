from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('camera/', views.camera_view, name='camera'),
    path('api/recognize/', views.recognize_api, name='recognize_api'),
]
