from PIL import Image, ImageOps
from io import StringIO
import os
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/')

    # todo move size to settings
    # todo move to signals-callback
    # todo make property User.thumbnail_url
    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        if self.avatar:
            file, ext = os.path.splitext(self.avatar.path)
            image = Image.open(self.avatar.path)
            thumbnail = ImageOps.fit(image, (200, 200), Image.ANTIALIAS)
            thumbnail.save(file + '.thumbnail' + ext)

