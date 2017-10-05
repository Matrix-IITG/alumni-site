from django import forms
from django.contrib.auth.models import User
from .models import Profile
import datetime

curr = datetime.datetime.now().year
YEARS = []
for i in range(2000, curr + 1):
    dum = [(i, str(i))]
    YEARS = YEARS + dum


class EditUserForm(forms.ModelForm):
    #first_name = forms.CharField(max_length=30, required=True)
    # first_name = forms.CharField(label="First Name:", max_length=30,
    #                            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'firstname'}))
    # last_name = forms.CharField(label="Last Name:", max_length=30,
    #                            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'lastname'}))
    # email = forms.CharField(label="Email id:", max_length=30,
    #                                   widget=forms.EmailInput(attrs={'class': 'form-control', 'name': 'emailid'}))
    #
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {
            "first_name": "First Name:",
            "last_name": "Last Name:",
            "email": "Email Id:"
        }

class EditProfileForm(forms.ModelForm):
    # year = forms.ChoiceField(label="Graduation Year:", choices=YEARS, required=True)
    # fb_link = forms.URLField(label="Facebook Id Link:", max_length=30,
    #                             widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'lastname'}))
    # email = forms.CharField(label="Email id:", max_length=30,
    #                         widget=forms.EmailInput(attrs={'class': 'form-control', 'name': 'emailid'}))

    class Meta:
        model = Profile
        fields = ('year', 'fb_link', 'ln_link', 'curr_work', 'prev_work', 'pro_img')
        labels = {
            "year": "Graduation Year:",
            "fb_link": "Facebook Profile Link:",
            "ln_link": "LinkedIn Profile Link:",
            "curr_work": "Currently working at:",
            "prev_work": "Previously worked at:",
            "pro_img": "Upload a recent image:"
        }


class CreateProfileForm(forms.ModelForm):
    # year = forms.ChoiceField(choices=YEARS, required=True)
    class Meta:
        model = Profile
        fields = ('year', 'fb_link', 'ln_link', 'curr_work', 'prev_work', 'pro_img')
        labels = {
            "year": "Graduation Year:",
            "fb_link": "Facebook Profile Link:",
            "ln_link": "LinkedIn Profile Link:",
            "curr_work": "Currently working at:",
            "prev_work": "Previously worked at:",
            "pro_img": "Upload a recent image:"
        }