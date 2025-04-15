from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import ClassInfoForm, LoginForm, RegisterForm

from .models import ClassInfo, SchoolUser, user_info

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

from .forms import CreateClassForm  # 폼을 import 해주세요

def create_class(request):
    if 'user_email' not in request.session:
        return redirect('login')

    # 이메일로 user_info 인스턴스를 찾아옴
    try:
        user = user_info.objects.get(UID=request.session['user_email'])
    except user_info.DoesNotExist:
        return redirect('login')  # 사용자가 없으면 로그인 페이지로

    if request.method == 'POST':
        form = CreateClassForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  # cleaned_data로 값 가져오기

            ClassInfo.objects.create(
                UID=user,  # user_info 객체를 외래키로 넣음
                class_name=cd['class_name'],
                class_type=cd['class_type'],
                class_time=cd['class_time'],
                class_grade=cd['class_grade'],
                create_grade=cd['create_grade'],
            )
            return redirect('dashboard')
    else:
        form = CreateClassForm()

    return render(request, 'create_class.html', {'form': form})

def dashboard(request):
    if 'user_email' not in request.session:
        return redirect('login')

    return render(request, 'dashboard.html', {
        'user': {
            'email': request.session['user_email'],
            'name': request.session['user_name'],
        }
    })

def delete_class(request):
    if 'user_email' not in request.session:
        return redirect('login')

    try:
        user = user_info.objects.get(UID=request.session['user_email'])
    except user_info.DoesNotExist:
        return redirect('login')

    # 현재 로그인된 사용자가 만든 모든 class_info 불러오기
    class_list = ClassInfo.objects.filter(UID=user)

    return render(request, 'delete_class.html', {
        'user': {
            'email': user.UID,
            'name': user.name,
        },
        'classes': class_list
    })