from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
  TeacherRegisterSerializer,
  TeacherListSerializer
)
from .models import TeacherProfile

# Create your views here.

# vista para el registro de profesores
class TeacherRegisterView(generics.CreateAPIView):
  serializer_class = TeacherRegisterSerializer
  permission_classes = []

  def post(self, request):
    serializer = TeacherRegisterSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Vista para el listado de profesores
class TeacherListView(generics.ListAPIView):
  queryset = TeacherProfile.objects.all()
  serializer_class = TeacherListSerializer
  permission_classes = [IsAuthenticated]

'''
# Vista para el panel de profesores
class TeacherDashboardView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    # Lógica para obtener los datos del profesor
    data = {
      'user': request.user.username,
      'message': 'Bienvenido al panel de profesores'
    }
    return Response(data)
'''