from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Employe, AccesLog, Visage
from .forms import EmployeForm
from django.contrib import messages


def historique_acces_view(request):
    data = AccesLog.objects.select_related('employe').order_by('-date_entree')
    return render(request, 'serveur/historique_acces.html', {'data': data})


def upload_image(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)
    
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                Visage.objects.create(employe=employe, image_path=image)
            messages.success(request, "Images téléchargées avec succès.")
        else:
            messages.warning(request, "Aucune image sélectionnée.")
        return redirect('employe_list') 
    
    return render(request, 'serveur/upload_image.html', {'employe': employe})


def employe_list(request):
    data = Employe.objects.all()
    return render(request, 'serveur/employe_list.html', {'data': data})

def ajouter_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            employe = form.save()
            images = request.FILES.getlist('images')
            for image in images:
                Visage.objects.create(employe=employe, image_path=image)
            return redirect('/serveur/employes/')
    else:
        form = EmployeForm()
    return render(request, 'serveur/ajouter_employe.html', {'form': form})
from django.contrib import messages  

def supprimer_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)
    employe.delete()
    messages.success(request, f"L'employé {employe.nom} a été supprimé.")
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

def index(request):
    return render(request, 'serveur/index.html')
