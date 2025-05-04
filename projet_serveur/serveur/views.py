from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Employe, AccesLog, Visage
from .forms import EmployeForm
from django.contrib import messages
import os
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import shutil

def historique_acces_view(request):
    data = AccesLog.objects.select_related('employe').order_by('-date_entree')
    return render(request, 'serveur/historique_acces.html', {'data': data})


def delete_historique(request, acces_id):
    acces = get_object_or_404(AccesLog, id=acces_id)
    acces.delete()
    messages.success(request, "Le record d'accès a été supprimé avec succès.")
    return redirect('historique_acces')  


def employe_list(request):
    data = Employe.objects.all()
    return render(request, 'serveur/employe_list.html', {'data': data})

def upload_image(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)
    
    if request.method == 'POST':
        images = request.FILES.getlist('images')  
        if images:
            employe_folder_path = os.path.join(settings.MEDIA_ROOT, 'visages', employe.nom)
            if not os.path.exists(employe_folder_path):
                os.makedirs(employe_folder_path)

            for image in images:
                image_path = os.path.join(employe_folder_path, image.name)
                try:
                    with open(image_path, 'wb+') as f:
                        for chunk in image.chunks():
                            f.write(chunk)

                    Visage.objects.create(employe=employe, image_path=image_path)
                    messages.success(request, f"L'image de {employe.nom} a été téléchargée avec succès.")
                except Exception as e:
                    messages.error(request, f"Une erreur s'est produite lors du téléchargement de l'image: {str(e)}")
        else:
            messages.warning(request, "Aucune image sélectionnée.")
        return HttpResponseRedirect(request.path_info)  # This will reload the current page with updated messages
    
    return render(request, 'serveur/upload_image.html', {'employe': employe})

def ajouter_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            employe = form.save()

            employe_name = employe.nom
            employe_folder_path = os.path.join(settings.MEDIA_ROOT, 'visages', employe_name)

            if not os.path.exists(employe_folder_path):
                os.makedirs(employe_folder_path)

            images = request.FILES.getlist('images')
            for image in images:
                image_path = os.path.join(employe_folder_path, image.name)
                
                with open(image_path, 'wb+') as f:
                    for chunk in image.chunks():
                        f.write(chunk)

                Visage.objects.create(employe=employe, image_path=image_path)

            return redirect('/serveur/employes/')
    else:
        form = EmployeForm()
    return render(request, 'serveur/ajouter_employe.html', {'form': form})


def supprimer_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    # Supprimer le dossier du visage associé
    folder_path = os.path.join(settings.MEDIA_ROOT, 'visages', employe.nom)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    employe.delete()
    messages.success(request, f"L'employé {employe.nom} a été supprimé avec ses images.")
    return redirect('employe_list')


def modifier_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            messages.success(request, f"Les informations de {employe.nom} ont été mises à jour.")
            return redirect('employe_list')
    else:
        form = EmployeForm(instance=employe)

    images = Visage.objects.filter(employe=employe)
    return render(request, 'serveur/modifier_employe.html', {'form': form, 'employe': employe, 'images': images})


