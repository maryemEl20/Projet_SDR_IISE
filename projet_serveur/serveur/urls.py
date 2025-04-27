# serveur/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='serveur_home'), 
    path('employes/', views.employe_list, name='employe_list'), 
]
