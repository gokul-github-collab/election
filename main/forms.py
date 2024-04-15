from django.forms import  ModelForm
from .models import User, Voters
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class VoterForm(ModelForm):
    class Meta:
        model = Voters
        exclude = ('vote', )

    def clean_age(self):
        age = self.cleaned_data['age']
        if age <= 18:
            raise ValidationError("Age must be greater than 18.")
        return age