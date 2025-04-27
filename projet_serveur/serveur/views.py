# serveur/views.py
from django.shortcuts import render
from .models import Employe, Visage, AccesLog

def index(request):
    return render(request, 'serveur/index.html')  

def employe_list(request):
    employes = Employe.objects.all()
    data = []

    for employe in employes:
        visage = Visage.objects.filter(employe=employe).first()  
        dernier_acces = AccesLog.objects.filter(employe=employe).order_by('-date_entree').first()  
        data.append({
            'employe': employe,
            'visage': visage,
            'dernier_acces': dernier_acces
        })

    return render(request, 'serveur/employe_list.html', {'data': data})
