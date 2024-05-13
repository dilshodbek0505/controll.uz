# Generated by Django 5.0.4 on 2024-05-12 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_alter_parent_parent_id_alter_student_student_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='parent_id',
            field=models.UUIDField(default=58018, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.UUIDField(default=61116, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_id',
            field=models.UUIDField(default=93711, editable=False, unique=True),
        ),
    ]
