from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
  CreateSubjectsSerializer,
  EnrollmentsSerializer,
  SubjectsSerializer,
  GradeSerializer
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
    serializer.save(teacher_id=self.request.user)

# Vista para inscribir materias
class EnrollmentsView(generics.CreateAPIView):
  queryset = Enrollments.objects.all()
  serializer_class = EnrollmentsSerializer
  permission_classes = [permissions.IsAuthenticated]

  def perform_create(self, serializer):
    request = self.request
    user = request.user
    if hasattr(user, 'teacherprofile'):
      raise PermissionDenied('Los profesores no pueden inscribirse en materias como estudiantes.')
    serializer.save(student_id=user)

# Vista para listar materias
class SubjectsListView(generics.ListCreateAPIView):
  serializer_class = SubjectsSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return Subjects.objects.filter(teacher_id=self.request.user)

  def perform_create(self, serializer):
    serializer.save(teacher_id=self.request.user)

# Vista para listar materias impartidas por un profesor junto con los estudiantes inscritos
class TeacherSubjectsView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request, *args, **kwargs):
    user = request.user
    if not hasattr(user, 'teacherprofile'):
      raise PermissionDenied('Solo los profesores pueden ver esta información.')

    subjects = Subjects.objects.filter(teacher_id=user)
    data = []
    for subject in subjects:
      students = Enrollments.objects.filter(subject_id=subject).values('student_id__username', 'calificacion')
      subject_data = {
        'nombre_materia': subject.nombre_materia,
        'creditos': subject.creditos,
        'horas': subject.horas,
        'students': [
          {
            'username': student['student_id__username'],
            'calificacion': student['calificacion'],
            'estado': 'aprobado' if student['calificacion'] is not None and student['calificacion'] >= 2.95 else 'reprobado' if student['calificacion'] is not None else 'sin calificación'
          }
          for student in students
        ]
      }
      data.append(subject_data)
    return Response(data)

# Vista para calificar estudiantes
class GradeStudentView(generics.UpdateAPIView):
  queryset = Enrollments.objects.all()
  serializer_class = GradeSerializer
  permission_classes = [permissions.IsAuthenticated]

  def perform_update(self, serializer):
    enrollment = self.get_object()
    if enrollment.subject_id.teacher_id != self.request.user:
      raise PermissionDenied('Solo el profesor que imparte la materia puede calificar a los estudiantes.')
    serializer.save()