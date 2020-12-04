from io import BytesIO

import factory
from PIL import Image
from django.core.files.base import File

from users.models import UserProfile


def get_image_file(name='test.png', ext='png', size=(500, 500), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGBA", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = factory.Sequence(lambda n: 'foobar{}'.format(n))
    email = factory.Sequence(lambda n: 'foobar{}@foobar.com'.format(n))
    password = 'foobar'
    avatar = get_image_file()
