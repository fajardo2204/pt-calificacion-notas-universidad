from rest_framework import serializers
from usuarios.serializers import UserSerializer
from .models import StudentProfile

class StudentRegisterSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  career = serializers.CharField(required=True)

  class Meta:
    model = StudentProfile
    fields = ('user', 'career')

  def create(self, validated_data):
    user_data = validated_data.pop('user')
    user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    student_profile = StudentProfile.objects.create(user=user, **validated_data)
    return student_profile

