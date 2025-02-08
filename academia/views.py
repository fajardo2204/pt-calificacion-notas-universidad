from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .serializers import (
  CreateSubjectsSerializer,
  EnrollmentsSerializer,
  SubjectsSerializer,
)
from .models import (
  Subjects,
  Enrollments
)

# Create your views here.

# Vista para crear materias
class SubjectsCreateView(generics.CreateAPIView):
  queryset = Subjects.objects.all()
  serializer_class = CreateSubjectsSerializer
  permission_classes = [permissions.IsAuthenticated]

  def perform_create(self, serializer):
    # Verificar si el usuario es profesor
    if not hasattr(self.request.user, 'teacherprofile'):
      raise PermissionDenied('No tienes permisos para crear materias')
    serializer.save(teacher_id=self.request.user)

# Vista para inscribir materias
class EnrollmentsView(generics.CreateAPIView):
  queryset = Enrollments.objects.all()
  serializer_class = EnrollmentsSerializer
  permission_classes = [permissions.IsAuthenticated]

# Vista para listar materias
class SubjectsListView(generics.ListCreateAPIView):
  serializer_class = SubjectsSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return Subjects.objects.filter(teachers__teacher_id=self.request.user)

  def perform_create(self, serializer):
    serializer.save(teacher=self.request.user)

# Vista para ver detalle de una materia y alumnos inscritos
class SubjectsDetailView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = SubjectsSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return Subjects.objects.filter(teachers__teacher_id=self.request.user)