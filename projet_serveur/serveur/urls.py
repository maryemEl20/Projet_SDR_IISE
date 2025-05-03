from django.urls import path
from . import views

urlpatterns = [
    path('', views.employe_list, name='employe_default'),
    path('employes/', views.employe_list, name='employe_list'),
    path('employe/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('historique/', views.historique_acces_view, name='historique-acces'),
    path('employe/<int:employe_id>/upload/', views.upload_image, name='upload_image'),
    path('employe/<int:employe_id>/supprimer/', views.supprimer_employe, name='supprimer_employe'),
    path('employe/<int:employe_id>/modifier/', views.modifier_employe, name='modifier_employe'),
]
