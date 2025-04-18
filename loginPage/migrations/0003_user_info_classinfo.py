# Generated by Django 5.2 on 2025-04-16 01:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginPage', '0002_alter_schooluser_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('UID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
        migrations.CreateModel(
            name='ClassInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
                ('class_type', models.CharField(max_length=50)),
                ('class_time', models.CharField(max_length=50)),
                ('class_grade', models.CharField(max_length=10)),
                ('create_grade', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('UID', models.ForeignKey(db_column='UID', on_delete=django.db.models.deletion.CASCADE, to='loginPage.user_info')),
            ],
            options={
                'db_table': 'class_info',
            },
        ),
    ]
