from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    model = User
    fields = UserCreationForm.Meta.fields + ('avatar',)


class CustomUserChangeForm(UserChangeForm):
    model = User
    fields = UserChangeForm.Meta.fields + ('avatar',)
