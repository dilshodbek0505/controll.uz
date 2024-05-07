from django.contrib import admin

from .models import (
    Student,
    Teacher,
    Parent,
    User
)

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
