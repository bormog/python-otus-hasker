from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=150)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'avatar', )

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email