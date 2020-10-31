from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/')
