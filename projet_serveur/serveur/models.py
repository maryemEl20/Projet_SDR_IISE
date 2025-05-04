from django.db import models
import os

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    matricule = models.CharField(max_length=50, unique=True)

class Visage(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='visages/')

    def __str__(self):
        return f"Visage de {self.employe.nom}"

class AccesLog(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_entree = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Accès de {self.employe.nom} à {self.date_entree}"

def save(self, *args, **kwargs):
        if not self.image_path.name.startswith(self.employe.nom):
            self.image_path.name = os.path.join('visages', self.employe.nom, os.path.basename(self.image_path.name))
        super().save(*args, **kwargs)