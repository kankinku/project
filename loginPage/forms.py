from django import forms
from django.contrib.auth.models import User
from .models import ClassInfo

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

class ClassInfoForm(forms.ModelForm):
    class Meta:
        model = ClassInfo
        fields = ['class_name', 'class_type', 'class_time', 'class_grade', 'create_grade']

class CreateClassForm(forms.Form):
    class_name = forms.CharField(max_length=100, label='Class Name')
    class_type = forms.ChoiceField(choices=[('type1', '전공'), ('type2', '교양')], label='Class Type')
    class_time = forms.CharField(max_length=50, label='Class Time')
    class_grade = forms.CharField(max_length=10, label='Class Grade')
    create_grade = forms.CharField(max_length=10, label='Create Grade')