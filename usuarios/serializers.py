from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Agregar información adicional al token
        if hasattr(user, 'teacherprofile'):
            token['user_type'] = 'teacher'
        elif hasattr(user, 'studentprofile'):
            token['user_type'] = 'student'
        else:
            token['user_type'] = 'unknown'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Verificar si el usuario está activo
        if not self.user.is_active:
            raise serializers.ValidationError('No existe una cuenta activa con estas credenciales.')

        return data

# Serializador para el hash de la contraseña
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password is not None:
            user.set_password(password)  # Hasheo de la contraseña
        user.save()
        return user
