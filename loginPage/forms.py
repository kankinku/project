# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import ClassInfo

DAYS = ['일','월', '화', '수', '목', '금','토']
PERIODS = ['1', '2', '3', '4', '5', '6', '7', '8']

CLASS_TIME_CHOICES = [
    (f"{day}{period}", f"{day}요일 {period}교시") for day in DAYS for period in PERIODS
]

GRADE_CHOICES = [
    ('1학년', '1학년'),
    ('2학년', '2학년'),
    ('3학년', '3학년'),
    ('4학년', '4학년')
]

# 새롭게 추가된 학점 선택지 (성적 등급)
GRADE_INPUT_CHOICES = [
    ('A+', 'A+'), ('A0', 'A0'),
    ('B+', 'B+'), ('B0', 'B0'),
    ('C+', 'C+'), ('C0', 'C0'),
    ('D+', 'D+'), ('D0', 'D0'),
    ('F', 'F')
]

GRADE_TO_POINT = {
    'A+': 4.5, 'A0': 4.0,
    'B+': 3.5, 'B0': 3.0,
    'C+': 2.5, 'C0': 2.0,
    'D+': 1.5, 'D0': 1.0,
    'F': 0.0
}

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
        fields = ['class_name', 'class_type', 'class_time', 'class_grade','create_grade']

class CreateClassForm(forms.Form):
    class_name = forms.CharField(max_length=100, label='Class Name')
    class_type = forms.ChoiceField(
        choices=[('전공', '전공'), ('교양', '교양'),('취미','취미'),('일','일')],
        label='Class Type'
    )
    class_time = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'class-time-input',
            'type': 'hidden',
        })
    )
    class_grade = forms.ChoiceField(
        choices=GRADE_CHOICES,
        label='학년 선택'
    )

class GradeInputForm(forms.ModelForm):
    class Meta:
        model = ClassInfo
        fields = ['class_id','create_grade']
        widgets = {
            'create_grade': forms.Select(choices=GRADE_INPUT_CHOICES)
        }
