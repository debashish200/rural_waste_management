from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class ComplaintForm(forms.ModelForm):
    class Meta:
        model=Complaint
        fields=['location','description']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']


    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)

        #Revomes Help text
        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs['class'] = 'form-control' 