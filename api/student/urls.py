from django.urls import path
from .views import (
    StudentCalendarApi,
    StudentAttendanceApi,
    StudentLessonApi,
    StudentGradeApi,
    StudentClassmatesApi
)

urlpatterns = [
    path('calendar/', StudentCalendarApi.as_view()),
    path('attendance/', StudentAttendanceApi.as_view()),
    path('lesson/', StudentLessonApi.as_view()),
    path('grades/', StudentGradeApi.as_view()),
    path('classmates/', StudentClassmatesApi.as_view())
]

