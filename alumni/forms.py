from django import forms

from .models import Post,Comment,Alumni

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class ProfileForm(forms.ModelForm):

    class Meta:
        model=Alumni
        fields=('name','profile_img','fb_link','ln_link','curr_work','prev_work',)
