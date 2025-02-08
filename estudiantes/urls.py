from django.urls import path
from .views import (
  StudentDashboardView,
  StudentRegisterView,
  StudentListView
)

urlpatterns = [
  path('register/', StudentRegisterView.as_view(), name='student_register'),
  path('dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
  path('list/', StudentListView.as_view(), name='student-list'),
]
