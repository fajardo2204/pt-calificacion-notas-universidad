from rest_framework import serializers
from .models import (
  Subjects,
  Enrollments,
  Grades
)
from usuarios.serializers import UserSerializer

User = UserSerializer()

# Serializador para crear materias
class CreateSubjectsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Subjects
    fields = ('nombre_materia', 'creditos', 'horas', 'teacher_id')
    read_only_fields = ('teacher_id',)

  def create(self, validated_data):
    request = self.context.get('request')
    validated_data['teacher_id'] = request.user
    return super().create(validated_data)

# Serializador para inscripciones
class EnrollmentsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Enrollments
    fields = ('subject_id', 'student_id')
    read_only_fields = ('student_id',)

  def create(self, validated_data):
    request = self.context.get('request')
    student = request.user
    validated_data['student_id'] = student
    return Enrollments.objects.create(**validated_data)

# Serializador para listar materias como profesor
class SubjectsSerializer(serializers.ModelSerializer):
  students = EnrollmentsSerializer(many=True, read_only=True)
  teacher = User

  class Meta:
    model = Subjects
    fields = ('nombre_materia', 'students', 'teacher',)