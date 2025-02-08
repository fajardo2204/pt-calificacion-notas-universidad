from django.urls import path
from .views import (
  SubjectsCreateView,
  EnrollmentsView,
  SubjectsListView,
  TeacherSubjectsView
)

urlpatterns = [
  path('student/enrollments/', EnrollmentsView.as_view(), name='enrollments'),
  path('student/subjects/', SubjectsListView.as_view(), name='subjects-list'),
  path('teacher/subjects/create', SubjectsCreateView.as_view(), name='create-subject'),
  path('teacher/subjects/list/', TeacherSubjectsView.as_view(), name='teacher-subjects-list'),
]
