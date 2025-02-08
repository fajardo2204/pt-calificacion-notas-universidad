from django.urls import path
from .views import (
  TeacherListView,
  TeacherRegisterView,
  #TeacherDashboardView
)

urlpatterns = [
  path('register/', TeacherRegisterView.as_view(), name='teacher-register'),
  path('list/', TeacherListView.as_view(), name='teacher-list'),
  #path('dashboard/', TeacherDashboardView.as_view(), name='professor_dashboard'),
]