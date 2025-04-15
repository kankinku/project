from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('admin', 'Admin')])

class SchoolUser(models.Model):
    uid = models.EmailField(primary_key=True)  # 이메일
    passwd = models.CharField(max_length=128)  # 비밀번호
    name = models.CharField(max_length=100)    # 이름

    class Meta:
            db_table = 'user_info'
            app_label = 'loginPage'  
            managed = False 

class user_info(models.Model):
    UID = models.CharField(max_length=50, primary_key=True)  # UID는 고유해야 하므로 primary_key로 설정
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'user_info'  # 테이블 이름 지정


class ClassInfo(models.Model):
    UID = models.ForeignKey(user_info, on_delete=models.CASCADE, db_column='UID')  # 외래키로 연결
    class_name = models.CharField(max_length=100)
    class_type = models.CharField(max_length=50)
    class_time = models.CharField(max_length=50)
    class_grade = models.CharField(max_length=10)
    create_grade = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'class_info' 