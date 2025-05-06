from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('employes/', views.employe_list, name='employe_list'),
    path('employe/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employe/<int:employe_id>/modifier/', views.modifier_employe, name='modifier_employe'),
    path('employe/<int:employe_id>/upload/', views.upload_image, name='upload_image'),
    path('employe/<int:employe_id>/supprimer/', views.supprimer_employe, name='supprimer_employe'),
    path('historique/', views.historique_acces_view, name='historique_acces'),  
    path('historique/delete/<int:acces_id>/', views.delete_historique, name='delete_historique'),    
    path('', views.index, name='index'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
