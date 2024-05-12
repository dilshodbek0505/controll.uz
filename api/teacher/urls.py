from django.urls import path
from .views import (
   AttendanceApi,
   MyScheduleApi, 
)


urlpatterns = [
    path('teacher/attendance/',AttendanceApi.as_view()),
    path('teacher/schedule/', MyScheduleApi.as_view())
]
