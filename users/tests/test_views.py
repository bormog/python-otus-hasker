from django.test import TestCase
from django.urls import reverse_lazy


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
