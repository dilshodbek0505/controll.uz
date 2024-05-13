from django.urls import path
from .views import (
    StudentCalendarApi,
    StudentClassmatesApi,
    StudentApi,
    StudentDashboardApi,
    StudentAnalyticsApi,
    UpdateStudentInformationApi
)

urlpatterns = [
    path('', StudentApi.as_view()),
    path('update/', UpdateStudentInformationApi.as_view()),
    path('calendar/', StudentCalendarApi.as_view()),
    path('classmates/', StudentClassmatesApi.as_view()),
    path('dashboard/', StudentDashboardApi.as_view()),
    path('analytics/', StudentAnalyticsApi.as_view())
]

