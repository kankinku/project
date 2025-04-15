from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    passwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

class RegisterForm(forms.ModelForm):
    passwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    role = forms.ChoiceField(
        choices=[('user', 'User'), ('admin', 'Admin')],
        widget=forms.Select()
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
