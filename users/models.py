from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/')
