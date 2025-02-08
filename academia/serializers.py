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
    try:
      teacher = request.user.teacher
    except:
      raise serializers.ValidationError('No tienes permisos para crear materias')
    validated_data['teacher_id'] = teacher
    return super().create(validated_data)

# Serializador para inscripciones
class EnrollmentsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Enrollments
    fields = ('subject_id', 'student_id')
    read_only_fields = ('subject_id',)

  def create(self, validated_data):
    request = self.context.get('request')
    student = request.user
    return Enrollments.objects.create(student_id=student, **validated_data)


# Serializador para listar materias
class SubjectsSerializer(serializers.ModelSerializer):
  students = EnrollmentsSerializer(many=True, read_only=True)
  teacher = User

  class Meta:
    model = Enrollments
    fields = ('nombre_materia', 'students', 'teacher',)