from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

# Payload del JWT según el tipo de usuario
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        '''
        Agregar información adicional al token
        En este caso, comprobar si el usuario es un profesor o un estudiante
        '''
        if hasattr(user, 'TeacherProfile'):
          token['user_type'] = 'profesor'
        elif hasattr(user, 'StudentProfile'):
          token['user_type'] = 'estudiante'
        else:
          token['user_type'] = 'usuario desconocido'
        return token

# Serializador para el hash de la contraseña
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, min_length=8)

  class Meta:
    model = User
    fields = ('username', 'email', 'password')

  def createPassword(self, validated_data):
    password = validated_data.pop('password', None)
    user = User(**validated_data)
    user.set_password(password) # Hasheo de la contraseña
    user.save()
    return user
