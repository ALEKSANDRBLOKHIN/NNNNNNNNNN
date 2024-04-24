from django import forms
from .models import Post
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ['author', 'post_type', 'title', 'content', 'categories']
            widgets = {
                'post_type': forms.Select(choices=Post.POST_TYPES)
            }



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=63,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))




class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone_number', 'birth_date']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget = forms.Textarea(attrs={'class': 'form-control'})
        self.fields['phone_number'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['birth_date'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})

from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Add a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user