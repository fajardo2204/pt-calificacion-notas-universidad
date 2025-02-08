from rest_framework import serializers
from usuarios.serializers import UserSerializer

from .models import TeacherProfile

# Serializador para registrar profesores
class TeacherRegisterSerializer(serializers.ModelSerializer):
  # Definir los campos del usuario
  user = UserSerializer()
  department = serializers.CharField(required=True)

  class Meta:
    model = TeacherProfile
    fields = ('user', 'department')

  def create(self, validated_data):
    user_data = validated_data.pop('user')
    user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    user.is_active = True  # Asegúrate de que el usuario esté activo
    user.save()
    teacher_profile = TeacherProfile.objects.create(user=user, **validated_data)
    return teacher_profile

# Serializador para listar profesores
class TeacherListSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = TeacherProfile
    fields = ('user', 'department')