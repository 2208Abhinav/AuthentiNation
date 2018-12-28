from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UpdateUserProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
