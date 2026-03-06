from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class ComplaintForm(forms.ModelForm):
    class Meta:
        model=Complaint
        fields=['location','description']


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

        