from django.conf import settings
from django.db import models

# Create your models here.

class TeacherProfile (models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  department = models.CharField(max_length=25)

  def __str__(self):
    return f"Profesor: {self.user.username} - Departamento: {self.department}"