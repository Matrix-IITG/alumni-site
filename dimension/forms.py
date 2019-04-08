from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from dimension.models import Confrence

class ConfrenceSignupForm(forms.ModelForm):
    class Meta:
        model = Confrence
        fields = ('name', 'contact' , 'email' , 'college','state','city','transaction')





