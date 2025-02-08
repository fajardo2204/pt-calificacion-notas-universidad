from django.conf import settings
from django.db import models

# Create your models here.

class StudentProfile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  career = models.CharField(max_length=25)

  def __str__(self):
    return f"Estudiante: {self.user.username} - Carrera: {self.career}"