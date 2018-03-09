from django import forms
from django.contrib.auth.models import User,Group
from alumni.models import Alumni
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    group=forms.ModelChoiceField(queryset=Group.objects.all(),required=True)
    #name = forms.CharField(max_length=30, required=True)
    name = forms.CharField(max_length=30, required=True)
    fb_link = forms.URLField(required=True)
    ln_link = forms.URLField(required=True)
    curr_work = forms.CharField(max_length=100, required=True)
    pre_work = forms.CharField(max_length=200, required=True)
    class Meta:
        model = User
        fields = ['username','name','fb_link','ln_link','curr_work','pre_work','password','group',]

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.name = self.cleaned_data["name"]
        user.ln_link = self.cleaned_data["ln_link"]
        user.fb_link = self.cleaned_data["fb_link"]
        user.curr_work = self.cleaned_data["curr_work"]
        user.pre_work = self.cleaned_data["pre_work"]
        if commit:
            user.save()
        return user