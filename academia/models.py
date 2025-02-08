from django.db import models
from django.conf import settings

# Create your models here.

# Modelo para materias
class Subjects(models.Model):
  nombre_materia = models.CharField(max_length=50)
  creditos = models.IntegerField()
  horas = models.IntegerField()

  teacher_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='Profesor',
    help_text='Profesor que imparte la materia',
    default=3
  )

  def __str__(self):
    return self.nombre_materia

# Modelo para inscripciones
class Enrollments(models.Model):
  subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)

  student_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='Estudiantes',
    help_text='Estudiante inscrito en la materia',
    default=4
  )

  calificacion = models.FloatField(null=True, blank=True)

  class Meta:
    unique_together = ['subject_id', 'student_id'] # Evita inscripciones duplicadas

  def __str__(self):
    return f"{self.subject_id} - {self.student_id}"

# Modelo para calificaciones
class Grades(models.Model):
  student_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    help_text='Estudiante al que se le asigna la calificación'
  )

  subject_id = models.ForeignKey(
    Subjects,
    on_delete=models.CASCADE,
  )