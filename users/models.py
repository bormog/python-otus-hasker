import os

from PIL import Image, ImageOps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=settings.USER_IMAGE_DIR)

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        if self.avatar:
            image = Image.open(self.avatar.path)
            thumbnail = ImageOps.fit(image, settings.USER_IMAGE_SIZE, Image.ANTIALIAS)
            thumbnail.save(self.thumbnail_path)

    @property
    def thumbnail_path(self):
        if self.avatar:
            file, ext = os.path.splitext(self.avatar.path)
            return '%s.thumbnail%s' % (file, ext)

    @property
    def thumbnail_url(self):
        if self.avatar:
            file, ext = os.path.splitext(self.avatar.url)
            return '%s.thumbnail%s' % (file, ext)
