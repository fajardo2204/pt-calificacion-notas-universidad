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
  estado = serializers.SerializerMethodField()

  class Meta:
    model = Enrollments
    fields = ('subject_id', 'student_id', 'calificacion', 'estado')
    read_only_fields = ('student_id',)

  def get_estado(self, obj):
    if obj.calificacion is not None:
      return "aprobado" if obj.calificacion >= 3.0 else "reprobado"
    return "sin calificación"

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

# Serializador para calificar estudiantes
class GradeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Enrollments
    fields = ('calificacion',)

  def validate_calificacion(self, value):
    if value < 0 or value > 5:
      raise serializers.ValidationError("La calificación debe estar entre 0 y 5.0.")
    return value

  def update(self, instance, validated_data):
    instance.calificacion = validated_data.get('calificacion', instance.calificacion)
    instance.save()
    return instance