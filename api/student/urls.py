from django.urls import path
from .views import (
    MyClassmatesApi,
    StudentApi,
    MyGradesApi,
    MyAttendanceApi
)


urlpatterns = [
    path('student/classmates/', MyClassmatesApi.as_view()),
    path('student/<int:pk>/', StudentApi.as_view()),
    path('student/grades/', MyGradesApi.as_view()),
    path('student/attendance', MyAttendanceApi.as_view())
]
