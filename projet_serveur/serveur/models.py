from django.db import models

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
  