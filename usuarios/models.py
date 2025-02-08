from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# Se crea la clase CustomUser que hereda de AbstractUser para desarrollar diferentes clases de usuarios
class CustomUser(AbstractUser):
  email = models.EmailField(unique=True)
  user_type = models.CharField(max_length=10)
  is_active = models.BooleanField(default=True)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']