# Generated by Django 5.0.4 on 2024-05-12 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_alter_parent_parent_id_alter_student_student_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='parent_id',
            field=models.UUIDField(default=84192, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.UUIDField(default=95956, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_id',
            field=models.UUIDField(default=48804, editable=False, unique=True),
        ),
    ]