from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Modelo para materias
class Subjects(models.Model):
  nombre_materia = models.CharField(max_length=50, unique=True)
  creditos = models.IntegerField()
  horas = models.IntegerField()

  teacher_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='materias_impartidas',
    help_text='Profesor que imparte la materia'
  )

  def __str__(self):
    return self.nombre_materia

# Modelo para inscripciones
class Enrollments(models.Model):
  subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='inscripciones')
  student_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='materias_inscritas',
    help_text='Estudiante inscrito en la materia'
  )

  calificacion = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

  class Meta:
    unique_together = ['subject_id', 'student_id']  # Evita inscripciones duplicadas

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