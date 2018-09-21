from django import forms
from .models import Post, Category


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(
        required=True,
        label='FirstName',
        max_length=32
    )
    last_name = forms.CharField(
        required=True,
        label='LastName',
        max_length=32
    )
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )
    city = forms.CharField(
        required=True,
        label='City',
        max_length=32
    )
    state = forms.CharField(
        required=True,
        label='State',
        max_length=32
    )

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'seo_title', 'seo_description', 'status']
        widget = {
            'title' :forms.TextInput(attrs={'class': 'form-control'}),
            'body' :forms.Textarea(attrs={'class': 'form-control'}),
            'category' :forms.Select(attrs={'class': 'form-control'}),
            'seo_title' :forms.TextInput(attrs={'class': 'form-control'}),
            'seo_description' :forms.TextInput(attrs={'class': 'form-control'}),
            'status' :forms.Select(attrs={'class': 'form-control'}),
        }























