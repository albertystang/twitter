from django import forms
from .models import Meep, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Profile extas form
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile Picture')
    profile_bio = forms.CharField(label='Profile Bio', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Profile Bio'}))
    homepage_link = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website Link'}))
    facebook_link = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook Link'}))
    instagram_link = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instagram Link'}))
    linkedin_link = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Linkedin Link'}))

    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio', 'homepage_link', 'facebook_link', 'instagram_link', 'linkedin_link')


class MeepForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Enter your Musker Meep!",
                "class": "form-control"
            }
        ),
        label=""
    )
    
    class Meta:
        model = Meep
        exclude = ("user", "likes")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
