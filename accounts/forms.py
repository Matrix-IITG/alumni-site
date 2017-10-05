from django import forms
from django.contrib.auth.models import User
from .models import Profile
import datetime

curr=datetime.datetime.now().year
YEARS=[]
for i in range(2000, curr+1):
    dum=[(i, str(i))]
    YEARS=YEARS+dum


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    class Meta:
        model =User
        fields = ("first_name", "last_name", "email")

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('year', 'fb_link', 'ln_link', 'curr_work', 'prev_work', 'pro_img' )

class CreateProfileForm(forms.ModelForm):
    # year = forms.ChoiceField(choices=YEARS, required=True)
    class Meta:
        model = Profile
        fields = ('year', 'fb_link', 'ln_link', 'curr_work', 'prev_work', 'pro_img' )
        
