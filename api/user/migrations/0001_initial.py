# Generated by Django 5.0.4 on 2024-05-05 17:22

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(help_text='Foydalanuvchining ismi', max_length=255)),
                ('last_name', models.CharField(help_text='Foydalanuvchining familiyasi', max_length=255)),
                ('middle_name', models.CharField(help_text='Foydalanuvchining sharfi', max_length=255)),
                ('username', models.CharField(error_messages={'unique': "Foydalanuvchi nomi takrorlanmas bo'lishi keark!"}, help_text='Foydalanuvchi nomi', max_length=255, unique=True)),
                ('phone_number', models.CharField(error_messages={'unique': "Foydalanuvchi telfon raqami takrorlanmas bo'lishi keark!"}, help_text='Foydalanuvchining telfon raqami', max_length=255, unique=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='user/image/')),
                ('role', models.CharField(choices=[('admin', 'admin'), ('student', 'student'), ('teacher', 'teacher'), ('parent', 'parent')], help_text="Foydalanuvchining tizimdagi o'rni", max_length=255)),
                ('updated', models.DateTimeField(auto_now=True, help_text='Taxrir qilingan vaqti')),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('student_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course')),
            ],
            options={
                'abstract': False,
            },
            bases=('user.user',),
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('children', models.ManyToManyField(to='user.student')),
            ],
            options={
                'abstract': False,
            },
            bases=('user.user',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.subject')),
            ],
            options={
                'abstract': False,
            },
            bases=('user.user',),
        ),
    ]
