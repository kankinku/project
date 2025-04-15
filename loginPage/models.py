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