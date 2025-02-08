from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView
from usuarios.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas de verificación de tokens
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas para autenticación
    path('teachers/', include('profesores.urls')),
    path('students/', include('estudiantes.urls')),

    # Rutas para la academia
    path('academy/', include('academia.urls')),
]
