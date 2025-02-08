from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import StudentRegisterSerializer, StudentListSerializer
from .models import StudentProfile

# Create your views here.

# vista para el registro de estudiantes
class StudentRegisterView(generics.CreateAPIView):
  serializer_class = StudentRegisterSerializer
  permission_classes = []

  def post(self, request):
    serializer = StudentRegisterSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Vista para listar estudiantes
class StudentListView(generics.ListAPIView):
  queryset = StudentProfile.objects.all()
  serializer_class = StudentListSerializer
  permission_classes = [IsAuthenticated]

# Vista para el login de estudiantes
# class StudentLoginView(APIView):

# vista para el panel de estudiantes
class StudentDashboardView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    # Lógica para obtener los datos del estudiante y materias inscritas
    data = {
      'user': request.user.username,
      'message': 'Bienvenido al panel de estudiantes'
    }
    return Response(data)