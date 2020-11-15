import os
import shutil
import tempfile
from io import BytesIO
from PIL import Image

from django.core.files.base import File
from django.test import TestCase, override_settings
from django.urls import reverse_lazy

from users.models import UserProfile

MEDIA_ROOT = tempfile.mkdtemp()


def get_image_file(name='test.png', ext='png', size=(500, 500), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGBA", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


class TestViews(TestCase):

    def test_login_form_has_required_fields(self):
        response = self.client.get(reverse_lazy('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.context['form'].fields)
        self.assertIn('password', response.context['form'].fields)

    def test_register_form_has_required_fields(self):
        response = self.client.get(reverse_lazy('users:register'))
        self.assertEqual(response.status_code, 200)
        fields = ('username', 'email', 'password1', 'password2', 'avatar')

        for field in fields:
            with self.subTest():
                self.assertIn(field, response.context['form'].fields)
                self.assertTrue(response.context['form'].fields[field].required)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestModels(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_user_can_upload_avatar(self):
        user = UserProfile.objects.create_user('foobar', 'foobar@foobar.com',
                                               'foobar',
                                               avatar=get_image_file())
        self.assertTrue(os.path.exists(user.avatar.path))
        self.assertTrue(os.path.exists(user.thumbnail_path))

