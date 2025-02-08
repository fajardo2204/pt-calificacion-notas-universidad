from rest_framework import serializers
from usuarios.serializers import UserSerializer
from .models import StudentProfile

# Serializador para registrar estudiantes
class StudentRegisterSerializer(serializers.ModelSerializer):
  # Definir los campos del usuario
  user = UserSerializer()
  career = serializers.CharField(required=True)

  class Meta:
    model = StudentProfile
    fields = ('user', 'career')

  def create(self, validated_data):
    user_data = validated_data.pop('user')
    user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    user.is_active = True  # Asegúrate de que el usuario esté activo
    user.save()
    student_profile = StudentProfile.objects.create(user=user, **validated_data)
    return student_profile

# Serializador para listar estudiantes
class StudentListSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = StudentProfile
    fields = ('user', 'career')