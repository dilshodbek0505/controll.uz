# Generated by Django 5.0.4 on 2024-05-12 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_lesson_lesson_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_status',
            field=models.CharField(choices=[('tugagan', 'tugagan'), ('boshlangan', 'boshlangan'), ('kutilmoqda', 'kutilmoqda')], default='kutilmoqda', max_length=50),
        ),
    ]