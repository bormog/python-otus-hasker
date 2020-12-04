import shutil
import tempfile

from django.core.files.storage import default_storage
from django.db.utils import IntegrityError
from django.test import TestCase, override_settings

from .fixtures import UserFactory

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestModels(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_user_can_upload_avatar(self):
        user = UserFactory.create()
        self.assertTrue(default_storage.exists(user.avatar.name))
        self.assertTrue(default_storage.exists(user.thumbnail_name))

    def test_user_has_unique_email(self):
        UserFactory.create(email='foo@bar.com')
        with self.assertRaises(IntegrityError):
            UserFactory.create(email='foo@bar.com')

    def test_user_has_unique_username(self):
        UserFactory.create(username='foobar')
        with self.assertRaises(IntegrityError):
            UserFactory.create(username='foobar')
