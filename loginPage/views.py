import ast
import json
from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import ClassInfoForm, LoginForm, RegisterForm, GradeInputForm, GRADE_TO_POINT
from django.forms import modelformset_factory

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
                    user = SchoolUser.objects.using('').get(uid=email)
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

from .forms import CreateClassForm  

def create_class(request):
    if 'user_email' not in request.session:
        return redirect('login')

    try:
        user = user_info.objects.get(UID=request.session['user_email'])
    except user_info.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        form = CreateClassForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ClassInfo.objects.create(
                UID=user,
                class_name=cd['class_name'],
                class_type=cd['class_type'],
                class_time=cd['class_time'],
                class_grade=cd['class_grade'],
                create_grade=None  # ← 지금은 학점 미입력 상태
            )
            return redirect('dashboard')
    else:
        form = CreateClassForm()

    return render(request, 'create_class.html', {'form': form})

import json  

# def create_class(request):
#     if 'user_email' not in request.session:
#         return redirect('login')

#     try:
#         user = user_info.objects.get(UID=request.session['user_email'])
#     except user_info.DoesNotExist:
#         return redirect('login')

#     form = None  # 🔥 무조건 초기화해두기

#     if request.method == 'POST':
#         form = CreateClassForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             try:
#                 parsed_times = json.loads(cd['class_time'])
#             except json.JSONDecodeError:
#                 parsed_times = []
#                 print("빈 array") 

#             ClassInfo.objects.create(
#                 UID=user,
#                 class_name=cd['class_name'],
#                 class_type=cd['class_type'],
#                 class_time=parsed_times,
#                 class_grade=cd['class_grade'],
#                 create_grade=None
#             )
#             return redirect('dashboard')
#     else:
#         print("error")
#         form = CreateClassForm()

#     return render(request, 'create_class.html', {'form': form})



def dashboard(request):
    if 'user_email' not in request.session:
        return redirect('login')
    
    try:
        user = user_info.objects.get(UID=request.session['user_email'])
    except user_info.DoesNotExist:
        return redirect('login')

    class_list = ClassInfo.objects.filter(UID=user)
    
    parsed_classes = []
    for c in class_list:
        try:
            time_data = json.loads(c.class_time)
        except (json.JSONDecodeError, TypeError):
            time_data = []

        parsed_classes.append({
            'name': c.class_name,
            'time': time_data
        })


    return render(request, 'dashboard.html', {
        'user': {
            'email': request.session['user_email'],
            'name': request.session['user_name'],
        },
        'class_list_json': json.dumps(parsed_classes, ensure_ascii=False)
        
    })

def delete_class(request):
    if 'user_email' not in request.session:
        return redirect('login')

    try:
        user = user_info.objects.get(UID=request.session['user_email'])
    except user_info.DoesNotExist:
        return redirect('login')

    
    class_list = ClassInfo.objects.filter(UID=user)

    return render(request, 'delete_class.html', {
        'user': {
            'email': user.UID,
            'name': user.name,
        },
        'classes': class_list
    })
    
def delete_selected_classes(request):
    if request.method == "POST":
        if 'user_email' not in request.session:
            return JsonResponse({'status': 'unauthorized'}, status=401)

        try:
            user = user_info.objects.get(UID=request.session['user_email'])
        except user_info.DoesNotExist:
            return JsonResponse({'status': 'unauthorized'}, status=401)

        selected_ids = request.POST.getlist('selected_ids[]')
        ClassInfo.objects.filter(class_id__in=selected_ids, UID=user).delete()

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'invalid'}, status=400)
    
# 학점 계산   
def grade_summary(request):
    user_email = request.session.get('user_email')
    if not user_email:
        return redirect('login')

    try:
        user = user_info.objects.get(UID=user_email)
    except user_info.DoesNotExist:
        return redirect('login')

    
    queryset = ClassInfo.objects.using('school_score').filter(UID=user)
    GradeFormSet = modelformset_factory(ClassInfo, form=GradeInputForm, extra=0)

    if request.method == 'POST':
        print("📦 POST 데이터:", request.POST)
        formset = GradeFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            print("✅ formset 유효함")
            for form in formset:
                print("✅ pk:", form.instance.pk)
                instance = ClassInfo.objects.using('school_score').get(pk=form.instance.pk)
                instance.create_grade = form.cleaned_data['create_grade']
                instance.save(using='school_score')
            return redirect('grade_summary')
    else:
        
        formset = GradeFormSet(queryset=queryset)
        print("❌ formset 유효하지 않음")
        print(formset.errors)
        



    # 평균 계산
    all_points = []
    major_points = []

    for cls in queryset:
        grade = cls.create_grade
        if grade in GRADE_TO_POINT:
            point = GRADE_TO_POINT[grade]
            all_points.append(point)
            if cls.class_type == 'type1':
                major_points.append(point)

    avg_all = round(sum(all_points) / len(all_points), 2) if all_points else 0.0
    avg_major = round(sum(major_points) / len(major_points), 2) if major_points else 0.0

    return render(request, 'grade_summary.html', {
    'formset': formset,
    'avg_all': avg_all,
    'avg_major': avg_major,
    'user_name': request.session.get('user_name'),
})
