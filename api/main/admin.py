from django.contrib import admin

from .models import (
    Course,
    Subject,
    Grade,
    Attendance,
    Season,
    LessonTime,
    Lesson
)

admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(LessonTime)
admin.site.register(Season)
admin.site.register(Grade)
admin.site.register(Attendance)


