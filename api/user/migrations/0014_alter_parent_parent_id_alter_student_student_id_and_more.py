# Generated by Django 5.0.4 on 2024-05-06 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_parent_parent_id_alter_student_student_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='parent_id',
            field=models.UUIDField(default=60825, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.UUIDField(default=17792, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_id',
            field=models.UUIDField(default=49151, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='static/img/user.jpg', null=True, upload_to='user/image/'),
        ),
    ]
