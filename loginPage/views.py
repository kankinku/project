from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm

from .models import SchoolUser

def auth_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    error_message = None  # 에러 메시지 변수

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['passwd']

                try:
                    user = SchoolUser.objects.using('school_score').get(uid=email)
                    if user.passwd == password:
                        request.session['user_email'] = user.uid
                        request.session['user_name'] = user.name
                        return redirect('dashboard')
                    else:
                        error_message = 'The password is incorrect.'
                except SchoolUser.DoesNotExist:
                    error_message = 'The email address does not exist.'

        elif 'register' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                uid = register_form.cleaned_data['email']
                name = register_form.cleaned_data['username']
                passwd = register_form.cleaned_data['passwd']

                if SchoolUser.objects.using('school_score').filter(uid=uid).exists():
                    error_message = 'This email is already registered.'
                else:
                    SchoolUser.objects.using('school_score').create(
                        uid=uid,
                        name=name,
                        passwd=passwd
                    )
                    request.session['user_email'] = uid
                    request.session['user_name'] = name
                    return redirect('dashboard')

    return render(request, 'login_page.html', {
        'login_form': login_form,
        'register_form': register_form,
        'error_message': error_message
    })

def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    if 'user_email' not in request.session:
        return redirect('login')

    return render(request, 'dashboard.html', {
        'user': {
            'email': request.session['user_email'],
            'name': request.session['user_name'],
        }
    })
