from django.urls import path
from .views import (
  SubjectsCreateView,
  EnrollmentsView,
  SubjectsListView,
  SubjectsDetailView
)

urlpatterns = [
  path('student/enrollments/', EnrollmentsView.as_view(), name='enrollments'),
  path('student/subjects/', SubjectsListView.as_view(), name='subjects-list'),
  path('teacher/create/subject/', SubjectsCreateView.as_view(), name='create-subject'),
  path('teacher/subjects/', SubjectsDetailView.as_view(), name='subjects-detail'),
]
