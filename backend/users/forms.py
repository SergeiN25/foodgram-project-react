from django import forms
from django.contrib.auth.forms import AuthenticationForm
from users.models import User


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )

    class Meta:
        model = User
        fields = ('username', 'password')
